"""V15-M31 candidate checkpoint evaluation harness dry-run gate (constants)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M31_GATE: Final[str] = "starlab.v15.candidate_checkpoint_evaluation_harness_gate.v1"
PROFILE_M31_DRY_RUN: Final[str] = "starlab.v15.m31.evaluation_harness_dry_run_gate.v1"

MILESTONE_LABEL_M31: Final[str] = "V15-M31"

EMITTER_MODULE_M31: Final[str] = (
    "starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate"
)

FILENAME_GATE_JSON: Final[str] = "v15_candidate_checkpoint_evaluation_harness_gate.json"
REPORT_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_harness_gate_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_harness_gate_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"

STATUS_READY: Final[str] = "evaluation_harness_dry_run_ready"
STATUS_BLOCKED: Final[str] = "evaluation_harness_refused_with_blockers"

SCORECARD_OPTIONAL_NOT_SUPPLIED: Final[str] = "optional_not_supplied"
SCORECARD_BOUND_IN_M31: Final[str] = "bound_in_m31"

GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

NON_CLAIMS_M31: Final[tuple[str, ...]] = (
    "not_strength_evaluation",
    "not_benchmark_pass",
    "not_checkpoint_promotion",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_or_t3",
)

RECOMMENDED_NEXT_DEFAULT: Final[str] = (
    "V15-M32_or_M31_followup_candidate_checkpoint_evaluation_execution"
)
