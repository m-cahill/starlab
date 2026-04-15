"""Constants for replay↔execution equivalence charter artifacts (M52)."""

from __future__ import annotations

from typing import Final, Literal

REPLAY_EXECUTION_EQUIVALENCE_CHARTER_SCHEMA_VERSION = (
    "starlab.replay_execution_equivalence_charter.v1"
)
REPLAY_EXECUTION_EQUIVALENCE_CHARTER_REPORT_SCHEMA_VERSION = (
    "starlab.replay_execution_equivalence_charter_report.v1"
)

CHARTER_FILENAME: Final[str] = "replay_execution_equivalence_charter.json"
CHARTER_REPORT_FILENAME: Final[str] = "replay_execution_equivalence_charter_report.json"

RUNTIME_CONTRACT_REL_PATH: Final[str] = "docs/runtime/replay_execution_equivalence_charter_v1.md"

REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION = (
    "starlab.replay_execution_equivalence_evidence.v1"
)
REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_REPORT_SCHEMA_VERSION = (
    "starlab.replay_execution_equivalence_evidence_report.v1"
)

EVIDENCE_FILENAME: Final[str] = "replay_execution_equivalence_evidence.json"
EVIDENCE_REPORT_FILENAME: Final[str] = "replay_execution_equivalence_evidence_report.json"

EVIDENCE_RUNTIME_CONTRACT_REL_PATH: Final[str] = (
    "docs/runtime/replay_execution_equivalence_evidence_surface_v1.md"
)

CHARTER_CONTRACT_ID: Final[str] = "starlab.replay_execution_equivalence_charter.v1"

PROFILE_IDENTITY_BINDING_V1: Final[str] = "starlab.m53.profile.identity_binding_v1"

REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION = "starlab.replay_execution_equivalence_audit.v1"
REPLAY_EXECUTION_EQUIVALENCE_AUDIT_REPORT_SCHEMA_VERSION = (
    "starlab.replay_execution_equivalence_audit_report.v1"
)

AUDIT_FILENAME: Final[str] = "replay_execution_equivalence_audit.json"
AUDIT_REPORT_FILENAME: Final[str] = "replay_execution_equivalence_audit_report.json"

AUDIT_RUNTIME_CONTRACT_REL_PATH: Final[str] = (
    "docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md"
)

GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1: Final[str] = (
    "starlab.m54.gatepack.identity_binding_acceptance_v1"
)

ProfileScopeStatus = Literal[
    "accepted_within_profile_scope",
    "rejected_within_profile_scope",
    "not_evaluable",
]

MergeBarLanguage = Literal[
    "would_clear_profile_scope_gate",
    "would_block_profile_scope_gate",
    "no_profile_scope_decision",
]

GateResultStatus = Literal["pass", "fail", "not_evaluable", "not_applicable"]

MismatchKind = Literal[
    "missing_counterpart",
    "identity_mismatch",
    "ordering_mismatch",
    "count_mismatch",
    "bounded_semantic_divergence",
    "unavailable_by_design",
    "out_of_scope",
]

MISMATCH_KINDS_ORDERED: Final[tuple[MismatchKind, ...]] = (
    "missing_counterpart",
    "identity_mismatch",
    "ordering_mismatch",
    "count_mismatch",
    "bounded_semantic_divergence",
    "unavailable_by_design",
    "out_of_scope",
)
