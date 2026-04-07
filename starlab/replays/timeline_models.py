"""Schema constants and check IDs for replay timeline artifacts (M10)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

TIMELINE_CONTRACT_VERSION = "starlab.replay_timeline_contract.v1"
TIMELINE_PROFILE = "starlab.replay_timeline.m10.v1"
TIMELINE_SCHEMA_VERSION = "starlab.replay_timeline.v1"
TIMELINE_REPORT_SCHEMA_VERSION = "starlab.replay_timeline_report.v1"

# Fixed merge order for determinism (not causal proof within one gameloop).
SOURCE_STREAM_PRECEDENCE: tuple[str, ...] = ("game", "message", "tracker")

MERGE_ORDER_POLICY = (
    "Sort by gameloop ascending, then by source_stream_precedence "
    f"{list(SOURCE_STREAM_PRECEDENCE)}, then by source_event_index ascending. "
    "This is a canonical merge order for artifact determinism only; it does not "
    "prove exact cross-stream causality within a single gameloop."
)

SemanticKind = Literal[
    "command_issued",
    "message_event",
    "ping_event",
    "unit_born",
    "unit_died",
    "unit_init",
    "unit_owner_changed",
    "unit_type_changed",
    "upgrade_completed",
]

ExtractionStatus = Literal["ok", "partial", "failed"]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

TIMELINE_CHECK_IDS: tuple[str, ...] = (
    "raw_parse_schema_valid",
    "replay_hash_present",
    "source_raw_parse_sha256_computed",
    "parse_receipt_hash_match",
    "parse_report_status_parsed",
    "metadata_hash_match",
    "metadata_report_hash_match",
    "raw_event_streams_present",
    "timeline_emitted",
)


@dataclass(frozen=True)
class TimelineCheckResult:
    """Single ordered check row for ``replay_timeline_report.json``."""

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


def finalize_timeline_checks(checks: list[TimelineCheckResult]) -> list[TimelineCheckResult]:
    """Emit checks in ``TIMELINE_CHECK_IDS`` order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[TimelineCheckResult] = []
    for cid in TIMELINE_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or TimelineCheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out
