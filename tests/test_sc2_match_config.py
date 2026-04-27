"""Match config parsing and validation."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest
from starlab.runs.identity import compute_config_hash, normalize_match_config_for_identity
from starlab.sc2.match_config import (
    BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY,
    BURNYSC2_DEFAULT_OPPONENT_MODE,
    BURNYSC2_DEFAULT_SUPPRESS_ATTACK,
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    BURNYSC2_POLICY_PASSIVE,
    BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
    BoundedHorizon,
    MapSpec,
    MatchConfig,
    load_match_config,
    match_config_from_mapping,
    match_config_to_mapping,
)


def test_roundtrip_deterministic() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=1,
        bounded_horizon=BoundedHorizon(100, 1),
        map=MapSpec(discover_under_maps_dir=True),
    )
    m1 = match_config_to_mapping(cfg)
    m2 = match_config_to_mapping(cfg)
    assert json.dumps(m1, sort_keys=True) == json.dumps(m2, sort_keys=True)


def test_rejects_two_map_modes() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=1,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(path="/x.SC2Map", discover_under_maps_dir=True),
    )
    with pytest.raises(ValueError, match="exactly one"):
        cfg.validate()


def test_from_mapping_minimal() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "fake",
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 7,
        },
    )
    assert cfg.bounded_horizon.max_game_steps == 100
    assert cfg.computer_difficulty == BURNYSC2_DEFAULT_COMPUTER_DIFFICULTY
    assert cfg.opponent_mode == BURNYSC2_DEFAULT_OPPONENT_MODE
    assert cfg.burnysc2_suppress_attack is BURNYSC2_DEFAULT_SUPPRESS_ATTACK


def test_load_fixture() -> None:
    src = Path(__file__).resolve().parent / "fixtures" / "match_fake_m02.json"
    cfg = load_match_config(src)
    assert cfg.adapter == "fake"
    assert cfg.seed == 4242
    assert cfg.burnysc2_policy == BURNYSC2_POLICY_PASSIVE


def test_burnysc2_hybrid_policy_roundtrip() -> None:
    src = (
        Path(__file__).resolve().parents[1]
        / "tests/fixtures/px1_m03/match_opponent_profile_scripted_style_v2_hybrid.json"
    )
    cfg = load_match_config(src)
    assert cfg.adapter == "burnysc2"
    assert cfg.burnysc2_policy == BURNYSC2_POLICY_PX1_M03_HYBRID_V1
    m = match_config_to_mapping(cfg)
    assert m["burnysc2_policy"] == BURNYSC2_POLICY_PX1_M03_HYBRID_V1


def test_computer_difficulty_nondefault_roundtrip() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
            "computer_difficulty": "VeryEasy",
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 1,
        },
    )
    assert cfg.computer_difficulty == "VeryEasy"
    m = match_config_to_mapping(cfg)
    assert m["computer_difficulty"] == "VeryEasy"


@pytest.mark.parametrize(
    "difficulty",
    ["VeryEasy", "Easy", "Medium", "Hard"],
)
def test_computer_difficulty_allowed_values_parse(difficulty: str) -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
            "computer_difficulty": difficulty,
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 0,
        },
    )
    assert cfg.computer_difficulty == difficulty


def test_computer_difficulty_invalid_raises() -> None:
    with pytest.raises(ValueError, match="unsupported computer_difficulty"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "computer_difficulty": "CheatInsane",
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_computer_difficulty_wrong_type_raises() -> None:
    with pytest.raises(ValueError, match="computer_difficulty must be a string"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "computer_difficulty": 3,
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_match_config_to_mapping_omits_default_computer_difficulty() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="burnysc2",
        seed=1,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(discover_under_maps_dir=True),
    )
    m = match_config_to_mapping(cfg)
    assert "computer_difficulty" not in m


def test_normalize_identity_unchanged_for_default_difficulty() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "fake",
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 7,
        },
    )
    base = normalize_match_config_for_identity(cfg)
    assert "computer_difficulty" not in base


def test_normalize_and_config_hash_change_with_nondefault_difficulty() -> None:
    raw = {
        "adapter": "burnysc2",
        "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
        "map": {"discover_under_maps_dir": True},
        "schema_version": "1",
        "seed": 1,
    }
    easy_cfg = match_config_from_mapping(dict(raw))
    very_cfg = match_config_from_mapping({**raw, "computer_difficulty": "VeryEasy"})
    assert compute_config_hash(easy_cfg) != compute_config_hash(very_cfg)
    vnorm = normalize_match_config_for_identity(very_cfg)
    assert vnorm.get("computer_difficulty") == "VeryEasy"


def test_opponent_mode_computer_and_passive_parse() -> None:
    c1 = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
            "map": {"discover_under_maps_dir": True},
            "opponent_mode": "computer",
            "schema_version": "1",
            "seed": 0,
        },
    )
    assert c1.opponent_mode == "computer"
    c2 = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
            "map": {"discover_under_maps_dir": True},
            "opponent_mode": BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
            "schema_version": "1",
            "seed": 0,
        },
    )
    assert c2.opponent_mode == BURNYSC2_OPPONENT_MODE_PASSIVE_BOT


def test_opponent_mode_invalid_raises() -> None:
    with pytest.raises(ValueError, match="unsupported opponent_mode"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "map": {"discover_under_maps_dir": True},
                "opponent_mode": "cheat_insane",
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_opponent_mode_type_raises() -> None:
    with pytest.raises(ValueError, match="opponent_mode must be a string"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "map": {"discover_under_maps_dir": True},
                "opponent_mode": 1,
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_match_config_to_mapping_omits_default_opponent_mode() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="burnysc2",
        seed=1,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(discover_under_maps_dir=True),
    )
    m = match_config_to_mapping(cfg)
    assert "opponent_mode" not in m


def test_normalize_and_config_hash_change_with_opponent_mode_passive() -> None:
    raw = {
        "adapter": "burnysc2",
        "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
        "map": {"discover_under_maps_dir": True},
        "schema_version": "1",
        "seed": 1,
    }
    base = match_config_from_mapping(dict(raw))
    passive = match_config_from_mapping(
        {**raw, "opponent_mode": BURNYSC2_OPPONENT_MODE_PASSIVE_BOT},
    )
    assert compute_config_hash(base) != compute_config_hash(passive)
    pn = normalize_match_config_for_identity(passive)
    assert pn.get("opponent_mode") == BURNYSC2_OPPONENT_MODE_PASSIVE_BOT


def test_burnysc2_computer_difficulty_names_exist_in_sc2_enum() -> None:
    """Maps config strings to python-sc2 ``Difficulty`` (optional dep; skipped in CI)."""

    pytest.importorskip("sc2", reason="python-sc2 not installed")
    difficulty_cls = importlib.import_module("sc2.data").Difficulty
    for name in ("VeryEasy", "Easy", "Medium", "Hard"):
        assert getattr(difficulty_cls, name).name == name


def test_fake_adapter_rejects_non_passive_burny_policy() -> None:
    for policy in (
        BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
        BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
    ):
        cfg = MatchConfig(
            schema_version="1",
            adapter="fake",
            seed=1,
            bounded_horizon=BoundedHorizon(10, 1),
            map=MapSpec(discover_under_maps_dir=True),
            burnysc2_policy=policy,
        )
        with pytest.raises(ValueError, match="burnysc2_policy"):
            cfg.validate()


def test_watchability_policy_roundtrip() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 8, "max_game_steps": 100},
            "burnysc2_policy": BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 9,
        },
    )
    assert cfg.burnysc2_policy == BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1
    m = match_config_to_mapping(cfg)
    assert m["burnysc2_policy"] == BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1


def test_watchability_suppress_attack_rejected() -> None:
    with pytest.raises(ValueError, match="burnysc2_suppress_attack requires"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
                "burnysc2_policy": BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
                "burnysc2_suppress_attack": True,
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 1,
            },
        )


def test_config_hash_differs_watchability_vs_hybrid() -> None:
    raw = {
        "adapter": "burnysc2",
        "bounded_horizon": {"game_step": 8, "max_game_steps": 8192},
        "map": {"discover_under_maps_dir": True},
        "schema_version": "1",
        "seed": 4242,
    }
    hybrid = match_config_from_mapping(
        {**raw, "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1}
    )
    watch = match_config_from_mapping(
        {**raw, "burnysc2_policy": BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1},
    )
    assert compute_config_hash(hybrid) != compute_config_hash(watch)
    hn = normalize_match_config_for_identity(hybrid)
    wn = normalize_match_config_for_identity(watch)
    assert hn.get("burnysc2_policy") == BURNYSC2_POLICY_PX1_M03_HYBRID_V1
    assert wn.get("burnysc2_policy") == BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1


def test_burnysc2_suppress_attack_true_parses() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
            "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
            "burnysc2_suppress_attack": True,
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 1,
        },
    )
    assert cfg.burnysc2_suppress_attack is True
    m = match_config_to_mapping(cfg)
    assert m["burnysc2_suppress_attack"] is True


def test_burnysc2_suppress_attack_non_bool_raises() -> None:
    with pytest.raises(ValueError, match="burnysc2_suppress_attack must be a boolean"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
                "burnysc2_suppress_attack": "yes",
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_burnysc2_suppress_attack_requires_hybrid_policy() -> None:
    with pytest.raises(ValueError, match="burnysc2_suppress_attack requires"):
        match_config_from_mapping(
            {
                "adapter": "burnysc2",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "burnysc2_suppress_attack": True,
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_burnysc2_suppress_attack_requires_burny_adapter() -> None:
    with pytest.raises(ValueError, match="burnysc2_suppress_attack may only be set"):
        match_config_from_mapping(
            {
                "adapter": "fake",
                "bounded_horizon": {"game_step": 1, "max_game_steps": 2},
                "burnysc2_suppress_attack": True,
                "map": {"discover_under_maps_dir": True},
                "schema_version": "1",
                "seed": 0,
            },
        )


def test_match_config_to_mapping_omits_default_suppress_attack() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="burnysc2",
        seed=1,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(discover_under_maps_dir=True),
        burnysc2_policy=BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    )
    m = match_config_to_mapping(cfg)
    assert "burnysc2_suppress_attack" not in m


def test_normalize_identity_unchanged_default_suppress_attack() -> None:
    cfg = match_config_from_mapping(
        {
            "adapter": "burnysc2",
            "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
            "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
            "map": {"discover_under_maps_dir": True},
            "schema_version": "1",
            "seed": 1,
        },
    )
    n = normalize_match_config_for_identity(cfg)
    assert "burnysc2_suppress_attack" not in n


def test_normalize_and_hash_change_when_suppress_attack_true() -> None:
    raw = {
        "adapter": "burnysc2",
        "bounded_horizon": {"game_step": 8, "max_game_steps": 10},
        "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
        "map": {"discover_under_maps_dir": True},
        "schema_version": "1",
        "seed": 1,
    }
    base = match_config_from_mapping(dict(raw))
    sup = match_config_from_mapping({**raw, "burnysc2_suppress_attack": True})
    assert compute_config_hash(base) != compute_config_hash(sup)
    assert normalize_match_config_for_identity(sup).get("burnysc2_suppress_attack") is True
