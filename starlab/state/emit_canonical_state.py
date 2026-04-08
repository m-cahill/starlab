"""CLI: emit canonical_state.json + canonical_state_report.json from an M14 bundle (M16)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.state.canonical_state_pipeline import emit_canonical_state_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.state.emit_canonical_state",
        description=(
            "Materialize one M15-shaped canonical state frame at --gameloop from a directory "
            "containing M14 replay_bundle_*.json and governed M09–M13 primary JSON."
        ),
    )
    parser.add_argument(
        "--bundle-dir",
        required=True,
        type=Path,
        help="Directory with replay_bundle_manifest.json / lineage / contents + primary artifacts",
    )
    parser.add_argument(
        "--gameloop",
        required=True,
        type=int,
        help="Target gameloop (non-negative; must not exceed replay_length_loops)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for canonical_state.json and canonical_state_report.json",
    )
    args = parser.parse_args(argv)

    try:
        emit_canonical_state_artifacts(
            bundle_dir=args.bundle_dir,
            output_dir=args.output_dir,
            target_gameloop=args.gameloop,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
