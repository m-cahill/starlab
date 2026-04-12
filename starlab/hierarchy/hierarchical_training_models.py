"""Constants for hierarchical training run artifacts (M43)."""

from __future__ import annotations

from typing import Final

HIERARCHICAL_TRAINING_RUN_VERSION: Final[str] = "starlab.hierarchical_training_run.v1"
HIERARCHICAL_TRAINING_RUN_REPORT_VERSION: Final[str] = "starlab.hierarchical_training_run_report.v1"

HIERARCHICAL_TRAINING_RUN_FILENAME: Final[str] = "hierarchical_training_run.json"
HIERARCHICAL_TRAINING_RUN_REPORT_FILENAME: Final[str] = "hierarchical_training_run_report.json"

MANAGER_MODEL_FAMILY_ID: Final[str] = "starlab.m43.model.manager_logistic_regression_delegate_v1"
WORKER_MODEL_FAMILY_ID: Final[str] = "starlab.m43.model.worker_logistic_regression_coarse_label_v1"

ENCODING_POLICY_ID: Final[str] = "starlab.m41.encoding.context_signature_onehot_v1"

WEIGHTS_SUBDIR: Final[str] = "weights"
WEIGHTS_ARTIFACT_BASENAME: Final[str] = "hierarchical_training_sklearn_bundle.joblib"

SKLEARN_BUNDLE_SCHEMA: Final[str] = "starlab.m43.hierarchical_sklearn_bundle.v1"

RUN_IDENTITY_VERSION: Final[str] = "starlab.hierarchical_training_run_identity.v1"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "benchmark_integrity",
    "hierarchical_comparison_m42_integration",
    "learned_agent_comparison_consumption",
    "live_play_m44",
    "live_sc2_ci",
    "live_sc2_execution",
    "m45_rl_self_play",
    "public_weights_release",
    "replay_execution_equivalence",
    "weights_in_repo",
)
