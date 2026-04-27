"""CLI: emit V15-M17 long GPU campaign evidence JSON, report, runbook, and checklist."""

# ruff: noqa: E501

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.long_gpu_campaign_evidence_io import emit_v15_long_gpu_campaign_evidence
from starlab.v15.long_gpu_campaign_evidence_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
    PROFILE_OPERATOR_PREFLIGHT,
    SEAL_KEY_ARTIFACT,
)

_SEAL = SEAL_KEY_ARTIFACT

_PROFILES = (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_PREFLIGHT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
)


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 M17 long GPU campaign evidence (fixture, preflight, declared, or local-guard path). "
            "Default is CI-safe. operator_preflight requires M16 JSON. operator_local_long_gpu_campaign "
            "requires triple guards + M16 JSON; does not run M08 training (delegation documented in artifact)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Output directory for JSON, report, runbook, checklist (and M08 receipt stub for operator_local).",
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci | operator_preflight | operator_declared | operator_local_long_gpu_campaign",
    )
    parser.add_argument(
        "--m16-short-gpu-environment-json",
        type=Path,
        default=None,
        help="M16 v15_short_gpu_environment_evidence.json (required for preflight and operator_local).",
    )
    parser.add_argument(
        "--operator-campaign-json",
        type=Path,
        default=None,
        help="Required for operator_declared: operator campaign metadata JSON (paths redacted).",
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required for operator_local_long_gpu_campaign (guard 1/3).",
    )
    parser.add_argument(
        "--authorize-long-gpu-campaign",
        action="store_true",
        help="Required for operator_local_long_gpu_campaign (guard 2/3).",
    )
    parser.add_argument(
        "--confirm-private-artifacts",
        action="store_true",
        help="Required for operator_local_long_gpu_campaign (guard 3/3).",
    )
    parser.add_argument(
        "--planned-wall-clock-hours",
        type=int,
        default=12,
        help="Planned hours recorded in preflight/guard path (default 12).",
    )
    args = parser.parse_args(argv)

    m16: Path | None = None
    if args.m16_short_gpu_environment_json is not None:
        m16 = _must_file(args.m16_short_gpu_environment_json, "--m16-short-gpu-environment-json")
    op_camp: Path | None = None
    if args.operator_campaign_json is not None:
        op_camp = _must_file(args.operator_campaign_json, "--operator-campaign-json")

    if args.profile == PROFILE_OPERATOR_DECLARED and op_camp is None:
        raise SystemExit(
            "error: --operator-campaign-json is required for --profile operator_declared"
        )

    if (
        args.profile in (PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN)
        and m16 is None
    ):
        raise SystemExit(
            f"error: --m16-short-gpu-environment-json is required for --profile {args.profile}"
        )
    if args.profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN and (
        not args.allow_operator_local_execution
        or not args.authorize_long_gpu_campaign
        or not args.confirm_private_artifacts
    ):
        raise SystemExit(
            "error: operator_local_long_gpu_campaign requires --allow-operator-local-execution, "
            "--authorize-long-gpu-campaign, and --confirm-private-artifacts"
        )

    sealed, _rep, p_j, p_r, p_b, p_c = emit_v15_long_gpu_campaign_evidence(
        args.output_dir,
        profile=args.profile,
        m16_path=m16,
        allow_operator_local_execution=args.allow_operator_local_execution,
        authorize_long_gpu_campaign=args.authorize_long_gpu_campaign,
        confirm_private_artifacts=args.confirm_private_artifacts,
        operator_campaign_path=op_camp,
        planned_wall_clock_hours=args.planned_wall_clock_hours,
    )
    print(f"wrote {p_j}", flush=True)
    print(f"wrote {p_r}", flush=True)
    print(f"wrote {p_b}", flush=True)
    print(f"wrote {p_c}", flush=True)
    if args.profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN:
        print(f"wrote {args.output_dir / 'v15_long_gpu_campaign_receipt.json'}", flush=True)
        print(f"wrote {args.output_dir / 'v15_long_gpu_campaign_receipt_report.json'}", flush=True)
    print(f"{_SEAL}={sealed.get(_SEAL, '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
