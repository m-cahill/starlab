"""CLI: V15-M53 twelve-hour operator run attempt (emitter: fixture + preflight only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m53_twelve_hour_operator_run_attempt_io import (
    emit_m53_fixture_ci,
    emit_m53_forbidden_refusal,
    emit_m53_operator_preflight_bundle,
    evaluate_m53_operator_preflight,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M53: sealed receipts for the governed 12-hour operator attempt. "
            "fixture_ci is CI-safe. operator_preflight validates M52 + inputs. "
            "Does not execute the 12-hour training run (use run_v15_m53)."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m52-launch-rehearsal-json", type=Path, default=None)
    parser.add_argument("--expected-m52-launch-rehearsal-sha256", type=str, default=None)
    parser.add_argument("--m52a-adapter-spike-json", type=Path, default=None)
    parser.add_argument("--expected-m52a-adapter-spike-sha256", type=str, default=None)
    parser.add_argument("--candidate-checkpoint-path", type=Path, default=None)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, default=None)
    parser.add_argument("--sc2-root", type=Path, default=None)
    parser.add_argument("--map-path", type=Path, default=None)
    parser.add_argument("--disk-root", type=Path, default=None)
    parser.add_argument("--max-retained-checkpoints", type=int, default=None)
    parser.add_argument("--estimated-checkpoint-mb", type=float, default=None)
    parser.add_argument(
        "--skip-disk-budget-strict",
        action="store_true",
        help="Do not require disk_root + estimates (tests / constrained hosts).",
    )
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()
    if bad:
        emit_m53_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m53_fixture_ci(out)
        return 0

    if args.m52_launch_rehearsal_json is None:
        sys.stderr.write("error: operator_preflight requires --m52-launch-rehearsal-json\n")
        return 2

    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=args.m52_launch_rehearsal_json,
        expected_m52_sha256=str(args.expected_m52_launch_rehearsal_sha256)
        if args.expected_m52_launch_rehearsal_sha256
        else None,
        m52a_adapter_spike_json=args.m52a_adapter_spike_json,
        expected_m52a_sha256=str(args.expected_m52a_adapter_spike_sha256)
        if args.expected_m52a_adapter_spike_sha256
        else None,
        candidate_checkpoint_path=args.candidate_checkpoint_path,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        sc2_root=args.sc2_root,
        map_path=args.map_path,
        disk_root=args.disk_root,
        estimated_checkpoint_mb=args.estimated_checkpoint_mb,
        max_retained_checkpoints=args.max_retained_checkpoints,
        skip_disk_strict=bool(args.skip_disk_budget_strict),
    )
    emit_m53_operator_preflight_bundle(
        out,
        pre=pre,
        profile_short=PROFILE_OPERATOR_PREFLIGHT,
    )
    return 0 if pre.ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
