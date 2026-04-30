"""V15-M43 bounded evaluation gate tests (routing only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_io import seal_m42_body
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_BLOCKED_M41_NOT_READY,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_READY as M42_READY,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_READY_WARNINGS as M42_STATUS_READY_WARNINGS,
)
from starlab.v15.m43_bounded_evaluation_gate_io import (
    build_fixture_benchmark_protocol_sealed,
    build_fixture_environment_manifest_sealed,
    build_synthetic_m42_package_ready_unsealed,
    decide_gate,
    emit_m43_disallowed_execution,
    emit_m43_fixture,
    emit_m43_operator,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    M42_FILENAME_MAIN_CANONICAL,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_BENCHMARK_PROTOCOL_MISSING,
    REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY,
    REFUSED_DISALLOWED_EXECUTION_REQUEST,
    REFUSED_ENVIRONMENT_PREREQUISITE_MISSING,
    REFUSED_M42_PACKAGE_NOT_READY,
    STATUS_GATE_NOT_READY,
    STATUS_GATE_READY,
    STATUS_GATE_READY_WITH_WARNINGS,
)


def _sealed_ready_m42() -> dict[str, Any]:
    body = dict(build_synthetic_m42_package_ready_unsealed())
    assert body["package_status"] == M42_READY
    return seal_m42_body(body)


def test_m43_fixture_ready_path(tmp_path: Path) -> None:
    out = tmp_path / "fx"
    sealed, _paths = emit_m43_fixture(out)
    assert sealed["gate_status"] == STATUS_GATE_READY
    assert sealed["evaluation_executed"] is False
    assert sealed["checkpoint_loaded"] is False
    assert sealed["promotion_decision_made"] is False
    assert (out / "v15_bounded_evaluation_gate.json").is_file()
    assert (out / M42_FILENAME_MAIN_CANONICAL).is_file()


def test_m43_operator_preflight_m42_not_ready(tmp_path: Path) -> None:
    body = dict(build_synthetic_m42_package_ready_unsealed())
    body["package_status"] = STATUS_BLOCKED_M41_NOT_READY
    m42 = seal_m42_body(body)
    proto = build_fixture_benchmark_protocol_sealed()
    env = build_fixture_environment_manifest_sealed()
    st, _, refusals, _ = decide_gate(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m42=m42,
        protocol=proto,
        env=env,
        m42_path_for_prereq=None,
    )
    assert st == REFUSED_M42_PACKAGE_NOT_READY
    assert refusals and refusals[0]["code"] == REFUSED_M42_PACKAGE_NOT_READY


def test_m43_candidate_posture_violation(tmp_path: Path) -> None:
    body = dict(build_synthetic_m42_package_ready_unsealed())
    cc = dict(body["candidate_checkpoint"])
    cc["promotion_status"] = "promoted_production_candidate"
    body["candidate_checkpoint"] = cc
    m42 = seal_m42_body(body)
    proto = build_fixture_benchmark_protocol_sealed()
    env = build_fixture_environment_manifest_sealed()
    st, _, refusals, _ = decide_gate(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m42=m42,
        protocol=proto,
        env=env,
        m42_path_for_prereq=None,
    )
    assert st == REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY
    codes = {r["code"] for r in refusals}
    assert REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY in codes


def test_m43_operator_declared_missing_protocol_environment(tmp_path: Path) -> None:
    m42 = _sealed_ready_m42()
    st, _, refusals, _ = decide_gate(
        profile=PROFILE_OPERATOR_DECLARED,
        m42=m42,
        protocol=None,
        env=None,
        m42_path_for_prereq=None,
    )
    assert st == STATUS_GATE_NOT_READY
    codes = {r["code"] for r in refusals}
    assert REFUSED_BENCHMARK_PROTOCOL_MISSING in codes
    assert REFUSED_ENVIRONMENT_PREREQUISITE_MISSING in codes


def test_m43_disallowed_execution_flags_emit(tmp_path: Path) -> None:
    out = tmp_path / "d"
    sealed, _ = emit_m43_disallowed_execution(
        out,
        profile=PROFILE_FIXTURE_CI,
        triggered_flags=["--run-benchmark"],
    )
    assert sealed["gate_status"] == REFUSED_DISALLOWED_EXECUTION_REQUEST
    assert sealed["evaluation_executed"] is False


def test_m43_no_torch_load_import_in_surface_modules() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "starlab" / "v15" / "m43_bounded_evaluation_gate_io.py"
    text = path.read_text(encoding="utf-8")
    assert "torch.load" not in text


def test_m43_fixture_emit_deterministic(tmp_path: Path) -> None:
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"
    emit_m43_fixture(out_a)
    emit_m43_fixture(out_b)
    ga = (out_a / "v15_bounded_evaluation_gate.json").read_text(encoding="utf-8")
    gb = (out_b / "v15_bounded_evaluation_gate.json").read_text(encoding="utf-8")
    assert ga == gb


def test_m43_fixture_ci_rejects_m42_warnings_even_with_strict_prereqs() -> None:
    body = dict(build_synthetic_m42_package_ready_unsealed())
    body["package_status"] = M42_STATUS_READY_WARNINGS
    body["noncritical_warnings"] = ["fixture_catalog_warning"]
    m42 = seal_m42_body(body)
    proto = build_fixture_benchmark_protocol_sealed()
    env = build_fixture_environment_manifest_sealed()
    st, _, _, _ = decide_gate(
        profile=PROFILE_FIXTURE_CI,
        m42=m42,
        protocol=proto,
        env=env,
        m42_path_for_prereq=None,
    )
    assert st == REFUSED_M42_PACKAGE_NOT_READY


def test_m43_operator_declared_warnings_carry_forward_status() -> None:
    body = dict(build_synthetic_m42_package_ready_unsealed())
    body["package_status"] = M42_STATUS_READY_WARNINGS
    body["noncritical_warnings"] = ["m41_operator_catalog_note"]
    m42 = seal_m42_body(body)
    proto = build_fixture_benchmark_protocol_sealed()
    env = build_fixture_environment_manifest_sealed()
    st, _, refusals, _ = decide_gate(
        profile=PROFILE_OPERATOR_DECLARED,
        m42=m42,
        protocol=proto,
        env=env,
        m42_path_for_prereq=None,
    )
    assert st == STATUS_GATE_READY_WITH_WARNINGS
    assert not refusals


def test_m43_redacts_operator_windows_path_hint(tmp_path: Path) -> None:
    pkg = tmp_path / "v15_m42_two_hour_candidate_checkpoint_evaluation_package.json"
    pkg.write_text(canonical_json_dumps(_sealed_ready_m42()), encoding="utf-8")
    proto_path = tmp_path / "prot.json"
    env_path = tmp_path / "env.json"
    proto_path.write_text(
        canonical_json_dumps(build_fixture_benchmark_protocol_sealed()),
        encoding="utf-8",
    )
    env_path.write_text(
        canonical_json_dumps(build_fixture_environment_manifest_sealed()),
        encoding="utf-8",
    )
    outp = tmp_path / "out"
    emit_m43_operator(
        outp,
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m42_package_path=pkg,
        benchmark_protocol_path=proto_path,
        environment_manifest_path=env_path,
        operator_logical_m42_hint=r"C:\Users\fixture_operator\M42\candidate_pkg.json",
    )
    blob = (outp / "v15_bounded_evaluation_gate.json").read_text(encoding="utf-8")
    assert r"C:\Users\fixture_operator" not in blob
    assert "<REDACTED" in blob.upper() or "REDACTED" in blob
