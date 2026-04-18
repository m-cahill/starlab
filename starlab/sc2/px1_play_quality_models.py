"""Types and constants for PX1-M02 play-quality protocol & evidence artifacts."""

from __future__ import annotations

from typing import Final, Literal

PX1_PLAY_QUALITY_PROTOCOL_CONTRACT_ID: Final[str] = "starlab.px1_play_quality_protocol.v1"
PX1_PLAY_QUALITY_PROTOCOL_SCHEMA_VERSION: Final[str] = "starlab.px1_play_quality_protocol.v1"
PX1_PLAY_QUALITY_PROTOCOL_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.px1_play_quality_protocol_report.v1"
)

PX1_PLAY_QUALITY_EVIDENCE_CONTRACT_ID: Final[str] = "starlab.px1_play_quality_evidence.v1"
PX1_PLAY_QUALITY_EVIDENCE_SCHEMA_VERSION: Final[str] = "starlab.px1_play_quality_evidence.v1"
PX1_PLAY_QUALITY_EVIDENCE_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.px1_play_quality_evidence_report.v1"
)

PX1_PLAY_QUALITY_PROTOCOL_FILENAME: Final[str] = "px1_play_quality_protocol.json"
PX1_PLAY_QUALITY_PROTOCOL_REPORT_FILENAME: Final[str] = "px1_play_quality_protocol_report.json"
PX1_PLAY_QUALITY_EVIDENCE_FILENAME: Final[str] = "px1_play_quality_evidence.json"
PX1_PLAY_QUALITY_EVIDENCE_REPORT_FILENAME: Final[str] = "px1_play_quality_evidence_report.json"

PX1_PLAY_QUALITY_RUNTIME_DOC_REL_PATH: Final[str] = (
    "docs/runtime/px1_play_quality_demo_candidate_selection_v1.md"
)

PX1_M02_PROTOCOL_PROFILE_BOUNDED_LOCAL_LIVE_V1: Final[str] = (
    "starlab.px1_m02.protocol_profile.bounded_local_live_play_v1"
)

SelectionStatus = Literal["candidate-selected", "not_selected_within_scope"]
EvidenceCompleteness = Literal["complete", "incomplete"]
