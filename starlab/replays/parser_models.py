"""Schema constants and models for replay parse substrate (M08)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

RECEIPT_SCHEMA_VERSION = "starlab.replay_parse_receipt.v1"
REPORT_SCHEMA_VERSION = "starlab.replay_parse_report.v1"
RAW_PARSE_SCHEMA_VERSION_V1 = "starlab.replay_raw_parse.v1"
RAW_PARSE_SCHEMA_VERSION_V2 = "starlab.replay_raw_parse.v2"
# Historical alias: M08 receipts referred to v1; v2 adds optional ``raw_event_streams`` (M10-owned).
RAW_PARSE_SCHEMA_VERSION = RAW_PARSE_SCHEMA_VERSION_V2

RAW_EVENT_STREAMS_SCHEMA_VERSION = "starlab.raw_event_streams.v1"
POLICY_VERSION = "starlab.replay_parser_substrate.v1"
PARSER_CONTRACT_VERSION = "starlab.replay_parser_contract.v1"

PARSER_FAMILY_S2PROTOCOL = "s2protocol"

ParseStatus = Literal[
    "parsed",
    "unsupported_protocol",
    "parser_unavailable",
    "parse_failed",
    "input_contract_failed",
]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

PARSE_CHECK_IDS: tuple[str, ...] = (
    "replay_file_readable",
    "replay_sha256_computed",
    "parser_dependency_available",
    "parser_adapter_selected",
    "intake_receipt_hash_match",
    "binding_hash_match",
    "parse_attempted",
    "raw_sections_normalized",
    "raw_parse_emitted",
)

NORMALIZATION_PROFILE_V1 = "starlab.parser_normalization.v1"


@dataclass(frozen=True)
class CheckResult:
    """Single ordered check row for ``replay_parse_report.json``."""

    check_id: str
    status: CheckStatus
    severity: CheckSeverity
    detail: str | None = None

    def to_mapping(self) -> dict[str, Any]:
        m: dict[str, Any] = {
            "check_id": self.check_id,
            "severity": self.severity,
            "status": self.status,
        }
        if self.detail is not None:
            m["detail"] = self.detail
        return m
