"""Tests for M20 benchmark contract + scorecard JSON Schema emission and validation."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest
from starlab.benchmarks.benchmark_contract_models import (
    BENCHMARK_CONTRACT_PROFILE,
    BENCHMARK_SCORECARD_PROFILE,
)
from starlab.benchmarks.benchmark_contract_schema import (
    build_benchmark_contract_json_schema,
    build_benchmark_contract_schema_report,
    validate_benchmark_contract,
)
from starlab.benchmarks.benchmark_scorecard_schema import (
    build_benchmark_scorecard_json_schema,
    build_benchmark_scorecard_schema_report,
    validate_benchmark_scorecard,
)
from starlab.benchmarks.emit_benchmark_contracts import write_benchmark_contract_artifacts
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

FIX = Path(__file__).resolve().parent / "fixtures" / "m20"

_M20_BENCHMARK_SOURCES = [
    Path("starlab") / "benchmarks" / "__init__.py",
    Path("starlab") / "benchmarks" / "benchmark_contract_models.py",
    Path("starlab") / "benchmarks" / "benchmark_contract_schema.py",
    Path("starlab") / "benchmarks" / "benchmark_scorecard_schema.py",
    Path("starlab") / "benchmarks" / "emit_benchmark_contracts.py",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_deterministic_golden_benchmark_contract_schema_emission() -> None:
    expected_path = FIX / "expected_benchmark_contract_schema.json"
    schema = build_benchmark_contract_json_schema()
    assert json.loads(canonical_json_dumps(schema)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_golden_benchmark_scorecard_schema_emission() -> None:
    expected_path = FIX / "expected_benchmark_scorecard_schema.json"
    schema = build_benchmark_scorecard_json_schema()
    assert json.loads(canonical_json_dumps(schema)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_benchmark_contract_schema_report_emission() -> None:
    expected_path = FIX / "expected_benchmark_contract_schema_report.json"
    schema = build_benchmark_contract_json_schema()
    report = build_benchmark_contract_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid_benchmark_contract": FIX / "valid_benchmark_contract.json",
            "invalid_benchmark_contract": FIX / "invalid_benchmark_contract.json",
        },
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_benchmark_scorecard_schema_report_emission() -> None:
    expected_path = FIX / "expected_benchmark_scorecard_schema_report.json"
    schema = build_benchmark_scorecard_json_schema()
    report = build_benchmark_scorecard_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid_benchmark_scorecard": FIX / "valid_benchmark_scorecard.json",
            "invalid_benchmark_scorecard": FIX / "invalid_benchmark_scorecard.json",
        },
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_schema_fingerprints_stable() -> None:
    c = build_benchmark_contract_json_schema()
    s = build_benchmark_scorecard_json_schema()
    assert sha256_hex_of_canonical_json(c) == sha256_hex_of_canonical_json(
        build_benchmark_contract_json_schema(),
    )
    assert sha256_hex_of_canonical_json(s) == sha256_hex_of_canonical_json(
        build_benchmark_scorecard_json_schema(),
    )
    r1 = build_benchmark_contract_schema_report(
        schema_obj=c,
        example_fixture_paths={"valid_benchmark_contract": FIX / "valid_benchmark_contract.json"},
    )
    assert r1["schema_sha256"] == sha256_hex_of_canonical_json(c)
    assert r1["profile"] == BENCHMARK_CONTRACT_PROFILE
    r2 = build_benchmark_scorecard_schema_report(
        schema_obj=s,
        example_fixture_paths={"valid_benchmark_scorecard": FIX / "valid_benchmark_scorecard.json"},
    )
    assert r2["schema_sha256"] == sha256_hex_of_canonical_json(s)
    assert r2["profile"] == BENCHMARK_SCORECARD_PROFILE


def test_valid_benchmark_contract_passes() -> None:
    doc = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    assert validate_benchmark_contract(doc) == []


def test_invalid_benchmark_contract_fails() -> None:
    doc = json.loads((FIX / "invalid_benchmark_contract.json").read_text(encoding="utf-8"))
    errs = validate_benchmark_contract(doc)
    assert errs


def test_valid_benchmark_scorecard_passes() -> None:
    doc = json.loads((FIX / "valid_benchmark_scorecard.json").read_text(encoding="utf-8"))
    assert validate_benchmark_scorecard(doc) == []


def test_invalid_benchmark_scorecard_fails() -> None:
    doc = json.loads((FIX / "invalid_benchmark_scorecard.json").read_text(encoding="utf-8"))
    errs = validate_benchmark_scorecard(doc)
    assert errs


def test_scorecard_benchmark_sha256_matches_canonical_contract_fixture() -> None:
    bench = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    want = sha256_hex_of_canonical_json(bench)
    score = json.loads((FIX / "valid_benchmark_scorecard.json").read_text(encoding="utf-8"))
    assert score["benchmark_contract_sha256"] == want


def test_metric_rows_follow_benchmark_metric_definition_order() -> None:
    bench = json.loads((FIX / "valid_benchmark_contract.json").read_text(encoding="utf-8"))
    score = json.loads((FIX / "valid_benchmark_scorecard.json").read_text(encoding="utf-8"))
    want = [m["metric_id"] for m in bench["metric_definitions"]]
    got = [r["metric_id"] for r in score["metric_rows"]]
    assert want == got


def test_cli_writes_all_four_artifacts(tmp_path: Path) -> None:
    write_benchmark_contract_artifacts(
        tmp_path,
        example_fixture_paths={
            "valid_benchmark_contract": FIX / "valid_benchmark_contract.json",
            "invalid_benchmark_contract": FIX / "invalid_benchmark_contract.json",
            "valid_benchmark_scorecard": FIX / "valid_benchmark_scorecard.json",
            "invalid_benchmark_scorecard": FIX / "invalid_benchmark_scorecard.json",
        },
    )
    assert (tmp_path / "benchmark_contract_schema.json").is_file()
    assert (tmp_path / "benchmark_contract_schema_report.json").is_file()
    assert (tmp_path / "benchmark_scorecard_schema.json").is_file()
    assert (tmp_path / "benchmark_scorecard_schema_report.json").is_file()


def test_m20_benchmark_modules_have_no_runtime_stack_imports() -> None:
    root = _repo_root()
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _M20_BENCHMARK_SOURCES:
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
