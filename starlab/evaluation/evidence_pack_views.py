"""Build baseline evidence pack views (M25).

Upstream: M21/M22 suites, M23 tournament, M24 diagnostics.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab._io import JSON_ROOT_MUST_BE_OBJECT, parse_json_object_text
from starlab.evaluation.evidence_pack_models import (
    BASELINE_EVIDENCE_PACK_NON_CLAIMS_V1,
    BASELINE_EVIDENCE_PACK_REPORT_VERSION,
    BASELINE_EVIDENCE_PACK_VERSION,
    BASELINE_EVIDENCE_PACK_WARNINGS_V1,
    FAILURE_VIEW_DRAW_EQUAL_PRIMARY,
    FAILURE_VIEW_LEXICOGRAPHIC,
    FAILURE_VIEW_LOWEST_POINTS,
    FAILURE_VIEW_TIEBREAK_SCALAR,
    FAILURE_VIEW_ZERO_WIN,
    REQUIRED_DIAGNOSTICS_VERSION,
    REQUIRED_TOURNAMENT_VERSION,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_json_object(path: Path) -> dict[str, Any]:
    """Load a JSON object from ``path``."""

    raw = path.read_text(encoding="utf-8")
    obj, err = parse_json_object_text(raw)
    if err is None:
        assert obj is not None
        return obj
    if err == JSON_ROOT_MUST_BE_OBJECT:
        msg = f"{path}: root must be a JSON object"
        raise TypeError(msg)
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in {path}: {exc}"
        raise ValueError(msg) from exc
    raise RuntimeError("unreachable")


def _require_keys(obj: dict[str, Any], keys: tuple[str, ...], *, label: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        msg = f"{label}: missing required keys: {', '.join(sorted(missing))}"
        raise ValueError(msg)


def _validate_tournament(tournament: dict[str, Any], *, label: str) -> None:
    _require_keys(
        tournament,
        (
            "benchmark_contract_sha256",
            "benchmark_id",
            "entrants",
            "evaluation_posture",
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


def _validate_diagnostics(diagnostics: dict[str, Any], *, label: str) -> None:
    _require_keys(
        diagnostics,
        (
            "benchmark_contract_sha256",
            "benchmark_id",
            "diagnostics_version",
            "entrant_diagnostics",
            "evaluation_posture",
            "failure_views",
            "measurement_surface",
            "tournament_id",
        ),
        label=label,
    )
    if diagnostics["diagnostics_version"] != REQUIRED_DIAGNOSTICS_VERSION:
        msg = f"{label}: unsupported diagnostics_version {diagnostics['diagnostics_version']!r}"
        raise ValueError(msg)
    if diagnostics.get("measurement_surface") != "fixture_only":
        msg = f"{label}: measurement_surface must be fixture_only"
        raise ValueError(msg)
    if diagnostics.get("evaluation_posture") != "fixture_only":
        msg = f"{label}: evaluation_posture must be fixture_only"
        raise ValueError(msg)


def _validate_suite(
    suite: dict[str, Any],
    *,
    label: str,
    tournament: dict[str, Any],
) -> None:
    _require_keys(
        suite,
        ("benchmark_contract_sha256", "benchmark_id"),
        label=label,
    )
    if suite["benchmark_contract_sha256"] != tournament["benchmark_contract_sha256"]:
        msg = f"{label}: benchmark_contract_sha256 does not match tournament"
        raise ValueError(msg)
    if suite["benchmark_id"] != tournament["benchmark_id"]:
        msg = f"{label}: benchmark_id does not match tournament"
        raise ValueError(msg)
    ms = suite.get("measurement_surface")
    if ms is not None and ms != "fixture_only":
        msg = f"{label}: measurement_surface must be fixture_only when present"
        raise ValueError(msg)
    ep = suite.get("evaluation_posture")
    if ep is not None and ep != "fixture_only":
        msg = f"{label}: evaluation_posture must be fixture_only when present"
        raise ValueError(msg)


def _failure_views_for_entrant(
    entrant_id: str,
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    fv = diagnostics["failure_views"]
    out: list[dict[str, Any]] = []

    for z in fv.get("zero_win_entrants", []):
        if z.get("entrant_id") == entrant_id:
            out.append(
                {
                    "failure_view_id": FAILURE_VIEW_ZERO_WIN,
                    "is_present": True,
                    "summary": (
                        "Entrant has zero wins under the governed M23 fixture-only tournament."
                    ),
                    "supporting_standing_context": {"bucket": "zero_win_entrants"},
                },
            )

    for z in fv.get("lowest_points_entrants", []):
        if z.get("entrant_id") == entrant_id:
            out.append(
                {
                    "failure_view_id": FAILURE_VIEW_LOWEST_POINTS,
                    "is_present": True,
                    "summary": "Entrant is among those with the lowest tournament points.",
                    "supporting_standing_context": {"bucket": "lowest_points_entrants"},
                },
            )

    for row in fv.get("draws_equal_primary_metric", []):
        if entrant_id in (row.get("entrant_a_id"), row.get("entrant_b_id")):
            mid = row.get("match_id")
            out.append(
                {
                    "failure_view_id": FAILURE_VIEW_DRAW_EQUAL_PRIMARY,
                    "is_present": True,
                    "summary": ("Draw where primary metric values are equal for both entrants."),
                    "supporting_match_ids": [mid] if mid is not None else [],
                },
            )

    for z in fv.get("standings_used_tiebreak_scalar", []):
        if z.get("entrant_id") == entrant_id:
            out.append(
                {
                    "failure_view_id": FAILURE_VIEW_TIEBREAK_SCALAR,
                    "is_present": True,
                    "summary": (
                        "Standing rank uses primary tie-break scalar separation from peers "
                        "with equal tournament points."
                    ),
                    "supporting_standing_context": {"bucket": "standings_used_tiebreak_scalar"},
                },
            )

    for z in fv.get("standings_used_lexicographic_tiebreak", []):
        if z.get("entrant_id") == entrant_id:
            out.append(
                {
                    "failure_view_id": FAILURE_VIEW_LEXICOGRAPHIC,
                    "is_present": True,
                    "summary": (
                        "Standing rank uses lexicographic entrant_id tie-break among peers "
                        "with equal points and tie-break scalar."
                    ),
                    "supporting_standing_context": {
                        "bucket": "standings_used_lexicographic_tiebreak",
                    },
                },
            )

    def sort_key(d: dict[str, Any]) -> tuple[str, str, str]:
        mids = d.get("supporting_match_ids")
        mid_s = json.dumps(mids, sort_keys=True) if isinstance(mids, list) else ""
        return (d["failure_view_id"], d["summary"], mid_s)

    return sorted(out, key=sort_key)


def _build_pack_and_report(
    tournament: dict[str, Any],
    diagnostics: dict[str, Any],
    suite_by_sha: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    _validate_tournament(tournament, label="evaluation tournament")
    _validate_diagnostics(diagnostics, label="evaluation diagnostics")

    if diagnostics["benchmark_contract_sha256"] != tournament["benchmark_contract_sha256"]:
        msg = "diagnostics benchmark_contract_sha256 does not match tournament"
        raise ValueError(msg)
    if diagnostics["benchmark_id"] != tournament["benchmark_id"]:
        msg = "diagnostics benchmark_id does not match tournament"
        raise ValueError(msg)
    if diagnostics["tournament_id"] != tournament["tournament_id"]:
        msg = "diagnostics tournament_id does not match tournament"
        raise ValueError(msg)

    suite_sha_set = set(suite_by_sha.keys())
    for idx, (sha, suite) in enumerate(sorted(suite_by_sha.items())):
        _validate_suite(suite, label=f"suite[{idx}] sha={sha[:12]}...", tournament=tournament)

    entrants_raw = tournament["entrants"]
    if not isinstance(entrants_raw, list):
        msg = "tournament entrants must be an array"
        raise ValueError(msg)
    entrant_by_id: dict[str, dict[str, Any]] = {}
    for e in entrants_raw:
        if not isinstance(e, dict):
            msg = "tournament entrants must be objects"
            raise ValueError(msg)
        eid = e["entrant_id"]
        entrant_by_id[eid] = e

    subject_keys: set[tuple[str, str]] = set()
    for e in entrants_raw:
        ref = e["source_scorecard_ref"]
        sha = ref["suite_sha256"]
        if sha not in suite_by_sha:
            msg = (
                f"tournament entrant {e['entrant_id']!r}: suite_sha256 {sha!r} "
                f"is not covered by supplied suite inputs"
            )
            raise ValueError(msg)
        loaded = suite_by_sha[sha]
        if sha256_hex_of_canonical_json(loaded) != sha:
            msg = f"suite canonical hash mismatch for entrant {e['entrant_id']!r}"
            raise ValueError(msg)
        sk = (e["suite_id"], e["subject_id"])
        if sk in subject_keys:
            msg = f"duplicate suite subject coverage for (suite_id, subject_id)={sk!r}"
            raise ValueError(msg)
        subject_keys.add(sk)

    diag_entrants = diagnostics["entrant_diagnostics"]
    if not isinstance(diag_entrants, list):
        msg = "diagnostics entrant_diagnostics must be an array"
        raise ValueError(msg)
    diag_by_id: dict[str, dict[str, Any]] = {}
    for row in diag_entrants:
        if not isinstance(row, dict):
            msg = "entrant_diagnostics rows must be objects"
            raise ValueError(msg)
        diag_by_id[row["entrant_id"]] = row

    t_ids = set(entrant_by_id.keys())
    d_ids = set(diag_by_id.keys())
    if t_ids != d_ids:
        msg = "diagnostics entrant_id set does not match tournament entrants"
        raise ValueError(msg)

    standings = tournament["standings"]
    if not isinstance(standings, list):
        msg = "tournament standings must be an array"
        raise ValueError(msg)

    warnings = sorted(BASELINE_EVIDENCE_PACK_WARNINGS_V1)
    non_claims = sorted(BASELINE_EVIDENCE_PACK_NON_CLAIMS_V1)

    entrants_out: list[dict[str, Any]] = []
    for st in standings:
        eid = st["entrant_id"]
        ent = entrant_by_id[eid]
        ref = ent["source_scorecard_ref"]
        rank = int(st["rank"])
        entrants_out.append(
            {
                "entrant_id": eid,
                "evidence_refs": {
                    "suite_ref": {
                        "suite_id": ent["suite_id"],
                        "suite_version": ref["suite_version"],
                        "subject_id": ent["subject_id"],
                        "subject_kind": ent["subject_kind"],
                    },
                    "tournament_ref": {
                        "entrant_id": eid,
                        "standing_rank": rank,
                        "tournament_version": tournament["tournament_version"],
                    },
                    "diagnostics_ref": {
                        "diagnostics_version": REQUIRED_DIAGNOSTICS_VERSION,
                        "entrant_id": eid,
                    },
                },
                "failure_views": _failure_views_for_entrant(eid, diagnostics),
                "primary_metric": st["primary_metric_value"],
                "primary_tiebreak_scalar": st["primary_metric_tiebreak_scalar"],
                "standing_rank": rank,
                "subject_id": ent["subject_id"],
                "subject_kind": ent["subject_kind"],
                "suite_id": ent["suite_id"],
                "tournament_points": st["points"],
                "draws": st["draws"],
                "losses": st["losses"],
                "wins": st["wins"],
            },
        )

    tournament_sha256 = sha256_hex_of_canonical_json(tournament)
    diagnostics_sha256 = sha256_hex_of_canonical_json(diagnostics)
    suite_sha256s = sorted(suite_sha_set)

    pack: dict[str, Any] = {
        "benchmark_contract_sha256": tournament["benchmark_contract_sha256"],
        "diagnostics_sha256": diagnostics_sha256,
        "entrants": entrants_out,
        "evidence_pack_version": BASELINE_EVIDENCE_PACK_VERSION,
        "non_claims": non_claims,
        "suite_sha256s": suite_sha256s,
        "tournament_sha256": tournament_sha256,
        "warnings": warnings,
    }

    subject_kind_counts: dict[str, int] = {}
    for row in entrants_out:
        sk = row["subject_kind"]
        subject_kind_counts[sk] = subject_kind_counts.get(sk, 0) + 1

    failure_view_counts: dict[str, int] = {}
    for row in entrants_out:
        for fv in row["failure_views"]:
            if fv.get("is_present") is True:
                fid = fv["failure_view_id"]
                failure_view_counts[fid] = failure_view_counts.get(fid, 0) + 1

    evidence_pack_sha256 = sha256_hex_of_canonical_json(pack)

    report: dict[str, Any] = {
        "entrant_count": len(entrants_out),
        "evidence_pack_sha256": evidence_pack_sha256,
        "failure_view_counts": dict(sorted(failure_view_counts.items())),
        "non_claims": non_claims,
        "report_version": BASELINE_EVIDENCE_PACK_REPORT_VERSION,
        "subject_kind_counts": dict(sorted(subject_kind_counts.items())),
        "suite_count": len(suite_sha256s),
        "warnings": warnings,
    }

    return pack, report


def build_baseline_evidence_pack_artifacts(
    *,
    suite_paths: list[Path],
    tournament_path: Path,
    diagnostics_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (baseline_evidence_pack, baseline_evidence_pack_report) dicts."""

    tournament = load_json_object(tournament_path)
    diagnostics = load_json_object(diagnostics_path)

    suite_by_sha: dict[str, dict[str, Any]] = {}
    for p in suite_paths:
        suite = load_json_object(p)
        sha = sha256_hex_of_canonical_json(suite)
        suite_by_sha[sha] = suite

    return _build_pack_and_report(tournament, diagnostics, suite_by_sha)
