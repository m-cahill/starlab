"""CLI: V15-M53 runner — Phase A candidate-watch smoke or Phase B 12-hour attempt."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from starlab.v15.m53_twelve_hour_operator_run_attempt_io import (
    emit_m53_forbidden_refusal,
    emit_m53_phase_b_operator_receipt,
    evaluate_m53_operator_preflight,
    load_m52a_phase_gate,
    run_phase_a_m52a_subprocess,
    run_phase_b_training_subprocess,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    FORBIDDEN_CLI_FLAGS,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_12H,
    GUARD_AUTHORIZE_SMOKE,
    PHASE_A_COMPLETED,
    PHASE_A_COMPLETED_WARNINGS,
    PHASE_A_SKIPPED_ACK,
    TARGET_WALL_CLOCK_SECONDS_DEFAULT,
    TRANSCRIPT_FILENAME,
)


def main(argv: list[str] | None = None) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    bad = sorted({x for x in FORBIDDEN_CLI_FLAGS if x in argv_list})
    clean = [a for a in argv_list if a not in FORBIDDEN_CLI_FLAGS]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M53 runner: Phase A delegates to M52A candidate adapter smoke; "
            "Phase B runs frozen M28 training launch (12h-class) with dual guards."
        ),
    )
    parser.add_argument(
        "--phase",
        required=True,
        choices=("candidate-watch-smoke", "full-12hour"),
    )
    parser.add_argument("--m52-launch-rehearsal-json", type=Path, required=True)
    parser.add_argument("--expected-m52-launch-rehearsal-sha256", type=str, default=None)
    parser.add_argument("--m52a-adapter-spike-json", type=Path, default=None)
    parser.add_argument("--expected-m52a-adapter-spike-sha256", type=str, default=None)
    parser.add_argument("--candidate-checkpoint-path", type=Path, required=True)
    parser.add_argument("--expected-candidate-checkpoint-sha256", type=str, required=True)
    parser.add_argument("--sc2-root", type=Path, required=True)
    parser.add_argument("--map-path", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--disk-root", type=Path, default=None)
    parser.add_argument("--estimated-checkpoint-mb", type=float, default=256.0)
    parser.add_argument("--max-retained-checkpoints", type=int, default=256)
    parser.add_argument(
        "--m53-training-launch-command",
        type=Path,
        default=None,
        help="Frozen resolved cmd for M28 12h-class run (Phase B).",
    )
    parser.add_argument(
        "--wall-clock-seconds",
        type=float,
        default=float(TARGET_WALL_CLOCK_SECONDS_DEFAULT),
    )
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--game-step", type=int, default=8)
    parser.add_argument("--max-game-steps", type=int, default=2048)
    parser.add_argument("--save-replay", action="store_true")
    parser.add_argument("--operator-note", type=Path, default=None)
    parser.add_argument("--m51-watchability-json", type=Path, default=None)
    parser.add_argument("--skip-disk-budget-strict", action="store_true")
    parser.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="Optional interruption receipt from a prior attempt (metadata only).",
    )
    parser.add_argument("--acknowledge-skip-candidate-watch-smoke", action="store_true")
    parser.add_argument("--allow-operator-local-execution", action="store_true")
    parser.add_argument("--authorize-candidate-watch-smoke", action="store_true")
    parser.add_argument("--authorize-12-hour-operator-run", action="store_true")

    args = parser.parse_args(clean)

    repo_root = Path(__file__).resolve().parents[2]
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if bad:
        emit_m53_forbidden_refusal(out, flags=bad)
        return 0

    if args.phase == "candidate-watch-smoke":
        if not (args.allow_operator_local_execution and args.authorize_candidate_watch_smoke):
            sys.stderr.write(
                f"error: Phase A requires {GUARD_ALLOW_OPERATOR_LOCAL} and "
                f"{GUARD_AUTHORIZE_SMOKE}\n",
            )
            return 2
        if args.m51_watchability_json is None:
            sys.stderr.write(
                "error: Phase A requires --m51-watchability-json (M52A upstream binding)\n",
            )
            return 2
        smoke_out = out / "candidate_watch_smoke"
        smoke_out.mkdir(parents=True, exist_ok=True)
        smoke_proc = run_phase_a_m52a_subprocess(
            repo_root=repo_root,
            m51_json=args.m51_watchability_json.resolve(),
            smoke_out=smoke_out,
            candidate_checkpoint=args.candidate_checkpoint_path.resolve(),
            expected_candidate_sha256=str(args.expected_candidate_checkpoint_sha256),
            sc2_root=args.sc2_root.resolve(),
            map_path=args.map_path.resolve(),
            device=str(args.device),
            game_step=int(args.game_step),
            max_game_steps=int(args.max_game_steps),
            save_replay=bool(args.save_replay),
            operator_note=args.operator_note.resolve() if args.operator_note else None,
        )
        rc = int(smoke_proc.returncode)
        return rc if rc <= 255 else 255

    # --- Phase B ---
    if not (args.allow_operator_local_execution and args.authorize_12_hour_operator_run):
        sys.stderr.write(
            f"error: Phase B requires {GUARD_ALLOW_OPERATOR_LOCAL} and {GUARD_AUTHORIZE_12H}\n",
        )
        return 2

    skip_ack = bool(args.acknowledge_skip_candidate_watch_smoke)
    m52a_path = args.m52a_adapter_spike_json.resolve() if args.m52a_adapter_spike_json else None

    phase_a_status, phase_a_blockers, m52a_obj = load_m52a_phase_gate(
        m52a_path,
        expected_sha256=str(args.expected_m52a_adapter_spike_sha256)
        if args.expected_m52a_adapter_spike_sha256
        else None,
        skip_acknowledged=skip_ack,
    )
    a_sha = (
        str(m52a_obj.get("artifact_sha256") or "").lower() if isinstance(m52a_obj, dict) else None
    )

    pre = evaluate_m53_operator_preflight(
        m52_launch_rehearsal_json=args.m52_launch_rehearsal_json.resolve(),
        expected_m52_sha256=str(args.expected_m52_launch_rehearsal_sha256)
        if args.expected_m52_launch_rehearsal_sha256
        else None,
        m52a_adapter_spike_json=args.m52a_adapter_spike_json,
        expected_m52a_sha256=str(args.expected_m52a_adapter_spike_sha256)
        if args.expected_m52a_adapter_spike_sha256
        else None,
        candidate_checkpoint_path=args.candidate_checkpoint_path,
        expected_candidate_sha256=args.expected_candidate_checkpoint_sha256,
        sc2_root=args.sc2_root,
        map_path=args.map_path,
        disk_root=args.disk_root,
        estimated_checkpoint_mb=float(args.estimated_checkpoint_mb)
        if args.estimated_checkpoint_mb is not None
        else None,
        max_retained_checkpoints=int(args.max_retained_checkpoints),
        skip_disk_strict=bool(args.skip_disk_budget_strict),
    )

    tcmd = args.m53_training_launch_command.resolve() if args.m53_training_launch_command else None
    transcript_path = out / TRANSCRIPT_FILENAME
    proc: subprocess.CompletedProcess[str] | None = None
    observed = 0.0
    interrupted = False
    txt = ""

    gate_ok = (
        phase_a_status
        in (
            PHASE_A_COMPLETED,
            PHASE_A_COMPLETED_WARNINGS,
            PHASE_A_SKIPPED_ACK,
        )
        and not phase_a_blockers
    )
    phase_b_train = bool(pre.ok and gate_ok and tcmd is not None and tcmd.is_file())

    if phase_b_train:
        assert tcmd is not None
        t_run0 = time.monotonic()
        proc, interrupted = run_phase_b_training_subprocess(
            tcmd,
            repo_root=repo_root,
            target_wall_clock_seconds=float(args.wall_clock_seconds),
            transcript_path=transcript_path,
        )
        observed = time.monotonic() - t_run0
        txt = transcript_path.read_text(encoding="utf-8", errors="replace")

    emit_m53_phase_b_operator_receipt(
        out,
        repo_root=repo_root,
        pre=pre,
        phase_a_status=phase_a_status,
        phase_a_blockers=phase_a_blockers,
        phase_a_m52a_sha=a_sha,
        candidate_sha256=str(args.expected_candidate_checkpoint_sha256),
        training_launch_file=tcmd,
        target_wall_clock_seconds=float(args.wall_clock_seconds),
        max_retained_checkpoints=int(args.max_retained_checkpoints),
        subprocess_result=proc,
        observed_wall_seconds=float(observed),
        interrupted=bool(interrupted),
        transcript_text=txt,
        resume_from=args.resume_from.resolve() if args.resume_from else None,
        skip_phase_a_ack=skip_ack,
    )

    if interrupted:
        return 130
    if proc is not None and int(proc.returncode) != 0:
        return min(255, max(1, int(proc.returncode)))
    if phase_b_train:
        return 0
    if tcmd is None or not tcmd.is_file():
        return 2
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
