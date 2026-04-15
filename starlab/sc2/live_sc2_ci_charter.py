"""Deterministic M57 live SC2-in-CI charter JSON (charter + report only)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_CHARTER_CONTRACT_ID,
    LIVE_SC2_IN_CI_CHARTER_REPORT_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_CHARTER_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_RUNTIME_DOC_REL_PATH,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
)


def non_claims() -> list[str]:
    return [
        "Live SC2 in CI is not proved as a default merge-gate or global norm.",
        "M57 introduces one bounded charter, one controlled runner profile, and one execution "
        "path over the existing M44 harness — not full operational proof of live SC2 in CI.",
        "M58 owns hardening, cost guardrails, and broader live-SC2 operational controls.",
        "M57 does not assert benchmark integrity, replay↔execution equivalence, or ladder/public "
        "performance.",
        "Supported candidate class is M43 hierarchical training runs with explicit local weights "
        "only; M41/M45 refit bundles and other classes are out of scope for M57.",
        "Default required CI remains fixture-only; this milestone does not add a required live "
        "SC2 merge check.",
    ]


def build_live_sc2_in_ci_charter_artifact() -> dict[str, Any]:
    return {
        "contract_id": LIVE_SC2_IN_CI_CHARTER_CONTRACT_ID,
        "schema_version": LIVE_SC2_IN_CI_CHARTER_SCHEMA_VERSION,
        "milestone": "M57",
        "phase": "VII",
        "charter_status": "charter_only",
        "runtime_contract": LIVE_SC2_IN_CI_RUNTIME_DOC_REL_PATH,
        "bounded_runner_profile_id": M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
        "m44_substrate": (
            "starlab.sc2.local_live_play_validation_harness.run_local_live_play_validation"
        ),
        "supported_runtime_modes": ["fixture_stub_ci", "local_live_sc2"],
        "supported_candidate_class": "starlab.hierarchical_training_run.v1_with_explicit_weights",
        "non_claims": non_claims(),
    }


def build_live_sc2_in_ci_charter_report(*, charter_obj: dict[str, Any]) -> dict[str, Any]:
    charter_hash = sha256_hex_of_canonical_json(charter_obj)
    return {
        "schema_version": LIVE_SC2_IN_CI_CHARTER_REPORT_SCHEMA_VERSION,
        "charter_canonical_sha256": charter_hash,
        "charter_artifact": "live_sc2_in_ci_charter.json",
        "report_artifact": "live_sc2_in_ci_charter_report.json",
        "emitter_module": "starlab.sc2.emit_live_sc2_in_ci_charter",
        "status": "charter_only",
        "non_claim_count": len(charter_obj["non_claims"]),
        "m58_boundary": {
            "summary": (
                "M57 establishes bounded charter + controlled runner receipts only. M58 adds "
                "hardening, cost ceilings, and operational guardrails for live SC2-in-CI posture."
            ),
            "explicit_non_claim": "This report does not prove live SC2 in CI as a merge boundary.",
        },
    }


def live_sc2_in_ci_charter_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    charter = build_live_sc2_in_ci_charter_artifact()
    report = build_live_sc2_in_ci_charter_report(charter_obj=charter)
    return charter, report
