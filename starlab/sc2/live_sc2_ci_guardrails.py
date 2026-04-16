"""Deterministic M58 live SC2-in-CI hardening + cost guardrails JSON (profile bundle)."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_CONTRACT_ID,
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_HARDENING_RUNTIME_DOC_REL_PATH,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
    M58_FLEET_REQUIRED_LABEL_SUBSTRINGS,
    M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
    M58_MAX_ARTIFACT_RETENTION_DAYS,
    M58_MAX_TIMEOUT_MINUTES,
)


def non_claims_guardrails() -> list[str]:
    return [
        "M58 hardens the closed M57 live-SC2-in-CI surface; it does not prove live SC2 as a "
        "default merge gate or global CI norm.",
        "Exactly one guardrail profile exists; no additional live runner profiles are introduced.",
        "M59+ ladder/public evaluation and M52–M54 replay↔execution equivalence remain out of "
        "scope unless separately chartered.",
    ]


def _single_guardrail_profile_dict() -> dict[str, Any]:
    return {
        "artifact_retention_policy": {
            "artifact_retention_days_max": M58_MAX_ARTIFACT_RETENTION_DAYS,
        },
        "attempt_policy": {"max_execution_attempts_per_workflow_invocation": 1},
        "candidate_class_policy": {
            "allowed": "starlab.hierarchical_training_run.v1_with_explicit_weights",
        },
        "fleet_label_policy": {
            "preserve_repo_runner_allowlist": True,
            "required_runner_label_substrings": list(M58_FLEET_REQUIRED_LABEL_SUBSTRINGS),
        },
        "guardrail_profile_id": M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
        "live_confirmation_policy": {
            "local_live_sc2_requires_explicit_workflow_confirmation": True,
        },
        "lock_policy": {
            "github_actions_concurrency": True,
            "python_advisory_lockfile": True,
            "scope": "m58_preflight_output_dir",
        },
        "runtime_mode_policy": {
            "explicit_modes_only": ["fixture_stub_ci", "local_live_sc2"],
            "no_implicit_runtime_downgrade": True,
        },
        "runner_profile_id": M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
        "timeout_budget_minutes_max": M58_MAX_TIMEOUT_MINUTES,
        "workflow_trigger_policy": {"allowed_triggers": ["workflow_dispatch"]},
    }


def build_live_sc2_in_ci_hardening_guardrails_artifact() -> dict[str, Any]:
    profile = _single_guardrail_profile_dict()
    return {
        "contract_id": LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_CONTRACT_ID,
        "guardrail_profile_count": 1,
        "guardrail_profiles": [profile],
        "milestone": "M58",
        "non_claims": non_claims_guardrails(),
        "phase": "VII",
        "runtime_contract": LIVE_SC2_IN_CI_HARDENING_RUNTIME_DOC_REL_PATH,
        "schema_version": LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_SCHEMA_VERSION,
    }


def build_live_sc2_in_ci_hardening_guardrails_report(
    *, guardrails_obj: dict[str, Any]
) -> dict[str, Any]:
    ghash = sha256_hex_of_canonical_json(guardrails_obj)
    return {
        "emitter_module": "starlab.sc2.emit_live_sc2_in_ci_guardrails",
        "guardrails_artifact": "live_sc2_in_ci_hardening_guardrails.json",
        "guardrails_canonical_sha256": ghash,
        "report_artifact": "live_sc2_in_ci_hardening_guardrails_report.json",
        "schema_version": LIVE_SC2_IN_CI_HARDENING_GUARDRAILS_REPORT_SCHEMA_VERSION,
    }


def live_sc2_in_ci_hardening_guardrails_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    body = build_live_sc2_in_ci_hardening_guardrails_artifact()
    rep = build_live_sc2_in_ci_hardening_guardrails_report(guardrails_obj=body)
    return body, rep
