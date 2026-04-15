"""M55 benchmark integrity charter (fixture-only; no verdicts or gates)."""

from __future__ import annotations

from pathlib import Path

from starlab.benchmark_integrity.benchmark_integrity_charter import (
    build_benchmark_integrity_charter_artifact,
    build_benchmark_integrity_charter_report,
)
from starlab.benchmark_integrity.benchmark_integrity_controls import split_governance_controls
from starlab.benchmark_integrity.benchmark_integrity_models import (
    CONTRACT_ID,
    CONTROL_FAMILY_ORDER,
    EVIDENCE_CLASSES_RESERVED_FOR_M56,
)
from starlab.benchmark_integrity.emit_benchmark_integrity_charter import (
    write_benchmark_integrity_charter_artifacts,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_emit_benchmark_integrity_charter_is_deterministic(tmp_path: Path) -> None:
    p1 = write_benchmark_integrity_charter_artifacts(tmp_path / "a")
    p2 = write_benchmark_integrity_charter_artifacts(tmp_path / "b")
    assert p1[0].read_text(encoding="utf-8") == p2[0].read_text(encoding="utf-8")
    assert p1[1].read_text(encoding="utf-8") == p2[1].read_text(encoding="utf-8")


def test_charter_contains_contract_schema_milestone_and_non_claims() -> None:
    obj = build_benchmark_integrity_charter_artifact()
    assert obj["contract_id"] == CONTRACT_ID
    assert obj["schema_version"] == CONTRACT_ID
    assert obj["milestone"] == "M55"
    assert obj["phase"] == "VII"
    assert obj["charter_status"] == "charter_only"
    assert "non_claims" in obj
    joined = "\n".join(obj["non_claims"]).lower()
    assert "not yet proved" in joined
    assert "reproducibility" in joined or "no reproducibility" in joined
    assert "live sc2" in joined
    assert "ladder" in joined or "public performance" in joined
    assert "m52" in joined or "m54" in joined or "replay" in joined


def test_report_charter_sha256_matches_canonical_charter() -> None:
    charter = build_benchmark_integrity_charter_artifact()
    report = build_benchmark_integrity_charter_report(charter_obj=charter)
    assert report["charter_canonical_sha256"] == sha256_hex_of_canonical_json(charter)


def test_control_ids_unique_and_families_complete() -> None:
    controls = split_governance_controls()
    ids = [c["control_id"] for c in controls]
    assert len(ids) == len(set(ids)) == 6
    families = [c["control_family"] for c in controls]
    assert families == list(CONTROL_FAMILY_ORDER)


def test_m56_evidence_classes_explicit() -> None:
    charter = build_benchmark_integrity_charter_artifact()
    ev = charter["evidence_classes_reserved_for_m56"]
    assert ev == list(EVIDENCE_CLASSES_RESERVED_FOR_M56)
    assert "benchmark_contract_identity" in ev
    assert "score_aggregation_reproducibility" in ev


def test_report_counts_and_m56_boundary() -> None:
    charter = build_benchmark_integrity_charter_artifact()
    report = build_benchmark_integrity_charter_report(charter_obj=charter)
    assert report["control_family_count"] == 6
    assert report["non_claim_count"] == len(charter["non_claims"])
    assert report["m56_evidence_class_count"] == len(EVIDENCE_CLASSES_RESERVED_FOR_M56)
    boundary = report["m56_boundary"]
    assert "summary" in boundary
    assert "reserved_for_m56" in boundary
    assert "m56" in boundary["summary"].lower()
    blob = (str(boundary) + report.get("notes", "")).lower()
    assert "gate" in blob or "m56" in blob


def test_cli_writes_exact_filenames(tmp_path: Path) -> None:
    write_benchmark_integrity_charter_artifacts(tmp_path)
    names = sorted(p.name for p in tmp_path.iterdir())
    assert names == ["benchmark_integrity_charter.json", "benchmark_integrity_charter_report.json"]


def test_ledger_m55_m56_benchmark_integrity_governance() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "M55" in text and "Benchmark integrity" in text
    assert "benchmark-integrity charter" in text.lower() or "Benchmark integrity charter" in text
    assert "M56" in text and "reproducibility" in text.lower()
    assert "M52" in text and "M54" in text and "Replay↔execution equivalence" in text
    assert "not yet proved" in text.lower() and "benchmark integrity" in text.lower()


def test_ledger_benchmark_integrity_not_equivalence_collapse() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Phase VII track separation" in text
    assert "not" in text.lower() and "substitute" in text.lower() and "M52" in text
    assert "replay↔execution equivalence" in text
    sec7 = text.split("## 7. Milestone table")[1].split("## 8")[0]
    assert "| M55 |" in sec7 and "Benchmark Integrity Charter" in sec7
    assert "| M56 |" in sec7 and "Benchmark Integrity Evidence" in sec7


def test_phase_vii_has_m55_m56_track_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "#### Benchmark integrity track" in text
    sec = text.split("#### Benchmark integrity track")[1].split(
        "#### Phase VII track separation"
    )[0]
    assert "M55" in sec and "M56" in sec
    assert "charter" in sec.lower() and "controls" in sec.lower()
    assert "evidence" in sec.lower() and "reproducibility" in sec.lower()
