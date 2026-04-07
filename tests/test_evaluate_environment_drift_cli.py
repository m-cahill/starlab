"""CLI tests for M06 evaluate_environment_drift (SC2-free)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures"


def _run_cli(tmp_path: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    probe = FIXTURE_DIR / "probe_m06_valid.json"
    cmd = [
        sys.executable,
        "-m",
        "starlab.sc2.evaluate_environment_drift",
        "--probe",
        str(probe),
        "--output-dir",
        str(tmp_path),
        *extra,
    ]
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_success_and_deterministic(tmp_path: Path) -> None:
    r1 = _run_cli(tmp_path / "o1")
    r2 = _run_cli(tmp_path / "o2")
    assert r1.returncode == 0
    assert r2.returncode == 0
    a = (tmp_path / "o1" / "environment_drift_report.json").read_text(encoding="utf-8")
    b = (tmp_path / "o2" / "environment_drift_report.json").read_text(encoding="utf-8")
    assert a == b
    m = json.loads((tmp_path / "o1" / "runtime_smoke_matrix.json").read_text(encoding="utf-8"))
    assert m["schema_version"] == "starlab.runtime_smoke_matrix.v1"


def test_cli_with_run_identity(tmp_path: Path) -> None:
    rid = FIXTURE_DIR / "run_identity_m06_fingerprint_match.json"
    r = _run_cli(tmp_path, "--run-identity", str(rid))
    assert r.returncode == 0
    rep = json.loads((tmp_path / "environment_drift_report.json").read_text(encoding="utf-8"))
    assert rep["fingerprint_comparison_performed"] is True
    assert rep["environment_fingerprint_used"] is True


def test_cli_profile_local_optional(tmp_path: Path) -> None:
    r = _run_cli(tmp_path, "--profile", "local_optional")
    assert r.returncode == 0
    rep = json.loads((tmp_path / "environment_drift_report.json").read_text(encoding="utf-8"))
    assert rep["profile"] == "local_optional"


def test_cli_missing_probe_file(tmp_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "starlab.sc2.evaluate_environment_drift",
        "--probe",
        str(tmp_path / "nope.json"),
        "--output-dir",
        str(tmp_path),
    ]
    p = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert p.returncode == 1


def test_cli_malformed_probe(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    cmd = [
        sys.executable,
        "-m",
        "starlab.sc2.evaluate_environment_drift",
        "--probe",
        str(bad),
        "--output-dir",
        str(tmp_path / "out"),
    ]
    p = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert p.returncode == 1


def test_cli_invalid_run_identity(tmp_path: Path) -> None:
    rid = tmp_path / "ri.json"
    rid.write_text("[]", encoding="utf-8")
    probe = FIXTURE_DIR / "probe_m06_valid.json"
    cmd = [
        sys.executable,
        "-m",
        "starlab.sc2.evaluate_environment_drift",
        "--probe",
        str(probe),
        "--run-identity",
        str(rid),
        "--output-dir",
        str(tmp_path / "out"),
    ]
    p = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert p.returncode == 1
