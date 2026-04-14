"""M50 campaign execution, locks, visibility posture, extended preflight."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from starlab.training.campaign_execution_lock import (
    read_lock_file,
    release_lock,
    try_acquire_campaign_output_lock,
)
from starlab.training.campaign_execution_preflight import run_campaign_execution_preflight
from starlab.training.execute_full_local_training_campaign import main as execute_campaign_main
from starlab.training.full_local_training_campaign_io import emit_full_local_training_campaign
from starlab.training.industrial_hidden_rollout_models import resolve_visibility_posture_v1

from tests.test_m49_full_local_training_campaign import (
    M28_FIX,
    MATCH_FAKE,
    REPO_ROOT,
    _build_m43_run_dir,
)

# Reuse M49 fixture builder for campaign contract.


def test_m50_visibility_hidden_resolves_to_minimized() -> None:
    cap = resolve_visibility_posture_v1(requested="hidden")
    assert cap["requested_visibility_mode"] == "hidden"
    assert cap["resolved_visibility_mode"] == "minimized"
    assert cap["hidden_rollout_supported"] is False
    assert cap["capability_warnings"]


def test_m50_campaign_output_lock_double_acquire_fails(tmp_path: Path) -> None:
    root = tmp_path / "camp"
    root.mkdir()
    ok1, p1, _ = try_acquire_campaign_output_lock(
        campaign_root=root,
        command="test",
        execution_id="e1",
    )
    assert ok1
    ok2, p2, msg = try_acquire_campaign_output_lock(
        campaign_root=root,
        command="test",
        execution_id="e2",
    )
    assert not ok2
    assert p1 == p2
    assert "pid=" in msg
    release_lock(p1)


def test_m50_execution_preflight_fixture_campaign(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="m50_pf",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    ok, receipt = run_campaign_execution_preflight(
        campaign_root=out,
        contract_path=out / "full_local_training_campaign_contract.json",
        requested_visibility_mode="hidden",
    )
    assert ok
    assert receipt["preflight_ok"] is True
    ids = {c["check_id"] for c in receipt["checks"]}
    assert "m50_visibility_posture_resolution" in ids


def test_m50_execute_fixture_smoke(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="m50_exec",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    code = execute_campaign_main(
        [
            "--campaign-contract",
            str(out / "full_local_training_campaign_contract.json"),
            "--campaign-root",
            str(out),
            "--execution-id",
            "exec_fixture_smoke",
            "--skip-execution-preflight",
            "--max-bootstrap-phases",
            "1",
            "--requested-visibility-mode",
            "minimized",
        ],
    )
    assert code == 0
    ed = out / "campaign_runs" / "exec_fixture_smoke"
    assert (ed / "hidden_rollout_campaign_run.json").is_file()
    assert (ed / "campaign_heartbeat.json").is_file()


def test_m50_execute_module_help() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "starlab.training.execute_full_local_training_campaign", "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert r.returncode == 0
    assert "usage" in (r.stdout + r.stderr).lower()


def test_m50_partial_tree_requires_allow_resume(tmp_path: Path) -> None:
    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="m50_part",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    ed = out / "campaign_runs" / "exec_partial"
    ed.mkdir(parents=True)
    (ed / "resume.json").write_text("{}", encoding="utf-8")
    code = execute_campaign_main(
        [
            "--campaign-contract",
            str(out / "full_local_training_campaign_contract.json"),
            "--campaign-root",
            str(out),
            "--execution-id",
            "exec_partial",
            "--skip-execution-preflight",
            "--max-bootstrap-phases",
            "1",
        ],
    )
    assert code == 3


def test_m50_lockfile_readable(tmp_path: Path) -> None:
    root = tmp_path / "c"
    root.mkdir()
    ok, lock_path, _ = try_acquire_campaign_output_lock(
        campaign_root=root,
        command="t",
        execution_id="e",
    )
    assert ok
    info = read_lock_file(lock_path)
    assert info is not None
    assert info.execution_id == "e"
    release_lock(lock_path)
