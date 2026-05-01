"""CLI: V15-M49 bounded scorecard result execution surface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m49_bounded_scorecard_result_execution_io import (
    emit_m49_fixture_ci,
    emit_m49_forbidden_flag_refusal,
    emit_m49_operator_declared,
    emit_m49_operator_preflight,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
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
            "V15-M49: deterministic bounded scorecard result execution surface over sealed "
            "V15-M48 preflight JSON and declared scorecard result evidence. Does not emit "
            "benchmark pass/fail, evaluate strength, promote checkpoints, invoke torch.load, "
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
            "fixture_ci: synthesize sealed M48 fixture then bounded result evidence; "
            "operator_preflight: sealed M48 JSON + scorecard result evidence JSON; "
            "operator_declared: declared M49 result JSON for normalization / sealing"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M49 result execution artifacts",
    )
    parser.add_argument(
        "--m48-preflight-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_scorecard_execution_preflight.json (V15-M48); "
        "required for operator_preflight",
    )
    parser.add_argument(
        "--scorecard-result-evidence-json",
        type=Path,
        default=None,
        help="Declared scorecard result evidence JSON "
        "(starlab.v15.bounded_scorecard_result_evidence.v1); "
        "required for operator_preflight",
    )
    parser.add_argument(
        "--declared-result-json",
        type=Path,
        default=None,
        help="Operator-declared M49 result JSON (operator_declared profile)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m49_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m49_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        dr = args.declared_result_json
        if dr is None:
            parser.error("--declared-result-json is required for operator_declared")
        emit_m49_operator_declared(out, declared_result_path=dr)
        return 0

    if args.scorecard_result_evidence_json is None:
        parser.error("--scorecard-result-evidence-json is required for operator_preflight")

    if args.m48_preflight_json is None:
        parser.error("--m48-preflight-json is required for operator_preflight")

    emit_m49_operator_preflight(
        out,
        m48_path=args.m48_preflight_json,
        evidence_path=args.scorecard_result_evidence_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
