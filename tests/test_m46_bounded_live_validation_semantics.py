"""M46: bounded live validation final_status aligns fixture and burnysc2 for M45 reward."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.sc2.artifacts import compute_artifact_hash, parse_execution_proof_mapping
from starlab.training.self_play_rl_bootstrap_pipeline import (
    compute_episode_reward_validation_outcome_v1,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_m45_reward_primary_ok_when_m44_final_status_ok_with_sc2_defeat_preserved() -> None:
    """final_status ok + sc2_game_result Defeat: M45 primary reward still 1.0."""
    vr = {
        "match_execution": {
            "adapter": "burnysc2",
            "final_status": "ok",
            "sc2_game_result": "Defeat",
        },
        "action_adapter_steps": [{"step_index": 0}, {"step_index": 1}],
    }
    out = compute_episode_reward_validation_outcome_v1(vr)
    assert out["reward_primary"] == 1.0
    assert out["final_status"] == "ok"


def test_m02_fixture_proof_hash_stable_without_sc2_game_result() -> None:
    """Legacy proofs omit sc2_game_result; hash matches checked-in artifact_hash."""
    path = REPO_ROOT / "tests" / "fixtures" / "m02_match_execution_proof.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rec = parse_execution_proof_mapping(data)
    assert rec.sc2_game_result is None
    assert compute_artifact_hash(rec) == data["artifact_hash"]
