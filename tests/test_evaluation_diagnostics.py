"""Tests for M24 evaluation diagnostics over M23 tournament artifacts."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.baselines.emit_heuristic_baseline_suite import write_heuristic_baseline_suite_artifacts
from starlab.baselines.emit_scripted_baseline_suite import write_scripted_baseline_suite_artifacts
from starlab.evaluation.diagnostics_views import (
    _tiebreak_scalar_decided_rank,
    load_tournament_json,
    validate_tournament_for_diagnostics,
)
from starlab.evaluation.emit_evaluation_diagnostics import (
    build_evaluation_diagnostics_artifacts,
    write_evaluation_diagnostics_artifacts,
)
from starlab.evaluation.emit_evaluation_tournament import write_evaluation_tournament_artifacts
from starlab.runs.json_util import canonical_json_dumps

REPO = Path(__file__).resolve().parents[1]
FIX_M21 = REPO / "tests" / "fixtures" / "m21"
FIX_M22 = REPO / "tests" / "fixtures" / "m22"
FIX_M23 = REPO / "tests" / "fixtures" / "m23"
FIX_M24 = REPO / "tests" / "fixtures" / "m24"

_M24_EVAL_SOURCES = [
    Path("starlab") / "evaluation" / "diagnostics_models.py",
    Path("starlab") / "evaluation" / "diagnostics_views.py",
    Path("starlab") / "evaluation" / "emit_evaluation_diagnostics.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_happy_path_matches_golden() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, r = build_evaluation_diagnostics_artifacts(t)
    assert json.loads(canonical_json_dumps(d)) == json.loads(
        (FIX_M24 / "expected_evaluation_diagnostics.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(r)) == json.loads(
        (FIX_M24 / "expected_evaluation_diagnostics_report.json").read_text(encoding="utf-8"),
    )


def test_deterministic_rerun() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d1, r1 = build_evaluation_diagnostics_artifacts(t)
    d2, r2 = build_evaluation_diagnostics_artifacts(t)
    assert canonical_json_dumps(d1) == canonical_json_dumps(d2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        load_tournament_json(bad)


def test_structurally_invalid_tournament() -> None:
    with pytest.raises(ValueError, match="missing required keys"):
        validate_tournament_for_diagnostics(
            {"tournament_version": "starlab.evaluation_tournament.v1"},
        )


def test_wrong_measurement_surface() -> None:
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    t["measurement_surface"] = "replay_only"
    with pytest.raises(ValueError, match="measurement_surface"):
        validate_tournament_for_diagnostics(t)


def test_wrong_evaluation_posture() -> None:
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    t["evaluation_posture"] = "replay_only"
    with pytest.raises(ValueError, match="evaluation_posture"):
        validate_tournament_for_diagnostics(t)


def test_wrong_tournament_version() -> None:
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    t["tournament_version"] = "other"
    with pytest.raises(ValueError, match="tournament_version"):
        validate_tournament_for_diagnostics(t)


def test_standings_entrant_mismatch() -> None:
    t = json.loads((FIX_M23 / "expected_evaluation_tournament.json").read_text(encoding="utf-8"))
    t["standings"] = t["standings"][:-1]
    with pytest.raises(ValueError, match="standings length"):
        validate_tournament_for_diagnostics(t)


def test_entrant_diagnostics_order_matches_tournament_entrants() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, _ = build_evaluation_diagnostics_artifacts(t)
    assert [e["entrant_id"] for e in t["entrants"]] == [
        e["entrant_id"] for e in d["entrant_diagnostics"]
    ]


def test_match_diagnostics_order_matches_tournament_matches() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, _ = build_evaluation_diagnostics_artifacts(t)
    assert [m["match_id"] for m in t["matches"]] == [m["match_id"] for m in d["match_diagnostics"]]


def test_standing_explanation_adjacent_tiebreak() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, _ = build_evaluation_diagnostics_artifacts(t)
    exp = d["standing_explanations"]
    assert exp[0]["adjacent_comparison"]["separated_by"] == "higher_points"
    assert exp[-1]["adjacent_comparison"] is None


def test_failure_views_zero_wins_and_lowest_points_main_golden() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, _ = build_evaluation_diagnostics_artifacts(t)
    fv = d["failure_views"]
    assert fv["draws_equal_primary_metric"] == []
    assert fv["standings_used_lexicographic_tiebreak"] == []
    assert fv["standings_used_tiebreak_scalar"] == []
    noop = "starlab.scripted_baseline_suite.m21.v1.demo::scripted_m21_noop"
    assert fv["zero_win_entrants"] == [{"entrant_id": noop}]
    assert fv["lowest_points_entrants"] == [{"entrant_id": noop}]


def test_synthetic_draw_fixture_failure_views() -> None:
    t = load_tournament_json(FIX_M24 / "synthetic_tournament_draw.json")
    d, r = build_evaluation_diagnostics_artifacts(t)
    fv = d["failure_views"]
    assert len(fv["draws_equal_primary_metric"]) == 1
    assert len(fv["standings_used_lexicographic_tiebreak"]) == 2
    assert r["failure_view_count"] == 7


def test_tiebreak_scalar_flag_unit() -> None:
    standings = [
        {"entrant_id": "b", "points": 1.0, "primary_metric_tiebreak_scalar": 9.0},
        {"entrant_id": "c", "points": 1.0, "primary_metric_tiebreak_scalar": 8.0},
    ]
    assert _tiebreak_scalar_decided_rank(standings[0], standings) is True
    assert _tiebreak_scalar_decided_rank(standings[1], standings) is True
    solo = [{"entrant_id": "x", "points": 1.0, "primary_metric_tiebreak_scalar": 1.0}]
    assert _tiebreak_scalar_decided_rank(solo[0], solo) is False


def test_sorted_warnings_and_non_claims() -> None:
    t = load_tournament_json(FIX_M23 / "expected_evaluation_tournament.json")
    d, r = build_evaluation_diagnostics_artifacts(t)
    assert d["warnings"] == sorted(d["warnings"])
    assert d["non_claims"] == sorted(d["non_claims"])
    assert r["warnings"] == sorted(r["warnings"])
    assert r["non_claims"] == sorted(r["non_claims"])


def test_cli_success_and_invalid_exit_codes(tmp_path: Path) -> None:
    write_evaluation_diagnostics_artifacts(
        tournament_path=FIX_M23 / "expected_evaluation_tournament.json",
        output_dir=tmp_path,
    )
    assert (tmp_path / "evaluation_diagnostics.json").is_file()
    proc_bad = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.evaluation.emit_evaluation_diagnostics",
            "--tournament",
            str(tmp_path / "nope.json"),
            "--output-dir",
            str(tmp_path / "out2"),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=_repo_root(),
    )
    assert proc_bad.returncode != 0


def test_m24_evaluation_modules_have_no_runtime_stack_imports() -> None:
    root = _repo_root()
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _M24_EVAL_SOURCES:
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


def test_e2e_m20_through_m24(tmp_path: Path) -> None:
    """Phase IV chain: contract -> M21 suite -> M22 suite -> M23 tournament -> M24 diagnostics."""

    contract_path = FIX_M21 / "valid_benchmark_contract.json"
    m21_dir = tmp_path / "m21_out"
    m22_dir = tmp_path / "m22_out"
    m23_dir = tmp_path / "m23_out"
    m24_dir = tmp_path / "m24_out"
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
    got = json.loads((m24_dir / "evaluation_diagnostics.json").read_text(encoding="utf-8"))
    want_path = FIX_M24 / "expected_evaluation_diagnostics.json"
    want = json.loads(want_path.read_text(encoding="utf-8"))
    assert got["diagnostics_version"] == want["diagnostics_version"]
    assert got["tournament_id"] == want["tournament_id"]
    assert got["benchmark_contract_sha256"] == want["benchmark_contract_sha256"]
    assert [e["entrant_id"] for e in got["entrant_diagnostics"]] == [
        e["entrant_id"] for e in want["entrant_diagnostics"]
    ]
