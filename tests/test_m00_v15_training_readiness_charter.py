"""V15-M00: training readiness charter deterministic JSON."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.training_readiness_charter_io import (
    build_training_readiness_charter_body,
    emit_training_readiness_charter,
    seal_training_readiness_charter,
)
from starlab.v15.training_readiness_charter_models import TRAINING_READINESS_CHARTER_VERSION


def test_training_readiness_charter_seal_stable() -> None:
    body = build_training_readiness_charter_body()
    sealed = seal_training_readiness_charter(body)
    assert sealed["training_readiness_charter_sha256"] == sha256_hex_of_canonical_json(body)
    assert sealed["charter_version"] == TRAINING_READINESS_CHARTER_VERSION


def test_training_readiness_charter_golden_sha256() -> None:
    """Bump intentionally if charter content changes."""

    body = build_training_readiness_charter_body()
    sealed = seal_training_readiness_charter(body)
    assert sealed["training_readiness_charter_sha256"] == (
        "eb33c3ad0167dafb87bd05e2dfc10bc75bda8c9768fbc03b35469cb2f8a5e82e"
    )


def test_emit_training_readiness_charter_writes_files(tmp_path: Path) -> None:
    _sealed, _rep, c_path, r_path = emit_training_readiness_charter(tmp_path)
    assert c_path.is_file() and r_path.is_file()
    assert c_path.name == "v15_training_readiness_charter.json"
    text = c_path.read_text(encoding="utf-8")
    assert "training_readiness_charter_sha256" in text
    assert "long_gpu_run_gates" in text


@pytest.mark.parametrize(
    "key",
    (
        "long_gpu_run_gates",
        "artifact_family_contract_ids",
        "non_claims",
        "evaluation_ladder",
        "xai_demonstration_surfaces",
    ),
)
def test_charter_required_top_level_keys(key: str) -> None:
    body = build_training_readiness_charter_body()
    assert key in body


def test_emit_v15_training_readiness_charter_cli_help() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "starlab.v15.emit_v15_training_readiness_charter", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "v15_training_readiness_charter" in proc.stdout
