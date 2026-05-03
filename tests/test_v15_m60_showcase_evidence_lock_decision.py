"""Tests for V15-M60 showcase-evidence lock decision."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m60_showcase_evidence_lock_decision import main as emit_m60_main
from starlab.v15.m59_adapter_smoke_readout_io import (
    build_fixture_readout_body,
    write_readout_artifacts,
)
from starlab.v15.m59_adapter_smoke_readout_models import FILENAME_MAIN_JSON as M59_FILENAME
from starlab.v15.m60_showcase_evidence_lock_decision_io import (
    _fixture_upstream_evidence,
    build_continue_remediate_body,
    build_decision_report,
    build_fixture_decision_body,
    evaluate_lock_gates,
    validate_m59_readout_blob,
    write_decision_artifacts,
)
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    CONTRACT_ID,
    CONTRACT_ID_REPORT,
    DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED,
    DECISION_STATUS_SHOWCASE_LOCK_DEFERRED,
    DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
    FILENAME_DECISION_JSON,
    LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY,
    NEXT_ROUTE_M61_RELEASE_LOCK,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
)

_ALLOWED_DECISION_STATUSES = (
    DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
    DECISION_STATUS_SHOWCASE_LOCK_DEFERRED,
    DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED,
)

_FORBIDDEN_FOR_LOCK_TEXT = (
    "benchmark passed",
    "strength proven",
    "checkpoint promoted",
    "v2 authorized",
    "72-hour authorized",
)


def test_fixture_emits_contract_and_status(tmp_path: Path) -> None:
    out = tmp_path / "o"
    assert emit_m60_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(out)]) == 0
    blob = cast(
        dict[str, Any], json.loads((out / FILENAME_DECISION_JSON).read_text(encoding="utf-8"))
    )
    assert blob["contract_id"] == CONTRACT_ID
    assert blob["milestone"] == "V15-M60"
    assert blob["decision_status"] == DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED
    assert blob["decision_status"] in _ALLOWED_DECISION_STATUSES
    flags = cast(dict[str, Any], blob["claim_flags"])
    assert flags["release_lock_executed"] is False
    ld = cast(dict[str, Any], blob["lock_decision"])
    assert ld["next_route_status"] == ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED


def test_non_claim_flags_false_except_showcase_true(tmp_path: Path) -> None:
    emit_m60_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(tmp_path / "z")])
    blob = cast(
        dict[str, Any],
        json.loads((tmp_path / "z" / FILENAME_DECISION_JSON).read_text(encoding="utf-8")),
    )
    f = cast(dict[str, Any], blob["claim_flags"])
    assert f["benchmark_passed"] is False
    assert f["strength_evaluated"] is False
    assert f["checkpoint_promoted"] is False
    assert f["ladder_public_performance_claim_authorized"] is False
    assert f["human_panel_claim_authorized"] is False
    assert f["release_lock_executed"] is False
    assert f["seventy_two_hour_authorized"] is False
    assert f["v2_authorized"] is False
    assert f["v2_recharter_authorized"] is False
    assert f["showcase_evidence_lock_recommended"] is True


def test_lock_route_and_scope(tmp_path: Path) -> None:
    emit_m60_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(tmp_path / "r")])
    blob = cast(
        dict[str, Any],
        json.loads((tmp_path / "r" / FILENAME_DECISION_JSON).read_text(encoding="utf-8")),
    )
    assert blob["claim_flags"]["showcase_evidence_lock_recommended"] is True
    ld = cast(dict[str, Any], blob["lock_decision"])
    assert ld["lock_scope"] == LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY
    assert ld["next_milestone"] == "V15-M61"
    assert ld["next_route"] == NEXT_ROUTE_M61_RELEASE_LOCK


def test_no_illegal_claim_phrases_in_canonical_fixture() -> None:
    body = build_fixture_decision_body()
    dumped = canonical_json_dumps(body).lower()
    for phrase in _FORBIDDEN_FOR_LOCK_TEXT:
        assert phrase not in dumped


def test_operator_preflight_valid_m59(tmp_path: Path) -> None:
    m59_out = tmp_path / "m59"
    write_readout_artifacts(m59_out, body=build_fixture_readout_body())
    m59_p = m59_out / M59_FILENAME
    out = tmp_path / "m60"
    rc = emit_m60_main(
        [
            "--profile",
            PROFILE_OPERATOR_PREFLIGHT,
            "--output-dir",
            str(out),
            "--m59-readout-json",
            str(m59_p),
        ],
    )
    assert rc == 0
    rep = json.loads((out / REPORT_FILENAME).read_text(encoding="utf-8"))
    assert "validated_m59_readout_canonical_sha256" in rep


def test_operator_preflight_missing_json_exit_2(tmp_path: Path) -> None:
    assert (
        emit_m60_main(
            ["--profile", PROFILE_OPERATOR_PREFLIGHT, "--output-dir", str(tmp_path / "bad")]
        )
        == 2
    )


def test_operator_preflight_invalid_m59_exit_2(tmp_path: Path) -> None:
    bad = tmp_path / "bad59.json"
    bad.write_text("{}", encoding="utf-8")
    assert (
        emit_m60_main(
            [
                "--profile",
                PROFILE_OPERATOR_PREFLIGHT,
                "--output-dir",
                str(tmp_path / "o"),
                "--m59-readout-json",
                str(bad),
            ],
        )
        == 2
    )


def test_operator_declared_ok(tmp_path: Path) -> None:
    ack = tmp_path / "ack.json"
    ack.write_text('{"m53_m59_public_closure_acknowledged": true}', encoding="utf-8")
    out = tmp_path / "decl"
    assert (
        emit_m60_main(
            [
                "--profile",
                PROFILE_OPERATOR_DECLARED,
                "--output-dir",
                str(out),
                "--operator-declaration-json",
                str(ack),
            ],
        )
        == 0
    )


def test_operator_declared_bad_ack_exit_2(tmp_path: Path) -> None:
    ack = tmp_path / "bad.json"
    ack.write_text("{}", encoding="utf-8")
    assert (
        emit_m60_main(
            [
                "--profile",
                PROFILE_OPERATOR_DECLARED,
                "--output-dir",
                str(tmp_path / "o"),
                "--operator-declaration-json",
                str(ack),
            ],
        )
        == 2
    )


def test_determinism_fixture(tmp_path_factory: pytest.TempPathFactory) -> None:
    blobs: list[dict[str, Any]] = []
    digests_report: list[str] = []
    for label in ("a", "b"):
        base = tmp_path_factory.mktemp(label)
        emit_m60_main(["--profile", PROFILE_FIXTURE_CI, "--output-dir", str(base / "emit")])
        b = cast(
            dict[str, Any],
            json.loads((base / "emit" / FILENAME_DECISION_JSON).read_text(encoding="utf-8")),
        )
        blobs.append(b)
        rep = cast(
            dict[str, Any],
            json.loads((base / "emit" / REPORT_FILENAME).read_text(encoding="utf-8")),
        )
        digests_report.append(str(rep["decision_canonical_sha256"]))
    assert blobs[0] == blobs[1]
    assert digests_report[0] == digests_report[1]


def test_remediate_body_vocab() -> None:
    upstream = dict(_fixture_upstream_evidence())
    bad = upstream["m53_12_hour_training_execution"]
    if isinstance(bad, dict):
        bad["status"] = "open"
    body = build_continue_remediate_body(
        violations=["not_closed:m53_12_hour_training_execution"],
        upstream_evidence=upstream,
        reason_primary="missing_m53_training_execution_evidence",
    )
    assert body["decision_status"] == DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED
    r1 = sha256_hex_of_canonical_json(body)
    r2 = sha256_hex_of_canonical_json(body)
    assert r1 == r2


def test_gate_helper_overclaim() -> None:
    up = _fixture_upstream_evidence()
    ok, fails = evaluate_lock_gates(upstream=up, overclaim_blocked=True)
    assert ok is False
    assert fails


def test_validate_m59_fixture_roundtrip(tmp_path: Path) -> None:
    mdir = tmp_path / "mx"
    write_readout_artifacts(mdir, body=build_fixture_readout_body())
    raw = cast(dict[str, Any], json.loads((mdir / M59_FILENAME).read_text(encoding="utf-8")))
    assert validate_m59_readout_blob(raw) == (True, "")


def test_report_sorted_keys_mirror_write(tmp_path: Path) -> None:
    body = build_fixture_decision_body()
    write_decision_artifacts(tmp_path / "w", body=body)
    rep1 = build_decision_report(body)
    rep2 = json.loads((tmp_path / "w" / REPORT_FILENAME).read_text(encoding="utf-8"))
    assert rep1 == rep2
    assert rep1["contract_id"] == CONTRACT_ID_REPORT
