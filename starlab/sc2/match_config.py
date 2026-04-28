"""M02 match configuration — STARLAB-owned, wrapper-agnostic."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class InterfaceConfig:
    """Observation interface selection for proof artifacts (M02 default: raw + score only)."""

    raw_interface: bool = True
    score_interface: bool = True
    feature_layer_interface: bool = False
    rendered_interface: bool = False


@dataclass(frozen=True, slots=True)
class BoundedHorizon:
    max_game_steps: int = 100
    game_step: int = 1


@dataclass(frozen=True, slots=True)
class MapSpec:
    """Map selection: explicit path, discovery, or Battle.net name (optional)."""

    path: str | None = None
    discover_under_maps_dir: bool = False
    battle_net_map_name: str | None = None


# BurnySc2 live policy: default passive harness; PX1-M03 hybrid = Terran scaffold + M43.
BURNYSC2_POLICY_PASSIVE = "passive"
BURNYSC2_POLICY_PX1_M03_HYBRID_V1 = "px1_m03_hybrid_v1"
# Scripted watchability/demo — no M43 runtime; sandbox-only (see px1_watchability_macro_scout_bot).
BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1 = "px1_watchability_macro_scout_v1"
# V15-M27 governed ID — implementation reuses PX1 watchability Terran scaffold (same action path).
BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1 = "v15_m27_nontrivial_macro_smoke_policy_v1"

# BurnySc2: python-sc2 `sc2.data.Difficulty` member names (VeryEasy, Easy, Medium, Hard).
BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY = "Easy"
BURNYSC2_COMPUTER_DIFFICULTY_VALUES: tuple[str, ...] = (
    "VeryEasy",
    "Easy",
    "Medium",
    "Hard",
)

# BurnySc2 opponent: built-in `Computer` AI (default) vs idle second `Bot` for watchability smokes.
BURNYSC2_DEFAULT_OPPONENT_MODE = "computer"
BURNYSC2_OPPONENT_MODE_PASSIVE_BOT = "passive_bot"
BURNYSC2_OPPONENT_MODES: tuple[str, ...] = (
    BURNYSC2_DEFAULT_OPPONENT_MODE,
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
)

# PX1-M03 hybrid: optional watchability — disable marine attack-move (default off).
BURNYSC2_DEFAULT_SUPPRESS_ATTACK = False


@dataclass(frozen=True, slots=True)
class MatchConfig:
    """Bounded harness configuration."""

    schema_version: str
    adapter: str
    seed: int
    bounded_horizon: BoundedHorizon
    map: MapSpec
    interface: InterfaceConfig = field(default_factory=InterfaceConfig)
    save_replay: bool = False
    replay_filename: str | None = None
    burnysc2_policy: str = BURNYSC2_POLICY_PASSIVE
    # BurnySc2 `Computer` opponent: maps to `sc2.data.Difficulty` by name (default matches legacy).
    computer_difficulty: str = BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY
    # BurnySc2: `computer` = built-in AI; `passive_bot` = idle second bot (watchability only).
    opponent_mode: str = BURNYSC2_DEFAULT_OPPONENT_MODE
    # BurnySc2 hybrid only: suppress marine attack-move for operator-local watchability smokes.
    burnysc2_suppress_attack: bool = BURNYSC2_DEFAULT_SUPPRESS_ATTACK

    def validate(self) -> None:
        if self.schema_version != "1":
            raise ValueError(f"unsupported schema_version: {self.schema_version!r}")
        if self.adapter not in {"fake", "burnysc2"}:
            raise ValueError(f"unsupported adapter: {self.adapter!r}")
        if self.burnysc2_policy not in {
            BURNYSC2_POLICY_PASSIVE,
            BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
            BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
            BURNYSC2_POLICY_V15_M27_NONTRIVIAL_MACRO_SMOKE_V1,
        }:
            raise ValueError(f"unsupported burnysc2_policy: {self.burnysc2_policy!r}")
        if self.adapter != "burnysc2" and self.burnysc2_policy != BURNYSC2_POLICY_PASSIVE:
            raise ValueError("burnysc2_policy may only be set when adapter is burnysc2")
        if self.bounded_horizon.max_game_steps < 1:
            raise ValueError("bounded_horizon.max_game_steps must be >= 1")
        if self.bounded_horizon.game_step < 1:
            raise ValueError("bounded_horizon.game_step must be >= 1")
        opts = [
            self.map.path is not None,
            self.map.discover_under_maps_dir,
            self.map.battle_net_map_name is not None,
        ]
        if sum(1 for o in opts if o) != 1:
            raise ValueError(
                "map selection must set exactly one of: path, discover_under_maps_dir, "
                "battle_net_map_name",
            )
        if self.computer_difficulty not in BURNYSC2_COMPUTER_DIFFICULTY_VALUES:
            allowed = ", ".join(BURNYSC2_COMPUTER_DIFFICULTY_VALUES)
            bad = self.computer_difficulty
            raise ValueError(
                f"unsupported computer_difficulty: {bad!r}; allowed: {allowed}",
            )
        if self.opponent_mode not in BURNYSC2_OPPONENT_MODES:
            oam = ", ".join(BURNYSC2_OPPONENT_MODES)
            raise ValueError(
                f"unsupported opponent_mode: {self.opponent_mode!r}; allowed: {oam}",
            )
        if self.burnysc2_suppress_attack:
            if self.adapter != "burnysc2":
                raise ValueError(
                    "burnysc2_suppress_attack may only be set when adapter is burnysc2",
                )
            if self.burnysc2_policy != BURNYSC2_POLICY_PX1_M03_HYBRID_V1:
                raise ValueError(
                    "burnysc2_suppress_attack requires burnysc2_policy 'px1_m03_hybrid_v1'",
                )


def _bounded_from_json(data: dict[str, Any]) -> BoundedHorizon:
    b = data.get("bounded_horizon") or {}
    return BoundedHorizon(
        max_game_steps=int(b.get("max_game_steps", 100)),
        game_step=int(b.get("game_step", 1)),
    )


def _map_from_json(data: dict[str, Any]) -> MapSpec:
    m = data.get("map") or {}
    path = m.get("path")
    discover = bool(m.get("discover_under_maps_dir", False))
    bn = m.get("battle_net_map_name")
    return MapSpec(
        path=str(path) if path is not None else None,
        discover_under_maps_dir=discover,
        battle_net_map_name=str(bn) if bn is not None else None,
    )


def _iface_from_json(data: dict[str, Any]) -> InterfaceConfig:
    i = data.get("interface") or {}
    return InterfaceConfig(
        raw_interface=bool(i.get("raw_interface", True)),
        score_interface=bool(i.get("score_interface", True)),
        feature_layer_interface=bool(i.get("feature_layer_interface", False)),
        rendered_interface=bool(i.get("rendered_interface", False)),
    )


def _computer_difficulty_from_json(data: dict[str, Any]) -> str:
    raw = data.get("computer_difficulty", BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY)
    if not isinstance(raw, str):
        msg = f"computer_difficulty must be a string, got {type(raw).__name__}"
        raise ValueError(msg)
    return raw


def _opponent_mode_from_json(data: dict[str, Any]) -> str:
    raw = data.get("opponent_mode", BURNYSC2_DEFAULT_OPPONENT_MODE)
    if not isinstance(raw, str):
        msg = f"opponent_mode must be a string, got {type(raw).__name__}"
        raise ValueError(msg)
    return raw


def _burnysc2_suppress_attack_from_json(data: dict[str, Any]) -> bool:
    raw = data.get("burnysc2_suppress_attack", BURNYSC2_DEFAULT_SUPPRESS_ATTACK)
    if not isinstance(raw, bool):
        msg = f"burnysc2_suppress_attack must be a boolean, got {type(raw).__name__}"
        raise ValueError(msg)
    return raw


def match_config_from_mapping(data: dict[str, Any]) -> MatchConfig:
    """Parse and validate a match config dict (typically from JSON)."""

    bpol = str(data.get("burnysc2_policy", BURNYSC2_POLICY_PASSIVE))
    cfg = MatchConfig(
        schema_version=str(data.get("schema_version", "1")),
        adapter=str(data["adapter"]),
        seed=int(data["seed"]),
        bounded_horizon=_bounded_from_json(data),
        map=_map_from_json(data),
        interface=_iface_from_json(data),
        save_replay=bool(data.get("save_replay", False)),
        replay_filename=data.get("replay_filename"),
        burnysc2_policy=bpol,
        computer_difficulty=_computer_difficulty_from_json(data),
        opponent_mode=_opponent_mode_from_json(data),
        burnysc2_suppress_attack=_burnysc2_suppress_attack_from_json(data),
    )
    cfg.validate()
    return cfg


def load_match_config(path: Path) -> MatchConfig:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("config root must be a JSON object")
    return match_config_from_mapping(data)


def match_config_to_mapping(cfg: MatchConfig) -> dict[str, Any]:
    """Deterministic JSON-serializable dict for configs."""

    out: dict[str, Any] = {
        "adapter": cfg.adapter,
        "bounded_horizon": {
            "game_step": cfg.bounded_horizon.game_step,
            "max_game_steps": cfg.bounded_horizon.max_game_steps,
        },
        "interface": {
            "feature_layer_interface": cfg.interface.feature_layer_interface,
            "raw_interface": cfg.interface.raw_interface,
            "rendered_interface": cfg.interface.rendered_interface,
            "score_interface": cfg.interface.score_interface,
        },
        "map": {},
        "replay_filename": cfg.replay_filename,
        "save_replay": cfg.save_replay,
        "schema_version": cfg.schema_version,
        "seed": cfg.seed,
    }
    m: dict[str, Any] = {}
    if cfg.map.path is not None:
        m["path"] = cfg.map.path
    if cfg.map.discover_under_maps_dir:
        m["discover_under_maps_dir"] = True
    if cfg.map.battle_net_map_name is not None:
        m["battle_net_map_name"] = cfg.map.battle_net_map_name
    out["map"] = m
    if cfg.burnysc2_policy != BURNYSC2_POLICY_PASSIVE:
        out["burnysc2_policy"] = cfg.burnysc2_policy
    if cfg.computer_difficulty != BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY:
        out["computer_difficulty"] = cfg.computer_difficulty
    if cfg.opponent_mode != BURNYSC2_DEFAULT_OPPONENT_MODE:
        out["opponent_mode"] = cfg.opponent_mode
    if cfg.burnysc2_suppress_attack:
        out["burnysc2_suppress_attack"] = True
    return out
