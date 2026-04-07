"""Deterministic replay binding to M03 run identity / lineage seed (M04).

Treats replay input as opaque bytes. Does not parse .SC2Replay semantics.
Does not claim canonical run artifact v0 (M05) or benchmark validity.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

REPLAY_BINDING_SCHEMA_VERSION = "starlab.replay_binding.v1"
REPLAY_BINDING_KIND = "starlab.replay_binding.v1"
BINDING_MODE = "opaque_content_sha256"

LATER_MILESTONES = [
    "M05 canonical run artifact v0",
    "M08 replay parser substrate",
]


def compute_replay_content_sha256(replay_path: Path) -> str:
    """SHA-256 hex of replay file bytes (opaque, no parsing)."""

    h = hashlib.sha256()
    h.update(replay_path.read_bytes())
    return h.hexdigest()


def build_replay_reference(replay_path: Path) -> dict[str, Any]:
    """Human-readable replay metadata (not part of identity hash)."""

    return {
        "basename": replay_path.name,
        "size_bytes": replay_path.stat().st_size,
        "suffix": replay_path.suffix,
    }


def compute_replay_binding_id(
    *,
    run_spec_id: str,
    execution_id: str,
    lineage_seed_id: str,
    proof_artifact_hash: str,
    replay_content_sha256: str,
) -> str:
    """Deterministic binding ID from M03 identities + replay content hash."""

    payload = {
        "execution_id": execution_id,
        "kind": REPLAY_BINDING_KIND,
        "lineage_seed_id": lineage_seed_id,
        "proof_artifact_hash": proof_artifact_hash,
        "replay_content_sha256": replay_content_sha256,
        "run_spec_id": run_spec_id,
    }
    return sha256_hex_of_canonical_json(payload)


def build_replay_binding_record(
    *,
    run_spec_id: str,
    execution_id: str,
    lineage_seed_id: str,
    proof_artifact_hash: str,
    replay_content_sha256: str,
    replay_reference: dict[str, Any],
) -> dict[str, Any]:
    """Full ``replay_binding.json`` body."""

    binding_id = compute_replay_binding_id(
        execution_id=execution_id,
        lineage_seed_id=lineage_seed_id,
        proof_artifact_hash=proof_artifact_hash,
        replay_content_sha256=replay_content_sha256,
        run_spec_id=run_spec_id,
    )
    return {
        "binding_mode": BINDING_MODE,
        "execution_id": execution_id,
        "later_milestones": list(LATER_MILESTONES),
        "lineage_seed_id": lineage_seed_id,
        "parent_references": [],
        "proof_artifact_hash": proof_artifact_hash,
        "replay_binding_id": binding_id,
        "replay_content_sha256": replay_content_sha256,
        "replay_reference": replay_reference,
        "run_spec_id": run_spec_id,
        "schema_version": REPLAY_BINDING_SCHEMA_VERSION,
    }


def load_run_identity(path: Path) -> dict[str, Any]:
    """Load and validate M03 ``run_identity.json``."""

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = "run_identity.json root must be a JSON object"
        raise ValueError(msg)
    for key in ("run_spec_id", "execution_id", "proof_artifact_hash", "schema_version"):
        if key not in data:
            msg = f"run_identity.json missing required field: {key}"
            raise ValueError(msg)
    if data["schema_version"] != "starlab.run_identity.v1":
        msg = f"unexpected run_identity schema_version: {data['schema_version']}"
        raise ValueError(msg)
    return data


def load_lineage_seed(path: Path) -> dict[str, Any]:
    """Load and validate M03 ``lineage_seed.json``."""

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = "lineage_seed.json root must be a JSON object"
        raise ValueError(msg)
    for key in ("lineage_seed_id", "schema_version"):
        if key not in data:
            msg = f"lineage_seed.json missing required field: {key}"
            raise ValueError(msg)
    if data["schema_version"] != "starlab.lineage_seed.v1":
        msg = f"unexpected lineage_seed schema_version: {data['schema_version']}"
        raise ValueError(msg)
    return data


def write_replay_binding(output_dir: Path, record: dict[str, Any]) -> Path:
    """Write deterministic ``replay_binding.json`` with trailing newline."""

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "replay_binding.json"
    out_path.write_text(canonical_json_dumps(record), encoding="utf-8")
    return out_path
