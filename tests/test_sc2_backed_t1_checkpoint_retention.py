"""Training path checkpoint retention (V15-M38)."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("torch")

from starlab.v15.sc2_backed_t1_training_execution import run_bounded_rollout_feature_training


def test_retention_caps_on_disk_files(tmp_path: Path) -> None:
    feats = [0.1, 0.2, 0.3, 0.4]
    ck = tmp_path / "ck"
    rec = run_bounded_rollout_feature_training(
        feats,
        min_updates=1,
        max_updates=120,
        checkpoint_cadence=10,
        checkpoint_dir=ck,
        wall_budget_seconds=30.0,
        seed=1,
        device_pref="cpu",
        disable_loss_floor_early_stop=True,
        require_full_wall_clock=False,
        max_retained_checkpoints=3,
    )
    assert rec.get("failure_reason") is None
    assert sum(1 for _ in ck.glob("*.pt")) <= 3
    written = int(rec.get("checkpoints_written_total") or 0)
    pruned = int(rec.get("checkpoints_pruned_total") or 0)
    assert written >= pruned
    assert written > 3
    retained = rec.get("checkpoint_paths_with_sha256") or []
    assert len(retained) <= 3
