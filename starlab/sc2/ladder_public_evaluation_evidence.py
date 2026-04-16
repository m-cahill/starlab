"""Build deterministic ladder_public_evaluation_evidence.json + report (M59)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.ladder_public_evaluation_models import (
    ALLOWED_EVIDENCE_CLASSES,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_CONTRACT_ID,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_FILENAME,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_FILENAME,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_SCHEMA_VERSION,
    LADDER_PUBLIC_EVALUATION_EVIDENCE_SCHEMA_VERSION,
    LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID,
    LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
    EvidencePostureStatus,
)


def _as_str(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        msg = f"{field} must be a non-empty string"
        raise ValueError(msg)
    return value.strip()


def _row_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row.get("stable_match_id", ""),
        row.get("observed_at", ""),
        row.get("opponent_label", ""),
        row.get("map_name") or "",
        row.get("evidence_class", ""),
        row.get("source_reference") or "",
        row.get("replay_reference_hash") or "",
    )


def _normalize_result_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for i, raw in enumerate(rows):
        if not isinstance(raw, dict):
            msg = f"result_rows[{i}] must be an object"
            raise ValueError(msg)
        stable = _as_str(raw.get("stable_match_id", ""), f"result_rows[{i}].stable_match_id")
        if stable in seen:
            msg = f"duplicate stable_match_id {stable!r}"
            raise ValueError(msg)
        seen.add(stable)

        observed_at = _as_str(raw.get("observed_at", ""), f"result_rows[{i}].observed_at")
        venue = _as_str(raw.get("venue_surface_kind", ""), f"result_rows[{i}].venue_surface_kind")
        opponent = _as_str(raw.get("opponent_label", ""), f"result_rows[{i}].opponent_label")

        map_name = raw.get("map_name")
        if map_name is not None and not isinstance(map_name, str):
            msg = f"result_rows[{i}].map_name must be a string or null"
            raise ValueError(msg)
        map_name_norm = map_name.strip() if isinstance(map_name, str) else None
        if map_name_norm == "":
            map_name_norm = None

        mr = _as_str(raw.get("match_result", ""), f"result_rows[{i}].match_result")
        if mr not in ("win", "loss", "draw", "unknown"):
            msg = f"result_rows[{i}].match_result must be win|loss|draw|unknown"
            raise ValueError(msg)

        ev_class = _as_str(raw.get("evidence_class", ""), f"result_rows[{i}].evidence_class")
        if ev_class not in ALLOWED_EVIDENCE_CLASSES:
            msg = f"result_rows[{i}].evidence_class must be one of {ALLOWED_EVIDENCE_CLASSES!r}"
            raise ValueError(msg)

        rr = raw.get("replay_reference_hash")
        if rr is not None and not isinstance(rr, str):
            msg = f"result_rows[{i}].replay_reference_hash must be a string or null"
            raise ValueError(msg)
        rr_norm = rr.strip() if isinstance(rr, str) else None
        if rr_norm == "":
            rr_norm = None

        src_ref = raw.get("source_reference")
        if src_ref is not None and not isinstance(src_ref, str):
            msg = f"result_rows[{i}].source_reference must be a string or null"
            raise ValueError(msg)
        src_ref_norm = src_ref.strip() if isinstance(src_ref, str) else None
        if src_ref_norm == "":
            src_ref_norm = None

        subj = _as_str(
            raw.get("subject_candidate_id", ""),
            f"result_rows[{i}].subject_candidate_id",
        )

        absence_raw = raw.get("absence_flags")
        if absence_raw is None:
            absence_flags: list[str] = []
        else:
            if not isinstance(absence_raw, list):
                msg = f"result_rows[{i}].absence_flags must be an array of strings"
                raise ValueError(msg)
            absence_flags = sorted(
                {
                    _as_str(x, f"result_rows[{i}].absence_flags[{j}]")
                    for j, x in enumerate(absence_raw)
                }
            )

        row_obj: dict[str, Any] = {
            "stable_match_id": stable,
            "observed_at": observed_at,
            "venue_surface_kind": venue,
            "opponent_label": opponent,
            "match_result": mr,
            "evidence_class": ev_class,
            "subject_candidate_id": subj,
            "absence_flags": absence_flags,
        }
        if map_name_norm is not None:
            row_obj["map_name"] = map_name_norm
        if rr_norm is not None:
            row_obj["replay_reference_hash"] = rr_norm
        if src_ref_norm is not None:
            row_obj["source_reference"] = src_ref_norm
        out.append(dict(sorted(row_obj.items())))
    return sorted(out, key=_row_sort_key)


def _compute_aggregates(rows: list[dict[str, Any]]) -> dict[str, Any]:
    wins = losses = draws = unknowns = 0
    by_class: dict[str, int] = {c: 0 for c in ALLOWED_EVIDENCE_CLASSES}
    map_known = map_unknown = 0
    by_map: dict[str, dict[str, int]] = {}

    for row in rows:
        mr = row["match_result"]
        if mr == "win":
            wins += 1
        elif mr == "loss":
            losses += 1
        elif mr == "draw":
            draws += 1
        else:
            unknowns += 1
        evc = row["evidence_class"]
        by_class[evc] = by_class.get(evc, 0) + 1
        mn = row.get("map_name")
        if mn:
            map_known += 1
            bucket = by_map.setdefault(str(mn), {"wins": 0, "losses": 0, "draws": 0, "unknown": 0})
            if mr == "win":
                bucket["wins"] += 1
            elif mr == "loss":
                bucket["losses"] += 1
            elif mr == "draw":
                bucket["draws"] += 1
            else:
                bucket["unknown"] += 1
        else:
            map_unknown += 1

    return {
        "total_matches_observed": len(rows),
        "results": {"wins": wins, "losses": losses, "draws": draws, "unknown": unknowns},
        "counts_by_evidence_class": dict(sorted(by_class.items())),
        "map_coverage": {"known_map_name_rows": map_known, "unknown_map_name_rows": map_unknown},
        "per_map_results": dict(sorted((k, dict(sorted(v.items()))) for k, v in by_map.items())),
    }


def _coverage_gaps(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    for row in rows:
        sid = row["stable_match_id"]
        evc = row["evidence_class"]
        if evc == "replay_bound_result":
            has_replay = "replay_reference_hash" in row
            has_absence = "replay_missing" in row.get("absence_flags", [])
            if not has_replay and not has_absence:
                gaps.append(
                    {
                        "stable_match_id": sid,
                        "kind": "replay_linkage_incomplete",
                        "detail": (
                            "replay_bound_result without replay_reference_hash or absence_flags "
                            "containing 'replay_missing'"
                        ),
                    }
                )
        if not row.get("map_name"):
            gaps.append(
                {
                    "stable_match_id": sid,
                    "kind": "map_name_unknown",
                    "detail": "map_name absent — coverage treated as unknown for this row",
                }
            )
    return sorted(gaps, key=lambda g: (g["stable_match_id"], g["kind"], g["detail"]))


def _warnings_for_rows(rows: list[dict[str, Any]]) -> list[str]:
    out: list[str] = []
    for row in rows:
        if row["evidence_class"] == "operator_attested_result":
            out.append(
                f"operator_attested_result for stable_match_id={row['stable_match_id']!r} "
                "is weaker descriptive evidence (explicit posture)."
            )
    return sorted(out)


def _posture(
    rows: list[dict[str, Any]],
    gaps: list[dict[str, str]],
) -> EvidencePostureStatus:
    if any(g["kind"] == "replay_linkage_incomplete" for g in gaps):
        return "bounded_incomplete"
    if any(g["kind"] == "map_name_unknown" for g in gaps):
        return "bounded_incomplete"
    if any(row.get("absence_flags") for row in rows):
        return "bounded_incomplete"
    return "bounded_complete"


def ladder_public_evaluation_evidence_bundle(
    *,
    protocol_obj: dict[str, Any],
    result_input_obj: dict[str, Any],
    result_input_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if protocol_obj.get("contract_id") != LADDER_PUBLIC_EVALUATION_PROTOCOL_CONTRACT_ID:
        msg = "protocol contract_id mismatch"
        raise ValueError(msg)

    proto_hash = sha256_hex_of_canonical_json(protocol_obj)
    profile_id = _as_str(
        protocol_obj.get("protocol_profile_id", ""),
        "protocol.protocol_profile_id",
    )
    subject = protocol_obj.get("subject_candidate")
    if not isinstance(subject, dict):
        msg = "protocol.subject_candidate must be an object"
        raise ValueError(msg)
    expected_cand = _as_str(
        subject.get("candidate_id", ""),
        "protocol.subject_candidate.candidate_id",
    )
    surface = _as_str(
        protocol_obj.get("evaluation_surface_kind", ""),
        "protocol.evaluation_surface_kind",
    )
    protocol_classes = set(protocol_obj.get("accepted_evidence_classes", []))

    session_id = _as_str(result_input_obj.get("evidence_session_id", ""), "evidence_session_id")
    rows_raw = result_input_obj.get("result_rows")
    if not isinstance(rows_raw, list):
        msg = "result_rows must be an array"
        raise ValueError(msg)

    rows = _normalize_result_rows(list(rows_raw))

    for row in rows:
        if row["subject_candidate_id"] != expected_cand:
            msg = (
                f"subject_candidate_id mismatch for stable_match_id={row['stable_match_id']!r}: "
                f"expected {expected_cand!r}, got {row['subject_candidate_id']!r}"
            )
            raise ValueError(msg)
        if row["venue_surface_kind"] != surface:
            msg = (
                f"venue_surface_kind mismatch for stable_match_id={row['stable_match_id']!r}: "
                f"expected protocol evaluation_surface_kind {surface!r}, "
                f"got {row['venue_surface_kind']!r}"
            )
            raise ValueError(msg)
        evc = row["evidence_class"]
        if evc not in protocol_classes:
            msg = (
                f"evidence_class {evc!r} not accepted by protocol for "
                f"stable_match_id={row['stable_match_id']!r}"
            )
            raise ValueError(msg)

    aggregates = _compute_aggregates(rows)
    gaps = _coverage_gaps(rows)
    posture = _posture(rows, gaps)
    warn = _warnings_for_rows(rows)

    non_claims = list(protocol_obj.get("required_non_claims", []))
    if not isinstance(non_claims, list):
        msg = "protocol.required_non_claims must be an array"
        raise ValueError(msg)
    non_claims_str = [str(x) for x in non_claims]
    non_claims_str.append(
        "Evidence rows are synthetic or operator-provided descriptive inputs — not an assertion "
        "of ladder performance proof."
    )

    attribution = dict(
        sorted(
            {
                "emitter_module": "starlab.sc2.emit_ladder_public_evaluation_evidence",
                "protocol_canonical_sha256": proto_hash,
                "result_input_sha256": result_input_sha256,
                "schema_version": LADDER_PUBLIC_EVALUATION_EVIDENCE_SCHEMA_VERSION,
                "runtime_contract": LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
            }.items()
        )
    )

    evidence: dict[str, Any] = {
        "contract_id": LADDER_PUBLIC_EVALUATION_EVIDENCE_CONTRACT_ID,
        "schema_version": LADDER_PUBLIC_EVALUATION_EVIDENCE_SCHEMA_VERSION,
        "runtime_contract": LADDER_PUBLIC_EVALUATION_RUNTIME_DOC_REL_PATH,
        "protocol_profile_id": profile_id,
        "protocol_sha256": proto_hash,
        "evidence_session_id": session_id,
        "subject_candidate": dict(sorted(subject.items())),
        "result_rows": rows,
        "aggregate_summary": aggregates,
        "coverage_gaps": gaps,
        "evidence_posture_status": posture,
        "warnings": warn,
        "non_claims": non_claims_str,
        "generated_attribution": attribution,
    }
    evidence = dict(sorted(evidence.items()))

    report = {
        "schema_version": LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_SCHEMA_VERSION,
        "evidence_canonical_sha256": sha256_hex_of_canonical_json(evidence),
        "protocol_canonical_sha256": proto_hash,
        "evidence_artifact": LADDER_PUBLIC_EVALUATION_EVIDENCE_FILENAME,
        "report_artifact": LADDER_PUBLIC_EVALUATION_EVIDENCE_REPORT_FILENAME,
        "emitter_module": "starlab.sc2.emit_ladder_public_evaluation_evidence",
        "status": "ok",
        "evidence_posture_status": posture,
        "m59_boundary": {
            "summary": (
                "Descriptive aggregates only — no significance, confidence, or merge-bar language."
            ),
            "explicit_non_claim": (
                "This report does not prove benchmark integrity or replay↔execution equivalence."
            ),
        },
    }
    return evidence, report
