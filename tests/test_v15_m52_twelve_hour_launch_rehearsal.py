"""Tests for V15-M52B twelve-hour launch rehearsal (no 12-hour execution)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from starlab.v15.m52_candidate_live_adapter_spike_models import FILENAME_MAIN_JSON as M52A_FILENAME
from starlab.v15.m52_twelve_hour_launch_rehearsal_io import (
    emit_m52b_fixture_ci,
    emit_m52b_forbidden_refusal,
    emit_m52b_operator_preflight,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    CONTRACT_ID_M52B,
    FORBIDDEN_FLAG_12H,
    LAUNCH_CMD_FILENAME,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_FORBIDDEN,
    REFUSED_M52A_SHA,
    STATUS_FIXTURE_ONLY,
    STATUS_REFUSED,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    FILENAME_MAIN_JSON as M52B_FILENAME,
)


def test_m52b_fixture_ci(tmp_path: Path) -> None:
    sealed, paths = emit_m52b_fixture_ci(tmp_path / "out")
    assert sealed["contract_id"] == CONTRACT_ID_M52B
    assert sealed["rehearsal_status"] == STATUS_FIXTURE_ONLY
    assert sealed["twelve_hour_run_executed_in_rehearsal"] is False
    assert any(p.name == LAUNCH_CMD_FILENAME for p in paths)
    cmd_path = tmp_path / "out" / LAUNCH_CMD_FILENAME
    cmd = cmd_path.read_text(encoding="utf-8")
    assert "run_v15_m53_twelve_hour_operator_run_attempt" in cmd
    assert "43200" in cmd


def test_m52b_m52a_sha_mismatch(tmp_path: Path) -> None:
    sub = tmp_path / "m52a"
    emit_m52b_fixture_ci(sub)
    m52a_path = sub / "m52a_upstream_fixture" / M52A_FILENAME
    sealed, _ = emit_m52b_operator_preflight(
        tmp_path / "m52bout",
        m52a_path=m52a_path,
        m52a_plain_override=None,
        expected_m52a_sha256="f" * 64,
        profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        allow_m52a_blocked_planning=True,
        m51_watchability_json=None,
        sc2_root=None,
        map_path=None,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=None,
        disk_root=None,
        estimated_checkpoint_mb=256.0,
        max_retained_checkpoints=256,
    )
    assert sealed["rehearsal_status"] == STATUS_REFUSED
    assert REFUSED_M52A_SHA in sealed["blockers"]


def test_m52b_forbidden_12h_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m52b_forbidden_refusal(
        tmp_path / "o",
        profile_short=PROFILE_FIXTURE_CI,
        flags=[FORBIDDEN_FLAG_12H],
    )
    assert sealed["rehearsal_status"] == STATUS_REFUSED
    assert REFUSED_FORBIDDEN in sealed["blockers"]
    assert "execute_12_hour_run_forbidden" in sealed["blockers"]


def test_m52b_cli_fixture(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m52_twelve_hour_launch_rehearsal",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert (out / M52B_FILENAME).is_file()
    assert (out / LAUNCH_CMD_FILENAME).is_file()
