"""M03 run identity and lineage seed — STARLAB-owned; not canonical run artifact (M05)."""

from __future__ import annotations

from starlab.runs.identity import (
    compute_config_hash,
    compute_execution_id,
    compute_lineage_seed_id,
    compute_run_spec_id,
    normalize_match_config_for_identity,
)
from starlab.runs.lineage import (
    build_lineage_seed_mapping,
    build_run_identity_mapping,
    environment_fingerprint_from_proof_and_env,
    resolved_artifact_hash,
    validate_proof_config_alignment,
)
from starlab.runs.models import (
    LINEAGE_SEED_SCHEMA_VERSION,
    RUN_IDENTITY_SCHEMA_VERSION,
    ArtifactReference,
    EnvironmentFingerprint,
)
from starlab.runs.writer import lineage_seed_to_json, run_identity_to_json, write_json_record

__all__ = [
    "RUN_IDENTITY_SCHEMA_VERSION",
    "LINEAGE_SEED_SCHEMA_VERSION",
    "ArtifactReference",
    "EnvironmentFingerprint",
    "build_lineage_seed_mapping",
    "build_run_identity_mapping",
    "compute_config_hash",
    "compute_execution_id",
    "compute_lineage_seed_id",
    "compute_run_spec_id",
    "environment_fingerprint_from_proof_and_env",
    "lineage_seed_to_json",
    "normalize_match_config_for_identity",
    "resolved_artifact_hash",
    "run_identity_to_json",
    "validate_proof_config_alignment",
    "write_json_record",
]
