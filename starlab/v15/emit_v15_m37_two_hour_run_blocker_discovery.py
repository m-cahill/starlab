"""CLI: V15-M37 two-hour run blocker discovery / operator readiness audit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m37_two_hour_run_blocker_discovery_io import (
    emit_m37_fixture,
    emit_m37_operator_audit,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M37: blocker discovery / readiness audit for a future V15-M39 7200s operator run. "
            "Does not execute training, SC2 matches, checkpoint loads, benchmark scoring, "
            "or promotion."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit deterministic fixture artifacts (schema-only; no operator audit).",
    )
    mode.add_argument(
        "--profile",
        type=str,
        choices=("operator_audit",),
        help="Operator-local readiness audit profile.",
    )
    parser.add_argument(
        "--allow-operator-local-inspection",
        action="store_true",
        help="Allow git/env/CUDA/sc2/nvidia-smi probes against this checkout.",
    )
    parser.add_argument(
        "--authorize-checkpoint-file-sha256",
        action="store_true",
        help="Allow hashing local candidate .pt path for SHA verification (large blob IO).",
    )
    parser.add_argument(
        "--candidate-checkpoint-path",
        type=Path,
        default=None,
        help="Optional operator-local candidate checkpoint path (.pt). Never loads weights.",
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=None,
        help=(
            "Expected candidate checkpoint SHA256 binding "
            f"(default public lineage record {EXPECTED_PUBLIC_CANDIDATE_SHA256})."
        ),
    )
    parser.add_argument("--m27-rollout-json", type=Path, default=None)
    parser.add_argument("--m28-training-json", type=Path, default=None)
    parser.add_argument("--m29-full-run-json", type=Path, default=None)
    parser.add_argument("--m34-cuda-probe-json", type=Path, default=None)
    parser.add_argument("--m35-readiness-json", type=Path, default=None)
    parser.add_argument("--m36-smoke-execution-json", type=Path, default=None)
    parser.add_argument(
        "--target-wall-clock-seconds",
        type=float,
        default=7200.0,
        help="Target M39 wall-clock horizon used for extrapolation (default 7200).",
    )
    parser.add_argument(
        "--min-free-disk-gb",
        type=float,
        default=100.0,
        help="Minimum required free disk (GiB) when operator inspection is enabled.",
    )
    parser.add_argument("--output-dir", type=Path, required=True)

    args = parser.parse_args(argv)
    out = args.output_dir.resolve()

    if args.fixture_ci:
        emit_m37_fixture(out)
        return 0

    if args.profile != "operator_audit":
        sys.stderr.write("error: expected --profile operator_audit\n")
        return 2

    emit_m37_operator_audit(
        out,
        repo_root=repo_root,
        allow_operator_local_inspection=bool(args.allow_operator_local_inspection),
        candidate_checkpoint_path=args.candidate_checkpoint_path,
        expected_candidate_sha256=args.expected_candidate_sha256,
        authorize_checkpoint_file_sha256=bool(args.authorize_checkpoint_file_sha256),
        m27_rollout_json=args.m27_rollout_json,
        m28_training_json=args.m28_training_json,
        m29_full_run_json=args.m29_full_run_json,
        m34_cuda_probe_json=args.m34_cuda_probe_json,
        m35_readiness_json=args.m35_readiness_json,
        m36_smoke_execution_json=args.m36_smoke_execution_json,
        target_wall_clock_seconds=float(args.target_wall_clock_seconds),
        min_free_disk_gb=float(args.min_free_disk_gb),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
