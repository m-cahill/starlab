"""Constants and vocabulary for V15-M10 replay-native XAI demonstration (deterministic JSON)."""

from __future__ import annotations

from typing import Final

from starlab.v15.xai_evidence_models import CONTRACT_ID_XAI_EVIDENCE

# M10 contract: consumes/binds M04 family (CONTRACT_ID_XAI_EVIDENCE); no duplicate M04 vocabulary.
CONTRACT_ID_REPLAY_NATIVE_XAI_DEMONSTRATION: Final[str] = (
    "starlab.v15.replay_native_xai_demonstration.v1"
)
PROFILE_ID_REPLAY_NATIVE_XAI_DEMONSTRATION: Final[str] = (
    "starlab.v15.replay_native_xai_demonstration_profile.v1"
)

MILESTONE_ID_V15_M10: Final[str] = "V15-M10"
EMITTER_MODULE_REPLAY_NATIVE_XAI: Final[str] = (
    "starlab.v15.emit_v15_replay_native_xai_demonstration"
)

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_REPLAY_NATIVE_XAI: Final[str] = "1"

FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION: Final[str] = "v15_replay_native_xai_demonstration.json"
REPORT_FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION: Final[str] = (
    "v15_replay_native_xai_demonstration_report.json"
)
FILENAME_XAI_EXPLANATION_REPORT_MD: Final[str] = "v15_xai_explanation_report.md"

SEAL_KEY_REPLAY_NATIVE_XAI_DEMONSTRATION: Final[str] = "replay_native_xai_demonstration_sha256"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_DEMONSTRATION_ID: Final[str] = "v15_m10:fixture_ci:deterministic"

# --- XAI evidence family (re-export for binding checks; defined in M04) ---
XAI_EVIDENCE_FAMILY_CONTRACT_ID: Final[str] = CONTRACT_ID_XAI_EVIDENCE

# --- Demonstration status vocabulary ---
DEMONSTRATION_STATUS_FIXTURE_CONTRACT_ONLY: Final[str] = "fixture_contract_only"
DEMONSTRATION_STATUS_BLOCKED_M08_RECEIPT: Final[str] = "blocked_missing_m08_campaign_receipt"
DEMONSTRATION_STATUS_BLOCKED_PROMOTED_CP: Final[str] = "blocked_missing_promoted_checkpoint"
DEMONSTRATION_STATUS_BLOCKED_REPLAY_ID: Final[str] = "blocked_missing_replay_identity"
DEMONSTRATION_STATUS_BLOCKED_CHECKPOINT_ID: Final[str] = "blocked_missing_checkpoint_identity"
DEMONSTRATION_STATUS_BLOCKED_DECISION_TRACE: Final[str] = "blocked_missing_decision_trace"
DEMONSTRATION_STATUS_BLOCKED_SCENE: Final[str] = "blocked_missing_scene_coverage"
DEMONSTRATION_STATUS_OPERATOR_DECLARED_PACK: Final[str] = "operator_declared_xai_pack"
DEMONSTRATION_STATUS_OPERATOR_LOCAL_VALIDATED: Final[str] = "operator_local_xai_demo_validated"

# --- Gate ids (X0–X10) ---
X0_ARTIFACT_INTEGRITY: Final[str] = "X0_artifact_integrity"
X1_PROMOTION_BINDING: Final[str] = "X1_promotion_binding"
X2_REPLAY_IDENTITY_BINDING: Final[str] = "X2_replay_identity_binding"
X3_CHECKPOINT_IDENTITY_BINDING: Final[str] = "X3_checkpoint_identity_binding"
X4_DECISION_TRACE_COVERAGE: Final[str] = "X4_decision_trace_coverage"
X5_SCENE_COVERAGE: Final[str] = "X5_scene_coverage"
X6_COUNTERFACTUAL_COVERAGE: Final[str] = "X6_counterfactual_coverage"
X7_OVERLAY_MANIFEST: Final[str] = "X7_overlay_manifest"
X8_REPORT_RENDERING: Final[str] = "X8_report_rendering"
X9_PUBLIC_PRIVATE_BOUNDARY: Final[str] = "X9_public_private_boundary"
X10_NON_CLAIM_BOUNDARY: Final[str] = "X10_non_claim_boundary"

ALL_GATE_IDS: Final[tuple[str, ...]] = (
    X0_ARTIFACT_INTEGRITY,
    X1_PROMOTION_BINDING,
    X2_REPLAY_IDENTITY_BINDING,
    X3_CHECKPOINT_IDENTITY_BINDING,
    X4_DECISION_TRACE_COVERAGE,
    X5_SCENE_COVERAGE,
    X6_COUNTERFACTUAL_COVERAGE,
    X7_OVERLAY_MANIFEST,
    X8_REPORT_RENDERING,
    X9_PUBLIC_PRIVATE_BOUNDARY,
    X10_NON_CLAIM_BOUNDARY,
)

GATE_STATUS_PASS: Final[str] = "pass"
GATE_STATUS_WARNING: Final[str] = "warning"
GATE_STATUS_FAIL: Final[str] = "fail"
GATE_STATUS_BLOCKED: Final[str] = "blocked"
GATE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"

# --- Scene types (v1.5 minimum demonstration coverage) ---
SCENE_OPENING_BUILD: Final[str] = "opening_build"
SCENE_FIRST_SCOUT: Final[str] = "first_scout"
SCENE_FIRST_COMBAT: Final[str] = "first_combat"
SCENE_EXPANSION_TIMING: Final[str] = "expansion_timing"
SCENE_DEFENSIVE_RESPONSE: Final[str] = "defensive_response"
SCENE_WINNING_PUSH: Final[str] = "winning_push"
SCENE_LOSS_OR_FAILURE: Final[str] = "loss_or_failure_case"
SCENE_COUNTERFACTUAL: Final[str] = "counterfactual_decision"

ALL_SCENE_TYPES: Final[tuple[str, ...]] = (
    SCENE_OPENING_BUILD,
    SCENE_FIRST_SCOUT,
    SCENE_FIRST_COMBAT,
    SCENE_EXPANSION_TIMING,
    SCENE_DEFENSIVE_RESPONSE,
    SCENE_WINNING_PUSH,
    SCENE_LOSS_OR_FAILURE,
    SCENE_COUNTERFACTUAL,
)

# --- Decision classes ---
DECISION_CLASS_MACRO: Final[str] = "macro"
DECISION_CLASS_TACTICAL: Final[str] = "tactical"
DECISION_CLASS_SCOUTING_UNCERTAINTY: Final[str] = "scouting_uncertainty"
DECISION_CLASS_COUNTERFACTUAL: Final[str] = "counterfactual"
DECISION_CLASS_ECONOMY: Final[str] = "economy"
DECISION_CLASS_PRODUCTION: Final[str] = "production"
DECISION_CLASS_MOVEMENT: Final[str] = "movement"
DECISION_CLASS_COMBAT: Final[str] = "combat"
DECISION_CLASS_FALLBACK_NOOP: Final[str] = "fallback_noop_safety"

ALL_DECISION_CLASSES: Final[tuple[str, ...]] = (
    DECISION_CLASS_MACRO,
    DECISION_CLASS_TACTICAL,
    DECISION_CLASS_SCOUTING_UNCERTAINTY,
    DECISION_CLASS_COUNTERFACTUAL,
    DECISION_CLASS_ECONOMY,
    DECISION_CLASS_PRODUCTION,
    DECISION_CLASS_MOVEMENT,
    DECISION_CLASS_COMBAT,
    DECISION_CLASS_FALLBACK_NOOP,
)

NON_CLAIMS_V15_M10: Final[tuple[str, ...]] = (
    "V15-M10 does not train a checkpoint; does not promote a checkpoint; does not run the long "
    "GPU campaign; does not prove explanation faithfulness; does not run a human panel; does "
    "not authorize strong-agent, human-benchmark, ladder, or v2 claims; and does not commit "
    "raw replays, weights, checkpoints, saliency tensors, videos, or private operator paths.",
    "M10 replay-native XAI demonstration is a governed reporting and validation surface over "
    f"M04 family packs (`{CONTRACT_ID_XAI_EVIDENCE}`), not a proof of real model inference or "
    "explanation faithfulness.",
)


def default_m10_authorization_flags() -> dict[str, bool]:
    return {
        "xai_demo_executed": False,
        "real_inference_executed": False,
        "faithfulness_validated": False,
        "checkpoint_promoted_for_xai": False,
        "strong_agent_claim_authorized": False,
        "human_benchmark_claim_authorized": False,
        "ladder_claim_authorized": False,
        "v2_authorized": False,
    }
