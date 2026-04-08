"""CLI tests for M13 replay slice extraction."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_slices import main as slice_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m13"


def test_cli_success_path(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    assert (
        slice_main(
            [
                "--timeline",
                str(FIX / "replay_timeline.json"),
                "--build-order-economy",
                str(FIX / "replay_build_order_economy.json"),
                "--combat-scouting-visibility",
                str(FIX / "replay_combat_scouting_visibility.json"),
                "--output-dir",
                str(out),
            ],
        )
        == 0
    )
    body = json.loads((out / "replay_slices.json").read_text(encoding="utf-8"))
    assert body["profile"] == "starlab.replay_slices.m13.v1"
    assert len(body["slices"]) == 8


def test_cli_timeline_load_failure(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    bad = tmp_path / "missing.json"
    bad.write_text("not json", encoding="utf-8")
    assert (
        slice_main(
            [
                "--timeline",
                str(bad),
                "--build-order-economy",
                str(FIX / "replay_build_order_economy.json"),
                "--combat-scouting-visibility",
                str(FIX / "replay_combat_scouting_visibility.json"),
                "--output-dir",
                str(out),
            ],
        )
        == 4
    )
