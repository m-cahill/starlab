"""Constants and version strings for M25 baseline evidence pack artifacts."""

from __future__ import annotations

BASELINE_EVIDENCE_PACK_VERSION = "starlab.baseline_evidence_pack.v1"
BASELINE_EVIDENCE_PACK_REPORT_VERSION = "starlab.baseline_evidence_pack_report.v1"

BASELINE_EVIDENCE_PACK_FILENAME = "baseline_evidence_pack.json"
BASELINE_EVIDENCE_PACK_REPORT_FILENAME = "baseline_evidence_pack_report.json"

REQUIRED_TOURNAMENT_VERSION = "starlab.evaluation_tournament.v1"
REQUIRED_DIAGNOSTICS_VERSION = "starlab.evaluation_diagnostics.v1"

# M25-level non-claims (sorted lexicographically at emission).
BASELINE_EVIDENCE_PACK_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m25.pack_non_claim.not_benchmark_integrity",
    "starlab.m25.pack_non_claim.not_leaderboard_validity_beyond_upstream",
    "starlab.m25.pack_non_claim.not_live_sc2_or_replay_execution",
    "starlab.m25.pack_non_claim.not_m26_imitation_or_learning",
    "starlab.m25.pack_non_claim.not_new_benchmark_semantics",
    "starlab.m25.pack_non_claim.not_new_diagnostics_or_scoring",
    "starlab.m25.pack_non_claim.not_raw_replay_or_archive_packaging",
    "starlab.m25.pack_non_claim.not_replay_execution_equivalence",
)

BASELINE_EVIDENCE_PACK_WARNINGS_V1: tuple[str, ...] = (
    "starlab.m25.warning.fixture_only_evidence_packaging_layer",
)

# Stable failure-view ids (entrant-scoped projection of M24 failure_views buckets).
FAILURE_VIEW_ZERO_WIN = "starlab.m25.failure_view.zero_win_entrant"
FAILURE_VIEW_LOWEST_POINTS = "starlab.m25.failure_view.lowest_points_entrant"
FAILURE_VIEW_DRAW_EQUAL_PRIMARY = "starlab.m25.failure_view.draw_equal_primary_metric"
FAILURE_VIEW_TIEBREAK_SCALAR = "starlab.m25.failure_view.standings_used_tiebreak_scalar"
FAILURE_VIEW_LEXICOGRAPHIC = "starlab.m25.failure_view.standings_used_lexicographic_tiebreak"
