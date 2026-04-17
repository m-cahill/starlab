"""Governance tests: ledger, CI wiring, and high-signal smoke checks."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_ledger_quick_scan_post_v1_current_pv1_m04_open() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    scan = text.split("## Current truth (quick scan)")[1].split("##")[0]
    assert "| Current milestone | **PV1-M04**" in scan
    assert "**open**" in scan
    assert "| PV1 campaign outcome (bounded, operator-local) |" in scan
    assert "**PV1-M03**" in scan
    assert "pull/77" in scan
    assert "threshold-not-met" in scan
    assert "tranche_b_operator_note.md" in scan or "PV1 execution evidence" in scan


@pytest.mark.smoke
def test_starlab_ledger_exists() -> None:
    ledger = REPO_ROOT / "docs" / "starlab.md"
    assert ledger.is_file()


@pytest.mark.smoke
def test_m47_recharter_and_m48_deferral_documented() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Governance recharter (2026-04-13 — user-directed)" in text
    assert "Bootstrap Episode Distinctness & Operator Ergonomics" in text
    assert (
        "**M47 — Bootstrap Episode Distinctness & Operator Ergonomics:** **closed** on `main`"
    ) in text
    m48_closed = "**M48 — Learned-agent comparison contract-path alignment:** **closed** on `main`"
    assert m48_closed in text
    assert "62 milestones (M00–M61)" in text or "62 milestones (M00-M61)" in text


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
    assert "46 milestones" in text
    assert "M00–M45" in text or "M00-M45" in text
    assert (
        "62 milestones" in text or "M00–M61" in text or "M00-M61" in text or "53 milestones" in text
    )
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
def test_ledger_post_v1_pv1_section() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "## Post-v1 (PV1) — Long Industrial Campaign & Scaling Evidence" in text
    assert "| `PV1-M00` |" in text
    assert "### PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria" in text
    assert "### PV1 evidence surfaces (PV1-M01 — inspection helpers)" in text
    assert "### PV1 evidence surfaces (PV1-M02 — Tranche A operator-local execution)" in text
    assert "tranche_checkpoint_receipt.json" in text
    assert "campaign_observability_index.json" in text
    assert "| `PV1-M01` |" in text
    assert "| `PV1-M02` |" in text
    assert "| `PV1-M03` |" in text
    assert "| `PV1-M04` |" in text
    assert "### PV1 evidence surfaces (PV1-M03 — Tranche B / full-run threshold)" in text
    assert "### Canonical PV1 operator artifacts (campaign root)" in text
    assert "[PR #74](https://github.com/m-cahill/starlab/pull/74)" in text
    assert "[PR #76](https://github.com/m-cahill/starlab/pull/76)" in text
    assert "[PR #77](https://github.com/m-cahill/starlab/pull/77)" in text
    assert "**open**" in text


@pytest.mark.smoke
def test_current_milestone_section_covers_m47_and_closed_phase_vi() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "### PV1-M04 — Post-Campaign Analysis / Comparative Readout — **open**" in section
    assert "### PV1-M03 — Tranche B / Full-Run Completion Evidence — **closed**" in section
    assert "### PV1-M02 — Tranche A Execution Evidence — **closed**" in section
    assert "### PV1-M01 — Campaign Observability & Checkpoint Discipline — **closed**" in section
    assert "PV1-M00" in section
    assert "M47" in section
    assert "M50" in section
    assert "M51" in section
    assert "M52" in section
    assert "M53" in section
    assert "Bootstrap Episode Distinctness" in section or "Operator Ergonomics" in section
    assert "M46" in section
    assert "M45" in section
    assert "Self-Play" in section or "RL" in section
    assert "M44" in section
    assert "Local Live-Play Validation" in section
    assert section.lower().count("closed") >= 2


@pytest.mark.smoke
def test_ledger_milestone_table_m37_m45_rows() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    sec = text.split("## 7. Milestone table")[1].split("## 8")[0]
    assert "| M37 |" in sec and "Audit Closure VI" in sec and "Coverage Margin Recovery" in sec
    assert "| M38 |" in sec and "Audit Closure VII" in sec and "Public Face Refresh" in sec
    assert "| M39 |" in sec and "Public Flagship Proof Pack" in sec
    assert "| M40 |" in sec and "Agent Training Program Charter" in sec
    assert "| M41 |" in sec and "Replay-Imitation Training Pipeline" in sec and "Complete" in sec
    assert "| M42 |" in sec and "Learned-Agent Comparison" in sec and "Complete" in sec
    assert "| M43 |" in sec and "Hierarchical Training Pipeline" in sec and "Complete" in sec
    assert "| M44 |" in sec and "Local Live-Play Validation" in sec and "Complete" in sec
    assert "| M45 |" in sec and "Self-Play" in sec
    m48_line = next(line for line in sec.splitlines() if line.strip().startswith("| M48 |"))
    assert "Learned-Agent Comparison Contract-Path" in m48_line and "Complete" in m48_line
    assert "| M49 |" in sec and "Full Local Training" in sec and "Complete" in sec
    m50_line = next(line for line in sec.splitlines() if line.strip().startswith("| M50 |"))
    assert "Industrial-scale hidden rollout" in m50_line and "Complete" in m50_line
    m51_line = next(line for line in sec.splitlines() if line.strip().startswith("| M51 |"))
    assert "post-bootstrap" in m51_line and "Complete" in m51_line and "v0.0.51-m51" in m51_line


@pytest.mark.smoke
def test_od007_deferred_beyond_active_arc() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("| OD-007 |"):
            assert "Deferred" in line
            assert "Beyond active arc" in line or "beyond" in line.lower()
            return
    raise AssertionError("OD-007 row not found in docs/starlab.md")


def test_m01_changelog_entry_present() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### 2026-04-06 — M01 closeout" in text
    assert "OD-005" in text
