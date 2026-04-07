"""M07 replay intake CLI tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_content_sha256,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
OPAQUE_REPLAY_FIXTURE = FIXTURE_DIR / "replay_m07_generated.SC2Replay"
M07_SAMPLE = FIXTURE_DIR / "replay_m07_sample.SC2Replay"


def _run_cli(tmp_path: Path, extra: list[str]) -> subprocess.CompletedProcess[str]:
    out = tmp_path / "out"
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "download",
                "declared_origin_class": "external",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "cli-test",
                "expected_replay_content_sha256": compute_replay_content_sha256(M07_SAMPLE),
            },
        ),
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        "-m",
        "starlab.replays.intake_cli",
        "--replay",
        str(M07_SAMPLE),
        "--metadata",
        str(meta),
        "--output-dir",
        str(out),
        *extra,
    ]
    return subprocess.run(
        cmd,
        check=False,
        text=True,
        capture_output=True,
    )


def test_cli_exit_code_eligible(tmp_path: Path) -> None:
    proc = _run_cli(tmp_path, [])
    assert proc.returncode == 0


def test_cli_creates_artifacts(tmp_path: Path) -> None:
    proc = _run_cli(tmp_path, [])
    assert proc.returncode == 0
    out = tmp_path / "out"
    assert (out / "replay_intake_receipt.json").is_file()
    assert (out / "replay_intake_report.json").is_file()
    rep = json.loads((out / "replay_intake_report.json").read_text(encoding="utf-8"))
    assert rep["intake_status"] == "eligible_for_canonical_review"


def test_cli_determinism(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    proc1 = _run_cli(tmp_path / "a", [])
    proc2 = _run_cli(tmp_path / "b", [])
    assert proc1.returncode == proc2.returncode == 0
    r1 = json.loads(
        (tmp_path / "a" / "out" / "replay_intake_report.json").read_text(encoding="utf-8")
    )
    r2 = json.loads(
        (tmp_path / "b" / "out" / "replay_intake_report.json").read_text(encoding="utf-8")
    )
    assert r1 == r2


def test_cli_optional_linked_artifacts(tmp_path: Path) -> None:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    sha = compute_replay_content_sha256(OPAQUE_REPLAY_FIXTURE)
    rb = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=sha,
        replay_reference=build_replay_reference(OPAQUE_REPLAY_FIXTURE),
        run_spec_id=ri["run_spec_id"],
    )
    ri_path = tmp_path / "run_identity.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(rb_path, rb)
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "generated",
                "declared_origin_class": "starlab_generated",
                "declared_provenance_status": "verified",
                "declared_redistribution_posture": "allowed",
                "declared_source_label": "cli",
                "expected_replay_content_sha256": sha,
            },
        ),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    cmd = [
        sys.executable,
        "-m",
        "starlab.replays.intake_cli",
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--metadata",
        str(meta),
        "--output-dir",
        str(out),
        "--replay-binding",
        str(rb_path),
        "--run-identity",
        str(ri_path),
    ]
    proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
    assert proc.returncode == 0
    receipt = json.loads((out / "replay_intake_receipt.json").read_text(encoding="utf-8"))
    assert receipt["linked_artifacts"]["replay_binding.json"] is not None
    assert receipt["linked_artifacts"]["run_identity.json"] is not None


def test_cli_exit_code_local_only(tmp_path: Path) -> None:
    meta = tmp_path / "meta.json"
    meta.write_text(
        json.dumps(
            {
                "schema_version": "starlab.replay_intake_metadata.v1",
                "declared_acquisition_channel": "unknown",
                "declared_origin_class": "external",
                "declared_provenance_status": "unknown",
                "declared_redistribution_posture": "unknown",
                "declared_source_label": "x",
            },
        ),
        encoding="utf-8",
    )
    out = tmp_path / "out"
    cmd = [
        sys.executable,
        "-m",
        "starlab.replays.intake_cli",
        "--replay",
        str(M07_SAMPLE),
        "--metadata",
        str(meta),
        "--output-dir",
        str(out),
    ]
    proc = subprocess.run(cmd, check=False, text=True, capture_output=True)
    assert proc.returncode == 2
