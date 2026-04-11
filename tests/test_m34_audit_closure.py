"""M34 audit closure: shared I/O, governance split, Dependabot, DIR-005 docs, manual prep."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_starlab_io_module_exists() -> None:
    p = REPO_ROOT / "starlab" / "_io.py"
    assert p.is_file()
    body = p.read_text(encoding="utf-8")
    assert "def load_json_object(" in body
    assert "def parse_json_object_text(" in body


def test_governance_tests_split_from_monolith() -> None:
    assert not (REPO_ROOT / "tests" / "test_governance.py").exists()
    for name in (
        "test_governance_docs.py",
        "test_governance_ci.py",
        "test_governance_milestones.py",
        "test_governance_runtime.py",
    ):
        assert (REPO_ROOT / "tests" / name).is_file()


def test_dependabot_config_exists() -> None:
    p = REPO_ROOT / ".github" / "dependabot.yml"
    assert p.is_file()
    body = p.read_text(encoding="utf-8")
    assert 'package-ecosystem: "pip"' in body
    assert 'package-ecosystem: "github-actions"' in body
    assert 'interval: "weekly"' in body


def test_dev_dependency_upper_bounds_in_pyproject() -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "ruff>=" in text and "<1" in text
    assert "mypy>=" in text and "<2" in text
    assert "pytest>=" in text and "<9" in text


def test_coverage_gate_unchanged_m34() -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r"fail_under = ([0-9.]+)", text)
    assert m is not None
    assert float(m.group(1)) >= 75.4


def test_operating_manual_promotion_readiness_doc_exists() -> None:
    p = REPO_ROOT / "docs" / "diligence" / "operating_manual_promotion_readiness.md"
    assert p.is_file()
    body = p.read_text(encoding="utf-8")
    assert "does not" in body.lower() or "does **not**" in body
    assert "docs/starlab.md" in body


def test_broad_exception_boundaries_doc_exists() -> None:
    p = REPO_ROOT / "docs" / "audit" / "broad_exception_boundaries.md"
    assert p.is_file()
    assert "s2protocol_adapter.py" in p.read_text(encoding="utf-8")


def test_deferred_registry_records_m34_resolutions() -> None:
    body = (REPO_ROOT / "docs" / "audit" / "DeferredIssuesRegistry.md").read_text(encoding="utf-8")
    assert "## M34 resolutions" in body
    assert "DIR-003" in body
    assert "DIR-004" in body
    assert "DIR-005" in body
    assert "DIR-006" in body


def test_ledger_notes_dir005_resolution_method() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "DIR-005" in text
    assert "documentation" in text.lower() or "confirming" in text.lower()


def test_m34_closeout_artifacts_exist() -> None:
    m34 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M34"
    for name in ("M34_run1.md", "M34_summary.md", "M34_audit.md"):
        assert (m34 / name).is_file()


def test_ci_workflow_topology_unchanged_m34() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert wf.strip().startswith("name: CI\n")
    for job in ("quality:", "smoke:", "tests:", "security:", "fieldtest:", "governance:"):
        assert job in wf
    assert re.search(r"actions/checkout@[0-9a-f]{40}", wf)
