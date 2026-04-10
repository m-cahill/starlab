"""Replay parse orchestration, linkage checks, and artifact emission (M08)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.replays.parser_io_run import run_replay_parse
from starlab.replays.parser_models import ParseStatus
from starlab.runs.json_util import canonical_json_dumps

__all__ = [
    "exit_code_for_parse_status",
    "run_replay_parse",
    "write_parse_artifacts",
]


def write_parse_artifacts(
    *,
    output_dir: Path,
    receipt: dict[str, Any],
    report: dict[str, Any],
    raw_parse: dict[str, Any],
) -> tuple[Path, Path, Path]:
    """Write deterministic JSON files with trailing newlines."""

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / "replay_parse_receipt.json"
    report_path = output_dir / "replay_parse_report.json"
    raw_path = output_dir / "replay_raw_parse.json"
    receipt_path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    report_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    raw_path.write_text(canonical_json_dumps(raw_parse), encoding="utf-8")
    return receipt_path, report_path, raw_path


def exit_code_for_parse_status(status: ParseStatus) -> int:
    """CLI exit code mapping for ``parse_status``."""

    if status == "parsed":
        return 0
    if status == "unsupported_protocol":
        return 2
    if status == "parser_unavailable":
        return 3
    if status == "parse_failed":
        return 4
    if status == "input_contract_failed":
        return 5
    msg = f"unknown parse status: {status!r}"
    raise ValueError(msg)
