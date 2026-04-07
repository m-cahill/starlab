"""M10 replay timeline extraction tests (fixture JSON; no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from starlab.replays.metadata_extraction import RAW_PARSE_SCHEMA_ACCEPTED
from starlab.replays.timeline_extraction import (
    EVENT_NAME_TO_SEMANTIC,
    build_public_payload,
    extract_timeline_envelope,
)
from starlab.replays.timeline_io import run_timeline_extraction
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m10"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_schema_acceptance_matches_m09_plus_v2() -> None:
    assert "starlab.replay_raw_parse.v1" in RAW_PARSE_SCHEMA_ACCEPTED
    assert "starlab.replay_raw_parse.v2" in RAW_PARSE_SCHEMA_ACCEPTED


def test_event_name_mapping_covers_m10_set() -> None:
    for k in EVENT_NAME_TO_SEMANTIC:
        assert k.startswith("NNet.")


def test_golden_timeline_deterministic() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    sha = sha256_hex_of_canonical_json(raw)
    status, timeline, report = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "completed"
    exp_t = json.loads((FIX / "expected_replay_timeline.json").read_text(encoding="utf-8"))
    exp_r = json.loads((FIX / "expected_replay_timeline_report.json").read_text(encoding="utf-8"))
    assert json.loads(canonical_json_dumps(timeline)) == exp_t
    assert json.loads(canonical_json_dumps(report)) == exp_r


def test_merge_order_game_before_tracker_same_gameloop() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    entries = timeline["entries"]
    assert entries[0]["source_stream"] == "game"
    assert entries[1]["source_stream"] == "tracker"


def test_v1_no_streams_partial_empty_entries() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    raw["schema_version"] = "starlab.replay_raw_parse.v1"
    del raw["raw_event_streams"]
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, report = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert timeline["entries"] == []
    assert report["extraction_status"] in ("partial", "ok")


def test_unsupported_event_reported_not_in_entries() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    raw["raw_event_streams"]["game_events"] = [
        {"_event": "NNet.Game.SUnknownFooEvent", "_gameloop": 1, "_eventid": 0},
    ]
    raw["raw_event_streams"]["tracker_events"] = None
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, report = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert timeline["entries"] == []
    assert "NNet.Game.SUnknownFooEvent" in report["unsupported_event_names"]


def test_privacy_no_chat_body_or_display_names() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    raw["raw_event_streams"]["message_events"] = [
        {
            "_event": "NNet.Game.SChatMessage",
            "_gameloop": 2,
            "_eventid": 0,
            "_userid": {"m_userId": 0},
            "m_name": "SecretName",
            "m_string": "secret body",
        },
    ]
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    dumped = canonical_json_dumps(timeline)
    assert "SecretName" not in dumped
    assert "secret body" not in dumped
    assert "m_string_length" in dumped


def test_public_payload_strips_strings_for_message_event() -> None:
    ev = {
        "_event": "NNet.Game.SChatMessage",
        "_gameloop": 1,
        "m_string": "hello",
    }
    p = build_public_payload(semantic_kind="message_event", event=ev)
    assert "hello" not in json.dumps(p)
    assert p.get("m_string_length") == 5


@pytest.mark.parametrize("fname", ["replay_raw_parse_timeline_happy.json"])
def test_m10_fixture_raw_parse_schema(fname: str) -> None:
    raw = _load(fname)
    assert raw["schema_version"] in RAW_PARSE_SCHEMA_ACCEPTED


def test_extract_timeline_envelope_direct() -> None:
    raw = _load("replay_raw_parse_timeline_happy.json")
    sha = sha256_hex_of_canonical_json(raw)
    tl, rep = extract_timeline_envelope(
        raw_parse=raw,
        source_metadata_report_sha256=None,
        source_metadata_sha256=None,
        source_parse_receipt_sha256=None,
        source_parse_report_sha256=None,
        source_raw_parse_sha256=sha,
    )
    assert tl["source_raw_parse_sha256"] == sha
    assert rep["extraction_status"] == "ok"
