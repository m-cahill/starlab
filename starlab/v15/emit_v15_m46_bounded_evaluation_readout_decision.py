"""CLI: V15-M46 bounded evaluation readout / promotion-refusal decision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m46_bounded_evaluation_readout_decision_io import (
    emit_m46_fixture_ci,
    emit_m46_forbidden_flag_refusal,
    emit_m46_operator_declared,
    emit_m46_operator_preflight,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
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
            "V15-M46: deterministic readout/refusal over sealed V15-M45 bounded execution "
            "bookkeeping. Does not produce benchmark pass/fail, scorecard results, strength "
            "evaluation, checkpoint promotion, torch.load, checkpoint blob loading, live SC2, "
            "XAI, human-panel, showcase, v2, or T2–T5 execution."
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
            "fixture_ci: synthesize M43→M44→M45 then read out; "
            "operator_preflight: consume sealed M45 JSON; "
            "operator_declared: normalize/validate declared readout JSON"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M46 readout artifacts",
    )
    parser.add_argument(
        "--m45-execution-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_candidate_evaluation_execution.json (V15-M45)",
    )
    parser.add_argument(
        "--declared-readout-json",
        type=Path,
        default=None,
        help="Operator-declared readout JSON (operator_declared profile)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m46_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m46_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        dr = args.declared_readout_json
        if dr is None:
            parser.error("--declared-readout-json is required for operator_declared")
        emit_m46_operator_declared(out, declared_readout_path=dr)
        return 0

    emit_m46_operator_preflight(out, m45_path=args.m45_execution_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
