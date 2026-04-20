"""Bounded current-candidate carry-forward after session transition (PX2-M03 slice 10).

Builds on :func:`run_bounded_operator_local_session_with_transition` (slice 9), then seals a
session-level pointer to the checkpoint / weight lineage the next bounded run should treat as
current — **not** global best-policy semantics; **not** **PX2-M04** exploit closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final, cast

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE10
from starlab.sc2.px2.self_play.current_candidate_record import (
    CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB,
    build_px2_self_play_current_candidate_artifacts,
)
from starlab.sc2.px2.self_play.operator_local_session_transition import (
    TransitionKind,
    run_bounded_operator_local_session_with_transition,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

DEFAULT_SLICE10_CAMPAIGN_ID: Final[str] = "px2_m03_slice10_current_candidate_carry_forward"
SLICE10_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice10_current_candidate_carry_forward_v1"

CURRENT_CANDIDATE_JSON: Final[str] = "px2_self_play_current_candidate.json"


def _load_continuity(root: Path, run_id: str) -> dict[str, Any]:
    p = root / "runs" / run_id / "px2_self_play_campaign_continuity.json"
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def load_px2_self_play_current_candidate(campaign_root: Path) -> dict[str, Any] | None:
    """Load ``px2_self_play_current_candidate.json`` if present."""

    p = campaign_root / CURRENT_CANDIDATE_JSON
    if not p.is_file():
        return None
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def next_run_preflight_hints_from_current_candidate(campaign_root: Path) -> dict[str, Any] | None:
    """Stable, next-run-readable hints for preflight / bounded execution (no filesystem writes).

    Returns ``None`` if no current-candidate artifact exists. Does **not** substitute for
    operator judgment or industrial campaign semantics.
    """

    cc = load_px2_self_play_current_candidate(campaign_root)
    if cc is None:
        return None
    anchor = cc.get("anchor")
    if not isinstance(anchor, dict):
        return None
    w = cc.get("weight_mode_declared_hint")
    init_only = w == WEIGHT_MODE_INIT_ONLY
    return {
        "current_candidate_sha256": str(cc.get("current_candidate_sha256", "")),
        "operator_local_session_transition_sha256": str(
            cc.get("operator_local_session_transition_sha256", "")
        ),
        "weight_mode_declared_hint": str(w) if w is not None else WEIGHT_MODE_INIT_ONLY,
        "init_only_recommended": bool(init_only),
        "anchor_continuity_run_id": str(anchor.get("continuity_run_id", "")),
        "anchor_continuity_step_index_zero_based": int(
            anchor.get("continuity_step_index_zero_based", 0)
        ),
        "checkpoint_receipt_sha256": str(anchor.get("checkpoint_receipt_sha256", "")),
        "checkpoint_relative_path": str(anchor.get("checkpoint_relative_path", "")),
        "continuity_sha256": str(anchor.get("continuity_sha256", "")),
        "weight_identity": cc.get("weight_identity"),
        "weight_bundle_ref": cc.get("weight_bundle_ref"),
        "source_receipt_lineage": cc.get("source_receipt_lineage"),
        "non_claims": cc.get("non_claims"),
    }


def _build_anchor_and_lineage(
    *,
    root: Path,
    transition_tm: dict[str, Any],
    transition_kind: TransitionKind,
) -> tuple[dict[str, Any], dict[str, Any], str | None, dict[str, Any]]:
    lineage_in = transition_tm.get("source_receipt_lineage")
    if not isinstance(lineage_in, dict):
        msg = "transition manifest missing source_receipt_lineage"
        raise RuntimeError(msg)
    current_rid = str(transition_tm.get("current_run_id_after_transition", ""))

    if transition_kind == "promotion":
        rid = str(lineage_in.get("last_run_id", ""))
        cont = _load_continuity(root, rid)
        sr = cont["step_records"]
        if not isinstance(sr, list) or not sr:
            raise RuntimeError("expected step_records on continuity run (promotion)")
        last = sr[-1]
        step_idx = int(last["continuity_step_index_zero_based"])
        anchor = {
            "interpretation": (
                "Carry forward last run's final checkpoint as current candidate pointer — "
                "not strength certification; not exploit closure."
            ),
            "continuity_run_id": rid,
            "continuity_step_index_zero_based": step_idx,
            "checkpoint_receipt_sha256": str(last["checkpoint_receipt_sha256"]),
            "checkpoint_relative_path": str(last["checkpoint_relative_path"]),
            "continuity_sha256": str(cont["continuity_sha256"]),
        }
    else:
        rid = str(lineage_in.get("first_run_id", ""))
        cont = _load_continuity(root, rid)
        sr = cont["step_records"]
        if not isinstance(sr, list) or not sr:
            raise RuntimeError("expected step_records on continuity run (rollback)")
        first = sr[0]
        step_idx = int(first["continuity_step_index_zero_based"])
        anchor = {
            "interpretation": (
                "Carry forward first run's baseline checkpoint after rollback stub — "
                "not PX2-M04 resolution; not industrial promotion."
            ),
            "continuity_run_id": rid,
            "continuity_step_index_zero_based": step_idx,
            "checkpoint_receipt_sha256": str(first["checkpoint_receipt_sha256"]),
            "checkpoint_relative_path": str(first["checkpoint_relative_path"]),
            "continuity_sha256": str(cont["continuity_sha256"]),
        }

    weight_identity = cont.get("weight_identity")
    if not isinstance(weight_identity, dict):
        msg = "continuity missing weight_identity"
        raise RuntimeError(msg)
    wb = cont.get("weight_bundle_ref")
    weight_bundle_ref_val = str(wb).strip() if wb else None

    lineage_out = {
        "transition_interpretation": lineage_in.get("interpretation"),
        "session_current_run_id_after_transition": current_rid,
        "anchor_matches_transition_rule": True,
        "prior_transition_checkpoint_receipt_sha256": str(anchor["checkpoint_receipt_sha256"]),
    }
    return anchor, weight_identity, weight_bundle_ref_val, lineage_out


def run_bounded_operator_local_session_transition_with_current_candidate(
    *,
    corpus_root: Path,
    transition_kind: TransitionKind,
    campaign_id: str = DEFAULT_SLICE10_CAMPAIGN_ID,
    base_dir: Path | None = None,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    run_ids: list[str] | None = None,
    run_count: int = 2,
    torch_seed: int = 42,
    run_torch_seeds: list[int] | None = None,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """Slice 9 transition plus slice-10 sealed current-candidate carry-forward."""

    base = run_bounded_operator_local_session_with_transition(
        corpus_root=corpus_root,
        transition_kind=transition_kind,
        campaign_id=campaign_id,
        base_dir=base_dir,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        run_ids=run_ids,
        run_count=run_count,
        torch_seed=torch_seed,
        run_torch_seeds=run_torch_seeds,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
    )
    root = Path(base["campaign_root"])
    tm_path = root / "px2_self_play_operator_local_session_transition.json"
    transition_tm = cast(dict[str, Any], json.loads(tm_path.read_text(encoding="utf-8")))
    sess_path = root / "px2_self_play_operator_local_session.json"
    sess = cast(dict[str, Any], json.loads(sess_path.read_text(encoding="utf-8")))
    session_sha = str(sess["operator_local_session_sha256"])
    trans_sha = str(transition_tm["operator_local_session_transition_sha256"])
    man_sha = str(base["campaign_root_manifest_sha256"])
    cc_sha = str(base["campaign_contract_sha256"])
    opp_sha = str(base["opponent_pool_identity_sha256"])
    current_rid = str(base["current_run_id_after_transition"])

    anchor, weight_identity, weight_bundle_ref_val, lineage_bind = _build_anchor_and_lineage(
        root=root,
        transition_tm=transition_tm,
        transition_kind=transition_kind,
    )

    weight_hint = WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE
    source_lineage = {
        **lineage_bind,
        "bounded_session_transition_lineage": transition_tm.get("source_receipt_lineage"),
    }
    non_claims = [
        "Slice-10 current-candidate pointer only — not industrial self-play execution.",
        "Deterministic stub carry-forward — not PX2-M04 exploit closure; not ladder strength.",
        "Not merge-gate default CI proof; not 'best policy' in any global sense.",
    ]
    cm, cr = build_px2_self_play_current_candidate_artifacts(
        execution_kind=EXECUTION_KIND_SLICE10,
        campaign_id=campaign_id,
        campaign_profile_id=SLICE10_CAMPAIGN_PROFILE_ID,
        campaign_root_resolved=root,
        operator_local_session_sha256=session_sha,
        operator_local_session_transition_sha256=trans_sha,
        campaign_contract_sha256=cc_sha,
        opponent_pool_identity_sha256=opp_sha,
        campaign_root_manifest_sha256=man_sha,
        current_candidate_rule_id=CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB,
        current_run_id_after_transition=current_rid,
        anchor=anchor,
        weight_identity=dict(weight_identity),
        weight_bundle_ref=weight_bundle_ref_val,
        weight_mode_declared_hint=weight_hint,
        source_receipt_lineage=source_lineage,
        non_claims=non_claims,
    )
    write_json(root / "px2_self_play_current_candidate.json", cm)
    write_json(root / "px2_self_play_current_candidate_report.json", cr)

    return {
        **base,
        "current_candidate_sha256": cm["current_candidate_sha256"],
        "current_candidate_rule_id": CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB,
        "weight_mode_declared_hint": weight_hint,
    }
