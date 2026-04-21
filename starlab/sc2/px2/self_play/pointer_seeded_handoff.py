"""Bounded post–pointer-seeded handoff (PX2-M03 slice 15).

Validates a successful slice-14 ``px2_self_play_pointer_seeded_run.json`` and emits a governed
handoff record declaring the next bounded step's lineage source — **not** an industrial campaign.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE14,
    EXECUTION_KIND_SLICE15,
)
from starlab.sc2.px2.self_play.pointer_seeded_handoff_record import (
    DECLARED_NEXT_STEP_FROM_SLICE14_POINTER_SEEDED_V1,
    POINTER_SEEDED_HANDOFF_RULE_AFTER_SLICE14_STUB,
    build_px2_self_play_pointer_seeded_handoff_artifacts,
)
from starlab.sc2.px2.self_play.pointer_seeded_run_record import (
    PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID,
    build_pointer_seeded_run_seal_basis,
)
from starlab.sc2.px2.self_play.run_artifacts import write_json

SLICE15_HANDOFF_CAMPAIGN_PROFILE_ID: Final[str] = "px2_m03_slice15_post_pointer_seeded_handoff_v1"

POINTER_SEEDED_HANDOFF_JSON: Final[str] = "px2_self_play_pointer_seeded_handoff.json"

HANDOFF_OK: Final[str] = "handed_off_ok"
REJECTED_MISSING_POINTER_SEEDED: Final[str] = "rejected_missing_pointer_seeded_run"
REJECTED_NOT_SEEDED_OK: Final[str] = "rejected_pointer_seeded_not_seeded_ok"
REJECTED_LINEAGE_MISMATCH: Final[str] = "rejected_lineage_mismatch"
REJECTED_CAMPAIGN_ID_MISMATCH: Final[str] = "rejected_campaign_id_mismatch"
REJECTED_POINTER_SEEDED_SEAL: Final[str] = "rejected_pointer_seeded_seal_mismatch"


def verify_loaded_pointer_seeded_run_self_seal(ps: dict[str, Any]) -> tuple[bool, list[str]]:
    """Recompute the pointer-seeded run logical seal (matches ``pointer_seeded_run_record``)."""

    try:
        anchor = ps.get("declared_seed_anchor_snapshot")
        weight_identity = ps.get("weight_identity_snapshot")
        if not isinstance(anchor, dict):
            return False, ["pointer_seeded_declared_seed_anchor_snapshot_not_dict"]
        if not isinstance(weight_identity, dict):
            return False, ["pointer_seeded_weight_identity_snapshot_not_dict"]
        nc = ps.get("non_claims")
        if not isinstance(nc, list):
            return False, ["pointer_seeded_non_claims_not_list"]
        wb = ps.get("weight_bundle_ref_declared")
        wb_out: str | None = str(wb).strip() if wb else None
        rv = ps.get("declared_seed_current_candidate_record_version")
        dver = str(rv) if rv is not None else ""
        basis = build_pointer_seeded_run_seal_basis(
            execution_kind=str(ps["execution_kind"]),
            campaign_id=str(ps["campaign_id"]),
            campaign_profile_id=str(ps["campaign_profile_id"]),
            pointer_seeded_run_rule_id=str(ps["pointer_seeded_run_rule_id"]),
            seed_semantics=str(ps["seed_semantics"]),
            declared_seed_current_candidate_sha256=str(
                ps["declared_seed_current_candidate_sha256"]
            ),
            declared_seed_current_candidate_record_version=dver,
            declared_seed_anchor_snapshot=anchor,
            weight_mode_declared=str(ps["weight_mode_declared"]),
            weight_identity_snapshot=weight_identity,
            weight_bundle_ref_declared=wb_out,
            prior_campaign_root_manifest_sha256_at_seed=str(
                ps["prior_campaign_root_manifest_sha256_at_seed"]
            ),
            pointer_seeded_run_id=str(ps["pointer_seeded_run_id"]),
            resulting_continuity_sha256=str(ps["resulting_continuity_sha256"])
            if ps.get("resulting_continuity_sha256")
            else None,
            updated_campaign_root_manifest_sha256=str(ps["updated_campaign_root_manifest_sha256"])
            if ps.get("updated_campaign_root_manifest_sha256")
            else None,
            seeding_status=str(ps["seeding_status"]),
            mismatch_reasons=[str(x) for x in ps.get("mismatch_reasons", [])]
            if isinstance(ps.get("mismatch_reasons"), list)
            else [],
            non_claims=[str(x) for x in nc],
        )
        expected = sha256_hex_of_canonical_json(basis)
        if expected != str(ps.get("pointer_seeded_run_sha256", "")):
            return False, ["pointer_seeded_run_self_seal_mismatch"]
    except (KeyError, TypeError, ValueError) as exc:
        return False, [f"pointer_seeded_run_seal_verify_error:{exc!s}"]
    return True, []


def run_bounded_pointer_seeded_handoff(
    *,
    campaign_root: Path,
    campaign_id: str,
) -> dict[str, Any]:
    """Validate slice-14 pointer-seeded artifact and emit governed handoff JSON + report.

    **Not** industrial self-play; **not** **PX2-M04** exploit closure; **not** merge-gate CI.
    """

    root = campaign_root.resolve()
    ps_path = root / "px2_self_play_pointer_seeded_run.json"
    base_non_claims = [
        "Slice-15 post–pointer-seeded handoff — next bounded step lineage from slice-14 "
        "pointer-seeded run; not a second unanchored run.",
        "Not industrial self-play execution; not PX2-M04 exploit closure; not ladder strength.",
        "Not merge-gate default CI proof; not Blackwell-scale default.",
    ]

    empty_man = ""
    empty_cc = ""

    def _emit_handoff(
        *,
        handoff_status: str,
        rejection_reasons: list[str],
        prior_ps_sha: str,
        prior_run_id: str,
        prior_ps_exec: str,
        cont_sha: str,
        man_sha: str,
        cc_sha: str,
        opp_sha: str,
    ) -> dict[str, Any]:
        tm, tr = build_px2_self_play_pointer_seeded_handoff_artifacts(
            campaign_root_resolved=root,
            handoff_execution_kind=EXECUTION_KIND_SLICE15,
            campaign_id=campaign_id,
            campaign_profile_id=SLICE15_HANDOFF_CAMPAIGN_PROFILE_ID,
            handoff_rule_id=POINTER_SEEDED_HANDOFF_RULE_AFTER_SLICE14_STUB,
            declared_next_step_source_lineage=DECLARED_NEXT_STEP_FROM_SLICE14_POINTER_SEEDED_V1,
            prior_pointer_seeded_run_sha256=prior_ps_sha,
            prior_pointer_seeded_run_id=prior_run_id,
            prior_pointer_seeded_execution_kind=prior_ps_exec,
            slice14_resulting_continuity_sha256=cont_sha,
            campaign_root_manifest_sha256_at_handoff=man_sha,
            campaign_contract_sha256=cc_sha,
            opponent_pool_identity_sha256=opp_sha,
            handoff_status=handoff_status,
            rejection_reasons=rejection_reasons,
            non_claims=base_non_claims,
        )
        write_json(root / POINTER_SEEDED_HANDOFF_JSON, tm)
        write_json(root / "px2_self_play_pointer_seeded_handoff_report.json", tr)
        return {
            "campaign_root": str(root),
            "handoff_status": handoff_status,
            "pointer_seeded_handoff_sha256": tm["pointer_seeded_handoff_sha256"],
            "rejection_reasons": list(rejection_reasons),
        }

    if not ps_path.is_file():
        return _emit_handoff(
            handoff_status=REJECTED_MISSING_POINTER_SEEDED,
            rejection_reasons=["missing_px2_self_play_pointer_seeded_run_json"],
            prior_ps_sha="",
            prior_run_id="",
            prior_ps_exec="",
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    ps = json.loads(ps_path.read_text(encoding="utf-8"))
    if not isinstance(ps, dict):
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["pointer_seeded_run_json_not_object"],
            prior_ps_sha="",
            prior_run_id="",
            prior_ps_exec="",
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    if str(ps.get("contract_id", "")) != PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID:
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["pointer_seeded_run_contract_id_unexpected"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=str(ps.get("pointer_seeded_run_id", "")),
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    if str(ps.get("campaign_id", "")) != campaign_id:
        return _emit_handoff(
            handoff_status=REJECTED_CAMPAIGN_ID_MISMATCH,
            rejection_reasons=["campaign_id_mismatch_vs_pointer_seeded_run"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=str(ps.get("pointer_seeded_run_id", "")),
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    seal_ok, seal_reasons = verify_loaded_pointer_seeded_run_self_seal(ps)
    if not seal_ok:
        return _emit_handoff(
            handoff_status=REJECTED_POINTER_SEEDED_SEAL,
            rejection_reasons=seal_reasons,
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=str(ps.get("pointer_seeded_run_id", "")),
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    if str(ps.get("seeding_status", "")) != "seeded_ok":
        return _emit_handoff(
            handoff_status=REJECTED_NOT_SEEDED_OK,
            rejection_reasons=["pointer_seeded_run_seeding_status_not_seeded_ok"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=str(ps.get("pointer_seeded_run_id", "")),
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    rid = str(ps["pointer_seeded_run_id"])
    cont_sha_expected = str(ps.get("resulting_continuity_sha256", ""))
    man_sha_expected = str(ps.get("updated_campaign_root_manifest_sha256", ""))
    if not cont_sha_expected or not man_sha_expected:
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["pointer_seeded_run_missing_continuity_or_manifest_sha"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha="",
            man_sha=empty_man,
            cc_sha=empty_cc,
            opp_sha="",
        )

    cont_path = root / "runs" / rid / "px2_self_play_campaign_continuity.json"
    if not cont_path.is_file():
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["missing_continuity_json_for_pointer_seeded_run_id"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha=cont_sha_expected,
            man_sha=man_sha_expected,
            cc_sha=empty_cc,
            opp_sha="",
        )

    cont = json.loads(cont_path.read_text(encoding="utf-8"))
    if str(cont.get("continuity_sha256", "")) != cont_sha_expected:
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["continuity_sha256_mismatch_vs_pointer_seeded_run"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha=cont_sha_expected,
            man_sha=man_sha_expected,
            cc_sha=empty_cc,
            opp_sha="",
        )

    if str(cont.get("execution_kind", "")) != EXECUTION_KIND_SLICE14:
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["continuity_execution_kind_not_slice14"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha=cont_sha_expected,
            man_sha=man_sha_expected,
            cc_sha=empty_cc,
            opp_sha="",
        )

    man_path = root / "px2_self_play_campaign_root_manifest.json"
    if not man_path.is_file():
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["missing_px2_self_play_campaign_root_manifest_json"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha=cont_sha_expected,
            man_sha=man_sha_expected,
            cc_sha=empty_cc,
            opp_sha="",
        )

    man = json.loads(man_path.read_text(encoding="utf-8"))
    man_sha_disk = str(man.get("campaign_root_manifest_sha256", ""))
    if man_sha_disk != man_sha_expected:
        return _emit_handoff(
            handoff_status=REJECTED_LINEAGE_MISMATCH,
            rejection_reasons=["campaign_root_manifest_stale_or_mismatch_vs_pointer_seeded_run"],
            prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
            prior_run_id=rid,
            prior_ps_exec=str(ps.get("execution_kind", "")),
            cont_sha=cont_sha_expected,
            man_sha=man_sha_expected,
            cc_sha=str(man.get("campaign_contract_sha256", "")),
            opp_sha=str(man.get("opponent_pool_identity_sha256", "")),
        )

    cc_sha = str(man.get("campaign_contract_sha256", ""))
    opp_sha = str(man.get("opponent_pool_identity_sha256", ""))
    snap = ps.get("weight_identity_snapshot")
    wcont = cont.get("weight_identity")
    if isinstance(snap, dict) and isinstance(wcont, dict):
        if sha256_hex_of_canonical_json(snap) != sha256_hex_of_canonical_json(wcont):
            return _emit_handoff(
                handoff_status=REJECTED_LINEAGE_MISMATCH,
                rejection_reasons=["weight_identity_mismatch_vs_slice14_continuity"],
                prior_ps_sha=str(ps.get("pointer_seeded_run_sha256", "")),
                prior_run_id=rid,
                prior_ps_exec=str(ps.get("execution_kind", "")),
                cont_sha=cont_sha_expected,
                man_sha=man_sha_expected,
                cc_sha=cc_sha,
                opp_sha=opp_sha,
            )

    return _emit_handoff(
        handoff_status=HANDOFF_OK,
        rejection_reasons=[],
        prior_ps_sha=str(ps["pointer_seeded_run_sha256"]),
        prior_run_id=rid,
        prior_ps_exec=str(ps["execution_kind"]),
        cont_sha=cont_sha_expected,
        man_sha=man_sha_expected,
        cc_sha=cc_sha,
        opp_sha=opp_sha,
    )
