"""Constants for benchmark integrity charter artifacts (M55 — charter only)."""

from __future__ import annotations

from typing import Final

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
