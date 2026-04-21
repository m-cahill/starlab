"""Bounded run seeded from ``px2_self_play_current_candidate.json`` (PX2-M03 slice 14)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE14
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.continuation_run import (
    merge_campaign_root_manifest_after_continuation_run,
    validate_current_candidate_for_continuation_run,
)
from starlab.sc2.px2.self_play.current_candidate import CURRENT_CANDIDATE_JSON
from starlab.sc2.px2.self_play.current_candidate_record import build_current_candidate_seal_basis
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.pointer_seeded_run_record import (
    POINTER_SEEDED_RUN_RULE_SEED_FROM_CURRENT_CANDIDATE_STUB,
    SEED_SEMANTICS_DECLARED_FROM_LATEST_CURRENT_CANDIDATE_V1,
    build_px2_self_play_pointer_seeded_run_artifacts,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

SLICE14_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice14_pointer_seeded_operator_local_run_v1"

POINTER_SEEDED_RUN_JSON: Final[str] = "px2_self_play_pointer_seeded_run.json"
SEEDING_OK: Final[str] = "seeded_ok"
REJECTED_MISSING_POINTER: Final[str] = "rejected_missing_pointer"
REJECTED_MISMATCH: Final[str] = "rejected_mismatch"


def _anchor_snapshot_from_cc(cc: dict[str, Any]) -> dict[str, Any]:
    anchor = cc.get("anchor")
    if not isinstance(anchor, dict):
        return {}
    keys = (
        "continuity_run_id",
        "continuity_step_index_zero_based",
        "checkpoint_receipt_sha256",
        "checkpoint_relative_path",
        "continuity_sha256",
    )
    return {k: anchor.get(k) for k in keys}


def verify_loaded_current_candidate_self_seal(cc: dict[str, Any]) -> tuple[bool, list[str]]:
    """Recompute the current-candidate seal and compare to ``current_candidate_sha256``."""

    try:
        anchor = cc.get("anchor")
        weight_identity = cc.get("weight_identity")
        source_lineage = cc.get("source_receipt_lineage")
        if not isinstance(anchor, dict):
            return False, ["current_candidate_anchor_not_dict"]
        if not isinstance(weight_identity, dict):
            return False, ["current_candidate_weight_identity_not_dict"]
        if not isinstance(source_lineage, dict):
            return False, ["current_candidate_source_receipt_lineage_not_dict"]
        wb = cc.get("weight_bundle_ref")
        wb_out: str | None = str(wb).strip() if wb else None
        nc = cc.get("non_claims")
        if not isinstance(nc, list):
            return False, ["current_candidate_non_claims_not_list"]
        rv = cc.get("current_candidate_record_version")
        basis = build_current_candidate_seal_basis(
            execution_kind=str(cc["execution_kind"]),
            campaign_id=str(cc["campaign_id"]),
            campaign_profile_id=str(cc["campaign_profile_id"]),
            operator_local_session_sha256=str(cc["operator_local_session_sha256"]),
            operator_local_session_transition_sha256=str(
                cc["operator_local_session_transition_sha256"]
            ),
            campaign_contract_sha256=str(cc["campaign_contract_sha256"]),
            opponent_pool_identity_sha256=str(cc["opponent_pool_identity_sha256"]),
            campaign_root_manifest_sha256=str(cc["campaign_root_manifest_sha256"]),
            current_candidate_rule_id=str(cc["current_candidate_rule_id"]),
            current_run_id_after_transition=str(cc["current_run_id_after_transition"]),
            anchor=anchor,
            weight_identity=weight_identity,
            weight_bundle_ref=wb_out,
            weight_mode_declared_hint=str(cc["weight_mode_declared_hint"]),
            source_receipt_lineage=source_lineage,
            non_claims=[str(x) for x in nc],
            record_version=str(rv) if rv else None,
        )
        expected = sha256_hex_of_canonical_json(basis)
        if expected != str(cc.get("current_candidate_sha256", "")):
            return False, ["current_candidate_self_seal_mismatch"]
    except (KeyError, TypeError, ValueError) as exc:
        return False, [f"current_candidate_seal_verify_error:{exc!s}"]
    return True, []


def run_bounded_pointer_seeded_operator_local_run(
    *,
    corpus_root: Path,
    campaign_root: Path,
    campaign_id: str,
    pointer_seeded_run_id: str,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    torch_seed: int = 101,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """One bounded pass whose **declared seed** is the latest current-candidate pointer JSON.

    **Not** industrial self-play campaign execution; **not** **PX2-M04** exploit closure;
    **not** merge-gate default CI proof.
    """

    root = campaign_root.resolve()
    cc_path = root / CURRENT_CANDIDATE_JSON
    base_non_claims = [
        "Slice-14 bounded pointer-seeded run — declared seed is latest "
        "`px2_self_play_current_candidate.json`; not consumption-only bookkeeping.",
        "Not industrial self-play execution; not PX2-M04 exploit closure; not ladder strength.",
        "Not merge-gate default CI proof; not Blackwell-scale default.",
    ]

    def _emit(
        *,
        seeding_status: str,
        mismatch_reasons: list[str],
        declared_cc_sha: str,
        declared_cc_ver: str,
        byte_sha: str,
        anchor_snap: dict[str, Any],
        weight_mode: str,
        weight_identity_snap: dict[str, Any],
        wb_ref: str | None,
        prior_man_sha: str,
        cont_sha: str | None,
        updated_man_sha: str | None,
    ) -> dict[str, Any]:
        tm, tr = build_px2_self_play_pointer_seeded_run_artifacts(
            campaign_root_resolved=root,
            execution_kind=EXECUTION_KIND_SLICE14,
            campaign_id=campaign_id,
            campaign_profile_id=SLICE14_CAMPAIGN_PROFILE_ID,
            pointer_seeded_run_rule_id=POINTER_SEEDED_RUN_RULE_SEED_FROM_CURRENT_CANDIDATE_STUB,
            seed_semantics=SEED_SEMANTICS_DECLARED_FROM_LATEST_CURRENT_CANDIDATE_V1,
            declared_seed_current_candidate_sha256=declared_cc_sha,
            declared_seed_current_candidate_record_version=declared_cc_ver,
            seed_source_file_byte_sha256=byte_sha,
            declared_seed_anchor_snapshot=anchor_snap,
            weight_mode_declared=weight_mode,
            weight_identity_snapshot=weight_identity_snap,
            weight_bundle_ref_declared=wb_ref,
            prior_campaign_root_manifest_sha256_at_seed=prior_man_sha,
            pointer_seeded_run_id=pointer_seeded_run_id,
            resulting_continuity_sha256=cont_sha,
            updated_campaign_root_manifest_sha256=updated_man_sha,
            seeding_status=seeding_status,
            mismatch_reasons=mismatch_reasons,
            non_claims=base_non_claims,
        )
        write_json(root / POINTER_SEEDED_RUN_JSON, tm)
        write_json(root / "px2_self_play_pointer_seeded_run_report.json", tr)
        return {
            "campaign_root": str(root),
            "seeding_status": seeding_status,
            "pointer_seeded_run_sha256": tm["pointer_seeded_run_sha256"],
            "pointer_seeded_run_id": pointer_seeded_run_id,
            "mismatch_reasons": list(mismatch_reasons),
            "declared_seed_current_candidate_sha256": declared_cc_sha,
            "current_candidate_path": str(cc_path),
        }

    if not cc_path.is_file():
        return _emit(
            seeding_status=REJECTED_MISSING_POINTER,
            mismatch_reasons=["missing_px2_self_play_current_candidate_json"],
            declared_cc_sha="",
            declared_cc_ver="",
            byte_sha="",
            anchor_snap={},
            weight_mode="",
            weight_identity_snap={},
            wb_ref=None,
            prior_man_sha="",
            cont_sha=None,
            updated_man_sha=None,
        )

    raw = cc_path.read_bytes()
    byte_sha = hashlib.sha256(raw).hexdigest()
    cc = json.loads(raw.decode("utf-8"))
    if not isinstance(cc, dict):
        return _emit(
            seeding_status=REJECTED_MISMATCH,
            mismatch_reasons=["current_candidate_json_not_object"],
            declared_cc_sha="",
            declared_cc_ver="",
            byte_sha=byte_sha,
            anchor_snap={},
            weight_mode="",
            weight_identity_snap={},
            wb_ref=None,
            prior_man_sha="",
            cont_sha=None,
            updated_man_sha=None,
        )

    seal_ok, seal_reasons = verify_loaded_current_candidate_self_seal(cc)
    declared_cc_sha = str(cc.get("current_candidate_sha256", ""))
    declared_cc_ver = str(cc.get("current_candidate_record_version", ""))
    anchor_snap = _anchor_snapshot_from_cc(cc)
    w_hint = str(cc.get("weight_mode_declared_hint", ""))
    wi = cc.get("weight_identity")
    weight_identity_snap = dict(wi) if isinstance(wi, dict) else {}
    wre = cc.get("weight_bundle_ref")
    wb_ref = str(wre).strip() if wre else None
    prior_man_sha = str(cc.get("campaign_root_manifest_sha256", ""))

    combined: list[str] = []
    if not seal_ok:
        combined.extend(seal_reasons)

    _cc_loaded, val_reasons = validate_current_candidate_for_continuation_run(
        campaign_root=root,
        campaign_id=campaign_id,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
    )
    combined.extend(val_reasons)

    if combined:
        return _emit(
            seeding_status=REJECTED_MISMATCH,
            mismatch_reasons=combined,
            declared_cc_sha=declared_cc_sha,
            declared_cc_ver=declared_cc_ver,
            byte_sha=byte_sha,
            anchor_snap=anchor_snap,
            weight_mode=w_hint,
            weight_identity_snap=weight_identity_snap,
            wb_ref=wb_ref,
            prior_man_sha=prior_man_sha,
            cont_sha=None,
            updated_man_sha=None,
        )

    inner = run_slice5_operator_local_campaign(
        corpus_root=corpus_root,
        campaign_root=root,
        init_only=init_only,
        weights_path=weights_path,
        weight_bundle_ref=weight_bundle_ref,
        campaign_id=campaign_id,
        campaign_profile_id=SLICE14_CAMPAIGN_PROFILE_ID,
        torch_seed=torch_seed,
        run_id=pointer_seeded_run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        execution_kind=EXECUTION_KIND_SLICE14,
        write_campaign_root_manifest=False,
    )
    cont_sha = str(inner["continuity_sha256"])
    man_path = root / "px2_self_play_campaign_root_manifest.json"
    man_before = json.loads(man_path.read_text(encoding="utf-8"))
    opp_rule = str(man_before.get("opponent_selection_rule_id", OPPONENT_SELECTION_ROUND_ROBIN))
    updated_sha, _, _ = merge_campaign_root_manifest_after_continuation_run(
        root,
        campaign_id=campaign_id,
        new_run_id=pointer_seeded_run_id,
        new_continuity_sha256=cont_sha,
        opponent_selection_rule_id=opp_rule,
        execution_kind=EXECUTION_KIND_SLICE14,
    )

    out = _emit(
        seeding_status=SEEDING_OK,
        mismatch_reasons=[],
        declared_cc_sha=declared_cc_sha,
        declared_cc_ver=declared_cc_ver,
        byte_sha=byte_sha,
        anchor_snap=anchor_snap,
        weight_mode=w_hint,
        weight_identity_snap=weight_identity_snap,
        wb_ref=wb_ref,
        prior_man_sha=prior_man_sha,
        cont_sha=cont_sha,
        updated_man_sha=updated_sha,
    )
    return {
        **out,
        "resulting_continuity_sha256": cont_sha,
        "updated_campaign_root_manifest_sha256": updated_sha,
        "weight_mode_declared": (WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE),
    }
