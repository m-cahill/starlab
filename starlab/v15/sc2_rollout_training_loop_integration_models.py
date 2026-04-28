"""Contracts and enums for V15-M27 SC2 rollout ↔ training-loop integration artifacts."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.sc2_rollout_training_loop_integration.v1"
REPORT_CONTRACT_KIND: Final[str] = "starlab.v15.sc2_rollout_training_loop_integration_report.v1"

MILESTONE_LABEL: Final[str] = "V15-M27"

POLICY_ID_M27_MACRO_SMOKE: Final[str] = "v15_m27_nontrivial_macro_smoke_policy_v1"

STATUS_ARTIFACT_EMITTED: Final[str] = "rollout_artifact_emitted"
STATUS_NOT_CONNECTED: Final[str] = "not_connected"
STATUS_SUMMARY_TO_TRAINING: Final[str] = "rollout_summary_available_to_training"
STATUS_TRAINING_UPDATE: Final[str] = "training_update_executed"

OUTCOME_COMPLETED: Final[str] = "sc2_rollout_training_loop_integration_completed"
OUTCOME_ROLLOUT_ONLY: Final[str] = "sc2_rollout_nontrivial_but_training_update_not_connected"
OUTCOME_BLOCKED_POLICY: Final[str] = "sc2_rollout_blocked_by_harness_or_policy"
OUTCOME_BLOCKED_RUNTIME: Final[str] = "sc2_rollout_blocked_by_sc2_runtime"
OUTCOME_FIXTURE_ONLY: Final[str] = "sc2_rollout_fixture_only"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_LOCAL: Final[str] = "operator_local"

FILENAME_MAIN: Final[str] = "v15_sc2_rollout_training_loop_integration.json"
FILENAME_REPORT: Final[str] = "v15_sc2_rollout_training_loop_integration_report.json"
FILENAME_CHECKLIST: Final[str] = "v15_sc2_rollout_training_loop_integration_checklist.md"
