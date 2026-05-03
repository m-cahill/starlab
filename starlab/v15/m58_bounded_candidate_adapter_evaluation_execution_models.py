"""V15-M58 — bounded candidate adapter evaluation execution attempt constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.bounded_candidate_adapter_evaluation_execution.v1"
REPORT_CONTRACT_ID: Final[str] = (
    "starlab.v15.bounded_candidate_adapter_evaluation_execution_report.v1"
)
PROFILE_M58: Final[str] = (
    "starlab.v15.m58.bounded_candidate_adapter_evaluation_execution_attempt.v1"
)

MILESTONE: Final[str] = "V15-M58"
EMITTER_MODULE: Final[str] = (
    "starlab.v15.emit_v15_m58_bounded_candidate_adapter_evaluation_execution"
)
RUNNER_MODULE: Final[str] = (
    "starlab.v15.run_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt"
)

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_candidate_adapter_evaluation_execution.json"
REPORT_FILENAME: Final[str] = "v15_bounded_candidate_adapter_evaluation_execution_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_bounded_candidate_adapter_evaluation_execution_checklist.md"
OPERATOR_TRANSCRIPT_FILENAME: Final[str] = "v15_m58_operator_transcript.txt"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_EXECUTION: Final[str] = "operator_local_execution"

# Upstream M57 contract (charter consumer).
CONTRACT_ID_M57_CHARTER: Final[str] = "starlab.v15.governed_evaluation_execution_charter.v1"

V15_M57_MERGE_SHA: Final[str] = "b56bc558591af38be8bcf91190d0235338aad3d5"

CANONICAL_M57A_OP1_WATCH_SESSION_SHA256: Final[str] = (
    "1b2b8704743354540e8f389a847315aa2bd8c8ead47b63edd81cd91a61df430c"
)
CANONICAL_M57A_OP1_M52A_ADAPTER_SHA256: Final[str] = (
    "7458f5c370be4b04465a2d4f9d85321b313c34ef0ab0e6d48124ff0dadd7fa47"
)
CANONICAL_M57A_OP1_REPLAY_SHA256: Final[str] = (
    "c0d88e54cdbc7eed7df27ddfcb4ae7e1b642993287a7e75c83d755097fbd89fa"
)
CANONICAL_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_M53_RUN_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

ROUTE_EXPECTED_FROM_M57: Final[str] = (
    "route_to_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt"
)
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

ROUTE_M59: Final[str] = (
    "route_to_v15_m59_evaluation_readout_benchmark_pass_fail_refusal_or_threshold_decision"
)
RECOMMENDED_NEXT_MILESTONE: Final[str] = "V15-M59"
RECOMMENDED_NEXT_TITLE: Final[str] = (
    "V15-M59 — Evaluation Readout / Benchmark Pass-Fail Refusal or Threshold Decision"
)

CHARTER_BASELINE_CLASS: Final[str] = "passive_or_scripted_baseline"
CHARTER_MAP_LOGICAL_KEY: Final[str] = "Maps/Waterfall.SC2Map"
CHARTER_GAME_STEP: Final[int] = 8
CHARTER_MAX_GAME_STEPS: Final[int] = 2048

OPPONENT_MODE_PASSIVE_OR_SCRIPTED: Final[str] = "passive_or_scripted_baseline"
OPPONENT_MODE_BURNY_PASSIVE: Final[str] = "burnysc2_passive_bot"
NORMALIZED_OPPONENT_MODE: Final[str] = "burnysc2_passive_bot"

MIN_ATTEMPT_COUNT: Final[int] = 1
MAX_ATTEMPT_COUNT: Final[int] = 3

STATUS_FIXTURE_SCHEMA_ONLY: Final[str] = "fixture_schema_only_no_live_sc2"
STATUS_PREFLIGHT_READY: Final[str] = (
    "operator_preflight_ready_for_bounded_candidate_adapter_execution"
)
STATUS_PREFLIGHT_BLOCKED: Final[str] = "operator_preflight_blocked"
STATUS_EXECUTION_COMPLETED: Final[str] = "bounded_candidate_adapter_execution_completed"
STATUS_EXECUTION_COMPLETED_WARNINGS: Final[str] = (
    "bounded_candidate_adapter_execution_completed_with_warnings"
)
STATUS_EXECUTION_BLOCKED: Final[str] = "bounded_candidate_adapter_execution_blocked"

BLOCKED_MISSING_M57_CHARTER: Final[str] = "blocked_missing_m57_charter"
BLOCKED_INVALID_M57_CHARTER: Final[str] = "blocked_invalid_m57_charter"
BLOCKED_INVALID_M57_ARTIFACT_SEAL: Final[str] = "blocked_invalid_m57_artifact_seal"
BLOCKED_M57_ROUTE_NOT_TO_M58: Final[str] = "blocked_m57_route_not_to_m58"
BLOCKED_M57_ROUTE_STATUS_NOT_RECOMMENDED: Final[str] = (
    "blocked_m57_route_status_not_recommended_not_executed"
)
BLOCKED_CANDIDATE_IDENTITY_MISMATCH: Final[str] = "blocked_candidate_identity_mismatch"
BLOCKED_CANDIDATE_CHECKPOINT_MISSING: Final[str] = "blocked_candidate_checkpoint_missing"
BLOCKED_CANDIDATE_CHECKPOINT_SHA_MISMATCH: Final[str] = "blocked_candidate_checkpoint_sha_mismatch"
BLOCKED_MISSING_SC2_ROOT: Final[str] = "blocked_missing_sc2_root"
BLOCKED_MISSING_MAP_PATH: Final[str] = "blocked_missing_map_path"
BLOCKED_DISALLOWED_BASELINE: Final[str] = "blocked_disallowed_baseline"
BLOCKED_DISALLOWED_MAP: Final[str] = "blocked_disallowed_map"
BLOCKED_DISALLOWED_HORIZON: Final[str] = "blocked_disallowed_horizon"
BLOCKED_REPLAY_NOT_SAVED: Final[str] = "blocked_replay_not_saved"
BLOCKED_M52A_DELEGATE_FAILED: Final[str] = "blocked_m52a_delegate_failed"
BLOCKED_CLAIM_FLAGS_VIOLATION: Final[str] = "blocked_claim_flags_violation"
BLOCKED_PRIVATE_BOUNDARY_VIOLATION: Final[str] = "blocked_private_boundary_violation"
BLOCKED_ATTEMPT_COUNT: Final[str] = "blocked_attempt_count_out_of_scope_for_m58"
BLOCKED_DUAL_GUARD_MISSING: Final[str] = (
    "blocked_bounded_candidate_adapter_evaluation_dual_guard_missing"
)

ROUTE_STATUS_TO_M59: Final[str] = "recommended_not_executed"

STRONGEST_ALLOWED: Final[str] = (
    "V15-M58 can execute a tightly bounded candidate-adapter evaluation-smoke attempt under "
    "explicit operator guards and emit completion/refusal metadata over the M57-chartered "
    "candidate-live adapter path. It does not compute benchmark pass/fail, produce scorecard "
    "results, evaluate strength, or promote the checkpoint."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "M58 is a bounded candidate-adapter execution attempt only.",
    "M58 does not compute benchmark pass/fail.",
    "M58 does not produce scorecard results.",
    "M58 does not evaluate strength.",
    "M58 does not promote or reject the checkpoint as a strength decision.",
    "M58 does not run XAI or human-panel evaluation.",
    "M58 does not release a showcase agent.",
    "M58 does not authorize v2 or T2–T5.",
)

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_BOUNDED_EVAL: Final[str] = "--authorize-bounded-candidate-adapter-evaluation"

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
    "evaluation_execution_performed": False,
    "bounded_adapter_execution_performed": False,
    "benchmark_execution_performed": False,
    "benchmark_passed": False,
    "benchmark_pass_fail_emitted": False,
    "scorecard_results_produced": False,
    "scorecard_total_computed": False,
    "win_rate_computed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "checkpoint_rejected_as_strength_decision": False,
    "torch_load_invoked_for_execution": False,
    "checkpoint_blob_loaded_for_execution": False,
    "live_sc2_executed": False,
    "gpu_inference_executed": False,
    "xai_executed": False,
    "human_panel_executed": False,
    "showcase_released": False,
    "v2_authorized": False,
    "t2_t3_t4_t5_executed": False,
}

M58_FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "benchmark_execution_performed",
        "benchmark_passed",
        "benchmark_pass_fail_emitted",
        "scorecard_results_produced",
        "scorecard_total_computed",
        "win_rate_computed",
        "strength_evaluated",
        "checkpoint_promoted",
        "checkpoint_rejected_as_strength_decision",
        "xai_executed",
        "human_panel_executed",
        "showcase_released",
        "v2_authorized",
        "t2_t3_t4_t5_executed",
    },
)

M52A_DELEGATE_SUBDIR: Final[str] = "candidate_live_adapter_watch"
M52A_REPLAY_RELPATH: Final[str] = "replay/validation.SC2Replay"
