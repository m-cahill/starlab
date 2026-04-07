"""CLI: governed replay parse → receipt / report / raw parse (M08)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.parser_io import (
    exit_code_for_parse_status,
    run_replay_parse,
    write_parse_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.parse_replay",
        description=(
            "Emit replay_parse_receipt.json, replay_parse_report.json, replay_raw_parse.json"
        ),
    )
    parser.add_argument("--replay", required=True, type=Path, help="Path to .SC2Replay")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for JSON outputs")
    parser.add_argument(
        "--intake-receipt",
        type=Path,
        default=None,
        help="Optional replay_intake_receipt.json for hash linkage",
    )
    parser.add_argument(
        "--intake-report",
        type=Path,
        default=None,
        help="Optional replay_intake_report.json (advisory)",
    )
    parser.add_argument(
        "--replay-binding",
        type=Path,
        default=None,
        help="Optional replay_binding.json for hash linkage",
    )
    args = parser.parse_args(argv)

    status, receipt, report, raw_parse = run_replay_parse(
        intake_receipt_path=args.intake_receipt,
        intake_report_path=args.intake_report,
        replay_binding_path=args.replay_binding,
        replay_path=args.replay,
    )
    write_parse_artifacts(
        output_dir=args.output_dir,
        raw_parse=raw_parse,
        receipt=receipt,
        report=report,
    )
    return exit_code_for_parse_status(status)


if __name__ == "__main__":
    sys.exit(main())
