"""V15-M08 long GPU campaign manifest / preflight / guarded runner (no real M50 execution in CI)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.environment_lock_models import (
    STATUS_FIXTURE_ONLY,
    STATUS_OPERATOR_LOCAL_READY,
)
from starlab.v15.long_gpu_training_manifest_io import (
    build_long_gpu_training_manifest_body_fixture,
    compute_preflight_gate_statuses,
    emit_v15_long_gpu_training_manifest_operator_declared,
    emit_v15_long_gpu_training_manifest_operator_preflight,
    long_campaign_execution_allowed,
    seal_long_gpu_training_manifest_body,
    validate_campaign_plan,
)
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
    FILENAME_LONG_GPU_TRAINING_MANIFEST,
    GATE_FIELD_NAMES,
    GATE_PASS,
    MILESTONE_ID_V15_M08,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
    SEAL_KEY_MANIFEST,
)
from starlab.v15.long_gpu_training_manifest_models import (
    PROFILE_OPERATOR_PREFLIGHT as PROF_PREFLIGHT,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_fixture_manifest_deterministic() -> None:
    a = build_long_gpu_training_manifest_body_fixture()
    b = build_long_gpu_training_manifest_body_fixture()
    assert a == b
    sa = seal_long_gpu_training_manifest_body(a)
    sb = seal_long_gpu_training_manifest_body(b)
    assert sa[SEAL_KEY_MANIFEST] == sb[SEAL_KEY_MANIFEST]


def test_fixture_contract_and_profile() -> None:
    body = build_long_gpu_training_manifest_body_fixture()
    assert body["contract_id"] == CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST
    assert body["profile_id"] == PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION
    assert body["profile"] == PROFILE_FIXTURE_CI
    af = body["authorization_flags"]
    assert af["long_gpu_run_authorized"] is False
    assert af["long_gpu_campaign_execution_performed"] is False


def test_seal_matches_report() -> None:
    body = build_long_gpu_training_manifest_body_fixture()
    sealed = seal_long_gpu_training_manifest_body(body)
    assert sealed[SEAL_KEY_MANIFEST] == sha256_hex_of_canonical_json(body)


def test_operator_declared_minimal(tmp_path: Path) -> None:
    body = build_long_gpu_training_manifest_body_fixture()
    body.pop(SEAL_KEY_MANIFEST, None)
    p = tmp_path / "m.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    out = tmp_path / "o"
    sealed, _rep, _rc, cp, rp = emit_v15_long_gpu_training_manifest_operator_declared(out, p)
    assert cp.is_file() and rp.is_file()
    assert sealed["authorization_flags"]["long_gpu_run_authorized"] is False


def test_operator_declared_redacts(tmp_path: Path) -> None:
    body = build_long_gpu_training_manifest_body_fixture()
    body.pop(SEAL_KEY_MANIFEST, None)
    body["operator_identity"] = {"posture": "x", "operator_label": "evil@example.com C:\\secret\\a"}
    p = tmp_path / "m2.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    out = tmp_path / "o2"
    sealed, _, _, _, _ = emit_v15_long_gpu_training_manifest_operator_declared(out, p)
    raw = json.dumps(sealed)
    assert "evil@" not in raw


def test_invalid_campaign_plan() -> None:
    with pytest.raises(ValueError, match="missing keys"):
        validate_campaign_plan({"campaign_id": "x"})


def test_preflight_missing_operator_inputs_exit_code(tmp_path: Path) -> None:
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_long_gpu_training_manifest",
            "--profile",
            PROF_PREFLIGHT,
            "--output-dir",
            str(tmp_path / "out"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 2


def test_run_campaign_requires_double_guard(tmp_path: Path) -> None:
    manifest = tmp_path / "mf.json"
    plan = tmp_path / "cp.json"
    manifest.write_text("{}", encoding="utf-8")
    plan.write_text("{}", encoding="utf-8")
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_long_gpu_campaign",
            "--campaign-manifest-json",
            str(manifest),
            "--campaign-plan-json",
            str(plan),
            "--output-root",
            str(tmp_path / "root"),
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 2


def _minimal_plan(cid: str = "m08_test_campaign") -> dict[str, Any]:
    return {
        "campaign_id": cid,
        "campaign_title": "test",
        "operator": "fixture",
        "milestone": MILESTONE_ID_V15_M08,
        "target_machine": "local",
        "target_gpu": "RTX_5090_class",
        "training_pipeline_id": "m49_m50_wrap",
        "training_profile_id": "v15_m08",
        "campaign_goal": "fixture_preflight",
        "target_duration_hours": 0,
        "minimum_duration_hours": 0,
        "max_wall_clock_hours": 1,
        "max_training_steps": 0,
        "checkpoint_interval_steps": 1,
        "evaluation_interval_steps": 1,
        "xai_sample_interval_steps": 1,
        "dataset_manifest_ref": "logical:ds",
        "training_config_ref": "logical:tc",
        "initial_checkpoint_ref": "logical:ckpt",
        "output_root_policy": "out/v15_m08_campaigns",
        "stop_policy": {"kind": "operator_ctrl_c"},
        "resume_policy": {"kind": "m50_resume"},
        "rollback_policy": {"kind": "operator_declared"},
        "failure_quarantine_policy": {"kind": "isolate"},
        "artifact_retention_policy": "local_only",
        "public_private_boundary": "operator_local_default",
        "non_claims": ["test non-claim"],
        "m49_full_local_training_campaign_contract_path": str(
            REPO_ROOT / "README.md",
        ),
        "m49_campaign_root": str(REPO_ROOT),
    }


def test_preflight_gate_m07_fixture_blocks_g(tmp_path: Path) -> None:
    plan = _minimal_plan()
    el = {
        "environment_lock_status": STATUS_OPERATOR_LOCAL_READY,
        "cuda_environment": {"cuda_available": True},
    }
    m07 = {"profile": PROFILE_FIXTURE_CI, "authorization_flags": {}}
    cl = {"checkpoint_lineage": [{"checkpoint_id": "a"}]}
    gates = compute_preflight_gate_statuses(
        campaign_plan=plan,
        environment_lock=el,
        m07_receipt=m07,
        checkpoint_lineage=cl,
        training_config={"k": 1},
        dataset_manifest={"k": 1},
        rights_manifest={"k": 1},
        strong_agent_scorecard={"k": 1},
        xai_evidence=None,
        human_panel_benchmark=None,
    )
    assert gates["gate_g_operator_status"] != GATE_PASS


def test_preflight_emit_writes_files(tmp_path: Path) -> None:
    plan = _minimal_plan("emit_files_cid")
    el = tmp_path / "el.json"
    cl = tmp_path / "cl.json"
    m07 = tmp_path / "m07.json"
    tc = tmp_path / "tc.json"
    dm = tmp_path / "dm.json"
    rm = tmp_path / "rm.json"
    el.write_text(
        json.dumps(
            {
                "environment_lock_status": STATUS_OPERATOR_LOCAL_READY,
                "cuda_environment": {"cuda_available": True},
            },
        ),
        encoding="utf-8",
    )
    cl.write_text(json.dumps({"checkpoint_lineage": [{"checkpoint_id": "x"}]}), encoding="utf-8")
    m07.write_text(
        json.dumps(
            {
                "profile": "operator_local_short_gpu",
                "authorization_flags": {"gpu_shakedown_performed": True},
                "contract_id": "starlab.v15.training_run_receipt.v1",
            },
        ),
        encoding="utf-8",
    )
    tc.write_text(json.dumps({"lr": 0.01}), encoding="utf-8")
    dm.write_text(json.dumps({"rows": []}), encoding="utf-8")
    rm.write_text(json.dumps({"rights": "ok"}), encoding="utf-8")
    out = tmp_path / "pref"
    emit_v15_long_gpu_training_manifest_operator_preflight(
        out,
        campaign_plan=plan,
        environment_lock_path=el,
        checkpoint_lineage_path=cl,
        m07_training_run_receipt_path=m07,
        training_config_path=tc,
        dataset_manifest_path=dm,
        rights_manifest_path=rm,
        strong_agent_scorecard_path=None,
        xai_evidence_path=None,
        human_panel_benchmark_path=None,
    )
    assert (out / FILENAME_LONG_GPU_TRAINING_MANIFEST).is_file()
    assert (out / "campaign_plan.json").is_file()


def test_long_run_allowed_with_override() -> None:
    gates = {k: GATE_PASS for k in GATE_FIELD_NAMES}
    gates["gate_g_operator_status"] = "blocked"
    ok_no, _ = long_campaign_execution_allowed(
        gates, governance_override_missing_m07_gpu_shakedown=False
    )
    assert ok_no is False
    ok_yes, bl = long_campaign_execution_allowed(
        gates, governance_override_missing_m07_gpu_shakedown=True
    )
    assert ok_yes is True
    assert not bl


def test_emit_cli_fixture_subprocess(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_long_gpu_training_manifest",
            "--output-dir",
            str(out),
            "--profile",
            PROFILE_FIXTURE_CI,
        ],
        cwd=REPO_ROOT,
        check=False,
    ).returncode
    assert rc == 0
    assert (out / FILENAME_LONG_GPU_TRAINING_MANIFEST).is_file()


def test_fixture_b_gate_not_pass_with_m02_fixture_only(tmp_path: Path) -> None:
    plan = _minimal_plan("b_gate")
    el = {
        "environment_lock_status": STATUS_FIXTURE_ONLY,
        "cuda_environment": {"cuda_available": False},
    }
    m07 = {
        "profile": "operator_local_short_gpu",
        "authorization_flags": {"gpu_shakedown_performed": True},
    }
    cl = {"checkpoint_lineage": [{"checkpoint_id": "a"}]}
    gates = compute_preflight_gate_statuses(
        campaign_plan=plan,
        environment_lock=el,
        m07_receipt=m07,
        checkpoint_lineage=cl,
        training_config={"k": 1},
        dataset_manifest={"k": 1},
        rights_manifest={"k": 1},
        strong_agent_scorecard={"k": 1},
        xai_evidence={"k": 1},
        human_panel_benchmark=None,
    )
    ok, blockers = long_campaign_execution_allowed(
        gates,
        governance_override_missing_m07_gpu_shakedown=True,
    )
    assert ok is False
    assert any("gate_b" in b for b in blockers)
