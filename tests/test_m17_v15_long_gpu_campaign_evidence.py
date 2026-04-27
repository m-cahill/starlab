"""V15-M17 long GPU campaign evidence — emit, M16 binding, governance."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.long_gpu_campaign_evidence_io import (
    build_long_gpu_campaign_evidence_body,
    emit_v15_long_gpu_campaign_evidence,
    parse_m16_short_gpu_environment_for_m17,
)
from starlab.v15.long_gpu_campaign_evidence_models import (
    ALL_READINESS_GATE_IDS,
    CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE,
    FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE,
    SEAL_KEY_ARTIFACT,
)
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
)
from starlab.v15.short_gpu_environment_models import (
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
    EVIDENCE_STATUS_PROBE_SUCCESS,
    M17_READY_PLANNING,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _success_m16_object() -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
        "profile": PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
        "evidence_status": EVIDENCE_STATUS_PROBE_SUCCESS,
        "operator_local_execution_performed": True,
        "short_gpu_probe_performed": True,
        "short_gpu_probe_result": "success",
        "m17_opening_recommendation": M17_READY_PLANNING,
        "long_gpu_run_authorized": False,
        "v2_authorized": False,
        "v2_recharter_authorized": False,
        "cuda_available": True,
        "torch_imported": True,
        "gpu_name": "NVIDIA Test GPU",
        "gpu_memory_summary": 12345,
        "torch_version": "2.0.0+cpu",
        "cuda_version": "12.0",
    }


def _m16_object_nested_torch_only() -> dict[str, object]:
    """Shape matching actual M16 emit: CUDA/torch under `torch_cuda_summary` only."""
    o = dict(_success_m16_object())
    o.pop("cuda_available", None)
    o.pop("torch_imported", None)
    o.pop("gpu_name", None)
    o.pop("gpu_memory_summary", None)
    o.pop("torch_version", None)
    o.pop("cuda_version", None)
    o["torch_cuda_summary"] = {
        "cuda_available": True,
        "cuda_version": "12.8",
        "torch_imported": True,
        "torch_version": "2.11.0+cu128",
    }
    o["gpu_summary"] = {
        "gpu_name": "NVIDIA GeForce RTX 5090",
        "memory_summary": "34190458880",
        "posture": "recorded_when_available",
    }
    return o


def _write_m16(path: Path, extra: dict[str, object] | None = None) -> Path:
    d = _success_m16_object()
    if extra:
        d = {**d, **extra}
    path.write_text(json.dumps(d), encoding="utf-8")
    return path


def test_default_emission_files(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    assert (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).is_file()
    assert (tmp_path / REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).is_file()
    assert (tmp_path / "v15_long_gpu_campaign_runbook.md").is_file()
    assert (tmp_path / "v15_long_gpu_campaign_closeout_checklist.md").is_file()
    assert not (tmp_path / "v15_long_gpu_campaign_receipt.json").is_file()


def test_json_deterministic(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    a = (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    b = (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    assert a == b


def test_contract_defaults_fixture(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    sealed = json.loads(
        (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    )
    assert sealed.get("contract_id") == CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE
    assert sealed.get("profile") == PROFILE_FIXTURE_CI
    for k, v in (
        ("operator_local_execution_performed", False),
        ("long_gpu_campaign_started", False),
        ("long_gpu_campaign_completed", False),
        ("long_gpu_run_authorized", False),
        ("v2_authorized", False),
        ("v2_recharter_authorized", False),
    ):
        assert sealed.get(k) is v, k
    base = {k: val for k, val in sealed.items() if k != SEAL_KEY_ARTIFACT}
    assert sealed[SEAL_KEY_ARTIFACT] == sha256_hex_of_canonical_json(base)


def test_gates_l0_l15(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    sealed = json.loads(
        (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    )
    gates = sealed.get("readiness_gates")
    assert [g.get("gate_id") for g in gates if isinstance(g, dict)] == list(ALL_READINESS_GATE_IDS)


def test_register_touchpoints(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    sealed = json.loads(
        (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    )
    r = sealed.get("register_touchpoints", [])
    docs = {x.get("register_doc") for x in r if isinstance(x, dict)}
    assert "docs/rights_register.md" in docs


def test_boundaries_and_non_claims(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    sealed = json.loads(
        (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    )
    b = sealed.get("public_private_boundary", {})
    assert "private_local_only_by_default" in b
    nc = " ".join(sealed.get("non_claims", []))
    assert "strong" in nc.lower() or "v2" in nc.lower() or "checkpoint" in nc.lower()


def test_m16_preflight(tmp_path: Path) -> None:
    m16p = _write_m16(tmp_path / "m16.json")
    emit_v15_long_gpu_campaign_evidence(
        tmp_path / "out",
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m16_path=m16p,
    )
    j = json.loads(
        (tmp_path / "out" / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8")
    )
    assert j.get("campaign_evidence_status") == "operator_preflight_ready"
    assert j.get("m16_json_canonical_sha256") != "0" * 64


def test_m16_bind_failures(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"contract_id": "wrong"}), encoding="utf-8")
    with pytest.raises(ValueError, match="M16 binding"):
        parse_m16_short_gpu_environment_for_m17(p)

    p2 = tmp_path / "bad2.json"
    o = _success_m16_object()
    o["profile"] = "fixture_ci"
    p2.write_text(json.dumps(o), encoding="utf-8")
    with pytest.raises(ValueError, match="profile"):
        parse_m16_short_gpu_environment_for_m17(p2)

    p3 = tmp_path / "bad3.json"
    o = _success_m16_object()
    o["cuda_available"] = False
    p3.write_text(json.dumps(o), encoding="utf-8")
    with pytest.raises(ValueError, match="cuda_available"):
        parse_m16_short_gpu_environment_for_m17(p3)


def test_parse_m16_accepts_nested_torch_cuda_summary(tmp_path: Path) -> None:
    p = tmp_path / "m16_nested.json"
    p.write_text(json.dumps(_m16_object_nested_torch_only()), encoding="utf-8")
    sha, _summary = parse_m16_short_gpu_environment_for_m17(p)
    assert len(sha) == 64
    # Same bytes as a second write should give the same bound SHA
    p2 = tmp_path / "m16_nested2.json"
    p2.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    sha2, _ = parse_m16_short_gpu_environment_for_m17(p2)
    assert sha == sha2


def test_parse_m16_nested_cuda_false_fails(tmp_path: Path) -> None:
    o = _m16_object_nested_torch_only()
    o["torch_cuda_summary"] = {
        "cuda_available": False,
        "torch_imported": True,
        "torch_version": "2.0.0",
        "cuda_version": "0",
    }
    p = tmp_path / "m16.json"
    p.write_text(json.dumps(o), encoding="utf-8")
    with pytest.raises(ValueError, match="cuda_available"):
        parse_m16_short_gpu_environment_for_m17(p)


def test_parse_m16_nested_torch_imported_false_fails(tmp_path: Path) -> None:
    o = _m16_object_nested_torch_only()
    o["torch_cuda_summary"] = {
        "cuda_available": True,
        "torch_imported": False,
        "torch_version": "2.0.0",
        "cuda_version": "12.0",
    }
    p = tmp_path / "m16.json"
    p.write_text(json.dumps(o), encoding="utf-8")
    with pytest.raises(ValueError, match="torch_imported"):
        parse_m16_short_gpu_environment_for_m17(p)


def test_parse_m16_prefers_top_level_cuda_over_nested(tmp_path: Path) -> None:
    """If top-level keys exist, they win (no fallback to nested for those keys)."""
    o = _m16_object_nested_torch_only()
    o["cuda_available"] = False
    o["torch_imported"] = True
    tcs = o["torch_cuda_summary"]
    assert isinstance(tcs, dict)
    o["torch_cuda_summary"] = {**tcs, "cuda_available": True}
    p = tmp_path / "m16.json"
    p.write_text(json.dumps(o), encoding="utf-8")
    with pytest.raises(ValueError, match="cuda_available"):
        parse_m16_short_gpu_environment_for_m17(p)


def test_m16_operator_preflight_nested_shape_emit(tmp_path: Path) -> None:
    p = tmp_path / "m16.json"
    p.write_text(json.dumps(_m16_object_nested_torch_only()), encoding="utf-8")
    outd = tmp_path / "m17out"
    emit_v15_long_gpu_campaign_evidence(
        outd,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m16_path=p,
    )
    j = json.loads((outd / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8"))
    assert j.get("campaign_evidence_status") == "operator_preflight_ready"
    assert j.get("m16_json_canonical_sha256") != "0" * 64


def test_cli_fixture(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_long_gpu_campaign_evidence",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).is_file()


def test_operator_local_requires_guards(tmp_path: Path) -> None:
    m = _write_m16(tmp_path / "m16.json")
    with pytest.raises(ValueError, match="triple guard"):
        build_long_gpu_campaign_evidence_body(
            profile=PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
            m16_path=m,
        )


def test_runtime_doc_mentions_non_claims() -> None:
    rt = REPO_ROOT / "docs" / "runtime" / "v15_long_gpu_campaign_evidence_v1.md"
    t = rt.read_text(encoding="utf-8").lower()
    assert "non-claim" in t
    assert "v15_long_gpu_campaign_evidence.json" in t


def test_receipt_stub_deterministic(tmp_path: Path) -> None:
    m = _write_m16(tmp_path / "m16.json")
    (tmp_path / "m16_clone.json").write_text(m.read_text(encoding="utf-8"), encoding="utf-8")
    d3 = tmp_path / "out3"
    d4 = tmp_path / "out4"
    d3.mkdir()
    d4.mkdir()
    emit_v15_long_gpu_campaign_evidence(
        d3,
        profile=PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
        m16_path=m,
        allow_operator_local_execution=True,
        authorize_long_gpu_campaign=True,
        confirm_private_artifacts=True,
    )
    emit_v15_long_gpu_campaign_evidence(
        d4,
        profile=PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
        m16_path=tmp_path / "m16_clone.json",
        allow_operator_local_execution=True,
        authorize_long_gpu_campaign=True,
        confirm_private_artifacts=True,
    )
    a2 = json.loads((d3 / "v15_long_gpu_campaign_receipt.json").read_text(encoding="utf-8"))
    b2 = json.loads((d4 / "v15_long_gpu_campaign_receipt.json").read_text(encoding="utf-8"))
    assert a2 == b2
    assert a2.get("contract_id") == CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
    assert a2.get("campaign_completion_status") == "not_executed"


def test_no_strong_agent_claims_in_fixture_json(tmp_path: Path) -> None:
    emit_v15_long_gpu_campaign_evidence(tmp_path)
    raw = (tmp_path / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE).read_text(encoding="utf-8").lower()
    assert "benchmark passed" not in raw
    assert "v2_authorized': true" not in raw and '"v2_authorized": true' not in raw


def test_m08_still_runnable_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.run_v15_long_gpu_campaign", "--help"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    out = proc.stdout + proc.stderr
    assert "run_v15_long_gpu_campaign" in out or "long GPU" in out.lower()
