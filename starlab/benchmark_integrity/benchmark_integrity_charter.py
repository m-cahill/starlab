"""Deterministic benchmark integrity charter payloads (M55 — charter only; no gates)."""

from __future__ import annotations

from typing import Any

from starlab.benchmark_integrity.benchmark_integrity_controls import split_governance_controls
from starlab.benchmark_integrity.benchmark_integrity_models import (
    BENCHMARK_INTEGRITY_CHARTER_REPORT_SCHEMA_VERSION,
    BENCHMARK_INTEGRITY_CHARTER_SCHEMA_VERSION,
    CHARTER_FILENAME,
    CHARTER_REPORT_FILENAME,
    CONTRACT_ID,
    EVIDENCE_CLASSES_RESERVED_FOR_M56,
    RUNTIME_CONTRACT_REL_PATH,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def non_claims() -> list[str]:
    return [
        "Benchmark integrity is not yet proved as of this charter milestone.",
        "M55 introduces no reproducibility gates, no pass/fail benchmark verdict, and no merge-bar "
        "language for benchmark integrity.",
        "M55 does not assert live SC2 in CI; default CI remains fixture-only where applicable.",
        "M55 does not assert ladder or public performance claims.",
        "M55 does not subsume or replace the closed M52–M54 replay↔execution equivalence track.",
        "Evidence classes listed under evidence_classes_reserved_for_m56 are obligations for "
        "later milestones, not satisfied by emitting this charter JSON.",
    ]


def build_benchmark_integrity_charter_artifact() -> dict[str, Any]:
    controls = split_governance_controls()
    return {
        "contract_id": CONTRACT_ID,
        "schema_version": BENCHMARK_INTEGRITY_CHARTER_SCHEMA_VERSION,
        "milestone": "M55",
        "phase": "VII",
        "charter_status": "charter_only",
        "runtime_contract": RUNTIME_CONTRACT_REL_PATH,
        "split_governance_controls": controls,
        "evidence_classes_reserved_for_m56": list(EVIDENCE_CLASSES_RESERVED_FOR_M56),
        "non_claims": non_claims(),
    }


def build_benchmark_integrity_charter_report(*, charter_obj: dict[str, Any]) -> dict[str, Any]:
    charter_hash = sha256_hex_of_canonical_json(charter_obj)
    controls = charter_obj["split_governance_controls"]
    ncs = charter_obj["non_claims"]
    ev_reserved = charter_obj["evidence_classes_reserved_for_m56"]
    return {
        "schema_version": BENCHMARK_INTEGRITY_CHARTER_REPORT_SCHEMA_VERSION,
        "charter_canonical_sha256": charter_hash,
        "charter_artifact": CHARTER_FILENAME,
        "report_artifact": CHARTER_REPORT_FILENAME,
        "emitter_module": "starlab.benchmark_integrity.emit_benchmark_integrity_charter",
        "status": "charter_only",
        "control_family_count": len(controls),
        "non_claim_count": len(ncs),
        "m56_evidence_class_count": len(ev_reserved),
        "m56_boundary": {
            "summary": (
                "M55 defines vocabulary, split-governance controls, and future evidence "
                "obligations only. M56 begins reproducibility evidence surfaces and "
                "benchmark-integrity gate families; no M56 logic is emitted here."
            ),
            "reserved_for_m56": [
                "Deterministic evidence artifacts for benchmark_contract_identity, corpus "
                "provenance, subject freeze, execution posture receipts, and score aggregation "
                "reproducibility.",
                "Optional gate packs that evaluate evidence rows — not introduced in M55.",
            ],
            "explicit_non_claim": (
                "This report does not prove benchmark integrity and does not implement "
                "reproducibility gates."
            ),
        },
        "notes": (
            "M55 pairs charter JSON with this report for governance traceability. Compare to the "
            "M52/M53/M54 layering on the replay↔execution equivalence track."
        ),
    }


def benchmark_integrity_charter_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    charter = build_benchmark_integrity_charter_artifact()
    report = build_benchmark_integrity_charter_report(charter_obj=charter)
    return charter, report
