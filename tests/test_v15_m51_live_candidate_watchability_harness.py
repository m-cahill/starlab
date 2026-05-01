"""Tests for V15-M51 live candidate watchability harness."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.artifacts import ExecutionProofRecord, ReplayMetadata
from starlab.sc2.harness import HarnessResult
from starlab.v15.m50_scorecard_result_readout_decision_io import emit_m50_fixture_ci
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    FILENAME_MAIN_JSON as M50_FILENAME,
)
from starlab.v15.m50_scorecard_result_readout_decision_models import ROUTE_TO_M51_WATCHABILITY
from starlab.v15.m51_live_candidate_watchability_harness_io import (
    M51LiveRunParams,
    emit_m51_fixture_ci,
    emit_m51_forbidden_flag_refusal,
    emit_m51_operator_declared,
    emit_m51_operator_preflight,
    run_m51_operator_local_watchability,
    validate_m50_for_m51,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    CANDIDATE_POLICY_SCAFFOLD,
    CANDIDATE_POLICY_UNAVAILABLE,
    CONTRACT_ID_M51,
    PROFILE_ID_OPERATOR_DECLARED,
    REFUSED_ADAPTER_MISSING,
    REFUSED_BENCHMARK_CLAIM,
    REFUSED_M50_CONTRACT_INVALID,
    REFUSED_M50_HONESTY,
    REFUSED_M50_ROUTE_EXECUTED,
    REFUSED_M50_ROUTE_NOT_WATCHABILITY,
    REFUSED_M50_SHA_MISMATCH,
    REFUSED_MISSING_M50,
    REFUSED_OPERATOR_AUTH,
    REFUSED_SC2_ROOT,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M52,
    STATUS_BLOCKED_MISSING_ADAPTER,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_LIVE_BLOCKED,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_SCAFFOLD_COMPLETED,
)


def _m51_honesty_false(blob: dict[str, object]) -> None:
    for k in (
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_results_produced",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "xai_executed",
        "human_panel_executed",
        "showcase_released",
        "v2_authorized",
        "t2_t3_t4_t5_executed",
        "twelve_hour_run_executed",
    ):
        assert blob.get(k) is False, k


def _m50_path(tmp_path: Path) -> Path:
    sub = tmp_path / "m50fx"
    emit_m50_fixture_ci(sub)
    return sub / M50_FILENAME


def test_m51_fixture_ci(tmp_path: Path) -> None:
    sealed, paths = emit_m51_fixture_ci(tmp_path / "out")
    assert sealed["watchability_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    assert sealed["contract_id"] == CONTRACT_ID_M51
    assert sealed["watchability_run"]["live_sc2_executed"] is False
    _m51_honesty_false(sealed)
    assert sealed["route_recommendation"]["route"] == ROUTE_TO_M52
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert len(paths) == 3


def test_m51_preflight_valid_m50(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=m50p,
        expected_sha256_lower=None,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert sealed["watchability_status"] in (
        "watchability_preflight_ready",
        "watchability_preflight_ready_with_warnings",
    )


def test_m51_sha_mismatch(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=m50p,
        expected_sha256_lower="f" * 64,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert sealed["watchability_status"] == STATUS_PREFLIGHT_BLOCKED
    assert any(r["code"] == REFUSED_M50_SHA_MISMATCH for r in sealed["refusals"])


def test_m51_invalid_m50_contract(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    m50 = json.loads(m50p.read_text(encoding="utf-8"))
    m50.pop("artifact_sha256", None)
    m50["contract_id"] = "wrong"
    from starlab.v15.m50_scorecard_result_readout_decision_io import seal_m50_body

    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m50_body(m50)), encoding="utf-8")
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=bad,
        expected_sha256_lower=None,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert any(r["code"] == REFUSED_M50_CONTRACT_INVALID for r in sealed["refusals"])


def test_m51_route_not_watchability(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    m50 = json.loads(m50p.read_text(encoding="utf-8"))
    m50.pop("artifact_sha256", None)
    cast_rr = m50.get("route_recommendation")
    assert isinstance(cast_rr, dict)
    cast_rr["next_route"] = "route_elsewhere"
    from starlab.v15.m50_scorecard_result_readout_decision_io import seal_m50_body

    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m50_body(m50)), encoding="utf-8")
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=bad,
        expected_sha256_lower=None,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert any(r["code"] == REFUSED_M50_ROUTE_NOT_WATCHABILITY for r in sealed["refusals"])


def test_m51_route_executed_refused(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    m50 = json.loads(m50p.read_text(encoding="utf-8"))
    m50.pop("artifact_sha256", None)
    rr = m50.get("route_recommendation")
    assert isinstance(rr, dict)
    rr["route_status"] = "already_executed"
    from starlab.v15.m50_scorecard_result_readout_decision_io import seal_m50_body

    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m50_body(m50)), encoding="utf-8")
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=bad,
        expected_sha256_lower=None,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert any(r["code"] == REFUSED_M50_ROUTE_EXECUTED for r in sealed["refusals"])


def test_m51_upstream_honesty(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    m50 = json.loads(m50p.read_text(encoding="utf-8"))
    m50.pop("artifact_sha256", None)
    m50["benchmark_passed"] = True
    from starlab.v15.m50_scorecard_result_readout_decision_io import seal_m50_body

    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m50_body(m50)), encoding="utf-8")
    sealed, _ = emit_m51_operator_preflight(
        tmp_path / "o",
        m50_path=bad,
        expected_sha256_lower=None,
        emit_profile_short="operator_preflight",
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert any(r["code"] == REFUSED_M50_HONESTY for r in sealed["refusals"])


def test_m51_forbidden_flags(tmp_path: Path) -> None:
    sealed, _ = emit_m51_forbidden_flag_refusal(
        tmp_path / "o",
        emit_profile_short="fixture_ci",
        triggered_flags=["--claim-benchmark-pass"],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_CLAIM for r in sealed["refusals"])


def test_m51_scaffold_blocked_without_flag(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    params = M51LiveRunParams(
        m50_path=m50p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        allow_scaffold=False,
        seed=0,
        video_path=None,
        operator_note_path=None,
        run_id=None,
        expected_m50_sha256=None,
        checkpoint_path=ck,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    sealed, _ = run_m51_operator_local_watchability(
        params, allow_local=True, authorize_watchability=True
    )
    assert sealed["watchability_status"] == STATUS_BLOCKED_MISSING_ADAPTER
    assert sealed["candidate_policy"]["candidate_policy_mode"] == CANDIDATE_POLICY_UNAVAILABLE
    assert any(r["code"] == REFUSED_ADAPTER_MISSING for r in sealed["refusals"])


def test_m51_runner_missing_guards(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    params = M51LiveRunParams(
        m50_path=m50p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        allow_scaffold=True,
        seed=0,
        video_path=None,
        operator_note_path=None,
        run_id=None,
        expected_m50_sha256=None,
        checkpoint_path=ck,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    sealed, _ = run_m51_operator_local_watchability(
        params, allow_local=False, authorize_watchability=False
    )
    assert sealed["watchability_status"] == STATUS_LIVE_BLOCKED
    assert any(r["code"] == REFUSED_OPERATOR_AUTH for r in sealed["refusals"])


def test_m51_runner_missing_sc2_root(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    missing = tmp_path / "nope"
    params = M51LiveRunParams(
        m50_path=m50p,
        output_dir=tmp_path / "out",
        sc2_root=missing,
        map_path=mp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        allow_scaffold=True,
        seed=0,
        video_path=None,
        operator_note_path=None,
        run_id=None,
        expected_m50_sha256=None,
        checkpoint_path=ck,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    sealed, _ = run_m51_operator_local_watchability(
        params, allow_local=True, authorize_watchability=True
    )
    assert any(r["code"] == REFUSED_SC2_ROOT for r in sealed["refusals"])


def test_m51_scaffold_success_patched(tmp_path: Path) -> None:
    m50p = _m50_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    proof = ExecutionProofRecord(
        schema_version="match_execution_proof.v1",
        adapter_name="burnysc2",
        runtime_boundary_name="test",
        base_build="b",
        data_version="d",
        map_logical_key="k",
        map_resolution="explicit_path",
        seed=0,
        interface={"raw_interface": True, "score_interface": True},
        step_policy={"game_step": 8, "max_game_steps": 32},
        status_sequence=("configure", "launch", "in_game", "bounded_exit", "result:Defeat"),
        observation_summaries=({"game_loop": 8, "minerals": 50, "vespene": 0},),
        action_count=2,
        final_status="ok",
        replay=ReplayMetadata(replay_saved=False),
        sc2_game_result="Defeat",
    )
    params = M51LiveRunParams(
        m50_path=m50p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        allow_scaffold=True,
        seed=0,
        video_path=None,
        operator_note_path=None,
        run_id=None,
        expected_m50_sha256=None,
        checkpoint_path=ck,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    with patch(
        "starlab.v15.m51_live_candidate_watchability_harness_io.run_match_execution",
        return_value=HarnessResult(ok=True, proof=proof, message=None),
    ):
        sealed, _ = run_m51_operator_local_watchability(
            params, allow_local=True, authorize_watchability=True
        )
    assert sealed["watchability_status"] == STATUS_SCAFFOLD_COMPLETED
    assert sealed["candidate_policy"]["candidate_policy_mode"] == CANDIDATE_POLICY_SCAFFOLD
    assert sealed["live_sc2_executed"] is True
    assert sealed["checkpoint_promoted"] is False
    _m51_honesty_false(sealed)


def test_m51_declared_overclaim(tmp_path: Path) -> None:
    d = {
        "contract_id": CONTRACT_ID_M51,
        "profile_id": PROFILE_ID_OPERATOR_DECLARED,
        "benchmark_passed": True,
    }
    p = tmp_path / "d.json"
    p.write_text(canonical_json_dumps(d), encoding="utf-8")
    sealed, _ = emit_m51_operator_declared(
        tmp_path / "o",
        declared_path=p,
        embedded_m50_path=None,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m42_path=None,
    )
    assert sealed["watchability_status"] == STATUS_PREFLIGHT_BLOCKED


def test_m51_preflight_fixture_never_live(tmp_path: Path) -> None:
    codes, _ = validate_m50_for_m51(None, expected_sha256_lower=None, require_canonical_seal=True)
    assert REFUSED_MISSING_M50 in codes


def test_m51_cli_fixture(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m51_live_candidate_watchability_harness",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert (out / "v15_live_candidate_watchability_harness.json").is_file()


def test_m51_no_torch_in_emit_io() -> None:
    import starlab.v15.emit_v15_m51_live_candidate_watchability_harness as em
    import starlab.v15.m51_live_candidate_watchability_harness_io as io

    for mod in (io, em):
        p = Path(mod.__file__ or "")
        assert p.read_text(encoding="utf-8").count("torch.load") == 0


def test_fixture_route_needle(tmp_path: Path) -> None:
    sealed, _ = emit_m51_fixture_ci(tmp_path / "fx")
    m50_plain = json.loads(
        (tmp_path / "fx" / "m50_upstream_fixture" / M50_FILENAME).read_text(encoding="utf-8")
    )
    assert m50_plain["route_recommendation"]["next_route"] == ROUTE_TO_M51_WATCHABILITY
