"""CLI: V15-M41 two-hour run package & evaluation readiness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m41_two_hour_run_package_evaluation_readiness_io import (
    OperatorInputs,
    emit_m41_fixture,
    emit_m41_operator_preflight,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    ANCHOR_M39_RECEIPT_SHA256,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M41: package the completed V15-M39 two-hour operator run for future "
            "evaluation routing. Does not run benchmarks, load checkpoints, or promote."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit CI-safe fixture (no M39 bundle required)",
    )
    mode.add_argument(
        "--profile",
        choices=(PROFILE_OPERATOR_PREFLIGHT,),
        default=None,
        help="Operator mode (requires M39 paths and expected SHAs)",
    )
    parser.add_argument(
        "--m39-run-json",
        type=Path,
        default=None,
        help="Sealed v15_two_hour_operator_run_attempt.json",
    )
    parser.add_argument(
        "--m39-telemetry-summary-json",
        type=Path,
        default=None,
        help="v15_m39_telemetry_summary.json",
    )
    parser.add_argument(
        "--m39-checkpoint-inventory-json",
        type=Path,
        default=None,
        help="v15_m39_checkpoint_inventory.json",
    )
    parser.add_argument(
        "--m39-transcript",
        type=Path,
        default=None,
        help="v15_m39_operator_transcript.txt",
    )
    parser.add_argument(
        "--expected-m39-artifact-sha256",
        type=str,
        default=None,
        help=(
            "Canonical sealed M39 receipt digest (artifact_sha256). "
            f"Ledger anchor: {ANCHOR_M39_RECEIPT_SHA256}"
        ),
    )
    parser.add_argument(
        "--expected-final-candidate-sha256",
        type=str,
        default=None,
        help=(
            "Final candidate SHA-256 from the completed run (metadata only). "
            f"Ledger anchor: {ANCHOR_FINAL_CANDIDATE_SHA256}"
        ),
    )
    parser.add_argument(
        "--authorize-final-checkpoint-file-sha256",
        action="store_true",
        help="If set with --final-candidate-checkpoint-path, hash the file bytes (no torch.load).",
    )
    parser.add_argument(
        "--final-candidate-checkpoint-path",
        type=Path,
        default=None,
        help="Optional checkpoint file path (basename only recorded unless hash authorized).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M41 artifacts",
    )
    args = parser.parse_args(argv)
    out = args.output_dir.resolve()
    repo_root = Path(__file__).resolve().parents[2]

    if args.fixture_ci:
        emit_m41_fixture(out, repo_root=repo_root)
        return 0

    assert args.profile == PROFILE_OPERATOR_PREFLIGHT
    missing = []
    for label, p in (
        ("--m39-run-json", args.m39_run_json),
        ("--m39-telemetry-summary-json", args.m39_telemetry_summary_json),
        ("--m39-checkpoint-inventory-json", args.m39_checkpoint_inventory_json),
        ("--m39-transcript", args.m39_transcript),
        ("--expected-m39-artifact-sha256", args.expected_m39_artifact_sha256),
        ("--expected-final-candidate-sha256", args.expected_final_candidate_sha256),
    ):
        if p is None:
            missing.append(label)
    if missing:
        raise SystemExit(
            f"operator_preflight requires: {', '.join(missing)}",
        )

    emit_m41_operator_preflight(
        out,
        repo_root=repo_root,
        inputs=OperatorInputs(
            m39_run_json=Path(args.m39_run_json).resolve(),
            m39_telemetry_summary_json=Path(args.m39_telemetry_summary_json).resolve(),
            m39_checkpoint_inventory_json=Path(args.m39_checkpoint_inventory_json).resolve(),
            m39_transcript=Path(args.m39_transcript).resolve(),
            expected_m39_artifact_sha256=str(args.expected_m39_artifact_sha256).strip().lower(),
            expected_final_candidate_sha256=str(
                args.expected_final_candidate_sha256,
            )
            .strip()
            .lower(),
            authorize_final_checkpoint_file_sha256=bool(
                args.authorize_final_checkpoint_file_sha256,
            ),
            final_candidate_checkpoint_path=(
                Path(args.final_candidate_checkpoint_path).resolve()
                if args.final_candidate_checkpoint_path is not None
                else None
            ),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
