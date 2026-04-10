"""Tests for hierarchical agent interface JSON Schema (M29)."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

from starlab.hierarchy.emit_hierarchical_agent_interface import main as emit_main
from starlab.hierarchy.hierarchical_interface_io import (
    build_hierarchical_agent_interface_schema_report,
    write_hierarchical_agent_interface_schema_artifacts,
)
from starlab.hierarchy.hierarchical_interface_models import HIERARCHICAL_AGENT_INTERFACE_PROFILE
from starlab.hierarchy.hierarchical_interface_schema import (
    build_hierarchical_agent_interface_json_schema,
    validate_hierarchical_trace_document,
    validate_hierarchical_trace_file,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX = REPO_ROOT / "tests" / "fixtures" / "m29"

M29_HIERARCHY_MODULES = (
    "hierarchical_interface_models.py",
    "hierarchical_interface_schema.py",
    "hierarchical_interface_io.py",
    "emit_hierarchical_agent_interface.py",
)


def test_deterministic_golden_schema_emission() -> None:
    expected_path = FIX / "expected_hierarchical_agent_interface_schema.json"
    schema = build_hierarchical_agent_interface_json_schema()
    assert json.loads(canonical_json_dumps(schema)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_deterministic_schema_report_emission() -> None:
    expected_path = FIX / "expected_hierarchical_agent_interface_schema_report.json"
    schema = build_hierarchical_agent_interface_json_schema()
    report = build_hierarchical_agent_interface_schema_report(
        schema_obj=schema,
        example_fixture_paths={
            "valid": FIX / "valid_hierarchical_trace.json",
            "invalid_label": FIX / "invalid_hierarchical_trace_bad_label.json",
            "invalid_missing_version": FIX / "invalid_hierarchical_trace_missing_version.json",
        },
    )
    assert json.loads(canonical_json_dumps(report)) == json.loads(
        expected_path.read_text(encoding="utf-8"),
    )


def test_schema_fingerprint_stable() -> None:
    schema = build_hierarchical_agent_interface_json_schema()
    h1 = sha256_hex_of_canonical_json(schema)
    h2 = sha256_hex_of_canonical_json(build_hierarchical_agent_interface_json_schema())
    assert h1 == h2
    report = build_hierarchical_agent_interface_schema_report(
        schema_obj=schema,
        example_fixture_paths={"valid": FIX / "valid_hierarchical_trace.json"},
    )
    assert report["schema_sha256"] == h1
    assert report["profile"] == HIERARCHICAL_AGENT_INTERFACE_PROFILE


def test_valid_trace_passes() -> None:
    assert validate_hierarchical_trace_file(FIX / "valid_hierarchical_trace.json") == []


def test_invalid_label_fails() -> None:
    errs = validate_hierarchical_trace_file(FIX / "invalid_hierarchical_trace_bad_label.json")
    assert any("semantic_coarse_label" in e for e in errs)


def test_missing_schema_version_fails() -> None:
    errs = validate_hierarchical_trace_file(FIX / "invalid_hierarchical_trace_missing_version.json")
    assert any("schema_version" in e for e in errs)


def test_extra_top_level_property_fails() -> None:
    doc = json.loads((FIX / "valid_hierarchical_trace.json").read_text(encoding="utf-8"))
    bad = dict(doc)
    bad["extra"] = 1
    errs = validate_hierarchical_trace_document(bad)
    assert any("additional properties" in e.lower() or "additionalProperties" in e for e in errs)


def test_e2e_emit_cli_matches_goldens(tmp_path: Path) -> None:
    """CLI emit with example fixtures matches checked-in expected report."""

    out = tmp_path / "out"
    code = emit_main(
        [
            "--output-dir",
            str(out),
            "--example-fixture",
            f"valid={FIX / 'valid_hierarchical_trace.json'}",
            "--example-fixture",
            f"invalid_label={FIX / 'invalid_hierarchical_trace_bad_label.json'}",
            "--example-fixture",
            f"invalid_missing_version={FIX / 'invalid_hierarchical_trace_missing_version.json'}",
        ],
    )
    assert code == 0
    exp_schema = json.loads(
        (FIX / "expected_hierarchical_agent_interface_schema.json").read_text(),
    )
    exp_rep_path = FIX / "expected_hierarchical_agent_interface_schema_report.json"
    exp_report = json.loads(exp_rep_path.read_text(encoding="utf-8"))
    got_sch_path = out / "hierarchical_agent_interface_schema.json"
    got_schema = json.loads(got_sch_path.read_text(encoding="utf-8"))
    got_report = json.loads(
        (out / "hierarchical_agent_interface_schema_report.json").read_text(encoding="utf-8"),
    )
    assert got_schema == exp_schema
    assert got_report == exp_report


def test_write_artifacts_idempotent(tmp_path: Path) -> None:
    write_hierarchical_agent_interface_schema_artifacts(tmp_path)
    a1 = (tmp_path / "hierarchical_agent_interface_schema.json").read_text(encoding="utf-8")
    shutil.rmtree(tmp_path)
    write_hierarchical_agent_interface_schema_artifacts(tmp_path)
    a2 = (tmp_path / "hierarchical_agent_interface_schema.json").read_text(encoding="utf-8")
    assert a1 == a2


def test_module_ast_import_guard() -> None:
    """M29 hierarchy modules must not depend on replay/SC2/parser stacks."""

    pkg = REPO_ROOT / "starlab" / "hierarchy"
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for name in M29_HIERARCHY_MODULES:
        path = pkg / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        found: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden or any(
                        alias.name == f or alias.name.startswith(f + ".") for f in forbidden
                    ):
                        found.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                mod = node.module
                if mod in forbidden or any(mod == f or mod.startswith(f + ".") for f in forbidden):
                    found.append(mod)
        assert not found, f"{name} forbidden imports: {found}"


def test_python_m_emit_entrypoint() -> None:
    """``python -m starlab.hierarchy.emit_hierarchical_agent_interface`` exits 0."""

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.hierarchy.emit_hierarchical_agent_interface",
            "--output-dir",
            str(REPO_ROOT / "tests" / "fixtures" / "m29" / "_tmp_emit_check"),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    shutil.rmtree(REPO_ROOT / "tests" / "fixtures" / "m29" / "_tmp_emit_check", ignore_errors=True)
