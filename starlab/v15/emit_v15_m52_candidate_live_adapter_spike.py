"""CLI: V15-M52A candidate live adapter spike preflight (M51-bound; not benchmark)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m52_candidate_live_adapter_spike_io import (
    emit_m52a_fixture_ci,
    emit_m52a_forbidden_flag_refusal,
    emit_m52a_operator_declared,
    emit_m52a_operator_preflight,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
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
            "V15-M52A: governed candidate-to-live adapter spike preflight over sealed "
            "V15-M51 JSON. "
            "Fixture/preflight does not load checkpoints or run live SC2. Does not execute "
            "benchmarks, strength evaluation, promotion, 12-hour runs, v2, T2–T5, XAI, "
            "human-panel, or showcase."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED),
        help="fixture_ci | operator_preflight | operator_declared",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--m51-watchability-json",
        type=Path,
        default=None,
        help="Sealed v15_live_candidate_watchability_harness.json (V15-M51)",
    )
    parser.add_argument("--expected-m51-watchability-sha256", type=str, default=None)
    parser.add_argument("--m42-package-json", type=Path, default=None)
    parser.add_argument("--m41-package-json", type=Path, default=None)
    parser.add_argument("--m39-run-json", type=Path, default=None)
    parser.add_argument("--m33-cuda-probe-json", type=Path, default=None)
    parser.add_argument("--candidate-checkpoint-path", type=Path, default=None)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, default=None)
    parser.add_argument("--sc2-root", type=Path, default=None)
    parser.add_argument("--map-path", type=Path, default=None)
    parser.add_argument("--declared-m52a-json", type=Path, default=None)
    parser.add_argument("--embedded-m51-json", type=Path, default=None)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()
    if bad:
        emit_m52a_forbidden_flag_refusal(
            out,
            emit_profile_short=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m52a_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        if args.declared_m52a_json is None:
            print("--declared-m52a-json required for operator_declared", file=sys.stderr)
            return 2
        emit_m52a_operator_declared(
            out,
            declared_path=args.declared_m52a_json,
            embedded_m51_path=args.embedded_m51_json,
            sc2_root=args.sc2_root.resolve() if args.sc2_root else None,
            map_path=args.map_path.resolve() if args.map_path else None,
            checkpoint_path=args.candidate_checkpoint_path.resolve()
            if args.candidate_checkpoint_path
            else None,
            expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
            m39_run_json_path=args.m39_run_json.resolve() if args.m39_run_json else None,
        )
        return 0

    if args.m51_watchability_json is None:
        print("--m51-watchability-json required for operator_preflight", file=sys.stderr)
        return 2

    emit_m52a_operator_preflight(
        out,
        m51_path=args.m51_watchability_json,
        m51_plain_override=None,
        expected_m51_sha256_lower=str(args.expected_m51_watchability_sha256).strip().lower()
        if args.expected_m51_watchability_sha256
        else None,
        emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        sc2_root=args.sc2_root.resolve() if args.sc2_root else None,
        map_path=args.map_path.resolve() if args.map_path else None,
        checkpoint_path=args.candidate_checkpoint_path.resolve()
        if args.candidate_checkpoint_path
        else None,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        m39_run_json_path=args.m39_run_json.resolve() if args.m39_run_json else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
