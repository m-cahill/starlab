"""CLI: V15-M39 two-hour operator run attempt (fixture + operator preflight)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256
from starlab.v15.m39_two_hour_operator_run_attempt_io import (
    emit_m39_fixture,
    emit_m39_operator_preflight,
)


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M39: sealed receipt surface for the 7200s operator-local SC2-backed T1 run. "
            "CI fixture emits schema only. Operator preflight validates M38 + launch command."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Deterministic fixture artifacts (CI-safe; no operator inputs).",
    )
    mode.add_argument(
        "--profile",
        type=str,
        choices=("operator_preflight",),
        help="Operator-local profile.",
    )
    parser.add_argument(
        "--m38-launch-rehearsal-json",
        type=Path,
        default=None,
        help="Sealed V15-M38 v15_two_hour_run_remediation_launch_rehearsal.json",
    )
    parser.add_argument(
        "--m39-launch-command",
        type=Path,
        default=None,
        help="Frozen v15_m39_launch_command.txt from M38 bundle.",
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        help="Expected lineage candidate SHA-256 (default: public M34/M37 anchor).",
    )
    parser.add_argument(
        "--skip-cuda-sc2-probes",
        action="store_true",
        help="Skip torch CUDA + sc2 import probes (tests / constrained environments).",
    )
    parser.add_argument(
        "--min-free-disk-gb",
        type=float,
        default=1.0,
        help="Minimum free disk for preflight output root (default 1 GiB).",
    )
    parser.add_argument("--output-dir", type=Path, required=True)

    args = parser.parse_args(argv)
    out = args.output_dir.resolve()

    if args.fixture_ci:
        emit_m39_fixture(out, repo_root=repo_root)
        return 0

    if args.m38_launch_rehearsal_json is None or args.m39_launch_command is None:
        sys.stderr.write(
            "error: operator_preflight requires "
            "--m38-launch-rehearsal-json and --m39-launch-command\n",
        )
        return 2

    emit_m39_operator_preflight(
        out,
        repo_root=repo_root,
        m38_launch_rehearsal_json=args.m38_launch_rehearsal_json.resolve(),
        m39_launch_command=args.m39_launch_command.resolve(),
        expected_candidate_sha256=str(args.expected_candidate_sha256),
        skip_cuda_sc2=bool(args.skip_cuda_sc2_probes),
        min_free_disk_gb=float(args.min_free_disk_gb),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
