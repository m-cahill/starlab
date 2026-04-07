"""M12 combat / scouting / visibility extraction tests (fixture JSON; no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.build_order_economy_io import run_build_order_economy_extraction
from starlab.replays.combat_scouting_visibility_extraction import (
    validate_build_order_economy_contract,
)
from starlab.replays.combat_scouting_visibility_io import run_combat_scouting_visibility_extraction
from starlab.replays.timeline_io import run_timeline_extraction
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m12"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_golden_combined_deterministic() -> None:
    raw = _load("replay_raw_parse_m12_combined.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    sha_boe = sha256_hex_of_canonical_json(boe)
    status, body, report = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert status == "completed"
    exp_b = json.loads(
        (FIX / "expected_replay_combat_scouting_visibility_combined.json").read_text(
            encoding="utf-8"
        )
    )
    exp_r = json.loads(
        (FIX / "expected_replay_combat_scouting_visibility_report_combined.json").read_text(
            encoding="utf-8",
        )
    )
    assert json.loads(canonical_json_dumps(body)) == exp_b
    assert json.loads(canonical_json_dumps(report)) == exp_r


def test_combat_window_clustering_gap() -> None:
    """Gaps <= COMBAT_WINDOW_GAP_LOOPS (160) stay in one window; larger gaps split."""

    raw = _load("replay_raw_parse_m12_combined.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    sha_boe = sha256_hex_of_canonical_json(boe)
    _, body, _ = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    wins = body["combat_windows"]
    assert len(wins) == 3
    assert wins[0]["start_gameloop"] == 700 and wins[0]["end_gameloop"] == 720
    assert wins[1]["start_gameloop"] == 1000
    assert wins[2]["start_gameloop"] == 1200


def test_visibility_observation_proxy_label() -> None:
    raw = _load("replay_raw_parse_m12_combined.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    sha_boe = sha256_hex_of_canonical_json(boe)
    _, body, _ = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    for w in body["visibility_windows"]:
        assert w["visibility_model"] == "observation_proxy"


def test_scouting_first_seen_no_duplicate_army_line() -> None:
    """First army-line signal (Reaper) suppresses later Marine for same subject."""

    raw = _load("replay_raw_parse_m12_combined.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    sha_boe = sha256_hex_of_canonical_json(boe)
    _, body, _ = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    army_sigs = [
        o for o in body["scouting_observations"] if o["signal_kind"] == "enemy_army_first_seen"
    ]
    p1_army = [o for o in army_sigs if o["subject_player_index"] == 1]
    assert len(p1_army) == 1
    assert p1_army[0]["entity_name"] == "Reaper"


def test_timeline_boe_hash_mismatch_fails() -> None:
    raw = _load("replay_raw_parse_m12_combined.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    boe["source_timeline_sha256"] = "0" * 64
    sha_boe = sha256_hex_of_canonical_json(boe)
    status, _, rep = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert status == "source_contract_failed"
    assert rep["extraction_status"] == "failed"


def test_unknown_build_order_economy_contract() -> None:
    boe = {"schema_version": "wrong", "build_order_economy_contract_version": "x"}
    ok, _ = validate_build_order_economy_contract(boe)
    assert not ok


def test_visibility_partial_without_unit_tags() -> None:
    """No unit_tag on entries → empty visibility_windows and partial extraction."""

    raw = _load("replay_raw_parse_m12_combined.json")
    sha_raw = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha_raw,
    )
    # Strip all unit_tag keys (changes timeline hash; BOE must be recomputed for consistency).
    for e in timeline["entries"]:
        if isinstance(e, dict) and "unit_tag" in e:
            del e["unit_tag"]
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, boe, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha_raw,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    sha_boe = sha256_hex_of_canonical_json(boe)
    _, body, rep = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=None,
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_build_order_economy_sha256=sha_boe,
        source_raw_parse_sha256=sha_raw,
        source_timeline_sha256=sha_t,
        timeline=timeline,
        timeline_report=None,
    )
    assert body["visibility_windows"] == []
    assert rep["extraction_status"] == "partial"
    assert rep["warnings"]
