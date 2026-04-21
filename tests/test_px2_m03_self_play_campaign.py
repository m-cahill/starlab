"""PX2-M03 self-play tests for slices 1–11 (CPU fixtures)."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest
import torch
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy
from starlab.sc2.px2.self_play.campaign_continuity import (
    EXECUTION_KIND_SLICE4,
    EXECUTION_KIND_SLICE5,
    EXECUTION_KIND_SLICE6,
    EXECUTION_KIND_SLICE7,
    EXECUTION_KIND_SLICE8,
    EXECUTION_KIND_SLICE9,
    EXECUTION_KIND_SLICE10,
    EXECUTION_KIND_SLICE11,
    PX2_SELF_PLAY_CAMPAIGN_CONTINUITY_CONTRACT_ID,
    run_operator_local_campaign_continuity,
)
from starlab.sc2.px2.self_play.campaign_contract import (
    PX2_SELF_PLAY_CAMPAIGN_CONTRACT_ID,
    build_px2_self_play_campaign_artifacts,
    seal_px2_self_play_campaign_body,
)
from starlab.sc2.px2.self_play.campaign_root import run_slice5_operator_local_campaign
from starlab.sc2.px2.self_play.campaign_root_manifest import (
    PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.campaign_run import (
    EXECUTION_KIND_SLICE2,
    PX2_SELF_PLAY_CAMPAIGN_RUN_CONTRACT_ID,
    run_px2_campaign_execution_skeleton,
)
from starlab.sc2.px2.self_play.canonical_operator_local_run import (
    resolve_canonical_campaign_root,
    run_canonical_operator_local_campaign_root_smoke,
)
from starlab.sc2.px2.self_play.continuation_run import (
    CONTINUATION_RUN_JSON,
    run_bounded_continuation_run_consuming_current_candidate,
)
from starlab.sc2.px2.self_play.continuation_run_record import (
    CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB,
    PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.current_candidate import (
    DEFAULT_SLICE10_CAMPAIGN_ID,
    next_run_preflight_hints_from_current_candidate,
    run_bounded_operator_local_session_transition_with_current_candidate,
)
from starlab.sc2.px2.self_play.current_candidate_record import (
    CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB,
    PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.execution_preflight import (
    PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID,
    run_execution_preflight,
)
from starlab.sc2.px2.self_play.operator_local_real_run import (
    DEFAULT_SLICE7_CAMPAIGN_ID,
    run_bounded_operator_local_real_run,
)
from starlab.sc2.px2.self_play.operator_local_real_run_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.operator_local_session import (
    DEFAULT_SLICE8_CAMPAIGN_ID,
    run_bounded_operator_local_session,
)
from starlab.sc2.px2.self_play.operator_local_session_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID,
)
from starlab.sc2.px2.self_play.operator_local_session_transition import (
    DEFAULT_SLICE9_CAMPAIGN_ID,
    run_bounded_operator_local_session_with_transition,
)
from starlab.sc2.px2.self_play.operator_local_session_transition_record import (
    PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID,
    TRANSITION_RULE_PROMOTION_LAST_RUN,
    TRANSITION_RULE_ROLLBACK_FIRST_RUN_BASELINE,
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
    OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
    select_opponent_ref,
)
from starlab.sc2.px2.self_play.policy_runtime_bridge import bootstrap_policy_runtime_step
from starlab.sc2.px2.self_play.promotion_receipts import PX2_SELF_PLAY_PROMOTION_RECEIPT_CONTRACT_ID
from starlab.sc2.px2.self_play.rollback_receipts import PX2_SELF_PLAY_ROLLBACK_RECEIPT_CONTRACT_ID
from starlab.sc2.px2.self_play.smoke_run import (
    PX2_SELF_PLAY_SMOKE_RUN_CONTRACT_ID,
    run_px2_fixture_self_play_smoke,
)
from starlab.sc2.px2.self_play.snapshot_pool import (
    DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS,
    build_default_opponent_pool_stub,
    build_slice5_opponent_pool,
    opponent_battle_ref_ids,
    opponent_pool_identity_sha256,
)
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


def test_opponent_selection_weighted_frozen_stub() -> None:
    refs = ("a", "b", "c")
    weights = (2, 1, 1)
    expanded_expect = ["a", "a", "b", "c"]
    for step, exp in enumerate(expanded_expect * 2):
        got = select_opponent_ref(
            step_index=step,
            rule_id=OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
            ref_ids=refs,
            weights=weights,
        )
        assert got == exp


def test_opponent_selection_weighted_requires_weights() -> None:
    with pytest.raises(ValueError, match="weights required"):
        select_opponent_ref(
            step_index=0,
            rule_id=OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
            ref_ids=("a", "b"),
        )


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
    assert pre["preflight_sha256"] == sha256_hex_of_canonical_json(pre["preflight_seal_basis"])
    assert "corpus_root" in pre and Path(pre["corpus_root"]).is_dir()
    assert rep["summary"]["preflight_ok"] is True
    assert rep["operator_absolute_paths_advisory"]["corpus_root"] == pre["corpus_root"]


def test_preflight_seal_stable_across_distinct_temp_roots() -> None:
    """Logical seal matches for the same run_id + fixture corpus even when output roots differ."""

    def run_one(base: Path) -> str:
        out = base / "out"
        ok, pre, _, err = run_execution_preflight(
            corpus_root=CORPUS,
            output_dir=out,
            init_only=True,
            weights_path=None,
            weight_bundle_ref=None,
            torch_seed=1,
            run_id="pf_cross",
        )
        assert ok and not err
        return str(pre["preflight_sha256"])

    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        assert run_one(Path(a)) == run_one(Path(b))


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
    assert "opponent_rotation_trace" in cont["episodes"][0]
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


def test_slice5_opponent_pool_identity_and_battle_refs() -> None:
    pool = build_slice5_opponent_pool(campaign_tag="t")
    battle = opponent_battle_ref_ids(pool)
    assert len(battle) == 4
    assert pool.seed_policy_ref_id not in battle
    id1 = opponent_pool_identity_sha256(pool)
    id2 = opponent_pool_identity_sha256(build_slice5_opponent_pool(campaign_tag="t"))
    assert id1 == id2


def test_slice5_campaign_root_manifest_deterministic_repeat(tmp_path: Path) -> None:
    """Repeat with identical paths for stable continuity + root-manifest hashes."""

    rid = "px2_slice5_fixed_run"
    fixed_cid = "px2_m03_slice5_ci"
    root = tmp_path / "camp"
    a1 = run_slice5_operator_local_campaign(
        corpus_root=CORPUS,
        campaign_root=root,
        init_only=True,
        campaign_id=fixed_cid,
        torch_seed=21,
        run_id=rid,
        continuity_step_count=2,
    )
    shutil.rmtree(root)
    a2 = run_slice5_operator_local_campaign(
        corpus_root=CORPUS,
        campaign_root=root,
        init_only=True,
        campaign_id=fixed_cid,
        torch_seed=21,
        run_id=rid,
        continuity_step_count=2,
    )
    assert a1["campaign_root_manifest_sha256"] == a2["campaign_root_manifest_sha256"]
    assert a1["continuity_sha256"] == a2["continuity_sha256"]

    mpath = root / "px2_self_play_campaign_root_manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    assert manifest["contract_id"] == PX2_SELF_PLAY_CAMPAIGN_ROOT_MANIFEST_CONTRACT_ID
    sealed = {k: v for k, v in manifest.items() if k != "campaign_root_manifest_sha256"}
    assert manifest["campaign_root_manifest_sha256"] == sha256_hex_of_canonical_json(sealed)
    assert (root / "opponent_pool" / "px2_opponent_pool_metadata.json").is_file()
    run_dir = root / "runs" / rid
    cont = json.loads(
        (run_dir / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    assert cont["execution_kind"] == EXECUTION_KIND_SLICE5
    assert cont["opponent_pool_identity_sha256"] == manifest["opponent_pool_identity_sha256"]
    pool = build_slice5_opponent_pool(campaign_tag=fixed_cid.replace("/", "_"))
    expect_rr = [
        select_opponent_ref(
            step_index=i,
            rule_id=OPPONENT_SELECTION_ROUND_ROBIN,
            ref_ids=opponent_battle_ref_ids(pool),
        )
        for i in range(2)
    ]
    refs = [e["opponent_snapshot_ref"] for e in cont["episodes"]]
    assert refs == expect_rr
    assert [e["opponent_rotation_trace"]["selected_opponent_ref"] for e in cont["episodes"]] == refs


def test_slice6_canonical_campaign_root_smoke_layout_and_kind(tmp_path: Path) -> None:
    cid = "px2_m03_slice6_canonical_smoke"
    rid = "px2_slice6_layout"
    root = resolve_canonical_campaign_root(cid, base_dir=tmp_path)
    assert root == tmp_path / "out" / "px2_self_play_campaigns" / cid
    summary = run_canonical_operator_local_campaign_root_smoke(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        torch_seed=11,
        run_id=rid,
        continuity_step_count=2,
    )
    assert Path(summary["campaign_root"]) == root
    cont = json.loads(
        (root / "runs" / rid / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    assert cont["execution_kind"] == EXECUTION_KIND_SLICE6
    assert (root / "px2_self_play_campaign_root_manifest.json").is_file()


def test_slice6_canonical_smoke_stable_across_distinct_base_dirs(tmp_path: Path) -> None:
    """Same logical campaign id + run id → same sealed continuity + root manifest across bases."""

    cid = "px2_m03_slice6_canonical_smoke"
    rid = "px2_slice6_cross_base"
    base1 = tmp_path / "w1"
    base2 = tmp_path / "w2"
    base1.mkdir()
    base2.mkdir()
    s1 = run_canonical_operator_local_campaign_root_smoke(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=base1,
        init_only=True,
        torch_seed=9,
        run_id=rid,
        continuity_step_count=2,
    )
    s2 = run_canonical_operator_local_campaign_root_smoke(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=base2,
        init_only=True,
        torch_seed=9,
        run_id=rid,
        continuity_step_count=2,
    )
    assert s1["continuity_sha256"] == s2["continuity_sha256"]
    assert s1["campaign_root_manifest_sha256"] == s2["campaign_root_manifest_sha256"]


def test_emit_canonical_campaign_root_smoke_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_canonical_campaign_root_smoke import main

    base = tmp_path / "op"
    base.mkdir()
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--base-dir",
                str(base),
                "--init-only",
                "--run-id",
                "cli_slice6",
                "--steps",
                "2",
            ]
        )
        == 0
    )
    root = base / "out" / "px2_self_play_campaigns" / "px2_m03_slice6_canonical_smoke"
    assert (root / "px2_self_play_campaign_root_manifest.json").is_file()


def test_slice7_bounded_real_run_init_only_emits_record(tmp_path: Path) -> None:
    cid = "px2_m03_slice7_ci"
    rid = "px2_slice7_real"
    out = run_bounded_operator_local_real_run(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        torch_seed=13,
        run_id=rid,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    assert (root / "px2_self_play_operator_local_real_run.json").is_file()
    assert (root / "px2_self_play_operator_local_real_run_report.json").is_file()
    rr = json.loads(
        (root / "px2_self_play_operator_local_real_run.json").read_text(encoding="utf-8")
    )
    assert rr["contract_id"] == PX2_SELF_PLAY_OPERATOR_LOCAL_REAL_RUN_CONTRACT_ID
    assert rr["execution_kind"] == EXECUTION_KIND_SLICE7
    assert rr["run_id"] == rid
    basis_only = {
        k: v
        for k, v in rr.items()
        if k
        not in (
            "operator_local_real_run_sha256",
            "weight_identity",
            "operator_note_convention",
            "campaign_root_resolved_posix",
        )
    }
    assert rr["operator_local_real_run_sha256"] == sha256_hex_of_canonical_json(basis_only)
    cont = json.loads(
        (root / "runs" / rid / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    assert cont["execution_kind"] == EXECUTION_KIND_SLICE7
    assert out["preflight_sha256"] == cont["preflight_sha256"]
    chain = json.loads((root / "runs" / rid / "continuity_chain.json").read_text(encoding="utf-8"))
    assert out["continuity_chain_sha256"] == chain["continuity_chain_sha256"]


def test_slice7_bounded_real_run_with_weights(tmp_path: Path) -> None:
    wpath = tmp_path / "slice7w.pt"
    pol = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    torch.save(pol.state_dict(), wpath)
    cid = "px2_m03_slice7_weights"
    rid = "wrun7"
    out = run_bounded_operator_local_real_run(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=False,
        weights_path=wpath,
        torch_seed=2,
        run_id=rid,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    rr = json.loads(
        (root / "px2_self_play_operator_local_real_run.json").read_text(encoding="utf-8")
    )
    assert rr["weights_path_basename"] == wpath.name
    assert rr["weight_mode"] == "weights_file"


def test_slice7_real_run_deterministic_repeat_fixed_paths(tmp_path: Path) -> None:
    cid = "px2_m03_slice7_det"
    rid = "det_run"
    root = tmp_path / "camp"
    a1 = run_bounded_operator_local_real_run(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=root,
        init_only=True,
        torch_seed=99,
        run_id=rid,
        continuity_step_count=2,
    )
    shutil.rmtree(root / "out")
    a2 = run_bounded_operator_local_real_run(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=root,
        init_only=True,
        torch_seed=99,
        run_id=rid,
        continuity_step_count=2,
    )
    assert a1["operator_local_real_run_sha256"] == a2["operator_local_real_run_sha256"]
    assert a1["continuity_sha256"] == a2["continuity_sha256"]


def test_emit_operator_local_real_run_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_real_run import main

    base = tmp_path / "op7"
    base.mkdir()
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--base-dir",
                str(base),
                "--init-only",
                "--run-id",
                "cli_slice7",
                "--campaign-id",
                DEFAULT_SLICE7_CAMPAIGN_ID,
                "--steps",
                "2",
            ]
        )
        == 0
    )
    root = base / "out" / "px2_self_play_campaigns" / DEFAULT_SLICE7_CAMPAIGN_ID
    assert (root / "px2_self_play_operator_local_real_run.json").is_file()


def test_slice8_bounded_session_init_only_emits_session_and_runs(tmp_path: Path) -> None:
    cid = "px2_m03_slice8_ci"
    r1, r2 = "sess_run_a", "sess_run_b"
    out = run_bounded_operator_local_session(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=7,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    assert (root / "px2_self_play_operator_local_session.json").is_file()
    assert (root / "px2_self_play_operator_local_session_report.json").is_file()
    assert (root / "px2_self_play_campaign_root_manifest.json").is_file()
    sess = json.loads(
        (root / "px2_self_play_operator_local_session.json").read_text(encoding="utf-8")
    )
    assert sess["contract_id"] == PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_CONTRACT_ID
    assert sess["execution_kind"] == EXECUTION_KIND_SLICE8
    assert sess["ordered_run_ids"] == [r1, r2]
    basis_only = {
        k: v
        for k, v in sess.items()
        if k
        not in (
            "operator_local_session_sha256",
            "operator_note_convention",
            "campaign_root_resolved_posix",
        )
    }
    assert sess["operator_local_session_sha256"] == sha256_hex_of_canonical_json(basis_only)
    rm = json.loads(
        (root / "px2_self_play_campaign_root_manifest.json").read_text(encoding="utf-8")
    )
    assert len(rm["continuity_run_references"]) == 2
    for rid in (r1, r2):
        rd = root / "runs" / rid
        assert (rd / "px2_self_play_campaign_continuity.json").is_file()
        rr = json.loads(
            (rd / "px2_self_play_operator_local_real_run.json").read_text(encoding="utf-8")
        )
        assert rr["execution_kind"] == EXECUTION_KIND_SLICE8
        assert rr["run_id"] == rid
    assert out["ordered_run_ids"] == [r1, r2]


def test_slice8_session_deterministic_repeat_fixed_paths(tmp_path: Path) -> None:
    cid = "px2_m03_slice8_det"
    base = tmp_path / "s8"
    ids = ["s8a", "s8b"]
    a = run_bounded_operator_local_session(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=21,
        continuity_step_count=2,
    )
    shutil.rmtree(base / "out")
    b = run_bounded_operator_local_session(
        corpus_root=CORPUS,
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=21,
        continuity_step_count=2,
    )
    assert a["operator_local_session_sha256"] == b["operator_local_session_sha256"]
    assert a["campaign_root_manifest_sha256"] == b["campaign_root_manifest_sha256"]


def test_emit_operator_local_session_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session import main

    base = tmp_path / "op8"
    base.mkdir()
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--base-dir",
                str(base),
                "--init-only",
                "--run-ids",
                "cli_a",
                "cli_b",
                "--campaign-id",
                DEFAULT_SLICE8_CAMPAIGN_ID,
                "--steps",
                "2",
            ]
        )
        == 0
    )
    root = base / "out" / "px2_self_play_campaigns" / DEFAULT_SLICE8_CAMPAIGN_ID
    assert (root / "px2_self_play_operator_local_session.json").is_file()


def test_slice9_promotion_init_only_emits_transition_and_seal(tmp_path: Path) -> None:
    cid = "px2_m03_slice9_ci"
    r1, r2 = "sess_tr_a", "sess_tr_b"
    out = run_bounded_operator_local_session_with_transition(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=7,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    assert (root / "px2_self_play_operator_local_session_transition.json").is_file()
    assert (root / "px2_self_play_operator_local_session_transition_report.json").is_file()
    tm = json.loads(
        (root / "px2_self_play_operator_local_session_transition.json").read_text(encoding="utf-8")
    )
    assert tm["contract_id"] == PX2_SELF_PLAY_OPERATOR_LOCAL_SESSION_TRANSITION_CONTRACT_ID
    assert tm["execution_kind"] == EXECUTION_KIND_SLICE9
    assert tm["transition_type"] == "promotion"
    assert tm["transition_rule_id"] == TRANSITION_RULE_PROMOTION_LAST_RUN
    assert tm["current_run_id_after_transition"] == r2
    assert tm["ordered_run_ids"] == [r1, r2]
    cont_last = json.loads(
        (root / "runs" / r2 / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    last_step = cont_last["step_records"][-1]
    assert (
        tm["source_receipt_lineage"]["promotion_receipt_sha256"]
        == last_step["promotion_receipt_sha256"]
    )
    assert (
        tm["source_receipt_lineage"]["checkpoint_receipt_sha256"]
        == last_step["checkpoint_receipt_sha256"]
    )
    basis_only = {
        k: v
        for k, v in tm.items()
        if k
        not in (
            "operator_local_session_transition_sha256",
            "operator_note_convention",
            "campaign_root_resolved_posix",
        )
    }
    assert tm["operator_local_session_transition_sha256"] == sha256_hex_of_canonical_json(
        basis_only
    )
    rep = json.loads(
        (root / "px2_self_play_operator_local_session_transition_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert rep["summary"]["transition_type"] == "promotion"
    assert rep["summary"]["current_run_id_after_transition"] == r2


def test_slice9_rollback_init_only_current_is_first_run(tmp_path: Path) -> None:
    cid = "px2_m03_slice9_rb"
    r1, r2 = "rb_a", "rb_b"
    out = run_bounded_operator_local_session_with_transition(
        corpus_root=CORPUS,
        transition_kind="rollback",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=11,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    tm = json.loads(
        (root / "px2_self_play_operator_local_session_transition.json").read_text(encoding="utf-8")
    )
    assert tm["transition_type"] == "rollback"
    assert tm["transition_rule_id"] == TRANSITION_RULE_ROLLBACK_FIRST_RUN_BASELINE
    assert tm["current_run_id_after_transition"] == r1
    cont_first = json.loads(
        (root / "runs" / r1 / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    cont_last = json.loads(
        (root / "runs" / r2 / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    first0 = cont_first["step_records"][0]
    last_fin = cont_last["step_records"][-1]
    assert (
        tm["source_receipt_lineage"]["baseline_checkpoint_receipt_sha256"]
        == first0["checkpoint_receipt_sha256"]
    )
    assert (
        tm["source_receipt_lineage"]["reference_last_run_final_rollback_receipt_sha256"]
        == last_fin["rollback_receipt_sha256"]
    )


def test_slice9_transition_deterministic_repeat_fixed_paths(tmp_path: Path) -> None:
    cid = "px2_m03_slice9_det"
    base = tmp_path / "s9"
    ids = ["s9a", "s9b"]
    a = run_bounded_operator_local_session_with_transition(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=31,
        continuity_step_count=2,
    )
    shutil.rmtree(base / "out")
    b = run_bounded_operator_local_session_with_transition(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=31,
        continuity_step_count=2,
    )
    assert (
        a["operator_local_session_transition_sha256"]
        == b["operator_local_session_transition_sha256"]
    )
    assert a["operator_local_session_sha256"] == b["operator_local_session_sha256"]


def test_emit_operator_local_session_transition_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session_transition import main

    base = tmp_path / "op9"
    base.mkdir()
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--base-dir",
                str(base),
                "--init-only",
                "--transition",
                "promotion",
                "--run-ids",
                "cli_tr_a",
                "cli_tr_b",
                "--campaign-id",
                DEFAULT_SLICE9_CAMPAIGN_ID,
                "--steps",
                "2",
            ]
        )
        == 0
    )
    root = base / "out" / "px2_self_play_campaigns" / DEFAULT_SLICE9_CAMPAIGN_ID
    assert (root / "px2_self_play_operator_local_session_transition.json").is_file()


def test_slice10_promotion_emits_current_candidate_seal_and_hints(tmp_path: Path) -> None:
    cid = "px2_m03_slice10_ci"
    r1, r2 = "cc_a", "cc_b"
    out = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=5,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    assert (root / "px2_self_play_current_candidate.json").is_file()
    assert (root / "px2_self_play_current_candidate_report.json").is_file()
    cc = json.loads((root / "px2_self_play_current_candidate.json").read_text(encoding="utf-8"))
    assert cc["contract_id"] == PX2_SELF_PLAY_CURRENT_CANDIDATE_CONTRACT_ID
    assert cc["execution_kind"] == EXECUTION_KIND_SLICE10
    assert cc["current_candidate_rule_id"] == CURRENT_CANDIDATE_RULE_FROM_TRANSITION_STUB
    assert (
        cc["operator_local_session_transition_sha256"]
        == out["operator_local_session_transition_sha256"]
    )
    assert cc["current_run_id_after_transition"] == r2
    anchor = cc["anchor"]
    assert anchor["continuity_run_id"] == r2
    cont = json.loads(
        (root / "runs" / r2 / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    last_step = cont["step_records"][-1]
    assert anchor["checkpoint_receipt_sha256"] == last_step["checkpoint_receipt_sha256"]
    assert cc["weight_identity"] == cont["weight_identity"]
    basis_only = {
        k: v
        for k, v in cc.items()
        if k
        not in (
            "current_candidate_sha256",
            "operator_note_convention",
            "campaign_root_resolved_posix",
        )
    }
    assert cc["current_candidate_sha256"] == sha256_hex_of_canonical_json(basis_only)
    hints = next_run_preflight_hints_from_current_candidate(root)
    assert hints is not None
    assert hints["anchor_continuity_run_id"] == r2
    assert hints["checkpoint_receipt_sha256"] == last_step["checkpoint_receipt_sha256"]
    assert (
        hints["operator_local_session_transition_sha256"]
        == out["operator_local_session_transition_sha256"]
    )


def test_slice10_rollback_anchor_first_run(tmp_path: Path) -> None:
    cid = "px2_m03_slice10_rb"
    r1, r2 = "cc_rb_a", "cc_rb_b"
    out = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="rollback",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=9,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    cc = json.loads((root / "px2_self_play_current_candidate.json").read_text(encoding="utf-8"))
    assert cc["anchor"]["continuity_run_id"] == r1
    cont = json.loads(
        (root / "runs" / r1 / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    first_step = cont["step_records"][0]
    assert cc["anchor"]["checkpoint_receipt_sha256"] == first_step["checkpoint_receipt_sha256"]


def test_slice10_current_candidate_deterministic_repeat(tmp_path: Path) -> None:
    cid = "px2_m03_slice10_det"
    base = tmp_path / "s10"
    ids = ["a10", "b10"]
    a = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=13,
        continuity_step_count=2,
    )
    shutil.rmtree(base / "out")
    b = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=ids,
        torch_seed=13,
        continuity_step_count=2,
    )
    assert a["current_candidate_sha256"] == b["current_candidate_sha256"]


def test_emit_current_candidate_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_current_candidate import main

    base = tmp_path / "op10"
    base.mkdir()
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--base-dir",
                str(base),
                "--init-only",
                "--transition",
                "promotion",
                "--run-ids",
                "cli_cc_a",
                "cli_cc_b",
                "--campaign-id",
                DEFAULT_SLICE10_CAMPAIGN_ID,
                "--steps",
                "2",
            ]
        )
        == 0
    )
    root = base / "out" / "px2_self_play_campaigns" / DEFAULT_SLICE10_CAMPAIGN_ID
    assert (root / "px2_self_play_current_candidate.json").is_file()


def test_slice11_consumption_consumed_ok_links_current_candidate(tmp_path: Path) -> None:
    cid = "px2_m03_slice11_ci"
    r1, r2 = "s11_a", "s11_b"
    out = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=[r1, r2],
        torch_seed=7,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    cont = run_bounded_continuation_run_consuming_current_candidate(
        corpus_root=CORPUS,
        campaign_root=root,
        campaign_id=cid,
        continuation_run_id="s11_cont",
        init_only=True,
        torch_seed=7,
        continuity_step_count=2,
    )
    assert cont["consumption_status"] == "consumed_ok"
    cr = json.loads((root / CONTINUATION_RUN_JSON).read_text(encoding="utf-8"))
    assert cr["contract_id"] == PX2_SELF_PLAY_CONTINUATION_RUN_CONTRACT_ID
    assert cr["execution_kind"] == EXECUTION_KIND_SLICE11
    assert cr["continuation_rule_id"] == CONTINUATION_RULE_CONSUME_CURRENT_CANDIDATE_STUB
    assert cr["consumption_status"] == "consumed_ok"
    cc = json.loads((root / "px2_self_play_current_candidate.json").read_text(encoding="utf-8"))
    assert cr["current_candidate_sha256"] == cc["current_candidate_sha256"]
    cont_run = json.loads(
        (root / "runs" / "s11_cont" / "px2_self_play_campaign_continuity.json").read_text(
            encoding="utf-8"
        )
    )
    assert cont_run["execution_kind"] == EXECUTION_KIND_SLICE11
    assert cr["continuation_continuity_sha256"] == cont_run["continuity_sha256"]
    man = json.loads(
        (root / "px2_self_play_campaign_root_manifest.json").read_text(encoding="utf-8")
    )
    assert len(man["continuity_run_references"]) == 3


def test_slice11_rejects_campaign_id_mismatch(tmp_path: Path) -> None:
    cid = "px2_m03_slice11_mm"
    out = run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=tmp_path,
        init_only=True,
        run_ids=["mm_a", "mm_b"],
        torch_seed=3,
        continuity_step_count=2,
    )
    root = Path(out["campaign_root"])
    cont = run_bounded_continuation_run_consuming_current_candidate(
        corpus_root=CORPUS,
        campaign_root=root,
        campaign_id="wrong_campaign_id",
        continuation_run_id="mm_cont",
        init_only=True,
    )
    assert cont["consumption_status"] == "rejected_mismatch"
    assert "campaign_id_mismatch" in cont["mismatch_reasons"]
    cr = json.loads((root / CONTINUATION_RUN_JSON).read_text(encoding="utf-8"))
    assert cr["consumption_status"] == "rejected_mismatch"
    assert cr["continuation_continuity_sha256"] is None
    assert "campaign_id_mismatch" in cr["mismatch_reasons"]


def test_slice11_continuation_deterministic_across_roots(tmp_path: Path) -> None:
    cid = "px2_m03_slice11_det"
    ids = ["d_a", "d_b"]

    def _once(base: Path) -> str:
        run_bounded_operator_local_session_transition_with_current_candidate(
            corpus_root=CORPUS,
            transition_kind="promotion",
            campaign_id=cid,
            base_dir=base,
            init_only=True,
            run_ids=ids,
            torch_seed=19,
            continuity_step_count=2,
        )
        root = base / "out" / "px2_self_play_campaigns" / cid
        run_bounded_continuation_run_consuming_current_candidate(
            corpus_root=CORPUS,
            campaign_root=root,
            campaign_id=cid,
            continuation_run_id="det_cont",
            init_only=True,
            torch_seed=19,
            continuity_step_count=2,
        )
        cr = json.loads((root / CONTINUATION_RUN_JSON).read_text(encoding="utf-8"))
        return str(cr["continuation_run_sha256"])

    a = _once(tmp_path / "t1")
    b = _once(tmp_path / "t2")
    assert a == b


def test_emit_continuation_run_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_continuation_run import main

    cid = "px2_m03_slice11_cli"
    base = tmp_path / "prep"
    run_bounded_operator_local_session_transition_with_current_candidate(
        corpus_root=CORPUS,
        transition_kind="promotion",
        campaign_id=cid,
        base_dir=base,
        init_only=True,
        run_ids=["cli_a", "cli_b"],
        torch_seed=2,
        continuity_step_count=2,
    )
    root = base / "out" / "px2_self_play_campaigns" / cid
    assert (
        main(
            [
                "--corpus-root",
                str(CORPUS),
                "--campaign-root",
                str(root),
                "--campaign-id",
                cid,
                "--continuation-run-id",
                "cli_cont",
                "--init-only",
                "--steps",
                "2",
            ]
        )
        == 0
    )
    assert (root / CONTINUATION_RUN_JSON).is_file()


def test_slice5_weighted_rotation_trace(tmp_path: Path) -> None:
    pool = build_slice5_opponent_pool(campaign_tag="w")
    battle = opponent_battle_ref_ids(pool)
    assert DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS == (2, 1, 1, 1)
    run_operator_local_campaign_continuity(
        corpus_root=CORPUS,
        output_dir=tmp_path / "wcont",
        init_only=True,
        campaign_id="weighted_ci",
        campaign_profile_id="weighted_profile",
        torch_seed=3,
        run_id="weighted_run",
        continuity_step_count=3,
        opponent_pool=pool,
        opponent_selection_rule_id=OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB,
        opponent_selection_weights=DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS,
        opponent_rotation_ref_ids=battle,
        execution_kind=EXECUTION_KIND_SLICE5,
    )
    cont = json.loads(
        (tmp_path / "wcont" / "px2_self_play_campaign_continuity.json").read_text(encoding="utf-8")
    )
    expanded: list[str] = []
    for rid, w in zip(battle, DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS, strict=True):
        expanded.extend([rid] * w)
    for i in range(3):
        assert cont["episodes"][i]["opponent_snapshot_ref"] == expanded[i % len(expanded)]


def test_emit_slice5_campaign_root_cli_init_only(tmp_path: Path) -> None:
    from starlab.sc2.px2.self_play.emit_px2_self_play_slice5_campaign_root import main

    root = tmp_path / "s5"
    assert (
        main(
            [
                "--campaign-root",
                str(root),
                "--corpus-root",
                str(CORPUS),
                "--init-only",
                "--steps",
                "2",
                "--run-id",
                "cli_s5",
            ]
        )
        == 0
    )
    assert (root / "px2_self_play_campaign_root_manifest.json").is_file()
    assert (root / "runs" / "cli_s5" / "px2_self_play_campaign_continuity.json").is_file()
