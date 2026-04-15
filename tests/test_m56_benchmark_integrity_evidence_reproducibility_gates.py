"""M56 benchmark integrity evidence + reproducibility gates (fixture-backed; no live SC2)."""

from __future__ import annotations

from pathlib import Path

from starlab.benchmark_integrity.benchmark_integrity_evidence import (
    benchmark_integrity_evidence_bundle,
    build_benchmark_integrity_evidence_artifact,
)
from starlab.benchmark_integrity.benchmark_integrity_gate_evaluation import (
    build_benchmark_integrity_reproducibility_gates_bundle,
)
from starlab.benchmark_integrity.benchmark_integrity_models import (
    BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION,
    EVIDENCE_CLASSES_RESERVED_FOR_M56,
    EVIDENCE_FILENAME,
    EVIDENCE_REPORT_FILENAME,
    M56_GATEPACK_FIXTURE_ONLY_BASELINE_CHAIN_V1,
    M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
    REPRODUCIBILITY_GATES_FILENAME,
    REPRODUCIBILITY_GATES_REPORT_FILENAME,
)
from starlab.benchmark_integrity.emit_benchmark_integrity_evidence import (
    write_benchmark_integrity_evidence_artifacts,
)
from starlab.benchmark_integrity.emit_benchmark_integrity_gates import (
    write_benchmark_integrity_gates_artifacts,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX_M56 = REPO_ROOT / "tests" / "fixtures" / "m56"
HAPPY = FIX_M56 / "happy"


def _paths(subdir: str) -> dict[str, Path]:
    base = FIX_M56 / subdir
    return {
        "scripted_baseline_suite": base / "scripted_baseline_suite.json",
        "heuristic_baseline_suite": base / "heuristic_baseline_suite.json",
        "evaluation_tournament": base / "evaluation_tournament.json",
        "evaluation_diagnostics": base / "evaluation_diagnostics.json",
        "baseline_evidence_pack": base / "baseline_evidence_pack.json",
    }


def test_evidence_emission_deterministic_and_sha_stable(tmp_path: Path) -> None:
    p = _paths("happy")
    a1, r1 = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    a2, r2 = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    assert a1 == a2
    assert r1 == r2
    h = sha256_hex_of_canonical_json(a1)
    assert h == r1["evidence_canonical_sha256"]
    assert h == r2["evidence_canonical_sha256"]


def test_required_evidence_classes_all_present_happy_path() -> None:
    p = _paths("happy")
    ev = build_benchmark_integrity_evidence_artifact(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    classes = [r["evidence_class"] for r in ev["evidence_rows"]]
    assert classes == list(EVIDENCE_CLASSES_RESERVED_FOR_M56)
    assert ev["schema_version"] == BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION


def test_corpus_row_not_applicable_happy_path() -> None:
    p = _paths("happy")
    ev, _ = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    corp = next(
        r for r in ev["evidence_rows"] if r["evidence_class"] == "corpus_provenance_and_promotion"
    )
    assert corp["status"] == "not_applicable"


def test_contract_mismatch_fails_gates() -> None:
    p = _paths("fail_contract_mismatch")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    g, _ = build_benchmark_integrity_reproducibility_gates_bundle(evidence=ev, evidence_report=rep)
    assert g["scope_status"] == "rejected_within_scope"
    failed = [x for x in g["gate_results"] if x["status"] == "fail"]
    assert any("contract_identity" in x["gate_id"] for x in failed)


def test_subject_mismatch_fails_gates() -> None:
    p = _paths("fail_subject_mismatch")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    g, _ = build_benchmark_integrity_reproducibility_gates_bundle(evidence=ev, evidence_report=rep)
    assert g["scope_status"] == "rejected_within_scope"
    assert any(x["status"] == "fail" and "subject" in x["gate_id"] for x in g["gate_results"])


def test_posture_mismatch_fails_gates() -> None:
    p = _paths("fail_posture_mismatch")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    assert any(
        r["evidence_class"] == "execution_posture_receipts" and r["status"] == "missing"
        for r in ev["evidence_rows"]
    )
    g, _ = build_benchmark_integrity_reproducibility_gates_bundle(evidence=ev, evidence_report=rep)
    assert g["scope_status"] == "rejected_within_scope"


def test_score_drift_fails_gates() -> None:
    p = _paths("fail_score_mismatch")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    g, _ = build_benchmark_integrity_reproducibility_gates_bundle(evidence=ev, evidence_report=rep)
    assert g["scope_status"] == "rejected_within_scope"
    assert any(
        x["status"] == "fail" and "diagnostics_and_pack" in x["gate_id"] for x in g["gate_results"]
    )


def test_corpus_implication_fails_gates() -> None:
    p = _paths("fail_corpus_implication")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    corp = next(
        r for r in ev["evidence_rows"] if r["evidence_class"] == "corpus_provenance_and_promotion"
    )
    assert corp["status"] == "present"
    g, _ = build_benchmark_integrity_reproducibility_gates_bundle(
        evidence=ev,
        evidence_report=rep,
    )
    assert g["scope_status"] == "rejected_within_scope"
    assert any(
        x["gate_id"].endswith("corpus_promotion_posture_v1") and x["status"] == "fail"
        for x in g["gate_results"]
    )


def test_gates_emission_deterministic(tmp_path: Path) -> None:
    p = _paths("happy")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    g1, r1 = build_benchmark_integrity_reproducibility_gates_bundle(
        evidence=ev,
        evidence_report=rep,
    )
    g2, r2 = build_benchmark_integrity_reproducibility_gates_bundle(
        evidence=ev,
        evidence_report=rep,
    )
    assert g1 == g2
    assert r1 == r2
    assert sha256_hex_of_canonical_json(g1) == r1["gates_canonical_sha256"]


def test_cli_evidence_writes_expected_files(tmp_path: Path) -> None:
    p = _paths("happy")
    write_benchmark_integrity_evidence_artifacts(
        baseline_evidence_pack=p["baseline_evidence_pack"],
        evaluation_diagnostics=p["evaluation_diagnostics"],
        evaluation_tournament=p["evaluation_tournament"],
        heuristic_baseline_suite=p["heuristic_baseline_suite"],
        output_dir=tmp_path,
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite=p["scripted_baseline_suite"],
    )
    names = sorted(x.name for x in tmp_path.iterdir())
    assert names == sorted([EVIDENCE_FILENAME, EVIDENCE_REPORT_FILENAME])


def test_cli_gates_writes_expected_files(tmp_path: Path) -> None:
    p = _paths("happy")
    ev, rep = benchmark_integrity_evidence_bundle(
        scope_id=M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        scripted_baseline_suite_path=p["scripted_baseline_suite"],
        heuristic_baseline_suite_path=p["heuristic_baseline_suite"],
        evaluation_tournament_path=p["evaluation_tournament"],
        evaluation_diagnostics_path=p["evaluation_diagnostics"],
        baseline_evidence_pack_path=p["baseline_evidence_pack"],
    )
    ev_path = tmp_path / "e" / EVIDENCE_FILENAME
    rep_path = tmp_path / "e" / EVIDENCE_REPORT_FILENAME
    ev_path.parent.mkdir(parents=True, exist_ok=True)

    ev_path.write_text(canonical_json_dumps(ev), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    out = tmp_path / "g"
    write_benchmark_integrity_gates_artifacts(
        evidence_path=ev_path,
        evidence_report_path=rep_path,
        output_dir=out,
    )
    names = sorted(x.name for x in out.iterdir())
    assert names == sorted([REPRODUCIBILITY_GATES_FILENAME, REPRODUCIBILITY_GATES_REPORT_FILENAME])


def test_ledger_m56_benchmark_integrity_governance() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### M57" in text
    assert "### M56" in text
    assert "M55" in text and "closed" in text.lower()
    assert "not yet proved" in text.lower() and "benchmark integrity" in text.lower()
    assert "M52" in text and "M54" in text and "Replay↔execution equivalence" in text
    assert "benchmark_integrity_evidence" in text or "benchmark integrity evidence" in text.lower()
    assert M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1 in text
    assert M56_GATEPACK_FIXTURE_ONLY_BASELINE_CHAIN_V1 in text


def test_phase_vii_benchmark_integrity_scope_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "#### Phase VII bounded benchmark-integrity scopes" in text
    assert "#### Phase VII bounded benchmark-integrity gatepacks" in text
