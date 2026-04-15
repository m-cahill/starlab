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
