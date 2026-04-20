"""Governed bounded operator-local session transition record (PX2-M03 slice 9)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_session_transition.v1"
)
PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_session_transition_report.v1"
)
OPERATOR_LOCAL_SESSION_TRANSITION_RECORD_VERSION: Final[str] = (
    "px2_m03_slice9_bounded_session_transition_v1"
)

TRANSITION_RULE_PROMOTION_LAST_RUN: Final[str] = "px2_m03_slice9_last_run_final_promotion_stub_v1"
TRANSITION_RULE_ROLLBACK_FIRST_RUN_BASELINE: Final[str] = (
    "px2_m03_slice9_rollback_to_first_run_first_checkpoint_stub_v1"
)


def _seal_transition_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_operator_local_session_transition_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    operator_local_session_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    ordered_run_ids: tuple[str, ...],
    transition_type: str,
    transition_rule_id: str,
    current_run_id_after_transition: str,
    source_receipt_lineage: dict[str, Any],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``operator_local_session_transition_sha256``."""

    return {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID,
        "operator_local_session_transition_record_version": (
            OPERATOR_LOCAL_SESSION_TRANSITION_RECORD_VERSION
        ),
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "operator_local_session_sha256": operator_local_session_sha256,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "campaign_root_manifest_sha256": campaign_root_manifest_sha256,
        "ordered_run_ids": list(ordered_run_ids),
        "transition_type": transition_type,
        "transition_rule_id": transition_rule_id,
        "current_run_id_after_transition": current_run_id_after_transition,
        "source_receipt_lineage": source_receipt_lineage,
        "non_claims": non_claims,
    }


def build_px2_self_play_operator_local_session_transition_artifacts(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    operator_local_session_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    ordered_run_ids: tuple[str, ...],
    transition_type: str,
    transition_rule_id: str,
    current_run_id_after_transition: str,
    source_receipt_lineage: dict[str, Any],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return session-transition JSON + report with sealed hash."""

    basis = build_operator_local_session_transition_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        operator_local_session_sha256=operator_local_session_sha256,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        campaign_root_manifest_sha256=campaign_root_manifest_sha256,
        ordered_run_ids=ordered_run_ids,
        transition_type=transition_type,
        transition_rule_id=transition_rule_id,
        current_run_id_after_transition=current_run_id_after_transition,
        source_receipt_lineage=source_receipt_lineage,
        non_claims=non_claims,
    )
    seal = _seal_transition_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "operator_local_session_transition_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_operator_local_session_transition_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_REPORT_CONTRACT_ID,
        "operator_local_session_transition_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "transition_type": transition_type,
            "transition_rule_id": transition_rule_id,
            "current_run_id_after_transition": current_run_id_after_transition,
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
