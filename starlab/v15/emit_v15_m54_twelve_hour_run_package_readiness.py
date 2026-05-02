"""CLI: V15-M54 twelve-hour run package / evaluation readiness emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m54_twelve_hour_run_package_readiness_io import (
    M54PreflightInputs,
    emit_m54_fixture_ci,
    emit_m54_forbidden_refusal,
    emit_m54_operator_declared,
    emit_m54_operator_preflight_bundle,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_models import (
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
            "V15-M54: package sealed V15-M53 twelve-hour evidence for bounded evaluation routing. "
            "Does not torch.load checkpoints, does not run benchmarks or promotion."
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
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m53-run-json", type=Path, default=None)
    parser.add_argument("--expected-m53-run-sha256", type=str, default=None)
    parser.add_argument("--raw-m53-file-sha256", type=str, default=None)
    parser.add_argument("--m53-checkpoint-inventory-json", type=Path, default=None)
    parser.add_argument("--m53-telemetry-summary-json", type=Path, default=None)
    parser.add_argument("--m53-transcript-path", type=Path, default=None)
    parser.add_argument("--phase-a-match-proof-json", type=Path, default=None)
    parser.add_argument("--expected-phase-a-proof-sha256", type=str, default=None)
    parser.add_argument("--final-candidate-checkpoint-path", type=Path, default=None)
    parser.add_argument("--expected-final-candidate-checkpoint-sha256", type=str, default=None)
    parser.add_argument(
        "--declared-readiness-json",
        type=Path,
        default=None,
        help="Operator-declared M54 envelope JSON (operator_declared profile).",
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m54_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m54_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        if args.declared_readiness_json is None:
            sys.stderr.write("error: operator_declared requires --declared-readiness-json\n")
            return 2
        try:
            emit_m54_operator_declared(out, declared_json=args.declared_readiness_json.resolve())
        except (OSError, ValueError) as exc:
            sys.stderr.write(f"error: operator_declared failed: {exc}\n")
            return 2
        return 0

    assert args.profile == PROFILE_OPERATOR_PREFLIGHT
    if args.m53_run_json is None:
        sys.stderr.write("error: operator_preflight requires --m53-run-json\n")
        return 2

    inputs = M54PreflightInputs(
        m53_run_json=args.m53_run_json.resolve(),
        expected_m53_run_sha256=args.expected_m53_run_sha256,
        raw_m53_file_sha256=args.raw_m53_file_sha256,
        m53_checkpoint_inventory_json=(
            args.m53_checkpoint_inventory_json.resolve()
            if args.m53_checkpoint_inventory_json
            else None
        ),
        m53_telemetry_summary_json=(
            args.m53_telemetry_summary_json.resolve() if args.m53_telemetry_summary_json else None
        ),
        m53_transcript_path=(
            args.m53_transcript_path.resolve() if args.m53_transcript_path else None
        ),
        phase_a_match_proof_json=(
            args.phase_a_match_proof_json.resolve() if args.phase_a_match_proof_json else None
        ),
        expected_phase_a_proof_sha256=args.expected_phase_a_proof_sha256,
        final_candidate_checkpoint_path=(
            args.final_candidate_checkpoint_path.resolve()
            if args.final_candidate_checkpoint_path
            else None
        ),
        expected_final_candidate_checkpoint_sha256=args.expected_final_candidate_checkpoint_sha256,
    )
    _sealed, _paths, ok_pack = emit_m54_operator_preflight_bundle(out, inputs=inputs)
    return 0 if ok_pack else 3


if __name__ == "__main__":
    raise SystemExit(main())
