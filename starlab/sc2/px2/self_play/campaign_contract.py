"""Versioned PX2 self-play campaign contract + report (PX2-M03 slice 1)."""

from __future__ import annotations

from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.feature_adapter import FEATURE_ADAPTER_PROFILE
from starlab.sc2.px2.self_play.opponent_selection import OPPONENT_SELECTION_ROUND_ROBIN
from starlab.sc2.px2.self_play.snapshot_pool import OpponentPoolStub, opponent_pool_to_json_dict

PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID: Final[str] = "starlab.px2.self_play_campaign_contract.v1"
PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_campaign_contract_report.v1"
)


def _non_claims_block() -> list[str]:
    return [
        (
            "This contract describes intent and posture; "
            "it does not prove an industrial self-play run."
        ),
        "Does not prove autonomous strength, ladder performance, or Blackwell completion.",
        "Does not prove compatibility with the legacy M49/M50/M51 sklearn-era executor loop.",
        "Direct torch PX2 loop vs M49 executor adaptation remains PX2-M03 implementation work.",
    ]


def seal_px2_self_play_campaign_body(body_without_seal: dict[str, Any]) -> str:
    """SHA-256 (hex) over canonical JSON of the body without ``campaign_sha256``."""

    return sha256_hex_of_canonical_json(body_without_seal)


def build_px2_self_play_campaign_artifacts(
    *,
    campaign_id: str,
    campaign_profile_id: str,
    opponent_pool: OpponentPoolStub,
    opponent_selection_rule_id: str = OPPONENT_SELECTION_ROUND_ROBIN,
    torch_seed: int = 42,
    seed_policy_notes: str = (
        "Deterministic BootstrapTerranPolicy init; no committed weights in slice 1."
    ),
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(campaign_json, report_json)`` with sealed ``campaign_sha256``."""

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
        "campaign_id": campaign_id,
        "campaign_profile_id": campaign_profile_id,
        "seed_policy_ref": {
            "kind": "bootstrap_terran_policy_deterministic_init",
            "feature_adapter_profile": FEATURE_ADAPTER_PROFILE,
            "torch_seed": torch_seed,
            "notes": seed_policy_notes,
        },
        "opponent_pool": opponent_pool_to_json_dict(opponent_pool),
        "opponent_selection_rule_id": opponent_selection_rule_id,
        "checkpoint_posture": {
            "cadence_games": 100,
            "trigger_mode": "every_n_games",
            "retention_expectation_games": "bounded_operator_disk_quota",
        },
        "eval_posture": {
            "cadence_games": 50,
            "trigger_mode": "every_n_games",
            "modes": ["offline_fixture", "operator_local_eval_deferred"],
        },
        "promotion_posture": {
            "decision_mode": "operator_gated_with_eval_threshold_stub",
            "notes": "Placeholder — real promotion decisions deferred to later PX2-M03 execution.",
        },
        "rollback_posture": {
            "trigger_mode": "eval_regression_or_operator_abort_stub",
            "notes": "Placeholder — smoke runs do not trigger rollback.",
        },
        "artifact_layout_expectations": {
            "campaign_root": "out/px2_self_play_campaigns/<campaign_id>/",
            "checkpoints_relative": "checkpoints/",
            "eval_artifacts_relative": "eval/",
            "smoke_artifacts_relative": "smoke/",
            "operator_local_only_note": "Large trees under out/ are not committed by default.",
        },
        "runtime_modes": [
            "fixture_smoke_cpu",
            "operator_local_blackwell_intent_deferred",
        ],
        "non_claims": _non_claims_block(),
    }
    seal = seal_px2_self_play_campaign_body(body)
    campaign = dict(body)
    campaign["campaign_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_CAMPAIGN_REPORT_CONTRACT_ID,
        "campaign_sha256": seal,
        "campaign_id": campaign_id,
        "summary": {
            "campaign_profile_id": campaign_profile_id,
            "opponent_selection_rule_id": opponent_selection_rule_id,
            "artifact_family": "px2_self_play_campaign_v1",
        },
        "non_claims": _non_claims_block(),
    }
    return campaign, report
