"""CLI tests for M17 observation surface schema emission."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.observation.emit_observation_surface_schema import main as emit_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m17"


def test_cli_success_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert (
        emit_main(
            [
                "--output-dir",
                str(out),
                "--example-fixture",
                f"valid={FIX / 'observation_surface_valid_example.json'}",
            ],
        )
        == 0
    )
    schema = json.loads((out / "observation_surface_schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    report_path = out / "observation_surface_schema_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert "schema_sha256" in report
    assert "valid" in report["example_fixture_hashes"]


def test_cli_invalid_example_fixture_flag() -> None:
    assert emit_main(["--output-dir", ".", "--example-fixture", "nope"]) == 2
