"""CLI: V15-M45 bounded candidate evaluation execution surface (consumes sealed M44 preflight)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m45_bounded_candidate_evaluation_execution_io import (
    emit_m45_fixture_ci,
    emit_m45_forbidden_flag_refusal,
    emit_m45_operator,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_models import (
    FORBIDDEN_CLI_FLAGS,
    GUARD_FLAG_ALLOW_OPERATOR_LOCAL_EXECUTION,
    GUARD_FLAG_AUTHORIZE_BOUNDED_EVALUATION_EXECUTION,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    allow_local = GUARD_FLAG_ALLOW_OPERATOR_LOCAL_EXECUTION in argv_list
    authorize_exec = GUARD_FLAG_AUTHORIZE_BOUNDED_EVALUATION_EXECUTION in argv_list
    clean = [
        a
        for a in clean
        if a
        not in (
            GUARD_FLAG_ALLOW_OPERATOR_LOCAL_EXECUTION,
            GUARD_FLAG_AUTHORIZE_BOUNDED_EVALUATION_EXECUTION,
        )
    ]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M45: bounded candidate evaluation execution surface over sealed V15-M44 "
            "preflight JSON. Does not produce benchmark pass/fail, scorecard results, "
            "strength evaluation, checkpoint promotion, torch.load, checkpoint blob "
            "loading, live SC2, XAI, human-panel, showcase, v2, or T2–T5 execution."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_PREFLIGHT,
            PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
        ),
        help=(
            "fixture_ci synthesizes M43→M44 upstream chain; operator_preflight validates "
            "but does not execute; operator_local_bounded_execution emits synthetic receipt"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M45 execution artifacts",
    )
    parser.add_argument(
        "--m44-preflight-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_evaluation_execution_preflight.json (V15-M44)",
    )
    parser.add_argument(
        "--operator-m44-logical-path",
        type=str,
        default=None,
        help="Optional label for m44_preflight_path_logical (paths redacted by default)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m45_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m45_fixture_ci(out)
        return 0

    emit_m45_operator(
        out,
        profile=args.profile,
        m44_preflight_path=args.m44_preflight_json,
        allow_operator_local_execution=allow_local,
        authorize_bounded_evaluation_execution=authorize_exec,
        operator_logical_hint=args.operator_m44_logical_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
