"""V15-M35 smoke benchmark readiness tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.emit_v15_m35_candidate_checkpoint_smoke_benchmark_readiness import (
    main as emit_m35_main,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io import seal_m33_body
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    CONTRACT_ID_M33_PROBE,
    PROFILE_M33_PROBE,
    STATUS_PROBE_COMPLETED,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_io import (
    emit_m35_readiness_fixture,
    emit_m35_readiness_operator_preflight,
    evaluate_operator_preflight_m35,
    validate_m33_probe_sealed,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    CONTRACT_ID_M35_READINESS,
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
    PROFILE_M35_READINESS,
    STATUS_BLOCKED_INVALID_M33,
    STATUS_BLOCKED_M05,
    STATUS_BLOCKED_MISSING_M33,
    STATUS_BLOCKED_NOT_CUDA,
    STATUS_BLOCKED_SHA_MISMATCH,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
)
from starlab.v15.strong_agent_scorecard_io import emit_v15_strong_agent_scorecard
from starlab.v15.strong_agent_scorecard_models import PROFILE_FIXTURE_CI

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_m33(tmp_path: Path, m33: dict[str, object]) -> Path:
    p = tmp_path / "m33.json"
    p.write_text(canonical_json_dumps(m33), encoding="utf-8")
    return p


def _sealed_m33_cuda_completed(
    *,
    cand_sha: str = EXPECTED_PUBLIC_CANDIDATE_SHA256,
    corrupt_seal: bool = False,
) -> dict[str, object]:
    body: dict[str, object] = {
        "schema_version": "1.0",
        "contract_id": CONTRACT_ID_M33_PROBE,
        "milestone": "V15-M33",
        "profile": PROFILE_M33_PROBE,
        "emitter_module": "starlab.v15.emit_v15_m33_candidate_checkpoint_model_load_cuda_probe",
        "fixture_ci": False,
        "probe_status": STATUS_PROBE_COMPLETED,
        "blocked_reasons": [],
        "recommended_next": "V15-M35_candidate_checkpoint_smoke_benchmark_readiness",
        "candidate_checkpoint_sha256": cand_sha,
        "candidate_checkpoint_promotion_status": "not_promoted_candidate_only",
        "checkpoint_blob_sha256_verified": True,
        "device_requested": "cuda",
        "device_observed": "cuda",
        "torch_version": "stub",
        "cuda_available": True,
        "cuda_device_name": "stub",
        "cuda_probe_performed": True,
        "training_performed": False,
        "benchmark_passed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "scorecard_execution_performed": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_or_t3_authorized": False,
        "long_gpu_run_authorized": False,
        "seventy_two_hour_run_authorized": False,
        "checkpoint_blob_io_performed": True,
        "candidate_model_loaded": True,
        "inference_probe_performed": True,
        "m32_execution_binding": {
            "artifact_sha256": "a" * 64,
            "execution_status": "candidate_evaluation_execution_operator_local_metadata_completed",
            "profile": "starlab.v15.m32.bounded_candidate_evaluation_execution.v1",
            "m32_json_path_note": "redacted",
        },
        "non_claims": [
            "no training",
            "no benchmark pass",
            "no strength evaluation",
            "no checkpoint promotion",
        ],
    }
    sealed = seal_m33_body(body)
    if corrupt_seal:
        sealed = dict(sealed)
        sealed["artifact_sha256"] = "0" * 64
    return sealed


def test_m35_fixture_emits_three_artifacts(tmp_path: Path) -> None:
    sealed, p_main, p_rep, p_chk = emit_m35_readiness_fixture(tmp_path / "o")
    assert sealed["readiness_status"] == STATUS_FIXTURE_ONLY
    assert p_main.is_file() and p_rep.is_file() and p_chk.is_file()
    nc_list = sealed.get("non_claims") or []
    assert isinstance(nc_list, list) and len(nc_list) >= 3
    js = json.loads(p_main.read_text(encoding="utf-8"))
    assert js["contract_id"] == CONTRACT_ID_M35_READINESS
    assert js["profile_id"] == PROFILE_M35_READINESS


def test_m35_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m35_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads(
        (tmp_path / "o" / "v15_candidate_checkpoint_smoke_benchmark_readiness.json").read_text(),
    )
    assert js["readiness_status"] == STATUS_FIXTURE_ONLY


def test_m35_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, *_ = emit_m35_readiness_fixture(tmp_path / "o")
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_operator_preflight_success_synthetic(tmp_path: Path) -> None:
    m33 = _sealed_m33_cuda_completed()
    assert validate_m33_probe_sealed(m33)
    body = evaluate_operator_preflight_m35(
        m33,
        expected_candidate_sha256=None,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_READY


def test_operator_preflight_blocked_missing_m33(tmp_path: Path) -> None:
    body = evaluate_operator_preflight_m35(
        None,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_BLOCKED_MISSING_M33


def test_operator_preflight_emit_missing_file(tmp_path: Path) -> None:
    sealed, *_ = emit_m35_readiness_operator_preflight(
        tmp_path / "o",
        m33_path=None,
        expected_candidate_sha256=None,
        m05_path=None,
    )
    assert sealed["readiness_status"] == STATUS_BLOCKED_MISSING_M33


def test_operator_preflight_invalid_m33_contract(tmp_path: Path) -> None:
    m33 = _sealed_m33_cuda_completed()
    m33 = dict(m33)
    m33["contract_id"] = "wrong.contract"
    m33 = seal_m33_body({k: v for k, v in m33.items() if k != "artifact_sha256"})
    body = evaluate_operator_preflight_m35(
        m33,
        expected_candidate_sha256=None,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_BLOCKED_INVALID_M33


def test_operator_preflight_invalid_m33_seal(tmp_path: Path) -> None:
    m33 = _sealed_m33_cuda_completed(corrupt_seal=True)
    body = evaluate_operator_preflight_m35(
        m33,
        expected_candidate_sha256=None,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_BLOCKED_INVALID_M33


def test_operator_preflight_sha_mismatch(tmp_path: Path) -> None:
    good = _sealed_m33_cuda_completed()
    body = evaluate_operator_preflight_m35(
        good,
        expected_candidate_sha256="f" * 64,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_BLOCKED_SHA_MISMATCH


def test_operator_preflight_blocked_not_cuda(tmp_path: Path) -> None:
    m33 = _sealed_m33_cuda_completed()
    m33 = dict(m33)
    m33["device_observed"] = "cpu"
    m33["cuda_probe_performed"] = False
    m33 = seal_m33_body({k: v for k, v in m33.items() if k != "artifact_sha256"})
    body = evaluate_operator_preflight_m35(
        m33,
        expected_candidate_sha256=None,
        m05=None,
    )
    assert body["readiness_status"] == STATUS_BLOCKED_NOT_CUDA


def test_optional_m05_binds(tmp_path: Path) -> None:
    m05d = tmp_path / "m05"
    emit_v15_strong_agent_scorecard(m05d, profile=PROFILE_FIXTURE_CI)
    m05_path = m05d / "v15_strong_agent_scorecard.json"
    m33 = _sealed_m33_cuda_completed()
    sealed, *_ = emit_m35_readiness_operator_preflight(
        tmp_path / "out",
        m33_path=None,
        expected_candidate_sha256=None,
        m05_path=m05_path,
    )
    assert sealed["readiness_status"] == STATUS_BLOCKED_MISSING_M33
    sealed2, *_ = emit_m35_readiness_operator_preflight(
        tmp_path / "out2",
        m33_path=_write_m33(tmp_path, m33),
        expected_candidate_sha256=None,
        m05_path=m05_path,
    )
    assert sealed2["readiness_status"] == STATUS_READY
    assert sealed2["upstream_bindings"]["m05_scorecard_protocol"]["binding_status"] == "bound_valid"


def test_invalid_m05_blocks(tmp_path: Path) -> None:
    m05_bad = tmp_path / "bad.json"
    m05_bad.write_text(canonical_json_dumps({"contract_id": "nope"}), encoding="utf-8")
    m33 = _sealed_m33_cuda_completed()
    sealed, *_ = emit_m35_readiness_operator_preflight(
        tmp_path / "out",
        m33_path=_write_m33(tmp_path, m33),
        expected_candidate_sha256=None,
        m05_path=m05_bad,
    )
    assert sealed["readiness_status"] == STATUS_BLOCKED_M05


def test_fixture_checklist_records_readiness_status(tmp_path: Path) -> None:
    sealed, _, _, p_chk = emit_m35_readiness_fixture(tmp_path / "o")
    text = p_chk.read_text(encoding="utf-8")
    assert "not_benchmark_execution" in text or "not benchmark" in text.lower()
    assert str(sealed["readiness_status"]) in text


def test_no_windows_path_leak_fixture(tmp_path: Path) -> None:
    _, p_main, _, _ = emit_m35_readiness_fixture(tmp_path / "o")
    low = p_main.read_text(encoding="utf-8").lower()
    assert "c:\\coding" not in low


def test_real_m33_file_if_present(tmp_path: Path) -> None:
    candidates = sorted(
        REPO_ROOT.glob("out/**/v15_candidate_checkpoint_model_load_cuda_probe.json"),
    )
    candidate = next(
        (p for p in candidates if "fixture_ci_report" not in str(p).replace("\\", "/")),
        None,
    )
    if candidate is None or not candidate.is_file():
        pytest.skip("Operator-local M33 JSON not present in this workspace")
    sealed, *_ = emit_m35_readiness_operator_preflight(
        tmp_path / "live",
        m33_path=candidate,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        m05_path=None,
    )
    assert sealed["readiness_status"] == STATUS_READY
