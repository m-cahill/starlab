"""Load M23 tournament artifacts; derive diagnostics, standing explanations, failure views (M24)."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Literal

from starlab._io import JSON_ROOT_MUST_BE_OBJECT, parse_json_object_text
from starlab.evaluation.diagnostics_models import (
    EVALUATION_DIAGNOSTICS_NON_CLAIMS_V1,
    EVALUATION_DIAGNOSTICS_REPORT_VERSION,
    EVALUATION_DIAGNOSTICS_VERSION,
    EVALUATION_DIAGNOSTICS_WARNINGS_V1,
    REQUIRED_TOURNAMENT_VERSION,
)

Outcome3 = Literal["win_a", "win_b", "draw"]


def load_tournament_json(path: Path) -> dict[str, Any]:
    """Load ``evaluation_tournament.json`` as a dict."""

    raw = path.read_text(encoding="utf-8")
    obj, err = parse_json_object_text(raw)
    if err is None:
        assert obj is not None
        return obj
    if err == JSON_ROOT_MUST_BE_OBJECT:
        msg = "tournament artifact must be a JSON object"
        raise TypeError(msg)
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in tournament artifact: {exc}"
        raise ValueError(msg) from exc
    raise RuntimeError("unreachable")


def _require_keys(obj: dict[str, Any], keys: tuple[str, ...], *, label: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        msg = f"{label}: missing required keys: {', '.join(sorted(missing))}"
        raise ValueError(msg)


def validate_tournament_for_diagnostics(tournament: dict[str, Any]) -> None:
    """Structural + semantic validation for M23 ``evaluation_tournament.json``.

    No new JSON Schema in M24.
    """

    label = "evaluation tournament"
    _require_keys(
        tournament,
        (
            "benchmark_contract_sha256",
            "benchmark_id",
            "entrants",
            "evaluation_posture",
            "matches",
            "measurement_surface",
            "standings",
            "tournament_id",
            "tournament_version",
        ),
        label=label,
    )

    if tournament["tournament_version"] != REQUIRED_TOURNAMENT_VERSION:
        msg = f"{label}: unsupported tournament_version {tournament['tournament_version']!r}"
        raise ValueError(msg)
    if tournament.get("measurement_surface") != "fixture_only":
        msg = f"{label}: measurement_surface must be fixture_only"
        raise ValueError(msg)
    if tournament.get("evaluation_posture") != "fixture_only":
        msg = f"{label}: evaluation_posture must be fixture_only"
        raise ValueError(msg)

    entrants: list[dict[str, Any]] = []
    raw_entrants = tournament["entrants"]
    if not isinstance(raw_entrants, list):
        msg = f"{label}: entrants must be an array"
        raise ValueError(msg)
    for i, e in enumerate(raw_entrants):
        if not isinstance(e, dict):
            msg = f"{label}: entrants[{i}] must be an object"
            raise ValueError(msg)
        _require_keys(
            e,
            ("entrant_id", "source_scorecard_ref", "subject_id", "subject_kind", "suite_id"),
            label=f"{label} entrants[{i}]",
        )
        entrants.append(e)

    entrant_ids = [e["entrant_id"] for e in entrants]
    if len(set(entrant_ids)) != len(entrant_ids):
        msg = f"{label}: duplicate entrant_id in entrants"
        raise ValueError(msg)
    entrant_set = set(entrant_ids)

    matches_raw = tournament["matches"]
    if not isinstance(matches_raw, list):
        msg = f"{label}: matches must be an array"
        raise ValueError(msg)
    for i, m in enumerate(matches_raw):
        if not isinstance(m, dict):
            msg = f"{label}: matches[{i}] must be an object"
            raise ValueError(msg)
        _require_keys(
            m,
            (
                "entrant_a_id",
                "entrant_b_id",
                "match_id",
                "metric_comparisons",
                "points_awarded",
                "primary_metric_decision",
                "result",
            ),
            label=f"{label} matches[{i}]",
        )
        ea = m["entrant_a_id"]
        eb = m["entrant_b_id"]
        if ea not in entrant_set or eb not in entrant_set:
            msg = f"{label}: matches[{i}] references unknown entrant_id"
            raise ValueError(msg)
        if ea == eb:
            msg = f"{label}: matches[{i}] has identical entrant_a_id and entrant_b_id"
            raise ValueError(msg)
        res = m["result"]
        if res != "draw" and res != "win":
            msg = f"{label}: matches[{i}] has invalid result"
            raise ValueError(msg)
        if res == "draw":
            if m.get("winner_entrant_id") is not None:
                msg = f"{label}: matches[{i}] draw must have null winner_entrant_id"
                raise ValueError(msg)
        else:
            wid = m.get("winner_entrant_id")
            if wid not in (ea, eb):
                msg = f"{label}: matches[{i}] winner_entrant_id must be entrant_a or entrant_b"
                raise ValueError(msg)

    standings_raw = tournament["standings"]
    if not isinstance(standings_raw, list):
        msg = f"{label}: standings must be an array"
        raise ValueError(msg)
    if len(standings_raw) != len(entrant_ids):
        msg = f"{label}: standings length must match entrants length"
        raise ValueError(msg)

    seen_ids: set[str] = set()
    ranks: list[int] = []
    for i, row in enumerate(standings_raw):
        if not isinstance(row, dict):
            msg = f"{label}: standings[{i}] must be an object"
            raise ValueError(msg)
        _require_keys(
            row,
            (
                "draws",
                "entrant_id",
                "losses",
                "points",
                "primary_metric_id",
                "primary_metric_optimization_direction",
                "primary_metric_tiebreak_scalar",
                "primary_metric_value",
                "rank",
                "wins",
            ),
            label=f"{label} standings[{i}]",
        )
        eid = row["entrant_id"]
        if eid not in entrant_set:
            msg = f"{label}: standings[{i}] unknown entrant_id"
            raise ValueError(msg)
        if eid in seen_ids:
            msg = f"{label}: duplicate entrant_id in standings"
            raise ValueError(msg)
        seen_ids.add(eid)
        ranks.append(int(row["rank"]))

    if seen_ids != entrant_set:
        msg = f"{label}: standings entrant_id set must match entrants"
        raise ValueError(msg)

    ranks_sorted = sorted(ranks)
    want = list(range(1, len(entrant_ids) + 1))
    if ranks_sorted != want:
        msg = f"{label}: standings ranks must be a permutation of 1..N"
        raise ValueError(msg)

    # Order matches M23 standings order: descending points, tiebreak scalar, ascending entrant_id.
    for i in range(len(standings_raw) - 1):
        a = standings_raw[i]
        b = standings_raw[i + 1]
        if a["points"] < b["points"]:
            msg = f"{label}: standings must be ordered by points descending"
            raise ValueError(msg)
        if a["points"] == b["points"]:
            if a["primary_metric_tiebreak_scalar"] < b["primary_metric_tiebreak_scalar"]:
                msg = f"{label}: standings tie-break scalar ordering invalid for equal points"
                raise ValueError(msg)
            if (
                a["primary_metric_tiebreak_scalar"] == b["primary_metric_tiebreak_scalar"]
                and a["entrant_id"] >= b["entrant_id"]
            ):
                msg = (
                    f"{label}: standings lexicographic entrant_id ordering invalid for equal points"
                )
                raise ValueError(msg)


def _match_outcome(m: dict[str, Any]) -> Outcome3:
    if m["result"] == "draw":
        return "draw"
    assert m["winner_entrant_id"] is not None
    if m["winner_entrant_id"] == m["entrant_a_id"]:
        return "win_a"
    return "win_b"


def _adjacent_separation(
    upper: dict[str, Any],
    lower: dict[str, Any],
) -> Literal["higher_points", "higher_primary_tiebreak_scalar", "lexicographic_entrant_id"]:
    if upper["points"] != lower["points"]:
        return "higher_points"
    if upper["primary_metric_tiebreak_scalar"] != lower["primary_metric_tiebreak_scalar"]:
        return "higher_primary_tiebreak_scalar"
    return "lexicographic_entrant_id"


def _lexicographic_tiebreak_used_for_row(
    standings_by_id: dict[str, dict[str, Any]],
    row: dict[str, Any],
) -> bool:
    pts = row["points"]
    tb = row["primary_metric_tiebreak_scalar"]
    eid = row["entrant_id"]
    peers = [
        s
        for s in standings_by_id.values()
        if s["points"] == pts
        and s["primary_metric_tiebreak_scalar"] == tb
        and s["entrant_id"] != eid
    ]
    return len(peers) > 0


def _tiebreak_scalar_decided_rank(row: dict[str, Any], standings: list[dict[str, Any]]) -> bool:
    """True if another entrant shares tournament points but differs in primary tie-break scalar."""

    pts = row["points"]
    eid = row["entrant_id"]
    tb = row["primary_metric_tiebreak_scalar"]
    for s in standings:
        if s["entrant_id"] == eid:
            continue
        if s["points"] == pts and s["primary_metric_tiebreak_scalar"] != tb:
            return True
    return False


def build_derived_views(tournament: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (evaluation_diagnostics, evaluation_diagnostics_report) dicts."""

    validate_tournament_for_diagnostics(tournament)

    warnings = sorted(EVALUATION_DIAGNOSTICS_WARNINGS_V1)
    non_claims = sorted(EVALUATION_DIAGNOSTICS_NON_CLAIMS_V1)

    entrants = tournament["entrants"]
    matches = tournament["matches"]
    standings = tournament["standings"]
    standings_by_id = {row["entrant_id"]: row for row in standings}

    # Match diagnostics (M23 match order).
    match_diagnostics: list[dict[str, Any]] = []
    for m in matches:
        pmd = m["primary_metric_decision"]
        match_diagnostics.append(
            {
                "decisive_metric_id": pmd["decisive_metric_id"],
                "decisive_metric_role": "primary",
                "entrant_a_id": m["entrant_a_id"],
                "entrant_b_id": m["entrant_b_id"],
                "match_id": m["match_id"],
                "metric_comparisons": m["metric_comparisons"],
                "outcome": _match_outcome(m),
                "points_awarded": m["points_awarded"],
                "winner_entrant_id": m.get("winner_entrant_id"),
            },
        )

    # Opponent results per entrant (match order).
    opponent_results: dict[str, list[dict[str, Any]]] = {e["entrant_id"]: [] for e in entrants}
    for m in matches:
        pa = m["points_awarded"]
        eid_a = m["entrant_a_id"]
        eid_b = m["entrant_b_id"]
        if m["result"] == "draw":
            opponent_results[eid_a].append(
                {
                    "match_id": m["match_id"],
                    "opponent_entrant_id": eid_b,
                    "outcome": "draw",
                    "points_awarded": float(pa[eid_a]),
                },
            )
            opponent_results[eid_b].append(
                {
                    "match_id": m["match_id"],
                    "opponent_entrant_id": eid_a,
                    "outcome": "draw",
                    "points_awarded": float(pa[eid_b]),
                },
            )
        else:
            assert m["winner_entrant_id"] is not None
            winner = m["winner_entrant_id"]
            loser = eid_b if winner == eid_a else eid_a
            opponent_results[winner].append(
                {
                    "match_id": m["match_id"],
                    "opponent_entrant_id": loser,
                    "outcome": "win",
                    "points_awarded": float(pa[winner]),
                },
            )
            opponent_results[loser].append(
                {
                    "match_id": m["match_id"],
                    "opponent_entrant_id": winner,
                    "outcome": "loss",
                    "points_awarded": float(pa[loser]),
                },
            )

    entrant_diagnostics: list[dict[str, Any]] = []
    for e in entrants:
        eid = e["entrant_id"]
        st = standings_by_id[eid]
        entrant_diagnostics.append(
            {
                "draws": st["draws"],
                "entrant_id": eid,
                "losses": st["losses"],
                "opponent_results": opponent_results[eid],
                "points": st["points"],
                "primary_metric_value": st["primary_metric_value"],
                "primary_tiebreak_scalar": st["primary_metric_tiebreak_scalar"],
                "source_scorecard_ref": e["source_scorecard_ref"],
                "standing_rank": st["rank"],
                "subject_id": e["subject_id"],
                "subject_kind": e["subject_kind"],
                "suite_id": e["suite_id"],
                "wins": st["wins"],
            },
        )

    standing_explanations: list[dict[str, Any]] = []
    for i, row in enumerate(standings):
        adj: dict[str, Any] | None
        if i + 1 < len(standings):
            lower = standings[i + 1]
            adj = {
                "lower_rank_entrant_id": lower["entrant_id"],
                "separated_by": _adjacent_separation(row, lower),
            }
        else:
            adj = None
        standing_explanations.append(
            {
                "adjacent_comparison": adj,
                "entrant_id": row["entrant_id"],
                "explained_by": {
                    "lexicographic_tiebreak_used": _lexicographic_tiebreak_used_for_row(
                        standings_by_id,
                        row,
                    ),
                    "points": row["points"],
                    "primary_tiebreak_scalar": row["primary_metric_tiebreak_scalar"],
                },
                "rank": row["rank"],
            },
        )

    zero_win = [
        {"entrant_id": eid}
        for eid in sorted(eid for eid, s in standings_by_id.items() if s["wins"] == 0)
    ]
    min_pts = min(s["points"] for s in standings)
    lowest_pts = [
        {"entrant_id": s["entrant_id"]}
        for s in sorted(
            (s for s in standings_by_id.values() if s["points"] == min_pts),
            key=lambda row: row["entrant_id"],
        )
    ]

    draws_equal_primary: list[dict[str, Any]] = []
    for m in matches:
        if m["result"] != "draw":
            continue
        pmd = m["primary_metric_decision"]
        if pmd["entrant_a_value"] == pmd["entrant_b_value"]:
            draws_equal_primary.append(
                {
                    "entrant_a_id": m["entrant_a_id"],
                    "entrant_b_id": m["entrant_b_id"],
                    "match_id": m["match_id"],
                    "primary_metric_id": pmd["decisive_metric_id"],
                },
            )

    tb_scalar_ids: set[str] = set()
    for row in standings:
        if _tiebreak_scalar_decided_rank(row, standings):
            tb_scalar_ids.add(row["entrant_id"])
    tb_scalar_entrants = [{"entrant_id": eid} for eid in sorted(tb_scalar_ids)]

    # Lexicographic: any entrant in a points+tiebreak_scalar group of size > 1.
    lex_groups: defaultdict[tuple[Any, Any], list[str]] = defaultdict(list)
    for row in standings:
        key = (row["points"], row["primary_metric_tiebreak_scalar"])
        lex_groups[key].append(row["entrant_id"])
    lex_used = {eid for eids in lex_groups.values() if len(eids) > 1 for eid in eids}
    lex_entrants = [{"entrant_id": eid} for eid in sorted(lex_used)]

    failure_views: dict[str, Any] = {
        "draws_equal_primary_metric": draws_equal_primary,
        "lowest_points_entrants": lowest_pts,
        "standings_used_lexicographic_tiebreak": lex_entrants,
        "standings_used_tiebreak_scalar": tb_scalar_entrants,
        "zero_win_entrants": zero_win,
    }

    failure_view_count = sum(len(v) for v in failure_views.values())

    diagnostics: dict[str, Any] = {
        "benchmark_contract_sha256": tournament["benchmark_contract_sha256"],
        "benchmark_id": tournament["benchmark_id"],
        "diagnostics_version": EVALUATION_DIAGNOSTICS_VERSION,
        "entrant_diagnostics": entrant_diagnostics,
        "evaluation_posture": tournament["evaluation_posture"],
        "failure_views": failure_views,
        "match_diagnostics": match_diagnostics,
        "measurement_surface": tournament["measurement_surface"],
        "non_claims": non_claims,
        "standing_explanations": standing_explanations,
        "tournament_id": tournament["tournament_id"],
        "warnings": warnings,
    }

    report: dict[str, Any] = {
        "benchmark_contract_sha256": tournament["benchmark_contract_sha256"],
        "diagnostics_verdict": "pass",
        "entrant_count": len(entrants),
        "failures": [],
        "failure_view_count": failure_view_count,
        "match_count": len(matches),
        "non_claims": non_claims,
        "report_version": EVALUATION_DIAGNOSTICS_REPORT_VERSION,
        "warnings": warnings,
    }

    return diagnostics, report
