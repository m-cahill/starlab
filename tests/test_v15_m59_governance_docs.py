"""Governance document checks for V15-M59."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m59_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    low = v15.lower()

    assert "v15-m59" in low
    assert "adapter smoke readout" in low or "adapter-smoke" in low
    assert "accepted within scope" in low
    assert "not benchmark evidence" in low
    assert "v15-m60" in low
    assert "continue/remediate" in low

    assert 'first 12-hour run" gate' in low

    for needle in (
        "starlab.v15.m59.adapter_smoke_readout.v1",
        "starlab.v15.m59.benchmark_overclaim_refusal.v1",
        "emit_v15_m59_adapter_smoke_readout",
    ):
        assert needle.lower() in low or needle in v15

    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""
