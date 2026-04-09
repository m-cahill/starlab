"""Constants for M23 evaluation tournament artifacts."""

from __future__ import annotations

EVALUATION_TOURNAMENT_VERSION = "starlab.evaluation_tournament.v1"
EVALUATION_TOURNAMENT_REPORT_VERSION = "starlab.evaluation_tournament_report.v1"

# Stable tournament identity for the M23 reference harness (deterministic goldens).
EVALUATION_TOURNAMENT_ID = "starlab.evaluation_tournament.m23.v1.demo"

EVALUATION_TOURNAMENT_FILENAME = "evaluation_tournament.json"
EVALUATION_TOURNAMENT_REPORT_FILENAME = "evaluation_tournament_report.json"

# Governed M21/M22 suite document versions (structural gate).
SCRIPTED_BASELINE_SUITE_VERSION = "starlab.scripted_baseline_suite.v1"
HEURISTIC_BASELINE_SUITE_VERSION = "starlab.heuristic_baseline_suite.v1"

# Tournament-level non-claims (sorted lexicographically at emission).
EVALUATION_TOURNAMENT_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m23.tournament_non_claim.not_attribution_diagnostics",
    "starlab.m23.tournament_non_claim.not_benchmark_integrity",
    "starlab.m23.tournament_non_claim.not_evidence_pack",
    "starlab.m23.tournament_non_claim.not_leaderboard_validity",
    "starlab.m23.tournament_non_claim.not_replay_execution_equivalence",
)

EVALUATION_TOURNAMENT_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m23.warning.fixture_only_tournament_harness",
)
