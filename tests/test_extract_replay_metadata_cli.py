"""M09 extract_replay_metadata CLI tests."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.replays.extract_replay_metadata import main

FIX = Path(__file__).resolve().parent / "fixtures" / "m09"
RAW_VALID = FIX / "replay_raw_parse_valid.json"
RCP_VALID = FIX / "replay_parse_receipt_valid.json"
RPT_VALID = FIX / "replay_parse_report_valid.json"


def test_cli_exit_zero_with_linkage(tmp_path: Path) -> None:
    rc = main(
        [
            "--raw-parse",
            str(RAW_VALID),
            "--output-dir",
            str(tmp_path),
            "--parse-receipt",
            str(RCP_VALID),
            "--parse-report",
            str(RPT_VALID),
        ],
    )
    assert rc == 0


def test_cli_deterministic_twice(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    d1.mkdir()
    d2.mkdir()
    tail = ["--parse-receipt", str(RCP_VALID), "--parse-report", str(RPT_VALID)]
    assert main(["--raw-parse", str(RAW_VALID), "--output-dir", str(d1), *tail]) == 0
    assert main(["--raw-parse", str(RAW_VALID), "--output-dir", str(d2), *tail]) == 0
    assert (d1 / "replay_metadata.json").read_text(encoding="utf-8") == (
        d2 / "replay_metadata.json"
    ).read_text(encoding="utf-8")


def test_cli_source_contract_failed_exit(tmp_path: Path) -> None:
    bad = tmp_path / "bad_receipt.json"
    data = json.loads(RCP_VALID.read_text(encoding="utf-8"))
    data["raw_parse_sha256"] = "0" * 64
    bad.write_text(json.dumps(data, sort_keys=True, indent=2), encoding="utf-8")
    out = tmp_path / "out2"
    out.mkdir()
    rc = main(
        [
            "--raw-parse",
            str(RAW_VALID),
            "--output-dir",
            str(out),
            "--parse-receipt",
            str(bad),
        ],
    )
    assert rc == 5


def test_cli_partial_raw_exit_zero(tmp_path: Path) -> None:
    partial = FIX / "replay_raw_parse_partial.json"
    rc = main(
        [
            "--raw-parse",
            str(partial),
            "--output-dir",
            str(tmp_path),
        ],
    )
    assert rc == 0
