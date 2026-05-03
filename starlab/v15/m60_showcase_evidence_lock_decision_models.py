"""V15-M60 — showcase-evidence lock vs continue/remediate decision constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.m60.showcase_evidence_lock_decision.v1"
CONTRACT_ID_REPORT: Final[str] = "starlab.v15.m60.showcase_evidence_lock_decision_report.v1"
PROFILE_ID: Final[str] = "starlab.v15.m60.showcase_evidence_lock_vs_continue_remediate.v1"

MILESTONE: Final[str] = "V15-M60"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m60_showcase_evidence_lock_decision"

FILENAME_DECISION_JSON: Final[str] = "v15_m60_showcase_evidence_lock_decision.json"
REPORT_FILENAME: Final[str] = "v15_m60_showcase_evidence_lock_decision_report.json"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

CANONICAL_M53_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
CANONICAL_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

# Upstream milestone contract references (fixture metadata; not full seals).
CONTRACT_ID_M53: Final[str] = "starlab.v15.twelve_hour_operator_run_attempt.v1"
CONTRACT_ID_M54: Final[str] = "starlab.v15.twelve_hour_run_package_evaluation_readiness.v1"
CONTRACT_ID_M55: Final[str] = "starlab.v15.bounded_evaluation_package_preflight.v1"
CONTRACT_ID_M56: Final[str] = "starlab.v15.bounded_evaluation_package_readout_decision.v1"
CONTRACT_ID_M56A: Final[str] = "starlab.v15.latest_candidate_visual_watchability_confirmation.v1"
CONTRACT_ID_M57A: Final[str] = "starlab.v15.operator_live_visual_candidate_watch_session.v1"
CONTRACT_ID_M57: Final[str] = "starlab.v15.governed_evaluation_execution_charter.v1"
CONTRACT_ID_M58: Final[str] = "starlab.v15.bounded_candidate_adapter_evaluation_execution.v1"

STATUS_CLOSED: Final[str] = "closed"

DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED: Final[str] = "showcase_lock_recommended"
DECISION_STATUS_SHOWCASE_LOCK_DEFERRED: Final[str] = "showcase_lock_deferred"
DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED: Final[str] = "continue_remediate_recommended"

LOCK_CLASS_BOUNDED_SHOWCASE: Final[str] = "bounded_showcase_evidence_lock"
LOCK_CLASS_NO_LOCK_MISSING_EVIDENCE: Final[str] = "no_lock_missing_required_evidence"
LOCK_CLASS_NO_LOCK_OVERCLAIM_RISK: Final[str] = "no_lock_due_to_overclaim_risk"

NEXT_MILESTONE_M61: Final[str] = "V15-M61"
NEXT_ROUTE_M61_RELEASE_LOCK: Final[str] = "route_to_v15_m61_release_lock_proof_pack_update"
NEXT_ROUTE_M60_REMEDIATION: Final[str] = "route_to_v15_m60_remediation_followup"

ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY: Final[str] = "bounded_showcase_evidence_package_only"

STRONGEST_ALLOWED_CLAIM_LOCK: Final[str] = (
    "STARLAB v1.5 has sufficient governed evidence to proceed to a bounded showcase-evidence lock "
    "or proof-pack update, without claiming benchmark pass/fail, strength evaluation, checkpoint "
    "promotion, ladder performance, human-panel success, 72-hour authorization, or v2 "
    "authorization."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "M60 does not execute benchmark matches.",
    "M60 does not compute benchmark pass/fail.",
    "M60 does not evaluate strength.",
    "M60 does not promote the checkpoint.",
    "M60 does not execute XAI or human-panel evaluation.",
    "M60 does not release the showcase pack.",
    "M60 does not authorize a 72-hour run.",
    "M60 does not authorize v2 or v2 recharter.",
)
