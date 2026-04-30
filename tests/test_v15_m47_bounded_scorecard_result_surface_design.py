"""V15-M47 bounded scorecard result surface design / refusal gate tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m46_bounded_evaluation_readout_decision_io import (
    emit_m46_fixture_ci,
    seal_m46_body,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    CONTRACT_ID_M46_READOUT,
    PROFILE_M46_READOUT,
    PROMOTION_REFUSED_INSUFFICIENT,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_SYNTH_WARNING,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    DIGEST_FIELD as M46_DIGEST_FIELD,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    FILENAME_MAIN_JSON as M46_FILENAME,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_io import (
    build_scorecard_surface_design_block,
    emit_m47_fixture_ci,
    emit_m47_forbidden_flag_refusal,
    emit_m47_operator_declared,
    emit_m47_operator_preflight,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    CLAIM_BENCHMARK_REFUSED,
    CONTRACT_ID_M47_SURFACE,
    FORBIDDEN_FLAG_AUTHORIZE_V2,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_CLAIM_SCORECARD,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL,
    FORBIDDEN_FLAG_EXECUTE_T5,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    PROFILE_M47_REFUSAL_GATE,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_LIVE_SC2,
    REFUSED_M46_HONESTY,
    REFUSED_M46_NOT_COMPLETED,
    REFUSED_M46_PROMOTION_NOT_REFUSED,
    REFUSED_M46_ROUTE_EXECUTED,
    REFUSED_M46_SCORECARD_PRESENT,
    REFUSED_SCORECARD_RESULTS_CLAIM,
    ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
    STATUS_DESIGN_READY,
    STATUS_DESIGN_READY_WARNINGS,
    STATUS_DESIGN_REFUSED,
)


def _m47_honesty_false_keys() -> tuple[str, ...]:
    return (
        "scorecard_results_produced",
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_total_computed",
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


def assert_all_false_m47_claim_bools(blob: dict[str, object]) -> None:
    for k in _m47_honesty_false_keys():
        assert blob.get(k) is False, f"{k}"


def test_m47_fixture_ci_deterministic_surface(tmp_path: Path) -> None:
    outp = tmp_path / "fx"
    sealed, paths = emit_m47_fixture_ci(outp)
    assert sealed["design_status"] == STATUS_DESIGN_READY
    assert sealed["claim_decisions"]["benchmark_pass_fail"] == CLAIM_BENCHMARK_REFUSED
    assert sealed["route_recommendation"]["next_route"] == ROUTE_TO_SCORECARD_EXEC_PREFLIGHT
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert_all_false_m47_claim_bools(sealed)
    ssd = sealed["scorecard_surface_design"]
    assert isinstance(ssd, dict)
    assert ssd.get("future_result_surface_allowed_in_m47") is False
    assert len(paths) == 3


def test_m47_preflight_valid_m46_completed(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46_p = m46_dir / M46_FILENAME
    out = tmp_path / "dec"
    sealed, _ = emit_m47_operator_preflight(out, m46_path=m46_p)
    assert sealed["design_status"] == STATUS_DESIGN_READY
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert_all_false_m47_claim_bools(sealed)
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46_p = m46_dir / M46_FILENAME
    m46 = json.loads(m46_p.read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    m46["decision_status"] = STATUS_READOUT_COMPLETED_SYNTH_WARNING
    m46["warnings"] = ["synthetic_upstream_warning"]
    sealed46 = seal_m46_body(m46)
    syn = tmp_path / "m46_syn.json"
    syn.write_text(canonical_json_dumps(sealed46), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m47_operator_preflight(out, m46_path=syn)
    assert sealed["design_status"] == STATUS_DESIGN_READY_WARNINGS
    w = sealed.get("warnings")
    assert isinstance(w, list) and len(w) >= 1


def test_m47_refuses_m46_not_ready(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46 = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    m46["decision_status"] = "bounded_evaluation_readout_refused"
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m46_body(m46)), encoding="utf-8")
    sealed, _ = emit_m47_operator_preflight(tmp_path / "o", m46_path=p)
    assert sealed["design_status"] == STATUS_DESIGN_REFUSED
    assert any(r["code"] == REFUSED_M46_NOT_COMPLETED for r in sealed["refusals"])


def test_m47_refuses_m46_honesty_violation(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46 = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    m46["scorecard_results_produced"] = True
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m46_body(m46)), encoding="utf-8")
    sealed, _ = emit_m47_operator_preflight(tmp_path / "o", m46_path=p)
    assert sealed["design_status"] == STATUS_DESIGN_REFUSED
    assert any(r["code"] == REFUSED_M46_SCORECARD_PRESENT for r in sealed["refusals"])


def test_m47_refuses_m46_honesty_benchmark_pass(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46 = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    m46["benchmark_passed"] = True
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m46_body(m46)), encoding="utf-8")
    sealed, _ = emit_m47_operator_preflight(tmp_path / "o", m46_path=p)
    assert sealed["design_status"] == STATUS_DESIGN_REFUSED
    assert any(r["code"] == REFUSED_M46_HONESTY for r in sealed["refusals"])


def test_m47_refuses_m46_route_executed(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46 = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    rr = dict(m46["route_recommendation"])
    rr["route_status"] = "executed_globally"
    m46["route_recommendation"] = rr
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m46_body(m46)), encoding="utf-8")
    sealed, _ = emit_m47_operator_preflight(tmp_path / "o", m46_path=p)
    assert sealed["design_status"] == STATUS_DESIGN_REFUSED
    assert any(r["code"] == REFUSED_M46_ROUTE_EXECUTED for r in sealed["refusals"])


def test_m47_refuses_m46_promotion_not_refused(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46"
    emit_m46_fixture_ci(m46_dir)
    m46 = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))
    m46.pop(M46_DIGEST_FIELD, None)
    pr = dict(m46["promotion_decision"])
    pr["promotion_status"] = "promoted_to_showcase"
    m46["promotion_decision"] = pr
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m46_body(m46)), encoding="utf-8")
    sealed, _ = emit_m47_operator_preflight(tmp_path / "o", m46_path=p)
    assert sealed["design_status"] == STATUS_DESIGN_REFUSED
    assert any(r["code"] == REFUSED_M46_PROMOTION_NOT_REFUSED for r in sealed["refusals"])


def test_m47_forbidden_scorecard_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_SCORECARD],
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m47_forbidden_benchmark_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_PASS_CLAIM for r in sealed["refusals"])


def test_m47_forbidden_compute_total_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL],
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m47_forbidden_strength_promote(tmp_path: Path) -> None:
    for flag, needle in (
        (FORBIDDEN_FLAG_CLAIM_STRENGTH, "refused_strength_claim"),
        (FORBIDDEN_FLAG_PROMOTE_CHECKPOINT, "refused_checkpoint_promotion_claim"),
    ):
        sealed, _ = emit_m47_forbidden_flag_refusal(
            tmp_path / f"x_{needle}",
            profile="fixture_ci",
            triggered_flags=[flag],
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m47_forbidden_load_live(tmp_path: Path) -> None:
    sealed, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_LOAD_CHECKPOINT],
    )
    assert REFUSED_CHECKPOINT_LOAD in {r["code"] for r in sealed["refusals"]}
    sealed2, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o2",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_RUN_LIVE_SC2],
    )
    assert REFUSED_LIVE_SC2 in {r["code"] for r in sealed2["refusals"]}


def test_m47_forbidden_xai_human_showcase_v2(tmp_path: Path) -> None:
    for flags, needle in (
        ([FORBIDDEN_FLAG_RUN_XAI], "refused_xai_claim"),
        ([FORBIDDEN_FLAG_RUN_HUMAN_PANEL], "refused_human_panel_claim"),
        ([FORBIDDEN_FLAG_RELEASE_SHOWCASE], "refused_showcase_release_claim"),
        ([FORBIDDEN_FLAG_AUTHORIZE_V2], "refused_v2_authorization_claim"),
    ):
        sealed, _ = emit_m47_forbidden_flag_refusal(
            tmp_path / f"n_{needle}",
            profile="fixture_ci",
            triggered_flags=flags,
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m47_forbidden_t5(tmp_path: Path) -> None:
    sealed, _ = emit_m47_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_EXECUTE_T5],
    )
    assert "refused_t2_t5_execution_claim" in {r["code"] for r in sealed["refusals"]}


def test_m47_no_torch_load_in_io_cli() -> None:
    from starlab.v15 import emit_v15_m47_bounded_scorecard_result_surface_design as cli_mod
    from starlab.v15 import m47_bounded_scorecard_result_surface_design_io as io_mod

    for mod in (io_mod, cli_mod):
        mf = mod.__file__
        assert mf is not None
        src = Path(mf).read_text(encoding="utf-8")
        assert "torch.load(" not in src
        assert "import torch" not in src


def test_m47_no_checkpoint_blob_reads_in_io() -> None:
    from starlab.v15 import m47_bounded_scorecard_result_surface_design_io as io_mod

    mf = io_mod.__file__
    assert mf is not None
    src = Path(mf).read_text(encoding="utf-8")
    assert ".pt" not in src
    assert ".pth" not in src
    assert "read_bytes" not in src


def test_m47_fixture_deterministic_digest(tmp_path: Path) -> None:
    a, _ = emit_m47_fixture_ci(tmp_path / "o1")
    b, _ = emit_m47_fixture_ci(tmp_path / "o2")
    assert a["artifact_sha256"] == b["artifact_sha256"]


def test_m47_brief_has_required_footer(tmp_path: Path) -> None:
    emit_m47_fixture_ci(tmp_path / "o")
    brief = (tmp_path / "o" / "v15_bounded_scorecard_result_surface_design_brief.md").read_text(
        encoding="utf-8"
    )
    assert "This brief defines a future bounded scorecard result surface and refusal gate." in brief
    assert "not scorecard results, benchmark pass/fail evidence" in brief


def test_m47_scorecard_design_lists_fields_no_numeric_scores() -> None:
    blk = build_scorecard_surface_design_block()
    blob = json.dumps(blk)
    assert "win_rate" in blob or "win rate" in blob.lower()
    for bad in ("0.75", " 0.", "99.9", 'win_rate": 0'):
        assert bad not in blob


def test_m47_cli_fixture_ci(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m47_bounded_scorecard_result_surface_design",
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
    assert (out / "v15_bounded_scorecard_result_surface_design.json").is_file()


def _example_declared_m47(
    *,
    m46_digest: str,
    decision_status: str,
    route_status: str = ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
) -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_M47_SURFACE,
        "profile_id": PROFILE_M47_REFUSAL_GATE,
        "m46_binding": {
            "contract_id": CONTRACT_ID_M46_READOUT,
            "profile_id": PROFILE_M46_READOUT,
            "artifact_sha256": m46_digest,
            "decision_status": decision_status,
            "promotion_decision": {"promotion_status": PROMOTION_REFUSED_INSUFFICIENT},
            "route_recommendation": {"route_status": route_status},
        },
    }


def test_m47_operator_declared_shape_ok(tmp_path: Path) -> None:
    m46_dir = tmp_path / "m46only"
    emit_m46_fixture_ci(m46_dir)
    digest = json.loads((m46_dir / M46_FILENAME).read_text(encoding="utf-8"))["artifact_sha256"]
    inp = tmp_path / "in.json"
    inp.write_text(
        canonical_json_dumps(
            _example_declared_m47(m46_digest=str(digest), decision_status=STATUS_READOUT_COMPLETED)
        ),
        encoding="utf-8",
    )
    sealed, _ = emit_m47_operator_declared(tmp_path / "out", declared_surface_path=inp)
    assert sealed["design_status"] == STATUS_DESIGN_READY
    assert_all_false_m47_claim_bools(sealed)


@pytest.mark.smoke
def test_m47_governance_ledger_runtime_needles() -> None:
    repo = Path(__file__).resolve().parents[1]
    v15 = repo / "docs/starlab-v1.5.md"
    ledger = repo / "docs/starlab.md"
    rt = repo / "docs/runtime/v15_bounded_scorecard_result_surface_design_v1.md"
    if not (v15.is_file() and ledger.is_file() and rt.is_file()):
        pytest.skip("docs not present in test workspace")
    v15_txt = v15.read_text(encoding="utf-8")
    lc = ledger.read_text(encoding="utf-8")
    assert "V15-M47" in v15_txt and "V15-M47" in lc
    combined = (v15_txt + lc + rt.read_text(encoding="utf-8")).lower().replace("`", "")
    needles = (
        "v15_bounded_scorecard_result_surface_design_v1.md",
        "starlab.v15.bounded_scorecard_result_surface_design.v1",
        "starlab.v15.m47.bounded_scorecard_result_refusal_gate.v1",
        "bounded_scorecard_result_surface_design_ready",
        "bounded_scorecard_result_surface_design_refused",
        "scorecard_results_refused_not_produced",
        "benchmark_pass_fail_refused_not_produced",
        "promotion_refused_no_scorecard_results",
        "refused_m46_readout_not_completed",
        "refused_m46_scorecard_results_present",
        "refused_scorecard_results_claim",
        "scorecard_results_produced",
        "benchmark_passed",
        "scorecard_total_computed",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
        "false",
    )
    for needle in needles:
        assert needle in combined, f"missing governance needle {needle!r}"
