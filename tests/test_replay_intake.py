"""M07 replay intake policy: unit tests (fixture-driven, opaque bytes)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.intake_io import run_replay_intake, write_intake_artifacts
from starlab.replays.intake_models import CHECK_IDS, parse_replay_intake_metadata
from starlab.replays.intake_policy import evaluate_intake_policy
from starlab.runs.canonical_run_artifact import build_manifest_mapping, load_canonical_manifest
from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_content_sha256,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
SYNTHETIC_REPLAY = FIXTURE_DIR / "synthetic_opaque_test.SC2Replay"
M07_SAMPLE = FIXTURE_DIR / "replay_m07_sample.SC2Replay"
M05_EXPECTED_MANIFEST = FIXTURE_DIR / "m05_expected" / "manifest.json"


def _meta(
    *,
    origin: str = "external",
    prov: str = "verified",
    redist: str = "allowed",
    expected_sha: str | None = None,
) -> Any:
    m: dict[str, Any] = {
        "schema_version": "starlab.replay_intake_metadata.v1",
        "declared_origin_class": origin,
        "declared_acquisition_channel": "download",
        "declared_provenance_status": prov,
        "declared_redistribution_posture": redist,
        "declared_source_label": "test-fixture",
    }
    if expected_sha is not None:
        m["expected_replay_content_sha256"] = expected_sha
    return parse_replay_intake_metadata(m)


def _m03_and_binding(replay_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    sha = compute_replay_content_sha256(replay_path)
    ref = build_replay_reference(replay_path)
    rb = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=sha,
        replay_reference=ref,
        run_spec_id=ri["run_spec_id"],
    )
    return ri, ls, rb


def test_check_ids_order_matches_policy() -> None:
    sha = compute_replay_content_sha256(M07_SAMPLE)
    meta = _meta()
    out = evaluate_intake_policy(
        manifest=None,
        manifest_error=None,
        metadata_error=None,
        meta=meta,
        replay_binding=None,
        replay_binding_error=None,
        replay_path=M07_SAMPLE,
        replay_read_error=None,
        replay_sha256=sha,
        run_identity=None,
        run_identity_error=None,
    )
    ids = [c["check_id"] for c in out.check_results]
    assert ids == list(CHECK_IDS)


def test_receipt_and_report_emission(tmp_path: Path) -> None:
    meta_path = tmp_path / "replay_intake_metadata.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
                "expected_replay_content_sha256": compute_replay_content_sha256(M07_SAMPLE),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    outcome, receipt, report = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert outcome.intake_status == "eligible_for_canonical_review"
    assert receipt["schema_version"] == "starlab.replay_intake_receipt.v1"
    assert report["schema_version"] == "starlab.replay_intake_report.v1"
    assert report["policy_version"] == "starlab.replay_intake_policy.v1"
    write_intake_artifacts(output_dir=tmp_path / "out", receipt=receipt, report=report)
    reread = json.loads(
        (tmp_path / "out" / "replay_intake_report.json").read_text(encoding="utf-8")
    )
    assert reread["reason_codes"] == sorted(reread["reason_codes"])
    assert reread["advisory_notes"] == sorted(reread["advisory_notes"])


def test_deterministic_outputs_repeated_runs(tmp_path: Path) -> None:
    sha = compute_replay_content_sha256(M07_SAMPLE)
    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
                "expected_replay_content_sha256": sha,
            },
        ),
        encoding="utf-8",
    )
    _, r1, p1 = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    _, r2, p2 = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert r1 == r2 and p1 == p2


def test_accepted_local_only_provenance_asserted(tmp_path: Path) -> None:
    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "unknown",
                "declared_origin_class": "external",
                "declared_provenance_status": "asserted",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
            },
        ),
        encoding="utf-8",
    )
    out, _, report = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert out.intake_status == "accepted_local_only"
    assert report["intake_status"] == "accepted_local_only"
    assert "provenance posture is not verified" in " ".join(report["advisory_notes"])


def test_quarantined_forbidden_redistribution(tmp_path: Path) -> None:
    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "forbidden",
                "declared_source_label": "x",
            },
        ),
        encoding="utf-8",
    )
    out, _, _ = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert out.intake_status == "quarantined"
    assert "redistribution_forbidden" in out.reason_codes


def test_rejected_invalid_metadata(tmp_path: Path) -> None:
    meta_path = tmp_path / "m.json"
    meta_path.write_text('{"not": "valid"}', encoding="utf-8")
    out, _, _ = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=None,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert out.intake_status == "rejected"
    assert "metadata_schema_invalid" in out.reason_codes


def test_rejected_binding_hash_mismatch(tmp_path: Path) -> None:
    ri, _ls, rb = _m03_and_binding(SYNTHETIC_REPLAY)
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(rb_path, rb)
    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "generated",
                "declared_origin_class": "starlab_generated",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
            },
        ),
        encoding="utf-8",
    )
    out, _, _ = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=rb_path,
        replay_path=M07_SAMPLE,
        run_identity_path=None,
    )
    assert out.intake_status == "rejected"
    assert "replay_binding_hash_mismatch" in out.reason_codes


def test_eligible_with_binding_and_lineage(tmp_path: Path) -> None:
    ri, ls, rb = _m03_and_binding(SYNTHETIC_REPLAY)
    ri_path = tmp_path / "run_identity.json"
    rb_path = tmp_path / "replay_binding.json"
    man_path = tmp_path / "manifest.json"
    write_json_record(ri_path, ri)
    write_json_record(rb_path, rb)
    man = build_manifest_mapping(lineage_seed=ls, replay_binding=rb, run_identity=ri)
    write_json_record(man_path, man)

    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "generated",
                "declared_origin_class": "starlab_generated",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
                "expected_replay_content_sha256": compute_replay_content_sha256(SYNTHETIC_REPLAY),
            },
        ),
        encoding="utf-8",
    )
    out, receipt, report = run_replay_intake(
        manifest_path=man_path,
        metadata_path=meta_path,
        replay_binding_path=rb_path,
        replay_path=SYNTHETIC_REPLAY,
        run_identity_path=ri_path,
    )
    assert out.intake_status == "eligible_for_canonical_review"
    assert report["canonical_review_eligible"] is True
    assert receipt["linked_artifacts"]["replay_binding.json"] is not None


def test_quarantine_identity_conflict(tmp_path: Path) -> None:
    ri, _ls, rb = _m03_and_binding(SYNTHETIC_REPLAY)
    bad_ri = dict(ri)
    bad_ri["execution_id"] = "f" * 64
    ri_path = tmp_path / "run_identity.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, bad_ri)
    write_json_record(rb_path, rb)

    meta_path = tmp_path / "m.json"
    meta_path.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "generated",
                "declared_origin_class": "starlab_generated",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "x",
                "expected_replay_content_sha256": compute_replay_content_sha256(SYNTHETIC_REPLAY),
            },
        ),
        encoding="utf-8",
    )
    out, _, _ = run_replay_intake(
        manifest_path=None,
        metadata_path=meta_path,
        replay_binding_path=rb_path,
        replay_path=SYNTHETIC_REPLAY,
        run_identity_path=ri_path,
    )
    assert out.intake_status == "quarantined"
    assert "evidence_conflict" in out.reason_codes


def test_load_canonical_manifest_round_trip() -> None:
    m = load_canonical_manifest(M05_EXPECTED_MANIFEST)
    assert m["schema_version"] == "starlab.canonical_run_artifact.v0"
    assert m["replay_content_sha256"]
