"""Constants and version strings for M24 evaluation diagnostics artifacts."""

from __future__ import annotations

EVALUATION_DIAGNOSTICS_VERSION = "starlab.evaluation_diagnostics.v1"
EVALUATION_DIAGNOSTICS_REPORT_VERSION = "starlab.evaluation_diagnostics_report.v1"

EVALUATION_DIAGNOSTICS_FILENAME = "evaluation_diagnostics.json"
EVALUATION_DIAGNOSTICS_REPORT_FILENAME = "evaluation_diagnostics_report.json"

# Governed M23 tournament document version (structural gate for diagnostics input).
REQUIRED_TOURNAMENT_VERSION = "starlab.evaluation_tournament.v1"

# Diagnostics-level non-claims (sorted lexicographically at emission).
EVALUATION_DIAGNOSTICS_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m24.diagnostics_non_claim.not_benchmark_integrity",
    "starlab.m24.diagnostics_non_claim.not_leaderboard_validity_beyond_fixture",
    "starlab.m24.diagnostics_non_claim.not_live_gameplay",
    "starlab.m24.diagnostics_non_claim.not_new_benchmark_semantics",
    "starlab.m24.diagnostics_non_claim.not_replay_derived_evidence",
    "starlab.m24.diagnostics_non_claim.not_root_cause_outside_tournament_artifact",
)

EVALUATION_DIAGNOSTICS_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m24.warning.fixture_only_diagnostics_consumer",
)
