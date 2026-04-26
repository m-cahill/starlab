"""CLI: emit V15-M16 short GPU / environment evidence JSON + report + checklist."""

# ruff: noqa: E501

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.short_gpu_environment_io import emit_v15_short_gpu_environment_evidence
from starlab.v15.short_gpu_environment_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
    SEAL_KEY_ARTIFACT,
)

_SEAL = SEAL_KEY_ARTIFACT


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 short GPU / environment evidence JSON, report, and Markdown checklist (V15-M16). "
            "Default fixture mode is CI-safe (no torch import). Operator-local probe requires both "
            "--allow-operator-local-execution and --authorize-short-gpu-probe."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for evidence JSON, report JSON, and checklist Markdown",
    )
    parser.add_argument(
        "--profile",
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_DECLARED,
            PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
        ),
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default), operator_declared, or operator_local_short_gpu_probe",
    )
    parser.add_argument(
        "--operator-environment-json",
        type=Path,
        default=None,
        help="Required for operator_declared: operator environment metadata JSON (path-like strings redacted)",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required with operator_local_short_gpu_probe (dual guard 1/2)",
    )
    parser.add_argument(
        "--authorize-short-gpu-probe",
        action="store_true",
        help="Required with operator_local_short_gpu_probe (dual guard 2/2)",
    )
    parser.add_argument(
        "--device",
        choices=("cuda", "cpu"),
        default="cuda",
        help="Torch device for operator_local_short_gpu_probe (default cuda)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=5,
        help="Bounded probe steps for operator_local_short_gpu_probe (default 5)",
    )
    parser.add_argument(
        "--m02-environment-lock-json",
        type=Path,
        default=None,
        help="Optional: v15_long_gpu_environment_lock.json (starlab.v15.long_gpu_environment_lock.v1)",
    )
    parser.add_argument(
        "--m07-training-run-receipt-json",
        type=Path,
        default=None,
        help="Optional: v15_training_run_receipt.json (starlab.v15.training_run_receipt.v1)",
    )
    parser.add_argument(
        "--m08-long-gpu-manifest-json",
        type=Path,
        default=None,
        help="Optional: v15_long_gpu_training_manifest.json (starlab.v15.long_gpu_training_manifest.v1)",
    )
    parser.add_argument(
        "--m15-preflight-json",
        type=Path,
        default=None,
        help="Optional: v15_operator_evidence_collection_preflight.json (M15 honest closeout posture)",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_DECLARED and args.operator_environment_json is None:
        raise SystemExit(
            "error: --operator-environment-json is required for --profile operator_declared"
        )

    if args.profile == PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE:
        if not args.allow_operator_local_execution or not args.authorize_short_gpu_probe:
            raise SystemExit(
                "error: operator_local_short_gpu_probe requires both "
                "--allow-operator-local-execution and --authorize-short-gpu-probe"
            )

    m02 = (
        _must_file(args.m02_environment_lock_json, "--m02-environment-lock-json")
        if args.m02_environment_lock_json
        else None
    )
    m07 = (
        _must_file(args.m07_training_run_receipt_json, "--m07-training-run-receipt-json")
        if args.m07_training_run_receipt_json
        else None
    )
    m08 = (
        _must_file(args.m08_long_gpu_manifest_json, "--m08-long-gpu-manifest-json")
        if args.m08_long_gpu_manifest_json
        else None
    )
    m15 = (
        _must_file(args.m15_preflight_json, "--m15-preflight-json")
        if args.m15_preflight_json
        else None
    )
    op_env = (
        _must_file(args.operator_environment_json, "--operator-environment-json")
        if args.operator_environment_json
        else None
    )

    sealed, _rep, p_j, p_r, p_m = emit_v15_short_gpu_environment_evidence(
        args.output_dir,
        profile=args.profile,
        operator_environment_path=op_env,
        allow_operator_local_execution=args.allow_operator_local_execution,
        authorize_short_gpu_probe=args.authorize_short_gpu_probe,
        device=args.device,
        max_steps=args.max_steps,
        m02_path=m02,
        m07_path=m07,
        m08_path=m08,
        m15_path=m15,
    )
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_m}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
