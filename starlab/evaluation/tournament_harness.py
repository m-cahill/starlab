"""Deterministic round-robin tournament harness over scorecard-derived entrants (M23)."""

from __future__ import annotations

from typing import Any, Literal

from starlab.benchmarks.benchmark_contract_models import OPTIMIZATION_DIRECTION_VALUES


def find_primary_metric_definition(
    benchmark_contract: dict[str, Any],
) -> dict[str, Any]:
    """Return the first metric definition with ``scoring_role`` ``primary`` (contract order)."""

    defs: list[dict[str, Any]] = list(benchmark_contract["metric_definitions"])
    for md in defs:
        if md.get("scoring_role") == "primary":
            return md
    msg = "benchmark contract has no primary metric definition"
    raise ValueError(msg)


def _metric_value_map(scorecard: dict[str, Any]) -> dict[str, float | int | None]:
    out: dict[str, float | int | None] = {}
    for row in scorecard["metric_rows"]:
        out[row["metric_id"]] = row["value"]
    return out


def _compare_numeric(
    a: float | int | None,
    b: float | int | None,
    direction: str,
) -> Literal["a", "b", "tie"]:
    if a is None or b is None:
        msg = "metric value cannot be null for tournament comparison"
        raise ValueError(msg)
    if direction == "maximize":
        if a > b:
            return "a"
        if b > a:
            return "b"
        return "tie"
    if direction == "minimize":
        if a < b:
            return "a"
        if b < a:
            return "b"
        return "tie"
    if direction == "none":
        return "tie"
    msg = f"unsupported optimization_direction for comparison: {direction!r}"
    raise ValueError(msg)


def _primary_tiebreak_scalar(
    value: float | int | None,
    direction: str,
) -> float:
    """Higher sort key is better in standings tie-break (after points)."""

    if value is None:
        msg = "primary metric value cannot be null for tie-break"
        raise ValueError(msg)
    v = float(value)
    if direction == "maximize":
        return v
    if direction == "minimize":
        return -v
    if direction == "none":
        return v
    msg = f"unsupported optimization_direction for tie-break: {direction!r}"
    raise ValueError(msg)


def run_round_robin_tournament(
    *,
    benchmark_contract: dict[str, Any],
    entrants: list[dict[str, Any]],
    scorecards_by_entrant: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (matches, standings) in deterministic order."""

    n = len(entrants)
    primary = find_primary_metric_definition(benchmark_contract)
    primary_id = primary["metric_id"]
    primary_direction = primary["optimization_direction"]
    if primary_direction not in OPTIMIZATION_DIRECTION_VALUES:
        msg = "invalid optimization_direction on primary metric"
        raise ValueError(msg)

    metric_defs: list[dict[str, Any]] = list(benchmark_contract["metric_definitions"])

    matches: list[dict[str, Any]] = []
    match_no = 0
    points: dict[str, float] = {e["entrant_id"]: 0.0 for e in entrants}
    wins: dict[str, int] = {e["entrant_id"]: 0 for e in entrants}
    draws: dict[str, int] = {e["entrant_id"]: 0 for e in entrants}
    losses: dict[str, int] = {e["entrant_id"]: 0 for e in entrants}

    for i in range(n):
        for j in range(i + 1, n):
            match_no += 1
            ea = entrants[i]
            eb = entrants[j]
            eid_a = ea["entrant_id"]
            eid_b = eb["entrant_id"]
            sc_a = scorecards_by_entrant[eid_a]
            sc_b = scorecards_by_entrant[eid_b]
            map_a = _metric_value_map(sc_a)
            map_b = _metric_value_map(sc_b)

            pv_a = map_a.get(primary_id)
            pv_b = map_b.get(primary_id)
            primary_cmp = _compare_numeric(pv_a, pv_b, primary_direction)

            metric_comparisons: list[dict[str, Any]] = []
            for md in metric_defs:
                mid = md["metric_id"]
                direction = md["optimization_direction"]
                va = map_a.get(mid)
                vb = map_b.get(mid)
                side = _compare_numeric(va, vb, direction)
                better: str | None
                if side == "tie":
                    better = None
                elif side == "a":
                    better = eid_a
                else:
                    better = eid_b
                metric_comparisons.append(
                    {
                        "better_entrant_id": better,
                        "entrant_a_value": va,
                        "entrant_b_value": vb,
                        "metric_id": mid,
                        "optimization_direction": direction,
                        "scoring_role": md["scoring_role"],
                        "unit": md["unit"],
                    },
                )

            if primary_cmp == "tie":
                result = "draw"
                winner_id: str | None = None
                loser_id: str | None = None
                points[eid_a] += 0.5
                points[eid_b] += 0.5
                draws[eid_a] += 1
                draws[eid_b] += 1
            elif primary_cmp == "a":
                result = "win"
                winner_id = eid_a
                loser_id = eid_b
                points[eid_a] += 1.0
                losses[eid_b] += 1
                wins[eid_a] += 1
            else:
                result = "win"
                winner_id = eid_b
                loser_id = eid_a
                points[eid_b] += 1.0
                losses[eid_a] += 1
                wins[eid_b] += 1

            match_id = f"starlab.evaluation_tournament.v1.match.{match_no:04d}"
            matches.append(
                {
                    "entrant_a_id": eid_a,
                    "entrant_b_id": eid_b,
                    "loser_entrant_id": loser_id,
                    "match_id": match_id,
                    "metric_comparisons": metric_comparisons,
                    "points_awarded": (
                        {eid_a: 0.5, eid_b: 0.5}
                        if result == "draw"
                        else (
                            {winner_id: 1.0, loser_id: 0.0}
                            if winner_id is not None and loser_id is not None
                            else {}
                        )
                    ),
                    "primary_metric_decision": {
                        "decisive_metric_id": primary_id,
                        "entrant_a_value": pv_a,
                        "entrant_b_value": pv_b,
                        "optimization_direction": primary_direction,
                        "outcome": primary_cmp,
                    },
                    "result": result,
                    "winner_entrant_id": winner_id,
                },
            )

    standings_rows: list[tuple[float, float, str]] = []
    for e in entrants:
        eid = e["entrant_id"]
        sc = scorecards_by_entrant[eid]
        pmap = _metric_value_map(sc)
        pv = pmap.get(primary_id)
        tb = _primary_tiebreak_scalar(pv, primary_direction)
        standings_rows.append((points[eid], tb, eid))

    standings_rows.sort(key=lambda r: (-r[0], -r[1], r[2]))

    standings: list[dict[str, Any]] = []
    for rank, (pts, tb_scalar, eid) in enumerate(standings_rows, start=1):
        sc = scorecards_by_entrant[eid]
        pmap = _metric_value_map(sc)
        standings.append(
            {
                "draws": draws[eid],
                "entrant_id": eid,
                "losses": losses[eid],
                "points": pts,
                "primary_metric_id": primary_id,
                "primary_metric_optimization_direction": primary_direction,
                "primary_metric_tiebreak_scalar": tb_scalar,
                "primary_metric_value": pmap.get(primary_id),
                "rank": rank,
                "wins": wins[eid],
            },
        )

    return matches, standings


def collect_scorecards_by_entrant(
    suites: list[dict[str, Any]],
    entrants: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Map entrant_id to embedded scorecard dict (suite order + scorecard order)."""

    by_entrant: dict[str, dict[str, Any]] = {}
    idx = 0
    for suite in suites:
        for sc in suite["scorecards"]:
            entrant_id = entrants[idx]["entrant_id"]
            by_entrant[entrant_id] = sc
            idx += 1
    if idx != len(entrants):
        msg = "entrant/scorecard alignment mismatch"
        raise ValueError(msg)
    return by_entrant
