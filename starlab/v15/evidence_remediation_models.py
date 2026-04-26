"""V15-M14 evidence remediation plan — constants and vocabulary (planning / readiness only)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN: Final[str] = "starlab.v15.evidence_remediation_plan.v1"

MILESTONE_ID_V15_M14: Final[str] = "V15-M14"
EMITTER_MODULE_EVIDENCE_REMEDIATION: Final[str] = "starlab.v15.emit_v15_evidence_remediation_plan"

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_EVIDENCE_REMEDIATION: Final[str] = "1"

SEAL_KEY_EVIDENCE_REMEDIATION_PLAN: Final[str] = "evidence_remediation_plan_sha256"

FILENAME_EVIDENCE_REMEDIATION_PLAN: Final[str] = "v15_evidence_remediation_plan.json"
REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN: Final[str] = "v15_evidence_remediation_plan_report.json"
FILENAME_OPERATOR_RUNBOOK_MD: Final[str] = "v15_operator_evidence_acquisition_runbook.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_WITH_M13_BINDING: Final[str] = "m13_bound"

PROFILE_ID_EVIDENCE_REMEDIATION_PLAN: Final[str] = (
    "starlab.v15.evidence_remediation_plan_profile.v1"
)

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_REMEDIATION_PLAN_ID: Final[str] = "v15_m14:fixture_ci:deterministic"

# Post-M13 status vocabulary
STATUS_EVIDENCE_GAP_INVENTORY_ONLY: Final[str] = "evidence_gap_inventory_only"
STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED: Final[str] = "operator_evidence_not_collected"
STATUS_REMEDIATION_PLAN_READY: Final[str] = "remediation_plan_ready"

# Gap ids (10)
GAP_01_LONG_GPU_RUN_RECEIPT: Final[str] = "GAP-01-long-gpu-run-receipt"
GAP_02_CHECKPOINT_LINEAGE: Final[str] = "GAP-02-checkpoint-lineage"
GAP_03_PROMOTED_CHECKPOINT: Final[str] = "GAP-03-promoted-checkpoint"
GAP_04_TRAINING_SCALE_PROVENANCE: Final[str] = "GAP-04-training-scale-provenance"
GAP_05_STRONG_AGENT_BENCHMARK: Final[str] = "GAP-05-strong-agent-benchmark"
GAP_06_REPLAY_NATIVE_XAI_PACK: Final[str] = "GAP-06-replay-native-xai-pack"
GAP_07_HUMAN_BENCHMARK_EVIDENCE: Final[str] = "GAP-07-human-benchmark-evidence"
GAP_08_SHOWCASE_RELEASE_EVIDENCE: Final[str] = "GAP-08-showcase-release-evidence"
GAP_09_V2_READINESS_EVIDENCE: Final[str] = "GAP-09-v2-readiness-evidence"
GAP_10_RIGHTS_AND_ASSET_CLEARANCE: Final[str] = "GAP-10-rights-and-asset-clearance"

ALL_GAP_IDS: Final[tuple[str, ...]] = (
    GAP_01_LONG_GPU_RUN_RECEIPT,
    GAP_02_CHECKPOINT_LINEAGE,
    GAP_03_PROMOTED_CHECKPOINT,
    GAP_04_TRAINING_SCALE_PROVENANCE,
    GAP_05_STRONG_AGENT_BENCHMARK,
    GAP_06_REPLAY_NATIVE_XAI_PACK,
    GAP_07_HUMAN_BENCHMARK_EVIDENCE,
    GAP_08_SHOWCASE_RELEASE_EVIDENCE,
    GAP_09_V2_READINESS_EVIDENCE,
    GAP_10_RIGHTS_AND_ASSET_CLEARANCE,
)

# Remediation gates E0–E13
E0_M13_DECISION_CONTEXT: Final[str] = "E0_m13_decision_context"
E1_EVIDENCE_GAPS_ENUMERATED: Final[str] = "E1_evidence_gaps_enumerated"
E2_OPERATOR_PRIVATE_PATHS: Final[str] = "E2_operator_private_acquisition_paths"
E3_LONG_GPU_EVIDENCE_REQ: Final[str] = "E3_long_gpu_evidence_requirements"
E4_CHECKPOINT_LINEAGE_REQ: Final[str] = "E4_checkpoint_lineage_requirements"
E5_PROMOTION_EVAL_REQ: Final[str] = "E5_promotion_evaluation_evidence_requirements"
E6_XAI_EVIDENCE_REQ: Final[str] = "E6_xai_evidence_requirements"
E7_HUMAN_BENCHMARK_REQ: Final[str] = "E7_human_benchmark_evidence_requirements"
E8_RIGHTS_REGISTER_TOUCHPOINTS: Final[str] = "E8_rights_asset_register_touchpoints"
E9_PUBLIC_PRIVATE_BOUNDARY: Final[str] = "E9_public_private_boundary_preserved"
E10_PROPOSED_ROADMAP: Final[str] = "E10_m15_m21_roadmap_recorded"
E11_V2_REMAINS_UNAUTHORIZED: Final[str] = "E11_v2_remains_unauthorized"
E12_NO_FABRICATED_EVIDENCE: Final[str] = "E12_no_operator_evidence_fabricated"
E13_DOCS_GOVERNANCE_ALIGNED: Final[str] = "E13_docs_governance_tests_aligned"

ALL_REMEDIATION_GATE_IDS: Final[tuple[str, ...]] = (
    E0_M13_DECISION_CONTEXT,
    E1_EVIDENCE_GAPS_ENUMERATED,
    E2_OPERATOR_PRIVATE_PATHS,
    E3_LONG_GPU_EVIDENCE_REQ,
    E4_CHECKPOINT_LINEAGE_REQ,
    E5_PROMOTION_EVAL_REQ,
    E6_XAI_EVIDENCE_REQ,
    E7_HUMAN_BENCHMARK_REQ,
    E8_RIGHTS_REGISTER_TOUCHPOINTS,
    E9_PUBLIC_PRIVATE_BOUNDARY,
    E10_PROPOSED_ROADMAP,
    E11_V2_REMAINS_UNAUTHORIZED,
    E12_NO_FABRICATED_EVIDENCE,
    E13_DOCS_GOVERNANCE_ALIGNED,
)

GATE_STATUS_PASS: Final[str] = "pass"
GATE_STATUS_WARNING: Final[str] = "warning"
GATE_STATUS_FAIL: Final[str] = "fail"
GATE_STATUS_BLOCKED: Final[str] = "blocked"
GATE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"

ALL_GATE_STATUSES: Final[tuple[str, ...]] = (
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    GATE_STATUS_FAIL,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_NOT_APPLICABLE,
)

NON_CLAIMS_V15_M14: Final[str] = (
    "V15-M14 does not train a checkpoint; does not promote a checkpoint; does not execute a long "
    "GPU campaign; does not run a short GPU shakedown; does not run benchmarks; does not run live "
    "SC2; does not run XAI inference; does not run human-panel matches; does not release a "
    "showcase agent; does not authorize v2; does not collect operator evidence; "
    "and does not commit "
    "model weights, checkpoint blobs, raw replays, videos, saliency tensors, participant records, "
    "private operator notes, or private paths. Proposed follow-on milestones V15-M15–V15-M21 are "
    "planning labels only until separately approved and implemented."
)

FORBIDDEN_RUNBOOK_SUBSTRINGS: Final[tuple[str, ...]] = (
    "v2 is authorized",
    "the showcase agent is released",
    "the checkpoint is promoted",
    "the campaign completed",
    "the agent is strong",
    "the agent beats most humans",
)


def default_m14_authorization_flags() -> dict[str, bool]:
    return {
        "operator_execution_performed": False,
        "long_gpu_campaign_completed": False,
        "checkpoint_promoted": False,
        "strong_agent_benchmark_executed": False,
        "real_xai_demonstration_executed": False,
        "human_panel_execution_performed": False,
        "showcase_agent_release_authorized": False,
        "v2_authorized": False,
    }


PROPOSED_M15_M21: Final[tuple[tuple[str, str, str], ...]] = (
    ("V15-M15", "Operator Evidence Collection Preflight", "proposed / not started"),
    ("V15-M16", "Short GPU / Environment Evidence Collection", "proposed / not started"),
    ("V15-M17", "Long GPU Campaign Evidence Collection", "proposed / not started"),
    ("V15-M18", "Candidate Checkpoint Evaluation Evidence Collection", "proposed / not started"),
    ("V15-M19", "XAI Evidence Collection and Validation", "proposed / not started"),
    ("V15-M20", "Human / Bounded Human Benchmark Evidence Collection", "proposed / not started"),
    ("V15-M21", "v2 Reconsideration Decision", "proposed / not started"),
)

__all__ = [
    "ALL_GAP_IDS",
    "ALL_GATE_STATUSES",
    "ALL_REMEDIATION_GATE_IDS",
    "CONTRACT_ID_EVIDENCE_REMEDIATION_PLAN",
    "CONTRACT_VERSION",
    "E0_M13_DECISION_CONTEXT",
    "E1_EVIDENCE_GAPS_ENUMERATED",
    "E10_PROPOSED_ROADMAP",
    "E11_V2_REMAINS_UNAUTHORIZED",
    "E12_NO_FABRICATED_EVIDENCE",
    "E13_DOCS_GOVERNANCE_ALIGNED",
    "E2_OPERATOR_PRIVATE_PATHS",
    "E3_LONG_GPU_EVIDENCE_REQ",
    "E4_CHECKPOINT_LINEAGE_REQ",
    "E5_PROMOTION_EVAL_REQ",
    "E6_XAI_EVIDENCE_REQ",
    "E7_HUMAN_BENCHMARK_REQ",
    "E8_RIGHTS_REGISTER_TOUCHPOINTS",
    "E9_PUBLIC_PRIVATE_BOUNDARY",
    "EMITTER_MODULE_EVIDENCE_REMEDIATION",
    "FILENAME_EVIDENCE_REMEDIATION_PLAN",
    "FILENAME_OPERATOR_RUNBOOK_MD",
    "FIXTURE_REMEDIATION_PLAN_ID",
    "FORBIDDEN_RUNBOOK_SUBSTRINGS",
    "GAP_01_LONG_GPU_RUN_RECEIPT",
    "GAP_02_CHECKPOINT_LINEAGE",
    "GAP_03_PROMOTED_CHECKPOINT",
    "GAP_04_TRAINING_SCALE_PROVENANCE",
    "GAP_05_STRONG_AGENT_BENCHMARK",
    "GAP_06_REPLAY_NATIVE_XAI_PACK",
    "GAP_07_HUMAN_BENCHMARK_EVIDENCE",
    "GAP_08_SHOWCASE_RELEASE_EVIDENCE",
    "GAP_09_V2_READINESS_EVIDENCE",
    "GAP_10_RIGHTS_AND_ASSET_CLEARANCE",
    "GATE_STATUS_BLOCKED",
    "GATE_STATUS_FAIL",
    "GATE_STATUS_NOT_APPLICABLE",
    "GATE_STATUS_NOT_EVALUATED",
    "GATE_STATUS_PASS",
    "GATE_STATUS_WARNING",
    "MILESTONE_ID_V15_M14",
    "NON_CLAIMS_V15_M14",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_ID_EVIDENCE_REMEDIATION_PLAN",
    "PROFILE_WITH_M13_BINDING",
    "PROPOSED_M15_M21",
    "REPORT_FILENAME_EVIDENCE_REMEDIATION_PLAN",
    "REPORT_VERSION_EVIDENCE_REMEDIATION",
    "SEAL_KEY_EVIDENCE_REMEDIATION_PLAN",
    "STATUS_EVIDENCE_GAP_INVENTORY_ONLY",
    "STATUS_OPERATOR_EVIDENCE_NOT_COLLECTED",
    "STATUS_REMEDIATION_PLAN_READY",
    "default_m14_authorization_flags",
]
