"""BurnySc2 opponent_mode wiring (no live SC2; requires python-sc2 import)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytest.importorskip("sc2", reason="python-sc2 not installed")

from sc2.player import Bot, Computer
from starlab.sc2.adapters.burnysc2_adapter import (
    passive_opponent_heartbeat_due,
    run_burnysc2_adapter,
    run_passive_opponent_heartbeat,
)
from starlab.sc2.match_config import (
    BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
    match_config_from_mapping,
)

_PROBES = {"root": "C:/SC2", "maps_dir": "C:/SC2/Maps"}


def _bot_player_stub(
    race: Any,
    ai: Any,
    name: str | None = None,
    fullscreen: bool = False,
) -> MagicMock:
    """Avoid sc2.player.Bot's isinstance check when testing hybrid factory with MagicMock AIs."""

    p = MagicMock()
    p.ai = ai
    return p


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


def test_hybrid_factory_receives_suppress_attack_false_by_default() -> None:
    raw = {
        **_minimal_burny_raw(),
        "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    }
    cfg = match_config_from_mapping(raw)
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Defeat"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    BotClass = MagicMock()
    BotClass.return_value = MagicMock()
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    make_hybrid = patch(
        "starlab.sc2.adapters.burnysc2_adapter.make_px1_m03_hybrid_terran_bot_class",
        return_value=BotClass,
    )
    with (
        resolve,
        make_hybrid as mk,
        patch("sc2.player.Bot", side_effect=_bot_player_stub),
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result),
    ):
        run_burnysc2_adapter(
            cfg,
            output_dir=Path("/tmp/starlab_burny_test_out"),
            hierarchical_sklearn_bundle={"k": "v"},
        )
    assert mk.call_args is not None
    assert mk.call_args.kwargs.get("suppress_attack") is False


def test_hybrid_factory_receives_suppress_attack_true() -> None:
    raw = {
        **_minimal_burny_raw(),
        "burnysc2_policy": BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
        "burnysc2_suppress_attack": True,
    }
    cfg = match_config_from_mapping(raw)
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Defeat"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    BotClass = MagicMock()
    BotClass.return_value = MagicMock()
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    make_hybrid = patch(
        "starlab.sc2.adapters.burnysc2_adapter.make_px1_m03_hybrid_terran_bot_class",
        return_value=BotClass,
    )
    with (
        resolve,
        make_hybrid as mk,
        patch("sc2.player.Bot", side_effect=_bot_player_stub),
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result),
    ):
        run_burnysc2_adapter(
            cfg,
            output_dir=Path("/tmp/starlab_burny_test_out"),
            hierarchical_sklearn_bundle={"k": "v"},
        )
    assert mk.call_args is not None
    assert mk.call_args.kwargs.get("suppress_attack") is True


def test_passive_opponent_heartbeat_due_periodicity() -> None:
    assert passive_opponent_heartbeat_due(0) is False
    assert passive_opponent_heartbeat_due(1) is False
    assert passive_opponent_heartbeat_due(48) is True
    assert passive_opponent_heartbeat_due(96) is True
    assert passive_opponent_heartbeat_due(47) is False


def test_run_passive_opponent_heartbeat_skips_when_not_ready() -> None:
    dist = AsyncMock()
    bot = MagicMock()
    bot.townhalls = None
    bot.distribute_workers = dist
    asyncio.run(run_passive_opponent_heartbeat(bot))
    dist.assert_not_awaited()


def test_run_passive_opponent_heartbeat_calls_distribute_workers_when_prereq_met() -> None:
    dist = AsyncMock()
    bot = MagicMock()
    bot.townhalls = MagicMock()
    bot.townhalls.ready = True
    bot.workers = [MagicMock()]
    bot.mineral_field = [MagicMock()]
    bot.distribute_workers = dist
    asyncio.run(run_passive_opponent_heartbeat(bot))
    dist.assert_awaited_once()


def test_run_passive_opponent_heartbeat_swallows_distribute_error() -> None:
    bot = MagicMock()
    bot.townhalls = MagicMock()
    bot.townhalls.ready = True
    bot.workers = [MagicMock()]
    bot.mineral_field = [MagicMock()]
    bot.distribute_workers = AsyncMock(side_effect=RuntimeError("simulated"))
    asyncio.run(run_passive_opponent_heartbeat(bot))


def test_run_burnysc2_watchability_policy_without_sklearn_bundle() -> None:
    raw = {
        **_minimal_burny_raw(),
        "burnysc2_policy": BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
    }
    cfg = match_config_from_mapping(raw)
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Tie"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    WatchClass = MagicMock()
    WatchClass.return_value = MagicMock()
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    mk_watch = patch(
        "starlab.sc2.adapters.burnysc2_adapter.make_px1_watchability_macro_scout_bot_class",
        return_value=WatchClass,
    )
    with (
        resolve,
        mk_watch as mk,
        patch("sc2.player.Bot", side_effect=_bot_player_stub),
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result),
    ):
        run_burnysc2_adapter(cfg, output_dir=Path("/tmp/starlab_burny_watch_out"))
    mk.assert_called_once()
    assert mk.call_args.kwargs["max_steps"] == 3


def test_run_burnysc2_watchability_factory_returns_terran_bot_class_name() -> None:
    raw = {
        **_minimal_burny_raw(),
        "burnysc2_policy": BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
        "opponent_mode": "passive_bot",
    }
    cfg = match_config_from_mapping(raw)
    mock_map = MagicMock()
    mock_result = MagicMock()
    mock_result.name = "Victory"
    mock_probe = MagicMock(
        base_build="96883",
        data_version="dv",
        paths=_PROBES,
    )
    from starlab.sc2.px1_watchability_macro_scout_bot import (
        make_px1_watchability_macro_scout_bot_class,
    )

    BotCls = make_px1_watchability_macro_scout_bot_class(
        max_steps=2,
        game_step=1,
        sink={
            "action_count": 0,
            "observations": [],
            "status_sequence": [],
            "live_action_tallies": {},
            "live_action_behavior_summary": {},
        },
    )
    resolve = patch(
        "starlab.sc2.adapters.burnysc2_adapter._resolve_map_for_burny",
        return_value=(mock_map, "k", "m"),
    )
    with (
        resolve,
        patch(
            "starlab.sc2.adapters.burnysc2_adapter.make_px1_watchability_macro_scout_bot_class",
            return_value=BotCls,
        ),
        patch("sc2.player.Bot", side_effect=_bot_player_stub),
        patch("starlab.sc2.adapters.burnysc2_adapter.run_probe", return_value=mock_probe),
        patch("sc2.main.run_game", return_value=mock_result) as rg,
    ):
        run_burnysc2_adapter(cfg, output_dir=Path("/tmp/starlab_burny_watch_cls"))
    players = rg.call_args[0][1]
    assert type(players[0].ai).__name__ == "_Px1WatchabilityMacroScoutBot"
