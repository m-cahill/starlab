"""Tests for M21 scripted baseline suite emission."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.baselines.emit_scripted_baseline_suite import write_scripted_baseline_suite_artifacts
from starlab.baselines.scripted_baseline_models import SCRIPTED_BASELINE_SUBJECT_IDS
from starlab.baselines.scripted_baseline_suite import build_scripted_baseline_suite_and_report
from starlab.benchmarks.benchmark_scorecard_schema import validate_benchmark_scorecard
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m21"

_M21_BASELINE_SOURCES = [
    Path("starlab") / "baselines" / "__init__.py",
    Path("starlab") / "baselines" / "scripted_baseline_models.py",
    Path("starlab") / "baselines" / "scripted_baseline_suite.py",
    Path("starlab") / "baselines" / "scripted_baseline_scorecards.py",
    Path("starlab") / "baselines" / "emit_scripted_baseline_suite.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_happy_path_emission_matches_golden() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    suite, report = build_scripted_baseline_suite_and_report(contract)
    assert json.loads(canonical_json_dumps(suite)) == json.loads(
        (FIX / "expected_scripted_baseline_suite.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        (FIX / "expected_scripted_baseline_suite_report.json").read_text(encoding="utf-8"),
    )


def test_invalid_benchmark_contract_fails() -> None:
    contract = json.loads((FIX / "invalid_benchmark_contract.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="benchmark contract validation failed"):
        build_scripted_baseline_suite_and_report(contract)


def test_measurement_surface_not_fixture_only_fails() -> None:
    contract = json.loads((FIX / "benchmark_contract_replay_only.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="measurement_surface"):
        build_scripted_baseline_suite_and_report(contract)


def test_deterministic_golden_stability() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    s1, r1 = build_scripted_baseline_suite_and_report(contract)
    s2, r2 = build_scripted_baseline_suite_and_report(contract)
    assert canonical_json_dumps(s1) == canonical_json_dumps(s2)
    assert canonical_json_dumps(r1) == canonical_json_dumps(r2)


def test_each_embedded_scorecard_validates_against_m20_schema() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    suite, _report = build_scripted_baseline_suite_and_report(contract)
    for sc in suite["scorecards"]:
        assert validate_benchmark_scorecard(sc) == []


def test_metric_row_order_equals_benchmark_metric_order() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    suite, _report = build_scripted_baseline_suite_and_report(contract)
    want = [m["metric_id"] for m in contract["metric_definitions"]]
    for sc in suite["scorecards"]:
        got = [row["metric_id"] for row in sc["metric_rows"]]
        assert want == got


def test_suite_has_two_scripted_subjects() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    suite, report = build_scripted_baseline_suite_and_report(contract)
    assert len(suite["subjects"]) == 2
    assert len(suite["scorecards"]) == 2
    assert report["subject_count"] == 2
    assert report["scorecard_count"] == 2
    for sub in suite["subjects"]:
        assert sub["subject_kind"] == "scripted"
    assert [s["subject_id"] for s in suite["subjects"]] == list(SCRIPTED_BASELINE_SUBJECT_IDS)


def test_benchmark_contract_sha256_matches_canonical_contract() -> None:
    contract = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    want = sha256_hex_of_canonical_json(contract)
    suite, report = build_scripted_baseline_suite_and_report(contract)
    assert suite["benchmark_contract_sha256"] == want
    assert report["benchmark_contract_sha256"] == want
    for sc in suite["scorecards"]:
        assert sc["benchmark_contract_sha256"] == want


def test_cli_writes_both_artifacts(tmp_path: Path) -> None:
    write_scripted_baseline_suite_artifacts(
        benchmark_contract_path=FIX / "valid_benchmark_contract.json",
        output_dir=tmp_path,
    )
    assert (tmp_path / "scripted_baseline_suite.json").is_file()
    assert (tmp_path / "scripted_baseline_suite_report.json").is_file()


def test_cli_invalid_contract_exits_nonzero(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.baselines.emit_scripted_baseline_suite",
            "--benchmark-contract",
            str(FIX / "invalid_benchmark_contract.json"),
            "--output-dir",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=_repo_root(),
    )
    assert proc.returncode != 0


def test_m21_baseline_modules_have_no_runtime_stack_imports() -> None:
    root = _repo_root()
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _M21_BASELINE_SOURCES:
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
