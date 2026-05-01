"""V15-M50 scorecard result readout / benchmark pass-fail refusal decision tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m49_bounded_scorecard_result_execution_io import (
    emit_m49_fixture_ci,
    seal_m49_body,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    CONTRACT_ID_M49_RESULT,
    PROFILE_M49_SURFACE,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    FILENAME_MAIN_JSON as M49_FILENAME,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    STATUS_RESULT_COMPLETED as M49_STATUS_COMPLETED,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    STATUS_RESULT_REFUSED as M49_REFUSED,
)
from starlab.v15.m50_scorecard_result_readout_decision_io import (
    decide_m50_from_m49,
    emit_m50_fixture_ci,
    emit_m50_forbidden_flag_refusal,
    emit_m50_operator_declared,
    emit_m50_operator_preflight,
    structural_m49_issues_for_m50,
)
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY,
    BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD,
    CONTRACT_ID_M50_READOUT,
    PROFILE_M50_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROMOTION_REFUSED_M50_READOUT_ONLY,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_DECLARED_SHAPE,
    REFUSED_M49_CONTRACT_INVALID,
    REFUSED_M49_RESULT_REFUSED,
    REFUSED_M49_SHA_MISMATCH,
    REFUSED_MISSING_M49,
    REFUSED_MISSING_SCORECARD_FIELDS,
    REFUSED_UPSTREAM_HONESTY,
    ROUTE_TO_M51_WATCHABILITY,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_WARNINGS,
    STATUS_READOUT_REFUSED,
)

DIGEST = "artifact_sha256"


def _m50_false_claim_keys() -> tuple[str, ...]:
    return (
        "benchmark_passed",
        "benchmark_failed",
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


def assert_m50_honesty_false(blob: dict[str, object]) -> None:
    for k in _m50_false_claim_keys():
        assert blob.get(k) is False, k


def test_m50_fixture_ci(tmp_path: Path) -> None:
    sealed, paths = emit_m50_fixture_ci(tmp_path / "fx")
    assert sealed["readout_status"] == STATUS_READOUT_COMPLETED
    assert sealed["contract_id"] == CONTRACT_ID_M50_READOUT
    assert sealed["profile_id"] == PROFILE_M50_SURFACE
    assert (
        sealed["benchmark_pass_fail_decision"]["decision"]
        == BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY
    )
    assert sealed["promotion_decision"]["decision"] == PROMOTION_REFUSED_M50_READOUT_ONLY
    assert sealed["route_recommendation"]["next_route"] == ROUTE_TO_M51_WATCHABILITY
    assert_m50_honesty_false(sealed)
    assert len(paths) == 3


def _emit_sealed_m49(tmp_path: Path) -> Path:
    sub = tmp_path / "m49"
    emit_m49_fixture_ci(sub)
    return sub / M49_FILENAME


def test_m50_preflight_accepts_valid_m49(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    sealed, _ = emit_m50_operator_preflight(
        tmp_path / "out",
        m49_path=m49_p,
        expected_sha256_lower=None,
    )
    assert sealed["readout_status"] == STATUS_READOUT_COMPLETED
    assert sealed["scorecard_readout"]["scorecard_results_seen"] is True


def test_m50_preflight_expected_sha_match(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    digest = str(m49[DIGEST]).lower()
    sealed, _ = emit_m50_operator_preflight(
        tmp_path / "out",
        m49_path=m49_p,
        expected_sha256_lower=digest,
    )
    assert sealed["readout_status"] == STATUS_READOUT_COMPLETED


def test_m50_preflight_expected_sha_mismatch_refuses(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    sealed, _ = emit_m50_operator_preflight(
        tmp_path / "out",
        m49_path=m49_p,
        expected_sha256_lower="a" * 64,
    )
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M49_SHA_MISMATCH for r in sealed["refusals"])


def test_m50_preflight_m49_refused_upstream(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49.pop(DIGEST, None)
    m49["result_status"] = M49_REFUSED
    m49["refusals"] = [{"code": "synthetic", "detail": "x"}]
    bad_p = tmp_path / "m49r.json"
    bad_p.write_text(canonical_json_dumps(seal_m49_body(m49)), encoding="utf-8")
    sealed, _ = emit_m50_operator_preflight(
        tmp_path / "out",
        m49_path=bad_p,
        expected_sha256_lower=None,
    )
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M49_RESULT_REFUSED for r in sealed["refusals"])


def test_m50_invalid_contract_refuses(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49.pop(DIGEST, None)
    m49["contract_id"] = "wrong.contract"
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m49_body(m49)), encoding="utf-8")
    sealed, _ = emit_m50_operator_preflight(tmp_path / "o", m49_path=p, expected_sha256_lower=None)
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_M49_CONTRACT_INVALID for r in sealed["refusals"])


def test_m50_upstream_benchmark_pass_overclaim(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49.pop(DIGEST, None)
    m49["benchmark_passed"] = True
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m49_body(m49)), encoding="utf-8")
    sealed, _ = emit_m50_operator_preflight(tmp_path / "o", m49_path=p, expected_sha256_lower=None)
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_UPSTREAM_HONESTY for r in sealed["refusals"])


def test_m50_missing_scorecard_block_refuses(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49.pop(DIGEST, None)
    del m49["scorecard_result"]
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m49_body(m49)), encoding="utf-8")
    sealed, _ = emit_m50_operator_preflight(tmp_path / "o", m49_path=p, expected_sha256_lower=None)
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_MISSING_SCORECARD_FIELDS for r in sealed["refusals"])


def test_m50_invalid_metrics_warns_not_pass_fail(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49.pop(DIGEST, None)
    scr = dict(m49["scorecard_result"])
    scr["win_rate"] = 2.0
    m49["scorecard_result"] = scr
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(seal_m49_body(m49)), encoding="utf-8")
    sealed, _ = emit_m50_operator_preflight(tmp_path / "o", m49_path=p, expected_sha256_lower=None)
    assert sealed["readout_status"] == STATUS_READOUT_COMPLETED_WARNINGS
    assert (
        sealed["benchmark_pass_fail_decision"]["decision"]
        == BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD
    )
    assert sealed["benchmark_pass_fail_decision"]["reason"]
    assert_m50_honesty_false(sealed)


def test_decide_missing_m49_file(tmp_path: Path) -> None:
    d = decide_m50_from_m49(None, expected_sha256_lower=None, require_canonical_seal=True)
    assert d.readout_status == STATUS_READOUT_REFUSED
    assert d.refusals[0]["code"] == REFUSED_MISSING_M49


def test_structural_bad_seal(tmp_path: Path) -> None:
    m49_p = _emit_sealed_m49(tmp_path)
    m49 = json.loads(m49_p.read_text(encoding="utf-8"))
    m49["artifact_sha256"] = "b" * 64
    errs = structural_m49_issues_for_m50(m49, require_canonical_seal=True)
    assert "m49_seal_invalid" in errs


def test_m50_forbidden_flags(tmp_path: Path) -> None:
    sealed, _ = emit_m50_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=["--claim-benchmark-pass"],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_PASS_CLAIM for r in sealed["refusals"])


def test_m50_forbidden_promote(tmp_path: Path) -> None:
    sealed, _ = emit_m50_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=["--promote-checkpoint"],
    )
    assert "refused_promotion_claim" in {r["code"] for r in sealed["refusals"]}


def _sha64(c: str = "c") -> str:
    return (c * 64).lower()


def _minimal_declared_m50() -> dict[str, object]:
    h = _sha64()
    return {
        "contract_id": CONTRACT_ID_M50_READOUT,
        "profile_id": PROFILE_M50_SURFACE,
        "m49_binding": {
            "contract_id": CONTRACT_ID_M49_RESULT,
            "profile_id": PROFILE_M49_SURFACE,
            "artifact_sha256": h,
            "status": M49_STATUS_COMPLETED,
        },
        "declared_m49_execution_summary": {
            "result_status": M49_STATUS_COMPLETED,
            "scorecard_results_produced": True,
            "scorecard_total_computed": True,
            "win_rate_computed": True,
            "scorecard_result": {
                "scorecard_total": 0.25,
                "win_rate": 0.5,
                "episode_count": 2,
                "valid_episode_count": 1,
            },
            "warnings": [],
        },
    }


def test_m50_operator_declared_ok(tmp_path: Path) -> None:
    p = tmp_path / "d.json"
    p.write_text(canonical_json_dumps(_minimal_declared_m50()), encoding="utf-8")
    sealed, _paths = emit_m50_operator_declared(tmp_path / "out", declared_readout_path=p)
    assert sealed["readout_status"] == STATUS_READOUT_COMPLETED
    assert sealed["profile"] == PROFILE_OPERATOR_DECLARED


def test_m50_operator_declared_overclaim_benchmark(tmp_path: Path) -> None:
    blob = _minimal_declared_m50()
    blob["benchmark_passed"] = True
    p = tmp_path / "d.json"
    p.write_text(canonical_json_dumps(blob), encoding="utf-8")
    sealed, _ = emit_m50_operator_declared(tmp_path / "out", declared_readout_path=p)
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED
    assert any(r["code"] == REFUSED_DECLARED_SHAPE for r in sealed["refusals"])


def test_m50_operator_declared_contract_bad(tmp_path: Path) -> None:
    blob = _minimal_declared_m50()
    blob["contract_id"] = "wrong"
    p = tmp_path / "d.json"
    p.write_text(canonical_json_dumps(blob), encoding="utf-8")
    sealed, _ = emit_m50_operator_declared(tmp_path / "out", declared_readout_path=p)
    assert sealed["readout_status"] == STATUS_READOUT_REFUSED


def test_m50_cli_fixture(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m50_scorecard_result_readout_decision",
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    assert (out / "v15_scorecard_result_readout_decision.json").is_file()
    assert (out / "v15_scorecard_result_readout_decision_brief.md").is_file()


def test_m50_cli_preflight_requires_m49(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m50_scorecard_result_readout_decision",
            "--profile",
            "operator_preflight",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert res.returncode != 0
    comb = (res.stderr or "") + (res.stdout or "")
    assert "--m49-scorecard-result-json is required" in comb


def test_m50_cli_preflight_sha_mismatch_exits_zero(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    m49_p = _emit_sealed_m49(tmp_path)
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m50_scorecard_result_readout_decision",
            "--profile",
            "operator_preflight",
            "--output-dir",
            str(out),
            "--m49-scorecard-result-json",
            str(m49_p),
            "--expected-m49-scorecard-result-sha256",
            "f" * 64,
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    main_json = out / "v15_scorecard_result_readout_decision.json"
    blob = json.loads(main_json.read_text(encoding="utf-8"))
    assert blob["readout_status"] == STATUS_READOUT_REFUSED


def test_m50_no_torch_in_modules() -> None:
    from starlab.v15 import emit_v15_m50_scorecard_result_readout_decision as cli_mod
    from starlab.v15 import m50_scorecard_result_readout_decision_io as io_mod

    for mod in (io_mod, cli_mod):
        mf = mod.__file__
        assert mf is not None
        src = Path(mf).read_text(encoding="utf-8")
        assert "torch.load(" not in src
        assert "import torch" not in src


def test_m50_fixture_digest_stable(tmp_path: Path) -> None:
    a, _ = emit_m50_fixture_ci(tmp_path / "a")
    b, _ = emit_m50_fixture_ci(tmp_path / "b")
    assert a[DIGEST] == b[DIGEST]


def test_m50_governance_ledger_runtime_needles() -> None:
    repo = Path(__file__).resolve().parents[1]
    v15 = repo / "docs/starlab-v1.5.md"
    ledger = repo / "docs/starlab.md"
    rt = repo / "docs/runtime/v15_scorecard_result_readout_decision_v1.md"
    if not (v15.is_file() and ledger.is_file() and rt.is_file()):
        pytest.skip("docs not present")
    v15_txt = v15.read_text(encoding="utf-8")
    lc = ledger.read_text(encoding="utf-8")
    assert "V15-M50" in v15_txt and "V15-M50" in lc
    combined = (v15_txt + lc + rt.read_text(encoding="utf-8")).lower().replace("`", "")
    needles = (
        "v15_scorecard_result_readout_decision_v1.md",
        "starlab.v15.scorecard_result_readout_decision.v1",
        "starlab.v15.m50.scorecard_result_readout_benchmark_pass_fail_refusal.v1",
        "scorecard_result_readout_completed",
        "scorecard_result_readout_refused",
        "benchmark_pass_fail_refused_m49_bounded_only",
        "promotion_refused_m50_readout_only",
        "refused_m49_sha_mismatch",
        "refused_m49_result_refused",
        "route_to_live_candidate_watchability_harness",
        "recommended_not_executed",
        "benchmark_passed",
        "false",
    )
    for needle in needles:
        assert needle in combined, f"missing governance needle {needle!r}"
