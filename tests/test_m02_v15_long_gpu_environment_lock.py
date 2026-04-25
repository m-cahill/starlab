"""V15-M02: long GPU environment lock deterministic JSON + governance pointers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import (
    build_environment_lock_body,
    emit_long_gpu_environment_lock,
    seal_environment_lock_body,
)
from starlab.v15.environment_lock_models import (
    CONTRACT_ID_LONG_GPU_ENV,
    FILENAME_LONG_GPU_ENV,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL,
    REPORT_FILENAME_LONG_GPU_ENV,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TOP_KEYS = (
    "contract_id",
    "milestone_id",
    "generated_by",
    "profile",
    "environment_lock_status",
    "long_gpu_run_authorized",
    "operator_local_ready",
    "evidence_scope",
    "repo_identity",
    "python_environment",
    "dependency_environment",
    "cuda_environment",
    "pytorch_environment",
    "gpu_environment",
    "sc2_environment",
    "map_pool_environment",
    "disk_environment",
    "path_disclosure_policy",
    "required_checks",
    "check_results",
    "status_vocabulary",
    "non_claims",
    "carry_forward_items",
)


def test_environment_lock_seal_stable() -> None:
    body = build_environment_lock_body(PROFILE_FIXTURE_CI)
    sealed = seal_environment_lock_body(body)
    assert sealed["long_gpu_environment_lock_sha256"] == sha256_hex_of_canonical_json(body)
    assert sealed["contract_id"] == CONTRACT_ID_LONG_GPU_ENV


def test_environment_lock_golden_sha256() -> None:
    body = build_environment_lock_body(PROFILE_FIXTURE_CI)
    sealed = seal_environment_lock_body(body)
    assert sealed["long_gpu_environment_lock_sha256"] == (
        "52ee51fbb59e779b073e7d6805441770c303550f5c75b4a200642a49173e5659"
    )


def test_emit_fixture_writes_files(tmp_path: Path) -> None:
    sealed, rep, c_path, r_path = emit_long_gpu_environment_lock(
        tmp_path, profile=PROFILE_FIXTURE_CI, probe_path=None
    )
    assert c_path.name == FILENAME_LONG_GPU_ENV
    assert r_path.name == REPORT_FILENAME_LONG_GPU_ENV
    assert rep["long_gpu_environment_lock_sha256"] == sealed["long_gpu_environment_lock_sha256"]


def test_emit_is_deterministic(tmp_path: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    a = tmp_path_factory.mktemp("a")
    b = tmp_path_factory.mktemp("b")
    emit_long_gpu_environment_lock(a, profile=PROFILE_FIXTURE_CI)
    emit_long_gpu_environment_lock(b, profile=PROFILE_FIXTURE_CI)
    t1 = (a / FILENAME_LONG_GPU_ENV).read_text(encoding="utf-8")
    t2 = (b / FILENAME_LONG_GPU_ENV).read_text(encoding="utf-8")
    assert t1 == t2


def test_fixture_posture() -> None:
    body = build_environment_lock_body(PROFILE_FIXTURE_CI)
    assert body["environment_lock_status"] == "fixture_only"
    assert body["operator_local_ready"] is False
    assert body["long_gpu_run_authorized"] is False
    assert body["profile"] == "fixture_ci"


def test_fixture_no_absolute_paths_in_json(tmp_path: Path) -> None:
    emit_long_gpu_environment_lock(tmp_path, profile=PROFILE_FIXTURE_CI)
    text = (tmp_path / FILENAME_LONG_GPU_ENV).read_text(encoding="utf-8")
    assert not re.search(r"[A-Za-z]:\\", text)
    assert ":\\\\" not in text  # UNC start not expected
    assert "/home/" not in text
    assert "/Users/" not in text


def test_non_claims_present() -> None:
    body = build_environment_lock_body(PROFILE_FIXTURE_CI)
    assert "m02_authorizes_long_gpu_run" in body["non_claims"]
    assert "px2_m04_opened" in body["non_claims"]


def test_required_sections_and_vocab() -> None:
    body = build_environment_lock_body(PROFILE_FIXTURE_CI)
    for k in REQUIRED_TOP_KEYS:
        assert k in body
    assert "environment_lock_status" in body["status_vocabulary"]
    assert "check_status" in body["status_vocabulary"]


def test_report_has_sha256_field(tmp_path: Path) -> None:
    _, rep, _, _ = emit_long_gpu_environment_lock(tmp_path, profile=PROFILE_FIXTURE_CI)
    assert "long_gpu_environment_lock_sha256" in rep
    assert rep["long_gpu_environment_lock_sha256"]


def test_starlab_ledger_m02_concise_pointers() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in text
    assert "docs/runtime/v15_long_gpu_run_environment_lock_v1.md" in text


def test_runtime_doc_and_v15_authority() -> None:
    doc = (REPO_ROOT / "docs" / "runtime" / "v15_long_gpu_run_environment_lock_v1.md").read_text(
        encoding="utf-8"
    )
    assert "starlab.v15.long_gpu_environment_lock.v1" in doc
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M02" in v15
    assert "starlab.v15.long_gpu_environment_lock.v1" in v15
    assert "python -m starlab.v15.emit_v15_long_gpu_environment_lock" in v15
    assert "**M02 non-claims" in v15


def test_emit_cli_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_long_gpu_environment_lock", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "v15_long_gpu_environment_lock" in proc.stdout
    assert "fixture_ci" in proc.stdout


def test_emit_cli_default_fixture(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_long_gpu_environment_lock",
            "--output-dir",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    data = json.loads((tmp_path / FILENAME_LONG_GPU_ENV).read_text(encoding="utf-8"))
    assert data["profile"] == PROFILE_FIXTURE_CI


def test_operator_probe_path_redaction(tmp_path: Path) -> None:
    probe = tmp_path / "probe.json"
    probe.write_text(
        json.dumps(
            {
                "evidence_scope": "operator_local_probe",
                "repo_identity": {
                    "git_sha": "a" * 40,
                    "branch": "main",
                },
                "python_environment": {
                    "python_version": "3.11.1",
                    "platform": "linux",
                    "implementation": "cpython",
                },
                "dependency_environment": {
                    "dependency_fingerprint": "fp-test-123",
                    "requirements_source": "pyproject",
                },
                "cuda_environment": {
                    "cuda_version": "12.4",
                    "driver_version": "550",
                    "nvidia_smi_status": "ok",
                },
                "pytorch_environment": {
                    "torch_version": "2.8.0",
                    "torch_cuda_version": "12.4",
                    "torch_installed": True,
                },
                "gpu_environment": {
                    "gpu_present": True,
                    "gpu_name": "Test GPU",
                },
                "sc2_environment": {
                    "sc2_client_declared": True,
                    "sc2_version": "4.1.0",
                },
                "map_pool_environment": {
                    "map_pool_id": "mp1",
                    "required_maps": ["m1"],
                },
                "disk_environment": {
                    "output_root_policy": "local_out",
                    "free_bytes_required": 1000,
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    # poison path
    p2 = json.loads(probe.read_text(encoding="utf-8"))
    p2["operator_notes"] = "install at C:\\Games\\Sc2"
    probe.write_text(json.dumps(p2), encoding="utf-8")

    emit_long_gpu_environment_lock(tmp_path, profile=PROFILE_OPERATOR_LOCAL, probe_path=probe)
    out = (tmp_path / FILENAME_LONG_GPU_ENV).read_text(encoding="utf-8")
    assert "C:\\\\Games" not in out
    assert "REDACTED_ABSOLUTE_PATH" in out
