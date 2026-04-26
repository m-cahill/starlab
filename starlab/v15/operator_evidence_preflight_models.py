"""V15-M15 operator evidence collection preflight — constants and vocabulary.

(Preflight only; no collection.)
"""

from __future__ import annotations

from typing import Final

CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT: Final[str] = (
    "starlab.v15.operator_evidence_collection_preflight.v1"
)

MILESTONE_ID_V15_M15: Final[str] = "V15-M15"
EMITTER_MODULE_OPERATOR_EVIDENCE_PREFLIGHT: Final[str] = (
    "starlab.v15.emit_v15_operator_evidence_collection_preflight"
)

REPORT_VERSION_OPERATOR_EVIDENCE_PREFLIGHT: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT: Final[str] = (
    "v15_operator_evidence_collection_preflight.json"
)
REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT: Final[str] = (
    "v15_operator_evidence_collection_preflight_report.json"
)
FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD: Final[str] = (
    "v15_operator_evidence_collection_checklist.md"
)

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_WITH_M13_M14_BINDINGS: Final[str] = "operator_preflight_with_bindings"

PLACEHOLDER_SHA256: Final[str] = "0" * 64

PREFLIGHT_STATUS_PLAN_READY: Final[str] = "preflight_plan_ready"
STATUS_OPERATOR_EVIDENCE_NOT_STARTED: Final[str] = "not_started"
STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED: Final[str] = "operator_evidence_not_collected"

# Preflight gate ids P0–P14
P0_M13_NO_GO: Final[str] = "P0_m13_no_go_context_bound"
P1_M14_PLAN: Final[str] = "P1_m14_remediation_plan_bound"
P2_PRIVATE_WORKSPACE: Final[str] = "P2_private_workspace_declared"
P3_NO_PRIVATE_PATHS_COMMITTED: Final[str] = "P3_no_private_paths_committed"
P4_INPUTS_INVENTORY: Final[str] = "P4_required_inputs_inventory_complete"
P5_RIGHTS_TOUCHPOINTS: Final[str] = "P5_rights_register_touchpoints_declared"
P6_M16_ENV: Final[str] = "P6_environment_evidence_preflight_defined"
P7_M17_LONG: Final[str] = "P7_long_gpu_campaign_preflight_defined"
P8_M18_CHECKPOINT: Final[str] = "P8_checkpoint_evaluation_preflight_defined"
P9_M19_XAI: Final[str] = "P9_xai_evidence_preflight_defined"
P10_HUMAN_PANEL: Final[str] = "P10_human_panel_preflight_defined"
P11_SHOWCASE_RELEASE: Final[str] = "P11_showcase_release_preflight_defined"
P12_V2_BLOCKED: Final[str] = "P12_v2_reconsideration_blocked"
P13_NO_EXEC: Final[str] = "P13_no_operator_execution"
P14_DOCS_TESTS: Final[str] = "P14_docs_tests_aligned"

ALL_PREFLIGHT_GATE_IDS: Final[tuple[str, ...]] = (
    P0_M13_NO_GO,
    P1_M14_PLAN,
    P2_PRIVATE_WORKSPACE,
    P3_NO_PRIVATE_PATHS_COMMITTED,
    P4_INPUTS_INVENTORY,
    P5_RIGHTS_TOUCHPOINTS,
    P6_M16_ENV,
    P7_M17_LONG,
    P8_M18_CHECKPOINT,
    P9_M19_XAI,
    P10_HUMAN_PANEL,
    P11_SHOWCASE_RELEASE,
    P12_V2_BLOCKED,
    P13_NO_EXEC,
    P14_DOCS_TESTS,
)

GATE_POSTURE_PASS: Final[str] = "pass"
GATE_POSTURE_PASS_FIXTURE: Final[str] = "pass_or_fixture"
GATE_POSTURE_NOT_EVALUATED: Final[str] = "not_evaluated"

# Sequence ids S0–S10
S0_CONTEXT: Final[str] = "S0_m13_m14_context_binding"
S1_WORKSPACE: Final[str] = "S1_private_workspace_preflight"
S2_ENV_SHORT: Final[str] = "S2_environment_and_short_gpu_inputs"
S3_TRAINING: Final[str] = "S3_training_asset_and_rights_inputs"
S4_LONG_GPU: Final[str] = "S4_long_gpu_campaign_inputs"
S5_CHECKPOINT: Final[str] = "S5_checkpoint_lineage_and_resume_inputs"
S6_EVAL: Final[str] = "S6_evaluation_and_promotion_inputs"
S7_XAI: Final[str] = "S7_xai_pack_inputs"
S8_HUMAN: Final[str] = "S8_human_panel_inputs"
S9_SHOWCASE: Final[str] = "S9_showcase_release_inputs"
S10_V2: Final[str] = "S10_v2_reconsideration_inputs"

ALL_SEQUENCE_IDS: Final[tuple[str, ...]] = (
    S0_CONTEXT,
    S1_WORKSPACE,
    S2_ENV_SHORT,
    S3_TRAINING,
    S4_LONG_GPU,
    S5_CHECKPOINT,
    S6_EVAL,
    S7_XAI,
    S8_HUMAN,
    S9_SHOWCASE,
    S10_V2,
)

SEQUENCE_STATUS_NOT_STARTED: Final[str] = "not_started"
SEQUENCE_STATUS_BLOCKED_ARTIFACTS: Final[str] = "blocked_missing_operator_artifacts"
SEQUENCE_STATUS_BLOCKED_RIGHTS: Final[str] = "blocked_private_rights_review"
SEQUENCE_STATUS_BLOCKED_UPSTREAM: Final[str] = "blocked_missing_upstream_evidence"
SEQUENCE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"
SEQUENCE_STATUS_READY_REVIEW: Final[str] = "ready_for_operator_review"

REGISTER_TOUCHPOINT_PATHS: Final[tuple[str, ...]] = (
    "docs/rights_register.md",
    "docs/training_asset_register.md",
    "docs/replay_corpus_register.md",
    "docs/model_weight_register.md",
    "docs/checkpoint_asset_register.md",
    "docs/xai_evidence_register.md",
    "docs/human_benchmark_register.md",
)

NON_CLAIMS_V15_M15: Final[str] = (
    "V15-M15 defines operator evidence collection preflight, sequencing, and register touchpoints; "
    "it does not collect operator evidence, does not run GPU training or shakedown, and does not "
    "promote a checkpoint or execute benchmarks, XAI, human-panel, or showcase surfaces, and does "
    "not authorize v2 or v2 recharter. V15-M16–V15-M21 are sequencing targets, not completed "
    "evidence."
)

FORBIDDEN_CHECKLIST_SUBSTRINGS: Final[tuple[str, ...]] = (
    "v2 is authorized",
    "the long gpu campaign completed",
    "the checkpoint is promoted for claim",
    "the agent beats most humans",
)

__all__ = [
    "ALL_PREFLIGHT_GATE_IDS",
    "ALL_SEQUENCE_IDS",
    "CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT",
    "EMITTER_MODULE_OPERATOR_EVIDENCE_PREFLIGHT",
    "FILENAME_OPERATOR_EVIDENCE_COLLECTION_CHECKLIST_MD",
    "FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT",
    "FORBIDDEN_CHECKLIST_SUBSTRINGS",
    "GATE_POSTURE_NOT_EVALUATED",
    "GATE_POSTURE_PASS",
    "GATE_POSTURE_PASS_FIXTURE",
    "MILESTONE_ID_V15_M15",
    "NON_CLAIMS_V15_M15",
    "P0_M13_NO_GO",
    "P1_M14_PLAN",
    "P10_HUMAN_PANEL",
    "P11_SHOWCASE_RELEASE",
    "P12_V2_BLOCKED",
    "P13_NO_EXEC",
    "P14_DOCS_TESTS",
    "P2_PRIVATE_WORKSPACE",
    "P3_NO_PRIVATE_PATHS_COMMITTED",
    "P4_INPUTS_INVENTORY",
    "P5_RIGHTS_TOUCHPOINTS",
    "P6_M16_ENV",
    "P7_M17_LONG",
    "P8_M18_CHECKPOINT",
    "P9_M19_XAI",
    "PREFLIGHT_STATUS_PLAN_READY",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_WITH_M13_M14_BINDINGS",
    "REPORT_FILENAME_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT",
    "REPORT_VERSION_OPERATOR_EVIDENCE_PREFLIGHT",
    "REGISTER_TOUCHPOINT_PATHS",
    "S0_CONTEXT",
    "S10_V2",
    "S1_WORKSPACE",
    "S2_ENV_SHORT",
    "S3_TRAINING",
    "S4_LONG_GPU",
    "S5_CHECKPOINT",
    "S6_EVAL",
    "S7_XAI",
    "S8_HUMAN",
    "S9_SHOWCASE",
    "SEAL_KEY_ARTIFACT",
    "STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED",
    "STATUS_OPERATOR_EVIDENCE_NOT_STARTED",
    "SEQUENCE_STATUS_BLOCKED_ARTIFACTS",
    "SEQUENCE_STATUS_BLOCKED_RIGHTS",
    "SEQUENCE_STATUS_BLOCKED_UPSTREAM",
    "SEQUENCE_STATUS_NOT_APPLICABLE",
    "SEQUENCE_STATUS_NOT_STARTED",
    "SEQUENCE_STATUS_READY_REVIEW",
]
