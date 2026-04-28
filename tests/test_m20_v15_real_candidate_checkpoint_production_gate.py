"""V15-M20 real candidate checkpoint production gate — tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.candidate_checkpoint_evaluation_package_models import PackageStatus
from starlab.v15.real_candidate_checkpoint_production_gate_io import (
    base_gate_body_template,
    discover_first_pytorch_checkpoint,
    emit_fixture_default,
    map_m19_status_to_gate,
    seal_real_candidate_gate_body,
    validate_m08_manifest,
    validate_m16_operator_local_probe_success,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE,
    FILENAME_GATE_JSON,
    RUN_TIER_T1_30_MIN,
    STATUS_FIXTURE_NO_OPERATOR_RUN,
    STATUS_T1_COMPLETED_NO_CHECKPOINT,
    STATUS_T1_PACKAGE_BLOCKED,
    STATUS_T1_PACKAGE_READY,
    STATUS_T1_RUN_FAILED,
)
from starlab.v15.short_gpu_environment_models import (
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_json(p: Path, obj: object) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(canonical_json_dumps(obj) + "\n", encoding="utf-8", newline="\n")


def test_fixture_gate_status_and_claim_flags(tmp_path: Path) -> None:
    sealed, *_ = emit_fixture_default(tmp_path)
    assert sealed["gate_status"] == STATUS_FIXTURE_NO_OPERATOR_RUN
    assert sealed["contract_id"] == CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE
    assert sealed["run_tier"] == RUN_TIER_T1_30_MIN
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_fixture_deterministic_two_runs(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_fixture_default(a)
    emit_fixture_default(b)
    xa = (a / FILENAME_GATE_JSON).read_text(encoding="utf-8")
    xb = (b / FILENAME_GATE_JSON).read_text(encoding="utf-8")
    assert xa == xb


def test_runner_requires_dual_guards(tmp_path: Path) -> None:
    dummy = tmp_path / "x.json"
    dummy.write_text("{}", encoding="utf-8")
    common = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate",
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
    r1 = subprocess.run(common + ["--authorize-t1-30min-gpu-run"], capture_output=True, text=True)
    assert r1.returncode == 2
    r2 = subprocess.run(
        common + ["--allow-operator-local-execution"],
        capture_output=True,
        text=True,
    )
    assert r2.returncode == 2


def test_preflight_blocked_fixture_m16(tmp_path: Path) -> None:
    m16 = tmp_path / "m16.json"
    _write_json(
        m16,
        {
            "contract_id": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
            "profile": "fixture_ci",
            "evidence_status": "fixture_only",
        },
    )
    ok, msg = validate_m16_operator_local_probe_success(m16)
    assert ok is False
    assert msg


def test_preflight_blocked_missing_m08_contract(tmp_path: Path) -> None:
    m08 = tmp_path / "m08.json"
    _write_json(m08, {"contract_id": "wrong"})
    ok, msg = validate_m08_manifest(m08)
    assert ok is False
    assert "m08_contract_id_mismatch" in msg


def test_synthetic_status_completed_no_checkpoint() -> None:
    body = base_gate_body_template(
        gate_status=STATUS_T1_COMPLETED_NO_CHECKPOINT,
        operator_run_performed=True,
        candidate_checkpoint_produced=False,
        candidate_kind="none",
        candidate_id=None,
        candidate_checkpoint_sha256=None,
        m08_campaign_receipt_sha256=None,
        m18_readiness_status=None,
        m19_package_status=None,
        ready_for_future_checkpoint_evaluation=False,
        blocked_reasons=[],
        allowed_next_steps=[],
        operator_run_duration_observed_seconds=10.0,
    )
    sealed = seal_real_candidate_gate_body(body)
    assert sealed["gate_status"] == STATUS_T1_COMPLETED_NO_CHECKPOINT


def test_synthetic_status_failed_run() -> None:
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
        blocked_reasons=["runner_failed"],
        allowed_next_steps=[],
        operator_run_duration_observed_seconds=None,
    )
    sealed = seal_real_candidate_gate_body(body)
    assert sealed["gate_status"] == STATUS_T1_RUN_FAILED


def test_discover_checkpoint_ignores_joblib(tmp_path: Path) -> None:
    (tmp_path / "w.joblib").write_bytes(b"fake")
    assert discover_first_pytorch_checkpoint(tmp_path) is None


def test_discover_prefers_sorted_pt(tmp_path: Path) -> None:
    (tmp_path / "b.pt").write_bytes(b"a")
    (tmp_path / "a.pt").write_bytes(b"b")
    got = discover_first_pytorch_checkpoint(tmp_path)
    assert got is not None
    assert got.name == "a.pt"


def test_map_m19_ready_vs_blocked() -> None:
    assert map_m19_status_to_gate(str(PackageStatus.EVALUATION_PACKAGE_READY)) == (
        STATUS_T1_PACKAGE_READY,
        True,
    )
    blocked_tup = map_m19_status_to_gate(
        str(PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE),
    )
    assert blocked_tup[0] == STATUS_T1_PACKAGE_BLOCKED
    assert blocked_tup[1] is False


def test_m20_claim_flags_never_true_in_fixture(tmp_path: Path) -> None:
    sealed, *_ = emit_fixture_default(tmp_path)
    assert all(sealed["claim_flags"].values()) is False


def test_runbook_emitted(tmp_path: Path) -> None:
    emit_fixture_default(tmp_path)
    rb = tmp_path / "v15_real_candidate_checkpoint_production_runbook.md"
    assert rb.is_file()
    assert "V15-M20" in rb.read_text(encoding="utf-8")


def test_governance_starlab_v15_m20_docs() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M20" in v15
    assert "T1_30_MIN" in v15 or "30-minute" in v15.lower()
    assert "not_12_hour_run" in v15 or "12-hour" in v15.lower()
    rt = REPO_ROOT / "docs" / "runtime" / "v15_real_candidate_checkpoint_production_gate_v1.md"
    assert rt.is_file()
    rtx = rt.read_text(encoding="utf-8").lower()
    assert "contract" in rtx and "m20" in rtx


def test_governance_starlab_md_pointer_concise() -> None:
    sm = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in sm
    assert "**V15-M20**" in sm or "V15-M20" in sm
    assert sm.count("Current (v1.5):") <= 6


def test_emit_cli_fixture_invocation(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_real_candidate_checkpoint_production_gate",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert (tmp_path / FILENAME_GATE_JSON).is_file()
