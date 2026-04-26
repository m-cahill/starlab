"""V15-M13 v2 go / no-go decision — constants and vocabulary (governance surface only)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_V2_GO_NO_GO_DECISION: Final[str] = "starlab.v15.v2_go_no_go_decision.v1"
CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED: Final[str] = (
    "starlab.v15.v2_decision_operator_evidence_declared.v1"
)

MILESTONE_ID_V15_M13: Final[str] = "V15-M13"
EMITTER_MODULE_V2_DECISION: Final[str] = "starlab.v15.emit_v15_v2_go_no_go_decision"

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_V2_DECISION: Final[str] = "1"

SEAL_KEY_V2_GO_NO_GO_DECISION: Final[str] = "v2_go_no_go_decision_sha256"

FILENAME_V2_GO_NO_GO_DECISION: Final[str] = "v15_v2_go_no_go_decision.json"
REPORT_FILENAME_V2_GO_NO_GO_DECISION: Final[str] = "v15_v2_go_no_go_decision_report.json"
FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD: Final[str] = "v15_v2_go_no_go_decision_brief.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

PROFILE_ID_V2_GO_NO_GO_DECISION: Final[str] = "starlab.v15.v2_go_no_go_decision_profile.v1"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_V2_DECISION_ID: Final[str] = "v15_m13:fixture_ci:deterministic"

# --- Decision status vocabulary ---
STATUS_FIXTURE_DECISION_ONLY: Final[str] = "fixture_decision_only"
STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK: Final[str] = "blocked_missing_showcase_release_pack"
STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION: Final[str] = (
    "blocked_missing_showcase_release_authorization"
)
STATUS_BLOCKED_MISSING_M08_CAMPAIGN_RECEIPT: Final[str] = "blocked_missing_m08_campaign_receipt"
STATUS_BLOCKED_MISSING_PROMOTED_CHECKPOINT: Final[str] = "blocked_missing_promoted_checkpoint"
STATUS_BLOCKED_MISSING_STRONG_AGENT_BENCHMARK: Final[str] = "blocked_missing_strong_agent_benchmark"
STATUS_BLOCKED_MISSING_XAI_DEMONSTRATION: Final[str] = "blocked_missing_xai_demonstration"
STATUS_BLOCKED_MISSING_HUMAN_BENCHMARK_CLAIM: Final[str] = "blocked_missing_human_benchmark_claim"
STATUS_BLOCKED_MISSING_RIGHTS_CLEARANCE: Final[str] = "blocked_missing_rights_clearance"
STATUS_BLOCKED_PUBLIC_PRIVATE_BOUNDARY: Final[str] = "blocked_public_private_boundary"
STATUS_NO_GO_INSUFFICIENT_EVIDENCE: Final[str] = "no_go_insufficient_evidence"
STATUS_NO_GO_OVERCLAIM_RISK: Final[str] = "no_go_overclaim_risk"
STATUS_DEFER_OPERATOR_EVIDENCE_COLLECTION: Final[str] = "defer_operator_evidence_collection"
STATUS_DEFER_V1_5_HARDENING: Final[str] = "defer_v1_5_hardening"
STATUS_DEFER_REPEAT_TRAINING: Final[str] = "defer_repeat_training"
STATUS_PROCEED_TO_V2_AUTHORIZED: Final[str] = "proceed_to_v2_authorized"

ALL_V2_DECISION_STATUSES: Final[tuple[str, ...]] = (
    STATUS_FIXTURE_DECISION_ONLY,
    STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK,
    STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION,
    STATUS_BLOCKED_MISSING_M08_CAMPAIGN_RECEIPT,
    STATUS_BLOCKED_MISSING_PROMOTED_CHECKPOINT,
    STATUS_BLOCKED_MISSING_STRONG_AGENT_BENCHMARK,
    STATUS_BLOCKED_MISSING_XAI_DEMONSTRATION,
    STATUS_BLOCKED_MISSING_HUMAN_BENCHMARK_CLAIM,
    STATUS_BLOCKED_MISSING_RIGHTS_CLEARANCE,
    STATUS_BLOCKED_PUBLIC_PRIVATE_BOUNDARY,
    STATUS_NO_GO_INSUFFICIENT_EVIDENCE,
    STATUS_NO_GO_OVERCLAIM_RISK,
    STATUS_DEFER_OPERATOR_EVIDENCE_COLLECTION,
    STATUS_DEFER_V1_5_HARDENING,
    STATUS_DEFER_REPEAT_TRAINING,
    STATUS_PROCEED_TO_V2_AUTHORIZED,
)

# --- Decision outcomes ---
OUTCOME_NO_GO: Final[str] = "no_go"
OUTCOME_DEFER: Final[str] = "defer"
OUTCOME_REPEAT_OR_EXTEND_TRAINING: Final[str] = "repeat_or_extend_training"
OUTCOME_V1_5_HARDENING: Final[str] = "v1_5_hardening"
OUTCOME_COLLECT_OPERATOR_EVIDENCE: Final[str] = "collect_operator_evidence"
OUTCOME_PROCEED_TO_V2: Final[str] = "proceed_to_v2"

ALL_DECISION_OUTCOMES: Final[tuple[str, ...]] = (
    OUTCOME_NO_GO,
    OUTCOME_DEFER,
    OUTCOME_REPEAT_OR_EXTEND_TRAINING,
    OUTCOME_V1_5_HARDENING,
    OUTCOME_COLLECT_OPERATOR_EVIDENCE,
    OUTCOME_PROCEED_TO_V2,
)

RECOMMENDED_NEXT_STEP_COLLECT: Final[str] = "collect_operator_evidence_before_v2"
RECOMMENDED_NEXT_STEP_V1_5_HARDENING: Final[str] = "v1_5_hardening"

# --- Gates D0–D14 ---
D0_ARTIFACT_INTEGRITY: Final[str] = "D0_artifact_integrity"
D1_M12_RELEASE_PACK_BINDING: Final[str] = "D1_m12_release_pack_binding"
D2_CAMPAIGN_EVIDENCE_GATE: Final[str] = "D2_campaign_evidence_gate"
D3_CHECKPOINT_PROMOTION_GATE: Final[str] = "D3_checkpoint_promotion_gate"
D4_STRONG_AGENT_BENCHMARK_GATE: Final[str] = "D4_strong_agent_benchmark_gate"
D5_XAI_EVIDENCE_GATE: Final[str] = "D5_xai_evidence_gate"
D6_HUMAN_BENCHMARK_GATE: Final[str] = "D6_human_benchmark_gate"
D7_RIGHTS_AND_REGISTER_GATE: Final[str] = "D7_rights_and_register_gate"
D8_PUBLIC_PRIVATE_BOUNDARY_GATE: Final[str] = "D8_public_private_boundary_gate"
D9_CLAIM_BOUNDARY_GATE: Final[str] = "D9_claim_boundary_gate"
D10_REPRODUCIBILITY_GATE: Final[str] = "D10_reproducibility_gate"
D11_AUDIT_POSTURE_GATE: Final[str] = "D11_audit_posture_gate"
D12_OPEN_RISK_DISPOSITION_GATE: Final[str] = "D12_open_risk_disposition_gate"
D13_V2_RECHARTER_SCOPE_GATE: Final[str] = "D13_v2_recharter_scope_gate"
D14_NON_CLAIM_BOUNDARY_GATE: Final[str] = "D14_non_claim_boundary_gate"

ALL_V2_DECISION_GATE_IDS: Final[tuple[str, ...]] = (
    D0_ARTIFACT_INTEGRITY,
    D1_M12_RELEASE_PACK_BINDING,
    D2_CAMPAIGN_EVIDENCE_GATE,
    D3_CHECKPOINT_PROMOTION_GATE,
    D4_STRONG_AGENT_BENCHMARK_GATE,
    D5_XAI_EVIDENCE_GATE,
    D6_HUMAN_BENCHMARK_GATE,
    D7_RIGHTS_AND_REGISTER_GATE,
    D8_PUBLIC_PRIVATE_BOUNDARY_GATE,
    D9_CLAIM_BOUNDARY_GATE,
    D10_REPRODUCIBILITY_GATE,
    D11_AUDIT_POSTURE_GATE,
    D12_OPEN_RISK_DISPOSITION_GATE,
    D13_V2_RECHARTER_SCOPE_GATE,
    D14_NON_CLAIM_BOUNDARY_GATE,
)

GATE_STATUS_PASS: Final[str] = "pass"
GATE_STATUS_WARNING: Final[str] = "warning"
GATE_STATUS_FAIL: Final[str] = "fail"
GATE_STATUS_BLOCKED: Final[str] = "blocked"
GATE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"

ALL_GATE_STATUSES: Final[tuple[str, ...]] = (
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    GATE_STATUS_FAIL,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_NOT_APPLICABLE,
)

NON_CLAIMS_V15_M13: Final[tuple[str, ...]] = (
    "V15-M13 does not train a checkpoint; does not promote a checkpoint; does not execute a long "
    "GPU campaign; does not run benchmarks; does not run live SC2; does not run XAI inference; "
    "does not run human-panel matches; does not release a showcase agent; does not authorize v2 "
    "on the default path; and does not commit model weights, checkpoint blobs, raw replays, "
    "videos, saliency tensors, participant records, private operator notes, or private paths.",
    "M13 consumes governed M12 release-pack evidence for a v2 decision; fixture/default paths "
    "remain no-go until non-default operator evidence satisfies all gates.",
)

OPERATOR_V2_DECISION_EVIDENCE_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {
        "contract_id",
        "evidence_bundle_id",
        "operator_public_notes",
        "operator_recommended_next_step",
        "operator_rationale",
        "v2_recharter_scope_declared",
        "rights_clearance_operator_declared",
    }
)


def default_m13_authorization_flags() -> dict[str, bool]:
    return {
        "v2_authorized": False,
        "v2_recharter_authorized": False,
        "showcase_agent_release_authorized": False,
        "public_showcase_claim_authorized": False,
        "strong_agent_claim_authorized": False,
        "human_benchmark_claim_authorized": False,
        "ladder_claim_authorized": False,
        "rights_clearance_for_v2": False,
        "operator_evidence_sufficient": False,
    }


__all__ = [
    "ALL_DECISION_OUTCOMES",
    "ALL_GATE_STATUSES",
    "ALL_V2_DECISION_GATE_IDS",
    "ALL_V2_DECISION_STATUSES",
    "CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED",
    "CONTRACT_ID_V2_GO_NO_GO_DECISION",
    "CONTRACT_VERSION",
    "D0_ARTIFACT_INTEGRITY",
    "D1_M12_RELEASE_PACK_BINDING",
    "D10_REPRODUCIBILITY_GATE",
    "D11_AUDIT_POSTURE_GATE",
    "D12_OPEN_RISK_DISPOSITION_GATE",
    "D13_V2_RECHARTER_SCOPE_GATE",
    "D14_NON_CLAIM_BOUNDARY_GATE",
    "D2_CAMPAIGN_EVIDENCE_GATE",
    "D3_CHECKPOINT_PROMOTION_GATE",
    "D4_STRONG_AGENT_BENCHMARK_GATE",
    "D5_XAI_EVIDENCE_GATE",
    "D6_HUMAN_BENCHMARK_GATE",
    "D7_RIGHTS_AND_REGISTER_GATE",
    "D8_PUBLIC_PRIVATE_BOUNDARY_GATE",
    "D9_CLAIM_BOUNDARY_GATE",
    "EMITTER_MODULE_V2_DECISION",
    "FILENAME_V2_GO_NO_GO_DECISION",
    "FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD",
    "FIXTURE_V2_DECISION_ID",
    "GATE_STATUS_BLOCKED",
    "GATE_STATUS_FAIL",
    "GATE_STATUS_NOT_APPLICABLE",
    "GATE_STATUS_NOT_EVALUATED",
    "GATE_STATUS_PASS",
    "GATE_STATUS_WARNING",
    "MILESTONE_ID_V15_M13",
    "NON_CLAIMS_V15_M13",
    "OPERATOR_V2_DECISION_EVIDENCE_ALLOWED_KEYS",
    "OUTCOME_COLLECT_OPERATOR_EVIDENCE",
    "OUTCOME_DEFER",
    "OUTCOME_NO_GO",
    "OUTCOME_PROCEED_TO_V2",
    "OUTCOME_REPEAT_OR_EXTEND_TRAINING",
    "OUTCOME_V1_5_HARDENING",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_ID_V2_GO_NO_GO_DECISION",
    "PROFILE_OPERATOR_DECLARED",
    "PROFILE_OPERATOR_PREFLIGHT",
    "RECOMMENDED_NEXT_STEP_COLLECT",
    "RECOMMENDED_NEXT_STEP_V1_5_HARDENING",
    "REPORT_FILENAME_V2_GO_NO_GO_DECISION",
    "REPORT_VERSION_V2_DECISION",
    "SEAL_KEY_V2_GO_NO_GO_DECISION",
    "STATUS_BLOCKED_MISSING_HUMAN_BENCHMARK_CLAIM",
    "STATUS_BLOCKED_MISSING_M08_CAMPAIGN_RECEIPT",
    "STATUS_BLOCKED_MISSING_PROMOTED_CHECKPOINT",
    "STATUS_BLOCKED_MISSING_RIGHTS_CLEARANCE",
    "STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_AUTHORIZATION",
    "STATUS_BLOCKED_MISSING_SHOWCASE_RELEASE_PACK",
    "STATUS_BLOCKED_MISSING_STRONG_AGENT_BENCHMARK",
    "STATUS_BLOCKED_MISSING_XAI_DEMONSTRATION",
    "STATUS_BLOCKED_PUBLIC_PRIVATE_BOUNDARY",
    "STATUS_DEFER_OPERATOR_EVIDENCE_COLLECTION",
    "STATUS_DEFER_REPEAT_TRAINING",
    "STATUS_DEFER_V1_5_HARDENING",
    "STATUS_FIXTURE_DECISION_ONLY",
    "STATUS_NO_GO_INSUFFICIENT_EVIDENCE",
    "STATUS_NO_GO_OVERCLAIM_RISK",
    "STATUS_PROCEED_TO_V2_AUTHORIZED",
    "default_m13_authorization_flags",
]
