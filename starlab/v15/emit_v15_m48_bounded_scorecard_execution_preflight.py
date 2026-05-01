"""CLI: V15-M48 bounded scorecard execution preflight / evidence requirements gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m48_bounded_scorecard_execution_preflight_io import (
    emit_m48_fixture_ci,
    emit_m48_forbidden_flag_refusal,
    emit_m48_operator_declared,
    emit_m48_operator_preflight,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
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
            "V15-M48: deterministic bounded scorecard execution preflight / evidence "
            "requirements gate over sealed V15-M47 surface-design JSON. Does not execute "
            "scorecards, emit scorecard results, benchmark pass/fail, totals, strength "
            "evaluation, checkpoint promotion, torch.load, checkpoint blob loading, "
            "live SC2, XAI, human-panel, showcase, v2, or T2–T5 execution."
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
            "fixture_ci: emit_m47_fixture_ci chain then sealed M47 + synthetic manifest; "
            "operator_preflight: sealed M47 JSON + evidence manifest JSON; "
            "operator_declared: declared M48 preflight JSON"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M48 preflight artifacts",
    )
    parser.add_argument(
        "--m47-surface-design-json",
        type=Path,
        default=None,
        help=(
            "Sealed v15_bounded_scorecard_result_surface_design.json (V15-M47); "
            "required for operator_preflight"
        ),
    )
    parser.add_argument(
        "--evidence-manifest-json",
        type=Path,
        default=None,
        help=(
            "Evidence manifest JSON "
            "(starlab.v15.bounded_scorecard_execution_evidence_manifest.v1); "
            "required for operator_preflight"
        ),
    )
    parser.add_argument(
        "--declared-preflight-json",
        type=Path,
        default=None,
        help="Operator-declared M48 preflight JSON (operator_declared profile)",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m48_forbidden_flag_refusal(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m48_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        dp = args.declared_preflight_json
        if dp is None:
            parser.error("--declared-preflight-json is required for operator_declared")
        emit_m48_operator_declared(out, declared_preflight_path=dp)
        return 0

    if args.evidence_manifest_json is None:
        parser.error("--evidence-manifest-json is required for operator_preflight")

    if args.m47_surface_design_json is None:
        parser.error("--m47-surface-design-json is required for operator_preflight")

    emit_m48_operator_preflight(
        out,
        m47_path=args.m47_surface_design_json,
        manifest_path=args.evidence_manifest_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
