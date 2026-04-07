"""M00 governance smoke tests: repo wiring only; no runtime or SC2 claims."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_GOVERNANCE_DOCS = [
    "docs/public_private_boundary.md",
    "docs/replay_data_provenance.md",
    "docs/rights_register.md",
    "docs/branding_and_naming.md",
    "docs/deployment/deployment_posture.md",
    "docs/deployment/env_matrix.md",
    "docs/runtime/sc2_runtime_surface.md",
    "docs/runtime/environment_lock.md",
    "docs/runtime/match_execution_harness.md",
    "docs/runtime/run_identity_lineage_seed.md",
]

_PLACEHOLDER_READMES = [
    "frontend/README.md",
    "backend/README.md",
    "ops/README.md",
]


@pytest.mark.parametrize("relative", _GOVERNANCE_DOCS)
def test_governance_doc_exists(relative: str) -> None:
    path = REPO_ROOT / relative
    assert path.is_file(), f"missing governance doc: {relative}"


@pytest.mark.parametrize("relative", _PLACEHOLDER_READMES)
def test_placeholder_readme_exists(relative: str) -> None:
    path = REPO_ROOT / relative
    assert path.is_file(), f"missing placeholder: {relative}"


def test_starlab_ledger_exists() -> None:
    ledger = REPO_ROOT / "docs" / "starlab.md"
    assert ledger.is_file()


def test_ledger_names_deployment_targets() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Netlify" in text
    assert "Render" in text


def test_milestone_m00_directory_exists() -> None:
    m00 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M00"
    assert m00.is_dir()


def test_rights_register_exists() -> None:
    path = REPO_ROOT / "docs" / "rights_register.md"
    assert path.is_file()


def test_ci_workflow_exists() -> None:
    wf = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file()


def test_pyproject_exists() -> None:
    assert (REPO_ROOT / "pyproject.toml").is_file()


def test_ledger_has_m01_runtime_title_and_m32_map() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "SC2 Runtime Surface Decision & Environment Lock" in text
    assert "M32" in text
    assert "Platform Boundary Review & Multi-Environment Charter" in text
    assert "Governance, Runtime Surface, and Deterministic Run Substrate" in text


def test_ledger_canonical_corpus_promotion_rule() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Canonical corpus promotion" in text
    assert "canonical STARLAB corpus" in text


def test_od005_resolved_row() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| OD-005"):
            assert "Resolved" in stripped
            assert "s2client-proto" in stripped or "s2client" in stripped.lower()
            return
    raise AssertionError("OD-005 row not found in ledger")


def test_current_milestone_is_m03() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "M03" in section
    assert "Run Identity" in section


def test_m01_complete_in_milestone_table() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.strip().startswith("| M01 "):
            assert "Complete" in line
            return
    raise AssertionError("M01 milestone row not found")


def test_m02_complete_in_milestone_table() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.strip().startswith("| M02 "):
            assert "Complete" in line
            return
    raise AssertionError("M02 milestone row not found")


def test_m03_stub_milestone_files_exist() -> None:
    m03 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M03"
    assert (m03 / "M03_plan.md").is_file()
    assert (m03 / "M03_toolcalls.md").is_file()


def test_starlab_runs_package_exists() -> None:
    runs_init = REPO_ROOT / "starlab" / "runs" / "__init__.py"
    assert runs_init.is_file()
    seed = REPO_ROOT / "starlab" / "runs" / "seed_from_proof.py"
    assert seed.is_file()


def test_m03_fixture_pair_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "m02_match_config.json").is_file()
    assert (fx / "m02_match_execution_proof.json").is_file()


def test_m01_changelog_entry_present() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### 2026-04-06 — M01 closeout" in text
    assert "OD-005" in text
