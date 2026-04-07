"""CLI tests for M11 build-order / economy extraction."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_build_order_economy import main as bo_main
from starlab.replays.extract_replay_timeline import main as tl_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m11"


def test_cli_success_path(tmp_path: Path) -> None:
    out_tl = tmp_path / "tl"
    out_tl.mkdir()
    assert (
        tl_main(
            [
                "--raw-parse",
                str(FIX / "replay_raw_parse_m11_happy.json"),
                "--output-dir",
                str(out_tl),
            ],
        )
        == 0
    )
    out_bo = tmp_path / "bo"
    out_bo.mkdir()
    assert (
        bo_main(
            [
                "--timeline",
                str(out_tl / "replay_timeline.json"),
                "--raw-parse",
                str(FIX / "replay_raw_parse_m11_happy.json"),
                "--output-dir",
                str(out_bo),
            ],
        )
        == 0
    )
    body = json.loads((out_bo / "replay_build_order_economy.json").read_text(encoding="utf-8"))
    assert body["build_order_economy_profile"] == "starlab.replay_build_order_economy.m11.v1"


def test_cli_timeline_load_failure(tmp_path: Path) -> None:
    out_bo = tmp_path / "bo"
    out_bo.mkdir()
    bad = tmp_path / "missing.json"
    bad.write_text("not json", encoding="utf-8")
    assert bo_main(["--timeline", str(bad), "--output-dir", str(out_bo)]) == 4
