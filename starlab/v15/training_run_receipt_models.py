"""V15-M07 training run receipt constants (shakedown tooling; not long GPU campaign)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_TRAINING_RUN_RECEIPT: Final[str] = "starlab.v15.training_run_receipt.v1"
PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN: Final[str] = (
    "starlab.v15.training_smoke_short_gpu_shakedown.v1"
)

MILESTONE_ID_V15_M07: Final[str] = "V15-M07"
EMITTER_MODULE_TRAINING_RUN_RECEIPT: Final[str] = "starlab.v15.emit_v15_training_run_receipt"

SEAL_KEY_TRAINING_RUN_RECEIPT: Final[str] = "training_run_receipt_sha256"
FILENAME_TRAINING_RUN_RECEIPT: Final[str] = "v15_training_run_receipt.json"
REPORT_FILENAME_TRAINING_RUN_RECEIPT: Final[str] = "v15_training_run_receipt_report.json"
REPORT_VERSION_TRAINING_RUN: Final[str] = "1"
CONTRACT_VERSION: Final[str] = "1"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_SHORT_GPU: Final[str] = "operator_local_short_gpu"

RUN_CLASS_FIXTURE_SMOKE: Final[str] = "fixture_smoke"
RUN_CLASS_OPERATOR_DECLARED: Final[str] = "operator_declared"
RUN_CLASS_OPERATOR_LOCAL_SHAKEDOWN: Final[str] = "operator_local_short_gpu_shakedown"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_RUN_ID: Final[str] = "v15_m07:fixture_ci:deterministic"

# Declared receipt JSON: allowed top-level keys (strict parse for operator_declared)
RECEIPT_DECLARED_JSON_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "profile",
    "run_id",
    "run_class",
    "execution_scope",
    "repo_identity",
    "operator_notes",
    "authorization_flags",
    "training_config_binding",
    "dataset_binding",
    "rights_binding",
    "device_probe",
    "training_smoke",
    "checkpoint_write_receipt",
    "non_claims",
    "optional_bindings",
)

NON_CLAIMS_V15_M07: Final[tuple[str, ...]] = (
    "V15-M07 does not execute the V15-M08 long GPU campaign.",
    "V15-M07 does not authorize a long GPU run (long_gpu_run_authorized remains false).",
    "V15-M07 does not promote a checkpoint for production or benchmark claims.",
    "V15-M07 does not run strong-agent benchmark execution or authorize strong-agent claims.",
    "V15-M07 does not run human-panel matches or human-benchmark claim authorization.",
    "V15-M07 does not perform XAI inference or XAI review.",
    "V15-M07 does not open v2 or PX2-M04/PX2-M05.",
    "Fixture and synthetic shakedown output is not model-quality or claim-critical evidence.",
)
