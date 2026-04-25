"""V15-M06 human panel benchmark protocol constants (protocol only; no human execution)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_HUMAN_PANEL_BENCHMARK: Final[str] = "starlab.v15.human_panel_benchmark.v1"
PROTOCOL_PROFILE_ID_HUMAN_PANEL: Final[str] = "starlab.v15.human_panel_benchmark_protocol.v1"

MILESTONE_ID_V15_M06: Final[str] = "V15-M06"
EMITTER_MODULE_HUMAN_PANEL: Final[str] = "starlab.v15.emit_v15_human_panel_benchmark"

SEAL_KEY_HUMAN_PANEL: Final[str] = "human_panel_benchmark_sha256"
FILENAME_HUMAN_PANEL_BENCHMARK: Final[str] = "v15_human_panel_benchmark.json"
REPORT_FILENAME_HUMAN_PANEL_BENCHMARK: Final[str] = "v15_human_panel_benchmark_report.json"
REPORT_VERSION_HUMAN_PANEL: Final[str] = "1"
CONTRACT_VERSION: Final[str] = "1"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

PROTOCOL_STATUS_FIXTURE_ONLY: Final[str] = "fixture_only"
PROTOCOL_STATUS_OP_COMPLETE: Final[str] = "operator_declared_complete"
PROTOCOL_STATUS_OP_INCOMPLETE: Final[str] = "operator_declared_incomplete"
PROTOCOL_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"

EVIDENCE_SCOPE_FIXTURE: Final[str] = "fixture_protocol"
EVIDENCE_SCOPE_OPERATOR: Final[str] = "operator_declared_protocol"
EVIDENCE_SCOPE_NOT_EVALUATED: Final[str] = "not_evaluated"

PLACEHOLDER_SHA256: Final[str] = "0" * 64

# §5 — participant tier vocabulary (synthetic / protocol; no real roster in fixture)
PARTICIPANT_TIER_IDS: Final[tuple[str, ...]] = (
    "casual_unranked",
    "bronze_silver_equivalent",
    "gold_platinum_equivalent",
    "diamond_plus_equivalent",
    "unknown_self_reported",
    "observer_or_non_competing",
)

# §5 — privacy posture (strict)
PRIVACY_POSTURE_IDS: Final[tuple[str, ...]] = (
    "private_identity_required",
    "public_identity_forbidden_by_default",
    "pseudonymous_participant_id_required",
    "raw_contact_info_forbidden_in_public_artifacts",
    "consent_record_required_for_execution",
)

# §5 — threshold policy options
THRESHOLD_OPTION_IDS: Final[tuple[str, ...]] = (
    "majority_threshold_gt_50",
    "supermajority_threshold_gte_65",
    "tier_scoped_majority",
    "no_claim_without_threshold_freeze",
)

# §5 — evidence *classes* (requirement tags; not results)
EVIDENCE_REQUIREMENT_CLASS_IDS: Final[tuple[str, ...]] = (
    "protocol_manifest",
    "participant_roster_private",
    "participant_tier_summary_public",
    "consent_receipts_private",
    "agent_checkpoint_identity",
    "checkpoint_lineage_manifest_sha256",
    "environment_lock_sha256",
    "match_replay_manifest",
    "match_result_manifest",
    "session_operator_note",
    "human_panel_result_report",
    "xai_pack_sample_requirement",
    "non_claims",
)

# Disallowed unbounded future claims (vocabulary; not asserted as outcomes)
DISALLOWED_CLAIM_SHAPES: Final[tuple[str, ...]] = (
    "beats all humans",
    "ladder-proven",
    "solved StarCraft II",
    "globally superior SC2 agent",
    "human-like reasoning proven",
    "v2-ready by default",
)

# Operator protocol JSON (top-level; metadata only; strict keys for parse_protocol_json)
PROTOCOL_JSON_TOP_LEVEL_KEYS: Final[tuple[str, ...]] = (
    "profile",
    "protocol_profile_id",
    "benchmark_id",
    "benchmark_name",
    "participant_privacy_profile",
    "participant_tiers",
    "eligibility_rules",
    "consent_requirements",
    "session_rules",
    "match_rules",
    "map_pool_policy",
    "agent_identity_requirements",
    "checkpoint_binding_requirements",
    "replay_capture_requirements",
    "result_policy",
    "threshold_policy",
    "evidence_requirements",
    "claim_boundary",
    "non_claims",
    "redaction_policy",
    "operator_notes",
    "extension_flags",
)

# Row shapes for operator validation
PRIVACY_POSTURE_ROW_FIELDS: Final[tuple[str, ...]] = (
    "posture_id",
    "enforcement",
    "protocol_status",
    "notes",
)
PARTICIPANT_TIER_ROW_FIELDS: Final[tuple[str, ...]] = (
    "tier_id",
    "description",
    "protocol_status",
    "notes",
)
THRESHOLD_POLICY_ROW_FIELDS: Final[tuple[str, ...]] = (
    "option_id",
    "description",
    "protocol_status",
    "notes",
)
EVIDENCE_REQ_ROW_FIELDS: Final[tuple[str, ...]] = (
    "evidence_class_id",
    "required",
    "storage_posture",
    "protocol_status",
    "notes",
)

NON_CLAIMS_V15_M06: Final[tuple[str, ...]] = (
    "V15-M06 defines and emits the human-panel benchmark protocol contract "
    "(starlab.v15.human_panel_benchmark.v1) and fixture v15_human_panel_benchmark.json + report. "
    "It is protocol and governance metadata only: it does not recruit or evaluate human "
    "participants; does not run human-panel matches; does not run live SC2; does not evaluate or "
    "promote a checkpoint; does not add real participant identities or results; does not "
    "authorize a 'beats most humans' claim; does not run GPU training or shakedown; does not "
    "perform XAI review; does not set human_benchmark_claim_authorized, strong_agent_claim_"
    "authorized, benchmark_execution_performed, human_panel_execution_performed, or "
    "long_gpu_run_authorized to true; does not approve real assets for claim-critical public "
    "registers; and does not open v2 or PX2-M04/PX2-M05. A human-panel benchmark protocol is not "
    "evidence that a human benchmark has been run or passed.",
    "A fixture human-panel protocol is schema and wiring only; not a performance or recruitment "
    "result.",
)

ALLOWED_FUTURE_CLAIM_BOUNDARY: Final[str] = (
    "The STARLAB v1.5 Showcase Agent exceeds the declared human-panel threshold under fixed "
    "Terran-first 1v1 rules, declared maps, fixed checkpoint identity, replay capture, "
    "participant-tier disclosure, and recorded non-claims."
)

__all__ = [
    "ALLOWED_FUTURE_CLAIM_BOUNDARY",
    "CONTRACT_ID_HUMAN_PANEL_BENCHMARK",
    "CONTRACT_VERSION",
    "DISALLOWED_CLAIM_SHAPES",
    "EMITTER_MODULE_HUMAN_PANEL",
    "EVIDENCE_REQ_ROW_FIELDS",
    "EVIDENCE_REQUIREMENT_CLASS_IDS",
    "EVIDENCE_SCOPE_FIXTURE",
    "EVIDENCE_SCOPE_NOT_EVALUATED",
    "EVIDENCE_SCOPE_OPERATOR",
    "FILENAME_HUMAN_PANEL_BENCHMARK",
    "MILESTONE_ID_V15_M06",
    "NON_CLAIMS_V15_M06",
    "PARTICIPANT_TIER_ROW_FIELDS",
    "PARTICIPANT_TIER_IDS",
    "PLACEHOLDER_SHA256",
    "PRIVACY_POSTURE_IDS",
    "PRIVACY_POSTURE_ROW_FIELDS",
    "PROFILE_FIXTURE_CI",
    "PROFILE_OPERATOR_DECLARED",
    "PROTOCOL_JSON_TOP_LEVEL_KEYS",
    "PROTOCOL_PROFILE_ID_HUMAN_PANEL",
    "PROTOCOL_STATUS_FIXTURE_ONLY",
    "PROTOCOL_STATUS_NOT_EVALUATED",
    "PROTOCOL_STATUS_OP_COMPLETE",
    "PROTOCOL_STATUS_OP_INCOMPLETE",
    "REPORT_FILENAME_HUMAN_PANEL_BENCHMARK",
    "REPORT_VERSION_HUMAN_PANEL",
    "SEAL_KEY_HUMAN_PANEL",
    "THRESHOLD_OPTION_IDS",
    "THRESHOLD_POLICY_ROW_FIELDS",
]
