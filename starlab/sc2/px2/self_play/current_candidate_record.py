"""Governed bounded operator-local current-candidate carry-forward record (PX2-M03 slice 10)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_current_candidate.v1"
)
PX2_SELF_PLAY_CURRENT_CANDIDATE_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_current_candidate_report.v1"
)
CURRENT_CANDIDATE_RECORD_VERSION: Final[str] = "px2_m03_slice10_current_candidate_carry_forward_v1"
CURRENT_CANDIDATE_RECORD_VERSION_SLICE12: Final[str] = (
    "px2_m03_slice12_current_candidate_reanchor_after_continuation_v1"
)

CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB: Final[str] = (
    "px2_m03_slice10_carry_forward_from_session_transition_stub_v1"
)
CURRENT_CANDIDATE_RULE_REANCHOR_FROM_CONTINUATION_STUB: Final[str] = (
    "px2_m03_slice12_reanchor_from_continuation_stub_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_current_candidate_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    operator_local_session_sha256: str,
    operator_local_session_transition_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    current_candidate_rule_id: str,
    current_run_id_after_transition: str,
    anchor: dict[str, Any],
    weight_identity: dict[str, Any],
    weight_bundle_ref: str | None,
    weight_mode_declared_hint: str,
    source_receipt_lineage: dict[str, Any],
    non_claims: list[str],
    record_version: str | None = None,
) -> dict[str, Any]:
    """Logical fields sealed as ``current_candidate_sha256``."""

    ver = record_version if record_version is not None else CURRENT_CANDIDATE_RECORD_VERSION
    return {
        "contract_id": PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID,
        "current_candidate_record_version": ver,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "operator_local_session_sha256": operator_local_session_sha256,
        "operator_local_session_transition_sha256": operator_local_session_transition_sha256,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "campaign_root_manifest_sha256": campaign_root_manifest_sha256,
        "current_candidate_rule_id": current_candidate_rule_id,
        "current_run_id_after_transition": current_run_id_after_transition,
        "anchor": anchor,
        "weight_identity": weight_identity,
        "weight_bundle_ref": weight_bundle_ref,
        "weight_mode_declared_hint": weight_mode_declared_hint,
        "source_receipt_lineage": source_receipt_lineage,
        "non_claims": non_claims,
    }


def build_px2_self_play_current_candidate_artifacts(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    operator_local_session_sha256: str,
    operator_local_session_transition_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    current_candidate_rule_id: str,
    current_run_id_after_transition: str,
    anchor: dict[str, Any],
    weight_identity: dict[str, Any],
    weight_bundle_ref: str | None,
    weight_mode_declared_hint: str,
    source_receipt_lineage: dict[str, Any],
    non_claims: list[str],
    record_version: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return current-candidate JSON + report with sealed hash."""

    basis = build_current_candidate_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        operator_local_session_sha256=operator_local_session_sha256,
        operator_local_session_transition_sha256=operator_local_session_transition_sha256,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        campaign_root_manifest_sha256=campaign_root_manifest_sha256,
        current_candidate_rule_id=current_candidate_rule_id,
        current_run_id_after_transition=current_run_id_after_transition,
        anchor=anchor,
        weight_identity=weight_identity,
        weight_bundle_ref=weight_bundle_ref,
        weight_mode_declared_hint=weight_mode_declared_hint,
        source_receipt_lineage=source_receipt_lineage,
        non_claims=non_claims,
        record_version=record_version,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "current_candidate_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_current_candidate_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CURRENT_CANDIDATE_REPORT_CONTRACT_ID,
        "current_candidate_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "current_candidate_rule_id": current_candidate_rule_id,
            "current_run_id_after_transition": current_run_id_after_transition,
            "anchor_continuity_run_id": anchor.get("continuity_run_id"),
            "weight_mode_declared_hint": weight_mode_declared_hint,
        },
        "next_run_operator_hints": {
            "read_via": "next_run_preflight_hints_from_current_candidate(campaign_root)",
            "artifact_relative_path": "px2_self_play_current_candidate.json",
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
