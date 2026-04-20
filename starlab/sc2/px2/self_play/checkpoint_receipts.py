"""Bounded checkpoint receipt artifacts (PX2-M03 slice 2 skeleton)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json

PX2_SELF_PLAY_CHECKPOINT_RECEIPT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_checkpoint_receipt.v1"
)
PX2_SELF_PLAY_CHECKPOINT_RECEIPT_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_checkpoint_receipt_report.v1"
)


def seal_checkpoint_receipt_body(body_without_seal: dict[str, Any]) -> str:
    """SHA-256 over canonical JSON without ``checkpoint_receipt_sha256``."""

    return sha256_hex_of_canonical_json(body_without_seal)


def build_checkpoint_receipt_artifacts(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    episode_index_one_based: int,
    games_completed_in_run: int,
    policy_snapshot_note: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(receipt, report)`` for one checkpoint boundary."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CHECKPOINT_RECEIPT_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "episode_index_one_based": episode_index_one_based,
        "games_completed_in_run": games_completed_in_run,
        "checkpoint_kind": "slice2_skeleton_fixture",
        "policy_snapshot_note": policy_snapshot_note,
        "non_claims": [
            "Skeleton checkpoint only — not an industrial campaign persistence proof.",
            "Does not prove promotion eligibility or strength.",
        ],
    }
    seal = seal_checkpoint_receipt_body(body)
    receipt = dict(body)
    receipt["checkpoint_receipt_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CHECKPOINT_RECEIPT_REPORT_CONTRACT_ID,
        "checkpoint_receipt_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "episode_index_one_based": episode_index_one_based,
            "games_completed_in_run": games_completed_in_run,
        },
        "non_claims": body["non_claims"],
    }
    return receipt, report
