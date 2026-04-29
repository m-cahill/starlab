"""V15-M30 SC2-backed candidate checkpoint evaluation package (constants)."""

from __future__ import annotations

from typing import Final

from starlab.v15.candidate_checkpoint_evaluation_package_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
)

PACKAGE_PROFILE_ID_M30: Final[str] = (
    "starlab.v15.m30.sc2_backed_candidate_checkpoint_evaluation_package.v1"
)
MILESTONE_LABEL_V30: Final[str] = "V15-M30"
EMITTER_MODULE_M30: Final[str] = (
    "starlab.v15.emit_v15_m30_sc2_backed_candidate_checkpoint_evaluation_package"
)

FILENAME_PACKAGE = "v15_candidate_checkpoint_evaluation_package.json"
REPORT_FILENAME = "v15_candidate_checkpoint_evaluation_package_report.json"
CHECKLIST_FILENAME = "v15_candidate_checkpoint_evaluation_package_checklist.md"
SCHEMA_VERSION: Final[str] = "1.0"

NON_CLAIMS_M30: Final[tuple[str, ...]] = (
    "not_strength_evaluation",
    "not_benchmark_pass",
    "not_checkpoint_promotion",
    "not_xai_execution",
    "not_human_panel_execution",
    "not_showcase_release",
    "not_v2_authorization",
    "not_t2_or_t3",
)

STATUS_READY: Final[str] = "ready_for_future_checkpoint_evaluation"
STATUS_BLOCKED: Final[str] = "blocked"

SCORECARD_BOUND: Final[str] = "bound"
SCORECARD_OPTIONAL_NOT_SUPPLIED: Final[str] = "optional_not_supplied"

# Re-export contract family for callers
CONTRACT_ID_PACKAGE_V1 = CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE
