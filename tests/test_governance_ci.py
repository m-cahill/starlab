"""Governance tests: ledger, CI wiring, and high-signal smoke checks."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_starlab_ledger_exists() -> None:
    ledger = REPO_ROOT / "docs" / "starlab.md"
    assert ledger.is_file()


@pytest.mark.smoke
def test_ledger_names_deployment_targets() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Netlify" in text
    assert "Render" in text


@pytest.mark.smoke
def test_milestone_m00_directory_exists() -> None:
    m00 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M00"
    assert m00.is_dir()


@pytest.mark.smoke
def test_rights_register_exists() -> None:
    path = REPO_ROOT / "docs" / "rights_register.md"
    assert path.is_file()


@pytest.mark.smoke
def test_ci_workflow_exists() -> None:
    wf = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file()


@pytest.mark.smoke
def test_pyproject_exists() -> None:
    assert (REPO_ROOT / "pyproject.toml").is_file()


@pytest.mark.smoke
def test_ledger_has_m01_runtime_title_and_m32_map() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "SC2 Runtime Surface Decision & Environment Lock" in text
    assert "M32" in text
    assert "42 milestones" in text
    assert "M00–M41" in text or "M00-M41" in text
    assert "Audit Closure I" in text
    assert "Platform Boundary Review" in text
    assert "Governance, Runtime Surface, and Deterministic Run Substrate" in text


@pytest.mark.smoke
def test_ledger_canonical_corpus_promotion_rule() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Canonical corpus promotion" in text
    assert "canonical STARLAB corpus" in text


@pytest.mark.smoke
def test_od005_resolved_row() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| OD-005"):
            assert "Resolved" in stripped
            assert "s2client-proto" in stripped or "s2client" in stripped.lower()
            return
    raise AssertionError("OD-005 row not found in ledger")


@pytest.mark.smoke
def test_current_milestone_is_m37() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "M37" in section
    assert "M36" in section
    assert "Audit Closure VI" in section
    assert "Coverage Margin Recovery" in section


@pytest.mark.smoke
def test_planned_program_arc_is_42_milestones() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "42 milestones" in text
    assert "M00–M41" in text or "M00-M41" in text


@pytest.mark.smoke
def test_ledger_milestone_table_m37_m41_rows() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    sec = text.split("## 7. Milestone table")[1].split("## 8")[0]
    assert "| M37 |" in sec and "Audit Closure VI" in sec and "Coverage Margin Recovery" in sec
    assert "| M38 |" in sec and "Audit Closure VII" in sec and "Public Face Refresh" in sec
    assert "| M39 |" in sec and "Public Flagship Proof Pack" in sec
    assert "| M40 |" in sec and "SC2 Substrate Review" in sec
    assert "| M41 |" in sec and "Platform Boundary Review" in sec


@pytest.mark.smoke
def test_od007_targets_m41() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("| OD-007 |"):
            assert "M41" in line
            return
    raise AssertionError("OD-007 row not found in docs/starlab.md")


def test_m01_changelog_entry_present() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### 2026-04-06 — M01 closeout" in text
    assert "OD-005" in text
