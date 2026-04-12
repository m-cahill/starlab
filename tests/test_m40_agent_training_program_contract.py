"""Tests for M40 agent training program contract emission."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.training.training_program_io import (
    build_agent_training_program_contract,
    write_agent_training_program_contract,
)
from starlab.training.training_program_models import (
    AGENT_TRAINING_PROGRAM_CONTRACT_VERSION,
    CONTRACT_FILENAME,
    REPORT_FILENAME,
    non_claims_v1,
)


def test_contract_deterministic_repeat(tmp_path: Path) -> None:
    write_agent_training_program_contract(tmp_path / "a")
    write_agent_training_program_contract(tmp_path / "b")
    c1 = (tmp_path / "a" / CONTRACT_FILENAME).read_text(encoding="utf-8")
    c2 = (tmp_path / "b" / CONTRACT_FILENAME).read_text(encoding="utf-8")
    assert c1 == c2
    r1 = (tmp_path / "a" / REPORT_FILENAME).read_text(encoding="utf-8")
    r2 = (tmp_path / "b" / REPORT_FILENAME).read_text(encoding="utf-8")
    assert r1 == r2


def test_contract_sha256_matches_payload(tmp_path: Path) -> None:
    write_agent_training_program_contract(tmp_path)
    contract = json.loads((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    digest = contract.pop("contract_sha256")
    assert sha256_hex_of_canonical_json(contract) == digest


def test_contract_required_sections() -> None:
    c = build_agent_training_program_contract()
    assert c["program_version"] == AGENT_TRAINING_PROGRAM_CONTRACT_VERSION
    assert "milestone_sequence" in c
    assert len(c["milestone_sequence"]) == 6
    assert c["milestone_sequence"][0]["milestone"] == "M40"
    assert c["milestone_sequence"][5]["milestone"] == "M45"
    assert "allowed_upstreams" in c
    assert "future_required_artifacts" in c
    assert "ci_policy" in c and c["ci_policy"]["no_gpu_training_in_ci"] is True
    assert "local_training_policy" in c
    assert set(c["non_claims"]) == set(non_claims_v1())
    assert "contract_sha256" in c


def test_report_links_contract(tmp_path: Path) -> None:
    write_agent_training_program_contract(tmp_path)
    contract = json.loads((tmp_path / CONTRACT_FILENAME).read_text(encoding="utf-8"))
    report = json.loads((tmp_path / REPORT_FILENAME).read_text(encoding="utf-8"))
    assert report["contract_sha256"] == contract["contract_sha256"]
    assert report["non_claims"] == contract["non_claims"]
