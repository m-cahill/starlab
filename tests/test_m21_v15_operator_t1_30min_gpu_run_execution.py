"""V15-M21 operator T1 execution / evidence capture — tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.candidate_checkpoint_evaluation_package_models import PackageStatus
from starlab.v15.checkpoint_evaluation_readiness_models import CandidateReadinessStatus
from starlab.v15.operator_evidence_preflight_models import (
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
)
from starlab.v15.operator_t1_30min_gpu_run_execution_io import (
    base_execution_body_template,
    build_execution_body_from_m20_gate_json,
    emit_execution_artifacts,
    emit_fixture_default,
    map_m20_gate_status_to_execution_status,
    recommended_m22_fork_for_status,
    seal_operator_t1_execution_body,
)
from starlab.v15.operator_t1_30min_gpu_run_execution_models import (
    CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION,
    FILENAME_EXECUTION_JSON,
    RUN_TIER_T1_30_MIN,
    STATUS_OPERATOR_PREFLIGHT_BLOCKED,
    STATUS_T1_COMPLETED_NO_CHECKPOINT,
    STATUS_T1_NOT_STARTED,
    STATUS_T1_PACKAGE_BLOCKED,
    STATUS_T1_PACKAGE_READY,
    STATUS_T1_RUN_FAILED,
    STATUS_T1_RUN_FAILED_INSUFFICIENT_TRAINING,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_COMPLETED_NO_CHECKPOINT as M20_NO_CK,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_INSUFFICIENT_TRAINING_WORKLOAD as M20_INSUFFICIENT,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    STATUS_T1_PACKAGE_READY as M20_PKG_READY,
)
from starlab.v15.short_gpu_environment_models import CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_json(p: Path, obj: object) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(canonical_json_dumps(obj) + "\n", encoding="utf-8", newline="\n")


def test_fixture_execution_status_and_claim_flags(tmp_path: Path) -> None:
    sealed, *_ = emit_fixture_default(tmp_path)
    assert sealed["execution_status"] == STATUS_T1_NOT_STARTED
    assert sealed["contract_id"] == CONTRACT_ID_OPERATOR_T1_30MIN_GPU_RUN_EXECUTION
    assert sealed["run_tier"] == RUN_TIER_T1_30_MIN
    assert all(v is False for v in sealed["claim_flags"].values())


def test_fixture_deterministic_two_runs(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_fixture_default(a)
    emit_fixture_default(b)
    xa = (a / FILENAME_EXECUTION_JSON).read_text(encoding="utf-8")
    xb = (b / FILENAME_EXECUTION_JSON).read_text(encoding="utf-8")
    assert xa == xb


def test_map_m20_insufficient_training_to_m21_execution_status() -> None:
    got = map_m20_gate_status_to_execution_status(
        gate_status=M20_INSUFFICIENT,
        blocked_reasons=[],
        dry_run_preflight_only=False,
    )
    assert got == STATUS_T1_RUN_FAILED_INSUFFICIENT_TRAINING
    fork = recommended_m22_fork_for_status(got)
    assert fork["fork_id"] == "t1_training_workload_remediation"


def test_m21_runner_requires_dual_guards(tmp_path: Path) -> None:
    dummy = tmp_path / "x.json"
    dummy.write_text("{}", encoding="utf-8")
    common = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_m21_t1_30min_gpu_run_execution",
        "--output-dir",
        str(tmp_path / "out"),
        "--m16-short-gpu-environment-json",
        str(dummy),
        "--m08-long-gpu-manifest-json",
        str(dummy),
        "--m15-preflight-json",
        str(dummy),
        "--checkpoint-lineage-json",
        str(dummy),
        "--environment-manifest-json",
        str(dummy),
        "--dataset-manifest-json",
        str(dummy),
        "--evaluation-protocol-json",
        str(dummy),
    ]
    r1 = subprocess.run(
        common + ["--authorize-t1-30min-gpu-run"],
        capture_output=True,
        text=True,
    )
    assert r1.returncode == 2
    r2 = subprocess.run(
        common + ["--allow-operator-local-execution"],
        capture_output=True,
        text=True,
    )
    assert r2.returncode == 2


def test_emit_cli_fixture_invocation(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_operator_t1_30min_gpu_run_execution",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert (tmp_path / FILENAME_EXECUTION_JSON).is_file()


def test_preflight_blocked_fixture_m16_shadow(tmp_path: Path) -> None:
    """Missing operator-local M16 probe posture blocks via shadow M20 gate."""

    m16 = tmp_path / "m16.json"
    _write_json(
        m16,
        {
            "contract_id": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
            "profile": "fixture_ci",
            "evidence_status": "fixture_only",
        },
    )
    m08 = tmp_path / "m08.json"
    _write_json(
        m08,
        {
            "contract_id": "starlab.v15.long_gpu_training_manifest.v1",
            "campaign_id": "c",
        },
    )
    m15 = tmp_path / "m15.json"
    _write_json(
        m15,
        {"contract_id": CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT},
    )
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_operator_t1_30min_gpu_run_execution",
            "--output-dir",
            str(tmp_path / "emit"),
            "--profile",
            "operator_preflight",
            "--m16-short-gpu-environment-json",
            str(m16),
            "--m08-long-gpu-manifest-json",
            str(m08),
            "--m15-preflight-json",
            str(m15),
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    raw = json.loads((tmp_path / "emit" / FILENAME_EXECUTION_JSON).read_text(encoding="utf-8"))
    assert raw["execution_status"] == STATUS_OPERATOR_PREFLIGHT_BLOCKED


def test_synthetic_completed_no_checkpoint_maps(tmp_path: Path) -> None:
    body = base_execution_body_template(
        execution_status=STATUS_T1_COMPLETED_NO_CHECKPOINT,
        operator_run_attempted=True,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=1.0,
        dry_run_preflight_performed=False,
        dry_run_preflight_status="not_applicable",
        candidate_checkpoint_produced=False,
        candidate_kind="none",
        candidate_id=None,
        candidate_checkpoint_sha256=None,
        m08_campaign_receipt_sha256=None,
        m08_campaign_completion_status="completed",
        m08_checkpoint_count=0,
        m18_readiness_status=None,
        m19_package_status=None,
        ready_for_future_checkpoint_evaluation=False,
        blocked_reasons=[],
        upstream_m20_gate_reference=None,
        orchestrator_notes=None,
        profile="test",
    )
    sealed = seal_operator_t1_execution_body(body)
    assert sealed["execution_status"] == STATUS_T1_COMPLETED_NO_CHECKPOINT


def test_synthetic_failed_run_maps(tmp_path: Path) -> None:
    body = base_execution_body_template(
        execution_status=STATUS_T1_RUN_FAILED,
        operator_run_attempted=True,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=None,
        dry_run_preflight_performed=False,
        dry_run_preflight_status="not_applicable",
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
        blocked_reasons=["runner_failed"],
        upstream_m20_gate_reference=None,
        orchestrator_notes=None,
        profile="test",
    )
    sealed = seal_operator_t1_execution_body(body)
    assert sealed["execution_status"] == STATUS_T1_RUN_FAILED


def test_synthetic_package_ready_maps(tmp_path: Path) -> None:
    body = base_execution_body_template(
        execution_status=STATUS_T1_PACKAGE_READY,
        operator_run_attempted=True,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=10.0,
        dry_run_preflight_performed=False,
        dry_run_preflight_status="not_applicable",
        candidate_checkpoint_produced=True,
        candidate_kind="pytorch_checkpoint",
        candidate_id="c1",
        candidate_checkpoint_sha256="a" * 64,
        m08_campaign_receipt_sha256="b" * 64,
        m08_campaign_completion_status="completed",
        m08_checkpoint_count=1,
        m18_readiness_status=str(CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION),
        m19_package_status=str(PackageStatus.EVALUATION_PACKAGE_READY),
        ready_for_future_checkpoint_evaluation=True,
        blocked_reasons=[],
        upstream_m20_gate_reference=None,
        orchestrator_notes=None,
        profile="test",
    )
    sealed = seal_operator_t1_execution_body(body)
    assert sealed["execution_status"] == STATUS_T1_PACKAGE_READY
    fork = sealed["recommended_m22_fork"]
    assert fork["fork_id"] == "candidate_evaluation_or_two_hour_scale_up"


def test_build_from_m20_gate_package_ready(tmp_path: Path) -> None:
    m20 = {
        "gate_status": M20_PKG_READY,
        "operator_run_performed": True,
        "candidate_checkpoint_produced": True,
        "candidate_kind": "pytorch_checkpoint",
        "candidate_id": "x",
        "candidate_checkpoint_sha256": "c" * 64,
        "m08_campaign_receipt_sha256": "d" * 64,
        "m18_readiness_status": str(CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION),
        "m19_package_status": str(PackageStatus.EVALUATION_PACKAGE_READY),
        "ready_for_future_checkpoint_evaluation": True,
        "blocked_reasons": [],
        "operator_run_duration_observed_seconds": 5.0,
    }
    out = tmp_path / "run"
    (out / "m08").mkdir(parents=True)
    _write_json(
        out / "m08" / "v15_long_gpu_campaign_receipt.json",
        {"campaign_completion_status": "completed", "checkpoint_count": 1},
    )
    body = build_execution_body_from_m20_gate_json(
        output_dir=out,
        m20_gate=m20,
        dry_run_preflight_only=False,
        subprocess_exit_code=0,
        started_at_utc="2026-04-27T12:00:00Z",
        finished_at_utc="2026-04-27T12:30:00Z",
    )
    assert body["execution_status"] == STATUS_T1_PACKAGE_READY
    assert body["operator_run_attempted"] is True
    assert body["m08_campaign_completion_status"] == "completed"
    assert body["m08_checkpoint_count"] == 1


def test_build_from_m20_gate_dry_run_no_training_attempt(tmp_path: Path) -> None:
    m20 = {
        "gate_status": M20_NO_CK,
        "operator_run_performed": False,
        "blocked_reasons": ["dry_run_preflight_only"],
        "candidate_checkpoint_produced": False,
        "candidate_kind": "none",
        "ready_for_future_checkpoint_evaluation": False,
    }
    body = build_execution_body_from_m20_gate_json(
        output_dir=tmp_path,
        m20_gate=m20,
        dry_run_preflight_only=True,
        subprocess_exit_code=0,
        started_at_utc=None,
        finished_at_utc=None,
    )
    assert body["execution_status"] == STATUS_T1_NOT_STARTED
    assert body["dry_run_preflight_performed"] is True
    assert body["operator_run_attempted"] is False


def test_m22_fork_table_coverage() -> None:
    """Fork ids align with planning vocabulary for each terminal execution status."""

    assert recommended_m22_fork_for_status(STATUS_T1_PACKAGE_READY)["fork_id"] == (
        "candidate_evaluation_or_two_hour_scale_up"
    )
    assert recommended_m22_fork_for_status(STATUS_OPERATOR_PREFLIGHT_BLOCKED)["fork_id"] == (
        "preflight_remediation"
    )
    assert recommended_m22_fork_for_status(STATUS_T1_COMPLETED_NO_CHECKPOINT)["fork_id"] == (
        "checkpoint_emission_remediation"
    )
    assert recommended_m22_fork_for_status(STATUS_T1_RUN_FAILED)["fork_id"] == (
        "operator_gpu_run_failure_remediation"
    )
    pkg_blocked_body = base_execution_body_template(
        execution_status=STATUS_T1_PACKAGE_BLOCKED,
        operator_run_attempted=True,
        operator_run_started_at_utc=None,
        operator_run_finished_at_utc=None,
        operator_run_duration_observed_seconds=None,
        dry_run_preflight_performed=False,
        dry_run_preflight_status="not_applicable",
        candidate_checkpoint_produced=True,
        candidate_kind="pytorch_checkpoint",
        candidate_id=None,
        candidate_checkpoint_sha256=None,
        m08_campaign_receipt_sha256=None,
        m08_campaign_completion_status=None,
        m08_checkpoint_count=0,
        m18_readiness_status=None,
        m19_package_status=str(PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE),
        ready_for_future_checkpoint_evaluation=False,
        blocked_reasons=[],
        upstream_m20_gate_reference=None,
        orchestrator_notes=None,
        profile="test",
    )
    fork_blocked_pkg = recommended_m22_fork_for_status(pkg_blocked_body["execution_status"])
    assert fork_blocked_pkg["fork_id"] == "candidate_package_remediation"


def test_runtime_doc_operator_t1_scope() -> None:
    rt = REPO_ROOT / "docs" / "runtime" / "v15_operator_t1_30min_gpu_run_execution_v1.md"
    txt = rt.read_text(encoding="utf-8").lower()
    assert "t1_30_min" in txt or "30-minute" in txt or "30 minute" in txt
    assert "forward-gated" in txt
    assert "v15_m21" in txt
    assert "contract id" in txt or "contract" in txt


def test_governance_starlab_v15_m21_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M21" in v15
    assert "starlab.v15.operator_t1_30min_gpu_run_execution.v1" in v15
    assert "not_12_hour_run" in v15 or "12-hour" in v15.lower()
    rt = REPO_ROOT / "docs" / "runtime" / "v15_operator_t1_30min_gpu_run_execution_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "non-claim" in rtx or "non_claims" in rtx.replace("-", "_")


def test_governance_starlab_md_pointer_concise() -> None:
    sm = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in sm
    assert "V15-M21" in sm


def test_private_note_template_exists_not_tracked_stub() -> None:
    """Operator note template path is optional in clones without company_secrets."""

    p = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "post-v1" / "V15-M21"
    # Template created by milestone tooling when present
    if (p / "V15-M21_operator_t1_30min_note.md").is_file():
        t = (p / "V15-M21_operator_t1_30min_note.md").read_text(encoding="utf-8")
        assert "operator_run_attempted" in t.lower() or "Operator run attempted" in t


def test_fallback_execution_emit_writes_json(tmp_path: Path) -> None:
    """Emit execution JSON when the M20 gate JSON is absent (runner fallback)."""

    from starlab.v15.operator_t1_30min_gpu_run_execution_models import (
        DRY_RUN_STATUS_NOT_APPLICABLE,
        PROFILE_OPERATOR_PREFLIGHT,
    )

    body = base_execution_body_template(
        execution_status=STATUS_OPERATOR_PREFLIGHT_BLOCKED,
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
        blocked_reasons=["missing_m20_gate_json_after_delegate"],
        upstream_m20_gate_reference=None,
        orchestrator_notes={"delegate_exit_code": 2},
        profile=PROFILE_OPERATOR_PREFLIGHT,
    )
    emit_execution_artifacts(tmp_path, body)
    assert (tmp_path / FILENAME_EXECUTION_JSON).is_file()
