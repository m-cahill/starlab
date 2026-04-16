"""Types and constants for M59 ladder/public evaluation protocol & evidence surface."""

from __future__ import annotations

from typing import Final, Literal

# --- Protocol artifact ---
LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID: Final[str] = (
    "starlab.ladder_public_evaluation_protocol.v1"
)
LADDER_PUBLIC_EVALUATION_PROTOCOL_SCHEMA_VERSION: Final[str] = (
    "starlab.ladder_public_evaluation_protocol.v1"
)
LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.ladder_public_evaluation_protocol_report.v1"
)

LADDER_PUBLIC_EVALUATION_PROTOCOL_FILENAME: Final[str] = "ladder_public_evaluation_protocol.json"
LADDER_PUBLIC_EVALUATION_PROTOCOL_REPORT_FILENAME: Final[str] = (
    "ladder_public_evaluation_protocol_report.json"
)

# --- Evidence artifact ---
LADDER_PUBLIC_EVALUATION_EVIDENCE_CONTRACT_ID: Final[str] = (
    "starlab.ladder_public_evaluation_evidence.v1"
)
LADDER_PUBLIC_EVALUATION_EVIDENCE_SCHEMA_VERSION: Final[str] = (
    "starlab.ladder_public_evaluation_evidence.v1"
)
LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.ladder_public_evaluation_evidence_report.v1"
)

LADDER_PUBLIC_EVALUATION_EVIDENCE_FILENAME: Final[str] = "ladder_public_evaluation_evidence.json"
LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_FILENAME: Final[str] = (
    "ladder_public_evaluation_evidence_report.json"
)

LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH: Final[str] = (
    "docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md"
)

# Exactly one bounded profile in M59 v1.
M59_PROTOCOL_PROFILE_SINGLE_CANDIDATE_PUBLIC_EVAL_V1: Final[str] = (
    "starlab.m59.protocol_profile.single_candidate_public_eval_v1"
)

EvaluationSurfaceKind = Literal["ladder_public", "public_match_set"]

EvidenceClass = Literal[
    "replay_bound_result",
    "result_row_only",
    "operator_attested_result",
]

EvidencePostureStatus = Literal["bounded_complete", "bounded_incomplete", "invalid"]

MatchResult = Literal["win", "loss", "draw", "unknown"]

ALLOWED_EVIDENCE_CLASSES: Final[tuple[str, ...]] = (
    "replay_bound_result",
    "result_row_only",
    "operator_attested_result",
)

DEFAULT_PROTOCOL_NON_CLAIMS: Final[tuple[str, ...]] = (
    "M59 describes and packages descriptive public/ladder-shaped evidence only — not ladder "
    "strength, statistical significance, or global performance proof.",
    "This protocol is not benchmark integrity, not replay↔execution equivalence, and not a "
    "substitute for M52–M56 governed surfaces.",
    "M59 does not automate ladder play, scrape public sources, or run live SC2 in default CI.",
    "Operator-attested rows are weaker evidence and are never upgraded silently.",
)

DEFAULT_PROTOCOL_OUT_OF_SCOPE: Final[tuple[str, ...]] = (
    "Automated ladder submission or matchmaking.",
    "OCR, screenshot parsing, or hosted dashboard integrations.",
    "Branch-protection or merge-bar automation.",
    "Rating certification or confidence intervals presented as proof.",
)
