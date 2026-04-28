"""Tests for V15-M28 SC2-backed T1 candidate training surfaces."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_verify_m27_rollout_json_accepts_operator_sha_seal() -> None:
    from starlab.v15.sc2_backed_t1_candidate_training_io import verify_m27_rollout_json

    p = (
        REPO_ROOT
        / "out/v15_m27/sc2_rollout_integration_run1/v15_sc2_rollout_training_loop_integration.json"
    )
    if not p.is_file():
        pytest.skip("operator-local M27 artifact not present in this checkout")

    raw, err = verify_m27_rollout_json(p)
    assert err is None
    assert raw is not None
    assert (
        raw.get("artifact_sha256")
        == "f9c2ca5aca7a3b15df0567358c1f207f99e112cd8d816f5ac1a1c6ff04022227"
    )


def test_verify_m27_rejects_sha_tamper(tmp_path: Path) -> None:
    from starlab.v15.sc2_backed_t1_candidate_training_io import verify_m27_rollout_json

    src = (
        REPO_ROOT
        / "out/v15_m27/sc2_rollout_integration_run1/v15_sc2_rollout_training_loop_integration.json"
    )
    if not src.is_file():
        pytest.skip("operator-local M27 artifact not present")

    dst = tmp_path / "m27.json"
    obj = json.loads(src.read_text(encoding="utf-8"))
    obj["episode_count"] = int(obj.get("episode_count") or 0) + 1
    dst.write_text(json.dumps(obj), encoding="utf-8")

    raw, err = verify_m27_rollout_json(dst)
    assert raw is None
    assert err == "sha_mismatch"


def test_sc2_rollout_feature_vector_non_trivial() -> None:
    from starlab.v15.sc2_backed_t1_candidate_training_io import (
        build_fixture_m27_like_dict_for_ci,
        sc2_rollout_feature_vector_from_m27_episodes,
    )

    m27 = build_fixture_m27_like_dict_for_ci()
    eps = m27["episodes"]
    vec, meta = sc2_rollout_feature_vector_from_m27_episodes(list(eps), bind_from_json=m27)
    assert len(vec) >= 6
    assert meta.get("merged_action_type_dim", 0) >= 1


def test_fixture_runner_emits_fixture_only(tmp_path: Path) -> None:
    out = tmp_path / "m28_fixture"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training",
            "--fixture-only",
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    main_p = out / "v15_sc2_backed_t1_candidate_training.json"
    assert main_p.is_file()
    sealed = json.loads(main_p.read_text(encoding="utf-8"))
    assert sealed.get("m28_outcome") == "fixture_only"
    assert sealed.get("training_attempt", {}).get("sc2_backed_features_used") is True
    ncs = sealed.get("non_claims") or []
    assert "not_strength_evaluation" in ncs
    assert (
        sealed.get("candidate_checkpoint", {}).get("promotion_status")
        == "not_promoted_candidate_only"
    )


def test_blocked_missing_m27_json(tmp_path: Path) -> None:
    out = tmp_path / "missing"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training",
            "--allow-operator-local-execution",
            "--authorize-sc2-backed-t1-candidate-training",
            "--m27-sc2-rollout-json",
            str(tmp_path / "nope.json"),
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 3
    body = json.loads(
        (out / "v15_sc2_backed_t1_candidate_training.json").read_text(encoding="utf-8")
    )
    assert body.get("m28_outcome") == "sc2_backed_candidate_training_blocked_missing_m27_rollout"


def test_m20_m21_deferred_field_present(tmp_path: Path) -> None:
    out = tmp_path / "m28_fixture2"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training",
            "--fixture-only",
            "--output-dir",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )
    sealed = json.loads(
        (out / "v15_sc2_backed_t1_candidate_training.json").read_text(encoding="utf-8")
    )
    assert (
        sealed.get("m20_m21_gate_integration")
        == "m20_m21_candidate_gate_integration_deferred_to_m29"
    )
