"""M04 replay binding: content hash, binding ID, and record determinism."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.runs.replay_binding import (
    BINDING_MODE,
    REPLAY_BINDING_SCHEMA_VERSION,
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_binding_id,
    compute_replay_content_sha256,
    load_lineage_seed,
    load_replay_binding,
    load_run_identity,
    write_replay_binding,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
SYNTHETIC_REPLAY = FIXTURE_DIR / "synthetic_opaque_test.SC2Replay"


def _generate_m03_artifacts(tmp_path: Path) -> tuple[Path, Path]:
    """Generate M03 run_identity.json and lineage_seed.json from M02 fixtures."""

    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    return ri_path, ls_path


def test_replay_content_sha256_stable() -> None:
    h1 = compute_replay_content_sha256(SYNTHETIC_REPLAY)
    h2 = compute_replay_content_sha256(SYNTHETIC_REPLAY)
    assert h1 == h2
    assert len(h1) == 64


def test_replay_reference_metadata() -> None:
    ref = build_replay_reference(SYNTHETIC_REPLAY)
    assert ref["basename"] == "synthetic_opaque_test.SC2Replay"
    assert ref["suffix"] == ".SC2Replay"
    assert isinstance(ref["size_bytes"], int)
    assert ref["size_bytes"] > 0


def test_binding_id_stable() -> None:
    kwargs = {
        "run_spec_id": "a" * 64,
        "execution_id": "b" * 64,
        "lineage_seed_id": "c" * 64,
        "proof_artifact_hash": "d" * 64,
        "replay_content_sha256": "e" * 64,
    }
    id1 = compute_replay_binding_id(**kwargs)
    id2 = compute_replay_binding_id(**kwargs)
    assert id1 == id2
    assert len(id1) == 64


def test_binding_id_changes_with_different_replay() -> None:
    base = {
        "run_spec_id": "a" * 64,
        "execution_id": "b" * 64,
        "lineage_seed_id": "c" * 64,
        "proof_artifact_hash": "d" * 64,
        "replay_content_sha256": "e" * 64,
    }
    alt = {**base, "replay_content_sha256": "f" * 64}
    assert compute_replay_binding_id(**base) != compute_replay_binding_id(**alt)


def test_binding_id_changes_with_different_run_spec() -> None:
    base = {
        "run_spec_id": "a" * 64,
        "execution_id": "b" * 64,
        "lineage_seed_id": "c" * 64,
        "proof_artifact_hash": "d" * 64,
        "replay_content_sha256": "e" * 64,
    }
    alt = {**base, "run_spec_id": "0" * 64}
    assert compute_replay_binding_id(**base) != compute_replay_binding_id(**alt)


def test_build_record_has_required_fields() -> None:
    ref = {"basename": "test.SC2Replay", "suffix": ".SC2Replay", "size_bytes": 100}
    record = build_replay_binding_record(
        execution_id="b" * 64,
        lineage_seed_id="c" * 64,
        proof_artifact_hash="d" * 64,
        replay_content_sha256="e" * 64,
        replay_reference=ref,
        run_spec_id="a" * 64,
    )
    assert record["schema_version"] == REPLAY_BINDING_SCHEMA_VERSION
    assert record["binding_mode"] == BINDING_MODE
    assert len(record["replay_binding_id"]) == 64
    assert record["parent_references"] == []
    assert isinstance(record["later_milestones"], list)
    assert len(record["later_milestones"]) == 2


def test_record_deterministic_twice() -> None:
    ref = {"basename": "test.SC2Replay", "suffix": ".SC2Replay", "size_bytes": 100}
    r1 = build_replay_binding_record(
        execution_id="b" * 64,
        lineage_seed_id="c" * 64,
        proof_artifact_hash="d" * 64,
        replay_content_sha256="e" * 64,
        replay_reference=ref,
        run_spec_id="a" * 64,
    )
    r2 = build_replay_binding_record(
        execution_id="b" * 64,
        lineage_seed_id="c" * 64,
        proof_artifact_hash="d" * 64,
        replay_content_sha256="e" * 64,
        replay_reference=ref,
        run_spec_id="a" * 64,
    )
    assert r1 == r2


def test_write_replay_binding_creates_file(tmp_path: Path) -> None:
    ref = {"basename": "test.SC2Replay", "suffix": ".SC2Replay", "size_bytes": 100}
    record = build_replay_binding_record(
        execution_id="b" * 64,
        lineage_seed_id="c" * 64,
        proof_artifact_hash="d" * 64,
        replay_content_sha256="e" * 64,
        replay_reference=ref,
        run_spec_id="a" * 64,
    )
    out = write_replay_binding(tmp_path, record)
    assert out.is_file()
    assert out.name == "replay_binding.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema_version"] == REPLAY_BINDING_SCHEMA_VERSION


def test_load_run_identity_validates(tmp_path: Path) -> None:
    ri_path, _ = _generate_m03_artifacts(tmp_path)
    ri = load_run_identity(ri_path)
    assert "run_spec_id" in ri
    assert "execution_id" in ri
    assert "proof_artifact_hash" in ri


def test_load_lineage_seed_validates(tmp_path: Path) -> None:
    _, ls_path = _generate_m03_artifacts(tmp_path)
    ls = load_lineage_seed(ls_path)
    assert "lineage_seed_id" in ls


def test_end_to_end_deterministic(tmp_path: Path) -> None:
    """Full e2e: generate M03 artifacts, bind synthetic replay, verify determinism."""

    ri_path, ls_path = _generate_m03_artifacts(tmp_path / "m03")

    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"

    for out_dir in (out1, out2):
        ri = load_run_identity(ri_path)
        ls = load_lineage_seed(ls_path)
        sha = compute_replay_content_sha256(SYNTHETIC_REPLAY)
        ref = build_replay_reference(SYNTHETIC_REPLAY)
        record = build_replay_binding_record(
            execution_id=ri["execution_id"],
            lineage_seed_id=ls["lineage_seed_id"],
            proof_artifact_hash=ri["proof_artifact_hash"],
            replay_content_sha256=sha,
            replay_reference=ref,
            run_spec_id=ri["run_spec_id"],
        )
        write_replay_binding(out_dir, record)

    text1 = (out1 / "replay_binding.json").read_text(encoding="utf-8")
    text2 = (out2 / "replay_binding.json").read_text(encoding="utf-8")
    assert text1 == text2

    data = json.loads(text1)
    assert data["replay_content_sha256"] == compute_replay_content_sha256(SYNTHETIC_REPLAY)
    assert len(data["replay_binding_id"]) == 64
    assert data["run_spec_id"] == load_run_identity(ri_path)["run_spec_id"]


def test_load_replay_binding_round_trip(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path)
    ri = load_run_identity(ri_path)
    ls = load_lineage_seed(ls_path)
    sha = compute_replay_content_sha256(SYNTHETIC_REPLAY)
    ref = build_replay_reference(SYNTHETIC_REPLAY)
    record = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=sha,
        replay_reference=ref,
        run_spec_id=ri["run_spec_id"],
    )
    out = write_replay_binding(tmp_path, record)
    loaded = load_replay_binding(out)
    assert loaded["replay_binding_id"] == record["replay_binding_id"]
    assert loaded["binding_mode"] == BINDING_MODE


def test_load_replay_binding_rejects_wrong_binding_id(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path)
    ri = load_run_identity(ri_path)
    ls = load_lineage_seed(ls_path)
    sha = compute_replay_content_sha256(SYNTHETIC_REPLAY)
    ref = build_replay_reference(SYNTHETIC_REPLAY)
    record = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=sha,
        replay_reference=ref,
        run_spec_id=ri["run_spec_id"],
    )
    record["replay_binding_id"] = "0" * 64
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="recomputed"):
        load_replay_binding(bad)
