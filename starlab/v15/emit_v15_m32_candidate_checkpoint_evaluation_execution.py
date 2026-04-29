"""CLI: emit V15-M32 bounded candidate checkpoint evaluation execution artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m32_candidate_checkpoint_evaluation_execution_io import (
    build_fixture_m31_sealed_gate,
    emit_v15_m32_candidate_checkpoint_evaluation_execution,
    load_m31_harness_gate_json,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_models import (
    EXECUTION_MODE_FIXTURE,
    EXECUTION_MODE_METADATA_ONLY,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M32 bounded evaluation execution from a sealed V15-M31 harness gate. "
            "Does not load checkpoint blobs or run benchmark games."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Use an internal deterministic M31 gate (same pipeline as M31 --fixture-ci)",
    )
    mode.add_argument(
        "--m31-harness-gate-json",
        type=Path,
        help="Path to sealed v15_candidate_checkpoint_evaluation_harness_gate.json (M31)",
    )
    parser.add_argument(
        "--execution-mode",
        choices=(EXECUTION_MODE_FIXTURE, EXECUTION_MODE_METADATA_ONLY),
        default=None,
        help=(
            "With --fixture-ci must be 'fixture' if set. "
            "With --m31-harness-gate-json must be 'metadata_only' if set (default)."
        ),
    )
    parser.add_argument(
        "--max-evaluation-cases",
        type=int,
        default=1,
        help="Bounded evaluation case cap (default 1)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M32 artifacts",
    )

    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()

    max_cases = int(args.max_evaluation_cases)
    if max_cases < 1:
        raise SystemExit("--max-evaluation-cases must be >= 1")

    if args.fixture_ci:
        exec_mode = args.execution_mode or EXECUTION_MODE_FIXTURE
        if exec_mode != EXECUTION_MODE_FIXTURE:
            raise SystemExit(
                "--fixture-ci requires --execution-mode fixture (or omit --execution-mode)",
            )
        m31_gate = build_fixture_m31_sealed_gate()
        fixture_ci = True
    else:
        gp = args.m31_harness_gate_json
        if gp is None or not Path(gp).is_file():
            raise SystemExit(
                f"missing required M31 harness gate JSON (--m31-harness-gate-json): {gp!s}",
            )
        exec_mode = args.execution_mode or EXECUTION_MODE_METADATA_ONLY
        if exec_mode != EXECUTION_MODE_METADATA_ONLY:
            raise SystemExit(
                "--m31-harness-gate-json requires --execution-mode metadata_only "
                "(or omit --execution-mode)",
            )
        m31_gate = load_m31_harness_gate_json(Path(gp).resolve())
        fixture_ci = False

    emit_v15_m32_candidate_checkpoint_evaluation_execution(
        output_dir,
        m31_gate=m31_gate,
        fixture_ci=fixture_ci,
        max_evaluation_cases=max_cases,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
