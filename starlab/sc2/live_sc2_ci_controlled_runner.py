"""M57 controlled runner: wraps M44 `run_local_live_play_validation` with a receipt envelope."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.env_probe import run_probe
from starlab.sc2.live_sc2_ci_models import (
    ENV_M57_SKIP_LIVE_WHEN_PREREQS_MISSING,
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_CONTRACT_ID,
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_SCHEMA_VERSION,
    LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_SCHEMA_VERSION,
    M44_STUB_REPLAY_WARNING,
    M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
    M57ExecutionStatus,
    M57RunnerPosture,
)
from starlab.sc2.local_live_play_validation_harness import (
    resolve_paths,
    run_local_live_play_validation,
)
from starlab.sc2.local_live_play_validation_models import RuntimeMode


def _read_json_object(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = f"expected JSON object at {path}"
        raise ValueError(msg)
    return obj


def assert_m43_candidate_or_raise(*, hierarchical_training_run_dir: Path) -> dict[str, Any]:
    """Reject non-M43 candidates (e.g. M41 flat runs) before invoking M44."""

    hr_path = hierarchical_training_run_dir / HIERARCHICAL_TRAINING_RUN_FILENAME
    if not hr_path.is_file():
        msg = f"missing {HIERARCHICAL_TRAINING_RUN_FILENAME} under {hierarchical_training_run_dir}"
        raise ValueError(msg)
    training_run = _read_json_object(hr_path)
    tr_ver = training_run.get("training_run_version")
    if tr_ver != "starlab.hierarchical_training_run.v1":
        msg = (
            "M57 controlled runner supports only M43 hierarchical_training_run.v1 candidates; "
            f"got training_run_version={tr_ver!r}"
        )
        raise ValueError(msg)
    return training_run


def live_sc2_binary_available_for_bounded_run() -> tuple[bool, list[str]]:
    """Narrow prerequisite signal: SC2 binary path presence from M01 probe (no gameplay claim)."""

    probe = run_probe()
    if probe.present.get("binary"):
        return True, []
    return False, sorted(probe.notes)


def assert_no_local_live_stub_fallback_or_raise(*, validation_run: dict[str, Any]) -> None:
    """M57: never treat a stubbed live replay as successful bounded live execution."""

    warnings = validation_run.get("warnings")
    if not isinstance(warnings, list):
        return
    for w in warnings:
        if isinstance(w, str) and M44_STUB_REPLAY_WARNING in w:
            msg = (
                "M57 policy: local_live_sc2 run emitted deterministic stub replay "
                "(prerequisites for real replay not satisfied). Refusing to record as "
                "executed_live_bounded."
            )
            raise RuntimeError(msg)


def _resolved_posture(*, requested: M57RunnerPosture, workflow_trigger: str) -> M57RunnerPosture:
    if workflow_trigger == "workflow_dispatch":
        return "github_workflow_dispatch"
    return requested


def _non_claims_receipt() -> list[str]:
    return [
        "This receipt does not prove live SC2 in CI as a default merge gate.",
        "M58 owns cost guardrails and broader operational controls.",
        "Benchmark integrity and replay↔execution equivalence are separate Phase VII tracks.",
    ]


def build_controlled_runner_receipt_body(
    *,
    execution_status: M57ExecutionStatus,
    requested_runtime_mode: RuntimeMode,
    resolved_runtime_mode: RuntimeMode,
    requested_runner_posture: str,
    resolved_runner_posture: str,
    candidate_run_id: str,
    candidate_run_sha256: str,
    weights_sha256: str,
    workflow_trigger: str,
    runner_labels: list[str],
    m44_output_paths: dict[str, str],
    replay_binding_paths: list[str],
    m44_validation_run_sha256: str | None,
    prerequisite_notes: list[str] | None,
    skip_reason: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "candidate_run_id": candidate_run_id,
        "candidate_run_sha256": candidate_run_sha256,
        "contract_id": LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_CONTRACT_ID,
        "execution_status": execution_status,
        "m44_output_paths": {k: m44_output_paths[k] for k in sorted(m44_output_paths)},
        "m44_validation_run_sha256": m44_validation_run_sha256,
        "non_claims": _non_claims_receipt(),
        "prerequisite_notes": sorted(prerequisite_notes) if prerequisite_notes else [],
        "replay_binding_paths": sorted(replay_binding_paths),
        "requested_runner_posture": requested_runner_posture,
        "requested_runtime_mode": requested_runtime_mode,
        "resolved_runner_posture": resolved_runner_posture,
        "resolved_runtime_mode": resolved_runtime_mode,
        "runner_labels": sorted(runner_labels),
        "runner_profile_id": M57_RUNNER_PROFILE_M44_SINGLE_VALIDATION_V1,
        "schema_version": LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_SCHEMA_VERSION,
        "skip_reason": skip_reason,
        "weights_sha256": weights_sha256,
        "workflow_trigger": workflow_trigger,
    }
    return body


def build_controlled_runner_receipt_report(*, receipt_obj: dict[str, Any]) -> dict[str, Any]:
    rhash = sha256_hex_of_canonical_json(receipt_obj)
    return {
        "emitter_module": "starlab.sc2.run_live_sc2_in_ci_controlled_runner",
        "receipt_artifact": "live_sc2_in_ci_controlled_runner_receipt.json",
        "receipt_canonical_sha256": rhash,
        "report_artifact": "live_sc2_in_ci_controlled_runner_receipt_report.json",
        "schema_version": LIVE_SC2_IN_CI_CONTROLLED_RUNNER_RECEIPT_REPORT_SCHEMA_VERSION,
    }


@dataclass(frozen=True, slots=True)
class ControlledRunnerResult:
    receipt: dict[str, Any]
    report: dict[str, Any]
    m44_output_dir: Path | None


def _weights_path(
    *,
    hierarchical_training_run_dir: Path,
    weights: Path | None,
) -> Path:
    if weights is not None:
        return weights
    return hierarchical_training_run_dir / WEIGHTS_SUBDIR / WEIGHTS_ARTIFACT_BASENAME


def _skip_flag_from_env_or_arg(*, skip_cli: bool) -> bool:
    if skip_cli:
        return True
    env = os.environ.get(ENV_M57_SKIP_LIVE_WHEN_PREREQS_MISSING, "")
    return env.strip() in {"1", "true", "TRUE", "yes", "YES"}


def run_m57_controlled_runner(
    *,
    m43_run_dir: Path,
    match_config: Path,
    output_dir: Path,
    runtime_mode: RuntimeMode,
    weights: Path | None = None,
    requested_runner_posture: M57RunnerPosture = "cli_manual",
    workflow_trigger: str = "cli",
    runner_labels: list[str] | None = None,
    skip_live_when_prereqs_missing: bool = False,
) -> ControlledRunnerResult:
    """Run one bounded M44 validation (M57 profile); emit receipt + report."""

    labels = sorted(runner_labels) if runner_labels is not None else []
    training_run = assert_m43_candidate_or_raise(hierarchical_training_run_dir=m43_run_dir)
    training_run_sha256 = training_run.get("training_run_sha256")
    if not isinstance(training_run_sha256, str):
        msg = "hierarchical_training_run.json missing training_run_sha256"
        raise ValueError(msg)
    run_id = training_run.get("run_id")
    if not isinstance(run_id, str):
        msg = "hierarchical_training_run.json missing run_id"
        raise ValueError(msg)

    wpath = _weights_path(hierarchical_training_run_dir=m43_run_dir, weights=weights)
    if not wpath.is_file():
        msg = f"M43 joblib weights not found at {wpath}"
        raise ValueError(msg)
    weights_sha = sha256_hex_file(wpath)

    skip_live = _skip_flag_from_env_or_arg(skip_cli=skip_live_when_prereqs_missing)
    resolved_posture = _resolved_posture(
        requested=requested_runner_posture,
        workflow_trigger=workflow_trigger,
    )

    if runtime_mode == "local_live_sc2":
        ok, notes = live_sc2_binary_available_for_bounded_run()
        if not ok and skip_live:
            receipt = build_controlled_runner_receipt_body(
                candidate_run_id=run_id,
                candidate_run_sha256=training_run_sha256,
                execution_status="skipped_by_policy",
                m44_output_paths={},
                m44_validation_run_sha256=None,
                prerequisite_notes=notes,
                replay_binding_paths=[],
                requested_runner_posture=requested_runner_posture,
                requested_runtime_mode=runtime_mode,
                resolved_runner_posture=resolved_posture,
                resolved_runtime_mode=runtime_mode,
                runner_labels=labels,
                skip_reason="live_sc2_prerequisites_not_satisfied_skip_by_policy",
                weights_sha256=weights_sha,
                workflow_trigger=workflow_trigger,
            )
            report = build_controlled_runner_receipt_report(receipt_obj=receipt)
            return ControlledRunnerResult(receipt=receipt, report=report, m44_output_dir=None)
        if not ok:
            msg = (
                "M57 policy: local_live_sc2 requested but SC2 binary prerequisites are not "
                f"satisfied: {notes}"
            )
            raise RuntimeError(msg)

    m44_result = run_local_live_play_validation(
        hierarchical_training_run_dir=m43_run_dir,
        match_config_path=match_config,
        output_dir=output_dir,
        runtime_mode=runtime_mode,
        weights_path=weights,
    )
    validation_run = m44_result.validation_run
    if runtime_mode == "local_live_sc2":
        assert_no_local_live_stub_fallback_or_raise(validation_run=validation_run)

    vsha = sha256_hex_of_canonical_json(validation_run)
    paths = resolve_paths(output_dir)
    m44_map = {
        "lineage_seed": str(paths.lineage_seed.resolve()),
        "local_live_play_validation_run": str(paths.run_json.resolve()),
        "match_config": str(paths.match_config.resolve()),
        "match_proof": str(paths.match_proof.resolve()),
        "replay_binding": str(paths.replay_binding.resolve()),
        "validation_replay": str(paths.validation_replay.resolve()),
    }
    replay_refs = [str(paths.replay_binding.resolve())]

    if runtime_mode == "fixture_stub_ci":
        status: M57ExecutionStatus = "executed_fixture_stub"
    else:
        status = "executed_live_bounded"

    receipt = build_controlled_runner_receipt_body(
        candidate_run_id=run_id,
        candidate_run_sha256=training_run_sha256,
        execution_status=status,
        m44_output_paths=m44_map,
        m44_validation_run_sha256=vsha,
        prerequisite_notes=None,
        replay_binding_paths=replay_refs,
        requested_runner_posture=requested_runner_posture,
        requested_runtime_mode=runtime_mode,
        resolved_runner_posture=resolved_posture,
        resolved_runtime_mode=runtime_mode,
        runner_labels=labels,
        skip_reason=None,
        weights_sha256=weights_sha,
        workflow_trigger=workflow_trigger,
    )
    report = build_controlled_runner_receipt_report(receipt_obj=receipt)
    return ControlledRunnerResult(receipt=receipt, report=report, m44_output_dir=output_dir)
