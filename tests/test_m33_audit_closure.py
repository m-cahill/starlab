"""M33 audit-closure wiring: CI tiering, field-test CI artifact, docs, governance tests."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_ci_workflow_has_parallel_tiers_and_governance_aggregate() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert wf.strip().startswith("name: CI\n")
    for job in ("quality:", "smoke:", "tests:", "security:", "fieldtest:", "governance:"):
        assert job in wf, f"missing job: {job}"
    assert "needs: [quality, smoke, tests, security, fieldtest]" in wf
    assert "continue-on-error" not in wf


def test_ci_workflow_fieldtest_uploads_directory_artifact() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "make fieldtest" in wf
    assert "out/fieldtest/replay_explorer_surface.json" in wf
    assert "out/fieldtest/replay_explorer_surface_report.json" in wf
    assert "name: fieldtest-output" in wf
    assert "path: out/fieldtest/" in wf
    assert "if-no-files-found: error" in wf


def test_ci_workflow_tests_job_retains_coverage_and_junit() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "--cov=starlab" in wf
    assert "--junitxml=pytest-junit.xml" in wf
    assert "coverage.xml" in wf
    assert "pytest-junit.xml" in wf


def test_ci_workflow_smoke_emits_junit_artifact() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "-m smoke" in wf
    assert "pytest-smoke-junit.xml" in wf
    assert "pytest-smoke-junit-xml" in wf


def test_ci_workflow_actions_remain_sha_pinned() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert re.search(r"actions/checkout@[0-9a-f]{40}", wf)
    assert re.search(r"actions/setup-python@[0-9a-f]{40}", wf)
    assert re.search(r"actions/upload-artifact@[0-9a-f]{40}", wf)
    assert re.search(r"gitleaks/gitleaks-action@[0-9a-f]{40}", wf)


def test_coverage_gate_unchanged_m33() -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "fail_under = 75.4" in text


def test_runtime_ci_tiering_contract_exists() -> None:
    p = REPO_ROOT / "docs" / "runtime" / "ci_tiering_field_test_readiness_v1.md"
    assert p.is_file()
    body = p.read_text(encoding="utf-8")
    assert "governance" in body
    assert "fieldtest-output" in body


def test_field_test_session_template_exists() -> None:
    p = REPO_ROOT / "docs" / "diligence" / "field_test_session_template.md"
    assert p.is_file()
    assert "Checkout SHA" in p.read_text(encoding="utf-8")


def test_architecture_doc_links_ci_tiering_and_boundaries() -> None:
    body = (REPO_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "ci_tiering_field_test_readiness_v1.md" in body
    assert "untrusted" in body.lower()
    assert "Milestone-to-package map" in body


def test_operating_manual_links_ci_tiers_and_deferred_registry() -> None:
    body = (REPO_ROOT / "docs" / "starlab_operating_manual_v0.md").read_text(encoding="utf-8")
    assert "ci_tiering_field_test_readiness_v1.md" in body
    assert "DeferredIssuesRegistry.md" in body


def test_ledger_m35_stub_and_m34_predecessor_surfaces() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "M35" in section
    assert "M34" in section
    assert "M33" in section
    assert "fieldtest-output" in section or "fieldtest" in section
    assert (
        "ci_tiering_field_test_readiness_v1.md" in section
        or "CI tiering" in section
        or "Audit Closure II" in section
    )


def test_no_m34_m35_product_creep_paths() -> None:
    """M33 must not add flagship proof-pack product modules."""
    assert not (REPO_ROOT / "starlab" / "flagship").exists()
    assert not (REPO_ROOT / "starlab" / "proof_pack").exists()


def test_m33_plan_is_complete_charter() -> None:
    plan = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M33" / "M33_plan.md"
    body = plan.read_text(encoding="utf-8")
    assert len(body) > 800
    assert "Acceptance criteria" in body
    assert "governance" in body.lower()
    assert "Complete on `main`" in body


def test_m35_plan_stub_exists() -> None:
    plan = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M35" / "M35_plan.md"
    assert plan.is_file()
    assert "M35" in plan.read_text(encoding="utf-8")
