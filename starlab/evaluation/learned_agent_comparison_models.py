"""Constants for learned-agent comparison artifacts (M42)."""

from __future__ import annotations

from typing import Final

COMPARISON_VERSION: Final[str] = "starlab.learned_agent_comparison.v1"
COMPARISON_REPORT_VERSION: Final[str] = "starlab.learned_agent_comparison_report.v1"

LEARNED_AGENT_COMPARISON_FILENAME: Final[str] = "learned_agent_comparison.json"
LEARNED_AGENT_COMPARISON_REPORT_FILENAME: Final[str] = "learned_agent_comparison_report.json"

# Same ordering as M28 metric ids for the shared evaluation surface.
M42_METRIC_IDS_ORDERED: Final[tuple[str, ...]] = (
    "accuracy",
    "macro_f1",
    "fallback_rate",
    "example_count",
)

RANKING_POLICY_ID: Final[str] = "starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1"

EVALUATION_SURFACE_ID: Final[str] = "starlab.m28.learned_agent_metrics_v1"

CANDIDATE_SOURCE_M27: Final[str] = "m27_frozen_baseline"
CANDIDATE_SOURCE_M41: Final[str] = "m41_training_run"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "leaderboard_validity",
    "live_sc2_execution",
    "replay_execution_equivalence",
    "m43_plus_hierarchical_training",
    "m28_scorecard_semantics_in_comparison_only_as_embedded_reference",
    "statistical_significance",
    "weights_in_repo",
)
