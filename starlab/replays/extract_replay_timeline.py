"""CLI: M08/M10 ``replay_raw_parse`` → ``replay_timeline.json`` + report (M10)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.timeline_io import exit_code_for_timeline_run, extract_timeline_from_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.extract_replay_timeline",
        description=(
            "Emit replay_timeline.json and replay_timeline_report.json from replay_raw_parse.json"
        ),
    )
    parser.add_argument(
        "--raw-parse",
        required=True,
        type=Path,
        help="Path to replay_raw_parse.json (M08/M10)",
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for JSON outputs")
    parser.add_argument(
        "--parse-receipt",
        type=Path,
        default=None,
        help="Optional replay_parse_receipt.json for hash linkage",
    )
    parser.add_argument(
        "--parse-report",
        type=Path,
        default=None,
        help="Optional replay_parse_report.json for linkage",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=None,
        help="Optional replay_metadata.json for linkage",
    )
    parser.add_argument(
        "--metadata-report",
        type=Path,
        default=None,
        help="Optional replay_metadata_report.json for linkage",
    )
    args = parser.parse_args(argv)

    status, _, _ = extract_timeline_from_paths(
        metadata_path=args.metadata,
        metadata_report_path=args.metadata_report,
        output_dir=args.output_dir,
        parse_receipt_path=args.parse_receipt,
        parse_report_path=args.parse_report,
        raw_parse_path=args.raw_parse,
    )
    return exit_code_for_timeline_run(status)


if __name__ == "__main__":
    sys.exit(main())
