"""CLI: V15-M50 scorecard result readout / benchmark pass-fail refusal decision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m50_scorecard_result_readout_decision_io import (
    emit_m50_fixture_ci,
    emit_m50_forbidden_flag_refusal,
    emit_m50_operator_declared,
    emit_m50_operator_preflight,
)
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    FORBIDDEN_CLI_FLAGS_M50,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS_M50 if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS_M50]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M50: deterministic scorecard readout and benchmark pass/fail refusal over sealed "
            "V15-M49 bounded scorecard result execution JSON. Does not execute benchmarks, emit "
            "authoritative pass/fail, evaluate strength, promote checkpoints, invoke torch.load, "
            "load checkpoint blobs, run live SC2, XAI, human-panel, showcase, v2, or T2–T5."
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
            "fixture_ci: M49 fixture chain then M50 readout; "
            "operator_preflight: sealed M49 JSON path + optional expected SHA; "
            "operator_declared: declared M50 envelope JSON"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M50 readout decision artifacts",
    )
    parser.add_argument(
        "--m49-scorecard-result-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_scorecard_result_execution.json (V15-M49); "
        "required for operator_preflight",
    )
    parser.add_argument(
        "--expected-m49-scorecard-result-sha256",
        default=None,
        help="Optional lowercase SHA256 of sealed M49 artifact body (digest field)",
    )
    parser.add_argument(
        "--declared-readout-json",
        type=Path,
        default=None,
        help="Operator-declared M50 envelope JSON (operator_declared profile)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m50_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m50_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        dr = args.declared_readout_json
        if dr is None:
            parser.error("--declared-readout-json is required for operator_declared")
        emit_m50_operator_declared(out, declared_readout_path=dr)
        return 0

    if args.m49_scorecard_result_json is None:
        parser.error("--m49-scorecard-result-json is required for operator_preflight")

    exp = args.expected_m49_scorecard_result_sha256
    exp_norm = str(exp).strip().lower() if exp is not None and str(exp).strip() else None

    emit_m50_operator_preflight(
        out,
        m49_path=args.m49_scorecard_result_json,
        expected_sha256_lower=exp_norm,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
