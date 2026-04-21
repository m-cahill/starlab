"""Governed bounded second-hop continuation record (PX2-M03 slice 13)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_second_hop_continuation.v1"
)
PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_second_hop_continuation_report.v1"
)
SECOND_HOP_CONTINUATION_RECORD_VERSION: Final[str] = "px2_m03_slice13_second_hop_continuation_v1"

SECOND_HOP_RULE_AFTER_SLICE12_REANCHOR_STUB: Final[str] = (
    "px2_m03_slice13_second_hop_after_slice12_reanchor_stub_v1"
)


def _seal_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_second_hop_continuation_seal_basis(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    second_hop_rule_id: str,
    prior_post_slice12_current_candidate_sha256: str,
    prior_first_hop_continuation_run_sha256: str,
    prior_slice12_reanchor_sha256: str,
    second_hop_continuation_run_id: str,
    second_hop_continuation_run_sha256: str | None,
    root_continuation_run_sha256: str | None,
    prior_campaign_root_manifest_sha256: str,
    updated_campaign_root_manifest_sha256: str | None,
    second_hop_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``second_hop_continuation_sha256``."""

    return {
        "contract_id": PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_CONTRACT_ID,
        "second_hop_continuation_record_version": SECOND_HOP_CONTINUATION_RECORD_VERSION,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "second_hop_rule_id": second_hop_rule_id,
        "prior_post_slice12_current_candidate_sha256": prior_post_slice12_current_candidate_sha256,
        "prior_first_hop_continuation_run_sha256": prior_first_hop_continuation_run_sha256,
        "prior_slice12_reanchor_sha256": prior_slice12_reanchor_sha256,
        "second_hop_continuation_run_id": second_hop_continuation_run_id,
        "second_hop_continuation_run_sha256": second_hop_continuation_run_sha256,
        "root_continuation_run_artifact_sha256": root_continuation_run_sha256,
        "prior_campaign_root_manifest_sha256": prior_campaign_root_manifest_sha256,
        "updated_campaign_root_manifest_sha256": updated_campaign_root_manifest_sha256,
        "second_hop_status": second_hop_status,
        "mismatch_reasons": list(mismatch_reasons),
        "non_claims": non_claims,
    }


def build_px2_self_play_second_hop_continuation_artifacts(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    second_hop_rule_id: str,
    prior_post_slice12_current_candidate_sha256: str,
    prior_first_hop_continuation_run_sha256: str,
    prior_slice12_reanchor_sha256: str,
    second_hop_continuation_run_id: str,
    second_hop_continuation_run_sha256: str | None,
    root_continuation_run_sha256: str | None,
    prior_campaign_root_manifest_sha256: str,
    updated_campaign_root_manifest_sha256: str | None,
    second_hop_status: str,
    mismatch_reasons: list[str],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return second-hop continuation JSON + report with sealed hash."""

    basis = build_second_hop_continuation_seal_basis(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        second_hop_rule_id=second_hop_rule_id,
        prior_post_slice12_current_candidate_sha256=prior_post_slice12_current_candidate_sha256,
        prior_first_hop_continuation_run_sha256=prior_first_hop_continuation_run_sha256,
        prior_slice12_reanchor_sha256=prior_slice12_reanchor_sha256,
        second_hop_continuation_run_id=second_hop_continuation_run_id,
        second_hop_continuation_run_sha256=second_hop_continuation_run_sha256,
        root_continuation_run_sha256=root_continuation_run_sha256,
        prior_campaign_root_manifest_sha256=prior_campaign_root_manifest_sha256,
        updated_campaign_root_manifest_sha256=updated_campaign_root_manifest_sha256,
        second_hop_status=second_hop_status,
        mismatch_reasons=mismatch_reasons,
        non_claims=non_claims,
    )
    seal = _seal_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "second_hop_continuation_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_second_hop_continuation_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_SECOND_HOP_CONTINUATION_REPORT_CONTRACT_ID,
        "second_hop_continuation_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "second_hop_status": second_hop_status,
            "second_hop_continuation_run_id": second_hop_continuation_run_id,
            "mismatch_reasons": list(mismatch_reasons),
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
        },
        "non_claims": non_claims,
    }
    return manifest, report
