"""Types and constants for PX1-M03 demo-readiness remediation protocol & evidence."""

from __future__ import annotations

from typing import Final, Literal

PX1_DEMO_READINESS_PROTOCOL_CONTRACT_ID: Final[str] = "starlab.px1_demo_readiness_protocol.v1"
PX1_DEMO_READINESS_PROTOCOL_SCHEMA_VERSION: Final[str] = "starlab.px1_demo_readiness_protocol.v1"
PX1_DEMO_READINESS_PROTOCOL_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.px1_demo_readiness_protocol_report.v1"
)

PX1_DEMO_READINESS_EVIDENCE_CONTRACT_ID: Final[str] = "starlab.px1_demo_readiness_evidence.v1"
PX1_DEMO_READINESS_EVIDENCE_SCHEMA_VERSION: Final[str] = "starlab.px1_demo_readiness_evidence.v1"
PX1_DEMO_READINESS_EVIDENCE_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.px1_demo_readiness_evidence_report.v1"
)

PX1_DEMO_READINESS_PROTOCOL_FILENAME: Final[str] = "px1_demo_readiness_protocol.json"
PX1_DEMO_READINESS_PROTOCOL_REPORT_FILENAME: Final[str] = "px1_demo_readiness_protocol_report.json"
PX1_DEMO_READINESS_EVIDENCE_FILENAME: Final[str] = "px1_demo_readiness_evidence.json"
PX1_DEMO_READINESS_EVIDENCE_REPORT_FILENAME: Final[str] = "px1_demo_readiness_evidence_report.json"

PX1_DEMO_READINESS_RUNTIME_DOC_REL_PATH: Final[str] = (
    "docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md"
)

PX1_M03_PROTOCOL_PROFILE_DEMO_READINESS_REMEDIATION_V1: Final[str] = (
    "starlab.px1_m03.protocol_profile.demo_readiness_remediation_v1"
)

DemoReadinessSelectionStatus = Literal[
    "demo-ready-candidate-selected",
    "no-demo-ready-candidate-within-scope",
]
EvidenceCompleteness = Literal["complete", "incomplete"]
