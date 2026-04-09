"""Constants and vocabulary for the M21 scripted baseline suite."""

from __future__ import annotations

# Suite / report document versions (governance).
SCRIPTED_BASELINE_SUITE_VERSION = "starlab.scripted_baseline_suite.v1"
SCRIPTED_BASELINE_SUITE_REPORT_VERSION = "starlab.scripted_baseline_suite_report.v1"

# Stable suite identity for the M21 reference suite (deterministic goldens).
SCRIPTED_BASELINE_SUITE_ID = "starlab.scripted_baseline_suite.m21.v1.demo"

# Artifact filenames (CLI / tests).
SCRIPTED_BASELINE_SUITE_FILENAME = "scripted_baseline_suite.json"
SCRIPTED_BASELINE_SUITE_REPORT_FILENAME = "scripted_baseline_suite_report.json"

# Fixed subject order (exactly two scripted subjects for M21).
SCRIPTED_BASELINE_SUBJECT_IDS: tuple[str, ...] = (
    "scripted_m21_noop",
    "scripted_m21_fixed",
)

# Per-subject deterministic fixture metric values: metric_id -> value (count or ratio).
# Keys must cover every metric_id in the M21 benchmark contract fixture.
SCRIPTED_BASELINE_SUBJECT_METRIC_VALUES: dict[str, dict[str, float | int]] = {
    "scripted_m21_noop": {"m1": 0, "m2": 0.0},
    "scripted_m21_fixed": {"m1": 10, "m2": 0.25},
}

# Fixed fixture case order (exactly one case for M21).
SCRIPTED_BASELINE_FIXTURE_CASE_IDS: tuple[str, ...] = ("fc_m21_001",)

# Suite-level verdicts for reports.
SUITE_VERDICT_PASS = "pass"

# Default suite-level warnings (sorted lexicographically at emission).
SCRIPTED_BASELINE_SUITE_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m21.warning.fixture_only_scripted_suite",
)

# Suite-level non-claims (sorted lexicographically at emission).
SCRIPTED_BASELINE_SUITE_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m21.suite_non_claim.not_benchmark_integrity",
    "starlab.m21.suite_non_claim.not_heuristic_baseline",
    "starlab.m21.suite_non_claim.not_replay_execution_equivalence",
)

# Scorecard-level non-claims for M21 embedded scorecards (sorted at emission).
SCRIPTED_BASELINE_SCORECARD_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m21.scorecard_non_claim.not_benchmark_integrity",
    "starlab.m21.scorecard_non_claim.not_replay_execution_equivalence",
)

# Scorecard-level warnings (sorted at emission).
SCRIPTED_BASELINE_SCORECARD_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m21.warning.fixture_only_scripted_scorecard",
)
