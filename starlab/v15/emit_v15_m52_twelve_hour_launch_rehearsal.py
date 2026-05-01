"""CLI: V15-M52B twelve-hour launch rehearsal (no 12-hour execution)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m52_twelve_hour_launch_rehearsal_io import (
    emit_m52b_fixture_ci,
    emit_m52b_forbidden_refusal,
    emit_m52b_operator_declared,
    emit_m52b_operator_preflight,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
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
            "V15-M52B: twelve-hour blocker discovery / launch rehearsal. "
            "Freezes M53 launch command "
            "and support artifacts only. Does not execute the 12-hour run, benchmarks, strength "
            "evaluation, promotion, XAI, human-panel, showcase, or v2."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m52a-adapter-spike-json", type=Path, default=None)
    parser.add_argument("--expected-m52a-adapter-spike-sha256", type=str, default=None)
    parser.add_argument("--allow-m52a-adapter-blocked-planning", action="store_true")
    parser.add_argument("--m51-watchability-json", type=Path, default=None)
    parser.add_argument("--candidate-checkpoint-path", type=Path, default=None)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, default=None)
    parser.add_argument("--sc2-root", type=Path, default=None)
    parser.add_argument("--map-path", type=Path, default=None)
    parser.add_argument("--disk-root", type=Path, default=None)
    parser.add_argument("--estimated-checkpoint-mb", type=float, default=None)
    parser.add_argument("--max-retained-checkpoints", type=int, default=None)
    parser.add_argument("--declared-m52b-json", type=Path, default=None)
    parser.add_argument("--embedded-m52a-json", type=Path, default=None)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()
    if bad:
        emit_m52b_forbidden_refusal(out, profile_short=args.profile, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m52b_fixture_ci(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        if args.declared_m52b_json is None:
            print("--declared-m52b-json required for operator_declared", file=sys.stderr)
            return 2
        emit_m52b_operator_declared(
            out,
            declared_path=args.declared_m52b_json,
            embedded_m52a_path=args.embedded_m52a_json,
        )
        return 0

    if args.m52a_adapter_spike_json is None:
        print("--m52a-adapter-spike-json required for operator_preflight", file=sys.stderr)
        return 2

    emit_m52b_operator_preflight(
        out,
        m52a_path=args.m52a_adapter_spike_json,
        m52a_plain_override=None,
        expected_m52a_sha256=str(args.expected_m52a_adapter_spike_sha256).strip().lower()
        if args.expected_m52a_adapter_spike_sha256
        else None,
        profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        allow_m52a_blocked_planning=bool(args.allow_m52a_adapter_blocked_planning),
        m51_watchability_json=args.m51_watchability_json.resolve()
        if args.m51_watchability_json
        else None,
        sc2_root=args.sc2_root.resolve() if args.sc2_root else None,
        map_path=args.map_path.resolve() if args.map_path else None,
        candidate_checkpoint_path=args.candidate_checkpoint_path.resolve()
        if args.candidate_checkpoint_path
        else None,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        disk_root=args.disk_root.resolve() if args.disk_root else None,
        estimated_checkpoint_mb=args.estimated_checkpoint_mb,
        max_retained_checkpoints=args.max_retained_checkpoints,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
