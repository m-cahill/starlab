"""V15-M45 bounded candidate evaluation execution surface tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m44_bounded_evaluation_execution_preflight_io import (
    emit_m44_fixture_ci as emit_m44_fixture,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
    DIGEST_FIELD as M44_DIGEST,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
    STATUS_PREFLIGHT_NOT_READY as M44_STATUS_NOT_READY,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_io import (
    emit_m45_fixture_ci,
    emit_m45_forbidden_flag_refusal,
    emit_m45_operator,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_models import (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_EXECUTE_T2,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD_RESULTS,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_CHECKPOINT_LOAD_REQUEST,
    REFUSED_DISALLOWED_BENCHMARK_REQUEST,
    REFUSED_HUMAN_PANEL_REQUEST,
    REFUSED_LIVE_SC2_REQUEST,
    REFUSED_M44_DRY_RUN_PLAN_NOT_CONSTRUCTED,
    REFUSED_M44_HONESTY_FLAGS_VIOLATION,
    REFUSED_M44_PREFLIGHT_NOT_READY,
    REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED,
    REFUSED_PROMOTION_REQUEST,
    REFUSED_ROUTE_OUT_OF_SCOPE,
    REFUSED_SCORECARD_RESULTS_REQUEST,
    REFUSED_XAI_REQUEST,
    STATUS_EXECUTION_COMPLETED_SYNTHETIC,
    STATUS_EXECUTION_NOT_READY,
    STATUS_EXECUTION_SURFACE_READY,
)


def _upstream_dir(tmp_path: Path) -> Path:
    u = tmp_path / "m44_fixture"
    emit_m44_fixture(u)
    return u


def test_m45_fixture_ready_path(tmp_path: Path) -> None:
    out = tmp_path / "fx"
    sealed, paths = emit_m45_fixture_ci(out)
    assert sealed["execution_status"] == STATUS_EXECUTION_SURFACE_READY
    for k in (
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_results_produced",
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
    ):
        assert sealed[k] is False, f"{k} must be False"
    assert sealed["bounded_execution_surface_invoked"] is False
    assert sealed["synthetic_execution_receipt_emitted"] is False
    receipt = sealed["execution_receipt"]
    assert receipt["receipt_status"] == "not_executed_or_synthetic_only"
    assert receipt["scorecard_mode"] == "none"
    assert receipt["benchmark_mode"] == "none"
    assert receipt["sc2_mode"] == "not_run"
    assert sealed["non_claims"]
    interp = sealed["m44_preflight_interpretation"]
    assert interp["interpretation"] == "preflight_bookkeeping_only_not_benchmark_success"
    assert len(paths) == 3


def test_m45_operator_preflight_valid_m44(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=m44_path,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_SURFACE_READY
    assert sealed["bounded_execution_surface_invoked"] is False
    assert sealed["synthetic_execution_receipt_emitted"] is False


def test_m45_operator_local_bounded_execution_synthetic(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
        m44_preflight_path=m44_path,
        allow_operator_local_execution=True,
        authorize_bounded_evaluation_execution=True,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_COMPLETED_SYNTHETIC
    assert sealed["bounded_execution_surface_invoked"] is True
    assert sealed["synthetic_execution_receipt_emitted"] is True
    receipt = sealed["execution_receipt"]
    assert receipt["receipt_status"] == "synthetic_execution_receipt_emitted"
    assert receipt["execution_mode"] == "operator_local_synthetic_bounded"
    assert receipt["scorecard_mode"] == "none"
    assert receipt["benchmark_mode"] == "none"
    assert receipt["sc2_mode"] == "not_run"
    for k in (
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_results_produced",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
    ):
        assert sealed[k] is False, f"{k} must remain False even in synthetic profile"


def test_m45_operator_local_refuses_without_both_guards(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    outp = tmp_path / "out1"
    sealed1, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
        m44_preflight_path=m44_path,
        allow_operator_local_execution=True,
        authorize_bounded_evaluation_execution=False,
    )
    assert sealed1["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED for r in sealed1["refusals"])

    outp2 = tmp_path / "out2"
    sealed2, _ = emit_m45_operator(
        outp2,
        profile=PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
        m44_preflight_path=m44_path,
        allow_operator_local_execution=False,
        authorize_bounded_evaluation_execution=True,
    )
    assert sealed2["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED for r in sealed2["refusals"])


def test_m45_refuses_missing_m44(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=None,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == "refused_missing_m44_preflight" for r in sealed["refusals"])


def test_m45_refuses_invalid_m44_seal(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    m44 = json.loads(m44_path.read_text(encoding="utf-8"))
    m44[M44_DIGEST] = "0" * 64
    bad_path = tmp_path / "bad_m44.json"
    bad_path.write_text(canonical_json_dumps(m44), encoding="utf-8")
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=bad_path,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == "refused_invalid_m44_preflight" for r in sealed["refusals"])


def test_m45_refuses_m44_not_ready(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    m44 = json.loads(m44_path.read_text(encoding="utf-8"))
    m44.pop(M44_DIGEST, None)
    m44["preflight_status"] = M44_STATUS_NOT_READY
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    wo = {k: v for k, v in m44.items() if k != M44_DIGEST}
    m44[M44_DIGEST] = sha256_hex_of_canonical_json(wo)
    bad_path = tmp_path / "not_ready_m44.json"
    bad_path.write_text(canonical_json_dumps(m44), encoding="utf-8")
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=bad_path,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == REFUSED_M44_PREFLIGHT_NOT_READY for r in sealed["refusals"])


def test_m45_refuses_m44_honesty_violation(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    m44 = json.loads(m44_path.read_text(encoding="utf-8"))
    m44.pop(M44_DIGEST, None)
    m44["benchmark_execution_performed"] = True
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    wo = {k: v for k, v in m44.items() if k != M44_DIGEST}
    m44[M44_DIGEST] = sha256_hex_of_canonical_json(wo)
    bad_path = tmp_path / "honesty_m44.json"
    bad_path.write_text(canonical_json_dumps(m44), encoding="utf-8")
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=bad_path,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == REFUSED_M44_HONESTY_FLAGS_VIOLATION for r in sealed["refusals"])


def test_m45_refuses_m44_dry_run_plan_not_constructed(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    m44_path = u / "v15_bounded_evaluation_execution_preflight.json"
    m44 = json.loads(m44_path.read_text(encoding="utf-8"))
    m44.pop(M44_DIGEST, None)
    m44["dry_run_plan"]["plan_status"] = "not_constructed_refused"
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    wo = {k: v for k, v in m44.items() if k != M44_DIGEST}
    m44[M44_DIGEST] = sha256_hex_of_canonical_json(wo)
    bad_path = tmp_path / "no_plan_m44.json"
    bad_path.write_text(canonical_json_dumps(m44), encoding="utf-8")
    outp = tmp_path / "out"
    sealed, _ = emit_m45_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m44_preflight_path=bad_path,
    )
    assert sealed["execution_status"] == STATUS_EXECUTION_NOT_READY
    assert any(r["code"] == REFUSED_M44_DRY_RUN_PLAN_NOT_CONSTRUCTED for r in sealed["refusals"])


def test_m45_forbidden_flag_benchmark_pass(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS],
    )
    assert sealed["execution_status"] == REFUSED_DISALLOWED_BENCHMARK_REQUEST
    assert any(r["code"] == REFUSED_DISALLOWED_BENCHMARK_REQUEST for r in sealed["refusals"])


def test_m45_forbidden_flag_scorecard_results(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_PRODUCE_SCORECARD_RESULTS],
    )
    assert sealed["execution_status"] == REFUSED_SCORECARD_RESULTS_REQUEST


def test_m45_forbidden_flag_checkpoint_load(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_LOAD_CHECKPOINT],
    )
    assert sealed["execution_status"] == REFUSED_CHECKPOINT_LOAD_REQUEST


def test_m45_forbidden_flag_live_sc2(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_RUN_LIVE_SC2],
    )
    assert sealed["execution_status"] == REFUSED_LIVE_SC2_REQUEST


def test_m45_forbidden_flag_promote_checkpoint(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_PROMOTE_CHECKPOINT],
    )
    assert sealed["execution_status"] == REFUSED_PROMOTION_REQUEST


def test_m45_forbidden_flag_xai(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_RUN_XAI],
    )
    assert sealed["execution_status"] == REFUSED_XAI_REQUEST


def test_m45_forbidden_flag_human_panel(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_RUN_HUMAN_PANEL],
    )
    assert sealed["execution_status"] == REFUSED_HUMAN_PANEL_REQUEST


def test_m45_forbidden_flag_t2_t5_out_of_scope(tmp_path: Path) -> None:
    outp = tmp_path / "out"
    sealed, _ = emit_m45_forbidden_flag_refusal(
        outp,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=[FORBIDDEN_FLAG_EXECUTE_T2],
    )
    assert sealed["execution_status"] == REFUSED_ROUTE_OUT_OF_SCOPE


def test_m45_no_torch_load_call_in_io_module() -> None:
    from starlab.v15 import m45_bounded_candidate_evaluation_execution_io as io_mod

    src = Path(io_mod.__file__).read_text(encoding="utf-8")
    assert "torch.load(" not in src
    assert "import torch" not in src


def test_m45_no_torch_load_call_in_cli_module() -> None:
    from starlab.v15 import emit_v15_m45_bounded_candidate_evaluation_execution as cli_mod

    src = Path(cli_mod.__file__).read_text(encoding="utf-8")
    assert "torch.load(" not in src
    assert "import torch" not in src


def test_m45_deterministic_fixture_sha(tmp_path: Path) -> None:
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    sealed1, _ = emit_m45_fixture_ci(out1)
    sealed2, _ = emit_m45_fixture_ci(out2)
    assert sealed1["artifact_sha256"] == sealed2["artifact_sha256"]


def test_m45_checklist_generated_with_footer(tmp_path: Path) -> None:
    out = tmp_path / "out"
    emit_m45_fixture_ci(out)
    chk = (out / "v15_bounded_candidate_evaluation_execution_checklist.md").read_text(
        encoding="utf-8"
    )
    assert "This checklist is bounded execution/refusal bookkeeping." in chk
    assert "not benchmark pass/fail evidence" in chk
    assert "scorecard results" in chk
    assert "strength evaluation" in chk
    assert "checkpoint promotion" in chk


def test_m45_cli_fixture_ci_runs(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m45_bounded_candidate_evaluation_execution",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (out / "v15_bounded_candidate_evaluation_execution.json").exists()


def test_m45_cli_forbidden_flag_refuses(tmp_path: Path) -> None:
    out = tmp_path / "cli_out"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m45_bounded_candidate_evaluation_execution",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
            "--claim-benchmark-pass",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    sealed = json.loads(
        (out / "v15_bounded_candidate_evaluation_execution.json").read_text(encoding="utf-8")
    )
    assert sealed["execution_status"] == REFUSED_DISALLOWED_BENCHMARK_REQUEST


def test_m45_governance_ledger_needles() -> None:
    ledger_v15 = Path("docs/starlab-v1.5.md")
    if not ledger_v15.exists():
        pytest.skip("ledger not present in test environment")
    content = ledger_v15.read_text(encoding="utf-8")
    needles = [
        "V15-M45",
        "v15_bounded_candidate_evaluation_execution_surface_v1.md",
        "starlab.v15.bounded_candidate_evaluation_execution.v1",
    ]
    for n in needles:
        assert n in content, f"Needle {n!r} not found in V15 ledger"


def test_m45_runtime_doc_exists() -> None:
    doc = Path("docs/runtime/v15_bounded_candidate_evaluation_execution_surface_v1.md")
    if not doc.exists():
        pytest.skip("runtime doc not present in test environment")
    content = doc.read_text(encoding="utf-8")
    assert "V15-M45" in content
    assert "bounded execution/refusal bookkeeping" in content
    assert "torch.load" in content
