"""Execution proof artifact hashing and serialization."""

from __future__ import annotations

from starlab.sc2.artifacts import (
    ExecutionProofRecord,
    ReplayMetadata,
    compute_artifact_hash,
    execution_proof_to_json,
    proof_record_to_hash_input_dict,
)


def _sample_record() -> ExecutionProofRecord:
    return ExecutionProofRecord(
        schema_version="match_execution_proof.v1",
        adapter_name="fake",
        runtime_boundary_name="s2client_proto_sc2api",
        base_build=None,
        data_version=None,
        map_logical_key="Maps/X/Y.SC2Map",
        map_resolution="explicit_path",
        seed=1,
        interface={
            "feature_layer_interface": False,
            "raw_interface": True,
            "rendered_interface": False,
            "score_interface": True,
        },
        step_policy={"game_step": 1, "max_game_steps": 3},
        status_sequence=("a", "b"),
        observation_summaries=(
            {"game_loop": 1, "minerals": 50, "vespene": 0},
            {"game_loop": 2, "minerals": 50, "vespene": 0},
        ),
        action_count=0,
        final_status="ok",
        replay=ReplayMetadata(replay_saved=False, note="x"),
    )


def test_hash_stable_across_key_order_in_interface() -> None:
    r1 = _sample_record()
    r2 = ExecutionProofRecord(
        schema_version=r1.schema_version,
        adapter_name=r1.adapter_name,
        runtime_boundary_name=r1.runtime_boundary_name,
        base_build=r1.base_build,
        data_version=r1.data_version,
        map_logical_key=r1.map_logical_key,
        map_resolution=r1.map_resolution,
        seed=r1.seed,
        interface={
            "score_interface": True,
            "raw_interface": True,
            "feature_layer_interface": False,
            "rendered_interface": False,
        },
        step_policy=r1.step_policy,
        status_sequence=r1.status_sequence,
        observation_summaries=r1.observation_summaries,
        action_count=r1.action_count,
        final_status=r1.final_status,
        replay=r1.replay,
    )
    assert compute_artifact_hash(r1) == compute_artifact_hash(r2)


def test_hash_excludes_artifact_hash_field() -> None:
    r = _sample_record()
    d = proof_record_to_hash_input_dict(r)
    assert "artifact_hash" not in d
    h1 = compute_artifact_hash(r)
    out = execution_proof_to_json(r)
    assert h1 in out


def test_json_redact_replay_name() -> None:
    r = ExecutionProofRecord(
        schema_version="match_execution_proof.v1",
        adapter_name="fake",
        runtime_boundary_name="x",
        base_build=None,
        data_version=None,
        map_logical_key="m",
        map_resolution="r",
        seed=1,
        interface={
            "raw_interface": True,
            "score_interface": True,
            "feature_layer_interface": False,
            "rendered_interface": False,
        },
        step_policy={"game_step": 1, "max_game_steps": 1},
        status_sequence=("s",),
        observation_summaries=(),
        action_count=0,
        final_status="ok",
        replay=ReplayMetadata(
            replay_saved=True,
            replay_file_name="secret.SC2Replay",
            replay_file_sha256="abc",
        ),
    )
    plain = execution_proof_to_json(r, redact=False)
    red = execution_proof_to_json(r, redact=True)
    assert "secret.SC2Replay" in plain
    assert "secret.SC2Replay" not in red
    assert "<redacted>" in red
