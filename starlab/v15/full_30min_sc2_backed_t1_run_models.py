"""Governed constants for V15-M29 — full-wall-clock SC2-backed T1 candidate run."""

from __future__ import annotations

CONTRACT_ID = "starlab.v15.full_30min_sc2_backed_t1_run.v1"
REPORT_CONTRACT_KIND = "starlab.v15.full_30min_sc2_backed_t1_run.report.v1"

MILESTONE_LABEL = "V15-M29"

UPSTREAM_M28_CONTRACT_ID = "starlab.v15.sc2_backed_t1_candidate_training.v1"
UPSTREAM_M27_ARTIFACT_SHA256 = "f9c2ca5aca7a3b15df0567358c1f207f99e112cd8d816f5ac1a1c6ff04022227"
UPSTREAM_M28_CANDIDATE_PT_SHA_SAMPLE = (
    "71897cfff94fba7209e667dd44e040eabc705e686c6a579cd26e13015f00ecc8"
)

M20_M21_DEFERRED = "m20_m21_candidate_gate_integration_deferred_to_m30"

PROFILE_OPERATOR_LOCAL_FULL_WALL = "operator_local_full_wall_clock"
PROFILE_FIXTURE_CI = "fixture_ci"

NON_CLAIM_DEFAULTS: tuple[str, ...] = (
    "not_strength_evaluation",
    "not_benchmark_pass",
    "not_checkpoint_promotion",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_or_t3",
    "not_long_gpu_campaign_completed_unless_wall_clock_evidence_met",
)

OUTCOME_FULL_30_WITH_CHECKPOINT = "sc2_backed_t1_full_30min_completed_with_candidate_checkpoint"
OUTCOME_FULL_30_WITHOUT_CHECKPOINT = "sc2_backed_t1_full_30min_completed_without_checkpoint"
OUTCOME_FIXTURE_ONLY = "fixture_only"
OUTCOME_LAUNCHED_FAILED = "sc2_backed_t1_full_30min_launched_failed_after_start"
OUTCOME_BLOCKED_WALL_CLOCK_SHORT_M28 = (
    "sc2_backed_t1_full_30min_blocked_by_runner_wall_clock_below_minimum"
)
OUTCOME_BLOCKED_MISSING_M27 = "sc2_backed_t1_full_30min_blocked_missing_m27_rollout"

EVAL_GATE_READY = "candidate_checkpoint_ready_for_m30_evaluation_package"
