"""CLI tests for M14 replay bundle extraction."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_bundle import main as bundle_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m14"


def test_cli_success_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    assert (
        bundle_main(
            [
                "--input-dir",
                str(FIX),
                "--output-dir",
                str(out),
                "--bundle-created-from",
                "tests/fixtures/m14",
            ],
        )
        == 0
    )
    body = json.loads((out / "replay_bundle_manifest.json").read_text(encoding="utf-8"))
    assert body["profile"] == "starlab.replay_bundle.m14.v1"
    assert body["primary_artifacts"][0] == "replay_metadata.json"


def test_cli_missing_primary_failure(tmp_path: Path) -> None:
    bad_dir = tmp_path / "incomplete"
    bad_dir.mkdir()
    (bad_dir / "replay_metadata.json").write_text("{}", encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    assert (
        bundle_main(
            [
                "--input-dir",
                str(bad_dir),
                "--output-dir",
                str(out),
            ],
        )
        == 4
    )
