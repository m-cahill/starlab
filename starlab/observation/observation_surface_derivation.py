"""Derive one M17-shaped observation frame from one M16 canonical state object (M18 prototype)."""

from __future__ import annotations

from typing import Any

from starlab.observation.observation_surface_catalog import (
    ACTION_MASK_FAMILY_NAMES,
    COORDINATE_FRAME_VALUES,
    ORDERED_SCALAR_FEATURE_NAMES,
)
from starlab.observation.observation_surface_models import (
    OBSERVATION_FRAME_SCHEMA_VERSION,
    OBSERVATION_SURFACE_CONTRACT,
)


def _player_by_index(players: list[dict[str, Any]], idx: int) -> dict[str, Any] | None:
    for p in players:
        if isinstance(p, dict) and p.get("player_index") == idx:
            return p
    return None


def _army_category_counts(player: dict[str, Any]) -> dict[str, int]:
    arm = player.get("army_summary") or {}
    raw = arm.get("army_unit_category_counts") if isinstance(arm, dict) else None
    if not isinstance(raw, dict):
        return {}
    out: dict[str, int] = {}
    for k, v in raw.items():
        if isinstance(k, str) and isinstance(v, int) and v > 0:
            out[k] = v
    return out


def _sorted_entity_rows_from_counts(
    *,
    counts: dict[str, int],
    owner_view: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cat in sorted(counts.keys()):
        rows.append(
            {
                "row_kind": "aggregated_category",
                "owner_view": owner_view,
                "category": cat,
                "count": counts[cat],
            },
        )
    return rows


def derive_observation_surface_frame(
    canonical_state: dict[str, Any],
    *,
    perspective_player_index: int,
    source_canonical_state_sha256: str,
) -> tuple[dict[str, Any], list[str]]:
    """Return ``(observation_frame, warnings)``.

    Pure over ``canonical_state`` JSON. ``source_canonical_state_sha256`` must be precomputed
    from the same object (caller responsibility).
    """

    warnings: list[str] = []

    players_raw = canonical_state.get("players")
    if not isinstance(players_raw, list) or not players_raw:
        msg = "canonical_state.players must be a non-empty array"
        raise ValueError(msg)

    players: list[dict[str, Any]] = [p for p in players_raw if isinstance(p, dict)]
    perspective = _player_by_index(players, perspective_player_index)
    if perspective is None:
        msg = (
            f"perspective_player_index {perspective_player_index} not found in "
            "canonical_state.players"
        )
        raise ValueError(msg)

    gameloop = canonical_state.get("gameloop")
    if not isinstance(gameloop, int) or gameloop < 0:
        msg = "canonical_state.gameloop must be a non-negative integer"
        raise ValueError(msg)

    src = canonical_state.get("source")
    source_bundle_id: str | None = None
    source_lineage_root: str | None = None
    source_replay_identity: str | None = None
    if isinstance(src, dict):
        bid = src.get("source_bundle_id")
        if isinstance(bid, str) and bid:
            source_bundle_id = bid
        lr = src.get("source_lineage_root")
        if isinstance(lr, str) and lr:
            source_lineage_root = lr
        sri = src.get("source_replay_identity")
        if isinstance(sri, str) and sri:
            source_replay_identity = sri

    metadata: dict[str, Any] = {
        "gameloop": gameloop,
        "observation_contract_version": "1",
        "perspective_player_index": perspective_player_index,
        "source_canonical_state_sha256": source_canonical_state_sha256,
    }
    if source_bundle_id is not None:
        metadata["source_bundle_id"] = source_bundle_id
    if source_lineage_root is not None:
        metadata["source_lineage_root"] = source_lineage_root
    if source_replay_identity is not None:
        metadata["source_replay_identity"] = source_replay_identity

    gc = canonical_state.get("global_context")
    active_combat_window_count = 0
    active_slice_count = 0
    if isinstance(gc, dict):
        acw = gc.get("active_combat_window_ids")
        if isinstance(acw, list):
            active_combat_window_count = len(acw)
        asl = gc.get("active_slice_ids")
        if isinstance(asl, list):
            active_slice_count = len(asl)

    econ = perspective.get("economy_summary") or {}
    if not isinstance(econ, dict):
        econ = {}
    prod = perspective.get("production_summary") or {}
    if not isinstance(prod, dict):
        prod = {}

    resource_signal = econ.get("resource_signal_category")
    structure_train = econ.get("structure_train_events_total")
    unit_train = econ.get("unit_train_events_total")
    if not isinstance(structure_train, int):
        structure_train = 0
    if not isinstance(unit_train, int):
        unit_train = 0

    qb = prod.get("active_build_queue_count")
    tech_started = prod.get("tech_upgrades_started_total")
    if not isinstance(qb, int):
        qb = 0
    if not isinstance(tech_started, int):
        tech_started = 0

    race = perspective.get("race_actual")
    if not isinstance(race, str):
        race = "Random"

    result_known = perspective.get("result")
    if result_known is not None and not isinstance(result_known, str):
        result_known = None

    sc = perspective.get("scouting_context")
    scout_count = 0
    if isinstance(sc, dict) and isinstance(sc.get("recent_scout_events_count"), int):
        scout_count = int(sc["recent_scout_events_count"])

    vc = perspective.get("visibility_context")
    vis_level: str | None = None
    if isinstance(vc, dict):
        vpl = vc.get("visibility_proxy_level")
        if isinstance(vpl, str):
            vis_level = vpl
    if vis_level is None:
        warnings.append(
            "visibility.proxy_level: no M16 visibility_context.visibility_proxy_level; "
            "using null (proxy-bounded posture; not fog-of-war truth).",
        )

    scalar_values: dict[str, Any] = {
        "economy.resource_signal_category": resource_signal
        if resource_signal is None or isinstance(resource_signal, str)
        else None,
        "economy.structure_train_events_total": structure_train,
        "economy.unit_train_events_total": unit_train,
        "global.active_combat_window_count": active_combat_window_count,
        "global.active_slice_count": active_slice_count,
        "production.active_build_queue_count": qb,
        "production.tech_upgrades_started_total": tech_started,
        "race.actual": race,
        "result.known": result_known,
        "scouting.recent_scout_events_count": scout_count,
        "visibility.proxy_level": vis_level,
    }

    ordered_entries: list[dict[str, Any]] = []
    for name in ORDERED_SCALAR_FEATURE_NAMES:
        ordered_entries.append({"name": name, "value": scalar_values[name]})

    # Entity rows: self + enemy (bounded); deterministic sort.
    rows_out: list[dict[str, Any]] = []
    self_counts = _army_category_counts(perspective)
    rows_out.extend(_sorted_entity_rows_from_counts(counts=self_counts, owner_view="self"))

    for p in sorted(players, key=lambda x: int(x.get("player_index", 0))):
        if not isinstance(p, dict):
            continue
        pi = p.get("player_index")
        if not isinstance(pi, int) or pi == perspective_player_index:
            continue
        enemy_counts = _army_category_counts(p)
        rows_out.extend(_sorted_entity_rows_from_counts(counts=enemy_counts, owner_view="enemy"))

    spatial_plane_family = {
        "planes": [
            {
                "channel_count": 2,
                "channel_order": [
                    "terrain_class",
                    "control_affinity",
                ],
                "coordinate_frame": COORDINATE_FRAME_VALUES[0],
                "grid_height": 8,
                "grid_width": 8,
                "plane_id": "example_placeholder_plane",
            },
        ],
    }

    # Prototype mask families: bounded heuristics from M16 summaries (not legality).
    army_total = sum(self_counts.values())
    # selection: second slot off when active slices exist (bounded signal; not UI semantics).
    selection_b = 0 if active_slice_count > 0 else 1
    families_payload: list[dict[str, Any]] = [
        {"family_name": "no_op", "ordered_mask_values": [1]},
        {"family_name": "selection", "ordered_mask_values": [1, selection_b]},
        {
            "family_name": "camera_or_view",
            "ordered_mask_values": [
                1,
                1 if active_combat_window_count > 0 else 0,
                0,
            ],
        },
        {
            "family_name": "production",
            "ordered_mask_values": [
                1,
                0,
                0,
                1 if qb > 0 else 0,
            ],
        },
        {
            "family_name": "build",
            "ordered_mask_values": [
                1 if structure_train > 0 else 0,
                1 if unit_train > 0 else 0,
            ],
        },
        {
            "family_name": "unit_command",
            "ordered_mask_values": [
                0,
                1 if army_total > 0 else 0,
                0,
            ],
        },
        {
            "family_name": "research_or_upgrade",
            "ordered_mask_values": [1 if tech_started > 0 or qb > 0 else 0],
        },
    ]

    names = [f["family_name"] for f in families_payload]
    if names != list(ACTION_MASK_FAMILY_NAMES):
        msg = "internal error: action mask family order drift vs catalog"
        raise RuntimeError(msg)

    frame: dict[str, Any] = {
        "action_mask_families": {"families": families_payload},
        "contract_id": OBSERVATION_SURFACE_CONTRACT,
        "entity_rows": {"rows": rows_out},
        "metadata": metadata,
        "scalar_features": {"ordered_entries": ordered_entries},
        "schema_version": OBSERVATION_FRAME_SCHEMA_VERSION,
        "spatial_plane_family": spatial_plane_family,
        "viewpoint": {
            "player_index": perspective_player_index,
            "single_player_relative_viewpoint": True,
            "visibility_policy": "proxy_bounded",
        },
    }
    return frame, warnings
