"""V15-M44 bounded evaluation execution preflight tests (dry-run only)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m43_bounded_evaluation_gate_io import (
    FILENAME_FIXTURE_ENV,
    FILENAME_FIXTURE_PROTOCOL,
    seal_m43_body,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M43_DIGEST,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    STATUS_GATE_NOT_READY,
    STATUS_GATE_READY_WITH_WARNINGS,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_io import (
    emit_m44_fixture_ci,
    emit_m44_operator,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
    PLAN_ID_EXPECTED,
    PLAN_STATUS_CONSTRUCTED,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_DISALLOWED_EXECUTION,
    REFUSED_DRY_RUN_PLAN_MISSING,
    REFUSED_ENV_MANIFEST_MISSING,
    REFUSED_LIVE_SC2,
    REFUSED_M43_GATE_NOT_READY,
    REFUSED_M43_HONESTY_VIOLATION,
    STATUS_PREFLIGHT_NOT_READY,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
)


def _upstream_dir(tmp_path: Path) -> Path:
    from starlab.v15.m43_bounded_evaluation_gate_io import emit_m43_fixture

    u = tmp_path / "m43_fixture"
    emit_m43_fixture(u)
    return u


def test_m44_fixture_ready_path(tmp_path: Path) -> None:
    out = tmp_path / "fx"
    sealed, paths = emit_m44_fixture_ci(out)
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_READY
    for k in (
        "benchmark_execution_performed",
        "evaluation_execution_performed",
        "scorecard_results_produced",
        "checkpoint_loaded",
        "checkpoint_promoted",
        "torch_load_invoked",
        "live_sc2_executed",
    ):
        assert sealed[k] is False
    assert sealed["dry_run_plan"]["plan_status"] == PLAN_STATUS_CONSTRUCTED
    assert sealed["dry_run_plan"]["planned_ladder_stage"] == "future_bounded_candidate_evaluation"
    assert sealed["non_claims"]
    interp = sealed["m43_status_interpretation"]
    assert interp["interpretation"] == "routing_eligibility_only"
    assert len(paths) == 3


def test_m44_operator_preflight_valid_m43(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate = u / "v15_bounded_evaluation_gate.json"
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    dry = tmp_path / "dry_run.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    outp = tmp_path / "out"
    sealed, _ = emit_m44_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m43_gate_path=gate,
        dry_run_plan_path=dry,
        evaluation_environment_path=envp,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_READY
    assert sealed["dry_run_plan"]["plan_status"] == PLAN_STATUS_CONSTRUCTED


def _mutate_gate_file(gate_fp: Path, dest: Path, **updates: Any) -> None:
    plain = json.loads(gate_fp.read_text(encoding="utf-8"))
    body = {k: v for k, v in plain.items() if k != M43_DIGEST}
    body.update(updates)
    dest.write_text(canonical_json_dumps(seal_m43_body(body)), encoding="utf-8")


def test_m44_m43_gate_not_ready(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate_bad = tmp_path / "gate_nr.json"
    _mutate_gate_file(
        u / "v15_bounded_evaluation_gate.json", gate_bad, gate_status=STATUS_GATE_NOT_READY
    )
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    dry = tmp_path / "dry.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    sealed, _ = emit_m44_operator(
        tmp_path / "out1",
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m43_gate_path=gate_bad,
        dry_run_plan_path=dry,
        evaluation_environment_path=envp,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_NOT_READY
    assert REFUSED_M43_GATE_NOT_READY in {r["code"] for r in sealed["refusals"]}


def test_m44_m43_honesty_violation(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate_bad = tmp_path / "gate_bad.json"
    _mutate_gate_file(
        u / "v15_bounded_evaluation_gate.json",
        gate_bad,
        evaluation_executed=True,
        checkpoint_loaded=False,
        promotion_decision_made=False,
    )
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    dry = tmp_path / "dry.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    sealed, _ = emit_m44_operator(
        tmp_path / "out2",
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m43_gate_path=gate_bad,
        dry_run_plan_path=dry,
        evaluation_environment_path=envp,
    )
    assert REFUSED_M43_HONESTY_VIOLATION in {r["code"] for r in sealed["refusals"]}


def test_m44_operator_preflight_missing_dry_run_arg(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate = u / "v15_bounded_evaluation_gate.json"
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    sealed, _ = emit_m44_operator(
        tmp_path / "outp",
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m43_gate_path=gate,
        dry_run_plan_path=None,
        evaluation_environment_path=envp,
    )
    assert REFUSED_DRY_RUN_PLAN_MISSING in {r["code"] for r in sealed["refusals"]}


def test_m44_operator_declared_missing_dry_run(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate = u / "v15_bounded_evaluation_gate.json"
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    sealed, _ = emit_m44_operator(
        tmp_path / "outd",
        profile=PROFILE_OPERATOR_DECLARED,
        m43_gate_path=gate,
        dry_run_plan_path=None,
        evaluation_environment_path=envp,
    )
    assert REFUSED_DRY_RUN_PLAN_MISSING in {r["code"] for r in sealed["refusals"]}
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_NOT_READY


def test_m44_operator_declared_missing_env_manifest(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate = u / "v15_bounded_evaluation_gate.json"
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    dry = tmp_path / "dry.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    sealed, _ = emit_m44_operator(
        tmp_path / "outm",
        profile=PROFILE_OPERATOR_DECLARED,
        m43_gate_path=gate,
        dry_run_plan_path=dry,
        evaluation_environment_path=None,
    )
    assert REFUSED_ENV_MANIFEST_MISSING in {r["code"] for r in sealed["refusals"]}


def test_m44_operator_declared_m43_warnings_path(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate_warn = tmp_path / "gw.json"
    g0 = json.loads((u / "v15_bounded_evaluation_gate.json").read_text(encoding="utf-8"))
    body = {k: v for k, v in g0.items() if k != M43_DIGEST}
    body["gate_status"] = STATUS_GATE_READY_WITH_WARNINGS
    mp = dict(body["m42_package"]) if isinstance(body.get("m42_package"), dict) else {}
    mp["m42_noncritical_warnings"] = ["fixture_catalog_note"]
    body["m42_package"] = mp
    gate_warn.write_text(canonical_json_dumps(seal_m43_body(body)), encoding="utf-8")
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    dry = tmp_path / "dry.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    sealed, _ = emit_m44_operator(
        tmp_path / "ww",
        profile=PROFILE_OPERATOR_DECLARED,
        m43_gate_path=gate_warn,
        dry_run_plan_path=dry,
        evaluation_environment_path=envp,
    )
    assert sealed["preflight_status"] == STATUS_PREFLIGHT_READY_WARNINGS


@pytest.mark.parametrize(
    "flag,expected_refusal",
    [
        ("--run-benchmark", REFUSED_DISALLOWED_EXECUTION),
        ("--execute-evaluation", REFUSED_DISALLOWED_EXECUTION),
        ("--load-checkpoint", REFUSED_CHECKPOINT_LOAD),
        ("--run-live-sc2", REFUSED_LIVE_SC2),
        ("--produce-scorecard-results", REFUSED_DISALLOWED_EXECUTION),
        ("--run-xai", REFUSED_DISALLOWED_EXECUTION),
        ("--run-human-panel", REFUSED_DISALLOWED_EXECUTION),
        ("--release-showcase", REFUSED_DISALLOWED_EXECUTION),
        ("--authorize-v2", REFUSED_DISALLOWED_EXECUTION),
        ("--promote-checkpoint", REFUSED_DISALLOWED_EXECUTION),
    ],
)
def test_m44_forbidden_flags_cli(
    tmp_path: Path,
    flag: str,
    expected_refusal: str,
) -> None:
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_m44_bounded_evaluation_execution_preflight",
            "--profile",
            PROFILE_FIXTURE_CI,
            "--output-dir",
            str(out),
            flag,
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0
    sealed = json.loads(
        (out / "v15_bounded_evaluation_execution_preflight.json").read_text(encoding="utf-8")
    )
    for k in ("benchmark_execution_performed", "torch_load_invoked", "live_sc2_executed"):
        assert sealed[k] is False
    refs = sealed.get("refusals") or []
    assert refs[0]["code"] == expected_refusal


@pytest.mark.smoke
def test_m44_fixture_emit_smoke(tmp_path: Path) -> None:
    emit_m44_fixture_ci(tmp_path / "sx")
    assert True


def test_m44_fixture_deterministic(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_m44_fixture_ci(a)
    emit_m44_fixture_ci(b)
    xa = (a / "v15_bounded_evaluation_execution_preflight.json").read_text(encoding="utf-8")
    xb = (b / "v15_bounded_evaluation_execution_preflight.json").read_text(encoding="utf-8")
    assert xa == xb


def test_m44_sealed_json_redacts_windows_path_hint(tmp_path: Path) -> None:
    u = _upstream_dir(tmp_path)
    gate = u / "v15_bounded_evaluation_gate.json"
    proto = json.loads((u / FILENAME_FIXTURE_PROTOCOL).read_text(encoding="utf-8"))
    env = json.loads((u / FILENAME_FIXTURE_ENV).read_text(encoding="utf-8"))
    dry = tmp_path / "dry.json"
    dry.write_text(
        canonical_json_dumps({"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto}),
        encoding="utf-8",
    )
    envp = tmp_path / "env.json"
    envp.write_text(canonical_json_dumps(env), encoding="utf-8")
    outp = tmp_path / "rz"
    emit_m44_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m43_gate_path=gate,
        dry_run_plan_path=dry,
        evaluation_environment_path=envp,
        operator_logical_hint=r"C:\Users\fixture_operator\M43\gate.json",
    )
    blob = (outp / "v15_bounded_evaluation_execution_preflight.json").read_text(encoding="utf-8")
    chk = (outp / "v15_bounded_evaluation_execution_preflight_checklist.md").read_text(
        encoding="utf-8"
    )
    assert r"C:\Users\fixture_operator" not in blob
    assert r"C:\Users\fixture_operator" not in chk


def test_m44_no_torch_load_in_surface_modules() -> None:
    root = Path(__file__).resolve().parents[1]
    for name in (
        "m44_bounded_evaluation_execution_preflight_io.py",
        "emit_v15_m44_bounded_evaluation_execution_preflight.py",
    ):
        txt = (root / "starlab" / "v15" / name).read_text(encoding="utf-8")
        assert "torch.load" not in txt


def test_m44_no_checkpoint_blob_suffix_logic() -> None:
    root = Path(__file__).resolve().parents[1]
    txt = (root / "starlab" / "v15" / "m44_bounded_evaluation_execution_preflight_io.py").read_text(
        encoding="utf-8",
    )
    lowered = txt.lower()
    assert '".pt"' not in lowered
    assert ".pth" not in lowered
