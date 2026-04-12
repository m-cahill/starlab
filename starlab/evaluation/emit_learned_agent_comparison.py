"""CLI: emit ``learned_agent_comparison.json`` + report (M42)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.evaluation.learned_agent_comparison_harness import (
    write_learned_agent_comparison_from_paths,
)
from starlab.training.training_program_io import build_agent_training_program_contract


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare frozen M27 baseline and M41 replay-imitation training runs "
            "on the shared M28 offline metric surface."
        ),
    )
    parser.add_argument(
        "--contract",
        required=True,
        type=Path,
        help="Path to M20-valid benchmark contract JSON (M28 fixture surface).",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        help="Path to replay_training_dataset.json.",
    )
    parser.add_argument(
        "--bundle",
        action="append",
        dest="bundles",
        default=[],
        metavar="PATH",
        help="M14 bundle dir (repeat once per dataset bundle_id).",
    )
    parser.add_argument(
        "--baseline",
        required=True,
        type=Path,
        help="Path to replay_imitation_baseline.json (M27 frozen baseline).",
    )
    parser.add_argument(
        "--m27-candidate-id",
        default="m27_frozen_baseline",
        help="Stable id for the M27 candidate in the comparison artifact.",
    )
    parser.add_argument(
        "--m41",
        action="append",
        nargs=3,
        default=[],
        metavar=("ID", "RUN_JSON", "RUN_DIR"),
        help=(
            "M41 candidate: candidate id, replay_imitation_training_run.json path, "
            "run output directory (contains weights/). Repeat --m41 for multiple runs."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for learned_agent_comparison.json and report.",
    )
    args = parser.parse_args(argv)

    if not args.bundles:
        print("error: at least one --bundle is required", file=sys.stderr)
        return 2

    m41_specs: list[tuple[str, Path, Path]] = []
    for triple in args.m41:
        cid, run_json_s, run_dir_s = triple[0], triple[1], triple[2]
        if not str(cid).strip():
            print("error: M41 candidate id must be non-empty", file=sys.stderr)
            return 2
        m41_specs.append((str(cid), Path(run_json_s), Path(run_dir_s)))

    contract = build_agent_training_program_contract()

    try:
        write_learned_agent_comparison_from_paths(
            contract_path=args.contract,
            dataset_path=args.dataset,
            bundle_dirs=[Path(p) for p in args.bundles],
            training_program_contract=contract,
            output_dir=args.output_dir,
            baseline_path=args.baseline,
            m41_specs=m41_specs,
            m27_candidate_id=str(args.m27_candidate_id),
        )
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
