"""V15-M05: strong-agent benchmark protocol / scorecard contract constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_STRONG_AGENT_SCORECARD: Final[str] = "starlab.v15.strong_agent_scorecard.v1"
PROTOCOL_PROFILE_ID: Final[str] = "starlab.v15.strong_agent_benchmark_protocol.v1"

MILESTONE_ID_V15_M05: Final[str] = "V15-M05"
EMITTER_MODULE_STRONG_AGENT: Final[str] = "starlab.v15.emit_v15_strong_agent_scorecard"

SEAL_KEY_STRONG_AGENT: Final[str] = "strong_agent_scorecard_sha256"
FILENAME_STRONG_AGENT_SCORECARD: Final[str] = "v15_strong_agent_scorecard.json"
REPORT_FILENAME_STRONG_AGENT_SCORECARD: Final[str] = "v15_strong_agent_scorecard_report.json"
REPORT_VERSION_STRONG_AGENT: Final[str] = "1"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

# §9 — benchmark_protocol_status
BENCHMARK_STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
BENCHMARK_STATUS_OP_COMPLETE: Final[str] = "operator_declared_complete"
BENCHMARK_STATUS_OP_INCOMPLETE: Final[str] = "operator_declared_incomplete"
BENCHMARK_STATUS_BLOCKED: Final[str] = "blocked"
BENCHMARK_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"

# evidence_scope
EVIDENCE_SCOPE_FIXTURE_PROTOCOL: Final[str] = "fixture_protocol"
EVIDENCE_SCOPE_OPERATOR_DECLARED: Final[str] = "operator_declared_protocol"
EVIDENCE_SCOPE_NOT_EVALUATED: Final[str] = "not_evaluated"

CHECK_PASS: Final[str] = "pass"
CHECK_FAIL: Final[str] = "fail"
CHECK_WARNING: Final[str] = "warning"

PLACEHOLDER_SHA256: Final[str] = "0" * 64

# §6.1 — operator protocol JSON (metadata only)
PROTOCOL_JSON_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "profile",
    "protocol_profile_id",
    "benchmark_id",
    "benchmark_name",
    "evaluation_ladder",
    "candidate_subject",
    "baseline_subjects",
    "map_pool",
    "opponent_pool",
    "scorecard_fields",
    "gate_thresholds",
    "evidence_requirements",
    "failure_mode_probes",
    "xai_requirements",
    "human_panel_reserved",
    "operator_notes",
    "non_claims",
)

# §2 — exact ladder stage ids
LADDER_STAGE_IDS: Final[tuple[str, ...]] = (
    "E0_artifact_integrity",
    "E1_fixture_smoke",
    "E2_scripted_baselines",
    "E3_heuristic_baselines",
    "E4_prior_starlab_checkpoints",
    "E5_local_live_sc2_bounded",
    "E6_failure_mode_probes",
    "E7_human_panel_reserved",
    "E8_xai_review_reserved",
)

LADDER_STAGE_TITLES: Final[dict[str, str]] = {
    "E0_artifact_integrity": "Artifact integrity and manifest coherence",
    "E1_fixture_smoke": "Fixture / CI wiring smoke (no real matches)",
    "E2_scripted_baselines": "Scripted baseline suite",
    "E3_heuristic_baselines": "Heuristic baseline suite",
    "E4_prior_starlab_checkpoints": "Prior STARLAB checkpoint agents",
    "E5_local_live_sc2_bounded": "Local live SC2 (bounded, operator-local)",
    "E6_failure_mode_probes": "Failure / exploit-surface probes",
    "E7_human_panel_reserved": "Human panel (reserved milestone)",
    "E8_xai_review_reserved": "XAI explanation review (reserved milestone)",
}

# Required metric / scorecard field names (names only for protocol rows)
REQUIRED_SCORECARD_METRIC_NAMES: Final[tuple[str, ...]] = (
    "win_rate",
    "loss_rate",
    "draw_or_timeout_rate",
    "average_game_length",
    "early_loss_rate",
    "economy_score",
    "production_score",
    "combat_score",
    "scouting_score",
    "expansion_score",
    "fallback_action_rate",
    "invalid_action_rate",
    "xai_trace_coverage",
    "critical_decision_trace_count",
)

STATUS_VOCABULARY: Final[dict[str, tuple[str, ...]]] = {
    "benchmark_protocol_status": (
        BENCHMARK_STATUS_FIXTURE_ONLY,
        BENCHMARK_STATUS_OP_COMPLETE,
        BENCHMARK_STATUS_OP_INCOMPLETE,
        BENCHMARK_STATUS_BLOCKED,
        BENCHMARK_STATUS_NOT_EVALUATED,
    ),
    "subject_kind": (
        "fixture_candidate",
        "scripted_baseline",
        "heuristic_baseline",
        "prior_starlab_checkpoint",
        "candidate_checkpoint",
        "live_sc2_candidate",
        "human_panel_reserved",
    ),
    "stage_status": (
        "defined",
        "fixture",
        "not_executed",
        "operator_declared",
        "blocked",
        "not_evaluated",
    ),
    "gate_status": (
        "defined",
        "not_evaluated",
        "passed",
        "failed",
        "blocked",
        "fixture",
    ),
    "evidence_kind": (
        "environment_lock",
        "checkpoint_lineage",
        "xai_evidence_pack",
        "benchmark_scorecard",
        "replay_binding",
        "match_result",
        "operator_note",
        "human_panel_reserved",
    ),
    "evidence_scope": (
        EVIDENCE_SCOPE_FIXTURE_PROTOCOL,
        EVIDENCE_SCOPE_OPERATOR_DECLARED,
        EVIDENCE_SCOPE_NOT_EVALUATED,
    ),
}

# Candidate subject (§6.2) — all keys
CANDIDATE_SUBJECT_FIELDS: Final[tuple[str, ...]] = (
    "subject_id",
    "subject_kind",
    "checkpoint_id",
    "checkpoint_lineage_manifest_sha256",
    "environment_lock_sha256",
    "training_run_reference",
    "claim_use",
    "subject_status",
    "notes",
)

# Baseline subject (§6.3)
BASELINE_SUBJECT_FIELDS: Final[tuple[str, ...]] = (
    "subject_id",
    "subject_kind",
    "baseline_family",
    "source_milestone",
    "scorecard_reference",
    "subject_status",
    "notes",
)

# Map pool (§6.4)
MAP_POOL_FIELDS: Final[tuple[str, ...]] = (
    "map_pool_id",
    "map_pool_name",
    "map_ids",
    "map_source",
    "rights_posture",
    "map_pool_status",
    "notes",
)

# Opponent pool (§6.5)
OPPONENT_POOL_FIELDS: Final[tuple[str, ...]] = (
    "opponent_pool_id",
    "opponent_kinds",
    "opponent_ids",
    "pool_status",
    "notes",
)

# Gate threshold (§6.6)
GATE_THRESHOLD_FIELDS: Final[tuple[str, ...]] = (
    "gate_id",
    "gate_name",
    "metric_name",
    "comparison",
    "threshold_value",
    "required",
    "gate_status",
    "notes",
)

# Scorecard field (§6.7)
SCORECARD_FIELD_DEF_FIELDS: Final[tuple[str, ...]] = (
    "field_name",
    "field_type",
    "required",
    "description",
    "status",
)

# Evidence requirement (§6.8)
EVIDENCE_REQUIREMENT_FIELDS: Final[tuple[str, ...]] = (
    "evidence_id",
    "evidence_kind",
    "required",
    "source_contract",
    "evidence_status",
    "notes",
)

# Failure-mode probe (§6.9)
FAILURE_PROBE_FIELDS: Final[tuple[str, ...]] = (
    "probe_id",
    "probe_kind",
    "required",
    "probe_status",
    "notes",
)

# XAI requirements (§6.10)
XAI_REQUIREMENT_FIELDS: Final[tuple[str, ...]] = (
    "xai_requirement_id",
    "required_artifact",
    "required",
    "source_contract",
    "requirement_status",
    "notes",
)

NON_CLAIMS_V15_M05: Final[tuple[str, ...]] = (
    "V15-M05 defines and emits the strong-agent benchmark protocol and scorecard contract. It may "
    "validate fixture protocol metadata and may normalize supplied operator-declared protocol "
    "metadata, but it does not execute benchmarks, does not run live SC2, does not evaluate a "
    "checkpoint, does not select or promote a strong agent, does not run XAI review, does not run "
    "human-panel evaluation, does not execute GPU training or shakedown, does not authorize a long "
    "GPU run, does not approve real assets for claim-critical use, does not open v2, and does not "
    "open PX2-M04/PX2-M05.",
    "A strong-agent scorecard contract is not evidence that a strong-agent benchmark has passed.",
    "A fixture benchmark protocol is schema/wiring evidence only, not a performance result.",
)


__all__ = [
    "BASELINE_SUBJECT_FIELDS",
    "BENCHMARK_STATUS_BLOCKED",
    "BENCHMARK_STATUS_FIXTURE_ONLY",
    "BENCHMARK_STATUS_NOT_EVALUATED",
    "BENCHMARK_STATUS_OP_COMPLETE",
    "BENCHMARK_STATUS_OP_INCOMPLETE",
    "CANDIDATE_SUBJECT_FIELDS",
    "CHECK_FAIL",
    "CHECK_PASS",
    "CHECK_WARNING",
    "CONTRACT_ID_STRONG_AGENT_SCORECARD",
    "EMITTER_MODULE_STRONG_AGENT",
    "EVIDENCE_REQUIREMENT_FIELDS",
    "EVIDENCE_SCOPE_FIXTURE_PROTOCOL",
    "EVIDENCE_SCOPE_NOT_EVALUATED",
    "EVIDENCE_SCOPE_OPERATOR_DECLARED",
    "FAILURE_PROBE_FIELDS",
    "FILENAME_STRONG_AGENT_SCORECARD",
    "GATE_THRESHOLD_FIELDS",
    "LADDER_STAGE_IDS",
    "LADDER_STAGE_TITLES",
    "MAP_POOL_FIELDS",
    "MILESTONE_ID_V15_M05",
    "NON_CLAIMS_V15_M05",
    "OPPONENT_POOL_FIELDS",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_OPERATOR_DECLARED",
    "PROTOCOL_JSON_TOP_LEVEL_KEYS",
    "PROTOCOL_PROFILE_ID",
    "REPORT_FILENAME_STRONG_AGENT_SCORECARD",
    "REPORT_VERSION_STRONG_AGENT",
    "REQUIRED_SCORECARD_METRIC_NAMES",
    "SCORECARD_FIELD_DEF_FIELDS",
    "SEAL_KEY_STRONG_AGENT",
    "STATUS_VOCABULARY",
    "XAI_REQUIREMENT_FIELDS",
]
