"""Bounded operator-local run anchored on slice-15 handoff JSON (PX2-M03 slice 16)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE14,
    EXECUTION_KIND_SLICE16,
)
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.continuation_run import (
    merge_campaign_root_manifest_after_continuation_run,
)
from starlab.sc2.px2.self_play.handoff_anchored_run_record import (
    ANCHOR_SEMANTICS_DECLARED_FROM_SLICE15_HANDOFF_JSON_V1,
    HANDOFF_ANCHORED_RUN_RULE_ANCHOR_ON_SLICE15_HANDOFF_STUB,
    build_px2_self_play_handoff_anchored_run_artifacts,
)
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.pointer_seeded_handoff import HANDOFF_OK, POINTER_SEEDED_HANDOFF_JSON
from starlab.sc2.px2.self_play.pointer_seeded_handoff_record import (
    PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID,
    build_pointer_seeded_handoff_seal_basis,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json
from starlab.sc2.px2.self_play.weight_loading import WEIGHT_MODE_INIT_ONLY, WEIGHT_MODE_WEIGHTS_FILE

SLICE16_HANDOFF_ANCHORED_PROFILE_ID: Final[str] = (
    "px2_m03_slice16_handoff_anchored_operator_local_run_v1"
)

HANDOFF_ANCHORED_RUN_JSON: Final[str] = "px2_self_play_handoff_anchored_run.json"

ANCHORED_OK: Final[str] = "anchored_ok"
REJECTED_MISSING_HANDOFF: Final[str] = "rejected_missing_pointer_seeded_handoff"
REJECTED_HANDOFF_NOT_OK: Final[str] = "rejected_pointer_seeded_handoff_not_handed_off_ok"
REJECTED_HANDOFF_SEAL: Final[str] = "rejected_pointer_seeded_handoff_seal_mismatch"
REJECTED_LINEAGE_MISMATCH: Final[str] = "rejected_lineage_mismatch"
REJECTED_CAMPAIGN_ID_MISMATCH: Final[str] = "rejected_campaign_id_mismatch"


def verify_loaded_pointer_seeded_handoff_self_seal(ho: dict[str, Any]) -> tuple[bool, list[str]]:
    """Recompute slice-15 handoff logical seal (matches ``pointer_seeded_handoff_record``)."""

    try:
        nc = ho.get("non_claims")
        if not isinstance(nc, list):
            return False, ["pointer_seeded_handoff_non_claims_not_list"]
        rr = ho.get("rejection_reasons")
        rej = [str(x) for x in rr] if isinstance(rr, list) else []
        basis = build_pointer_seeded_handoff_seal_basis(
            handoff_execution_kind=str(ho["handoff_execution_kind"]),
            campaign_id=str(ho["campaign_id"]),
            campaign_profile_id=str(ho["campaign_profile_id"]),
            handoff_rule_id=str(ho["handoff_rule_id"]),
            declared_next_step_source_lineage=str(ho["declared_next_step_source_lineage"]),
            prior_pointer_seeded_run_sha256=str(ho["prior_pointer_seeded_run_sha256"]),
            prior_pointer_seeded_run_id=str(ho["prior_pointer_seeded_run_id"]),
            prior_pointer_seeded_execution_kind=str(ho["prior_pointer_seeded_execution_kind"]),
            slice14_resulting_continuity_sha256=str(ho["slice14_resulting_continuity_sha256"]),
            campaign_root_manifest_sha256_at_handoff=str(
                ho["campaign_root_manifest_sha256_at_handoff"]
            ),
            campaign_contract_sha256=str(ho["campaign_contract_sha256"]),
            opponent_pool_identity_sha256=str(ho["opponent_pool_identity_sha256"]),
            handoff_status=str(ho["handoff_status"]),
            rejection_reasons=rej,
            non_claims=[str(x) for x in nc],
        )
        expected = sha256_hex_of_canonical_json(basis)
        if expected != str(ho.get("pointer_seeded_handoff_sha256", "")):
            return False, ["pointer_seeded_handoff_self_seal_mismatch"]
    except (KeyError, TypeError, ValueError) as exc:
        return False, [f"pointer_seeded_handoff_seal_verify_error:{exc!s}"]
    return True, []


def run_bounded_handoff_anchored_operator_local_run(
    *,
    corpus_root: Path,
    campaign_root: Path,
    campaign_id: str,
    handoff_anchored_run_id: str,
    init_only: bool = True,
    weights_path: Path | None = None,
    weight_bundle_ref: str | None = None,
    torch_seed: int = 103,
    continuity_step_count: int = 2,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> dict[str, Any]:
    """One bounded pass whose **declared anchor** is ``px2_self_play_pointer_seeded_handoff.json``.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    root = campaign_root.resolve()
    ho_path = root / POINTER_SEEDED_HANDOFF_JSON
    base_non_claims = [
        "Slice-16 bounded handoff-anchored run — declared anchor is slice-15 "
        "`px2_self_play_pointer_seeded_handoff.json`; not an unanchored continuity pass.",
        "Not industrial self-play execution; not PX2-M04 exploit closure; not ladder strength.",
        "Not merge-gate default CI proof; not Blackwell-scale default.",
    ]

    def _emit(
        *,
        anchoring_status: str,
        mismatch_reasons: list[str],
        ho_sha: str,
        prior_ps_sha: str,
        prior_ps_rid: str,
        slice14_cont_at_anchor: str,
        man_at_anchor: str,
        cont_sha: str | None,
        updated_man_sha: str | None,
    ) -> dict[str, Any]:
        tm, tr = build_px2_self_play_handoff_anchored_run_artifacts(
            campaign_root_resolved=root,
            execution_kind=EXECUTION_KIND_SLICE16,
            campaign_id=campaign_id,
            campaign_profile_id=SLICE16_HANDOFF_ANCHORED_PROFILE_ID,
            handoff_anchored_run_rule_id=HANDOFF_ANCHORED_RUN_RULE_ANCHOR_ON_SLICE15_HANDOFF_STUB,
            anchor_semantics=ANCHOR_SEMANTICS_DECLARED_FROM_SLICE15_HANDOFF_JSON_V1,
            prior_pointer_seeded_handoff_sha256=ho_sha,
            prior_pointer_seeded_run_sha256=prior_ps_sha,
            prior_pointer_seeded_run_id=prior_ps_rid,
            slice14_resulting_continuity_sha256_at_anchor=slice14_cont_at_anchor,
            campaign_root_manifest_sha256_at_anchor=man_at_anchor,
            handoff_anchored_run_id=handoff_anchored_run_id,
            resulting_continuity_sha256=cont_sha,
            updated_campaign_root_manifest_sha256=updated_man_sha,
            anchoring_status=anchoring_status,
            mismatch_reasons=mismatch_reasons,
            non_claims=base_non_claims,
        )
        write_json(root / HANDOFF_ANCHORED_RUN_JSON, tm)
        write_json(root / "px2_self_play_handoff_anchored_run_report.json", tr)
        return {
            "campaign_root": str(root),
            "anchoring_status": anchoring_status,
            "handoff_anchored_run_sha256": tm["handoff_anchored_run_sha256"],
            "handoff_anchored_run_id": handoff_anchored_run_id,
            "mismatch_reasons": list(mismatch_reasons),
            "prior_pointer_seeded_handoff_sha256": ho_sha,
        }

    if not ho_path.is_file():
        return _emit(
            anchoring_status=REJECTED_MISSING_HANDOFF,
            mismatch_reasons=["missing_px2_self_play_pointer_seeded_handoff_json"],
            ho_sha="",
            prior_ps_sha="",
            prior_ps_rid="",
            slice14_cont_at_anchor="",
            man_at_anchor="",
            cont_sha=None,
            updated_man_sha=None,
        )

    ho = json.loads(ho_path.read_text(encoding="utf-8"))
    if not isinstance(ho, dict):
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["pointer_seeded_handoff_json_not_object"],
            ho_sha="",
            prior_ps_sha="",
            prior_ps_rid="",
            slice14_cont_at_anchor="",
            man_at_anchor="",
            cont_sha=None,
            updated_man_sha=None,
        )

    ho_sha_expected = str(ho.get("pointer_seeded_handoff_sha256", ""))

    if str(ho.get("contract_id", "")) != PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID:
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["pointer_seeded_handoff_contract_id_unexpected"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=str(ho.get("prior_pointer_seeded_run_sha256", "")),
            prior_ps_rid=str(ho.get("prior_pointer_seeded_run_id", "")),
            slice14_cont_at_anchor=str(ho.get("slice14_resulting_continuity_sha256", "")),
            man_at_anchor=str(ho.get("campaign_root_manifest_sha256_at_handoff", "")),
            cont_sha=None,
            updated_man_sha=None,
        )

    if str(ho.get("campaign_id", "")) != campaign_id:
        return _emit(
            anchoring_status=REJECTED_CAMPAIGN_ID_MISMATCH,
            mismatch_reasons=["campaign_id_mismatch_vs_pointer_seeded_handoff"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=str(ho.get("prior_pointer_seeded_run_sha256", "")),
            prior_ps_rid=str(ho.get("prior_pointer_seeded_run_id", "")),
            slice14_cont_at_anchor=str(ho.get("slice14_resulting_continuity_sha256", "")),
            man_at_anchor=str(ho.get("campaign_root_manifest_sha256_at_handoff", "")),
            cont_sha=None,
            updated_man_sha=None,
        )

    seal_ok, seal_reasons = verify_loaded_pointer_seeded_handoff_self_seal(ho)
    if not seal_ok:
        return _emit(
            anchoring_status=REJECTED_HANDOFF_SEAL,
            mismatch_reasons=seal_reasons,
            ho_sha=ho_sha_expected,
            prior_ps_sha=str(ho.get("prior_pointer_seeded_run_sha256", "")),
            prior_ps_rid=str(ho.get("prior_pointer_seeded_run_id", "")),
            slice14_cont_at_anchor=str(ho.get("slice14_resulting_continuity_sha256", "")),
            man_at_anchor=str(ho.get("campaign_root_manifest_sha256_at_handoff", "")),
            cont_sha=None,
            updated_man_sha=None,
        )

    if str(ho.get("handoff_status", "")) != HANDOFF_OK:
        return _emit(
            anchoring_status=REJECTED_HANDOFF_NOT_OK,
            mismatch_reasons=["pointer_seeded_handoff_status_not_handed_off_ok"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=str(ho.get("prior_pointer_seeded_run_sha256", "")),
            prior_ps_rid=str(ho.get("prior_pointer_seeded_run_id", "")),
            slice14_cont_at_anchor=str(ho.get("slice14_resulting_continuity_sha256", "")),
            man_at_anchor=str(ho.get("campaign_root_manifest_sha256_at_handoff", "")),
            cont_sha=None,
            updated_man_sha=None,
        )

    prior_rid = str(ho["prior_pointer_seeded_run_id"])
    slice14_cont_expected = str(ho.get("slice14_resulting_continuity_sha256", ""))
    man_expected = str(ho.get("campaign_root_manifest_sha256_at_handoff", ""))
    prior_ps_sha = str(ho.get("prior_pointer_seeded_run_sha256", ""))

    if not slice14_cont_expected or not man_expected:
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["handoff_missing_slice14_continuity_or_manifest_sha"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    cont_path = root / "runs" / prior_rid / "px2_self_play_campaign_continuity.json"
    if not cont_path.is_file():
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["missing_slice14_continuity_json_for_prior_pointer_seeded_run_id"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    cont = json.loads(cont_path.read_text(encoding="utf-8"))
    if str(cont.get("continuity_sha256", "")) != slice14_cont_expected:
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["slice14_continuity_sha256_mismatch_vs_handoff"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    if str(cont.get("execution_kind", "")) != EXECUTION_KIND_SLICE14:
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["slice14_continuity_execution_kind_not_slice14"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    man_path = root / "px2_self_play_campaign_root_manifest.json"
    if not man_path.is_file():
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["missing_px2_self_play_campaign_root_manifest_json"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    man = json.loads(man_path.read_text(encoding="utf-8"))
    man_disk = str(man.get("campaign_root_manifest_sha256", ""))
    if man_disk != man_expected:
        return _emit(
            anchoring_status=REJECTED_LINEAGE_MISMATCH,
            mismatch_reasons=["campaign_root_manifest_stale_or_mismatch_vs_handoff"],
            ho_sha=ho_sha_expected,
            prior_ps_sha=prior_ps_sha,
            prior_ps_rid=prior_rid,
            slice14_cont_at_anchor=slice14_cont_expected,
            man_at_anchor=man_expected,
            cont_sha=None,
            updated_man_sha=None,
        )

    ps_path = root / "px2_self_play_pointer_seeded_run.json"
    if ps_path.is_file():
        ps = json.loads(ps_path.read_text(encoding="utf-8"))
        if str(ps.get("pointer_seeded_run_sha256", "")) != prior_ps_sha:
            return _emit(
                anchoring_status=REJECTED_LINEAGE_MISMATCH,
                mismatch_reasons=["on_disk_pointer_seeded_run_sha256_mismatch_vs_handoff"],
                ho_sha=ho_sha_expected,
                prior_ps_sha=prior_ps_sha,
                prior_ps_rid=prior_rid,
                slice14_cont_at_anchor=slice14_cont_expected,
                man_at_anchor=man_expected,
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
        campaign_profile_id=SLICE16_HANDOFF_ANCHORED_PROFILE_ID,
        torch_seed=torch_seed,
        run_id=handoff_anchored_run_id,
        continuity_step_count=continuity_step_count,
        device_intent=device_intent,
        map_location=map_location,
        opponent_selection_rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
        execution_kind=EXECUTION_KIND_SLICE16,
        write_campaign_root_manifest=False,
    )
    new_cont_sha = str(inner["continuity_sha256"])
    man_before = json.loads(man_path.read_text(encoding="utf-8"))
    opp_rule = str(man_before.get("opponent_selection_rule_id", OPPONENT_SELECTION_ROUND_ROBIN))
    updated_sha, _, _ = merge_campaign_root_manifest_after_continuation_run(
        root,
        campaign_id=campaign_id,
        new_run_id=handoff_anchored_run_id,
        new_continuity_sha256=new_cont_sha,
        opponent_selection_rule_id=opp_rule,
        execution_kind=EXECUTION_KIND_SLICE16,
    )

    out = _emit(
        anchoring_status=ANCHORED_OK,
        mismatch_reasons=[],
        ho_sha=ho_sha_expected,
        prior_ps_sha=prior_ps_sha,
        prior_ps_rid=prior_rid,
        slice14_cont_at_anchor=slice14_cont_expected,
        man_at_anchor=man_expected,
        cont_sha=new_cont_sha,
        updated_man_sha=updated_sha,
    )
    return {
        **out,
        "resulting_continuity_sha256": new_cont_sha,
        "updated_campaign_root_manifest_sha256": updated_sha,
        "weight_mode_declared": (WEIGHT_MODE_INIT_ONLY if init_only else WEIGHT_MODE_WEIGHTS_FILE),
    }
