"""Deterministic run spec, execution, and lineage seed identities (M03)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.runs.models import (
    EXECUTION_KIND,
    LINEAGE_SEED_KIND,
    RUN_SPEC_KIND,
)
from starlab.sc2.match_config import (
    BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY,
    BURNYSC2_DEFAULT_OPPONENT_MODE,
    BURNYSC2_DEFAULT_SUPPRESS_ATTACK,
    BURNYSC2_POLICY_PASSIVE,
    MatchConfig,
)


def _posix_path_name_for_identity(pathish: str) -> str:
    """Basename stable on all OSes (Windows paths may appear in configs on Linux CI)."""

    return Path(pathish.replace("\\", "/")).name


def normalize_map_spec_for_identity(cfg: MatchConfig) -> dict[str, Any]:
    """Path-stable map selection for hashing (no host absolute paths)."""

    m = cfg.map
    if m.discover_under_maps_dir:
        return {"mode": "discover_under_maps_dir"}
    if m.battle_net_map_name is not None:
        return {"battle_net_map_name": m.battle_net_map_name, "mode": "battle_net"}
    if m.path is not None:
        return {"basename": _posix_path_name_for_identity(m.path), "mode": "path"}
    raise ValueError("map selection is incomplete")


def normalize_match_config_for_identity(cfg: MatchConfig) -> dict[str, Any]:
    """Stable dict for config_hash and run_spec (no timestamps, path-stable)."""

    iface = cfg.interface
    replay_filename: str | None = None
    if cfg.replay_filename:
        replay_filename = _posix_path_name_for_identity(cfg.replay_filename)
    out: dict[str, Any] = {
        "adapter": cfg.adapter,
        "bounded_horizon": {
            "game_step": cfg.bounded_horizon.game_step,
            "max_game_steps": cfg.bounded_horizon.max_game_steps,
        },
        "interface": {
            "feature_layer_interface": iface.feature_layer_interface,
            "raw_interface": iface.raw_interface,
            "rendered_interface": iface.rendered_interface,
            "score_interface": iface.score_interface,
        },
        "map": normalize_map_spec_for_identity(cfg),
        "replay_filename": replay_filename,
        "save_replay": cfg.save_replay,
        "schema_version": cfg.schema_version,
        "seed": cfg.seed,
    }
    if cfg.computer_difficulty != BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY:
        out["computer_difficulty"] = cfg.computer_difficulty
    if cfg.opponent_mode != BURNYSC2_DEFAULT_OPPONENT_MODE:
        out["opponent_mode"] = cfg.opponent_mode
    if cfg.burnysc2_suppress_attack != BURNYSC2_DEFAULT_SUPPRESS_ATTACK:
        out["burnysc2_suppress_attack"] = cfg.burnysc2_suppress_attack
    if cfg.adapter == "burnysc2" and cfg.burnysc2_policy != BURNYSC2_POLICY_PASSIVE:
        out["burnysc2_policy"] = cfg.burnysc2_policy
    return out


def compute_config_hash(cfg: MatchConfig) -> str:
    """SHA-256 hex of normalized match config identity (sorted JSON)."""

    return sha256_hex_of_canonical_json(normalize_match_config_for_identity(cfg))


def compute_run_spec_id(cfg: MatchConfig, runtime_boundary_label: str) -> str:
    """Deterministic run spec identity for intended run shape + boundary."""

    payload = {
        "kind": RUN_SPEC_KIND,
        "match_config": normalize_match_config_for_identity(cfg),
        "runtime_boundary_label": runtime_boundary_label,
    }
    return sha256_hex_of_canonical_json(payload)


def compute_execution_id(artifact_hash: str) -> str:
    """Execution identity from STARLAB M02 ``artifact_hash`` (distinct from raw hash string)."""

    payload = {
        "artifact_hash": artifact_hash,
        "kind": EXECUTION_KIND,
    }
    return sha256_hex_of_canonical_json(payload)


def compute_lineage_seed_id(
    *,
    run_spec_id: str,
    execution_id: str,
    config_hash: str,
    proof_artifact_hash: str,
) -> str:
    """Linkage record identity tying run spec to execution (M03 seed)."""

    payload = {
        "config_hash": config_hash,
        "execution_id": execution_id,
        "kind": LINEAGE_SEED_KIND,
        "proof_artifact_hash": proof_artifact_hash,
        "run_spec_id": run_spec_id,
    }
    return sha256_hex_of_canonical_json(payload)
