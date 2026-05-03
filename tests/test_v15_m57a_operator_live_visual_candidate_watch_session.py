"""Tests for V15-M57A operator live visual candidate watch session."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.m52_candidate_live_adapter_spike_io import emit_m52a_fixture_ci
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    ADAPTER_SPIKE_LABEL,
    STATUS_SPIKE_COMPLETED,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_io import (
    DeclaredInputs,
    PreflightInputs,
    build_fixture_watch_session,
    build_operator_declared_watch_session,
    build_operator_preflight_watch_session,
    seal_m57a_body,
    session_body_from_m52a_delegate,
    write_watch_session_artifacts,
)
from starlab.v15.m57a_operator_live_visual_candidate_watch_session_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CLASSIFICATION_BLOCKED_MISSING_ADAPTER,
    CLASSIFICATION_CANDIDATE_LIVE_COMPLETED,
    CLASSIFICATION_PREFLIGHT_BLOCKED,
    CONTRACT_ID,
    FILENAME_MAIN_JSON,
    GUARD_ALLOW_OPERATOR_LOCAL,
    GUARD_AUTHORIZE_SESSION,
    REPORT_FILENAME,
    ROUTE_M57,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY_ADAPTER,
)
from starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session import (
    main as m57a_runner_main,
)


def test_fixture_three_artifacts_and_claims(tmp_path: Path) -> None:
    sealed, paths = write_watch_session_artifacts(
        tmp_path / "o", body_unsealed=build_fixture_watch_session()
    )
    assert paths[0].name == FILENAME_MAIN_JSON
    assert paths[1].name == REPORT_FILENAME
    assert paths[2].name.endswith("_checklist.md")
    ws = sealed["watch_session"]
    assert ws["session_status"] == STATUS_FIXTURE_ONLY
    for _k, v in sealed["claim_flags"].items():
        assert v is False
    assert sealed["input_bindings"]["m54_package_sha256"] == CANONICAL_M54_PACKAGE_SHA256
    assert (
        sealed["input_bindings"]["candidate_checkpoint_sha256"]
        == CANONICAL_CANDIDATE_CHECKPOINT_SHA256
    )
    rr = sealed["route_recommendation"]
    assert rr["route"] == ROUTE_M57
    assert rr["route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def test_seal_roundtrip() -> None:
    body = build_fixture_watch_session()
    sealed = seal_m57a_body(body)
    digest = sealed["artifact_sha256"]
    base = {k: v for k, v in sealed.items() if k != "artifact_sha256"}
    assert digest == sha256_hex_of_canonical_json(base)


def test_preflight_neither_m51_nor_m52(tmp_path: Path) -> None:
    body = build_operator_preflight_watch_session(
        PreflightInputs(
            m56_readout_json=None,
            m55_preflight_json=None,
            m54_package_json=None,
            m53_run_json=None,
            m51_watchability_json=None,
            m52a_adapter_json=None,
            m56a_context_json=None,
            candidate_checkpoint=None,
            expected_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["watch_session"]["session_status"] == STATUS_PREFLIGHT_BLOCKED


def test_preflight_with_m52a_fixture_path(tmp_path: Path) -> None:
    _, (m52_main, _, _) = emit_m52a_fixture_ci(tmp_path / "m52")
    body = build_operator_preflight_watch_session(
        PreflightInputs(
            m56_readout_json=None,
            m55_preflight_json=None,
            m54_package_json=None,
            m53_run_json=None,
            m51_watchability_json=None,
            m52a_adapter_json=m52_main,
            m56a_context_json=None,
            candidate_checkpoint=None,
            expected_package_sha256=CANONICAL_M54_PACKAGE_SHA256,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["watch_session"]["session_status"] == STATUS_PREFLIGHT_READY_ADAPTER


def test_declared_rejects_benchmark_claim(tmp_path: Path) -> None:
    bad = build_fixture_watch_session()
    bad["claim_flags"]["benchmark_passed"] = True
    bad["contract_id"] = CONTRACT_ID
    p = tmp_path / "d.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    body = build_operator_declared_watch_session(
        DeclaredInputs(
            declared_path=p,
            expected_candidate_sha256=CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        ),
    )
    assert body["visual_classification"]["classification"] == CLASSIFICATION_PREFLIGHT_BLOCKED


def test_session_from_m52a_completed_maps(tmp_path: Path) -> None:
    m52: dict[str, Any] = {
        "contract_id": "starlab.v15.candidate_live_adapter_spike.v1",
        "adapter_status": STATUS_SPIKE_COMPLETED,
        "adapter_kind": ADAPTER_SPIKE_LABEL,
        "live_sc2_executed": True,
        "torch_load_invoked": True,
        "checkpoint_blob_loaded": True,
        "artifact_sha256": "a" * 64,
        "watchability_run": {
            "replay_saved": False,
            "action_count": 3,
            "observation_count": 2,
        },
        "candidate_identity": {
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256
        },
        "refusals": [],
    }
    base = {k: v for k, v in m52.items() if k != "artifact_sha256"}
    m52["artifact_sha256"] = sha256_hex_of_canonical_json(base)
    body = session_body_from_m52a_delegate(m52, m57_output_dir=tmp_path)
    assert (
        body["visual_classification"]["classification"] == CLASSIFICATION_CANDIDATE_LIVE_COMPLETED
    )
    assert body["visual_classification"]["is_candidate_policy_control_confirmed"] is True


def test_runner_requires_guards(tmp_path: Path) -> None:
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"x")
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session",
            "--output-dir",
            str(tmp_path / "o"),
            "--expected-candidate-sha256",
            CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "--candidate-checkpoint",
            str(ck),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert rc.returncode == 2


def test_runner_blocked_missing_paths(tmp_path: Path) -> None:
    ck = tmp_path / "c.pt"
    ck.write_bytes(b"blob")
    rc = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session",
            GUARD_ALLOW_OPERATOR_LOCAL,
            GUARD_AUTHORIZE_SESSION,
            "--output-dir",
            str(tmp_path / "out"),
            "--expected-candidate-sha256",
            CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "--candidate-checkpoint",
            str(ck),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert rc.returncode == 3
    main = tmp_path / "out" / FILENAME_MAIN_JSON
    assert main.is_file()
    data = json.loads(main.read_text(encoding="utf-8"))
    assert data["visual_classification"]["classification"] == CLASSIFICATION_BLOCKED_MISSING_ADAPTER


@pytest.mark.smoke
def test_runner_scaffold_guard_emits_blocked_without_m51_flags(tmp_path: Path) -> None:
    """Without --allow-scaffold-watchability-policy the runner must refuse (exit 3)."""

    ck = tmp_path / "c.pt"
    ck.write_bytes(b"z")
    out = tmp_path / "out2"
    argv = [
        GUARD_ALLOW_OPERATOR_LOCAL,
        GUARD_AUTHORIZE_SESSION,
        "--output-dir",
        str(out),
        "--expected-candidate-sha256",
        CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "--candidate-checkpoint",
        str(ck),
    ]
    with patch(
        "starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session.validate_candidate_sha",
        return_value=None,
    ):
        rc = m57a_runner_main(argv)
    assert rc == 3
    main_json = out / FILENAME_MAIN_JSON
    assert main_json.is_file()
    data = json.loads(main_json.read_text(encoding="utf-8"))
    assert (
        "scaffold"
        in str(
            data.get("visual_classification", {}).get("classification_reason", ""),
        ).lower()
    )
