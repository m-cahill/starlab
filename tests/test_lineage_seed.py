"""M03 lineage seed record hashing and stable serialization."""

from __future__ import annotations

from pathlib import Path

from starlab.runs.lineage import (
    build_lineage_seed_mapping,
    build_run_identity_mapping,
    environment_fingerprint_from_proof_and_env,
)
from starlab.runs.models import ArtifactReference
from starlab.runs.writer import lineage_seed_to_json, run_identity_to_json
from starlab.sc2.artifacts import ExecutionProofRecord, parse_execution_proof_mapping
from starlab.sc2.match_config import MatchConfig, load_match_config

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def _fixture_record_and_config() -> tuple[ExecutionProofRecord, MatchConfig]:
    import json

    proof = json.loads(
        (FIXTURE_DIR / "m02_match_execution_proof.json").read_text(encoding="utf-8"),
    )
    if not isinstance(proof, dict):
        raise AssertionError("expected dict")
    rec = parse_execution_proof_mapping(proof)
    cfg = load_match_config(FIXTURE_DIR / "m02_match_config.json")
    return rec, cfg


def test_lineage_seed_id_stable() -> None:
    rec, cfg = _fixture_record_and_config()
    proof_hash = "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774"
    refs_in = [
        ArtifactReference(logical_name="match_config", role="config"),
        ArtifactReference(logical_name="match_execution_proof", role="proof"),
    ]
    refs_out = [
        ArtifactReference(logical_name="run_identity.json", role="artifact"),
        ArtifactReference(logical_name="lineage_seed.json", role="artifact"),
    ]
    a = build_lineage_seed_mapping(
        artifact_refs=refs_out,
        cfg=cfg,
        input_refs=refs_in,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    b = build_lineage_seed_mapping(
        artifact_refs=refs_out,
        cfg=cfg,
        input_refs=refs_in,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    assert a["lineage_seed_id"] == b["lineage_seed_id"]
    assert a["run_spec_id"] == b["run_spec_id"]
    assert a["execution_id"] == b["execution_id"]


def test_run_identity_json_stable_twice() -> None:
    rec, cfg = _fixture_record_and_config()
    proof_hash = "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774"
    env = environment_fingerprint_from_proof_and_env(rec, None)
    m1 = build_run_identity_mapping(
        cfg=cfg,
        env=env,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    m2 = build_run_identity_mapping(
        cfg=cfg,
        env=env,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    assert run_identity_to_json(m1) == run_identity_to_json(m2)


def test_lineage_seed_json_stable_twice() -> None:
    rec, cfg = _fixture_record_and_config()
    proof_hash = "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774"
    refs_in = [
        ArtifactReference(logical_name="match_config", role="config"),
        ArtifactReference(logical_name="match_execution_proof", role="proof"),
    ]
    refs_out = [ArtifactReference(logical_name="lineage_seed.json", role="artifact")]
    m1 = build_lineage_seed_mapping(
        artifact_refs=refs_out,
        cfg=cfg,
        input_refs=refs_in,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    m2 = build_lineage_seed_mapping(
        artifact_refs=refs_out,
        cfg=cfg,
        input_refs=refs_in,
        proof_artifact_hash=proof_hash,
        record=rec,
    )
    assert lineage_seed_to_json(m1) == lineage_seed_to_json(m2)
