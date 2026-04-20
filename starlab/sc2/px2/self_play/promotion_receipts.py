"""Explicit promotion receipt surfaces (PX2-M03 slice 4 — stub transitions)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json

PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_promotion_receipt.v1"
)
PX2_SELF_PLAY_PROMOTION_RECEIPT_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_promotion_receipt_report.v1"
)

PROMOTION_TRANSITION_SLICE4_STUB: Final[str] = (
    "starlab.px2.promotion_transition.slice4_deterministic_stub_v1"
)


def seal_promotion_receipt_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def build_promotion_receipt_artifacts(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    preflight_sha256: str,
    weight_identity: dict[str, Any],
    continuity_step_index_zero_based: int,
    continuity_step_count: int,
    linked_evaluation_receipt_sha256: str,
    prior_promotion_receipt_sha256: str | None,
    decision: str,
    transition_logic_id: str = PROMOTION_TRANSITION_SLICE4_STUB,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(receipt, report)`` for one promotion boundary.

    ``decision`` is recorded explicitly; slice-4 default logic is deterministic/stubbed.
    """

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "preflight_sha256": preflight_sha256,
        "weight_identity": weight_identity,
        "continuity_step_index_zero_based": continuity_step_index_zero_based,
        "continuity_step_count": continuity_step_count,
        "linked_evaluation_receipt_sha256": linked_evaluation_receipt_sha256,
        "prior_promotion_receipt_sha256": prior_promotion_receipt_sha256,
        "decision": decision,
        "transition_logic_id": transition_logic_id,
        "non_claims": [
            "Slice-4 promotion receipt — transition logic may be stubbed; not PX2-M04 closure.",
            "Does not prove exploit resolution or production promotion policy.",
        ],
    }
    seal = seal_promotion_receipt_body(body)
    receipt = dict(body)
    receipt["promotion_receipt_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_PROMOTION_RECEIPT_REPORT_CONTRACT_ID,
        "promotion_receipt_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "decision": decision,
            "continuity_step_index_zero_based": continuity_step_index_zero_based,
        },
        "non_claims": body["non_claims"],
    }
    return receipt, report


def slice4_stub_promotion_decision(
    *,
    step_index_zero_based: int,
    step_count: int,
) -> str:
    """Deterministic non-industrial decision: advance through stub gate until final step."""

    if step_index_zero_based >= step_count - 1:
        return "hold_pending_industrial_campaign"
    return "promote_through_eval_stub_gate"
