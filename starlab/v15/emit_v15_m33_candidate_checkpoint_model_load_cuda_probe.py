"""CLI: V15-M33 candidate checkpoint model-load / CUDA inference probe."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io import (
    emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture,
    emit_m33_candidate_checkpoint_model_load_cuda_probe_operator,
    load_m32_evaluation_execution_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M33: SHA-verify a candidate checkpoint blob, load M28/M29-style weights, "
            "and run a minimal inference probe. Does not train or benchmark."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit schema-only fixture (no M32 file, no checkpoint, no torch CUDA requirement)",
    )
    mode.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required flag alongside authorization for operator-local probe",
    )

    parser.add_argument(
        "--authorize-candidate-model-load-probe",
        action="store_true",
        help="Second required guard for operator-local probe",
    )
    parser.add_argument(
        "--m32-evaluation-execution-json",
        type=Path,
        default=None,
        help="Sealed v15_candidate_checkpoint_evaluation_execution.json (M32)",
    )
    parser.add_argument(
        "--candidate-checkpoint-path",
        type=Path,
        default=None,
        help="Path to candidate .pt checkpoint blob",
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=None,
        help="SHA-256 of the checkpoint blob (must match M32 candidate + on-disk file)",
    )
    parser.add_argument(
        "--device",
        choices=("cuda", "cpu"),
        default="cuda",
        help="Inference device for operator-local probe (default cuda)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M33 artifacts",
    )

    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()

    if args.fixture_ci:
        emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture(output_dir)
        return 0

    if not args.allow_operator_local_execution or not args.authorize_candidate_model_load_probe:
        raise SystemExit(
            "operator-local mode requires both "
            "--allow-operator-local-execution and --authorize-candidate-model-load-probe",
        )

    m32_path = args.m32_evaluation_execution_json
    if m32_path is None or not Path(m32_path).is_file():
        raise SystemExit(
            "missing or unreadable --m32-evaluation-execution-json "
            f"(blocked_missing_m32_evaluation_execution_json): {m32_path!s}",
        )

    ck = args.candidate_checkpoint_path
    if ck is None:
        raise SystemExit(
            "operator-local mode requires --candidate-checkpoint-path "
            "(blocked_missing_candidate_checkpoint_path)",
        )

    exp = args.expected_candidate_sha256
    if not exp:
        raise SystemExit(
            "--expected-candidate-sha256 is required for operator-local mode "
            "(blocked_candidate_checkpoint_sha_missing)",
        )

    m32 = load_m32_evaluation_execution_json(Path(m32_path).resolve())
    emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        output_dir,
        m32=m32,
        candidate_checkpoint_path=Path(ck).resolve(),
        expected_candidate_sha256=str(exp).strip().lower(),
        device_requested=str(args.device),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
