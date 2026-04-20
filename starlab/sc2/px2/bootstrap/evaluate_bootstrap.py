"""Held-out eval, trivial baselines, legality-aware decode, compile stats (PX2-M02)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

import torch

from starlab.sc2.px2 import GameStateSnapshot, TerranAction, compile_terran_action, legality_for
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim, pad_or_trunc
from starlab.sc2.px2.bootstrap.game_state_presets import snapshot_dict_to_dataclass_kwargs
from starlab.sc2.px2.bootstrap.policy_model import (
    ACTION_INDEX_BY_ID,
    PRODUCER_KEYS,
    BootstrapTerranPolicy,
    features_tensor_from_observation,
)
from starlab.sc2.px2.terran_action_schema import family_for_action


@dataclass(frozen=True, slots=True)
class EvalReport:
    metrics: dict[str, float | int]
    rows: list[dict[str, Any]]


def _state_from_snapshot(d: dict[str, Any]) -> GameStateSnapshot:
    return GameStateSnapshot(**snapshot_dict_to_dataclass_kwargs(d))


def materialize_arguments(
    action_id: str,
    out: dict[str, torch.Tensor],
    batch_index: int,
) -> dict[str, Any]:
    """Build argument dict from auxiliary heads (argmax)."""

    def _row(t: torch.Tensor) -> torch.Tensor:
        return t[batch_index] if t.dim() > 1 else t

    bs = int(_row(out["build_slot_logits"]).argmax().item())
    es = int(_row(out["expansion_slot_logits"]).argmax().item())
    rs = int(_row(out["region_slot_logits"]).argmax().item())
    pi = int(_row(out["producer_logits"]).argmax().item())
    producer_key = PRODUCER_KEYS[pi] if pi < len(PRODUCER_KEYS) else PRODUCER_KEYS[0]

    if action_id in {
        "build_supply_depot",
        "build_barracks",
        "build_factory",
        "build_starport",
        "build_engineering_bay",
    }:
        return {"build_slot": bs}
    if action_id == "build_refinery":
        return {"expansion_slot": es}
    if action_id == "expand_command_center":
        return {"expansion_slot": es}
    if action_id in {
        "train_marine",
        "train_marauder",
        "train_siege_tank",
        "train_medivac",
        "train_viking",
        "produce_scv",
    }:
        return {"producer_key": producer_key}
    if action_id in {"scout_to_region", "recheck_last_seen_region"}:
        return {"region_slot": rs}
    if action_id in {
        "army_move_region",
        "army_attack_move_region",
        "army_regroup_region",
        "army_retreat_region",
    }:
        return {"region_slot": rs}
    if action_id == "cleanup_search_region":
        return {"region_slot": rs, "target_handle_kind": "structure_class"}
    if action_id in {
        "dispatch_worker_scout",
        "rebalance_workers",
        "set_rally_point",
        "idle_worker_recall",
    }:
        return {"target_key": "main"}
    if action_id == "dispatch_unit_scout":
        return {"unit_role": "marine", "target_key": "map"}
    if action_id in {"tank_siege", "tank_unsiege"}:
        return {"unit_batch_id": "tanks_1"}
    if action_id in {"stim_units_hook", "orbital_scan_hook"}:
        return {"hook_target": "bio_1"}
    if action_id == "morph_orbital_command":
        return {"command_center_key": "cc_main"}
    if action_id in {"add_tech_lab", "add_reactor"}:
        return {"target_structure": "barracks"}
    return {}


def decode_legality_aware(
    model: BootstrapTerranPolicy,
    features: torch.Tensor,
    state: GameStateSnapshot,
    *,
    max_try: int = 32,
) -> TerranAction | None:
    """Pick highest-probability legal action under ``legality_for`` (+ valid args)."""

    model.eval()
    with torch.no_grad():
        out = model(features if features.dim() > 1 else features.unsqueeze(0))
        logits = out["action_logits"][0]
        order = torch.argsort(logits, descending=True).tolist()
        for j in order[:max_try]:
            aid = ACTION_INDEX_BY_ID[int(j)]
            args = materialize_arguments(aid, out, 0)
            try:
                ta = TerranAction(action_id=aid, arguments=args)
            except ValueError:
                continue
            if legality_for(state, ta).legal:
                return ta
    return None


def evaluate_examples(
    model: BootstrapTerranPolicy,
    examples: list[dict[str, Any]],
    *,
    device: torch.device | None = None,
) -> EvalReport:
    """Compute accuracy, family accuracy, compile success, trivial baselines."""

    dev = device or torch.device("cpu")
    model.to(dev)

    fam_correct = 0
    exact_correct = 0
    raw_argmax_correct = 0
    compile_ok = 0
    n = len(examples)
    if n == 0:
        return EvalReport({"n": 0}, [])

    action_counts = Counter(str(ex["label"]["action_id"]) for ex in examples)
    majority_action = action_counts.most_common(1)[0][0]
    fam_counts: Counter[str] = Counter()
    for ex in examples:
        aid = str(ex["label"]["action_id"])
        fam_counts[family_for_action(aid).value] += 1
    majority_family = fam_counts.most_common(1)[0][0]

    maj_action_hits = sum(1 for ex in examples if str(ex["label"]["action_id"]) == majority_action)
    maj_fam_hits = sum(
        1
        for ex in examples
        if family_for_action(str(ex["label"]["action_id"])).value == majority_family
    )

    rows: list[dict[str, Any]] = []
    for ex in examples:
        fv = ex.get("feature_vector")
        if isinstance(fv, list) and fv:
            feat = pad_or_trunc(
                torch.tensor(fv, dtype=torch.float32), observation_feature_dim()
            ).to(dev)
        else:
            obs = ex.get("observation_surface")
            obs = obs if isinstance(obs, dict) else {}
            feat = features_tensor_from_observation(obs).to(dev)
        state = _state_from_snapshot(ex["game_state_snapshot"])
        true_id = str(ex["label"]["action_id"])
        true_fam = family_for_action(true_id).value

        model.eval()
        with torch.no_grad():
            out = model(feat if feat.dim() > 1 else feat.unsqueeze(0))
            raw_id = ACTION_INDEX_BY_ID[int(out["action_logits"][0].argmax().item())]
        if raw_id == true_id:
            raw_argmax_correct += 1

        pred = decode_legality_aware(model, feat, state)
        pred_id = pred.action_id if pred is not None else "__illegal__"
        pred_fam = family_for_action(pred_id).value if pred is not None else "__none__"

        if pred_id == true_id:
            exact_correct += 1
        if pred_fam == true_fam:
            fam_correct += 1

        compiled = False
        if pred is not None:
            try:
                compile_terran_action(pred, state)
                compiled = True
                compile_ok += 1
            except ValueError:
                compiled = False

        rows.append(
            {
                "example_id": ex.get("example_id"),
                "true_action_id": true_id,
                "pred_action_id": pred_id,
                "compile_ok": compiled,
            },
        )

    return EvalReport(
        metrics={
            "n": n,
            "accuracy_action_argmax_raw": raw_argmax_correct / n,
            "accuracy_action_exact_after_legality_decode": exact_correct / n,
            "accuracy_family": fam_correct / n,
            "compile_success_rate": compile_ok / n,
            "baseline_majority_action_acc": maj_action_hits / n,
            "baseline_majority_family_acc": maj_fam_hits / n,
        },
        rows=rows,
    )
