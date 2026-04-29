"""CLI: V15-M36 smoke benchmark execution surface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
)
from starlab.v15.m36_smoke_benchmark_execution_io import (
    emit_m36_bounded_synthetic_smoke,
    emit_m36_fixture,
    emit_m36_operator_preflight,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "V15-M36: governed smoke benchmark execution bookkeeping over sealed M35 readiness "
            "JSON. Does not run live SC2, load checkpoints, or produce benchmark results."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--fixture-ci",
        action="store_true",
        help="Emit CI-safe fixture (no M35 file required)",
    )
    mode.add_argument(
        "--profile",
        type=str,
        choices=("operator_preflight", "operator_local_bounded_smoke"),
        help=(
            "operator_preflight: validate sealed M35 JSON; bounded_smoke requires "
            "authorization flags plus valid M35"
        ),
    )
    parser.add_argument(
        "--m35-readiness-json",
        type=Path,
        default=None,
        help="Path to sealed v15_candidate_checkpoint_smoke_benchmark_readiness.json (M35)",
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=None,
        help=(
            "Expected candidate checkpoint SHA-256 binding (default public record: "
            f"{EXPECTED_PUBLIC_CANDIDATE_SHA256})"
        ),
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Safety guard for bounded smoke mode only",
    )
    parser.add_argument(
        "--authorize-smoke-benchmark-execution",
        action="store_true",
        help="Authorization guard for bounded smoke mode only",
    )
    parser.add_argument(
        "--max-smoke-steps",
        type=int,
        default=1,
        help="Synthetic bounded bookkeeping cap (default 1; no wall-clock tier)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for M36 artifacts",
    )
    args = parser.parse_args(argv)
    out = args.output_dir.resolve()
    exp = args.expected_candidate_sha256
    if exp is not None:
        exp = str(exp).strip().lower()

    if args.fixture_ci:
        emit_m36_fixture(out)
        return 0

    if args.profile == "operator_preflight":
        m35_path = args.m35_readiness_json
        emit_m36_operator_preflight(
            out,
            m35_path=m35_path.resolve() if m35_path else None,
            expected_candidate_sha256=exp,
        )
        return 0

    if args.profile != "operator_local_bounded_smoke":
        raise SystemExit("--profile operator_local_bounded_smoke required for bounded path")

    if not args.allow_operator_local_execution or not args.authorize_smoke_benchmark_execution:
        raise SystemExit(
            "operator_local_bounded_smoke requires "
            "--allow-operator-local-execution and --authorize-smoke-benchmark-execution",
        )

    mp = args.m35_readiness_json
    if mp is None or not Path(mp).is_file():
        raise SystemExit(
            f"operator_local_bounded_smoke requires readable --m35-readiness-json: {mp!s}",
        )
    try:
        emit_m36_bounded_synthetic_smoke(
            out,
            m35_path=Path(mp).resolve(),
            expected_candidate_sha256=exp,
            max_smoke_steps=max(1, int(args.max_smoke_steps)),
        )
    except ValueError as e:
        raise SystemExit(str(e)) from e
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
