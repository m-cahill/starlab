"""V15-M49 bounded scorecard result execution surface tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m48_bounded_scorecard_execution_preflight_io import (
    emit_m48_fixture_ci,
    seal_m48_body,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    CONTRACT_ID_M48_PREFLIGHT,
    PROFILE_M48_EVIDENCE_GATE,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    DIGEST_FIELD as M48_DIGEST_FIELD,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    FILENAME_MAIN_JSON as M48_FILENAME,
)
from starlab.v15.m49_bounded_scorecard_result_execution_io import (
    build_fixture_scorecard_result_evidence,
    decide_m49_from_m48_and_evidence,
    emit_m49_fixture_ci,
    emit_m49_forbidden_flag_refusal,
    emit_m49_operator_declared,
    emit_m49_operator_preflight,
    evaluate_scorecard_result_evidence,
    upstream_candidate_sha_from_m48,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    CONTRACT_ID_M49_RESULT,
    FIXTURE_ARTIFACT_SHA_PLACEHOLDER,
    FORBIDDEN_FLAG_AUTHORIZE_V2,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_EXECUTE_T5,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    M48_STATUS_READY,
    PROFILE_M49_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_CANDIDATE_MISMATCH,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_DECLARED_SHAPE,
    REFUSED_INVALID_METRICS,
    REFUSED_INVALID_RESULT_EVIDENCE,
    REFUSED_LIVE_SC2,
    REFUSED_M48_HONESTY,
    REFUSED_M48_NOT_READY,
    REFUSED_M48_ROUTE_EXECUTED,
    REFUSED_M48_SCORECARD_ALREADY,
    REFUSED_MISSING_METRICS,
    REFUSED_MISSING_RESULT_EVIDENCE,
    REFUSED_MISSING_THRESHOLD,
    REFUSED_ROUTE_OUT_OF_SCOPE,
    RESULT_MODE_OPERATOR_BOUND,
    ROUTE_READOUT_PROMOTION_REFUSAL,
    STATUS_RESULT_COMPLETED,
    STATUS_RESULT_COMPLETED_WARNINGS,
    STATUS_RESULT_REFUSED,
    WARN_CANDIDATE_UPSTREAM_UNAVAILABLE,
    WARN_FORWARD_HINT_MISSING,
)

M49_DIGEST_FIELD = "artifact_sha256"


def _m49_false_claim_keys() -> tuple[str, ...]:
    return (
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
        "xai_executed",
        "human_panel_executed",
        "showcase_released",
        "v2_authorized",
        "t2_t3_t4_t5_executed",
    )


def assert_exec_refusals_false(blob: dict[str, object]) -> None:
    for k in _m49_false_claim_keys():
        assert blob.get(k) is False, k


def test_m49_fixture_ci_deterministic(tmp_path: Path) -> None:
    sealed, paths = emit_m49_fixture_ci(tmp_path / "fx")
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED
    assert sealed["contract_id"] == CONTRACT_ID_M49_RESULT
    assert sealed["profile_id"] == PROFILE_M49_SURFACE
    assert sealed["scorecard_results_produced"] is True
    assert sealed["scorecard_total_computed"] is True
    assert sealed["win_rate_computed"] is True
    assert_exec_refusals_false(sealed)
    assert len(paths) == 3


def _emit_valid_m48_and_evidence(tmp_path: Path) -> tuple[Path, Path]:
    m48_dir = tmp_path / "m48"
    emit_m48_fixture_ci(m48_dir)
    m48_p = m48_dir / M48_FILENAME
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    digest = str(m48[M48_DIGEST_FIELD]).lower()
    ev_path = tmp_path / "evidence.json"
    ev_path.write_text(
        canonical_json_dumps(build_fixture_scorecard_result_evidence(m48_digest_lower=digest)),
        encoding="utf-8",
    )
    return m48_p, ev_path


def _rebind_evidence_to_m48(*, m48_path: Path, ev_path: Path) -> None:
    m48 = json.loads(m48_path.read_text(encoding="utf-8"))
    digest = str(m48[M48_DIGEST_FIELD]).lower()
    ev_path.write_text(
        canonical_json_dumps(build_fixture_scorecard_result_evidence(m48_digest_lower=digest)),
        encoding="utf-8",
    )


def test_m49_preflight_valid_m48_completed(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "out",
        m48_path=m48_p,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED_WARNINGS
    w = [str(x) for x in (sealed.get("warnings") or [])]
    assert WARN_CANDIDATE_UPSTREAM_UNAVAILABLE in w
    assert sealed["scorecard_results_produced"] is True


def test_m49_preflight_m48_warnings(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    m48["preflight_status"] = "bounded_scorecard_execution_preflight_ready_with_warnings"
    m48["warnings"] = ["synthetic_m48_warning"]
    m48_p2 = tmp_path / "m48w.json"
    m48_p2.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=m48_p2, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "out2",
        m48_path=m48_p2,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED_WARNINGS
    w = sealed.get("warnings")
    assert isinstance(w, list) and len(w) >= 1


def test_m49_refuses_m48_not_ready(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    m48["preflight_status"] = "bounded_scorecard_execution_preflight_refused"
    mp = tmp_path / "bad.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_M48_NOT_READY for r in sealed["refusals"])


def test_m49_refuses_m48_honesty(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    m48["benchmark_passed"] = True
    mp = tmp_path / "bad.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_M48_HONESTY for r in sealed["refusals"])


def test_m49_refuses_m48_route_executed(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    rr = dict(m48["route_recommendation"])
    rr["route_status"] = "executed_globally"
    m48["route_recommendation"] = rr
    mp = tmp_path / "bad.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_M48_ROUTE_EXECUTED for r in sealed["refusals"])


def test_m49_refuses_m48_scorecard_execution_performed(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    m48["scorecard_execution_performed"] = True
    mp = tmp_path / "bad.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_M48_SCORECARD_ALREADY for r in sealed["refusals"])


def test_m49_missing_evidence(tmp_path: Path) -> None:
    m48_p, _ = _emit_valid_m48_and_evidence(tmp_path)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=None,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_MISSING_RESULT_EVIDENCE for r in sealed["refusals"])


def test_m49_invalid_evidence_contract(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    ev = json.loads(ev_p.read_text(encoding="utf-8"))
    ev["contract_id"] = "wrong"
    ev_p2 = tmp_path / "ev2.json"
    ev_p2.write_text(canonical_json_dumps(ev), encoding="utf-8")
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p2,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_INVALID_RESULT_EVIDENCE for r in sealed["refusals"])


def test_m49_missing_metrics(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    ev = json.loads(ev_p.read_text(encoding="utf-8"))
    del ev["metric_results"]
    ev_p2 = tmp_path / "ev2.json"
    ev_p2.write_text(canonical_json_dumps(ev), encoding="utf-8")
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p2,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_MISSING_METRICS for r in sealed["refusals"])


def test_m49_invalid_metrics(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    ev = json.loads(ev_p.read_text(encoding="utf-8"))
    ev["metric_results"]["win_rate"] = 1.5
    ev_p2 = tmp_path / "ev2.json"
    ev_p2.write_text(canonical_json_dumps(ev), encoding="utf-8")
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p2,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_INVALID_METRICS for r in sealed["refusals"])


def test_m49_candidate_mismatch(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    erg = m48.get("evidence_requirements_gate")
    assert isinstance(erg, dict)
    other_cand = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    erg["evidence_manifest_snapshot"] = {
        "candidate_checkpoint_sha256": other_cand,
    }
    m48["evidence_requirements_gate"] = erg
    mp = tmp_path / "m48b.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_CANDIDATE_MISMATCH for r in sealed["refusals"])


def test_m49_missing_threshold_policy(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    ev = json.loads(ev_p.read_text(encoding="utf-8"))
    del ev["threshold_policy"]
    ev_p2 = tmp_path / "ev2.json"
    ev_p2.write_text(canonical_json_dumps(ev), encoding="utf-8")
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p2,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_MISSING_THRESHOLD for r in sealed["refusals"])


def test_m49_valid_sets_scorecard_flags(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p,
    )
    assert sealed["scorecard_results_produced"] is True
    assert sealed["scorecard_total_computed"] is True
    assert sealed["win_rate_computed"] is True


def test_m49_valid_keeps_false_claims(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "o",
        m48_path=m48_p,
        evidence_path=ev_p,
    )
    assert_exec_refusals_false(sealed)


def test_m49_forbidden_benchmark_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m49_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_PASS_CLAIM for r in sealed["refusals"])


def test_m49_forbidden_strength_promote(tmp_path: Path) -> None:
    for flag, needle in (
        (FORBIDDEN_FLAG_CLAIM_STRENGTH, "refused_strength_claim"),
        (FORBIDDEN_FLAG_PROMOTE_CHECKPOINT, "refused_checkpoint_promotion_claim"),
    ):
        sealed, _ = emit_m49_forbidden_flag_refusal(
            tmp_path / f"x_{needle}",
            profile="fixture_ci",
            triggered_flags=[flag],
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m49_forbidden_load_live(tmp_path: Path) -> None:
    sealed, _ = emit_m49_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_LOAD_CHECKPOINT],
    )
    assert REFUSED_CHECKPOINT_LOAD in {r["code"] for r in sealed["refusals"]}
    sealed2, _ = emit_m49_forbidden_flag_refusal(
        tmp_path / "o2",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_RUN_LIVE_SC2],
    )
    assert REFUSED_LIVE_SC2 in {r["code"] for r in sealed2["refusals"]}


def test_m49_forbidden_xai_human_showcase_v2(tmp_path: Path) -> None:
    for flags, needle in (
        ([FORBIDDEN_FLAG_RUN_XAI], "refused_xai_claim"),
        ([FORBIDDEN_FLAG_RUN_HUMAN_PANEL], "refused_human_panel_claim"),
        ([FORBIDDEN_FLAG_RELEASE_SHOWCASE], "refused_showcase_release_claim"),
        ([FORBIDDEN_FLAG_AUTHORIZE_V2], "refused_v2_authorization_claim"),
    ):
        sealed, _ = emit_m49_forbidden_flag_refusal(
            tmp_path / f"n_{needle}",
            profile="fixture_ci",
            triggered_flags=flags,
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m49_forbidden_t5(tmp_path: Path) -> None:
    sealed, _ = emit_m49_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_EXECUTE_T5],
    )
    assert "refused_t2_t5_execution_claim" in {r["code"] for r in sealed["refusals"]}


def test_m49_no_torch_load_in_io_cli() -> None:
    from starlab.v15 import emit_v15_m49_bounded_scorecard_result_execution as cli_mod
    from starlab.v15 import m49_bounded_scorecard_result_execution_io as io_mod

    for mod in (io_mod, cli_mod):
        mf = mod.__file__
        assert mf is not None
        src = Path(mf).read_text(encoding="utf-8")
        assert "torch.load(" not in src
        assert "import torch" not in src


def test_m49_no_checkpoint_blob_reads_in_io() -> None:
    from starlab.v15 import m49_bounded_scorecard_result_execution_io as io_mod

    mf = io_mod.__file__
    assert mf is not None
    src = Path(mf).read_text(encoding="utf-8")
    assert ".pt" not in src
    assert ".pth" not in src
    assert "read_bytes" not in src


def test_m49_fixture_deterministic_digest(tmp_path: Path) -> None:
    a, _ = emit_m49_fixture_ci(tmp_path / "a")
    b, _ = emit_m49_fixture_ci(tmp_path / "b")
    assert a[M49_DIGEST_FIELD] == b[M49_DIGEST_FIELD]


def test_m49_brief_footer(tmp_path: Path) -> None:
    emit_m49_fixture_ci(tmp_path / "o")
    brief = (tmp_path / "o" / "v15_bounded_scorecard_result_execution_brief.md").read_text(
        encoding="utf-8",
    )
    assert "This brief is a bounded scorecard result artifact." in brief
    assert "not benchmark pass/fail " in brief.lower() or "benchmark pass/fail" in brief.lower()


def test_m49_governance_ledger_runtime_needles() -> None:
    repo = Path(__file__).resolve().parents[1]
    v15 = repo / "docs/starlab-v1.5.md"
    ledger = repo / "docs/starlab.md"
    rt = repo / "docs/runtime/v15_bounded_scorecard_result_execution_surface_v1.md"
    if not (v15.is_file() and ledger.is_file() and rt.is_file()):
        pytest.skip("docs not present in test workspace")
    v15_txt = v15.read_text(encoding="utf-8")
    lc = ledger.read_text(encoding="utf-8")
    assert "V15-M49" in v15_txt and "V15-M49" in lc
    combined = (v15_txt + lc + rt.read_text(encoding="utf-8")).lower().replace("`", "")
    needles = (
        "v15_bounded_scorecard_result_execution_surface_v1.md",
        "starlab.v15.bounded_scorecard_result_execution.v1",
        "starlab.v15.m49.bounded_scorecard_result_execution_surface.v1",
        "bounded_scorecard_result_execution_completed",
        "bounded_scorecard_result_execution_completed_with_warnings",
        "bounded_scorecard_result_execution_refused",
        "scorecard_results_emitted_bounded",
        "benchmark_pass_fail_refused_pending_threshold_readout",
        "promotion_refused_pending_scorecard_readout",
        "refused_m48_preflight_not_ready",
        "refused_invalid_scorecard_result_evidence",
        "refused_candidate_identity_mismatch",
        "refused_missing_metric_results",
        "scorecard_results_produced",
        "scorecard_total_computed",
        "win_rate_computed",
        "benchmark_passed",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
        "false",
    )
    for needle in needles:
        assert needle in combined, f"missing governance needle {needle!r}"


def test_m49_warning_forward_hint_missing(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    cep = m48.get("scorecard_execution_preflight")
    assert isinstance(cep, dict)
    cep.pop("future_contract_id", None)
    cep.pop("future_profile_id", None)
    m48["scorecard_execution_preflight"] = cep
    mp = tmp_path / "m48nh.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "out",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED_WARNINGS
    w = [str(x) for x in (sealed.get("warnings") or [])]
    assert any(WARN_FORWARD_HINT_MISSING in x for x in w)


def test_m49_refuses_forward_hint_conflict(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48 = json.loads(m48_p.read_text(encoding="utf-8"))
    m48.pop(M48_DIGEST_FIELD, None)
    cep = m48.get("scorecard_execution_preflight")
    assert isinstance(cep, dict)
    cep["future_contract_id"] = "wrong"
    m48["scorecard_execution_preflight"] = cep
    mp = tmp_path / "m48bad.json"
    mp.write_text(canonical_json_dumps(seal_m48_body(m48)), encoding="utf-8")
    _rebind_evidence_to_m48(m48_path=mp, ev_path=ev_p)
    sealed, _ = emit_m49_operator_preflight(
        tmp_path / "out",
        m48_path=mp,
        evidence_path=ev_p,
    )
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_ROUTE_OUT_OF_SCOPE for r in sealed["refusals"])


def test_m49_upstream_candidate_warn_when_missing(tmp_path: Path) -> None:
    m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    m48_plain = json.loads(m48_p.read_text(encoding="utf-8"))
    assert upstream_candidate_sha_from_m48(m48_plain) is None
    d = decide_m49_from_m48_and_evidence(
        m48_plain,
        json.loads(ev_p.read_text(encoding="utf-8")),
        result_mode=RESULT_MODE_OPERATOR_BOUND,
        require_canonical_seal=True,
    )
    assert d.result_status == STATUS_RESULT_COMPLETED_WARNINGS
    assert any(WARN_CANDIDATE_UPSTREAM_UNAVAILABLE in w for w in d.warnings)


def _sha64_char(c: str = "c") -> str:
    return (c * 64).lower()


def _minimal_operator_declared_m49() -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_M49_RESULT,
        "profile_id": PROFILE_M49_SURFACE,
        "result_status": STATUS_RESULT_COMPLETED,
        "m48_binding": {
            "contract_id": CONTRACT_ID_M48_PREFLIGHT,
            "profile_id": PROFILE_M48_EVIDENCE_GATE,
            "artifact_sha256": _sha64_char("c"),
            "preflight_status": M48_STATUS_READY,
        },
        "scorecard_result": {
            "candidate_checkpoint_sha256": FIXTURE_ARTIFACT_SHA_PLACEHOLDER,
            "scorecard_total": 0.5,
            "win_rate": 0.25,
            "episode_count": 4,
            "valid_episode_count": 1,
            "threshold_policy": {
                "policy_id": "declared_bounded_threshold_policy_v1",
                "pass_threshold": 0.0,
            },
            "metric_results": {},
        },
    }


def _write_declared_json(tmp_path: Path, payload: dict[str, object]) -> Path:
    p = tmp_path / "declared.json"
    p.write_text(canonical_json_dumps(payload), encoding="utf-8")
    return p


def test_m49_operator_declared_completed(tmp_path: Path) -> None:
    dpath = _write_declared_json(tmp_path, _minimal_operator_declared_m49())
    sealed, _paths = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED
    assert sealed["profile"] == PROFILE_OPERATOR_DECLARED
    assert (tmp_path / "od" / "v15_bounded_scorecard_result_execution.json").is_file()


def test_m49_operator_declared_completed_with_warnings(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["result_status"] = STATUS_RESULT_COMPLETED_WARNINGS
    blob["warnings"] = ["declared_warning"]
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_COMPLETED_WARNINGS
    w = [str(x) for x in (sealed.get("warnings") or [])]
    assert "declared_warning" in w


def test_m49_operator_declared_contract_mismatch(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["contract_id"] = "wrong.contract"
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_DECLARED_SHAPE for r in sealed["refusals"])


def test_m49_operator_declared_overclaim(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["benchmark_passed"] = True
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == REFUSED_DECLARED_SHAPE for r in sealed["refusals"])
    assert "declared_overclaim" in (sealed["refusals"][0].get("detail") or "")


def test_m49_operator_declared_invalid_m48_binding(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["m48_binding"] = {"artifact_sha256": ""}
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(
        r["code"] == REFUSED_DECLARED_SHAPE and "m48_binding" in (r.get("detail") or "")
        for r in sealed["refusals"]
    )


def test_m49_operator_declared_refused_passthrough(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["result_status"] = STATUS_RESULT_REFUSED
    blob["refusals"] = [{"code": "synthetic_declared_refusal", "detail": "x"}]
    blob["route_recommendation"] = {"next_route": ROUTE_READOUT_PROMOTION_REFUSAL}
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(r["code"] == "synthetic_declared_refusal" for r in sealed["refusals"])


def test_m49_operator_declared_refused_missing_refs(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["result_status"] = STATUS_RESULT_REFUSED
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(
        "declared_refused_without_refusals" in (r.get("detail") or "") for r in sealed["refusals"]
    )


def test_m49_operator_declared_invalid_result_status(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["result_status"] = "not_a_valid_status"
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any("invalid_result_status" in (r.get("detail") or "") for r in sealed["refusals"])


def test_m49_operator_declared_metrics_invalid(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    scr = blob["scorecard_result"]
    assert isinstance(scr, dict)
    scr["win_rate"] = 2.0
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(
        "scorecard_result_metric_fields_invalid" in (r.get("detail") or "")
        for r in sealed["refusals"]
    )


def test_m49_operator_declared_non_claims_merge(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["non_claims"] = ["operator_supplied_non_claim"]
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    ncl = sealed.get("non_claims") or []
    flat = " ".join(str(x) for x in ncl)
    assert "operator_supplied_non_claim" in flat


def test_m49_operator_declared_m48_interpretation_preserved(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    mb = blob["m48_binding"]
    assert isinstance(mb, dict)
    mb["interpretation"] = "operator_m48_binding_interpretation"
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    m48b = sealed.get("m48_binding")
    assert isinstance(m48b, dict)
    assert m48b.get("interpretation") == "operator_m48_binding_interpretation"


def test_m49_operator_declared_disallowed_claim_decision(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    blob["claim_decisions"] = {"scorecard_results": "not_an_allowed_claim_token"}
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    det = " ".join(str(r.get("detail") or "") for r in sealed["refusals"])
    assert "disallowed_claim_decision" in det


def test_m49_operator_declared_scorecard_block_missing(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    del blob["scorecard_result"]
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(
        "scorecard_result_missing_or_invalid" in (r.get("detail") or "") for r in sealed["refusals"]
    )


def test_m49_operator_declared_candidate_required(tmp_path: Path) -> None:
    blob = _minimal_operator_declared_m49()
    scr = blob["scorecard_result"]
    assert isinstance(scr, dict)
    scr["candidate_checkpoint_sha256"] = "short"
    dpath = _write_declared_json(tmp_path, blob)
    sealed, _ = emit_m49_operator_declared(tmp_path / "od", declared_result_path=dpath)
    assert sealed["result_status"] == STATUS_RESULT_REFUSED
    assert any(
        "candidate_checkpoint_sha256_required" in (r.get("detail") or "")
        for r in sealed["refusals"]
    )


def test_evaluate_evidence_binding_mismatch(tmp_path: Path) -> None:
    _m48_p, ev_p = _emit_valid_m48_and_evidence(tmp_path)
    ev = json.loads(ev_p.read_text(encoding="utf-8"))
    refs, _ = evaluate_scorecard_result_evidence(
        ev,
        m48_digest_expected="0" * 64,
    )
    assert REFUSED_INVALID_RESULT_EVIDENCE in refs


def test_m49_cli_fixture_ci(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m49_bounded_scorecard_result_execution",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    assert (out / "v15_bounded_scorecard_result_execution.json").is_file()


def test_m49_cli_preflight_requires_m48(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ev_p = tmp_path / "e.json"
    ev_p.write_text('{"contract_id":"x"}', encoding="utf-8")
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m49_bounded_scorecard_result_execution",
            "--profile",
            "operator_preflight",
            "--output-dir",
            str(out),
            "--scorecard-result-evidence-json",
            str(ev_p),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode != 0
    comb = (res.stderr or "") + (res.stdout or "")
    assert "--m48-preflight-json is required for operator_preflight" in comb
