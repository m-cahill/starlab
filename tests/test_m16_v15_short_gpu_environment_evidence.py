"""V15-M16 short GPU / environment evidence — emit, bindings, governance text."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.emit_v15_long_gpu_environment_lock import main as m02_main
from starlab.v15.emit_v15_long_gpu_training_manifest import main as m08_main
from starlab.v15.emit_v15_operator_evidence_collection_preflight import main as m15_main
from starlab.v15.emit_v15_training_run_receipt import main as m07_main
from starlab.v15.operator_evidence_preflight_models import (
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
)
from starlab.v15.short_gpu_environment_io import (
    build_short_gpu_environment_body,
    emit_v15_short_gpu_environment_evidence,
    parse_m15_operator_evidence_preflight,
)
from starlab.v15.short_gpu_environment_models import (
    ALL_READINESS_GATE_IDS,
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
    FILENAME_SHORT_GPU_ENV_CHECKLIST_MD,
    FILENAME_SHORT_GPU_ENV_EVIDENCE,
    M17_BLOCKED_PENDING,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
    REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE,
    SEAL_KEY_ARTIFACT,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_default_emission_three_files(tmp_path: Path) -> None:
    emit_v15_short_gpu_environment_evidence(tmp_path)
    assert (tmp_path / FILENAME_SHORT_GPU_ENV_EVIDENCE).is_file()
    assert (tmp_path / REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE).is_file()
    assert (tmp_path / FILENAME_SHORT_GPU_ENV_CHECKLIST_MD).is_file()


def test_json_deterministic_emit(tmp_path: Path) -> None:
    emit_v15_short_gpu_environment_evidence(tmp_path)
    a = (tmp_path / FILENAME_SHORT_GPU_ENV_EVIDENCE).read_text(encoding="utf-8")
    emit_v15_short_gpu_environment_evidence(tmp_path)
    b = (tmp_path / FILENAME_SHORT_GPU_ENV_EVIDENCE).read_text(encoding="utf-8")
    assert a == b


def test_contract_and_defaults(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(tmp_path)
    assert sealed.get("contract_id") == CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE
    assert sealed.get("profile") == PROFILE_FIXTURE_CI
    assert sealed.get("operator_local_execution_performed") is False
    assert sealed.get("short_gpu_probe_performed") is False
    assert sealed.get("long_gpu_run_authorized") is False
    assert sealed.get("v2_authorized") is False
    assert sealed.get("v2_recharter_authorized") is False
    assert sealed.get("m17_opening_recommendation") == M17_BLOCKED_PENDING
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_ARTIFACT}
    assert sealed[SEAL_KEY_ARTIFACT] == sha256_hex_of_canonical_json(base)


def test_readiness_gates_g0_g12(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(tmp_path)
    gates = sealed.get("readiness_gates")
    assert isinstance(gates, list)
    got = [g.get("gate_id") for g in gates if isinstance(g, dict)]
    assert got == list(ALL_READINESS_GATE_IDS)


def test_register_touchpoints(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(tmp_path)
    reg = sealed.get("register_touchpoints")
    assert isinstance(reg, list)
    paths = {x.get("register_doc") for x in reg if isinstance(x, dict)}
    assert "docs/rights_register.md" in paths
    assert "docs/human_benchmark_register.md" in paths


def test_public_private_boundary(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(tmp_path)
    b = sealed.get("public_private_boundary")
    assert isinstance(b, dict)
    priv = b.get("private_local_only_by_default")
    assert isinstance(priv, list)
    assert "model_weights" in priv
    assert "checkpoint_blobs" in priv


def _emit_fixture_m02(tmp_path: Path) -> Path:
    m02_main(["--output-dir", str(tmp_path)])
    return tmp_path / "v15_long_gpu_environment_lock.json"


def _emit_fixture_m07(tmp_path: Path) -> Path:
    m07_main(["--output-dir", str(tmp_path)])
    return tmp_path / "v15_training_run_receipt.json"


def _emit_fixture_m08(tmp_path: Path) -> Path:
    m08_main(["--output-dir", str(tmp_path)])
    return tmp_path / "v15_long_gpu_training_manifest.json"


def _emit_fixture_m15(tmp_path: Path) -> Path:
    m15_main(["--output-dir", str(tmp_path)])
    return tmp_path / "v15_operator_evidence_collection_preflight.json"


def test_m02_binding_fixture_file(tmp_path: Path) -> None:
    m02d = tmp_path / "m02"
    m02d.mkdir()
    p = _emit_fixture_m02(m02d)
    out = tmp_path / "out"
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(out, m02_path=p)
    ub = sealed.get("upstream_bindings")
    assert isinstance(ub, dict)
    b = ub.get("m02_environment_lock")
    assert isinstance(b, dict)
    assert b.get("binding_mode") == "file_bound"
    assert b.get("m02_environment_lock_json_canonical_sha256") != "0" * 64


def test_m07_binding_fixture_file(tmp_path: Path) -> None:
    d = tmp_path / "m07"
    d.mkdir()
    p = _emit_fixture_m07(d)
    out = tmp_path / "out"
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(out, m07_path=p)
    ub = sealed.get("upstream_bindings")
    assert isinstance(ub, dict)
    b = ub.get("m07_training_run_receipt")
    assert isinstance(b, dict)
    assert b["binding_mode"] == "file_bound"
    assert b.get("m07_emit_profile_readonly") == PROFILE_FIXTURE_CI


def test_m08_binding_fixture_file(tmp_path: Path) -> None:
    d = tmp_path / "m08"
    d.mkdir()
    p = _emit_fixture_m08(d)
    out = tmp_path / "out"
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(out, m08_path=p)
    ub = sealed.get("upstream_bindings")
    assert isinstance(ub, dict)
    b = ub.get("m08_long_gpu_training_manifest")
    assert isinstance(b, dict)
    assert b["binding_mode"] == "file_bound"
    assert b.get("m08_manifest_role_readonly") == "implementation_preflight_manifest_tooling"


def test_m15_binding_fixture_file(tmp_path: Path) -> None:
    d = tmp_path / "m15"
    d.mkdir()
    p = _emit_fixture_m15(d)
    out = tmp_path / "out"
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(out, m15_path=p)
    ub = sealed.get("upstream_bindings")
    assert isinstance(ub, dict)
    b = ub.get("m15_operator_evidence_preflight")
    assert isinstance(b, dict)
    assert b["binding_mode"] == "file_bound"


def test_malformed_m02_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"contract_id": "wrong"}), encoding="utf-8")
    with pytest.raises(ValueError, match="M02 binding"):
        emit_v15_short_gpu_environment_evidence(tmp_path / "o", m02_path=bad)


def test_malformed_m15_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "contract_id": CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
                "operator_evidence_collection_status": "not_started",
                "preflight_gates": [],
                "evidence_sequence": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="M15 binding"):
        parse_m15_operator_evidence_preflight(bad)


def test_cli_fixture_mode(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_short_gpu_environment_evidence",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / FILENAME_SHORT_GPU_ENV_EVIDENCE).is_file()


def test_runtime_doc_non_claims_and_files() -> None:
    rt = REPO_ROOT / "docs" / "runtime" / "v15_short_gpu_environment_evidence_v1.md"
    t = rt.read_text(encoding="utf-8").lower()
    assert "non-claim" in t
    assert "v15_short_gpu_environment_evidence.json" in t


def test_starlab_v15_mentions_m16() -> None:
    v15 = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "V15-M16" in v15
    assert "starlab.v15.short_gpu_environment_evidence.v1" in v15


def test_rights_register_m16_note() -> None:
    rights = (REPO_ROOT / "docs" / "rights_register.md").read_text(encoding="utf-8")
    assert "V15-M16" in rights


def test_fixture_no_operator_collection_implied(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(tmp_path)
    assert sealed.get("operator_local_execution_performed") is False
    assert sealed.get("evidence_status") == "fixture_only"


def test_operator_declared_no_execution(tmp_path: Path) -> None:
    op = tmp_path / "op.json"
    op.write_text(
        json.dumps(
            {
                "environment_summary": {"python_version": "3.12.0"},
                "sc2_environment_summary": {"sc2_client_posture": "declared_not_verified"},
            }
        ),
        encoding="utf-8",
    )
    body = build_short_gpu_environment_body(
        profile=PROFILE_OPERATOR_DECLARED,
        operator_environment_path=op,
        allow_operator_local_execution=False,
        authorize_short_gpu_probe=False,
        device="cuda",
        max_steps=5,
        m02_path=None,
        m07_path=None,
        m08_path=None,
        m15_path=None,
    )
    assert body["operator_local_execution_performed"] is False
    assert body["short_gpu_probe_performed"] is False


def test_probe_requires_dual_guards() -> None:
    with pytest.raises(ValueError, match="dual"):
        build_short_gpu_environment_body(
            profile=PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
            operator_environment_path=None,
            allow_operator_local_execution=False,
            authorize_short_gpu_probe=True,
            device="cpu",
            max_steps=2,
            m02_path=None,
            m07_path=None,
            m08_path=None,
            m15_path=None,
        )


@pytest.mark.skipif(
    not os.environ.get("STARLAB_RUN_M16_LOCAL_PROBE_TEST"),
    reason="Set STARLAB_RUN_M16_LOCAL_PROBE_TEST=1 to run operator-local torch probe test",
)
def test_operator_local_probe_cpu_when_enabled(tmp_path: Path) -> None:
    sealed, _, _, _, _ = emit_v15_short_gpu_environment_evidence(
        tmp_path,
        profile=PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
        allow_operator_local_execution=True,
        authorize_short_gpu_probe=True,
        device="cpu",
        max_steps=2,
    )
    assert sealed["operator_local_execution_performed"] is True
    assert sealed["short_gpu_probe_performed"] is True
    assert sealed["short_gpu_probe_result"] == "success"
