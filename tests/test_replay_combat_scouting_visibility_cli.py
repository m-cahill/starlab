"""CLI tests for M12 combat / scouting / visibility extraction."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_build_order_economy import main as bo_main
from starlab.replays.extract_replay_combat_scouting_visibility import main as csv_main
from starlab.replays.extract_replay_timeline import main as tl_main

FIX = Path(__file__).resolve().parent / "fixtures" / "m12"


def test_cli_success_path(tmp_path: Path) -> None:
    out_tl = tmp_path / "tl"
    out_tl.mkdir()
    assert (
        tl_main(
            [
                "--raw-parse",
                str(FIX / "replay_raw_parse_m12_combined.json"),
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
                str(FIX / "replay_raw_parse_m12_combined.json"),
                "--output-dir",
                str(out_bo),
            ],
        )
        == 0
    )
    out_m12 = tmp_path / "m12"
    out_m12.mkdir()
    assert (
        csv_main(
            [
                "--timeline",
                str(out_tl / "replay_timeline.json"),
                "--build-order-economy",
                str(out_bo / "replay_build_order_economy.json"),
                "--raw-parse",
                str(FIX / "replay_raw_parse_m12_combined.json"),
                "--output-dir",
                str(out_m12),
            ],
        )
        == 0
    )
    body = json.loads(
        (out_m12 / "replay_combat_scouting_visibility.json").read_text(encoding="utf-8"),
    )
    assert (
        body["combat_scouting_visibility_profile"]
        == "starlab.replay_combat_scouting_visibility.m12.v1"
    )


def test_cli_timeline_load_failure(tmp_path: Path) -> None:
    out_m12 = tmp_path / "m12"
    out_m12.mkdir()
    bad = tmp_path / "missing.json"
    bad.write_text("not json", encoding="utf-8")
    bo = FIX / "replay_build_order_economy_m12_combined.json"
    assert (
        csv_main(
            ["--timeline", str(bad), "--build-order-economy", str(bo), "--output-dir", str(out_m12)]
        )
        == 4
    )
