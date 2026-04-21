"""Bounded post-continuation current-candidate re-anchoring (PX2-M03 slice 12)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final, cast

from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE12
from starlab.sc2.px2.self_play.continuation_run import CONTINUATION_RUN_JSON
from starlab.sc2.px2.self_play.current_candidate import (
    CURRENT_CANDIDATE_JSON,
    load_px2_self_play_current_candidate,
)
from starlab.sc2.px2.self_play.current_candidate_reanchor_record import (
    REANCHOR_RULE_POST_CONTINUATION_STUB,
    build_px2_self_play_current_candidate_reanchor_artifacts,
)
from starlab.sc2.px2.self_play.current_candidate_record import (
    CURRENT_CANDIDATE_RECORD_VERSION_SLICE12,
    CURRENT_CANDIDATE_RULE_REANCHOR_FROM_CONTINUATION_STUB,
    build_px2_self_play_current_candidate_artifacts,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json

SLICE12_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice12_current_candidate_reanchor_v1"

CURRENT_CANDIDATE_REANCHOR_JSON: Final[str] = "px2_self_play_current_candidate_reanchor.json"


def _load_continuity_run(campaign_root: Path, run_id: str) -> dict[str, Any]:
    p = campaign_root / "runs" / run_id / "px2_self_play_campaign_continuity.json"
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


def _anchor_from_continuation_run(
    *,
    continuation_run_id: str,
    continuity: dict[str, Any],
) -> dict[str, Any]:
    sr = continuity.get("step_records")
    if not isinstance(sr, list) or not sr:
        msg = "continuation continuity missing step_records"
        raise RuntimeError(msg)
    last = sr[-1]
    step_idx = int(last["continuity_step_index_zero_based"])
    return {
        "interpretation": (
            "Re-anchored to continuation run's final checkpoint — "
            "not industrial campaign; not PX2-M04 exploit closure."
        ),
        "continuity_run_id": continuation_run_id,
        "continuity_step_index_zero_based": step_idx,
        "checkpoint_receipt_sha256": str(last["checkpoint_receipt_sha256"]),
        "checkpoint_relative_path": str(last["checkpoint_relative_path"]),
        "continuity_sha256": str(continuity["continuity_sha256"]),
    }


def run_bounded_current_candidate_reanchor_after_continuation(
    *,
    campaign_root: Path,
    campaign_id: str,
) -> dict[str, Any]:
    """Refresh ``px2_self_play_current_candidate.json`` after ``consumed_ok`` slice-11 continuation.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    root = campaign_root.resolve()
    cont_path = root / CONTINUATION_RUN_JSON
    base_non_claims = [
        "Slice-12 post-continuation current-candidate re-anchor — not industrial execution.",
        "Pointer refresh only; not ladder strength; not PX2-M04 exploit closure.",
        "Not merge-gate default CI proof.",
    ]

    def _emit_reanchor_only(
        *,
        prior_cc_sha: str,
        prior_cont_sha: str,
        continuation_run_id: str,
        refreshed_sha: str | None,
        consumption_observed: str,
        status: str,
        reasons: list[str],
        contract_sha: str,
        opp_sha: str,
        man_sha: str,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return build_px2_self_play_current_candidate_reanchor_artifacts(
            execution_kind=EXECUTION_KIND_SLICE12,
            campaign_id=campaign_id,
            campaign_profile_id=SLICE12_CAMPAIGN_PROFILE_ID,
            campaign_root_resolved=root,
            reanchor_rule_id=REANCHOR_RULE_POST_CONTINUATION_STUB,
            prior_current_candidate_sha256=prior_cc_sha,
            prior_continuation_run_sha256=prior_cont_sha,
            continuation_run_id=continuation_run_id,
            refreshed_current_candidate_sha256=refreshed_sha,
            campaign_contract_sha256=contract_sha,
            opponent_pool_identity_sha256=opp_sha,
            campaign_root_manifest_sha256=man_sha,
            continuation_consumption_status_observed=consumption_observed,
            reanchor_status=status,
            rejection_reasons=reasons,
            non_claims=base_non_claims,
        )

    if not cont_path.is_file():
        man_path = root / "px2_self_play_campaign_root_manifest.json"
        man_sha = ""
        cc_sha = ""
        opp_sha = ""
        contract_sha = ""
        if man_path.is_file():
            man = cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8")))
            man_sha = str(man.get("campaign_root_manifest_sha256", ""))
            opp_sha = str(man.get("opponent_pool_identity_sha256", ""))
            contract_sha = str(man.get("campaign_contract_sha256", ""))
        cc0 = load_px2_self_play_current_candidate(root)
        if cc0 is not None:
            cc_sha = str(cc0.get("current_candidate_sha256", ""))
        rm, rr = _emit_reanchor_only(
            prior_cc_sha=cc_sha,
            prior_cont_sha="",
            continuation_run_id="",
            refreshed_sha=None,
            consumption_observed="missing",
            status="rejected",
            reasons=["missing_px2_self_play_continuation_run_json"],
            contract_sha=contract_sha,
            opp_sha=opp_sha,
            man_sha=man_sha,
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["missing_px2_self_play_continuation_run_json"],
        }

    cont_rec = cast(dict[str, Any], json.loads(cont_path.read_text(encoding="utf-8")))
    prior_cont_sha = str(cont_rec.get("continuation_run_sha256", ""))
    consumption = str(cont_rec.get("consumption_status", ""))
    continuation_run_id = str(cont_rec.get("continuation_run_id", ""))

    man_path = root / "px2_self_play_campaign_root_manifest.json"
    if not man_path.is_file():
        rm, rr = _emit_reanchor_only(
            prior_cc_sha="",
            prior_cont_sha=prior_cont_sha,
            continuation_run_id=continuation_run_id,
            refreshed_sha=None,
            consumption_observed=consumption,
            status="rejected",
            reasons=["missing_px2_self_play_campaign_root_manifest_json"],
            contract_sha="",
            opp_sha="",
            man_sha="",
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["missing_px2_self_play_campaign_root_manifest_json"],
        }

    man = cast(dict[str, Any], json.loads(man_path.read_text(encoding="utf-8")))
    man_sha = str(man["campaign_root_manifest_sha256"])
    opp_sha = str(man["opponent_pool_identity_sha256"])
    contract_sha = str(man["campaign_contract_sha256"])

    if str(cont_rec.get("campaign_id", "")) != campaign_id:
        cc0 = load_px2_self_play_current_candidate(root)
        cc_sha = str(cc0.get("current_candidate_sha256", "")) if cc0 else ""
        rm, rr = _emit_reanchor_only(
            prior_cc_sha=cc_sha,
            prior_cont_sha=prior_cont_sha,
            continuation_run_id=continuation_run_id,
            refreshed_sha=None,
            consumption_observed=consumption,
            status="rejected",
            reasons=["continuation_campaign_id_mismatch"],
            contract_sha=contract_sha,
            opp_sha=opp_sha,
            man_sha=man_sha,
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["continuation_campaign_id_mismatch"],
        }

    if consumption != "consumed_ok":
        cc0 = load_px2_self_play_current_candidate(root)
        cc_sha = str(cc0.get("current_candidate_sha256", "")) if cc0 else ""
        rm, rr = _emit_reanchor_only(
            prior_cc_sha=cc_sha,
            prior_cont_sha=prior_cont_sha,
            continuation_run_id=continuation_run_id,
            refreshed_sha=None,
            consumption_observed=consumption,
            status="rejected",
            reasons=["continuation_not_consumed_ok"],
            contract_sha=contract_sha,
            opp_sha=opp_sha,
            man_sha=man_sha,
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["continuation_not_consumed_ok"],
        }

    prior_cc = load_px2_self_play_current_candidate(root)
    if prior_cc is None:
        rm, rr = _emit_reanchor_only(
            prior_cc_sha="",
            prior_cont_sha=prior_cont_sha,
            continuation_run_id=continuation_run_id,
            refreshed_sha=None,
            consumption_observed=consumption,
            status="rejected",
            reasons=["missing_px2_self_play_current_candidate_json"],
            contract_sha=contract_sha,
            opp_sha=opp_sha,
            man_sha=man_sha,
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["missing_px2_self_play_current_candidate_json"],
        }

    prior_cc_sha = str(prior_cc.get("current_candidate_sha256", ""))
    if not continuation_run_id:
        rm, rr = _emit_reanchor_only(
            prior_cc_sha=prior_cc_sha,
            prior_cont_sha=prior_cont_sha,
            continuation_run_id="",
            refreshed_sha=None,
            consumption_observed=consumption,
            status="rejected",
            reasons=["missing_continuation_run_id"],
            contract_sha=contract_sha,
            opp_sha=opp_sha,
            man_sha=man_sha,
        )
        write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
        write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)
        return {
            "campaign_root": str(root),
            "reanchor_status": "rejected",
            "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
            "refreshed_current_candidate_sha256": None,
            "rejection_reasons": ["missing_continuation_run_id"],
        }

    continuity = _load_continuity_run(root, continuation_run_id)
    anchor = _anchor_from_continuation_run(
        continuation_run_id=continuation_run_id,
        continuity=continuity,
    )
    weight_identity = continuity.get("weight_identity")
    if not isinstance(weight_identity, dict):
        msg = "continuation missing weight_identity"
        raise RuntimeError(msg)
    wb = continuity.get("weight_bundle_ref")
    weight_bundle_ref_val = str(wb).strip() if wb else None

    sess_sha = str(prior_cc.get("operator_local_session_sha256", ""))
    trans_sha = str(prior_cc.get("operator_local_session_transition_sha256", ""))
    weight_hint = str(prior_cc.get("weight_mode_declared_hint", ""))

    lineage = {
        "reanchor_interpretation": (
            "Post-continuation pointer refresh — prior candidate and continuation seals bound "
            "in this lineage block."
        ),
        "prior_current_candidate_sha256": prior_cc_sha,
        "prior_continuation_run_sha256": prior_cont_sha,
        "continuation_run_id": continuation_run_id,
        "prior_rule_id": str(prior_cc.get("current_candidate_rule_id", "")),
    }

    cc_non_claims = [
        "Slice-12 refreshed current-candidate pointer — not industrial execution.",
        "Not global best policy; not PX2-M04 exploit closure.",
        "Not merge-gate default CI proof.",
    ]

    cm, cr = build_px2_self_play_current_candidate_artifacts(
        execution_kind=EXECUTION_KIND_SLICE12,
        campaign_id=campaign_id,
        campaign_profile_id=SLICE12_CAMPAIGN_PROFILE_ID,
        campaign_root_resolved=root,
        operator_local_session_sha256=sess_sha,
        operator_local_session_transition_sha256=trans_sha,
        campaign_contract_sha256=contract_sha,
        opponent_pool_identity_sha256=opp_sha,
        campaign_root_manifest_sha256=man_sha,
        current_candidate_rule_id=CURRENT_CANDIDATE_RULE_REANCHOR_FROM_CONTINUATION_STUB,
        current_run_id_after_transition=continuation_run_id,
        anchor=anchor,
        weight_identity=dict(weight_identity),
        weight_bundle_ref=weight_bundle_ref_val,
        weight_mode_declared_hint=weight_hint,
        source_receipt_lineage=lineage,
        non_claims=cc_non_claims,
        record_version=CURRENT_CANDIDATE_RECORD_VERSION_SLICE12,
    )
    write_json(root / CURRENT_CANDIDATE_JSON, cm)
    write_json(root / "px2_self_play_current_candidate_report.json", cr)

    refreshed_sha = str(cm["current_candidate_sha256"])
    rm, rr = _emit_reanchor_only(
        prior_cc_sha=prior_cc_sha,
        prior_cont_sha=prior_cont_sha,
        continuation_run_id=continuation_run_id,
        refreshed_sha=refreshed_sha,
        consumption_observed=consumption,
        status="reanchored_ok",
        reasons=[],
        contract_sha=contract_sha,
        opp_sha=opp_sha,
        man_sha=man_sha,
    )
    write_json(root / CURRENT_CANDIDATE_REANCHOR_JSON, rm)
    write_json(root / "px2_self_play_current_candidate_reanchor_report.json", rr)

    return {
        "campaign_root": str(root),
        "reanchor_status": "reanchored_ok",
        "current_candidate_reanchor_sha256": rm["current_candidate_reanchor_sha256"],
        "refreshed_current_candidate_sha256": refreshed_sha,
        "prior_current_candidate_sha256": prior_cc_sha,
        "prior_continuation_run_sha256": prior_cont_sha,
        "continuation_run_id": continuation_run_id,
    }
