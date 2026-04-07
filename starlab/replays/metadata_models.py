"""Schema constants and check model for replay metadata extraction (M09)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

METADATA_SCHEMA_VERSION = "starlab.replay_metadata.v1"
METADATA_REPORT_SCHEMA_VERSION = "starlab.replay_metadata_report.v1"
METADATA_CONTRACT_VERSION = "starlab.replay_metadata_contract.v1"
METADATA_PROFILE = "starlab.replay_metadata_profile.v1"

ExtractionStatus = Literal["extracted", "partial", "source_contract_failed", "extraction_failed"]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

PlayerKind = Literal["human", "computer", "observer", "unknown"]
RaceRequested = Literal["terran", "zerg", "protoss", "random", "unknown"]
RaceActual = Literal["terran", "zerg", "protoss", "unknown"]
PlayerResult = Literal["win", "loss", "tie", "unknown"]

METADATA_CHECK_IDS: tuple[str, ...] = (
    "raw_parse_schema_valid",
    "replay_hash_present",
    "source_raw_parse_sha256_computed",
    "parse_receipt_hash_match",
    "parse_report_status_parsed",
    "required_sections_present",
    "core_metadata_extracted",
    "player_metadata_extracted",
    "metadata_emitted",
)


@dataclass(frozen=True)
class MetadataCheckResult:
    """Single ordered check row for ``replay_metadata_report.json``."""

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


def finalize_metadata_checks(checks: list[MetadataCheckResult]) -> list[MetadataCheckResult]:
    """Emit checks in ``METADATA_CHECK_IDS`` order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[MetadataCheckResult] = []
    for cid in METADATA_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or MetadataCheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out
