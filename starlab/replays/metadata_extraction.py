"""Pure extraction: M08 ``replay_raw_parse`` envelope → normalized metadata (M09)."""

from __future__ import annotations

from typing import Any

from starlab.replays.metadata_models import (
    METADATA_CONTRACT_VERSION,
    METADATA_PROFILE,
    METADATA_SCHEMA_VERSION,
    PlayerKind,
    PlayerResult,
    RaceActual,
    RaceRequested,
)

RAW_PARSE_SCHEMA_EXPECTED = "starlab.replay_raw_parse.v1"
RAW_PARSE_SCHEMA_ACCEPTED = frozenset(
    {
        "starlab.replay_raw_parse.v1",
        "starlab.replay_raw_parse.v2",
    },
)


def _as_int(v: Any) -> int | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    return None


def _norm_key(s: str) -> str:
    return s.strip().upper().replace("E", "").replace("_", "")


def map_player_kind(raw: Any) -> PlayerKind:
    """Map ``m_control`` (int or normalized enum name) to ``player_kind``."""

    if raw is None:
        return "unknown"
    if isinstance(raw, str):
        nk = _norm_key(raw)
        if "HUMAN" in nk or nk == "HUMAN":
            return "human"
        if "COMPUTER" in nk or "AI" in nk or nk == "COMPUTER":
            return "computer"
        if "OBSERVER" in nk or "REFERE" in nk:
            return "observer"
        return "unknown"
    if isinstance(raw, int):
        # Common s2protocol / SC2 control values (conservative; unknown if not listed).
        if raw in (1,):
            return "human"
        if raw in (2,):
            return "computer"
        if raw in (3,):
            return "observer"
        return "unknown"
    return "unknown"


def map_race_requested(raw: Any) -> RaceRequested:
    """Map Blizzard race field to requested race enum."""

    if raw is None:
        return "unknown"
    if not isinstance(raw, str):
        return "unknown"
    n = raw.lower()
    if n in ("terran", "t"):
        return "terran"
    if n in ("zerg", "z"):
        return "zerg"
    if n in ("protoss", "p"):
        return "protoss"
    if "random" in n:
        return "random"
    return "unknown"


def map_race_actual(raw: Any) -> RaceActual:
    """Map Blizzard race field to actual race enum (no ``random`` in contract)."""

    r = map_race_requested(raw)
    if r == "random":
        return "unknown"
    if r == "unknown":
        return "unknown"
    return r


def map_result(raw: Any) -> PlayerResult:
    if raw is None:
        return "unknown"
    if isinstance(raw, str):
        n = raw.lower()
        if n in ("win", "victory"):
            return "win"
        if n in ("loss", "defeat"):
            return "loss"
        if n in ("tie", "draw", "undecided"):
            return "tie"
        return "unknown"
    if isinstance(raw, int):
        # Common result encodings (conservative).
        if raw == 1:
            return "win"
        if raw == 2:
            return "loss"
        if raw == 3:
            return "tie"
        return "unknown"
    return "unknown"


def source_sections_present(raw_sections: Any) -> list[str]:
    """Lexicographically sorted list of raw section keys with non-null values."""

    if not isinstance(raw_sections, dict):
        return []
    keys = [k for k, v in raw_sections.items() if v is not None]
    return sorted(keys, key=str)


def extract_protocol_fields(raw: dict[str, Any]) -> dict[str, Any]:
    """``protocol`` block from ``protocol_context`` and/or ``header.m_version``."""

    ctx = raw.get("protocol_context")
    header = None
    rs = raw.get("raw_sections")
    if isinstance(rs, dict):
        header = rs.get("header")
    ver: dict[str, Any] | None = None
    if isinstance(header, dict):
        ver = header.get("m_version") if isinstance(header.get("m_version"), dict) else None

    base: int | None = None
    data_build: int | None = None
    data_version: int | None = None

    if isinstance(ctx, dict):
        base = _as_int(ctx.get("m_baseBuild"))
        db = _as_int(ctx.get("m_dataBuild"))
        if db is not None:
            data_build = db
        rev = _as_int(ctx.get("m_revision"))
        if rev is not None:
            data_version = rev

    if isinstance(ver, dict):
        if base is None:
            base = _as_int(ver.get("m_baseBuild"))
        if data_build is None:
            data_build = _as_int(ver.get("m_dataBuild"))
        if data_version is None:
            data_version = _as_int(ver.get("m_revision"))

    return {
        "base_build": 0 if base is None else base,
        "data_build": 0 if data_build is None else data_build,
        "data_version": data_version,
    }


def extract_players(details: Any) -> tuple[list[dict[str, Any]], bool]:
    """Return player rows and whether any field was ambiguous (forces partial posture)."""

    ambiguous = False
    if not isinstance(details, dict):
        return [], ambiguous
    pl = details.get("m_playerList")
    if not isinstance(pl, list):
        return [], ambiguous
    rows: list[dict[str, Any]] = []
    for idx, p in enumerate(pl):
        if not isinstance(p, dict):
            ambiguous = True
            continue
        slot = _as_int(p.get("m_workingSetSlotId"))
        player_index = slot if slot is not None else idx
        kind = map_player_kind(p.get("m_control"))
        rq = map_race_requested(p.get("m_race"))
        ra = map_race_actual(p.get("m_race"))
        if rq == "random" and ra == "unknown":
            pass
        res = map_result(p.get("m_result"))
        if kind == "unknown" and p.get("m_control") is not None:
            ambiguous = True
        if rq == "unknown" and p.get("m_race") is not None:
            ambiguous = True
        rows.append(
            {
                "player_index": player_index,
                "player_kind": kind,
                "race_requested": rq,
                "race_actual": ra,
                "result": res,
            },
        )
    rows.sort(key=lambda r: (int(r["player_index"]),))
    return rows, ambiguous


def build_normalized_metadata(raw: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Build the inner ``metadata`` object (no top-level envelope).

    Returns ``(metadata, ambiguous)`` where ``ambiguous`` is True if a player row
    carried an unmapped control/race value (partial extraction posture).
    """

    rs = raw.get("raw_sections")
    details = rs.get("details") if isinstance(rs, dict) else None
    protocol = extract_protocol_fields(raw)

    map_name = None
    if isinstance(details, dict):
        t = details.get("m_title")
        if isinstance(t, str):
            map_name = t
        elif t is not None:
            map_name = None

    game_length: int | None = None
    player_count = 0
    if isinstance(details, dict):
        gl = details.get("m_gameDurationLoops")
        game_length = _as_int(gl)
        pl = details.get("m_playerList")
        if isinstance(pl, list):
            player_count = len(pl)

    ev = raw.get("event_streams_available")
    if not isinstance(ev, dict):
        ev = {
            "attribute_events_available": False,
            "game_events_available": False,
            "message_events_available": False,
            "tracker_events_available": False,
        }
    else:
        ev = {
            "attribute_events_available": bool(ev.get("attribute_events_available")),
            "game_events_available": bool(ev.get("game_events_available")),
            "message_events_available": bool(ev.get("message_events_available")),
            "tracker_events_available": bool(ev.get("tracker_events_available")),
        }

    players, ambiguous = extract_players(details)
    if player_count == 0 and players:
        player_count = len(players)

    meta = {
        "game": {
            "event_streams_available": ev,
            "game_length_loops": game_length,
            "player_count": player_count,
        },
        "map": {
            "map_name": map_name,
        },
        "players": players,
        "protocol": protocol,
    }
    return meta, ambiguous


def build_metadata_envelope(
    *,
    raw: dict[str, Any],
    source_raw_parse_sha256: str,
) -> tuple[dict[str, Any], bool]:
    """Full ``replay_metadata.json`` body. Returns ``(envelope, ambiguous)``."""

    replay_hash = raw.get("replay_content_sha256")
    parser_family = raw.get("parser_family")
    parser_version = raw.get("parser_version")
    if not isinstance(parser_family, str):
        parser_family = "unknown"
    if not isinstance(parser_version, str):
        parser_version = "unknown"

    rs = raw.get("raw_sections")
    present = source_sections_present(rs)

    inner, ambiguous = build_normalized_metadata(raw)
    env = {
        "metadata": inner,
        "metadata_contract_version": METADATA_CONTRACT_VERSION,
        "metadata_profile": METADATA_PROFILE,
        "parser_family": parser_family,
        "parser_version": parser_version,
        "replay_content_sha256": replay_hash if isinstance(replay_hash, str) else None,
        "schema_version": METADATA_SCHEMA_VERSION,
        "source_raw_parse_sha256": source_raw_parse_sha256,
        "source_sections_present": present,
    }
    return env, ambiguous


def required_sections_non_null(raw: dict[str, Any]) -> bool:
    rs = raw.get("raw_sections")
    if not isinstance(rs, dict):
        return False
    for key in ("header", "details", "init_data"):
        if rs.get(key) is None:
            return False
    return True


def core_metadata_ok(metadata: dict[str, Any]) -> bool:
    """True if protocol ints present and game block is structurally complete."""

    prot = metadata.get("protocol")
    if not isinstance(prot, dict):
        return False
    if not isinstance(prot.get("base_build"), int):
        return False
    if not isinstance(prot.get("data_build"), int):
        return False
    game = metadata.get("game")
    if not isinstance(game, dict):
        return False
    if not isinstance(game.get("player_count"), int):
        return False
    ev = game.get("event_streams_available")
    if not isinstance(ev, dict):
        return False
    return True


def player_rows_complete(players: list[dict[str, Any]]) -> bool:
    """True if each player row has required keys (unknown enum values still count)."""

    keys = ("player_index", "player_kind", "race_requested", "race_actual", "result")
    for _p in players:
        if not all(k in _p for k in keys):
            return False
    return True


__all__ = [
    "RAW_PARSE_SCHEMA_ACCEPTED",
    "RAW_PARSE_SCHEMA_EXPECTED",
    "build_metadata_envelope",
    "build_normalized_metadata",
    "core_metadata_ok",
    "extract_players",
    "map_player_kind",
    "map_race_actual",
    "map_race_requested",
    "map_result",
    "player_rows_complete",
    "required_sections_non_null",
    "source_sections_present",
]
