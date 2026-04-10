"""CLI: emit replay_hierarchical_imitation_agent.json + _report.json (M30)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.hierarchy.hierarchical_agent_fit import (
    write_replay_hierarchical_imitation_agent_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.hierarchy.emit_replay_hierarchical_imitation_agent",
        description=(
            "Emit replay_hierarchical_imitation_agent.json and "
            "replay_hierarchical_imitation_agent_report.json (deterministic M30 artifacts)."
        ),
    )
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        help="Path to governed replay_training_dataset.json (M26)",
    )
    parser.add_argument(
        "--bundle",
        action="append",
        required=True,
        dest="bundle_dirs",
        metavar="DIR",
        help="M14 bundle directory (repeatable)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for agent + report JSON outputs",
    )
    args = parser.parse_args(argv)

    write_replay_hierarchical_imitation_agent_artifacts(
        dataset_path=args.dataset,
        bundle_dirs=[Path(p).resolve() for p in args.bundle_dirs],
        output_dir=args.output_dir,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
