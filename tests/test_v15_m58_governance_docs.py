"""Governance document checks for V15-M58."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m58_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs/starlab.md").read_text(encoding="utf-8")
    low = v15.lower()
    needles = (
        "v15-m58",
        "bounded candidate adapter evaluation execution attempt",
        "starlab.v15.bounded_candidate_adapter_evaluation_execution.v1",
        "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90",
        "emit_v15_m58_bounded_candidate_adapter_evaluation_execution",
        "run_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt",
        "v15_bounded_candidate_adapter_evaluation_execution_attempt_v1.md",
        "route_to_v15_m59_evaluation_readout",
        "v15-m59",
        "bounded candidate-adapter evaluation-smoke attempt",
        "no benchmark pass/fail",
    )
    for needle in needles:
        assert needle in low
    low_led = ledger.lower()
    assert (
        "v15-m58" in low_led and "bounded candidate adapter evaluation execution attempt" in low_led
    )

    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""
