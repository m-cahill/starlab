"""Schema constants and check IDs for replay combat / scouting / visibility artifacts (M12)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

COMBAT_SCOUTING_VISIBILITY_CONTRACT_VERSION = (
    "starlab.replay_combat_scouting_visibility_contract.v1"
)
COMBAT_SCOUTING_VISIBILITY_PROFILE = "starlab.replay_combat_scouting_visibility.m12.v1"
COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION = "starlab.replay_combat_scouting_visibility.v1"
COMBAT_SCOUTING_VISIBILITY_REPORT_SCHEMA_VERSION = (
    "starlab.replay_combat_scouting_visibility_report.v1"
)

CATALOG_NAME = "starlab.combat_scouting_visibility_catalog.m12.v1"

# Fixed clustering constant (gameloops). Documented in contract; auditable for M12.
COMBAT_WINDOW_GAP_LOOPS = 160

COMBAT_WINDOW_MODEL = (
    "Combat windows are clusters of unit_died timeline entries (M10). Entries are sorted by "
    "timeline_index ascending; a new window starts when the gameloop gap from the previous "
    f"death exceeds COMBAT_WINDOW_GAP_LOOPS ({COMBAT_WINDOW_GAP_LOOPS} gameloops). "
    "This is a conservative segmentation surface, not a full battle simulator."
)

SCOUTING_MODEL = (
    "Deterministic first-seen signals per subject_player_index for macro and army categories, "
    "derived from timeline order with entity identity from supplemental raw parse when available "
    "and optional category hints from replay_build_order_economy.json (M11)."
)

VISIBILITY_MODEL = (
    "Predominantly observation_proxy: presence intervals keyed by unit_tag when present, "
    "spanning first to last timeline mention of that tag. Does not assert true fog-of-war state."
)

ORDERING_POLICY = (
    "Process timeline entries in ascending timeline_index order (M10 public event plane). "
    "replay_build_order_economy.json (M11) supplies governed macro context; "
    "replay_raw_parse.json v2 raw_event_streams are supplemental only for identity, position, "
    "and fields that directly encode visibility when present. Timeline ordering always wins; "
    "do not reorder events using raw streams."
)

ExtractionStatus = Literal["ok", "partial", "failed"]
RunStatus = Literal["completed", "source_contract_failed", "extraction_failed"]

CheckStatus = Literal["pass", "warn", "fail", "not_evaluated"]
CheckSeverity = Literal["required", "warning"]

COMBAT_SCOUTING_VISIBILITY_CHECK_IDS: tuple[str, ...] = (
    "timeline_schema_valid",
    "build_order_economy_schema_valid",
    "timeline_boe_hash_consistent",
    "replay_hash_present",
    "source_timeline_sha256_computed",
    "source_build_order_economy_sha256_computed",
    "source_raw_parse_identity_match",
    "combat_scouting_visibility_emitted",
)


@dataclass(frozen=True)
class CombatScoutingVisibilityCheckResult:
    """Single ordered check row for ``replay_combat_scouting_visibility_report.json``."""

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


def finalize_combat_scouting_visibility_checks(
    checks: list[CombatScoutingVisibilityCheckResult],
) -> list[CombatScoutingVisibilityCheckResult]:
    """Emit checks in fixed order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[CombatScoutingVisibilityCheckResult] = []
    for cid in COMBAT_SCOUTING_VISIBILITY_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or CombatScoutingVisibilityCheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out
