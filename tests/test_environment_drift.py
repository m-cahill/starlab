"""M06 environment drift and smoke matrix tests (fixture-driven; SC2-free)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.sc2.environment_drift import (
    emit_m06_artifacts,
    evaluate_environment_drift,
    matrix_to_json,
    report_to_json,
    validate_m01_probe_surface,
)
from starlab.sc2.runtime_smoke_matrix import CI_PROFILE, LOCAL_PROFILE

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def _load(name: str) -> dict[str, object]:
    raw = (FIXTURE_DIR / name).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        pytest.fail("expected object")
    return data


def test_validate_probe_accepts_fixture() -> None:
    probe = _load("probe_m06_valid.json")
    assert validate_m01_probe_surface(probe) == []


def test_validate_probe_rejects_bad_surface() -> None:
    probe = _load("probe_m06_fail_invalid_surface.json")
    errs = validate_m01_probe_surface(probe)
    assert any("control_observation_surface" in e for e in errs)


def test_emit_deterministic_matrix_and_report() -> None:
    probe = _load("probe_m06_valid.json")
    m1, r1 = emit_m06_artifacts(probe=probe, profile=CI_PROFILE, run_identity=None)
    m2, r2 = emit_m06_artifacts(probe=probe, profile=CI_PROFILE, run_identity=None)
    assert matrix_to_json(m1) == matrix_to_json(m2)
    assert report_to_json(r1) == report_to_json(r2)


def test_ci_fixture_passes() -> None:
    probe = _load("probe_m06_valid.json")
    report = evaluate_environment_drift(probe=probe, profile=CI_PROFILE, run_identity=None)
    assert report["overall_status"] == "pass"
    assert report["fingerprint_comparison_performed"] is False
    assert report["environment_fingerprint_used"] is False


def test_local_optional_warns_on_null_versions() -> None:
    probe = _load("probe_m06_warn.json")
    report = evaluate_environment_drift(probe=probe, profile=LOCAL_PROFILE, run_identity=None)
    assert report["overall_status"] == "warn"
    ids = {c["check_id"]: c["status"] for c in report["check_results"]}
    assert ids["adapter_name_present"] == "not_evaluated"
    assert ids["base_build_captured"] == "warn"
    assert ids["data_version_captured"] == "warn"


def test_required_checks_fail_on_invalid_probe() -> None:
    probe = _load("probe_m06_fail_invalid_surface.json")
    report = evaluate_environment_drift(probe=probe, profile=CI_PROFILE, run_identity=None)
    assert report["overall_status"] == "fail"


def test_fingerprint_mismatch_warns() -> None:
    probe = _load("probe_m06_valid.json")
    rid = _load("run_identity_m06_fingerprint.json")
    report = evaluate_environment_drift(probe=probe, profile=CI_PROFILE, run_identity=rid)
    assert report["fingerprint_comparison_performed"] is True
    assert report["environment_fingerprint_used"] is True
    assert report["overall_status"] == "warn"
    ids = {c["check_id"]: c["status"] for c in report["check_results"]}
    assert ids["fingerprint_base_build_match"] == "warn"
    assert ids["fingerprint_data_version_match"] == "warn"


def test_fingerprint_match_passes_warnings() -> None:
    probe = _load("probe_m06_valid.json")
    rid = _load("run_identity_m06_fingerprint_match.json")
    report = evaluate_environment_drift(probe=probe, profile=CI_PROFILE, run_identity=rid)
    assert report["overall_status"] == "pass"
    ids = {c["check_id"]: c["status"] for c in report["check_results"]}
    assert ids.get("fingerprint_runtime_boundary_match") == "pass"
    assert ids.get("fingerprint_base_build_match") == "pass"
    assert ids.get("fingerprint_data_version_match") == "pass"


def test_local_optional_adapter_name_from_fingerprint() -> None:
    probe = _load("probe_m06_warn.json")
    rid = _load("run_identity_m06_fingerprint_match.json")
    report = evaluate_environment_drift(probe=probe, profile=LOCAL_PROFILE, run_identity=rid)
    ids = {c["check_id"]: c["status"] for c in report["check_results"]}
    assert ids["adapter_name_present"] == "pass"
