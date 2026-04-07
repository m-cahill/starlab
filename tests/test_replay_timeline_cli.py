"""CLI tests for extract_replay_timeline (M10)."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_timeline import main

FIX = Path(__file__).resolve().parent / "fixtures" / "m10"
RAW = FIX / "replay_raw_parse_timeline_happy.json"


def test_cli_writes_two_json_files(tmp_path: Path) -> None:
    rc = main(
        [
            "--raw-parse",
            str(RAW),
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert rc == 0
    for name in ("replay_timeline.json", "replay_timeline_report.json"):
        p = tmp_path / name
        assert p.is_file()
        json.loads(p.read_text(encoding="utf-8"))


def test_cli_deterministic_twice(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    d1.mkdir()
    d2.mkdir()
    assert main(["--raw-parse", str(RAW), "--output-dir", str(d1)]) == 0
    assert main(["--raw-parse", str(RAW), "--output-dir", str(d2)]) == 0
    assert (d1 / "replay_timeline.json").read_text(encoding="utf-8") == (
        d2 / "replay_timeline.json"
    ).read_text(encoding="utf-8")


def test_cli_malformed_raw_parse(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    rc = main(["--raw-parse", str(bad), "--output-dir", str(tmp_path / "out")])
    assert rc == 4
