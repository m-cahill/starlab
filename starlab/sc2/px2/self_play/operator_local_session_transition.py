"""Bounded operator-local session + governed promotion/rollback step (PX2-M03 slice 9).

Builds on :func:`run_bounded_operator_local_session` (slice 8), then records one deterministic
session-level transition bound to existing per-run receipt lineage.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final, Literal, cast

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE9
from starlab.sc2.px2.self_play.operator_local_session import run_bounded_operator_local_session
from starlab.sc2.px2.self_play.operator_local_session_transition_record import (
    TRANSITION_RULE_PROMOTION_LAST_RUN,
    TRANSITION_RULE_ROLLBACK_FIRST_RUN_BASELINE,
    build_px2_self_play_operator_local_session_transition_artifacts,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

DEFAULT_SLICE9_CAMPAIGN_ID: Final[str] = "px2_m03_slice9_bounded_session_transition"
SLICE9_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice9_bounded_session_transition_v1"

TransitionKind = Literal["promotion", "rollback"]


def _load_continuity(root: Path, run_id: str) -> dict[str, Any]:
    p = root / "runs" / run_id / "px2_self_play_campaign_continuity.json"
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def run_bounded_operator_local_session_with_transition(
    *,
    corpus_root: Path,
    transition_kind: TransitionKind,
    campaign_id: str = DEFAULT_SLICE9_CAMPAIGN_ID,
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
    """Slice-8 multi-run session plus one sealed session-level transition record.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    base = run_bounded_operator_local_session(
        corpus_root=corpus_root,
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
    ordered = list(base["ordered_run_ids"])
    if len(ordered) < 2:
        msg = "session transition requires at least two runs"
        raise RuntimeError(msg)

    sess_path = root / "px2_self_play_operator_local_session.json"
    sess = json.loads(sess_path.read_text(encoding="utf-8"))
    session_sha = str(sess["operator_local_session_sha256"])
    man_sha = str(base["campaign_root_manifest_sha256"])
    cc_sha = str(base["campaign_contract_sha256"])
    opp_sha = str(base["opponent_pool_identity_sha256"])
    rids = tuple(ordered)
    first_id, last_id = ordered[0], ordered[-1]
    cont_first = _load_continuity(root, first_id)
    cont_last = _load_continuity(root, last_id)
    sr_first = cont_first["step_records"]
    sr_last = cont_last["step_records"]
    if not isinstance(sr_first, list) or not sr_first:
        msg = "expected step_records on first run"
        raise RuntimeError(msg)
    if not isinstance(sr_last, list) or not sr_last:
        msg = "expected step_records on last run"
        raise RuntimeError(msg)
    first0 = sr_first[0]
    last_fin = sr_last[-1]

    if transition_kind == "promotion":
        rule = TRANSITION_RULE_PROMOTION_LAST_RUN
        current = last_id
        lineage: dict[str, Any] = {
            "interpretation": (
                "Stub: promote to last run's final promotion receipt — not strength proof; "
                "not exploit closure."
            ),
            "last_run_id": last_id,
            "last_run_continuity_sha256": str(cont_last["continuity_sha256"]),
            "final_step_index_zero_based": int(last_fin["continuity_step_index_zero_based"]),
            "checkpoint_receipt_sha256": str(last_fin["checkpoint_receipt_sha256"]),
            "evaluation_receipt_sha256": str(last_fin["evaluation_receipt_sha256"]),
            "promotion_receipt_sha256": str(last_fin["promotion_receipt_sha256"]),
            "rollback_receipt_sha256": str(last_fin["rollback_receipt_sha256"]),
        }
    else:
        rule = TRANSITION_RULE_ROLLBACK_FIRST_RUN_BASELINE
        current = first_id
        lineage = {
            "interpretation": (
                "Stub: rollback current candidate to first run's first checkpoint — "
                "not exploit resolution; not PX2-M04."
            ),
            "first_run_id": first_id,
            "first_run_continuity_sha256": str(cont_first["continuity_sha256"]),
            "last_run_id": last_id,
            "last_run_continuity_sha256": str(cont_last["continuity_sha256"]),
            "baseline_step_index_zero_based": int(first0["continuity_step_index_zero_based"]),
            "baseline_checkpoint_receipt_sha256": str(first0["checkpoint_receipt_sha256"]),
            "reference_last_run_final_rollback_receipt_sha256": str(
                last_fin["rollback_receipt_sha256"]
            ),
        }

    non_claims = [
        "Slice-9 bounded session-level promotion/rollback step — not industrial self-play.",
        "Deterministic stub rule only — not PX2-M04 exploit closure; not ranking semantics.",
        "Not Blackwell-scale; not ladder strength; not merge-gate default CI proof.",
    ]
    tm, tr = build_px2_self_play_operator_local_session_transition_artifacts(
        execution_kind=EXECUTION_KIND_SLICE9,
        campaign_id=campaign_id,
        campaign_profile_id=SLICE9_CAMPAIGN_PROFILE_ID,
        campaign_root_resolved=root,
        operator_local_session_sha256=session_sha,
        campaign_contract_sha256=cc_sha,
        opponent_pool_identity_sha256=opp_sha,
        campaign_root_manifest_sha256=man_sha,
        ordered_run_ids=rids,
        transition_type=transition_kind,
        transition_rule_id=rule,
        current_run_id_after_transition=current,
        source_receipt_lineage=lineage,
        non_claims=non_claims,
    )
    write_json(root / "px2_self_play_operator_local_session_transition.json", tm)
    write_json(root / "px2_self_play_operator_local_session_transition_report.json", tr)

    return {
        **base,
        "transition_kind": transition_kind,
        "transition_rule_id": rule,
        "current_run_id_after_transition": current,
        "operator_local_session_transition_sha256": tm["operator_local_session_transition_sha256"],
        "weight_mode_declared": (WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE),
    }
