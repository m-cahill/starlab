"""CLI: reconcile canonical_state.json with observation_surface.json (M19 audit)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.observation.observation_reconciliation_pipeline import emit_reconciliation_artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.observation.audit_observation_surface",
        description=(
            "Audit one M16 canonical_state.json against one M18 observation_surface.json; "
            "writes observation_reconciliation_audit.json and "
            "observation_reconciliation_audit_report.json."
        ),
    )
    parser.add_argument(
        "--canonical-state",
        required=True,
        type=Path,
        help="Path to M16 canonical_state.json",
    )
    parser.add_argument(
        "--observation-surface",
        required=True,
        type=Path,
        help="Path to observation_surface.json",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for reconciliation audit artifacts",
    )
    parser.add_argument(
        "--canonical-state-report",
        type=Path,
        default=None,
        help="Optional canonical_state_report.json for hash cross-check",
    )
    parser.add_argument(
        "--observation-surface-report",
        type=Path,
        default=None,
        help="Optional observation_surface_report.json for hash cross-check",
    )
    args = parser.parse_args(argv)

    try:
        _ap, _rp, verdict = emit_reconciliation_artifacts(
            canonical_state_path=args.canonical_state,
            observation_surface_path=args.observation_surface,
            output_dir=args.output_dir,
            canonical_state_report_path=args.canonical_state_report,
            observation_surface_report_path=args.observation_surface_report,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if verdict == "fail":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
