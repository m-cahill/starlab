"""Tests for V15-M59 adapter smoke readout and benchmark overclaim refusal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m59_adapter_smoke_readout import main as emit_m59_main
from starlab.v15.m58_bounded_candidate_adapter_evaluation_execution_models import (
    STATUS_EXECUTION_COMPLETED as M58_COMPLETED,
)
from starlab.v15.m59_adapter_smoke_readout_io import (
    build_fixture_readout_body,
    build_readout_report,
    validate_operator_evidence_inputs,
    write_readout_artifacts,
)
from starlab.v15.m59_adapter_smoke_readout_models import (
    CANONICAL_M58_ARTIFACT_SHA256,
    CANONICAL_UPSTREAM_MAIN_SHA,
    CONTRACT_ID_REFUSAL_REPORT,
    FILENAME_MAIN_JSON,
    M58_ACCEPTANCE_REASON_COMPLETED,
    M58_STATUS_ACCEPTED,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_EVIDENCE,
    READOUT_ADAPTER_SMOKE_ACCEPTED,
    READOUT_BENCHMARK_NOT_EVIDENCE,
    READOUT_NOT_PROMOTED,
    REFUSED_CLAIMS,
    REPORT_FILENAME,
    SCHEMA_VERSION_READOUT,
)

_FORBIDDEN_SUBSTRINGS = (
    "benchmark passed",
    "benchmark-ready",
    "candidate is strong",
    "v1.5 lock approved",
    "72-hour run is approved",
    "v2 is opened",
)


def test_fixture_profile_emit_paths(tmp_path: Path) -> None:
    out = tmp_path / "o"
    assert emit_m59_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)]) == 0
    main_blob = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert main_blob["schema_version"] == SCHEMA_VERSION_READOUT
    ro = cast(dict[str, Any], main_blob["readout"])
    assert ro["adapter_smoke_status"] == READOUT_ADAPTER_SMOKE_ACCEPTED
    assert ro["benchmark_status"] == READOUT_BENCHMARK_NOT_EVIDENCE
    assert ro["promotion_status"] == READOUT_NOT_PROMOTED
    ue = cast(dict[str, Any], main_blob["upstream_evidence"])
    assert ue["m58_status"] == M58_STATUS_ACCEPTED
    assert ue["m58_acceptance_reason"] == M58_ACCEPTANCE_REASON_COMPLETED
    assert ue["artifact_sha256"] == CANONICAL_M58_ARTIFACT_SHA256
    assert ue["main_sha"] == CANONICAL_UPSTREAM_MAIN_SHA


def test_overclaim_refusal_booleans(tmp_path: Path) -> None:
    out = tmp_path / "o2"
    emit_m59_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)])
    main_blob = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    rc = cast(dict[str, Any], main_blob["refused_claims"])
    for k, v in REFUSED_CLAIMS.items():
        assert rc.get(k) is True is v
    dumped = canonical_json_dumps(main_blob)
    low = dumped.lower()
    for sub in _FORBIDDEN_SUBSTRINGS:
        assert sub not in low


def test_determinism_fixture(tmp_path_factory: pytest.TempPathFactory) -> None:
    bodies: list[dict[str, Any]] = []
    for label in ("a", "b"):
        out = tmp_path_factory.mktemp(label)
        emit_m59_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)])
        main_blob = cast(
            dict[str, Any],
            json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8")),
        )
        bodies.append(main_blob)
        rep = json.loads((out / REPORT_FILENAME).read_text(encoding="utf-8"))
        assert rep["contract_id"] == CONTRACT_ID_REFUSAL_REPORT
        assert rep["readout_canonical_sha256"] == sha256_hex_of_canonical_json(main_blob)
    assert bodies[0] == bodies[1]


def test_operator_evidence_cli_ok(tmp_path: Path) -> None:
    out = tmp_path / "op"
    rc = emit_m59_main(
        [
            "--profile",
            PROFILE_OPERATOR_EVIDENCE,
            "--output-dir",
            str(out),
            "--m58-status",
            M58_STATUS_ACCEPTED,
            "--m58-acceptance-reason",
            M58_COMPLETED,
            "--main-sha",
            CANONICAL_UPSTREAM_MAIN_SHA,
            "--m58-artifact-sha256",
            CANONICAL_M58_ARTIFACT_SHA256,
        ],
    )
    assert rc == 0
    main_blob = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert (
        cast(dict[str, Any], main_blob["readout"])["benchmark_status"]
        == READOUT_BENCHMARK_NOT_EVIDENCE
    )


def test_operator_evidence_missing_field_exit_2(tmp_path: Path) -> None:
    assert (
        emit_m59_main(
            [
                "--profile",
                PROFILE_OPERATOR_EVIDENCE,
                "--output-dir",
                str(tmp_path / "bad"),
                "--m58-status",
                M58_STATUS_ACCEPTED,
                "--m58-acceptance-reason",
                M58_COMPLETED,
                "--main-sha",
                CANONICAL_UPSTREAM_MAIN_SHA,
            ],
        )
        == 2
    )


def test_validate_operator_rejects_bad_reason() -> None:
    ok, _ = validate_operator_evidence_inputs(
        m58_status=M58_STATUS_ACCEPTED,
        m58_acceptance_reason="wrong_reason",
        main_sha=CANONICAL_UPSTREAM_MAIN_SHA,
        m58_artifact_sha256=CANONICAL_M58_ARTIFACT_SHA256,
    )
    assert ok is False


def test_report_sorted_keys_match_project(tmp_path: Path) -> None:
    body = build_fixture_readout_body()
    write_readout_artifacts(tmp_path / "w", body=body)
    txt = (tmp_path / "w" / FILENAME_MAIN_JSON).read_text(encoding="utf-8")
    assert txt == canonical_json_dumps(body)
    rep1 = build_readout_report(body)
    rep2 = json.loads((tmp_path / "w" / REPORT_FILENAME).read_text(encoding="utf-8"))
    assert rep1 == rep2
