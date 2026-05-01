"""V15-M52A — Terran bot driven by a minimal candidate projection (watchability spike only).

Uses the same low-level Terran patterns as PX1 watchability macro/scout, but the step policy index
comes from ``pick_action_index`` (checkpoint-derived in the operator runner). Not benchmark play.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_M52A_TALLY_KEYS: tuple[str, ...] = (
    "m52a_no_op",
    "m52a_select_idle_worker",
    "m52a_build_worker",
    "m52a_build_supply",
    "m52a_build_barracks",
    "m52a_train_marine",
    "m52a_move_army",
    "m52a_scout",
    "m52a_action_failed",
)


def _init_tallies() -> dict[str, int]:
    return {k: 0 for k in _M52A_TALLY_KEYS}


def _bump(tallies: dict[str, int], key: str, n: int = 1) -> None:
    tallies[key] = tallies.get(key, 0) + n


def make_m52a_candidate_projection_spike_bot_class(
    *,
    max_steps: int,
    game_step: int,
    sink: dict[str, Any],
    pick_action_index: Callable[[int, int, int, int], int],
) -> type:
    """Return BurnySc2 ``BotAI`` subclass for M52A candidate projection spike."""

    from sc2.bot_ai import BotAI
    from sc2.ids.unit_typeid import UnitTypeId
    from sc2.position import Point2

    tallies: dict[str, int] = sink.setdefault("live_action_tallies", _init_tallies())
    if not tallies:
        tallies.update(_init_tallies())
    for k in _M52A_TALLY_KEYS:
        tallies.setdefault(k, 0)
    summary: dict[str, Any] = sink.setdefault("live_action_behavior_summary", {})
    summary.setdefault(
        "operator_readable_summary_v1",
        (
            "policy_id: v15_m52a_candidate_projection_spike_policy_v1; "
            "candidate_output_projection: provisional_safe_action_projection_v1 — "
            "watchability spike only."
        ),
    )

    _GATHER_EVERY = 48
    _TARGET_WORKERS = 14
    _CAP_MARINES = 8

    class _M52aCandidateProjectionSpikeBot(BotAI):
        def __init__(self) -> None:
            super().__init__()
            self._max_steps = max_steps
            self._game_step = game_step
            self._out = sink
            self._pick = pick_action_index
            self._scout_done = False

        async def on_start(self) -> None:
            self.client.game_step = self._game_step
            self._out["status_sequence"].append("in_game")
            ping = await self.client.ping()  # type: ignore[no-untyped-call]
            self._out["base_build"] = ping.ping.base_build
            dv = getattr(ping.ping, "data_version", None)
            self._out["data_version"] = dv if dv else None

        def _safe_patrol_points(self) -> tuple[Any, Any] | None:
            cc = self.townhalls.ready.first if self.townhalls.ready else None
            if cc is None:
                return None
            pos = cc.position
            a = pos + Point2((6.0, 2.0))
            b = pos + Point2((-4.0, 7.0))
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
                idx = int(self._pick(iteration, gl, minerals, vespene))
                idx = max(0, min(7, idx))
                await self._dispatch_projected(idx, iteration, gl)
            except (
                AttributeError,
                RuntimeError,
                ValueError,
                TypeError,
                KeyError,
            ) as exc:
                errs = self._out.setdefault("hybrid_remediation_errors", [])
                errs.append(f"{type(exc).__name__}:{exc}")
                _bump(self._out["live_action_tallies"], "m52a_action_failed")

            if iteration >= self._max_steps - 1:
                self._out["status_sequence"].append("bounded_exit")
                await self.client.leave()

        async def _dispatch_projected(self, idx: int, iteration: int, gl: int) -> None:
            tl = self._out["live_action_tallies"]
            cc_ready = self.townhalls.ready
            if idx == 0:
                _bump(tl, "m52a_no_op")
                return

            if idx == 1:
                if iteration > 0 and iteration % _GATHER_EVERY == 0:
                    try:
                        if self.workers and self.mineral_field:
                            await self.distribute_workers()
                            _bump(tl, "m52a_select_idle_worker")
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                    except (AttributeError, RuntimeError, ValueError, TypeError):
                        _bump(tl, "m52a_action_failed")
                return

            if not cc_ready:
                return

            if idx == 2:
                workers_amt = self.workers.amount
                if workers_amt < _TARGET_WORKERS and self.supply_left > 0:
                    n = self.train(UnitTypeId.SCV, 1)
                    if n > 0:
                        _bump(tl, "m52a_build_worker", int(n))
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + int(n)
                    else:
                        _bump(tl, "m52a_action_failed")
                return

            if idx == 3:
                if self.supply_left < 4 and self.minerals >= 100:
                    if self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                        cc = cc_ready.first
                        if cc is not None:
                            built = await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position)
                            if built:
                                _bump(tl, "m52a_build_supply")
                                self._out["action_count"] = (
                                    int(self._out.get("action_count", 0)) + 1
                                )
                            else:
                                _bump(tl, "m52a_action_failed")
                return

            if idx == 4:
                if self.structures(UnitTypeId.BARRACKS).empty and self.minerals >= 150:
                    if self.already_pending(UnitTypeId.BARRACKS) == 0:
                        cc = cc_ready.first
                        if cc is not None:
                            built = await self.build(UnitTypeId.BARRACKS, near=cc.position)
                            if built:
                                _bump(tl, "m52a_build_barracks")
                                self._out["action_count"] = (
                                    int(self._out.get("action_count", 0)) + 1
                                )
                            else:
                                _bump(tl, "m52a_action_failed")
                return

            if idx == 5:
                rax = self.structures(UnitTypeId.BARRACKS).ready
                marine_amt = self.units(UnitTypeId.MARINE).amount
                if rax and self.supply_left > 0 and self.can_afford(UnitTypeId.MARINE):
                    if marine_amt < _CAP_MARINES:
                        n = self.train(UnitTypeId.MARINE, 1)
                        if n > 0:
                            _bump(tl, "m52a_train_marine", int(n))
                            self._out["action_count"] = int(self._out.get("action_count", 0)) + int(
                                n,
                            )
                        else:
                            _bump(tl, "m52a_action_failed")
                return

            if idx == 6:
                pts = self._safe_patrol_points()
                ready_m = self.units(UnitTypeId.MARINE).ready
                if pts is not None and ready_m and gl > 200:
                    p_a, p_b = pts
                    tgt = p_a if (iteration // 48) % 2 == 0 else p_b
                    cmds = 0
                    for um in list(ready_m)[:6]:
                        try:
                            self.do(um.patrol(tgt))  # type: ignore[arg-type]
                            cmds += 1
                        except (AttributeError, RuntimeError, ValueError):
                            _bump(tl, "m52a_action_failed")
                    if cmds > 0:
                        _bump(tl, "m52a_move_army", cmds)
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + cmds
                else:
                    _bump(tl, "m52a_no_op")
                return

            if idx == 7:
                marine_units = self.units(UnitTypeId.MARINE)
                if not self._scout_done and marine_units and marine_units.ready:
                    scout = marine_units.ready.first
                    if scout is not None:
                        target = self.game_info.map_center
                        self.do(scout.move(target))  # type: ignore[arg-type]
                        _bump(tl, "m52a_scout")
                        self._out["action_count"] = int(self._out.get("action_count", 0)) + 1
                        self._scout_done = True
                return

    return _M52aCandidateProjectionSpikeBot
