"""V15-M07 training run receipt tests (fixture, operator_declared, optional local GPU)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.training_run_receipt_io import (
    build_training_run_receipt_body_fixture,
    build_training_run_receipt_report,
    default_authorization_flags,
    emit_v15_training_run_receipt,
    parse_declared_receipt_json,
    seal_training_run_receipt_body,
    sha256_file,
)
from starlab.v15.training_run_receipt_models import (
    CONTRACT_ID_TRAINING_RUN_RECEIPT,
    FILENAME_TRAINING_RUN_RECEIPT,
    PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN,
    REPORT_FILENAME_TRAINING_RUN_RECEIPT,
    SEAL_KEY_TRAINING_RUN_RECEIPT,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_fixture_determinism() -> None:
    a = build_training_run_receipt_body_fixture()
    b = build_training_run_receipt_body_fixture()
    assert a == b
    sa = sha256_hex_of_canonical_json(a)
    sb = sha256_hex_of_canonical_json(b)
    assert sa == sb


def test_fixture_contract_and_profile() -> None:
    body = build_training_run_receipt_body_fixture()
    assert body["contract_id"] == CONTRACT_ID_TRAINING_RUN_RECEIPT
    assert body["profile_id"] == PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN
    assert body["profile"] == "fixture_ci"


def test_fixture_authorization_flags_invariant() -> None:
    body = build_training_run_receipt_body_fixture()
    af = body["authorization_flags"]
    for k, v in default_authorization_flags().items():
        assert af[k] is v
        if k in (
            "long_gpu_run_authorized",
            "strong_agent_claim_authorized",
            "human_benchmark_claim_authorized",
            "benchmark_execution_performed",
            "human_panel_execution_performed",
            "xai_review_performed",
            "v2_authorized",
        ):
            assert af[k] is False


def test_seal_and_report_match() -> None:
    body = build_training_run_receipt_body_fixture()
    sealed = seal_training_run_receipt_body(body)
    rep = build_training_run_receipt_report(sealed, redaction_count=0)
    d = sha256_hex_of_canonical_json(body)
    assert sealed[SEAL_KEY_TRAINING_RUN_RECEIPT] == d
    assert rep["artifact_sha256"] == d


def test_operator_declared_minimal(tmp_path: Path) -> None:
    p = tmp_path / "decl.json"
    p.write_text(
        json.dumps(
            {
                "run_id": "m07_test_decl",
                "profile": "operator_declared",
            }
        ),
        encoding="utf-8",
    )
    data = parse_declared_receipt_json(p)
    assert data["run_id"] == "m07_test_decl"
    out = tmp_path / "o"
    sealed, rep, rc, c_path, r_path = emit_v15_training_run_receipt(
        out,
        profile="operator_declared",
        declared_receipt_path=p,
    )
    assert c_path.is_file() and r_path.is_file()
    assert sealed["authorization_flags"]["long_gpu_run_authorized"] is False
    assert rc >= 0
    assert rep["artifact_sha256"] == sealed[SEAL_KEY_TRAINING_RUN_RECEIPT]


def test_operator_declared_redacts_path_and_email(tmp_path: Path) -> None:
    p = tmp_path / "decl2.json"
    p.write_text(
        json.dumps(
            {
                "run_id": "r2",
                "profile": "operator_declared",
                "operator_notes": "Contact: bad@example.com and C:\\SECRET\\x",
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "o2"
    sealed, _r, _rc, _, _ = emit_v15_training_run_receipt(
        out, profile="operator_declared", declared_receipt_path=p
    )
    raw = json.dumps(sealed)
    assert "bad@example" not in raw
    assert "C:\\\\SECRET" not in raw or "REDACTED" in raw or "<REDACTED" in raw


def test_parse_declared_rejects_list_root_json(tmp_path: Path) -> None:
    p = tmp_path / "l.json"
    p.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="receipt JSON must be a single object"):
        parse_declared_receipt_json(p)

    p3 = tmp_path / "l3.json"
    p3.write_text('{"x": 1}', encoding="utf-8")
    with pytest.raises(ValueError, match="unknown top-level keys"):
        parse_declared_receipt_json(p3)


def test_operator_local_requires_allow() -> None:
    with pytest.raises(ValueError, match="allow-operator-local-execution"):
        emit_v15_training_run_receipt(
            Path("."),
            profile="operator_local_short_gpu",
            allow_operator_local=False,
        )


def test_import_training_run_receipt_io_does_not_import_torch() -> None:
    r = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; from starlab.v15 import training_run_receipt_io; "
                "assert 'torch' not in sys.modules"
            ),
        ],
        cwd=str(REPO_ROOT),
        check=False,
    )
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)


def test_optional_torch_shakedown_if_installed(tmp_path: Path) -> None:
    try:
        import importlib.util

        if importlib.util.find_spec("torch") is None:
            pytest.skip("torch not installed")
    except ModuleNotFoundError:
        pytest.skip("torch not installed")
    d = tmp_path / "r"
    d.mkdir()
    _sealed, _rep, _rc, c, r = emit_v15_training_run_receipt(
        d,
        profile="operator_local_short_gpu",
        allow_operator_local=True,
        run_id="m07_t",
        max_steps=2,
        device="cpu",
    )
    assert c.is_file() and (d / "m07_synthetic_shakedown.pt").is_file()
    h = d / "m07_synthetic_shakedown.pt"
    assert len(sha256_file(h)) == 64


def test_emit_operator_declared_binds_m02_json_sha(tmp_path: Path) -> None:
    m02 = tmp_path / "e.json"
    m02.write_text('{"c":0,"b":0,"a":0}\n', encoding="utf-8")
    decl = tmp_path / "d.json"
    decl.write_text(json.dumps({"run_id": "b", "profile": "operator_declared"}), encoding="utf-8")
    outd = tmp_path / "eout"
    outd.mkdir()
    from starlab.v15.training_run_receipt_io import _json_file_canonical_sha256

    h = _json_file_canonical_sha256(m02)
    sealed, _rep, _rc, _, _ = emit_v15_training_run_receipt(
        outd,
        profile="operator_declared",
        declared_receipt_path=decl,
        environment_lock_path=m02,
    )
    assert sealed["optional_bindings"]["environment_lock_json_canonical_sha256"] == h


def test_cli_fixture_path(tmp_path: Path) -> None:
    d = tmp_path / "o"
    d.mkdir()
    r = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_training_run_receipt", "--output-dir", str(d)],
        cwd=str(REPO_ROOT),
        check=False,
    )
    assert r.returncode == 0
    assert (d / FILENAME_TRAINING_RUN_RECEIPT).is_file()
    assert (d / REPORT_FILENAME_TRAINING_RUN_RECEIPT).is_file()


def test_fixture_output_no_checkpoint_blobs_in_json(tmp_path: Path) -> None:
    d = tmp_path / "f"
    d.mkdir()
    emit_v15_training_run_receipt(d, profile="fixture_ci")
    txt = (d / FILENAME_TRAINING_RUN_RECEIPT).read_text(encoding="utf-8")
    assert ".pt" not in txt
    # no absolute Windows drive paths in fixture
    assert "C:\\" not in txt


def test_optional_binding_env_lock_sha(tmp_path: Path) -> None:
    m02 = tmp_path / "m02.json"
    m02.write_text('{"a":1,"b":2}\n', encoding="utf-8")
    from starlab.v15.training_run_receipt_io import _json_file_canonical_sha256

    exp = _json_file_canonical_sha256(m02)
    body = build_training_run_receipt_body_fixture(
        optional_sha={"environment_lock_json_canonical_sha256": exp},
    )
    assert body["optional_bindings"]["environment_lock_json_canonical_sha256"] == exp
    assert body["optional_bindings"]["checkpoint_lineage_json_canonical_sha256"] is None
