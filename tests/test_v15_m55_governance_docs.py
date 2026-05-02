"""Governance document checks for V15-M55."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m55_governance_docs() -> None:
    v15 = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    ledger = (REPO_ROOT / "docs/starlab.md").read_text(encoding="utf-8")
    low = v15.lower()
    needles = (
        "v15-m55",
        "starlab.v15.bounded_evaluation_package_preflight.v1",
        "starlab.v15.bounded_evaluation_package_preflight_report.v1",
        "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6",
        "emit_v15_m55_bounded_evaluation_package_preflight",
        "no evaluation execution",
        "no benchmark pass/fail",
    )
    for needle in needles:
        assert needle in low
    assert "v15_bounded_evaluation_package_preflight_v1.md" in v15.replace("\n", " ").lower()
    required_ledger = (
        "emit_v15_m55_bounded_evaluation_package_preflight",
        "docs/starlab-v1.5.md",
        "v15-m55",
        "bounded_evaluation_package_preflight",
    )
    low_led = ledger.lower()
    for n in required_ledger:
        assert n in low_led
    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""
