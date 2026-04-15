"""Constants and types for M57 live SC2-in-CI charter & controlled runner receipts."""

from __future__ import annotations

from typing import Final, Literal

# --- Charter (governance JSON) ---
LIVE_SC2_IN_CI_CHARTER_CONTRACT_ID: Final[str] = "starlab.live_sc2_in_ci_charter.v1"
LIVE_SC2_IN_CI_CHARTER_SCHEMA_VERSION: Final[str] = "starlab.live_sc2_in_ci_charter.v1"
LIVE_SC2_IN_CI_CHARTER_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_charter_report.v1"
)

LIVE_SC2_IN_CI_CHARTER_FILENAME: Final[str] = "live_sc2_in_ci_charter.json"
LIVE_SC2_IN_CI_CHARTER_REPORT_FILENAME: Final[str] = "live_sc2_in_ci_charter_report.json"

LIVE_SC2_IN_CI_RUNTIME_DOC_REL_PATH: Final[str] = (
    "docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md"
)

# --- Controlled runner receipt ---
LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_CONTRACT_ID: Final[str] = (
    "starlab.live_sc2_in_ci_controlled_runner_receipt.v1"
)
LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_controlled_runner_receipt.v1"
)
LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_controlled_runner_receipt_report.v1"
)

LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_FILENAME: Final[str] = (
    "live_sc2_in_ci_controlled_runner_receipt.json"
)
LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_FILENAME: Final[str] = (
    "live_sc2_in_ci_controlled_runner_receipt_report.json"
)

# Exactly one bounded profile in M57.
M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1: Final[str] = (
    "starlab.m57.runner_profile.m44_single_validation_v1"
)

M57RunnerPosture = Literal["cli_manual", "github_workflow_dispatch"]

M57ExecutionStatus = Literal[
    "prepared",
    "executed_fixture_stub",
    "executed_live_bounded",
    "skipped_by_policy",
    "failed_preconditions",
]

M44_STUB_REPLAY_WARNING: Final[str] = (
    "local_live_sc2: real replay not copied; emitted deterministic stub replay instead"
)

ENV_M57_SKIP_LIVE_WHEN_PREREQS_MISSING: Final[str] = "STARLAB_M57_SKIP_LIVE_WHEN_PREREQS_MISSING"
