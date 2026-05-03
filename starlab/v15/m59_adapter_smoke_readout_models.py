"""V15-M59 — adapter smoke readout & benchmark overclaim refusal constants."""

from __future__ import annotations

from typing import Final

SCHEMA_VERSION_READOUT: Final[str] = "starlab.v15.m59.adapter_smoke_readout.v1"
CONTRACT_ID_REFUSAL_REPORT: Final[str] = "starlab.v15.m59.benchmark_overclaim_refusal.v1"

MILESTONE: Final[str] = "V15-M59"
UPSTREAM_MILESTONE: Final[str] = "V15-M58"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m59_adapter_smoke_readout"

FILENAME_MAIN_JSON: Final[str] = "v15_m59_adapter_smoke_readout.json"
REPORT_FILENAME: Final[str] = "v15_m59_adapter_smoke_readout_report.json"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_EVIDENCE: Final[str] = "operator_evidence"

# M58 closeout identity (upstream evidence bindings).
CANONICAL_UPSTREAM_MAIN_SHA: Final[str] = "6d69ea01adbe8c16c922c32857d719b78b78bf70"
CANONICAL_M58_ARTIFACT_SHA256: Final[str] = (
    "9de034bc5585d62d08b7129a27be45ccf4a79ef01f45d5631bc358dfdc0c1d05"
)

M58_STATUS_ACCEPTED: Final[str] = "accepted"
M58_ACCEPTANCE_REASON_COMPLETED: Final[str] = "bounded_candidate_adapter_execution_completed"

EVIDENCE_SOURCE_OPERATOR_LOCAL: Final[str] = "operator_local"
EVIDENCE_SOURCE_FIXTURE: Final[str] = "fixture_labeled"

READOUT_ADAPTER_SMOKE_ACCEPTED: Final[str] = "accepted_within_scope"
READOUT_BENCHMARK_NOT_EVIDENCE: Final[str] = "not_benchmark_evidence"
READOUT_NOT_PROMOTED: Final[str] = "not_promoted"
LOCK_DEFERRED_M60: Final[str] = "deferred_to_v15_m60"
NEXT_DECISION_M60: Final[str] = "v15_m60_showcase_evidence_lock_vs_continue_remediate"

STRONGEST_ALLOWED_CLAIM: Final[str] = (
    "M58 completed a bounded candidate-adapter smoke execution under declared operator-local "
    "conditions."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "This is not benchmark pass/fail evidence.",
    "This is not a strength result.",
    "This is not ladder or public performance proof.",
    "This does not select or promote a final v1.5 showcase agent.",
    "This does not open V15-M62 as a first 12-hour run.",
    "This does not authorize a 72-hour run or v2 recharter.",
)

# refused_claims: True means the overclaim is refused (not authorized).
REFUSED_CLAIMS: Final[dict[str, bool]] = {
    "benchmark_pass_claim": True,
    "candidate_strength_claim": True,
    "ladder_public_performance_claim": True,
    "human_panel_claim": True,
    "v15_lock_claim": True,
    "second_12_hour_run_claim": True,
    "seventy_two_hour_charter_claim": True,
    "v2_recharter_claim": True,
}

NEXT_MILESTONE_LEDGER: Final[str] = "V15-M60"
