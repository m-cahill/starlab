"""M03 ``seed_from_proof`` CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.seed_from_proof import main as seed_main

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_seed_from_proof_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "starlab.runs.seed_from_proof", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--proof" in result.stdout


def test_seed_from_proof_writes_artifacts(tmp_path: Path) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    argv = [
        "--proof",
        str(proof),
        "--config",
        str(cfg),
        "--output-dir",
        str(tmp_path),
    ]
    assert seed_main(argv) == 0
    ri = tmp_path / "run_identity.json"
    ls = tmp_path / "lineage_seed.json"
    assert ri.is_file()
    assert ls.is_file()
    text_ri = ri.read_text(encoding="utf-8")
    assert "run_spec_id" in text_ri
    assert "starlab.run_identity.v1" in text_ri
    text_ls = ls.read_text(encoding="utf-8")
    assert "lineage_seed_id" in text_ls
    assert "starlab.lineage_seed.v1" in text_ls


def test_seed_from_proof_rejects_bad_hash(tmp_path: Path) -> None:
    good = (FIXTURE_DIR / "m02_match_execution_proof.json").read_text(encoding="utf-8")
    bad = good.replace(
        "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774",
        "0" * 64,
    )
    proof = tmp_path / "bad_proof.json"
    proof.write_text(bad, encoding="utf-8")
    cfg = FIXTURE_DIR / "m02_match_config.json"
    out = tmp_path / "out"
    out.mkdir()
    argv = ["--proof", str(proof), "--config", str(cfg), "--output-dir", str(out)]
    with pytest.raises(ValueError, match="artifact_hash"):
        seed_main(argv)
