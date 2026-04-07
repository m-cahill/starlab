"""Pure extraction: M10 timeline + M11 build-order/economy (+ optional raw).

Combat / scouting / visibility surface (M12).
"""

from __future__ import annotations

from typing import Any

from starlab.replays.build_order_economy_models import BUILD_ORDER_ECONOMY_CONTRACT_VERSION
from starlab.replays.combat_scouting_visibility_catalog import ENTITY_ROLE, STRUCTURE_ROLES
from starlab.replays.combat_scouting_visibility_models import (
    CATALOG_NAME,
    COMBAT_SCOUTING_VISIBILITY_CONTRACT_VERSION,
    COMBAT_SCOUTING_VISIBILITY_PROFILE,
    COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION,
    COMBAT_WINDOW_GAP_LOOPS,
    COMBAT_WINDOW_MODEL,
    ORDERING_POLICY,
    SCOUTING_MODEL,
    VISIBILITY_MODEL,
)
from starlab.replays.timeline_models import TIMELINE_CONTRACT_VERSION

TIMELINE_SCHEMA_ACCEPTED = frozenset({"starlab.replay_timeline.v1"})
BUILD_ORDER_ECONOMY_SCHEMA_ACCEPTED = frozenset({"starlab.replay_build_order_economy.v1"})

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


def _role_for_entity_name(name: str | None) -> str:
    if not name:
        return "unknown"
    return ENTITY_ROLE.get(name, "unknown")


def _xy_from_raw_event(ev: dict[str, Any]) -> tuple[float, float] | None:
    x = ev.get("m_x")
    y = ev.get("m_y")
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return float(x), float(y)
    return None


def validate_timeline_contract(timeline: dict[str, Any]) -> tuple[bool, str | None]:
    sv = timeline.get("schema_version")
    if sv not in TIMELINE_SCHEMA_ACCEPTED:
        return False, "unsupported or missing timeline schema_version"
    cv = timeline.get("timeline_contract_version")
    if cv != TIMELINE_CONTRACT_VERSION:
        return False, "unsupported timeline_contract_version"
    rhash = timeline.get("replay_content_sha256")
    if not isinstance(rhash, str) or len(rhash) != 64:
        return False, "replay_content_sha256 missing or not 64-hex"
    return True, None


def validate_build_order_economy_contract(boe: dict[str, Any]) -> tuple[bool, str | None]:
    sv = boe.get("schema_version")
    if sv not in BUILD_ORDER_ECONOMY_SCHEMA_ACCEPTED:
        return False, "unsupported or missing build_order_economy schema_version"
    cv = boe.get("build_order_economy_contract_version")
    if cv != BUILD_ORDER_ECONOMY_CONTRACT_VERSION:
        return False, "unsupported build_order_economy_contract_version"
    rhash = boe.get("replay_content_sha256")
    if not isinstance(rhash, str) or len(rhash) != 64:
        return False, "replay_content_sha256 missing or not 64-hex"
    return True, None


def _m11_step_by_timeline_index(boe: dict[str, Any]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    steps = boe.get("build_order_steps")
    if not isinstance(steps, list):
        return out
    for s in steps:
        if not isinstance(s, dict):
            continue
        tli = s.get("source_timeline_index")
        if isinstance(tli, int) and not isinstance(tli, bool):
            out[tli] = s
    return out


def _evidence_model(
    *,
    raw_ev: dict[str, Any] | None,
    tl_idx: int,
    steps_by_tl: dict[int, dict[str, Any]],
) -> str:
    if raw_ev is not None:
        return "timeline_plus_raw"
    if tl_idx in steps_by_tl:
        return "timeline_plus_macro"
    return "timeline_only"


def _scouting_signal_kind(*, role: str, townhall_index: int) -> str | None:
    if role == "townhall":
        if townhall_index == 1:
            return "enemy_townhall_first_seen"
        if townhall_index == 2:
            return "enemy_expansion_first_seen"
        return None
    if role == "gas_structure":
        return "enemy_gas_first_seen"
    if role == "production_structure":
        return "enemy_production_first_seen"
    if role == "tech_structure":
        return "enemy_tech_first_seen"
    if role == "army":
        return "enemy_army_first_seen"
    if role in ("scout", "detector"):
        return "enemy_army_first_seen"
    return None


def extract_combat_scouting_visibility_envelope(
    *,
    timeline: dict[str, Any],
    source_timeline_sha256: str,
    build_order_economy: dict[str, Any],
    source_build_order_economy_sha256: str,
    raw_parse: dict[str, Any] | None,
    source_raw_parse_sha256: str | None,
    source_timeline_report_sha256: str | None,
    source_build_order_economy_report_sha256: str | None,
    source_metadata_sha256: str | None,
    source_metadata_report_sha256: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return artifact body and partial report (no file writes)."""

    warnings: list[str] = []
    unclassified: set[str] = set()
    unsupported_signal_kinds: set[str] = set()

    entries = timeline.get("entries")
    if not isinstance(entries, list):
        entries = []

    sorted_entries = sorted(
        [e for e in entries if isinstance(e, dict)],
        key=lambda e: _int_field(e, "timeline_index"),
    )

    steps_by_tl = _m11_step_by_timeline_index(build_order_economy)

    # --- Combat: unit_died clustering ---
    deaths: list[dict[str, Any]] = []
    for entry in sorted_entries:
        if entry.get("semantic_kind") != "unit_died":
            continue
        src_stream = entry.get("source_stream")
        src_idx = entry.get("source_event_index")
        if (
            not isinstance(src_stream, str)
            or not isinstance(src_idx, int)
            or isinstance(src_idx, bool)
        ):
            warnings.append("unit_died missing source_stream or source_event_index; skipped")
            continue
        victim = _player_index_from_entry(entry)
        if victim is None:
            warnings.append("unit_died missing player_index; skipped")
            continue
        deaths.append(
            {
                "entry": entry,
                "gameloop": _int_field(entry, "gameloop"),
                "timeline_index": _int_field(entry, "timeline_index"),
                "victim_player_index": victim,
                "source_stream": src_stream,
                "source_event_index": src_idx,
            },
        )

    combat_windows: list[dict[str, Any]] = []
    window_index = 0
    i = 0
    while i < len(deaths):
        cluster = [deaths[i]]
        j = i + 1
        while j < len(deaths):
            prev_gl = cluster[-1]["gameloop"]
            cur_gl = deaths[j]["gameloop"]
            if cur_gl - prev_gl > COMBAT_WINDOW_GAP_LOOPS:
                break
            cluster.append(deaths[j])
            j += 1

        start_gl = cluster[0]["gameloop"]
        end_gl = cluster[-1]["gameloop"]
        start_ti = cluster[0]["timeline_index"]
        end_ti = cluster[-1]["timeline_index"]
        victims = [c["victim_player_index"] for c in cluster]
        players_involved = sorted(set(victims))
        death_count = len(cluster)

        deaths_by_player: dict[str, int] = {}
        for v in victims:
            deaths_by_player[str(v)] = deaths_by_player.get(str(v), 0) + 1

        losses_by_role: dict[str, int] = {}
        x_sum = 0.0
        y_sum = 0.0
        pos_n = 0
        for death in cluster:
            raw_ev = _lookup_raw_event(
                raw_parse,
                source_stream=death["source_stream"],
                source_event_index=death["source_event_index"],
            )
            victim_type: str | None = None
            if raw_ev is not None:
                victim_type, _k = _identity_name_from_raw_event(raw_ev)
            role = _role_for_entity_name(victim_type)
            if role == "unknown" and victim_type:
                unclassified.add(victim_type)
            losses_by_role[role] = losses_by_role.get(role, 0) + 1
            if raw_ev is not None:
                xy = _xy_from_raw_event(raw_ev)
                if xy is not None:
                    x_sum += xy[0]
                    y_sum += xy[1]
                    pos_n += 1

        row_c: dict[str, Any] = {
            "window_index": window_index,
            "start_gameloop": start_gl,
            "end_gameloop": end_gl,
            "start_timeline_index": start_ti,
            "end_timeline_index": end_ti,
            "players_involved": players_involved,
            "death_count": death_count,
            "deaths_by_player": dict(sorted(deaths_by_player.items())),
            "losses_by_role": dict(sorted(losses_by_role.items())),
        }
        if pos_n > 0:
            row_c["location_centroid"] = {"x": x_sum / pos_n, "y": y_sum / pos_n}
            row_c["location_model"] = "raw_position"
        else:
            row_c["location_model"] = "omitted"

        combat_windows.append(row_c)
        window_index += 1
        i = j

    # --- Scouting: first-seen ---
    scouting_observations: list[dict[str, Any]] = []
    observation_index = 0

    townhall_tags_seen: dict[int, set[str]] = {}
    townhall_event_count: dict[int, int] = {}
    first_seen_flags: dict[tuple[int, str], bool] = {}

    def _ensure_tags(pid: int) -> set[str]:
        if pid not in townhall_tags_seen:
            townhall_tags_seen[pid] = set()
        return townhall_tags_seen[pid]

    for entry in sorted_entries:
        sk = entry.get("semantic_kind")
        if not isinstance(sk, str):
            continue
        if sk not in ("unit_born", "unit_init"):
            continue

        player_index = _player_index_from_entry(entry)
        if player_index is None:
            continue

        src_stream = entry.get("source_stream")
        src_idx = entry.get("source_event_index")
        if (
            not isinstance(src_stream, str)
            or not isinstance(src_idx, int)
            or isinstance(src_idx, bool)
        ):
            continue

        tl_idx = _int_field(entry, "timeline_index")
        raw_ev = _lookup_raw_event(raw_parse, source_stream=src_stream, source_event_index=src_idx)
        identity_name: str | None
        if raw_ev is not None:
            identity_name, _kh = _identity_name_from_raw_event(raw_ev)
        else:
            identity_name = None
            if isinstance(steps_by_tl.get(tl_idx), dict):
                en = steps_by_tl[tl_idx].get("entity_name")
                identity_name = en if isinstance(en, str) else None
            if raw_parse is not None and identity_name is None:
                warnings.append(
                    f"raw_event lookup miss for ({src_stream!r}, {src_idx}); "
                    "scouting identity thin",
                )

        role = _role_for_entity_name(identity_name)
        if identity_name and role == "unknown":
            unclassified.add(identity_name)

        # M11 category hint
        m11_cat: str | None = None
        step_row = steps_by_tl.get(tl_idx)
        if isinstance(step_row, dict):
            cat_raw = step_row.get("category")
            if isinstance(cat_raw, str):
                m11_cat = cat_raw
        if role == "unknown" and m11_cat:
            # Map M11 category string to M12 role
            if m11_cat == "combat_or_other":
                role = "army"
            elif m11_cat in STRUCTURE_ROLES or m11_cat in (
                "worker",
                "gas_structure",
                "production_structure",
                "tech_structure",
                "townhall",
                "supply_provider",
            ):
                role = {
                    "worker": "worker",
                    "townhall": "townhall",
                    "gas_structure": "gas_structure",
                    "supply_provider": "supply_provider",
                    "production_structure": "production_structure",
                    "tech_structure": "tech_structure",
                    "combat_or_other": "army",
                }.get(m11_cat, "unknown")

        ut = entry.get("unit_tag")
        unit_tag_s = ut if isinstance(ut, str) else None

        # Townhall counting (expansion detection): prefer unit_tag dedupe
        th_idx_for_signal: int | None = None
        if role == "townhall":
            if unit_tag_s:
                tags = _ensure_tags(player_index)
                if unit_tag_s not in tags:
                    tags.add(unit_tag_s)
                    th_idx_for_signal = len(tags)
            else:
                townhall_event_count[player_index] = townhall_event_count.get(player_index, 0) + 1
                th_idx_for_signal = townhall_event_count[player_index]

        sig_kind: str | None = None
        if role == "townhall" and th_idx_for_signal is not None:
            sig_kind = _scouting_signal_kind(role=role, townhall_index=th_idx_for_signal)
        elif role in (
            "gas_structure",
            "production_structure",
            "tech_structure",
            "army",
            "scout",
            "detector",
        ):
            key: tuple[int, str]
            if role in ("army", "scout", "detector"):
                # One first-seen bucket per subject for army-line (Reaper before Marine).
                key = (player_index, "army_line_first_seen")
            else:
                key = (player_index, role)
            if key not in first_seen_flags:
                first_seen_flags[key] = True
                if role in ("army", "scout", "detector"):
                    sig_kind = "enemy_army_first_seen"
                else:
                    sig_kind = _scouting_signal_kind(role=role, townhall_index=0)

        if sig_kind is None:
            continue

        evm = _evidence_model(raw_ev=raw_ev, tl_idx=tl_idx, steps_by_tl=steps_by_tl)
        obs_row: dict[str, Any] = {
            "observation_index": observation_index,
            "gameloop": _int_field(entry, "gameloop"),
            "source_timeline_index": tl_idx,
            "subject_player_index": player_index,
            "signal_kind": sig_kind,
            "entity_name": identity_name if identity_name else "unknown",
            "entity_role": role,
            "evidence_model": evm,
        }
        if unit_tag_s:
            obs_row["unit_tag"] = unit_tag_s
        scouting_observations.append(obs_row)
        observation_index += 1

    # --- Visibility: observation_proxy by unit_tag ---
    visibility_windows: list[dict[str, Any]] = []
    by_tag: dict[str, list[dict[str, Any]]] = {}
    vis_kinds = frozenset(
        {
            "unit_born",
            "unit_init",
            "unit_died",
            "unit_type_changed",
        },
    )
    for entry in sorted_entries:
        sk = entry.get("semantic_kind")
        if sk not in vis_kinds:
            continue
        ut = entry.get("unit_tag")
        if not isinstance(ut, str) or not ut:
            continue
        by_tag.setdefault(ut, []).append(entry)

    vw_i = 0
    for tag in sorted(by_tag.keys()):
        evs = sorted(by_tag[tag], key=lambda e: _int_field(e, "timeline_index"))
        gls = [_int_field(e, "gameloop") for e in evs]
        tis = [_int_field(e, "timeline_index") for e in evs]
        start_gl, end_gl = min(gls), max(gls)
        start_ti, end_ti = min(tis), max(tis)
        subj: int | None = None
        ent_name = "unknown"
        for e in evs:
            subj = _player_index_from_entry(e)
            if subj is not None:
                break
        for e in evs:
            ss = e.get("source_stream")
            si = e.get("source_event_index")
            if not isinstance(ss, str) or not isinstance(si, int) or isinstance(si, bool):
                continue
            if e.get("semantic_kind") not in ("unit_born", "unit_init", "unit_died"):
                continue
            rev = _lookup_raw_event(raw_parse, source_stream=ss, source_event_index=si)
            if rev is not None:
                n, _k = _identity_name_from_raw_event(rev)
                if n:
                    ent_name = n
                    break

        er = _role_for_entity_name(ent_name if ent_name != "unknown" else None)
        if ent_name != "unknown" and er == "unknown":
            unclassified.add(ent_name)

        vrow: dict[str, Any] = {
            "window_index": vw_i,
            "start_gameloop": start_gl,
            "end_gameloop": end_gl,
            "start_timeline_index": start_ti,
            "end_timeline_index": end_ti,
            "entity_name": ent_name,
            "entity_role": er,
            "unit_tag": tag,
            "visibility_model": "observation_proxy",
        }
        if subj is not None:
            vrow["subject_player_index"] = subj
        visibility_windows.append(vrow)
        vw_i += 1

    if not by_tag and sorted_entries:
        warnings.append(
            "no unit_tag on timeline entries; visibility_windows empty "
            "(observation_proxy requires tags)",
        )

    body: dict[str, Any] = {
        "combat_scouting_visibility_contract_version": COMBAT_SCOUTING_VISIBILITY_CONTRACT_VERSION,
        "combat_scouting_visibility_profile": COMBAT_SCOUTING_VISIBILITY_PROFILE,
        "schema_version": COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION,
        "replay_content_sha256": timeline.get("replay_content_sha256"),
        "source_timeline_sha256": source_timeline_sha256,
        "source_build_order_economy_sha256": source_build_order_economy_sha256,
        "source_timeline_report_sha256": source_timeline_report_sha256,
        "source_build_order_economy_report_sha256": source_build_order_economy_report_sha256,
        "source_metadata_sha256": source_metadata_sha256,
        "source_metadata_report_sha256": source_metadata_report_sha256,
        "source_raw_parse_sha256": source_raw_parse_sha256,
        "ordering_policy": ORDERING_POLICY,
        "combat_window_model": COMBAT_WINDOW_MODEL,
        "scouting_model": SCOUTING_MODEL,
        "visibility_model": VISIBILITY_MODEL,
        "combat_window_gap_loops": COMBAT_WINDOW_GAP_LOOPS,
        "classification_profile": {"catalog_name": CATALOG_NAME},
        "combat_windows": combat_windows,
        "scouting_observations": scouting_observations,
        "visibility_windows": visibility_windows,
    }
    return body, {
        "warnings": sorted(set(warnings)),
        "unsupported_signal_kinds": sorted(unsupported_signal_kinds),
        "unclassified_entity_names": sorted(unclassified),
    }
