"""Constants and vocabulary for the M22 heuristic baseline suite."""

from __future__ import annotations

# Suite / report document versions (governance).
HEURISTIC_BASELINE_SUITE_VERSION = "starlab.heuristic_baseline_suite.v1"
HEURISTIC_BASELINE_SUITE_REPORT_VERSION = "starlab.heuristic_baseline_suite_report.v1"

# Stable suite identity for the M22 reference suite (deterministic goldens).
HEURISTIC_BASELINE_SUITE_ID = "starlab.heuristic_baseline_suite.m22.v1.demo"

# Artifact filenames (CLI / tests).
HEURISTIC_BASELINE_SUITE_FILENAME = "heuristic_baseline_suite.json"
HEURISTIC_BASELINE_SUITE_REPORT_FILENAME = "heuristic_baseline_suite_report.json"

# Fixed subject order (exactly two heuristic subjects for M22).
HEURISTIC_BASELINE_SUBJECT_IDS: tuple[str, ...] = (
    "heuristic_economy_first_v1",
    "heuristic_pressure_first_v1",
)

# Per-subject deterministic fixture metric values: metric_id -> value (count or ratio).
HEURISTIC_BASELINE_SUBJECT_METRIC_VALUES: dict[str, dict[str, float | int]] = {
    "heuristic_economy_first_v1": {"m1": 8, "m2": 0.15},
    "heuristic_pressure_first_v1": {"m1": 12, "m2": 0.35},
}

# Fixed fixture case order (exactly one case for M22).
HEURISTIC_BASELINE_FIXTURE_CASE_IDS: tuple[str, ...] = ("fc_m22_001",)

# Suite-level verdicts for reports.
SUITE_VERDICT_PASS = "pass"

# Default suite-level warnings (sorted lexicographically at emission).
HEURISTIC_BASELINE_SUITE_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m22.warning.fixture_only_heuristic_suite",
)

# Suite-level non-claims (sorted lexicographically at emission).
HEURISTIC_BASELINE_SUITE_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m22.suite_non_claim.not_benchmark_integrity",
    "starlab.m22.suite_non_claim.not_evaluation_runner",
    "starlab.m22.suite_non_claim.not_replay_execution_equivalence",
)

# Scorecard-level non-claims for M22 embedded scorecards (sorted at emission).
HEURISTIC_BASELINE_SCORECARD_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m22.scorecard_non_claim.not_benchmark_integrity",
    "starlab.m22.scorecard_non_claim.not_replay_execution_equivalence",
)

# Scorecard-level warnings (sorted at emission).
HEURISTIC_BASELINE_SCORECARD_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m22.warning.fixture_only_heuristic_scorecard",
)
