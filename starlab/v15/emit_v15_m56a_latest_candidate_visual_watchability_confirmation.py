"""CLI: V15-M56A latest candidate visual watchability confirmation emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    DeclaredInputs,
    PreflightInputs,
    build_fixture_confirmation,
    build_operator_declared_confirmation,
    build_operator_preflight_confirmation,
    emit_forbidden_refusal,
    validate_sha256,
    write_confirmation_artifacts,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    STATUS_BLOCKED_ADAPTER,
    STATUS_PREFLIGHT_BLOCKED,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M56A: governed latest-candidate visual watchability confirmation "
            "artifacts. Does not run SC2, load checkpoints, or execute benchmarks."
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
    parser.add_argument("--m55-preflight-json", type=Path, default=None)
    parser.add_argument("--m54-package-json", type=Path, default=None)
    parser.add_argument("--m53-run-json", type=Path, default=None)
    parser.add_argument("--expected-m54-package-sha256", type=str, default=None)
    parser.add_argument("--expected-candidate-sha256", type=str, default=None)
    parser.add_argument("--m51-watchability-json", type=Path, default=None)
    parser.add_argument("--m52a-adapter-spike-json", type=Path, default=None)
    parser.add_argument("--watchability-evidence-json", type=Path, default=None)
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        write_confirmation_artifacts(out, body_unsealed=build_fixture_confirmation())
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        if (
            args.m55_preflight_json is None
            or args.m54_package_json is None
            or args.m53_run_json is None
            or args.expected_m54_package_sha256 is None
            or args.expected_candidate_sha256 is None
        ):
            sys.stderr.write(
                "error: operator_preflight requires "
                "--m55-preflight-json, --m54-package-json, --m53-run-json, "
                "--expected-m54-package-sha256, --expected-candidate-sha256\n",
            )
            return 2
        if (
            validate_sha256(str(args.expected_m54_package_sha256)) is None
            or validate_sha256(str(args.expected_candidate_sha256)) is None
        ):
            sys.stderr.write("error: expected SHA-256 args must be 64 lowercase hex chars\n")
            return 2
        if (
            str(args.expected_m54_package_sha256).strip().lower() != CANONICAL_M54_PACKAGE_SHA256
            or str(args.expected_candidate_sha256).strip().lower()
            != CANONICAL_CANDIDATE_CHECKPOINT_SHA256
        ):
            sys.stderr.write(
                "error: this milestone binds canonical M54 package and latest candidate SHA "
                "from V15-M53/V15-M54; declared expectations must match those anchors.\n",
            )
            return 2
        body = build_operator_preflight_confirmation(
            PreflightInputs(
                m55_preflight_json=args.m55_preflight_json.resolve(),
                m54_package_json=args.m54_package_json.resolve(),
                m53_run_json=args.m53_run_json.resolve(),
                expected_m54_package_sha256=str(args.expected_m54_package_sha256),
                expected_candidate_sha256=str(args.expected_candidate_sha256),
                m51_watchability_json=args.m51_watchability_json.resolve()
                if args.m51_watchability_json is not None
                else None,
                m52a_adapter_spike_json=args.m52a_adapter_spike_json.resolve()
                if args.m52a_adapter_spike_json is not None
                else None,
            ),
        )
        write_confirmation_artifacts(out, body_unsealed=body)
        wp = body.get("watchability_profile") or {}
        st = str(wp.get("visual_confirmation_status") or "")
        if st == STATUS_PREFLIGHT_BLOCKED or st == STATUS_BLOCKED_ADAPTER:
            return 3
        return 0

    assert args.profile == PROFILE_OPERATOR_DECLARED
    if (
        args.watchability_evidence_json is None
        or args.m55_preflight_json is None
        or args.expected_candidate_sha256 is None
    ):
        sys.stderr.write(
            "error: operator_declared requires --watchability-evidence-json, "
            "--m55-preflight-json, --expected-candidate-sha256\n",
        )
        return 2
    if validate_sha256(str(args.expected_candidate_sha256)) is None:
        sys.stderr.write("error: --expected-candidate-sha256 must be 64 lowercase hex chars\n")
        return 2
    if str(args.expected_candidate_sha256).strip().lower() != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        sys.stderr.write(
            "error: --expected-candidate-sha256 must match the canonical latest candidate "
            f"SHA ({CANONICAL_CANDIDATE_CHECKPOINT_SHA256}).\n",
        )
        return 2
    body = build_operator_declared_confirmation(
        DeclaredInputs(
            watchability_evidence_json=args.watchability_evidence_json.resolve(),
            m55_preflight_json=args.m55_preflight_json.resolve(),
            expected_candidate_sha256=str(args.expected_candidate_sha256),
        ),
    )
    write_confirmation_artifacts(out, body_unsealed=body)
    wp = body.get("watchability_profile") or {}
    st = str(wp.get("visual_confirmation_status") or "")
    if st == STATUS_PREFLIGHT_BLOCKED or st == STATUS_BLOCKED_ADAPTER:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
