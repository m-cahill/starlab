"""Tests for V15-M58 bounded candidate adapter evaluation execution."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
import starlab.v15.run_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt as run_mod
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m58_bounded_candidate_adapter_evaluation_execution import (
    main as emit_m58_main,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    CONTRACT_ID_M52A,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FILENAME_MAIN_JSON as M52A_MAIN,
)
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    STATUS_SPIKE_COMPLETED as M52A_COMPLETED,
)
from starlab.v15.m57_governed_evaluation_execution_charter_io import (
    build_fixture_charter,
)
from starlab.v15.m57_governed_evaluation_execution_charter_io import (
    write_charter_artifacts as write_m57_charter,
)
from starlab.v15.m57_governed_evaluation_execution_charter_models import (
    FILENAME_MAIN_JSON as M57_FN,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_io import (
    OperatorDeclaredExecutionInputs,
    OperatorPreflightExecutionInputs,
    build_m52a_delegate_argv,
    build_operator_declared_execution,
    build_operator_preflight_execution,
    load_m57_charter,
    normalize_opponent_mode,
    parse_m52a_delegate_receipts,
    validate_execution_claim_flags,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
    BLOCKED_CLAIM_FLAGS_VIOLATION,
    BLOCKED_DUAL_GUARD_MISSING,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CONTRACT_ID,
    PROFILE_FIXTURE_CI,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
)
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
    FILENAME_MAIN_JSON as M58_MAIN,
)
from starlab.v15.run_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt import (
    main as run_m58_main,
)


def _m57_fixture_path(dir_path: Path) -> Path:
    emit_dir = dir_path / "m57_emit"
    write_m57_charter(emit_dir, body_unsealed=build_fixture_charter())
    return emit_dir / M57_FN


def test_emit_fixture(tmp_path: Path) -> None:
    out = tmp_path / "outfx"
    assert emit_m58_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)]) == 0
    main_blob = json.loads((out / M58_MAIN).read_text(encoding="utf-8"))
    assert main_blob["contract_id"] == CONTRACT_ID
    assert main_blob["execution_result"]["execution_status"] == STATUS_FIXTURE_SCHEMA_ONLY
    assert all(v is False for v in cast(dict[str, bool], main_blob["claim_flags"]).values())


def test_fixture_seal_roundtrip(tmp_path: Path) -> None:
    out = tmp_path / "s"
    emit_m58_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)])
    sealed = json.loads((out / M58_MAIN).read_text(encoding="utf-8"))
    digest = str(sealed.pop("artifact_sha256"))
    assert digest == sha256_hex_of_canonical_json(sealed)


def test_preflight_ready(tmp_path: Path) -> None:
    charter_p = _m57_fixture_path(tmp_path)
    (tmp_path / "sc2").mkdir()
    pmap = tmp_path / "Waterfall.SC2Map"
    pmap.write_bytes(b"map")

    body = build_operator_preflight_execution(
        OperatorPreflightExecutionInputs(
            m57_charter_json=charter_p,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            candidate_checkpoint=None,
            sc2_root=tmp_path / "sc2",
            map_path=pmap,
            opponent_mode=None,
            game_step=None,
            max_game_steps=None,
        ),
    )
    assert body["execution_result"]["execution_status"] == STATUS_PREFLIGHT_READY


def test_preflight_blocked_horizon(tmp_path: Path) -> None:
    charter_p = _m57_fixture_path(tmp_path)
    (tmp_path / "sc2").mkdir()
    pmap = tmp_path / "Waterfall.SC2Map"
    pmap.write_bytes(b".")

    body = build_operator_preflight_execution(
        OperatorPreflightExecutionInputs(
            m57_charter_json=charter_p,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            candidate_checkpoint=None,
            sc2_root=tmp_path / "sc2",
            map_path=pmap,
            opponent_mode="passive_or_scripted_baseline",
            game_step=9,
            max_game_steps=2048,
        ),
    )
    assert body["execution_result"]["execution_status"] == STATUS_PREFLIGHT_BLOCKED


def test_preflight_missing_charter(tmp_path: Path) -> None:
    body = build_operator_preflight_execution(
        OperatorPreflightExecutionInputs(
            m57_charter_json=tmp_path / "nope.json",
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            candidate_checkpoint=None,
            sc2_root=tmp_path / "sc",
            map_path=tmp_path / "m",
            opponent_mode=None,
            game_step=None,
            max_game_steps=None,
        ),
    )
    assert body["execution_result"]["execution_status"] == STATUS_PREFLIGHT_BLOCKED


def test_m57_bad_route_blocked(tmp_path: Path) -> None:
    emit_dir = tmp_path / "m57e"
    tpl = dict(build_fixture_charter())
    rr = dict(cast(dict[str, Any], tpl["route_recommendation"]))
    rr["route"] = "route_elsewhere_bad"
    tpl["route_recommendation"] = rr
    write_m57_charter(emit_dir, body_unsealed=tpl)
    _, errs = load_m57_charter(emit_dir / M57_FN)
    assert errs


def test_opponent_modes() -> None:
    assert normalize_opponent_mode(None) == "burnysc2_passive_bot"
    assert normalize_opponent_mode("passive_or_scripted_baseline") == "burnysc2_passive_bot"
    assert normalize_opponent_mode("burnysc2_passive_bot") == "burnysc2_passive_bot"
    assert normalize_opponent_mode("human_ladder") is None


def test_parse_delegate_ok(tmp_path: Path) -> None:
    dlg = tmp_path / "dlg"
    dlg.mkdir()
    replay = dlg / "candidate_live_adapter_watch" / "replay" / "validation.SC2Replay"
    replay.parent.mkdir(parents=True, exist_ok=True)
    replay.write_bytes(b"x")
    (dlg / M52A_MAIN).write_text(
        canonical_json_dumps(
            {
                "contract_id": CONTRACT_ID_M52A,
                "adapter_status": M52A_COMPLETED,
                "watchability_run": {
                    "replay_saved": True,
                    "live_sc2_executed": True,
                    "action_count": 2,
                    "observation_count": 4,
                    "final_status": "ok",
                },
            },
        ),
        encoding="utf-8",
    )
    recv = parse_m52a_delegate_receipts(dlg, require_replay=True)
    assert recv["ok"] is True


def test_delegate_argv_shape() -> None:
    argv = build_m52a_delegate_argv(
        python_executable=sys.executable,
        m51_json=Path("m.json"),
        delegate_output_dir=Path("out"),
        ck_path=Path("ck.pt"),
        expected_ck_sha=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        sc2_root=Path("sc2"),
        map_path=Path("Waterfall.SC2Map"),
        device="cpu",
        game_step=8,
        max_game_steps=2048,
        save_replay=True,
        seed=0,
        expected_m51_sha256=None,
    )
    assert "starlab.v15.run_v15_m52_candidate_live_adapter_spike" in argv


def test_runner_no_dual_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(run_mod, "validate_candidate_checkpoint_sha", MagicMock(return_value=[]))

    charter_p = _m57_fixture_path(tmp_path)
    (tmp_path / "sc2").mkdir()
    pmap = tmp_path / "Waterfall.SC2Map"
    pmap.write_bytes(b"x")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"data")

    outd = tmp_path / "o_no_guard"
    rc = run_m58_main(
        [
            "--m57-charter-json",
            str(charter_p),
            "--m51-watchability-json",
            str(pmap),
            "--candidate-checkpoint",
            str(ck),
            "--sc2-root",
            str(tmp_path / "sc2"),
            "--map-path",
            str(pmap),
            "--save-replay",
            "--output-dir",
            str(outd),
        ],
    )
    assert rc == 3
    body = json.loads((outd / M58_MAIN).read_text(encoding="utf-8"))
    blocked = cast(list[Any], body["execution_result"]["blocked_reasons"])
    assert BLOCKED_DUAL_GUARD_MISSING in blocked


def test_runner_success_mock(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(run_mod, "validate_candidate_checkpoint_sha", MagicMock(return_value=[]))
    monkeypatch.setattr(
        subprocess,
        "run",
        MagicMock(return_value=MagicMock(stdout="", stderr="", returncode=0)),
    )
    monkeypatch.setattr(
        run_mod,
        "parse_m52a_delegate_receipts",
        MagicMock(
            return_value={
                "ok": True,
                "blocked_reasons": [],
                "adapter_status": M52A_COMPLETED,
                "live_sc2_executed": True,
                "replay_saved": True,
                "replay_sha256": "a" * 64,
                "action_count": 5,
                "observation_count": 6,
                "game_steps_observed": 6,
                "sc2_result_metadata": "ok",
            },
        ),
    )

    charter_p = _m57_fixture_path(tmp_path)
    (tmp_path / "sc2").mkdir()
    pmap = tmp_path / "Waterfall.SC2Map"
    pmap.write_bytes(b"y")
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"checkpoint-bytes-placeholder")

    outd = tmp_path / "o_ok"
    rc = run_m58_main(
        [
            "--allow-operator-local-execution",
            "--authorize-bounded-candidate-adapter-evaluation",
            "--m57-charter-json",
            str(charter_p),
            "--m51-watchability-json",
            str(pmap),
            "--candidate-checkpoint",
            str(ck),
            "--sc2-root",
            str(tmp_path / "sc2"),
            "--map-path",
            str(pmap),
            "--save-replay",
            "--output-dir",
            str(outd),
        ],
    )
    assert rc == 0
    body = json.loads((outd / M58_MAIN).read_text(encoding="utf-8"))
    cf = cast(dict[str, Any], body["claim_flags"])
    assert cf["bounded_adapter_execution_performed"] is True
    assert cf["benchmark_passed"] is False

    charter_p = _m57_fixture_path(tmp_path)
    dec = tmp_path / "decl.json"
    dec.write_text(
        canonical_json_dumps({"claim_flags": {"benchmark_passed": True}}),
        encoding="utf-8",
    )
    merged = build_operator_declared_execution(
        OperatorDeclaredExecutionInputs(
            declared_execution_json=dec,
            m57_charter_json=charter_p,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    blob = canonical_json_dumps(merged)
    assert BLOCKED_CLAIM_FLAGS_VIOLATION in blob


def test_deep_claim_walk() -> None:
    blob = {"a": [{"claim_flags": {"strength_evaluated": True}}]}
    assert validate_execution_claim_flags(blob) is True
