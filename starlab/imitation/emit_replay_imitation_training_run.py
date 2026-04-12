"""CLI: emit M41 replay_imitation_training_run JSON + report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.imitation.replay_imitation_training_pipeline import (
    write_replay_imitation_training_pipeline_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.imitation.emit_replay_imitation_training_run",
        description=(
            "Train a deterministic replay-imitation classifier (sklearn) from a governed "
            "M26 replay_training_dataset.json + M14 bundle dirs; emit M41 run + report JSON "
            "and optional local-only joblib weights."
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
        help="Run root directory (e.g. out/training_runs/<run_id>/)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for LogisticRegression (default: 42)",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        metavar="ID",
        help="Optional run id override (default: deterministic hash)",
    )
    parser.add_argument(
        "--no-weights",
        action="store_true",
        help="Do not write joblib weights under weights/",
    )
    args = parser.parse_args(argv)

    try:
        write_replay_imitation_training_pipeline_artifacts(
            bundle_dirs=args.bundles,
            dataset_path=args.dataset,
            emit_weights=not args.no_weights,
            output_dir=args.output_dir,
            run_id=args.run_id,
            seed=args.seed,
        )
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
