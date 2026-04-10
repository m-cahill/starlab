"""CLI: emit ``learned_agent_evaluation.json`` + report (M28)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.evaluation.learned_agent_evaluation import write_learned_agent_evaluation_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate a frozen M27 imitation baseline on the M26 held-out split.",
    )
    parser.add_argument(
        "--contract",
        required=True,
        type=Path,
        help="Path to M20-valid benchmark contract JSON.",
    )
    parser.add_argument(
        "--baseline",
        required=True,
        type=Path,
        help="Path to replay_imitation_baseline.json.",
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
        help="M14 bundle dir (repeat once per dataset bundle_id; extras rejected).",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for learned_agent_evaluation.json and report.",
    )
    parser.add_argument(
        "--evaluation-split",
        default="test",
        help="Held-out split (M28 v1: test only).",
    )
    args = parser.parse_args(argv)

    if not args.bundles:
        print("error: at least one --bundle is required", file=sys.stderr)
        return 2

    try:
        write_learned_agent_evaluation_artifacts(
            contract_path=args.contract,
            baseline_path=args.baseline,
            dataset_path=args.dataset,
            bundle_dirs=[Path(p) for p in args.bundles],
            output_dir=args.output_dir,
            evaluation_split=str(args.evaluation_split),
        )
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
