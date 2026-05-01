"""CLI: V15-M51 live candidate watchability harness (M50-bound preflight; not benchmark)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m51_live_candidate_watchability_harness_io import (
    emit_m51_fixture_ci,
    emit_m51_forbidden_flag_refusal,
    emit_m51_operator_declared,
    emit_m51_operator_preflight,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
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
            "V15-M51: governed live candidate watchability harness preflight over sealed V15-M50 "
            "JSON. Does not execute benchmarks, pass/fail authority, strength evaluation, "
            "checkpoint promotion, PyTorch checkpoint blob loading, live SC2 (this emitter), "
            "XAI, human-panel, showcase, v2, T2–T5, or 12-hour runs."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED),
        help="fixture_ci: M50 fixture + harness preflight CI; operator_preflight: sealed M50 path; "
        "operator_declared: operator envelope JSON with embedded M50 object",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M51 artifacts",
    )
    parser.add_argument(
        "--m50-readout-json",
        type=Path,
        default=None,
        help="Sealed v15_scorecard_result_readout_decision.json (V15-M50); "
        "required for operator_preflight",
    )
    parser.add_argument(
        "--expected-m50-readout-sha256",
        default=None,
        help="Optional SHA256 of sealed M50 digest field (canonical body seal)",
    )
    parser.add_argument(
        "--m42-package-json",
        type=Path,
        default=None,
        help="Optional M42 package JSON for candidate identity enrichment",
    )
    parser.add_argument(
        "--m41-package-json",
        type=Path,
        default=None,
        help="Reserved optional binding (ignored unless future milestone wires parse)",
    )
    parser.add_argument(
        "--m39-run-json",
        type=Path,
        default=None,
        help="Reserved optional binding (ignored unless future milestone wires parse)",
    )
    parser.add_argument(
        "--candidate-checkpoint-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--expected-candidate-checkpoint-sha256",
        default=None,
    )
    parser.add_argument(
        "--map-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--sc2-root",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--declared-watchability-json",
        type=Path,
        default=None,
        help="Operator-declared M51 envelope (operator_declared profile)",
    )
    parser.add_argument(
        "--embedded-m50-object-json",
        type=Path,
        default=None,
        help="Nested sealed M50 JSON file referenced by declared envelope (optional shortcut)",
    )
    args = parser.parse_args(clean)

    _ = args.m41_package_json
    _ = args.m39_run_json

    out = args.output_dir.resolve()

    if bad:
        emit_m51_forbidden_flag_refusal(
            out,
            emit_profile_short=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m51_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if args.m50_readout_json is None:
            parser.error("--m50-readout-json is required for operator_preflight")
        exp = args.expected_m50_readout_sha256
        exp_norm = str(exp).strip().lower() if exp is not None and str(exp).strip() else None
        emit_m51_operator_preflight(
            out,
            m50_path=args.m50_readout_json,
            m50_plain_override=None,
            expected_sha256_lower=exp_norm,
            emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
            require_canonical_seal=True,
            sc2_root=args.sc2_root,
            map_path=args.map_path,
            checkpoint_path=args.candidate_checkpoint_path,
            expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
            m42_path=args.m42_package_json,
        )
        return 0

    dr = args.declared_watchability_json
    emb = args.embedded_m50_object_json
    if dr is None:
        parser.error("--declared-watchability-json is required for operator_declared")
    emit_m51_operator_declared(
        out,
        declared_path=dr,
        embedded_m50_path=emb,
        sc2_root=args.sc2_root,
        map_path=args.map_path,
        checkpoint_path=args.candidate_checkpoint_path,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        m42_path=args.m42_package_json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
