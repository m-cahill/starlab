"""Canonical run artifact v0 — deterministic bundle of M03 + M04 STARLAB records (M05).

Does not include raw replay bytes or raw proof/config. Does not claim parser semantics.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.runs.replay_binding import (
    BINDING_MODE,
    load_lineage_seed,
    load_replay_binding,
    load_run_identity,
)
from starlab.runs.writer import write_json_record

CANONICAL_RUN_ARTIFACT_SCHEMA_VERSION = "starlab.canonical_run_artifact.v0"
CANONICAL_RUN_ARTIFACT_HASHES_SCHEMA_VERSION = "starlab.canonical_run_artifact.hashes.v0"
BUNDLE_MODE = "starlab_owned_records_only"
RUN_ARTIFACT_KIND = "starlab.canonical_run_artifact.v0"

# Fixed package shape: order is part of the contract (guardrail against silent drift).
INCLUDED_ARTIFACTS: tuple[str, ...] = (
    "run_identity.json",
    "lineage_seed.json",
    "replay_binding.json",
)

LATER_MILESTONES = [
    "M06 environment drift & runtime smoke matrix",
    "M07 replay intake policy & provenance enforcement",
    "M08 replay parser substrate",
]


def validate_included_artifacts(names: list[str]) -> None:
    """Reject manifest lists that drift from the canonical v0 package shape."""

    if names != list(INCLUDED_ARTIFACTS):
        msg = (
            "included_artifacts must match the canonical M05 v0 list exactly "
            f"(order-sensitive): {list(INCLUDED_ARTIFACTS)!r}; got {names!r}"
        )
        raise ValueError(msg)


def validate_upstream_coherence(
    *,
    run_identity: dict[str, Any],
    lineage_seed: dict[str, Any],
    replay_binding: dict[str, Any],
) -> None:
    """Fail fast if M03/M04 records disagree on shared identity fields."""

    rs_ri = run_identity["run_spec_id"]
    rs_ls = lineage_seed["run_spec_id"]
    rs_rb = replay_binding["run_spec_id"]
    if rs_ri != rs_ls or rs_ri != rs_rb:
        msg = (
            "run_spec_id mismatch across artifacts: "
            f"run_identity={rs_ri!r}, lineage_seed={rs_ls!r}, replay_binding={rs_rb!r}"
        )
        raise ValueError(msg)

    ex_ri = run_identity["execution_id"]
    ex_ls = lineage_seed["execution_id"]
    ex_rb = replay_binding["execution_id"]
    if ex_ri != ex_ls or ex_ri != ex_rb:
        msg = (
            "execution_id mismatch across artifacts: "
            f"run_identity={ex_ri!r}, lineage_seed={ex_ls!r}, replay_binding={ex_rb!r}"
        )
        raise ValueError(msg)

    lsid_ls = lineage_seed["lineage_seed_id"]
    lsid_rb = replay_binding["lineage_seed_id"]
    if lsid_ls != lsid_rb:
        msg = f"lineage_seed_id mismatch: lineage_seed={lsid_ls!r}, replay_binding={lsid_rb!r}"
        raise ValueError(msg)

    ph_ri = run_identity["proof_artifact_hash"]
    ph_ls = lineage_seed["proof_artifact_hash"]
    ph_rb = replay_binding["proof_artifact_hash"]
    if ph_ri != ph_ls or ph_ri != ph_rb:
        msg = (
            "proof_artifact_hash mismatch across artifacts: "
            f"run_identity={ph_ri!r}, lineage_seed={ph_ls!r}, replay_binding={ph_rb!r}"
        )
        raise ValueError(msg)

    if replay_binding["binding_mode"] != BINDING_MODE:
        msg = f"replay_binding binding_mode must be {BINDING_MODE!r}"
        raise ValueError(msg)


def build_manifest_mapping(
    *,
    run_identity: dict[str, Any],
    lineage_seed: dict[str, Any],
    replay_binding: dict[str, Any],
) -> dict[str, Any]:
    """Minimum ``manifest.json`` body for canonical run artifact v0."""

    included = list(INCLUDED_ARTIFACTS)
    validate_included_artifacts(included)
    return {
        "bundle_mode": BUNDLE_MODE,
        "execution_id": run_identity["execution_id"],
        "external_references": {
            "proof_json_included": False,
            "replay_bytes_included": False,
        },
        "included_artifacts": included,
        "later_milestones": list(LATER_MILESTONES),
        "lineage_seed_id": lineage_seed["lineage_seed_id"],
        "parent_references": [],
        "proof_artifact_hash": run_identity["proof_artifact_hash"],
        "replay_binding_id": replay_binding["replay_binding_id"],
        "replay_content_sha256": replay_binding["replay_content_sha256"],
        "run_spec_id": run_identity["run_spec_id"],
        "schema_version": CANONICAL_RUN_ARTIFACT_SCHEMA_VERSION,
    }


def compute_artifact_hashes(
    *,
    run_identity: dict[str, Any],
    lineage_seed: dict[str, Any],
    replay_binding: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, str]:
    """Per-file SHA-256 (hex) over compact canonical JSON for each emitted object."""

    return {
        "lineage_seed.json": sha256_hex_of_canonical_json(lineage_seed),
        "manifest.json": sha256_hex_of_canonical_json(manifest),
        "replay_binding.json": sha256_hex_of_canonical_json(replay_binding),
        "run_identity.json": sha256_hex_of_canonical_json(run_identity),
    }


def compute_run_artifact_id(*, artifact_hashes: dict[str, str]) -> str:
    """Content-addressed bundle id (excludes ``hashes.json``)."""

    payload = {
        "artifact_hashes": {k: artifact_hashes[k] for k in sorted(artifact_hashes)},
        "kind": RUN_ARTIFACT_KIND,
    }
    return sha256_hex_of_canonical_json(payload)


def build_hashes_mapping(*, artifact_hashes: dict[str, str]) -> dict[str, Any]:
    """``hashes.json`` body."""

    run_artifact_id = compute_run_artifact_id(artifact_hashes=artifact_hashes)
    return {
        "artifact_hashes": {k: artifact_hashes[k] for k in sorted(artifact_hashes)},
        "run_artifact_id": run_artifact_id,
        "schema_version": CANONICAL_RUN_ARTIFACT_HASHES_SCHEMA_VERSION,
    }


def load_canonical_manifest(path: Path) -> dict[str, Any]:
    """Load and validate M05 ``manifest.json`` (canonical run artifact v0)."""

    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = "manifest.json root must be a JSON object"
        raise ValueError(msg)
    for key in (
        "bundle_mode",
        "execution_id",
        "external_references",
        "included_artifacts",
        "later_milestones",
        "lineage_seed_id",
        "parent_references",
        "proof_artifact_hash",
        "replay_binding_id",
        "replay_content_sha256",
        "run_spec_id",
        "schema_version",
    ):
        if key not in data:
            msg = f"manifest.json missing required field: {key}"
            raise ValueError(msg)
    if data["schema_version"] != CANONICAL_RUN_ARTIFACT_SCHEMA_VERSION:
        msg = f"unexpected manifest schema_version: {data['schema_version']}"
        raise ValueError(msg)
    if data["bundle_mode"] != BUNDLE_MODE:
        msg = f"manifest bundle_mode must be {BUNDLE_MODE!r}"
        raise ValueError(msg)
    validate_included_artifacts(list(data["included_artifacts"]))
    return data


def load_validated_upstream(
    *,
    run_identity_path: Path,
    lineage_seed_path: Path,
    replay_binding_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load M03/M04 JSON and validate schema + internal replay-binding coherence."""

    ri = load_run_identity(run_identity_path)
    ls = load_lineage_seed(lineage_seed_path)
    rb = load_replay_binding(replay_binding_path)
    validate_upstream_coherence(run_identity=ri, lineage_seed=ls, replay_binding=rb)
    return ri, ls, rb


def write_canonical_run_artifact_bundle(
    *,
    run_identity_path: Path,
    lineage_seed_path: Path,
    replay_binding_path: Path,
    output_dir: Path,
) -> None:
    """Write deterministic directory bundle: manifest, three upstream JSON files, hashes.

    ``output_dir`` must not exist (no overwrite semantics in M05).
    """

    if output_dir.exists():
        msg = f"refusing to write: output directory already exists: {output_dir}"
        raise ValueError(msg)

    ri, ls, rb = load_validated_upstream(
        lineage_seed_path=lineage_seed_path,
        replay_binding_path=replay_binding_path,
        run_identity_path=run_identity_path,
    )
    manifest = build_manifest_mapping(lineage_seed=ls, replay_binding=rb, run_identity=ri)
    validate_included_artifacts(manifest["included_artifacts"])

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_record(output_dir / "run_identity.json", ri)
    write_json_record(output_dir / "lineage_seed.json", ls)
    write_json_record(output_dir / "replay_binding.json", rb)
    write_json_record(output_dir / "manifest.json", manifest)

    artifact_hashes = compute_artifact_hashes(
        lineage_seed=ls,
        manifest=manifest,
        replay_binding=rb,
        run_identity=ri,
    )
    hashes_record = build_hashes_mapping(artifact_hashes=artifact_hashes)
    write_json_record(output_dir / "hashes.json", hashes_record)
