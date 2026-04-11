"""M03 lineage seed record hashing and stable serialization."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from starlab.runs.identity import (
    normalize_map_spec_for_identity,
    normalize_match_config_for_identity,
)
from starlab.runs.lineage import (
    build_lineage_seed_mapping,
    build_run_identity_mapping,
    environment_fingerprint_from_proof_and_env,
    validate_proof_config_alignment,
)
from starlab.runs.models import ArtifactReference
from starlab.runs.writer import lineage_seed_to_json, run_identity_to_json
from starlab.sc2.artifacts import ExecutionProofRecord, parse_execution_proof_mapping
from starlab.sc2.match_config import BoundedHorizon, MapSpec, MatchConfig, load_match_config

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


def test_artifact_reference_to_mapping_includes_optional_keys() -> None:
    full = ArtifactReference(
        logical_name="proof",
        path="match_execution_proof.json",
        content_sha256="a" * 64,
        role="proof",
    )
    assert full.to_mapping() == {
        "logical_name": "proof",
        "path": "match_execution_proof.json",
        "content_sha256": "a" * 64,
        "role": "proof",
    }
    minimal = ArtifactReference(logical_name="only")
    assert minimal.to_mapping() == {"logical_name": "only"}


def test_validate_proof_config_alignment_rejects_mismatches() -> None:
    rec, cfg = _fixture_record_and_config()
    with pytest.raises(ValueError, match="seed mismatch"):
        validate_proof_config_alignment(replace(cfg, seed=cfg.seed + 999), rec)
    other_adapter = "burnysc2" if cfg.adapter == "fake" else "fake"
    with pytest.raises(ValueError, match="adapter mismatch"):
        validate_proof_config_alignment(replace(cfg, adapter=other_adapter), rec)
    bad_max = replace(cfg.bounded_horizon, max_game_steps=cfg.bounded_horizon.max_game_steps + 1)
    with pytest.raises(ValueError, match="max_game_steps"):
        validate_proof_config_alignment(replace(cfg, bounded_horizon=bad_max), rec)
    bad_step = replace(cfg.bounded_horizon, game_step=cfg.bounded_horizon.game_step + 1)
    with pytest.raises(ValueError, match="game_step"):
        validate_proof_config_alignment(replace(cfg, bounded_horizon=bad_step), rec)


def test_normalize_map_spec_incomplete_raises() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=1,
        bounded_horizon=BoundedHorizon(5, 1),
        map=MapSpec(),
    )
    with pytest.raises(ValueError, match="map selection is incomplete"):
        normalize_map_spec_for_identity(cfg)


def test_normalize_map_spec_path_mode_uses_basename_only() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=7,
        bounded_horizon=BoundedHorizon(3, 1),
        map=MapSpec(path="/abs/path/to/MyMap.SC2Map"),
    )
    assert normalize_map_spec_for_identity(cfg) == {"basename": "MyMap.SC2Map", "mode": "path"}


def test_normalize_identity_helpers_cover_battle_net_map_and_replay_basename() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=42,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(battle_net_map_name="Test Map"),
        replay_filename="C:\\data\\replays\\fixture.SC2Replay",
    )
    assert normalize_map_spec_for_identity(cfg) == {
        "battle_net_map_name": "Test Map",
        "mode": "battle_net",
    }
    norm = normalize_match_config_for_identity(cfg)
    assert norm["replay_filename"] == "fixture.SC2Replay"


def test_environment_fingerprint_merges_env_file_overrides() -> None:
    rec, _cfg = _fixture_record_and_config()
    fp = environment_fingerprint_from_proof_and_env(
        rec,
        {
            "base_build": "override-base",
            "data_version": "override-dv",
            "platform_string": "override-platform",
            "probe_digest": "override-probe",
        },
    )
    assert fp.base_build == "override-base"
    assert fp.data_version == "override-dv"
    assert fp.platform_string == "override-platform"
    assert fp.probe_digest == "override-probe"


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
