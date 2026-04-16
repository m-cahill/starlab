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

# --- M58 hardening / cost guardrails (static JSON) ---
LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_CONTRACT_ID: Final[str] = (
    "starlab.live_sc2_in_ci_hardening_guardrails.v1"
)
LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_hardening_guardrails.v1"
)
LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_hardening_guardrails_report.v1"
)

LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_FILENAME: Final[str] = (
    "live_sc2_in_ci_hardening_guardrails.json"
)
LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_FILENAME: Final[str] = (
    "live_sc2_in_ci_hardening_guardrails_report.json"
)

LIVE_SC2_IN_CI_HARDENING_RUNTIME_DOC_REL_PATH: Final[str] = (
    "docs/runtime/live_sc2_in_ci_hardening_cost_guardrails_v1.md"
)

M58_FLEET_REQUIRED_LABEL_SUBSTRINGS: Final[tuple[str, ...]] = ("self-hosted", "starlab-sc2")
M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1: Final[str] = (
    "starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1"
)
M58_MAX_ARTIFACT_RETENTION_DAYS: Final[int] = 7
M58_MAX_TIMEOUT_MINUTES: Final[int] = 30

# --- M58 preflight receipt ---
LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID: Final[str] = (
    "starlab.live_sc2_in_ci_preflight_receipt.v1"
)
LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_preflight_receipt.v1"
)
LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_SCHEMA_VERSION: Final[str] = (
    "starlab.live_sc2_in_ci_preflight_receipt_report.v1"
)

LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_FILENAME: Final[str] = "live_sc2_in_ci_preflight_receipt.json"
LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_FILENAME: Final[str] = (
    "live_sc2_in_ci_preflight_receipt_report.json"
)

M58PreflightStatus = Literal[
    "cleared",
    "failed_preconditions",
    "skipped_by_policy",
    "lock_denied",
]
