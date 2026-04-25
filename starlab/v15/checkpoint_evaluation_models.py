"""V15-M09 checkpoint evaluation and promotion decision — contract constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_CHECKPOINT_EVALUATION: Final[str] = "starlab.v15.checkpoint_evaluation.v1"
CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION: Final[str] = (
    "starlab.v15.checkpoint_promotion_decision.v1"
)
PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION: Final[str] = (
    "starlab.v15.checkpoint_evaluation_promotion.v1"
)

MILESTONE_ID_V15_M09: Final[str] = "V15-M09"
EMITTER_MODULE_CHECKPOINT_EVALUATION: Final[str] = "starlab.v15.emit_v15_checkpoint_evaluation"
EMITTER_MODULE_PROMOTION_DECISION: Final[str] = "starlab.v15.emit_v15_checkpoint_promotion_decision"

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_EVALUATION: Final[str] = "1"
REPORT_VERSION_PROMOTION: Final[str] = "1"

SEAL_KEY_CHECKPOINT_EVALUATION: Final[str] = "checkpoint_evaluation_sha256"
SEAL_KEY_CHECKPOINT_PROMOTION: Final[str] = "checkpoint_promotion_decision_sha256"

FILENAME_CHECKPOINT_EVALUATION: Final[str] = "v15_checkpoint_evaluation.json"
REPORT_FILENAME_CHECKPOINT_EVALUATION: Final[str] = "v15_checkpoint_evaluation_report.json"
FILENAME_CHECKPOINT_PROMOTION: Final[str] = "v15_checkpoint_promotion_decision.json"
REPORT_FILENAME_CHECKPOINT_PROMOTION: Final[str] = "v15_checkpoint_promotion_decision_report.json"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_EVALUATION: Final[str] = "operator_local_evaluation"
PROFILE_OPERATOR_PROMOTION_DECISION: Final[str] = "operator_promotion_decision"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_EVALUATION_ID: Final[str] = "v15_m09:fixture_ci:deterministic"
FIXTURE_CANDIDATE_CHECKPOINT_ID: Final[str] = "v15_m09:fixture:non_candidate"

GATE_STATUS_PASS: Final[str] = "pass"
GATE_STATUS_WARNING: Final[str] = "warning"
GATE_STATUS_FAIL: Final[str] = "fail"
GATE_STATUS_BLOCKED: Final[str] = "blocked"
GATE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"

# Gate ids (G0–G10)
G0_ARTIFACT_INTEGRITY: Final[str] = "G0_artifact_integrity"
G1_LINEAGE_CONSISTENCY: Final[str] = "G1_lineage_consistency"
G2_ENVIRONMENT_BINDING: Final[str] = "G2_environment_binding"
G3_DATASET_RIGHTS_BINDING: Final[str] = "G3_dataset_rights_binding"
G4_CHECKPOINT_HASH_VERIFICATION: Final[str] = "G4_checkpoint_hash_verification"
G5_LOAD_SMOKE: Final[str] = "G5_load_smoke"
G6_RESUME_CONTINUATION: Final[str] = "G6_resume_or_continuation_receipt"
G7_EVAL_CADENCE: Final[str] = "G7_eval_cadence_presence"
G8_BASIC_METRIC_THRESHOLDS: Final[str] = "G8_basic_metric_thresholds"
G9_FAILURE_PROBE: Final[str] = "G9_failure_probe_presence"
G10_NON_CLAIM_BOUNDARY: Final[str] = "G10_non_claim_boundary"

ALL_GATE_IDS: Final[tuple[str, ...]] = (
    G0_ARTIFACT_INTEGRITY,
    G1_LINEAGE_CONSISTENCY,
    G2_ENVIRONMENT_BINDING,
    G3_DATASET_RIGHTS_BINDING,
    G4_CHECKPOINT_HASH_VERIFICATION,
    G5_LOAD_SMOKE,
    G6_RESUME_CONTINUATION,
    G7_EVAL_CADENCE,
    G8_BASIC_METRIC_THRESHOLDS,
    G9_FAILURE_PROBE,
    G10_NON_CLAIM_BOUNDARY,
)

EVALUATION_STATUS_NOT_EVALUATED_FIXTURE: Final[str] = "not_evaluated_fixture_only"
EVALUATION_STATUS_BLOCKED_NO_RECEIPT: Final[str] = "blocked_missing_m08_campaign_receipt"
EVALUATION_STATUS_BLOCKED_NO_CANDIDATE: Final[str] = "blocked_missing_candidate_checkpoint"
EVALUATION_STATUS_BLOCKED_PREFLIGHT: Final[str] = "blocked_preflight_evidence_incomplete"

PROMOTION_STATUS_BLOCKED_EVIDENCE: Final[str] = "blocked_missing_evidence"
PROMOTION_STATUS_BLOCKED_CAMPAIGN: Final[str] = "blocked_missing_m08_campaign"
PROMOTION_STATUS_BLOCKED_CANDIDATE: Final[str] = "blocked_missing_candidate_checkpoint"
PROMOTION_STATUS_NOT_PROMOTED: Final[str] = "evaluated_not_promoted"
PROMOTION_STATUS_PROMOTED_CANDIDATE: Final[str] = "promoted_candidate_for_downstream_evaluation"
PROMOTION_STATUS_PROMOTED_XAI: Final[str] = "promoted_candidate_for_xai_demo"
PROMOTION_STATUS_REJECTED: Final[str] = "rejected"
PROMOTION_STATUS_DEFERRED: Final[str] = "deferred"
PROMOTION_STATUS_BLOCKED: Final[str] = "blocked"

NON_CLAIMS_V15_M09: Final[tuple[str, ...]] = (
    "V15-M09 may emit checkpoint evaluation and promotion decision artifacts only under "
    "declared profiles; fixture output is not a completed evaluation.",
    "V15-M09 does not execute the long GPU campaign or train new checkpoints.",
    "V15-M09 does not pass or execute the strong-agent benchmark unless separately evidenced.",
    "V15-M09 does not authorize strong-agent or human-benchmark claims.",
    "V15-M09 does not run human-panel matches or perform XAI inference review.",
    "V15-M09 does not release model weights or commit raw checkpoint blobs to the repository.",
    "A promotion decision is a governance routing label for downstream evaluation, not a "
    "strong-agent or release-ready claim.",
)

EVALUATION_DECLARED_TOP_LEVEL_KEYS: Final[frozenset[str]] = frozenset(
    {
        "contract_id",
        "contract_version",
        "profile_id",
        "profile",
        "milestone",
        "created_by",
        "evaluation_id",
        "candidate_checkpoint_id",
        "candidate_checkpoint_role",
        "evaluation_status",
        "evidence_scope",
        "m08_training_manifest_binding",
        "m08_campaign_receipt_binding",
        "checkpoint_lineage_binding",
        "checkpoint_metadata_binding",
        "environment_lock_binding",
        "training_config_binding",
        "dataset_manifest_binding",
        "rights_manifest_binding",
        "strong_agent_protocol_binding",
        "xai_contract_binding",
        "human_panel_protocol_binding",
        "artifact_integrity",
        "lineage_consistency",
        "checkpoint_hash_verification",
        "load_smoke",
        "resume_or_continuation_receipt",
        "evaluation_metrics",
        "evaluation_gates",
        "failure_probes",
        "provenance_gaps",
        "non_claims",
        "authorization_flags",
        "redaction_policy",
        "optional_bindings",
        SEAL_KEY_CHECKPOINT_EVALUATION,
    }
)


def default_m09_evaluation_authorization_flags() -> dict[str, bool]:
    return {
        "checkpoint_candidate_available": False,
        "checkpoint_bytes_verified": False,
        "checkpoint_evaluation_performed": False,
        "checkpoint_promotion_performed": False,
        "promoted_checkpoint_selected": False,
        "benchmark_execution_performed": False,
        "strong_agent_claim_authorized": False,
        "human_panel_execution_performed": False,
        "human_benchmark_claim_authorized": False,
        "xai_review_performed": False,
        "long_gpu_campaign_completed": False,
        "v2_authorized": False,
    }
