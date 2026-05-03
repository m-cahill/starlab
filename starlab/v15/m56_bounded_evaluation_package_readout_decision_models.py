"""V15-M56 — bounded evaluation package readout / decision constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.bounded_evaluation_package_readout_decision.v1"
REPORT_CONTRACT_ID: Final[str] = "starlab.v15.bounded_evaluation_package_readout_decision_report.v1"
PROFILE_M56: Final[str] = "starlab.v15.m56.bounded_evaluation_package_readout_decision.v1"

MILESTONE: Final[str] = "V15-M56"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m56_bounded_evaluation_package_readout_decision"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_bounded_evaluation_package_readout_decision.json"
REPORT_FILENAME: Final[str] = "v15_bounded_evaluation_package_readout_decision_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_bounded_evaluation_package_readout_decision_checklist.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

CONTRACT_ID_M55: Final[str] = "starlab.v15.bounded_evaluation_package_preflight.v1"
M55_STATUS_READY: Final[str] = "ready_for_bounded_readout"

CANONICAL_M54_PACKAGE_SHA256: Final[str] = (
    "bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6"
)
CANONICAL_M53_RUN_ARTIFACT_SHA256: Final[str] = (
    "18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8"
)
CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

ROUTE_NEXT: Final[str] = "route_to_future_governed_evaluation_design_or_execution_gate"
ROUTE_STATUS: Final[str] = "recommended_not_executed"
RECOMMENDED_NEXT_MILESTONE: Final[str] = "V15-M57"
RECOMMENDED_NEXT_TITLE: Final[str] = (
    "V15-M57 — Governed Evaluation Execution Charter / Dry-Run Gate"
)

DECISION_READY: Final[str] = "ready_for_future_governed_evaluation"
DECISION_READY_WARNINGS: Final[str] = "ready_for_future_governed_evaluation_with_warnings"
DECISION_BLOCKED_MISSING_M55: Final[str] = "blocked_missing_m55_preflight"
DECISION_BLOCKED_INVALID_M55_CONTRACT: Final[str] = "blocked_invalid_m55_contract"
DECISION_BLOCKED_INVALID_M55_SEAL: Final[str] = "blocked_invalid_m55_artifact_seal"
DECISION_BLOCKED_M55_NOT_READY: Final[str] = "blocked_m55_preflight_not_ready"
DECISION_BLOCKED_M54_MISMATCH: Final[str] = "blocked_m54_anchor_mismatch"
DECISION_BLOCKED_M53_MISMATCH: Final[str] = "blocked_m53_anchor_mismatch"
DECISION_BLOCKED_CANDIDATE_MISMATCH: Final[str] = "blocked_candidate_identity_mismatch"
DECISION_BLOCKED_CLAIM_FLAGS: Final[str] = "blocked_claim_flags_violation"
DECISION_BLOCKED_PRIVATE_BOUNDARY: Final[str] = "blocked_private_boundary_violation"
DECISION_REQUIRES_REMEDIATION: Final[str] = "requires_remediation"

CONTRACT_ID_M54: Final[str] = "starlab.v15.twelve_hour_run_package_evaluation_readiness.v1"
CONTRACT_ID_M56A: Final[str] = "starlab.v15.latest_candidate_visual_watchability_confirmation.v1"

WARNING_M56A_ABSENT: Final[str] = "m56a_context_not_supplied_non_gating"
WARNING_M56A_STUB: Final[str] = "m56a_context_stub_or_scaffold_only_not_benchmark_evidence"
WARNING_M56A_INVALID: Final[str] = "m56a_context_invalid_non_gating"
WARNING_CROSS_CHECK_NO_M54_BODY: Final[str] = (
    "m53_candidate_cross_check_not_verified_from_m54_readiness_without_optional_path"
)

M56A_CONTEXT_ABSENT: Final[str] = "visual_watchability_context_absent"
M56A_CONTEXT_STUB: Final[str] = "visual_watchability_context_stub_only"
M56A_CONTEXT_SCAFFOLD: Final[str] = "visual_watchability_context_not_candidate_policy"
M56A_CONTEXT_ADAPTER_DECLARED: Final[str] = "supplied_candidate_adapter_declared"
M56A_GATING_NOT_A_GATE: Final[str] = "not_a_gate"

STRONGEST_ALLOWED: Final[str] = (
    "V15-M56 can read sealed V15-M55 preflight artifacts and emit a bounded readout / "
    "decision indicating whether the package is ready, blocked, or requires remediation "
    "for a future governed evaluation step. It does not execute evaluation or authorize "
    "benchmark/pass/promotion claims."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "No evaluation execution was performed.",
    "No benchmark pass/fail was computed or emitted.",
    "No scorecard results were produced.",
    "No strength evaluation was performed.",
    "No checkpoint was promoted.",
    "No checkpoint was rejected as a strength decision.",
    "No torch.load was invoked.",
    "No checkpoint blob was loaded.",
    "No live SC2 was executed.",
    "No GPU inference was executed.",
    "No XAI was executed.",
    "No human-panel evaluation was executed.",
    "No showcase agent was released.",
    "No v2 authorization was made.",
    "No T2–T5 execution was performed.",
)

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "evaluation_executed": False,
    "benchmark_execution_performed": False,
    "benchmark_passed": False,
    "benchmark_pass_fail_emitted": False,
    "scorecard_results_produced": False,
    "scorecard_total_computed": False,
    "win_rate_computed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "checkpoint_rejected_as_strength_decision": False,
    "torch_load_invoked": False,
    "checkpoint_blob_loaded": False,
    "live_sc2_executed": False,
    "gpu_inference_executed": False,
    "xai_executed": False,
    "human_panel_executed": False,
    "showcase_released": False,
    "v2_authorized": False,
    "t2_t3_t4_t5_executed": False,
}

M55_FORBIDDEN_TRUE_FLAGS: Final[frozenset[str]] = frozenset(
    (
        "evaluation_executed",
        "benchmark_pass_claimed",
        "candidate_promoted",
        "strong_agent_claimed",
        "human_panel_claimed",
        "xai_demo_claimed",
        "v2_ready_claimed",
    ),
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
FORBIDDEN_FLAG_LOAD_CKPT: Final[str] = "--load-checkpoint-for-evaluation"
FORBIDDEN_FLAG_TORCH_LOAD: Final[str] = "--torch-load-checkpoint"
FORBIDDEN_FLAG_BENCHMARK_PASS: Final[str] = "--emit-benchmark-pass"
FORBIDDEN_FLAG_EVAL_EXECUTED: Final[str] = "--claim-evaluation-executed"

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
    FORBIDDEN_FLAG_LOAD_CKPT,
    FORBIDDEN_FLAG_TORCH_LOAD,
    FORBIDDEN_FLAG_BENCHMARK_PASS,
    FORBIDDEN_FLAG_EVAL_EXECUTED,
)
