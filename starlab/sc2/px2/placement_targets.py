"""PX2 Terran placement and target abstractions — named slots, not raw click-space."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class ExpansionSlotId(IntEnum):
    """Logical expansion index for legality and compiler (Terran core v1)."""

    NATURAL = 0
    THIRD = 1
    FOURTH = 2
    FIFTH = 3


class BuildSlotId(IntEnum):
    """Coarse main-base build grid slot (v1 — bounded vocabulary)."""

    MAIN_GRID_A = 0
    MAIN_GRID_B = 1
    MAIN_GRID_C = 2
    MAIN_GRID_D = 3


class RegionSlotId(IntEnum):
    """Scouting / army movement region slots (map-agnostic logical regions)."""

    ENEMY_NATURAL = 0
    ENEMY_THIRD = 1
    MAP_CENTER = 2
    ARMY_RALLY = 3
    RETREAT_SAFE = 4


@dataclass(frozen=True, slots=True)
class EnemyClusterHandle:
    """Opaque handle for targeting (resolved at execution time)."""

    kind: str
    handle_id: str
    region_slot: RegionSlotId | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "handle_id": self.handle_id,
            "region_slot": int(self.region_slot) if self.region_slot is not None else None,
        }


@dataclass(frozen=True, slots=True)
class PlacementRequest:
    """Structured placement — compiler maps this to concrete geometry later."""

    expansion_slot: ExpansionSlotId | None
    build_slot: BuildSlotId | None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "expansion_slot": int(self.expansion_slot) if self.expansion_slot is not None else None,
            "build_slot": int(self.build_slot) if self.build_slot is not None else None,
        }
