"""Tests for V15-M56A latest candidate visual watchability confirmation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.m51_live_candidate_watchability_harness_io import emit_m51_fixture_ci
from starlab.v15.m52_candidate_live_adapter_spike_io import emit_m52a_fixture_ci
from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
    build_fixture_preflight,
    build_operator_preflight_blocked,
    write_preflight_artifacts,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io import (
    DeclaredInputs,
    PreflightInputs,
    build_fixture_confirmation,
    build_operator_declared_confirmation,
    build_operator_preflight_confirmation,
    seal_m56a_body,
    write_confirmation_artifacts,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    EMITTER_MODULE,
    EVIDENCE_CONTRACT_DECLARED,
    FILENAME_MAIN_JSON,
    FLAG_SCAFFOLD_POLICY,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_VISUAL,
    POLICY_CANDIDATE_LIVE,
    POLICY_SCAFFOLD,
    REPORT_FILENAME,
    ROUTE_M56_READOUT,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    RUNNER_MODULE,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STATUS_SCAFFOLD_CONFIRMED,
)


def test_fixture_three_artifacts_and_claims(tmp_path: Path) -> None:
    sealed, paths = write_confirmation_artifacts(
        tmp_path / "o",
        body_unsealed=build_fixture_confirmation(),
    )
    assert paths[0].name == FILENAME_MAIN_JSON
    assert paths[1].name == REPORT_FILENAME
    assert paths[2].name.endswith("_checklist.md")
    wp = sealed["watchability_profile"]
    assert wp["visual_confirmation_status"] == STATUS_FIXTURE_ONLY
    for _k, v in sealed["claim_flags"].items():
        assert v is False
    assert sealed["input_bindings"]["m54_package_sha256"] == CANONICAL_M54_PACKAGE_SHA256
    assert (
        sealed["input_bindings"]["candidate_checkpoint_sha256"]
        == CANONICAL_CANDIDATE_CHECKPOINT_SHA256
    )
    rr = sealed["route_recommendation"]
    assert rr["route"] == ROUTE_M56_READOUT
    assert rr["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def test_seal_roundtrip() -> None:
    body = build_fixture_confirmation()
    sealed = seal_m56a_body(body)
    digest = sealed["artifact_sha256"]
    base = {k: v for k, v in sealed.items() if k != "artifact_sha256"}
    assert digest == sha256_hex_of_canonical_json(base)


def test_preflight_missing_m55(tmp_path: Path) -> None:
    body = build_operator_preflight_confirmation(
        PreflightInputs(
            m55_preflight_json=tmp_path / "nope.json",
            m54_package_json=tmp_path / "m54.json",
            m53_run_json=tmp_path / "m53.json",
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m51_watchability_json=tmp_path / "m51.json",
            m52a_adapter_spike_json=None,
        ),
    )
    assert "blocked_missing_m55_preflight" in (body.get("blocked_reasons") or [])


def test_preflight_m55_not_ready(tmp_path: Path) -> None:
    m55_dir = tmp_path / "m55out"
    _, (main_path, _) = write_preflight_artifacts(
        m55_dir,
        body_unsealed=build_operator_preflight_blocked(),
    )
    m55_final = tmp_path / "m55.json"
    m55_final.write_text(main_path.read_text(encoding="utf-8"), encoding="utf-8")
    m54 = tmp_path / "m54.json"
    m53 = tmp_path / "m53.json"
    m51 = tmp_path / "m51.json"
    for p in (m54, m53, m51):
        p.write_text("{}", encoding="utf-8")
    body = build_operator_preflight_confirmation(
        PreflightInputs(
            m55_preflight_json=m55_final,
            m54_package_json=m54,
            m53_run_json=m53,
            expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            m51_watchability_json=m51,
            m52a_adapter_spike_json=None,
        ),
    )
    assert "blocked_m55_preflight_not_ready" in (body.get("blocked_reasons") or [])


def _write_ready_m55(path: Path, tmp_root: Path) -> None:
    _, (main, _) = write_preflight_artifacts(tmp_root, body_unsealed=build_fixture_preflight())
    main.replace(path)


def test_preflight_missing_watchability_path(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    m54 = tmp_path / "m54.json"
    m53 = tmp_path / "m53.json"
    m54.write_text("{}", encoding="utf-8")
    m53.write_text("{}", encoding="utf-8")

    fake_m54 = {
        "candidate_checkpoint_binding": {
            "produced_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256
        }
    }

    with (
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m54_file",
            return_value=fake_m54,
        ),
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m53_file",
            return_value={},
        ),
    ):
        body = build_operator_preflight_confirmation(
            PreflightInputs(
                m55_preflight_json=m55,
                m54_package_json=m54,
                m53_run_json=m53,
                expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
                expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
                m51_watchability_json=None,
                m52a_adapter_spike_json=None,
            ),
        )
    assert "blocked_missing_watchability_path" in (body.get("blocked_reasons") or [])


def test_preflight_happy_m51_only(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    m54 = tmp_path / "m54.json"
    m53 = tmp_path / "m53.json"
    m54.write_text("{}", encoding="utf-8")
    m53.write_text("{}", encoding="utf-8")
    _, paths = emit_m51_fixture_ci(tmp_path / "m51out")
    m51_path = paths[0]

    fake_m54 = {
        "candidate_checkpoint_binding": {
            "produced_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256
        }
    }

    with (
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m54_file",
            return_value=fake_m54,
        ),
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m53_file",
            return_value={},
        ),
    ):
        body = build_operator_preflight_confirmation(
            PreflightInputs(
                m55_preflight_json=m55,
                m54_package_json=m54,
                m53_run_json=m53,
                expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
                expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
                m51_watchability_json=m51_path,
                m52a_adapter_spike_json=None,
            ),
        )
    wp = body["watchability_profile"]
    assert wp["visual_confirmation_status"] == STATUS_PREFLIGHT_READY
    assert body["input_bindings"]["m51_watchability_json_sha256"] is not None
    assert body["input_bindings"]["m52a_adapter_spike_json_sha256"] is None


def test_preflight_m52a_sets_live_policy_label(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    m54 = tmp_path / "m54.json"
    m53 = tmp_path / "m53.json"
    m54.write_text("{}", encoding="utf-8")
    m53.write_text("{}", encoding="utf-8")
    _, m52_paths = emit_m52a_fixture_ci(tmp_path / "m52out")
    m52_main = m52_paths[0]

    fake_m54 = {
        "candidate_checkpoint_binding": {
            "produced_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256
        }
    }

    with (
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m54_file",
            return_value=fake_m54,
        ),
        patch(
            "starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_io._validate_m53_file",
            return_value={},
        ),
    ):
        body = build_operator_preflight_confirmation(
            PreflightInputs(
                m55_preflight_json=m55,
                m54_package_json=m54,
                m53_run_json=m53,
                expected_m54_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
                expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
                m51_watchability_json=None,
                m52a_adapter_spike_json=m52_main,
            ),
        )
    assert body["watchability_profile"]["policy_source"] == POLICY_CANDIDATE_LIVE


def test_operator_declared_scaffold_ok(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    ev = tmp_path / "ev.json"
    ev.write_text(
        json.dumps(
            {
                "contract_id": EVIDENCE_CONTRACT_DECLARED,
                "declared_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
                "policy_source": POLICY_SCAFFOLD,
                "live_sc2_executed": True,
                "replay_saved": False,
                "video_metadata_supplied": False,
                "watchability_notes_supplied": True,
            }
        ),
        encoding="utf-8",
    )
    body = build_operator_declared_confirmation(
        DeclaredInputs(
            watchability_evidence_json=ev,
            m55_preflight_json=m55,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["watchability_profile"]["visual_confirmation_status"] == STATUS_SCAFFOLD_CONFIRMED


def test_operator_declared_claim_flag_blocks(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    ev = tmp_path / "ev.json"
    blob = {
        "contract_id": EVIDENCE_CONTRACT_DECLARED,
        "declared_candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "policy_source": POLICY_SCAFFOLD,
        "live_sc2_executed": False,
        "replay_saved": False,
        "video_metadata_supplied": False,
        "watchability_notes_supplied": False,
        "claim_flags": {"benchmark_passed": True},
    }
    ev.write_text(json.dumps(blob), encoding="utf-8")
    body = build_operator_declared_confirmation(
        DeclaredInputs(
            watchability_evidence_json=ev,
            m55_preflight_json=m55,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["watchability_profile"]["visual_confirmation_status"] == STATUS_PREFLIGHT_BLOCKED


def test_operator_declared_private_path_blocks(tmp_path: Path) -> None:
    m55 = tmp_path / "m55.json"
    _write_ready_m55(m55, tmp_path / "pref")
    ev = tmp_path / "ev.json"
    ev.write_text(
        '{"contract_id": "' + EVIDENCE_CONTRACT_DECLARED + '", "note": "docs/company_secrets/x"}',
        encoding="utf-8",
    )
    body = build_operator_declared_confirmation(
        DeclaredInputs(
            watchability_evidence_json=ev,
            m55_preflight_json=m55,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert "blocked_private_boundary_violation" in (body.get("blocked_reasons") or [])


def test_emitter_cli_fixture_subprocess(tmp_path: Path) -> None:
    out = tmp_path / "cli"
    repo = Path(__file__).resolve().parents[1]
    r2 = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r2.returncode == 0, (r2.stdout, r2.stderr)
    assert (out / FILENAME_MAIN_JSON).is_file()


@pytest.mark.smoke
def test_emitter_forbidden_flag_zero(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    out = tmp_path / "e"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            "fixture_ci",
            "--claim-benchmark-pass",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0


def test_runner_refusal_subprocess(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    m55 = tmp_path / "m55.json"
    m55.write_text("{}", encoding="utf-8")
    out = tmp_path / "r"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            RUNNER_MODULE,
            GUARD_ALLOW_OPERATOR_LOCAL,
            GUARD_AUTHORIZE_VISUAL,
            "--m55-preflight-json",
            str(m55),
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 3
    assert (out / FILENAME_MAIN_JSON).is_file()


def test_runner_stub_triple_guard_subprocess(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    m55 = tmp_path / "m55.json"
    m55.write_text("{}", encoding="utf-8")
    out = tmp_path / "r2"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            RUNNER_MODULE,
            GUARD_ALLOW_OPERATOR_LOCAL,
            GUARD_AUTHORIZE_VISUAL,
            FLAG_SCAFFOLD_POLICY,
            "--m55-preflight-json",
            str(m55),
            "--output-dir",
            str(out),
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0
    raw = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert raw["watchability_profile"]["policy_source"] == POLICY_SCAFFOLD
