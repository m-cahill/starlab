"""Deterministic benchmark integrity evidence rows over M21–M25 fixture-only chain (M56)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.benchmark_integrity.benchmark_integrity_models import (
    BENCHMARK_INTEGRITY_EVIDENCE_CONTRACT_ID,
    BENCHMARK_INTEGRITY_EVIDENCE_REPORT_SCHEMA_VERSION,
    BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION,
    EVIDENCE_FILENAME,
    EVIDENCE_REPORT_FILENAME,
    EVIDENCE_ROW_ORDER,
    M56_RUNTIMEV1_EVIDENCE_GATES_REL_PATH,
    M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

_ART_SCRIPTED = "scripted_baseline_suite"
_ART_HEURISTIC = "heuristic_baseline_suite"
_ART_TOURNAMENT = "evaluation_tournament"
_ART_DIAGNOSTICS = "evaluation_diagnostics"
_ART_PACK = "baseline_evidence_pack"

_CORPUS_MARKERS: tuple[str, ...] = (
    "canonical_replay_corpus",
    "corpus_promotion_posture_canonical",
    '"corpus_promotion_posture": "canonical"',
    "replay_corpus_canonical",
)


def _load_json(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = f"{path}: JSON root must be an object"
        raise ValueError(msg)
    return obj


def _canonical_sha(obj: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(obj)


def evidence_non_claims() -> list[str]:
    return [
        "Benchmark integrity is not globally proved by this bounded M56 evidence surface.",
        "M56 evaluates only starlab.m56.scope.fixture_only_baseline_chain_v1 (M21–M25 chain).",
        "M56 does not subsume or replace the closed M52–M54 replay↔execution equivalence track.",
        "M56 does not assert live SC2 in CI, ladder/public performance, or learned-subject chains.",
        "Corpus promotion governance is not exercised when corpus_provenance_and_promotion is "
        "not_applicable for this fixture-only scope.",
    ]


def _scan_corpus_implication(*, objects: list[dict[str, Any]]) -> bool:
    for obj in objects:
        blob = canonical_json_dumps(obj)
        if any(m in blob for m in _CORPUS_MARKERS):
            return True
    return False


def _row(
    *,
    evidence_class: str,
    status: str,
    owned_surface: str,
    source_artifacts: list[dict[str, Any]],
    canonical_sha256s: dict[str, str],
    observations: list[str],
    residual_non_claims: list[str],
) -> dict[str, Any]:
    return {
        "evidence_class": evidence_class,
        "status": status,
        "owned_surface": owned_surface,
        "source_artifacts": source_artifacts,
        "canonical_sha256s": dict(sorted(canonical_sha256s.items())),
        "observations": observations,
        "residual_non_claims": residual_non_claims,
    }


def _artifact_refs(
    *,
    scripted_path: Path,
    heuristic_path: Path,
    tournament_path: Path,
    diagnostics_path: Path,
    pack_path: Path,
) -> list[dict[str, str]]:
    return [
        {"artifact": "scripted_baseline_suite.json", "path": str(scripted_path)},
        {"artifact": "heuristic_baseline_suite.json", "path": str(heuristic_path)},
        {"artifact": "evaluation_tournament.json", "path": str(tournament_path)},
        {"artifact": "evaluation_diagnostics.json", "path": str(diagnostics_path)},
        {"artifact": "baseline_evidence_pack.json", "path": str(pack_path)},
    ]


def _build_benchmark_contract_identity_row(
    *,
    m21: dict[str, Any],
    m22: dict[str, Any],
    tournament: dict[str, Any],
    diagnostics: dict[str, Any],
    pack: dict[str, Any],
    sha_map: dict[str, str],
    refs: list[dict[str, str]],
    owned: str,
) -> dict[str, Any]:
    obs: list[str] = []
    ids = [
        m21.get("benchmark_id"),
        m22.get("benchmark_id"),
        tournament.get("benchmark_id"),
        diagnostics.get("benchmark_id"),
    ]
    if isinstance(pack.get("benchmark_id"), str):
        ids.append(pack.get("benchmark_id"))

    shas = [
        m21.get("benchmark_contract_sha256"),
        m22.get("benchmark_contract_sha256"),
        tournament.get("benchmark_contract_sha256"),
        diagnostics.get("benchmark_contract_sha256"),
        pack.get("benchmark_contract_sha256"),
    ]
    if None in ids or None in shas:
        obs.append("missing_benchmark_id_or_benchmark_contract_sha256 in one or more artifacts")
        return _row(
            evidence_class="benchmark_contract_identity",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=[
                "A single benchmark contract identity across the chain is required for this scope.",
            ],
        )

    if len(set(ids)) != 1 or len(set(shas)) != 1:
        obs.append(f"benchmark_id_set={sorted({str(x) for x in ids})}")
        obs.append(f"benchmark_contract_sha256_set={sorted({str(x) for x in shas})}")
        return _row(
            evidence_class="benchmark_contract_identity",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=[
                "benchmark_contract_identity does not assert global benchmark integrity.",
            ],
        )

    obs.append(
        "benchmark_id and benchmark_contract_sha256 are consistent across M21/M22/M23/M24/M25 "
        "artifacts in this scope.",
    )
    return _row(
        evidence_class="benchmark_contract_identity",
        status="present",
        owned_surface=owned,
        source_artifacts=refs,
        canonical_sha256s=sha_map,
        observations=obs,
        residual_non_claims=[
            "benchmark_contract_identity is scoped to supplied artifact paths only.",
        ],
    )


def _suite_subject_pairs(suite: dict[str, Any]) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    sid = suite.get("suite_id")
    if not isinstance(sid, str):
        return out
    subs = suite.get("subjects")
    if not isinstance(subs, list):
        return out
    for s in subs:
        if isinstance(s, dict) and isinstance(s.get("subject_id"), str):
            out.add((sid, s["subject_id"]))
    return out


def _build_subject_identity_row(
    *,
    m21: dict[str, Any],
    m22: dict[str, Any],
    tournament: dict[str, Any],
    pack: dict[str, Any],
    sha_map: dict[str, str],
    refs: list[dict[str, str]],
    owned: str,
) -> dict[str, Any]:
    obs: list[str] = []
    expected = _suite_subject_pairs(m21) | _suite_subject_pairs(m22)

    entrants = tournament.get("entrants")
    if not isinstance(entrants, list):
        return _row(
            evidence_class="subject_identity_and_freeze",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=["tournament.entrants is missing or not an array"],
            residual_non_claims=["subject_identity_and_freeze is chain-local only."],
        )

    found: set[tuple[str, str]] = set()
    entrant_ids: list[str] = []
    for e in entrants:
        if not isinstance(e, dict):
            continue
        eid = e.get("entrant_id")
        if isinstance(eid, str):
            entrant_ids.append(eid)
        su = e.get("suite_id")
        sj = e.get("subject_id")
        if isinstance(su, str) and isinstance(sj, str):
            found.add((su, sj))

    if expected != found:
        obs.append(f"expected_suite_subject_pairs={sorted(expected)}")
        obs.append(f"tournament_suite_subject_pairs={sorted(found)}")
        return _row(
            evidence_class="subject_identity_and_freeze",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=["subject_identity_and_freeze does not prove global integrity."],
        )

    pack_rows = pack.get("entrants")
    if not isinstance(pack_rows, list):
        return _row(
            evidence_class="subject_identity_and_freeze",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=["baseline_evidence_pack.entrants is missing or not an array"],
            residual_non_claims=["subject_identity_and_freeze is chain-local only."],
        )

    pack_ids: set[str] = set()
    for row in pack_rows:
        if not isinstance(row, dict):
            continue
        eid = row.get("entrant_id")
        if isinstance(eid, str):
            pack_ids.add(eid)

    if set(entrant_ids) != pack_ids or len(entrant_ids) != len(set(entrant_ids)):
        obs.append(f"tournament_entrant_ids={sorted(set(entrant_ids))}")
        obs.append(f"pack_entrant_ids={sorted(pack_ids)}")
        return _row(
            evidence_class="subject_identity_and_freeze",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=["subject_identity_and_freeze does not prove global integrity."],
        )

    for row in pack_rows:
        if not isinstance(row, dict):
            continue
        eid = row.get("entrant_id")
        if not isinstance(eid, str):
            continue
        exp = next(
            (e for e in entrants if isinstance(e, dict) and e.get("entrant_id") == eid),
            None,
        )
        if exp is None:
            continue
        if row.get("subject_id") != exp.get("subject_id"):
            obs.append(f"pack_entrant_subject_mismatch for {eid!r}")
        if row.get("suite_id") != exp.get("suite_id"):
            obs.append(f"pack_entrant_suite_mismatch for {eid!r}")

    if obs:
        return _row(
            evidence_class="subject_identity_and_freeze",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=["subject_identity_and_freeze does not prove global integrity."],
        )

    obs.append(
        "Suite subject coverage matches tournament entrants; evidence pack entrant ids align "
        "with tournament entrant ids and suite/subject fields.",
    )
    return _row(
        evidence_class="subject_identity_and_freeze",
        status="present",
        owned_surface=owned,
        source_artifacts=refs,
        canonical_sha256s=sha_map,
        observations=obs,
        residual_non_claims=["subject_identity_and_freeze does not prove global integrity."],
    )


def _posture_ok(obj: dict[str, Any], *, label: str) -> tuple[bool, list[str]]:
    obs: list[str] = []
    ms = obj.get("measurement_surface")
    ep = obj.get("evaluation_posture")
    if ms is not None and ms != "fixture_only":
        obs.append(f"{label}: measurement_surface must be fixture_only or absent")
    if ep is not None and ep != "fixture_only":
        obs.append(f"{label}: evaluation_posture must be fixture_only or absent")
    return (len(obs) == 0, obs)


def _build_execution_posture_row(
    *,
    m21: dict[str, Any],
    m22: dict[str, Any],
    tournament: dict[str, Any],
    diagnostics: dict[str, Any],
    pack: dict[str, Any],
    sha_map: dict[str, str],
    refs: list[dict[str, str]],
    owned: str,
) -> dict[str, Any]:
    obs: list[str] = []
    for ok, part in (
        _posture_ok(m21, label="M21"),
        _posture_ok(m22, label="M22"),
        _posture_ok(tournament, label="M23"),
        _posture_ok(diagnostics, label="M24"),
    ):
        if not ok:
            obs.extend(part)

    ms = pack.get("measurement_surface")
    ep = pack.get("evaluation_posture")
    if ms is not None and ms != "fixture_only":
        obs.append("M25: measurement_surface must be fixture_only when present")
    if ep is not None and ep != "fixture_only":
        obs.append("M25: evaluation_posture must be fixture_only when present")

    if obs:
        return _row(
            evidence_class="execution_posture_receipts",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=[
                "execution_posture_receipts does not assert live SC2 evaluation.",
            ],
        )

    obs.append(
        "M21–M24 measurement_surface/evaluation_posture are fixture_only; M25 does not "
        "introduce stronger posture fields.",
    )
    return _row(
        evidence_class="execution_posture_receipts",
        status="present",
        owned_surface=owned,
        source_artifacts=refs,
        canonical_sha256s=sha_map,
        observations=obs,
        residual_non_claims=[
            "execution_posture_receipts does not assert live SC2 evaluation.",
        ],
    )


def _build_score_aggregation_row(
    *,
    tournament: dict[str, Any],
    diagnostics: dict[str, Any],
    pack: dict[str, Any],
    sha_map: dict[str, str],
    refs: list[dict[str, str]],
    owned: str,
) -> dict[str, Any]:
    obs: list[str] = []
    t_sha = _canonical_sha(tournament)
    d_sha = _canonical_sha(diagnostics)

    if pack.get("tournament_sha256") != t_sha:
        obs.append(
            "baseline_evidence_pack.tournament_sha256 does not match canonical evaluation "
            f"tournament.json sha256 ({t_sha})",
        )
    if pack.get("diagnostics_sha256") != d_sha:
        obs.append(
            "baseline_evidence_pack.diagnostics_sha256 does not match canonical evaluation "
            f"diagnostics.json sha256 ({d_sha})",
        )

    if diagnostics.get("tournament_id") != tournament.get("tournament_id"):
        obs.append("M24 diagnostics.tournament_id does not match M23 tournament.tournament_id")
    if diagnostics.get("benchmark_id") != tournament.get("benchmark_id"):
        obs.append("M24 diagnostics.benchmark_id does not match M23 tournament.benchmark_id")

    standings = tournament.get("standings")
    if not isinstance(standings, list):
        obs.append("tournament.standings is not an array")
    else:
        by_id: dict[str, dict[str, Any]] = {}
        for row in pack.get("entrants", []) if isinstance(pack.get("entrants"), list) else []:
            if isinstance(row, dict) and isinstance(row.get("entrant_id"), str):
                by_id[row["entrant_id"]] = row
        for st in standings:
            if not isinstance(st, dict):
                continue
            eid = st.get("entrant_id")
            if not isinstance(eid, str):
                continue
            pr = by_id.get(eid)
            if pr is None:
                obs.append(f"pack missing entrant row for tournament standing {eid!r}")
                continue
            if pr.get("tournament_points") != st.get("points"):
                obs.append(f"tournament_points mismatch for entrant {eid!r}")
            if pr.get("standing_rank") != st.get("rank"):
                obs.append(f"standing_rank mismatch for entrant {eid!r}")

    if obs:
        return _row(
            evidence_class="score_aggregation_reproducibility",
            status="missing",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=obs,
            residual_non_claims=[
                "M24 remains interpretive; M25 remains packaging/traceability over M23/M24.",
            ],
        )

    obs.append(
        "Evidence pack records canonical M23/M24 hashes; pack standings match tournament "
        "points/ranks; M24 diagnostics reference the same tournament identifiers as M23.",
    )
    return _row(
        evidence_class="score_aggregation_reproducibility",
        status="present",
        owned_surface=owned,
        source_artifacts=refs,
        canonical_sha256s=sha_map,
        observations=obs,
        residual_non_claims=[
            "M24 remains interpretive; M25 remains packaging/traceability over M23/M24.",
        ],
    )


def _build_corpus_row(
    *,
    m21: dict[str, Any],
    m22: dict[str, Any],
    tournament: dict[str, Any],
    diagnostics: dict[str, Any],
    pack: dict[str, Any],
    sha_map: dict[str, str],
    refs: list[dict[str, str]],
    owned: str,
) -> dict[str, Any]:
    if _scan_corpus_implication(objects=[m21, m22, tournament, diagnostics, pack]):
        return _row(
            evidence_class="corpus_provenance_and_promotion",
            status="present",
            owned_surface=owned,
            source_artifacts=refs,
            canonical_sha256s=sha_map,
            observations=[
                "canonical_replay_corpus / corpus promotion implication markers detected in "
                "supplied artifact bytes; not allowed for this fixture-only baseline-chain scope.",
            ],
            residual_non_claims=[
                "corpus_provenance_and_promotion does not assert global corpus governance.",
            ],
        )

    return _row(
        evidence_class="corpus_provenance_and_promotion",
        status="not_applicable",
        owned_surface=owned,
        source_artifacts=refs,
        canonical_sha256s=sha_map,
        observations=[
            "Fixture-only fixture chain does not exercise canonical replay-corpus promotion "
            "discipline.",
        ],
        residual_non_claims=[
            (
                "corpus_promotion_not_applicable does not imply corpus governance is satisfied "
                "elsewhere."
            ),
        ],
    )


def build_benchmark_integrity_evidence_artifact(
    *,
    scope_id: str,
    scripted_baseline_suite_path: Path,
    heuristic_baseline_suite_path: Path,
    evaluation_tournament_path: Path,
    evaluation_diagnostics_path: Path,
    baseline_evidence_pack_path: Path,
) -> dict[str, Any]:
    """Load governed M21–M25 paths and emit deterministic evidence rows."""

    if scope_id != M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1:
        msg = f"unsupported scope_id for M56: {scope_id!r}"
        raise ValueError(msg)

    m21 = _load_json(scripted_baseline_suite_path)
    m22 = _load_json(heuristic_baseline_suite_path)
    tournament = _load_json(evaluation_tournament_path)
    diagnostics = _load_json(evaluation_diagnostics_path)
    pack = _load_json(baseline_evidence_pack_path)

    sha_map: dict[str, str] = {
        _ART_SCRIPTED: _canonical_sha(m21),
        _ART_HEURISTIC: _canonical_sha(m22),
        _ART_TOURNAMENT: _canonical_sha(tournament),
        _ART_DIAGNOSTICS: _canonical_sha(diagnostics),
        _ART_PACK: _canonical_sha(pack),
    }

    refs = _artifact_refs(
        scripted_path=scripted_baseline_suite_path,
        heuristic_path=heuristic_baseline_suite_path,
        tournament_path=evaluation_tournament_path,
        diagnostics_path=evaluation_diagnostics_path,
        pack_path=baseline_evidence_pack_path,
    )

    owned = M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1

    rows_by_class: dict[str, dict[str, Any]] = {}
    rows_by_class["benchmark_contract_identity"] = _build_benchmark_contract_identity_row(
        m21=m21,
        m22=m22,
        tournament=tournament,
        diagnostics=diagnostics,
        pack=pack,
        sha_map=sha_map,
        refs=refs,
        owned=owned,
    )
    rows_by_class["subject_identity_and_freeze"] = _build_subject_identity_row(
        m21=m21,
        m22=m22,
        tournament=tournament,
        pack=pack,
        sha_map=sha_map,
        refs=refs,
        owned=owned,
    )
    rows_by_class["execution_posture_receipts"] = _build_execution_posture_row(
        m21=m21,
        m22=m22,
        tournament=tournament,
        diagnostics=diagnostics,
        pack=pack,
        sha_map=sha_map,
        refs=refs,
        owned=owned,
    )
    rows_by_class["score_aggregation_reproducibility"] = _build_score_aggregation_row(
        tournament=tournament,
        diagnostics=diagnostics,
        pack=pack,
        sha_map=sha_map,
        refs=refs,
        owned=owned,
    )
    rows_by_class["corpus_provenance_and_promotion"] = _build_corpus_row(
        m21=m21,
        m22=m22,
        tournament=tournament,
        diagnostics=diagnostics,
        pack=pack,
        sha_map=sha_map,
        refs=refs,
        owned=owned,
    )

    ordered_rows = [rows_by_class[k] for k in EVIDENCE_ROW_ORDER if k in rows_by_class]

    return {
        "contract_id": BENCHMARK_INTEGRITY_EVIDENCE_CONTRACT_ID,
        "schema_version": BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION,
        "milestone": "M56",
        "phase": "VII",
        "scope_id": scope_id,
        "runtime_contract": M56_RUNTIMEV1_EVIDENCE_GATES_REL_PATH,
        "evidence_rows": ordered_rows,
        "non_claims": evidence_non_claims(),
    }


def build_benchmark_integrity_evidence_report(*, evidence_obj: dict[str, Any]) -> dict[str, Any]:
    ev_hash = sha256_hex_of_canonical_json(evidence_obj)
    rows = evidence_obj.get("evidence_rows", [])
    counts: dict[str, int] = {}
    for r in rows:
        if isinstance(r, dict) and isinstance(r.get("status"), str):
            st = r["status"]
            counts[st] = counts.get(st, 0) + 1
    counts_sorted = dict(sorted(counts.items()))

    return {
        "schema_version": BENCHMARK_INTEGRITY_EVIDENCE_REPORT_SCHEMA_VERSION,
        "evidence_canonical_sha256": ev_hash,
        "evidence_artifact": EVIDENCE_FILENAME,
        "report_artifact": EVIDENCE_REPORT_FILENAME,
        "emitter_module": "starlab.benchmark_integrity.emit_benchmark_integrity_evidence",
        "implemented_scope_id": evidence_obj.get("scope_id"),
        "contract_id": evidence_obj.get("contract_id"),
        "row_counts_by_status": counts_sorted,
        "residual_non_claims": [
            "Benchmark integrity is not globally proved by this bounded M56 evidence surface.",
            "Why this is still not global benchmark integrity: M56 is intentionally narrow "
            "(fixture-only offline M21–M25 chain), does not cover learned replay subjects, "
            "live/local evaluation, ladder/public protocols, or replay-corpus promotion proofs.",
        ],
        "why_not_global_benchmark_integrity": (
            "M56 emits bounded evidence rows and reproducibility gates for fixture-only baseline "
            "artifacts only; it does not prove benchmark integrity across all STARLAB subjects or "
            "runtime postures."
        ),
    }


def benchmark_integrity_evidence_bundle(
    *,
    scope_id: str,
    scripted_baseline_suite_path: Path,
    heuristic_baseline_suite_path: Path,
    evaluation_tournament_path: Path,
    evaluation_diagnostics_path: Path,
    baseline_evidence_pack_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ev = build_benchmark_integrity_evidence_artifact(
        scope_id=scope_id,
        scripted_baseline_suite_path=scripted_baseline_suite_path,
        heuristic_baseline_suite_path=heuristic_baseline_suite_path,
        evaluation_tournament_path=evaluation_tournament_path,
        evaluation_diagnostics_path=evaluation_diagnostics_path,
        baseline_evidence_pack_path=baseline_evidence_pack_path,
    )
    rep = build_benchmark_integrity_evidence_report(evidence_obj=ev)
    return ev, rep
