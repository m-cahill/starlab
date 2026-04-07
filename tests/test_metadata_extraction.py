"""M09 metadata extraction unit tests (fixture raw parse JSON; no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from starlab.replays.metadata_extraction import (
    RAW_PARSE_SCHEMA_ACCEPTED,
    RAW_PARSE_SCHEMA_EXPECTED,
    build_metadata_envelope,
    build_normalized_metadata,
    map_player_kind,
    map_race_actual,
    map_race_requested,
    map_result,
    source_sections_present,
)
from starlab.replays.metadata_io import extract_from_paths, run_metadata_extraction
from starlab.runs.json_util import sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m09"
RAW_VALID = FIX / "replay_raw_parse_valid.json"
RAW_PARTIAL = FIX / "replay_raw_parse_partial.json"
RCP_VALID = FIX / "replay_parse_receipt_valid.json"
RPT_VALID = FIX / "replay_parse_report_valid.json"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_source_sections_present_sorted() -> None:
    raw = _load("replay_raw_parse_valid.json")
    rs = raw["raw_sections"]
    # ``attribute_events`` is null in fixture → omitted from present list
    assert source_sections_present(rs) == ["details", "header", "init_data"]


def test_map_player_kind_int() -> None:
    assert map_player_kind(1) == "human"
    assert map_player_kind(2) == "computer"
    assert map_player_kind(3) == "observer"
    assert map_player_kind(99) == "unknown"


def test_map_race_and_result() -> None:
    assert map_race_requested("Terran") == "terran"
    assert map_race_actual("Terran") == "terran"
    assert map_race_requested("Random") == "random"
    assert map_race_actual("Random") == "unknown"
    assert map_result(1) == "win"
    assert map_result(2) == "loss"


def test_build_normalized_metadata_deterministic() -> None:
    raw = _load("replay_raw_parse_valid.json")
    a, am = build_normalized_metadata(raw)
    b, bm = build_normalized_metadata(raw)
    assert a == b
    assert am is False


def test_player_ordering_by_index() -> None:
    raw = _load("replay_raw_parse_valid.json")
    meta, _ = build_normalized_metadata(raw)
    idx = [p["player_index"] for p in meta["players"]]
    assert idx == sorted(idx)


def test_receipt_linkage_success() -> None:
    raw = _load("replay_raw_parse_valid.json")
    sha = sha256_hex_of_canonical_json(raw)
    receipt = _load("replay_parse_receipt_valid.json")
    report = _load("replay_parse_report_valid.json")
    status, meta, rep = run_metadata_extraction(
        parse_receipt=receipt,
        parse_report=report,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "extracted"
    assert rep["extraction_status"] == "extracted"
    assert meta["metadata"]["map"]["map_name"] == "Test Map"
    assert len(meta["metadata"]["players"]) == 2


def test_receipt_mismatch_source_contract_failed() -> None:
    raw = _load("replay_raw_parse_valid.json")
    sha = sha256_hex_of_canonical_json(raw)
    receipt = _load("replay_parse_receipt_valid.json")
    receipt = dict(receipt)
    receipt["raw_parse_sha256"] = "0" * 64
    status, meta, rep = run_metadata_extraction(
        parse_receipt=receipt,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "source_contract_failed"
    assert rep["extraction_status"] == "source_contract_failed"


def test_parse_report_not_parsed_failed() -> None:
    raw = _load("replay_raw_parse_valid.json")
    sha = sha256_hex_of_canonical_json(raw)
    report = _load("replay_parse_report_valid.json")
    report = dict(report)
    report["parse_status"] = "parse_failed"
    status, _, rep = run_metadata_extraction(
        parse_receipt=None,
        parse_report=report,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "source_contract_failed"


def test_partial_missing_init_data() -> None:
    raw = _load("replay_raw_parse_partial.json")
    sha = sha256_hex_of_canonical_json(raw)
    status, _, rep = run_metadata_extraction(
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "partial"
    assert rep["extraction_status"] == "partial"


def test_invalid_schema_source_contract_failed() -> None:
    raw = _load("replay_raw_parse_valid.json")
    raw = dict(raw)
    raw["schema_version"] = "wrong"
    sha = sha256_hex_of_canonical_json(raw)
    status, _, rep = run_metadata_extraction(
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "source_contract_failed"
    assert "raw_parse_schema_invalid" in rep["reason_codes"]


def test_malformed_player_list_ambiguous() -> None:
    raw = _load("replay_raw_parse_valid.json")
    raw = json.loads(json.dumps(raw))
    raw["raw_sections"]["details"]["m_playerList"] = ["not-a-dict"]
    sha = sha256_hex_of_canonical_json(raw)
    status, _, rep = run_metadata_extraction(
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    assert status == "partial"
    assert "player_metadata_ambiguous" in rep["reason_codes"]


def test_build_metadata_envelope_schema_version() -> None:
    raw = _load("replay_raw_parse_valid.json")
    sha = sha256_hex_of_canonical_json(raw)
    env, _ = build_metadata_envelope(raw=raw, source_raw_parse_sha256=sha)
    assert env["schema_version"] == "starlab.replay_metadata.v1"
    assert env["metadata_contract_version"] == "starlab.replay_metadata_contract.v1"


@pytest.mark.parametrize("fname", ["replay_raw_parse_valid.json", "replay_raw_parse_partial.json"])
def test_raw_fixture_schema_matches_m08(fname: str) -> None:
    raw = _load(fname)
    assert raw["schema_version"] in RAW_PARSE_SCHEMA_ACCEPTED
    assert raw["schema_version"] == RAW_PARSE_SCHEMA_EXPECTED


def test_extract_from_paths_writes_files(tmp_path: Path) -> None:
    status, _, _ = extract_from_paths(
        output_dir=tmp_path,
        parse_receipt_path=RCP_VALID,
        parse_report_path=RPT_VALID,
        raw_parse_path=RAW_VALID,
    )
    assert status == "extracted"
    assert (tmp_path / "replay_metadata.json").is_file()
    assert (tmp_path / "replay_metadata_report.json").is_file()
