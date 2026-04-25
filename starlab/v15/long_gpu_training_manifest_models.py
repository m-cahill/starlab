"""V15-M08 long GPU training manifest constants.

Governance + preflight only; not claim authorization.
"""

from __future__ import annotations

from typing import Final

CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST: Final[str] = "starlab.v15.long_gpu_training_manifest.v1"
CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT: Final[str] = "starlab.v15.long_gpu_campaign_receipt.v1"
PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION: Final[str] = "starlab.v15.long_gpu_campaign_execution.v1"

MILESTONE_ID_V15_M08: Final[str] = "V15-M08"
EMITTER_MODULE_LONG_GPU_MANIFEST: Final[str] = "starlab.v15.emit_v15_long_gpu_training_manifest"
RUNNER_MODULE_LONG_GPU_CAMPAIGN: Final[str] = "starlab.v15.run_v15_long_gpu_campaign"

SEAL_KEY_MANIFEST: Final[str] = "long_gpu_training_manifest_sha256"
SEAL_KEY_CAMPAIGN_RECEIPT: Final[str] = "v15_long_gpu_campaign_receipt_sha256"

FILENAME_LONG_GPU_TRAINING_MANIFEST: Final[str] = "v15_long_gpu_training_manifest.json"
REPORT_FILENAME_LONG_GPU_TRAINING_MANIFEST: Final[str] = (
    "v15_long_gpu_training_manifest_report.json"
)
FILENAME_CAMPAIGN_RECEIPT: Final[str] = "v15_long_gpu_campaign_receipt.json"
REPORT_FILENAME_CAMPAIGN_RECEIPT: Final[str] = "v15_long_gpu_campaign_receipt_report.json"

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_MANIFEST: Final[str] = "1"
REPORT_VERSION_RECEIPT: Final[str] = "1"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_CAMPAIGN_ID: Final[str] = "v15_m08:fixture_ci:deterministic"

GATE_PASS: Final[str] = "pass"
GATE_WARNING: Final[str] = "warning"
GATE_BLOCKED: Final[str] = "blocked"
GATE_NOT_EVALUATED: Final[str] = "not_evaluated"

GATE_FIELD_NAMES: Final[tuple[str, ...]] = (
    "gate_a_governance_status",
    "gate_b_environment_status",
    "gate_c_data_status",
    "gate_d_checkpoint_status",
    "gate_e_evaluation_status",
    "gate_f_xai_status",
    "gate_g_operator_status",
)

CAMPAIGN_PLAN_REQUIRED_KEYS: Final[tuple[str, ...]] = (
    "campaign_id",
    "campaign_title",
    "operator",
    "milestone",
    "target_machine",
    "target_gpu",
    "training_pipeline_id",
    "training_profile_id",
    "campaign_goal",
    "target_duration_hours",
    "minimum_duration_hours",
    "max_wall_clock_hours",
    "max_training_steps",
    "checkpoint_interval_steps",
    "evaluation_interval_steps",
    "xai_sample_interval_steps",
    "dataset_manifest_ref",
    "training_config_ref",
    "initial_checkpoint_ref",
    "output_root_policy",
    "stop_policy",
    "resume_policy",
    "rollback_policy",
    "failure_quarantine_policy",
    "artifact_retention_policy",
    "public_private_boundary",
    "non_claims",
    "m49_full_local_training_campaign_contract_path",
)

MANIFEST_OPERATOR_DECLARED_TOP_LEVEL_KEYS: Final[frozenset[str]] = frozenset(
    {
        "contract_id",
        "contract_version",
        "profile_id",
        "profile",
        "milestone",
        "created_by",
        "campaign_id",
        "campaign_status",
        "campaign_authorization",
        "campaign_plan_sha256",
        "repo_identity",
        "operator_identity",
        "public_private_boundary",
        "environment_lock_binding",
        "m07_shakedown_binding",
        "training_config_binding",
        "dataset_manifest_binding",
        "rights_manifest_binding",
        "checkpoint_lineage_binding",
        "strong_agent_protocol_binding",
        "xai_contract_binding",
        "human_panel_protocol_binding",
        "runbook_binding",
        "storage_policy",
        "checkpoint_policy",
        "evaluation_policy",
        "xai_sample_policy",
        "stop_resume_policy",
        "failure_quarantine_policy",
        "provenance_gaps",
        "gate_statuses",
        "non_claims",
        "optional_bindings",
        "redaction_policy",
        "authorization_flags",
        "m49_execution_binding",
        "check_results",
        SEAL_KEY_MANIFEST,
    }
)

CAMPAIGN_STATUS_FIXTURE: Final[str] = "implementation_ready_preflight_blocked"
CAMPAIGN_STATUS_WAITING: Final[str] = "implementation_ready_waiting_for_operator_run"

NON_CLAIMS_V15_M08: Final[tuple[str, ...]] = (
    "V15-M08 may record operator-local long GPU campaign evidence only under explicit "
    "authorization and honest preflight gates.",
    "V15-M08 does not promote a checkpoint (V15-M09).",
    "V15-M08 does not execute or pass the strong-agent benchmark.",
    "V15-M08 does not run human-panel matches or authorize human-benchmark claims.",
    "V15-M08 does not perform XAI review or prove explanation faithfulness.",
    "V15-M08 does not authorize v2 or open PX2-M04/PX2-M05.",
    "V15-M08 does not prove ladder dominance, global SC2 solution, or multi-race generality.",
    "Fixture and preflight-only output is not a completed long GPU campaign.",
)


def default_m08_authorization_flags() -> dict[str, bool]:
    return {
        "long_gpu_run_authorized": False,
        "long_gpu_campaign_execution_performed": False,
        "long_gpu_campaign_completed": False,
        "checkpoint_promotion_performed": False,
        "benchmark_execution_performed": False,
        "strong_agent_claim_authorized": False,
        "human_panel_execution_performed": False,
        "human_benchmark_claim_authorized": False,
        "xai_review_performed": False,
        "v2_authorized": False,
    }
