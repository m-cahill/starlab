"""Governed bounded operator-local multi-run session record (PX2-M03 slice 8)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_continuity import EXECUTION_KIND_SLICE8
from starlab.sc2.px2.self_play.campaign_root import recommended_operator_out_campaign_root_path

PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_session.v1"
)
PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_operator_local_session_report.v1"
)
OPERATOR_LOCAL_SESSION_RECORD_VERSION: Final[str] = "px2_m03_slice8_bounded_session_v1"


def _seal_session_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_operator_local_session_seal_basis(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    ordered_run_ids: tuple[str, ...],
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    per_run: tuple[dict[str, str], ...],
    non_claims: list[str],
) -> dict[str, Any]:
    """Logical fields sealed as ``operator_local_session_sha256`` (no absolute paths)."""

    return {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID,
        "operator_local_session_record_version": OPERATOR_LOCAL_SESSION_RECORD_VERSION,
        "execution_kind": EXECUTION_KIND_SLICE8,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "ordered_run_ids": list(ordered_run_ids),
        "recommended_campaign_root_logical": recommended_operator_out_campaign_root_path(
            campaign_id
        ),
        "campaign_contract_sha256": campaign_contract_sha256,
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "campaign_root_manifest_sha256": campaign_root_manifest_sha256,
        "per_run": list(per_run),
        "non_claims": non_claims,
    }


def build_px2_self_play_operator_local_session_artifacts(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    campaign_root_resolved: Path,
    campaign_contract_sha256: str,
    opponent_pool_identity_sha256: str,
    campaign_root_manifest_sha256: str,
    ordered_run_ids: tuple[str, ...],
    per_run: tuple[dict[str, str], ...],
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return session JSON + report with sealed ``operator_local_session_sha256``."""

    basis = build_operator_local_session_seal_basis(
        campaign_id=campaign_id,
        campaign_profile_id=campaign_profile_id,
        ordered_run_ids=ordered_run_ids,
        campaign_contract_sha256=campaign_contract_sha256,
        opponent_pool_identity_sha256=opponent_pool_identity_sha256,
        campaign_root_manifest_sha256=campaign_root_manifest_sha256,
        per_run=per_run,
        non_claims=non_claims,
    )
    seal = _seal_session_body(basis)
    root_posix = campaign_root_resolved.resolve().as_posix()

    manifest: dict[str, Any] = {
        **basis,
        "operator_local_session_sha256": seal,
        "operator_note_convention": (
            "Optional human note (not sealed): "
            f"``{recommended_operator_out_campaign_root_path(campaign_id)}"
            "px2_operator_local_session_operator_note.md``"
        ),
        "campaign_root_resolved_posix": root_posix,
    }

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_REPORT_CONTRACT_ID,
        "operator_local_session_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "session_run_count": len(ordered_run_ids),
            "ordered_run_ids": list(ordered_run_ids),
        },
        "operator_absolute_paths_advisory": {
            "campaign_root": root_posix,
            "runs_prefix": "runs/",
        },
        "non_claims": non_claims,
    }
    return manifest, report
