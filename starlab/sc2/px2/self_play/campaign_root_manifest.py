"""Sealed operator-local campaign-root manifest (PX2-M03 slice 5)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.campaign_contract import PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID

PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_root_manifest.v1"
)
PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_root_manifest_report.v1"
)


def seal_campaign_root_manifest_body(body_without_seal: dict[str, Any]) -> str:
    """SHA-256 (hex) over canonical JSON of the body without ``campaign_root_manifest_sha256``."""

    return sha256_hex_of_canonical_json(body_without_seal)


def build_px2_self_play_campaign_root_manifest_artifacts(
    *,
    campaign_id: str,
    campaign_contract_sha256: str,
    root_path_expected: str,
    allowed_subdirectories: tuple[str, ...],
    run_subdirectory_receipt_layout: dict[str, str],
    continuity_run_references: tuple[dict[str, str], ...],
    opponent_pool_identity_sha256: str,
    opponent_selection_rule_id: str,
    non_claims: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(manifest_json, report_json)`` with sealed ``campaign_root_manifest_sha256``."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID,
        "campaign_id": campaign_id,
        "linked_campaign_contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "campaign_contract_sha256": campaign_contract_sha256,
        "root_path_expected": root_path_expected,
        "allowed_subdirectories": list(allowed_subdirectories),
        "run_subdirectory_receipt_layout": run_subdirectory_receipt_layout,
        "continuity_run_references": list(continuity_run_references),
        "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
        "opponent_selection_rule_id": opponent_selection_rule_id,
        "non_claims": non_claims,
    }
    seal = seal_campaign_root_manifest_body(body)
    manifest = dict(body)
    manifest["campaign_root_manifest_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_REPORT_CONTRACT_ID,
        "campaign_root_manifest_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "continuity_run_count": len(continuity_run_references),
            "opponent_pool_identity_sha256": opponent_pool_identity_sha256,
            "campaign_root_resolved_note": (
                "Absolute path varies by operator machine; sealed manifest uses canonical "
                "`out/px2_self_play_campaigns/<campaign_id>/` expectation only."
            ),
        },
        "non_claims": non_claims,
    }
    return manifest, report
