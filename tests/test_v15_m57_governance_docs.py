"""Governance document checks for V15-M57."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m57_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs/starlab.md").read_text(encoding="utf-8")
    low = v15.lower()
    needles = (
        "v15-m57",
        "starlab.v15.governed_evaluation_execution_charter.v1",
        "candidate_live_visual_watch_completed",
        "7458f5c370be4b04465a2d4f9d85321b313c34ef0ab0e6d48124ff0dadd7fa47",
        "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90",
        "emit_v15_m57_governed_evaluation_execution_charter",
        "v15_governed_evaluation_execution_charter_dry_run_gate_v1.md",
        "v15-m58",
        "no torch.load in m57",
        "no benchmark execution",
    )
    for needle in needles:
        assert needle in low
    low_led = ledger.lower()
    for n in (
        "v15-m57",
        "docs/starlab-v1.5.md",
        "emit_v15_m57_governed_evaluation_execution_charter",
    ):
        assert n in low_led
    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""
