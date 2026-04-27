"""CLI: emit V15-M19 candidate checkpoint evaluation package + report + checklist."""

# ruff: noqa: E501

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.candidate_checkpoint_evaluation_package_io import (
    emit_operator_declared_package,
    emit_v15_candidate_checkpoint_evaluation_package,
)
from starlab.v15.candidate_checkpoint_evaluation_package_models import (
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 M19 candidate checkpoint evaluation package (JSON, report, checklist). "
            "Default fixture mode uses no input paths and is CI-safe. Does not read checkpoint blobs."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for package JSON, report JSON, and checklist Markdown",
    )
    parser.add_argument(
        "--profile",
        choices=(PROFILE_FIXTURE_DEFAULT, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED),
        default=PROFILE_FIXTURE_DEFAULT,
        help="fixture_default (default), operator_preflight, or operator_declared",
    )
    parser.add_argument(
        "--m18-readiness-json",
        type=Path,
        default=None,
        help="M18 v15_checkpoint_evaluation_readiness.json (operator_preflight)",
    )
    parser.add_argument(
        "--candidate-manifest",
        type=Path,
        default=None,
        help="M18 candidate checkpoint manifest (operator_preflight)",
    )
    parser.add_argument(
        "--campaign-receipt",
        type=Path,
        default=None,
        help="M08 v15_long_gpu_campaign_receipt.json (operator_preflight)",
    )
    parser.add_argument(
        "--checkpoint-lineage",
        type=Path,
        default=None,
        help="M03 v15_checkpoint_lineage_manifest.json (operator_preflight)",
    )
    parser.add_argument(
        "--environment-manifest",
        type=Path,
        default=None,
        help="M02 v15_long_gpu_environment_lock.json (operator_preflight)",
    )
    parser.add_argument(
        "--dataset-manifest",
        type=Path,
        default=None,
        help="Dataset manifest JSON (operator_preflight)",
    )
    parser.add_argument(
        "--evaluation-protocol-json",
        type=Path,
        default=None,
        help="M05 v15_strong_agent_scorecard.json (operator_preflight)",
    )
    parser.add_argument(
        "--package-json",
        type=Path,
        default=None,
        help="Pre-built M19 package JSON (operator_declared only; metadata-only normalize)",
    )
    args = parser.parse_args(argv)

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        for label, p in [
            ("--m18-readiness-json", args.m18_readiness_json),
            ("--candidate-manifest", args.candidate_manifest),
            ("--campaign-receipt", args.campaign_receipt),
            ("--checkpoint-lineage", args.checkpoint_lineage),
            ("--environment-manifest", args.environment_manifest),
            ("--dataset-manifest", args.dataset_manifest),
            ("--evaluation-protocol-json", args.evaluation_protocol_json),
        ]:
            if p is None:
                raise SystemExit(
                    f"error: {label} is required for profile {PROFILE_OPERATOR_PREFLIGHT!r}"
                )
        emit_v15_candidate_checkpoint_evaluation_package(
            args.output_dir,
            profile=PROFILE_OPERATOR_PREFLIGHT,
            m18_path=_must_file(args.m18_readiness_json, "--m18-readiness-json"),
            candidate_manifest_path=_must_file(args.candidate_manifest, "--candidate-manifest"),
            campaign_receipt_path=_must_file(args.campaign_receipt, "--campaign-receipt"),
            checkpoint_lineage_path=_must_file(args.checkpoint_lineage, "--checkpoint-lineage"),
            environment_manifest_path=_must_file(
                args.environment_manifest, "--environment-manifest"
            ),
            dataset_manifest_path=_must_file(args.dataset_manifest, "--dataset-manifest"),
            evaluation_protocol_path=_must_file(
                args.evaluation_protocol_json, "--evaluation-protocol-json"
            ),
        )
    elif args.profile == PROFILE_OPERATOR_DECLARED:
        if args.package_json is None:
            raise SystemExit(
                f"error: --package-json is required for profile {PROFILE_OPERATOR_DECLARED!r}"
            )
        emit_operator_declared_package(
            args.output_dir, package_json=_must_file(args.package_json, "--package-json")
        )
    else:
        emit_v15_candidate_checkpoint_evaluation_package(
            args.output_dir, profile=PROFILE_FIXTURE_DEFAULT
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
