"""Bridge PX2 internal commands to coarse semantic labels (M44-style), not raw BotAI."""

from __future__ import annotations

from typing import Any

# Maps PX2 action_id -> hierarchical coarse label used by semantic_live_action_adapter (M44).
_ACTION_TO_COARSE: dict[str, str] = {
    "produce_scv": "economy_worker",
    "rebalance_workers": "economy_worker",
    "set_rally_point": "economy_worker",
    "idle_worker_recall": "economy_worker",
    "build_supply_depot": "production_structure",
    "build_refinery": "production_structure",
    "build_barracks": "production_structure",
    "build_factory": "production_structure",
    "build_starport": "production_structure",
    "build_engineering_bay": "production_structure",
    "add_tech_lab": "production_structure",
    "add_reactor": "production_structure",
    "train_marine": "production_unit",
    "train_marauder": "production_unit",
    "train_siege_tank": "production_unit",
    "train_medivac": "production_unit",
    "train_viking": "production_unit",
    "morph_orbital_command": "production_structure",
    "dispatch_worker_scout": "scout",
    "dispatch_unit_scout": "scout",
    "scout_to_region": "scout",
    "recheck_last_seen_region": "scout",
    "expand_command_center": "economy_expand",
    "army_move_region": "army_move",
    "army_attack_move_region": "army_attack",
    "army_regroup_region": "army_move",
    "army_retreat_region": "army_move",
    "cleanup_search_region": "army_attack",
    "tank_siege": "army_attack",
    "tank_unsiege": "army_move",
    "stim_units_hook": "army_attack",
    "orbital_scan_hook": "scout",
}


def internal_command_to_semantic_hint(action_id: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Return a bounded hint record for tracing and optional M44 template mapping."""

    coarse = _ACTION_TO_COARSE.get(action_id, "other")
    return {
        "px2_action_id": action_id,
        "semantic_coarse_label": coarse,
        "bridge_policy_id": "starlab.px2.burny_bridge.v1",
        "arguments_echo": dict(arguments),
    }
