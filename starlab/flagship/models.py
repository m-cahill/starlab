"""Version identifiers and non-claims for the public flagship proof pack (M39)."""

from __future__ import annotations

from typing import Final

PROOF_PACK_VERSION: Final[str] = "starlab.public_flagship_proof_pack.v1"
PROOF_PACK_REPORT_VERSION: Final[str] = "starlab.public_flagship_proof_pack_report.v1"

PROOF_PACK_FILENAME: Final[str] = "public_flagship_proof_pack.json"
PROOF_PACK_REPORT_FILENAME: Final[str] = "public_flagship_proof_pack_report.json"
HASHES_FILENAME: Final[str] = "hashes.json"

PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1: Final[tuple[str, ...]] = (
    "starlab.m39.non_claim.not_benchmark_integrity",
    "starlab.m39.non_claim.not_live_sc2_in_ci",
    "starlab.m39.non_claim.not_replay_execution_equivalence",
    "starlab.m39.non_claim.not_new_agent_training_or_play_testing_track",
    "starlab.m39.non_claim.not_new_benchmark_semantics",
    "starlab.m39.non_claim.not_operating_manual_v1",
    "starlab.m39.non_claim.not_phase_vi_m40_m41",
    "starlab.m39.non_claim.not_product_ui_or_hosted_frontend_as_milestone_scope",
    "starlab.m39.non_claim.not_stronger_rts_ai_claim_than_assembled_surfaces",
)
