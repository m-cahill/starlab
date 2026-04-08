"""CLI: M10 timeline + M11 economy + M12 combat/scouting/visibility → slice JSON (M13)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.replay_slice_io import (
    exit_code_for_replay_slice_run,
    extract_replay_slices_from_paths,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.extract_replay_slices",
        description=(
            "Emit replay_slices.json and replay_slices_report.json from replay_timeline.json, "
            "replay_build_order_economy.json, and replay_combat_scouting_visibility.json"
        ),
    )
    parser.add_argument(
        "--timeline",
        required=True,
        type=Path,
        help="Path to replay_timeline.json (M10)",
    )
    parser.add_argument(
        "--build-order-economy",
        required=True,
        type=Path,
        help="Path to replay_build_order_economy.json (M11)",
    )
    parser.add_argument(
        "--combat-scouting-visibility",
        required=True,
        type=Path,
        help="Path to replay_combat_scouting_visibility.json (M12)",
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for JSON outputs")
    parser.add_argument(
        "--timeline-report",
        type=Path,
        default=None,
        help="Optional replay_timeline_report.json for lineage enrichment",
    )
    parser.add_argument(
        "--build-order-economy-report",
        type=Path,
        default=None,
        help="Optional replay_build_order_economy_report.json for lineage enrichment",
    )
    parser.add_argument(
        "--combat-scouting-visibility-report",
        type=Path,
        default=None,
        help="Optional replay_combat_scouting_visibility_report.json for lineage enrichment",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=None,
        help="Optional replay_metadata.json for lineage enrichment / optional bounds check",
    )
    parser.add_argument(
        "--metadata-report",
        type=Path,
        default=None,
        help="Optional replay_metadata_report.json for lineage enrichment",
    )
    args = parser.parse_args(argv)

    status, _, _ = extract_replay_slices_from_paths(
        build_order_economy_path=args.build_order_economy,
        build_order_economy_report_path=args.build_order_economy_report,
        combat_scouting_visibility_path=args.combat_scouting_visibility,
        combat_scouting_visibility_report_path=args.combat_scouting_visibility_report,
        metadata_path=args.metadata,
        metadata_report_path=args.metadata_report,
        output_dir=args.output_dir,
        timeline_path=args.timeline,
        timeline_report_path=args.timeline_report,
    )
    return exit_code_for_replay_slice_run(status)


if __name__ == "__main__":
    sys.exit(main())
