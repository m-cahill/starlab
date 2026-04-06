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
from starlab.sc2.match_config import MatchConfig
from starlab.sc2.models import Sc2RuntimeSpec


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
    config: MatchConfig, output_dir: Path | None = None
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

    map_settings, logical_key, map_resolution = _resolve_map_for_burny(config, maps_root)

    bot = _HarnessBot(
        config.bounded_horizon.max_game_steps,
        config.bounded_horizon.game_step,
        sink,
    )
    players = [
        Bot(Race.Random, bot),
        Computer(Race.Random, Difficulty.Easy),
    ]

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

    final = getattr(result, "name", str(result))
    sink["status_sequence"].append(f"result:{final}")

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
        final_status=final,
        replay=replay_meta,
    )
