"""CLI: emit V15-M18 checkpoint evaluation readiness / refusal JSON + report."""

# ruff: noqa: E501

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.checkpoint_evaluation_readiness_io import (
    emit_v15_checkpoint_evaluation_readiness,
    inventory_local_root,
    load_campaign_receipt_optional,
    load_candidate_manifest,
    load_checkpoint_lineage_optional,
)
from starlab.v15.checkpoint_evaluation_readiness_models import (
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_EXPLICIT_INPUTS,
)


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must be an existing file ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit v1.5 M18 checkpoint evaluation readiness / refusal artifacts. "
            "Default path is CI-safe (no candidate manifest). Does not scan out/ unless "
            "--local-inspection-root is set (inventory only)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for v15_checkpoint_evaluation_readiness.json and _report.json.",
    )
    parser.add_argument(
        "--candidate-manifest",
        type=Path,
        default=None,
        help="Optional candidate checkpoint manifest (starlab.v15.candidate_checkpoint_manifest.v1).",
    )
    parser.add_argument(
        "--campaign-receipt",
        type=Path,
        default=None,
        help="Optional M08 v15_long_gpu_campaign_receipt.json.",
    )
    parser.add_argument(
        "--checkpoint-lineage",
        type=Path,
        default=None,
        help="Optional M03 v15_checkpoint_lineage_manifest.json.",
    )
    parser.add_argument(
        "--local-inspection-root",
        type=Path,
        default=None,
        help="Optional operator-local root to inventory file extensions only (no default scan of out/).",
    )
    args = parser.parse_args(argv)

    inspection_checks: list[dict[str, object]] = []
    if args.local_inspection_root is not None:
        inspection_checks.extend(inventory_local_root(args.local_inspection_root))

    cand: dict[str, object] | None = None
    if args.candidate_manifest is not None:
        cand = load_candidate_manifest(_must_file(args.candidate_manifest, "--candidate-manifest"))

    receipt = load_campaign_receipt_optional(
        _must_file(args.campaign_receipt, "--campaign-receipt") if args.campaign_receipt else None
    )
    lineage = load_checkpoint_lineage_optional(
        _must_file(args.checkpoint_lineage, "--checkpoint-lineage")
        if args.checkpoint_lineage
        else None
    )

    profile = PROFILE_FIXTURE_DEFAULT
    if cand is not None or receipt is not None or lineage is not None:
        profile = PROFILE_OPERATOR_EXPLICIT_INPUTS

    emit_v15_checkpoint_evaluation_readiness(
        args.output_dir,
        profile=profile,
        candidate_manifest=cand,
        campaign_receipt=receipt,
        checkpoint_lineage=lineage,
        inspection_checks=inspection_checks,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
