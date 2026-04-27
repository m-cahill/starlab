"""V15-M17 long GPU campaign evidence — constants and vocabulary."""

# ruff: noqa: E501

from __future__ import annotations

from typing import Final

CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE: Final[str] = "starlab.v15.long_gpu_campaign_evidence.v1"
MILESTONE_ID_V15_M17: Final[str] = "V15-M17"
EMITTER_MODULE_LONG_GPU_CAMPAIGN_EVIDENCE: Final[str] = (
    "starlab.v15.emit_v15_long_gpu_campaign_evidence"
)

REPORT_VERSION_LONG_GPU_CAMPAIGN_EVIDENCE: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE: Final[str] = "v15_long_gpu_campaign_evidence.json"
REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE: Final[str] = (
    "v15_long_gpu_campaign_evidence_report.json"
)
FILENAME_RUNBOOK_MD: Final[str] = "v15_long_gpu_campaign_runbook.md"
FILENAME_CLOSEOUT_CHECKLIST_MD: Final[str] = "v15_long_gpu_campaign_closeout_checklist.md"
FILENAME_CAMPAIGN_RECEIPT: Final[str] = "v15_long_gpu_campaign_receipt.json"
REPORT_FILENAME_CAMPAIGN_RECEIPT: Final[str] = "v15_long_gpu_campaign_receipt_report.json"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN: Final[str] = "operator_local_long_gpu_campaign"

PLACEHOLDER_SHA256: Final[str] = "0" * 64

CAMPAIGN_EVIDENCE_STATUS_FIXTURE: Final[str] = "fixture_only"
CAMPAIGN_EVIDENCE_STATUS_PREFLIGHT: Final[str] = "operator_preflight_ready"
CAMPAIGN_EVIDENCE_STATUS_DECLARED: Final[str] = "operator_declared_metadata"
CAMPAIGN_EVIDENCE_STATUS_LOCAL_GUARDS: Final[str] = "operator_local_guards_acknowledged"

M18_DEPENDENCY_NOTE: Final[str] = (
    "V15-M18 owns candidate checkpoint evaluation evidence; M17 does not promote checkpoints."
)

# Readiness gates L0–L15 (default_status = fixture/CI default posture)
L0: Final[str] = "L0_m16_environment_evidence_bound"
L1: Final[str] = "L1_m16_cuda_probe_success"
L2: Final[str] = "L2_private_output_root_declared"
L3: Final[str] = "L3_operator_guards_required"
L4: Final[str] = "L4_campaign_plan_declared"
L5: Final[str] = "L5_checkpoint_policy_declared"
L6: Final[str] = "L6_eval_policy_declared"
L7: Final[str] = "L7_dataset_rights_refs_declared"
L8: Final[str] = "L8_storage_retention_policy_declared"
L9: Final[str] = "L9_interruption_resume_policy_declared"
L10: Final[str] = "L10_no_public_private_leakage"
L11: Final[str] = "L11_no_claim_escalation"
L12: Final[str] = "L12_campaign_execution_status_recorded"
L13: Final[str] = "L13_receipt_requirements_declared"
L14: Final[str] = "L14_m18_dependency_declared"
L15: Final[str] = "L15_docs_tests_aligned"

ALL_READINESS_GATE_IDS: Final[tuple[str, ...]] = (
    L0,
    L1,
    L2,
    L3,
    L4,
    L5,
    L6,
    L7,
    L8,
    L9,
    L10,
    L11,
    L12,
    L13,
    L14,
    L15,
)

GATE_POSTURE_PASS: Final[str] = "pass"
GATE_POSTURE_PASS_FIXTURE: Final[str] = "pass_or_fixture"
GATE_POSTURE_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_POSTURE_PASS_OR_NA: Final[str] = "pass_or_not_applicable"
GATE_POSTURE_BLOCKED_OR_FIXTURE: Final[str] = "blocked_or_fixture"

REGISTER_TOUCHPOINT_PATHS: Final[tuple[str, ...]] = (
    "docs/rights_register.md",
    "docs/training_asset_register.md",
    "docs/replay_corpus_register.md",
    "docs/model_weight_register.md",
    "docs/checkpoint_asset_register.md",
    "docs/xai_evidence_register.md",
    "docs/human_benchmark_register.md",
)

NON_CLAIMS_V15_M17: Final[str] = (
    "V15-M17 defines and may record governed long GPU campaign evidence and preflight metadata only. "
    "It does not by itself clear assets for public redistribution, promote a checkpoint, authorize "
    "strong-agent claims, human-benchmark claims, release a showcase agent, or authorize v2. "
    "A completed M17 record is training-evidence and routing posture, not a capability claim. "
    "Real long GPU execution uses the M08 manifest + plan + starlab.v15.run_v15_long_gpu_campaign "
    "under separate operator control."
)

__all__ = [
    "ALL_READINESS_GATE_IDS",
    "CAMPAIGN_EVIDENCE_STATUS_DECLARED",
    "CAMPAIGN_EVIDENCE_STATUS_FIXTURE",
    "CAMPAIGN_EVIDENCE_STATUS_LOCAL_GUARDS",
    "CAMPAIGN_EVIDENCE_STATUS_PREFLIGHT",
    "CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE",
    "EMITTER_MODULE_LONG_GPU_CAMPAIGN_EVIDENCE",
    "FILENAME_CAMPAIGN_RECEIPT",
    "FILENAME_CLOSEOUT_CHECKLIST_MD",
    "FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE",
    "FILENAME_RUNBOOK_MD",
    "GATE_POSTURE_BLOCKED_OR_FIXTURE",
    "GATE_POSTURE_NOT_EVALUATED",
    "GATE_POSTURE_PASS",
    "GATE_POSTURE_PASS_FIXTURE",
    "GATE_POSTURE_PASS_OR_NA",
    "L0",
    "L1",
    "L10",
    "L11",
    "L12",
    "L13",
    "L14",
    "L15",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
    "L8",
    "L9",
    "M18_DEPENDENCY_NOTE",
    "MILESTONE_ID_V15_M17",
    "NON_CLAIMS_V15_M17",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_OPERATOR_DECLARED",
    "PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN",
    "PROFILE_OPERATOR_PREFLIGHT",
    "REGISTER_TOUCHPOINT_PATHS",
    "REPORT_FILENAME_CAMPAIGN_RECEIPT",
    "REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE",
    "REPORT_VERSION_LONG_GPU_CAMPAIGN_EVIDENCE",
    "SEAL_KEY_ARTIFACT",
]
