"""M08 parse_replay CLI tests (default adapter; CI without replay-parser extra)."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.parse_replay import main
from starlab.replays.s2protocol_adapter import S2ProtocolReplayAdapter

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
OPAQUE_REPLAY = FIXTURE_DIR / "replay_m07_generated.SC2Replay"


def _expected_default_cli_exit() -> int:
    """Expected exit for default CLI on opaque fixture.

    CI: no ``s2protocol`` → ``parser_unavailable`` (3).
    Local dev with optional extra: fixture is not a valid MPQ → ``parse_failed`` (4).
    """

    if not S2ProtocolReplayAdapter().dependency_available():
        return 3
    return 4


def test_cli_writes_three_json_files(tmp_path: Path) -> None:
    rc = main(
        [
            "--replay",
            str(OPAQUE_REPLAY),
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert rc == _expected_default_cli_exit()
    for name in (
        "replay_parse_receipt.json",
        "replay_parse_report.json",
        "replay_raw_parse.json",
    ):
        p = tmp_path / name
        assert p.is_file()
        json.loads(p.read_text(encoding="utf-8"))


def test_cli_deterministic_twice(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    d1.mkdir()
    d2.mkdir()
    exp = _expected_default_cli_exit()
    assert main(["--replay", str(OPAQUE_REPLAY), "--output-dir", str(d1)]) == exp
    assert main(["--replay", str(OPAQUE_REPLAY), "--output-dir", str(d2)]) == exp
    assert (d1 / "replay_parse_report.json").read_text(encoding="utf-8") == (
        d2 / "replay_parse_report.json"
    ).read_text(encoding="utf-8")
