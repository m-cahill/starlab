"""CLI: V15-M57 governed evaluation execution charter / dry-run gate emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    validate_sha256 as validate_sha256_hex,
)
from starlab.v15.m57_governed_evaluation_execution_charter_io import (
    OperatorDeclaredCharterInputs,
    OperatorPreflightCharterInputs,
    build_fixture_charter,
    build_operator_declared_charter,
    build_operator_preflight_charter,
    charter_is_blocked,
    emit_forbidden_refusal,
    write_charter_artifacts,
)
from starlab.v15.m57_governed_evaluation_execution_charter_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
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
            "V15-M57: emit governed evaluation execution charter / dry-run gate. "
            "Does not execute evaluation, run SC2, invoke torch.load, or load checkpoints."
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
    parser.add_argument("--m56-readout-json", type=Path, default=None)
    parser.add_argument("--m57a-watch-session-json", type=Path, default=None)
    parser.add_argument("--m52a-adapter-json", type=Path, default=None)
    parser.add_argument("--match-execution-proof-json", type=Path, default=None)
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    parser.add_argument("--declared-charter-json", type=Path, default=None)
    args = parser.parse_args(clean)
    out = args.output_dir.resolve()

    if bad:
        emit_forbidden_refusal(out, flags=bad)
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        write_charter_artifacts(out, body_unsealed=build_fixture_charter())
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        missing = args.m57a_watch_session_json is None or args.m52a_adapter_json is None
        if missing:
            sys.stderr.write(
                "error: operator_preflight requires --m57a-watch-session-json "
                "and --m52a-adapter-json\n",
            )
            return 2
        exp = validate_sha256_hex(str(args.expected_candidate_sha256))
        if exp is None:
            sys.stderr.write(
                "error: --expected-candidate-sha256 must be 64 lowercase hex\n",
            )
            return 2
        body = build_operator_preflight_charter(
            OperatorPreflightCharterInputs(
                m57a_watch_session_json=args.m57a_watch_session_json.resolve(),
                m52a_adapter_json=args.m52a_adapter_json.resolve(),
                expected_candidate_sha256=str(args.expected_candidate_sha256),
                m56_readout_json=(
                    args.m56_readout_json.resolve() if args.m56_readout_json is not None else None
                ),
                match_execution_proof_json=(
                    args.match_execution_proof_json.resolve()
                    if args.match_execution_proof_json is not None
                    else None
                ),
            ),
        )
        write_charter_artifacts(out, body_unsealed=body)
        return 3 if charter_is_blocked(body) else 0

    assert args.profile == PROFILE_OPERATOR_DECLARED
    if (
        args.declared_charter_json is None
        or args.m57a_watch_session_json is None
        or validate_sha256_hex(str(args.expected_candidate_sha256)) is None
    ):
        sys.stderr.write(
            "error: operator_declared requires --declared-charter-json, "
            "--m57a-watch-session-json, and valid --expected-candidate-sha256\n",
        )
        return 2
    body = build_operator_declared_charter(
        OperatorDeclaredCharterInputs(
            declared_charter_json=args.declared_charter_json.resolve(),
            m57a_watch_session_json=args.m57a_watch_session_json.resolve(),
            expected_candidate_sha256=str(args.expected_candidate_sha256),
        ),
    )
    write_charter_artifacts(out, body_unsealed=body)
    return 3 if charter_is_blocked(body) else 0


if __name__ == "__main__":
    raise SystemExit(main())
