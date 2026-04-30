"""CLI: V15-M44 bounded evaluation execution preflight (consumes sealed M43 — dry-run only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m44_bounded_evaluation_execution_preflight_io import (
    emit_m44_disallowed_execution,
    emit_m44_fixture_ci,
    emit_m44_operator,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
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
            "V15-M44: bounded evaluation execution preflight / dry-run plan over sealed "
            "V15-M43 gate JSON. Does not execute benchmarks, load checkpoint blobs, run live "
            "SC2, or promote."
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
        help="fixture_ci synthesizes M43 upstream + plan; operator profiles require paths",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M44 preflight artifacts",
    )
    parser.add_argument(
        "--m43-gate-json",
        type=Path,
        default=None,
        help="Sealed v15_bounded_evaluation_gate.json (V15-M43)",
    )
    parser.add_argument(
        "--dry-run-plan-json",
        type=Path,
        default=None,
        help="Operator dry-run envelope JSON (plan_id + scorecard_protocol object)",
    )
    parser.add_argument(
        "--evaluation-environment-json",
        type=Path,
        default=None,
        help="Sealed long GPU environment manifest JSON (M02 contract)",
    )
    parser.add_argument(
        "--operator-m43-logical-path",
        type=str,
        default=None,
        help="Optional label for m43_gate_path_logical (paths redacted by default)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m44_disallowed_execution(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m44_fixture_ci(out)
        return 0

    emit_m44_operator(
        out,
        profile=args.profile,
        m43_gate_path=args.m43_gate_json,
        dry_run_plan_path=args.dry_run_plan_json,
        evaluation_environment_path=args.evaluation_environment_json,
        operator_logical_hint=args.operator_m43_logical_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
