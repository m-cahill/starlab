"""Governed post-continuation current-candidate re-anchor record (PX2-M03 slice 12)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_current_candidate_reanchor.v1"
)
PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_current_candidate_reanchor_report.v1"
)
REANCHOR_RECORD_VERSION: Final[str] = "px2_m03_slice12_current_candidate_reanchor_v1"
REANCHOR_RECORD_VERSION_SLICE13: Final[str] = (
    "px2_m03_slice13_current_candidate_reanchor_second_hop_v1"
)

REANCHOR_RULE_POST_CONTINUATION_STUB: Final[str] = (
    "px2_m03_slice12_reanchor_after_consumed_continuation_stub_v1"
)
REANCHOR_RULE_POST_SECOND_HOP_STUB: Final[str] = (
    "px2_m03_slice13_reanchor_after_consumed_second_hop_stub_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_current_candidate_reanchor_seal_basis(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    reanchor_rule_id: str,
    prior_current_candidate_sha256: str,
    prior_continuation_run_sha256: str,
    continuation_run_id: str,
    refreshed_current_candidate_sha256: str | None,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    continuation_consumption_status_observed: str,
    reanchor_status: str,
    rejection_reasons: list[str],
    non_claims: list[str],
    current_candidate_reanchor_record_version: str | None = None,
    prior_first_hop_continuation_run_sha256: str = "",
    prior_slice12_reanchor_sha256: str = "",
) -> dict[str, Any]:
    """Logical fields sealed as ``current_candidate_reanchor_sha256``."""

    rec_ver = (
        current_candidate_reanchor_record_version
        if current_candidate_reanchor_record_version is not None
        else REANCHOR_RECORD_VERSION
    )
    return {
        "contract_id": PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_CONTRACT_ID,
        "current_candidate_reanchor_record_version": rec_ver,
        "execution_kind": execution_kind,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "reanchor_rule_id": reanchor_rule_id,
        "prior_current_candidate_sha256": prior_current_candidate_sha256,
        "prior_continuation_run_sha256": prior_continuation_run_sha256,
        "continuation_run_id": continuation_run_id,
        "refreshed_current_candidate_sha256": refreshed_current_candidate_sha256,
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "campaign_root_manifest_sha256": campaign_root_manifest_sha256,
        "continuation_consumption_status_observed": continuation_consumption_status_observed,
        "reanchor_status": reanchor_status,
        "rejection_reasons": list(rejection_reasons),
        "non_claims": non_claims,
        "prior_first_hop_continuation_run_sha256": prior_first_hop_continuation_run_sha256,
        "prior_slice12_reanchor_sha256": prior_slice12_reanchor_sha256,
    }


def build_px2_self_play_current_candidate_reanchor_artifacts(
    *,
    execution_kind: str,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    reanchor_rule_id: str,
    prior_current_candidate_sha256: str,
    prior_continuation_run_sha256: str,
    continuation_run_id: str,
    refreshed_current_candidate_sha256: str | None,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    continuation_consumption_status_observed: str,
    reanchor_status: str,
    rejection_reasons: list[str],
    non_claims: list[str],
    current_candidate_reanchor_record_version: str | None = None,
    prior_first_hop_continuation_run_sha256: str = "",
    prior_slice12_reanchor_sha256: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return re-anchor JSON + report with sealed hash."""

    basis = build_current_candidate_reanchor_seal_basis(
        execution_kind=execution_kind,
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        reanchor_rule_id=reanchor_rule_id,
        prior_current_candidate_sha256=prior_current_candidate_sha256,
        prior_continuation_run_sha256=prior_continuation_run_sha256,
        continuation_run_id=continuation_run_id,
        refreshed_current_candidate_sha256=refreshed_current_candidate_sha256,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        campaign_root_manifest_sha256=campaign_root_manifest_sha256,
        continuation_consumption_status_observed=continuation_consumption_status_observed,
        reanchor_status=reanchor_status,
        rejection_reasons=rejection_reasons,
        non_claims=non_claims,
        current_candidate_reanchor_record_version=current_candidate_reanchor_record_version,
        prior_first_hop_continuation_run_sha256=prior_first_hop_continuation_run_sha256,
        prior_slice12_reanchor_sha256=prior_slice12_reanchor_sha256,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "current_candidate_reanchor_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_current_candidate_reanchor_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CURRENT_CANDIDATE_REANCHOR_REPORT_CONTRACT_ID,
        "current_candidate_reanchor_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "reanchor_status": reanchor_status,
            "continuation_run_id": continuation_run_id,
            "continuation_consumption_status_observed": continuation_consumption_status_observed,
            "rejection_reasons": list(rejection_reasons),
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
