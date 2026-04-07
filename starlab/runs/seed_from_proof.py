"""CLI: derive M03 ``run_identity.json`` and ``lineage_seed.json`` from M02 proof + config."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from starlab.runs.lineage import (
    build_lineage_seed_mapping,
    build_run_identity_mapping,
    environment_fingerprint_from_proof_and_env,
    resolved_artifact_hash,
    validate_proof_config_alignment,
)
from starlab.runs.models import ArtifactReference
from starlab.runs.writer import write_json_record
from starlab.sc2.artifacts import parse_execution_proof_mapping
from starlab.sc2.match_config import load_match_config


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _load_proof_mapping(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = "proof root must be a JSON object"
        raise ValueError(msg)
    return data


def _load_env_optional(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = "env JSON root must be an object"
        raise ValueError(msg)
    return data


def build_seed_from_paths(
    *,
    proof_path: Path,
    config_path: Path,
    env_path: Path | None,
    include_fingerprint: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load config + proof and return ``(run_identity, lineage_seed)`` mappings."""

    proof_mapping = _load_proof_mapping(proof_path)
    record = parse_execution_proof_mapping(proof_mapping)
    cfg = load_match_config(config_path)
    validate_proof_config_alignment(cfg, record)
    computed_hash = resolved_artifact_hash(record)
    embedded = proof_mapping.get("artifact_hash")
    if embedded is not None and str(embedded) != computed_hash:
        msg = "proof artifact_hash does not match recomputed STARLAB hash"
        raise ValueError(msg)
    proof_hash = computed_hash
    env_file = _load_env_optional(env_path)
    env = (
        environment_fingerprint_from_proof_and_env(record, env_file)
        if include_fingerprint
        else None
    )
    run_identity = build_run_identity_mapping(
        cfg=cfg,
        env=env,
        proof_artifact_hash=proof_hash,
        record=record,
    )
    proof_digest = _sha256_file(proof_path)
    config_digest = _sha256_file(config_path)
    input_refs = [
        ArtifactReference(
            content_sha256=config_digest,
            logical_name="match_config",
            path=str(config_path),
            role="config",
        ),
        ArtifactReference(
            content_sha256=proof_digest,
            logical_name="match_execution_proof",
            path=str(proof_path),
            role="proof",
        ),
    ]
    artifact_refs = [
        ArtifactReference(logical_name="run_identity.json", role="artifact"),
        ArtifactReference(logical_name="lineage_seed.json", role="artifact"),
    ]
    lineage = build_lineage_seed_mapping(
        artifact_refs=artifact_refs,
        cfg=cfg,
        input_refs=input_refs,
        proof_artifact_hash=proof_hash,
        record=record,
    )
    return run_identity, lineage


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Derive M03 run_identity.json and lineage_seed.json from M02 proof + config.",
    )
    parser.add_argument(
        "--proof", required=True, type=Path, help="Path to match_execution_proof.json"
    )
    parser.add_argument("--config", required=True, type=Path, help="Path to match config JSON")
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory to write run_identity.json and lineage_seed.json",
    )
    parser.add_argument(
        "--env-json",
        type=Path,
        default=None,
        help="Optional JSON with base_build, data_version, platform_string, probe_digest overrides",
    )
    parser.add_argument(
        "--no-environment-fingerprint",
        action="store_true",
        help="Omit environment_fingerprint from run_identity (default: include)",
    )
    args = parser.parse_args(argv)
    include_fp = not args.no_environment_fingerprint
    run_identity, lineage = build_seed_from_paths(
        config_path=args.config,
        env_path=args.env_json,
        include_fingerprint=include_fp,
        proof_path=args.proof,
    )
    out_dir = args.output_dir
    write_json_record(out_dir / "run_identity.json", run_identity)
    write_json_record(out_dir / "lineage_seed.json", lineage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
