"""M50: governed campaign execution artifacts under M49 campaign root."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.industrial_hidden_rollout_models import (
    CAMPAIGN_EXECUTION_MANIFEST_VERSION,
    CAMPAIGN_HEARTBEAT_VERSION,
    CAMPAIGN_RESUME_STATE_VERSION,
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_REPORT_VERSION,
    IndustrialHiddenRolloutCapabilityV1,
)

HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME: Final[str] = "hidden_rollout_campaign_run.json"
HIDDEN_ROLLOUT_CAMPAIGN_RUN_REPORT_FILENAME: Final[str] = "hidden_rollout_campaign_run_report.json"
CAMPAIGN_EXECUTION_MANIFEST_FILENAME: Final[str] = "campaign_execution_manifest.json"
CAMPAIGN_HEARTBEAT_FILENAME: Final[str] = "campaign_heartbeat.json"
CAMPAIGN_RESUME_STATE_FILENAME: Final[str] = "campaign_resume_state.json"
STOP_REQUEST_FILENAME: Final[str] = "STOP_REQUEST"


def campaign_runs_dir(campaign_root: Path) -> Path:
    return campaign_root / "campaign_runs"


def execution_dir(campaign_root: Path, execution_id: str) -> Path:
    return campaign_runs_dir(campaign_root) / execution_id


def quarantine_dir_for_failed_execution(campaign_root: Path, execution_id: str) -> Path:
    """Renamed partial tree suggestion: ``campaign_runs/<execution_id>_quarantine_<unix>``."""

    return campaign_runs_dir(campaign_root) / f"{execution_id}_quarantine_{int(time.time())}"


def write_initial_heartbeat(
    *,
    execution_dir: Path,
    execution_id: str,
    campaign_sha256: str,
) -> Path:
    path = execution_dir / CAMPAIGN_HEARTBEAT_FILENAME
    body: dict[str, Any] = {
        "campaign_sha256": campaign_sha256,
        "execution_id": execution_id,
        "heartbeat_version": CAMPAIGN_HEARTBEAT_VERSION,
        "last_alive_at_unix_utc": time.time(),
        "last_episode_completed_at_unix_utc": None,
        "last_episode_completed_index": None,
        "last_phase": None,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(body), encoding="utf-8")
    return path


def update_heartbeat(
    *,
    heartbeat_path: Path,
    last_phase: str | None,
    episode_index: int | None,
) -> None:
    raw = heartbeat_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("heartbeat corrupt")
    now = time.time()
    data["last_alive_at_unix_utc"] = now
    if last_phase is not None:
        data["last_phase"] = last_phase
    if episode_index is not None:
        data["last_episode_completed_index"] = episode_index
        data["last_episode_completed_at_unix_utc"] = now
    heartbeat_path.write_text(canonical_json_dumps(data), encoding="utf-8")


def write_resume_state(
    *,
    execution_dir: Path,
    execution_id: str,
    campaign_sha256: str,
    status: str,
    detail: str,
    phase: str | None = None,
) -> Path:
    path = execution_dir / CAMPAIGN_RESUME_STATE_FILENAME
    body: dict[str, Any] = {
        "campaign_sha256": campaign_sha256,
        "detail": detail,
        "execution_id": execution_id,
        "phase": phase,
        "resume_state_version": CAMPAIGN_RESUME_STATE_VERSION,
        "status": status,
        "updated_at_unix_utc": time.time(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(body), encoding="utf-8")
    return path


def write_execution_manifest(
    *,
    execution_dir: Path,
    execution_id: str,
    campaign_sha256: str,
    campaign_id: str,
    capability: IndustrialHiddenRolloutCapabilityV1,
    phases_planned: list[str],
) -> Path:
    path = execution_dir / CAMPAIGN_EXECUTION_MANIFEST_FILENAME
    body: dict[str, Any] = {
        "campaign_execution_manifest_version": CAMPAIGN_EXECUTION_MANIFEST_VERSION,
        "campaign_id": campaign_id,
        "campaign_sha256": campaign_sha256,
        "execution_id": execution_id,
        "hidden_rollout_capability": dict(capability),
        "phases_planned": phases_planned,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(body), encoding="utf-8")
    return path


def seal_hidden_rollout_campaign_run_body(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "run_sha256": digest}


def build_hidden_rollout_campaign_run_report(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "non_claims": run.get("non_claims", []),
        "report_version": HIDDEN_ROLLOUT_CAMPAIGN_RUN_REPORT_VERSION,
        "run_sha256": run.get("run_sha256"),
        "summary": {
            "campaign_sha256": run.get("campaign_sha256"),
            "execution_id": run.get("execution_id"),
            "execution_status": run.get("execution_status"),
        },
    }


def write_hidden_rollout_campaign_run_artifacts(
    *,
    execution_dir: Path,
    run_body: dict[str, Any],
    report_body: dict[str, Any],
) -> tuple[Path, Path]:
    r_path = execution_dir / HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME
    rep_path = execution_dir / HIDDEN_ROLLOUT_CAMPAIGN_RUN_REPORT_FILENAME
    r_path.write_text(canonical_json_dumps(run_body), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report_body), encoding="utf-8")
    return r_path, rep_path
