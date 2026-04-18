"""Match config parsing and validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.sc2.match_config import (
    BURNYSC2_POLICY_PASSIVE,
    BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
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


def test_fake_adapter_rejects_non_passive_burny_policy() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=1,
        bounded_horizon=BoundedHorizon(10, 1),
        map=MapSpec(discover_under_maps_dir=True),
        burnysc2_policy=BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    )
    with pytest.raises(ValueError, match="burnysc2_policy"):
        cfg.validate()
