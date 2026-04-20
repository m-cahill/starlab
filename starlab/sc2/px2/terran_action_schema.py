"""PX2 Terran core v1 — structured action schema (versioned, learnable heads)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

PX2_TERRAN_CORE_SURFACE_VERSION: Final[str] = "starlab.px2.terran_core.v1"
PX2_ACTION_SCHEMA_CONTRACT_ID: Final[str] = "starlab.px2.terran_action_schema.v1"


class ActionFamily(StrEnum):
    """High-level families for masking and later neural heads."""

    ECONOMY = "economy"
    SUPPLY_STRUCTURE = "supply_structure"
    GAS = "gas"
    PRODUCTION_STRUCTURE = "production_structure"
    UNIT_PRODUCTION = "unit_production"
    TECH_MORPH = "tech_morph"
    SCOUTING = "scouting"
    EXPANSION = "expansion"
    COMBAT = "combat"
    SEARCH = "search"
    ABILITY = "ability"


# --- Action id registry (Terran core v1) ---

ECONOMY_ACTIONS: frozenset[str] = frozenset(
    {
        "produce_scv",
        "rebalance_workers",
        "set_rally_point",
        "idle_worker_recall",
    },
)
SUPPLY_ACTIONS: frozenset[str] = frozenset({"build_supply_depot"})
GAS_ACTIONS: frozenset[str] = frozenset({"build_refinery"})
PROD_STRUCT_ACTIONS: frozenset[str] = frozenset(
    {
        "build_barracks",
        "build_factory",
        "build_starport",
        "build_engineering_bay",
        "add_tech_lab",
        "add_reactor",
    },
)
UNIT_PROD_ACTIONS: frozenset[str] = frozenset(
    {
        "train_marine",
        "train_marauder",
        "train_siege_tank",
        "train_medivac",
        "train_viking",
    },
)
TECH_MORPH_ACTIONS: frozenset[str] = frozenset({"morph_orbital_command"})
SCOUT_ACTIONS: frozenset[str] = frozenset(
    {
        "dispatch_worker_scout",
        "dispatch_unit_scout",
        "scout_to_region",
        "recheck_last_seen_region",
    },
)
EXPANSION_ACTIONS: frozenset[str] = frozenset({"expand_command_center"})
COMBAT_ACTIONS: frozenset[str] = frozenset(
    {
        "army_move_region",
        "army_attack_move_region",
        "army_regroup_region",
        "army_retreat_region",
    },
)
SEARCH_ACTIONS: frozenset[str] = frozenset({"cleanup_search_region"})
ABILITY_ACTIONS: frozenset[str] = frozenset(
    {
        "tank_siege",
        "tank_unsiege",
        "stim_units_hook",
        "orbital_scan_hook",
    },
)

ALL_TERRAN_CORE_V1_ACTION_IDS: frozenset[str] = (
    ECONOMY_ACTIONS
    | SUPPLY_ACTIONS
    | GAS_ACTIONS
    | PROD_STRUCT_ACTIONS
    | UNIT_PROD_ACTIONS
    | TECH_MORPH_ACTIONS
    | SCOUT_ACTIONS
    | EXPANSION_ACTIONS
    | COMBAT_ACTIONS
    | SEARCH_ACTIONS
    | ABILITY_ACTIONS
)

_FAMILY_BY_ACTION: dict[str, ActionFamily] = {}
for _ids, _fam in (
    (ECONOMY_ACTIONS, ActionFamily.ECONOMY),
    (SUPPLY_ACTIONS, ActionFamily.SUPPLY_STRUCTURE),
    (GAS_ACTIONS, ActionFamily.GAS),
    (PROD_STRUCT_ACTIONS, ActionFamily.PRODUCTION_STRUCTURE),
    (UNIT_PROD_ACTIONS, ActionFamily.UNIT_PRODUCTION),
    (TECH_MORPH_ACTIONS, ActionFamily.TECH_MORPH),
    (SCOUT_ACTIONS, ActionFamily.SCOUTING),
    (EXPANSION_ACTIONS, ActionFamily.EXPANSION),
    (COMBAT_ACTIONS, ActionFamily.COMBAT),
    (SEARCH_ACTIONS, ActionFamily.SEARCH),
    (ABILITY_ACTIONS, ActionFamily.ABILITY),
):
    for _aid in _ids:
        _FAMILY_BY_ACTION[_aid] = _fam


def family_for_action(action_id: str) -> ActionFamily:
    if action_id not in _FAMILY_BY_ACTION:
        msg = f"unknown Terran core v1 action_id: {action_id!r}"
        raise ValueError(msg)
    return _FAMILY_BY_ACTION[action_id]


@dataclass(frozen=True, slots=True)
class TerranAction:
    """A single structured Terran command on the PX2 surface."""

    action_id: str
    arguments: dict[str, Any]

    def __post_init__(self) -> None:
        if self.action_id not in ALL_TERRAN_CORE_V1_ACTION_IDS:
            msg = f"invalid action_id for Terran core v1: {self.action_id!r}"
            raise ValueError(msg)
        validate_arguments(self.action_id, self.arguments)

    @property
    def family(self) -> ActionFamily:
        return family_for_action(self.action_id)

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "surface_version": PX2_TERRAN_CORE_SURFACE_VERSION,
            "action_id": self.action_id,
            "family": self.family.value,
            "arguments": self.arguments,
        }


def validate_arguments(action_id: str, arguments: dict[str, Any]) -> None:
    """Validate argument shapes for Terran core v1 (bounded)."""

    def _need(keys: set[str]) -> None:
        missing = keys - set(arguments)
        if missing:
            msg = f"{action_id}: missing arguments {sorted(missing)}"
            raise ValueError(msg)

    if action_id in {"build_supply_depot", "build_barracks", "build_factory", "build_starport"}:
        _need({"build_slot"})
        if not isinstance(arguments["build_slot"], int):
            msg = "build_slot must be int (BuildSlotId)"
            raise ValueError(msg)
    elif action_id == "build_refinery":
        _need({"expansion_slot"})
    elif action_id == "build_engineering_bay":
        _need({"build_slot"})
    elif action_id in {"add_tech_lab", "add_reactor"}:
        _need({"target_structure"})
    elif action_id in UNIT_PROD_ACTIONS or action_id == "produce_scv":
        _need({"producer_key"})
    elif action_id == "expand_command_center":
        _need({"expansion_slot"})
    elif action_id in {"scout_to_region", "recheck_last_seen_region"}:
        _need({"region_slot"})
    elif action_id == "dispatch_worker_scout":
        _need({"target_key"})
    elif action_id == "dispatch_unit_scout":
        _need({"unit_role", "target_key"})
    elif action_id == "cleanup_search_region":
        _need({"region_slot", "target_handle_kind"})
        if not isinstance(arguments["region_slot"], int):
            msg = "region_slot must be int (RegionSlotId)"
            raise ValueError(msg)
    elif action_id in COMBAT_ACTIONS:
        _need({"region_slot"})
        if not isinstance(arguments["region_slot"], int):
            msg = "region_slot must be int (RegionSlotId)"
            raise ValueError(msg)
    elif action_id in {"tank_siege", "tank_unsiege"}:
        _need({"unit_batch_id"})
    elif action_id in {"stim_units_hook", "orbital_scan_hook"}:
        _need({"hook_target"})
    elif action_id == "morph_orbital_command":
        _need({"command_center_key"})
    elif action_id in {"rebalance_workers", "set_rally_point", "idle_worker_recall"}:
        _need({"target_key"})


def terran_action_from_json_dict(data: dict[str, Any]) -> TerranAction:
    """Parse a JSON-compatible dict into ``TerranAction``."""

    aid = data["action_id"]
    args = dict(data.get("arguments", {}))
    return TerranAction(action_id=str(aid), arguments=args)


def terran_action_json_dumps(action: TerranAction) -> str:
    return json.dumps(action.to_json_dict(), sort_keys=True, separators=(",", ":"))
