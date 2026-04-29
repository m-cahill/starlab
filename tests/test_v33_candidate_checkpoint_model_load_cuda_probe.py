"""V15-M33 candidate checkpoint model-load / CUDA inference probe tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.emit_v15_m33_candidate_checkpoint_model_load_cuda_probe import (
    main as emit_m33_main,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_io import (
    build_fixture_m31_sealed_gate,
    emit_v15_m32_candidate_checkpoint_evaluation_execution,
    seal_m32_execution_body,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io import (
    emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture,
    emit_m33_candidate_checkpoint_model_load_cuda_probe_operator,
    load_m32_evaluation_execution_json,
    run_torch_cuda_inference_probe,
    validate_m32_for_m33,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    CONTRACT_ID_M33_PROBE,
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
    PROFILE_M33_PROBE,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PROBE_COMPLETED,
    STATUS_REFUSED_BLOCKERS,
)

torch = pytest.importorskip("torch")
from torch import nn  # noqa: E402


def _fixture_m32_path(tmp_path: Path) -> Path:
    m31 = build_fixture_m31_sealed_gate()
    _, p32, _, _ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "m32_out",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    return p32


def test_m33_fixture_ci(tmp_path: Path) -> None:
    sealed, jp, _, _ = emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture(
        tmp_path / "fx",
    )
    txt = jp.read_text(encoding="utf-8").lower()
    assert "c:\\coding" not in txt
    assert "/home/" not in txt
    assert sealed["contract_id"] == CONTRACT_ID_M33_PROBE
    assert sealed["profile"] == PROFILE_M33_PROBE
    assert sealed["probe_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    assert sealed["training_performed"] is False
    assert sealed["benchmark_passed"] is False


def test_m33_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m33_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads(
        (tmp_path / "o" / "v15_candidate_checkpoint_model_load_cuda_probe.json").read_text()
    )
    assert js["probe_status"] == STATUS_FIXTURE_SCHEMA_ONLY


def test_cli_operator_missing_m32(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="m32-evaluation-execution-json"):
        emit_m33_main(
            [
                "--allow-operator-local-execution",
                "--authorize-candidate-model-load-probe",
                "--m32-evaluation-execution-json",
                str(tmp_path / "missing.json"),
                "--candidate-checkpoint-path",
                str(tmp_path / "x.pt"),
                "--expected-candidate-sha256",
                EXPECTED_PUBLIC_CANDIDATE_SHA256,
                "--device",
                "cpu",
                "--output-dir",
                str(tmp_path / "o"),
            ],
        )


def test_cli_operator_missing_guards(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="operator-local mode requires"):
        emit_m33_main(
            [
                "--allow-operator-local-execution",
                "--m32-evaluation-execution-json",
                str(tmp_path / "m.json"),
                "--candidate-checkpoint-path",
                str(tmp_path / "x.pt"),
                "--expected-candidate-sha256",
                "a" * 64,
                "--output-dir",
                str(tmp_path / "o"),
            ],
        )


def test_blocked_invalid_m32_contract(tmp_path: Path) -> None:
    p32 = _fixture_m32_path(tmp_path)
    raw = json.loads(p32.read_text(encoding="utf-8"))
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    wo["contract_id"] = "wrong"
    bad = seal_m32_execution_body(wo)
    p_bad = tmp_path / "bad32.json"
    p_bad.write_text(canonical_json_dumps(bad), encoding="utf-8")
    m32 = load_m32_evaluation_execution_json(p_bad)
    pt = tmp_path / "c.pt"
    pt.write_bytes(b"x")
    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=pt,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cpu",
    )
    assert sealed["probe_status"] == STATUS_REFUSED_BLOCKERS
    assert "blocked_invalid_m32_contract" in sealed["blocked_reasons"]


def test_blocked_m32_claim_flags(tmp_path: Path) -> None:
    p32 = _fixture_m32_path(tmp_path)
    raw = json.loads(p32.read_text(encoding="utf-8"))
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    wo["benchmark_passed"] = True
    bad = seal_m32_execution_body(wo)
    p_bad = tmp_path / "bad32.json"
    p_bad.write_text(canonical_json_dumps(bad), encoding="utf-8")
    m32 = load_m32_evaluation_execution_json(p_bad)
    pt = tmp_path / "c.pt"
    pt.write_bytes(b"x")
    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=pt,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cpu",
    )
    assert "blocked_m32_claim_flags_inconsistent" in sealed["blocked_reasons"]


def test_blocked_missing_checkpoint_file(tmp_path: Path) -> None:
    p32 = _fixture_m32_path(tmp_path)
    m32 = load_m32_evaluation_execution_json(p32)
    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=tmp_path / "none.pt",
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cpu",
    )
    assert "blocked_candidate_checkpoint_missing" in sealed["blocked_reasons"]


def test_blocked_checkpoint_sha_mismatch(tmp_path: Path) -> None:
    p32 = _fixture_m32_path(tmp_path)
    m32 = load_m32_evaluation_execution_json(p32)
    pt = tmp_path / "c.pt"
    pt.write_bytes(b"not-the-candidate-bytes")
    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=pt,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cpu",
    )
    assert "blocked_candidate_checkpoint_sha_mismatch" in sealed["blocked_reasons"]


def test_run_torch_cpu_tiny_checkpoint_roundtrip(tmp_path: Path) -> None:
    hid = 16
    in_f = 8
    model = nn.Sequential(nn.Linear(in_f, hid), nn.Tanh(), nn.Linear(hid, 1))
    p = tmp_path / "m28ish.pt"
    torch.save({"model_state_dict": model.state_dict()}, p)
    telem, blockers = run_torch_cuda_inference_probe(p, device_requested="cpu")
    assert not blockers
    assert telem["device_observed"] == "cpu"


def test_operator_success_with_probes_stubbed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    p32 = _fixture_m32_path(tmp_path)
    m32 = load_m32_evaluation_execution_json(p32)
    pt = tmp_path / "c.pt"
    pt.write_bytes(b"opaque")

    def _fake_sha(_path: Path) -> str:
        return EXPECTED_PUBLIC_CANDIDATE_SHA256

    def _fake_run(
        _checkpoint_path: Path,
        *,
        device_requested: str,
    ) -> tuple[dict[str, object], list[str]]:
        return (
            {
                "torch_version": "stub",
                "cuda_available": False,
                "cuda_device_name": "",
                "device_requested": device_requested,
                "device_observed": "cpu",
            },
            [],
        )

    monkeypatch.setattr(
        "starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io.sha256_hex_file",
        _fake_sha,
    )
    monkeypatch.setattr(
        "starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io.run_torch_cuda_inference_probe",
        _fake_run,
    )

    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=pt,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cpu",
    )
    assert sealed["probe_status"] == STATUS_PROBE_COMPLETED
    assert sealed["checkpoint_blob_sha256_verified"] is True
    assert sealed["candidate_model_loaded"] is True
    assert sealed["training_performed"] is False


def test_validate_m32_expected_sha_mismatch(tmp_path: Path) -> None:
    m31 = build_fixture_m31_sealed_gate()
    sealed32, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "m32gen",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    br = validate_m32_for_m33(sealed32, expected_candidate_sha256="f" * 64)
    assert "blocked_m32_claim_flags_inconsistent" in br


def test_cuda_path_unavailable_monkeypatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p32 = _fixture_m32_path(tmp_path)
    m32 = load_m32_evaluation_execution_json(p32)
    pt = tmp_path / "c.pt"
    pt.write_bytes(b"opaque")

    def _fake_sha(_path: Path) -> str:
        return EXPECTED_PUBLIC_CANDIDATE_SHA256

    def _fake_run(
        _checkpoint_path: Path,
        *,
        device_requested: str,
    ) -> tuple[dict[str, object], list[str]]:
        return (
            {
                "torch_version": "stub",
                "cuda_available": False,
                "cuda_device_name": "",
                "device_requested": device_requested,
                "device_observed": "cuda_unavailable",
            },
            ["blocked_cuda_unavailable"],
        )

    monkeypatch.setattr(
        "starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io.sha256_hex_file",
        _fake_sha,
    )
    monkeypatch.setattr(
        "starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_io.run_torch_cuda_inference_probe",
        _fake_run,
    )

    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_operator(
        tmp_path / "out",
        m32=m32,
        candidate_checkpoint_path=pt,
        expected_candidate_sha256=EXPECTED_PUBLIC_CANDIDATE_SHA256,
        device_requested="cuda",
    )
    assert "blocked_cuda_unavailable" in sealed["blocked_reasons"]


def test_governance_non_claims_in_fixture_json(tmp_path: Path) -> None:
    sealed, *_ = emit_m33_candidate_checkpoint_model_load_cuda_probe_fixture(tmp_path / "g")
    assert "not_seventy_two_hour_campaign" in sealed["non_claims"]
