"""Bounded evaluation receipt artifacts (PX2-M03 slice 2 skeleton)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json

PX2_SELF_PLAY_EVALUATION_RECEIPT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_evaluation_receipt.v1"
)
PX2_SELF_PLAY_EVALUATION_RECEIPT_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_evaluation_receipt_report.v1"
)


def seal_evaluation_receipt_body(body_without_seal: dict[str, Any]) -> str:
    """SHA-256 over canonical JSON without ``evaluation_receipt_sha256``."""

    return sha256_hex_of_canonical_json(body_without_seal)


def build_evaluation_receipt_artifacts(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    episode_index_one_based: int,
    games_completed_in_run: int,
    eval_modes: list[str],
    metrics_stub: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(receipt, report)`` for one evaluation boundary."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EVALUATION_RECEIPT_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "episode_index_one_based": episode_index_one_based,
        "games_completed_in_run": games_completed_in_run,
        "eval_kind": "slice2_skeleton_fixture",
        "eval_modes": eval_modes,
        "metrics_stub": metrics_stub,
        "non_claims": [
            "Fixture eval receipt only — not a real match outcome distribution.",
            "Does not prove ladder or industrial eval quality.",
        ],
    }
    seal = seal_evaluation_receipt_body(body)
    receipt = dict(body)
    receipt["evaluation_receipt_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EVALUATION_RECEIPT_REPORT_CONTRACT_ID,
        "evaluation_receipt_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "episode_index_one_based": episode_index_one_based,
            "metrics_stub_keys": sorted(metrics_stub.keys()),
        },
        "non_claims": body["non_claims"],
    }
    return receipt, report


def build_slice4_evaluation_receipt_artifacts(
    *,
    campaign_id: str,
    run_id: str,
    campaign_sha256: str,
    linked_campaign_contract_id: str,
    preflight_sha256: str,
    weight_identity: dict[str, Any],
    continuity_step_index_zero_based: int,
    episode_index_one_based: int,
    games_completed_in_run: int,
    link_checkpoint_receipt_sha256: str,
    eval_modes: list[str],
    metrics_stub: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Evaluation receipt with slice-4 linkage to checkpoint and preflight."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EVALUATION_RECEIPT_CONTRACT_ID,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "campaign_sha256": campaign_sha256,
        "linked_campaign_contract_id": linked_campaign_contract_id,
        "preflight_sha256": preflight_sha256,
        "weight_identity": weight_identity,
        "continuity_step_index_zero_based": continuity_step_index_zero_based,
        "episode_index_one_based": episode_index_one_based,
        "games_completed_in_run": games_completed_in_run,
        "eval_kind": "slice4_operator_local_continuity",
        "link_checkpoint_receipt_sha256": link_checkpoint_receipt_sha256,
        "eval_modes": eval_modes,
        "metrics_stub": metrics_stub,
        "non_claims": [
            "Slice-4 continuity eval — not a real match outcome distribution.",
            "Does not prove ladder, industrial eval, or promotion eligibility.",
        ],
    }
    seal = seal_evaluation_receipt_body(body)
    receipt = dict(body)
    receipt["evaluation_receipt_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EVALUATION_RECEIPT_REPORT_CONTRACT_ID,
        "evaluation_receipt_sha256": seal,
        "campaign_id": campaign_id,
        "run_id": run_id,
        "summary": {
            "continuity_step_index_zero_based": continuity_step_index_zero_based,
            "link_checkpoint_receipt_sha256": link_checkpoint_receipt_sha256,
            "metrics_stub_keys": sorted(metrics_stub.keys()),
        },
        "non_claims": body["non_claims"],
    }
    return receipt, report
