"""Constants and protocol defaults for M49 full local training / bootstrap campaign charter."""

from __future__ import annotations

from typing import Final, TypedDict

FULL_LOCAL_TRAINING_CAMPAIGN_VERSION: Final[str] = "starlab.full_local_training_campaign.v1"
FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_VERSION: Final[str] = (
    "starlab.full_local_training_campaign_report.v1"
)
FULL_LOCAL_TRAINING_CAMPAIGN_PREFLIGHT_RECEIPT_VERSION: Final[str] = (
    "starlab.full_local_training_campaign_preflight_receipt.v1"
)

FULL_LOCAL_TRAINING_CAMPAIGN_FILENAME: Final[str] = "full_local_training_campaign_contract.json"
FULL_LOCAL_TRAINING_CAMPAIGN_REPORT_FILENAME: Final[str] = (
    "full_local_training_campaign_contract_report.json"
)
CAMPAIGN_PREFLIGHT_RECEIPT_FILENAME: Final[str] = "campaign_preflight_receipt.json"

NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "automatic_campaign_execution",
    "automatic_campaign_success",
    "benchmark_integrity",
    "bootstrap_run_artifact_implies_full_campaign",
    "full_local_campaign_proves_learning_gains",
    "full_local_campaign_proves_strong_policy",
    "ladder_or_public_performance",
    "live_sc2_in_ci",
    "long_operator_run_as_merge_gate",
    "replay_execution_equivalence",
    "statistical_significance_of_ranking",
    "weights_in_repo",
)


def default_campaign_protocol_v1() -> dict[str, object]:
    """Recommended phased protocol (documentation + contract default; not auto-executed)."""

    return {
        "minimum_episodes_governed_full_run": 100,
        "recommended_default_total_episodes": 250,
        "stretch_total_episodes_note": (
            "Continue beyond 250 only if episode-level evidence remains clean "
            "(see M47 distinctness posture)."
        ),
        "phases": [
            {
                "phase": "preflight",
                "kind": "gate",
                "description": "Deterministic readiness checks.",
            },
            {
                "phase": "shakedown",
                "kind": "bootstrap_episodes",
                "episode_budget": 5,
                "description": "Short integration smoke before tranches.",
            },
            {
                "phase": "tranche_a",
                "kind": "bootstrap_episodes",
                "episode_budget": 50,
                "description": "First governed batch.",
            },
            {
                "phase": "tranche_b",
                "kind": "bootstrap_episodes",
                "episode_budget": 50,
                "description": "Second governed batch (100 cumulative).",
            },
            {
                "phase": "optional_stretch",
                "kind": "bootstrap_episodes",
                "episode_budget": 150,
                "description": "Optional continuation toward 250 total when stable.",
            },
            {
                "phase": "optional_weighted_refit",
                "kind": "optional",
                "description": "M45 weighted re-fit when prerequisites and policy allow.",
            },
            {
                "phase": "post_refit_m42_comparison",
                "kind": "offline",
                "description": "M42 learned-agent comparison with aligned M20/M40 paths (M48).",
            },
            {
                "phase": "watchable_m44_validation",
                "kind": "operator_review",
                "episode_budget": 1,
                "description": "One watchable M44 validation run for qualitative review.",
            },
        ],
    }


def evidence_interpretation_block_v1() -> dict[str, object]:
    """M47-aligned interpretation rules (contract text; not statistical proof)."""

    return {
        "integration_success": (
            "Pipeline completed and emitted governed JSON under configured runtime_mode and "
            "policies."
        ),
        "distinct_episode_evidence": (
            "Do not treat configured episode counts as independent multi-sample evidence unless "
            "governed per-episode identities differ (see M47 episode manifest / "
            "validation_run_sha256)."
        ),
        "reward_summary": "Heuristic M45 reward from M44 validation outcomes — not ladder score.",
        "refit_eligibility": (
            "Weighted re-fit requires matching M26 dataset identity to M43 source_dataset and "
            "governed M14 bundle paths."
        ),
        "post_refit_comparison": (
            "M42 comparison binds M20 benchmark identity and M40 training-program identity "
            "(strict M41 rows when used)."
        ),
    }


class AuthorizationPostureV1(TypedDict):
    """Planning-only posture: charter does not execute or guarantee outcomes."""

    status: str
    meaning: str


AUTHORIZATION_POSTURE_PLANNED_CHARTER_ONLY: Final[AuthorizationPostureV1] = {
    "status": "planned_charter_only",
    "meaning": (
        "This artifact defines and authorizes a governed local campaign for operator execution. "
        "It does not run training, bootstrap, comparison, or validation by itself. "
        "It does not guarantee completion, success, or learning outcomes."
    ),
}
