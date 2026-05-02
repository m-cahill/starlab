"""CLI: V15-M55 bounded evaluation package preflight emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
    OperatorDeclaredInputs,
    build_fixture_preflight,
    build_operator_declared_preflight,
    build_operator_preflight_blocked,
    emit_forbidden_refusal,
    validate_sha256,
    write_preflight_artifacts,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    STATUS_READY,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M55: bounded evaluation package structural preflight for a "
            "later readout milestone. Does not execute evaluation, load checkpoints, "
            "run SC2, or GPU inference."
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
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--evaluation-package-id", type=str, default=None)
    parser.add_argument("--evaluation-package-sha256", type=str, default=None)
    parser.add_argument("--upstream-m54-package-id", type=str, default=None)
    parser.add_argument("--upstream-m54-package-sha256", type=str, default=None)
    parser.add_argument("--evaluation-package-manifest", type=Path, default=None)
    parser.add_argument("--candidate-identity", type=Path, default=None)
    parser.add_argument("--scorecard-readout-plan", type=Path, default=None)
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        body = build_fixture_preflight()
        write_preflight_artifacts(out, body_unsealed=body)
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        body = build_operator_preflight_blocked()
        write_preflight_artifacts(out, body_unsealed=body)
        return 3

    assert args.profile == PROFILE_OPERATOR_DECLARED
    missing = (
        args.evaluation_package_id is None
        or args.evaluation_package_sha256 is None
        or args.upstream_m54_package_id is None
        or args.upstream_m54_package_sha256 is None
        or args.evaluation_package_manifest is None
        or args.candidate_identity is None
        or args.scorecard_readout_plan is None
    )
    if missing:
        sys.stderr.write("error: operator_declared requires all package id/sha/path arguments\n")
        return 2

    for label, raw in (
        ("--evaluation-package-sha256", args.evaluation_package_sha256),
        ("--upstream-m54-package-sha256", args.upstream_m54_package_sha256),
    ):
        if validate_sha256(str(raw)) is None:
            sys.stderr.write(f"error: {label} must be 64 lowercase hex characters\n")
            return 2

    op = OperatorDeclaredInputs(
        evaluation_package_id=str(args.evaluation_package_id),
        evaluation_package_sha256=str(args.evaluation_package_sha256),
        upstream_m54_package_id=str(args.upstream_m54_package_id),
        upstream_m54_package_sha256=str(args.upstream_m54_package_sha256),
        evaluation_package_manifest=args.evaluation_package_manifest.resolve(),
        candidate_identity=args.candidate_identity.resolve(),
        scorecard_readout_plan=args.scorecard_readout_plan.resolve(),
    )
    try:
        body = build_operator_declared_preflight(op)
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"error: operator_declared failed: {exc}\n")
        return 2
    write_preflight_artifacts(out, body_unsealed=body)
    return 0 if body.get("preflight_status") == STATUS_READY else 3


if __name__ == "__main__":
    raise SystemExit(main())
