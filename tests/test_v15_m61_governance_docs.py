"""Governance docs for V15-M61."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_v15_m61_governance_docs_starlab_v15_and_gitignore() -> None:
    text = (REPO_ROOT / "docs/starlab-v1.5.md").read_text(encoding="utf-8")
    low = text.lower()

    for needle in (
        "v15-m61",
        "release-lock / showcase video proof-pack update",
        "bounded showcase-evidence",
        "showcase video",
        "starlab.v15.m61.release_lock_proof_pack.v1",
        "emit_v15_m61_release_lock_proof_pack",
        "not benchmark pass/fail",
        "not strength evaluation",
        "not checkpoint promotion",
        "not 72-hour authorization",
        "not v2 authorization",
        "v15-m62",
    ):
        assert needle in low

    start = low.find("### v15-m61")
    assert start >= 0, "V15-M61 section missing"
    end_marker = "\n\n**provisional next:**"
    end_pos = low.find(end_marker, start)
    if end_pos < 0:
        rest = low[start + 1 :]
        next_h3 = rest.find("\n### ")
        section = low[start : start + 1 + next_h3] if next_h3 >= 0 else low[start:]
    else:
        section = low[start:end_pos]

    forbidden = (
        "benchmark passed",
        "strength proven",
        "checkpoint promoted",
        "72-hour authorized",
        "v2 authorized",
    )
    for fb in forbidden:
        assert fb not in section

    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.stdout.strip() == ""

    rt = (
        (REPO_ROOT / "docs/runtime/v15_release_lock_showcase_video_proof_pack_v1.md")
        .read_text(
            encoding="utf-8",
        )
        .lower()
    )
    assert "starlab.v15.m61.showcase_video_capture_manifest.v1" in rt
    assert "fixture_ci" in rt
