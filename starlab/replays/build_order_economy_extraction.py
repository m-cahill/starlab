"""Pure extraction: M10 timeline (+ optional raw parse identity) → build-order / economy (M11)."""

from __future__ import annotations

from typing import Any

from starlab.replays.build_order_economy_catalog import (
    ENTITY_CATEGORY,
    MORPH_DESTINATION_CATEGORY,
    STRUCTURE_CATEGORIES,
    UPGRADE_CATEGORY,
)
from starlab.replays.build_order_economy_models import (
    BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
    BUILD_ORDER_ECONOMY_PROFILE,
    BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
    BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
    CATALOG_NAME,
    MORPH_RULES_PROFILE,
    ORDERING_POLICY,
)

TIMELINE_SCHEMA_ACCEPTED = frozenset({"starlab.replay_timeline.v1"})

IGNORED_SEMANTIC_KINDS: frozenset[str] = frozenset(
    {
        "command_issued",
        "message_event",
        "ping_event",
        "unit_owner_changed",
        "unit_died",
    },
)

_STREAM_TO_RAW_KEY = {
    "game": "game_events",
    "message": "message_events",
    "tracker": "tracker_events",
}


def _int_field(entry: dict[str, Any], key: str, default: int = 0) -> int:
    v = entry.get(key)
    if isinstance(v, int) and not isinstance(v, bool):
        return v
    return default


def _player_index_from_entry(entry: dict[str, Any]) -> int | None:
    pi = entry.get("player_index")
    if isinstance(pi, int) and not isinstance(pi, bool):
        return pi
    payload = entry.get("payload")
    if isinstance(payload, dict):
        for k in ("m_controlPlayerId", "m_upkeepPlayerId"):
            v = payload.get(k)
            if isinstance(v, int) and not isinstance(v, bool):
                return v
    return None


def _lookup_raw_event(
    raw_parse: dict[str, Any] | None,
    *,
    source_stream: str,
    source_event_index: int,
) -> dict[str, Any] | None:
    if raw_parse is None:
        return None
    streams = raw_parse.get("raw_event_streams")
    if not isinstance(streams, dict):
        return None
    key = _STREAM_TO_RAW_KEY.get(source_stream)
    if key is None:
        return None
    arr = streams.get(key)
    if not isinstance(arr, list):
        return None
    if source_event_index < 0 or source_event_index >= len(arr):
        return None
    ev = arr[source_event_index]
    return ev if isinstance(ev, dict) else None


def _identity_name_from_raw_event(ev: dict[str, Any]) -> tuple[str | None, str]:
    """Return (name, kind) where kind is ``unit``, ``upgrade``, or ``unknown``."""

    en = ev.get("_event")
    if en == "NNet.Replay.Tracker.SUpgradeEvent":
        u = ev.get("m_upgradeTypeName")
        if isinstance(u, str) and u:
            return u, "upgrade"
        return None, "upgrade"
    u = ev.get("m_unitTypeName")
    if isinstance(u, str) and u:
        return u, "unit"
    return None, "unknown"


def _category_for_name(
    *,
    name: str | None,
    kind_hint: str,
    semantic_kind: str,
) -> str:
    if not name:
        return "unknown"
    if semantic_kind == "upgrade_completed" or kind_hint == "upgrade":
        return UPGRADE_CATEGORY.get(name, "unknown")
    if semantic_kind == "unit_type_changed":
        return MORPH_DESTINATION_CATEGORY.get(name, ENTITY_CATEGORY.get(name, "unknown"))
    return ENTITY_CATEGORY.get(name, "unknown")


def _entity_kind_for(
    *,
    category: str,
    semantic_kind: str,
) -> str:
    if semantic_kind == "upgrade_completed":
        return "upgrade"
    if semantic_kind == "unit_type_changed":
        return "morph"
    if category in STRUCTURE_CATEGORIES:
        return "structure"
    return "unit"


def _should_emit_step(*, semantic_kind: str, category: str, phase: str) -> bool:
    if semantic_kind == "unit_init":
        return category in STRUCTURE_CATEGORIES or category == "worker"
    if semantic_kind == "unit_born":
        return True
    if semantic_kind == "upgrade_completed":
        return True
    if semantic_kind == "unit_type_changed":
        return category != "unknown"
    return False


def _increments_counters(
    *,
    semantic_kind: str,
    phase: str,
    category: str,
) -> dict[str, int]:
    """Return counter deltas (non-zero keys only) for completed macro-relevant events."""

    deltas: dict[str, int] = {}
    if phase != "completed":
        return deltas
    if semantic_kind == "upgrade_completed" and category == "economy_upgrade":
        deltas["economy_upgrade_count"] = 1
        return deltas
    if semantic_kind not in ("unit_born", "unit_type_changed"):
        return deltas
    if category == "worker":
        deltas["workers_completed"] = 1
    if category == "townhall":
        deltas["townhalls_completed"] = 1
    if category == "gas_structure":
        deltas["gas_structures_completed"] = 1
    if category == "supply_provider":
        deltas["supply_providers_completed"] = 1
    if category == "production_structure":
        deltas["production_structures_completed"] = 1
    if category == "tech_structure":
        deltas["tech_structures_completed"] = 1
    return deltas


def extract_build_order_economy_envelope(
    *,
    timeline: dict[str, Any],
    source_timeline_sha256: str,
    raw_parse: dict[str, Any] | None,
    source_raw_parse_sha256: str | None,
    source_timeline_report_sha256: str | None,
    source_metadata_sha256: str | None,
    source_metadata_report_sha256: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(replay_build_order_economy body, report body)`` without file writes."""

    warnings: list[str] = []
    ignored_kinds: dict[str, int] = {}
    unclassified_units: set[str] = set()
    unclassified_upgrades: set[str] = set()

    entries = timeline.get("entries")
    if not isinstance(entries, list):
        entries = []

    steps: list[dict[str, Any]] = []
    checkpoints: list[dict[str, Any]] = []

    # Per-player cumulative counters
    cum: dict[int, dict[str, int]] = {}

    def _ensure_player(pid: int) -> dict[str, int]:
        if pid not in cum:
            cum[pid] = {
                "workers_completed": 0,
                "townhalls_completed": 0,
                "gas_structures_completed": 0,
                "supply_providers_completed": 0,
                "production_structures_completed": 0,
                "tech_structures_completed": 0,
                "economy_upgrade_count": 0,
            }
        return cum[pid]

    sorted_entries = sorted(
        [e for e in entries if isinstance(e, dict)],
        key=lambda e: int(e.get("timeline_index", 0)),
    )

    if raw_parse is None and sorted_entries:
        warnings.append(
            "supplemental replay_raw_parse.json not provided; entity identity unavailable "
            "(m_unitTypeName / m_upgradeTypeName); classifications may be unknown",
        )

    step_index = 0
    checkpoint_index = 0

    for entry in sorted_entries:
        sk = entry.get("semantic_kind")
        if not isinstance(sk, str):
            continue
        if sk in IGNORED_SEMANTIC_KINDS:
            ignored_kinds[sk] = ignored_kinds.get(sk, 0) + 1
            continue
        if sk not in (
            "unit_init",
            "unit_born",
            "upgrade_completed",
            "unit_type_changed",
        ):
            ignored_kinds[sk] = ignored_kinds.get(sk, 0) + 1
            continue

        player_index = _player_index_from_entry(entry)
        if player_index is None:
            warnings.append("missing player_index for timeline entry; skipped")
            continue

        src_stream = entry.get("source_stream")
        src_idx = entry.get("source_event_index")
        if (
            not isinstance(src_stream, str)
            or not isinstance(src_idx, int)
            or isinstance(
                src_idx,
                bool,
            )
        ):
            warnings.append("missing source_stream or source_event_index; skipped")
            continue

        raw_ev = _lookup_raw_event(
            raw_parse,
            source_stream=src_stream,
            source_event_index=src_idx,
        )
        name: str | None
        kind_hint: str
        if raw_ev is not None:
            name, kind_hint = _identity_name_from_raw_event(raw_ev)
        else:
            name, kind_hint = None, "unknown"
            if raw_parse is not None:
                warnings.append(
                    "raw_event lookup miss for "
                    f"({src_stream!r}, {src_idx}); identity unknown for classification",
                )

        category = _category_for_name(
            name=name,
            kind_hint=kind_hint,
            semantic_kind=sk,
        )
        if category == "unknown" and name:
            if sk == "upgrade_completed" or kind_hint == "upgrade":
                unclassified_upgrades.add(name)
            else:
                unclassified_units.add(name)
        if sk == "unit_init":
            phase = "started"
        elif sk == "unit_type_changed":
            phase = "completed"
        else:
            phase = "completed"

        if not _should_emit_step(semantic_kind=sk, category=category, phase=phase):
            continue

        ek = _entity_kind_for(category=category, semantic_kind=sk)
        display_name = name if name else "unknown"
        ut = entry.get("unit_tag")
        row: dict[str, Any] = {
            "step_index": step_index,
            "player_index": player_index,
            "gameloop": _int_field(entry, "gameloop"),
            "source_timeline_index": _int_field(entry, "timeline_index"),
            "entity_name": display_name,
            "entity_kind": ek,
            "phase": phase,
            "category": category,
        }
        if isinstance(ut, str):
            row["unit_tag"] = ut
        steps.append(row)

        deltas = _increments_counters(semantic_kind=sk, phase=phase, category=category)
        if deltas:
            st = _ensure_player(player_index)
            changed = False
            for k, dv in deltas.items():
                st[k] = st.get(k, 0) + dv
                changed = True
            if changed:
                checkpoints.append(
                    {
                        "checkpoint_index": checkpoint_index,
                        "player_index": player_index,
                        "gameloop": row["gameloop"],
                        "source_step_index": step_index,
                        "workers_completed": st["workers_completed"],
                        "townhalls_completed": st["townhalls_completed"],
                        "gas_structures_completed": st["gas_structures_completed"],
                        "supply_providers_completed": st["supply_providers_completed"],
                        "production_structures_completed": st["production_structures_completed"],
                        "tech_structures_completed": st["tech_structures_completed"],
                        "economy_upgrade_count": st["economy_upgrade_count"],
                    },
                )
                checkpoint_index += 1

        step_index += 1

    players_out = [{"player_index": i} for i in sorted(cum.keys())]

    body: dict[str, Any] = {
        "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
        "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
        "schema_version": BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
        "replay_content_sha256": timeline.get("replay_content_sha256"),
        "source_timeline_sha256": source_timeline_sha256,
        "source_timeline_report_sha256": source_timeline_report_sha256,
        "source_metadata_sha256": source_metadata_sha256,
        "source_metadata_report_sha256": source_metadata_report_sha256,
        "source_raw_parse_sha256": source_raw_parse_sha256,
        "ordering_policy": ORDERING_POLICY,
        "classification_profile": {
            "catalog_name": CATALOG_NAME,
            "morph_rules_profile": MORPH_RULES_PROFILE,
        },
        "players": players_out,
        "build_order_steps": steps,
        "economy_checkpoints": checkpoints,
    }
    return body, {
        "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
        "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
        "schema_version": BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
        "warnings": sorted(set(warnings)),
        "ignored_timeline_semantic_kinds": dict(sorted(ignored_kinds.items())),
        "unclassified_unit_names": sorted(unclassified_units),
        "unclassified_upgrade_names": sorted(unclassified_upgrades),
    }


def validate_timeline_contract(timeline: dict[str, Any]) -> tuple[bool, str | None]:
    """Return (ok, error detail)."""

    sv = timeline.get("schema_version")
    if sv not in TIMELINE_SCHEMA_ACCEPTED:
        return False, "unsupported or missing timeline schema_version"
    cv = timeline.get("timeline_contract_version")
    if cv != "starlab.replay_timeline_contract.v1":
        return False, "unsupported timeline_contract_version"
    rhash = timeline.get("replay_content_sha256")
    if not isinstance(rhash, str) or len(rhash) != 64:
        return False, "replay_content_sha256 missing or not 64-hex"
    return True, None
