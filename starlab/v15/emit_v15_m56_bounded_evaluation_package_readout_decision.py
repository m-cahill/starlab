"""CLI: V15-M56 bounded evaluation package readout / decision emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m56_bounded_evaluation_package_readout_decision_io import (
    OperatorDeclaredReadoutInputs,
    OperatorPreflightReadoutInputs,
    build_fixture_readout_decision,
    build_operator_declared_readout_decision,
    build_operator_preflight_readout_decision,
    validate_sha256,
    write_readout_artifacts,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
    DECISION_BLOCKED_CLAIM_FLAGS,
    DECISION_READY,
    FORBIDDEN_CLI_FLAGS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
)


def _readout_is_blocked(decision_status: str) -> bool:
    return decision_status != DECISION_READY


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M56: bounded evaluation package readout / decision over sealed "
            "V15-M55 preflight artifacts. Does not execute evaluation, load checkpoints, "
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
    parser.add_argument("--m55-preflight-json", type=Path, default=None)
    parser.add_argument("--m54-readiness-json", type=Path, default=None)
    parser.add_argument("--m56a-context-json", type=Path, default=None)
    parser.add_argument("--expected-m54-package-sha256", type=str, default=None)
    parser.add_argument("--expected-m53-run-artifact-sha256", type=str, default=None)
    parser.add_argument("--expected-candidate-sha256", type=str, default=None)
    parser.add_argument("--declared-readout-json", type=Path, default=None)
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        body = build_fixture_readout_decision()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        ro = body.get("readout")
        if isinstance(ro, dict):
            ro["decision_status"] = DECISION_BLOCKED_CLAIM_FLAGS
            ro["blocked_reasons"] = [f"forbidden_cli_flag:{','.join(bad)}"]
            ro["decision_reason"] = "forbidden_cli_flag"
        write_readout_artifacts(out, body_unsealed=body)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        body = build_fixture_readout_decision()
        write_readout_artifacts(out, body_unsealed=body)
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        missing = (
            args.m55_preflight_json is None
            or args.expected_m54_package_sha256 is None
            or args.expected_m53_run_artifact_sha256 is None
            or args.expected_candidate_sha256 is None
        )
        if missing:
            sys.stderr.write(
                "error: operator_preflight requires --m55-preflight-json and "
                "all --expected-*-sha256 arguments\n",
            )
            return 2
        for label, raw in (
            ("--expected-m54-package-sha256", args.expected_m54_package_sha256),
            ("--expected-m53-run-artifact-sha256", args.expected_m53_run_artifact_sha256),
            ("--expected-candidate-sha256", args.expected_candidate_sha256),
        ):
            if validate_sha256(str(raw)) is None:
                sys.stderr.write(
                    f"error: {label} must be 64 lowercase hex characters\n",
                )
                return 2
        try:
            body = build_operator_preflight_readout_decision(
                OperatorPreflightReadoutInputs(
                    m55_preflight_json=args.m55_preflight_json.resolve(),
                    expected_m54_package_sha256=str(args.expected_m54_package_sha256),
                    expected_m53_run_artifact_sha256=str(
                        args.expected_m53_run_artifact_sha256,
                    ),
                    expected_candidate_sha256=str(args.expected_candidate_sha256),
                    m54_readiness_json=(
                        args.m54_readiness_json.resolve()
                        if args.m54_readiness_json is not None
                        else None
                    ),
                    m56a_context_json=(
                        args.m56a_context_json.resolve()
                        if args.m56a_context_json is not None
                        else None
                    ),
                ),
            )
        except (OSError, ValueError) as exc:
            sys.stderr.write(f"error: operator_preflight failed: {exc}\n")
            return 2
        ds = ""
        ro = body.get("readout")
        if isinstance(ro, dict):
            ds = str(ro.get("decision_status") or "")
        write_readout_artifacts(out, body_unsealed=body)
        return 0 if not _readout_is_blocked(ds) else 3

    assert args.profile == PROFILE_OPERATOR_DECLARED
    if (
        args.declared_readout_json is None
        or args.m55_preflight_json is None
        or args.expected_candidate_sha256 is None
    ):
        sys.stderr.write(
            "error: operator_declared requires --declared-readout-json, "
            "--m55-preflight-json, --expected-candidate-sha256\n",
        )
        return 2
    if validate_sha256(str(args.expected_candidate_sha256)) is None:
        sys.stderr.write(
            "error: --expected-candidate-sha256 must be 64 lowercase hex characters\n",
        )
        return 2
    try:
        body = build_operator_declared_readout_decision(
            OperatorDeclaredReadoutInputs(
                declared_readout_json=args.declared_readout_json.resolve(),
                m55_preflight_json=args.m55_preflight_json.resolve(),
                expected_candidate_sha256=str(args.expected_candidate_sha256),
            ),
        )
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"error: operator_declared failed: {exc}\n")
        return 2
    ro = body.get("readout")
    ds = str(ro.get("decision_status") or "") if isinstance(ro, dict) else ""
    write_readout_artifacts(out, body_unsealed=body)
    return 0 if not _readout_is_blocked(ds) else 3


if __name__ == "__main__":
    raise SystemExit(main())
