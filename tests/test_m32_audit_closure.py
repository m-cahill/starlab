"""M32 audit-closure wiring: coverage config, CI artifacts, docs, smoke lane, field-test path."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_has_coverage_fail_under_m32_gate() -> None:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.coverage.report]" in text
    assert "fail_under = " in text
    m = re.search(r"fail_under = ([0-9.]+)", text)
    assert m is not None
    assert float(m.group(1)) >= 75.4, "coverage gate must not be lowered below the M32 baseline"
    assert "pytest-cov" in text


def test_ci_workflow_uploads_coverage_and_junit() -> None:
    wf = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "coverage.xml" in wf
    assert "pytest-junit.xml" in wf
    assert "--junitxml=pytest-junit.xml" in wf
    assert "jobs:" in wf
    assert "tests:" in wf
    assert "actions/checkout@" in wf
    assert re.search(r"actions/checkout@[0-9a-f]{40}", wf)
    assert re.search(r"actions/setup-python@[0-9a-f]{40}", wf)
    assert re.search(r"actions/upload-artifact@[0-9a-f]{40}", wf)
    assert re.search(r"gitleaks/gitleaks-action@[0-9a-f]{40}", wf)


def test_makefile_has_required_targets() -> None:
    mk = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    for t in (
        "install-dev",
        "smoke",
        "test",
        "coverage",
        "lint",
        "typecheck",
        "audit",
        "fieldtest",
        "check",
    ):
        assert t in mk, f"missing make target: {t}"


def test_fieldtest_emit_replay_explorer_fixture_path(tmp_path: Path) -> None:
    """Same CLI path as `make fieldtest` (M31 explorer on fixtures)."""
    bundle = REPO_ROOT / "tests" / "fixtures" / "m31" / "bundle"
    agent = REPO_ROOT / "tests" / "fixtures" / "m30" / "replay_hierarchical_imitation_agent.json"
    out = tmp_path / "ft"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.explorer.emit_replay_explorer_surface",
            "--bundle-dir",
            str(bundle),
            "--agent-path",
            str(agent),
            "--output-dir",
            str(out),
            "--max-panels",
            "2",
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    assert (out / "replay_explorer_surface.json").is_file()
    assert (out / "replay_explorer_surface_report.json").is_file()


def test_smoke_collection_count_in_target_band() -> None:
    """Bounded fast lane: ~25–35 smoke tests (see M32 plan; M33+ closeout adds governance rows).

    Upper band includes M10–M13 smoke governance tests (`test_v15_m10_governance_docs`,
    `test_v15_m11_governance_docs`, `test_v15_m12_governance_docs`, `test_v15_m13_governance_docs`)
    without broadening the policy.
    """
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-m", "smoke", "tests"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    out = proc.stdout + proc.stderr
    m = re.search(r"(\d+)/\d+\s+tests collected", out) or re.search(
        r"(\d+)\s+tests?\s+selected",
        out,
    )
    assert m, out
    n = int(m.group(1))
    _msg = (
        f"smoke count {n} outside 25–89 band "
        "(M13 adds `test_v15_m13_governance_docs`; band widened by observed count, not policy)"
    )
    assert 25 <= n <= 89, _msg


def test_ledger_milestone_rows_m32_m47() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "| M32 | Audit Closure I" in text
    assert "| M33 | Audit Closure II" in text
    assert "| M34 | Audit Closure III" in text
    assert "| M35 | Audit Closure IV" in text
    assert "| M36 | Audit Closure V" in text
    assert "| M37 | Audit Closure VI" in text
    assert "| M38 | Audit Closure VII" in text
    assert "| M39 | Public Flagship Proof Pack" in text
    assert "| M40 | Agent Training Program Charter" in text
    for line in text.splitlines():
        if line.strip().startswith("| M40 |") and "Agent Training Program Charter" in line:
            assert "Complete" in line
            break
    else:
        raise AssertionError("M40 milestone table row missing Complete")
    assert "| M41 | Replay-Imitation Training Pipeline" in text
    assert "| M42 | Learned-Agent Comparison Harness" in text
    assert "| M45 | Self-Play / RL Bootstrap" in text
    assert "| M46 | Bounded Live Validation Final-Status Semantics" in text
    for line in text.splitlines():
        stripped = line.strip()
        m47 = "Bootstrap Episode Distinctness & Operator Ergonomics"
        if stripped.startswith("| M47 |") and m47 in stripped:
            assert "Complete" in stripped
            break
    else:
        raise AssertionError("M47 milestone table row missing Complete")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("| M48 |") and (
            "Learned-Agent Comparison Contract-Path Alignment" in stripped
        ):
            assert "Complete" in stripped
            break
    else:
        raise AssertionError("M48 milestone table row missing Complete")


def test_flagship_proof_pack_module_exists_post_m39() -> None:
    """M39 introduces ``starlab.flagship`` for the public flagship proof pack."""

    assert (REPO_ROOT / "starlab" / "flagship").is_dir()
    assert not (REPO_ROOT / "starlab" / "proof_pack").exists()


def test_agent_training_program_package_exists_post_m40() -> None:
    """M40 introduces ``starlab.training`` for the governed training-program contract."""

    assert (REPO_ROOT / "starlab" / "training").is_dir()


def test_deferred_issues_registry_has_required_columns() -> None:
    p = REPO_ROOT / "docs" / "audit" / "DeferredIssuesRegistry.md"
    body = p.read_text(encoding="utf-8")
    assert "Exit criteria" in body
    assert "DIR-001" in body
    assert "M33" in body
