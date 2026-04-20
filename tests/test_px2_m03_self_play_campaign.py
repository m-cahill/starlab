"""PX2-M03 self-play tests: slices 1–4 (incl. continuity). CPU fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy
from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE4,
    PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID,
    run_operator_local_campaign_continuity,
)
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
from starlab.sc2.px2.self_play.execution_preflight import (
    PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID,
    run_execution_preflight,
)
from starlab.sc2.px2.self_play.operator_local_smoke import (
    EXECUTION_KIND_SLICE3,
    PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID,
    run_operator_local_campaign_smoke,
)
from starlab.sc2.px2.self_play.opponent_selection import (
    OPPONENT_SELECTION_FROZEN_SEED,
    OPPONENT_SELECTION_ROUND_ROBIN,
    OPPONENT_SELECTION_SELF_SNAPSHOT,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.promotion_receipts import PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID
from starlab.sc2.px2.self_play.rollback_receipts import PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID
from starlab.sc2.px2.self_play.smoke_run import (
    PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID,
    run_px2_fixture_self_play_smoke,
)
from starlab.sc2.px2.self_play.snapshot_pool import build_default_opponent_pool_stub
from starlab.sc2.px2.self_play.weight_loading import (
    build_policy_operator_local,
    sha256_hex_file,
)

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


def test_sha256_hex_file_stable(tmp_path: Path) -> None:
    p = tmp_path / "w.bin"
    p.write_bytes(b"abc")
    assert sha256_hex_file(p) == sha256_hex_file(p)


def test_preflight_init_only_ok(tmp_path: Path) -> None:
    out = tmp_path / "out"
    ok, pre, rep, err = run_execution_preflight(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=True,
        weights_path=None,
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf1",
    )
    assert ok and not err
    assert pre["contract_id"] == PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID
    sealed = {k: v for k, v in pre.items() if k != "preflight_sha256"}
    assert pre["preflight_sha256"] == sha256_hex_of_canonical_json(sealed)
    assert rep["summary"]["preflight_ok"] is True


def test_preflight_fails_missing_corpus(tmp_path: Path) -> None:
    ok, _, _, err = run_execution_preflight(
        corpus_root=tmp_path / "nope",
        output_dir=tmp_path / "out",
        init_only=True,
        weights_path=None,
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf2",
    )
    assert not ok
    assert "corpus_root_not_found" in err


def test_preflight_init_only_rejects_weights_path(tmp_path: Path) -> None:
    w = tmp_path / "w.pt"
    w.write_bytes(b"x")
    ok, _, _, err = run_execution_preflight(
        corpus_root=CORPUS,
        output_dir=tmp_path / "out",
        init_only=True,
        weights_path=w,
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf3",
    )
    assert not ok
    assert "weights_path_forbidden_when_init_only" in err


def test_preflight_not_init_requires_weights(tmp_path: Path) -> None:
    ok, _, _, err = run_execution_preflight(
        corpus_root=CORPUS,
        output_dir=tmp_path / "out",
        init_only=False,
        weights_path=None,
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf4",
    )
    assert not ok
    assert "weights_path_required_when_not_init_only" in err


def test_preflight_missing_weight_file(tmp_path: Path) -> None:
    ok, _, _, err = run_execution_preflight(
        corpus_root=CORPUS,
        output_dir=tmp_path / "out",
        init_only=False,
        weights_path=tmp_path / "missing.pt",
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf5",
    )
    assert not ok
    assert "weights_file_missing" in err


def test_preflight_invalid_weights_file(tmp_path: Path) -> None:
    bad = tmp_path / "bad.pt"
    bad.write_bytes(b"not_a_torch_file")
    ok, _, _, err = run_execution_preflight(
        corpus_root=CORPUS,
        output_dir=tmp_path / "out",
        init_only=False,
        weights_path=bad,
        weight_bundle_ref=None,
        torch_seed=1,
        run_id="pf6",
    )
    assert not ok
    assert "weights_load_failed" in err


def test_build_policy_init_only_matches_seed(tmp_path: Path) -> None:
    m1, meta1 = build_policy_operator_local(init_only=True, weights_path=None, torch_seed=5)
    m2, meta2 = build_policy_operator_local(init_only=True, weights_path=None, torch_seed=5)
    assert meta1["weight_mode"] == "init_only"
    sd1 = m1.state_dict()
    sd2 = m2.state_dict()
    assert all(torch.equal(sd1[k], sd2[k]) for k in sd1)


def test_build_policy_from_weights_file_roundtrip(tmp_path: Path) -> None:
    m0 = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    path = tmp_path / "policy.pt"
    torch.save(m0.state_dict(), path)
    m1, meta = build_policy_operator_local(init_only=False, weights_path=path, torch_seed=0)
    assert meta["weights_file_sha256"] == sha256_hex_file(path)
    assert meta["weight_mode"] == "weights_file"
    assert torch.equal(m0.fc1.weight, m1.fc1.weight)


def test_operator_local_smoke_init_only_writes_artifacts(tmp_path: Path) -> None:
    out = tmp_path / "ol"
    run = run_operator_local_campaign_smoke(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=True,
        weights_path=None,
        weight_bundle_ref=None,
        torch_seed=11,
        run_id="ol_run_fixed",
        episode_budget=2,
    )
    assert run["run_id"] == "ol_run_fixed"
    sm = json.loads((out / "px2_self_play_operator_local_smoke.json").read_text(encoding="utf-8"))
    assert sm["contract_id"] == PX2_SELF_PLAY_OPERATOR_LOCAL_SMOKE_CONTRACT_ID
    assert sm["execution_kind"] == EXECUTION_KIND_SLICE3
    assert sm["weight_identity"]["weight_mode"] == "init_only"
    seal = {k: v for k, v in sm.items() if k != "operator_local_smoke_sha256"}
    assert sm["operator_local_smoke_sha256"] == sha256_hex_of_canonical_json(seal)
    assert (out / "px2_self_play_execution_preflight.json").is_file()


def test_operator_local_smoke_with_weights_file(tmp_path: Path) -> None:
    out = tmp_path / "ol2"
    wpath = tmp_path / "p.pt"
    pol = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    torch.save(pol.state_dict(), wpath)
    run = run_operator_local_campaign_smoke(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=False,
        weights_path=wpath,
        torch_seed=3,
        run_id="ol_w",
        episode_budget=1,
    )
    sm = json.loads((out / "px2_self_play_operator_local_smoke.json").read_text(encoding="utf-8"))
    assert sm["weight_identity"]["weight_mode"] == "weights_file"
    assert sm["weight_identity"]["weights_file_sha256"] == sha256_hex_file(wpath)
    assert run["run_id"] == "ol_w"


def test_build_policy_rejects_init_only_with_path(tmp_path: Path) -> None:
    p = tmp_path / "x.pt"
    p.write_bytes(b"a")
    with pytest.raises(ValueError, match="weights_path must be None"):
        build_policy_operator_local(init_only=True, weights_path=p, torch_seed=0)


def test_build_policy_requires_path_when_not_init_only(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="weights_path is required"):
        build_policy_operator_local(init_only=False, weights_path=None, torch_seed=0)


def test_operator_local_smoke_raises_when_preflight_fails(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="preflight failed"):
        run_operator_local_campaign_smoke(
            corpus_root=tmp_path / "missing_corpus",
            output_dir=tmp_path / "out",
            init_only=True,
            weights_path=None,
            run_id="fail",
            episode_budget=1,
        )


def test_emit_execution_preflight_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_execution_preflight import main

    out = tmp_path / "pf"
    assert (
        main(
            [
                "--output-dir",
                str(out),
                "--corpus-root",
                str(CORPUS),
                "--init-only",
                "--run-id",
                "cli_pf",
            ]
        )
        == 0
    )
    assert (out / "px2_self_play_execution_preflight.json").is_file()


def test_emit_operator_local_smoke_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_smoke import main

    out = tmp_path / "ols"
    assert (
        main(
            [
                "--output-dir",
                str(out),
                "--corpus-root",
                str(CORPUS),
                "--init-only",
                "--episodes",
                "1",
                "--run-id",
                "cli_ol",
            ]
        )
        == 0
    )
    assert (out / "px2_self_play_operator_local_smoke.json").is_file()


def test_operator_local_continuity_deterministic_init_only(tmp_path: Path) -> None:
    rid = "px2_cont_fixed_run_001"
    out = tmp_path / "same_out"
    s1 = run_operator_local_campaign_continuity(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=True,
        weights_path=None,
        torch_seed=7,
        run_id=rid,
        continuity_step_count=3,
    )
    s2 = run_operator_local_campaign_continuity(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=True,
        weights_path=None,
        torch_seed=7,
        run_id=rid,
        continuity_step_count=3,
    )
    assert s1["continuity_sha256"] == s2["continuity_sha256"]
    assert s1["continuity_chain_sha256"] == s2["continuity_chain_sha256"]

    root = out
    cont = json.loads((root / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8"))
    assert cont["contract_id"] == PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID
    assert cont["execution_kind"] == EXECUTION_KIND_SLICE4
    sealed = {k: v for k, v in cont.items() if k != "continuity_sha256"}
    assert cont["continuity_sha256"] == sha256_hex_of_canonical_json(sealed)

    assert (root / "checkpoint_receipts" / "ckpt_step001.json").is_file()
    assert (root / "evaluation_receipts" / "eval_step001.json").is_file()
    assert (root / "promotion_receipts" / "promotion_step001.json").is_file()
    assert (root / "rollback_receipts" / "rollback_step001.json").is_file()
    assert (root / "continuity_chain.json").is_file()

    ck1 = json.loads(
        (root / "checkpoint_receipts" / "ckpt_step001.json").read_text(encoding="utf-8")
    )
    ev1 = json.loads(
        (root / "evaluation_receipts" / "eval_step001.json").read_text(encoding="utf-8")
    )
    assert ck1["preflight_sha256"] == cont["preflight_sha256"]
    assert ev1["link_checkpoint_receipt_sha256"] == ck1["checkpoint_receipt_sha256"]

    pr2 = json.loads(
        (root / "promotion_receipts" / "promotion_step002.json").read_text(encoding="utf-8")
    )
    assert pr2["contract_id"] == PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID
    assert pr2["prior_promotion_receipt_sha256"] is not None

    rb3 = json.loads(
        (root / "rollback_receipts" / "rollback_step003.json").read_text(encoding="utf-8")
    )
    assert rb3["contract_id"] == PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID
    assert rb3["triggered"] is False

    steps = cont["step_records"]
    assert len(steps) == 3
    ck2 = json.loads(
        (root / "checkpoint_receipts" / "ckpt_step002.json").read_text(encoding="utf-8")
    )
    assert ck2["prior_checkpoint_receipt_sha256"] == steps[0]["checkpoint_receipt_sha256"]
    assert ck2["prior_evaluation_receipt_sha256"] == steps[0]["evaluation_receipt_sha256"]


def test_operator_local_continuity_with_weights(tmp_path: Path) -> None:
    wpath = tmp_path / "pol.pt"
    pol = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    torch.save(pol.state_dict(), wpath)
    out = tmp_path / "cw"
    run_operator_local_campaign_continuity(
        corpus_root=CORPUS,
        output_dir=out,
        init_only=False,
        weights_path=wpath,
        torch_seed=1,
        run_id="wcont",
        continuity_step_count=2,
    )
    cont = json.loads((out / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8"))
    assert cont["weight_identity"]["weights_file_sha256"] == sha256_hex_file(wpath)


def test_emit_campaign_continuity_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_campaign_continuity import main

    out = tmp_path / "cc"
    assert (
        main(
            [
                "--output-dir",
                str(out),
                "--corpus-root",
                str(CORPUS),
                "--init-only",
                "--steps",
                "2",
                "--run-id",
                "cli_cc",
            ]
        )
        == 0
    )
    assert (out / "px2_self_play_campaign_continuity.json").is_file()
