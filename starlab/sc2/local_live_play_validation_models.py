"""M44 local live-play validation run artifact constants and types."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

LOCAL_LIVE_PLAY_VALIDATION_RUN_VERSION = "starlab.local_live_play_validation_run.v1"
LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_VERSION = "starlab.local_live_play_validation_run_report.v1"

LOCAL_LIVE_PLAY_VALIDATION_RUN_FILENAME = "local_live_play_validation_run.json"
LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_FILENAME = "local_live_play_validation_run_report.json"

RUNTIME_MODE_FIXTURE_STUB_CI: Literal["fixture_stub_ci"] = "fixture_stub_ci"
RUNTIME_MODE_LOCAL_LIVE_SC2: Literal["local_live_sc2"] = "local_live_sc2"

RuntimeMode = Literal["fixture_stub_ci", "local_live_sc2"]

NON_CLAIMS_V1: tuple[str, ...] = (
    "benchmark_integrity",
    "ladder_or_public_performance",
    "live_sc2_in_ci",
    "m45_rl_self_play",
    "mandatory_video_proof",
    "replay_execution_equivalence",
    "strong_gameplay_or_optimality",
    "weights_in_repo",
)


@dataclass(frozen=True, slots=True)
class OptionalVideoRegistration:
    """Supplementary media metadata (replay remains primary evidence)."""

    path: str
    sha256: str
    size_bytes: int
    duration_seconds: float | None
    format: str
    resolution: str | None = None
    codec: str | None = None


@dataclass(frozen=True, slots=True)
class LivePlayValidationPaths:
    """Resolved layout under ``out/live_validation_runs/<run_id>/``."""

    output_dir: Path
    run_json: Path
    report_json: Path
    match_proof: Path
    match_config: Path
    run_identity: Path
    lineage_seed: Path
    replay_dir: Path
    validation_replay: Path
    replay_binding: Path
