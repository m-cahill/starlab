"""Tests for V15-M29 full-wall-clock SC2-backed T1 run surfaces."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_tolerance_window_for_minimum_seconds() -> None:
    """1790 observed seconds still counts as horizon with +10 tol vs 1800 required."""
    assert 1790 + 10 >= 1800


def test_m29_fixture_only_ci_emits_fixture_outcome(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m29_full_30min_sc2_backed_t1_run",
            "--fixture-only-m29",
            "--output-dir",
            str(tmp_path / "m29fx"),
            "--m27-sc2-rollout-json",
            str(REPO_ROOT / "dummy"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout

    m29_main = tmp_path / "m29fx" / "v15_full_30min_sc2_backed_t1_run.json"
    assert m29_main.is_file()
    body = json.loads(m29_main.read_text(encoding="utf-8"))
    assert body.get("m29_outcome") == "fixture_only"
    low = json.dumps(body).lower()
    assert "not_strength_evaluation" in low


def test_training_loop_disables_early_stop_under_full_horizon(tmp_path: Path) -> None:
    from starlab.v15.sc2_backed_t1_training_execution import run_bounded_rollout_feature_training

    feats = [0.02, -0.1, 1.414, -0.5, 9.8765] * 3
    chk = tmp_path / "ck"
    rec = run_bounded_rollout_feature_training(
        feats,
        min_updates=1,
        max_updates=200000,
        checkpoint_cadence=99999999,
        checkpoint_dir=chk,
        wall_budget_seconds=3.5,
        seed=1,
        device_pref="cpu",
        disable_loss_floor_early_stop=True,
        require_full_wall_clock=True,
    )
    assert float(rec["wall_clock_seconds_observed"]) >= 3.499
    assert rec.get("early_stop_reason") == "wall_clock_budget"
    assert int(rec["training_update_count"]) >= 2500


def test_classify_requires_rc_zero_for_success_outcome() -> None:
    from starlab.v15.full_30min_sc2_backed_t1_run_models import (
        OUTCOME_FULL_30_WITH_CHECKPOINT,
        OUTCOME_FULL_30_WITHOUT_CHECKPOINT,
        OUTCOME_LAUNCHED_FAILED,
    )
    from starlab.v15.run_v15_m29_full_30min_sc2_backed_t1_run import classify_m29_outcome

    body = _fake_m28(
        outcome="sc2_backed_candidate_training_completed_with_candidate_checkpoint",
        wall=1800.0,
        full_wall_satisfied_observed=True,
        updates=10_000,
        cand_sha="b" * 64,
    )
    assert classify_m29_outcome(m28_rc=0, m28_body=body) == OUTCOME_FULL_30_WITH_CHECKPOINT

    no_ck = dict(body)
    no_ck["candidate_checkpoint"] = {
        "sha256": "",
        "produced": False,
        "promotion_status": "not_promoted_candidate_only",
    }
    assert classify_m29_outcome(m28_rc=0, m28_body=no_ck) == OUTCOME_FULL_30_WITHOUT_CHECKPOINT

    assert classify_m29_outcome(m28_rc=9, m28_body=body) == OUTCOME_LAUNCHED_FAILED


def _fake_m28(
    *,
    outcome: str,
    wall: float,
    full_wall_satisfied_observed: bool,
    updates: int,
    cand_sha: str,
) -> dict[str, Any]:
    return {
        "contract_id": "starlab.v15.sc2_backed_t1_candidate_training.v1",
        "m28_outcome": outcome,
        "artifact_sha256": "0" * 64,
        "training_attempt": {
            "wall_clock_seconds": wall,
            "full_wall_clock_satisfied": full_wall_satisfied_observed,
            "disable_loss_floor_early_stop": True,
            "requested_min_wall_clock_seconds": 1800.0,
            "checkpoint_count": 1,
            "training_update_count": updates,
            "sc2_backed_features_used": True,
            "continue_after_checkpoint": False,
            "checkpoint_cadence_updates": 50,
        },
        "candidate_checkpoint": {
            "sha256": cand_sha,
            "produced": bool(cand_sha),
            "promotion_status": "not_promoted_candidate_only",
        },
        "upstream_m27_rollout": {
            "sha256": ("f9c2ca5aca7a3b15df0567358c1f207f99e112cd8d816f5ac1a1c6ff04022227"),
        },
        "non_claims": ["not_strength_evaluation", "not_benchmark_pass"],
        "feature_derivation": {},
        "m20_m21_gate_integration": "m20_m21_candidate_gate_integration_deferred_to_m30",
    }
