"""V15-M41 two-hour run package & evaluation readiness tests."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m41_two_hour_run_package_evaluation_readiness import main as emit_m41_main
from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256
from starlab.v15.m39_two_hour_operator_run_attempt_io import build_fixture_body, seal_m39_body
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    STATUS_FIXTURE_ONLY as M39_FIXTURE_ONLY,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    STATUS_RUN_COMPLETED_WITH_CKPT,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_io import (
    OperatorInputs,
    emit_m41_fixture,
    emit_m41_operator_preflight,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    ANCHOR_M39_RECEIPT_SHA256,
    CANDIDATE_INDEX_FILENAME,
    CONTRACT_ID_M41,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    PROFILE_FIXTURE_CI,
    STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH,
    STATUS_BLOCKED_INVALID_M39,
    STATUS_BLOCKED_M39_NOT_COMPLETED,
    STATUS_BLOCKED_MISSING_INVENTORY,
    STATUS_BLOCKED_MISSING_M39,
    STATUS_BLOCKED_MISSING_TELEMETRY,
    STATUS_BLOCKED_MISSING_TRANSCRIPT,
    STATUS_READY,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    STATUS_FIXTURE_ONLY as M41_FIXTURE,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

_EXPECTED_ARTIFACTS = {
    FILENAME_MAIN_JSON,
    "v15_two_hour_run_package_evaluation_readiness_report.json",
    "v15_two_hour_run_package_evaluation_readiness_checklist.md",
    "v15_m41_evaluation_readiness_packet.md",
    CANDIDATE_INDEX_FILENAME,
}

FINAL_OK = ANCHOR_FINAL_CANDIDATE_SHA256
WRONG_FINAL = "0" * 64


def _completed_m39_dict() -> dict[str, object]:
    b = build_fixture_body(repo_root=REPO_ROOT, m38_obj=None)
    b["profile"] = "operator_local_two_hour_run"
    b["run_status"] = STATUS_RUN_COMPLETED_WITH_CKPT
    b["full_wall_clock_satisfied"] = True
    b["observed_wall_clock_seconds"] = 7202.0
    b["target_wall_clock_seconds"] = 7200
    assert isinstance(b["candidate_checkpoint"], dict)
    b["candidate_checkpoint"]["source_candidate_sha256"] = EXPECTED_PUBLIC_CANDIDATE_SHA256
    b["candidate_checkpoint"]["final_candidate_sha256"] = FINAL_OK
    b["checkpoint_retention"] = {
        "checkpoint_retention_enabled": True,
        "checkpoint_retention_max_retained": 256,
        "checkpoints_written_total": 21515,
        "checkpoints_pruned_total": 21259,
        "final_step_checkpoint_persisted": True,
    }
    assert isinstance(b["execution_telemetry"], dict)
    b["execution_telemetry"]["training_update_count"] = 10757291
    b["execution_telemetry"]["sc2_backed_features_used"] = True
    b["execution_telemetry"]["transcript_captured"] = True
    b["execution_telemetry"]["telemetry_summary_captured"] = True
    b["execution_telemetry"]["checkpoint_inventory_captured"] = True
    assert isinstance(b["claim_flags"], dict)
    for k in (
        "benchmark_passed",
        "scorecard_results_produced",
        "strength_evaluated",
        "checkpoint_promoted",
        "xai_execution_performed",
        "human_panel_execution_performed",
        "showcase_release_authorized",
        "v2_authorized",
        "t2_authorized",
        "t3_authorized",
    ):
        b["claim_flags"][k] = False
    return b


def _inventory_with_final(final_sha: str) -> dict[str, object]:
    return {
        "checkpoint_files": [
            {
                "path_relative_to_m39_output_dir": "dummy.pt",
                "size_bytes": 1,
                "mtime_epoch": 1.0,
                "sha256": final_sha,
            },
        ],
        "classification_note": "test",
    }


def test_m41_fixture_emits_all_artifacts(tmp_path: Path) -> None:
    sealed, paths = emit_m41_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert {p.name for p in paths} == _EXPECTED_ARTIFACTS
    assert sealed["package_status"] == M41_FIXTURE
    assert sealed["contract_id"] == CONTRACT_ID_M41


def test_m41_fixture_status(tmp_path: Path) -> None:
    sealed, _ = emit_m41_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert sealed["package_status"] == "fixture_schema_only_no_operator_package"


def test_m41_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, _ = emit_m41_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    for _k, v in sealed["claim_flags"].items():
        assert v is False


def test_m41_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m41_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads((tmp_path / "o" / FILENAME_MAIN_JSON).read_text())
    assert js["profile"] == PROFILE_FIXTURE_CI


def test_operator_preflight_ok(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "v15_two_hour_operator_run_attempt.json").write_text(
        canonical_json_dumps(sealed_m39),
        encoding="utf-8",
    )
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"profile": "test", "ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("fixture transcript\n", encoding="utf-8")

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "v15_two_hour_operator_run_attempt.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_READY
    assert sealed41["evaluation_ready"] is True
    idx = json.loads((tmp_path / "out" / CANDIDATE_INDEX_FILENAME).read_text())
    roles = [c["role"] for c in idx["candidates"]]
    assert "source_candidate_lineage_anchor" in roles
    assert "final_two_hour_candidate_checkpoint" in roles


def test_operator_blocked_missing_m39(tmp_path: Path) -> None:
    missing = tmp_path / "none.json"
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=missing,
            m39_telemetry_summary_json=tmp_path / "t.json",
            m39_checkpoint_inventory_json=tmp_path / "i.json",
            m39_transcript=tmp_path / "tr.txt",
            expected_m39_artifact_sha256=ANCHOR_M39_RECEIPT_SHA256,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_MISSING_M39


def test_operator_blocked_invalid_contract(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    m39o["contract_id"] = "wrong.contract"
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_INVALID_M39


def _write_companions(d: Path) -> None:
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("ok\n", encoding="utf-8")


def test_operator_blocked_m39_not_completed(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    m39o["run_status"] = M39_FIXTURE_ONLY
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_M39_NOT_COMPLETED


def test_operator_blocked_wall_clock(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    m39o["full_wall_clock_satisfied"] = False
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_M39_NOT_COMPLETED


def test_operator_blocked_final_mismatch(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=WRONG_FINAL,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH


def test_operator_blocked_missing_inventory_file(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("ok\n", encoding="utf-8")

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "missing.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_MISSING_INVENTORY


def test_operator_blocked_missing_telemetry(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("ok\n", encoding="utf-8")

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "missing.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_MISSING_TELEMETRY


def test_transcript_not_copied_to_main_json(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    secret_line = "SECRET_TRANSCRIPT_LINE_XYZ_123\n"
    (d / "v15_m39_operator_transcript.txt").write_text(secret_line * 50, encoding="utf-8")

    emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    main_txt = (tmp_path / "out" / FILENAME_MAIN_JSON).read_text(encoding="utf-8")
    assert "SECRET_TRANSCRIPT_LINE" not in main_txt


def test_candidate_index_not_promoted(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "v15_two_hour_operator_run_attempt.json").write_text(
        canonical_json_dumps(sealed_m39),
        encoding="utf-8",
    )
    _write_companions(d)
    _, paths = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "v15_two_hour_operator_run_attempt.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    idxp = next(p for p in paths if p.name == CANDIDATE_INDEX_FILENAME)
    idx = json.loads(idxp.read_text(encoding="utf-8"))
    for c in idx["candidates"]:
        assert c["promotion_status"] == "not_promoted_candidate_only"
    assert idx["candidates"][1]["sha256"] == FINAL_OK


def test_seal_deterministic(tmp_path: Path) -> None:
    b = emit_m41_fixture(tmp_path / "a", repo_root=REPO_ROOT)[0]
    c = emit_m41_fixture(tmp_path / "b", repo_root=REPO_ROOT)[0]
    d1 = str(b[GATE_ARTIFACT_DIGEST_FIELD])
    d2 = str(c[GATE_ARTIFACT_DIGEST_FIELD])
    assert d1 == d2

    wo = {k: v for k, v in b.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    assert sha256_hex_of_canonical_json(wo) == d1


def test_operator_blocked_expected_digest_mismatch(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)
    wrong_digest = "1" * 64
    assert wrong_digest != str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=wrong_digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_INVALID_M39


def test_operator_blocked_missing_transcript(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("", encoding="utf-8")

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_MISSING_TRANSCRIPT


def test_operator_blocked_inventory_without_final_sha(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(WRONG_FINAL)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("ok\n", encoding="utf-8")

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_MISSING_INVENTORY


def test_operator_blocked_m39_benchmark_claim(tmp_path: Path) -> None:
    d = tmp_path / "bundle"
    d.mkdir()
    m39o = _completed_m39_dict()
    assert isinstance(m39o["claim_flags"], dict)
    m39o["claim_flags"]["benchmark_passed"] = True
    sealed_m39 = seal_m39_body(m39o)
    digest = str(sealed_m39[GATE_ARTIFACT_DIGEST_FIELD])
    (d / "m39.json").write_text(canonical_json_dumps(sealed_m39), encoding="utf-8")
    _write_companions(d)

    sealed41, _ = emit_m41_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=OperatorInputs(
            m39_run_json=d / "m39.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    assert sealed41["package_status"] == STATUS_BLOCKED_INVALID_M39
