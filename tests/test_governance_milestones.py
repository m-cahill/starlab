"""Governance tests: milestone table rows and milestone secret-folder files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _milestone_table_section() -> str:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    return text.split("## 7. Milestone table")[1].split("## 8")[0]


def test_ledger_documents_starlab_archive_policy() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "docs/starlab_archive.md" in text
    assert "Ledger archival policy" in text


def _assert_milestone_row_complete(milestone_id: str, name_fragment: str) -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith(f"| {milestone_id} |") and name_fragment in stripped:
            assert "Complete" in stripped, f"{milestone_id} row missing Complete"
            return
    raise AssertionError(f"{milestone_id} milestone row not found or not complete")


def _closeout_filenames(prefix: str) -> tuple[str, ...]:
    return tuple(
        f"{prefix}_{name}"
        for name in ("plan.md", "toolcalls.md", "run1.md", "summary.md", "audit.md")
    )


@dataclass(frozen=True)
class _MilestoneFolder:
    folder: str
    filenames: tuple[str, ...]


# (milestone_id, table name substring) — smoke-marked entries run under `pytest -m smoke`.
_MILESTONE_COMPLETE_ROWS = [
    pytest.param("M01", "SC2 Runtime Surface Decision"),
    pytest.param("M02", "Deterministic Match Execution Harness"),
    pytest.param("M03", "Lineage Seed"),
    pytest.param("M04", "Replay Binding"),
    pytest.param("M05", "Canonical Run Artifact"),
    pytest.param("M06", "Environment Drift"),
    pytest.param("M08", "Replay Parser Substrate"),
    pytest.param("M09", "Replay Metadata Extraction"),
    pytest.param("M10", "Timeline"),
    pytest.param("M11", "Build-Order"),
    pytest.param("M12", "Combat"),
    pytest.param("M13", "Replay Slice"),
    pytest.param("M14", "Replay Bundle"),
    pytest.param("M15", "Canonical State"),
    pytest.param("M16", "Structured State"),
    pytest.param("M17", "Observation"),
    pytest.param("M18", "Perceptual"),
    pytest.param("M19", "Reconciliation"),
    pytest.param("M20", "Benchmark Contract"),
    pytest.param("M21", "Scripted Baseline"),
    pytest.param("M22", "Heuristic Baseline"),
    pytest.param("M23", "Evaluation Runner"),
    pytest.param("M24", "Attribution"),
    pytest.param("M25", "Evidence"),
    pytest.param("M26", "Training Dataset"),
    pytest.param("M27", "Replay-Derived Imitation"),
    pytest.param("M28", "Learned-Agent Evaluation"),
    pytest.param("M29", "Hierarchical", marks=pytest.mark.smoke),
    pytest.param("M30", "First Learned Hierarchical Agent", marks=pytest.mark.smoke),
    pytest.param("M31", "Replay Explorer", marks=pytest.mark.smoke),
    pytest.param("M32", "Audit Closure I", marks=pytest.mark.smoke),
    pytest.param("M33", "Audit Closure II", marks=pytest.mark.smoke),
    pytest.param("M34", "Audit Closure III", marks=pytest.mark.smoke),
    pytest.param("M35", "Audit Closure IV", marks=pytest.mark.smoke),
]


@pytest.mark.parametrize(("milestone_id", "name_fragment"), _MILESTONE_COMPLETE_ROWS)
def test_milestone_complete_in_milestone_table(milestone_id: str, name_fragment: str) -> None:
    _assert_milestone_row_complete(milestone_id, name_fragment)


_MILESTONE_FOLDERS: list[Any] = [
    _MilestoneFolder("M03", ("M03_plan.md", "M03_toolcalls.md")),
    _MilestoneFolder("M04", ("M04_plan.md", "M04_toolcalls.md")),
    _MilestoneFolder("M05", ("M05_plan.md", "M05_toolcalls.md")),
    _MilestoneFolder("M06", ("M06_plan.md", "M06_toolcalls.md")),
    _MilestoneFolder("M07", _closeout_filenames("M07")),
    _MilestoneFolder("M08", _closeout_filenames("M08")),
    _MilestoneFolder("M09", _closeout_filenames("M09")),
    _MilestoneFolder("M10", _closeout_filenames("M10")),
    _MilestoneFolder("M11", _closeout_filenames("M11")),
    _MilestoneFolder("M12", _closeout_filenames("M12")),
    _MilestoneFolder("M13", _closeout_filenames("M13")),
    _MilestoneFolder("M14", _closeout_filenames("M14")),
    _MilestoneFolder("M15", _closeout_filenames("M15")),
    _MilestoneFolder("M16", _closeout_filenames("M16")),
    _MilestoneFolder("M17", _closeout_filenames("M17")),
    _MilestoneFolder("M18", _closeout_filenames("M18")),
    _MilestoneFolder("M19", _closeout_filenames("M19")),
    _MilestoneFolder("M20", _closeout_filenames("M20")),
    _MilestoneFolder("M21", _closeout_filenames("M21")),
    _MilestoneFolder("M22", _closeout_filenames("M22")),
    _MilestoneFolder("M23", _closeout_filenames("M23")),
    _MilestoneFolder("M24", _closeout_filenames("M24")),
    _MilestoneFolder("M25", _closeout_filenames("M25")),
    _MilestoneFolder("M26", _closeout_filenames("M26")),
    _MilestoneFolder("M27", _closeout_filenames("M27")),
    _MilestoneFolder("M28", _closeout_filenames("M28")),
    pytest.param(
        _MilestoneFolder("M29", ("M29_plan.md", "M29_toolcalls.md")),
        id="M29",
    ),
    pytest.param(
        _MilestoneFolder("M30", _closeout_filenames("M30")),
        id="M30",
    ),
    pytest.param(
        _MilestoneFolder("M31", _closeout_filenames("M31")),
        id="M31",
    ),
    pytest.param(
        _MilestoneFolder("M32", _closeout_filenames("M32")),
        marks=pytest.mark.smoke,
        id="M32",
    ),
    pytest.param(
        _MilestoneFolder("M33", _closeout_filenames("M33")),
        marks=pytest.mark.smoke,
        id="M33",
    ),
    pytest.param(
        _MilestoneFolder("M34", _closeout_filenames("M34")),
        marks=pytest.mark.smoke,
        id="M34",
    ),
    pytest.param(
        _MilestoneFolder("M35", _closeout_filenames("M35")),
        marks=pytest.mark.smoke,
        id="M35",
    ),
    pytest.param(
        _MilestoneFolder("M36", ("M36_plan.md", "M36_toolcalls.md")),
        marks=pytest.mark.smoke,
        id="M36",
    ),
    pytest.param(
        _MilestoneFolder("M37", ("M37_plan.md", "M37_toolcalls.md")),
        marks=pytest.mark.smoke,
        id="M37",
    ),
    pytest.param(
        _MilestoneFolder("M38", ("M38_plan.md", "M38_toolcalls.md")),
        marks=pytest.mark.smoke,
        id="M38",
    ),
    pytest.param(
        _MilestoneFolder("M39", ("M39_plan.md", "M39_toolcalls.md")),
        marks=pytest.mark.smoke,
        id="M39",
    ),
]


def _assert_milestone_folder(spec: _MilestoneFolder) -> None:
    d = REPO_ROOT / "docs" / "company_secrets" / "milestones" / spec.folder
    for name in spec.filenames:
        assert (d / name).is_file(), f"missing {d / name}"


@pytest.mark.parametrize("spec", _MILESTONE_FOLDERS)
def test_milestone_expected_folder_files_exist(spec: _MilestoneFolder) -> None:
    _assert_milestone_folder(spec)
