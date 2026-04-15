"""Gate pack: starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1 (M56)."""

from __future__ import annotations

from typing import Any, Final

from starlab.benchmark_integrity.benchmark_integrity_models import (
    BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION,
    M56_GATEPACK_FIXTURE_ONLY_BASELINE_CHAIN_V1,
    M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
)

_GATE_PREFIX: Final[str] = "starlab.m56.gate.fixture_only_baseline_chain"


def _row(
    *,
    gate_id: str,
    description: str,
    status: str,
    subject_refs: list[str],
    reason_codes: list[str],
    notes: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "description": description,
        "status": status,
        "subject_refs": subject_refs,
        "reason_codes": reason_codes,
        "notes": notes,
    }


def _row_for_class(
    evidence_rows: list[dict[str, Any]],
    evidence_class: str,
) -> dict[str, Any] | None:
    for r in evidence_rows:
        if isinstance(r, dict) and r.get("evidence_class") == evidence_class:
            return r
    return None


def evaluate_fixture_only_baseline_chain_reproducibility_v1(
    *,
    evidence: dict[str, Any],
) -> tuple[list[dict[str, Any]], str]:
    """Return ``(gate_results, scope_status)`` for the single M56 gate pack."""

    results: list[dict[str, Any]] = []

    def add(g: dict[str, Any]) -> None:
        results.append(g)

    if not isinstance(evidence, dict):
        add(
            _row(
                gate_id=f"{_GATE_PREFIX}.evidence_document",
                description="Evidence JSON must deserialize to an object.",
                status="not_evaluable",
                subject_refs=[],
                reason_codes=["evidence.not_object"],
                notes="Top-level JSON value is not an object.",
            )
        )
        return results, "not_evaluable"

    if evidence.get("schema_version") != BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION:
        add(
            _row(
                gate_id=f"{_GATE_PREFIX}.evidence_schema_recognized",
                description="Evidence schema_version matches M56 evidence contract.",
                status="not_evaluable",
                subject_refs=["schema_version"],
                reason_codes=["evidence.schema_version.unrecognized"],
                notes=f"Expected {BENCHMARK_INTEGRITY_EVIDENCE_SCHEMA_VERSION}.",
            )
        )
        return results, "not_evaluable"

    if evidence.get("scope_id") != M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1:
        add(
            _row(
                gate_id=f"{_GATE_PREFIX}.scope_id_recognized",
                description="Evidence scope_id matches the implemented M56 bounded scope.",
                status="not_evaluable",
                subject_refs=["scope_id"],
                reason_codes=["scope.unrecognized"],
                notes=f"Expected {M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1}.",
            )
        )
        return results, "not_evaluable"

    rows_raw = evidence.get("evidence_rows")
    if not isinstance(rows_raw, list):
        add(
            _row(
                gate_id=f"{_GATE_PREFIX}.evidence_rows_present",
                description="Evidence object must contain evidence_rows array.",
                status="not_evaluable",
                subject_refs=["evidence_rows"],
                reason_codes=["evidence_rows.missing"],
                notes="evidence_rows missing or not an array.",
            )
        )
        return results, "not_evaluable"

    rows: list[dict[str, Any]] = [r for r in rows_raw if isinstance(r, dict)]

    def status_of(ec: str) -> str | None:
        r = _row_for_class(rows, ec)
        if r is None:
            return None
        st = r.get("status")
        return str(st) if isinstance(st, str) else None

    # 1) Contract identity stable
    st_b = status_of("benchmark_contract_identity")
    ok_b = st_b == "present"
    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.contract_identity_stable_v1",
            description="benchmark_contract_identity evidence row is present (stable ids/shas).",
            status="pass" if ok_b else "fail",
            subject_refs=["benchmark_contract_identity"],
            reason_codes=[] if ok_b else ["benchmark_contract_identity.not_present"],
            notes="Requires status=present on benchmark_contract_identity.",
        )
    )

    # 2) Subject identities traceable
    st_s = status_of("subject_identity_and_freeze")
    ok_s = st_s == "present"
    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.subject_identities_traceable_v1",
            description="subject_identity_and_freeze evidence row is present.",
            status="pass" if ok_s else "fail",
            subject_refs=["subject_identity_and_freeze"],
            reason_codes=[] if ok_s else ["subject_identity_and_freeze.not_present"],
            notes="Requires status=present on subject_identity_and_freeze.",
        )
    )

    # 3) Execution posture remains fixture-only
    st_e = status_of("execution_posture_receipts")
    ok_e = st_e == "present"
    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.execution_posture_fixture_only_v1",
            description="execution_posture_receipts evidence row is present.",
            status="pass" if ok_e else "fail",
            subject_refs=["execution_posture_receipts"],
            reason_codes=[] if ok_e else ["execution_posture_receipts.not_present"],
            notes="Requires status=present on execution_posture_receipts.",
        )
    )

    # 4) Diagnostics interpretive (via score aggregation row — M24/M25 drift)
    st_sc = status_of("score_aggregation_reproducibility")
    ok_sc = st_sc == "present"
    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.diagnostics_and_pack_semantics_consistent_v1",
            description=(
                "score_aggregation_reproducibility is present (M24 interpretive; M25 packaging "
                "does not rescore)."
            ),
            status="pass" if ok_sc else "fail",
            subject_refs=["score_aggregation_reproducibility"],
            reason_codes=[] if ok_sc else ["score_aggregation_reproducibility.not_present"],
            notes="Fails when M24/M25 drift vs M23 or hash mismatch vs evidence pack.",
        )
    )

    # 5) Evidence pack does not invent stronger semantics — covered by score row + posture row;
    # add explicit gate referencing both.
    ok_pack = ok_sc and ok_e
    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.evidence_pack_traceability_only_v1",
            description="Packaging layer does not contradict tournament posture or rescore.",
            status="pass" if ok_pack else "fail",
            subject_refs=["execution_posture_receipts", "score_aggregation_reproducibility"],
            reason_codes=[] if ok_pack else ["evidence_pack.semantic_drift"],
            notes="Combines execution posture + score aggregation checks for M25.",
        )
    )

    # 6) Corpus promotion posture (fixture-only scope: expect not_applicable)
    st_c = status_of("corpus_provenance_and_promotion")
    ok_c = st_c == "not_applicable"

    add(
        _row(
            gate_id=f"{_GATE_PREFIX}.corpus_promotion_posture_v1",
            description=(
                "corpus_provenance_and_promotion is not_applicable for fixture-only scope, "
                "and must not imply canonical corpus promotion."
            ),
            status="pass" if ok_c else "fail",
            subject_refs=["corpus_provenance_and_promotion"],
            reason_codes=[] if ok_c else ["corpus.canonical_implication_forbidden"],
            notes=(
                "In M56 v1, corpus evidence is present only when canonical corpus implication "
                "markers are detected in supplied artifacts (forbidden for this scope)."
            ),
        )
    )

    failed = any(isinstance(g, dict) and g.get("status") == "fail" for g in results)
    scope_status = "rejected_within_scope" if failed else "accepted_within_scope"
    return results, scope_status


def gatepack_id_fixture_only_baseline_chain_v1() -> str:
    return M56_GATEPACK_FIXTURE_ONLY_BASELINE_CHAIN_V1
