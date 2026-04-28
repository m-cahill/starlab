"""V15-M20 operator-local T1 (30-minute) candidate checkpoint production orchestrator."""

# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_io import (
    emit_v15_candidate_checkpoint_evaluation_package,
)
from starlab.v15.checkpoint_evaluation_readiness_io import emit_v15_checkpoint_evaluation_readiness
from starlab.v15.checkpoint_evaluation_readiness_models import (
    PROFILE_OPERATOR_EXPLICIT_INPUTS,
    CandidateReadinessStatus,
)
from starlab.v15.long_gpu_training_manifest_io import build_campaign_receipt_report
from starlab.v15.long_gpu_training_manifest_models import (
    FILENAME_CAMPAIGN_RECEIPT,
    REPORT_FILENAME_CAMPAIGN_RECEIPT,
    SEAL_KEY_CAMPAIGN_RECEIPT,
)
from starlab.v15.real_candidate_checkpoint_production_gate_io import (
    base_gate_body_template,
    build_candidate_manifest_body,
    build_operator_completed_campaign_receipt,
    discover_first_pytorch_checkpoint,
    emit_gate_artifacts,
    map_m19_status_to_gate,
    validate_m08_manifest,
    validate_m15_preflight,
    validate_m16_operator_local_probe_success,
    write_checkpoint_sha_sidecar,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    EMITTER_MODULE_REAL_CANDIDATE_GATE,
    PROFILE_OPERATOR_PREFLIGHT,
    RUN_TIER_T1_30_MIN,
    STATUS_OPERATOR_PREFLIGHT_BLOCKED,
    STATUS_T1_COMPLETED_NO_CHECKPOINT,
    STATUS_T1_PACKAGE_BLOCKED,
    STATUS_T1_RUN_FAILED,
)
from starlab.v15.strong_agent_scorecard_models import PROTOCOL_PROFILE_ID


def _json_sha(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"expected JSON object: {path}")
    return sha256_hex_of_canonical_json(raw)


def _candidate_id_from_lineage(lineage: dict[str, Any], sha: str) -> str:
    for key in ("checkpoints", "checkpoint_lineage"):
        rows = lineage.get(key)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            if str(row.get("checkpoint_sha256", "")).lower() == sha.lower():
                cid = str(row.get("checkpoint_id", "")).strip()
                if cid:
                    return cid
    return f"t1_candidate_{sha[:12]}"


def _must_file(p: Path, label: str) -> Path:
    if not p.is_file():
        raise SystemExit(f"error: {label} must exist ({p})")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate",
        description=(
            "V15-M20 T1 operator-local orchestrator: validates preflight JSON, runs M08 runner "
            "with wall-clock budget, collects receipts, reruns M18/M19 emitters."
        ),
    )
    parser.add_argument(
        "--allow-operator-local-execution",
        action="store_true",
        help="Required guard for intentional operator-local GPU execution.",
    )
    parser.add_argument(
        "--authorize-t1-30min-gpu-run",
        action="store_true",
        help="Required guard authorizing the bounded T1 30-minute campaign attempt.",
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
        help="Forwarded to M08 runner -> execute_full_local_training_campaign.",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--dry-run-preflight-only",
        action="store_true",
        help="Validate inputs + emit gate JSON only (no M08 subprocess).",
    )
    args = parser.parse_args(argv)

    if not args.allow_operator_local_execution or not args.authorize_t1_30min_gpu_run:
        sys.stderr.write(
            "error: requires --allow-operator-local-execution and --authorize-t1-30min-gpu-run\n",
        )
        return 2

    out_root = args.output_dir.resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    m16_p = _must_file(args.m16_short_gpu_environment_json, "--m16-short-gpu-environment-json")
    m08_m = _must_file(args.m08_long_gpu_manifest_json, "--m08-long-gpu-manifest-json")
    m15_p = _must_file(args.m15_preflight_json, "--m15-preflight-json")
    lineage_p = _must_file(args.checkpoint_lineage_json, "--checkpoint-lineage-json")
    env_p = _must_file(args.environment_manifest_json, "--environment-manifest-json")
    ds_p = _must_file(args.dataset_manifest_json, "--dataset-manifest-json")
    score_p = _must_file(args.evaluation_protocol_json, "--evaluation-protocol-json")

    blocked: list[str] = []
    ok_a, msg_a = validate_m16_operator_local_probe_success(m16_p)
    if not ok_a:
        blocked.append(msg_a)
    ok_b, msg_b = validate_m08_manifest(m08_m)
    if not ok_b:
        blocked.append(msg_b)
    ok_c, msg_c = validate_m15_preflight(m15_p)
    if not ok_c:
        blocked.append(msg_c)

    if blocked:
        body = base_gate_body_template(
            gate_status=STATUS_OPERATOR_PREFLIGHT_BLOCKED,
            operator_run_performed=False,
            candidate_checkpoint_produced=False,
            candidate_kind="none",
            candidate_id=None,
            candidate_checkpoint_sha256=None,
            m08_campaign_receipt_sha256=None,
            m18_readiness_status=None,
            m19_package_status=None,
            ready_for_future_checkpoint_evaluation=False,
            blocked_reasons=blocked,
            allowed_next_steps=[],
            operator_run_duration_observed_seconds=None,
            artifact_notes={
                "m16_json_sha256": _json_sha(m16_p),
                "m08_manifest_sha256": _json_sha(m08_m),
                "m15_preflight_sha256": _json_sha(m15_p),
            },
        )
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["emitter_module"] = EMITTER_MODULE_REAL_CANDIDATE_GATE
        emit_gate_artifacts(out_root, body)
        return 7

    plan_path = args.campaign_plan_json
    if plan_path is None:
        candidate = m08_m.parent / "campaign_plan.json"
        plan_path = candidate if candidate.is_file() else None
    if plan_path is None or not plan_path.is_file():
        sys.stderr.write(
            "error: campaign_plan.json not found — pass --campaign-plan-json explicitly.\n",
        )
        return 2

    manifest_obj = json.loads(m08_m.read_text(encoding="utf-8"))
    if not isinstance(manifest_obj, dict):
        return 2
    campaign_id = str(manifest_obj.get("campaign_id", "unknown_campaign"))
    manifest_sha_bind = _json_sha(m08_m)

    if args.dry_run_preflight_only:
        body = base_gate_body_template(
            gate_status=STATUS_T1_COMPLETED_NO_CHECKPOINT,
            operator_run_performed=False,
            candidate_checkpoint_produced=False,
            candidate_kind="none",
            candidate_id=None,
            candidate_checkpoint_sha256=None,
            m08_campaign_receipt_sha256=None,
            m18_readiness_status=None,
            m19_package_status=None,
            ready_for_future_checkpoint_evaluation=False,
            blocked_reasons=["dry_run_preflight_only"],
            allowed_next_steps=[],
            operator_run_duration_observed_seconds=None,
        )
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["emitter_module"] = EMITTER_MODULE_REAL_CANDIDATE_GATE
        emit_gate_artifacts(out_root, body)
        return 0

    lineage_obj = json.loads(lineage_p.read_text(encoding="utf-8"))
    if not isinstance(lineage_obj, dict):
        sys.stderr.write("error: lineage JSON must be an object\n")
        return 2

    exec_root = out_root / "m08_campaign_execution"
    exec_root.mkdir(parents=True, exist_ok=True)
    execution_id = str(uuid.uuid4())

    cmd = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_long_gpu_campaign",
        "--campaign-manifest-json",
        str(m08_m.resolve()),
        "--campaign-plan-json",
        str(plan_path.resolve()),
        "--output-root",
        str(exec_root.resolve()),
        "--allow-operator-local-execution",
        "--authorize-long-gpu-campaign",
        "--execution-id",
        execution_id,
        "--max-wall-clock-minutes",
        str(args.max_wall_clock_minutes),
        "--run-tier",
        RUN_TIER_T1_30_MIN,
    ]

    t0 = time.monotonic()
    proc = subprocess.run(cmd, check=False)
    elapsed = time.monotonic() - t0

    m08_dir = out_root / "m08"
    m08_dir.mkdir(parents=True, exist_ok=True)

    ck_path = discover_first_pytorch_checkpoint(exec_root)
    ck_sha: str | None = sha256_hex_file(ck_path) if ck_path is not None else None
    cand_id = _candidate_id_from_lineage(lineage_obj, ck_sha or "")

    receipt_sealed = build_operator_completed_campaign_receipt(
        campaign_id=campaign_id,
        execution_id=execution_id,
        checkpoint_id=cand_id if ck_sha else None,
        checkpoint_sha256=ck_sha,
        manifest_sha256_bind=manifest_sha_bind,
    )
    rec_path = m08_dir / FILENAME_CAMPAIGN_RECEIPT
    rec_path.write_text(canonical_json_dumps(receipt_sealed) + "\n", encoding="utf-8", newline="\n")
    rep_path = m08_dir / REPORT_FILENAME_CAMPAIGN_RECEIPT
    rep_path.write_text(
        canonical_json_dumps(build_campaign_receipt_report(receipt_sealed)) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    receipt_plain = {k: v for k, v in receipt_sealed.items() if k != SEAL_KEY_CAMPAIGN_RECEIPT}

    gate_notes: dict[str, Any] = {
        "m08_subprocess_exit_code": proc.returncode,
        "manifest_sha256": manifest_sha_bind,
        "execution_output_root": "m08_campaign_execution",
    }

    if proc.returncode != 0:
        body = base_gate_body_template(
            gate_status=STATUS_T1_RUN_FAILED,
            operator_run_performed=True,
            candidate_checkpoint_produced=False,
            candidate_kind="none",
            candidate_id=None,
            candidate_checkpoint_sha256=None,
            m08_campaign_receipt_sha256=None,
            m18_readiness_status=None,
            m19_package_status=None,
            ready_for_future_checkpoint_evaluation=False,
            blocked_reasons=["m08_runner_nonzero_exit"],
            allowed_next_steps=["review_execution_logs_operator_local_only"],
            operator_run_duration_observed_seconds=elapsed,
            artifact_notes=gate_notes,
        )
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["emitter_module"] = EMITTER_MODULE_REAL_CANDIDATE_GATE
        emit_gate_artifacts(out_root, body)
        return min(max(proc.returncode, 1), 8)

    if ck_path is None:
        body = base_gate_body_template(
            gate_status=STATUS_T1_COMPLETED_NO_CHECKPOINT,
            operator_run_performed=True,
            candidate_checkpoint_produced=False,
            candidate_kind="none",
            candidate_id=None,
            candidate_checkpoint_sha256=None,
            m08_campaign_receipt_sha256=receipt_sealed.get(SEAL_KEY_CAMPAIGN_RECEIPT),
            m18_readiness_status=None,
            m19_package_status=None,
            ready_for_future_checkpoint_evaluation=False,
            blocked_reasons=["no_pytorch_checkpoint_artifact_under_execution_root"],
            allowed_next_steps=["investigate_training_outputs_emit_joblib_only"],
            operator_run_duration_observed_seconds=elapsed,
            artifact_notes=gate_notes,
        )
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["emitter_module"] = EMITTER_MODULE_REAL_CANDIDATE_GATE
        emit_gate_artifacts(out_root, body)
        return 0

    cand_dir = out_root / "candidate"
    cand_dir.mkdir(parents=True, exist_ok=True)
    dest_ck = cand_dir / ck_path.name
    shutil.copy2(ck_path, dest_ck)
    write_checkpoint_sha_sidecar(dest_ck, ck_sha or "")

    env_sha = _json_sha(env_p)
    ds_sha = _json_sha(ds_p)

    cand_body = build_candidate_manifest_body(
        candidate_id=cand_id,
        checkpoint_path=dest_ck,
        checkpoint_sha256=ck_sha or "",
        environment_manifest_sha256=env_sha,
        dataset_manifest_sha256=ds_sha,
        evaluation_protocol_id=PROTOCOL_PROFILE_ID,
        produced_by_run_id=execution_id,
        source_campaign_receipt_sha256=str(receipt_sealed.get(SEAL_KEY_CAMPAIGN_RECEIPT)),
        source_training_manifest_sha256=manifest_sha_bind,
    )

    cand_manifest_path = cand_dir / "candidate_checkpoint_manifest.json"
    cand_manifest_path.write_text(
        canonical_json_dumps(cand_body) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    m18_out = out_root / "m18"
    m18_out.mkdir(parents=True, exist_ok=True)
    sealed_m18, _, _ = emit_v15_checkpoint_evaluation_readiness(
        m18_out,
        profile=PROFILE_OPERATOR_EXPLICIT_INPUTS,
        candidate_manifest=cand_body,
        campaign_receipt=receipt_plain,
        checkpoint_lineage=lineage_obj,
    )

    m19_out = out_root / "m19"
    sealed_m19, _, _, _ = emit_v15_candidate_checkpoint_evaluation_package(
        m19_out,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m18_path=m18_out / "v15_checkpoint_evaluation_readiness.json",
        candidate_manifest_path=cand_manifest_path,
        campaign_receipt_path=rec_path,
        checkpoint_lineage_path=lineage_p,
        environment_manifest_path=env_p,
        dataset_manifest_path=ds_p,
        evaluation_protocol_path=score_p,
    )

    m18_readiness_s = str(sealed_m18.get("readiness_status", ""))
    m19_pkg_s = str(sealed_m19.get("package_status", ""))

    gst, ready_eval = map_m19_status_to_gate(m19_pkg_s)
    if m18_readiness_s != str(CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION):
        gst = STATUS_T1_PACKAGE_BLOCKED
        ready_eval = False

    br: list[str] = []
    if not ready_eval:
        br.append("m18_or_m19_structural_gate_failed")

    body = base_gate_body_template(
        gate_status=gst,
        operator_run_performed=True,
        candidate_checkpoint_produced=True,
        candidate_kind="pytorch_checkpoint",
        candidate_id=cand_id,
        candidate_checkpoint_sha256=ck_sha,
        m08_campaign_receipt_sha256=receipt_sealed.get(SEAL_KEY_CAMPAIGN_RECEIPT),
        m18_readiness_status=m18_readiness_s,
        m19_package_status=m19_pkg_s,
        ready_for_future_checkpoint_evaluation=ready_eval,
        blocked_reasons=br,
        allowed_next_steps=(
            ["consider_forward_gate_t2_two_hour_campaign"]
            if ready_eval
            else ["remediation_candidate_checkpoint_evaluation_inputs"]
        ),
        operator_run_duration_observed_seconds=elapsed,
        artifact_notes=gate_notes,
    )
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["emitter_module"] = EMITTER_MODULE_REAL_CANDIDATE_GATE
    emit_gate_artifacts(out_root, body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
