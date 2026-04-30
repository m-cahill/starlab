"""CLI: V15-M43 bounded evaluation gate (consumes sealed M42 JSON — routing only)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m43_bounded_evaluation_gate_io import (
    emit_m43_disallowed_execution,
    emit_m43_fixture,
    emit_m43_operator,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M43: bounded evaluation gate over sealed V15-M42 package metadata. "
            "Does not execute benchmarks, load checkpoint blobs via PyTorch weight "
            "deserialization, or promote."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(
            PROFILE_FIXTURE_CI,
            PROFILE_OPERATOR_PREFLIGHT,
            PROFILE_OPERATOR_DECLARED,
        ),
        help=(
            "fixture_ci synthesizes deterministic inputs; operator profiles consume "
            "--m42-package-json"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for bounded evaluation gate artifacts",
    )
    parser.add_argument(
        "--m42-package-json",
        type=Path,
        default=None,
        help=(
            "Sealed M42 main JSON (typically "
            "v15_m42_two_hour_candidate_checkpoint_evaluation_package.json)"
        ),
    )
    parser.add_argument(
        "--benchmark-protocol-json",
        type=Path,
        default=None,
        help="Governed strong-agent benchmark protocol JSON (routing metadata)",
    )
    parser.add_argument(
        "--environment-manifest-json",
        type=Path,
        default=None,
        help="Sealed long GPU environment manifest JSON (routing metadata)",
    )
    parser.add_argument(
        "--operator-m42-logical-path",
        type=str,
        default=None,
        help=(
            "Optional logical label replacing raw OS path hints in emitted JSON "
            "(paths are redacted by default)."
        ),
    )
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_m43_disallowed_execution(
            out,
            profile=args.profile,
            triggered_flags=bad,
        )
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        emit_m43_fixture(out)
        return 0

    missing: list[str] = []
    if args.m42_package_json is None:
        missing.append("--m42-package-json")
    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if args.benchmark_protocol_json is None:
            missing.append("--benchmark-protocol-json")
        if args.environment_manifest_json is None:
            missing.append("--environment-manifest-json")
    if missing:
        parser.error(f"{args.profile} requires: {', '.join(missing)}")

    emit_m43_operator(
        out,
        profile=args.profile,
        m42_package_path=Path(args.m42_package_json),
        benchmark_protocol_path=args.benchmark_protocol_json,
        environment_manifest_path=args.environment_manifest_json,
        operator_logical_m42_hint=args.operator_m42_logical_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
