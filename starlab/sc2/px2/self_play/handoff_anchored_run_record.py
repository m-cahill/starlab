"""Governed bounded handoff-anchored operator-local run record (PX2-M03 slice 16)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_handoff_anchored_run.v1"
)
PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_handoff_anchored_run_report.v1"
)
HANDOFF_ANCHORED_RUN_RECORD_VERSION: Final[str] = "px2_m03_slice16_handoff_anchored_run_v1"

HANDOFF_ANCHORED_RUN_RULE_ANCHOR_ON_SLICE15_HANDOFF_STUB: Final[str] = (
    "px2_m03_slice16_anchor_bounded_run_on_slice15_pointer_seeded_handoff_stub_v1"
)

ANCHOR_SEMANTICS_DECLARED_FROM_SLICE15_HANDOFF_JSON_V1: Final[str] = (
    "declared_starting_posture_from_px2_self_play_pointer_seeded_handoff_json_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_handoff_anchored_run_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    handoff_anchored_run_rule_id: str,
    anchor_semantics: str,
    prior_pointer_seeded_handoff_sha256: str,
    prior_pointer_seeded_run_sha256: str,
    prior_pointer_seeded_run_id: str,
    slice14_resulting_continuity_sha256_at_anchor: str,
    campaign_root_manifest_sha256_at_anchor: str,
    handoff_anchored_run_id: str,
    resulting_continuity_sha256: str | None,
    updated_campaign_root_manifest_sha256: str | None,
    anchoring_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``handoff_anchored_run_sha256``."""

    return {
        "contract_id": PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_CONTRACT_ID,
        "handoff_anchored_run_record_version": HANDOFF_ANCHORED_RUN_RECORD_VERSION,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "handoff_anchored_run_rule_id": handoff_anchored_run_rule_id,
        "anchor_semantics": anchor_semantics,
        "prior_pointer_seeded_handoff_sha256": prior_pointer_seeded_handoff_sha256,
        "prior_pointer_seeded_run_sha256": prior_pointer_seeded_run_sha256,
        "prior_pointer_seeded_run_id": prior_pointer_seeded_run_id,
        "slice14_resulting_continuity_sha256_at_anchor": (
            slice14_resulting_continuity_sha256_at_anchor
        ),
        "campaign_root_manifest_sha256_at_anchor": campaign_root_manifest_sha256_at_anchor,
        "handoff_anchored_run_id": handoff_anchored_run_id,
        "resulting_continuity_sha256": resulting_continuity_sha256,
        "updated_campaign_root_manifest_sha256": updated_campaign_root_manifest_sha256,
        "anchoring_status": anchoring_status,
        "mismatch_reasons": list(mismatch_reasons),
        "non_claims": non_claims,
    }


def build_px2_self_play_handoff_anchored_run_artifacts(
    *,
    campaign_root_resolved: Path,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    handoff_anchored_run_rule_id: str,
    anchor_semantics: str,
    prior_pointer_seeded_handoff_sha256: str,
    prior_pointer_seeded_run_sha256: str,
    prior_pointer_seeded_run_id: str,
    slice14_resulting_continuity_sha256_at_anchor: str,
    campaign_root_manifest_sha256_at_anchor: str,
    handoff_anchored_run_id: str,
    resulting_continuity_sha256: str | None,
    updated_campaign_root_manifest_sha256: str | None,
    anchoring_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return handoff-anchored run JSON + report with sealed hash."""

    basis = build_handoff_anchored_run_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        handoff_anchored_run_rule_id=handoff_anchored_run_rule_id,
        anchor_semantics=anchor_semantics,
        prior_pointer_seeded_handoff_sha256=prior_pointer_seeded_handoff_sha256,
        prior_pointer_seeded_run_sha256=prior_pointer_seeded_run_sha256,
        prior_pointer_seeded_run_id=prior_pointer_seeded_run_id,
        slice14_resulting_continuity_sha256_at_anchor=slice14_resulting_continuity_sha256_at_anchor,
        campaign_root_manifest_sha256_at_anchor=campaign_root_manifest_sha256_at_anchor,
        handoff_anchored_run_id=handoff_anchored_run_id,
        resulting_continuity_sha256=resulting_continuity_sha256,
        updated_campaign_root_manifest_sha256=updated_campaign_root_manifest_sha256,
        anchoring_status=anchoring_status,
        mismatch_reasons=mismatch_reasons,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "handoff_anchored_run_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_handoff_anchored_run_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
        "prior_pointer_seeded_handoff_artifact_relative_path": (
            "px2_self_play_pointer_seeded_handoff.json"
        ),
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_HANDOFF_ANCHORED_RUN_REPORT_CONTRACT_ID,
        "handoff_anchored_run_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "anchoring_status": anchoring_status,
            "handoff_anchored_run_id": handoff_anchored_run_id,
            "mismatch_reasons": list(mismatch_reasons),
            "anchor_semantics": anchor_semantics,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
