"""Build reproducibility gates JSON + report over M56 evidence (M56)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.benchmark_integrity.benchmark_integrity_gatepacks import (
    evaluate_fixture_only_baseline_chain_reproducibility_v1,
    gatepack_id_fixture_only_baseline_chain_v1,
)
from starlab.benchmark_integrity.benchmark_integrity_models import (
    BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_CONTRACT_ID,
    BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_REPORT_SCHEMA_VERSION,
    BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_SCHEMA_VERSION,
    M56_RUNTIMEV1_EVIDENCE_GATES_REL_PATH,
    M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
    REPRODUCIBILITY_GATES_FILENAME,
    REPRODUCIBILITY_GATES_REPORT_FILENAME,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_evidence_object(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = "evidence JSON top-level value must be an object"
        raise ValueError(msg)
    return obj


def load_evidence_report_object(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = "evidence report JSON top-level value must be an object"
        raise ValueError(msg)
    return obj


def _count_gate_statuses(gate_results: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for g in gate_results:
        st = str(g.get("status", "unknown"))
        out[st] = out.get(st, 0) + 1
    return dict(sorted(out.items()))


def build_benchmark_integrity_reproducibility_gates_bundle(
    *,
    evidence: dict[str, Any],
    evidence_report: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    input_sha = sha256_hex_of_canonical_json(evidence)
    gate_results, scope_status = evaluate_fixture_only_baseline_chain_reproducibility_v1(
        evidence=evidence
    )

    report_sha_ok = True
    if evidence_report is not None:
        expected = evidence_report.get("evidence_canonical_sha256")
        if isinstance(expected, str) and expected != input_sha:
            report_sha_ok = False

    if not report_sha_ok:
        gate_results = list(gate_results)
        gate_results.insert(
            0,
            {
                "gate_id": (
                    "starlab.m56.gate.fixture_only_baseline_chain.evidence_report_sha_mismatch_v1"
                ),
                "description": (
                    "Optional evidence report evidence_canonical_sha256 matches evidence JSON."
                ),
                "status": "fail",
                "subject_refs": ["evidence_report.evidence_canonical_sha256"],
                "reason_codes": ["evidence_report.sha256_mismatch"],
                "notes": "Supplied evidence report does not match canonical hash of evidence JSON.",
            },
        )
        scope_status = "rejected_within_scope"

    merged_nc = [
        "Benchmark integrity is not globally proved by bounded M56 reproducibility gates.",
        "M56 gate results apply only to starlab.m56.scope.fixture_only_baseline_chain_v1.",
        "M56 does not subsume or replace the closed M52–M54 replay↔execution equivalence track.",
        "merge_bar_language is not used in M56; scope_status is bounded top-level status only.",
    ]

    gates_obj: dict[str, Any] = {
        "contract_id": BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_CONTRACT_ID,
        "schema_version": BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_SCHEMA_VERSION,
        "milestone": "M56",
        "phase": "VII",
        "scope_id": M56_SCOPE_FIXTURE_ONLY_BASELINE_CHAIN_V1,
        "gatepack_id": gatepack_id_fixture_only_baseline_chain_v1(),
        "runtime_contract": M56_RUNTIMEV1_EVIDENCE_GATES_REL_PATH,
        "input_evidence_sha256": input_sha,
        "scope_status": scope_status,
        "gate_results": gate_results,
        "gate_counts_by_status": _count_gate_statuses(gate_results),
        "residual_non_claims": merged_nc,
    }

    report = build_benchmark_integrity_reproducibility_gates_report(gates_obj=gates_obj)
    return gates_obj, report


def build_benchmark_integrity_reproducibility_gates_report(
    *,
    gates_obj: dict[str, Any],
) -> dict[str, Any]:
    gates_hash = sha256_hex_of_canonical_json(gates_obj)
    return {
        "schema_version": BENCHMARK_INTEGRITY_REPRODUCIBILITY_GATES_REPORT_SCHEMA_VERSION,
        "gates_canonical_sha256": gates_hash,
        "gates_artifact": REPRODUCIBILITY_GATES_FILENAME,
        "report_artifact": REPRODUCIBILITY_GATES_REPORT_FILENAME,
        "emitter_module": "starlab.benchmark_integrity.emit_benchmark_integrity_gates",
        "implemented_scope_id": gates_obj.get("scope_id"),
        "implemented_gatepack_id": gates_obj.get("gatepack_id"),
        "input_evidence_sha256": gates_obj.get("input_evidence_sha256"),
        "scope_status": gates_obj.get("scope_status"),
        "gate_counts_by_status": gates_obj.get("gate_counts_by_status"),
        "residual_non_claims": gates_obj.get("residual_non_claims", []),
        "why_not_global_benchmark_integrity": (
            "M56 reproducibility gates validate only the fixture-only offline baseline chain "
            "evidence rows; they do not prove benchmark integrity across all STARLAB benchmarks, "
            "subjects, or evaluation postures."
        ),
    }
