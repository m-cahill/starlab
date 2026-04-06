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
