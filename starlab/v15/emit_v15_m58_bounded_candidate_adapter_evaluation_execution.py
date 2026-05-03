"""CLI: V15-M58 bounded candidate adapter evaluation execution attempt emitter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    validate_sha256 as validate_sha256_hex,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_io import (
    OperatorDeclaredExecutionInputs,
    OperatorPreflightExecutionInputs,
    build_fixture_execution,
    build_operator_declared_execution,
    build_operator_preflight_execution,
    emit_forbidden_refusal,
    execution_is_blocked_profile,
    write_execution_artifacts,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
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
            "V15-M58: emit bounded candidate adapter evaluation execution attempt artifacts. "
            "Does not run SC2 or invoke torch.load."
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
    parser.add_argument("--m57-charter-json", type=Path, default=None)
    parser.add_argument("--candidate-checkpoint", type=Path, default=None)
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    parser.add_argument("--sc2-root", type=Path, default=None)
    parser.add_argument("--map-path", type=Path, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--opponent-mode", type=str, default=None)
    parser.add_argument("--game-step", type=int, default=None)
    parser.add_argument("--max-game-steps", type=int, default=None)
    parser.add_argument("--declared-execution-json", type=Path, default=None)
    args = parser.parse_args(clean)

    out = args.output_dir.resolve()

    if bad:
        emit_forbidden_refusal(out, flags=list(bad))
        return 0

    if args.profile == PROFILE_FIXTURE_CI:
        write_execution_artifacts(out, body_unsealed=build_fixture_execution())
        return 0

    if args.profile == PROFILE_OPERATOR_PREFLIGHT:
        missing = args.m57_charter_json is None
        if missing:
            sys.stderr.write("error: operator_preflight requires --m57-charter-json\n")
            return 2
        if validate_sha256_hex(str(args.expected_candidate_sha256)) is None:
            sys.stderr.write("error: --expected-candidate-sha256 must be 64 lowercase hex\n")
            return 2
        body = build_operator_preflight_execution(
            OperatorPreflightExecutionInputs(
                m57_charter_json=args.m57_charter_json.resolve(),
                expected_candidate_sha256=str(args.expected_candidate_sha256),
                candidate_checkpoint=(
                    args.candidate_checkpoint.resolve() if args.candidate_checkpoint else None
                ),
                sc2_root=args.sc2_root.resolve() if args.sc2_root else None,
                map_path=args.map_path.resolve() if args.map_path else None,
                opponent_mode=args.opponent_mode,
                game_step=int(args.game_step) if args.game_step is not None else None,
                max_game_steps=int(args.max_game_steps)
                if args.max_game_steps is not None
                else None,
            ),
        )
        write_execution_artifacts(out, body_unsealed=body)
        return 3 if execution_is_blocked_profile(body) else 0

    assert args.profile == PROFILE_OPERATOR_DECLARED
    if (
        args.declared_execution_json is None
        or args.m57_charter_json is None
        or validate_sha256_hex(str(args.expected_candidate_sha256)) is None
    ):
        sys.stderr.write(
            "error: operator_declared requires --declared-execution-json, "
            "--m57-charter-json, valid --expected-candidate-sha256\n",
        )
        return 2
    body = build_operator_declared_execution(
        OperatorDeclaredExecutionInputs(
            declared_execution_json=args.declared_execution_json.resolve(),
            m57_charter_json=args.m57_charter_json.resolve(),
            expected_candidate_sha256=str(args.expected_candidate_sha256),
        ),
    )
    write_execution_artifacts(out, body_unsealed=body)
    return 3 if execution_is_blocked_profile(body) else 0


if __name__ == "__main__":
    raise SystemExit(main())
