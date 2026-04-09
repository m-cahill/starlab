"""CLI: emit observation_surface + report from M16 canonical state (M18)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.observation.observation_surface_pipeline import emit_observation_surface_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.observation.emit_observation_surface",
        description=(
            "Materialize one M17-shaped observation frame from canonical_state.json "
            "for one perspective_player_index; writes observation_surface.json and "
            "observation_surface_report.json."
        ),
    )
    parser.add_argument(
        "--canonical-state",
        required=True,
        type=Path,
        help="Path to M16 canonical_state.json",
    )
    parser.add_argument(
        "--perspective-player-index",
        required=True,
        type=int,
        help="0-based player index (must exist in canonical_state.players)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for observation_surface.json and observation_surface_report.json",
    )
    parser.add_argument(
        "--canonical-state-report",
        type=Path,
        default=None,
        help="Optional canonical_state_report.json for hash cross-check and warning propagation",
    )
    args = parser.parse_args(argv)

    try:
        emit_observation_surface_artifacts(
            canonical_state_path=args.canonical_state,
            output_dir=args.output_dir,
            perspective_player_index=args.perspective_player_index,
            canonical_state_report_path=args.canonical_state_report,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
