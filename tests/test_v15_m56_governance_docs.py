"""Governance document checks for V15-M56."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m56_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs/starlab.md").read_text(encoding="utf-8")
    low = v15.lower()
    needles = (
        "v15-m56",
        "starlab.v15.bounded_evaluation_package_readout_decision.v1",
        "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6",
        "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90",
        "emit_v15_m56_bounded_evaluation_package_readout_decision",
        "v15_bounded_evaluation_package_readout_decision_v1.md",
        "no benchmark execution",
        "recommended_not_executed",
        "v15-m57",
        "m56a",
    )
    for needle in needles:
        assert needle in low
    low_led = ledger.lower()
    for n in (
        "v15-m56",
        "docs/starlab-v1.5.md",
        "bounded_evaluation_package_readout",
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
