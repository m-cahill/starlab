"""Tests for V15-M54 twelve-hour run package / evaluation readiness."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import pytest
from starlab.runs.json_util import canonical_json_dumps
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m53_twelve_hour_operator_run_attempt_io import (
    build_m53_fixture_body,
    seal_m53_body,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    PHASE_A_COMPLETED,
    STATUS_12H_COMPLETED_CKPT,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_io import (
    M54PreflightInputs,
    emit_m54_fixture_ci,
    emit_m54_operator_declared,
    emit_m54_operator_preflight_bundle,
    evaluate_m54_operator_preflight,
    sha256_file_hex,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_models import (
    ANCHOR_INPUT_CANDIDATE_CHECKPOINT_SHA256,
    BINDING_FILENAME,
    BLOCKED_FINAL_CKPT_MISSING,
    BLOCKED_FINAL_CKPT_NOT_PERSISTED_M53,
    BLOCKED_FULL_WALL_CLOCK,
    BLOCKED_INVENTORY_MISSING_FINAL,
    BLOCKED_M53_CONTRACT_INVALID,
    BLOCKED_M53_HAS_BLOCKERS,
    BLOCKED_M53_HAS_FAILURE_REASONS,
    BLOCKED_M53_NOT_COMPLETED,
    BLOCKED_M53_SHA_MISMATCH,
    BLOCKED_PHASE_A_PROOF,
    BLOCKED_RAW_SHA_MISMATCH,
    BLOCKED_TELEMETRY_MISSING,
    BLOCKED_TRANSCRIPT_MISSING,
    CHECKLIST_FILENAME,
    CONTRACT_ID_M54,
    EMITTER_MODULE_M54,
    FILENAME_MAIN_JSON,
    FINAL_CHECKPOINT_RELATIVE_PATH,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_TORCH_LOAD,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_SUCCESS,
    ROUTE_BOUNDED_EVAL_PREFLIGHT,
    STATUS_BLOCKED,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
    STATUS_READY_WARNINGS,
    WARNING_FINAL_M53_REPLAY_FALSE,
    WARNING_PHASE_A_REPLAY_BUT_M53_FALSE,
    WARNING_RAW_ARTIFACT_HASH_MISSING,
    WARNING_TRANSCRIPT_SHORT,
)

_INP_CKPT = ANCHOR_INPUT_CANDIDATE_CHECKPOINT_SHA256


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _completed_m53_body(*, ck_sha: str, inp_sha: str) -> dict[str, Any]:
    body = build_m53_fixture_body(run_id="m54_unit_test")
    body["run_status"] = STATUS_12H_COMPLETED_CKPT
    smoke = body["phase_a_candidate_watch_smoke"]
    assert isinstance(smoke, dict)
    smoke["status"] = PHASE_A_COMPLETED
    smoke["live_sc2_executed"] = True
    pb = body["phase_b_12hour_run"]
    assert isinstance(pb, dict)
    pb["twelve_hour_run_executed"] = True
    pb["observed_wall_clock_seconds"] = 43202.187
    pb["full_wall_clock_satisfied"] = True
    pb["final_step_checkpoint_persisted"] = True
    pb["final_candidate_checkpoint_sha256"] = ck_sha
    pb["training_update_count"] = 59858688
    pb["checkpoints_written_total"] = 1197174
    pb["checkpoints_pruned_total"] = 1196918
    cid = body["candidate_identity"]
    assert isinstance(cid, dict)
    cid["candidate_checkpoint_sha256"] = inp_sha
    body["operator_artifacts"] = {
        "transcript_captured": True,
        "telemetry_summary_captured": True,
        "checkpoint_inventory_captured": True,
        "replay_saved": False,
    }
    body["checkpoints_retained"] = 256
    body["blockers"] = []
    body["failure_reasons"] = []
    return body


def _write_sealed_m53(path: Path, *, ck_sha: str, inp_sha: str) -> str:
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=inp_sha)
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    return str(sealed["artifact_sha256"])


def _inventory_rows(ck_sha: str) -> dict[str, Any]:
    return {
        "checkpoint_files": [
            {
                "path_relative_to_m39_output_dir": FINAL_CHECKPOINT_RELATIVE_PATH,
                "sha256": ck_sha,
                "size_bytes": 12,
                "mtime_epoch": 1.0,
            },
        ],
    }


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_m54_fixture_emits_bundle_no_torch_use(tmp_path: Path) -> None:
    sealed, paths = emit_m54_fixture_ci(tmp_path / "fx")
    names = {p.name for p in paths}
    assert FILENAME_MAIN_JSON in names
    assert CHECKLIST_FILENAME in names
    assert BINDING_FILENAME in names
    assert sealed["package_status"] == STATUS_FIXTURE_ONLY
    assert sealed["honesty"]["checkpoint_promoted"] is False
    assert sealed["honesty"]["checkpoint_loaded_for_evaluation"] is False
    assert sealed["honesty"]["benchmark_passed"] is False


def test_m54_preflight_happy_path(tmp_path: Path) -> None:
    ck_bytes = b"m54_ckpt_blob_test"
    ck_sha = _sha256_bytes(ck_bytes)
    inp_sha = _INP_CKPT
    m53p = tmp_path / "v15_twelve_hour_operator_run_attempt.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=inp_sha)

    proof_obj = {"replay_saved": True, "note": "unit"}
    proof_p = tmp_path / "match_execution_proof.json"
    proof_p.write_text(json.dumps(proof_obj), encoding="utf-8")
    proof_digest = sha256_file_hex(proof_p)

    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text(json.dumps({"ok": True}), encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("x" * 200 + "\noperator transcript line\n", encoding="utf-8")
    ck_p = tmp_path / FINAL_CHECKPOINT_RELATIVE_PATH.replace("/", "__")
    ck_p.parent.mkdir(parents=True, exist_ok=True)
    ck_p.write_bytes(ck_bytes)

    inp = M54PreflightInputs(
        m53_run_json=m53p,
        expected_m53_run_sha256=digest,
        raw_m53_file_sha256=None,
        m53_checkpoint_inventory_json=inv_p,
        m53_telemetry_summary_json=tel_p,
        m53_transcript_path=tr_p,
        phase_a_match_proof_json=proof_p,
        expected_phase_a_proof_sha256=proof_digest,
        final_candidate_checkpoint_path=ck_p,
        expected_final_candidate_checkpoint_sha256=ck_sha,
    )
    sealed, _paths, ok_pack = emit_m54_operator_preflight_bundle(tmp_path / "out", inputs=inp)
    assert ok_pack
    assert sealed["package_status"] == STATUS_READY_WARNINGS
    warns = sealed["warnings"]
    assert WARNING_RAW_ARTIFACT_HASH_MISSING in warns
    assert WARNING_FINAL_M53_REPLAY_FALSE in warns
    assert WARNING_PHASE_A_REPLAY_BUT_M53_FALSE in warns
    assert sealed["candidate_checkpoint_binding"]["promotion_status"] == (
        "not_promoted_candidate_only"
    )
    assert sealed["readiness_decision"]["route_to"] == ROUTE_BOUNDED_EVAL_PREFLIGHT
    assert sealed["recommended_next"] == RECOMMENDED_NEXT_SUCCESS


def test_m53_sha_mismatch_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"a")
    m53p = tmp_path / "m53.json"
    _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256="f" * 64,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=tmp_path / "i.json",
            m53_telemetry_summary_json=tmp_path / "t.json",
            m53_transcript_path=tmp_path / "tr.txt",
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert body["package_status"] == STATUS_BLOCKED
    assert BLOCKED_M53_SHA_MISMATCH in body["blockers"]


def test_m53_invalid_contract_blocks(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"contract_id": "nope"}), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text("{}", encoding="utf-8")
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256="a" * 64,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=sha256_file_hex(proof_p),
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=_sha256_bytes(b"x"),
        ),
    )
    assert BLOCKED_M53_CONTRACT_INVALID in body["blockers"]


def test_m53_not_completed_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"z")
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=_INP_CKPT)
    core["run_status"] = "twelve_hour_operator_run_blocked"
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    p = tmp_path / "m53.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256=str(sealed["artifact_sha256"]),
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_M53_NOT_COMPLETED in body["blockers"]


def test_m53_blockers_nonempty_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"y")
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=_INP_CKPT)
    core["blockers"] = ["x"]
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    p = tmp_path / "m53.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text("{}", encoding="utf-8")
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256=str(sealed["artifact_sha256"]),
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=sha256_file_hex(proof_p),
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_M53_HAS_BLOCKERS in body["blockers"]


def test_m53_failure_reasons_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"w")
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=_INP_CKPT)
    core["failure_reasons"] = ["boom"]
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    p = tmp_path / "m53.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text("{}", encoding="utf-8")
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256=str(sealed["artifact_sha256"]),
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=sha256_file_hex(proof_p),
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_M53_HAS_FAILURE_REASONS in body["blockers"]


def test_wall_clock_false_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"q")
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=_INP_CKPT)
    pb = core["phase_b_12hour_run"]
    assert isinstance(pb, dict)
    pb["full_wall_clock_satisfied"] = False
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    p = tmp_path / "m53.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text("{}", encoding="utf-8")
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256=str(sealed["artifact_sha256"]),
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=sha256_file_hex(proof_p),
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_FULL_WALL_CLOCK in body["blockers"]


def test_final_ckpt_not_persisted_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"r")
    core = _completed_m53_body(ck_sha=ck_sha, inp_sha=_INP_CKPT)
    pb = core["phase_b_12hour_run"]
    assert isinstance(pb, dict)
    pb["final_step_checkpoint_persisted"] = False
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(core)))
    p = tmp_path / "m53.json"
    p.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    proof_p = tmp_path / "proof.json"
    proof_p.write_text("{}", encoding="utf-8")
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=p,
            expected_m53_run_sha256=str(sealed["artifact_sha256"]),
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=sha256_file_hex(proof_p),
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_FINAL_CKPT_NOT_PERSISTED_M53 in body["blockers"]


def test_missing_final_ckpt_file_blocks(tmp_path: Path) -> None:
    ck_bytes = b"blob"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text("{}", encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("y" * 200 + "\n", encoding="utf-8")
    inp = M54PreflightInputs(
        m53_run_json=m53p,
        expected_m53_run_sha256=digest,
        raw_m53_file_sha256=None,
        m53_checkpoint_inventory_json=inv_p,
        m53_telemetry_summary_json=tel_p,
        m53_transcript_path=tr_p,
        phase_a_match_proof_json=proof_p,
        expected_phase_a_proof_sha256=pd,
        final_candidate_checkpoint_path=tmp_path / "missing.pt",
        expected_final_candidate_checkpoint_sha256=ck_sha,
    )
    body = evaluate_m54_operator_preflight(inp)
    assert BLOCKED_FINAL_CKPT_MISSING in body["blockers"]


def test_inventory_missing_final_blocks(tmp_path: Path) -> None:
    ck_bytes = b"m54_ckpt_blob_test2"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    bad_inv: dict[str, Any] = {"checkpoint_files": []}
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(bad_inv), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text("{}", encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("z" * 200 + "\n", encoding="utf-8")
    ck_p = tmp_path / "f.pt"
    ck_p.write_bytes(ck_bytes)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=inv_p,
            m53_telemetry_summary_json=tel_p,
            m53_transcript_path=tr_p,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=ck_p,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_INVENTORY_MISSING_FINAL in body["blockers"]


def test_missing_telemetry_blocks(tmp_path: Path) -> None:
    ck_bytes = b"b"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("w" * 200 + "\n", encoding="utf-8")
    ck_p = tmp_path / "c.pt"
    ck_p.write_bytes(ck_bytes)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=inv_p,
            m53_telemetry_summary_json=tmp_path / "missing.json",
            m53_transcript_path=tr_p,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=ck_p,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_TELEMETRY_MISSING in body["blockers"]


def test_missing_transcript_blocks(tmp_path: Path) -> None:
    ck_bytes = b"c"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text("{}", encoding="utf-8")
    ck_p = tmp_path / "c.pt"
    ck_p.write_bytes(ck_bytes)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=inv_p,
            m53_telemetry_summary_json=tel_p,
            m53_transcript_path=tmp_path / "missing.txt",
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=ck_p,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_TRANSCRIPT_MISSING in body["blockers"]


def test_phase_a_proof_missing_blocks(tmp_path: Path) -> None:
    ck_sha = _sha256_bytes(b"d")
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=None,
            m53_telemetry_summary_json=None,
            m53_transcript_path=None,
            phase_a_match_proof_json=None,
            expected_phase_a_proof_sha256=None,
            final_candidate_checkpoint_path=None,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_PHASE_A_PROOF in body["blockers"]


def test_short_transcript_warning(tmp_path: Path) -> None:
    ck_bytes = b"m54_ckpt_blob_short_tr"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text("{}", encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("short\n", encoding="utf-8")
    ck_p = tmp_path / "f.pt"
    ck_p.write_bytes(ck_bytes)
    sealed, _, ok_pack = emit_m54_operator_preflight_bundle(
        tmp_path / "o",
        inputs=M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256=None,
            m53_checkpoint_inventory_json=inv_p,
            m53_telemetry_summary_json=tel_p,
            m53_transcript_path=tr_p,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=ck_p,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert ok_pack
    assert WARNING_TRANSCRIPT_SHORT in sealed["warnings"]


def test_raw_file_sha_mismatch_blocks(tmp_path: Path) -> None:
    ck_bytes = b"raw_test_ckpt"
    ck_sha = _sha256_bytes(ck_bytes)
    m53p = tmp_path / "m53.json"
    digest = _write_sealed_m53(m53p, ck_sha=ck_sha, inp_sha=_INP_CKPT)
    proof_p = tmp_path / "proof.json"
    proof_p.write_text('{"replay_saved":false}', encoding="utf-8")
    pd = sha256_file_hex(proof_p)
    inv_p = tmp_path / "inv.json"
    inv_p.write_text(json.dumps(_inventory_rows(ck_sha)), encoding="utf-8")
    tel_p = tmp_path / "tel.json"
    tel_p.write_text("{}", encoding="utf-8")
    tr_p = tmp_path / "tr.txt"
    tr_p.write_text("u" * 200 + "\n", encoding="utf-8")
    ck_p = tmp_path / "f.pt"
    ck_p.write_bytes(ck_bytes)
    body = evaluate_m54_operator_preflight(
        M54PreflightInputs(
            m53_run_json=m53p,
            expected_m53_run_sha256=digest,
            raw_m53_file_sha256="f" * 64,
            m53_checkpoint_inventory_json=inv_p,
            m53_telemetry_summary_json=tel_p,
            m53_transcript_path=tr_p,
            phase_a_match_proof_json=proof_p,
            expected_phase_a_proof_sha256=pd,
            final_candidate_checkpoint_path=ck_p,
            expected_final_candidate_checkpoint_sha256=ck_sha,
        ),
    )
    assert BLOCKED_RAW_SHA_MISMATCH in body["blockers"]


@pytest.mark.parametrize(
    "flag",
    [
        FORBIDDEN_FLAG_CLAIM_BENCHMARK,
        "--claim-strength",
        "--promote-checkpoint",
        "--run-benchmark",
        "--run-xai",
        "--run-human-panel",
        "--release-showcase",
        "--authorize-v2",
        "--execute-t2",
        "--execute-t3",
        "--execute-t4",
        "--execute-t5",
        "--load-checkpoint-for-evaluation",
        FORBIDDEN_FLAG_TORCH_LOAD,
    ],
)
def test_emit_cli_forbidden_flags(tmp_path: Path, repo_root: Path, flag: str) -> None:
    out = tmp_path / "rf"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE_M54,
            "--profile",
            PROFILE_OPERATOR_PREFLIGHT,
            "--output-dir",
            str(out),
            flag,
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["package_status"] == "twelve_hour_run_package_refused"


def test_fixture_emit_cli(tmp_path: Path, repo_root: Path) -> None:
    out = tmp_path / "cli"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE_M54,
            "--profile",
            "fixture_ci",
            "--output-dir",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0


def test_operator_declared_roundtrip(tmp_path: Path) -> None:
    decl = tmp_path / "decl.json"
    decl.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "contract_id": CONTRACT_ID_M54,
                "profile_id": "starlab.v15.m54.twelve_hour_run_package_evaluation_readiness.v1",
                "package_status": STATUS_READY,
                "m53_binding": {"artifact_sha256": "ab" * 32},
                "warnings": [],
                "blockers": [],
                "honesty": {
                    "benchmark_passed": False,
                    "benchmark_pass_fail_emitted": False,
                    "strength_evaluated": False,
                    "checkpoint_promoted": False,
                    "checkpoint_loaded_for_evaluation": False,
                    "xai_executed": False,
                    "human_panel_executed": False,
                    "showcase_released": False,
                    "v2_authorized": False,
                    "t2_t3_t4_t5_executed": False,
                },
                "non_claims": [],
                "recommended_next": RECOMMENDED_NEXT_SUCCESS,
                "readiness_decision": {
                    "recommended_next": RECOMMENDED_NEXT_SUCCESS,
                    "route_status": "recommended_not_executed",
                    "route_to": ROUTE_BOUNDED_EVAL_PREFLIGHT,
                },
            },
        ),
        encoding="utf-8",
    )
    sealed, paths = emit_m54_operator_declared(tmp_path / "od", declared_json=decl)
    assert sealed["contract_id"] == CONTRACT_ID_M54
    assert paths[0].name == FILENAME_MAIN_JSON
