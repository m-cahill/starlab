"""Bounded observation → context signature projection (M27)."""

from __future__ import annotations

from typing import Any


def _norm_race(raw: str | None) -> str:
    if not isinstance(raw, str) or not raw:
        return "unknown"
    return raw.strip().lower()


def _scalar_map(observation_frame: dict[str, Any]) -> dict[str, Any]:
    sf = observation_frame.get("scalar_features")
    if not isinstance(sf, dict):
        return {}
    entries = sf.get("ordered_entries")
    if not isinstance(entries, list):
        return {}
    out: dict[str, Any] = {}
    for e in entries:
        if isinstance(e, dict) and isinstance(e.get("name"), str):
            out[e["name"]] = e.get("value")
    return out


def _player_by_index(players: list[dict[str, Any]], idx: int) -> dict[str, Any] | None:
    for p in players:
        if isinstance(p, dict) and p.get("player_index") == idx:
            return p
    return None


def _opponent_race(canonical_state: dict[str, Any], perspective_player_index: int) -> str:
    players_raw = canonical_state.get("players")
    if not isinstance(players_raw, list):
        return "unknown"
    players: list[dict[str, Any]] = [p for p in players_raw if isinstance(p, dict)]
    others: list[dict[str, Any]] = []
    for p in players:
        pi = p.get("player_index")
        if isinstance(pi, int) and pi != perspective_player_index:
            others.append(p)
    if not others:
        return "unknown"
    others.sort(key=lambda x: int(x.get("player_index", 0)))
    return _norm_race(others[0].get("race_actual"))


def _bucket_thresholds(n: int, thresholds: tuple[int, ...]) -> str:
    """Map non-negative ``n`` to ``b0``, ``b1``, … by cumulative thresholds."""

    for i, t in enumerate(thresholds):
        if n <= t:
            return f"b{i}"
    return f"b{len(thresholds)}"


def _enemy_army_total(observation_frame: dict[str, Any]) -> int:
    rows_wrap = observation_frame.get("entity_rows")
    if not isinstance(rows_wrap, dict):
        return 0
    rlist = rows_wrap.get("rows")
    if not isinstance(rlist, list):
        return 0
    total = 0
    for r in rlist:
        if not isinstance(r, dict):
            continue
        if r.get("owner_view") != "enemy":
            continue
        c = r.get("count")
        if isinstance(c, int) and not isinstance(c, bool):
            total += c
    return total


def _self_army_total(observation_frame: dict[str, Any]) -> int:
    rows_wrap = observation_frame.get("entity_rows")
    if not isinstance(rows_wrap, dict):
        return 0
    rlist = rows_wrap.get("rows")
    if not isinstance(rlist, list):
        return 0
    total = 0
    for r in rlist:
        if not isinstance(r, dict):
            continue
        if r.get("owner_view") != "self":
            continue
        c = r.get("count")
        if isinstance(c, int) and not isinstance(c, bool):
            total += c
    return total


def game_phase_bucket(gameloop: int) -> str:
    """Coarse game phase from gameloop (deterministic, audit-friendly)."""

    if gameloop < 0:
        msg = "gameloop must be non-negative"
        raise ValueError(msg)
    if gameloop < 400:
        return "very_early"
    if gameloop < 900:
        return "early"
    if gameloop < 1500:
        return "mid"
    if gameloop < 2400:
        return "late"
    return "very_late"


def visible_enemy_presence_bucket(enemy_army_total: int) -> str:
    if enemy_army_total <= 0:
        return "none"
    if enemy_army_total <= 2:
        return "low"
    if enemy_army_total <= 6:
        return "medium"
    return "high"


def build_context_signature(
    *,
    observation_frame: dict[str, Any],
    canonical_state: dict[str, Any],
    perspective_player_index: int,
) -> str:
    """Return deterministic ``context_signature`` for M27 observation_signature_v1."""

    meta = observation_frame.get("metadata")
    if not isinstance(meta, dict):
        msg = "observation_frame.metadata must be an object"
        raise ValueError(msg)
    gl = meta.get("gameloop")
    if not isinstance(gl, int) or isinstance(gl, bool):
        msg = "metadata.gameloop must be an integer"
        raise ValueError(msg)

    smap = _scalar_map(observation_frame)
    ra = smap.get("race.actual")
    perspective_race = _norm_race(ra if isinstance(ra, str) else None)

    opp = _opponent_race(canonical_state, perspective_player_index)
    gpb = game_phase_bucket(gl)

    utrain = smap.get("economy.unit_train_events_total")
    strain = smap.get("economy.structure_train_events_total")
    ut = int(utrain) if isinstance(utrain, int) and not isinstance(utrain, bool) else 0
    st = int(strain) if isinstance(strain, int) and not isinstance(strain, bool) else 0
    supply_proxy = ut + st
    supply_used_bucket = _bucket_thresholds(supply_proxy, (0, 3, 8))

    players_raw = canonical_state.get("players")
    if not isinstance(players_raw, list):
        msg = "canonical_state.players must be an array"
        raise ValueError(msg)
    players: list[dict[str, Any]] = [p for p in players_raw if isinstance(p, dict)]
    perspective = _player_by_index(players, perspective_player_index)
    if perspective is None:
        msg = f"perspective_player_index {perspective_player_index} not found in canonical_state"
        raise ValueError(msg)

    es = perspective.get("economy_summary")
    ps = perspective.get("production_summary")
    econ = es if isinstance(es, dict) else {}
    prod = ps if isinstance(ps, dict) else {}

    str_train = econ.get("structure_train_events_total")
    st_ev = int(str_train) if isinstance(str_train, int) and not isinstance(str_train, bool) else 0
    base_count_bucket = _bucket_thresholds(st_ev, (0, 1))

    am = perspective.get("army_summary")
    ac = am if isinstance(am, dict) else {}
    raw_counts = ac.get("army_unit_category_counts")
    worker_n = 0
    if isinstance(raw_counts, dict):
        wk = raw_counts.get("worker")
        if isinstance(wk, int) and not isinstance(wk, bool):
            worker_n = wk
    worker_count_bucket = _bucket_thresholds(worker_n, (0, 2, 5))

    army_n = _self_army_total(observation_frame)
    army_count_bucket = _bucket_thresholds(army_n, (0, 2, 6))

    enemy_tot = _enemy_army_total(observation_frame)
    veb = visible_enemy_presence_bucket(enemy_tot)

    tech = prod.get("tech_upgrades_started_total")
    tech_n = int(tech) if isinstance(tech, int) and not isinstance(tech, bool) else 0
    upgrade_progress_presence = "yes" if tech_n > 0 else "no"

    parts: dict[str, str] = {
        "army_count_bucket": army_count_bucket,
        "base_count_bucket": base_count_bucket,
        "game_phase_bucket": gpb,
        "opponent_race": opp,
        "perspective_race": perspective_race,
        "supply_used_bucket": supply_used_bucket,
        "upgrade_progress_presence": upgrade_progress_presence,
        "visible_enemy_presence_bucket": veb,
        "worker_count_bucket": worker_count_bucket,
    }

    # Single-line signature: sorted ``key=value`` joined by ``|`` (keys are ASCII).
    return "|".join(f"{k}={parts[k]}" for k in sorted(parts.keys()))

