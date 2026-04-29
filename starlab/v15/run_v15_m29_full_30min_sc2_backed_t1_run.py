"""V15-M29 — full 30-minute wall-clock SC2-backed T1 candidate run (delegates to M28 path)."""

from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlab.v15.full_30min_sc2_backed_t1_run_io import (
    build_m29_evidence_payload,
    load_m28_sealed,
    seal_m29_body,
    write_m29_bundle,
)
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    EVAL_GATE_READY,
    OUTCOME_BLOCKED_MISSING_M27,
    OUTCOME_BLOCKED_WALL_CLOCK_SHORT_M28,
    OUTCOME_FIXTURE_ONLY,
    OUTCOME_FULL_30_WITH_CHECKPOINT,
    OUTCOME_FULL_30_WITHOUT_CHECKPOINT,
    OUTCOME_LAUNCHED_FAILED,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL_FULL_WALL,
)
from starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training import main as m28_main
from starlab.v15.sc2_backed_t1_candidate_training_models import OUTCOME_BLOCKED_WALL_CLOCK_SHORT

REPO_ROOT = Path(__file__).resolve().parents[2]

_MIN_FULL_SEC_TOLERANCE = 10.0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_m29_full_30min_sc2_backed_t1_run",
        description=(
            "V15-M29 wrapper: delegates to the V15-M28 runner with full-wall-clock safeguards "
            "and emits distinct M29 evidence artifacts."
        ),
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required guard forwarding to the M28 operator training path.",
    )
    parser.add_argument(
        "--authorize-full-30min-sc2-backed-t1-run",
        action="store_true",
        help="Governance guard authorizing full-horizon M29 operator-local execution.",
    )
    parser.add_argument(
        "--m27-sc2-rollout-json",
        type=Path,
        default=None,
        help=(
            "Path to sealed M27 rollout JSON (required for operator-local full-horizon run; "
            "unused with --fixture-only-m29)."
        ),
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-wall-clock-minutes", type=float, default=30.0)
    parser.add_argument("--min-wall-clock-minutes", type=float, default=None)
    parser.add_argument("--checkpoint-cadence-updates", type=int, default=50)
    parser.add_argument(
        "--max-retained-checkpoints",
        type=int,
        default=256,
        help="Forwarded to M28; cap on checkpoint files retained on disk.",
    )
    parser.add_argument(
        "--device",
        choices=("auto", "cuda", "cpu"),
        default="auto",
        help="Training device forwarded to M28 runner.",
    )
    parser.add_argument("--seed", type=int, default=20260428)
    parser.add_argument(
        "--fixture-only-m29",
        action="store_true",
        help=(
            "CI-safe path: runs M28 `--fixture-only` inside the output dir, "
            "then attaches M29 evidence JSON (bounded budget; seconds-scale)."
        ),
    )

    args = parser.parse_args(argv)

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    transcript = out / "m29_operator_transcript.txt"

    if args.fixture_only_m29:
        inner_fixture = ["--fixture-only", "--output-dir", str(out)]
        rc_fixture = m28_main(inner_fixture)
        m28_path_fixture = out / "v15_sc2_backed_t1_candidate_training.json"
        sealed_m28 = load_m28_sealed(m28_path_fixture)
        gate = (
            EVAL_GATE_READY
            if bool((sealed_m28.get("candidate_checkpoint") or {}).get("sha256"))
            else "fixture_only_evaluation_gate_placeholder"
        )
        sealed29_fixture = seal_m29_body(
            _stamp_emit_ts(
                build_m29_evidence_payload(
                    m28_sealed=sealed_m28,
                    profile=PROFILE_FIXTURE_CI,
                    m29_outcome=OUTCOME_FIXTURE_ONLY,
                    evaluation_gate_status=gate,
                    fixture_only=True,
                ),
            ),
        )
        write_m29_bundle(out, sealed29_fixture)
        return rc_fixture

    if args.m27_sc2_rollout_json is None:
        transcript.write_text("error: --m27-sc2-rollout-json is required\n", encoding="utf-8")
        sys.stderr.write(transcript.read_text(encoding="utf-8"))
        return 2

    if not (args.allow_operator_local_execution and args.authorize_full_30min_sc2_backed_t1_run):
        msg = (
            "error: requires --allow-operator-local-execution and "
            "--authorize-full-30min-sc2-backed-t1-run\n"
        )
        transcript.write_text(msg, encoding="utf-8")
        sys.stderr.write(msg)
        return 2

    min_eff = (
        args.min_wall_clock_minutes
        if args.min_wall_clock_minutes is not None
        else args.max_wall_clock_minutes
    )
    inner_command: list[str] = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training",
        "--allow-operator-local-execution",
        "--authorize-sc2-backed-t1-candidate-training",
        "--m27-sc2-rollout-json",
        str(args.m27_sc2_rollout_json.resolve()),
        "--output-dir",
        str(out),
        "--max-wall-clock-minutes",
        str(args.max_wall_clock_minutes),
        "--min-wall-clock-minutes",
        str(float(min_eff)),
        "--checkpoint-cadence-updates",
        str(args.checkpoint_cadence_updates),
        "--max-retained-checkpoints",
        str(int(args.max_retained_checkpoints)),
        "--device",
        args.device,
        "--seed",
        str(int(args.seed)),
        "--require-full-wall-clock",
        "--disable-loss-floor-early-stop",
        "--continue-after-checkpoint",
    ]

    with transcript.open("w", encoding="utf-8") as tf:
        proc = subprocess.run(
            inner_command,
            cwd=str(REPO_ROOT),
            stdout=tf,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        m28_rc = int(proc.returncode)

    m28_path = out / "v15_sc2_backed_t1_candidate_training.json"
    if not m28_path.is_file():
        transcript.write_text(
            transcript.read_text(encoding="utf-8") + "\nerror: missing M28 JSON\n",
            encoding="utf-8",
        )
        return max(m28_rc, 8)

    sealed_m28 = load_m28_sealed(m28_path)
    outcome = classify_m29_outcome(m28_rc=m28_rc, m28_body=sealed_m28)
    sealed29 = seal_m29_body(
        _stamp_emit_ts(
            build_m29_evidence_payload(
                m28_sealed=sealed_m28,
                profile=PROFILE_OPERATOR_LOCAL_FULL_WALL,
                m29_outcome=outcome,
                evaluation_gate_status=evaluation_gate(sealed_m28),
                fixture_only=False,
            ),
        ),
    )
    write_m29_bundle(out, sealed29)
    return m28_rc


def _stamp_emit_ts(body_pre: dict[str, Any]) -> dict[str, Any]:
    stamped = dict(body_pre)
    stamped["emit_timestamp_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    return stamped


def classify_m29_outcome(*, m28_rc: int, m28_body: dict[str, Any]) -> str:
    mco = str(m28_body.get("m28_outcome") or "")
    ta = m28_body.get("training_attempt") or {}
    cc = str((m28_body.get("candidate_checkpoint") or {}).get("sha256") or "")
    wc = float(ta.get("wall_clock_seconds") or 0.0)
    full_ok = bool(ta.get("full_wall_clock_satisfied"))

    horizon_ok = full_ok or (wc + 1e-9 >= 1800.0 - _MIN_FULL_SEC_TOLERANCE)

    if mco == OUTCOME_BLOCKED_WALL_CLOCK_SHORT:
        return OUTCOME_BLOCKED_WALL_CLOCK_SHORT_M28

    if mco == "sc2_backed_candidate_training_blocked_missing_m27_rollout":
        return OUTCOME_BLOCKED_MISSING_M27

    if m28_rc == 4:
        return OUTCOME_LAUNCHED_FAILED

    if m28_rc != 0:
        return OUTCOME_LAUNCHED_FAILED

    if horizon_ok:
        return OUTCOME_FULL_30_WITH_CHECKPOINT if cc else OUTCOME_FULL_30_WITHOUT_CHECKPOINT

    return OUTCOME_LAUNCHED_FAILED


def evaluation_gate(body: dict[str, Any]) -> str:
    ta = body.get("training_attempt") or {}
    full_ok = bool(ta.get("full_wall_clock_satisfied"))
    wc = float(ta.get("wall_clock_seconds") or 0.0)
    cand = bool((body.get("candidate_checkpoint") or {}).get("sha256"))
    horizon_ok = full_ok or (wc + 1e-9 >= 1800.0 - _MIN_FULL_SEC_TOLERANCE)
    if horizon_ok and cand:
        return EVAL_GATE_READY
    if horizon_ok:
        return "candidate_checkpoint_package_inputs_partial"
    return "candidate_checkpoint_package_blocked_missing_full_wall_clock_evidence"


if __name__ == "__main__":
    raise SystemExit(main())
