"""Governed bounded post–pointer-seeded handoff record (PX2-M03 slice 15)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_pointer_seeded_handoff.v1"
)
PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_pointer_seeded_handoff_report.v1"
)
POINTER_SEEDED_HANDOFF_RECORD_VERSION: Final[str] = "px2_m03_slice15_pointer_seeded_handoff_v1"

POINTER_SEEDED_HANDOFF_RULE_AFTER_SLICE14_STUB: Final[str] = (
    "px2_m03_slice15_handoff_after_slice14_pointer_seeded_stub_v1"
)

DECLARED_NEXT_STEP_FROM_SLICE14_POINTER_SEEDED_V1: Final[str] = (
    "declared_next_bounded_step_from_slice14_pointer_seeded_run_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_pointer_seeded_handoff_seal_basis(
    *,
    handoff_execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    handoff_rule_id: str,
    declared_next_step_source_lineage: str,
    prior_pointer_seeded_run_sha256: str,
    prior_pointer_seeded_run_id: str,
    prior_pointer_seeded_execution_kind: str,
    slice14_resulting_continuity_sha256: str,
    campaign_root_manifest_sha256_at_handoff: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    handoff_status: str,
    rejection_reasons: list[str],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``pointer_seeded_handoff_sha256``."""

    return {
        "contract_id": PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_CONTRACT_ID,
        "pointer_seeded_handoff_record_version": POINTER_SEEDED_HANDOFF_RECORD_VERSION,
        "handoff_execution_kind": handoff_execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "handoff_rule_id": handoff_rule_id,
        "declared_next_step_source_lineage": declared_next_step_source_lineage,
        "prior_pointer_seeded_run_sha256": prior_pointer_seeded_run_sha256,
        "prior_pointer_seeded_run_id": prior_pointer_seeded_run_id,
        "prior_pointer_seeded_execution_kind": prior_pointer_seeded_execution_kind,
        "slice14_resulting_continuity_sha256": slice14_resulting_continuity_sha256,
        "campaign_root_manifest_sha256_at_handoff": campaign_root_manifest_sha256_at_handoff,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "handoff_status": handoff_status,
        "rejection_reasons": list(rejection_reasons),
        "non_claims": non_claims,
    }


def build_px2_self_play_pointer_seeded_handoff_artifacts(
    *,
    campaign_root_resolved: Path,
    handoff_execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    handoff_rule_id: str,
    declared_next_step_source_lineage: str,
    prior_pointer_seeded_run_sha256: str,
    prior_pointer_seeded_run_id: str,
    prior_pointer_seeded_execution_kind: str,
    slice14_resulting_continuity_sha256: str,
    campaign_root_manifest_sha256_at_handoff: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    handoff_status: str,
    rejection_reasons: list[str],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return pointer-seeded handoff JSON + report with sealed hash."""

    basis = build_pointer_seeded_handoff_seal_basis(
        handoff_execution_kind=handoff_execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        handoff_rule_id=handoff_rule_id,
        declared_next_step_source_lineage=declared_next_step_source_lineage,
        prior_pointer_seeded_run_sha256=prior_pointer_seeded_run_sha256,
        prior_pointer_seeded_run_id=prior_pointer_seeded_run_id,
        prior_pointer_seeded_execution_kind=prior_pointer_seeded_execution_kind,
        slice14_resulting_continuity_sha256=slice14_resulting_continuity_sha256,
        campaign_root_manifest_sha256_at_handoff=campaign_root_manifest_sha256_at_handoff,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        handoff_status=handoff_status,
        rejection_reasons=rejection_reasons,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "pointer_seeded_handoff_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_pointer_seeded_handoff_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
        "prior_pointer_seeded_artifact_relative_path": "px2_self_play_pointer_seeded_run.json",
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_POINTER_SEEDED_HANDOFF_REPORT_CONTRACT_ID,
        "pointer_seeded_handoff_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "handoff_status": handoff_status,
            "prior_pointer_seeded_run_id": prior_pointer_seeded_run_id,
            "rejection_reasons": list(rejection_reasons),
            "declared_next_step_source_lineage": declared_next_step_source_lineage,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
