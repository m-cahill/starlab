"""V15-M56A — latest candidate visual watchability confirmation constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.latest_candidate_visual_watchability_confirmation.v1"
REPORT_CONTRACT_ID: Final[str] = (
    "starlab.v15.latest_candidate_visual_watchability_confirmation_report.v1"
)
PROFILE_M56A: Final[str] = "starlab.v15.m56a.latest_candidate_visual_watchability_confirmation.v1"

MILESTONE: Final[str] = "V15-M56A"
EMITTER_MODULE: Final[str] = (
    "starlab.v15.emit_v15_m56a_latest_candidate_visual_watchability_confirmation"
)
RUNNER_MODULE: Final[str] = (
    "starlab.v15.run_v15_m56a_latest_candidate_visual_watchability_confirmation"
)

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_latest_candidate_visual_watchability_confirmation.json"
REPORT_FILENAME: Final[str] = "v15_latest_candidate_visual_watchability_confirmation_report.json"
CHECKLIST_FILENAME: Final[str] = (
    "v15_latest_candidate_visual_watchability_confirmation_checklist.md"
)

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL: Final[str] = "operator_local_watchability"

MODE_FIXTURE_CI: Final[str] = "fixture_ci"
MODE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
MODE_OPERATOR_DECLARED: Final[str] = "operator_declared"
MODE_OPERATOR_LOCAL: Final[str] = "operator_local_watchability"

POLICY_FIXTURE: Final[str] = "fixture"
POLICY_SCAFFOLD: Final[str] = "scaffold_watchability_policy"
POLICY_CANDIDATE_LIVE: Final[str] = "candidate_live_adapter"
POLICY_BLOCKED: Final[str] = "blocked_missing_adapter"

ADAPTER_NOT_USED: Final[str] = "not_used"
ADAPTER_AVAILABLE: Final[str] = "available"
ADAPTER_MISSING: Final[str] = "missing"
ADAPTER_BLOCKED: Final[str] = "blocked"
ADAPTER_OPERATOR_DECLARED: Final[str] = "operator_declared"

STATUS_FIXTURE_ONLY: Final[str] = "fixture_schema_only_no_live_sc2"
STATUS_PREFLIGHT_READY: Final[str] = "watchability_preflight_ready"
STATUS_PREFLIGHT_BLOCKED: Final[str] = "watchability_blocked"
STATUS_VISUAL_CONFIRMED: Final[str] = "visual_watchability_confirmed"
STATUS_VISUAL_CONFIRMED_WARNINGS: Final[str] = "visual_watchability_confirmed_with_warnings"
STATUS_BLOCKED_ADAPTER: Final[str] = "watchability_blocked_missing_candidate_live_policy_adapter"
STATUS_SCAFFOLD_CONFIRMED: Final[str] = "scaffold_watchability_confirmed_not_candidate_policy"

CANONICAL_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_M53_RUN_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

ROUTE_M56_READOUT: Final[str] = "route_to_v15_m56_bounded_evaluation_package_readout_decision"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"

REASON_BLOCKED_MISSING_M55: Final[str] = "blocked_missing_m55_preflight"
REASON_BLOCKED_M55_NOT_READY: Final[str] = "blocked_m55_preflight_not_ready"
REASON_BLOCKED_M55_CONTRACT: Final[str] = "blocked_m55_contract_or_seal_invalid"
REASON_BLOCKED_M54_MISMATCH: Final[str] = "blocked_m54_package_mismatch"
REASON_BLOCKED_M53_MISMATCH: Final[str] = "blocked_m53_run_artifact_mismatch"
REASON_BLOCKED_CANDIDATE_MISMATCH: Final[str] = "blocked_candidate_identity_mismatch"
REASON_BLOCKED_WATCHABILITY_PATH: Final[str] = "blocked_missing_watchability_path"
REASON_BLOCKED_PRIVATE_BOUNDARY: Final[str] = "blocked_private_boundary_violation"
REASON_BLOCKED_CLAIM_VIOLATION: Final[str] = "blocked_claim_violation_in_declared_evidence"

GUARD_ALLOW_OPERATOR_LOCAL: Final[str] = "--allow-operator-local-execution"
GUARD_AUTHORIZE_VISUAL: Final[str] = "--authorize-visual-watchability-run"
FLAG_SCAFFOLD_POLICY: Final[str] = "--allow-scaffold-watchability-policy"

EVIDENCE_CONTRACT_DECLARED: Final[str] = (
    "starlab.v15.latest_candidate_visual_watchability_evidence_declared.v1"
)

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "evaluation_executed": False,
    "benchmark_passed": False,
    "benchmark_pass_fail_emitted": False,
    "scorecard_results_produced": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "torch_load_invoked_for_evaluation": False,
    "checkpoint_blob_loaded_for_evaluation": False,
    "xai_executed": False,
    "human_panel_executed": False,
    "showcase_released": False,
    "v2_authorized": False,
    "t2_t3_t4_t5_executed": False,
}

NON_CLAIMS: Final[tuple[str, ...]] = (
    "Visual watchability confirmation is not benchmark execution.",
    "Visual watchability confirmation is not strength evaluation.",
    "Visual watchability confirmation is not checkpoint promotion.",
    "Visual watchability confirmation is not benchmark pass/fail evidence.",
    "Visual watchability confirmation is not scorecard authority.",
    "Visual watchability confirmation is not XAI, human-panel, showcase, v2, or T2–T5 evidence.",
)

STRONGEST_ALLOWED_DEFAULT: Final[str] = (
    "The latest candidate checkpoint can be visually observed through a governed "
    "watchability path, "
    "or the path is deterministically blocked with reasons. "
    "This is observation/watchability evidence only, not benchmark evidence."
)

STRONGEST_ALLOWED_SCAFFOLD: Final[str] = (
    "The SC2 visual watchability path can be exercised with the scaffold watchability policy while "
    "binding the latest candidate identity; this does not prove the latest candidate policy itself "
    "is controlling gameplay."
)

STRONGEST_ALLOWED_OPERATOR_DECLARED_LIVE: Final[str] = (
    "Operator declared a candidate-live adapter watchability session for the bound "
    "checkpoint identity. "
    "This is declared observation metadata only, not independent proof that the trained policy "
    "controlled gameplay, and not benchmark evidence."
)

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
FORBIDDEN_FLAG_TORCH_LOAD: Final[str] = "--torch-load-checkpoint"
FORBIDDEN_FLAG_LOAD_CKPT: Final[str] = "--load-checkpoint-for-evaluation"

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
    FORBIDDEN_FLAG_TORCH_LOAD,
    FORBIDDEN_FLAG_LOAD_CKPT,
)
