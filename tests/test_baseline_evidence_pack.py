"""Tests for M25 baseline evidence pack over M21/M22 + M23 + M24 artifacts."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.baselines.emit_heuristic_baseline_suite import write_heuristic_baseline_suite_artifacts
from starlab.baselines.emit_scripted_baseline_suite import write_scripted_baseline_suite_artifacts
from starlab.evaluation.emit_baseline_evidence_pack import (
    write_baseline_evidence_pack_artifacts,
)
from starlab.evaluation.emit_evaluation_diagnostics import write_evaluation_diagnostics_artifacts
from starlab.evaluation.emit_evaluation_tournament import write_evaluation_tournament_artifacts
from starlab.evaluation.evidence_pack_views import build_baseline_evidence_pack_artifacts
from starlab.runs.json_util import canonical_json_dumps

REPO = Path(__file__).resolve().parents[1]
FIX_M21 = REPO / "tests" / "fixtures" / "m21"
FIX_M22 = REPO / "tests" / "fixtures" / "m22"
FIX_M23 = REPO / "tests" / "fixtures" / "m23"
FIX_M24 = REPO / "tests" / "fixtures" / "m24"
FIX_M25 = REPO / "tests" / "fixtures" / "m25"

_M25_EVAL_SOURCES = [
    Path("starlab") / "evaluation" / "evidence_pack_models.py",
    Path("starlab") / "evaluation" / "evidence_pack_views.py",
    Path("starlab") / "evaluation" / "emit_baseline_evidence_pack.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_happy_path_matches_golden() -> None:
    pack, report = build_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
    )
    assert json.loads(canonical_json_dumps(pack)) == json.loads(
        (FIX_M25 / "baseline_evidence_pack.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        (FIX_M25 / "baseline_evidence_pack_report.json").read_text(encoding="utf-8"),
    )


def test_deterministic_rerun() -> None:
    p1, r1 = build_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
    )
    p2, r2 = build_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
    )
    assert canonical_json_dumps(p1) == canonical_json_dumps(p2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_entrant_order_follows_m23_standings() -> None:
    pack, _ = build_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
    )
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    want = [row["entrant_id"] for row in t["standings"]]
    assert [e["entrant_id"] for e in pack["entrants"]] == want


def test_lineage_mismatch_missing_suite(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not covered by supplied"):
        build_baseline_evidence_pack_artifacts(
            suite_paths=[FIX_M21 / "expected_scripted_baseline_suite.json"],
            tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
            diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
        )


def test_diagnostics_mismatch_benchmark_id(tmp_path: Path) -> None:
    dpath = tmp_path / "d.json"
    d = json.loads((FIX_M24 / "expected_evaluation_diagnostics.json").read_text(encoding="utf-8"))
    d["benchmark_id"] = "wrong"
    dpath.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(ValueError, match="benchmark_id"):
        build_baseline_evidence_pack_artifacts(
            suite_paths=[
                FIX_M21 / "expected_scripted_baseline_suite.json",
                FIX_M22 / "expected_heuristic_baseline_suite.json",
            ],
            tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
            diagnostics_path=dpath,
        )


def test_diagnostics_mismatch_entrant_set(tmp_path: Path) -> None:
    dpath = tmp_path / "d.json"
    d = json.loads((FIX_M24 / "expected_evaluation_diagnostics.json").read_text(encoding="utf-8"))
    d["entrant_diagnostics"] = d["entrant_diagnostics"][:-1]
    dpath.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(ValueError, match="entrant_id set"):
        build_baseline_evidence_pack_artifacts(
            suite_paths=[
                FIX_M21 / "expected_scripted_baseline_suite.json",
                FIX_M22 / "expected_heuristic_baseline_suite.json",
            ],
            tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
            diagnostics_path=dpath,
        )


def test_duplicate_suite_subject_coverage(tmp_path: Path) -> None:
    tpath = tmp_path / "t.json"
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    dup = json.loads(json.dumps(t["entrants"][1]))
    dup["entrant_id"] = "synthetic.duplicate::same_subject"
    t["entrants"].append(dup)
    # Break standings / matches — only need duplicate (suite_id, subject_id) on two entrants
    tpath.write_text(json.dumps(t), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate suite subject"):
        build_baseline_evidence_pack_artifacts(
            suite_paths=[
                FIX_M21 / "expected_scripted_baseline_suite.json",
                FIX_M22 / "expected_heuristic_baseline_suite.json",
            ],
            tournament_path=tpath,
            diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
        )


def test_failure_view_projection_zero_win_and_lowest() -> None:
    pack, _ = build_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
    )
    noop = "starlab.scripted_baseline_suite.m21.v1.demo::scripted_m21_noop"
    row = next(e for e in pack["entrants"] if e["entrant_id"] == noop)
    ids = {fv["failure_view_id"] for fv in row["failure_views"]}
    assert "starlab.m25.failure_view.zero_win_entrant" in ids
    assert "starlab.m25.failure_view.lowest_points_entrant" in ids


def test_m25_evaluation_modules_have_no_runtime_stack_imports() -> None:
    root = _repo_root()
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _M25_EVAL_SOURCES:
        text = (root / rel).read_text(encoding="utf-8")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not any(alias.name.startswith(prefix) for prefix in forbidden), (
                        f"{rel}: forbidden import {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                assert node.module is not None
                assert not any(
                    node.module == prefix or node.module.startswith(prefix + ".")
                    for prefix in forbidden
                ), f"{rel}: forbidden import from {node.module}"


def test_cli_success_and_invalid_exit_codes(tmp_path: Path) -> None:
    write_baseline_evidence_pack_artifacts(
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        diagnostics_path=FIX_M24 / "expected_evaluation_diagnostics.json",
        output_dir=tmp_path,
    )
    assert (tmp_path / "baseline_evidence_pack.json").is_file()
    proc_bad = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.evaluation.emit_baseline_evidence_pack",
            "--suite",
            str(FIX_M21 / "expected_scripted_baseline_suite.json"),
            "--tournament",
            str(tmp_path / "nope.json"),
            "--diagnostics",
            str(FIX_M24 / "expected_evaluation_diagnostics.json"),
            "--output-dir",
            str(tmp_path / "out2"),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=_repo_root(),
    )
    assert proc_bad.returncode != 0


def test_e2e_m20_through_m25(tmp_path: Path) -> None:
    """Phase IV chain: contract -> M21 -> M22 -> M23 -> M24 -> M25 evidence pack."""

    contract_path = FIX_M21 / "valid_benchmark_contract.json"
    m21_dir = tmp_path / "m21_out"
    m22_dir = tmp_path / "m22_out"
    m23_dir = tmp_path / "m23_out"
    m24_dir = tmp_path / "m24_out"
    m25_dir = tmp_path / "m25_out"
    write_scripted_baseline_suite_artifacts(
        benchmark_contract_path=contract_path,
        output_dir=m21_dir,
    )
    write_heuristic_baseline_suite_artifacts(
        benchmark_contract_path=contract_path,
        output_dir=m22_dir,
    )
    write_evaluation_tournament_artifacts(
        benchmark_contract_path=contract_path,
        suite_paths=[
            m21_dir / "scripted_baseline_suite.json",
            m22_dir / "heuristic_baseline_suite.json",
        ],
        output_dir=m23_dir,
    )
    write_evaluation_diagnostics_artifacts(
        tournament_path=m23_dir / "evaluation_tournament.json",
        output_dir=m24_dir,
    )
    write_baseline_evidence_pack_artifacts(
        suite_paths=[
            m21_dir / "scripted_baseline_suite.json",
            m22_dir / "heuristic_baseline_suite.json",
        ],
        tournament_path=m23_dir / "evaluation_tournament.json",
        diagnostics_path=m24_dir / "evaluation_diagnostics.json",
        output_dir=m25_dir,
    )
    got = json.loads((m25_dir / "baseline_evidence_pack.json").read_text(encoding="utf-8"))
    want = json.loads((FIX_M25 / "baseline_evidence_pack.json").read_text(encoding="utf-8"))
    assert got["evidence_pack_version"] == want["evidence_pack_version"]
    assert got["benchmark_contract_sha256"] == want["benchmark_contract_sha256"]
    assert [e["entrant_id"] for e in got["entrants"]] == [e["entrant_id"] for e in want["entrants"]]
