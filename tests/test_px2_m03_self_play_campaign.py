"""PX2-M03 slice 1 — campaign contract, bridge, opponent selection, smoke JSON (CPU)."""

from __future__ import annotations

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
