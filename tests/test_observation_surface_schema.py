"""Tests for M17 observation surface JSON Schema emission and validation."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.observation.observation_surface_io import (
    build_observation_surface_schema_report,
    validate_observation_surface_file,
    write_observation_surface_schema_artifacts,
)
from starlab.observation.observation_surface_models import OBSERVATION_SURFACE_PROFILE
from starlab.observation.observation_surface_schema import (
    build_observation_surface_json_schema,
    validate_observation_surface_frame,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m17"


def test_deterministic_golden_schema_emission() -> None:
    expected_path = FIX / "expected_observation_surface_schema.json"
    schema = build_observation_surface_json_schema()
    assert json.loads(canonical_json_dumps(schema)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_schema_report_emission() -> None:
    expected_path = FIX / "expected_observation_surface_schema_report.json"
    schema = build_observation_surface_json_schema()
    report = build_observation_surface_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid": FIX / "observation_surface_valid_example.json",
            "invalid": FIX / "observation_surface_invalid_example_bad_schema_version.json",
        },
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_schema_fingerprint_stable() -> None:
    schema = build_observation_surface_json_schema()
    h1 = sha256_hex_of_canonical_json(schema)
    h2 = sha256_hex_of_canonical_json(build_observation_surface_json_schema())
    assert h1 == h2
    report = build_observation_surface_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid": FIX / "observation_surface_valid_example.json",
        },
    )
    assert report["schema_sha256"] == h1
    assert report["profile"] == OBSERVATION_SURFACE_PROFILE


def test_valid_example_passes_validation() -> None:
    assert validate_observation_surface_file(FIX / "observation_surface_valid_example.json") == []


def test_invalid_example_fails_validation() -> None:
    bad = FIX / "observation_surface_invalid_example_bad_schema_version.json"
    errs = validate_observation_surface_file(bad)
    assert any("schema_version" in e for e in errs)


def test_additional_properties_rejected() -> None:
    doc = json.loads((FIX / "observation_surface_valid_example.json").read_text(encoding="utf-8"))
    bad = dict(doc)
    bad["extra_top_level"] = 1
    errs = validate_observation_surface_frame(bad)
    assert any("additional properties" in e.lower() for e in errs)


def test_write_artifacts_round_trip(tmp_path: Path) -> None:
    write_observation_surface_schema_artifacts(
        tmp_path,
        example_fixture_paths={
            "valid": FIX / "observation_surface_valid_example.json",
        },
    )
    assert (tmp_path / "observation_surface_schema.json").is_file()
    assert (tmp_path / "observation_surface_schema_report.json").is_file()


def test_action_mask_family_order_is_stable() -> None:
    schema = build_observation_surface_json_schema()
    fam = schema["properties"]["action_mask_families"]["properties"]["families"]
    prefix = fam["prefixItems"]
    assert len(prefix) == 7
    assert prefix[0]["properties"]["family_name"]["const"] == "no_op"
    assert prefix[6]["properties"]["family_name"]["const"] == "research_or_upgrade"
