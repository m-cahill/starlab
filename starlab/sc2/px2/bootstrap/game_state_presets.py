"""Minimal legal ``GameStateSnapshot`` presets for compile checks (PX2-M02).

Not tactical policy — scaffolding for compile receipts only.
"""

from __future__ import annotations

from typing import Any


def preset_snapshot_for_supervised_action(action_id: str) -> dict[str, Any]:
    """Return JSON-compatible snapshot dict sufficient for ``compile_terran_action`` legality.

    Conservative scaffolding so labeled actions compile — not inferred policy.
    """

    base: dict[str, Any] = {
        "minerals": 500,
        "vespene": 500,
        "supply_used": 10,
        "supply_cap": 60,
        "structures": ["command_center", "barracks", "factory", "starport"],
        "units": {},
        "owned_expansion_slots": [0, 1],
        "structure_addons": [],
        "orbital_available": True,
    }

    if action_id == "build_barracks":
        return {
            **base,
            "structures": ["command_center"],
            "minerals": 500,
            "supply_used": 5,
            "supply_cap": 15,
        }
    if action_id == "build_supply_depot":
        return {
            **base,
            "structures": ["command_center", "barracks"],
            "minerals": 200,
            "supply_used": 20,
            "supply_cap": 27,
        }
    if action_id == "build_refinery":
        return {
            **base,
            "structures": ["command_center", "barracks"],
            "minerals": 200,
            "owned_expansion_slots": [0],
            "supply_used": 10,
            "supply_cap": 30,
        }
    if action_id == "train_marine":
        return {
            **base,
            "structures": ["command_center", "barracks"],
            "minerals": 200,
            "supply_used": 10,
            "supply_cap": 27,
        }
    if action_id == "train_medivac":
        return {
            **base,
            "structures": ["command_center", "barracks", "factory", "starport"],
            "minerals": 300,
            "supply_used": 20,
            "supply_cap": 40,
        }
    if action_id in {"train_marauder", "train_siege_tank", "train_viking"}:
        return {
            **base,
            "minerals": 400,
            "supply_used": 20,
            "supply_cap": 40,
        }
    return dict(base)


def snapshot_dict_to_dataclass_kwargs(d: dict[str, Any]) -> dict[str, Any]:
    """Convert JSON list structures to ``GameStateSnapshot`` kwargs."""

    return {
        "minerals": int(d["minerals"]),
        "vespene": int(d["vespene"]),
        "supply_used": int(d["supply_used"]),
        "supply_cap": int(d["supply_cap"]),
        "structures": frozenset(str(x) for x in d.get("structures", [])),
        "units": {str(k): int(v) for k, v in dict(d.get("units", {})).items()},
        "owned_expansion_slots": frozenset(int(x) for x in d.get("owned_expansion_slots", [])),
        "structure_addons": frozenset(str(x) for x in d.get("structure_addons", [])),
        "orbital_available": bool(d.get("orbital_available", False)),
    }
