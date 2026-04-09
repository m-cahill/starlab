"""Constants and controlled vocabularies for benchmark contract + scorecard (M20)."""

from __future__ import annotations

# Contract / profile identifiers (governance + reports).
BENCHMARK_CONTRACT_CONTRACT = "starlab.benchmark_contract.v1"
BENCHMARK_CONTRACT_PROFILE = "starlab.benchmark_contract.m20.v1"
BENCHMARK_SCORECARD_CONTRACT = "starlab.benchmark_scorecard.v1"
BENCHMARK_SCORECARD_PROFILE = "starlab.benchmark_scorecard.m20.v1"

# Document ``schema_version`` values (instances validated by emitted JSON Schemas).
BENCHMARK_CONTRACT_DOCUMENT_SCHEMA_VERSION = "starlab.benchmark_contract.v1"
BENCHMARK_SCORECARD_DOCUMENT_SCHEMA_VERSION = "starlab.benchmark_scorecard.v1"

# Emitted JSON Schema document identities ($id).
BENCHMARK_CONTRACT_JSON_SCHEMA_ID = "starlab.benchmark_contract.m20.v1.schema.json"
BENCHMARK_SCORECARD_JSON_SCHEMA_ID = "starlab.benchmark_scorecard.m20.v1.schema.json"

# Artifact filenames (CLI / tests / governance).
BENCHMARK_CONTRACT_SCHEMA_FILENAME = "benchmark_contract_schema.json"
BENCHMARK_CONTRACT_SCHEMA_REPORT_FILENAME = "benchmark_contract_schema_report.json"
BENCHMARK_SCORECARD_SCHEMA_FILENAME = "benchmark_scorecard_schema.json"
BENCHMARK_SCORECARD_SCHEMA_REPORT_FILENAME = "benchmark_scorecard_schema_report.json"

# Controlled vocabularies (locked M20).
SCORING_STATUS_VALUES: tuple[str, ...] = ("scored", "unscored", "disqualified")
COMPARABILITY_STATUS_VALUES: tuple[str, ...] = ("comparable", "provisional", "non_comparable")
MEASUREMENT_SURFACE_VALUES: tuple[str, ...] = (
    "fixture_only",
    "replay_only",
    "runtime_execution",
    "hybrid",
)
EVALUATION_POSTURE_VALUES: tuple[str, ...] = (
    "contract_only",
    "fixture_only",
    "replay_backed",
    "runtime_backed",
    "hybrid",
)
SUBJECT_KINDS_ALLOWED_VALUES: tuple[str, ...] = (
    "scripted",
    "heuristic",
    "imitation",
    "hierarchical",
    "rl",
    "human_replay",
)

OPTIMIZATION_DIRECTION_VALUES: tuple[str, ...] = ("minimize", "maximize", "none")
AGGREGATION_METHOD_VALUES: tuple[str, ...] = (
    "sum",
    "mean",
    "min",
    "max",
    "weighted_mean",
    "last",
)
SCORING_ROLE_VALUES: tuple[str, ...] = ("primary", "secondary", "diagnostic", "informational")
GATING_RULE_SEVERITY_VALUES: tuple[str, ...] = ("hard", "soft")
AGGREGATION_POLICY_KIND_VALUES: tuple[str, ...] = ("weighted_sum", "min", "max", "lexicographic")

# Default non-claims recorded on schema reports (bounded; not exhaustive).
BENCHMARK_CONTRACT_REPORT_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m20.benchmark_contract_non_claim.not_benchmark_integrity",
    "starlab.m20.benchmark_contract_non_claim.not_replay_execution_equivalence",
    "starlab.m20.benchmark_contract_non_claim.not_baseline_performance",
)

BENCHMARK_SCORECARD_REPORT_NON_CLAIMS_V1: tuple[str, ...] = (
    "starlab.m20.benchmark_scorecard_non_claim.not_benchmark_integrity",
    "starlab.m20.benchmark_scorecard_non_claim.not_replay_execution_equivalence",
    "starlab.m20.benchmark_scorecard_non_claim.schema_only_not_run_truth",
)

# Deterministic ordering for reports (lexicographic).
ORDERED_BENCHMARK_CONTRACT_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "aggregation_policy",
    "benchmark_id",
    "benchmark_name",
    "benchmark_version",
    "gating_rules",
    "input_requirements",
    "measurement_surface",
    "metric_definitions",
    "non_claims",
    "schema_version",
    "scorecard_schema_ref",
    "subject_kinds_allowed",
)

ORDERED_SCORECARD_TOP_LEVEL_KEYS: tuple[str, ...] = (
    "aggregate_scores",
    "benchmark_contract_sha256",
    "benchmark_id",
    "benchmark_version",
    "comparability_status",
    "evaluation_posture",
    "gating_outcomes",
    "metric_rows",
    "non_claims",
    "schema_version",
    "scoring_status",
    "subject_ref",
    "warnings",
)
