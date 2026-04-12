"""Constants for replay-imitation training run artifacts (M41)."""

from __future__ import annotations

from typing import Final

REPLAY_IMITATION_TRAINING_RUN_VERSION: Final[str] = "starlab.replay_imitation_training_run.v1"
REPLAY_IMITATION_TRAINING_RUN_REPORT_VERSION: Final[str] = (
    "starlab.replay_imitation_training_run_report.v1"
)

REPLAY_IMITATION_TRAINING_RUN_FILENAME: Final[str] = "replay_imitation_training_run.json"
REPLAY_IMITATION_TRAINING_RUN_REPORT_FILENAME: Final[str] = (
    "replay_imitation_training_run_report.json"
)

MODEL_FAMILY: Final[str] = "starlab.m41.model.logistic_regression_signature_onehot_v1"
ENCODING_POLICY_ID: Final[str] = "starlab.m41.encoding.context_signature_onehot_v1"

WEIGHTS_SUBDIR: Final[str] = "weights"
WEIGHTS_ARTIFACT_BASENAME: Final[str] = "replay_imitation_sklearn_bundle.joblib"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "imitation_superiority_to_m27_beyond_recorded_metrics",
    "ladder_validity",
    "learned_agent_comparison_m42",
    "live_sc2_ci",
    "live_sc2_execution",
    "m43_plus_hierarchical_training",
    "public_weights_release",
    "replay_execution_equivalence",
    "weights_in_repo",
)
