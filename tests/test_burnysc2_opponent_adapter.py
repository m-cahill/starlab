"""BurnySc2 opponent_mode wiring (no live SC2; requires python-sc2 import)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("sc2", reason="python-sc2 not installed")

from sc2.player import Bot, Computer
from starlab.sc2.adapters.burnysc2_adapter import run_burnysc2_adapter
from starlab.sc2.match_config import match_config_from_mapping

_PROBES = {"root": "C:/SC2", "maps_dir": "C:/SC2/Maps"}


def _minimal_burny_raw() -> dict[str, Any]:
    return {
        "adapter": "burnysc2",
        "bounded_horizon": {"game_step": 1, "max_game_steps": 3},
        "map": {"discover_under_maps_dir": True},
        "schema_version": "1",
        "seed": 0,
    }


def test_burnysc2_run_game_gets_computer_when_opponent_mode_computer() -> None:
    cfg = match_config_from_mapping(_minimal_burny_raw())
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Defeat"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    with (
        resolve,
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result) as rg,
    ):
        run_burnysc2_adapter(cfg, output_dir=Path("/tmp/starlab_burny_test_out"))
    players = rg.call_args[0][1]
    assert isinstance(players[0], Bot)
    assert isinstance(players[1], Computer)


def test_burnysc2_run_game_gets_second_bot_when_opponent_mode_passive_bot() -> None:
    raw = {**_minimal_burny_raw(), "opponent_mode": "passive_bot"}
    cfg = match_config_from_mapping(raw)
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Victory"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    with (
        resolve,
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result) as rg,
    ):
        run_burnysc2_adapter(cfg, output_dir=Path("/tmp/starlab_burny_test_out"))
    players = rg.call_args[0][1]
    assert isinstance(players[0], Bot)
    assert isinstance(players[1], Bot)
    assert type(players[1].ai).__name__ == "_PassiveOpponentBot"
