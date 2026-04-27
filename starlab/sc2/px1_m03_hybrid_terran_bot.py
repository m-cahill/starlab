"""PX1-M03 hybrid Terran bot — bounded macro scaffold + narrow M43-driven combat/scout.

Loaded only when BurnySc2 is available (see ``burnysc2_adapter``)."""

from __future__ import annotations

from typing import Any

from starlab.hierarchy.m43_sklearn_runtime import predict_delegate_and_coarse_label

# Tally keys aligned with PX1-M03 proof surface (applied / attempted).
TALLY_KEYS_APPLIED = (
    "worker_train_applied",
    "supply_structure_applied",
    "scout_move_applied",
    "military_structure_applied",
    "military_unit_applied",
    "combat_or_attack_move_applied",
    "combat_or_attack_move_suppressed",
    "other_live_action_applied",
)

TALLY_KEYS_ATTEMPTED = (
    "worker_train_attempted",
    "supply_structure_attempted",
    "military_structure_attempted",
    "military_unit_attempted",
    "combat_or_attack_move_attempted",
)


def _init_tallies() -> dict[str, int]:
    d: dict[str, int] = {}
    for k in TALLY_KEYS_APPLIED + TALLY_KEYS_ATTEMPTED:
        d[k] = 0
    return d


def _bump(tallies: dict[str, int], key: str, n: int = 1) -> None:
    tallies[key] = tallies.get(key, 0) + n


def _derive_sig(iteration: int, game_loop: int, minerals: int, vespene: int) -> str:
    return f"m44_step={iteration}|gameloop={game_loop}|minerals={minerals}|vespene={vespene}"


def make_px1_m03_hybrid_terran_bot_class(
    *,
    max_steps: int,
    game_step: int,
    sink: dict[str, Any],
    hierarchical_sklearn_bundle: dict[str, Any],
    suppress_attack: bool = False,
) -> type:
    """Return a BurnySc2 ``BotAI`` subclass for PX1-M03 hybrid remediation."""

    from sc2.bot_ai import BotAI
    from sc2.ids.unit_typeid import UnitTypeId

    tallies: dict[str, int] = sink.setdefault("live_action_tallies", _init_tallies())
    if not tallies:
        tallies.update(_init_tallies())
    summary: dict[str, Any] = sink.setdefault("live_action_behavior_summary", {})

    class _Px1M03HybridTerranBot(BotAI):
        def __init__(self) -> None:
            super().__init__()
            self._max_steps = max_steps
            self._game_step = game_step
            self._out = sink
            self._bundle = hierarchical_sklearn_bundle
            self._scout_done = False
            self._suppress_attack = suppress_attack

        async def on_start(self) -> None:
            self.client.game_step = self._game_step
            self._out["status_sequence"].append("in_game")
            ping = await self.client.ping()
            self._out["base_build"] = ping.ping.base_build
            dv = getattr(ping.ping, "data_version", None)
            self._out["data_version"] = dv if dv else None

        async def on_step(self, iteration: int) -> None:
            st = self.state
            gl = int(st.game_loop)
            minerals = int(st.common.minerals)
            vespene = int(st.common.vespene)
            self._out["observations"].append(
                {
                    "game_loop": gl,
                    "minerals": minerals,
                    "vespene": vespene,
                },
            )

            try:
                await self._px1_m03_logic(iteration, gl, minerals, vespene)
            except (AttributeError, RuntimeError, ValueError, TypeError, KeyError) as exc:
                errs = self._out.setdefault("hybrid_remediation_errors", [])
                errs.append(f"{type(exc).__name__}:{exc}")

            if iteration >= self._max_steps - 1:
                self._out["status_sequence"].append("bounded_exit")
                await self.client.leave()

        async def _px1_m03_logic(
            self,
            iteration: int,
            gl: int,
            minerals: int,
            vespene: int,
        ) -> None:
            tallies_local: dict[str, int] = self._out["live_action_tallies"]
            cc_ready = self.townhalls.ready
            if not cc_ready:
                return

            # --- Hard-coded macro essentials (Terran) ---
            workers = self.workers.amount
            target_workers = 14

            if workers < target_workers and self.supply_left > 0:
                _bump(tallies_local, "worker_train_attempted")
                n = self.train(UnitTypeId.SCV, 1)
                if n > 0:
                    _bump(tallies_local, "worker_train_applied", n)
                    self._out["action_count"] = int(self._out.get("action_count", 0)) + int(n)
                    if summary.get("first_worker_train_game_loop") is None:
                        summary["first_worker_train_game_loop"] = gl

            # Supply depot when tight
            if self.supply_left < 4 and self.minerals >= 100:
                if self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                    _bump(tallies_local, "supply_structure_attempted")
                    cc = cc_ready.first
                    if cc is not None:
                        built = await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position)
                        if built:
                            _bump(tallies_local, "supply_structure_applied")
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                            if summary.get("first_supply_depot_game_loop") is None:
                                summary["first_supply_depot_game_loop"] = gl

            # Barracks
            if self.structures(UnitTypeId.BARRACKS).empty and self.minerals >= 150:
                if self.already_pending(UnitTypeId.BARRACKS) == 0:
                    _bump(tallies_local, "military_structure_attempted")
                    cc = cc_ready.first
                    if cc is not None:
                        built = await self.build(UnitTypeId.BARRACKS, near=cc.position)
                        if built:
                            _bump(tallies_local, "military_structure_applied")
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                            if summary.get("first_barracks_game_loop") is None:
                                summary["first_barracks_game_loop"] = gl

            # Marines from ready barracks
            rax = self.structures(UnitTypeId.BARRACKS).ready
            if rax and self.supply_left > 0 and self.can_afford(UnitTypeId.MARINE):
                marine_count = self.units(UnitTypeId.MARINE).amount
                if marine_count < 10:
                    _bump(tallies_local, "military_unit_attempted")
                    n = self.train(UnitTypeId.MARINE, 1)
                    if n > 0:
                        _bump(tallies_local, "military_unit_applied", n)
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + int(n)
                        if summary.get("first_marine_train_game_loop") is None:
                            summary["first_marine_train_game_loop"] = gl

            # One early scout (bounded): first marine toward map center
            marine_units = self.units(UnitTypeId.MARINE)
            if not self._scout_done and marine_units and marine_units.ready:
                scout = marine_units.ready.first
                if scout is not None:
                    self.do(scout.move(self.game_info.map_center))
                    _bump(tallies_local, "scout_move_applied")
                    self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                    self._scout_done = True
                    if summary.get("first_scout_move_game_loop") is None:
                        summary["first_scout_move_game_loop"] = gl

            # Model-driven / bounded-rule combat (narrow)
            sig = _derive_sig(iteration, gl, minerals, vespene)
            delegate_id, coarse = predict_delegate_and_coarse_label(self._bundle, sig)
            self._out["last_m43_delegate_id"] = delegate_id
            self._out["last_m43_coarse_label"] = coarse

            ready_marines = self.units(UnitTypeId.MARINE).ready
            if len(ready_marines) >= 2:
                target = (
                    self.enemy_start_locations[0]
                    if self.enemy_start_locations
                    else self.game_info.map_center
                )
                coarse_attack = coarse in {
                    "army_attack",
                    "army_move",
                    "scout",
                    "production_unit",
                    "economy_expand",
                }
                # Throttle: avoid issuing duplicate attack orders every frame.
                model_attack = coarse_attack and (iteration % 16 == 0)
                fallback_rule = iteration % 64 == 0 and iteration > 0
                if model_attack or fallback_rule:
                    n_marine = min(12, len(ready_marines))
                    if self._suppress_attack:
                        _bump(tallies_local, "combat_or_attack_move_suppressed", n_marine)
                    else:
                        _bump(tallies_local, "combat_or_attack_move_attempted")
                        cmds = 0
                        for m in ready_marines[:12]:
                            self.do(m.attack(target))
                            cmds += 1
                        if cmds > 0:
                            _bump(tallies_local, "combat_or_attack_move_applied", cmds)
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + cmds
                            if summary.get("first_combat_or_attack_game_loop") is None:
                                summary["first_combat_or_attack_game_loop"] = gl

    return _Px1M03HybridTerranBot
