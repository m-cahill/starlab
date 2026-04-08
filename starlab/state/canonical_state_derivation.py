"""Deterministic canonical state frame derivation from governed M09–M13 JSON (M16)."""

from __future__ import annotations

from typing import Any

from starlab.state.canonical_state_inputs import M14BundleInputs
from starlab.state.canonical_state_models import CANONICAL_STATE_FRAME_SCHEMA_VERSION


def _canonical_player_index_from_m11_m12(player_index: int) -> int:
    """Map M11/M12 1-based player ids to canonical 0-based ``player_index``."""

    return player_index - 1 if player_index >= 1 else player_index


def _normalize_race(raw: str) -> str:
    m = raw.strip().lower()
    if m == "terran":
        return "Terran"
    if m == "protoss":
        return "Protoss"
    if m == "zerg":
        return "Zerg"
    if m == "random":
        return "Random"
    return "Random"


def _normalize_result(raw: str) -> str:
    m = raw.strip().lower()
    if m in ("win", "loss", "tie", "unknown"):
        return m
    return "unknown"


def compute_replay_length_loops(
    *,
    metadata: dict[str, Any],
    timeline: dict[str, Any],
) -> tuple[int, list[str]]:
    """Compute replay_length_loops and optional warnings."""

    warnings: list[str] = []
    meta_loops: int | None = None
    try:
        gl = metadata["metadata"]["game"]["game_length_loops"]
        meta_loops = int(gl)
    except (KeyError, TypeError, ValueError):
        meta_loops = None

    entries = timeline.get("entries") or []
    timeline_max = 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        g = e.get("gameloop")
        if isinstance(g, int):
            timeline_max = max(timeline_max, g)

    if meta_loops is None:
        return timeline_max, warnings

    r = max(meta_loops, timeline_max)
    if meta_loops != timeline_max:
        warnings.append(
            "metadata.game.game_length_loops differs from max timeline entry gameloop; "
            f"using replay_length_loops={r} (max of both)."
        )
    return r, warnings


def _economy_summary_for_player(
    *,
    boe: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> dict[str, Any]:
    steps_raw = boe.get("build_order_steps") or []
    steps: list[dict[str, Any]] = []
    for s in steps_raw:
        if not isinstance(s, dict):
            continue
        gl = s.get("gameloop")
        if not isinstance(gl, int) or gl > gameloop:
            continue
        pid = s.get("player_index")
        if not isinstance(pid, int):
            continue
        if _canonical_player_index_from_m11_m12(pid) != canonical_player_index:
            continue
        steps.append(s)

    unit_train = 0
    structure_train = 0
    for s in steps:
        ek = s.get("entity_kind")
        if ek == "unit":
            unit_train += 1
        elif ek == "structure":
            structure_train += 1

    resource_cat: str | None = None
    checkpoints_raw = boe.get("economy_checkpoints") or []
    checkpoints: list[dict[str, Any]] = []
    for c in checkpoints_raw:
        if not isinstance(c, dict):
            continue
        gl = c.get("gameloop")
        if not isinstance(gl, int) or gl > gameloop:
            continue
        pid = c.get("player_index")
        if not isinstance(pid, int):
            continue
        if _canonical_player_index_from_m11_m12(pid) != canonical_player_index:
            continue
        checkpoints.append(c)
    checkpoints.sort(key=lambda x: (int(x.get("checkpoint_index", 0)), int(x.get("gameloop", 0))))
    if checkpoints:
        last = checkpoints[-1]
        w = int(last.get("workers_completed") or 0)
        if w <= 0:
            resource_cat = "low"
        elif w <= 5:
            resource_cat = "medium"
        else:
            resource_cat = "high"

    out: dict[str, Any] = {
        "structure_train_events_total": structure_train,
        "unit_train_events_total": unit_train,
    }
    if resource_cat is not None:
        out["resource_signal_category"] = resource_cat
    else:
        out["resource_signal_category"] = None
    return out


def _production_summary_for_player(
    *,
    boe: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> dict[str, Any]:
    """Infer production queue + tech starts from M11 steps (conservative)."""

    steps_raw = boe.get("build_order_steps") or []
    by_step: dict[int, dict[str, Any]] = {}
    for s in steps_raw:
        if not isinstance(s, dict):
            continue
        gl = s.get("gameloop")
        if not isinstance(gl, int) or gl > gameloop:
            continue
        pid = s.get("player_index")
        if not isinstance(pid, int):
            continue
        if _canonical_player_index_from_m11_m12(pid) != canonical_player_index:
            continue
        si = s.get("step_index")
        if not isinstance(si, int):
            continue
        # Last update for this step_index at or before gameloop wins.
        prev = by_step.get(si)
        if prev is None or int(prev.get("gameloop", -1)) <= gl:
            by_step[si] = s

    active_queue = 0
    tech_started = 0
    for _si, s in sorted(by_step.items()):
        phase = s.get("phase")
        cat = str(s.get("category") or "")
        if phase == "started":
            active_queue += 1
        if "tech" in cat.lower() or "upgrade" in str(s.get("entity_name") or "").lower():
            tech_started += 1

    return {
        "active_build_queue_count": active_queue,
        "tech_upgrades_started_total": tech_started,
    }


def _army_summary_for_player(
    *,
    boe: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> dict[str, Any]:
    steps_raw = boe.get("build_order_steps") or []
    counts: dict[str, int] = {}
    for s in steps_raw:
        if not isinstance(s, dict):
            continue
        if s.get("entity_kind") != "unit":
            continue
        gl = s.get("gameloop")
        if not isinstance(gl, int) or gl > gameloop:
            continue
        pid = s.get("player_index")
        if not isinstance(pid, int):
            continue
        if _canonical_player_index_from_m11_m12(pid) != canonical_player_index:
            continue
        cat = str(s.get("category") or "unknown")
        bucket = (
            "heavy"
            if cat == "combat_or_other"
            else "light"
            if cat in ("worker", "scout")
            else "other"
        )
        counts[bucket] = counts.get(bucket, 0) + 1
    return {"army_unit_category_counts": counts}


def _combat_window_id(window: dict[str, Any]) -> str:
    wi = window.get("window_index")
    if isinstance(wi, int):
        return f"combat_window:{wi}"
    return "combat_window:unknown"


def _combat_active_at_gameloop(*, csv_doc: dict[str, Any], gameloop: int) -> list[str]:
    out: list[str] = []
    for w in csv_doc.get("combat_windows") or []:
        if not isinstance(w, dict):
            continue
        a = w.get("start_gameloop")
        b = w.get("end_gameloop")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        if a <= gameloop <= b:
            out.append(_combat_window_id(w))
    return sorted(set(out))


def _player_combat_window_ids(
    *,
    csv_doc: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> list[str]:
    out: list[str] = []
    for w in csv_doc.get("combat_windows") or []:
        if not isinstance(w, dict):
            continue
        a = w.get("start_gameloop")
        b = w.get("end_gameloop")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        if not (a <= gameloop <= b):
            continue
        inv = w.get("players_involved") or []
        ok = False
        for p in inv:
            if isinstance(p, int):
                cpi = _canonical_player_index_from_m11_m12(p)
                if cpi == canonical_player_index:
                    ok = True
                    break
            if isinstance(p, str) and p.isdigit():
                if _canonical_player_index_from_m11_m12(int(p)) == canonical_player_index:
                    ok = True
                    break
        if ok:
            out.append(_combat_window_id(w))
    return sorted(set(out))


def _scouting_event_count(
    *,
    csv_doc: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> int:
    proto = canonical_player_index + 1
    n = 0
    for o in csv_doc.get("scouting_observations") or []:
        if not isinstance(o, dict):
            continue
        gl = o.get("gameloop")
        if not isinstance(gl, int) or gl > gameloop:
            continue
        sp = o.get("subject_player_index")
        if isinstance(sp, int) and sp == proto:
            n += 1
    return n


def _visibility_context_for_player(
    *,
    csv_doc: dict[str, Any],
    canonical_player_index: int,
    gameloop: int,
) -> dict[str, Any] | None:
    proto = canonical_player_index + 1
    hits = 0
    for vw in csv_doc.get("visibility_windows") or []:
        if not isinstance(vw, dict):
            continue
        a = vw.get("start_gameloop")
        b = vw.get("end_gameloop")
        if not isinstance(a, int) or not isinstance(b, int):
            continue
        if not (a <= gameloop <= b):
            continue
        sp = vw.get("subject_player_index")
        if isinstance(sp, int) and sp == proto:
            hits += 1
    if hits == 0:
        return None
    level = "high" if hits >= 3 else "medium"
    return {
        "visibility_proxy_level": level,
        "visibility_signal_non_truth_disclaimer": "starlab.visibility_proxy_not_fog_of_war_truth",
    }


def derive_canonical_state_frame(
    bundle: M14BundleInputs,
    *,
    target_gameloop: int,
) -> tuple[dict[str, Any], list[str]]:
    """Return ``(canonical_state_object, warnings)`` for one ``target_gameloop``."""

    warnings: list[str] = []

    metadata = bundle.replay_metadata
    timeline = bundle.replay_timeline
    boe = bundle.replay_build_order_economy
    csv_doc = bundle.replay_combat_scouting_visibility
    slices = bundle.replay_slices
    manifest = bundle.manifest

    replay_len, wlen = compute_replay_length_loops(metadata=metadata, timeline=timeline)
    warnings.extend(wlen)

    if target_gameloop < 0:
        msg = f"target_gameloop must be non-negative, got {target_gameloop}"
        raise ValueError(msg)
    if target_gameloop > replay_len:
        msg = f"target_gameloop {target_gameloop} exceeds replay_length_loops {replay_len}"
        raise ValueError(msg)

    meta_players = (metadata.get("metadata") or {}).get("players") or []
    players_out: list[dict[str, Any]] = []

    def _meta_player_sort_key(x: Any) -> int:
        if isinstance(x, dict) and isinstance(x.get("player_index"), int):
            return int(x["player_index"])
        return 0

    for p in sorted(meta_players, key=_meta_player_sort_key):
        if not isinstance(p, dict):
            continue
        idx = p.get("player_index")
        if not isinstance(idx, int):
            continue
        race = _normalize_race(str(p.get("race_actual") or "random"))
        pl: dict[str, Any] = {
            "army_summary": _army_summary_for_player(
                boe=boe,
                canonical_player_index=idx,
                gameloop=target_gameloop,
            ),
            "economy_summary": _economy_summary_for_player(
                boe=boe,
                canonical_player_index=idx,
                gameloop=target_gameloop,
            ),
            "player_index": idx,
            "production_summary": _production_summary_for_player(
                boe=boe,
                canonical_player_index=idx,
                gameloop=target_gameloop,
            ),
            "race_actual": race,
        }
        if "result" in p and isinstance(p.get("result"), str):
            pl["result"] = _normalize_result(str(p["result"]))

        pc = _player_combat_window_ids(
            canonical_player_index=idx,
            csv_doc=csv_doc,
            gameloop=target_gameloop,
        )
        if pc:
            pl["combat_context"] = {"active_combat_window_ids": pc}

        sc = _scouting_event_count(
            canonical_player_index=idx,
            csv_doc=csv_doc,
            gameloop=target_gameloop,
        )
        if sc > 0:
            pl["scouting_context"] = {"recent_scout_events_count": sc}

        vc = _visibility_context_for_player(
            canonical_player_index=idx,
            csv_doc=csv_doc,
            gameloop=target_gameloop,
        )
        if vc is not None:
            pl["visibility_context"] = vc

        players_out.append(pl)

    if not players_out:
        msg = "replay_metadata.json: no players[] entries to materialize"
        raise ValueError(msg)

    map_name = str(((metadata.get("metadata") or {}).get("map") or {}).get("map_name") or "")

    active_slices: list[str] = []
    for sl in slices.get("slices") or []:
        if not isinstance(sl, dict):
            continue
        a = sl.get("start_gameloop")
        b = sl.get("end_gameloop")
        sid = sl.get("slice_id")
        if not isinstance(a, int) or not isinstance(b, int) or not isinstance(sid, str):
            continue
        if a <= target_gameloop <= b:
            active_slices.append(sid)
    active_slices = sorted(set(active_slices))

    combat_global = _combat_active_at_gameloop(csv_doc=csv_doc, gameloop=target_gameloop)

    global_ctx: dict[str, Any] = {}
    if map_name:
        global_ctx["map_name"] = map_name
    if active_slices:
        global_ctx["active_slice_ids"] = active_slices
    if combat_global:
        global_ctx["active_combat_window_ids"] = combat_global

    source: dict[str, Any] = {}
    bid = manifest.get("bundle_id")
    if isinstance(bid, str) and bid:
        source["source_bundle_id"] = bid
    lr = manifest.get("lineage_root")
    if isinstance(lr, str) and lr:
        source["source_lineage_root"] = lr
    sri = manifest.get("source_replay_identity")
    if isinstance(sri, str) and sri:
        source["source_replay_identity"] = sri

    frame: dict[str, Any] = {
        "frame_kind": "replay_derived",
        "gameloop": target_gameloop,
        "global_context": global_ctx,
        "players": players_out,
        "provenance": {
            "uses_build_order_economy_plane": True,
            "uses_combat_scouting_visibility_plane": True,
            "uses_metadata_plane": True,
            "uses_replay_bundle_plane": True,
            "uses_slice_plane": True,
            "uses_timeline_plane": True,
        },
        "schema_version": CANONICAL_STATE_FRAME_SCHEMA_VERSION,
        "source": source,
    }
    return frame, warnings
