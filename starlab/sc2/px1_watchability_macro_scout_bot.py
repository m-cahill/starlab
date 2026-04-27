"""PX1 watchability macro/scout Terran bot — deterministic sandbox demo (no trained agent).

Loaded only when BurnySc2 is available (policy ``px1_watchability_macro_scout_v1``).
"""

from __future__ import annotations

from typing import Any

_WATCHABILITY_TALLY_KEYS: tuple[str, ...] = (
    "watchability_worker_train_applied",
    "watchability_worker_gather_applied",
    "watchability_supply_structure_applied",
    "watchability_military_structure_applied",
    "watchability_military_unit_applied",
    "watchability_scout_move_applied",
    "watchability_patrol_or_rally_applied",
    "watchability_noncombat_move_applied",
    "watchability_action_failed",
)


def _init_watchability_tallies() -> dict[str, int]:
    return {k: 0 for k in _WATCHABILITY_TALLY_KEYS}


def _bump(tallies: dict[str, int], key: str, n: int = 1) -> None:
    tallies[key] = tallies.get(key, 0) + n


def make_px1_watchability_macro_scout_bot_class(
    *,
    max_steps: int,
    game_step: int,
    sink: dict[str, Any],
) -> type:
    """Return a BurnySc2 ``BotAI`` subclass for watchability-only local smokes."""

    from sc2.bot_ai import BotAI
    from sc2.ids.unit_typeid import UnitTypeId
    from sc2.position import Point2

    tallies: dict[str, int] = sink.setdefault("live_action_tallies", _init_watchability_tallies())
    if not tallies:
        tallies.update(_init_watchability_tallies())
    for k in _WATCHABILITY_TALLY_KEYS:
        tallies.setdefault(k, 0)
    summary: dict[str, Any] = sink.setdefault("live_action_behavior_summary", {})
    summary.setdefault(
        "operator_readable_summary_v1",
        (
            "policy: px1_watchability_macro_scout_v1; purpose: watchability/sandbox only; "
            "attacks: disabled by design — not trained play, not benchmark evidence."
        ),
    )

    # Throttle helpers (iteration = python-sc2 step index).
    _GATHER_EVERY = 64
    _PATROL_EVERY = 96
    _TARGET_WORKERS = 14
    _CAP_MARINES = 12

    class _Px1WatchabilityMacroScoutBot(BotAI):
        def __init__(self) -> None:
            super().__init__()
            self._max_steps = max_steps
            self._game_step = game_step
            self._out = sink
            self._scout_done = False
            self._patrol_phase = 0

        async def on_start(self) -> None:
            self.client.game_step = self._game_step
            self._out["status_sequence"].append("in_game")
            ping = await self.client.ping()  # type: ignore[no-untyped-call]
            self._out["base_build"] = ping.ping.base_build
            dv = getattr(ping.ping, "data_version", None)
            self._out["data_version"] = dv if dv else None

        def _safe_patrol_points(self) -> tuple[Any, Any] | None:
            """Two local points near the main CC — patrol ping-pong for visibility."""

            cc = self.townhalls.ready.first if self.townhalls.ready else None
            if cc is None:
                return None
            pos = cc.position
            a = pos + Point2((8.0, 1.5))
            b = pos + Point2((-3.0, 9.0))
            return a, b

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
                await self._watchability_logic(iteration, gl)
            except (AttributeError, RuntimeError, ValueError, TypeError, KeyError) as exc:
                errs = self._out.setdefault("hybrid_remediation_errors", [])
                errs.append(f"{type(exc).__name__}:{exc}")
                _bump(self._out["live_action_tallies"], "watchability_action_failed")

            if iteration >= self._max_steps - 1:
                self._out["status_sequence"].append("bounded_exit")
                await self.client.leave()

        async def _watchability_logic(self, iteration: int, gl: int) -> None:
            tl = self._out["live_action_tallies"]

            cc_ready = self.townhalls.ready
            if not cc_ready:
                return

            # Periodic worker redistribution — visible gathering activity.
            if iteration > 0 and iteration % _GATHER_EVERY == 0:
                try:
                    if self.workers and self.mineral_field:
                        await self.distribute_workers()
                        _bump(tl, "watchability_worker_gather_applied")
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                except (AttributeError, RuntimeError, ValueError, TypeError):
                    _bump(tl, "watchability_action_failed")

            workers_amt = self.workers.amount
            if workers_amt < _TARGET_WORKERS and self.supply_left > 0:
                n = self.train(UnitTypeId.SCV, 1)
                if n > 0:
                    _bump(tl, "watchability_worker_train_applied", int(n))
                    self._out["action_count"] = int(self._out.get("action_count", 0)) + int(n)
                else:
                    _bump(tl, "watchability_action_failed")

            if self.supply_left < 4 and self.minerals >= 100:
                if self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                    cc = cc_ready.first
                    if cc is not None:
                        built = await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position)
                        if built:
                            _bump(tl, "watchability_supply_structure_applied")
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                        else:
                            _bump(tl, "watchability_action_failed")

            if self.structures(UnitTypeId.BARRACKS).empty and self.minerals >= 150:
                if self.already_pending(UnitTypeId.BARRACKS) == 0:
                    cc = cc_ready.first
                    if cc is not None:
                        built = await self.build(UnitTypeId.BARRACKS, near=cc.position)
                        if built:
                            _bump(tl, "watchability_military_structure_applied")
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                        else:
                            _bump(tl, "watchability_action_failed")

            rax = self.structures(UnitTypeId.BARRACKS).ready
            marine_amt = self.units(UnitTypeId.MARINE).amount
            if rax and self.supply_left > 0 and self.can_afford(UnitTypeId.MARINE):
                if marine_amt < _CAP_MARINES:
                    n = self.train(UnitTypeId.MARINE, 1)
                    if n > 0:
                        _bump(tl, "watchability_military_unit_applied", int(n))
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + int(n)
                    else:
                        _bump(tl, "watchability_action_failed")

            marine_units = self.units(UnitTypeId.MARINE)
            if not self._scout_done and marine_units and marine_units.ready:
                scout = marine_units.ready.first
                if scout is not None:
                    target = self.game_info.map_center
                    self.do(scout.move(target))  # type: ignore[arg-type]
                    _bump(tl, "watchability_scout_move_applied")
                    _bump(tl, "watchability_noncombat_move_applied")
                    self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                    self._scout_done = True

            # Recurring patrol near base — primary watchability motion after setup.
            if iteration > 0 and iteration % _PATROL_EVERY == 0 and gl > 400:
                pts = self._safe_patrol_points()
                ready_m = self.units(UnitTypeId.MARINE).ready
                if pts is not None and ready_m:
                    p_a, p_b = pts
                    self._patrol_phase += 1
                    tgt = p_a if self._patrol_phase % 2 == 0 else p_b
                    cmds = 0
                    for um in list(ready_m)[:10]:
                        try:
                            self.do(um.patrol(tgt))  # type: ignore[arg-type]
                            cmds += 1
                        except (AttributeError, RuntimeError, ValueError):
                            _bump(tl, "watchability_action_failed")
                    if cmds > 0:
                        _bump(tl, "watchability_patrol_or_rally_applied", cmds)
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + cmds

    return _Px1WatchabilityMacroScoutBot
