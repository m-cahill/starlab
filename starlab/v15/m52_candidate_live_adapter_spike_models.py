"""V15-M52A candidate-to-live policy adapter spike (M51-bound; watchability only)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M52A: Final[str] = "starlab.v15.candidate_live_adapter_spike.v1"

PROFILE_M52A_SURFACE: Final[str] = "starlab.v15.m52a.candidate_to_live_policy_adapter_spike.v1"
PROFILE_ID_FIXTURE_CI: Final[str] = "starlab.v15.m52a.profile.fixture_ci.v1"
PROFILE_ID_OPERATOR_PREFLIGHT: Final[str] = "starlab.v15.m52a.profile.operator_preflight.v1"
PROFILE_ID_OPERATOR_DECLARED: Final[str] = "starlab.v15.m52a.profile.operator_declared.v1"
PROFILE_ID_OPERATOR_LOCAL_ADAPTER: Final[str] = (
    "starlab.v15.m52a.profile.operator_local_adapter_spike.v1"
)

MILESTONE_LABEL_M52A: Final[str] = "V15-M52A"
EMITTER_MODULE_M52A: Final[str] = "starlab.v15.emit_v15_m52_candidate_live_adapter_spike"
RUNNER_MODULE_M52A: Final[str] = "starlab.v15.run_v15_m52_candidate_live_adapter_spike"

FILENAME_MAIN_JSON: Final[str] = "v15_candidate_live_adapter_spike.json"
REPORT_FILENAME: Final[str] = "v15_candidate_live_adapter_spike_report.json"
BRIEF_FILENAME: Final[str] = "v15_candidate_live_adapter_spike_brief.md"

DIGEST_FIELD: Final[str] = "artifact_sha256"
SCHEMA_VERSION: Final[str] = "1.0"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_ADAPTER_SPIKE: Final[str] = "operator_local_adapter_spike"

STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_candidate_adapter_execution"
STATUS_PREFLIGHT_READY: Final[str] = "candidate_live_adapter_preflight_ready"
STATUS_PREFLIGHT_READY_WARNINGS: Final[str] = "candidate_live_adapter_preflight_ready_with_warnings"
STATUS_PREFLIGHT_BLOCKED: Final[str] = "candidate_live_adapter_preflight_blocked"

STATUS_SPIKE_COMPLETED: Final[str] = "candidate_live_adapter_spike_completed"
STATUS_SPIKE_COMPLETED_WARNINGS: Final[str] = "candidate_live_adapter_spike_completed_with_warnings"
STATUS_SPIKE_BLOCKED: Final[str] = "candidate_live_adapter_spike_blocked"
STATUS_SPIKE_FAILED: Final[str] = "candidate_live_adapter_spike_failed"

ADAPTER_SPIKE_LABEL: Final[str] = "real_candidate_live_adapter_spike"
ADAPTER_SCAFFOLD_LABEL: Final[str] = "scaffold_watchability_policy_not_candidate"
ADAPTER_BLOCKED_LABEL: Final[str] = "candidate_live_adapter_blocked"
ADAPTER_FIXTURE_LABEL: Final[str] = "fixture_no_live_adapter"

PROJECTION_ID: Final[str] = "provisional_safe_action_projection_v1"
ADAPTER_ID: Final[str] = "provisional_candidate_live_adapter_spike_v1"

ROUTE_TO_M52_BLOCKER_REHEARSAL: Final[str] = "route_to_12_hour_blocker_discovery_launch_rehearsal"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_ADAPTER_SPIKE: Final[str] = "--authorize-candidate-live-adapter-spike"

REFUSED_M51_CONTRACT_INVALID: Final[str] = "refused_m51_contract_invalid"
REFUSED_M51_SHA_MISMATCH: Final[str] = "refused_m51_sha_mismatch"
REFUSED_M51_ROUTE_NOT_12HR_REHEARSAL: Final[str] = "refused_m51_route_not_to_12hr_rehearsal"
REFUSED_M51_HONESTY: Final[str] = "refused_m51_honesty_flags_violation"
REFUSED_CANDIDATE_CHECKPOINT_MISSING: Final[str] = "refused_candidate_checkpoint_missing"
REFUSED_CANDIDATE_CHECKPOINT_SHA: Final[str] = "refused_candidate_checkpoint_sha_mismatch"
REFUSED_CANDIDATE_MODEL_LOAD_FAILED: Final[str] = "refused_candidate_model_load_failed"
REFUSED_ACTION_MAPPING_MISSING: Final[str] = "refused_candidate_action_mapping_missing"
REFUSED_SC2_ROOT: Final[str] = "refused_sc2_root_missing"
REFUSED_MAP_MISSING: Final[str] = "refused_map_missing"
REFUSED_OPERATOR_AUTH: Final[str] = "refused_operator_authorization_missing"
REFUSED_LIVE_SC2_RUNTIME: Final[str] = "refused_live_sc2_runtime_error"
REFUSED_BENCHMARK_CLAIM: Final[str] = "refused_disallowed_benchmark_claim"
REFUSED_STRENGTH_CLAIM: Final[str] = "refused_disallowed_strength_claim"
REFUSED_PROMOTION_CLAIM: Final[str] = "refused_disallowed_promotion_claim"
REFUSED_12H: Final[str] = "refused_disallowed_12_hour_execution"

FORBIDDEN_FLAG_CLAIM_BENCHMARK: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE: Final[str] = "--promote-checkpoint"
FORBIDDEN_FLAG_RUN_BENCHMARK: Final[str] = "--run-benchmark"
FORBIDDEN_FLAG_HUMAN_PANEL: Final[str] = "--run-human-panel"
FORBIDDEN_FLAG_XAI: Final[str] = "--run-xai"
FORBIDDEN_FLAG_SHOWCASE: Final[str] = "--release-showcase"
FORBIDDEN_FLAG_V2: Final[str] = "--authorize-v2"
FORBIDDEN_FLAG_T2: Final[str] = "--execute-t2"
FORBIDDEN_FLAG_T3: Final[str] = "--execute-t3"
FORBIDDEN_FLAG_T4: Final[str] = "--execute-t4"
FORBIDDEN_FLAG_T5: Final[str] = "--execute-t5"
FORBIDDEN_FLAG_12H: Final[str] = "--execute-12-hour-run"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_PROMOTE,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    FORBIDDEN_FLAG_HUMAN_PANEL,
    FORBIDDEN_FLAG_XAI,
    FORBIDDEN_FLAG_SHOWCASE,
    FORBIDDEN_FLAG_V2,
    FORBIDDEN_FLAG_T2,
    FORBIDDEN_FLAG_T3,
    FORBIDDEN_FLAG_T4,
    FORBIDDEN_FLAG_T5,
    FORBIDDEN_FLAG_12H,
)

FORBIDDEN_FLAG_TO_REFUSAL: Final[dict[str, str]] = {
    FORBIDDEN_FLAG_CLAIM_BENCHMARK: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_CLAIM_STRENGTH: REFUSED_STRENGTH_CLAIM,
    FORBIDDEN_FLAG_PROMOTE: REFUSED_PROMOTION_CLAIM,
    FORBIDDEN_FLAG_RUN_BENCHMARK: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_HUMAN_PANEL: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_XAI: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_SHOWCASE: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_V2: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_T2: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_T3: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_T4: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_T5: REFUSED_BENCHMARK_CLAIM,
    FORBIDDEN_FLAG_12H: REFUSED_12H,
}

# Upstream sealed M51 must keep these false for binding (parity with M51 honesty).
M51_UPSTREAM_HONESTY_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_results_produced",
    "strength_evaluated",
    "checkpoint_promoted",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
    "twelve_hour_run_executed",
)

M52A_HONESTY_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "strength_evaluated",
    "checkpoint_promoted",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
    "twelve_hour_run_executed",
)

M52A_DECLARED_OVERCLAIM_KEYS: Final[tuple[str, ...]] = M52A_HONESTY_FALSE_KEYS

ACTION_VOCABULARY: Final[tuple[str, ...]] = (
    "no_op",
    "select_idle_worker",
    "build_worker",
    "build_supply_depot",
    "build_barracks",
    "train_marine",
    "move_camera_or_army",
    "scout_enemy_start",
)

NON_CLAIMS_M52A: Final[tuple[str, ...]] = (
    "not_benchmark_execution",
    "not_benchmark_pass_fail",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_twelve_hour_run",
    "not_xai",
    "not_human_panel",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
    "watchability_adapter_spike_only",
    "candidate_adapter_distinct_from_scaffold_watchability",
    "route_recommendation_advisory_only_recommended_not_executed",
)

from starlab.v15.m51_live_candidate_watchability_harness_models import (  # noqa: E402
    CONTRACT_ID_M51,
)

CONTRACT_ID_M51_UPSTREAM: Final[str] = CONTRACT_ID_M51
