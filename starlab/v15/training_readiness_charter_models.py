"""Constants for V15-M00 training readiness charter (deterministic JSON)."""

from __future__ import annotations

from typing import Final

TRAINING_READINESS_CHARTER_VERSION: Final[str] = "starlab.v15.training_readiness_charter.v1"
TRAINING_READINESS_CHARTER_REPORT_VERSION: Final[str] = (
    "starlab.v15.training_readiness_charter_report.v1"
)

TRAINING_READINESS_CHARTER_FILENAME: Final[str] = "v15_training_readiness_charter.json"
TRAINING_READINESS_CHARTER_REPORT_FILENAME: Final[str] = (
    "v15_training_readiness_charter_report.json"
)

MILESTONE_ID_V15_M00: Final[str] = "V15-M00"

NON_CLAIMS_V15_M00: Final[tuple[str, ...]] = (
    "long_gpu_training_completed",
    "strong_agent_achieved",
    "human_panel_benchmark_completed",
    "xai_demonstration_completed",
    "v2_opened",
    "px2_m04_auto_opened",
    "ladder_or_public_performance_proof",
    "benchmark_integrity_globally_proved",
    "replay_execution_equivalence_globally_proved",
)

ARTIFACT_FAMILY_CONTRACT_IDS_V1: Final[tuple[str, ...]] = (
    "starlab.v15.training_readiness_charter.v1",
    "starlab.v15.long_gpu_training_manifest.v1",
    "starlab.v15.checkpoint_lineage_manifest.v1",
    "starlab.v15.training_run_receipt.v1",
    "starlab.v15.strong_agent_scorecard.v1",
    "starlab.v15.xai_evidence_pack.v1",
    "starlab.v15.human_panel_benchmark.v1",
    "starlab.v15.showcase_agent_release_pack.v1",
)

AUTHORIZATION_POSTURE_CHARTER_ONLY: Final[str] = "charter_only_long_gpu_run_not_executed_in_m00"
