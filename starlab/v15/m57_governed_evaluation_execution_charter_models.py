"""V15-M57 — governed evaluation execution charter / dry-run gate constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.governed_evaluation_execution_charter.v1"
REPORT_CONTRACT_ID: Final[str] = "starlab.v15.governed_evaluation_execution_charter_report.v1"
PROFILE_M57: Final[str] = "starlab.v15.m57.governed_evaluation_execution_charter_dry_run_gate.v1"

MILESTONE: Final[str] = "V15-M57"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m57_governed_evaluation_execution_charter"

SCHEMA_VERSION: Final[str] = "1.0"
GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

FILENAME_MAIN_JSON: Final[str] = "v15_governed_evaluation_execution_charter.json"
REPORT_FILENAME: Final[str] = "v15_governed_evaluation_execution_charter_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_governed_evaluation_execution_charter_checklist.md"
DRY_RUN_COMMAND_FILENAME: Final[str] = "v15_m58_candidate_evaluation_dry_run_command.txt"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

# V15-M57A-OP1 canonical sealed artifact digests (must match operator-local success receipts).
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

# Upstream milestone merge anchors (public ledger) — see docs/starlab-v1.5.md for SHAs.
CONTRACT_ID_M56: Final[str] = "starlab.v15.bounded_evaluation_package_readout_decision.v1"
CONTRACT_ID_M57A: Final[str] = "starlab.v15.operator_live_visual_candidate_watch_session.v1"
CONTRACT_ID_M52A: Final[str] = "starlab.v15.candidate_live_adapter_spike.v1"

CHARTER_READY: Final[str] = "governed_evaluation_execution_charter_ready"
CHARTER_READY_WARNINGS: Final[str] = "governed_evaluation_execution_charter_ready_with_warnings"
CHARTER_BLOCKED: Final[str] = "governed_evaluation_execution_charter_blocked"

DRY_RUN_READY: Final[str] = "dry_run_gate_ready"
DRY_RUN_BLOCKED: Final[str] = "dry_run_gate_blocked"

CLASSIFICATION_CANDIDATE_LIVE_WATCH_COMPLETED: Final[str] = "candidate_live_visual_watch_completed"
CLASSIFICATION_SCAFFOLD_WATCH: Final[str] = "scaffold_visual_watch_completed_not_candidate_policy"

POLICY_CANDIDATE_LIVE_ADAPTER: Final[str] = "candidate_live_adapter"

M52A_STATUS_COMPLETED: Final[str] = "candidate_live_adapter_spike_completed"

ROUTE_M58: Final[str] = "route_to_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt"
ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED: Final[str] = "recommended_not_executed"
RECOMMENDED_NEXT_MILESTONE: Final[str] = "V15-M58"
RECOMMENDED_NEXT_TITLE: Final[str] = (
    "V15-M58 — Bounded Candidate Adapter Evaluation Execution Attempt"
)

M56_DECISION_READY: Final[str] = "ready_for_future_governed_evaluation"
M56_ROUTE_EXPECTED: Final[str] = "route_to_future_governed_evaluation_design_or_execution_gate"

WARNING_M56_READOUT_ABSENT: Final[str] = "m56_readout_context_not_supplied_non_blocking"
NOTICE_M56_READOUT_VERIFIED: Final[str] = "m56_readout_context_supplied_verified"

BLOCKED_INVALID_M56_READOUT_CONTEXT: Final[str] = "blocked_invalid_m56_readout_context"
BLOCKED_MISSING_M57A: Final[str] = "blocked_missing_m57a_watch_session"
BLOCKED_M57A_NOT_CANDIDATE_LIVE: Final[str] = "blocked_m57a_not_candidate_live_watch_completed"
BLOCKED_M57A_SCAFFOLD_ONLY: Final[str] = "blocked_m57a_scaffold_only_not_candidate_adapter"
BLOCKED_CANDIDATE_POLICY_NOT_CONFIRMED: Final[str] = (
    "blocked_candidate_policy_control_not_confirmed"
)
BLOCKED_MISSING_M52A: Final[str] = "blocked_missing_m52a_adapter_artifact"
BLOCKED_M52A_NOT_COMPLETED: Final[str] = "blocked_m52a_adapter_not_completed"
BLOCKED_CANDIDATE_IDENTITY: Final[str] = "blocked_candidate_identity_mismatch"
BLOCKED_REPLAY_NOT_SAVED: Final[str] = "blocked_replay_not_saved"
BLOCKED_INVALID_SEAL: Final[str] = "blocked_invalid_artifact_seal"
BLOCKED_CLAIM_FLAGS: Final[str] = "blocked_claim_flags_violation"
BLOCKED_PRIVATE_BOUNDARY: Final[str] = "blocked_private_boundary_violation"
BLOCKED_M57A_OP1_ANCHOR: Final[str] = "blocked_m57a_op1_anchor_mismatch"
BLOCKED_M52A_OP1_ANCHOR: Final[str] = "blocked_m52a_op1_anchor_mismatch"
BLOCKED_REPLAY_ANCHOR: Final[str] = "blocked_replay_anchor_mismatch"
BLOCKED_INVALID_MATCH_PROOF: Final[str] = "blocked_invalid_match_execution_proof"
BLOCKED_MATCH_PROOF_ACTION_MISMATCH: Final[str] = "blocked_match_proof_action_count_mismatch"
BLOCKED_MATCH_PROOF_MAP_MISMATCH: Final[str] = "blocked_match_proof_map_mismatch"

DRY_RUN_COMMAND_PLANNED: Final[str] = "planned_not_executed"

STRONGEST_ALLOWED: Final[str] = (
    "V15-M57 defines and validates a governed evaluation execution charter / dry-run gate "
    "for a future bounded candidate-adapter evaluation attempt, using the successful "
    "V15-M57A-OP1 candidate-live visual watch as evidence that the candidate adapter path can "
    "run live SC2. It does not execute evaluation or authorize benchmark/pass/promotion claims."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "M57 defines a governed evaluation execution charter and dry-run gate only.",
    "M57 does not execute evaluation matches.",
    "M57 does not compute benchmark pass/fail.",
    "M57 does not produce scorecard results.",
    "M57 does not evaluate strength.",
    "M57 does not promote or reject the checkpoint as a strength decision.",
    "M57 does not invoke torch.load.",
    "M57 does not load checkpoint blobs.",
    "M57 does not run live SC2.",
    "M57 does not run GPU inference.",
    "M57 does not run XAI or human-panel evaluation.",
    "M57 does not authorize showcase release, v2, or T2–T5.",
    "M57A-OP1 proved watchability adapter viability, not benchmark competence.",
)

DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "evaluation_execution_performed": False,
    "benchmark_execution_performed": False,
    "benchmark_passed": False,
    "benchmark_pass_fail_emitted": False,
    "scorecard_results_produced": False,
    "scorecard_total_computed": False,
    "win_rate_computed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "checkpoint_rejected_as_strength_decision": False,
    "torch_load_invoked_in_m57": False,
    "checkpoint_blob_loaded_in_m57": False,
    "live_sc2_executed_in_m57": False,
    "gpu_inference_executed_in_m57": False,
    "xai_executed": False,
    "human_panel_executed": False,
    "showcase_released": False,
    "v2_authorized": False,
    "t2_t3_t4_t5_executed": False,
}

M57_FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    DEFAULT_CLAIM_FLAGS.keys(),
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
