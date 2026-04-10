"""Build replay explorer surface + report artifacts (M31)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.explorer.replay_explorer_models import (
    COMBAT_SCOUTING_EXCERPT_MAX,
    DEFAULT_NON_CLAIMS,
    ECONOMY_EXCERPT_MAX,
    OBSERVATION_SCALAR_ENTRIES_MAX,
    REPORT_VERSION,
    SELECTION_POLICY_ID,
    SURFACE_VERSION,
    TIMELINE_EXCERPT_MAX,
)
from starlab.explorer.replay_explorer_selection import (
    ordered_slices_for_explorer,
    slice_anchor_gameloop,
)
from starlab.hierarchy.delegate_policy import DELEGATE_POLICY_ID
from starlab.hierarchy.hierarchical_agent_models import (
    AGENT_VERSION,
    INTERFACE_TRACE_SCHEMA_VERSION,
)
from starlab.hierarchy.hierarchical_agent_predictor import FrozenHierarchicalImitationPredictor
from starlab.hierarchy.hierarchical_interface_schema import validate_hierarchical_trace_document
from starlab.imitation.baseline_features import build_context_signature
from starlab.imitation.replay_observation_materialization import (
    materialize_observation_for_observation_request,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def _load_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"expected JSON object in {path}"
        raise ValueError(msg)
    return raw


def _interval_anchor_distance(anchor: int, start: int, end: int) -> int:
    if start <= anchor <= end:
        return 0
    if anchor < start:
        return start - anchor
    return anchor - end


def timeline_excerpt_for_slice(
    timeline: dict[str, Any],
    *,
    start_gameloop: int,
    end_gameloop: int,
    anchor_gameloop: int,
) -> list[dict[str, Any]]:
    entries = timeline.get("entries")
    if not isinstance(entries, list):
        return []
    in_window: list[dict[str, Any]] = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        gl = e.get("gameloop")
        if not isinstance(gl, int) or isinstance(gl, bool):
            continue
        if start_gameloop <= gl <= end_gameloop:
            in_window.append(e)
    in_window.sort(
        key=lambda e: (
            abs(int(e["gameloop"]) - anchor_gameloop),
            int(e.get("timeline_index", 0)),
        ),
    )
    picked = in_window[:TIMELINE_EXCERPT_MAX]
    picked.sort(
        key=lambda e: (int(e["gameloop"]), int(e.get("timeline_index", 0))),
    )
    return picked


def economy_excerpt_for_slice(
    boe: dict[str, Any],
    *,
    start_gameloop: int,
    end_gameloop: int,
    anchor_gameloop: int,
) -> list[dict[str, Any]]:
    steps = boe.get("build_order_steps")
    if not isinstance(steps, list):
        return []
    in_window: list[dict[str, Any]] = []
    for s in steps:
        if not isinstance(s, dict):
            continue
        gl = s.get("gameloop")
        if not isinstance(gl, int) or isinstance(gl, bool):
            continue
        if start_gameloop <= gl <= end_gameloop:
            in_window.append(s)
    in_window.sort(
        key=lambda s: (
            abs(int(s["gameloop"]) - anchor_gameloop),
            int(s.get("step_index", 0)),
        ),
    )
    picked = in_window[:ECONOMY_EXCERPT_MAX]
    picked.sort(
        key=lambda s: (int(s["gameloop"]), int(s.get("step_index", 0))),
    )
    return picked


def combat_scouting_excerpt_for_slice(
    csv: dict[str, Any],
    *,
    slice_subject: int,
    start_gameloop: int,
    end_gameloop: int,
    anchor_gameloop: int,
) -> list[dict[str, Any]]:
    candidates: list[tuple[int, int, str, dict[str, Any]]] = []

    scouting = csv.get("scouting_observations")
    if isinstance(scouting, list):
        for obs in scouting:
            if not isinstance(obs, dict):
                continue
            if obs.get("subject_player_index") != slice_subject:
                continue
            gl = obs.get("gameloop")
            oidx = obs.get("observation_index")
            if not isinstance(gl, int) or isinstance(gl, bool):
                continue
            if not isinstance(oidx, int) or isinstance(oidx, bool):
                continue
            if not (start_gameloop <= gl <= end_gameloop):
                continue
            dist = abs(gl - anchor_gameloop)
            candidates.append((dist, 0, f"scout:{oidx}", obs))

    windows = csv.get("combat_windows")
    if isinstance(windows, list):
        for w in windows:
            if not isinstance(w, dict):
                continue
            ws = w.get("start_gameloop")
            we = w.get("end_gameloop")
            if not isinstance(ws, int) or not isinstance(we, int):
                continue
            if we < start_gameloop or ws > end_gameloop:
                continue
            widx = w.get("window_index")
            if not isinstance(widx, int) or isinstance(widx, bool):
                continue
            dist = _interval_anchor_distance(anchor_gameloop, ws, we)
            candidates.append((dist, 1, f"combat:{widx}", w))

    candidates.sort(key=lambda t: (t[0], t[1], t[2]))
    out: list[dict[str, Any]] = []
    for _d, _kind, tid, payload in candidates[:COMBAT_SCOUTING_EXCERPT_MAX]:
        kind = "scouting_observation" if tid.startswith("scout:") else "combat_window"
        out.append({"excerpt_kind": kind, "excerpt_id": tid, "payload": payload})
    return out


def canonical_state_excerpt(canonical_state: dict[str, Any]) -> dict[str, Any]:
    """Bounded projection per runtime contract."""

    gc = canonical_state.get("global_context")
    gmap: dict[str, Any] = {}
    if isinstance(gc, dict):
        if "map_name" in gc:
            gmap["map_name"] = gc.get("map_name")
        if "active_slice_ids" in gc:
            gmap["active_slice_ids"] = gc.get("active_slice_ids")

    players_out: list[dict[str, Any]] = []
    pl = canonical_state.get("players")
    if isinstance(pl, list):
        for p in pl:
            if not isinstance(p, dict):
                continue
            pi = p.get("player_index")
            if not isinstance(pi, int) or isinstance(pi, bool):
                continue
            row: dict[str, Any] = {
                "player_index": pi,
                "race_actual": p.get("race_actual"),
            }
            if "economy_summary" in p and isinstance(p.get("economy_summary"), dict):
                row["economy_summary"] = p["economy_summary"]
            am = p.get("army_summary")
            if isinstance(am, dict) and "army_unit_category_counts" in am:
                row["army_unit_category_counts"] = am.get("army_unit_category_counts")
            players_out.append(row)

    return {
        "frame_kind": canonical_state.get("frame_kind"),
        "gameloop": canonical_state.get("gameloop"),
        "global_context": gmap,
        "players": players_out,
    }


def observation_excerpt(observation: dict[str, Any]) -> dict[str, Any]:
    meta = observation.get("metadata")
    if not isinstance(meta, dict):
        meta = {}
    sf = observation.get("scalar_features")
    entries: list[Any] = []
    if isinstance(sf, dict):
        oe = sf.get("ordered_entries")
        if isinstance(oe, list):
            entries = oe[:OBSERVATION_SCALAR_ENTRIES_MAX]
    return {
        "metadata": meta,
        "scalar_features": {"ordered_entries": entries},
    }


def build_replay_explorer_artifacts(
    *,
    bundle_dir: Path,
    agent_path: Path,
    max_panels: int,
    slice_id_filter: str | None,
    non_claims: tuple[str, ...] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load bundle + agent, emit surface + report dicts."""

    nc = tuple(non_claims) if non_claims is not None else DEFAULT_NON_CLAIMS

    manifest = _load_json(bundle_dir / "replay_bundle_manifest.json")
    slices_json = _load_json(bundle_dir / "replay_slices.json")
    timeline = _load_json(bundle_dir / "replay_timeline.json")
    boe = _load_json(bundle_dir / "replay_build_order_economy.json")
    csv = _load_json(bundle_dir / "replay_combat_scouting_visibility.json")

    bundle_id = manifest.get("bundle_id")
    lineage_root = manifest.get("lineage_root")
    if not isinstance(bundle_id, str) or not isinstance(lineage_root, str):
        msg = "bundle manifest missing bundle_id or lineage_root"
        raise ValueError(msg)

    art_hashes = manifest.get("artifact_hashes")
    if not isinstance(art_hashes, dict):
        art_hashes = {}

    replay_sha = csv.get("replay_content_sha256")
    if not isinstance(replay_sha, str):
        replay_sha = manifest.get("source_replay_identity")
    if not isinstance(replay_sha, str):
        replay_sha = ""

    agent_body = _load_json(agent_path)
    predictor = FrozenHierarchicalImitationPredictor.from_agent_body(agent_body)

    selected = ordered_slices_for_explorer(
        slices_json,
        slice_id_filter=slice_id_filter,
        max_panels=max_panels,
    )

    panels: list[dict[str, Any]] = []
    delegate_counts: dict[str, int] = {}
    label_counts: dict[str, int] = {}
    missing_upstream = 0
    trace_validation_notes: list[str] = []

    for sl in selected:
        s_start = sl.get("start_gameloop")
        s_end = sl.get("end_gameloop")
        s_subj = sl.get("subject_player_index")
        sid = sl.get("slice_id")
        if (
            not isinstance(s_start, int)
            or isinstance(s_start, bool)
            or not isinstance(s_end, int)
            or isinstance(s_end, bool)
            or not isinstance(s_subj, int)
            or isinstance(s_subj, bool)
            or not isinstance(sid, str)
        ):
            missing_upstream += 1
            panels.append(
                {
                    "slice_id": sid if isinstance(sid, str) else "invalid_slice_record",
                    "anchor_gameloop": 0,
                    "slice_window": {"start_gameloop": 0, "end_gameloop": 0},
                    "timeline_excerpt": [],
                    "economy_excerpt": [],
                    "combat_scouting_excerpt": [],
                    "canonical_state_excerpt": {},
                    "observation_excerpt": {},
                    "hierarchical_trace_document": None,
                    "warnings": ["invalid_slice_record_fields"],
                    "source_hashes": {},
                },
            )
            continue

        anchor = slice_anchor_gameloop(s_start, s_end)

        obs_req = {
            "bundle_id": bundle_id,
            "lineage_root": lineage_root,
            "gameloop": anchor,
            "perspective_player_index": s_subj,
        }

        try:
            canonical_state, obs_frame, cs_report, mat_warnings = (
                materialize_observation_for_observation_request(
                    bundle_dir=bundle_dir,
                    observation_request=obs_req,
                )
            )
        except (OSError, ValueError, KeyError) as exc:
            missing_upstream += 1
            panels.append(
                {
                    "slice_id": sid,
                    "anchor_gameloop": anchor,
                    "slice_window": {"start_gameloop": s_start, "end_gameloop": s_end},
                    "timeline_excerpt": [],
                    "economy_excerpt": [],
                    "combat_scouting_excerpt": [],
                    "canonical_state_excerpt": {},
                    "observation_excerpt": {},
                    "hierarchical_trace_document": None,
                    "warnings": sorted([f"materialization_failed:{exc}"]),
                    "source_hashes": {},
                },
            )
            continue

        sig = build_context_signature(
            observation_frame=obs_frame,
            canonical_state=canonical_state,
            perspective_player_index=s_subj,
        )
        frame_ref = {
            "bundle_id": bundle_id,
            "lineage_root": lineage_root,
            "gameloop": anchor,
            "perspective_player_index": s_subj,
        }
        trace_doc = predictor.build_trace_document_for_signature(
            context_signature=sig,
            frame_ref=frame_ref,
        )
        val_errs = validate_hierarchical_trace_document(trace_doc)
        if val_errs:
            trace_validation_notes.append(f"slice:{sid}:{'|'.join(val_errs[:5])}")

        mgr = trace_doc.get("hierarchical_decision_trace", {})
        mgr_resp = mgr.get("manager_response", {}) if isinstance(mgr, dict) else {}
        wrk_resp = mgr.get("worker_response", {}) if isinstance(mgr, dict) else {}
        did = mgr_resp.get("selected_delegate_id") if isinstance(mgr_resp, dict) else None
        lab = wrk_resp.get("semantic_coarse_label") if isinstance(wrk_resp, dict) else None
        if isinstance(did, str):
            delegate_counts[did] = delegate_counts.get(did, 0) + 1
        if isinstance(lab, str):
            label_counts[lab] = label_counts.get(lab, 0) + 1

        tl_ex = timeline_excerpt_for_slice(
            timeline,
            start_gameloop=s_start,
            end_gameloop=s_end,
            anchor_gameloop=anchor,
        )
        ec_ex = economy_excerpt_for_slice(
            boe,
            start_gameloop=s_start,
            end_gameloop=s_end,
            anchor_gameloop=anchor,
        )
        cs_ex = combat_scouting_excerpt_for_slice(
            csv,
            slice_subject=s_subj,
            start_gameloop=s_start,
            end_gameloop=s_end,
            anchor_gameloop=anchor,
        )

        warn_set = {*mat_warnings}
        if val_errs:
            warn_set.add(f"m29_schema:{sid}")
        warnings = sorted(warn_set)

        panel_hashes = {
            k: v for k, v in art_hashes.items() if isinstance(k, str) and isinstance(v, str)
        }

        panels.append(
            {
                "slice_id": sid,
                "anchor_gameloop": anchor,
                "slice_window": {"start_gameloop": s_start, "end_gameloop": s_end},
                "timeline_excerpt": tl_ex,
                "economy_excerpt": ec_ex,
                "combat_scouting_excerpt": cs_ex,
                "canonical_state_excerpt": canonical_state_excerpt(canonical_state),
                "observation_excerpt": observation_excerpt(obs_frame),
                "hierarchical_trace_document": trace_doc,
                "warnings": warnings,
                "canonical_state_report_sha256": sha256_hex_of_canonical_json(cs_report),
                "source_hashes": panel_hashes,
            },
        )

    surface: dict[str, Any] = {
        "surface_version": SURFACE_VERSION,
        "selection_policy_id": SELECTION_POLICY_ID,
        "non_claims": list(nc),
        "source_bundle": {
            "bundle_id": bundle_id,
            "lineage_root": lineage_root,
            "replay_content_sha256": replay_sha,
            "artifact_hashes": {
                k: v for k, v in art_hashes.items() if isinstance(k, str) and isinstance(v, str)
            },
        },
        "agent": {
            "agent_version": AGENT_VERSION,
            "delegate_policy_id": DELEGATE_POLICY_ID,
            "trace_schema_version": INTERFACE_TRACE_SCHEMA_VERSION,
            "agent_artifact_filename": agent_path.name,
        },
        "panels": panels,
    }

    report: dict[str, Any] = {
        "report_version": REPORT_VERSION,
        "selection_policy_id": SELECTION_POLICY_ID,
        "surface_version": SURFACE_VERSION,
        "panel_count": len(panels),
        "slice_count": len(selected),
        "delegate_frequency": dict(sorted(delegate_counts.items())),
        "worker_label_frequency": dict(sorted(label_counts.items())),
        "missing_or_unavailable_upstream_count": missing_upstream,
        "bounded_excerpt_policy": {
            "timeline_max": TIMELINE_EXCERPT_MAX,
            "economy_max": ECONOMY_EXCERPT_MAX,
            "combat_scouting_max": COMBAT_SCOUTING_EXCERPT_MAX,
            "observation_scalar_entries_max": OBSERVATION_SCALAR_ENTRIES_MAX,
            "max_panels_default": max_panels,
        },
        "governed_asset_classes": [
            "m14_bundle_json",
            "m10_timeline",
            "m11_build_order_economy",
            "m12_combat_scouting_visibility",
            "m13_slices",
            "m16_canonical_state",
            "m18_observation_surface",
            "m30_replay_hierarchical_imitation_agent",
            "m29_hierarchical_trace_schema",
        ],
        "non_claims": list(nc),
        "trace_validation_notes": trace_validation_notes,
    }

    return surface, report
