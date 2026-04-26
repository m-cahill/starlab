"""V15-M11 human panel execution and bounded human-benchmark claim decision.

Constants only; no real execution.
"""

from __future__ import annotations

from typing import Final

# M11 execution artifact (reuses M06 vocabulary in IO; does not duplicate M06 protocol rows)
CONTRACT_ID_HUMAN_PANEL_EXECUTION: Final[str] = "starlab.v15.human_panel_execution.v1"
CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION: Final[str] = (
    "starlab.v15.human_benchmark_claim_decision.v1"
)

MILESTONE_ID_V15_M11: Final[str] = "V15-M11"
EMITTER_MODULE_HUMAN_PANEL_EXECUTION: Final[str] = "starlab.v15.emit_v15_human_panel_execution"
EMITTER_MODULE_HUMAN_BENCHMARK_CLAIM_DECISION: Final[str] = (
    "starlab.v15.emit_v15_human_benchmark_claim_decision"
)

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_HUMAN_PANEL_EXECUTION: Final[str] = "1"
REPORT_VERSION_HUMAN_BENCHMARK_CLAIM: Final[str] = "1"

SEAL_KEY_HUMAN_PANEL_EXECUTION: Final[str] = "human_panel_execution_sha256"
SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION: Final[str] = "human_benchmark_claim_decision_sha256"

FILENAME_HUMAN_PANEL_EXECUTION: Final[str] = "v15_human_panel_execution.json"
REPORT_FILENAME_HUMAN_PANEL_EXECUTION: Final[str] = "v15_human_panel_execution_report.json"
FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION: Final[str] = "v15_human_benchmark_claim_decision.json"
REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION: Final[str] = (
    "v15_human_benchmark_claim_decision_report.json"
)

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_EXECUTION_ID: Final[str] = "v15_m11:fixture_ci:deterministic"
FIXTURE_CLAIM_DECISION_ID: Final[str] = "v15_m11:fixture_ci:claim_decision:deterministic"

# --- Human panel status (M11) ---
HUMAN_PANEL_STATUS_FIXTURE_ONLY: Final[str] = "fixture_contract_only"
HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP: Final[str] = "blocked_missing_promoted_checkpoint"
HUMAN_PANEL_STATUS_BLOCKED_M06: Final[str] = "blocked_missing_human_panel_protocol"
HUMAN_PANEL_STATUS_BLOCKED_M08: Final[str] = "blocked_missing_m08_campaign_receipt"
HUMAN_PANEL_STATUS_BLOCKED_M10: Final[str] = "blocked_missing_xai_demonstration"
HUMAN_PANEL_STATUS_BLOCKED_PRIVACY: Final[str] = "blocked_missing_participant_privacy_review"
HUMAN_PANEL_STATUS_BLOCKED_ROSTER: Final[str] = "blocked_missing_participant_roster"
HUMAN_PANEL_STATUS_BLOCKED_MATCH: Final[str] = "blocked_missing_match_results"
HUMAN_PANEL_STATUS_BLOCKED_REPLAY: Final[str] = "blocked_missing_replay_capture"
HUMAN_PANEL_STATUS_BLOCKED_THRESHOLD: Final[str] = "blocked_missing_threshold_freeze"
HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE: Final[str] = "operator_declared_panel_evidence"
HUMAN_PANEL_STATUS_OP_PANEL_VALIDATED: Final[str] = "operator_declared_panel_evidence_validated"
HUMAN_PANEL_STATUS_OP_EXEC_DECLARED: Final[str] = "human_panel_executed_operator_declared"

# --- Gates H0–H12 ---
H0_ARTIFACT_INTEGRITY: Final[str] = "H0_artifact_integrity"
H1_PROTOCOL_BINDING: Final[str] = "H1_protocol_binding"
H2_CHECKPOINT_PROMOTION_BINDING: Final[str] = "H2_checkpoint_promotion_binding"
H3_CAMPAIGN_RECEIPT_BINDING: Final[str] = "H3_campaign_receipt_binding"
H4_PARTICIPANT_PRIVACY_BOUNDARY: Final[str] = "H4_participant_privacy_boundary"
H5_PARTICIPANT_TIER_COVERAGE: Final[str] = "H5_participant_tier_coverage"
H6_MATCH_SCHEDULE_COVERAGE: Final[str] = "H6_match_schedule_coverage"
H7_REPLAY_CAPTURE_COVERAGE: Final[str] = "H7_replay_capture_coverage"
H8_RESULT_INTEGRITY: Final[str] = "H8_result_integrity"
H9_THRESHOLD_POLICY: Final[str] = "H9_threshold_policy"
H10_XAI_SAMPLE_BINDING: Final[str] = "H10_xai_sample_binding"
H11_PUBLIC_PRIVATE_BOUNDARY: Final[str] = "H11_public_private_boundary"
H12_NON_CLAIM_BOUNDARY: Final[str] = "H12_non_claim_boundary"

ALL_HUMAN_PANEL_GATE_IDS: Final[tuple[str, ...]] = (
    H0_ARTIFACT_INTEGRITY,
    H1_PROTOCOL_BINDING,
    H2_CHECKPOINT_PROMOTION_BINDING,
    H3_CAMPAIGN_RECEIPT_BINDING,
    H4_PARTICIPANT_PRIVACY_BOUNDARY,
    H5_PARTICIPANT_TIER_COVERAGE,
    H6_MATCH_SCHEDULE_COVERAGE,
    H7_REPLAY_CAPTURE_COVERAGE,
    H8_RESULT_INTEGRITY,
    H9_THRESHOLD_POLICY,
    H10_XAI_SAMPLE_BINDING,
    H11_PUBLIC_PRIVATE_BOUNDARY,
    H12_NON_CLAIM_BOUNDARY,
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

# --- Claim decision labels (M11) ---
CLAIM_DECISION_BLOCKED: Final[str] = "blocked"
CLAIM_DECISION_BLOCKED_PROMOTED_CP: Final[str] = "blocked_missing_promoted_checkpoint"
CLAIM_DECISION_BLOCKED_NO_EXEC: Final[str] = "blocked_missing_human_panel_execution"
CLAIM_DECISION_BLOCKED_THRESHOLD: Final[str] = "blocked_missing_threshold_freeze"
CLAIM_DECISION_BLOCKED_PRIVACY: Final[str] = "blocked_missing_privacy_clearance"
CLAIM_DECISION_BLOCKED_REPLAY: Final[str] = "blocked_missing_replay_evidence"
CLAIM_DECISION_EVALUATED_NOT_AUTH: Final[str] = "evaluated_not_authorized"
CLAIM_DECISION_AUTH_BOUNDED: Final[str] = "authorized_bounded_human_benchmark_claim"

ALL_CLAIM_DECISION_LABELS: Final[tuple[str, ...]] = (
    CLAIM_DECISION_BLOCKED,
    CLAIM_DECISION_BLOCKED_PROMOTED_CP,
    CLAIM_DECISION_BLOCKED_NO_EXEC,
    CLAIM_DECISION_BLOCKED_THRESHOLD,
    CLAIM_DECISION_BLOCKED_PRIVACY,
    CLAIM_DECISION_BLOCKED_REPLAY,
    CLAIM_DECISION_EVALUATED_NOT_AUTH,
    CLAIM_DECISION_AUTH_BOUNDED,
)

NON_CLAIMS_V15_M11_EXECUTION: Final[tuple[str, ...]] = (
    "V15-M11 does not recruit human participants; does not run human-panel matches in CI; does not "
    "run live SC2 by default; does not promote a checkpoint; does not train a checkpoint; does not "
    "prove a strong-agent benchmark; does not authorize “beats most humans,” ladder, strong-agent, "
    "or v2 claims on the default path; and does not commit participant identities, raw replays, "
    "videos, checkpoint blobs, weights, private operator paths, or private human-panel notes.",
    "M11 is an execution and claim-decision *surface* over M06 protocol vocabulary and prior "
    "milestone SHA bindings; default fixture and honest public paths remain blocked and "
    "non-executing.",
)

NON_CLAIMS_V15_M11_CLAIM: Final[tuple[str, ...]] = (
    "V15-M11 human-benchmark claim decision is a deterministic read of "
    "starlab.v15.human_panel_execution.v1; it does not independently verify match outcomes, "
    "replays, or participant consent; and does not authorize a bounded human-benchmark claim "
    "unless the "
    "execution artifact records explicit non-default evidence and gate pass posture.",
)

PROFILE_ID_HUMAN_PANEL_EXECUTION: Final[str] = "starlab.v15.human_panel_execution_profile.v1"
PROFILE_ID_HUMAN_BENCHMARK_CLAIM: Final[str] = (
    "starlab.v15.human_benchmark_claim_decision_profile.v1"
)


def default_m11_authorization_flags() -> dict[str, bool]:
    return {
        "human_panel_execution_performed": False,
        "benchmark_execution_performed": False,
        "human_benchmark_claim_authorized": False,
        "strong_agent_claim_authorized": False,
        "checkpoint_promoted_for_human_panel": False,
        "xai_sample_bound": False,
        "ladder_claim_authorized": False,
        "v2_authorized": False,
    }


__all__ = [
    "ALL_CLAIM_DECISION_LABELS",
    "ALL_GATE_STATUSES",
    "ALL_HUMAN_PANEL_GATE_IDS",
    "CLAIM_DECISION_AUTH_BOUNDED",
    "CLAIM_DECISION_BLOCKED",
    "CLAIM_DECISION_BLOCKED_NO_EXEC",
    "CLAIM_DECISION_BLOCKED_PRIVACY",
    "CLAIM_DECISION_BLOCKED_PROMOTED_CP",
    "CLAIM_DECISION_BLOCKED_REPLAY",
    "CLAIM_DECISION_BLOCKED_THRESHOLD",
    "CLAIM_DECISION_EVALUATED_NOT_AUTH",
    "CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION",
    "CONTRACT_ID_HUMAN_PANEL_EXECUTION",
    "CONTRACT_VERSION",
    "EMITTER_MODULE_HUMAN_BENCHMARK_CLAIM_DECISION",
    "EMITTER_MODULE_HUMAN_PANEL_EXECUTION",
    "FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION",
    "FILENAME_HUMAN_PANEL_EXECUTION",
    "FIXTURE_CLAIM_DECISION_ID",
    "FIXTURE_EXECUTION_ID",
    "GATE_STATUS_BLOCKED",
    "GATE_STATUS_FAIL",
    "GATE_STATUS_NOT_APPLICABLE",
    "GATE_STATUS_NOT_EVALUATED",
    "GATE_STATUS_PASS",
    "GATE_STATUS_WARNING",
    "H0_ARTIFACT_INTEGRITY",
    "H1_PROTOCOL_BINDING",
    "H10_XAI_SAMPLE_BINDING",
    "H11_PUBLIC_PRIVATE_BOUNDARY",
    "H12_NON_CLAIM_BOUNDARY",
    "H2_CHECKPOINT_PROMOTION_BINDING",
    "H3_CAMPAIGN_RECEIPT_BINDING",
    "H4_PARTICIPANT_PRIVACY_BOUNDARY",
    "H5_PARTICIPANT_TIER_COVERAGE",
    "H6_MATCH_SCHEDULE_COVERAGE",
    "H7_REPLAY_CAPTURE_COVERAGE",
    "H8_RESULT_INTEGRITY",
    "H9_THRESHOLD_POLICY",
    "MILESTONE_ID_V15_M11",
    "NON_CLAIMS_V15_M11_CLAIM",
    "NON_CLAIMS_V15_M11_EXECUTION",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_ID_HUMAN_BENCHMARK_CLAIM",
    "PROFILE_ID_HUMAN_PANEL_EXECUTION",
    "PROFILE_OPERATOR_DECLARED",
    "PROFILE_OPERATOR_PREFLIGHT",
    "REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION",
    "REPORT_FILENAME_HUMAN_PANEL_EXECUTION",
    "REPORT_VERSION_HUMAN_BENCHMARK_CLAIM",
    "REPORT_VERSION_HUMAN_PANEL_EXECUTION",
    "SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION",
    "SEAL_KEY_HUMAN_PANEL_EXECUTION",
    "HUMAN_PANEL_STATUS_BLOCKED_M06",
    "HUMAN_PANEL_STATUS_BLOCKED_M08",
    "HUMAN_PANEL_STATUS_BLOCKED_M10",
    "HUMAN_PANEL_STATUS_BLOCKED_MATCH",
    "HUMAN_PANEL_STATUS_BLOCKED_PRIVACY",
    "HUMAN_PANEL_STATUS_BLOCKED_PROMOTED_CP",
    "HUMAN_PANEL_STATUS_BLOCKED_REPLAY",
    "HUMAN_PANEL_STATUS_BLOCKED_ROSTER",
    "HUMAN_PANEL_STATUS_BLOCKED_THRESHOLD",
    "HUMAN_PANEL_STATUS_FIXTURE_ONLY",
    "HUMAN_PANEL_STATUS_OP_EXEC_DECLARED",
    "HUMAN_PANEL_STATUS_OP_PANEL_EVIDENCE",
    "HUMAN_PANEL_STATUS_OP_PANEL_VALIDATED",
    "default_m11_authorization_flags",
]
