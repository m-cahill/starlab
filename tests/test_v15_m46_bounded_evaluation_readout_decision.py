"""V15-M46 bounded evaluation readout / promotion refusal decision tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m45_bounded_candidate_evaluation_execution_io import (
    emit_m45_fixture_ci,
    seal_m45_body,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_models import (
    DIGEST_FIELD as M45_DIGEST_FIELD,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_models import (
    FILENAME_MAIN_JSON as M45_FILENAME,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_io import (
    emit_m46_fixture_ci,
    emit_m46_forbidden_flag_refusal,
    emit_m46_operator_declared,
    emit_m46_operator_preflight,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    CLAIM_BENCHMARK_REFUSED,
    CONTRACT_ID_M45_EXECUTION,
    CONTRACT_ID_M46_READOUT,
    FORBIDDEN_FLAG_AUTHORIZE_V2,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_EXECUTE_T5,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_PRODUCE_SCORECARD,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    M45_STATUS_COMPLETED_SYNTHETIC,
    M45_STATUS_NOT_READY,
    M45_STATUS_SURFACE_READY,
    PROFILE_M46_READOUT,
    PROMOTION_REFUSED_INSUFFICIENT,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_LIVE_SC2,
    REFUSED_M45_HONESTY,
    REFUSED_M45_NOT_READY,
    REFUSED_M45_SYNTHETIC_OVERINTERPRET,
    REFUSED_PROMOTION_CLAIM,
    REFUSED_SCORECARD_RESULTS_CLAIM,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_BENCHMARK_DESIGN,
    ROUTE_TO_M45_REMEDIATION,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_SYNTH_WARNING,
    STATUS_READOUT_REFUSED,
)


def _honesty_false_keys() -> tuple[str, ...]:
    return (
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
    )


def assert_all_false_claim_bools(blob: dict[str, object]) -> None:
    for k in _honesty_false_keys():
        assert blob.get(k) is False, f"{k}"


def test_m46_fixture_ci_deterministic_readout(tmp_path: Path) -> None:
    outp = tmp_path / "fx"
    sealed, paths = emit_m46_fixture_ci(outp)
    assert sealed["decision_status"] == STATUS_READOUT_COMPLETED
    assert sealed["claim_decisions"]["benchmark_pass_fail"] == CLAIM_BENCHMARK_REFUSED
    assert sealed["route_recommendation"]["next_route"] == ROUTE_TO_BENCHMARK_DESIGN
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert_all_false_claim_bools(sealed)
    assert sealed["promotion_decision"]["promotion_status"] == PROMOTION_REFUSED_INSUFFICIENT
    assert len(paths) == 3


def test_m46_operator_preflight_surface_ready(tmp_path: Path) -> None:
    m45_dir = tmp_path / "m45"
    emit_m45_fixture_ci(m45_dir)
    m45_p = m45_dir / M45_FILENAME
    out = tmp_path / "dec"
    sealed, _ = emit_m46_operator_preflight(out, m45_path=m45_p)
    assert sealed["decision_status"] == STATUS_READOUT_COMPLETED
    assert sealed["promotion_decision"]["promotion_status"] == PROMOTION_REFUSED_INSUFFICIENT
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def test_m46_operator_preflight_synthetic_completed(tmp_path: Path) -> None:
    m45_dir = tmp_path / "bx"
    emit_m45_fixture_ci(m45_dir)
    m45_p = m45_dir / M45_FILENAME
    m45 = json.loads(m45_p.read_text(encoding="utf-8"))
    m45.pop(M45_DIGEST_FIELD, None)
    m45["execution_status"] = M45_STATUS_COMPLETED_SYNTHETIC
    m45["synthetic_execution_receipt_emitted"] = True
    m45["bounded_execution_surface_invoked"] = True
    rec = dict(m45["execution_receipt"])
    rec["receipt_status"] = "synthetic_execution_receipt_emitted"
    rec["benchmark_mode"] = "none"
    rec["scorecard_mode"] = "none"
    m45["execution_receipt"] = rec
    wo = {k: v for k, v in m45.items() if k != M45_DIGEST_FIELD}
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    m45[M45_DIGEST_FIELD] = sha256_hex_of_canonical_json(wo)
    synth_path = tmp_path / "m45_syn.json"
    synth_path.write_text(canonical_json_dumps(m45), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m46_operator_preflight(out, m45_path=synth_path)
    assert sealed["decision_status"] == STATUS_READOUT_COMPLETED_SYNTH_WARNING
    assert synthetic_warning_any(sealed)


def synthetic_warning_any(sealed: dict[str, object]) -> bool:
    w = sealed.get("warnings")
    rs = sealed.get("route_recommendation")
    rsw = rs.get("route_warnings") if isinstance(rs, dict) else None
    if isinstance(w, list) and len(w) > 0:
        return True
    if isinstance(rsw, list) and len(rsw) > 0:
        return True
    return False


def test_m46_refuses_not_ready_m45(tmp_path: Path) -> None:
    m45_dir = tmp_path / "m45"
    emit_m45_fixture_ci(m45_dir)
    m45_p = m45_dir / M45_FILENAME
    m45 = json.loads(m45_p.read_text(encoding="utf-8"))
    m45.pop(M45_DIGEST_FIELD, None)
    m45["execution_status"] = M45_STATUS_NOT_READY
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    wo = {k: v for k, v in m45.items() if k != M45_DIGEST_FIELD}
    m45[M45_DIGEST_FIELD] = sha256_hex_of_canonical_json(wo)
    bad_path = tmp_path / "nr.json"
    bad_path.write_text(canonical_json_dumps(m45), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m46_operator_preflight(out, m45_path=bad_path)
    assert sealed["decision_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M45_NOT_READY for r in sealed["refusals"])
    assert sealed["route_recommendation"]["next_route"] == ROUTE_TO_M45_REMEDIATION


def test_m46_refuses_m45_honesty_violation(tmp_path: Path) -> None:
    m45_dir = tmp_path / "m45"
    emit_m45_fixture_ci(m45_dir)
    m45_p = m45_dir / M45_FILENAME
    m45 = json.loads(m45_p.read_text(encoding="utf-8"))
    m45.pop(M45_DIGEST_FIELD, None)
    m45["benchmark_passed"] = True
    from starlab.runs.json_util import sha256_hex_of_canonical_json

    wo = {k: v for k, v in m45.items() if k != M45_DIGEST_FIELD}
    m45[M45_DIGEST_FIELD] = sha256_hex_of_canonical_json(wo)
    bad_path = tmp_path / "hon.json"
    bad_path.write_text(canonical_json_dumps(m45), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m46_operator_preflight(out, m45_path=bad_path)
    assert sealed["decision_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M45_HONESTY for r in sealed["refusals"])


def test_m46_refuses_synthetic_receipt_overinterpreted(tmp_path: Path) -> None:
    sub = tmp_path / "m45_sub"
    emit_m45_fixture_ci(sub)
    m45_path = sub / M45_FILENAME
    m45 = json.loads(m45_path.read_text(encoding="utf-8"))
    m45.pop(M45_DIGEST_FIELD, None)
    m45["execution_status"] = M45_STATUS_COMPLETED_SYNTHETIC
    m45["synthetic_execution_receipt_emitted"] = True
    m45["bounded_execution_surface_invoked"] = True
    rec = dict(m45["execution_receipt"])
    rec["benchmark_mode"] = "not_none_overclaim"
    m45["execution_receipt"] = rec
    m45_sealed = seal_m45_body(m45)
    bad_path = tmp_path / "ov.json"
    bad_path.write_text(canonical_json_dumps(m45_sealed), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m46_operator_preflight(out, m45_path=bad_path)
    assert sealed["decision_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M45_SYNTHETIC_OVERINTERPRET for r in sealed["refusals"])


def test_m46_flag_benchmark_pass_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS]
    )
    assert sealed["decision_status"] == STATUS_READOUT_REFUSED
    assert REFUSED_BENCHMARK_PASS_CLAIM in {r["code"] for r in sealed["refusals"]}


def test_m46_flag_scorecard_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_PRODUCE_SCORECARD]
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m46_flag_strength_claim_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_CLAIM_STRENGTH]
    )
    assert any("refused_strength_claim" == r["code"] for r in sealed["refusals"])


def test_m46_flag_promote_checkpoint_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_PROMOTE_CHECKPOINT]
    )
    assert any(r["code"] == REFUSED_PROMOTION_CLAIM for r in sealed["refusals"])


def test_m46_flag_load_checkpoint_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_LOAD_CHECKPOINT]
    )
    assert any(r["code"] == REFUSED_CHECKPOINT_LOAD for r in sealed["refusals"])


def test_m46_flag_live_sc2_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_RUN_LIVE_SC2]
    )
    assert any(r["code"] == REFUSED_LIVE_SC2 for r in sealed["refusals"])


def test_m46_flags_xai_human_showcase_v2(tmp_path: Path) -> None:
    for flags, needle in (
        ([FORBIDDEN_FLAG_RUN_XAI], "refused_xai_claim"),
        ([FORBIDDEN_FLAG_RUN_HUMAN_PANEL], "refused_human_panel_claim"),
        ([FORBIDDEN_FLAG_RELEASE_SHOWCASE], "refused_showcase_release_claim"),
        ([FORBIDDEN_FLAG_AUTHORIZE_V2], "refused_v2_authorization_claim"),
    ):
        out = tmp_path / f"n_{needle}"
        sealed, _ = emit_m46_forbidden_flag_refusal(
            out, profile="fixture_ci", triggered_flags=flags
        )
        codes = {r["code"] for r in sealed["refusals"]}
        assert needle in codes


def test_m46_flags_t5_refuses(tmp_path: Path) -> None:
    out = tmp_path / "o"
    sealed, _ = emit_m46_forbidden_flag_refusal(
        out, profile="fixture_ci", triggered_flags=[FORBIDDEN_FLAG_EXECUTE_T5]
    )
    codes = {r["code"] for r in sealed["refusals"]}
    assert "refused_t2_t5_execution_claim" in codes


def test_m46_no_torch_load_in_io_cli() -> None:
    from starlab.v15 import emit_v15_m46_bounded_evaluation_readout_decision as cli_mod
    from starlab.v15 import m46_bounded_evaluation_readout_decision_io as io_mod

    for mod in (io_mod, cli_mod):
        mod_file = mod.__file__
        assert mod_file is not None
        src = Path(mod_file).read_text(encoding="utf-8")
        assert "torch.load(" not in src
        assert "import torch" not in src


def test_m46_no_checkpoint_blob_reads_in_io() -> None:
    from starlab.v15 import m46_bounded_evaluation_readout_decision_io as io_mod

    io_file = io_mod.__file__
    assert io_file is not None
    src = Path(io_file).read_text(encoding="utf-8")
    assert ".pt" not in src
    assert ".pth" not in src
    assert "read_bytes" not in src


def test_m46_fixture_deterministic_digest(tmp_path: Path) -> None:
    sealed1, _ = emit_m46_fixture_ci(tmp_path / "o1")
    sealed2, _ = emit_m46_fixture_ci(tmp_path / "o2")
    assert sealed1["artifact_sha256"] == sealed2["artifact_sha256"]


def test_m46_brief_has_required_footer(tmp_path: Path) -> None:
    emit_m46_fixture_ci(tmp_path / "o")
    brief = (tmp_path / "o" / "v15_bounded_evaluation_readout_decision_brief.md").read_text(
        encoding="utf-8",
    )
    assert "This brief is a readout/refusal decision over bounded execution bookkeeping." in brief
    assert (
        "not benchmark pass/fail evidence, scorecard results, strength evaluation" in brief.lower()
        or "not benchmark pass/fail evidence" in brief
    )


@pytest.mark.smoke
def test_m46_governance_ledger_runtime_needles() -> None:
    repo = Path(__file__).resolve().parents[1]
    v15 = repo / "docs/starlab-v1.5.md"
    ledger = repo / "docs/starlab.md"
    rt = repo / "docs/runtime/v15_bounded_evaluation_readout_decision_v1.md"
    if not (v15.is_file() and ledger.is_file() and rt.is_file()):
        pytest.skip("docs not present in test workspace")
    v15_txt = v15.read_text(encoding="utf-8")
    lc = ledger.read_text(encoding="utf-8")
    assert "V15-M46" in v15_txt and ("V15-M46" in lc or "**`V15-M46`**" in lc)
    combined_needles = (v15_txt + lc + rt.read_text(encoding="utf-8")).lower().replace("`", "")
    needles = (
        "v15_bounded_evaluation_readout_decision_v1.md",
        "starlab.v15.bounded_evaluation_readout_decision.v1",
        "starlab.v15.m46.bounded_evaluation_readout_promotion_refusal.v1",
        "bounded_evaluation_readout_completed",
        "bounded_evaluation_readout_completed_with_synthetic_only_warning",
        "promotion_refused_insufficient_evidence",
        "refused_m45_execution_not_ready",
        "refused_m45_synthetic_receipt_overinterpreted",
        "refused_benchmark_pass_claim",
        "refused_scorecard_results_claim",
        "torch.load",
        "benchmark_passed",
        "scorecard_results_produced",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
        "false",
    )
    for needle in needles:
        assert needle in combined_needles, f"missing governance needle {needle!r}"


def test_m46_cli_fixture_ci(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m46_bounded_evaluation_readout_decision",
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
    assert (out / "v15_bounded_evaluation_readout_decision.json").is_file()


def _example_declared(m45_digest: str, execution_status: str) -> dict[str, object]:
    return {
        "contract_id": CONTRACT_ID_M46_READOUT,
        "profile_id": PROFILE_M46_READOUT,
        "m45_binding": {
            "contract_id": CONTRACT_ID_M45_EXECUTION,
            "artifact_sha256": m45_digest,
            "execution_status": execution_status,
            "interpretation": "bounded_execution_bookkeeping_only_not_benchmark_success",
        },
    }


def test_m46_operator_declared_shape_ok(tmp_path: Path) -> None:
    outp = tmp_path / "decl"
    outp.mkdir(parents=True, exist_ok=True)
    m45_dir = tmp_path / "m45only"
    emit_m45_fixture_ci(m45_dir)
    m45_digest = json.loads((m45_dir / M45_FILENAME).read_text(encoding="utf-8"))["artifact_sha256"]
    dpath = outp / "in.json"
    dec = _example_declared(str(m45_digest), M45_STATUS_SURFACE_READY)
    dpath.write_text(canonical_json_dumps(dec), encoding="utf-8")
    out = tmp_path / "dec_dir"
    sealed, _ = emit_m46_operator_declared(out, declared_readout_path=dpath)
    assert sealed["decision_status"] == STATUS_READOUT_COMPLETED
    assert_all_false_claim_bools(sealed)


def test_m46_flag_interpret_synthetic_cli_refuses(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m46_bounded_evaluation_readout_decision",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
            "--interpret-m45-synthetic-as-benchmark-success",
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    sealed = json.loads(
        (out / "v15_bounded_evaluation_readout_decision.json").read_text(encoding="utf-8")
    )
    assert sealed["decision_status"] == STATUS_READOUT_REFUSED
    codes = {r["code"] for r in sealed["refusals"]}
    assert REFUSED_M45_SYNTHETIC_OVERINTERPRET in codes
