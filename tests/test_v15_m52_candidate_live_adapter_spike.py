"""Tests for V15-M52A candidate live adapter spike."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.artifacts import ExecutionProofRecord, ReplayMetadata
from starlab.sc2.harness import HarnessResult
from starlab.v15.m51_live_candidate_watchability_harness_io import (
    emit_m51_fixture_ci,
    seal_m51_body,
)
from starlab.v15.m51_live_candidate_watchability_harness_models import (
    FILENAME_MAIN_JSON as M51_FILENAME,
)
from starlab.v15.m52_candidate_live_adapter_spike_io import (
    M52aAdapterRunParams,
    emit_m52a_fixture_ci,
    emit_m52a_forbidden_flag_refusal,
    emit_m52a_operator_preflight,
    run_m52a_operator_local_adapter_spike,
    validate_m51_for_m52a,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    CONTRACT_ID_M52A,
    FORBIDDEN_FLAG_12H,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    M52A_HONESTY_FALSE_KEYS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_12H,
    REFUSED_ACTION_MAPPING_MISSING,
    REFUSED_BENCHMARK_CLAIM,
    REFUSED_M51_CONTRACT_INVALID,
    REFUSED_M51_HONESTY,
    REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL,
    REFUSED_M51_SHA_MISMATCH,
    REFUSED_OPERATOR_AUTH,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M52_BLOCKER_REHEARSAL,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_SPIKE_BLOCKED,
    STATUS_SPIKE_COMPLETED,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FILENAME_MAIN_JSON as M52A_FILENAME,
)


def _m52a_honesty_false(blob: dict[str, object]) -> None:
    for k in M52A_HONESTY_FALSE_KEYS:
        assert blob.get(k) is False, k


def _m51_path(tmp_path: Path) -> Path:
    sub = tmp_path / "m51fx"
    emit_m51_fixture_ci(sub)
    return sub / M51_FILENAME


def test_m52a_fixture_ci(tmp_path: Path) -> None:
    sealed, paths = emit_m52a_fixture_ci(tmp_path / "out")
    assert sealed["adapter_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    assert sealed["contract_id"] == CONTRACT_ID_M52A
    assert sealed["watchability_run"]["live_sc2_executed"] is False
    _m52a_honesty_false(sealed)
    assert sealed["adapter"]["torch_load_invoked"] is False
    rr = sealed["route_recommendation"]
    assert isinstance(rr, dict)
    assert rr["route"] == ROUTE_TO_M52_BLOCKER_REHEARSAL
    assert rr["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert len(paths) == 3


def test_m52a_preflight_valid_m51(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    sealed, _ = emit_m52a_operator_preflight(
        tmp_path / "o",
        m51_path=m51p,
        m51_plain_override=None,
        expected_m51_sha256_lower=None,
        emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m39_run_json_path=None,
    )
    assert sealed["adapter_status"] in (
        STATUS_PREFLIGHT_READY,
        STATUS_PREFLIGHT_READY_WARNINGS,
    )


def test_m52a_m51_sha_mismatch(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    sealed, _ = emit_m52a_operator_preflight(
        tmp_path / "o",
        m51_path=m51p,
        m51_plain_override=None,
        expected_m51_sha256_lower="f" * 64,
        emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m39_run_json_path=None,
    )
    assert sealed["adapter_status"] == STATUS_PREFLIGHT_BLOCKED
    assert any(r["code"] == REFUSED_M51_SHA_MISMATCH for r in sealed["refusals"])


def test_m52a_m51_route_not_12hr(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    m51 = json.loads(m51p.read_text(encoding="utf-8"))
    m51.pop("artifact_sha256", None)
    rr = m51.get("route_recommendation")
    assert isinstance(rr, dict)
    rr["route"] = "route_elsewhere"
    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m51_body(m51)), encoding="utf-8")
    sealed, _ = emit_m52a_operator_preflight(
        tmp_path / "o",
        m51_path=bad,
        m51_plain_override=None,
        expected_m51_sha256_lower=None,
        emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m39_run_json_path=None,
    )
    assert any(r["code"] == REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL for r in sealed["refusals"])


def test_m52a_m51_upstream_honesty(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    m51 = json.loads(m51p.read_text(encoding="utf-8"))
    m51.pop("artifact_sha256", None)
    m51["twelve_hour_run_executed"] = True
    bad = tmp_path / "bad.json"
    bad.write_text(canonical_json_dumps(seal_m51_body(m51)), encoding="utf-8")
    sealed, _ = emit_m52a_operator_preflight(
        tmp_path / "o",
        m51_path=bad,
        m51_plain_override=None,
        expected_m51_sha256_lower=None,
        emit_profile_short=PROFILE_OPERATOR_PREFLIGHT,
        require_canonical_seal=True,
        sc2_root=None,
        map_path=None,
        checkpoint_path=None,
        expected_candidate_sha256=None,
        m39_run_json_path=None,
    )
    assert any(r["code"] == REFUSED_M51_HONESTY for r in sealed["refusals"])


def test_m52a_forbidden_run_benchmark(tmp_path: Path) -> None:
    sealed, _ = emit_m52a_forbidden_flag_refusal(
        tmp_path / "o",
        emit_profile_short=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_RUN_BENCHMARK],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_CLAIM for r in sealed["refusals"])


def test_m52a_forbidden_12h(tmp_path: Path) -> None:
    sealed, _ = emit_m52a_forbidden_flag_refusal(
        tmp_path / "o",
        emit_profile_short=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_12H],
    )
    assert any(r["code"] == REFUSED_12H for r in sealed["refusals"])


def test_m52a_runner_missing_guards(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    exp = hashlib.sha256(ck.read_bytes()).hexdigest()
    params = M52aAdapterRunParams(
        m51_path=m51p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=exp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        device="cpu",
        seed=0,
        expected_m51_sha256=None,
        operator_note_path=None,
        m39_run_json_path=None,
    )
    sealed, _ = run_m52a_operator_local_adapter_spike(
        params, allow_local=False, authorize_spike=False
    )
    assert sealed["adapter_status"] == STATUS_SPIKE_BLOCKED
    assert any(r["code"] == REFUSED_OPERATOR_AUTH for r in sealed["refusals"])


def test_m52a_spike_success_patched(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    exp = hashlib.sha256(ck.read_bytes()).hexdigest()
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
    params = M52aAdapterRunParams(
        m51_path=m51p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=exp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        device="cpu",
        seed=0,
        expected_m51_sha256=None,
        operator_note_path=None,
        m39_run_json_path=None,
    )

    def _pick(_i: int, _gl: int, _m: int, _v: int) -> int:
        return 0

    with (
        patch(
            "starlab.v15.m52_candidate_live_adapter_spike_projection.load_checkpoint_state_dict",
            return_value={},
        ),
        patch(
            "starlab.v15.m52_candidate_live_adapter_spike_projection.make_pick_action_index_from_state",
            return_value=_pick,
        ),
        patch(
            "starlab.v15.m52_candidate_live_adapter_spike_io.run_match_execution",
            return_value=HarnessResult(ok=True, proof=proof, message=None),
        ),
    ):
        sealed, _ = run_m52a_operator_local_adapter_spike(
            params, allow_local=True, authorize_spike=True
        )
    assert sealed["adapter_status"] == STATUS_SPIKE_COMPLETED
    assert sealed["watchability_run"]["live_sc2_executed"] is True
    assert sealed["torch_load_invoked"] is True
    assert sealed["twelve_hour_run_executed"] is False


def test_m52a_action_mapping_refused_patched(tmp_path: Path) -> None:
    m51p = _m51_path(tmp_path)
    sc2 = tmp_path / "sc2"
    sc2.mkdir()
    mp = tmp_path / "m.SC2Map"
    mp.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"y")
    exp = hashlib.sha256(ck.read_bytes()).hexdigest()
    params = M52aAdapterRunParams(
        m51_path=m51p,
        output_dir=tmp_path / "out",
        sc2_root=sc2,
        map_path=mp,
        candidate_checkpoint_path=ck,
        expected_candidate_sha256=exp,
        game_step=8,
        max_game_steps=32,
        save_replay=False,
        device="cpu",
        seed=0,
        expected_m51_sha256=None,
        operator_note_path=None,
        m39_run_json_path=None,
    )
    with (
        patch(
            "starlab.v15.m52_candidate_live_adapter_spike_projection.load_checkpoint_state_dict",
            return_value={},
        ),
        patch(
            "starlab.v15.m52_candidate_live_adapter_spike_projection.make_pick_action_index_from_state",
            side_effect=ValueError("no_action_mapping"),
        ),
    ):
        sealed, _ = run_m52a_operator_local_adapter_spike(
            params, allow_local=True, authorize_spike=True
        )
    assert sealed["adapter_status"] == STATUS_SPIKE_BLOCKED
    assert any(r["code"] == REFUSED_ACTION_MAPPING_MISSING for r in sealed["refusals"])
    assert sealed["watchability_run"]["live_sc2_executed"] is False


def test_m52a_validate_missing_m51() -> None:
    codes, _ = validate_m51_for_m52a(
        None,
        expected_sha256_lower=None,
        require_canonical_seal=True,
    )
    assert REFUSED_M51_CONTRACT_INVALID in codes


def test_m52a_cli_fixture(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m52_candidate_live_adapter_spike",
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
    assert (out / M52A_FILENAME).is_file()


def test_m52a_no_torch_in_emit_modules() -> None:
    import starlab.v15.emit_v15_m52_candidate_live_adapter_spike as em
    import starlab.v15.m52_candidate_live_adapter_spike_io as io

    for mod in (io, em):
        p = Path(mod.__file__ or "")
        assert p.read_text(encoding="utf-8").count("torch.load") == 0
