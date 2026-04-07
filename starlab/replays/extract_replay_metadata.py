"""CLI: M08 raw parse → replay_metadata.json + replay_metadata_report.json (M09)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.metadata_io import exit_code_for_extraction_status, extract_from_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.extract_replay_metadata",
        description=(
            "Emit replay_metadata.json and replay_metadata_report.json from M08 raw parse artifacts"
        ),
    )
    parser.add_argument(
        "--raw-parse",
        required=True,
        type=Path,
        help="Path to replay_raw_parse.json (M08)",
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
        help="Optional replay_parse_report.json for parse_status linkage",
    )
    args = parser.parse_args(argv)

    status, _, _ = extract_from_paths(
        output_dir=args.output_dir,
        parse_receipt_path=args.parse_receipt,
        parse_report_path=args.parse_report,
        raw_parse_path=args.raw_parse,
    )
    return exit_code_for_extraction_status(status)


if __name__ == "__main__":
    sys.exit(main())
