"""PX2-M03 self-play tests: slice 1 contract/smoke; slice 2 skeleton/receipts. CPU fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
    seal_px2_self_play_campaign_body,
)
from starlab.sc2.px2.self_play.campaign_run import (
    EXECUTION_KIND_SLICE2,
    PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID,
    run_px2_campaign_execution_skeleton,
)
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_FROZEN_SEED,
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_SELF_SNAPSHOT,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.smoke_run import (
    PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID,
    run_px2_fixture_self_play_smoke,
)
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub

CORPUS = Path(__file__).resolve().parent / "fixtures" / "px2_m02" / "corpus"


def test_campaign_contract_seal_roundtrip() -> None:
    pool = build_default_opponent_pool_stub()
    c, r = build_px2_self_play_campaign_artifacts(
        campaign_id="c1",
        campaign_profile_id="p1",
        opponent_pool=pool,
        torch_seed=7,
    )
    assert c["contract_id"] == PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID
    seal = c.pop("campaign_sha256")
    assert seal == seal_px2_self_play_campaign_body(c)
    c["campaign_sha256"] = seal
    assert r["campaign_sha256"] == seal


def test_opponent_selection_deterministic() -> None:
    refs = ("a", "b", "c")
    assert (
        select_opponent_ref(step_index=0, rule_id=OPPONENT_SELECTION_SELF_SNAPSHOT, ref_ids=refs)
        == "a"
    )
    assert (
        select_opponent_ref(step_index=99, rule_id=OPPONENT_SELECTION_FROZEN_SEED, ref_ids=refs)
        == "a"
    )
    assert (
        select_opponent_ref(step_index=0, rule_id=OPPONENT_SELECTION_ROUND_ROBIN, ref_ids=refs)
        == "a"
    )
    assert (
        select_opponent_ref(step_index=1, rule_id=OPPONENT_SELECTION_ROUND_ROBIN, ref_ids=refs)
        == "b"
    )
    assert (
        select_opponent_ref(step_index=2, rule_id=OPPONENT_SELECTION_ROUND_ROBIN, ref_ids=refs)
        == "c"
    )


def test_opponent_selection_empty_refs_errors() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        select_opponent_ref(step_index=0, rule_id=OPPONENT_SELECTION_ROUND_ROBIN, ref_ids=())


def test_opponent_selection_unknown_rule_errors() -> None:
    bad = "starlab.px2.opponent_selection.nope.v1"
    with pytest.raises(ValueError, match="unknown"):
        select_opponent_ref(step_index=0, rule_id=bad, ref_ids=("x",))


def test_policy_bridge_decode_compile(tmp_path: Path) -> None:
    from starlab.sc2.px2.bootstrap.dataset_contract import load_examples_from_dataset_file
    from starlab.sc2.px2.bootstrap.emit_replay_bootstrap_dataset import emit_from_corpus

    emit_from_corpus(CORPUS, tmp_path)
    examples = load_examples_from_dataset_file(tmp_path / "px2_replay_bootstrap_dataset.json")
    ex = examples[0]
    torch.manual_seed(0)
    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    receipt = bootstrap_policy_runtime_step(
        model,
        ex["observation_surface"],
        ex["game_state_snapshot"],
    )
    assert receipt.decode_ok
    assert receipt.compile_receipt_sha256
    assert receipt.internal_command.command_kind


def test_smoke_run_emits_stable_hashes(tmp_path: Path) -> None:
    c1, cr1, s1, sr1 = run_px2_fixture_self_play_smoke(
        corpus_root=CORPUS,
        campaign_id="px2_m03_test_campaign",
        campaign_profile_id="px2_m03_test_profile",
        torch_seed=99,
    )
    c2, cr2, s2, sr2 = run_px2_fixture_self_play_smoke(
        corpus_root=CORPUS,
        campaign_id="px2_m03_test_campaign",
        campaign_profile_id="px2_m03_test_profile",
        torch_seed=99,
    )
    assert c1 == c2 and s1 == s2
    assert s1["contract_id"] == PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID
    assert s1["smoke_sha256"] == sha256_hex_of_canonical_json(
        {k: v for k, v in s1.items() if k != "smoke_sha256"}
    )
    assert sr1 == sr2


def test_emit_campaign_contract_cli_writes_json(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_campaign_contract import main

    assert main(["--output-dir", str(tmp_path)]) == 0
    assert (tmp_path / "px2_self_play_campaign_contract.json").is_file()
    assert (tmp_path / "px2_self_play_campaign_contract_report.json").is_file()


def test_emit_smoke_run_cli_writes_four_artifacts(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_smoke_run import main

    rc = main(
        [
            "--output-dir",
            str(tmp_path),
            "--corpus-root",
            str(CORPUS),
        ]
    )
    assert rc == 0
    assert (tmp_path / "px2_self_play_smoke_run.json").is_file()
    assert (tmp_path / "px2_self_play_smoke_run_report.json").is_file()


def test_campaign_execution_skeleton_deterministic_artifacts(tmp_path: Path) -> None:
    run_id = "px2_test_skeleton_run_fixed_001"
    s1 = run_px2_campaign_execution_skeleton(
        corpus_root=CORPUS,
        output_dir=tmp_path / "a",
        campaign_id="px2_skeleton_ci",
        campaign_profile_id="px2_skeleton_profile",
        run_id=run_id,
        torch_seed=7,
        fixture_episode_count=3,
        checkpoint_episode_cadence=2,
        eval_episode_cadence=2,
    )
    s2 = run_px2_campaign_execution_skeleton(
        corpus_root=CORPUS,
        output_dir=tmp_path / "b",
        campaign_id="px2_skeleton_ci",
        campaign_profile_id="px2_skeleton_profile",
        run_id=run_id,
        torch_seed=7,
        fixture_episode_count=3,
        checkpoint_episode_cadence=2,
        eval_episode_cadence=2,
    )
    assert s1["run_sha256"] == s2["run_sha256"]
    assert s1["checkpoint_paths"] == s2["checkpoint_paths"]
    assert s1["evaluation_paths"] == s2["evaluation_paths"]

    run_path = tmp_path / "a" / "px2_self_play_campaign_run.json"
    run_json = json.loads(run_path.read_text(encoding="utf-8"))
    assert run_json["contract_id"] == PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID
    assert run_json["execution_kind"] == EXECUTION_KIND_SLICE2
    assert run_json["run_id"] == run_id
    sealed = {k: v for k, v in run_json.items() if k != "run_sha256"}
    assert run_json["run_sha256"] == sha256_hex_of_canonical_json(sealed)

    manifest = json.loads((tmp_path / "a" / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_id"] == run_id
    assert manifest["execution_kind"] == EXECUTION_KIND_SLICE2

    ck = tmp_path / "a" / "checkpoint_receipts"
    ev = tmp_path / "a" / "evaluation_receipts"
    assert (ck / "ckpt_ep002.json").is_file() and (ck / "ckpt_ep002_report.json").is_file()
    assert (ev / "eval_ep002.json").is_file() and (ev / "eval_ep002_report.json").is_file()
    # games_done=3 with cadence 2 => no boundary at episode 3 (3 % 2 != 0)
    assert not (ck / "ckpt_ep003.json").exists()
    assert s1["checkpoint_paths"] == ["checkpoint_receipts/ckpt_ep002.json"]
    assert s1["evaluation_paths"] == ["evaluation_receipts/eval_ep002.json"]

    ck_body = json.loads((ck / "ckpt_ep002.json").read_text(encoding="utf-8"))
    assert ck_body["episode_index_one_based"] == 2
    ev_body = json.loads((ev / "eval_ep002.json").read_text(encoding="utf-8"))
    assert ev_body["episode_index_one_based"] == 2

    episodes = run_json["episodes"]
    assert len(episodes) == 3
    refs = [e["opponent_snapshot_ref"] for e in episodes]
    pool = build_default_opponent_pool_stub()
    expect = [
        select_opponent_ref(
            step_index=i,
            rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
            ref_ids=tuple(r.ref_id for r in pool.snapshot_refs),
        )
        for i in range(3)
    ]
    assert refs == expect


def test_emit_campaign_execution_skeleton_cli_writes_tree(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_campaign_execution_skeleton import main

    out = tmp_path / "skel"
    rc = main(
        [
            "--output-dir",
            str(out),
            "--corpus-root",
            str(CORPUS),
            "--run-id",
            "cli_fixed_run_01",
            "--torch-seed",
            "3",
        ]
    )
    assert rc == 0
    assert (out / "px2_self_play_campaign_run.json").is_file()
    assert (out / "run_manifest.json").is_file()
    assert (out / "checkpoint_receipts" / "ckpt_ep002.json").is_file()
