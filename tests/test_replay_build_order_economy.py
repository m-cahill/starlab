"""M11 replay build-order / economy extraction tests (fixture JSON; no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.build_order_economy_extraction import extract_build_order_economy_envelope
from starlab.replays.build_order_economy_io import run_build_order_economy_extraction
from starlab.replays.timeline_io import run_timeline_extraction
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m11"


def _load(name: str) -> dict[str, Any]:
    data: Any = json.loads((FIX / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_golden_build_order_economy_deterministic() -> None:
    raw = _load("replay_raw_parse_m11_happy.json")
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
    status, body, report = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    assert status == "completed"
    exp_b = json.loads(
        (FIX / "expected_replay_build_order_economy.json").read_text(encoding="utf-8")
    )
    exp_r = json.loads(
        (FIX / "expected_replay_build_order_economy_report.json").read_text(encoding="utf-8")
    )
    assert json.loads(canonical_json_dumps(body)) == exp_b
    assert json.loads(canonical_json_dumps(report)) == exp_r


def test_timeline_ordering_is_authoritative() -> None:
    """Steps follow timeline_index even if supplemental raw keys differ in memory layout."""

    raw = _load("replay_raw_parse_m11_happy.json")
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
    _, body, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    steps = body["build_order_steps"]
    assert steps[0]["source_timeline_index"] == 0
    assert steps[1]["source_timeline_index"] == 1


def test_economy_checkpoint_accumulation_worker() -> None:
    raw = _load("replay_raw_parse_m11_happy.json")
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
    _, body, _ = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    cps = body["economy_checkpoints"]
    assert len(cps) == 1
    assert cps[0]["workers_completed"] == 1


def test_without_supplemental_raw_parse_partial_unknown() -> None:
    raw = _load("replay_raw_parse_m11_happy.json")
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
    body, _rep = extract_build_order_economy_envelope(
        raw_parse=None,
        source_metadata_report_sha256=None,
        source_metadata_sha256=None,
        source_raw_parse_sha256=None,
        source_timeline_report_sha256=None,
        source_timeline_sha256=sha_t,
        timeline=timeline,
    )
    steps = body["build_order_steps"]
    assert all(s["category"] == "unknown" for s in steps)
    _, _, full_rep = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=None,
        source_raw_parse_sha256=None,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    assert full_rep["extraction_status"] == "partial"
    assert full_rep["warnings"]


def test_catalog_classification_mapping() -> None:
    from starlab.replays.build_order_economy_catalog import ENTITY_CATEGORY, UPGRADE_CATEGORY

    assert ENTITY_CATEGORY["SCV"] == "worker"
    assert ENTITY_CATEGORY["CommandCenter"] == "townhall"
    assert UPGRADE_CATEGORY["Stimpack"] == "tech_upgrade"


def test_supplemental_raw_parse_hash_mismatch_warns() -> None:
    raw = _load("replay_raw_parse_m11_happy.json")
    sha = sha256_hex_of_canonical_json(raw)
    _, timeline, _ = run_timeline_extraction(
        metadata=None,
        metadata_report=None,
        parse_receipt=None,
        parse_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
    )
    # Mutate timeline hash field so supplemental raw hash cannot match.
    timeline["source_raw_parse_sha256"] = "0" * 64
    sha_t = sha256_hex_of_canonical_json(timeline)
    _, _, rep = run_build_order_economy_extraction(
        metadata=None,
        metadata_report=None,
        raw_parse=raw,
        source_raw_parse_sha256=sha,
        timeline=timeline,
        timeline_report=None,
        source_timeline_sha256=sha_t,
    )
    assert rep["extraction_status"] == "partial"
    assert rep["reason_codes"] == ["supplemental_raw_parse_hash_mismatch"]
