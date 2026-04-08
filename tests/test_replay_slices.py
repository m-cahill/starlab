"""M13 replay slice generation tests (fixture JSON; no s2protocol, no raw parse)."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from starlab.replays.replay_slice_generation import (
    generate_replay_slices_envelope,
    slice_identity_payload_for_hash,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m13"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_golden_replay_slices_deterministic() -> None:
    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe)
    sha_csv = sha256_hex_of_canonical_json(csv)
    status, body, report = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert status == "completed"
    exp_b = json.loads((FIX / "expected_replay_slices.json").read_text(encoding="utf-8"))
    exp_r = json.loads((FIX / "expected_replay_slices_report.json").read_text(encoding="utf-8"))
    assert json.loads(canonical_json_dumps(body)) == exp_b
    assert json.loads(canonical_json_dumps(report)) == exp_r


def test_empty_upstream_candidates() -> None:
    """Valid empty slice artifact when M12 surfaces are empty."""

    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    boe_e = deepcopy(boe)
    csv_e = deepcopy(csv)
    boe_e["build_order_steps"] = []
    csv_e["combat_windows"] = []
    csv_e["scouting_observations"] = []
    csv_e["visibility_windows"] = []
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe_e)
    sha_csv = sha256_hex_of_canonical_json(csv_e)
    boe_e["source_timeline_sha256"] = sha_t
    csv_e["source_timeline_sha256"] = sha_t
    csv_e["source_build_order_economy_sha256"] = sha_boe
    status, body, _report = generate_replay_slices_envelope(
        build_order_economy=boe_e,
        build_order_economy_report=None,
        combat_scouting_visibility=csv_e,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert status == "completed"
    assert body["slices"] == []


def test_lineage_mismatch_fails() -> None:
    """Caller-supplied canonical hash must match upstream embedded refs (M11/M12)."""

    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe)
    sha_csv = sha256_hex_of_canonical_json(csv)
    status, body, report = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256="0" * 64,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert status == "lineage_failed"
    assert body["slices"] == []
    assert "lineage_hash_mismatch" in report.get("reason_codes", [])
    assert sha_boe != "0" * 64


def test_combat_slice_clipping_counts() -> None:
    """Fixture: one end clip (window 2) and one start clip (first scouting anchor 100)."""

    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe)
    sha_csv = sha256_hex_of_canonical_json(csv)
    _s, _b, report = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert report["clipped_to_start_count"] == 1
    assert report["clipped_to_end_count"] == 1


def test_combat_anchor_is_window_start() -> None:
    csv = _load("replay_combat_scouting_visibility.json")
    wins = csv["combat_windows"]
    assert wins[0]["start_gameloop"] == 700
    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe)
    sha_csv = sha256_hex_of_canonical_json(csv)
    _s, body, _r = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    cw_slice = next(s for s in body["slices"] if s["slice_kind"] == "combat_window")
    assert cw_slice["anchor_gameloop"] == 700


def test_stable_slice_id_idempotent() -> None:
    timeline = _load("replay_timeline.json")
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    sha_t = sha256_hex_of_canonical_json(timeline)
    sha_boe = sha256_hex_of_canonical_json(boe)
    sha_csv = sha256_hex_of_canonical_json(csv)
    _, a1, _ = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    _, a2, _ = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha_boe,
        source_combat_scouting_visibility_sha256=sha_csv,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert [s["slice_id"] for s in a1["slices"]] == [s["slice_id"] for s in a2["slices"]]


def test_slice_id_excludes_overlap_derived_fields() -> None:
    """Identity payload for hashing must not include overlap lists."""

    pl = slice_identity_payload_for_hash(
        anchor_gameloop=1,
        anchor_ref={"combat_window_id": "combat_window:0"},
        end_gameloop=10,
        evidence_model=None,
        opponent_player_index=None,
        slice_kind="combat_window",
        start_gameloop=0,
        subject_player_index=1,
    )
    dumped = json.dumps(pl, sort_keys=True)
    assert "overlap" not in dumped
    assert "visibility" not in dumped
    _ = sha256_hex_of_canonical_json(pl)


def test_source_contract_failed_bad_timeline() -> None:
    bad_tl: dict[str, Any] = {"entries": [], "schema_version": "wrong"}
    boe = _load("replay_build_order_economy.json")
    csv = _load("replay_combat_scouting_visibility.json")
    status, _, report = generate_replay_slices_envelope(
        build_order_economy=boe,
        build_order_economy_report=None,
        combat_scouting_visibility=csv,
        combat_scouting_visibility_report=None,
        metadata=None,
        metadata_report=None,
        source_build_order_economy_sha256=sha256_hex_of_canonical_json(boe),
        source_combat_scouting_visibility_sha256=sha256_hex_of_canonical_json(csv),
        source_timeline_sha256=sha256_hex_of_canonical_json(bad_tl),
        timeline=bad_tl,
        timeline_report=None,
    )
    assert status == "source_contract_failed"
    assert "source_contract_failed" in report.get("reason_codes", [])
