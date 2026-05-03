"""Tests for V15-M57 governed evaluation execution charter / dry-run gate."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m57_governed_evaluation_execution_charter import (
    main as emit_m57_main,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_io import (
    write_readout_artifacts as write_m56_artifacts,
)
from starlab.v15.m57_governed_evaluation_execution_charter_io import (
    OperatorDeclaredCharterInputs,
    OperatorPreflightCharterInputs,
    _validate_m57a_watch_session,
    build_fixture_charter,
    build_operator_declared_charter,
    build_operator_preflight_charter,
    charter_is_blocked,
    write_charter_artifacts,
)
from starlab.v15.m57_governed_evaluation_execution_charter_models import (
    BLOCKED_M57A_OP1_ANCHOR,
    BLOCKED_M57A_SCAFFOLD_ONLY,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CHARTER_BLOCKED,
    CHARTER_READY,
    CLASSIFICATION_SCAFFOLD_WATCH,
    CONTRACT_ID,
    DRY_RUN_COMMAND_FILENAME,
    DRY_RUN_READY,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    PROFILE_FIXTURE_CI,
    REPORT_FILENAME,
    ROUTE_M58,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests/fixtures/v15_m57"
OP1_M57A = FIXTURE_DIR / "op1_m57a_watch_session.json"
OP1_M52A = FIXTURE_DIR / "op1_m52a_adapter.json"
OP1_PROOF = FIXTURE_DIR / "op1_match_proof_minimal.json"
DECLARED_MIN = FIXTURE_DIR / "declared_charter_minimal.json"


def test_fixture_seal_and_four_artifacts(tmp_path: Path) -> None:
    sealed, paths = write_charter_artifacts(tmp_path / "o", body_unsealed=build_fixture_charter())
    assert (tmp_path / "o" / FILENAME_MAIN_JSON).is_file()
    assert (tmp_path / "o" / REPORT_FILENAME).is_file()
    assert (tmp_path / "o" / DRY_RUN_COMMAND_FILENAME).is_file()
    digest = sealed["artifact_sha256"]
    base = {k: v for k, v in sealed.items() if k != "artifact_sha256"}
    assert digest == sha256_hex_of_canonical_json(base)
    assert sealed["contract_id"] == CONTRACT_ID
    ec = sealed["evaluation_charter"]
    assert ec["charter_status"] == CHARTER_READY
    dg = sealed["dry_run_gate"]
    assert dg["gate_status"] == DRY_RUN_READY
    assert dg["dry_run_command_status"] == "planned_not_executed"
    assert dg["m58_runner_exists_in_m57"] is False
    rr = sealed["route_recommendation"]
    assert rr["route"] == ROUTE_M58
    assert rr["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    for _k, v in sealed["claim_flags"].items():
        assert v is False
    txt = (tmp_path / "o" / DRY_RUN_COMMAND_FILENAME).read_text(encoding="utf-8")
    assert "PLANNED_NOT_EXECUTED" in txt
    assert "run_v15_m58" in txt


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_preflight_op1_fixtures_ready(tmp_path: Path) -> None:
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=OP1_M57A,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m56_readout_json=None,
            match_execution_proof_json=OP1_PROOF if OP1_PROOF.is_file() else None,
        ),
    )
    assert not charter_is_blocked(body)
    assert "m56_readout_context_not_supplied_non_blocking" in (body.get("_notices") or [])


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_preflight_with_m56_fixture(tmp_path: Path) -> None:
    m56dir = tmp_path / "m56"
    _, (m56_main, _, _) = write_m56_artifacts(
        m56dir,
        body_unsealed=__import__(
            "starlab.v15.m56_bounded_evaluation_package_readout_decision_io",
            fromlist=["build_fixture_readout_decision"],
        ).build_fixture_readout_decision(),
    )
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=OP1_M57A,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m56_readout_json=m56_main,
        ),
    )
    assert not charter_is_blocked(body)


def test_preflight_missing_m57a(tmp_path: Path) -> None:
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=tmp_path / "missing.json",
            m52a_adapter_json=tmp_path / "missing2.json",
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_preflight_bad_m57a_seal(tmp_path: Path) -> None:
    bad = tmp_path / "bad_m57a.json"
    obj = json.loads(OP1_M57A.read_text(encoding="utf-8"))
    obj["artifact_sha256"] = "0" * 64
    bad.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=bad,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
def test_validate_m57a_scaffold_classification_is_blocked() -> None:
    raw = json.loads(OP1_M57A.read_text(encoding="utf-8"))
    vc = raw.get("visual_classification")
    if isinstance(vc, dict):
        vc["classification"] = CLASSIFICATION_SCAFFOLD_WATCH
    raw["visual_classification"] = vc
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    raw["artifact_sha256"] = sha256_hex_of_canonical_json(wo)
    errs = _validate_m57a_watch_session(raw)
    assert BLOCKED_M57A_SCAFFOLD_ONLY in errs
    assert BLOCKED_M57A_OP1_ANCHOR in errs


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_preflight_resealed_m57a_loses_op1_anchor(tmp_path: Path) -> None:
    """Any material change to M57A requires a new seal; digest won't match canonical OP1."""
    bad = tmp_path / "scaffold_m57a.json"
    raw = json.loads(OP1_M57A.read_text(encoding="utf-8"))
    vc = raw.get("visual_classification")
    if isinstance(vc, dict):
        vc["classification"] = "scaffold_visual_watch_completed_not_candidate_policy"
    raw["visual_classification"] = vc
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    raw["artifact_sha256"] = sha256_hex_of_canonical_json(wo)
    bad.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=bad,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_preflight_wrong_op1_digest(tmp_path: Path) -> None:
    bad = tmp_path / "wrong_digest_m57a.json"
    shutil.copy(OP1_M57A, bad)
    raw = json.loads(bad.read_text(encoding="utf-8"))
    raw["milestone"] = "V15-M57A-tampered"
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    raw["artifact_sha256"] = sha256_hex_of_canonical_json(wo)
    bad.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=bad,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
def test_match_proof_action_mismatch(tmp_path: Path) -> None:
    bad_proof = tmp_path / "bad_proof.json"
    bad_proof.write_text(
        json.dumps(
            {
                "action_count": 999,
                "artifact_hash": "78ea8b4c0fef4377c4af06082e573e3779a671e71611d6dcab161aba877cfed7",
                "final_status": "ok",
                "map_logical_key": "Maps/Waterfall.SC2Map",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=OP1_M57A,
            m52a_adapter_json=OP1_M52A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            match_execution_proof_json=bad_proof,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not OP1_M52A.is_file(), reason="OP1 M52A fixture missing")
@pytest.mark.skipif(not DECLARED_MIN.is_file(), reason="Declared fixture missing")
def test_operator_declared_ok(tmp_path: Path) -> None:
    body = build_operator_declared_charter(
        OperatorDeclaredCharterInputs(
            declared_charter_json=DECLARED_MIN,
            m57a_watch_session_json=OP1_M57A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert not charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not DECLARED_MIN.is_file(), reason="Declared fixture missing")
def test_operator_declared_wrong_m52a_binding(tmp_path: Path) -> None:
    bad_decl = tmp_path / "decl.json"
    d: dict[str, Any] = json.loads(DECLARED_MIN.read_text(encoding="utf-8"))
    ib = d.get("input_bindings")
    if isinstance(ib, dict):
        ib["m52a_adapter_artifact_sha256"] = "0" * 64
    bad_decl.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
    body = build_operator_declared_charter(
        OperatorDeclaredCharterInputs(
            declared_charter_json=bad_decl,
            m57a_watch_session_json=OP1_M57A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


@pytest.mark.skipif(not OP1_M57A.is_file(), reason="OP1 M57A fixture missing")
@pytest.mark.skipif(not DECLARED_MIN.is_file(), reason="Declared fixture missing")
def test_operator_declared_overclaim(tmp_path: Path) -> None:
    bad_decl = tmp_path / "decl2.json"
    d: dict[str, Any] = {"evaluation_charter": {"execution_performed_in_m57": True}}
    bad_decl.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
    body = build_operator_declared_charter(
        OperatorDeclaredCharterInputs(
            declared_charter_json=bad_decl,
            m57a_watch_session_json=OP1_M57A,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert charter_is_blocked(body)


def test_emit_cli_fixture(tmp_path: Path) -> None:
    assert (
        emit_m57_main(
            ["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(tmp_path / "e")],
        )
        == 0
    )
    main_j = json.loads((tmp_path / "e" / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert main_j["evaluation_charter"]["charter_status"] == CHARTER_READY


def test_emit_cli_forbidden_flag(tmp_path: Path) -> None:
    assert (
        emit_m57_main(
            [
                "--profile",
                PROFILE_FIXTURE_CI,
                "--output-dir",
                str(tmp_path / "f"),
                FORBIDDEN_FLAG_CLAIM_BENCHMARK,
            ],
        )
        == 0
    )
    main_j = json.loads((tmp_path / "f" / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert main_j["evaluation_charter"]["charter_status"] == CHARTER_BLOCKED


def test_blocked_charter_skips_m58_command_file(tmp_path: Path) -> None:
    body = build_operator_preflight_charter(
        OperatorPreflightCharterInputs(
            m57a_watch_session_json=tmp_path / "nope.json",
            m52a_adapter_json=tmp_path / "nope2.json",
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    _, _ = write_charter_artifacts(tmp_path / "b", body_unsealed=body)
    assert not (tmp_path / "b" / DRY_RUN_COMMAND_FILENAME).is_file()
