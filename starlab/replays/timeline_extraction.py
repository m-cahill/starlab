"""Pure extraction: M08/M10 ``replay_raw_parse`` → governed timeline entries (M10)."""

from __future__ import annotations

from typing import Any

from starlab.replays.timeline_models import (
    MERGE_ORDER_POLICY,
    SOURCE_STREAM_PRECEDENCE,
    TIMELINE_CONTRACT_VERSION,
    TIMELINE_PROFILE,
    TIMELINE_REPORT_SCHEMA_VERSION,
    TIMELINE_SCHEMA_VERSION,
)

RAW_PARSE_SCHEMA_ACCEPTED = frozenset(
    {
        "starlab.replay_raw_parse.v1",
        "starlab.replay_raw_parse.v2",
    },
)

# Blizzard ``_event`` typename → public semantic kind (narrow M10 set).
EVENT_NAME_TO_SEMANTIC: dict[str, str] = {
    "NNet.Game.SChatMessage": "message_event",
    "NNet.Game.SCmdEvent": "command_issued",
    "NNet.Game.SPingMessage": "ping_event",
    "NNet.Replay.Tracker.SUnitBornEvent": "unit_born",
    "NNet.Replay.Tracker.SUnitDiedEvent": "unit_died",
    "NNet.Replay.Tracker.SUnitInitEvent": "unit_init",
    "NNet.Replay.Tracker.SUnitOwnerChangeEvent": "unit_owner_changed",
    "NNet.Replay.Tracker.SUnitTypeChangeEvent": "unit_type_changed",
    "NNet.Replay.Tracker.SUpgradeEvent": "upgrade_completed",
}

_STREAM_KEY_TO_NAME = {
    "game_events": "game",
    "message_events": "message",
    "tracker_events": "tracker",
}

_STREAM_ORDER = {name: i for i, name in enumerate(SOURCE_STREAM_PRECEDENCE)}

_PRIVACY_DROP_KEYS = frozenset(
    {
        "m_name",
        "m_playerName",
        "m_clanTag",
        "m_toonHandle",
        "m_string",
    },
)


def _gameloop(ev: dict[str, Any]) -> int:
    g = ev.get("_gameloop")
    return int(g) if isinstance(g, int) and not isinstance(g, bool) else 0


def _player_index(ev: dict[str, Any]) -> int | None:
    u = ev.get("_userid")
    if isinstance(u, dict):
        mid = u.get("m_userId")
        if isinstance(mid, int) and not isinstance(mid, bool):
            return mid
    return None


def _unit_tag_hex(ev: dict[str, Any]) -> str | None:
    if (
        "m_unitTag" in ev
        and isinstance(ev["m_unitTag"], int)
        and not isinstance(ev["m_unitTag"], bool)
    ):
        return f"{ev['m_unitTag']:016x}"
    idx = ev.get("m_unitTagIndex")
    rec = ev.get("m_unitTagRecycle")
    if (
        isinstance(idx, int)
        and not isinstance(idx, bool)
        and isinstance(rec, int)
        and not isinstance(rec, bool)
    ):
        tag = (idx << 18) + rec
        return f"{tag:016x}"
    return None


def _scrub_value(key: str, val: Any, semantic_kind: str) -> Any | None:
    """Drop privacy-sensitive or unbounded strings; keep bounded numeric metadata."""

    if key in _PRIVACY_DROP_KEYS:
        return None
    if key == "m_string" and semantic_kind == "message_event":
        if isinstance(val, str):
            return len(val)
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, int) and not isinstance(val, bool):
        return val
    if isinstance(val, float):
        return val
    if val is None:
        return None
    if isinstance(val, str):
        return None
    if isinstance(val, dict):
        out: dict[str, Any] = {}
        for k in sorted(val.keys()):
            if not isinstance(k, str):
                continue
            sub = _scrub_value(k, val[k], semantic_kind)
            if sub is not None:
                out[k] = sub
        return out if out else None
    if isinstance(val, list):
        out_l = [_scrub_value("_item", x, semantic_kind) for x in val]
        out_l = [x for x in out_l if x is not None]
        return out_l if out_l else None
    return None


def build_public_payload(*, semantic_kind: str, event: dict[str, Any]) -> dict[str, Any]:
    """Bounded, privacy-safe payload for the public timeline contract."""

    out: dict[str, Any] = {}
    for k in sorted(event.keys()):
        if not isinstance(k, str):
            continue
        if k.startswith("_") and k not in ("_event", "_eventid", "_gameloop", "_userid"):
            continue
        if k.startswith("_"):
            if k == "_userid":
                u = event.get("_userid")
                if isinstance(u, dict):
                    scrubbed = _scrub_value("_userid", u, semantic_kind)
                    if scrubbed is not None:
                        out["_userid"] = scrubbed
            elif k in ("_event", "_eventid", "_gameloop"):
                v = event.get(k)
                if v is not None:
                    out[k] = v
            continue
        if k == "m_string" and semantic_kind == "message_event":
            v = event.get("m_string")
            if isinstance(v, str):
                out["m_string_length"] = len(v)
            continue
        scrubbed = _scrub_value(k, event[k], semantic_kind)
        if scrubbed is not None:
            out[k] = scrubbed
    return out


def _collect_stream_events(
    raw_event_streams: dict[str, Any],
) -> list[tuple[str, int, dict[str, Any]]]:
    collected: list[tuple[str, int, dict[str, Any]]] = []
    for stream_key, stream_name in _STREAM_KEY_TO_NAME.items():
        arr = raw_event_streams.get(stream_key)
        if not isinstance(arr, list):
            continue
        for i, ev in enumerate(arr):
            if isinstance(ev, dict):
                collected.append((stream_name, i, ev))
    return collected


def _merge_sort(
    events: list[tuple[str, int, dict[str, Any]]],
) -> list[tuple[str, int, dict[str, Any]]]:
    return sorted(
        events,
        key=lambda t: (_gameloop(t[2]), _STREAM_ORDER[t[0]], t[1]),
    )


def extract_timeline_envelope(
    *,
    raw_parse: dict[str, Any],
    source_raw_parse_sha256: str,
    source_parse_receipt_sha256: str | None,
    source_parse_report_sha256: str | None,
    source_metadata_sha256: str | None,
    source_metadata_report_sha256: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(replay_timeline body, report body)`` (without file writes)."""

    warnings: list[str] = []
    unsupported: set[str] = set()
    counts_by_stream: dict[str, int] = {n: 0 for n in SOURCE_STREAM_PRECEDENCE}
    counts_by_semantic: dict[str, int] = {}

    schema_ok = (
        isinstance(raw_parse.get("schema_version"), str)
        and raw_parse.get("schema_version") in RAW_PARSE_SCHEMA_ACCEPTED
    )
    rhash = raw_parse.get("replay_content_sha256")
    hash_ok = isinstance(rhash, str) and len(rhash) == 64

    ev_avail = raw_parse.get("event_streams_available")
    if not isinstance(ev_avail, dict):
        ev_avail = {
            "attribute_events_available": False,
            "game_events_available": False,
            "message_events_available": False,
            "tracker_events_available": False,
        }

    entries: list[dict[str, Any]] = []
    raw_streams = raw_parse.get("raw_event_streams")
    if raw_parse.get("schema_version") == "starlab.replay_raw_parse.v1" or raw_streams is None:
        warnings.append(
            "raw_event_streams absent (v1 parse or no M10 lowering); timeline entries empty"
        )

    if isinstance(raw_streams, dict):
        for stream_key, stream_name in _STREAM_KEY_TO_NAME.items():
            arr = raw_streams.get(stream_key)
            counts_by_stream[stream_name] = len(arr) if isinstance(arr, list) else 0

        collected = _collect_stream_events(raw_streams)
        merged = _merge_sort(collected)
        timeline_index = 0
        for stream_name, src_idx, ev in merged:
            ename = ev.get("_event")
            if not isinstance(ename, str):
                unsupported.add("unknown")
                continue
            semantic = EVENT_NAME_TO_SEMANTIC.get(ename)
            if semantic is None:
                unsupported.add(ename)
                continue
            payload = build_public_payload(semantic_kind=semantic, event=ev)
            entry: dict[str, Any] = {
                "gameloop": _gameloop(ev),
                "payload": payload,
                "semantic_kind": semantic,
                "source_event_index": src_idx,
                "source_event_name": ename,
                "source_stream": stream_name,
                "timeline_index": timeline_index,
            }
            pi = _player_index(ev)
            if pi is not None:
                entry["player_index"] = pi
            ut = _unit_tag_hex(ev)
            if ut is not None:
                entry["unit_tag"] = ut
            entries.append(entry)
            counts_by_semantic[semantic] = counts_by_semantic.get(semantic, 0) + 1
            timeline_index += 1

    if not schema_ok or not hash_ok:
        status: str = "failed"
    elif warnings or not entries:
        status = "partial"
    else:
        status = "ok"

    timeline: dict[str, Any] = {
        "entries": entries,
        "event_streams_available": ev_avail,
        "merge_order_policy": MERGE_ORDER_POLICY,
        "replay_content_sha256": rhash if isinstance(rhash, str) else None,
        "schema_version": TIMELINE_SCHEMA_VERSION,
        "source_metadata_report_sha256": source_metadata_report_sha256,
        "source_metadata_sha256": source_metadata_sha256,
        "source_parse_receipt_sha256": source_parse_receipt_sha256,
        "source_parse_report_sha256": source_parse_report_sha256,
        "source_raw_parse_sha256": source_raw_parse_sha256,
        "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
        "timeline_profile": TIMELINE_PROFILE,
    }

    report = {
        "counts_by_semantic_kind": dict(sorted(counts_by_semantic.items())),
        "counts_by_stream": dict(sorted(counts_by_stream.items())),
        "extraction_status": status,
        "schema_version": TIMELINE_REPORT_SCHEMA_VERSION,
        "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
        "timeline_profile": TIMELINE_PROFILE,
        "unsupported_event_names": sorted(unsupported),
        "warnings": sorted(set(warnings)),
    }
    return timeline, report
