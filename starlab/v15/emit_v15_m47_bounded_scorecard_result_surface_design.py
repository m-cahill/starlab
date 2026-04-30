"""CLI: V15-M47 bounded scorecard result surface design / refusal gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m47_bounded_scorecard_result_surface_design_io import (
    emit_m47_fixture_ci,
    emit_m47_forbidden_flag_refusal,
    emit_m47_operator_declared,
    emit_m47_operator_preflight,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M47: deterministic bounded scorecard result surface design / refusal gate "
            "over sealed V15-M46 readout JSON. Does not produce scorecard results, benchmark "
            "pass/fail, scorecard totals, strength evaluation, checkpoint promotion, "
            "torch.load, checkpoint blob loading, live SC2, XAI, human-panel, showcase, v2, "
            "or T2–T5 execution."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_PREFLIGHT,
            PROFILE_OPERATOR_DECLARED,
        ),
        help=(
            "fixture_ci: reuse M46 fixture chain then consume sealed M46; "
            "operator_preflight: consume sealed v15_bounded_evaluation_readout_decision.json; "
            "operator_declared: normalize/validate declared M47 design JSON"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M47 surface-design artifacts",
    )
    parser.add_argument(
        "--m46-readout-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_evaluation_readout_decision.json (V15-M46)",
    )
    parser.add_argument(
        "--declared-scorecard-surface-json",
        type=Path,
        default=None,
        help="Operator-declared M47 design JSON (operator_declared profile)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m47_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m47_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        dr = args.declared_scorecard_surface_json
        if dr is None:
            parser.error("--declared-scorecard-surface-json is required for operator_declared")
        emit_m47_operator_declared(out, declared_surface_path=dr)
        return 0

    emit_m47_operator_preflight(out, m46_path=args.m46_readout_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
