"""Constants for replay-derived imitation baseline artifacts (M27)."""

from __future__ import annotations

from typing import Final

BASELINE_VERSION: Final[str] = "starlab.replay_imitation_baseline.v1"
BASELINE_REPORT_VERSION: Final[str] = "starlab.replay_imitation_baseline_report.v1"

MODEL_FAMILY: Final[str] = "starlab.m27.model.observation_signature_majority_v1"
FEATURE_POLICY_ID: Final[str] = "starlab.m27.feature.observation_signature_v1"

REPLAY_IMITATION_BASELINE_FILENAME: Final[str] = "replay_imitation_baseline.json"
REPLAY_IMITATION_BASELINE_REPORT_FILENAME: Final[str] = "replay_imitation_baseline_report.json"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "hierarchical_control",
    "imitation_quality_beyond_internal_smoke",
    "leaderboard_validity",
    "learned_agent_evaluation_harness_m28",
    "live_sc2_execution",
    "m29_plus_work",
    "raw_replay_parser_execution_in_m27_modules",
    "replay_execution_equivalence",
)
