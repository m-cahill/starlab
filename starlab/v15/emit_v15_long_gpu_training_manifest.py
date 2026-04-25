"""CLI: emit V15-M08 long GPU training manifest + reports.

Does not start automatic long campaign execution.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from starlab.v15.long_gpu_training_manifest_io import (
    emit_v15_long_gpu_training_manifest_fixture,
    emit_v15_long_gpu_training_manifest_operator_declared,
    emit_v15_long_gpu_training_manifest_operator_preflight,
    validate_campaign_plan,
)
from starlab.v15.long_gpu_training_manifest_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)

_PROFILES = (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M08 long GPU training manifest (fixture_ci / operator_preflight / "
            "operator_declared). Does not run the long GPU campaign."
        ),
    )
    parser.add_argument(
        "--output-dir", required=True, type=Path, help="Directory for emitted JSON."
    )
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="fixture_ci (default) | operator_preflight | operator_declared",
    )
    parser.add_argument(
        "--campaign-plan-json", type=Path, default=None, help="Required for operator_preflight."
    )
    parser.add_argument(
        "--environment-lock-json",
        type=Path,
        default=None,
        help="M02 v15_long_gpu_environment_lock.json (operator_preflight).",
    )
    parser.add_argument(
        "--checkpoint-lineage-json",
        type=Path,
        default=None,
        help="M03 v15_checkpoint_lineage_manifest.json (operator_preflight).",
    )
    parser.add_argument(
        "--m07-training-run-receipt-json",
        type=Path,
        default=None,
        help="M07 v15_training_run_receipt.json (operator_preflight).",
    )
    parser.add_argument(
        "--training-config-json",
        type=Path,
        default=None,
        help="Training config JSON (operator_preflight).",
    )
    parser.add_argument(
        "--dataset-manifest-json",
        type=Path,
        default=None,
        help="Dataset manifest JSON (operator_preflight).",
    )
    parser.add_argument(
        "--rights-manifest-json",
        type=Path,
        default=None,
        help="Rights manifest JSON (operator_preflight).",
    )
    parser.add_argument(
        "--strong-agent-scorecard-json",
        type=Path,
        default=None,
        help="Optional M05 scorecard JSON (operator_preflight).",
    )
    parser.add_argument(
        "--xai-evidence-json",
        type=Path,
        default=None,
        help="Optional M04 XAI pack JSON (operator_preflight).",
    )
    parser.add_argument(
        "--human-panel-benchmark-json",
        type=Path,
        default=None,
        help="Optional M06 human panel protocol JSON (operator_preflight).",
    )
    parser.add_argument(
        "--manifest-json",
        type=Path,
        default=None,
        help="Declared manifest path (operator_declared).",
    )
    args = parser.parse_args(argv)

    out = args.output_dir
    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in (
            ("--campaign-plan-json", args.campaign_plan_json),
            ("--environment-lock-json", args.environment_lock_json),
            ("--manifest-json", args.manifest_json),
        ):
            if p is not None:
                print(f"warning: {label} ignored for fixture_ci", flush=True)
        emit_v15_long_gpu_training_manifest_fixture(out)
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        required = (
            ("--campaign-plan-json", args.campaign_plan_json),
            ("--environment-lock-json", args.environment_lock_json),
            ("--checkpoint-lineage-json", args.checkpoint_lineage_json),
            ("--m07-training-run-receipt-json", args.m07_training_run_receipt_json),
            ("--training-config-json", args.training_config_json),
            ("--dataset-manifest-json", args.dataset_manifest_json),
            ("--rights-manifest-json", args.rights_manifest_json),
        )
        for label, p in required:
            if p is None:
                print(f"error: {label} is required for operator_preflight", flush=True)
                return 2
            if not p.is_file():
                print(f"error: {label} not found: {p}", flush=True)
                return 2
        raw_plan = json.loads(args.campaign_plan_json.read_text(encoding="utf-8"))
        try:
            plan = validate_campaign_plan(raw_plan)
        except ValueError as e:
            print(f"error: invalid campaign plan: {e}", flush=True)
            return 2
        emit_v15_long_gpu_training_manifest_operator_preflight(
            out,
            campaign_plan=plan,
            environment_lock_path=args.environment_lock_json,
            checkpoint_lineage_path=args.checkpoint_lineage_json,
            m07_training_run_receipt_path=args.m07_training_run_receipt_json,
            training_config_path=args.training_config_json,
            dataset_manifest_path=args.dataset_manifest_json,
            rights_manifest_path=args.rights_manifest_json,
            strong_agent_scorecard_path=args.strong_agent_scorecard_json,
            xai_evidence_path=args.xai_evidence_json,
            human_panel_benchmark_path=args.human_panel_benchmark_json,
        )
        return 0

    if args.manifest_json is None or not args.manifest_json.is_file():
        print("error: --manifest-json required for operator_declared", flush=True)
        return 2
    emit_v15_long_gpu_training_manifest_operator_declared(out, args.manifest_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
