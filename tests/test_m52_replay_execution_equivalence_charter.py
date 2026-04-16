"""M52 replay↔execution equivalence charter (fixture-only; no live SC2)."""

from __future__ import annotations

from pathlib import Path

import pytest
from starlab.equivalence.emit_replay_execution_equivalence_charter import (
    write_replay_execution_equivalence_charter_artifacts,
)
from starlab.equivalence.equivalence_charter import (
    build_replay_execution_equivalence_charter_artifact,
    build_replay_execution_equivalence_charter_report,
)
from starlab.equivalence.equivalence_models import MISMATCH_KINDS_ORDERED
from starlab.runs.json_util import sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_emit_replay_execution_equivalence_charter_is_deterministic(tmp_path: Path) -> None:
    p1 = write_replay_execution_equivalence_charter_artifacts(tmp_path / "a")
    p2 = write_replay_execution_equivalence_charter_artifacts(tmp_path / "b")
    assert p1[0].read_text(encoding="utf-8") == p2[0].read_text(encoding="utf-8")
    assert p1[1].read_text(encoding="utf-8") == p2[1].read_text(encoding="utf-8")


def test_charter_contains_required_fields_and_non_claims() -> None:
    obj = build_replay_execution_equivalence_charter_artifact()
    assert obj["schema_version"] == "starlab.replay_execution_equivalence_charter.v1"
    assert obj["milestone"] == "M52"
    assert "explicit_non_claims" in obj
    claims = "\n".join(obj["explicit_non_claims"])
    assert "Does not prove replay" in claims or "not" in claims.lower()
    assert isinstance(obj["mismatch_taxonomy"], list)
    kinds = [row["kind"] for row in obj["mismatch_taxonomy"]]
    assert kinds == list(MISMATCH_KINDS_ORDERED)


def test_report_charter_sha256_matches_canonical_charter() -> None:
    charter = build_replay_execution_equivalence_charter_artifact()
    report = build_replay_execution_equivalence_charter_report(charter_obj=charter)
    assert report["charter_canonical_sha256"] == sha256_hex_of_canonical_json(charter)


def test_ledger_has_phase_vii_and_milestone_rows_m52_m61() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Phase VII" in text
    assert "Trust, Equivalence, Benchmark Integrity, and Release Lock" in text
    assert "62 milestones (M00–M61)" in text or "62 milestones (M00-M61)" in text
    sec = text.split("## 7. Milestone table")[1].split("## 8")[0]
    assert "| M52 |" in sec
    assert "V1 Endgame Recharter" in sec or "v1 endgame" in sec.lower()
    assert "| M61 |" in sec and "SC2 Foundation Release Lock" in sec
    for mid, frag in (
        ("M53", "Replay↔Execution Equivalence Evidence Surface"),
        ("M54", "Replay↔Execution Equivalence Audit"),
        ("M55", "Benchmark Integrity Charter"),
        ("M56", "Benchmark Integrity Evidence"),
        ("M57", "Narrow Live SC2 in CI Charter"),
        ("M58", "Live SC2 in CI Hardening"),
        ("M59", "Ladder/Public Evaluation Protocol"),
        ("M60", "Audit Hardening"),
    ):
        line = next(line for line in sec.splitlines() if line.strip().startswith(f"| {mid} |"))
        assert frag in line
    m61_line = next(line for line in sec.splitlines() if line.strip().startswith("| M61 |"))
    assert "Complete" in m61_line and "SC2 Foundation Release Lock" in m61_line


def test_intent_map_includes_m52_m61() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    sec = text.split("## 8. Milestone intent map")[1].split("## 9")[0]
    assert "| M52 |" in sec and "| M61 |" in sec


def test_ledger_remaining_v1_proof_track_map() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Remaining v1 proof-track map" in text
    assert "v2" in text.lower() or "**v2**" in text


def test_governance_runtime_contract_listed() -> None:
    docs = (REPO_ROOT / "tests" / "test_governance_docs.py").read_text(encoding="utf-8")
    assert "replay_execution_equivalence_charter_v1.md" in docs


@pytest.mark.smoke
def test_starlab_md_v1_boundary_honest_non_claims() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    scan = text.split("## Current truth")[1].split("## Start Here")[0]
    assert "not" in scan.lower() and "proved" in scan.lower()
    assert "planned" in scan.lower() and "v1" in scan.lower()
