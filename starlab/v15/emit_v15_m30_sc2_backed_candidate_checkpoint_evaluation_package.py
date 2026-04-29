"""CLI: emit V15-M30 SC2-backed candidate checkpoint evaluation package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_io import (
    emit_m30_sc2_backed_candidate_checkpoint_evaluation_package,
)


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M30 candidate checkpoint evaluation package from sealed M27/M28/M29 JSON. "
            "Does not read checkpoint blobs. M05 scorecard is optional (protocol bind only)."
        ),
    )
    parser.add_argument(
        "--m27-sc2-rollout-json",
        required=True,
        type=Path,
        help="Sealed v15_sc2_rollout_training_loop_integration.json (M27)",
    )
    parser.add_argument(
        "--m28-sc2-backed-training-json",
        required=True,
        type=Path,
        help="Sealed v15_sc2_backed_t1_candidate_training.json (M28)",
    )
    parser.add_argument(
        "--m29-full-30min-run-json",
        required=True,
        type=Path,
        help="Sealed v15_full_30min_sc2_backed_t1_run.json (M29)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="Optional M05 v15_strong_agent_scorecard.json (protocol binding only)",
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory")
    args = parser.parse_args(argv)

    emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
        args.output_dir.resolve(),
        m27_path=_must_file(args.m27_sc2_rollout_json, "--m27-sc2-rollout-json"),
        m28_path=_must_file(args.m28_sc2_backed_training_json, "--m28-sc2-backed-training-json"),
        m29_path=_must_file(args.m29_full_30min_run_json, "--m29-full-30min-run-json"),
        scorecard_path=(
            _must_file(args.m05_scorecard_json, "--m05-scorecard-json")
            if args.m05_scorecard_json is not None
            else None
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
