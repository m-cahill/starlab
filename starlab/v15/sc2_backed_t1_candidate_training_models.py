"""Governed constants for V15-M28 SC2-backed T1 candidate training."""

from __future__ import annotations

CONTRACT_ID = "starlab.v15.sc2_backed_t1_candidate_training.v1"
MILESTONE_LABEL = "V15-M28"
REPORT_CONTRACT_KIND = "starlab.v15.sc2_backed_t1_candidate_training.report.v1"

PROFILE_OPERATOR_LOCAL = "operator_local"
PROFILE_FIXTURE_CI = "fixture_ci"

RUN_TIER_T1_30_MIN = "T1_30_MIN"

EXPECTED_M27_CONTRACT_ID = "starlab.v15.sc2_rollout_training_loop_integration.v1"
M27_OUTCOME_COMPLETED = "sc2_rollout_training_loop_integration_completed"

# Primary milestone classification outcomes (honest branches).
OUTCOME_WITH_CHECKPOINT = "sc2_backed_candidate_training_completed_with_candidate_checkpoint"
OUTCOME_WITHOUT_CHECKPOINT = "sc2_backed_candidate_training_completed_without_checkpoint"
OUTCOME_STARTED_FAILED = "sc2_backed_candidate_training_started_failed"
OUTCOME_BLOCKED_MISSING_M27 = "sc2_backed_candidate_training_blocked_missing_m27_rollout"
OUTCOME_BLOCKED_SHA_MISMATCH = "sc2_backed_candidate_training_blocked_m27_rollout_sha_mismatch"
OUTCOME_BLOCKED_TRAINING_LOOP = "sc2_backed_candidate_training_blocked_by_training_loop"
OUTCOME_FIXTURE_ONLY = "fixture_only"

TRAINING_CONDITION_LABEL = "sc2_rollout_feature_conditioned_training_smoke_not_strength_learning"

M20_M21_DEFERRED = "m20_m21_candidate_gate_integration_deferred_to_m29"

NON_CLAIM_DEFAULTS: tuple[str, ...] = (
    "not_strength_evaluation",
    "not_benchmark_pass",
    "not_checkpoint_promotion",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_or_t3",
)
