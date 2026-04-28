"""V15-M27 SC2 rollout integration contracts and fixture runner."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration import main as m27_main
from starlab.v15.sc2_rollout_training_loop_integration_io import (
    build_fixture_episodes,
    classify_rollout_success,
    seal_with_sha256,
    validate_integration_contract_minimum,
)
from starlab.v15.sc2_rollout_training_loop_integration_models import (
    CONTRACT_ID,
    OUTCOME_FIXTURE_ONLY,
    POLICY_ID_M27_MACRO_SMOKE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_m27_fixture_episodes_classify_nontrivial() -> None:
    eps = build_fixture_episodes(episode_count=3, game_step=8, max_game_steps=512)
    ok, _ = classify_rollout_success(eps, min_episodes_with_actions=2)
    assert ok
    assert all(int(e["action_count"]) > 0 for e in eps)


def test_m27_artifact_rejects_invalid_contract_id() -> None:
    with pytest.raises(ValueError, match="contract_id"):
        validate_integration_contract_minimum({"contract_id": "wrong", "milestone": "V15-M27"})


def test_m27_runner_fixture_only_writes_json(tmp_path: Path) -> None:
    out = tmp_path / "m27"
    code = m27_main(
        [
            "--fixture-only",
            "--output-dir",
            str(out),
            "--episodes",
            "3",
            "--game-step",
            "8",
            "--max-game-steps",
            "128",
        ],
    )
    assert code == 0
    main_p = out / "v15_sc2_rollout_training_loop_integration.json"
    raw = json.loads(main_p.read_text(encoding="utf-8"))
    assert raw["contract_id"] == CONTRACT_ID
    assert raw["m27_outcome"] == OUTCOME_FIXTURE_ONLY
    assert raw["policy_id"] == POLICY_ID_M27_MACRO_SMOKE
    sealed = seal_with_sha256({k: v for k, v in raw.items() if k != "artifact_sha256"})
    assert sealed["artifact_sha256"] == raw["artifact_sha256"]
    assert sum(int(e["action_count"]) for e in raw["episodes"]) > 0


def test_harness_passive_smoke_labeled_in_docs() -> None:
    """Governed elsewhere — ensure runtime doc mentions passive harness smoke-only."""

    p = REPO_ROOT / "docs" / "runtime" / "v15_sc2_rollout_training_loop_integration_v1.md"
    t = p.read_text(encoding="utf-8")
    assert "passive" in t.lower() or "_HarnessBot" in t or "smoke" in t.lower()


@pytest.mark.smoke
def test_m27_cli_module_invocation_fixture(tmp_path: Path) -> None:
    out = tmp_path / "out_m27"
    cmd = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_m27_sc2_rollout_training_loop_integration",
        "--fixture-only",
        "--output-dir",
        str(out),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    assert (out / "v15_sc2_rollout_training_loop_integration.json").is_file()
