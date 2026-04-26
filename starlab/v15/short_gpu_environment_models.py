"""V15-M16 short GPU / environment evidence — constants and vocabulary."""

# ruff: noqa: E501

from __future__ import annotations

from typing import Final

CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE: Final[str] = (
    "starlab.v15.short_gpu_environment_evidence.v1"
)
MILESTONE_ID_V15_M16: Final[str] = "V15-M16"
EMITTER_MODULE_SHORT_GPU_ENVIRONMENT: Final[str] = (
    "starlab.v15.emit_v15_short_gpu_environment_evidence"
)

REPORT_VERSION_SHORT_GPU_ENV: Final[str] = "1"
SEAL_KEY_ARTIFACT: Final[str] = "artifact_sha256"

FILENAME_SHORT_GPU_ENV_EVIDENCE: Final[str] = "v15_short_gpu_environment_evidence.json"
REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE: Final[str] = (
    "v15_short_gpu_environment_evidence_report.json"
)
FILENAME_SHORT_GPU_ENV_CHECKLIST_MD: Final[str] = "v15_short_gpu_environment_checklist.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE: Final[str] = "operator_local_short_gpu_probe"

PLACEHOLDER_SHA256: Final[str] = "0" * 64

EVIDENCE_STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
EVIDENCE_STATUS_OPERATOR_DECLARED: Final[str] = "operator_declared_metadata"
EVIDENCE_STATUS_PROBE_BLOCKED: Final[str] = "operator_local_probe_blocked"
EVIDENCE_STATUS_PROBE_SUCCESS: Final[str] = "operator_local_probe_success"

SHORT_GPU_PROBE_NOT_RUN: Final[str] = "not_run"
SHORT_GPU_PROBE_SUCCESS: Final[str] = "success"
SHORT_GPU_PROBE_BLOCKED_CUDA: Final[str] = "blocked_cuda_unavailable"
SHORT_GPU_PROBE_BLOCKED_TORCH: Final[str] = "blocked_torch_unavailable"
SHORT_GPU_PROBE_FAILED: Final[str] = "probe_failed"

M17_BLOCKED_PENDING: Final[str] = "blocked_pending_operator_evidence"
M17_BLOCKED_CUDA: Final[str] = "blocked_cuda_unavailable"
M17_BLOCKED_M15: Final[str] = "blocked_missing_m15_preflight"
M17_BLOCKED_RIGHTS: Final[str] = "blocked_missing_rights_or_asset_register_review"
M17_READY_PLANNING: Final[str] = "ready_for_m17_planning"
M17_READY_PREFLIGHT: Final[str] = "ready_for_m17_operator_preflight_only"

G0_M15: Final[str] = "G0_m15_preflight_bound"
G1_REPO: Final[str] = "G1_repo_identity_recorded"
G2_PYTHON: Final[str] = "G2_python_environment_recorded"
G3_DEPS: Final[str] = "G3_dependency_lock_recorded"
G4_TORCH: Final[str] = "G4_torch_import_posture_recorded"
G5_CUDA: Final[str] = "G5_cuda_availability_recorded"
G6_GPU: Final[str] = "G6_gpu_identity_recorded"
G7_PROBE: Final[str] = "G7_short_probe_bounded"
G8_SC2: Final[str] = "G8_sc2_environment_declared"
G9_DISK: Final[str] = "G9_disk_output_root_declared"
G10_REDACT: Final[str] = "G10_private_path_redaction"
G11_REGISTER: Final[str] = "G11_register_touchpoints_declared"
G12_M17: Final[str] = "G12_m17_opening_recommendation"

ALL_READINESS_GATE_IDS: Final[tuple[str, ...]] = (
    G0_M15,
    G1_REPO,
    G2_PYTHON,
    G3_DEPS,
    G4_TORCH,
    G5_CUDA,
    G6_GPU,
    G7_PROBE,
    G8_SC2,
    G9_DISK,
    G10_REDACT,
    G11_REGISTER,
    G12_M17,
)

GATE_POSTURE_PASS: Final[str] = "pass"
GATE_POSTURE_PASS_FIXTURE: Final[str] = "pass_or_fixture"
GATE_POSTURE_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_POSTURE_PASS_OR_NA: Final[str] = "pass_or_not_applicable"

REGISTER_TOUCHPOINT_PATHS: Final[tuple[str, ...]] = (
    "docs/rights_register.md",
    "docs/training_asset_register.md",
    "docs/replay_corpus_register.md",
    "docs/model_weight_register.md",
    "docs/checkpoint_asset_register.md",
    "docs/xai_evidence_register.md",
    "docs/human_benchmark_register.md",
)

NON_CLAIMS_V15_M16: Final[str] = (
    "V15-M16 defines and may collect bounded short GPU / environment evidence only; it does not "
    "execute the long GPU campaign, does not train or promote a checkpoint, does not run live SC2, "
    "benchmark matches, XAI inference, or human-panel execution, does not release a showcase agent, "
    "does not authorize v2 or v2 recharter, and does not add claim-critical public register rows "
    "by default. Upstream M02/M07/M08 bindings are SHA-only metadata; M08 remains manifest/preflight "
    "tooling unless paired with valid operator receipts."
)

FORBIDDEN_CHECKLIST_SUBSTRINGS: Final[tuple[str, ...]] = (
    "long gpu campaign completed",
    "long_gpu_run_authorized: true",
    "v2 is authorized",
    "checkpoint is promoted for claim",
    "the agent beats most humans",
)

__all__ = [
    "ALL_READINESS_GATE_IDS",
    "CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE",
    "EMITTER_MODULE_SHORT_GPU_ENVIRONMENT",
    "EVIDENCE_STATUS_FIXTURE_ONLY",
    "EVIDENCE_STATUS_OPERATOR_DECLARED",
    "EVIDENCE_STATUS_PROBE_BLOCKED",
    "EVIDENCE_STATUS_PROBE_SUCCESS",
    "FILENAME_SHORT_GPU_ENV_CHECKLIST_MD",
    "FILENAME_SHORT_GPU_ENV_EVIDENCE",
    "FORBIDDEN_CHECKLIST_SUBSTRINGS",
    "G0_M15",
    "G1_REPO",
    "G10_REDACT",
    "G11_REGISTER",
    "G12_M17",
    "G2_PYTHON",
    "G3_DEPS",
    "G4_TORCH",
    "G5_CUDA",
    "G6_GPU",
    "G7_PROBE",
    "G8_SC2",
    "G9_DISK",
    "GATE_POSTURE_NOT_EVALUATED",
    "GATE_POSTURE_PASS",
    "GATE_POSTURE_PASS_FIXTURE",
    "GATE_POSTURE_PASS_OR_NA",
    "M17_BLOCKED_CUDA",
    "M17_BLOCKED_M15",
    "M17_BLOCKED_PENDING",
    "M17_BLOCKED_RIGHTS",
    "M17_READY_PLANNING",
    "M17_READY_PREFLIGHT",
    "MILESTONE_ID_V15_M16",
    "NON_CLAIMS_V15_M16",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_OPERATOR_DECLARED",
    "PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE",
    "REGISTER_TOUCHPOINT_PATHS",
    "REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE",
    "REPORT_VERSION_SHORT_GPU_ENV",
    "SEAL_KEY_ARTIFACT",
    "SHORT_GPU_PROBE_BLOCKED_CUDA",
    "SHORT_GPU_PROBE_BLOCKED_TORCH",
    "SHORT_GPU_PROBE_FAILED",
    "SHORT_GPU_PROBE_NOT_RUN",
    "SHORT_GPU_PROBE_SUCCESS",
]
