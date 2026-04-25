"""CLI: emit V15-M09 checkpoint evaluation + report (fixture and operator profiles)."""

from __future__ import annotations

import argparse
from pathlib import Path

from starlab.v15.checkpoint_evaluation_io import (
    emit_v15_checkpoint_evaluation_fixture,
    emit_v15_checkpoint_evaluation_operator_declared,
    emit_v15_checkpoint_evaluation_operator_local_evaluation,
    emit_v15_checkpoint_evaluation_operator_preflight,
)
from starlab.v15.checkpoint_evaluation_models import (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_EVALUATION,
    PROFILE_OPERATOR_PREFLIGHT,
)

_PROFILES = (
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_PREFLIGHT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_EVALUATION,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit V15-M09 checkpoint evaluation (fixture_ci, operator_preflight, "
            "operator_declared, operator_local_evaluation dry-run). "
            "Does not load checkpoint blobs in CI or default preflight."
        ),
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory for JSON.")
    parser.add_argument(
        "--profile",
        choices=_PROFILES,
        default=PROFILE_FIXTURE_CI,
        help="Emission profile (default fixture_ci).",
    )
    parser.add_argument(
        "--m08-training-manifest-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--m08-campaign-receipt-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--checkpoint-lineage-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--candidate-checkpoint-metadata-json",
        type=Path,
        default=None,
        help="(preflight / local eval)",
    )
    parser.add_argument(
        "--environment-lock-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--training-config-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--dataset-manifest-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--rights-manifest-json", type=Path, default=None, help="(preflight / local eval)"
    )
    parser.add_argument(
        "--strong-agent-scorecard-json", type=Path, default=None, help="(optional; preflight)"
    )
    parser.add_argument(
        "--xai-evidence-json", type=Path, default=None, help="(optional; preflight)"
    )
    parser.add_argument(
        "--human-panel-benchmark-json", type=Path, default=None, help="(optional; preflight)"
    )
    parser.add_argument(
        "--evaluation-json", type=Path, default=None, help="(operator_declared) input to normalize"
    )
    parser.add_argument(
        "--allow-operator-local-evaluation",
        action="store_true",
        help="(operator_local_evaluation) first guard",
    )
    parser.add_argument(
        "--authorize-checkpoint-evaluation",
        action="store_true",
        help="(operator_local_evaluation) second guard; still dry-run only in M09",
    )
    args = parser.parse_args(argv)
    out = args.output_dir

    if args.profile == PROFILE_FIXTURE_CI:
        for label, p in (
            ("--m08-training-manifest-json", args.m08_training_manifest_json),
            ("--evaluation-json", args.evaluation_json),
        ):
            if p is not None:
                print(f"warning: {label} ignored for fixture_ci", flush=True)
        emit_v15_checkpoint_evaluation_fixture(out)
        return 0

    if args.profile == PROFILE_OPERATOR_DECLARED:
        if args.evaluation_json is None or not args.evaluation_json.is_file():
            print("error: --evaluation-json required for operator_declared", flush=True)
            return 2
        for label, p in (
            ("--m08-training-manifest-json", args.m08_training_manifest_json),
            ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
        ):
            if p is not None:
                print(f"warning: {label} ignored for operator_declared", flush=True)
        _s, _r, _c, _r2, rc = emit_v15_checkpoint_evaluation_operator_declared(
            out, args.evaluation_json
        )
        print(f"redaction_count={rc}", flush=True)
        return 0

    if args.profile == PROFILE_OPERATOR_LOCAL_EVALUATION:
        if not args.allow_operator_local_evaluation or not args.authorize_checkpoint_evaluation:
            print(
                "error: --allow-operator-local-evaluation and --authorize-checkpoint-evaluation "
                "required for operator_local_evaluation",
                flush=True,
            )
            return 2
    required = (
        ("--m08-training-manifest-json", args.m08_training_manifest_json),
        ("--m08-campaign-receipt-json", args.m08_campaign_receipt_json),
        ("--checkpoint-lineage-json", args.checkpoint_lineage_json),
        ("--candidate-checkpoint-metadata-json", args.candidate_checkpoint_metadata_json),
        ("--environment-lock-json", args.environment_lock_json),
        ("--training-config-json", args.training_config_json),
        ("--dataset-manifest-json", args.dataset_manifest_json),
        ("--rights-manifest-json", args.rights_manifest_json),
    )
    for label, p in required:
        if p is None:
            print(f"error: {label} is required for {args.profile}", flush=True)
            return 2
        if not p.is_file():
            print(f"error: {label} not found: {p}", flush=True)
            return 2

    preflight_params = {
        "m08_training_manifest": args.m08_training_manifest_json,
        "m08_campaign_receipt": args.m08_campaign_receipt_json,
        "checkpoint_lineage": args.checkpoint_lineage_json,
        "candidate_checkpoint_metadata": args.candidate_checkpoint_metadata_json,
        "environment_lock": args.environment_lock_json,
        "training_config": args.training_config_json,
        "dataset_manifest": args.dataset_manifest_json,
        "rights_manifest": args.rights_manifest_json,
        "strong_agent_scorecard": args.strong_agent_scorecard_json,
        "xai_evidence": args.xai_evidence_json,
        "human_panel_benchmark": args.human_panel_benchmark_json,
    }

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        emit_v15_checkpoint_evaluation_operator_preflight(out, **preflight_params)
    else:
        emit_v15_checkpoint_evaluation_operator_local_evaluation(out, **preflight_params)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
