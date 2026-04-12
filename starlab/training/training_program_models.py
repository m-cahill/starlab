"""Version constants and structured content for the agent training program contract (M40)."""

from __future__ import annotations

from typing import Final, TypedDict

AGENT_TRAINING_PROGRAM_CONTRACT_VERSION: Final[str] = "starlab.agent_training_program_contract.v1"
AGENT_TRAINING_PROGRAM_CONTRACT_REPORT_VERSION: Final[str] = (
    "starlab.agent_training_program_contract_report.v1"
)

CONTRACT_FILENAME: Final[str] = "agent_training_program_contract.json"
REPORT_FILENAME: Final[str] = "agent_training_program_contract_report.json"

TRAINING_PHASE_VERSION: Final[str] = "starlab.training_phase.vi_m40_m45.v1"


class MilestoneIntentRow(TypedDict):
    milestone: str
    title: str
    one_line_intent: str


def milestone_sequence_v1() -> tuple[MilestoneIntentRow, ...]:
    return (
        {
            "milestone": "M40",
            "title": "Agent Training Program Charter & Artifact Contract",
            "one_line_intent": (
                "Recharter Phase VI and define the governed training-program contract; "
                "no model training in M40."
            ),
        },
        {
            "milestone": "M41",
            "title": "Replay-Imitation Training Pipeline v1",
            "one_line_intent": (
                "First governed replay-imitation training pipeline emitting required artifacts; "
                "local-first execution."
            ),
        },
        {
            "milestone": "M42",
            "title": "Learned-Agent Comparison Harness v1",
            "one_line_intent": (
                "Comparable evaluation of learned agents against canonical harness entrypoints; "
                "explicit non-claims preserved."
            ),
        },
        {
            "milestone": "M43",
            "title": "Hierarchical Training Pipeline v1",
            "one_line_intent": (
                "Governed hierarchical training path building on M29/M30 surfaces; "
                "bounded scope."
            ),
        },
        {
            "milestone": "M44",
            "title": "Local Live-Play Validation Harness v1",
            "one_line_intent": (
                "Local-only validation against live or harnessed play; "
                "not proved in CI."
            ),
        },
        {
            "milestone": "M45",
            "title": "Self-Play / RL Bootstrap v1",
            "one_line_intent": (
                "Governed self-play or RL bootstrap lane under contract; "
                "no benchmark-integrity claim by default."
            ),
        },
    )


def allowed_upstreams_v1() -> dict[str, object]:
    return {
        "m26_replay_training_dataset": (
            "Governed replay_training_dataset.json / report over M14 bundles "
            "(dataset contract; not training execution)."
        ),
        "m28_learned_agent_evaluation": (
            "learned_agent_evaluation.json / report — canonical learned-agent evaluation "
            "entrypoint pattern for fixture/offline evaluation."
        ),
        "m29_hierarchical_agent_interface": (
            "hierarchical_agent_interface_schema — two-level trace contract."
        ),
        "m30_replay_hierarchical_imitation_agent": (
            "replay_hierarchical_imitation_agent — hierarchical imitation agent artifacts."
        ),
        "m31_replay_explorer_surface": (
            "replay_explorer_surface — operator evidence / explorer surfaces."
        ),
        "m20_through_m25_evaluation_chain": (
            "Benchmark contract, baselines, M23 tournament, M24 diagnostics, M25 evidence pack "
            "as governed evaluation context (not upgraded to benchmark integrity)."
        ),
    }


def future_required_artifacts_v1() -> dict[str, list[str]]:
    return {
        "M41": [
            "training_run_manifest.json (or equivalent) with lineage to M26/M14 inputs",
            "replay_imitation_training_report.json (or equivalent) — metrics, splits, non-claims",
            "explicit local-only execution record where applicable",
        ],
        "M42": [
            "learned_agent_comparison.json / report aligned to M28-style evaluation posture",
            "entrant catalog and comparison methodology summary",
        ],
        "M43": [
            "hierarchical_training_run.json / report binding to M29/M30 contracts",
            "delegate / trace policy identifiers as required by hierarchy contract",
        ],
        "M44": [
            "local_live_play_validation.json / report — local-only; not CI-proved",
            "explicit separation from benchmark-integrity claims",
        ],
        "M45": [
            "self_play_or_rl_bootstrap.json / report under program version",
            "non-claims for ladder, live ranking, and benchmark certification",
        ],
    }


def ci_policy_v1() -> dict[str, object]:
    return {
        "no_gpu_training_in_ci": True,
        "no_live_sc2_in_ci": True,
        "no_benchmark_integrity_claim_in_ci": True,
        "allowed_in_ci": [
            "Contract and schema validation for training-program metadata",
            "Deterministic emission of agent_training_program_contract.json / report",
            "Tests of training code paths that are fixture-only or mocked",
            "Import / governance guards consistent with existing repo patterns",
        ],
        "not_allowed_in_ci": [
            "Heavy GPU training jobs",
            "StarCraft II client execution as proof",
            "Claiming replay↔execution equivalence or benchmark integrity",
        ],
    }


def local_training_policy_v1() -> dict[str, object]:
    return {
        "training_runs_are_local_first": True,
        "reference_local_gpu": "NVIDIA GeForce RTX 5090 Blackwell",
        "ci_is_not_a_training_cluster": True,
        "operators_expected_to_record": [
            "Run identity / lineage where the milestone contract requires it",
            "Data and weight provenance per rights_register and replay policy",
        ],
    }


def non_claims_v1() -> tuple[str, ...]:
    return (
        "starlab.m40.non_claim.not_benchmark_integrity",
        "starlab.m40.non_claim.not_replay_execution_equivalence",
        "starlab.m40.non_claim.not_live_sc2_in_ci",
        "starlab.m40.non_claim.not_gpu_training_in_ci",
        "starlab.m40.non_claim.training_runs_local_first_not_ci_certified",
        "starlab.m40.non_claim.m41_through_m45_artifacts_not_proved_until_merged_closed",
        "starlab.m40.non_claim.no_weights_committed_by_default",
        "starlab.m40.non_claim.no_ladder_or_live_play_ranking_claim",
    )


def rights_and_provenance_reminders_v1() -> tuple[str, ...]:
    return (
        "Training data, labels, and model weights must respect docs/replay_data_provenance.md "
        "and docs/rights_register.md.",
        "Third-party replays and derived tensors remain subject to intake policy; "
        "no automatic license to redistribute weights.",
        "Contract emission does not certify legal clearance of any corpus.",
    )


def canonical_evaluation_entrypoints_v1() -> tuple[str, ...]:
    return (
        "M28 learned_agent_evaluation harness (offline, explicit non-claims)",
        "M23 evaluation_tournament + M24 diagnostics + M25 baseline_evidence_pack (fixture chain)",
        "M31 replay_explorer_surface (operator evidence; not benchmark integrity)",
        "M39 public flagship proof pack (assembles surfaces; non-claims in pack JSON)",
    )
