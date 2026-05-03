"""Governance docs for V15-M60."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m60_governance_docs_starlab_v15_and_gitignore() -> None:
    text = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    low = text.lower()

    for needle in (
        "v15-m60",
        "showcase-evidence lock vs continue/remediate",
        "starlab.v15.m60.showcase_evidence_lock_decision.v1",
        "starlab.v15.m60.showcase_evidence_lock_decision_report.v1",
        "emit_v15_m60_showcase_evidence_lock_decision",
        "v15-m61",
    ):
        assert needle in low

    forbidden = ("m62 first 12-hour run", "v15-m62 first 12-hour run")
    for fb in forbidden:
        assert fb not in low

    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""
