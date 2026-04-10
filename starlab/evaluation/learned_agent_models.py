"""Constants for learned-agent evaluation artifacts (M28)."""

from __future__ import annotations

from typing import Final

EVALUATION_VERSION: Final[str] = "starlab.learned_agent_evaluation.v1"
EVALUATION_REPORT_VERSION: Final[str] = "starlab.learned_agent_evaluation_report.v1"

LEARNED_AGENT_EVALUATION_FILENAME: Final[str] = "learned_agent_evaluation.json"
LEARNED_AGENT_EVALUATION_REPORT_FILENAME: Final[str] = "learned_agent_evaluation_report.json"

# Contract metric ids (v1); must match ``tests/fixtures/m28/benchmark_contract_m28.json``.
M28_METRIC_IDS_ORDERED: Final[tuple[str, ...]] = (
    "accuracy",
    "macro_f1",
    "fallback_rate",
    "example_count",
)

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "leaderboard_validity",
    "live_sc2_execution",
    "m23_tournament_semantics",
    "m24_diagnostics_surfaces",
    "m25_evidence_pack_surfaces",
    "replay_execution_equivalence",
    "replay_parser_in_m28_modules",
    "stronger_imitation_quality_than_explicit_metrics",
)
