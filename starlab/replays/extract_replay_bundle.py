"""CLI: governed replay JSON directory → bundle manifest + lineage + contents (M14)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.replays.replay_bundle_io import (
    exit_code_for_replay_bundle_run,
    extract_replay_bundle_from_paths,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.replays.extract_replay_bundle",
        description=(
            "Emit replay_bundle_manifest.json, replay_bundle_lineage.json, and "
            "replay_bundle_contents.json from replay_metadata.json, replay_timeline.json, "
            "replay_build_order_economy.json, replay_combat_scouting_visibility.json, "
            "and replay_slices.json in an input directory (optional *_report.json members)."
        ),
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        type=Path,
        help="Directory containing required replay JSON artifacts",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for bundle JSON outputs",
    )
    parser.add_argument(
        "--bundle-created-from",
        type=str,
        default=None,
        help="Stable provenance string for replay_bundle_manifest.bundle_created_from",
    )
    parser.add_argument(
        "--optional-intake-receipt",
        type=Path,
        default=None,
        help="Optional replay_intake_receipt.json for contextual M07 lineage only",
    )
    parser.add_argument(
        "--optional-parse-receipt",
        type=Path,
        default=None,
        help="Optional replay_parse_receipt.json for contextual M08 lineage only",
    )
    args = parser.parse_args(argv)

    status, _err, _m, _l, _c = extract_replay_bundle_from_paths(
        bundle_created_from=args.bundle_created_from,
        input_dir=args.input_dir,
        optional_intake_receipt_path=args.optional_intake_receipt,
        optional_parse_receipt_path=args.optional_parse_receipt,
        output_dir=args.output_dir,
    )
    return exit_code_for_replay_bundle_run(status)


if __name__ == "__main__":
    sys.exit(main())
