"""Build, seal, and emit V15-M21 operator T1 execution / evidence artifacts."""

# ruff: noqa: E501

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.long_gpu_training_manifest_models import FILENAME_CAMPAIGN_RECEIPT
from starlab.v15.operator_t1_30min_gpu_run_execution_models import (
    CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION,
    DEFAULT_CLAIM_FLAGS,
    DRY_RUN_STATUS_FAILED,
    DRY_RUN_STATUS_NOT_APPLICABLE,
    DRY_RUN_STATUS_PASSED,
    EMITTER_MODULE_OPERATOR_T1_EXECUTION,
    FILENAME_EXECUTION_JSON,
    FILENAME_RUNBOOK_MD,
    MILESTONE_ID_V15_M21,
    NON_CLAIMS_V15_M21,
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_FILENAME_EXECUTION_JSON,
    REPORT_VERSION,
    RUN_TIER_T1_30_MIN,
    SCHEMA_VERSION,
    SEAL_KEY_ARTIFACT,
    STATUS_OPERATOR_PREFLIGHT_BLOCKED,
    STATUS_T1_COMPLETED_NO_CHECKPOINT,
    STATUS_T1_NOT_STARTED,
    STATUS_T1_PACKAGE_BLOCKED,
    STATUS_T1_PACKAGE_READY,
    STATUS_T1_RUN_FAILED,
    STATUS_T1_RUN_FAILED_INSUFFICIENT_TRAINING,
    STRONGEST_ALLOWED_CLAIM_M21,
    UPSTREAM_M20_CONTRACT_REFERENCE,
)
from starlab.v15.real_candidate_checkpoint_production_gate_io import (
    emit_operator_preflight_gate,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    FILENAME_GATE_JSON as M20_FILENAME_GATE_JSON,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    RUNNER_MODULE_T1_GATE,
    STATUS_FIXTURE_NO_OPERATOR_RUN,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_OPERATOR_PREFLIGHT_BLOCKED as M20_STATUS_OPERATOR_PREFLIGHT_BLOCKED,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_COMPLETED_NO_CHECKPOINT as M20_STATUS_T1_COMPLETED_NO_CHECKPOINT,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_INSUFFICIENT_TRAINING_WORKLOAD as M20_STATUS_T1_INSUFFICIENT_TRAINING_WORKLOAD,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_NOT_STARTED as M20_STATUS_T1_NOT_STARTED,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_PACKAGE_BLOCKED as M20_STATUS_T1_PACKAGE_BLOCKED,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_PACKAGE_READY as M20_STATUS_T1_PACKAGE_READY,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_RUN_FAILED as M20_STATUS_T1_RUN_FAILED,
)

_SEAL = SEAL_KEY_ARTIFACT


def default_claim_flags() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def seal_operator_t1_execution_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[_SEAL] = digest
    return sealed


def build_execution_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_operator_t1_30min_gpu_run_execution_report",
        "report_version": REPORT_VERSION,
        "milestone": MILESTONE_ID_V15_M21,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "primary_filename": FILENAME_EXECUTION_JSON,
    }


def recommended_m22_fork_for_status(execution_status: str) -> dict[str, Any]:
    """Map M21 execution outcome to a recommended V15-M22 fork (planning vocabulary only)."""

    if execution_status == STATUS_T1_PACKAGE_READY:
        return {
            "fork_id": "candidate_evaluation_or_two_hour_scale_up",
            "title": "V15-M22 — Candidate Evaluation or 2-Hour Scale-Up Gate",
            "rationale": (
                "Package-ready checkpoint exists; choose bounded evaluation vs 2-hour scale-up "
                "per operator policy."
            ),
        }
    if execution_status == STATUS_T1_PACKAGE_BLOCKED:
        return {
            "fork_id": "candidate_package_remediation",
            "title": "V15-M22 — Candidate Package Remediation",
            "rationale": "Checkpoint exists but M18/M19 structural gates did not align.",
        }
    if execution_status == STATUS_T1_COMPLETED_NO_CHECKPOINT:
        return {
            "fork_id": "checkpoint_emission_remediation",
            "title": "V15-M22 — Checkpoint Emission Remediation",
            "rationale": "Run completed without a governed .pt/.pth candidate checkpoint.",
        }
    if execution_status == STATUS_T1_RUN_FAILED:
        return {
            "fork_id": "operator_gpu_run_failure_remediation",
            "title": "V15-M22 — Operator GPU Run Failure Remediation",
            "rationale": "T1 run began but failed before a valid candidate checkpoint.",
        }
    if execution_status == STATUS_T1_RUN_FAILED_INSUFFICIENT_TRAINING:
        return {
            "fork_id": "t1_training_workload_remediation",
            "title": "V15-M22 — T1 Training Workload / Duration Remediation",
            "rationale": (
                "Operator T1 completed without a checkpoint and below minimum bounded training "
                "duration — diagnose campaign protocol, synthetic CUDA phase, or wall-clock caps."
            ),
        }
    if execution_status == STATUS_OPERATOR_PREFLIGHT_BLOCKED:
        return {
            "fork_id": "preflight_remediation",
            "title": "V15-M22 — Operator Preflight Remediation",
            "rationale": "T1 could not begin because operator preflight blocked.",
        }
    # t1_30min_run_not_started and others
    return {
        "fork_id": "operator_scheduling_follow_up",
        "title": "V15-M22 — Operator Scheduling / Authorization Follow-Up",
        "rationale": "Operator-local T1 was not started or remains in fixture/no-run posture.",
    }


def map_m20_gate_status_to_execution_status(
    *,
    gate_status: str,
    blocked_reasons: list[Any],
    dry_run_preflight_only: bool,
) -> str:
    """Translate V15-M20 gate_status (+ context) into V15-M21 execution_status."""

    br = [str(x) for x in blocked_reasons]
    if dry_run_preflight_only and "dry_run_preflight_only" in br:
        return STATUS_T1_NOT_STARTED
    if gate_status == STATUS_FIXTURE_NO_OPERATOR_RUN:
        return STATUS_T1_NOT_STARTED
    if gate_status == M20_STATUS_OPERATOR_PREFLIGHT_BLOCKED:
        return STATUS_OPERATOR_PREFLIGHT_BLOCKED
    if gate_status == M20_STATUS_T1_NOT_STARTED:
        return STATUS_T1_NOT_STARTED
    if gate_status == M20_STATUS_T1_RUN_FAILED:
        return STATUS_T1_RUN_FAILED
    if gate_status == M20_STATUS_T1_INSUFFICIENT_TRAINING_WORKLOAD:
        return STATUS_T1_RUN_FAILED_INSUFFICIENT_TRAINING
    if gate_status == M20_STATUS_T1_COMPLETED_NO_CHECKPOINT:
        return STATUS_T1_COMPLETED_NO_CHECKPOINT
    if gate_status == M20_STATUS_T1_PACKAGE_BLOCKED:
        return STATUS_T1_PACKAGE_BLOCKED
    if gate_status == M20_STATUS_T1_PACKAGE_READY:
        return STATUS_T1_PACKAGE_READY
    return STATUS_T1_NOT_STARTED


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def base_execution_body_template(
    *,
    execution_status: str,
    operator_run_attempted: bool,
    operator_run_started_at_utc: str | None,
    operator_run_finished_at_utc: str | None,
    operator_run_duration_observed_seconds: float | None,
    dry_run_preflight_performed: bool,
    dry_run_preflight_status: str | None,
    candidate_checkpoint_produced: bool,
    candidate_kind: str,
    candidate_id: str | None,
    candidate_checkpoint_sha256: str | None,
    m08_campaign_receipt_sha256: str | None,
    m08_campaign_completion_status: str | None,
    m08_checkpoint_count: int,
    m18_readiness_status: str | None,
    m19_package_status: str | None,
    ready_for_future_checkpoint_evaluation: bool,
    blocked_reasons: list[str],
    upstream_m20_gate_reference: dict[str, Any] | None,
    orchestrator_notes: dict[str, Any] | None,
    profile: str,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION,
        "milestone_id": MILESTONE_ID_V15_M21,
        "run_tier": RUN_TIER_T1_30_MIN,
        "execution_status": execution_status,
        "operator_run_attempted": operator_run_attempted,
        "operator_run_started_at_utc": operator_run_started_at_utc,
        "operator_run_finished_at_utc": operator_run_finished_at_utc,
        "operator_run_duration_target_minutes": 30,
        "operator_run_duration_observed_seconds": operator_run_duration_observed_seconds,
        "dry_run_preflight_performed": dry_run_preflight_performed,
        "dry_run_preflight_status": dry_run_preflight_status,
        "candidate_checkpoint_produced": candidate_checkpoint_produced,
        "candidate_kind": candidate_kind,
        "candidate_id": candidate_id,
        "candidate_checkpoint_sha256": candidate_checkpoint_sha256,
        "m08_campaign_receipt_sha256": m08_campaign_receipt_sha256,
        "m08_campaign_completion_status": m08_campaign_completion_status,
        "m08_checkpoint_count": m08_checkpoint_count,
        "m18_readiness_status": m18_readiness_status,
        "m19_package_status": m19_package_status,
        "ready_for_future_checkpoint_evaluation": ready_for_future_checkpoint_evaluation,
        "recommended_m22_fork": recommended_m22_fork_for_status(execution_status),
        "claim_flags": default_claim_flags(),
        "blocked_reasons": blocked_reasons,
        "non_claims": list(NON_CLAIMS_V15_M21),
        "strongest_allowed_claim_hint": STRONGEST_ALLOWED_CLAIM_M21,
        "emitter_module": EMITTER_MODULE_OPERATOR_T1_EXECUTION,
        "profile": profile,
        "upstream_reference": upstream_m20_gate_reference,
    }
    if orchestrator_notes:
        body["orchestrator_notes"] = orchestrator_notes
    return body


def emit_fixture_default(output_dir: Path) -> tuple[dict[str, Any], Path, Path, Path]:
    """CI-safe fixture: no operator execution, explicit not-started posture."""

    body = base_execution_body_template(
        execution_status=STATUS_T1_NOT_STARTED,
        operator_run_attempted=False,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=None,
        dry_run_preflight_performed=False,
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
        blocked_reasons=["fixture_ci_no_operator_execution"],
        upstream_m20_gate_reference={"contract_id": UPSTREAM_M20_CONTRACT_REFERENCE},
        orchestrator_notes=None,
        profile=PROFILE_FIXTURE_DEFAULT,
    )
    return emit_execution_artifacts(output_dir, body)


def emit_operator_preflight_execution(
    output_dir: Path,
    *,
    m16_path: Path,
    m08_manifest_path: Path,
    m15_preflight_path: Path,
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Validate M16/M08/M15 like M20 preflight snapshot; emit M21 execution JSON."""

    gate_dir = output_dir / "_m20_shadow"
    emit_operator_preflight_gate(
        gate_dir,
        m16_path=m16_path,
        m08_manifest_path=m08_manifest_path,
        m15_preflight_path=m15_preflight_path,
    )
    m20_path = gate_dir / M20_FILENAME_GATE_JSON
    m20_raw = json.loads(m20_path.read_text(encoding="utf-8"))
    blocked = list(m20_raw.get("blocked_reasons", []))
    gs = str(m20_raw.get("gate_status", ""))
    exec_status = map_m20_gate_status_to_execution_status(
        gate_status=gs,
        blocked_reasons=blocked,
        dry_run_preflight_only=False,
    )
    body = base_execution_body_template(
        execution_status=exec_status,
        operator_run_attempted=False,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=None,
        dry_run_preflight_performed=False,
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
        blocked_reasons=[str(x) for x in blocked],
        upstream_m20_gate_reference={
            "contract_id": UPSTREAM_M20_CONTRACT_REFERENCE,
            "gate_status_shadow_copy": gs,
        },
        orchestrator_notes={"shadow_emit_dir": "_m20_shadow"},
        profile=PROFILE_OPERATOR_PREFLIGHT,
    )
    return emit_execution_artifacts(output_dir, body)


def emit_execution_artifacts(
    output_dir: Path,
    body_without_seal: dict[str, Any],
) -> tuple[dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sealed = seal_operator_t1_execution_body(body_without_seal)
    j_path = output_dir / FILENAME_EXECUTION_JSON
    r_path = output_dir / REPORT_FILENAME_EXECUTION_JSON
    rb_path = output_dir / FILENAME_RUNBOOK_MD
    j_path.write_text(canonical_json_dumps(sealed) + "\n", encoding="utf-8", newline="\n")
    r_path.write_text(
        canonical_json_dumps(build_execution_report(sealed)) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rb_path.write_text(build_runbook_markdown(sealed), encoding="utf-8", newline="\n")
    return sealed, j_path, r_path, rb_path


def build_runbook_markdown(sealed: dict[str, Any]) -> str:
    es = sealed.get("execution_status", "")
    return (
        f"# V15-M21 — Operator T1 30-Minute GPU Run Execution\n\n"
        f"- Milestone: `{MILESTONE_ID_V15_M21}`\n"
        f"- Contract: `{CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION}`\n"
        f"- Execution status: `{es}`\n"
        f"- Run tier: `{RUN_TIER_T1_30_MIN}` only (no T2/T3 in this milestone)\n\n"
        "See `docs/runtime/v15_operator_t1_30min_gpu_run_execution_v1.md` for commands and "
        "non-claims.\n"
    )


def load_optional_m08_metrics(output_dir: Path) -> tuple[str | None, int]:
    """Read optional M08 receipt next to orchestrator output for completion status / counts."""

    rec_path = output_dir / "m08" / FILENAME_CAMPAIGN_RECEIPT
    if not rec_path.is_file():
        return None, 0
    try:
        raw = json.loads(rec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, 0
    if not isinstance(raw, dict):
        return None, 0
    completion = raw.get("campaign_completion_status")
    ck_raw = raw.get("checkpoint_count", 0)
    try:
        ck_count = int(ck_raw)
    except (TypeError, ValueError):
        ck_count = 0
    comp_s = str(completion) if completion is not None else None
    return comp_s, ck_count


def build_execution_body_from_m20_gate_json(
    *,
    output_dir: Path,
    m20_gate: dict[str, Any],
    dry_run_preflight_only: bool,
    subprocess_exit_code: int,
    started_at_utc: str | None,
    finished_at_utc: str | None,
) -> dict[str, Any]:
    """Compose an M21 body after delegating to the M20 orchestrator (filesystem-assisted)."""

    gs = str(m20_gate.get("gate_status", ""))
    blocked = list(m20_gate.get("blocked_reasons", []))
    exec_status = map_m20_gate_status_to_execution_status(
        gate_status=gs,
        blocked_reasons=blocked,
        dry_run_preflight_only=dry_run_preflight_only,
    )
    attempted = bool(m20_gate.get("operator_run_performed")) and not dry_run_preflight_only

    dry_pf_status: str | None
    if dry_run_preflight_only:
        dry_pf_status = (
            DRY_RUN_STATUS_PASSED if subprocess_exit_code == 0 else DRY_RUN_STATUS_FAILED
        )
    else:
        dry_pf_status = DRY_RUN_STATUS_NOT_APPLICABLE

    comp_s, ck_count = load_optional_m08_metrics(output_dir)

    body = base_execution_body_template(
        execution_status=exec_status,
        operator_run_attempted=attempted,
        operator_run_started_at_utc=started_at_utc,
        operator_run_finished_at_utc=finished_at_utc,
        operator_run_duration_observed_seconds=m20_gate.get(
            "operator_run_duration_observed_seconds"
        ),
        dry_run_preflight_performed=dry_run_preflight_only,
        dry_run_preflight_status=dry_pf_status,
        candidate_checkpoint_produced=bool(m20_gate.get("candidate_checkpoint_produced")),
        candidate_kind=str(m20_gate.get("candidate_kind", "none")),
        candidate_id=m20_gate.get("candidate_id"),
        candidate_checkpoint_sha256=m20_gate.get("candidate_checkpoint_sha256"),
        m08_campaign_receipt_sha256=m20_gate.get("m08_campaign_receipt_sha256"),
        m08_campaign_completion_status=comp_s,
        m08_checkpoint_count=ck_count,
        m18_readiness_status=m20_gate.get("m18_readiness_status"),
        m19_package_status=m20_gate.get("m19_package_status"),
        ready_for_future_checkpoint_evaluation=bool(
            m20_gate.get("ready_for_future_checkpoint_evaluation")
        ),
        blocked_reasons=[str(x) for x in blocked],
        upstream_m20_gate_reference={
            "contract_id": UPSTREAM_M20_CONTRACT_REFERENCE,
            "gate_status": gs,
        },
        orchestrator_notes={
            "m20_emitter_module": m20_gate.get("emitter_module"),
            "delegated_runner_module": RUNNER_MODULE_T1_GATE,
        },
        profile=PROFILE_OPERATOR_PREFLIGHT,
    )
    return body
