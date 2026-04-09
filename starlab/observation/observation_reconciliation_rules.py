"""Deterministic reconciliation rules: expected observation vs canonical (M19)."""

from __future__ import annotations

from typing import Any, Literal

from starlab.observation.observation_surface_catalog import (
    ACTION_MASK_FAMILY_NAMES,
    ORDERED_SCALAR_FEATURE_NAMES,
)
from starlab.observation.observation_surface_derivation import derive_observation_surface_frame

ScalarSemanticWhenMatch = Literal[
    "exact",
    "derived",
    "bounded_lossy",
    "unavailable_by_design",
]

# When observation value matches M18 deterministic expectation from canonical, semantic status.
SCALAR_SEMANTIC_WHEN_MATCH: dict[str, ScalarSemanticWhenMatch] = {
    "economy.resource_signal_category": "bounded_lossy",
    "economy.structure_train_events_total": "exact",
    "economy.unit_train_events_total": "exact",
    "global.active_combat_window_count": "derived",
    "global.active_slice_count": "derived",
    "production.active_build_queue_count": "exact",
    "production.tech_upgrades_started_total": "exact",
    "race.actual": "exact",
    "result.known": "exact",
    "scouting.recent_scout_events_count": "exact",
    "visibility.proxy_level": "bounded_lossy",
}

# Canonical JSON path templates (perspective index substituted).
SCALAR_CANONICAL_PATHS: dict[str, str] = {
    "economy.resource_signal_category": ("players[{p}].economy_summary.resource_signal_category"),
    "economy.structure_train_events_total": (
        "players[{p}].economy_summary.structure_train_events_total"
    ),
    "economy.unit_train_events_total": "players[{p}].economy_summary.unit_train_events_total",
    "global.active_combat_window_count": "global_context.active_combat_window_ids (length)",
    "global.active_slice_count": "global_context.active_slice_ids (length)",
    "production.active_build_queue_count": (
        "players[{p}].production_summary.active_build_queue_count"
    ),
    "production.tech_upgrades_started_total": (
        "players[{p}].production_summary.tech_upgrades_started_total"
    ),
    "race.actual": "players[{p}].race_actual",
    "result.known": "players[{p}].result",
    "scouting.recent_scout_events_count": "players[{p}].scouting_context.recent_scout_events_count",
    "visibility.proxy_level": "players[{p}].visibility_context.visibility_proxy_level",
}


def expected_observation_from_canonical(
    canonical_state: dict[str, Any],
    *,
    perspective_player_index: int,
    source_canonical_state_sha256: str,
) -> tuple[dict[str, Any], list[str]]:
    """Return the M18-expected observation frame and derivation warnings."""

    return derive_observation_surface_frame(
        canonical_state,
        perspective_player_index=perspective_player_index,
        source_canonical_state_sha256=source_canonical_state_sha256,
    )


def scalar_paths_for_perspective(perspective_player_index: int) -> dict[str, str]:
    p = str(perspective_player_index)
    return {k: v.format(p=p) for k, v in SCALAR_CANONICAL_PATHS.items()}


def ordered_scalar_names() -> tuple[str, ...]:
    return ORDERED_SCALAR_FEATURE_NAMES


def ordered_action_family_names() -> tuple[str, ...]:
    return ACTION_MASK_FAMILY_NAMES
