"""V15-M21 wrapper over the V15-M20 orchestrator; emits M21 execution artifacts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from starlab.v15.operator_t1_30min_gpu_run_execution_io import (
    base_execution_body_template,
    build_execution_body_from_m20_gate_json,
    emit_execution_artifacts,
    utc_now_iso,
)
from starlab.v15.operator_t1_30min_gpu_run_execution_models import (
    DRY_RUN_STATUS_NOT_APPLICABLE,
    PROFILE_OPERATOR_PREFLIGHT,
    STATUS_OPERATOR_PREFLIGHT_BLOCKED,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    FILENAME_GATE_JSON as M20_FILENAME_GATE_JSON,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_m21_t1_30min_gpu_run_execution",
        description=(
            "V15-M21 operator-local wrapper: invokes run_v15_t1_30min_candidate_checkpoint_gate "
            "(M20), then emits distinct M21 execution artifacts."
        ),
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Forwarded — required guard for intentional operator-local GPU execution.",
    )
    parser.add_argument(
        "--authorize-t1-30min-gpu-run",
        action="store_true",
        help="Forwarded — required guard authorizing the bounded T1 30-minute campaign attempt.",
    )
    parser.add_argument("--m16-short-gpu-environment-json", required=True, type=Path)
    parser.add_argument("--m08-long-gpu-manifest-json", required=True, type=Path)
    parser.add_argument("--m15-preflight-json", required=True, type=Path)
    parser.add_argument("--campaign-plan-json", type=Path, default=None)
    parser.add_argument("--checkpoint-lineage-json", required=True, type=Path)
    parser.add_argument("--environment-manifest-json", required=True, type=Path)
    parser.add_argument("--dataset-manifest-json", required=True, type=Path)
    parser.add_argument("--evaluation-protocol-json", required=True, type=Path)
    parser.add_argument(
        "--max-wall-clock-minutes",
        type=float,
        default=30.0,
        help="Forwarded to M20 orchestrator.",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--dry-run-preflight-only",
        action="store_true",
        help="Forwarded — validate inputs / gate-only path without full training invocation.",
    )
    args = parser.parse_args(argv)

    if not args.allow_operator_local_execution or not args.authorize_t1_30min_gpu_run:
        sys.stderr.write(
            "error: requires --allow-operator-local-execution and --authorize-t1-30min-gpu-run\n",
        )
        return 2

    out_root = args.output_dir.resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate",
        "--allow-operator-local-execution",
        "--authorize-t1-30min-gpu-run",
        "--m16-short-gpu-environment-json",
        str(args.m16_short_gpu_environment_json.resolve()),
        "--m08-long-gpu-manifest-json",
        str(args.m08_long_gpu_manifest_json.resolve()),
        "--m15-preflight-json",
        str(args.m15_preflight_json.resolve()),
        "--checkpoint-lineage-json",
        str(args.checkpoint_lineage_json.resolve()),
        "--environment-manifest-json",
        str(args.environment_manifest_json.resolve()),
        "--dataset-manifest-json",
        str(args.dataset_manifest_json.resolve()),
        "--evaluation-protocol-json",
        str(args.evaluation_protocol_json.resolve()),
        "--max-wall-clock-minutes",
        str(args.max_wall_clock_minutes),
        "--output-dir",
        str(out_root),
    ]
    if args.campaign_plan_json is not None:
        cmd.extend(["--campaign-plan-json", str(args.campaign_plan_json.resolve())])
    if args.dry_run_preflight_only:
        cmd.append("--dry-run-preflight-only")

    started = utc_now_iso()
    proc = subprocess.run(cmd, check=False)
    finished = utc_now_iso()

    gate_path = out_root / M20_FILENAME_GATE_JSON
    if gate_path.is_file():
        try:
            m20_gate = json.loads(gate_path.read_text(encoding="utf-8"))
            if not isinstance(m20_gate, dict):
                raise ValueError("gate not object")
        except (OSError, json.JSONDecodeError, ValueError):
            m20_gate = {}
    else:
        m20_gate = {}

    if not m20_gate:
        body = base_execution_body_template(
            execution_status=STATUS_OPERATOR_PREFLIGHT_BLOCKED,
            operator_run_attempted=False,
            operator_run_started_at_utc=started,
            operator_run_finished_at_utc=finished,
            operator_run_duration_observed_seconds=None,
            dry_run_preflight_performed=bool(args.dry_run_preflight_only),
            dry_run_preflight_status=DRY_RUN_STATUS_NOT_APPLICABLE,
            candidate_checkpoint_produced=False,
            candidate_kind="none",
            candidate_id=None,
            candidate_checkpoint_sha256=None,
            m08_campaign_receipt_sha256=None,
            m08_campaign_completion_status=None,
            m08_checkpoint_count=0,
            m18_readiness_status=None,
            m19_package_status=None,
            ready_for_future_checkpoint_evaluation=False,
            blocked_reasons=["missing_m20_gate_json_after_delegate"],
            upstream_m20_gate_reference=None,
            orchestrator_notes={"delegate_exit_code": proc.returncode},
            profile=PROFILE_OPERATOR_PREFLIGHT,
        )
        emit_execution_artifacts(out_root, body)
        return min(max(proc.returncode, 1), 8)

    body_without_seal = build_execution_body_from_m20_gate_json(
        output_dir=out_root,
        m20_gate=m20_gate,
        dry_run_preflight_only=bool(args.dry_run_preflight_only),
        subprocess_exit_code=proc.returncode,
        started_at_utc=started,
        finished_at_utc=finished,
    )
    emit_execution_artifacts(out_root, body_without_seal)

    rc = proc.returncode
    return rc if rc <= 127 else 8


if __name__ == "__main__":
    raise SystemExit(main())
