"""Identifiers and vocabulary for SC2 foundation v1 release lock (M61)."""

from __future__ import annotations

from typing import Final

# Scope & profile (ledger-aligned)
RELEASE_SCOPE_SC2_FOUNDATION_V1: Final[str] = "starlab.m61.release_scope.sc2_foundation_v1"
CAMPAIGN_EVIDENCE_PROFILE_OPERATOR_LOCAL_V1: Final[str] = (
    "starlab.m61.campaign_evidence_profile."
    "operator_local_hidden_rollout_with_watchable_validation_v1"
)

# Artifact contracts
PROOF_PACK_CONTRACT_V1: Final[str] = "starlab.sc2_foundation_v1_proof_pack.v1"
PROOF_PACK_REPORT_CONTRACT_V1: Final[str] = "starlab.sc2_foundation_v1_proof_pack_report.v1"
AUDIT_CONTRACT_V1: Final[str] = "starlab.sc2_foundation_release_lock_audit.v1"
AUDIT_REPORT_CONTRACT_V1: Final[str] = "starlab.sc2_foundation_release_lock_audit_report.v1"

# Filenames
PROOF_PACK_FILENAME: Final[str] = "sc2_foundation_v1_proof_pack.json"
PROOF_PACK_REPORT_FILENAME: Final[str] = "sc2_foundation_v1_proof_pack_report.json"
AUDIT_FILENAME: Final[str] = "sc2_foundation_release_lock_audit.json"
AUDIT_REPORT_FILENAME: Final[str] = "sc2_foundation_release_lock_audit_report.json"

# Campaign length classes (proof-pack input / declaration)
CAMPAIGN_LENGTH_SHAKEDOWN: Final[str] = "shakedown"
CAMPAIGN_LENGTH_BOUNDED_SUBSTANTIVE: Final[str] = "bounded_substantive_run"
CAMPAIGN_LENGTH_OPERATOR_FULL_RUN: Final[str] = "operator_declared_full_run"

# Audit outcomes
RELEASE_SCOPE_READY: Final[str] = "ready_within_scope"
RELEASE_SCOPE_NOT_READY: Final[str] = "not_ready_within_scope"
RELEASE_SCOPE_NOT_EVALUABLE: Final[str] = "not_evaluable"

# Default non-claims merged into proof packs unless superseded by explicit input
SC2_FOUNDATION_V1_DEFAULT_NON_CLAIMS: Final[tuple[str, ...]] = (
    "starlab.m61.non_claim.not_benchmark_integrity_universal",
    "starlab.m61.non_claim.not_replay_execution_equivalence_universal",
    "starlab.m61.non_claim.not_live_sc2_default_merge_gate",
    "starlab.m61.non_claim.not_global_live_sc2_in_ci_proof",
    "starlab.m61.non_claim.not_ladder_public_performance_proof",
    "starlab.m61.non_claim.not_repository_branch_protection_via_proof_pack",
    "starlab.m61.non_claim.not_substitution_for_m52_m54_equivalence_track",
    "starlab.m61.non_claim.not_substitution_for_m55_m56_benchmark_integrity_track",
    "starlab.m61.non_claim.not_substitution_for_m57_m58_live_sc2_posture",
    "starlab.m61.non_claim.not_substitution_for_m59_ladder_protocol_alone",
)

# Minimum markers the release-lock audit expects (subset check; input may add more)
M61_AUDIT_REQUIRED_NON_CLAIM_MARKERS: Final[tuple[str, ...]] = (
    "starlab.m61.non_claim.not_benchmark_integrity_universal",
    "starlab.m61.non_claim.not_replay_execution_equivalence_universal",
    "starlab.m61.non_claim.not_ladder_public_performance_proof",
)
