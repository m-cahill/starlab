"""Governed bounded substantive operator-local execution record (PX2-M03 post–slice-16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_BOUNDED_SUBSTANTIVE_EXECUTION_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_bounded_substantive_execution.v1"
)
PX2_SELF_PLAY_BOUNDED_SUBSTANTIVE_EXECUTION_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_bounded_substantive_execution_report.v1"
)
BOUNDED_SUBSTANTIVE_EXECUTION_RECORD_VERSION: Final[str] = (
    "px2_m03_bounded_substantive_operator_local_execution_v2"
)

BOUNDED_SUBSTANTIVE_RULE_STUB: Final[str] = (
    "px2_m03_bounded_substantive_execution_operator_local_stub_v1"
)

SUBSTANTIVE_LINEAGE_CAMPAIGN_ROOT_ONLY: Final[str] = "campaign_root_only"
SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE15_HANDOFF: Final[str] = (
    "optional_slice15_pointer_seeded_handoff_present"
)
SUBSTANTIVE_LINEAGE_OPTIONAL_SLICE16_ANCHORED: Final[str] = (
    "optional_slice16_handoff_anchored_run_present"
)
SUBSTANTIVE_LINEAGE_OPTIONAL_BOTH: Final[str] = (
    "optional_slice15_handoff_and_slice16_handoff_anchored_present"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_bounded_substantive_execution_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    bounded_substantive_rule_id: str,
    substantive_run_id: str,
    continuity_step_count_requested: int,
    continuity_step_count_effective: int,
    resulting_continuity_sha256: str,
    updated_campaign_root_manifest_sha256: str,
    weight_mode_declared: str,
    substantive_lineage_mode: str,
    optional_pointer_seeded_handoff_sha256: str,
    optional_handoff_anchored_run_sha256: str,
    weights_file_sha256_declared: str,
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``bounded_substantive_execution_sha256``."""

    rec_ver = BOUNDED_SUBSTANTIVE_EXECUTION_RECORD_VERSION
    return {
        "contract_id": PX2_SELF_PLAY_BOUNDED_SUBSTANTIVE_EXECUTION_CONTRACT_ID,
        "bounded_substantive_execution_record_version": rec_ver,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "bounded_substantive_rule_id": bounded_substantive_rule_id,
        "substantive_run_id": substantive_run_id,
        "continuity_step_count_requested": continuity_step_count_requested,
        "continuity_step_count_effective": continuity_step_count_effective,
        "resulting_continuity_sha256": resulting_continuity_sha256,
        "updated_campaign_root_manifest_sha256": updated_campaign_root_manifest_sha256,
        "weight_mode_declared": weight_mode_declared,
        "weights_file_sha256_declared": weights_file_sha256_declared,
        "substantive_lineage_mode": substantive_lineage_mode,
        "optional_pointer_seeded_handoff_sha256": optional_pointer_seeded_handoff_sha256,
        "optional_handoff_anchored_run_sha256": optional_handoff_anchored_run_sha256,
        "non_claims": non_claims,
    }


def build_px2_self_play_bounded_substantive_execution_artifacts(
    *,
    campaign_root_resolved: Path,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    bounded_substantive_rule_id: str,
    substantive_run_id: str,
    continuity_step_count_requested: int,
    continuity_step_count_effective: int,
    resulting_continuity_sha256: str,
    updated_campaign_root_manifest_sha256: str,
    weight_mode_declared: str,
    substantive_lineage_mode: str,
    optional_pointer_seeded_handoff_sha256: str,
    optional_handoff_anchored_run_sha256: str,
    weights_file_sha256_declared: str,
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return bounded substantive execution JSON + report with sealed hash."""

    basis = build_bounded_substantive_execution_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        bounded_substantive_rule_id=bounded_substantive_rule_id,
        substantive_run_id=substantive_run_id,
        continuity_step_count_requested=continuity_step_count_requested,
        continuity_step_count_effective=continuity_step_count_effective,
        resulting_continuity_sha256=resulting_continuity_sha256,
        updated_campaign_root_manifest_sha256=updated_campaign_root_manifest_sha256,
        weight_mode_declared=weight_mode_declared,
        substantive_lineage_mode=substantive_lineage_mode,
        optional_pointer_seeded_handoff_sha256=optional_pointer_seeded_handoff_sha256,
        optional_handoff_anchored_run_sha256=optional_handoff_anchored_run_sha256,
        weights_file_sha256_declared=weights_file_sha256_declared,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "bounded_substantive_execution_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_bounded_substantive_execution_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_BOUNDED_SUBSTANTIVE_EXECUTION_REPORT_CONTRACT_ID,
        "bounded_substantive_execution_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "substantive_run_id": substantive_run_id,
            "continuity_step_count_effective": continuity_step_count_effective,
            "substantive_lineage_mode": substantive_lineage_mode,
            "weight_mode_declared": weight_mode_declared,
            "weights_file_sha256_declared": weights_file_sha256_declared,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
