"""Explicit rollback receipt surfaces (PX2-M03 slice 4 — stub transitions)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json

PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID: Final[str] = "starlab.px2.self_play_rollback_receipt.v1"
PX2_SELF_PLAY_ROLLBACK_RECEIPT_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_rollback_receipt_report.v1"
)

ROLLBACK_TRANSITION_SLICE4_STUB: Final[str] = "starlab.px2.rollback_transition.slice4_stub_v1"


def seal_rollback_receipt_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_rollback_receipt_artifacts(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    preflight_sha256: str,
    continuity_step_index_zero_based: int,
    linked_promotion_receipt_sha256: str,
    triggered: bool,
    rollback_reason: str | None,
    would_revert_to_checkpoint_receipt_sha256: str | None,
    transition_logic_id: str = ROLLBACK_TRANSITION_SLICE4_STUB,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(receipt, report)`` for rollback posture at a step boundary."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "preflight_sha256": preflight_sha256,
        "continuity_step_index_zero_based": continuity_step_index_zero_based,
        "linked_promotion_receipt_sha256": linked_promotion_receipt_sha256,
        "triggered": triggered,
        "rollback_reason": rollback_reason,
        "would_revert_to_checkpoint_receipt_sha256": would_revert_to_checkpoint_receipt_sha256,
        "transition_logic_id": transition_logic_id,
        "non_claims": [
            "Slice-4 rollback receipt — default path does not trigger rollback.",
            "Does not prove automated revert in industrial runs or PX2-M04 exploit handling.",
        ],
    }
    seal = seal_rollback_receipt_body(body)
    receipt = dict(body)
    receipt["rollback_receipt_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_ROLLBACK_RECEIPT_REPORT_CONTRACT_ID,
        "rollback_receipt_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "triggered": triggered,
            "continuity_step_index_zero_based": continuity_step_index_zero_based,
        },
        "non_claims": body["non_claims"],
    }
    return receipt, report
