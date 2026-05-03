"""V15-M57A — operator live visual candidate watch session constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.operator_live_visual_candidate_watch_session.v1"
REPORT_CONTRACT_ID: Final[str] = (
    "starlab.v15.operator_live_visual_candidate_watch_session_report.v1"
)
PROFILE_M57A: Final[str] = "starlab.v15.m57a.operator_live_visual_candidate_watch_session.v1"

MILESTONE: Final[str] = "V15-M57A"
EMITTER_MODULE: Final[str] = (
    "starlab.v15.emit_v15_m57a_operator_live_visual_candidate_watch_session"
)
RUNNER_MODULE: Final[str] = "starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_operator_live_visual_candidate_watch_session.json"
REPORT_FILENAME: Final[str] = "v15_operator_live_visual_candidate_watch_session_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_operator_live_visual_candidate_watch_session_checklist.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

POLICY_FIXTURE: Final[str] = "fixture"
POLICY_CANDIDATE_LIVE_ADAPTER: Final[str] = "candidate_live_adapter"
POLICY_SCAFFOLD: Final[str] = "scaffold_watchability_policy"
POLICY_BLOCKED: Final[str] = "blocked_missing_adapter"

ADAPTER_NOT_USED: Final[str] = "not_used"
ADAPTER_AVAILABLE: Final[str] = "available"
ADAPTER_LOADED: Final[str] = "loaded"
ADAPTER_MISSING: Final[str] = "missing"
ADAPTER_BLOCKED: Final[str] = "blocked"
ADAPTER_OPERATOR_DECLARED: Final[str] = "operator_declared"

CANONICAL_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_M53_RUN_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_live_sc2"
STATUS_PREFLIGHT_READY_ADAPTER: Final[str] = (
    "operator_visual_watch_preflight_ready_candidate_adapter"
)
STATUS_PREFLIGHT_READY_SCAFFOLD: Final[str] = "operator_visual_watch_preflight_ready_scaffold_only"
STATUS_PREFLIGHT_BLOCKED: Final[str] = "operator_visual_watch_preflight_blocked"

CLASSIFICATION_FIXTURE: Final[str] = "fixture_schema_only_no_live_sc2"
CLASSIFICATION_CANDIDATE_LIVE_COMPLETED: Final[str] = "candidate_live_visual_watch_completed"
CLASSIFICATION_BLOCKED_MISSING_ADAPTER: Final[str] = (
    "candidate_live_visual_watch_blocked_missing_adapter"
)
CLASSIFICATION_ADAPTER_LOADED_SC2_BLOCKED: Final[str] = (
    "candidate_adapter_loaded_but_live_sc2_blocked"
)
CLASSIFICATION_SCAFFOLD: Final[str] = "scaffold_visual_watch_completed_not_candidate_policy"
CLASSIFICATION_PREFLIGHT_BLOCKED: Final[str] = "operator_visual_watch_preflight_blocked"

ROUTE_M57: Final[str] = "route_to_v15_m57_governed_evaluation_execution_charter_dry_run_gate"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"
RECOMMENDED_NEXT_MILESTONE: Final[str] = "V15-M57"

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_SESSION: Final[str] = "--authorize-live-visual-watch-session"
FLAG_PREFER_ADAPTER: Final[str] = "--prefer-candidate-live-adapter"
FLAG_SCAFFOLD_POLICY: Final[str] = "--allow-scaffold-watchability-policy"

FORBIDDEN_FLAG_CLAIM_BENCHMARK: Final[str] = "--claim-benchmark-pass"
FORBIDDEN_FLAG_CLAIM_STRENGTH: Final[str] = "--claim-strength"
FORBIDDEN_FLAG_PROMOTE: Final[str] = "--promote-checkpoint"
FORBIDDEN_FLAG_RUN_BENCHMARK: Final[str] = "--run-benchmark"
FORBIDDEN_FLAG_RUN_XAI: Final[str] = "--run-xai"
FORBIDDEN_FLAG_RUN_HUMAN_PANEL: Final[str] = "--run-human-panel"
FORBIDDEN_FLAG_SHOWCASE: Final[str] = "--release-showcase"
FORBIDDEN_FLAG_V2: Final[str] = "--authorize-v2"
FORBIDDEN_FLAG_T2: Final[str] = "--execute-t2"
FORBIDDEN_FLAG_T3: Final[str] = "--execute-t3"
FORBIDDEN_FLAG_T4: Final[str] = "--execute-t4"
FORBIDDEN_FLAG_T5: Final[str] = "--execute-t5"

FORBIDDEN_CLI_FLAGS: Final[tuple[str, ...]] = (
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_CLAIM_STRENGTH,
    FORBIDDEN_FLAG_PROMOTE,
    FORBIDDEN_FLAG_RUN_BENCHMARK,
    FORBIDDEN_FLAG_RUN_XAI,
    FORBIDDEN_FLAG_RUN_HUMAN_PANEL,
    FORBIDDEN_FLAG_SHOWCASE,
    FORBIDDEN_FLAG_V2,
    FORBIDDEN_FLAG_T2,
    FORBIDDEN_FLAG_T3,
    FORBIDDEN_FLAG_T4,
    FORBIDDEN_FLAG_T5,
)

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "visual_watch_session_attempted": False,
    "live_sc2_executed": False,
    "candidate_policy_control_confirmed": False,
    "scaffold_policy_used": False,
    "benchmark_execution_performed": False,
    "benchmark_passed": False,
    "benchmark_pass_fail_emitted": False,
    "scorecard_results_produced": False,
    "scorecard_total_computed": False,
    "win_rate_computed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "checkpoint_rejected_as_strength_decision": False,
    "xai_executed": False,
    "human_panel_executed": False,
    "showcase_released": False,
    "v2_authorized": False,
    "t2_t3_t4_t5_executed": False,
}

NON_CLAIMS: Final[tuple[str, ...]] = (
    "Visual watchability is observation evidence only.",
    "This is not benchmark execution.",
    "This is not benchmark pass/fail.",
    "This is not scorecard results.",
    "This is not strength evaluation.",
    "This is not checkpoint promotion.",
    "Scaffold watchability, if used, is not evidence that the trained candidate policy "
    "controlled gameplay.",
)

STRONGEST_ALLOWED_DEFAULT: Final[str] = (
    "V15-M57A can attempt an operator-local visual watch session for the latest V15-M53/V15-M54 "
    "candidate checkpoint through the best available governed live path, while honestly "
    "classifying whether the observed behavior came from a real candidate-live adapter or a "
    "scaffold watchability policy. It is observation/watchability evidence only, not benchmark "
    "evidence."
)

WARNING_M56_READOUT_ABSENT: Final[str] = "m56_readout_context_not_supplied_non_gating"
WARNING_M56A_ABSENT: Final[str] = "m56a_context_not_supplied_non_gating"
