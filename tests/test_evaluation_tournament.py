"""Tests for M23 evaluation tournament harness."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.baselines.emit_heuristic_baseline_suite import write_heuristic_baseline_suite_artifacts
from starlab.baselines.emit_scripted_baseline_suite import write_scripted_baseline_suite_artifacts
from starlab.evaluation.emit_evaluation_tournament import (
    build_evaluation_tournament_artifacts,
    write_evaluation_tournament_artifacts,
)
from starlab.evaluation.tournament_harness import run_round_robin_tournament
from starlab.runs.json_util import canonical_json_dumps

REPO = Path(__file__).resolve().parents[1]
FIX_M21 = REPO / "tests" / "fixtures" / "m21"
FIX_M22 = REPO / "tests" / "fixtures" / "m22"
FIX_M23 = REPO / "tests" / "fixtures" / "m23"

_M23_EVAL_SOURCES = [
    Path("starlab") / "evaluation" / "__init__.py",
    Path("starlab") / "evaluation" / "evaluation_runner_models.py",
    Path("starlab") / "evaluation" / "evaluation_runner.py",
    Path("starlab") / "evaluation" / "tournament_harness.py",
    Path("starlab") / "evaluation" / "emit_evaluation_tournament.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_happy_path_matches_golden() -> None:
    t, r = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    assert json.loads(canonical_json_dumps(t)) == json.loads(
        (FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(r)) == json.loads(
        (FIX_M23 / "expected_evaluation_tournament_report.json").read_text(encoding="utf-8"),
    )


def test_deterministic_rerun() -> None:
    a1, r1 = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    a2, r2 = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    assert canonical_json_dumps(a1) == canonical_json_dumps(a2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_invalid_benchmark_contract_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=bad,
            suite_paths=[FIX_M21 / "expected_scripted_baseline_suite.json"],
        )


def test_invalid_benchmark_contract_schema() -> None:
    with pytest.raises(ValueError, match="benchmark contract validation failed"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=FIX_M21 / "invalid_benchmark_contract.json",
            suite_paths=[FIX_M21 / "expected_scripted_baseline_suite.json"],
        )


def test_invalid_suite_json(tmp_path: Path) -> None:
    bad = tmp_path / "suite.json"
    bad.write_text("[1,2]", encoding="utf-8")
    with pytest.raises(ValueError, match="suite artifact must be a JSON object"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
            suite_paths=[bad],
        )


def test_mismatched_benchmark_contract_sha256(tmp_path: Path) -> None:
    suite = json.loads(
        (FIX_M21 / "expected_scripted_baseline_suite.json").read_text(encoding="utf-8"),
    )
    suite["benchmark_contract_sha256"] = "0" * 64
    p = tmp_path / "suite.json"
    p.write_text(canonical_json_dumps(suite), encoding="utf-8")
    with pytest.raises(ValueError, match="benchmark_contract_sha256"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
            suite_paths=[p],
        )


def test_non_fixture_only_benchmark_contract_rejected() -> None:
    with pytest.raises(ValueError, match="measurement_surface"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=FIX_M21 / "benchmark_contract_replay_only.json",
            suite_paths=[FIX_M21 / "expected_scripted_baseline_suite.json"],
        )


def test_non_fixture_only_suite_rejected(tmp_path: Path) -> None:
    suite = json.loads(
        (FIX_M21 / "expected_scripted_baseline_suite.json").read_text(encoding="utf-8"),
    )
    suite["measurement_surface"] = "replay_only"
    p = tmp_path / "suite.json"
    p.write_text(canonical_json_dumps(suite), encoding="utf-8")
    with pytest.raises(ValueError, match="measurement_surface"):
        build_evaluation_tournament_artifacts(
            benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
            suite_paths=[p],
        )


def test_entrant_order_follows_suite_order() -> None:
    t_fwd, _ = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    t_rev, _ = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M22 / "expected_heuristic_baseline_suite.json",
            FIX_M21 / "expected_scripted_baseline_suite.json",
        ],
    )
    fwd_ids = [e["entrant_id"] for e in t_fwd["entrants"]]
    rev_ids = [e["entrant_id"] for e in t_rev["entrants"]]
    assert fwd_ids[:2] != rev_ids[:2]
    assert fwd_ids == [
        "starlab.scripted_baseline_suite.m21.v1.demo::scripted_m21_noop",
        "starlab.scripted_baseline_suite.m21.v1.demo::scripted_m21_fixed",
        "starlab.heuristic_baseline_suite.m22.v1.demo::heuristic_economy_first_v1",
        "starlab.heuristic_baseline_suite.m22.v1.demo::heuristic_pressure_first_v1",
    ]
    assert rev_ids[:2] == [
        "starlab.heuristic_baseline_suite.m22.v1.demo::heuristic_economy_first_v1",
        "starlab.heuristic_baseline_suite.m22.v1.demo::heuristic_pressure_first_v1",
    ]


def test_match_order_round_robin_indices() -> None:
    t, _ = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    ids = [e["entrant_id"] for e in t["entrants"]]
    for m in t["matches"]:
        ia = ids.index(m["entrant_a_id"])
        ib = ids.index(m["entrant_b_id"])
        assert ia < ib
    assert [m["match_id"] for m in t["matches"]] == [
        f"starlab.evaluation_tournament.v1.match.{i:04d}" for i in range(1, 7)
    ]


def test_standings_sorted_by_points_then_tiebreak_then_id() -> None:
    t, _ = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    ranks = [s["rank"] for s in t["standings"]]
    assert ranks == [1, 2, 3, 4]
    pts = [s["points"] for s in t["standings"]]
    assert pts == sorted(pts, reverse=True)


def test_standings_tiebreak_lexicographic_entrant_id() -> None:
    """Synthetic two-entrant tournament: equal points and primary value -> entrant_id wins."""

    contract = json.loads((FIX_M21 / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    sc_a = json.loads(
        (FIX_M21 / "expected_scripted_baseline_suite.json").read_text(encoding="utf-8"),
    )["scorecards"][0]
    sc_b = json.loads(
        (FIX_M21 / "expected_scripted_baseline_suite.json").read_text(encoding="utf-8"),
    )["scorecards"][1]
    for sc in (sc_a, sc_b):
        for row in sc["metric_rows"]:
            if row["metric_id"] == "m1":
                row["value"] = 5
            if row["metric_id"] == "m2":
                row["value"] = 0.1
    entrants = [
        {
            "entrant_id": "z_suite::s1",
            "source_scorecard_ref": {},
            "subject_id": "s1",
            "subject_kind": "scripted",
            "suite_id": "z_suite",
        },
        {
            "entrant_id": "a_suite::s2",
            "source_scorecard_ref": {},
            "subject_id": "s2",
            "subject_kind": "scripted",
            "suite_id": "a_suite",
        },
    ]
    by_entrant = {
        "z_suite::s1": sc_a,
        "a_suite::s2": sc_b,
    }
    matches, standings = run_round_robin_tournament(
        benchmark_contract=contract,
        entrants=entrants,
        scorecards_by_entrant=by_entrant,
    )
    assert matches[0]["result"] == "draw"
    assert standings[0]["points"] == 0.5
    assert standings[1]["points"] == 0.5
    assert standings[0]["entrant_id"] == "a_suite::s2"
    assert standings[1]["entrant_id"] == "z_suite::s1"


def test_sorted_warnings_and_non_claims() -> None:
    t, r = build_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
    )
    assert t["warnings"] == sorted(t["warnings"])
    assert t["non_claims"] == sorted(t["non_claims"])
    assert r["warnings"] == sorted(r["warnings"])
    assert r["non_claims"] == sorted(r["non_claims"])


def test_cli_success_and_invalid_exit_codes(tmp_path: Path) -> None:
    write_evaluation_tournament_artifacts(
        benchmark_contract_path=FIX_M21 / "valid_benchmark_contract.json",
        suite_paths=[
            FIX_M21 / "expected_scripted_baseline_suite.json",
            FIX_M22 / "expected_heuristic_baseline_suite.json",
        ],
        output_dir=tmp_path,
    )
    assert (tmp_path / "evaluation_tournament.json").is_file()
    proc_bad = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.evaluation.emit_evaluation_tournament",
            "--benchmark-contract",
            str(FIX_M21 / "invalid_benchmark_contract.json"),
            "--suite",
            str(FIX_M21 / "expected_scripted_baseline_suite.json"),
            "--output-dir",
            str(tmp_path / "out2"),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=_repo_root(),
    )
    assert proc_bad.returncode != 0


def test_m23_evaluation_modules_have_no_runtime_stack_imports() -> None:
    root = _repo_root()
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _M23_EVAL_SOURCES:
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


def test_e2e_m20_m21_m22_emitters_feed_m23(tmp_path: Path) -> None:
    """Phase IV chain: contract -> M21 suite -> M22 suite -> M23 tournament."""

    contract_path = FIX_M21 / "valid_benchmark_contract.json"
    m21_dir = tmp_path / "m21_out"
    m22_dir = tmp_path / "m22_out"
    m23_dir = tmp_path / "m23_out"
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
    got = json.loads((m23_dir / "evaluation_tournament.json").read_text(encoding="utf-8"))
    want = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    assert got["tournament_id"] == want["tournament_id"]
    assert got["benchmark_contract_sha256"] == want["benchmark_contract_sha256"]
    assert [e["entrant_id"] for e in got["entrants"]] == [e["entrant_id"] for e in want["entrants"]]
    assert got["matches"] == want["matches"]
    assert got["standings"] == want["standings"]
    for gsi, wsi in zip(got["suite_inputs"], want["suite_inputs"], strict=True):
        assert gsi["suite_id"] == wsi["suite_id"]
        assert gsi["suite_sha256"] == wsi["suite_sha256"]
        assert gsi["suite_version"] == wsi["suite_version"]
