"""``generate_replay_slices_envelope`` implementation (M13 / M35 split)."""

from __future__ import annotations

from typing import Any

from starlab.replays.combat_scouting_visibility_extraction import (
    validate_build_order_economy_contract,
    validate_timeline_contract,
)
from starlab.replays.replay_slice_catalog import (
    TAG_COMBAT,
    TAG_EXPLICIT_VISIBILITY_OVERLAP,
    TAG_PROXY_VISIBILITY_OVERLAP,
    TAG_SCOUTING,
)
from starlab.replays.replay_slice_generation_helpers import (
    RunStatus,
    combat_window_id,
    hex_eq,
    max_gameloop_from_timeline,
    metadata_max_loops_optional,
    overlap_build_steps,
    overlap_visibility_windows,
    primary_anchor_id,
    scouting_observation_id,
    slice_identity_payload_for_hash,
    validate_csv_contract,
)
from starlab.replays.replay_slice_models import (
    REPLAY_SLICES_CONTRACT_VERSION,
    REPLAY_SLICES_PROFILE,
    REPLAY_SLICES_REPORT_SCHEMA_VERSION,
    REPLAY_SLICES_SCHEMA_VERSION,
    SLICE_KIND_COMBAT,
    SLICE_KIND_SCOUTING,
    SLICE_PADDING_POST_LOOPS,
    SLICE_PADDING_PRE_LOOPS,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def generate_replay_slices_envelope(
    *,
    timeline: dict[str, Any],
    source_timeline_sha256: str,
    build_order_economy: dict[str, Any],
    source_build_order_economy_sha256: str,
    combat_scouting_visibility: dict[str, Any],
    source_combat_scouting_visibility_sha256: str,
    timeline_report: dict[str, Any] | None,
    build_order_economy_report: dict[str, Any] | None,
    combat_scouting_visibility_report: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    """Return ``(run_status, artifact, report)``."""

    ok_tl, err_tl = validate_timeline_contract(timeline)
    ok_boe, err_boe = validate_build_order_economy_contract(build_order_economy)
    ok_csv, err_csv = validate_csv_contract(combat_scouting_visibility)

    if not ok_tl or not ok_boe or not ok_csv:
        detail = err_tl or err_boe or err_csv
        empty_art: dict[str, Any] = {
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "generation_parameters": {
                "replay_slice_catalog": "starlab.replay_slice_catalog.m13.v1",
                "slice_padding_post_loops": SLICE_PADDING_POST_LOOPS,
                "slice_padding_pre_loops": SLICE_PADDING_PRE_LOOPS,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "schema_version": REPLAY_SLICES_SCHEMA_VERSION,
            "slices": [],
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        rep_fail: dict[str, Any] = {
            "clipped_to_end_count": 0,
            "clipped_to_start_count": 0,
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "duration_summary_by_kind": {},
            "generation_parameters": empty_art["generation_parameters"],
            "lineage_error": detail,
            "omitted_candidates_by_reason": {},
            "overlap_summary": {
                "visibility_overlap_total": 0,
                "build_order_overlap_total": 0,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "reason_codes": ["source_contract_failed"],
            "schema_version": REPLAY_SLICES_REPORT_SCHEMA_VERSION,
            "slice_counts_by_kind": {},
            "slice_counts_by_player": {},
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        return "source_contract_failed", empty_art, rep_fail

    boe_tl = build_order_economy.get("source_timeline_sha256")
    hash_tl_boe = isinstance(boe_tl, str) and hex_eq(boe_tl, source_timeline_sha256)

    csv_tl = combat_scouting_visibility.get("source_timeline_sha256")
    csv_boe = combat_scouting_visibility.get("source_build_order_economy_sha256")
    hash_tl_csv = isinstance(csv_tl, str) and hex_eq(csv_tl, source_timeline_sha256)
    hash_boe_csv = isinstance(csv_boe, str) and hex_eq(csv_boe, source_build_order_economy_sha256)

    lineage_ok = hash_tl_boe and hash_tl_csv and hash_boe_csv
    lineage_detail: str | None = None
    if not hash_tl_boe:
        lineage_detail = (
            "build_order_economy.source_timeline_sha256 mismatch vs canonical timeline hash"
        )
    elif not hash_tl_csv:
        lineage_detail = (
            "combat_scouting_visibility.source_timeline_sha256 mismatch vs canonical timeline hash"
        )
    elif not hash_boe_csv:
        lineage_detail = (
            "combat_scouting_visibility.source_build_order_economy_sha256 mismatch vs "
            "canonical boe hash"
        )

    if not lineage_ok:
        empty_l: dict[str, Any] = {
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "generation_parameters": {
                "replay_slice_catalog": "starlab.replay_slice_catalog.m13.v1",
                "slice_padding_post_loops": SLICE_PADDING_POST_LOOPS,
                "slice_padding_pre_loops": SLICE_PADDING_PRE_LOOPS,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "schema_version": REPLAY_SLICES_SCHEMA_VERSION,
            "slices": [],
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        rep_l: dict[str, Any] = {
            "clipped_to_end_count": 0,
            "clipped_to_start_count": 0,
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "duration_summary_by_kind": {},
            "generation_parameters": empty_l["generation_parameters"],
            "lineage_error": lineage_detail,
            "omitted_candidates_by_reason": {},
            "overlap_summary": {
                "visibility_overlap_total": 0,
                "build_order_overlap_total": 0,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "reason_codes": ["lineage_hash_mismatch"],
            "schema_version": REPLAY_SLICES_REPORT_SCHEMA_VERSION,
            "slice_counts_by_kind": {},
            "slice_counts_by_player": {},
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        return "lineage_failed", empty_l, rep_l

    replay_max = max_gameloop_from_timeline(timeline)
    meta_max = metadata_max_loops_optional(metadata)
    if meta_max is not None and replay_max > meta_max:
        empty_m: dict[str, Any] = {
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "generation_parameters": {
                "replay_slice_catalog": "starlab.replay_slice_catalog.m13.v1",
                "slice_padding_post_loops": SLICE_PADDING_POST_LOOPS,
                "slice_padding_pre_loops": SLICE_PADDING_PRE_LOOPS,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "schema_version": REPLAY_SLICES_SCHEMA_VERSION,
            "slices": [],
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        rep_m: dict[str, Any] = {
            "clipped_to_end_count": 0,
            "clipped_to_start_count": 0,
            "contract": REPLAY_SLICES_CONTRACT_VERSION,
            "duration_summary_by_kind": {},
            "generation_parameters": empty_m["generation_parameters"],
            "lineage_error": (
                f"timeline max gameloop {replay_max} exceeds optional metadata "
                f"game_length_loops {meta_max}"
            ),
            "omitted_candidates_by_reason": {},
            "overlap_summary": {
                "visibility_overlap_total": 0,
                "build_order_overlap_total": 0,
            },
            "profile": REPLAY_SLICES_PROFILE,
            "reason_codes": ["metadata_timeline_bounds_mismatch"],
            "schema_version": REPLAY_SLICES_REPORT_SCHEMA_VERSION,
            "slice_counts_by_kind": {},
            "slice_counts_by_player": {},
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
            "source_timeline_sha256": source_timeline_sha256,
        }
        return "lineage_failed", empty_m, rep_m

    steps_raw = build_order_economy.get("build_order_steps")
    steps: list[dict[str, Any]] = steps_raw if isinstance(steps_raw, list) else []

    combat_windows = combat_scouting_visibility.get("combat_windows")
    scouting_observations = combat_scouting_visibility.get("scouting_observations")
    visibility_windows = combat_scouting_visibility.get("visibility_windows")
    assert isinstance(combat_windows, list)
    assert isinstance(scouting_observations, list)
    assert isinstance(visibility_windows, list)

    clipped_start = 0
    clipped_end = 0
    raw_slices: list[dict[str, Any]] = []

    for cw in combat_windows:
        if not isinstance(cw, dict):
            continue
        wi = cw.get("window_index")
        sg = cw.get("start_gameloop")
        eg = cw.get("end_gameloop")
        if (
            not isinstance(wi, int)
            or isinstance(wi, bool)
            or not isinstance(sg, int)
            or isinstance(sg, bool)
            or not isinstance(eg, int)
            or isinstance(eg, bool)
        ):
            continue
        raw_start = sg - SLICE_PADDING_PRE_LOOPS
        raw_end = eg + SLICE_PADDING_POST_LOOPS
        if raw_start < 0:
            clipped_start += 1
        if raw_end > replay_max:
            clipped_end += 1
        start_gameloop = max(0, raw_start)
        end_gameloop = min(replay_max, raw_end)
        anchor_gameloop = sg
        anchor_ref = {"combat_window_id": combat_window_id(wi)}

        players_involved = cw.get("players_involved")
        subj: int | None = None
        opp: int | None = None
        if isinstance(players_involved, list) and players_involved:
            p0 = players_involved[0]
            if isinstance(p0, int) and not isinstance(p0, bool):
                subj = p0
            if len(players_involved) > 1:
                p1 = players_involved[1]
                if isinstance(p1, int) and not isinstance(p1, bool):
                    opp = p1

        id_body = slice_identity_payload_for_hash(
            anchor_gameloop=anchor_gameloop,
            anchor_ref=anchor_ref,
            end_gameloop=end_gameloop,
            evidence_model=None,
            opponent_player_index=opp,
            slice_kind=SLICE_KIND_COMBAT,
            start_gameloop=start_gameloop,
            subject_player_index=subj,
        )
        slice_id = sha256_hex_of_canonical_json(id_body)

        vis_ids, has_proxy, has_expl = overlap_visibility_windows(
            end_gameloop=end_gameloop,
            start_gameloop=start_gameloop,
            visibility_windows=visibility_windows,
        )
        bo_ids = overlap_build_steps(
            end_gameloop=end_gameloop,
            start_gameloop=start_gameloop,
            steps=steps,
        )

        tags: list[str] = [TAG_COMBAT]
        if has_proxy:
            tags.append(TAG_PROXY_VISIBILITY_OVERLAP)
        if has_expl:
            tags.append(TAG_EXPLICIT_VISIBILITY_OVERLAP)
        tags_sorted = sorted(set(tags))

        duration_loops = end_gameloop - start_gameloop + 1

        raw_slices.append(
            {
                "_sort_anchor": primary_anchor_id(
                    observation_index=None,
                    slice_kind=SLICE_KIND_COMBAT,
                    window_index=wi,
                ),
                "anchor_gameloop": anchor_gameloop,
                "anchor_ref": anchor_ref,
                "duration_loops": duration_loops,
                "end_gameloop": end_gameloop,
                "opponent_player_index": opp,
                "overlapping_build_order_step_ids": bo_ids,
                "overlapping_visibility_window_ids": vis_ids,
                "slice_id": slice_id,
                "slice_kind": SLICE_KIND_COMBAT,
                "start_gameloop": start_gameloop,
                "subject_player_index": subj,
                "tags": tags_sorted,
            },
        )

    for so in scouting_observations:
        if not isinstance(so, dict):
            continue
        oi = so.get("observation_index")
        ag = so.get("gameloop")
        if (
            not isinstance(oi, int)
            or isinstance(oi, bool)
            or not isinstance(ag, int)
            or isinstance(ag, bool)
        ):
            continue
        raw_start = ag - SLICE_PADDING_PRE_LOOPS
        raw_end = ag + SLICE_PADDING_POST_LOOPS
        if raw_start < 0:
            clipped_start += 1
        if raw_end > replay_max:
            clipped_end += 1
        start_gameloop = max(0, raw_start)
        end_gameloop = min(replay_max, raw_end)
        anchor_gameloop = ag
        anchor_ref = {"scouting_observation_id": scouting_observation_id(oi)}

        sp = so.get("subject_player_index")
        subj_scout: int | None = sp if isinstance(sp, int) and not isinstance(sp, bool) else None

        ev = so.get("evidence_model")
        ev_s: str | None = ev if isinstance(ev, str) else None

        id_body_s = slice_identity_payload_for_hash(
            anchor_gameloop=anchor_gameloop,
            anchor_ref=anchor_ref,
            end_gameloop=end_gameloop,
            evidence_model=ev_s,
            opponent_player_index=None,
            slice_kind=SLICE_KIND_SCOUTING,
            start_gameloop=start_gameloop,
            subject_player_index=subj_scout,
        )
        slice_id_s = sha256_hex_of_canonical_json(id_body_s)

        vis_ids_s, has_proxy_s, has_expl_s = overlap_visibility_windows(
            end_gameloop=end_gameloop,
            start_gameloop=start_gameloop,
            visibility_windows=visibility_windows,
        )
        bo_ids_s = overlap_build_steps(
            end_gameloop=end_gameloop,
            start_gameloop=start_gameloop,
            steps=steps,
        )

        tags_s: list[str] = [TAG_SCOUTING]
        if has_proxy_s:
            tags_s.append(TAG_PROXY_VISIBILITY_OVERLAP)
        if has_expl_s:
            tags_s.append(TAG_EXPLICIT_VISIBILITY_OVERLAP)
        tags_sorted_s = sorted(set(tags_s))

        duration_loops_s = end_gameloop - start_gameloop + 1

        raw_slices.append(
            {
                "_sort_anchor": primary_anchor_id(
                    observation_index=oi,
                    slice_kind=SLICE_KIND_SCOUTING,
                    window_index=None,
                ),
                "anchor_gameloop": anchor_gameloop,
                "anchor_ref": anchor_ref,
                "duration_loops": duration_loops_s,
                "end_gameloop": end_gameloop,
                "opponent_player_index": None,
                "overlapping_build_order_step_ids": bo_ids_s,
                "overlapping_visibility_window_ids": vis_ids_s,
                "slice_id": slice_id_s,
                "slice_kind": SLICE_KIND_SCOUTING,
                "start_gameloop": start_gameloop,
                "subject_player_index": subj_scout,
                "tags": tags_sorted_s,
            },
        )

    def _sort_key(row: dict[str, Any]) -> tuple[int, int, str, str]:
        return (
            int(row["start_gameloop"]),
            int(row["end_gameloop"]),
            str(row["slice_kind"]),
            str(row["_sort_anchor"]),
        )

    slices_sorted = sorted(raw_slices, key=_sort_key)
    for row in slices_sorted:
        row.pop("_sort_anchor", None)

    gen_params = {
        "replay_max_gameloop": replay_max,
        "replay_slice_catalog": "starlab.replay_slice_catalog.m13.v1",
        "slice_padding_post_loops": SLICE_PADDING_POST_LOOPS,
        "slice_padding_pre_loops": SLICE_PADDING_PRE_LOOPS,
    }

    artifact: dict[str, Any] = {
        "contract": REPLAY_SLICES_CONTRACT_VERSION,
        "generation_parameters": gen_params,
        "profile": REPLAY_SLICES_PROFILE,
        "schema_version": REPLAY_SLICES_SCHEMA_VERSION,
        "slices": slices_sorted,
        "source_build_order_economy_sha256": source_build_order_economy_sha256,
        "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
        "source_timeline_sha256": source_timeline_sha256,
    }

    counts_kind: dict[str, int] = {}
    for s in slices_sorted:
        k = str(s["slice_kind"])
        counts_kind[k] = counts_kind.get(k, 0) + 1

    counts_player: dict[str, dict[str, int]] = {}
    for s in slices_sorted:
        kind = str(s["slice_kind"])
        for pk, pl in (
            (s.get("subject_player_index"), "subject"),
            (s.get("opponent_player_index"), "opponent"),
        ):
            if isinstance(pk, int) and not isinstance(pk, bool):
                key = str(pk)
                counts_player.setdefault(key, {})
                counts_player[key][kind] = counts_player[key].get(kind, 0) + 1
    counts_player_out = {k: dict(sorted(v.items())) for k, v in sorted(counts_player.items())}

    dur_by_kind: dict[str, dict[str, int]] = {}
    for s in slices_sorted:
        k = str(s["slice_kind"])
        d = int(s["duration_loops"])
        bucket = dur_by_kind.setdefault(k, {"max": d, "min": d, "sum": 0, "count": 0})
        bucket["min"] = min(bucket["min"], d)
        bucket["max"] = max(bucket["max"], d)
        bucket["sum"] = bucket["sum"] + d
        bucket["count"] = bucket["count"] + 1
    duration_summary: dict[str, Any] = {}
    for k, b in sorted(dur_by_kind.items()):
        c = b["count"]
        mean_int = b["sum"] // c if c else 0
        duration_summary[k] = {
            "count": c,
            "max": b["max"],
            "mean_loops": mean_int,
            "min": b["min"],
            "sum_loops": b["sum"],
        }

    bo_total = sum(len(s.get("overlapping_build_order_step_ids", [])) for s in slices_sorted)
    vis_total = sum(len(s.get("overlapping_visibility_window_ids", [])) for s in slices_sorted)

    report: dict[str, Any] = {
        "clipped_to_end_count": clipped_end,
        "clipped_to_start_count": clipped_start,
        "contract": REPLAY_SLICES_CONTRACT_VERSION,
        "duration_summary_by_kind": duration_summary,
        "generation_parameters": gen_params,
        "omitted_candidates_by_reason": {},
        "overlap_summary": {
            "build_order_overlap_total": bo_total,
            "visibility_overlap_total": vis_total,
        },
        "profile": REPLAY_SLICES_PROFILE,
        "schema_version": REPLAY_SLICES_REPORT_SCHEMA_VERSION,
        "slice_counts_by_kind": dict(sorted(counts_kind.items())),
        "slice_counts_by_player": counts_player_out,
        "source_build_order_economy_sha256": source_build_order_economy_sha256,
        "source_combat_scouting_visibility_sha256": source_combat_scouting_visibility_sha256,
        "source_timeline_sha256": source_timeline_sha256,
    }

    # Optional lineage enrichment hashes (non-authoritative for slice_id)
    tr_sha = sha256_hex_of_canonical_json(timeline_report) if timeline_report is not None else None
    boe_rep_sha = (
        sha256_hex_of_canonical_json(build_order_economy_report)
        if build_order_economy_report is not None
        else None
    )
    csv_rep_sha = (
        sha256_hex_of_canonical_json(combat_scouting_visibility_report)
        if combat_scouting_visibility_report is not None
        else None
    )
    meta_sha = sha256_hex_of_canonical_json(metadata) if metadata is not None else None
    meta_rep_sha = (
        sha256_hex_of_canonical_json(metadata_report) if metadata_report is not None else None
    )

    if tr_sha is not None:
        report["optional_source_timeline_report_sha256"] = tr_sha
        artifact["optional_source_timeline_report_sha256"] = tr_sha
    if boe_rep_sha is not None:
        report["optional_source_build_order_economy_report_sha256"] = boe_rep_sha
        artifact["optional_source_build_order_economy_report_sha256"] = boe_rep_sha
    if csv_rep_sha is not None:
        report["optional_source_combat_scouting_visibility_report_sha256"] = csv_rep_sha
        artifact["optional_source_combat_scouting_visibility_report_sha256"] = csv_rep_sha
    if meta_sha is not None:
        report["optional_source_metadata_sha256"] = meta_sha
        artifact["optional_source_metadata_sha256"] = meta_sha
    if meta_rep_sha is not None:
        report["optional_source_metadata_report_sha256"] = meta_rep_sha
        artifact["optional_source_metadata_report_sha256"] = meta_rep_sha

    return "completed", artifact, report
