"""V15-M32 bounded candidate checkpoint evaluation execution tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution import main as emit_m32_main
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import seal_m31_gate_body
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    CONTRACT_ID_M31_GATE,
    PROFILE_M31_DRY_RUN,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_io import (
    build_fixture_m31_sealed_gate,
    emit_v15_m32_candidate_checkpoint_evaluation_execution,
    load_m31_harness_gate_json,
    validate_m31_for_m32,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_models import (
    CONTRACT_ID_M32_EVAL_EXEC,
    FILENAME_EXEC_JSON,
    PROFILE_M32_BOUNDED,
    STATUS_FIXTURE_COMPLETED,
    STATUS_OPERATOR_LOCAL_METADATA_COMPLETED,
    STATUS_REFUSED_BLOCKERS,
)

FIXTURE_M31_GATE_DIGEST = "04c7cbde96d6a581ad0c97ca4083fb1179fc83f2f6b24955ac780d2c10a1ae2e"


def _reseal_m31(body_wo_digest: dict[str, object]) -> dict[str, object]:
    """Reseal mutated M31 gate bodies for deterministic negative-path tests."""
    return seal_m31_gate_body(body_wo_digest)


def test_m32_fixture_ci_success(tmp_path: Path) -> None:
    m31 = build_fixture_m31_sealed_gate()
    assert m31["artifact_sha256"] == FIXTURE_M31_GATE_DIGEST
    sealed, jp, _, _ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "m32_out",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    txt = jp.read_text(encoding="utf-8").lower()
    assert "c:\\coding" not in txt
    assert "/home/" not in txt
    assert sealed["contract_id"] == CONTRACT_ID_M32_EVAL_EXEC
    assert sealed["profile"] == PROFILE_M32_BOUNDED
    assert sealed["execution_status"] == STATUS_FIXTURE_COMPLETED
    assert sealed["evaluation_execution_performed"] is True
    assert sealed["scorecard_execution_performed"] is False
    assert sealed["benchmark_passed"] is False
    assert sealed["checkpoint_blob_io_performed"] is False
    assert sealed["candidate_model_loaded"] is False
    assert sealed["fixture_ci"] is True
    assert sealed["bounded_execution_result"]["strength_score_present"] is False


def test_m32_operator_local_m31_file_success(tmp_path: Path) -> None:
    m31 = build_fixture_m31_sealed_gate()
    gp = tmp_path / "gate.json"
    gp.write_text(canonical_json_dumps(m31), encoding="utf-8")
    loaded = load_m31_harness_gate_json(gp)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "out",
        m31_gate=loaded,
        fixture_ci=False,
        max_evaluation_cases=1,
    )
    assert sealed["execution_status"] == STATUS_OPERATOR_LOCAL_METADATA_COMPLETED
    assert sealed["evaluation_execution_performed"] is True
    assert sealed["fixture_ci"] is False


def test_cli_missing_m31_path(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="missing required M31"):
        emit_m32_main(
            [
                "--m31-harness-gate-json",
                str(tmp_path / "nope.json"),
                "--output-dir",
                str(tmp_path / "o"),
            ],
        )


def test_blocked_invalid_m31_contract(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["contract_id"] = "wrong"
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_invalid_m31_contract" in sealed["blocked_reasons"]
    assert sealed["execution_status"] == STATUS_REFUSED_BLOCKERS
    assert sealed["evaluation_execution_performed"] is False


def test_blocked_invalid_m31_profile(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["profile"] = f"{PROFILE_M31_DRY_RUN}x"
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_invalid_m31_profile" in sealed["blocked_reasons"]


def test_blocked_m31_gate_not_ready(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["gate_status"] = "evaluation_harness_refused_with_blockers"
    wo["evaluation_harness_ready"] = False
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_m31_gate_not_ready" in sealed["blocked_reasons"]


def test_blocked_m31_claim_flags_inconsistent(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["benchmark_passed"] = True
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_m31_claim_flags_inconsistent" in sealed["blocked_reasons"]


def test_blocked_candidate_missing(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["candidate_checkpoint"] = {}
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_m31_candidate_checkpoint_missing" in sealed["blocked_reasons"]


def test_blocked_candidate_not_candidate_only(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["candidate_checkpoint"] = {
        "sha256": "a" * 64,
        "promotion_status": "promoted",
    }
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_m31_candidate_checkpoint_not_candidate_only" in sealed["blocked_reasons"]


def test_blocked_dry_run_plan_missing(tmp_path: Path) -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["dry_run_evaluation_plan"] = {"plan_status": "wrong"}
    m31 = _reseal_m31(wo)
    sealed, *_ = emit_v15_m32_candidate_checkpoint_evaluation_execution(
        tmp_path / "o",
        m31_gate=m31,
        fixture_ci=True,
        max_evaluation_cases=1,
    )
    assert "blocked_m31_dry_run_plan_missing" in sealed["blocked_reasons"]


def test_validate_m31_for_m32_sorts_blockers() -> None:
    base = build_fixture_m31_sealed_gate()
    wo = {k: v for k, v in base.items() if k != "artifact_sha256"}
    wo["contract_id"] = "x"
    wo["profile"] = "y"
    m31 = _reseal_m31(wo)
    br = validate_m31_for_m32(m31)
    assert br == sorted(br)
    assert br[0] == "blocked_invalid_m31_contract"


def test_emit_cli_fixture_writes_json(tmp_path: Path) -> None:
    rc = emit_m32_main(
        [
            "--fixture-ci",
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )
    assert rc == 0
    p = tmp_path / "out" / FILENAME_EXEC_JSON
    assert p.is_file()
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert raw["execution_status"] == STATUS_FIXTURE_COMPLETED


def test_fixture_m31_digest_anchor_documented() -> None:
    """Known fixture M31 gate digest (CI fixture pipeline; not a universal operator requirement)."""
    assert build_fixture_m31_sealed_gate()["artifact_sha256"] == FIXTURE_M31_GATE_DIGEST


def test_sealed_m31_contract_constant_matches_gate() -> None:
    g = build_fixture_m31_sealed_gate()
    assert g["contract_id"] == CONTRACT_ID_M31_GATE
