"""Compile PX2 Terran actions to internal commands and optional Burny bridge hints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from starlab.sc2.px2.burny_bridge import internal_command_to_semantic_hint
from starlab.sc2.px2.terran_action_schema import (
    PX2_TERRAN_CORE_SURFACE_VERSION,
    TerranAction,
)
from starlab.sc2.px2.terran_legality import GameStateSnapshot, legality_for

PX2_INTERNAL_COMMAND_CONTRACT: Final[str] = "starlab.px2.internal_command.v1"


@dataclass(frozen=True, slots=True)
class Px2InternalCommand:
    """STARLAB-owned command object — not raw Burny/SC2 API calls."""

    command_kind: str
    surface_version: str
    action_id: str
    payload: dict[str, Any]
    burny_bridge_hint: dict[str, Any] | None

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "contract_id": PX2_INTERNAL_COMMAND_CONTRACT,
            "surface_version": self.surface_version,
            "command_kind": self.command_kind,
            "action_id": self.action_id,
            "payload": self.payload,
            "burny_bridge_hint": self.burny_bridge_hint,
        }


def _command_kind_for(action_id: str) -> str:
    if action_id in {"produce_scv"} or action_id.startswith("train_"):
        return "train_unit"
    if action_id.startswith("build_") or action_id in {"expand_command_center"}:
        return "place_structure"
    if action_id.startswith("army_") or action_id == "cleanup_search_region":
        return "army_order"
    if (
        action_id.startswith("dispatch_")
        or action_id.startswith("scout")
        or action_id.startswith("recheck")
    ):
        return "scout_order"
    if action_id in {"morph_orbital_command", "add_tech_lab", "add_reactor"}:
        return "structure_order"
    if action_id in {"tank_siege", "tank_unsiege", "stim_units_hook", "orbital_scan_hook"}:
        return "ability_order"
    return "macro_order"


def compile_terran_action(
    action: TerranAction,
    state: GameStateSnapshot | None,
) -> Px2InternalCommand:
    """Compile a structured Terran action. If ``state`` is given, legality is checked."""

    if state is not None:
        res = legality_for(state, action)
        if not res.legal:
            msg = f"illegal action {action.action_id}: {res.code} {res.detail}"
            raise ValueError(msg)

    kind = _command_kind_for(action.action_id)
    payload = {
        "arguments": dict(action.arguments),
        "family": action.family.value,
    }
    hint = internal_command_to_semantic_hint(action.action_id, action.arguments)
    return Px2InternalCommand(
        command_kind=kind,
        surface_version=PX2_TERRAN_CORE_SURFACE_VERSION,
        action_id=action.action_id,
        payload=payload,
        burny_bridge_hint=hint,
    )
