"""CLI tests for M15 canonical state schema emission."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.state.emit_canonical_state_schema import main as emit_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m15"


def test_cli_success_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert (
        emit_main(
            [
                "--output-dir",
                str(out),
                "--example-fixture",
                f"valid={FIX / 'valid_canonical_state_example.json'}",
            ],
        )
        == 0
    )
    schema = json.loads((out / "canonical_state_schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    report = json.loads((out / "canonical_state_schema_report.json").read_text(encoding="utf-8"))
    assert "schema_sha256" in report
    assert "valid" in report["example_fixture_hashes"]


def test_cli_invalid_example_fixture_flag() -> None:
    assert emit_main(["--output-dir", ".", "--example-fixture", "nope"]) == 2
