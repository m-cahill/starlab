"""Constants and vocabulary for V15-M04 XAI evidence pack (deterministic JSON)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_XAI_EVIDENCE: Final[str] = "starlab.v15.xai_evidence_pack.v1"
REPORT_VERSION_XAI_EVIDENCE: Final[str] = "starlab.v15.xai_evidence_pack_report.v1"
FILENAME_XAI_EVIDENCE: Final[str] = "v15_xai_evidence_pack.json"
REPORT_FILENAME_XAI_EVIDENCE: Final[str] = "v15_xai_evidence_pack_report.json"

MILESTONE_ID_V15_M04: Final[str] = "V15-M04"
EMITTER_MODULE_XAI: Final[str] = "starlab.v15.emit_v15_xai_evidence_pack"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

# xai_evidence_status
XAI_STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
XAI_STATUS_OP_COMPLETE: Final[str] = "operator_declared_complete"
XAI_STATUS_OP_INCOMPLETE: Final[str] = "operator_declared_incomplete"
XAI_STATUS_BLOCKED: Final[str] = "blocked"
XAI_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"

# evidence_scope
EVIDENCE_CI_FIXTURE: Final[str] = "ci_fixture"
EVIDENCE_OPERATOR_DECLARED: Final[str] = "operator_declared"
EVIDENCE_OPERATOR_LOCAL_METADATA: Final[str] = "operator_local_metadata"
EVIDENCE_NOT_EVALUATED: Final[str] = "not_evaluated"

# check_status
CHECK_PASS: Final[str] = "pass"
CHECK_FAIL: Final[str] = "fail"
CHECK_WARNING: Final[str] = "warning"
CHECK_NOT_APPLICABLE: Final[str] = "not_applicable"
CHECK_FIXTURE: Final[str] = "fixture"

CONTRACT_ID_M03_CHECKPOINT_LINEAGE: Final[str] = "starlab.v15.checkpoint_lineage_manifest.v1"
CONTRACT_ID_M02_ENV_LOCK: Final[str] = "starlab.v15.long_gpu_environment_lock.v1"

REQUIRED_LOGICAL_ARTIFACT_NAMES: Final[tuple[str, ...]] = (
    "xai_manifest.json",
    "replay_identity.json",
    "checkpoint_identity.json",
    "decision_trace.json",
    "critical_decision_index.json",
    "attribution_summary.json",
    "concept_activation_summary.json",
    "counterfactual_probe_results.json",
    "alternative_action_rankings.json",
    "uncertainty_report.json",
    "replay_overlay_manifest.json",
    "xai_explanation_report.md",
)

STATUS_VOCABULARY: Final[dict[str, tuple[str, ...]]] = {
    "xai_evidence_status": (
        XAI_STATUS_FIXTURE_ONLY,
        XAI_STATUS_OP_COMPLETE,
        XAI_STATUS_OP_INCOMPLETE,
        XAI_STATUS_BLOCKED,
        XAI_STATUS_NOT_EVALUATED,
    ),
    "evidence_scope": (
        EVIDENCE_CI_FIXTURE,
        EVIDENCE_OPERATOR_DECLARED,
        EVIDENCE_OPERATOR_LOCAL_METADATA,
        EVIDENCE_NOT_EVALUATED,
    ),
    "replay_binding_status": (
        "fixture",
        "declared_only",
        "bound_external",
        "missing",
        "not_evaluated",
    ),
    "checkpoint_binding_status": (
        "fixture",
        "declared_only",
        "bound_external",
        "missing",
        "not_evaluated",
    ),
    "checkpoint_hash_verification_status": (
        "fixture",
        "declared_only",
        "verified_external",
        "missing",
        "mismatch",
        "not_evaluated",
    ),
    "trace_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "missing",
        "invalid",
        "not_evaluated",
    ),
    "attribution_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_computed",
        "missing",
        "not_evaluated",
    ),
    "concept_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_computed",
        "missing",
        "not_evaluated",
    ),
    "counterfactual_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_computed",
        "missing",
        "not_evaluated",
    ),
    "ranking_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_computed",
        "missing",
        "not_evaluated",
    ),
    "uncertainty_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_computed",
        "missing",
        "not_evaluated",
    ),
    "overlay_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_rendered",
        "missing",
        "not_evaluated",
    ),
    "report_status": (
        "fixture",
        "declared_only",
        "generated_external",
        "not_rendered",
        "missing",
        "not_evaluated",
    ),
    "path_disclosure": (
        "public_safe",
        "redacted",
        "logical_reference_only",
        "private_local_only",
        "forbidden_public",
    ),
    "check_status": (CHECK_PASS, CHECK_FAIL, CHECK_WARNING, CHECK_NOT_APPLICABLE, CHECK_FIXTURE),
}

SCENE_TYPE_VOCABULARY: Final[tuple[str, ...]] = (
    "opening_build",
    "first_scout",
    "first_combat",
    "expansion_timing",
    "defensive_response",
    "winning_push",
    "loss_or_failure_case",
    "fixture",
)

METHOD_VOCABULARY_EXAMPLES: Final[tuple[str, ...]] = (
    "fixture_method",
    "saliency_summary",
    "attention_summary",
    "concept_activation",
    "counterfactual_probe",
    "alternative_action_ranking",
    "uncertainty_summary",
)

NON_CLAIMS_V15_M04: Final[tuple[str, ...]] = (
    "m04_executes_xai_inference",
    "m04_generates_real_saliency_or_attribution",
    "m04_runs_counterfactual_evaluation",
    "m04_parses_real_replays",
    "m04_verifies_checkpoint_bytes",
    "m04_proves_explanation_faithfulness",
    "m04_runs_benchmarks",
    "m04_runs_human_panel",
    "m04_executes_gpu_training",
    "m04_executes_gpu_shakedown",
    "m04_authorizes_long_gpu_run",
    "m04_approves_real_xai_assets_for_claim_critical_use",
    "v2_opened",
    "px2_m04_opened",
    "px2_m05_opened",
)

EVIDENCE_JSON_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "profile",
    "xai_pack_id",
    "replay_identity",
    "checkpoint_identity",
    "decision_trace",
    "critical_decision_index",
    "attribution_summary",
    "concept_activation_summary",
    "counterfactual_probe_results",
    "alternative_action_rankings",
    "uncertainty_report",
    "replay_overlay_manifest",
    "xai_explanation_report",
    "operator_notes",
    "non_claims",
    "xai_evidence_status",
    "real_xai_inference_executed",
    "explanation_faithfulness_validated",
)

REPLAY_IDENTITY_FIELDS: Final[tuple[str, ...]] = (
    "replay_id",
    "replay_reference",
    "replay_sha256",
    "replay_binding_status",
    "source_milestone",
    "notes",
)

CHECKPOINT_IDENTITY_FIELDS: Final[tuple[str, ...]] = (
    "checkpoint_id",
    "checkpoint_reference",
    "checkpoint_lineage_manifest_sha256",
    "checkpoint_hash_verification_status",
    "checkpoint_binding_status",
    "source_milestone",
    "notes",
)

DECISION_TRACE_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "gameloop",
    "agent_perspective",
    "decision_type",
    "selected_action",
    "selected_action_label",
    "available_alternatives_count",
    "state_summary_reference",
    "input_feature_references",
    "policy_head",
    "confidence",
    "trace_status",
    "notes",
)

CRITICAL_DECISION_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "criticality_reason",
    "scene_type",
    "expected_review_status",
    "linked_trace_status",
    "notes",
)

ATTRIBUTION_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "method_id",
    "feature_group",
    "attribution_score",
    "normalization_policy",
    "attribution_status",
    "notes",
)

CONCEPT_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "concept_id",
    "concept_label",
    "activation_score",
    "concept_source",
    "concept_status",
    "notes",
)

COUNTERFACTUAL_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "counterfactual_id",
    "changed_factor",
    "original_action",
    "counterfactual_action",
    "outcome_delta_summary",
    "counterfactual_status",
    "notes",
)

ALTERNATIVE_RANK_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "rank",
    "action_id",
    "action_label",
    "score",
    "why_not_selected_summary",
    "ranking_status",
    "notes",
)

UNCERTAINTY_ROW_FIELDS: Final[tuple[str, ...]] = (
    "decision_id",
    "uncertainty_kind",
    "uncertainty_value",
    "threshold_policy",
    "uncertainty_status",
    "notes",
)

OVERLAY_MANIFEST_ROW_FIELDS: Final[tuple[str, ...]] = (
    "overlay_id",
    "decision_id",
    "overlay_kind",
    "overlay_reference",
    "path_disclosure",
    "overlay_status",
    "notes",
)

EXPLANATION_REPORT_ROW_FIELDS: Final[tuple[str, ...]] = (
    "report_id",
    "report_format",
    "report_reference",
    "path_disclosure",
    "report_status",
    "notes",
)

SEAL_KEY_XAI_EVIDENCE: Final[str] = "xai_evidence_pack_sha256"

__all__ = [
    "ATTRIBUTION_ROW_FIELDS",
    "ALTERNATIVE_RANK_ROW_FIELDS",
    "CHECKPOINT_IDENTITY_FIELDS",
    "CONCEPT_ROW_FIELDS",
    "CONTRACT_ID_M02_ENV_LOCK",
    "CONTRACT_ID_M03_CHECKPOINT_LINEAGE",
    "CONTRACT_ID_XAI_EVIDENCE",
    "COUNTERFACTUAL_ROW_FIELDS",
    "CRITICAL_DECISION_ROW_FIELDS",
    "DECISION_TRACE_ROW_FIELDS",
    "EMITTER_MODULE_XAI",
    "EVIDENCE_JSON_TOP_LEVEL_KEYS",
    "EVIDENCE_CI_FIXTURE",
    "EVIDENCE_NOT_EVALUATED",
    "EVIDENCE_OPERATOR_DECLARED",
    "EVIDENCE_OPERATOR_LOCAL_METADATA",
    "EXPLANATION_REPORT_ROW_FIELDS",
    "FILENAME_XAI_EVIDENCE",
    "METHOD_VOCABULARY_EXAMPLES",
    "MILESTONE_ID_V15_M04",
    "NON_CLAIMS_V15_M04",
    "OVERLAY_MANIFEST_ROW_FIELDS",
    "PROFILE_FIXTURE_CI",
    "PROFILE_OPERATOR_DECLARED",
    "REPORT_FILENAME_XAI_EVIDENCE",
    "REPORT_VERSION_XAI_EVIDENCE",
    "REPLAY_IDENTITY_FIELDS",
    "REQUIRED_LOGICAL_ARTIFACT_NAMES",
    "SCENE_TYPE_VOCABULARY",
    "STATUS_VOCABULARY",
    "UNCERTAINTY_ROW_FIELDS",
    "XAI_STATUS_BLOCKED",
    "XAI_STATUS_FIXTURE_ONLY",
    "XAI_STATUS_NOT_EVALUATED",
    "XAI_STATUS_OP_COMPLETE",
    "XAI_STATUS_OP_INCOMPLETE",
    "CHECK_PASS",
    "CHECK_FAIL",
    "CHECK_WARNING",
    "CHECK_NOT_APPLICABLE",
    "CHECK_FIXTURE",
    "SEAL_KEY_XAI_EVIDENCE",
]
