"""Bounded multi-step operator-local continuity (PX2-M03 slice 4)."""

from __future__ import annotations

import random
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Any, Final

import torch

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.dataset_contract import load_examples_from_dataset_file
from starlab.sc2.px2.bootstrap.emit_replay_bootstrap_dataset import emit_from_corpus
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
)
from starlab.sc2.px2.self_play.checkpoint_receipts import build_slice4_checkpoint_receipt_artifacts
from starlab.sc2.px2.self_play.evaluation_receipts import build_slice4_evaluation_receipt_artifacts
from starlab.sc2.px2.self_play.execution_preflight import run_execution_preflight
from starlab.sc2.px2.self_play.opponent_rotation import build_opponent_rotation_trace
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.promotion_receipts import (
    build_promotion_receipt_artifacts,
    slice4_stub_promotion_decision,
)
from starlab.sc2.px2.self_play.rollback_receipts import build_rollback_receipt_artifacts
from starlab.sc2.px2.self_play.run_artifacts import (
    build_slice4_continuity_manifest,
    default_operator_local_slice4_subdirs,
    ensure_operator_local_slice4_layout,
    write_json,
)
from starlab.sc2.px2.self_play.snapshot_pool import (
    OpponentPoolStub,
    build_default_opponent_pool_stub,
    opponent_pool_identity_sha256,
)
from starlab.sc2.px2.self_play.weight_loading import build_policy_operator_local

PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_continuity.v1"
)
PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_continuity_report.v1"
)

EXECUTION_KIND_SLICE4: Final[str] = "px2_m03_slice4_operator_local_continuity_v1"
EXECUTION_KIND_SLICE5: Final[str] = "px2_m03_slice5_operator_local_campaign_root_v1"
EXECUTION_KIND_SLICE6: Final[str] = "px2_m03_slice6_canonical_operator_local_campaign_root_smoke_v1"
EXECUTION_KIND_SLICE7: Final[str] = "px2_m03_slice7_bounded_operator_local_real_run_v1"
EXECUTION_KIND_SLICE8: Final[str] = "px2_m03_slice8_bounded_operator_local_session_v1"
EXECUTION_KIND_SLICE9: Final[str] = "px2_m03_slice9_bounded_operator_local_session_transition_v1"
EXECUTION_KIND_SLICE10: Final[str] = "px2_m03_slice10_bounded_current_candidate_carry_forward_v1"
EXECUTION_KIND_SLICE11: Final[str] = (
    "px2_m03_slice11_bounded_continuation_run_consuming_candidate_v1"
)


def _seal_continuity_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def run_operator_local_campaign_continuity(
    *,
    corpus_root: Path,
    output_dir: Path,
    init_only: bool,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    campaign_id: str = "px2_m03_slice4_operator_local",
    campaign_profile_id: str = "px2_m03_slice4_continuity_v1",
    torch_seed: int = 42,
    run_id: str | None = None,
    continuity_step_count: int = 3,
    device_intent: str = "cpu",
    map_location: str = "cpu",
    opponent_pool: OpponentPoolStub | None = None,
    opponent_selection_rule_id: str = OPPONENT_SELECTION_ROUND_ROBIN,
    opponent_selection_weights: tuple[int, ...] | None = None,
    opponent_rotation_ref_ids: tuple[str, ...] | None = None,
    execution_kind: str = EXECUTION_KIND_SLICE4,
) -> dict[str, Any]:
    """Multi-step continuity proof: preflight → N bounded steps with sealed receipt chain.

    ``continuity_step_count`` is clamped to ``[2, 3]`` for non-industrial bounds.
    """

    random.seed(torch_seed)
    torch.manual_seed(torch_seed)

    n_steps = max(2, min(int(continuity_step_count), 3))
    rid = run_id or f"px2_cont_{uuid.uuid4().hex[:12]}"

    ok, preflight, preflight_report, errors = run_execution_preflight(
        corpus_root=corpus_root,
        output_dir=output_dir,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        torch_seed=torch_seed,
        run_id=rid,
        device_intent=device_intent,
        map_location=map_location,
    )

    out = output_dir.resolve()
    write_json(out / "px2_self_play_execution_preflight.json", preflight)
    write_json(out / "px2_self_play_execution_preflight_report.json", preflight_report)

    if not ok:
        msg = "execution preflight failed: " + "; ".join(errors)
        raise ValueError(msg)

    layout_paths = ensure_operator_local_slice4_layout(out)
    sub = default_operator_local_slice4_subdirs()

    model, weight_meta = build_policy_operator_local(
        init_only=init_only,
        weights_path=weights_path,
        torch_seed=torch_seed,
        map_location=map_location,
    )

    pool = (
        opponent_pool
        if opponent_pool is not None
        else build_default_opponent_pool_stub(campaign_tag="slice4")
    )
    ref_ids = (
        opponent_rotation_ref_ids
        if opponent_rotation_ref_ids is not None
        else tuple(r.ref_id for r in pool.snapshot_refs)
    )
    if opponent_selection_rule_id == OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB:
        if opponent_selection_weights is None:
            msg = "opponent_selection_weights required for weighted_frozen_stub"
            raise ValueError(msg)
    elif opponent_selection_weights is not None:
        msg = "opponent_selection_weights only valid for weighted_frozen_stub"
        raise ValueError(msg)

    campaign, _cr = build_px2_self_play_campaign_artifacts(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        opponent_pool=pool,
        opponent_selection_rule_id=opponent_selection_rule_id,
        torch_seed=torch_seed,
    )
    campaign_sha = str(campaign["campaign_sha256"])

    tmp_emit = Path(tempfile.mkdtemp(prefix="px2_m03_cont_dataset_"))
    try:
        emit_from_corpus(corpus_root, tmp_emit)
        examples = load_examples_from_dataset_file(tmp_emit / "px2_replay_bootstrap_dataset.json")
    finally:
        shutil.rmtree(tmp_emit, ignore_errors=True)

    if len(examples) < 1:
        msg = "corpus must yield at least one labeled example"
        raise ValueError(msg)

    prior_ck: str | None = None
    prior_ev: str | None = None
    prior_promo: str | None = None
    step_records: list[dict[str, Any]] = []
    episodes_out: list[dict[str, Any]] = []
    continuity_chain: list[dict[str, str]] = []

    pf_sha = str(preflight["preflight_sha256"])

    for step in range(n_steps):
        ex = examples[step % len(examples)]
        obs = ex["observation_surface"]
        gss = ex["game_state_snapshot"]
        opponent_ref = select_opponent_ref(
            step_index=step,
            rule_id=opponent_selection_rule_id,
            ref_ids=ref_ids,
            weights=opponent_selection_weights,
        )
        rot_trace = build_opponent_rotation_trace(
            step_index=step,
            rule_id=opponent_selection_rule_id,
            ref_ids=ref_ids,
            selected_ref=opponent_ref,
            weights=opponent_selection_weights,
        )
        bridge = bootstrap_policy_runtime_step(model, obs, gss)
        games_done = step + 1
        episodes_out.append(
            {
                "continuity_step_index_zero_based": step,
                "episode_index_one_based": games_done,
                "example_id": ex.get("example_id"),
                "opponent_snapshot_ref": opponent_ref,
                "opponent_rotation_trace": rot_trace,
                "bridge": bridge.to_json_dict(),
            }
        )

        ck_r, ck_rep = build_slice4_checkpoint_receipt_artifacts(
            campaign_id=campaign_id,
            run_id=rid,
            campaign_sha256=campaign_sha,
            linked_campaign_contract_id=PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
            preflight_sha256=pf_sha,
            weight_identity=weight_meta,
            continuity_step_index_zero_based=step,
            episode_index_one_based=games_done,
            games_completed_in_run=games_done,
            policy_snapshot_note=(
                "BootstrapTerranPolicy slice-4 continuity — no weight mutation between steps."
            ),
            prior_checkpoint_receipt_sha256=prior_ck,
            prior_evaluation_receipt_sha256=prior_ev,
        )
        ck_stem = f"ckpt_step{step + 1:03d}"
        ck_json = layout_paths["checkpoints"] / f"{ck_stem}.json"
        ck_rep_json = layout_paths["checkpoints"] / f"{ck_stem}_report.json"
        write_json(ck_json, ck_r)
        write_json(ck_rep_json, ck_rep)
        ck_seal = str(ck_r["checkpoint_receipt_sha256"])

        ev_r, ev_rep = build_slice4_evaluation_receipt_artifacts(
            campaign_id=campaign_id,
            run_id=rid,
            campaign_sha256=campaign_sha,
            linked_campaign_contract_id=PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
            preflight_sha256=pf_sha,
            weight_identity=weight_meta,
            continuity_step_index_zero_based=step,
            episode_index_one_based=games_done,
            games_completed_in_run=games_done,
            link_checkpoint_receipt_sha256=ck_seal,
            eval_modes=["offline_fixture", "slice4_continuity_stub"],
            metrics_stub={
                "continuity_step": step,
                "eval_stub_gate_passed": True,
            },
        )
        ev_stem = f"eval_step{step + 1:03d}"
        ev_json = layout_paths["evaluations"] / f"{ev_stem}.json"
        ev_rep_json = layout_paths["evaluations"] / f"{ev_stem}_report.json"
        write_json(ev_json, ev_r)
        write_json(ev_rep_json, ev_rep)
        ev_seal = str(ev_r["evaluation_receipt_sha256"])

        promo_decision = slice4_stub_promotion_decision(
            step_index_zero_based=step,
            step_count=n_steps,
        )
        pr_r, pr_rep = build_promotion_receipt_artifacts(
            campaign_id=campaign_id,
            run_id=rid,
            campaign_sha256=campaign_sha,
            preflight_sha256=pf_sha,
            weight_identity=weight_meta,
            continuity_step_index_zero_based=step,
            continuity_step_count=n_steps,
            linked_evaluation_receipt_sha256=ev_seal,
            prior_promotion_receipt_sha256=prior_promo,
            decision=promo_decision,
        )
        pr_stem = f"promotion_step{step + 1:03d}"
        pr_json = layout_paths["promotions"] / f"{pr_stem}.json"
        pr_rep_json = layout_paths["promotions"] / f"{pr_stem}_report.json"
        write_json(pr_json, pr_r)
        write_json(pr_rep_json, pr_rep)
        pr_seal = str(pr_r["promotion_receipt_sha256"])

        # Stub path: no automatic revert; "hold" on final step is not a rollback trigger.
        rb_r, rb_rep = build_rollback_receipt_artifacts(
            campaign_id=campaign_id,
            run_id=rid,
            campaign_sha256=campaign_sha,
            preflight_sha256=pf_sha,
            continuity_step_index_zero_based=step,
            linked_promotion_receipt_sha256=pr_seal,
            triggered=False,
            rollback_reason=None,
            would_revert_to_checkpoint_receipt_sha256=None,
        )
        rb_stem = f"rollback_step{step + 1:03d}"
        rb_json = layout_paths["rollbacks"] / f"{rb_stem}.json"
        rb_rep_json = layout_paths["rollbacks"] / f"{rb_stem}_report.json"
        write_json(rb_json, rb_r)
        write_json(rb_rep_json, rb_rep)
        rb_seal = str(rb_r["rollback_receipt_sha256"])

        rec = {
            "continuity_step_index_zero_based": step,
            "checkpoint_receipt_sha256": ck_seal,
            "checkpoint_relative_path": f"{sub['checkpoints']}/{ck_stem}.json",
            "evaluation_receipt_sha256": ev_seal,
            "evaluation_relative_path": f"{sub['evaluations']}/{ev_stem}.json",
            "promotion_receipt_sha256": pr_seal,
            "promotion_relative_path": f"{sub['promotions']}/{pr_stem}.json",
            "rollback_receipt_sha256": rb_seal,
            "rollback_relative_path": f"{sub['rollbacks']}/{rb_stem}.json",
            "promotion_decision": promo_decision,
        }
        step_records.append(rec)
        continuity_chain.append(
            {
                "step": str(step),
                "checkpoint_receipt_sha256": ck_seal,
                "evaluation_receipt_sha256": ev_seal,
                "promotion_receipt_sha256": pr_seal,
                "rollback_receipt_sha256": rb_seal,
            }
        )

        prior_ck = ck_seal
        prior_ev = ev_seal
        prior_promo = pr_seal

    pool_identity = opponent_pool_identity_sha256(pool)
    if execution_kind == EXECUTION_KIND_SLICE6:
        continuity_non_claims = [
            "Slice-6 canonical campaign-root smoke — not industrial self-play campaign.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ]
    elif execution_kind == EXECUTION_KIND_SLICE7:
        continuity_non_claims = [
            "Slice-7 bounded operator-local real run — not industrial self-play campaign.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ]
    elif execution_kind == EXECUTION_KIND_SLICE8:
        continuity_non_claims = [
            "Slice-8 bounded operator-local multi-run session member — not industrial self-play.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ]
    elif execution_kind == EXECUTION_KIND_SLICE11:
        continuity_non_claims = [
            "Slice-11 bounded continuation run — current-candidate consumption; "
            "not industrial self-play.",
            "Not PX2-M04 exploit closure; not Blackwell-scale; not merge-gate default CI proof.",
        ]
    elif execution_kind == EXECUTION_KIND_SLICE5:
        continuity_non_claims = [
            "Slice-5 operator-local campaign-root continuity — not industrial self-play campaign.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ]
    else:
        continuity_non_claims = [
            "Slice-4 bounded multi-step continuity — not industrial self-play campaign.",
            "Not Blackwell-scale; not merge-gate default CI proof.",
        ]

    continuity_body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": rid,
        "campaign_sha256": campaign_sha,
        "linked_campaign_contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "execution_kind": execution_kind,
        "preflight_sha256": pf_sha,
        "torch_seed": torch_seed,
        "continuity_step_count": n_steps,
        "weight_identity": weight_meta,
        "weight_bundle_ref": weight_bundle_ref.strip() if weight_bundle_ref else None,
        "device_intent": device_intent,
        "opponent_pool_identity_sha256": pool_identity,
        "opponent_selection_rule_id": opponent_selection_rule_id,
        "opponent_selection_weights": list(opponent_selection_weights)
        if opponent_selection_weights is not None
        else None,
        "opponent_rotation_ref_ids": list(ref_ids),
        "episodes": episodes_out,
        "step_records": step_records,
        "non_claims": continuity_non_claims,
    }
    continuity_no_seal = {k: v for k, v in continuity_body.items() if k != "continuity_sha256"}
    seal = _seal_continuity_body(continuity_no_seal)
    continuity = dict(continuity_body)
    continuity["continuity_sha256"] = seal

    continuity_report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_REPORT_CONTRACT_ID,
        "continuity_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": rid,
        "summary": {
            "preflight_sha256": pf_sha,
            "continuity_steps": n_steps,
            "final_checkpoint_receipt_sha256": step_records[-1]["checkpoint_receipt_sha256"],
            "opponent_pool_identity_sha256": pool_identity,
        },
        "non_claims": continuity_body["non_claims"],
    }

    chain_body = {
        "chain_version": "starlab.px2.self_play_continuity_chain.v1",
        "run_id": rid,
        "campaign_sha256": campaign_sha,
        "preflight_sha256": pf_sha,
        "ordered_seals": continuity_chain,
    }
    chain_seal = sha256_hex_of_canonical_json(chain_body)
    chain_out = dict(chain_body)
    chain_out["continuity_chain_sha256"] = chain_seal

    if execution_kind == EXECUTION_KIND_SLICE4:
        cnote = "PX2-M02 fixture corpus lineage; slice-4 bounded continuity proof."
    elif execution_kind == EXECUTION_KIND_SLICE6:
        cnote = "PX2-M02 fixture corpus lineage; slice-6 canonical campaign-root smoke proof."
    elif execution_kind == EXECUTION_KIND_SLICE7:
        cnote = "PX2-M02 fixture corpus lineage; slice-7 bounded operator-local real-run proof."
    elif execution_kind == EXECUTION_KIND_SLICE8:
        cnote = "PX2-M02 fixture corpus lineage; slice-8 bounded operator-local session proof."
    else:
        cnote = "PX2-M02 fixture corpus lineage; slice-5 campaign-root continuity proof."

    manifest = build_slice4_continuity_manifest(
        campaign_id=campaign_id,
        run_id=rid,
        campaign_sha256=campaign_sha,
        execution_kind=execution_kind,
        continuity_step_count=n_steps,
        preflight_sha256=pf_sha,
        corpus_note=cnote,
        torch_seed=torch_seed,
        operator_local_layout=sub,
    )

    write_json(out / "px2_self_play_campaign_continuity.json", continuity)
    write_json(out / "px2_self_play_campaign_continuity_report.json", continuity_report)
    write_json(out / "continuity_chain.json", chain_out)
    write_json(out / "run_manifest.json", manifest)

    return {
        "output_dir": str(out),
        "run_id": rid,
        "continuity_sha256": seal,
        "continuity_chain_sha256": chain_seal,
        "preflight_sha256": pf_sha,
        "campaign_sha256": campaign_sha,
        "continuity_step_count": n_steps,
        "weight_identity": weight_meta,
        "step_records": step_records,
    }
