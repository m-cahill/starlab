"""CLI: emit replay_imitation_baseline.json and replay_imitation_baseline_report.json (M27)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.imitation.baseline_fit import write_replay_imitation_baseline_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.imitation.emit_replay_imitation_baseline",
        description=(
            "Emit replay_imitation_baseline.json and replay_imitation_baseline_report.json "
            "from a governed M26 replay_training_dataset.json and referenced M14 bundle dirs (M27)."
        ),
    )
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        metavar="PATH",
        help="Path to replay_training_dataset.json (starlab.replay_training_dataset.v1)",
    )
    parser.add_argument(
        "--bundle",
        action="append",
        dest="bundles",
        required=True,
        metavar="PATH",
        type=Path,
        help="Directory for one governed M14 replay bundle (repeatable)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for baseline + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_replay_imitation_baseline_artifacts(
            dataset_path=args.dataset,
            bundle_dirs=args.bundles,
            output_dir=args.output_dir,
        )
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
