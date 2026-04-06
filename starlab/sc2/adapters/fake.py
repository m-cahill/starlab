"""Deterministic fake adapter for CI — no SC2, no BurnySc2 imports."""

from __future__ import annotations

from starlab.sc2.artifacts import (
    PROOF_SCHEMA_VERSION,
    ExecutionProofRecord,
    ReplayMetadata,
)
from starlab.sc2.match_config import MatchConfig
from starlab.sc2.models import Sc2RuntimeSpec


class FakeMatchHarnessAdapter:
    name = "fake"

    def run(self, config: MatchConfig) -> ExecutionProofRecord:
        spec = Sc2RuntimeSpec()
        max_steps = config.bounded_horizon.max_game_steps
        summaries: list[dict[str, int]] = []
        for i in range(max_steps):
            gl = (i + 1) * config.bounded_horizon.game_step
            summaries.append(
                {
                    "game_loop": gl,
                    "minerals": 50 + i,
                    "vespene": 0,
                },
            )
        status_seq = ("launched", "joined", "stepping", "ended")
        iface = {
            "feature_layer_interface": config.interface.feature_layer_interface,
            "raw_interface": config.interface.raw_interface,
            "rendered_interface": config.interface.rendered_interface,
            "score_interface": config.interface.score_interface,
        }
        return ExecutionProofRecord(
            schema_version=PROOF_SCHEMA_VERSION,
            adapter_name=self.name,
            runtime_boundary_name=spec.control_observation_surface,
            base_build=None,
            data_version=None,
            map_logical_key="fake://deterministic",
            map_resolution="fake_adapter",
            seed=config.seed,
            interface=iface,
            step_policy={
                "game_step": config.bounded_horizon.game_step,
                "max_game_steps": config.bounded_horizon.max_game_steps,
            },
            status_sequence=status_seq,
            observation_summaries=tuple(summaries),
            action_count=0,
            final_status="ok",
            replay=ReplayMetadata(replay_saved=False, note="fake adapter"),
        )
