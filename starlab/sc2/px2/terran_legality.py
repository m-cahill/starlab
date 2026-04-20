"""Legality and masking for PX2 Terran core v1 (scaffolding — not policy)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from starlab.sc2.px2.terran_action_schema import (
    ALL_TERRAN_CORE_V1_ACTION_IDS,
    TerranAction,
)


@dataclass(frozen=True, slots=True)
class GameStateSnapshot:
    """Minimal game snapshot for legality checks (fixture-driven; not full observation)."""

    minerals: int
    vespene: int
    supply_used: int
    supply_cap: int
    # Structure keys: command_center, barracks, factory, starport, engineering_bay, ...
    structures: frozenset[str] = frozenset()
    # Counts by logical key
    units: dict[str, int] = field(default_factory=dict)
    # Expansion slots already claimed by the player (ExpansionSlotId ints)
    owned_expansion_slots: frozenset[int] = frozenset()
    # Add-on state per structure key (e.g. barracks_0 -> tech_lab)
    structure_addons: frozenset[str] = frozenset()
    # Whether orbital upgrade is available / done for a CC key
    orbital_available: bool = False


@dataclass(frozen=True, slots=True)
class LegalityResult:
    """Whether an action is legal and optional reason when not."""

    legal: bool
    code: str | None = None
    detail: str | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return {"legal": self.legal, "code": self.code, "detail": self.detail}


def _cost(action_id: str) -> tuple[int, int]:
    """Rough mineral / gas costs for gating (v1 — not exhaustive)."""

    costs: dict[str, tuple[int, int]] = {
        "produce_scv": (50, 0),
        "build_supply_depot": (100, 0),
        "build_refinery": (75, 0),
        "build_barracks": (150, 0),
        "build_factory": (150, 100),
        "build_starport": (150, 100),
        "build_engineering_bay": (125, 0),
        "train_marine": (50, 0),
        "train_marauder": (100, 25),
        "train_siege_tank": (150, 125),
        "train_medivac": (100, 100),
        "train_viking": (150, 75),
        "expand_command_center": (400, 0),
        "morph_orbital_command": (150, 0),
        "add_tech_lab": (50, 25),
        "add_reactor": (50, 50),
    }
    return costs.get(action_id, (0, 0))


def legality_for(state: GameStateSnapshot, action: TerranAction) -> LegalityResult:
    """Return whether ``action`` is legal under ``state`` (conservative v1 rules)."""

    aid = action.action_id
    args = action.arguments

    def _afford() -> bool:
        m, g = _cost(aid)
        return state.minerals >= m and state.vespene >= g

    def _supply_headroom() -> int:
        return max(0, state.supply_cap - state.supply_used)

    if aid == "produce_scv":
        if "command_center" not in state.structures and "orbital_command" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_command_center")
        if _supply_headroom() < 1:
            return LegalityResult(False, "supply_blocked", "no_supply_headroom")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid == "build_supply_depot":
        if "command_center" not in state.structures and "orbital_command" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_command_center")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid in {"build_barracks", "build_factory", "build_starport", "build_engineering_bay"}:
        if "command_center" not in state.structures and "orbital_command" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_command_center")
        if aid == "build_factory" and "barracks" not in state.structures:
            return LegalityResult(False, "tech_prereq", "need_barracks_for_factory")
        if aid == "build_starport" and "factory" not in state.structures:
            return LegalityResult(False, "tech_prereq", "need_factory_for_starport")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid == "build_refinery":
        slot = int(args["expansion_slot"])
        if slot in state.owned_expansion_slots and state.minerals >= 75:
            return LegalityResult(True)
        return LegalityResult(False, "invalid_expansion", "need_owned_expansion")

    if aid in {"train_marine", "train_marauder"}:
        if "barracks" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_barracks")
        need = 2 if aid == "train_marauder" else 1
        if _supply_headroom() < need:
            return LegalityResult(False, "supply_blocked", "no_supply_headroom")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid == "train_siege_tank":
        if "factory" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_factory")
        if _supply_headroom() < 3:
            return LegalityResult(False, "supply_blocked", "no_supply_headroom")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid in {"train_medivac", "train_viking"}:
        if "starport" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_starport")
        if _supply_headroom() < 3:
            return LegalityResult(False, "supply_blocked", "no_supply_headroom")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid == "expand_command_center":
        slot = int(args["expansion_slot"])
        if slot in state.owned_expansion_slots:
            return LegalityResult(False, "already_owned", "expansion_taken")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid == "morph_orbital_command":
        if "command_center" not in state.structures:
            return LegalityResult(False, "missing_structure", "need_command_center")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid in {"add_tech_lab", "add_reactor"}:
        tgt = str(args["target_structure"])
        if tgt not in state.structures:
            return LegalityResult(False, "missing_structure", "target_not_built")
        if not _afford():
            return LegalityResult(False, "insufficient_resources", None)
        return LegalityResult(True)

    if aid in {
        "dispatch_worker_scout",
        "dispatch_unit_scout",
        "scout_to_region",
        "recheck_last_seen_region",
        "army_move_region",
        "army_attack_move_region",
        "army_regroup_region",
        "army_retreat_region",
        "cleanup_search_region",
        "rebalance_workers",
        "set_rally_point",
        "idle_worker_recall",
        "tank_siege",
        "tank_unsiege",
        "stim_units_hook",
        "orbital_scan_hook",
    }:
        return LegalityResult(True)

    return LegalityResult(False, "unhandled", aid)


def legal_mask(state: GameStateSnapshot) -> dict[str, bool]:
    """Map each Terran core v1 action id to legality under ``state``."""

    out: dict[str, bool] = {}
    for aid in sorted(ALL_TERRAN_CORE_V1_ACTION_IDS):
        dummy_args: dict[str, Any] = {}
        if aid in {
            "build_supply_depot",
            "build_barracks",
            "build_factory",
            "build_starport",
            "build_engineering_bay",
        }:
            dummy_args = {"build_slot": 0}
        elif aid == "build_refinery":
            dummy_args = {"expansion_slot": 0}
        elif aid in {
            "train_marine",
            "train_marauder",
            "train_siege_tank",
            "train_medivac",
            "train_viking",
            "produce_scv",
        }:
            dummy_args = {"producer_key": "default"}
        elif aid == "expand_command_center":
            dummy_args = {"expansion_slot": 1}
        elif aid in {"scout_to_region", "recheck_last_seen_region"}:
            dummy_args = {"region_slot": 0}
        elif aid == "dispatch_worker_scout":
            dummy_args = {"target_key": "enemy_natural"}
        elif aid == "dispatch_unit_scout":
            dummy_args = {"unit_role": "marine", "target_key": "map"}
        elif aid in {
            "army_move_region",
            "army_attack_move_region",
            "army_regroup_region",
            "army_retreat_region",
        }:
            dummy_args = {"region_slot": 0}
        elif aid == "cleanup_search_region":
            dummy_args = {"region_slot": 0, "target_handle_kind": "structure_class"}
        elif aid in {"tank_siege", "tank_unsiege"}:
            dummy_args = {"unit_batch_id": "tanks_1"}
        elif aid in {"stim_units_hook", "orbital_scan_hook"}:
            dummy_args = {"hook_target": "bio_1"}
        elif aid == "morph_orbital_command":
            dummy_args = {"command_center_key": "cc_main"}
        elif aid in {"add_tech_lab", "add_reactor"}:
            dummy_args = {"target_structure": "barracks"}
        elif aid in {"rebalance_workers", "set_rally_point", "idle_worker_recall"}:
            dummy_args = {"target_key": "main"}

        try:
            ta = TerranAction(action_id=aid, arguments=dummy_args)
        except ValueError:
            out[aid] = False
            continue
        out[aid] = legality_for(state, ta).legal
    return out
