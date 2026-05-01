"""V15-M48 bounded scorecard execution preflight / evidence requirements gate tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m47_bounded_scorecard_result_surface_design_io import (
    emit_m47_fixture_ci,
    seal_m47_body,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    DIGEST_FIELD as M47_DIGEST_FIELD,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    FILENAME_MAIN_JSON as M47_FILENAME,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    STATUS_DESIGN_READY_WARNINGS as M47_DESIGN_READY_WARNINGS,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_io import (
    build_fixture_evidence_manifest,
    emit_m48_fixture_ci,
    emit_m48_forbidden_flag_refusal,
    emit_m48_operator_preflight,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    CLAIM_BENCHMARK_REFUSED,
    CONTRACT_ID_M48_PREFLIGHT,
    EVIDENCE_MANIFEST_CONTRACT_ID,
    FORBIDDEN_FLAG_AUTHORIZE_V2,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS,
    FORBIDDEN_FLAG_CLAIM_SCORECARD,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL,
    FORBIDDEN_FLAG_COMPUTE_WIN_RATE,
    FORBIDDEN_FLAG_EXECUTE_SCORECARD,
    FORBIDDEN_FLAG_EXECUTE_T5,
    FORBIDDEN_FLAG_LOAD_CHECKPOINT,
    FORBIDDEN_FLAG_PROMOTE_CHECKPOINT,
    FORBIDDEN_FLAG_RELEASE_SHOWCASE,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_RUN_LIVE_SC2,
    FORBIDDEN_FLAG_RUN_XAI,
    GATE_SATISFIED,
    PROFILE_M48_EVIDENCE_GATE,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_LIVE_SC2,
    REFUSED_M47_FUTURE_SURFACE_ALLOWED,
    REFUSED_M47_FUTURE_SURFACE_NOT_SEPARATE,
    REFUSED_M47_HONESTY,
    REFUSED_M47_NOT_READY,
    REFUSED_M47_ROUTE_EXECUTED,
    REFUSED_M47_SCORECARD_PRESENT,
    REFUSED_REQUIRED_EVIDENCE_INVALID,
    REFUSED_REQUIRED_EVIDENCE_MISSING,
    REFUSED_SCORECARD_RESULTS_CLAIM,
    REFUSED_SCORECARD_TOTAL_CLAIM,
    ROUTE_TO_SCORECARD_EXEC_SURFACE,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_PREFLIGHT_REFUSED,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    DIGEST_FIELD as M48_DIGEST_FIELD,
)


def _m48_honesty_false_keys() -> tuple[str, ...]:
    return (
        "scorecard_execution_performed",
        "scorecard_results_produced",
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_total_computed",
        "win_rate_computed",
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


def assert_all_false_m48_claim_blobs(blob: dict[str, object]) -> None:
    for k in _m48_honesty_false_keys():
        assert blob.get(k) is False, f"{k}"


def _valid_manifest() -> dict[str, object]:
    return dict(build_fixture_evidence_manifest())


def _reseal_m47(m47: dict[str, object]) -> dict[str, object]:
    m47.pop(M47_DIGEST_FIELD, None)
    return seal_m47_body(m47)


def test_m48_fixture_ci_deterministic_preflight(tmp_path: Path) -> None:
    outp = tmp_path / "fx"
    sealed, paths = emit_m48_fixture_ci(outp)
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_READY
    assert sealed["claim_decisions"]["benchmark_pass_fail"] == CLAIM_BENCHMARK_REFUSED
    erg = sealed["evidence_requirements_gate"]
    assert erg["gate_status"] == GATE_SATISFIED
    assert sealed["route_recommendation"]["next_route"] == ROUTE_TO_SCORECARD_EXEC_SURFACE
    assert sealed["route_recommendation"]["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED
    assert_all_false_m48_claim_blobs(sealed)
    assert len(paths) == 3


def test_m48_preflight_valid_m47_completed(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47_p = m47_dir / M47_FILENAME
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    out = tmp_path / "dec"
    sealed, _ = emit_m48_operator_preflight(out, m47_path=m47_p, manifest_path=manifest_p)
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_READY

    m47 = json.loads(m47_p.read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    m47["design_status"] = M47_DESIGN_READY_WARNINGS
    m47["warnings"] = ["synthetic_upstream_warning"]
    syn_path = tmp_path / "m47_syn.json"
    syn_path.write_text(canonical_json_dumps(seal_m47_body(m47)), encoding="utf-8")
    sealed2, _ = emit_m48_operator_preflight(out / "w", m47_path=syn_path, manifest_path=manifest_p)
    assert sealed2["preflight_status"] == STATUS_PREFLIGHT_READY_WARNINGS
    w = sealed2.get("warnings")
    assert isinstance(w, list) and len(w) >= 1


def test_m48_refuses_m47_not_ready(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    m47["design_status"] = "bounded_scorecard_result_surface_design_refused"
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_NOT_READY for r in sealed["refusals"])


def test_m48_refuses_m47_honesty_violation(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    m47["benchmark_passed"] = True
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_HONESTY for r in sealed["refusals"])


def test_m48_refuses_m47_route_executed(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    rr = dict(m47["route_recommendation"])
    rr["route_status"] = "executed_globally"
    m47["route_recommendation"] = rr
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_ROUTE_EXECUTED for r in sealed["refusals"])


def test_m48_refuses_m47_future_surface_allowed(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    sd = dict(m47["scorecard_surface_design"])
    sd["future_result_surface_allowed_in_m47"] = True
    m47["scorecard_surface_design"] = sd
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_FUTURE_SURFACE_ALLOWED for r in sealed["refusals"])


def test_m48_refuses_m47_future_surface_not_separate(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    sd = dict(m47["scorecard_surface_design"])
    sd["future_result_surface_requires_separate_milestone"] = False
    m47["scorecard_surface_design"] = sd
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_FUTURE_SURFACE_NOT_SEPARATE for r in sealed["refusals"])


def test_m48_refuses_m47_scorecard_results_present(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47 = json.loads((m47_dir / M47_FILENAME).read_text(encoding="utf-8"))
    m47.pop(M47_DIGEST_FIELD, None)
    m47["scorecard_results_produced"] = True
    p = tmp_path / "bad.json"
    p.write_text(canonical_json_dumps(_reseal_m47(m47)), encoding="utf-8")
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(_valid_manifest()), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_M47_SCORECARD_PRESENT for r in sealed["refusals"])


def test_m48_missing_evidence_manifest(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47_p = m47_dir / M47_FILENAME
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=m47_p,
        manifest_path=None,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_REQUIRED_EVIDENCE_MISSING for r in sealed["refusals"])


def test_m48_invalid_manifest_contract(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47_p = m47_dir / M47_FILENAME
    bad_man = _valid_manifest()
    bad_man["contract_id"] = "wrong.contract"
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(bad_man), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=m47_p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_REQUIRED_EVIDENCE_INVALID for r in sealed["refusals"])


def test_m48_manifest_forbidden_win_rate_key(tmp_path: Path) -> None:
    m47_dir = tmp_path / "m47"
    emit_m47_fixture_ci(m47_dir)
    m47_p = m47_dir / M47_FILENAME
    bad_man = _valid_manifest()
    bad_man["win_rate"] = 0.42
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text(canonical_json_dumps(bad_man), encoding="utf-8")
    sealed, _ = emit_m48_operator_preflight(
        tmp_path / "o",
        m47_path=m47_p,
        manifest_path=manifest_p,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_REFUSED
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m48_forbidden_execute_scorecard(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_EXECUTE_SCORECARD],
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m48_forbidden_scorecard_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_SCORECARD],
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed["refusals"])


def test_m48_forbidden_benchmark_flag(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_CLAIM_BENCHMARK_PASS],
    )
    assert any(r["code"] == REFUSED_BENCHMARK_PASS_CLAIM for r in sealed["refusals"])


def test_m48_forbidden_total_winrate(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_COMPUTE_SCORECARD_TOTAL],
    )
    assert any(r["code"] == REFUSED_SCORECARD_TOTAL_CLAIM for r in sealed["refusals"])
    sealed2, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o2",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_COMPUTE_WIN_RATE],
    )
    assert any(r["code"] == REFUSED_SCORECARD_RESULTS_CLAIM for r in sealed2["refusals"])


def test_m48_forbidden_strength_promote(tmp_path: Path) -> None:
    for flag, needle in (
        (FORBIDDEN_FLAG_CLAIM_STRENGTH, "refused_strength_claim"),
        (FORBIDDEN_FLAG_PROMOTE_CHECKPOINT, "refused_checkpoint_promotion_claim"),
    ):
        sealed, _ = emit_m48_forbidden_flag_refusal(
            tmp_path / f"x_{needle}",
            profile="fixture_ci",
            triggered_flags=[flag],
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m48_forbidden_load_live(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_LOAD_CHECKPOINT],
    )
    assert REFUSED_CHECKPOINT_LOAD in {r["code"] for r in sealed["refusals"]}
    sealed2, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o2",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_RUN_LIVE_SC2],
    )
    assert REFUSED_LIVE_SC2 in {r["code"] for r in sealed2["refusals"]}


def test_m48_forbidden_xai_human_showcase_v2(tmp_path: Path) -> None:
    for flags, needle in (
        ([FORBIDDEN_FLAG_RUN_XAI], "refused_xai_claim"),
        ([FORBIDDEN_FLAG_RUN_HUMAN_PANEL], "refused_human_panel_claim"),
        ([FORBIDDEN_FLAG_RELEASE_SHOWCASE], "refused_showcase_release_claim"),
        ([FORBIDDEN_FLAG_AUTHORIZE_V2], "refused_v2_authorization_claim"),
    ):
        sealed, _ = emit_m48_forbidden_flag_refusal(
            tmp_path / f"n_{needle}",
            profile="fixture_ci",
            triggered_flags=flags,
        )
        assert needle in {r["code"] for r in sealed["refusals"]}


def test_m48_forbidden_t5(tmp_path: Path) -> None:
    sealed, _ = emit_m48_forbidden_flag_refusal(
        tmp_path / "o",
        profile="fixture_ci",
        triggered_flags=[FORBIDDEN_FLAG_EXECUTE_T5],
    )
    assert "refused_t2_t5_execution_claim" in {r["code"] for r in sealed["refusals"]}


def test_m48_no_torch_load_in_io_cli() -> None:
    from starlab.v15 import emit_v15_m48_bounded_scorecard_execution_preflight as cli_mod
    from starlab.v15 import m48_bounded_scorecard_execution_preflight_io as io_mod

    for mod in (io_mod, cli_mod):
        mf = mod.__file__
        assert mf is not None
        src = Path(mf).read_text(encoding="utf-8")
        assert "torch.load(" not in src
        assert "import torch" not in src


def test_m48_no_checkpoint_blob_reads_in_io() -> None:
    from starlab.v15 import m48_bounded_scorecard_execution_preflight_io as io_mod

    mf = io_mod.__file__
    assert mf is not None
    src = Path(mf).read_text(encoding="utf-8")
    assert ".pt" not in src
    assert ".pth" not in src
    assert "read_bytes" not in src


def test_m48_fixture_deterministic_digest(tmp_path: Path) -> None:
    a, _ = emit_m48_fixture_ci(tmp_path / "o1")
    b, _ = emit_m48_fixture_ci(tmp_path / "o2")
    assert a[M48_DIGEST_FIELD] == b[M48_DIGEST_FIELD]


def test_m48_brief_has_required_footer(tmp_path: Path) -> None:
    emit_m48_fixture_ci(tmp_path / "o")
    brief = (tmp_path / "o" / "v15_bounded_scorecard_execution_preflight_brief.md").read_text(
        encoding="utf-8",
    )
    needle_title = (
        "This brief is a bounded scorecard execution preflight and evidence requirements gate."
    )
    assert needle_title in brief
    assert "not scorecard execution, scorecard results, benchmark pass/fail evidence" in brief


def test_m48_governance_ledger_runtime_needles() -> None:
    repo = Path(__file__).resolve().parents[1]
    v15 = repo / "docs/starlab-v1.5.md"
    ledger = repo / "docs/starlab.md"
    rt = repo / "docs/runtime/v15_bounded_scorecard_execution_preflight_v1.md"
    if not (v15.is_file() and ledger.is_file() and rt.is_file()):
        pytest.skip("docs not present in test workspace")
    v15_txt = v15.read_text(encoding="utf-8")
    lc = ledger.read_text(encoding="utf-8")
    assert "V15-M48" in v15_txt and "V15-M48" in lc
    combined = (v15_txt + lc + rt.read_text(encoding="utf-8")).lower().replace("`", "")
    needles = (
        "v15_bounded_scorecard_execution_preflight_v1.md",
        "starlab.v15.bounded_scorecard_execution_preflight.v1",
        "starlab.v15.m48.bounded_scorecard_execution_preflight_evidence_requirements_gate.v1",
        "bounded_scorecard_execution_preflight_ready",
        "bounded_scorecard_execution_preflight_refused",
        "evidence_requirements_satisfied_for_future_preflight",
        "scorecard_results_refused_not_executed",
        "benchmark_pass_fail_refused_not_executed",
        "promotion_refused_no_scorecard_execution",
        "refused_m47_design_not_ready",
        "refused_m47_future_surface_allowed",
        "refused_required_evidence_missing",
        "refused_scorecard_total_claim",
        "scorecard_execution_performed",
        "scorecard_results_produced",
        "benchmark_passed",
        "scorecard_total_computed",
        "win_rate_computed",
        "strength_evaluated",
        "checkpoint_promoted",
        "torch_load_invoked",
        "checkpoint_blob_loaded",
        "live_sc2_executed",
        "false",
    )
    for needle in needles:
        assert needle in combined, f"missing governance needle {needle!r}"


def test_m48_cli_fixture_ci(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m48_bounded_scorecard_execution_preflight",
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
    assert (out / "v15_bounded_scorecard_execution_preflight.json").is_file()


def test_m48_cli_operator_preflight_requires_m47_path(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest_p = tmp_path / "manifest.json"
    manifest_p.write_text('{"contract_id":"x"}', encoding="utf-8")
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m48_bounded_scorecard_execution_preflight",
            "--profile",
            "operator_preflight",
            "--output-dir",
            str(out),
            "--evidence-manifest-json",
            str(manifest_p),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode != 0
    combined = (res.stderr or "") + (res.stdout or "")
    assert "--m47-surface-design-json is required for operator_preflight" in combined


def test_m48_manifest_contract_constant_matches_fixture(tmp_path: Path) -> None:
    man = build_fixture_evidence_manifest()
    assert man["contract_id"] == EVIDENCE_MANIFEST_CONTRACT_ID
    fx = tmp_path / "fx"
    sealed, _ = emit_m48_fixture_ci(fx)
    assert sealed["contract_id"] == CONTRACT_ID_M48_PREFLIGHT
    assert sealed["profile_id"] == PROFILE_M48_EVIDENCE_GATE
