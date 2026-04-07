"""CLI: M10 ``replay_timeline`` (+ optional raw parse identity) → build-order/economy JSON (M11)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.build_order_economy_io import (
    exit_code_for_build_order_economy_run,
    extract_build_order_economy_from_paths,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.extract_replay_build_order_economy",
        description=(
            "Emit replay_build_order_economy.json and replay_build_order_economy_report.json "
            "from replay_timeline.json (optional replay_raw_parse.json v2 for identity)"
        ),
    )
    parser.add_argument(
        "--timeline",
        required=True,
        type=Path,
        help="Path to replay_timeline.json (M10)",
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for JSON outputs")
    parser.add_argument(
        "--raw-parse",
        type=Path,
        default=None,
        help="Optional replay_raw_parse.json (v2) for entity identity lookup only",
    )
    parser.add_argument(
        "--timeline-report",
        type=Path,
        default=None,
        help="Optional replay_timeline_report.json for lineage hashes",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=None,
        help="Optional replay_metadata.json for lineage hashes",
    )
    parser.add_argument(
        "--metadata-report",
        type=Path,
        default=None,
        help="Optional replay_metadata_report.json for lineage hashes",
    )
    args = parser.parse_args(argv)

    status, _, _ = extract_build_order_economy_from_paths(
        metadata_path=args.metadata,
        metadata_report_path=args.metadata_report,
        output_dir=args.output_dir,
        raw_parse_path=args.raw_parse,
        timeline_path=args.timeline,
        timeline_report_path=args.timeline_report,
    )
    return exit_code_for_build_order_economy_run(status)


if __name__ == "__main__":
    sys.exit(main())
