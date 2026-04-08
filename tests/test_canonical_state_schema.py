"""Tests for M15 canonical state JSON Schema emission and validation."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.state.canonical_state_io import (
    build_canonical_state_schema_report,
    validate_canonical_state_file,
    write_canonical_state_schema_artifacts,
)
from starlab.state.canonical_state_models import CANONICAL_STATE_PROFILE
from starlab.state.canonical_state_schema import (
    build_canonical_state_json_schema,
    validate_canonical_state_frame,
)

FIX = Path(__file__).resolve().parent / "fixtures" / "m15"


def test_deterministic_golden_schema_emission() -> None:
    expected_path = FIX / "expected_canonical_state_schema.json"
    schema = build_canonical_state_json_schema()
    assert json.loads(canonical_json_dumps(schema)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_schema_report_emission() -> None:
    expected_path = FIX / "expected_canonical_state_schema_report.json"
    schema = build_canonical_state_json_schema()
    report = build_canonical_state_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid": FIX / "valid_canonical_state_example.json",
            "invalid": FIX / "invalid_canonical_state_example_missing_required.json",
        },
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_schema_fingerprint_stable() -> None:
    schema = build_canonical_state_json_schema()
    h1 = sha256_hex_of_canonical_json(schema)
    h2 = sha256_hex_of_canonical_json(build_canonical_state_json_schema())
    assert h1 == h2
    report = build_canonical_state_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid": FIX / "valid_canonical_state_example.json",
        },
    )
    assert report["schema_sha256"] == h1
    assert report["profile"] == CANONICAL_STATE_PROFILE


def test_valid_example_passes_validation() -> None:
    assert validate_canonical_state_file(FIX / "valid_canonical_state_example.json") == []


def test_invalid_example_fails_validation() -> None:
    bad = FIX / "invalid_canonical_state_example_missing_required.json"
    errs = validate_canonical_state_file(bad)
    assert any("schema_version" in e for e in errs)


def test_omission_nullability_enforced() -> None:
    """Optional sections may be omitted; invalid documents fail required-field checks."""

    doc = json.loads((FIX / "valid_canonical_state_example.json").read_text(encoding="utf-8"))
    assert "combat_context" not in doc["players"][0]
    assert validate_canonical_state_frame(doc) == []

    bad = dict(doc)
    bad["extra_top_level"] = 1
    errs = validate_canonical_state_frame(bad)
    assert any("additional properties" in e.lower() for e in errs)


def test_write_artifacts_round_trip(tmp_path: Path) -> None:
    write_canonical_state_schema_artifacts(
        tmp_path,
        example_fixture_paths={
            "valid": FIX / "valid_canonical_state_example.json",
        },
    )
    assert (tmp_path / "canonical_state_schema.json").is_file()
    assert (tmp_path / "canonical_state_schema_report.json").is_file()
