"""Governed bounded pointer-seeded operator-local run record (PX2-M03 slice 14)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_pointer_seeded_run.v1"
)
PX2_SELF_PLAY_POINTER_SEEDED_RUN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_pointer_seeded_run_report.v1"
)
POINTER_SEEDED_RUN_RECORD_VERSION: Final[str] = "px2_m03_slice14_pointer_seeded_run_v1"

POINTER_SEEDED_RUN_RULE_SEED_FROM_CURRENT_CANDIDATE_STUB: Final[str] = (
    "px2_m03_slice14_seed_from_current_candidate_pointer_stub_v1"
)

# Declares the run's governed starting posture: latest `px2_self_play_current_candidate.json`
# is the declared seed, not merely a hint to be optionally read.
SEED_SEMANTICS_DECLARED_FROM_LATEST_CURRENT_CANDIDATE_V1: Final[str] = (
    "declared_starting_point_from_latest_current_candidate_json_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_pointer_seeded_run_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    pointer_seeded_run_rule_id: str,
    seed_semantics: str,
    declared_seed_current_candidate_sha256: str,
    declared_seed_current_candidate_record_version: str,
    declared_seed_anchor_snapshot: dict[str, Any],
    weight_mode_declared: str,
    weight_identity_snapshot: dict[str, Any],
    weight_bundle_ref_declared: str | None,
    prior_campaign_root_manifest_sha256_at_seed: str,
    pointer_seeded_run_id: str,
    resulting_continuity_sha256: str | None,
    updated_campaign_root_manifest_sha256: str | None,
    seeding_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``pointer_seeded_run_sha256`` (path-independent)."""

    return {
        "contract_id": PX2_SELF_PLAY_POINTER_SEEDED_RUN_CONTRACT_ID,
        "pointer_seeded_run_record_version": POINTER_SEEDED_RUN_RECORD_VERSION,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "pointer_seeded_run_rule_id": pointer_seeded_run_rule_id,
        "seed_semantics": seed_semantics,
        "declared_seed_current_candidate_sha256": declared_seed_current_candidate_sha256,
        "declared_seed_current_candidate_record_version": (
            declared_seed_current_candidate_record_version
        ),
        "declared_seed_anchor_snapshot": declared_seed_anchor_snapshot,
        "weight_mode_declared": weight_mode_declared,
        "weight_identity_snapshot": weight_identity_snapshot,
        "weight_bundle_ref_declared": weight_bundle_ref_declared,
        "prior_campaign_root_manifest_sha256_at_seed": prior_campaign_root_manifest_sha256_at_seed,
        "pointer_seeded_run_id": pointer_seeded_run_id,
        "resulting_continuity_sha256": resulting_continuity_sha256,
        "updated_campaign_root_manifest_sha256": updated_campaign_root_manifest_sha256,
        "seeding_status": seeding_status,
        "mismatch_reasons": list(mismatch_reasons),
        "non_claims": non_claims,
    }


def build_px2_self_play_pointer_seeded_run_artifacts(
    *,
    campaign_root_resolved: Path,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    pointer_seeded_run_rule_id: str,
    seed_semantics: str,
    declared_seed_current_candidate_sha256: str,
    declared_seed_current_candidate_record_version: str,
    seed_source_file_byte_sha256: str,
    declared_seed_anchor_snapshot: dict[str, Any],
    weight_mode_declared: str,
    weight_identity_snapshot: dict[str, Any],
    weight_bundle_ref_declared: str | None,
    prior_campaign_root_manifest_sha256_at_seed: str,
    pointer_seeded_run_id: str,
    resulting_continuity_sha256: str | None,
    updated_campaign_root_manifest_sha256: str | None,
    seeding_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return pointer-seeded run JSON + report with sealed hash."""

    basis = build_pointer_seeded_run_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        pointer_seeded_run_rule_id=pointer_seeded_run_rule_id,
        seed_semantics=seed_semantics,
        declared_seed_current_candidate_sha256=declared_seed_current_candidate_sha256,
        declared_seed_current_candidate_record_version=declared_seed_current_candidate_record_version,
        declared_seed_anchor_snapshot=declared_seed_anchor_snapshot,
        weight_mode_declared=weight_mode_declared,
        weight_identity_snapshot=weight_identity_snapshot,
        weight_bundle_ref_declared=weight_bundle_ref_declared,
        prior_campaign_root_manifest_sha256_at_seed=prior_campaign_root_manifest_sha256_at_seed,
        pointer_seeded_run_id=pointer_seeded_run_id,
        resulting_continuity_sha256=resulting_continuity_sha256,
        updated_campaign_root_manifest_sha256=updated_campaign_root_manifest_sha256,
        seeding_status=seeding_status,
        mismatch_reasons=mismatch_reasons,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "pointer_seeded_run_sha256": seal,
        "seed_source_file_byte_sha256_advisory": seed_source_file_byte_sha256,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_pointer_seeded_run_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
        "seed_source_artifact_relative_path": "px2_self_play_current_candidate.json",
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_POINTER_SEEDED_RUN_REPORT_CONTRACT_ID,
        "pointer_seeded_run_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "seeding_status": seeding_status,
            "pointer_seeded_run_id": pointer_seeded_run_id,
            "mismatch_reasons": list(mismatch_reasons),
            "seed_semantics": seed_semantics,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "seed_source_file_byte_sha256_advisory": seed_source_file_byte_sha256,
        "non_claims": non_claims,
    }
    return manifest, report
