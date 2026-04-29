"""V15-M30 SC2-backed candidate checkpoint evaluation package tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    CONTRACT_ID as CONTRACT_M29,
)
from starlab.v15.full_30min_sc2_backed_t1_run_models import (
    OUTCOME_FULL_30_WITH_CHECKPOINT,
    PROFILE_OPERATOR_LOCAL_FULL_WALL,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_io import (
    emit_m30_sc2_backed_candidate_checkpoint_evaluation_package,
    validate_m30_inputs,
)
from starlab.v15.m30_sc2_backed_candidate_checkpoint_evaluation_package_models import (
    PACKAGE_PROFILE_ID_M30,
    STATUS_READY,
)
from starlab.v15.sc2_backed_t1_candidate_training_io import seal_m28_body
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    CONTRACT_ID as CONTRACT_M28,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    EXPECTED_M27_CONTRACT_ID,
    M27_OUTCOME_COMPLETED,
)
from starlab.v15.sc2_backed_t1_candidate_training_models import (
    OUTCOME_WITH_CHECKPOINT as M28_OUTCOME_WITH_CKPT,
)
from starlab.v15.sc2_rollout_training_loop_integration_models import CONTRACT_ID as CONTRACT_M27
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

CAND_HEX = "eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26"


def _write_aligned_fixture_chain(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Minimal sealed M27/M28/M29 JSON that satisfies M30 guards."""

    m27_pre = {
        "contract_id": CONTRACT_M27,
        "milestone": "V15-M27",
        "m27_outcome": M27_OUTCOME_COMPLETED,
        "episodes": [{"action_count": 5}],
        "training_loop_binding": {"status": "training_update_executed"},
    }
    m27 = seal_m28_body(m27_pre)
    p27 = tmp_path / "m27.json"
    p27.write_text(canonical_json_dumps(m27), encoding="utf-8")
    sha27 = str(m27["artifact_sha256"])

    m28_pre = {
        "contract_id": CONTRACT_M28,
        "milestone": "V15-M28",
        "m28_outcome": M28_OUTCOME_WITH_CKPT,
        "training_attempt": {
            "sc2_backed_features_used": True,
            "full_wall_clock_satisfied": True,
            "require_full_wall_clock": True,
            "wall_clock_seconds": 1800.0,
            "requested_min_wall_clock_seconds": 1800.0,
            "candidate_checkpoint_sha256": CAND_HEX,
        },
        "candidate_checkpoint": {
            "produced": True,
            "sha256": CAND_HEX,
            "promotion_status": "not_promoted_candidate_only",
        },
        "upstream_m27_rollout": {
            "path_role": "operator_local_input",
            "resolved_path": "C:\\op\\fake_m27.json",
            "contract_id": EXPECTED_M27_CONTRACT_ID,
            "sha256": sha27,
            "outcome": M27_OUTCOME_COMPLETED,
            "action_count_summary": [5],
            "training_loop_binding_status": "training_update_executed",
        },
    }
    m28 = seal_m28_body(m28_pre)
    p28 = tmp_path / "m28.json"
    p28.write_text(canonical_json_dumps(m28), encoding="utf-8")
    sha28 = str(m28["artifact_sha256"])

    m29_pre = {
        "contract_id": CONTRACT_M29,
        "milestone": "V15-M29",
        "profile": PROFILE_OPERATOR_LOCAL_FULL_WALL,
        "m29_outcome": OUTCOME_FULL_30_WITH_CHECKPOINT,
        "full_wall_clock_satisfied": True,
        "requested_min_wall_clock_seconds": 1800.0,
        "observed_wall_clock_seconds": 1800.0,
        "sc2_backed_features_used": True,
        "candidate_checkpoint_promotion_status": "not_promoted_candidate_only",
        "candidate_checkpoint_sha256_operator_local": CAND_HEX,
        "upstream_m27_artifact_sha256": sha27,
        "upstream_m28_primary_artifact_sha256": sha28,
        "upstream_m28_candidate_checkpoint_sha256_reference": CAND_HEX,
        "upstream_m28_contract_consumed": CONTRACT_M28,
    }
    m29 = seal_m28_body(m29_pre)
    p29 = tmp_path / "m29.json"
    p29.write_text(canonical_json_dumps(m29), encoding="utf-8")

    return p27, p28, p29


def test_m30_fixture_chain_ready(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    assert validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=None) == []

    out = tmp_path / "pkg"
    sealed, pkg_p, _, _ = emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
        out,
        m27_path=p27,
        m28_path=p28,
        m29_path=p29,
        scorecard_path=None,
    )
    assert sealed["evaluation_package_ready"] is True
    assert sealed["package_status"] == STATUS_READY
    assert sealed["package_profile_id"] == PACKAGE_PROFILE_ID_M30
    assert sealed["strength_evaluated"] is False
    assert sealed["checkpoint_promoted"] is False
    assert sealed["benchmark_passed"] is False
    assert sealed["blocked_reasons"] == []

    pkg_txt = pkg_p.read_text(encoding="utf-8")
    assert "C:\\\\" not in pkg_txt and "C:\\" not in pkg_txt


def test_m29_full_wall_clock_blocked(tmp_path: Path) -> None:
    p27, p28, m29p = _write_aligned_fixture_chain(tmp_path)
    m29 = json.loads(m29p.read_text(encoding="utf-8"))
    m29["full_wall_clock_satisfied"] = False
    m29_sealed = seal_m28_body({k: v for k, v in m29.items() if k != "artifact_sha256"})
    m29p.write_text(canonical_json_dumps(m29_sealed), encoding="utf-8")

    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads((tmp_path / "m28.json").read_text(encoding="utf-8"))
    raw29 = json.loads(m29p.read_text(encoding="utf-8"))
    br = validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=None)
    assert "blocked_m29_full_wall_clock_not_satisfied" in br


def test_m28_m29_artifact_mismatch(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    m29 = json.loads(p29.read_text(encoding="utf-8"))
    m29["upstream_m28_primary_artifact_sha256"] = "a" * 64
    m29_sealed = seal_m28_body({k: v for k, v in m29.items() if k != "artifact_sha256"})
    p29.write_text(canonical_json_dumps(m29_sealed), encoding="utf-8")

    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    br = validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=None)
    assert "blocked_m28_m29_artifact_sha_mismatch" in br


def test_m27_chain_mismatch(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    m29 = json.loads(p29.read_text(encoding="utf-8"))
    m29["upstream_m27_artifact_sha256"] = "b" * 64
    m29_sealed = seal_m28_body({k: v for k, v in m29.items() if k != "artifact_sha256"})
    p29.write_text(canonical_json_dumps(m29_sealed), encoding="utf-8")

    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    br = validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=None)
    assert "blocked_m27_m28_m29_artifact_sha_mismatch" in br


def test_candidate_sha_mismatch(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    m29 = json.loads(p29.read_text(encoding="utf-8"))
    m29["candidate_checkpoint_sha256_operator_local"] = "c" * 64
    m29["upstream_m28_candidate_checkpoint_sha256_reference"] = "c" * 64
    m29_sealed = seal_m28_body({k: v for k, v in m29.items() if k != "artifact_sha256"})
    p29.write_text(canonical_json_dumps(m29_sealed), encoding="utf-8")

    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    br = validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=None)
    assert "blocked_candidate_checkpoint_sha_mismatch" in br


def test_optional_scorecard_invalid(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    bad_sc = {"contract_id": "wrong", "protocol_profile_id": PROTOCOL_PROFILE_ID}
    br = validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=bad_sc)
    assert "blocked_invalid_scorecard_protocol_json" in br


def test_optional_scorecard_ok(tmp_path: Path) -> None:
    p27, p28, p29 = _write_aligned_fixture_chain(tmp_path)
    sc_pre = {
        "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
    }
    sc = seal_m28_body(sc_pre)
    sc_p = tmp_path / "sc.json"
    sc_p.write_text(canonical_json_dumps(sc), encoding="utf-8")
    raw_sc = json.loads(sc_p.read_text(encoding="utf-8"))

    raw27 = json.loads(p27.read_text(encoding="utf-8"))
    raw28 = json.loads(p28.read_text(encoding="utf-8"))
    raw29 = json.loads(p29.read_text(encoding="utf-8"))
    assert validate_m30_inputs(m27=raw27, m28=raw28, m29=raw29, scorecard=raw_sc) == []

    sealed, _, _, _ = emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
        tmp_path / "out",
        m27_path=p27,
        m28_path=p28,
        m29_path=p29,
        scorecard_path=sc_p,
    )
    assert sealed["evaluation_protocol_binding"]["scorecard_binding_status"] == "bound"


@pytest.mark.skipif(
    not (
        REPO_ROOT
        / "out"
        / "v15_m29"
        / "full_30min_sc2_backed_t1_run1"
        / "v15_full_30min_sc2_backed_t1_run.json"
    ).is_file(),
    reason="operator-local out/ bundle not present",
)
def test_operator_local_bundle_when_present(tmp_path: Path) -> None:
    m27 = (
        REPO_ROOT
        / "out/v15_m27/sc2_rollout_integration_run1/v15_sc2_rollout_training_loop_integration.json"
    )
    m28 = (
        REPO_ROOT
        / "out/v15_m29/full_30min_sc2_backed_t1_run1/v15_sc2_backed_t1_candidate_training.json"
    )
    m29 = (
        REPO_ROOT
        / "out/v15_m29/full_30min_sc2_backed_t1_run1/v15_full_30min_sc2_backed_t1_run.json"
    )
    if not (m27.is_file() and m28.is_file() and m29.is_file()):
        pytest.skip("missing one of operator-local inputs")

    sealed, _, _, _ = emit_m30_sc2_backed_candidate_checkpoint_evaluation_package(
        tmp_path / "op_pkg",
        m27_path=m27,
        m28_path=m28,
        m29_path=m29,
        scorecard_path=None,
    )
    assert sealed["evaluation_package_ready"] is True
