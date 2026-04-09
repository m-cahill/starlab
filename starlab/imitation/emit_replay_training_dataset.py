"""CLI: emit replay_training_dataset.json and replay_training_dataset_report.json (M26)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.imitation.dataset_models import (
    REPLAY_TRAINING_DATASET_FILENAME,
    REPLAY_TRAINING_DATASET_REPORT_FILENAME,
)
from starlab.imitation.dataset_views import build_replay_training_dataset_artifacts
from starlab.runs.json_util import canonical_json_dumps


def write_replay_training_dataset_artifacts(
    *,
    bundle_dirs: list[Path],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset, report = build_replay_training_dataset_artifacts(bundle_dirs=bundle_dirs)
    p_ds = output_dir / REPLAY_TRAINING_DATASET_FILENAME
    p_rep = output_dir / REPLAY_TRAINING_DATASET_REPORT_FILENAME
    p_ds.write_text(canonical_json_dumps(dataset), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(report), encoding="utf-8")
    return p_ds, p_rep


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.imitation.emit_replay_training_dataset",
        description=(
            "Emit replay_training_dataset.json and replay_training_dataset_report.json "
            "from governed M14 replay bundle directories (M26)."
        ),
    )
    parser.add_argument(
        "--bundle",
        action="append",
        dest="bundles",
        required=True,
        metavar="PATH",
        type=Path,
        help="Directory containing replay_bundle_*.json and governed replay JSON (repeatable)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for dataset + report JSON outputs",
    )
    args = parser.parse_args(argv)

    try:
        write_replay_training_dataset_artifacts(
            bundle_dirs=args.bundles,
            output_dir=args.output_dir,
        )
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
