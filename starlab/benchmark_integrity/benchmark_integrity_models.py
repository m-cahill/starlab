"""Constants for benchmark integrity charter artifacts (M55 — charter only)."""

from __future__ import annotations

from typing import Final, Literal

CONTRACT_ID: Final[str] = "starlab.benchmark_integrity_charter.v1"

BENCHMARK_INTEGRITY_CHARTER_SCHEMA_VERSION: Final[str] = "starlab.benchmark_integrity_charter.v1"
BENCHMARK_INTEGRITY_CHARTER_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.benchmark_integrity_charter_report.v1"
)

CHARTER_FILENAME: Final[str] = "benchmark_integrity_charter.json"
CHARTER_REPORT_FILENAME: Final[str] = "benchmark_integrity_charter_report.json"

RUNTIME_CONTRACT_REL_PATH: Final[str] = "docs/runtime/benchmark_integrity_charter_v1.md"

EVIDENCE_CLASSES_RESERVED_FOR_M56: Final[tuple[str, ...]] = (
    "benchmark_contract_identity",
    "corpus_provenance_and_promotion",
    "subject_identity_and_freeze",
    "execution_posture_receipts",
    "score_aggregation_reproducibility",
)

CONTROL_FAMILY_ORDER: Final[tuple[str, ...]] = (
    "benchmark_definition_control",
    "corpus_promotion_control",
    "subject_identity_freeze_control",
    "execution_posture_control",
    "score_aggregation_publication_control",
    "acceptance_authority_control",
)

CONTROL_IDS_ORDERED: Final[tuple[str, ...]] = (
    "starlab.m55.control.benchmark_definition_v1",
    "starlab.m55.control.corpus_promotion_v1",
    "starlab.m55.control.subject_identity_freeze_v1",
    "starlab.m55.control.execution_posture_v1",
    "starlab.m55.control.score_aggregation_publication_v1",
    "starlab.m55.control.acceptance_authority_v1",
)

# --- M56 — bounded evidence + reproducibility gates (fixture-only baseline chain v1) ---

BENCHMARK_INTEGRITY_EVIDENCE_CONTRACT_ID: Final[str] = "starlab.benchmark_integrity_evidence.v1"
BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION: Final[str] = "starlab.benchmark_integrity_evidence.v1"
BENCHMARK_INTEGRITY_EVIDENCE_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.benchmark_integrity_evidence_report.v1"
)

BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_CONTRACT_ID: Final[str] = (
    "starlab.benchmark_integrity_reproducibility_gates.v1"
)
BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_SCHEMA_VERSION: Final[str] = (
    "starlab.benchmark_integrity_reproducibility_gates.v1"
)
BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.benchmark_integrity_reproducibility_gates_report.v1"
)

EVIDENCE_FILENAME: Final[str] = "benchmark_integrity_evidence.json"
EVIDENCE_REPORT_FILENAME: Final[str] = "benchmark_integrity_evidence_report.json"
REPRODUCIBILITY_GATES_FILENAME: Final[str] = "benchmark_integrity_reproducibility_gates.json"
REPRODUCIBILITY_GATES_REPORT_FILENAME: Final[str] = (
    "benchmark_integrity_reproducibility_gates_report.json"
)

M56_RUNTIMEV1_EVIDENCE_GATES_REL_PATH: Final[str] = (
    "docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md"
)

M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1: Final[str] = (
    "starlab.m56.scope.fixture_only_baseline_chain_v1"
)
M56_GATEPACK_FIXTURE_ONLY_BASELINE_CHAIN_V1: Final[str] = (
    "starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1"
)

# Evidence row status vocabulary (M56).
EvidenceRowStatus = Literal[
    "present",
    "missing",
    "not_applicable",
    "unavailable_by_design",
    "out_of_scope",
]

# Scope gate outcome (top-level).
M56ScopeGateStatus = Literal[
    "accepted_within_scope",
    "rejected_within_scope",
    "not_evaluable",
]

# Gate predicate result.
M56GateResultStatus = Literal["pass", "fail", "not_evaluable", "not_applicable"]

EVIDENCE_ROW_ORDER: Final[tuple[str, ...]] = EVIDENCE_CLASSES_RESERVED_FOR_M56
