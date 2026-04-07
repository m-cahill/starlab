"""Schema constants and check IDs for replay build-order / economy artifacts (M11)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

BUILD_ORDER_ECONOMY_CONTRACT_VERSION = "starlab.replay_build_order_economy_contract.v1"
BUILD_ORDER_ECONOMY_PROFILE = "starlab.replay_build_order_economy.m11.v1"
BUILD_ORDER_ECONOMY_SCHEMA_VERSION = "starlab.replay_build_order_economy.v1"
BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION = "starlab.replay_build_order_economy_report.v1"

CATALOG_NAME = "starlab.build_order_economy_catalog.m11.v1"
MORPH_RULES_PROFILE = "starlab.build_order_economy_morph.m11.v1"

ORDERING_POLICY = (
    "Process timeline entries in ascending timeline_index order (M10 public event plane). "
    "When replay_raw_parse.json v2 raw_event_streams are present, use them only as a "
    "supplemental identity lookup keyed by (source_stream, source_event_index); "
    "timeline ordering and semantics always win over raw-stream ordering."
)

ExtractionStatus = Literal["ok", "partial", "failed"]
RunStatus = Literal["completed", "source_contract_failed", "extraction_failed"]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

BUILD_ORDER_ECONOMY_CHECK_IDS: tuple[str, ...] = (
    "timeline_schema_valid",
    "replay_hash_present",
    "source_timeline_sha256_computed",
    "source_raw_parse_identity_match",
    "build_order_economy_emitted",
)


@dataclass(frozen=True)
class BuildOrderEconomyCheckResult:
    """Single ordered check row for ``replay_build_order_economy_report.json``."""

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


def finalize_build_order_economy_checks(
    checks: list[BuildOrderEconomyCheckResult],
) -> list[BuildOrderEconomyCheckResult]:
    """Emit checks in ``BUILD_ORDER_ECONOMY_CHECK_IDS`` order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[BuildOrderEconomyCheckResult] = []
    for cid in BUILD_ORDER_ECONOMY_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or BuildOrderEconomyCheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out
