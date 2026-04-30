"""CLI: run governed V15-M39 7200s operator attempt (dual-guarded; not for CI)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256
from starlab.v15.m39_two_hour_operator_run_attempt_io import (
    emit_m39_operator_run_receipt,
    evaluate_operator_preflight,
    run_operator_subprocess,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    STATUS_PREFLIGHT_READY,
    TRANSCRIPT_FILENAME,
)


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(
        description=(
            "V15-M39: execute the frozen M38 launch command (7200s-class) with transcript capture "
            "and sealed receipts. Requires explicit dual guards; do not run in merge CI."
        ),
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required guard for any local subprocess.",
    )
    parser.add_argument(
        "--authorize-2hour-operator-run",
        action="store_true",
        help="Required guard for the 7200-second training attempt.",
    )
    parser.add_argument(
        "--m38-launch-rehearsal-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--m39-launch-command",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--expected-candidate-sha256",
        type=str,
        default=EXPECTED_PUBLIC_CANDIDATE_SHA256,
    )
    parser.add_argument(
        "--target-wall-clock-seconds",
        type=float,
        default=7200.0,
    )
    parser.add_argument(
        "--max-retained-checkpoints",
        type=int,
        default=256,
        help="Expected retention cap (recorded; launch command should match M38 freeze).",
    )
    parser.add_argument(
        "--skip-cuda-sc2-probes",
        action="store_true",
        help="Skip CUDA/sc2 preflight probes (not recommended for real attempts).",
    )
    parser.add_argument(
        "--min-free-disk-gb",
        type=float,
        default=100.0,
    )
    parser.add_argument(
        "--launch-command-delta-detected",
        action="store_true",
        help="Record that the operator deliberately diverged from the frozen launch file.",
    )
    parser.add_argument("--output-dir", type=Path, required=True)

    args = parser.parse_args(argv)
    if not (args.allow_operator_local_execution and args.authorize_2hour_operator_run):
        sys.stderr.write(
            "error: requires --allow-operator-local-execution and --authorize-2hour-operator-run\n",
        )
        return 2

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    pre = evaluate_operator_preflight(
        repo_root=repo_root,
        m38_launch_rehearsal_json=args.m38_launch_rehearsal_json.resolve(),
        m39_launch_command=args.m39_launch_command.resolve(),
        expected_candidate_sha256=str(args.expected_candidate_sha256),
        skip_cuda_sc2=bool(args.skip_cuda_sc2_probes),
        min_free_bytes=int(max(float(args.min_free_disk_gb), 0.001) * (1024**3)),
        output_dir=out,
    )

    transcript_path = out / TRANSCRIPT_FILENAME

    if pre.status != STATUS_PREFLIGHT_READY:
        emit_m39_operator_run_receipt(
            out,
            repo_root=repo_root,
            m38_launch_rehearsal_json=args.m38_launch_rehearsal_json.resolve(),
            m39_launch_command=args.m39_launch_command.resolve(),
            expected_candidate_sha256=str(args.expected_candidate_sha256),
            max_retained_checkpoints=int(args.max_retained_checkpoints),
            target_wall_clock_seconds=float(args.target_wall_clock_seconds),
            skip_cuda_sc2=bool(args.skip_cuda_sc2_probes),
            min_free_disk_gb=float(args.min_free_disk_gb),
            subprocess_result=None,
            observed_wall_seconds=0.0,
            interrupted=False,
            launch_command_delta_detected=bool(args.launch_command_delta_detected),
            transcript_text=f"blocked_before_subprocess:{pre.status}\n",
            preflight_outcome=pre,
        )
        return 2

    t_run0 = time.monotonic()
    proc, interrupted = run_operator_subprocess(
        args.m39_launch_command.resolve(),
        repo_root=repo_root,
        target_wall_clock_seconds=float(args.target_wall_clock_seconds),
        transcript_path=transcript_path,
    )
    observed = time.monotonic() - t_run0

    txt = transcript_path.read_text(encoding="utf-8", errors="replace")
    emit_m39_operator_run_receipt(
        out,
        repo_root=repo_root,
        m38_launch_rehearsal_json=args.m38_launch_rehearsal_json.resolve(),
        m39_launch_command=args.m39_launch_command.resolve(),
        expected_candidate_sha256=str(args.expected_candidate_sha256),
        max_retained_checkpoints=int(args.max_retained_checkpoints),
        target_wall_clock_seconds=float(args.target_wall_clock_seconds),
        skip_cuda_sc2=bool(args.skip_cuda_sc2_probes),
        min_free_disk_gb=float(args.min_free_disk_gb),
        subprocess_result=proc,
        observed_wall_seconds=float(observed),
        interrupted=bool(interrupted),
        launch_command_delta_detected=bool(args.launch_command_delta_detected),
        transcript_text=txt,
        preflight_outcome=pre,
    )

    rc = int(proc.returncode)
    if interrupted:
        return 130
    if rc != 0:
        return min(255, max(1, rc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
