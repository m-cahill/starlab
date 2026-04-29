"""V15-M32 bounded candidate checkpoint evaluation execution (constants)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_M32_EVAL_EXEC: Final[str] = "starlab.v15.candidate_checkpoint_evaluation_execution.v1"
PROFILE_M32_BOUNDED: Final[str] = "starlab.v15.m32.bounded_candidate_evaluation_execution.v1"

MILESTONE_LABEL_M32: Final[str] = "V15-M32"

EMITTER_MODULE_M32: Final[str] = (
    "starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution"
)

FILENAME_EXEC_JSON: Final[str] = "v15_candidate_checkpoint_evaluation_execution.json"
REPORT_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_execution_report.json"
CHECKLIST_FILENAME: Final[str] = "v15_candidate_checkpoint_evaluation_execution_checklist.md"

SCHEMA_VERSION: Final[str] = "1.0"

STATUS_FIXTURE_COMPLETED: Final[str] = "candidate_evaluation_execution_fixture_completed"
STATUS_OPERATOR_LOCAL_METADATA_COMPLETED: Final[str] = (
    "candidate_evaluation_execution_operator_local_metadata_completed"
)
STATUS_REFUSED_BLOCKERS: Final[str] = "candidate_evaluation_execution_refused_with_blockers"

EXECUTION_SCOPE_FIXTURE_METADATA: Final[str] = "fixture_or_metadata_only"

EXECUTION_MODE_FIXTURE: Final[str] = "fixture"
EXECUTION_MODE_METADATA_ONLY: Final[str] = "metadata_only"

GATE_ARTIFACT_DIGEST_FIELD: Final[str] = "artifact_sha256"

SCORECARD_INHERITED_BOUND_IN_M31: Final[str] = "inherited_from_m31_bound_in_m31"
SCORECARD_INHERITED_OPTIONAL_NOT_SUPPLIED: Final[str] = "inherited_from_m31_optional_not_supplied"
SCORECARD_INHERITED_MISSING: Final[str] = "inherited_from_m31_missing"

NON_CLAIMS_M32: Final[tuple[str, ...]] = (
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
    "V15-M33_candidate_checkpoint_model_load_cuda_inference_probe"
)
