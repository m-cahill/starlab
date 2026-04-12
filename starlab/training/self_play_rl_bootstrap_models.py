"""Constants and types for M45 self-play / RL bootstrap run artifacts."""

from __future__ import annotations

from typing import Final, Literal

SELF_PLAY_RL_BOOTSTRAP_RUN_VERSION: Final[str] = "starlab.self_play_rl_bootstrap_run.v1"
SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_VERSION: Final[str] = (
    "starlab.self_play_rl_bootstrap_run_report.v1"
)

SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME: Final[str] = "self_play_rl_bootstrap_run.json"
SELF_PLAY_RL_BOOTSTRAP_RUN_REPORT_FILENAME: Final[str] = "self_play_rl_bootstrap_run_report.json"
BOOTSTRAP_DATASET_FILENAME: Final[str] = "bootstrap_dataset.json"
EPISODE_MANIFEST_FILENAME: Final[str] = "episode_manifest.json"

UPDATED_POLICY_SUBDIR: Final[str] = "updated_policy"
UPDATED_BUNDLE_BASENAME: Final[str] = "rl_bootstrap_candidate_bundle.joblib"

REWARD_POLICY_ID: Final[str] = "starlab.m45.reward.validation_outcome_v1"
UPDATE_POLICY_ID: Final[str] = "starlab.m45.update.weighted_logistic_refit_v1"
EPISODE_MANIFEST_VERSION: Final[str] = "starlab.m45.episode_manifest.v1"

BootstrapMode = Literal[
    "single_candidate_fixture_stub",
    "single_candidate_local_live",
    "mirror_self_play_local",
]

NON_CLAIMS_V1: tuple[str, ...] = (
    "benchmark_integrity",
    "bootstrap_only_not_full_rl_program",
    "ladder_or_public_performance",
    "live_sc2_in_ci",
    "m45_rl_product_beyond_bootstrap",
    "replay_execution_equivalence",
    "weights_in_repo",
)
