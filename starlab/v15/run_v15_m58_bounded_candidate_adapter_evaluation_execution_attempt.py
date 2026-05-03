"""CLI: V15-M58 bounded candidate adapter evaluation execution attempt (operator-local)."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, cast

from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    validate_sha256 as validate_sha256_hex,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_io import (
    OperatorPreflightExecutionInputs,
    apply_completed_attempts_to_body,
    build_blocked_execution_body,
    build_m52a_delegate_argv,
    build_operator_preflight_execution,
    execution_is_blocked_profile,
    load_m57_charter,
    normalize_opponent_mode,
    parse_m52a_delegate_receipts,
    validate_attempt_bounds,
    validate_candidate_checkpoint_sha,
    validate_execution_claim_flags,
    write_execution_artifacts,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
    BLOCKED_ATTEMPT_COUNT,
    BLOCKED_CANDIDATE_IDENTITY_MISMATCH,
    BLOCKED_CLAIM_FLAGS_VIOLATION,
    BLOCKED_DUAL_GUARD_MISSING,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_BOUNDED_EVAL,
    OPERATOR_TRANSCRIPT_FILENAME,
    RUNNER_MODULE,
    STATUS_EXECUTION_BLOCKED,
    STATUS_EXECUTION_COMPLETED,
)


def _strip_guards_and_forbidden(argv_list: list[str]) -> tuple[bool, bool, list[str]]:
    forbid = frozenset(FORBIDDEN_CLI_FLAGS)
    guards = frozenset({GUARD_ALLOW_OPERATOR_LOCAL, GUARD_AUTHORIZE_BOUNDED_EVAL})
    allow_ok = GUARD_ALLOW_OPERATOR_LOCAL in argv_list
    auth_ok = GUARD_AUTHORIZE_BOUNDED_EVAL in argv_list
    clean = [a for a in argv_list if a not in forbid and a not in guards]
    return allow_ok, auth_ok, clean


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    allow_ok, auth_ok, clean = _strip_guards_and_forbidden(argv_list)

    parser = argparse.ArgumentParser(
        description=(
            "V15-M58: bounded candidate adapter evaluation-smoke execution via subprocess "
            "delegation to the M52A candidate-live adapter runner. Requires dual guards."
        ),
    )
    parser.add_argument("--m57-charter-json", type=Path, required=True)
    parser.add_argument("--m51-watchability-json", type=Path, required=True)
    parser.add_argument("--candidate-checkpoint", type=Path, required=True)
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    )
    parser.add_argument("--expected-m51-watchability-sha256", type=str, default=None)
    parser.add_argument("--sc2-root", type=Path, required=True)
    parser.add_argument("--map-path", type=Path, required=True)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=2048)
    parser.add_argument("--opponent-mode", type=str, default=None)
    parser.add_argument("--attempt-count", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--save-replay", action="store_true")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(clean)

    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    transcript_p = out / OPERATOR_TRANSCRIPT_FILENAME

    if bad:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body(
                [f"forbidden_cli_flag:{','.join(sorted(bad))}"],
                charter=None,
            ),
        )
        return 0

    if not allow_ok or not auth_ok:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body([BLOCKED_DUAL_GUARD_MISSING], charter=None),
        )
        return 3

    cand_exp_raw = validate_sha256_hex(str(args.expected_candidate_sha256))
    if cand_exp_raw is None:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body(
                [BLOCKED_CANDIDATE_IDENTITY_MISMATCH],
                charter=None,
            ),
        )
        return 3

    ch, errs = load_m57_charter(args.m57_charter_json.resolve())
    if ch is None:
        write_execution_artifacts(
            out, body_unsealed=build_blocked_execution_body(errs, charter=None)
        )
        return 3
    if errs:
        write_execution_artifacts(out, body_unsealed=build_blocked_execution_body(errs, charter=ch))
        return 3

    opp = normalize_opponent_mode(args.opponent_mode)
    if opp is None:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body(["blocked_disallowed_baseline"], charter=ch),
        )
        return 3

    if not validate_attempt_bounds(int(args.attempt_count)):
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body([BLOCKED_ATTEMPT_COUNT], charter=ch),
        )
        return 3

    if int(args.game_step) != 8 or int(args.max_game_steps) != 2048:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body(["blocked_disallowed_horizon"], charter=ch),
        )
        return 3

    pre = build_operator_preflight_execution(
        OperatorPreflightExecutionInputs(
            m57_charter_json=args.m57_charter_json.resolve(),
            expected_candidate_sha256=cand_exp_raw,
            candidate_checkpoint=None,
            sc2_root=args.sc2_root.resolve(),
            map_path=args.map_path.resolve(),
            opponent_mode=args.opponent_mode,
            game_step=int(args.game_step),
            max_game_steps=int(args.max_game_steps),
        ),
    )
    if execution_is_blocked_profile(pre):
        write_execution_artifacts(out, body_unsealed=pre)
        return 3

    c_err = validate_candidate_checkpoint_sha(
        args.candidate_checkpoint.resolve(),
        expected_lower=cand_exp_raw,
    )
    if c_err:
        write_execution_artifacts(
            out, body_unsealed=build_blocked_execution_body(c_err, charter=ch)
        )
        return 3

    if not args.save_replay:
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body(["blocked_replay_not_saved"], charter=ch),
        )
        return 3

    if validate_execution_claim_flags(pre):
        write_execution_artifacts(
            out,
            body_unsealed=build_blocked_execution_body([BLOCKED_CLAIM_FLAGS_VIOLATION], charter=ch),
        )
        return 3

    attempts: list[dict[str, Any]] = []
    durations: list[float] = []
    warnings: list[str] = []

    attempt_n = int(args.attempt_count)
    transcript_p.write_text(
        f"V15-M58 subprocess delegate transcript module={RUNNER_MODULE}\n\n",
        encoding="utf-8",
    )

    for idx in range(1, attempt_n + 1):
        delegate_out = out / f"m52a_delegate_attempt_{idx}"
        delegate_out.mkdir(parents=True, exist_ok=True)
        m51_optional = (
            validate_sha256_hex(str(args.expected_m51_watchability_sha256))
            if args.expected_m51_watchability_sha256
            else None
        )
        cmd = build_m52a_delegate_argv(
            python_executable=sys.executable,
            m51_json=args.m51_watchability_json.resolve(),
            delegate_output_dir=delegate_out.resolve(),
            ck_path=args.candidate_checkpoint.resolve(),
            expected_ck_sha=cand_exp_raw,
            sc2_root=args.sc2_root.resolve(),
            map_path=args.map_path.resolve(),
            device=str(args.device),
            game_step=int(args.game_step),
            max_game_steps=int(args.max_game_steps),
            save_replay=True,
            seed=int(args.seed) + idx,
            expected_m51_sha256=m51_optional,
        )
        started = time.monotonic()
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        durations.append(time.monotonic() - started)
        prev = transcript_p.read_text(encoding="utf-8", errors="replace")
        transcript_bits = (
            f"\n--- attempt {idx} ---\ncmd: {' '.join(cmd)}\nreturn_code: {proc.returncode}\n"
            f"--- stdout ---\n{proc.stdout or ''}\n--- stderr ---\n{proc.stderr or ''}\n"
        )
        transcript_p.write_text(prev + transcript_bits, encoding="utf-8")

        recv = parse_m52a_delegate_receipts(delegate_out.resolve(), require_replay=True)

        ast: dict[str, Any] = {
            "attempt_index": idx,
            "status": STATUS_EXECUTION_COMPLETED if recv["ok"] else STATUS_EXECUTION_BLOCKED,
            "ok": recv["ok"],
            "blocked_reasons": list(cast(list[Any], recv.get("blocked_reasons") or [])),
            "replay_saved": bool(recv.get("replay_saved")),
            "replay_sha256": recv.get("replay_sha256"),
            "action_count": recv.get("action_count"),
            "observation_count": recv.get("observation_count"),
            "game_steps_observed": recv.get("game_steps_observed"),
            "adapter_status": recv.get("adapter_status"),
            "live_sc2_executed": bool(recv.get("live_sc2_executed")),
            "sc2_result_metadata": recv.get("sc2_result_metadata"),
        }
        attempts.append(ast)

        if not recv["ok"]:
            break

    final_body = apply_completed_attempts_to_body(
        charter=ch,
        attempts=attempts,
        durations_s=durations,
        requested=attempt_n,
        warnings=warnings,
        opponent_norm=str(opp),
    )
    write_execution_artifacts(out, body_unsealed=final_body)
    return 3 if execution_is_blocked_profile(final_body) else 0


if __name__ == "__main__":
    raise SystemExit(main())
