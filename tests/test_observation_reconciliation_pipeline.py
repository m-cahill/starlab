"""M19 observation reconciliation audit tests (fixture-only; no replay, no s2protocol)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.observation.audit_observation_surface import main as audit_main
from starlab.observation.observation_reconciliation_inputs import load_json_object
from starlab.observation.observation_reconciliation_pipeline import (
    build_reconciliation_artifacts,
    emit_reconciliation_artifacts,
)
from starlab.runs.json_util import canonical_json_dumps

FIX = Path(__file__).resolve().parent / "fixtures" / "m19"

M19_RECON_MODULES = (
    "starlab.observation.observation_reconciliation_inputs",
    "starlab.observation.observation_reconciliation_rules",
    "starlab.observation.observation_reconciliation_pipeline",
    "starlab.observation.audit_observation_surface",
)


def test_audit_matches_golden_with_reports() -> None:
    cs, e1 = load_json_object(FIX / "canonical_state.json")
    obs, e2 = load_json_object(FIX / "observation_surface.json")
    csr, e3 = load_json_object(FIX / "canonical_state_report.json")
    osr, e4 = load_json_object(FIX / "observation_surface_report.json")
    assert e1 is None and e2 is None and e3 is None and e4 is None
    assert cs is not None and obs is not None and csr is not None and osr is not None

    audit, report = build_reconciliation_artifacts(
        canonical_state=cs,
        observation_surface=obs,
        canonical_state_report=csr,
        observation_surface_report=osr,
    )

    exp_a = json.loads(
        (FIX / "expected_observation_reconciliation_audit.json").read_text(encoding="utf-8")
    )
    exp_r = json.loads(
        (FIX / "expected_observation_reconciliation_audit_report.json").read_text(encoding="utf-8"),
    )
    assert json.loads(canonical_json_dumps(audit)) == exp_a
    assert json.loads(canonical_json_dumps(report)) == exp_r
    assert report["audit_verdict"] == "pass_with_warnings"


def test_audit_without_reports_passes() -> None:
    cs, _ = load_json_object(FIX / "canonical_state.json")
    obs, _ = load_json_object(FIX / "observation_surface.json")
    assert cs is not None and obs is not None
    audit, report = build_reconciliation_artifacts(
        canonical_state=cs,
        observation_surface=obs,
        canonical_state_report=None,
        observation_surface_report=None,
    )
    assert report["audit_verdict"] in ("pass", "pass_with_warnings")
    assert report["failures"] == []
    assert audit["source_identity"]["canonical_state_report_supplied"] is False
    assert audit["source_identity"]["observation_surface_report_supplied"] is False


def test_gameloop_mismatch_fails() -> None:
    cs, _ = load_json_object(FIX / "canonical_state.json")
    obs, _ = load_json_object(FIX / "observation_surface_gameloop_mismatch.json")
    assert cs is not None and obs is not None
    _audit, report = build_reconciliation_artifacts(
        canonical_state=cs,
        observation_surface=obs,
        canonical_state_report=None,
        observation_surface_report=None,
    )
    assert report["audit_verdict"] == "fail"
    assert any("gameloop mismatch" in f for f in report["failures"])


def test_canonical_state_report_hash_mismatch_fails() -> None:
    cs, _ = load_json_object(FIX / "canonical_state.json")
    obs, _ = load_json_object(FIX / "observation_surface.json")
    bad_rep, _ = load_json_object(FIX / "canonical_state_report_bad_hash.json")
    assert cs is not None and obs is not None and bad_rep is not None
    _audit, report = build_reconciliation_artifacts(
        canonical_state=cs,
        observation_surface=obs,
        canonical_state_report=bad_rep,
        observation_surface_report=None,
    )
    assert report["audit_verdict"] == "fail"
    assert any("hash mismatch" in f for f in report["failures"])


def test_deterministic_repeat_emission(tmp_path: Path) -> None:
    out1 = tmp_path / "a"
    out2 = tmp_path / "b"
    p1, _r1, v1 = emit_reconciliation_artifacts(
        canonical_state_path=FIX / "canonical_state.json",
        observation_surface_path=FIX / "observation_surface.json",
        output_dir=out1,
        canonical_state_report_path=FIX / "canonical_state_report.json",
        observation_surface_report_path=FIX / "observation_surface_report.json",
    )
    p2, _r2, v2 = emit_reconciliation_artifacts(
        canonical_state_path=FIX / "canonical_state.json",
        observation_surface_path=FIX / "observation_surface.json",
        output_dir=out2,
        canonical_state_report_path=FIX / "canonical_state_report.json",
        observation_surface_report_path=FIX / "observation_surface_report.json",
    )
    assert v1 == v2
    assert p1.read_text(encoding="utf-8") == p2.read_text(encoding="utf-8")


def test_audit_cli_exit_codes(tmp_path: Path) -> None:
    good = tmp_path / "good"
    assert (
        audit_main(
            [
                "--canonical-state",
                str(FIX / "canonical_state.json"),
                "--observation-surface",
                str(FIX / "observation_surface.json"),
                "--output-dir",
                str(good),
                "--canonical-state-report",
                str(FIX / "canonical_state_report.json"),
                "--observation-surface-report",
                str(FIX / "observation_surface_report.json"),
            ],
        )
        == 0
    )

    bad = tmp_path / "bad"
    assert (
        audit_main(
            [
                "--canonical-state",
                str(FIX / "canonical_state.json"),
                "--observation-surface",
                str(FIX / "observation_surface_gameloop_mismatch.json"),
                "--output-dir",
                str(bad),
            ],
        )
        == 2
    )


@pytest.mark.parametrize("mod", M19_RECON_MODULES)
def test_m19_reconciliation_modules_do_not_reference_replay_stack(mod: str) -> None:
    import importlib.util

    spec = importlib.util.find_spec(mod)
    assert spec is not None and spec.origin is not None
    src = Path(spec.origin).read_text(encoding="utf-8")
    assert "import s2protocol" not in src
    assert "from s2protocol" not in src
    assert "from starlab.replays" not in src
    assert "import starlab.replays" not in src
