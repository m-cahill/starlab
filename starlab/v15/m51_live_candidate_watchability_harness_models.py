"""V15-M51 live candidate watchability harness (M50-bound; not benchmark)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M51: Final[str] = "starlab.v15.live_candidate_watchability_harness.v1"

PROFILE_M51_SURFACE: Final[str] = "starlab.v15.m51.live_candidate_watchability_harness.v1"
PROFILE_ID_FIXTURE_CI: Final[str] = "starlab.v15.m51.profile.fixture_ci_no_live_sc2.v1"
PROFILE_ID_OPERATOR_PREFLIGHT: Final[str] = "starlab.v15.m51.profile.operator_preflight.v1"
PROFILE_ID_OPERATOR_LOCAL_WATCHABILITY: Final[str] = (
    "starlab.v15.m51.profile.operator_local_watchability_run.v1"
)
PROFILE_ID_OPERATOR_DECLARED: Final[str] = "starlab.v15.m51.profile.operator_declared.v1"

MILESTONE_LABEL_M51: Final[str] = "V15-M51"
EMITTER_MODULE_M51: Final[str] = "starlab.v15.emit_v15_m51_live_candidate_watchability_harness"
RUNNER_MODULE_M51: Final[str] = "starlab.v15.run_v15_m51_live_candidate_watchability_harness"

FILENAME_MAIN_JSON: Final[str] = "v15_live_candidate_watchability_harness.json"
REPORT_FILENAME: Final[str] = "v15_live_candidate_watchability_harness_report.json"
BRIEF_FILENAME: Final[str] = "v15_live_candidate_watchability_harness_brief.md"

DIGEST_FIELD: Final[str] = "artifact_sha256"
SCHEMA_VERSION: Final[str] = "1.0"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_live_sc2"
STATUS_PREFLIGHT_READY: Final[str] = "watchability_preflight_ready"
STATUS_PREFLIGHT_READY_WARNINGS: Final[str] = "watchability_preflight_ready_with_warnings"
STATUS_PREFLIGHT_BLOCKED: Final[str] = "watchability_preflight_blocked"

STATUS_LIVE_COMPLETED: Final[str] = "live_candidate_watchability_run_completed"
STATUS_LIVE_COMPLETED_WARNINGS: Final[str] = (
    "live_candidate_watchability_run_completed_with_warnings"
)
STATUS_LIVE_BLOCKED: Final[str] = "live_candidate_watchability_run_blocked"
STATUS_LIVE_FAILED: Final[str] = "live_candidate_watchability_run_failed"

STATUS_BLOCKED_MISSING_ADAPTER: Final[str] = (
    "watchability_blocked_missing_candidate_live_policy_adapter"
)
STATUS_SCAFFOLD_COMPLETED: Final[str] = "scaffold_watchability_run_completed_not_candidate_policy"

CANDIDATE_POLICY_REAL: Final[str] = "real_candidate_policy_adapter"
CANDIDATE_POLICY_SCAFFOLD: Final[str] = "scaffold_watchability_policy_not_candidate"
CANDIDATE_POLICY_UNAVAILABLE: Final[str] = "unavailable_candidate_policy_adapter_missing"
CANDIDATE_POLICY_FIXTURE: Final[str] = "fixture_no_policy"

ROUTE_TO_M51_UPSTREAM: Final[str] = "route_to_live_candidate_watchability_harness"
ROUTE_TO_M52: Final[str] = "route_to_12_hour_blocker_discovery_launch_rehearsal"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_WATCHABILITY: Final[str] = "--authorize-live-candidate-watchability"
FLAG_SCAFFOLD_POLICY: Final[str] = "--allow-scaffold-watchability-policy"

REFUSED_MISSING_M50: Final[str] = "refused_missing_m50_readout_json"
REFUSED_M50_CONTRACT_INVALID: Final[str] = "refused_m50_contract_invalid"
REFUSED_M50_SHA_MISMATCH: Final[str] = "refused_m50_sha_mismatch"
REFUSED_M50_ROUTE_NOT_WATCHABILITY: Final[str] = "refused_m50_route_not_to_watchability"
REFUSED_M50_ROUTE_EXECUTED: Final[str] = "refused_m50_route_already_executed"
REFUSED_M50_HONESTY: Final[str] = "refused_m50_honesty_flags_violation"
REFUSED_CANDIDATE_IDENTITY: Final[str] = "refused_candidate_identity_missing"
REFUSED_CANDIDATE_CHECKPOINT_SHA: Final[str] = "refused_candidate_checkpoint_sha_mismatch"
REFUSED_ADAPTER_MISSING: Final[str] = "refused_candidate_live_policy_adapter_missing"
REFUSED_SC2_ROOT: Final[str] = "refused_sc2_root_missing"
REFUSED_MAP_MISSING: Final[str] = "refused_map_missing"
REFUSED_OPERATOR_AUTH: Final[str] = "refused_operator_authorization_missing"
REFUSED_BENCHMARK_CLAIM: Final[str] = "refused_disallowed_benchmark_claim"
REFUSED_STRENGTH_CLAIM: Final[str] = "refused_disallowed_strength_claim"
REFUSED_PROMOTION_CLAIM: Final[str] = "refused_disallowed_promotion_claim"
REFUSED_12H: Final[str] = "refused_disallowed_12_hour_execution"
REFUSED_LIVE_SC2_RUNTIME: Final[str] = "refused_live_sc2_runtime_error"
REFUSED_INVALID_DECLARED_M51: Final[str] = "refused_invalid_declared_m51_shape"

FORBIDDEN_FLAG_CLAIM_BENCHMARK: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE: Final[str] = "--promote-checkpoint"
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

# Upstream sealed M50 must keep these booleans false (parity with M50 honesty block).
M50_UPSTREAM_HONESTY_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_failed",
    "benchmark_pass_fail_emitted",
    "strength_evaluated",
    "checkpoint_promoted",
    "torch_load_invoked",
    "checkpoint_blob_loaded",
    "live_sc2_executed",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
)

M51_HONESTY_FALSE_KEYS: Final[tuple[str, ...]] = (
    "benchmark_passed",
    "benchmark_pass_fail_emitted",
    "scorecard_results_produced",
    "strength_evaluated",
    "checkpoint_promoted",
    "torch_load_invoked",
    "checkpoint_blob_loaded",
    "xai_executed",
    "human_panel_executed",
    "showcase_released",
    "v2_authorized",
    "t2_t3_t4_t5_executed",
    "twelve_hour_run_executed",
)

M51_DECLARED_OVERCLAIM_KEYS: Final[tuple[str, ...]] = M51_HONESTY_FALSE_KEYS + (
    "live_sc2_executed",
)

BEHAVIOR_TAGS_SUGGESTED: Final[tuple[str, ...]] = (
    "started_game",
    "loaded_map",
    "issued_actions",
    "no_actions_observed",
    "scouted",
    "built_workers",
    "built_supply",
    "built_units",
    "expanded",
    "moved_army",
    "attacked",
    "retreated",
    "idled",
    "stalled",
    "crashed",
    "bounded_exit",
    "voluntary_leave",
    "replay_saved",
    "video_registered",
)

POLICY_ADAPTER_SCAFFOLD_BURNY_M27_STYLE: Final[str] = (
    "starlab.sc2.burnysc2_policy.v15_m27_nontrivial_macro_smoke_watchability_scaffold_v1"
)


def real_candidate_live_policy_adapter_available() -> bool:
    """Return True only when a governed trained-checkpoint→live-SC2 adapter is wired (not yet)."""

    return False


NON_CLAIMS_M51: Final[tuple[str, ...]] = (
    "not_benchmark_execution",
    "not_benchmark_pass_fail",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_scorecard_authority",
    "not_twelve_hour_run",
    "not_xai",
    "not_human_panel",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
    "watchability_observation_only_when_live_sc2",
    "scaffold_policy_not_trained_candidate",
    "route_recommendation_advisory_only_recommended_not_executed",
)
