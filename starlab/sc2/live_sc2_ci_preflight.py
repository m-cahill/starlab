"""M58 preflight receipt: validates bounded M57/M44 posture before controlled runner."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.live_sc2_ci_controlled_runner import (
    assert_m43_candidate_or_raise,
    live_sc2_binary_available_for_bounded_run,
)
from starlab.sc2.live_sc2_ci_models import (
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID,
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_SCHEMA_VERSION,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
    M58_FLEET_REQUIRED_LABEL_SUBSTRINGS,
    M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
    M58_MAX_ARTIFACT_RETENTION_DAYS,
    M58_MAX_TIMEOUT_MINUTES,
    M58PreflightStatus,
)
from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.sc2.match_config import load_match_config


def _parse_labels(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def _labels_satisfy_fleet_policy(labels: list[str]) -> bool:
    joined = ",".join(labels)
    return all(sub in joined for sub in M58_FLEET_REQUIRED_LABEL_SUBSTRINGS)


def _validate_match_config_adapter(
    *,
    match_config: Path,
    runtime_mode: RuntimeMode,
) -> tuple[bool, str | None, str | None]:
    try:
        cfg = load_match_config(match_config)
    except (OSError, ValueError) as e:
        return False, None, str(e)
    adapter = cfg.adapter
    if runtime_mode == "fixture_stub_ci" and adapter != "fake":
        return False, adapter, "fixture_stub_ci requires match config adapter=fake"
    if runtime_mode == "local_live_sc2" and adapter != "burnysc2":
        return False, adapter, "local_live_sc2 requires match config adapter=burnysc2"
    return True, adapter, None


def build_preflight_receipt_report(*, receipt_obj: dict[str, Any]) -> dict[str, Any]:
    rhash = sha256_hex_of_canonical_json(receipt_obj)
    return {
        "emitter_module": "starlab.sc2.emit_live_sc2_in_ci_preflight",
        "receipt_artifact": "live_sc2_in_ci_preflight_receipt.json",
        "receipt_canonical_sha256": rhash,
        "report_artifact": "live_sc2_in_ci_preflight_receipt_report.json",
        "schema_version": LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_REPORT_SCHEMA_VERSION,
    }


def build_lock_denied_preflight_receipt(
    *,
    workflow_trigger: str,
    runner_labels_csv: str,
    lock_denial_message: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt: dict[str, Any] = {
        "artifact_retention_days_requested": 0,
        "contract_id": LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID,
        "explicit_live_confirmation": False,
        "failure_reasons": ["lock_denied"],
        "guardrail_profile_id": M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
        "lock_acquired": False,
        "lock_denial_message": lock_denial_message,
        "match_config_adapter_observed": None,
        "milestone": "M58",
        "non_claims": [
            "Preflight receipt does not prove global live-SC2-in-CI operational maturity.",
            "M57 runner profile remains the sole live execution profile.",
        ],
        "phase": "VII",
        "preflight_status": "lock_denied",
        "requested_runtime_mode": "fixture_stub_ci",
        "runner_labels_observed": sorted(_parse_labels(runner_labels_csv)),
        "runner_profile_id": M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
        "schema_version": LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_SCHEMA_VERSION,
        "sc2_probe_notes": [],
        "sc2_probe_status": "not_applicable",
        "timeout_minutes_requested": 0,
        "workflow_trigger_requested": workflow_trigger,
    }
    return receipt, build_preflight_receipt_report(receipt_obj=receipt)


def evaluate_live_sc2_in_ci_preflight(
    *,
    m43_run_dir: Path,
    weights_path: Path,
    match_config: Path,
    runtime_mode: RuntimeMode,
    workflow_trigger: str,
    runner_labels_csv: str,
    timeout_minutes: int,
    artifact_retention_days: int,
    live_sc2_confirmed: bool,
) -> tuple[bool, dict[str, Any], dict[str, Any], list[str]]:
    """Return (ok, receipt, report, failure_reasons)."""

    failure_reasons: list[str] = []
    match_adapter: str | None = None
    sc2_notes: list[str] = []
    probe_status: Literal["not_applicable", "passed", "failed"] = "not_applicable"

    if workflow_trigger != "workflow_dispatch":
        failure_reasons.append("workflow_trigger_not_workflow_dispatch")

    if timeout_minutes > M58_MAX_TIMEOUT_MINUTES:
        failure_reasons.append("timeout_minutes_exceeds_m58_guardrail_max")

    if artifact_retention_days > M58_MAX_ARTIFACT_RETENTION_DAYS:
        failure_reasons.append("artifact_retention_days_exceeds_m58_guardrail_max")

    labels = _parse_labels(runner_labels_csv)
    if not _labels_satisfy_fleet_policy(labels):
        failure_reasons.append("runner_labels_missing_required_fleet_allowlist_entries")

    if runtime_mode == "local_live_sc2" and not live_sc2_confirmed:
        failure_reasons.append("local_live_sc2_requires_explicit_confirmation")

    try:
        assert_m43_candidate_or_raise(hierarchical_training_run_dir=m43_run_dir)
    except ValueError as e:
        failure_reasons.append(f"m43_candidate_invalid:{e}")

    if not weights_path.is_file():
        failure_reasons.append("weights_path_missing")
    if not match_config.is_file():
        failure_reasons.append("match_config_missing")

    ok_adapt, adapter_observed, adapt_err = _validate_match_config_adapter(
        match_config=match_config,
        runtime_mode=runtime_mode,
    )
    match_adapter = adapter_observed
    if not ok_adapt:
        failure_reasons.append(f"match_config_adapter_inconsistent:{adapt_err}")

    if runtime_mode == "fixture_stub_ci":
        probe_status = "not_applicable"
        sc2_notes = ["sc2_probe_skipped_fixture_mode"]
    else:
        probe_ok, notes = live_sc2_binary_available_for_bounded_run()
        sc2_notes = list(notes)
        if probe_ok:
            probe_status = "passed"
        else:
            probe_status = "failed"
            failure_reasons.append("sc2_probe_failed_for_local_live_sc2")

    pre_status: M58PreflightStatus = "cleared" if not failure_reasons else "failed_preconditions"

    receipt: dict[str, Any] = {
        "artifact_retention_days_requested": artifact_retention_days,
        "contract_id": LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_CONTRACT_ID,
        "explicit_live_confirmation": live_sc2_confirmed,
        "failure_reasons": sorted(failure_reasons),
        "guardrail_profile_id": M58_GUARDRAIL_PROFILE_M57_SINGLE_VALIDATION_COST_GUARDRAILS_V1,
        "lock_acquired": True,
        "lock_denial_message": None,
        "match_config_adapter_observed": match_adapter,
        "milestone": "M58",
        "non_claims": [
            "Preflight receipt does not prove global live-SC2-in-CI operational maturity.",
            "M57 runner profile remains the sole live execution profile.",
        ],
        "phase": "VII",
        "preflight_status": pre_status,
        "requested_runtime_mode": runtime_mode,
        "runner_labels_observed": sorted(labels),
        "runner_profile_id": M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
        "schema_version": LIVE_SC2_IN_CI_PREFLIGHT_RECEIPT_SCHEMA_VERSION,
        "sc2_probe_notes": sorted(sc2_notes),
        "sc2_probe_status": probe_status,
        "timeout_minutes_requested": timeout_minutes,
        "workflow_trigger_requested": workflow_trigger,
    }
    report = build_preflight_receipt_report(receipt_obj=receipt)
    ok = pre_status == "cleared"
    return ok, receipt, report, failure_reasons
