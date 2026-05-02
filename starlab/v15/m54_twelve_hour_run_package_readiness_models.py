"""V15-M54 — twelve-hour run package / evaluation readiness constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M54: Final[str] = "starlab.v15.twelve_hour_run_package_evaluation_readiness.v1"
PROFILE_M54: Final[str] = "starlab.v15.m54.twelve_hour_run_package_evaluation_readiness.v1"

MILESTONE_LABEL_M54: Final[str] = "V15-M54"

EMITTER_MODULE_M54: Final[str] = "starlab.v15.emit_v15_m54_twelve_hour_run_package_readiness"

FILENAME_MAIN_JSON: Final[str] = "v15_twelve_hour_run_package_readiness.json"
REPORT_FILENAME: Final[str] = "v15_twelve_hour_run_package_readiness_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_twelve_hour_run_package_readiness_checklist.md"
BINDING_FILENAME: Final[str] = "v15_m54_candidate_checkpoint_binding.json"
MANIFEST_FILENAME: Final[str] = "v15_m54_evaluation_readiness_manifest.json"
BRIEF_FILENAME: Final[str] = "v15_twelve_hour_run_package_readiness_brief.md"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_package_evidence"
STATUS_READY: Final[str] = "twelve_hour_run_package_ready_for_bounded_evaluation_readiness"
STATUS_READY_WARNINGS: Final[str] = "twelve_hour_run_package_ready_with_warnings"
STATUS_BLOCKED: Final[str] = "twelve_hour_run_package_blocked"
STATUS_REFUSED: Final[str] = "twelve_hour_run_package_refused"

ANCHOR_CANONICAL_M53_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
ANCHOR_RAW_M53_FILE_SHA256: Final[str] = (
    "6831c693c83b2184555be74f2d73d70a7ccae9c6147a4ac47c5a7fd18c002150"
)
ANCHOR_PRODUCED_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)
ANCHOR_INPUT_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943"
)
ANCHOR_PHASE_A_MATCH_PROOF_SHA256: Final[str] = (
    "07923255659d0d09798f5e051ece295de77fdb527698313ec69c8df46b1be2aa"
)

FINAL_CHECKPOINT_RELATIVE_PATH: Final[str] = (
    "m28_training/checkpoints/candidate_checkpoint_step_59858688_final.pt"
)

RECOMMENDED_NEXT_SUCCESS: Final[str] = "V15-M55_bounded_evaluation_package_preflight"
RECOMMENDED_NEXT_REMEDIATION: Final[str] = "V15-M55_12_hour_run_package_remediation"

ROUTE_BOUNDED_EVAL_PREFLIGHT: Final[str] = "route_to_bounded_evaluation_package_preflight"
ROUTE_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

BINDING_REQUIRED_SENTENCE: Final[str] = (
    "The produced checkpoint is bound as a candidate artifact for future evaluation routing. "
    "V15-M54 does not promote this checkpoint."
)

NON_CLAIMS_M54: Final[tuple[str, ...]] = (
    "not_benchmark_pass_fail",
    "not_strength_evaluation",
    "not_checkpoint_promotion",
    "not_xai",
    "not_human_panel",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_t3_t4_t5_execution",
    "package_and_readiness_routing_only",
)

WARNING_M50_UPSTREAM: Final[str] = "warning_m50_upstream_fixture_bounded_only"
WARNING_FINAL_M53_REPLAY_FALSE: Final[str] = "warning_final_m53_replay_saved_false"
WARNING_TRANSCRIPT_SHORT: Final[str] = "warning_transcript_short_or_redacted"
WARNING_PHASE_A_REPLAY_BUT_M53_FALSE: Final[str] = (
    "warning_phase_a_replay_saved_but_final_m53_replay_false"
)
WARNING_PACKAGE_READY_NOT_EVAL: Final[str] = "warning_package_ready_but_not_evaluation"
WARNING_CHECKPOINT_CANDIDATE_ONLY: Final[str] = "warning_checkpoint_candidate_only_not_promoted"
WARNING_RAW_ARTIFACT_HASH_MISSING: Final[str] = "warning_raw_artifact_hash_missing"

BLOCKED_MISSING_M53_JSON: Final[str] = "blocked_missing_m53_run_json"
BLOCKED_M53_CONTRACT_INVALID: Final[str] = "blocked_m53_contract_invalid"
BLOCKED_M53_SHA_MISMATCH: Final[str] = "blocked_m53_sha_mismatch"
BLOCKED_M53_NOT_COMPLETED: Final[str] = "blocked_m53_not_completed"
BLOCKED_M53_HAS_BLOCKERS: Final[str] = "blocked_m53_has_blockers"
BLOCKED_M53_HAS_FAILURE_REASONS: Final[str] = "blocked_m53_has_failure_reasons"
BLOCKED_FULL_WALL_CLOCK: Final[str] = "blocked_full_wall_clock_not_satisfied"
BLOCKED_FINAL_CKPT_NOT_PERSISTED_M53: Final[str] = "blocked_final_checkpoint_not_persisted"
BLOCKED_FINAL_CKPT_MISSING: Final[str] = "blocked_final_checkpoint_missing"
BLOCKED_FINAL_CKPT_SHA_MISMATCH: Final[str] = "blocked_final_checkpoint_sha_mismatch"
BLOCKED_INVENTORY_MISSING: Final[str] = "blocked_checkpoint_inventory_missing"
BLOCKED_INVENTORY_MISSING_FINAL: Final[str] = (
    "blocked_checkpoint_inventory_missing_final_checkpoint"
)
BLOCKED_TELEMETRY_MISSING: Final[str] = "blocked_telemetry_summary_missing"
BLOCKED_TRANSCRIPT_MISSING: Final[str] = "blocked_transcript_missing"
BLOCKED_PHASE_A_PROOF: Final[str] = "blocked_phase_a_proof_missing"
BLOCKED_PUBLIC_PRIVATE: Final[str] = "blocked_public_private_boundary_risk"
BLOCKED_RAW_SHA_MISMATCH: Final[str] = "blocked_raw_artifact_hash_mismatch"

REFUSED_FORBIDDEN: Final[str] = "refused_forbidden_overclaim_flag"

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
FORBIDDEN_FLAG_LOAD_CKPT_EVAL: Final[str] = "--load-checkpoint-for-evaluation"
FORBIDDEN_FLAG_TORCH_LOAD: Final[str] = "--torch-load-checkpoint"

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
    FORBIDDEN_FLAG_LOAD_CKPT_EVAL,
    FORBIDDEN_FLAG_TORCH_LOAD,
)

TRANSCRIPT_SHORT_WARN_BYTES: Final[int] = 160
