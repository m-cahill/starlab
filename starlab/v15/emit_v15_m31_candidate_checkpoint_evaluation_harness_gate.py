"""CLI: emit V15-M31 evaluation harness dry-run gate artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    build_fixture_m30_sealed_package,
    emit_v15_m31_candidate_checkpoint_evaluation_harness_gate,
    load_sealed_m30_package_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M31 harness dry-run gate from sealed V15-M30 evaluation package JSON. "
            "Does not load checkpoint blobs or run benchmark games."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit using a deterministic synthetic sealed M30 package internal to this gate",
    )
    mode.add_argument(
        "--m30-evaluation-package-json",
        type=Path,
        help="Path to sealed v15_candidate_checkpoint_evaluation_package.json (M30 profile)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help=(
            "Optional M05 protocol JSON (evaluation_protocol metadata binding at M31; "
            "does not imply execution)"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for harness gate artifacts",
    )

    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()

    if args.fixture_ci:
        m30 = build_fixture_m30_sealed_package()
        fixture_ci = True
    else:
        mp = args.m30_evaluation_package_json
        if mp is None or not Path(mp).is_file():
            raise SystemExit(
                f"missing required M30 sealed package JSON (--m30-evaluation-package-json): {mp!s}",
            )
        m30 = load_sealed_m30_package_json(Path(mp).resolve())
        fixture_ci = False

    if args.m05_scorecard_json is not None:
        m05_p = Path(args.m05_scorecard_json).resolve()
        if not m05_p.is_file():
            raise SystemExit(f"M05 scorecard JSON not found (--m05-scorecard-json): {m05_p}")
        m05 = m05_p
    else:
        m05 = None

    emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
        output_dir,
        m30_sealed=m30,
        fixture_ci=fixture_ci,
        m05_path=m05,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
