"""CLI: V15-M57A operator live visual candidate watch session emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import validate_sha256
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_io import (
    DeclaredInputs,
    PreflightInputs,
    build_fixture_watch_session,
    build_operator_declared_watch_session,
    build_operator_preflight_watch_session,
    emit_forbidden_refusal,
    write_watch_session_artifacts,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
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
            "V15-M57A: emit governed operator live visual watch session artifacts. "
            "Does not run SC2 or load checkpoints unless validating a declared JSON envelope."
        ),
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=(PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT, PROFILE_OPERATOR_DECLARED),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--m56-readout-json", type=Path, default=None)
    parser.add_argument("--m55-preflight-json", type=Path, default=None)
    parser.add_argument("--m54-package-json", type=Path, default=None)
    parser.add_argument("--m53-run-json", type=Path, default=None)
    parser.add_argument("--m51-watchability-json", type=Path, default=None)
    parser.add_argument("--m52a-adapter-json", type=Path, default=None)
    parser.add_argument("--m56a-context-json", type=Path, default=None)
    parser.add_argument("--candidate-checkpoint", type=Path, default=None)
    parser.add_argument(
        "--expected-package-sha256",
        type=str,
        default=CANONICAL_M54_PACKAGE_SHA256,
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    parser.add_argument("--declared-watch-session-json", type=Path, default=None)
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        write_watch_session_artifacts(out, body_unsealed=build_fixture_watch_session())
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        write_watch_session_artifacts(
            out,
            body_unsealed=build_operator_preflight_watch_session(
                PreflightInputs(
                    m56_readout_json=args.m56_readout_json,
                    m55_preflight_json=args.m55_preflight_json,
                    m54_package_json=args.m54_package_json,
                    m53_run_json=args.m53_run_json,
                    m51_watchability_json=args.m51_watchability_json,
                    m52a_adapter_json=args.m52a_adapter_json,
                    m56a_context_json=args.m56a_context_json,
                    candidate_checkpoint=args.candidate_checkpoint,
                    expected_package_sha256=str(args.expected_package_sha256),
                    expected_candidate_sha256=str(args.expected_candidate_sha256),
                ),
            ),
        )
        return 0

    if args.declared_watch_session_json is None:
        sys.stderr.write("error: operator_declared requires --declared-watch-session-json\n")
        return 2
    exp = str(args.expected_candidate_sha256).strip().lower()
    if validate_sha256(exp) is None:
        sys.stderr.write("error: --expected-candidate-sha256 must be 64 lowercase hex chars\n")
        return 2
    if exp != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
        sys.stderr.write(
            "error: this milestone binds the canonical latest candidate SHA from V15-M53/M54.\n",
        )
        return 2
    write_watch_session_artifacts(
        out,
        body_unsealed=build_operator_declared_watch_session(
            DeclaredInputs(
                declared_path=args.declared_watch_session_json,
                expected_candidate_sha256=exp,
            ),
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
