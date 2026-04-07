"""Assemble run identity and lineage seed records from M02 proof/config (M03)."""

from __future__ import annotations

from typing import Any

from starlab.runs.identity import (
    compute_config_hash,
    compute_execution_id,
    compute_lineage_seed_id,
    compute_run_spec_id,
)
from starlab.runs.models import (
    LINEAGE_SEED_SCHEMA_VERSION,
    RUN_IDENTITY_SCHEMA_VERSION,
    ArtifactReference,
    EnvironmentFingerprint,
)
from starlab.sc2.artifacts import ExecutionProofRecord, compute_artifact_hash
from starlab.sc2.match_config import MatchConfig


def environment_fingerprint_from_proof_and_env(
    record: ExecutionProofRecord,
    env_file: dict[str, Any] | None,
) -> EnvironmentFingerprint:
    """Merge proof fields with optional env JSON overrides.

    Recognized keys include ``base_build`` and ``data_version`` (see runtime doc).
    """

    base = record.base_build
    dv = record.data_version
    platform: str | None = None
    probe_digest: str | None = None
    if env_file:
        if "base_build" in env_file:
            base = env_file.get("base_build")
        if "data_version" in env_file:
            dv = env_file.get("data_version")
        platform = env_file.get("platform_string")
        probe_digest = env_file.get("probe_digest")
    return EnvironmentFingerprint(
        adapter_name=record.adapter_name,
        base_build=base,
        data_version=dv,
        platform_string=platform,
        probe_digest=probe_digest,
        runtime_boundary_label=record.runtime_boundary_name,
    )


def validate_proof_config_alignment(cfg: MatchConfig, record: ExecutionProofRecord) -> None:
    """Raise if config and proof do not describe the same bounded run."""

    if cfg.adapter != record.adapter_name:
        msg = f"adapter mismatch: config={cfg.adapter!r} proof={record.adapter_name!r}"
        raise ValueError(msg)
    if cfg.seed != record.seed:
        msg = f"seed mismatch: config={cfg.seed} proof={record.seed}"
        raise ValueError(msg)
    if record.step_policy["max_game_steps"] != cfg.bounded_horizon.max_game_steps:
        msg = "bounded_horizon.max_game_steps does not match proof step_policy"
        raise ValueError(msg)
    if record.step_policy["game_step"] != cfg.bounded_horizon.game_step:
        msg = "bounded_horizon.game_step does not match proof step_policy"
        raise ValueError(msg)


def resolved_artifact_hash(record: ExecutionProofRecord) -> str:
    """M02 STARLAB hash of proof content (ignores any embedded artifact_hash field)."""

    return compute_artifact_hash(record)


def build_run_identity_mapping(
    *,
    cfg: MatchConfig,
    record: ExecutionProofRecord,
    proof_artifact_hash: str,
    env: EnvironmentFingerprint | None,
) -> dict[str, Any]:
    """``run_identity.json`` body (stable key order handled by writer)."""

    validate_proof_config_alignment(cfg, record)
    runtime_boundary = record.runtime_boundary_name
    rsid = compute_run_spec_id(cfg, runtime_boundary)
    eid = compute_execution_id(proof_artifact_hash)
    iface = {k: record.interface[k] for k in sorted(record.interface)}
    step_policy = {k: record.step_policy[k] for k in sorted(record.step_policy)}
    out: dict[str, Any] = {
        "adapter_name": record.adapter_name,
        "bounded_horizon": step_policy,
        "config_hash": compute_config_hash(cfg),
        "environment_fingerprint": None if env is None else env.to_mapping(),
        "execution_id": eid,
        "interface_summary": iface,
        "normalized_map_reference": record.map_logical_key,
        "proof_artifact_hash": proof_artifact_hash,
        "run_spec_id": rsid,
        "runtime_boundary_label": runtime_boundary,
        "schema_version": RUN_IDENTITY_SCHEMA_VERSION,
        "seed": record.seed,
    }
    return out


def build_lineage_seed_mapping(
    *,
    cfg: MatchConfig,
    record: ExecutionProofRecord,
    proof_artifact_hash: str,
    input_refs: list[ArtifactReference],
    artifact_refs: list[ArtifactReference],
) -> dict[str, Any]:
    """``lineage_seed.json`` body."""

    validate_proof_config_alignment(cfg, record)
    runtime_boundary = record.runtime_boundary_name
    ch = compute_config_hash(cfg)
    rsid = compute_run_spec_id(cfg, runtime_boundary)
    eid = compute_execution_id(proof_artifact_hash)
    lsid = compute_lineage_seed_id(
        config_hash=ch,
        execution_id=eid,
        proof_artifact_hash=proof_artifact_hash,
        run_spec_id=rsid,
    )
    return {
        "artifact_references": [r.to_mapping() for r in artifact_refs],
        "config_hash": ch,
        "execution_id": eid,
        "input_references": [r.to_mapping() for r in input_refs],
        "later_milestones": {
            "m04_replay_binding": ("Replay file hash and binding hooks may attach here."),
            "m05_canonical_run_artifact": (
                "Canonical run artifact v0 may supersede or wrap this seed."
            ),
        },
        "lineage_seed_id": lsid,
        "parent_references": [],
        "proof_artifact_hash": proof_artifact_hash,
        "run_spec_id": rsid,
        "schema_version": LINEAGE_SEED_SCHEMA_VERSION,
    }
