"""Governed bounded continuation run record (PX2-M03 slice 11)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID: Final[str] = "starlab.px2.self_play_continuation_run.v1"
PX2_SELF_PLAY_CONTINUATION_RUN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_continuation_run_report.v1"
)
CONTINUATION_RUN_RECORD_VERSION: Final[str] = "px2_m03_slice11_continuation_run_v1"

CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB: Final[str] = (
    "px2_m03_slice11_consume_current_candidate_stub_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_continuation_run_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    continuation_rule_id: str,
    current_candidate_sha256: str,
    operator_local_session_sha256: str,
    operator_local_session_transition_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    prior_campaign_root_manifest_sha256: str,
    consumed_checkpoint_receipt_sha256: str,
    continuation_run_id: str,
    continuation_continuity_sha256: str | None,
    consumption_status: str,
    mismatch_reasons: list[str],
    updated_campaign_root_manifest_sha256: str | None,
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``continuation_run_sha256``."""

    return {
        "contract_id": PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID,
        "continuation_run_record_version": CONTINUATION_RUN_RECORD_VERSION,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "continuation_rule_id": continuation_rule_id,
        "current_candidate_sha256": current_candidate_sha256,
        "operator_local_session_sha256": operator_local_session_sha256,
        "operator_local_session_transition_sha256": operator_local_session_transition_sha256,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "prior_campaign_root_manifest_sha256": prior_campaign_root_manifest_sha256,
        "consumed_checkpoint_receipt_sha256": consumed_checkpoint_receipt_sha256,
        "continuation_run_id": continuation_run_id,
        "continuation_continuity_sha256": continuation_continuity_sha256,
        "consumption_status": consumption_status,
        "mismatch_reasons": list(mismatch_reasons),
        "updated_campaign_root_manifest_sha256": updated_campaign_root_manifest_sha256,
        "non_claims": non_claims,
    }


def build_px2_self_play_continuation_run_artifacts(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    continuation_rule_id: str,
    current_candidate_sha256: str,
    operator_local_session_sha256: str,
    operator_local_session_transition_sha256: str,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    prior_campaign_root_manifest_sha256: str,
    consumed_checkpoint_receipt_sha256: str,
    continuation_run_id: str,
    continuation_continuity_sha256: str | None,
    consumption_status: str,
    mismatch_reasons: list[str],
    updated_campaign_root_manifest_sha256: str | None,
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return continuation-run JSON + report with sealed hash."""

    basis = build_continuation_run_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        continuation_rule_id=continuation_rule_id,
        current_candidate_sha256=current_candidate_sha256,
        operator_local_session_sha256=operator_local_session_sha256,
        operator_local_session_transition_sha256=operator_local_session_transition_sha256,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        prior_campaign_root_manifest_sha256=prior_campaign_root_manifest_sha256,
        consumed_checkpoint_receipt_sha256=consumed_checkpoint_receipt_sha256,
        continuation_run_id=continuation_run_id,
        continuation_continuity_sha256=continuation_continuity_sha256,
        consumption_status=consumption_status,
        mismatch_reasons=mismatch_reasons,
        updated_campaign_root_manifest_sha256=updated_campaign_root_manifest_sha256,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "continuation_run_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_continuation_run_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CONTINUATION_RUN_REPORT_CONTRACT_ID,
        "continuation_run_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "consumption_status": consumption_status,
            "continuation_run_id": continuation_run_id,
            "mismatch_reasons": list(mismatch_reasons),
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
