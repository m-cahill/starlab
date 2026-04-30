"""CLI: V15-M42 two-hour candidate checkpoint evaluation package assembly."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_io import (
    M42OperatorInputs,
    emit_m42_fixture,
    emit_m42_operator_preflight,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    ANCHOR_M39_RECEIPT_SHA256,
    PROFILE_OPERATOR_PREFLIGHT,
    SOURCE_CANDIDATE_LINEAGE_SHA256,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M42: assemble governed candidate checkpoint evaluation package from sealed "
            "M41 readiness JSON. Requires M41; does not run benchmarks, torch.load, or promotion."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit CI-safe fixture (no operator M41 package)",
    )
    mode.add_argument(
        "--profile",
        choices=(PROFILE_OPERATOR_PREFLIGHT,),
        default=None,
        help="Operator mode — requires sealed M41 JSON and ledger SHAs",
    )
    parser.add_argument(
        "--m41-package-json",
        type=Path,
        default=None,
        help=(
            "Sealed v15_two_hour_run_package_evaluation_readiness.json "
            "(required for operator_preflight)"
        ),
    )
    parser.add_argument(
        "--expected-m41-package-sha256",
        type=str,
        default=None,
        help="Optional: assert sealed M41 artifact_sha256 matches this digest",
    )
    parser.add_argument(
        "--expected-m39-artifact-sha256",
        type=str,
        default=None,
        help=(
            "Sealed M39 receipt digest binding (ledger anchor). "
            f"Canonical: {ANCHOR_M39_RECEIPT_SHA256}"
        ),
    )
    parser.add_argument(
        "--expected-source-candidate-sha256",
        type=str,
        default=None,
        help=(
            "Source lineage candidate SHA binding. "
            f"Ledger anchor: {SOURCE_CANDIDATE_LINEAGE_SHA256}"
        ),
    )
    parser.add_argument(
        "--expected-final-candidate-sha256",
        type=str,
        default=None,
        help=(
            f"Final two-hour candidate SHA binding. Ledger anchor: {ANCHOR_FINAL_CANDIDATE_SHA256}"
        ),
    )
    parser.add_argument(
        "--m39-run-json",
        type=Path,
        default=None,
        help="Optional cross-check — sealed M39 operator run receipt JSON",
    )
    parser.add_argument(
        "--m39-checkpoint-inventory-json",
        type=Path,
        default=None,
        help="Optional cross-check — M39 checkpoint inventory JSON",
    )
    parser.add_argument(
        "--m39-telemetry-summary-json",
        type=Path,
        default=None,
        help="Optional cross-check — M39 telemetry summary JSON",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="Optional M05 protocol JSON (binding only)",
    )
    parser.add_argument(
        "--authorize-final-checkpoint-file-sha256",
        action="store_true",
        help="With --final-candidate-checkpoint-path, hash checkpoint bytes only (no torch.load).",
    )
    parser.add_argument(
        "--final-candidate-checkpoint-path",
        type=Path,
        default=None,
        help="Optional checkpoint file — basename emitted unless hashing authorized.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M42 artifacts",
    )
    args = parser.parse_args(argv)
    out = args.output_dir.resolve()
    repo_root = Path(__file__).resolve().parents[2]

    if args.fixture_ci:
        emit_m42_fixture(out, repo_root=repo_root)
        return 0

    assert args.profile == PROFILE_OPERATOR_PREFLIGHT
    missing_labels: list[str] = []
    if args.m41_package_json is None:
        missing_labels.append("--m41-package-json")
    for label, val in (
        ("--expected-m39-artifact-sha256", args.expected_m39_artifact_sha256),
        ("--expected-source-candidate-sha256", args.expected_source_candidate_sha256),
        ("--expected-final-candidate-sha256", args.expected_final_candidate_sha256),
    ):
        if val is None:
            missing_labels.append(label)
    if missing_labels:
        raise SystemExit(
            f"operator_preflight requires: {', '.join(missing_labels)}",
        )

    m39_paths = (
        args.m39_run_json,
        args.m39_checkpoint_inventory_json,
        args.m39_telemetry_summary_json,
    )
    ancillary_m39_without_m41 = False
    m41_missing = args.m41_package_json is None or not Path(args.m41_package_json).is_file()
    if m41_missing and any(p is not None and Path(p).is_file() for p in m39_paths if p is not None):
        ancillary_m39_without_m41 = True

    emit_m42_operator_preflight(
        out,
        repo_root=repo_root,
        inputs=M42OperatorInputs(
            m41_package_json=Path(args.m41_package_json).resolve(),
            expected_m41_package_sha256=(
                str(args.expected_m41_package_sha256).strip().lower()
                if args.expected_m41_package_sha256 is not None
                else None
            ),
            expected_m39_artifact_sha256=str(args.expected_m39_artifact_sha256).strip().lower(),
            expected_source_candidate_sha256=str(
                args.expected_source_candidate_sha256,
            )
            .strip()
            .lower(),
            expected_final_candidate_sha256=str(
                args.expected_final_candidate_sha256,
            )
            .strip()
            .lower(),
            m39_run_json=Path(args.m39_run_json).resolve()
            if args.m39_run_json is not None
            else None,
            m39_checkpoint_inventory_json=(
                Path(args.m39_checkpoint_inventory_json).resolve()
                if args.m39_checkpoint_inventory_json is not None
                else None
            ),
            m39_telemetry_summary_json=(
                Path(args.m39_telemetry_summary_json).resolve()
                if args.m39_telemetry_summary_json is not None
                else None
            ),
            m05_scorecard_json=(
                Path(args.m05_scorecard_json).resolve()
                if args.m05_scorecard_json is not None
                else None
            ),
            authorize_final_checkpoint_file_sha256=bool(
                args.authorize_final_checkpoint_file_sha256,
            ),
            final_candidate_checkpoint_path=(
                Path(args.final_candidate_checkpoint_path).resolve()
                if args.final_candidate_checkpoint_path is not None
                else None
            ),
            ancillary_m39_present_without_m41=ancillary_m39_without_m41,
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
