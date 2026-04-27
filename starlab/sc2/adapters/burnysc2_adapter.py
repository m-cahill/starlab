"""Real match execution via BurnySc2 — import only when this module runs."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from starlab.sc2.artifacts import (
    PROOF_SCHEMA_VERSION,
    ExecutionProofRecord,
    ReplayMetadata,
)
from starlab.sc2.env_probe import run_probe
from starlab.sc2.maps import ResolvedMap, resolve_local_map_path
from starlab.sc2.match_config import (
    BURNYSC2_OPPONENT_MODE_PASSIVE_BOT,
    BURNYSC2_POLICY_PX1_M03_HYBRID_V1,
    BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1,
    MatchConfig,
)
from starlab.sc2.models import Sc2RuntimeSpec
from starlab.sc2.px1_m03_hybrid_terran_bot import make_px1_m03_hybrid_terran_bot_class
from starlab.sc2.px1_watchability_macro_scout_bot import (
    make_px1_watchability_macro_scout_bot_class,
)

# Watchability: passive second player runs occasional non-combat economic heartbeat
# (not a pressure opponent).
_PASSIVE_OPPONENT_HEARTBEAT_EVERY: int = 48


def passive_opponent_heartbeat_due(iteration: int) -> bool:
    """Return True on periodic steps when the passive bot should run non-combat activity."""

    return iteration > 0 and iteration % _PASSIVE_OPPONENT_HEARTBEAT_EVERY == 0


async def run_passive_opponent_heartbeat(bot: Any) -> None:
    """Assign workers via BotAI.distribute_workers; no attack or scout. Swallows API/race flukes."""

    try:
        if not bot.townhalls or not bot.townhalls.ready:
            return
        if not bot.workers or not bot.mineral_field:
            return
        await bot.distribute_workers()
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, RuntimeError):
        return


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve_map_for_burny(config: MatchConfig, maps_root: Path | None) -> tuple[Any, str, str]:
    """Return ``(sc2.Map, logical_key, resolution_label)``."""

    if config.map.battle_net_map_name is not None:
        from sc2.maps import get as sc2_map_get

        m = sc2_map_get(config.map.battle_net_map_name)
        return m, str(m.name), "battle_net_name"

    resolved: ResolvedMap = resolve_local_map_path(
        maps_root=maps_root,
        explicit_path=config.map.path,
        discover=config.map.discover_under_maps_dir,
    )
    from sc2.maps import Map as Sc2Map

    return Sc2Map(resolved.map_path), resolved.logical_key, resolved.resolution


def run_burnysc2_adapter(
    config: MatchConfig,
    output_dir: Path | None = None,
    *,
    hierarchical_sklearn_bundle: dict[str, Any] | None = None,
) -> ExecutionProofRecord:
    """Run a bounded bot-vs-AI game via BurnySc2.

    Requires optional ``sc2-harness`` extras and a local SC2 install.
    """

    try:
        from sc2.bot_ai import BotAI
        from sc2.data import Difficulty, Race
        from sc2.main import run_game
        from sc2.player import Bot, Computer
    except ImportError as e:
        raise RuntimeError(
            "burnysc2 is not installed. Install optional extras: pip install -e '.[sc2-harness]'",
        ) from e

    probe = run_probe()
    root = probe.paths.get("root")
    if root:
        os.environ["SC2PATH"] = root

    maps_dir_raw = probe.paths.get("maps_dir")
    maps_root = Path(maps_dir_raw) if maps_dir_raw else None

    spec = Sc2RuntimeSpec()
    sink: dict[str, Any] = {
        "action_count": 0,
        "observations": [],
        "status_sequence": ["configure", "launch"],
    }

    use_hybrid = config.burnysc2_policy == BURNYSC2_POLICY_PX1_M03_HYBRID_V1
    use_watchability = config.burnysc2_policy == BURNYSC2_POLICY_PX1_WATCHABILITY_MACRO_SCOUT_V1
    if use_hybrid and hierarchical_sklearn_bundle is None:
        msg = "burnysc2_policy px1_m03_hybrid_v1 requires hierarchical_sklearn_bundle"
        raise RuntimeError(msg)

    class _HarnessBot(BotAI):
        def __init__(self, max_steps: int, game_step: int, out: dict[str, Any]) -> None:
            super().__init__()
            self._max_steps = max_steps
            self._game_step = game_step
            self._out = out

        async def on_start(self) -> None:
            self.client.game_step = self._game_step
            self._out["status_sequence"].append("in_game")
            ping = await self.client.ping()
            self._out["base_build"] = ping.ping.base_build
            dv = getattr(ping.ping, "data_version", None)
            self._out["data_version"] = dv if dv else None

        async def on_step(self, iteration: int) -> None:
            st = self.state
            self._out["observations"].append(
                {
                    "game_loop": int(st.game_loop),
                    "minerals": int(st.common.minerals),
                    "vespene": int(st.common.vespene),
                },
            )
            if iteration >= self._max_steps - 1:
                self._out["status_sequence"].append("bounded_exit")
                await self.client.leave()

    class _PassiveOpponentBot(BotAI):
        """Second-player low-pressure bot: no attacks; optional economic heartbeat."""

        def __init__(self, game_step: int) -> None:
            super().__init__()
            self._game_step = game_step

        async def on_start(self) -> None:
            self.client.game_step = self._game_step

        async def on_step(self, iteration: int) -> None:
            if passive_opponent_heartbeat_due(iteration):
                await run_passive_opponent_heartbeat(self)

    map_settings, logical_key, map_resolution = _resolve_map_for_burny(config, maps_root)

    if use_hybrid:
        assert hierarchical_sklearn_bundle is not None
        bot_cls = make_px1_m03_hybrid_terran_bot_class(
            max_steps=config.bounded_horizon.max_game_steps,
            game_step=config.bounded_horizon.game_step,
            sink=sink,
            hierarchical_sklearn_bundle=hierarchical_sklearn_bundle,
            suppress_attack=config.burnysc2_suppress_attack,
        )
        bot = bot_cls()
        bot_race = Race.Terran
    elif use_watchability:
        bot_cls = make_px1_watchability_macro_scout_bot_class(
            max_steps=config.bounded_horizon.max_game_steps,
            game_step=config.bounded_horizon.game_step,
            sink=sink,
        )
        bot = bot_cls()
        bot_race = Race.Terran
    else:
        bot = _HarnessBot(
            config.bounded_horizon.max_game_steps,
            config.bounded_horizon.game_step,
            sink,
        )
        bot_race = Race.Random
    gstep = config.bounded_horizon.game_step
    if config.opponent_mode == BURNYSC2_OPPONENT_MODE_PASSIVE_BOT:
        passive_opp = _PassiveOpponentBot(gstep)
        players = [Bot(bot_race, bot), Bot(Race.Random, passive_opp)]
    else:
        sc2_difficulty = getattr(Difficulty, config.computer_difficulty)
        players = [Bot(bot_race, bot), Computer(Race.Random, sc2_difficulty)]

    save_replay_as: str | None = None
    if config.save_replay and output_dir is not None:
        name = config.replay_filename or "starlab_m02.SC2Replay"
        save_replay_as = str((output_dir / name).resolve())

    sc2_version = os.environ.get("STARLAB_SC2_BASE_BUILD")

    result = run_game(
        map_settings,
        players,
        realtime=False,
        random_seed=config.seed,
        save_replay_as=save_replay_as,
        sc2_version=sc2_version,
    )

    literal_sc2 = str(getattr(result, "name", str(result)))
    sink["status_sequence"].append(f"result:{literal_sc2}")
    # Bounded harness exits voluntarily at step cap (bounded_exit); SC2 reports a loss result
    # (e.g. Defeat) but validation success is governed separately from match outcome.
    bounded_completed = "bounded_exit" in sink["status_sequence"]
    validation_final_status = "ok" if bounded_completed else literal_sc2

    iface = {
        "feature_layer_interface": config.interface.feature_layer_interface,
        "raw_interface": config.interface.raw_interface,
        "rendered_interface": config.interface.rendered_interface,
        "score_interface": config.interface.score_interface,
    }

    replay_meta: ReplayMetadata | None = None
    if save_replay_as is not None:
        rp = Path(save_replay_as)
        if rp.is_file():
            replay_meta = ReplayMetadata(
                replay_saved=True,
                replay_file_name=rp.name,
                replay_file_sha256=_sha256_file(rp),
                note="replay bytes hashed; not a replay-binding claim",
            )
        else:
            replay_meta = ReplayMetadata(
                replay_saved=False,
                note="save requested but file missing after run",
            )
    else:
        replay_meta = ReplayMetadata(replay_saved=False, note="replay save not requested")

    base_build = sink.get("base_build")
    data_version = sink.get("data_version")
    bb = str(base_build) if base_build is not None else probe.base_build
    dv = str(data_version) if data_version is not None else probe.data_version

    obs_tuple = tuple(dict(x) for x in sink["observations"])

    lat = sink.get("live_action_tallies")
    tallies_out: dict[str, int] | None = None
    if isinstance(lat, dict) and lat:
        tallies_out = {str(k): int(v) for k, v in lat.items()}
    lbs = sink.get("live_action_behavior_summary")
    summary_out: dict[str, Any] | None = None
    if isinstance(lbs, dict) and lbs:
        summary_out = dict(lbs)
        if use_hybrid:
            if config.burnysc2_suppress_attack:
                summary_out["operator_readable_summary_v1"] = (
                    "PX1-M03 hybrid (watchability: suppress_attack): hard-coded Terran worker/"
                    "supply/barracks/marine scaffold; one early scout move; M43 labels logged; "
                    "marine attack-move toward enemy is disabled — not full strategic play."
                )
            else:
                summary_out["operator_readable_summary_v1"] = (
                    "PX1-M03 hybrid: hard-coded Terran worker/supply/barracks/marine scaffold; "
                    "one early scout move; throttled marine attack-move toward enemy start using "
                    "M43 coarse labels with periodic fallback — not full strategic play."
                )
        elif use_watchability:
            summary_out["operator_readable_summary_v1"] = (
                "policy: px1_watchability_macro_scout_v1; purpose: watchability/sandbox only; "
                "attacks: disabled by design — scripted macro, scout, and patrol near base."
            )

    return ExecutionProofRecord(
        schema_version=PROOF_SCHEMA_VERSION,
        adapter_name="burnysc2",
        runtime_boundary_name=spec.control_observation_surface,
        base_build=bb,
        data_version=dv,
        map_logical_key=logical_key,
        map_resolution=map_resolution,
        seed=config.seed,
        interface=iface,
        step_policy={
            "game_step": config.bounded_horizon.game_step,
            "max_game_steps": config.bounded_horizon.max_game_steps,
        },
        status_sequence=tuple(sink["status_sequence"]),
        observation_summaries=obs_tuple,
        action_count=int(sink["action_count"]),
        final_status=validation_final_status,
        replay=replay_meta,
        sc2_game_result=literal_sc2,
        live_action_tallies=tallies_out,
        live_action_behavior_summary=summary_out,
    )
