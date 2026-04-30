"""V15-M42 two-hour candidate checkpoint evaluation package tests."""

from __future__ import annotations

import json
from pathlib import Path

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.emit_v15_m42_two_hour_candidate_checkpoint_evaluation_package import (
    main as emit_m42_main,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_models import EXPECTED_PUBLIC_CANDIDATE_SHA256
from starlab.v15.m39_two_hour_operator_run_attempt_io import build_fixture_body, seal_m39_body
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M39_DIGEST_FIELD,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    STATUS_RUN_COMPLETED_WITH_CKPT,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_io import (
    OperatorInputs as M41OperatorInputs,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_io import (
    build_fixture_m41_body,
    emit_m41_operator_preflight,
    seal_m41_body,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    FILENAME_MAIN_JSON as M41_MAIN_JSON,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M41_GATE,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    PROFILE_M41 as M41_PROFILE,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    STATUS_FIXTURE_ONLY as M41_FIXTURE_PKG,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    STATUS_READY as M41_PKG_READY,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_io import (
    M42OperatorInputs,
    emit_m42_fixture,
    emit_m42_operator_preflight,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    ANCHOR_M39_RECEIPT_SHA256,
    BINDINGS_INDEX_FILENAME,
    CONTRACT_ID_EVAL_PACKAGE_FAMILY,
    FILENAME_MAIN_JSON,
    PROFILE_FIXTURE_CI,
    SOURCE_CANDIDATE_LINEAGE_SHA256,
    STATUS_BLOCKED_FINAL_MISMATCH,
    STATUS_BLOCKED_INVALID_M05,
    STATUS_BLOCKED_INVALID_M41,
    STATUS_BLOCKED_M39_RECEIPT_MISMATCH,
    STATUS_BLOCKED_M41_NOT_READY,
    STATUS_BLOCKED_MISSING_FINAL_INDEX,
    STATUS_BLOCKED_MISSING_M41,
    STATUS_BLOCKED_SOURCE_MISMATCH,
    STATUS_READY,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M42_GATE,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_FIXTURE_ONLY as M42_FIXTURE,
)
from starlab.v15.strong_agent_scorecard_io import (
    build_strong_agent_scorecard_body_fixture,
    seal_strong_agent_scorecard_body,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

_EXPECTED_ARTIFACTS = {
    FILENAME_MAIN_JSON,
    "v15_m42_two_hour_candidate_checkpoint_evaluation_package_report.json",
    "v15_m42_two_hour_candidate_checkpoint_evaluation_package_checklist.md",
    "v15_m42_candidate_evaluation_routing_packet.md",
    BINDINGS_INDEX_FILENAME,
}

FINAL_OK = ANCHOR_FINAL_CANDIDATE_SHA256
WRONG_FINAL_HEX = "f" * 64
WRONG_SRC_HEX = "a" + SOURCE_CANDIDATE_LINEAGE_SHA256[1:]


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


def _write_completed_m41_bundle(tmp_path: Path) -> tuple[Path, Path, str]:
    """Return (bundle_dir, sealed_m41_path, m39_digest)."""
    d = tmp_path / "bundle"
    d.mkdir(parents=True, exist_ok=True)
    m39o = _completed_m39_dict()
    sealed_m39 = seal_m39_body(m39o)
    digest_m39 = str(sealed_m39[M39_DIGEST_FIELD])
    (d / "v15_two_hour_operator_run_attempt.json").write_text(
        canonical_json_dumps(sealed_m39),
        encoding="utf-8",
    )
    (d / "v15_m39_telemetry_summary.json").write_text(
        canonical_json_dumps({"ok": True}),
        encoding="utf-8",
    )
    (d / "v15_m39_checkpoint_inventory.json").write_text(
        canonical_json_dumps(_inventory_with_final(FINAL_OK)),
        encoding="utf-8",
    )
    (d / "v15_m39_operator_transcript.txt").write_text("fixture transcript\n", encoding="utf-8")

    sealed41, _paths = emit_m41_operator_preflight(
        tmp_path / "m41_out",
        repo_root=REPO_ROOT,
        inputs=M41OperatorInputs(
            m39_run_json=d / "v15_two_hour_operator_run_attempt.json",
            m39_telemetry_summary_json=d / "v15_m39_telemetry_summary.json",
            m39_checkpoint_inventory_json=d / "v15_m39_checkpoint_inventory.json",
            m39_transcript=d / "v15_m39_operator_transcript.txt",
            expected_m39_artifact_sha256=digest_m39,
            expected_final_candidate_sha256=FINAL_OK,
            authorize_final_checkpoint_file_sha256=False,
            final_candidate_checkpoint_path=None,
        ),
    )
    m41p = tmp_path / "m41_out" / M41_MAIN_JSON
    assert sealed41["package_status"] == M41_PKG_READY
    return d, m41p, digest_m39


def _m42_inp(
    m41_path: Path,
    *,
    m39_digest: str,
    m41_digest: str | None,
    authorize_hash: bool = False,
    ckpt_file: Path | None = None,
    m05: Path | None = None,
    m39_run: Path | None = None,
    inventory: Path | None = None,
    telemetry: Path | None = None,
    ancillary: bool = False,
    wrong_source: bool = False,
    wrong_final_exp: bool = False,
    wrong_m39_digest: str | None = None,
) -> M42OperatorInputs:
    digest_use = wrong_m39_digest if wrong_m39_digest is not None else m39_digest
    return M42OperatorInputs(
        m41_package_json=m41_path,
        expected_m41_package_sha256=m41_digest.strip().lower() if m41_digest else None,
        expected_m39_artifact_sha256=digest_use.strip().lower(),
        expected_source_candidate_sha256=(
            WRONG_SRC_HEX if wrong_source else SOURCE_CANDIDATE_LINEAGE_SHA256
        )
        .strip()
        .lower(),
        expected_final_candidate_sha256=(WRONG_FINAL_HEX if wrong_final_exp else FINAL_OK)
        .strip()
        .lower(),
        m39_run_json=m39_run,
        m39_checkpoint_inventory_json=inventory,
        m39_telemetry_summary_json=telemetry,
        m05_scorecard_json=m05,
        authorize_final_checkpoint_file_sha256=authorize_hash,
        final_candidate_checkpoint_path=ckpt_file,
        ancillary_m39_present_without_m41=ancillary,
    )


def test_m42_fixture_emits_all_artifacts(tmp_path: Path) -> None:
    sealed, paths = emit_m42_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert {p.name for p in paths} == _EXPECTED_ARTIFACTS
    assert sealed["package_status"] == M42_FIXTURE
    assert sealed["contract_id"] == CONTRACT_ID_EVAL_PACKAGE_FAMILY


def test_m42_fixture_claim_flags_false(tmp_path: Path) -> None:
    sealed, _ = emit_m42_fixture(tmp_path / "o", repo_root=REPO_ROOT)
    assert sealed["package_status"] == "fixture_schema_only_no_operator_package"
    assert sealed["evaluation_package_ready"] is False
    assert all(not v for v in sealed["claim_flags"].values())


def test_m42_fixture_cli(tmp_path: Path) -> None:
    rc = emit_m42_main(["--fixture-ci", "--output-dir", str(tmp_path / "o")])
    assert rc == 0
    js = json.loads((tmp_path / "o" / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert js["profile"] == PROFILE_FIXTURE_CI


def test_operator_preflight_ok_with_synthetic_m41(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(m41p, m39_digest=m39_digest, m41_digest=str(digest_m41)),
    )
    assert sealed42["package_status"] == STATUS_READY
    assert sealed42["evaluation_package_ready"] is True
    cand = sealed42["candidate_checkpoint"]
    assert isinstance(cand, dict)
    assert cand["promotion_status"] == "not_promoted_candidate_only"
    assert cand["checkpoint_blob_loaded"] is False
    assert cand["torch_load_performed"] is False


def test_operator_blocked_missing_m41(tmp_path: Path) -> None:
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            tmp_path / "no_m41.json",
            m39_digest=ANCHOR_M39_RECEIPT_SHA256,
            m41_digest=None,
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_MISSING_M41


def test_operator_blocked_invalid_m41_contract(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"contract_id": "x", "profile_id": M41_PROFILE}), encoding="utf-8")
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(p, m39_digest=ANCHOR_M39_RECEIPT_SHA256, m41_digest=None),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_INVALID_M41


def test_operator_blocked_m41_not_ready(tmp_path: Path) -> None:
    base = build_fixture_m41_body()
    base["package_status"] = M41_FIXTURE_PKG
    sealed_m41 = seal_m41_body(base)
    p = tmp_path / "m41.json"
    p.write_text(canonical_json_dumps(sealed_m41), encoding="utf-8")
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            p,
            m39_digest=ANCHOR_M39_RECEIPT_SHA256,
            m41_digest=str(sealed_m41[M41_GATE]),
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_M41_NOT_READY


def test_operator_blocked_m39_receipt_mismatch(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            wrong_m39_digest="aa" + m39_digest[2:],
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_M39_RECEIPT_MISMATCH


def test_operator_blocked_source_mismatch(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(m41p, m39_digest=m39_digest, m41_digest=str(digest_m41), wrong_source=True),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_SOURCE_MISMATCH


def test_operator_blocked_final_mismatch(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            wrong_final_exp=True,
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_FINAL_MISMATCH


def test_operator_blocked_missing_final_index_inconsistent_ready_m41(tmp_path: Path) -> None:
    _bundle_dir, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    _ = _bundle_dir
    raw = json.loads(m41p.read_text(encoding="utf-8"))
    stripped = {k: v for k, v in raw.items() if k != M41_GATE}
    stripped["package_status"] = M41_PKG_READY
    cc = dict(stripped["candidate_checkpoint"])
    cc["final_candidate_sha256"] = None
    stripped["candidate_checkpoint"] = cc
    bad_m41 = seal_m41_body(stripped)
    p = tmp_path / "bad_m41.json"
    p.write_text(canonical_json_dumps(bad_m41), encoding="utf-8")
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(p, m39_digest=m39_digest, m41_digest=str(bad_m41[M41_GATE])),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_MISSING_FINAL_INDEX


def test_optional_m05_binds_when_valid(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    m05b = seal_strong_agent_scorecard_body(build_strong_agent_scorecard_body_fixture())
    m05_path = tmp_path / "v15_strong_agent_scorecard.json"
    m05_path.write_text(canonical_json_dumps(m05b), encoding="utf-8")
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            m05=m05_path,
        ),
    )
    assert sealed42["package_status"] == STATUS_READY
    ub = sealed42["upstream_bindings"]
    assert isinstance(ub, dict)
    m05s = ub.get("m05_scorecard_protocol")
    assert isinstance(m05s, dict)
    assert m05s["binding_status"] == "bound_operator_supplied_cli"


def test_optional_m05_invalid_blocks(tmp_path: Path) -> None:
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    m05_path = tmp_path / "bad_m05.json"
    m05_path.write_text(
        canonical_json_dumps({"contract_id": "starlab.v15.strong_agent_scorecard.v1"}),
        encoding="utf-8",
    )
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            m05=m05_path,
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_INVALID_M05


SEAL_FIELD_M05_STUB = "strong_agent_scorecard_sha256"  # not a valid seal — parse path


def test_path_without_authorize_does_not_verify_file_hash(tmp_path: Path) -> None:
    fp = tmp_path / "tiny.pt"
    fp.write_bytes(b"x")
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            ckpt_file=fp,
            authorize_hash=False,
        ),
    )
    assert sealed42["candidate_checkpoint"]["checkpoint_file_sha256_verified"] is False
    assert sealed42["noncritical_warnings"]


def test_authorized_file_hash_must_match_expected_final_metadata(tmp_path: Path) -> None:
    fp = tmp_path / "tiny.pt"
    fp.write_bytes(b"z")
    _bundle, m41p, m39_digest = _write_completed_m41_bundle(tmp_path)
    digest_m41 = json.loads(m41p.read_text(encoding="utf-8"))[M41_GATE]
    sealed42, _ = emit_m42_operator_preflight(
        tmp_path / "out",
        repo_root=REPO_ROOT,
        inputs=_m42_inp(
            m41p,
            m39_digest=m39_digest,
            m41_digest=str(digest_m41),
            ckpt_file=fp,
            authorize_hash=True,
        ),
    )
    assert sealed42["package_status"] == STATUS_BLOCKED_FINAL_MISMATCH


def test_seal_deterministic(tmp_path: Path) -> None:
    a = emit_m42_fixture(tmp_path / "a", repo_root=REPO_ROOT)[0]
    b = emit_m42_fixture(tmp_path / "b", repo_root=REPO_ROOT)[0]
    d1 = str(a[M42_GATE])
    d2 = str(b[M42_GATE])
    assert d1 == d2
    wo = {k: v for k, v in a.items() if k != M42_GATE}
    assert sha256_hex_of_canonical_json(wo) == d1


def test_fixture_emission_no_private_path_patterns(tmp_path: Path) -> None:
    sealed, paths = emit_m42_fixture(tmp_path / "emit", repo_root=REPO_ROOT)
    parts = [canonical_json_dumps(sealed)]
    parts.extend(p.read_text(encoding="utf-8") for p in paths)
    assert not emission_has_private_path_patterns("".join(parts))
