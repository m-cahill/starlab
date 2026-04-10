"""Raw parse envelope construction for replay parser pipeline (M08 / M35)."""

from __future__ import annotations

from typing import Any

from starlab.replays.parser_interfaces import RawEventStreams, RawParseSections, ReplayParserAdapter
from starlab.replays.parser_models import (
    NORMALIZATION_PROFILE_V1,
    RAW_EVENT_STREAMS_SCHEMA_VERSION,
    RAW_PARSE_SCHEMA_VERSION_V1,
)
from starlab.replays.parser_normalization import normalize_value


def _normalize_raw_sections(raw: RawParseSections) -> dict[str, Any]:
    """Normalize raw section dicts to JSON-safe trees."""

    sections: dict[str, Any] = {}
    for key, val in (
        ("header", raw.header),
        ("details", raw.details),
        ("init_data", raw.init_data),
        ("attribute_events", raw.attribute_events),
    ):
        if val is None:
            sections[key] = None
        else:
            sections[key] = normalize_value(val)
    return sections


def _build_raw_parse_empty(
    *,
    adapter: ReplayParserAdapter,
    replay_sha256: str | None,
) -> dict[str, Any]:
    return {
        "event_streams_available": {
            "attribute_events_available": False,
            "game_events_available": False,
            "message_events_available": False,
            "tracker_events_available": False,
        },
        "normalization_profile": NORMALIZATION_PROFILE_V1,
        "parser_family": adapter.parser_family(),
        "parser_version": adapter.parser_version(),
        "protocol_context": None,
        "raw_sections": {
            "attribute_events": None,
            "details": None,
            "header": None,
            "init_data": None,
        },
        "replay_content_sha256": replay_sha256,
        "schema_version": RAW_PARSE_SCHEMA_VERSION_V1,
    }


def _normalize_raw_event_streams(streams: RawEventStreams) -> dict[str, Any]:
    """Lower decoded event lists to JSON-safe trees (M10-owned payload area)."""

    out: dict[str, Any] = {"raw_event_streams_schema": RAW_EVENT_STREAMS_SCHEMA_VERSION}
    for key, val in (
        ("game_events", streams.game_events),
        ("message_events", streams.message_events),
        ("tracker_events", streams.tracker_events),
    ):
        if val is None:
            out[key] = None
        else:
            out[key] = normalize_value(val)
    return out


__all__ = [
    "_build_raw_parse_empty",
    "_normalize_raw_event_streams",
    "_normalize_raw_sections",
]
