"""V15-M01: training asset registers deterministic JSON + public docs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.training_asset_register_io import (
    build_training_asset_registers_body,
    emit_training_asset_registers,
    seal_training_asset_registers,
)
from starlab.v15.training_asset_register_models import (
    ASSET_CLASSES_V1,
    CLAIM_USE_VOCABULARY_V1,
    TRAINING_ASSET_REGISTERS_CONTRACT_VERSION,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

_REGISTER_DOC_PATHS = (
    "docs/training_asset_register.md",
    "docs/replay_corpus_register.md",
    "docs/model_weight_register.md",
    "docs/checkpoint_asset_register.md",
    "docs/human_benchmark_register.md",
    "docs/xai_evidence_register.md",
    "docs/rights_register.md",
)


def test_training_asset_registers_seal_stable() -> None:
    body = build_training_asset_registers_body()
    sealed = seal_training_asset_registers(body)
    assert sealed["training_asset_registers_sha256"] == sha256_hex_of_canonical_json(body)
    assert sealed["contract_id"] == TRAINING_ASSET_REGISTERS_CONTRACT_VERSION


def test_training_asset_registers_golden_sha256() -> None:
    """Bump intentionally if register contract content changes."""

    body = build_training_asset_registers_body()
    sealed = seal_training_asset_registers(body)
    assert sealed["training_asset_registers_sha256"] == (
        "14118169d640e7b64b8fa59c5fecf91c5184655556790f56db0ace947db48acc"
    )


def test_emit_training_asset_registers_writes_files(tmp_path: Path) -> None:
    sealed, rep, c_path, r_path = emit_training_asset_registers(tmp_path)
    assert c_path.is_file() and r_path.is_file()
    assert c_path.name == "v15_training_asset_registers.json"
    assert r_path.name == "v15_training_asset_registers_report.json"
    assert rep["training_asset_registers_sha256"] == sealed["training_asset_registers_sha256"]
    loaded = json.loads(c_path.read_text(encoding="utf-8"))
    assert loaded["contract_id"] == TRAINING_ASSET_REGISTERS_CONTRACT_VERSION
    report = json.loads(r_path.read_text(encoding="utf-8"))
    assert report["validation"]["contract_id_recognized"] is True


def test_emit_training_asset_registers_is_deterministic(
    tmp_path: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    a = tmp_path_factory.mktemp("a")
    b = tmp_path_factory.mktemp("b")
    emit_training_asset_registers(a)
    emit_training_asset_registers(b)
    p1 = (a / "v15_training_asset_registers.json").read_text(encoding="utf-8")
    p2 = (b / "v15_training_asset_registers.json").read_text(encoding="utf-8")
    assert p1 == p2


@pytest.mark.parametrize("relative", _REGISTER_DOC_PATHS)
def test_m01_public_register_doc_exists(relative: str) -> None:
    assert (REPO_ROOT / relative).is_file(), f"missing register doc: {relative}"


def test_m01_contract_lists_asset_classes_and_registers() -> None:
    body = build_training_asset_registers_body()
    assert tuple(body["asset_classes"]) == ASSET_CLASSES_V1
    reg_docs = {r["public_doc"] for r in body["required_registers"]}
    for p in _REGISTER_DOC_PATHS:
        assert p in reg_docs
    for field in (
        "asset_id",
        "claim_use",
        "review_status",
        "rights_posture",
        "storage_posture",
        "sha256_or_hash_reference",
    ):
        assert field in body["required_fields"]


def test_m01_vocabularies_include_expected_values() -> None:
    body = build_training_asset_registers_body()
    assert "first_party" in body["source_kind_vocabulary"]
    assert "repo_public" in body["storage_posture_vocabulary"]
    assert "private" in body["public_private_posture_vocabulary"]
    assert "blizzard_terms_local_only" in body["rights_posture_vocabulary"]
    assert "reference_only" in body["redistribution_posture_vocabulary"]
    assert set(CLAIM_USE_VOCABULARY_V1).issubset(set(body["claim_use_vocabulary"]))
    assert "quarantined" in body["status_vocabulary"]


def test_starlab_v15_authority_mentions_m01_runtime_and_non_claims() -> None:
    text = (REPO_ROOT / "docs" / "starlab-v1.5.md").read_text(encoding="utf-8")
    assert "docs/runtime/v15_training_scale_provenance_asset_registers_v1.md" in text
    assert "starlab.v15.training_asset_registers.v1" in text
    assert "**M01 non-claims:**" in text
    assert "no checkpoint lineage **runtime**" in text
    assert "CVE-2026-3219" in text


def test_starlab_ledger_stays_concise_on_m01() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab-v1.5.md" in text
    assert "### V15-M01 —" in text
    assert text.count("claim_use") <= 2


def test_emit_v15_training_asset_registers_cli_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_training_asset_registers", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "v15_training_asset_registers" in proc.stdout


def test_emit_v15_training_asset_registers_cli_writes_outputs(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_training_asset_registers",
            "--output-dir",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert (tmp_path / "v15_training_asset_registers.json").is_file()
    assert (tmp_path / "v15_training_asset_registers_report.json").is_file()
