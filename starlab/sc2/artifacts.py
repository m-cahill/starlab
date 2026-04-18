"""STARLAB execution proof artifact (M02) — not the canonical run artifact (M05)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

PROOF_SCHEMA_VERSION = "match_execution_proof.v1"


@dataclass(frozen=True, slots=True)
class ReplayMetadata:
    replay_saved: bool
    replay_file_name: str | None = None
    replay_file_sha256: str | None = None
    note: str | None = None


@dataclass(frozen=True, slots=True)
class ExecutionProofRecord:
    """Normalized fields for ``match_execution_proof.json`` (hash excludes ``artifact_hash``)."""

    schema_version: str
    adapter_name: str
    runtime_boundary_name: str
    base_build: str | None
    data_version: str | None
    map_logical_key: str
    map_resolution: str
    seed: int
    interface: dict[str, bool]
    step_policy: dict[str, int]
    status_sequence: tuple[str, ...]
    observation_summaries: tuple[dict[str, int], ...]
    action_count: int
    final_status: str
    replay: ReplayMetadata | None
    sc2_game_result: str | None = None
    artifact_hash: str | None = None
    live_action_tallies: Mapping[str, int] | None = None
    live_action_behavior_summary: Mapping[str, Any] | None = None


def _sorted_json(obj: Any) -> str:
    dumped = json.dumps(
        obj,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return dumped + "\n"


def proof_record_to_hash_input_dict(record: ExecutionProofRecord) -> dict[str, Any]:
    """Mapping used for deterministic hashing (excludes ``artifact_hash``)."""

    replay_out: dict[str, Any] | None = None
    if record.replay is not None:
        replay_out = {
            "note": record.replay.note,
            "replay_file_name": record.replay.replay_file_name,
            "replay_file_sha256": record.replay.replay_file_sha256,
            "replay_saved": record.replay.replay_saved,
        }

    summaries_sorted = [
        {k: int(obs[k]) for k in sorted(obs)} for obs in record.observation_summaries
    ]
    out: dict[str, Any] = {
        "action_count": record.action_count,
        "adapter_name": record.adapter_name,
        "base_build": record.base_build,
        "data_version": record.data_version,
        "final_status": record.final_status,
        "interface": {k: record.interface[k] for k in sorted(record.interface)},
        "map_logical_key": record.map_logical_key,
        "map_resolution": record.map_resolution,
        "observation_summaries": summaries_sorted,
        "replay": replay_out,
        "runtime_boundary_name": record.runtime_boundary_name,
        "schema_version": record.schema_version,
        "seed": record.seed,
        "status_sequence": list(record.status_sequence),
        "step_policy": {k: record.step_policy[k] for k in sorted(record.step_policy)},
    }
    if record.sc2_game_result is not None:
        out["sc2_game_result"] = record.sc2_game_result
    if record.live_action_tallies:
        lat = record.live_action_tallies
        out["live_action_tallies"] = {k: int(lat[k]) for k in sorted(lat)}
    if record.live_action_behavior_summary:
        lbs = record.live_action_behavior_summary
        out["live_action_behavior_summary"] = {k: lbs[k] for k in sorted(lbs)}
    return out


def compute_artifact_hash(record: ExecutionProofRecord) -> str:
    """SHA-256 over canonical JSON of the record without ``artifact_hash``."""

    base = proof_record_to_hash_input_dict(record)
    payload = _sorted_json(base)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def execution_proof_to_json(record: ExecutionProofRecord, *, redact: bool = False) -> str:
    """Serialize proof record; when ``redact``, strip volatile replay path details."""

    d = proof_record_to_hash_input_dict(record)
    h = compute_artifact_hash(record)
    d["artifact_hash"] = h
    if redact and d.get("replay") and isinstance(d["replay"], dict):
        r = dict(d["replay"])
        if r.get("replay_file_name"):
            r["replay_file_name"] = "<redacted>"
        d["replay"] = r
    return _sorted_json(d)


def parse_execution_proof_mapping(data: dict[str, Any]) -> ExecutionProofRecord:
    """Parse a proof JSON object (e.g. for tests)."""

    iface = data["interface"]
    summaries = tuple(dict(x) for x in data.get("observation_summaries", []))
    replay_raw = data.get("replay")
    replay: ReplayMetadata | None = None
    if isinstance(replay_raw, dict):
        replay = ReplayMetadata(
            replay_saved=bool(replay_raw.get("replay_saved", False)),
            replay_file_name=replay_raw.get("replay_file_name"),
            replay_file_sha256=replay_raw.get("replay_file_sha256"),
            note=replay_raw.get("note"),
        )
    sgr = data.get("sc2_game_result")
    lat_raw = data.get("live_action_tallies")
    lat: dict[str, int] | None = None
    if isinstance(lat_raw, dict):
        lat = {str(k): int(v) for k, v in lat_raw.items()}
    lbs_raw = data.get("live_action_behavior_summary")
    lbs: dict[str, Any] | None = None
    if isinstance(lbs_raw, dict):
        lbs = dict(lbs_raw)
    return ExecutionProofRecord(
        schema_version=str(data["schema_version"]),
        adapter_name=str(data["adapter_name"]),
        runtime_boundary_name=str(data["runtime_boundary_name"]),
        base_build=data.get("base_build"),
        data_version=data.get("data_version"),
        map_logical_key=str(data["map_logical_key"]),
        map_resolution=str(data["map_resolution"]),
        seed=int(data["seed"]),
        interface={k: bool(v) for k, v in iface.items()},
        step_policy={k: int(v) for k, v in data["step_policy"].items()},
        status_sequence=tuple(str(x) for x in data["status_sequence"]),
        observation_summaries=summaries,
        action_count=int(data["action_count"]),
        final_status=str(data["final_status"]),
        replay=replay,
        sc2_game_result=str(sgr) if sgr is not None else None,
        artifact_hash=data.get("artifact_hash"),
        live_action_tallies=lat,
        live_action_behavior_summary=lbs,
    )
