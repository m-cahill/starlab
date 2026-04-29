"""CLI: V15-M35 candidate checkpoint smoke benchmark readiness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_io import (
    emit_m35_readiness_fixture,
    emit_m35_readiness_operator_preflight,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M35: readiness/refusal surface for routing an M33 CUDA-probed candidate into a "
            "future smoke benchmark execution path. Does not run benchmarks."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit CI-safe fixture (no M33 file required)",
    )
    mode.add_argument(
        "--m33-cuda-probe-json",
        type=Path,
        default=None,
        help="Sealed v15_candidate_checkpoint_model_load_cuda_probe.json (M33)",
    )
    parser.add_argument(
        "--m05-scorecard-json",
        type=Path,
        default=None,
        help="Optional M05 v15_strong_agent_scorecard.json (protocol binding only)",
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=None,
        help=(
            "Optional expected candidate SHA-256; must match M33 when supplied "
            f"(default public record: {EXPECTED_PUBLIC_CANDIDATE_SHA256})"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M35 artifacts",
    )
    args = parser.parse_args(argv)
    out = args.output_dir.resolve()
    exp = args.expected_candidate_sha256
    if exp is not None:
        exp = str(exp).strip().lower()

    if args.fixture_ci:
        emit_m35_readiness_fixture(out)
        return 0

    m33p = args.m33_cuda_probe_json
    if m33p is None or not Path(m33p).is_file():
        raise SystemExit(
            "operator_preflight requires readable --m33-cuda-probe-json "
            f"(smoke_benchmark_readiness_blocked_missing_m33_probe): {m33p!s}",
        )
    m05p = args.m05_scorecard_json
    emit_m35_readiness_operator_preflight(
        out,
        m33_path=Path(m33p).resolve(),
        expected_candidate_sha256=exp,
        m05_path=Path(m05p).resolve() if m05p is not None else None,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
