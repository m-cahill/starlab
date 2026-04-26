"""V15-M12 showcase agent release pack — constants and vocabulary (governance surface only)."""

from __future__ import annotations

from typing import Final

CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK: Final[str] = "starlab.v15.showcase_agent_release_pack.v1"
CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED: Final[str] = (
    "starlab.v15.showcase_operator_release_evidence_declared.v1"
)

MILESTONE_ID_V15_M12: Final[str] = "V15-M12"
EMITTER_MODULE_SHOWCASE_RELEASE: Final[str] = "starlab.v15.emit_v15_showcase_agent_release_pack"

CONTRACT_VERSION: Final[str] = "1"
REPORT_VERSION_SHOWCASE_RELEASE: Final[str] = "1"

SEAL_KEY_SHOWCASE_RELEASE_PACK: Final[str] = "showcase_agent_release_pack_sha256"

FILENAME_SHOWCASE_RELEASE_PACK: Final[str] = "v15_showcase_agent_release_pack.json"
REPORT_FILENAME_SHOWCASE_RELEASE_PACK: Final[str] = "v15_showcase_agent_release_pack_report.json"
FILENAME_SHOWCASE_RELEASE_BRIEF_MD: Final[str] = "v15_showcase_agent_release_brief.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"

PROFILE_ID_SHOWCASE_RELEASE_PACK: Final[str] = "starlab.v15.showcase_agent_release_pack_profile.v1"

PLACEHOLDER_SHA256: Final[str] = "0" * 64
FIXTURE_RELEASE_PACK_ID: Final[str] = "v15_m12:fixture_ci:deterministic"

# --- Release status vocabulary ---
STATUS_FIXTURE_CONTRACT_ONLY: Final[str] = "fixture_contract_only"
STATUS_BLOCKED_M08_RECEIPT: Final[str] = "blocked_missing_m08_campaign_receipt"
STATUS_BLOCKED_PROMOTED_CP: Final[str] = "blocked_missing_promoted_checkpoint"
STATUS_BLOCKED_STRONG_AGENT: Final[str] = "blocked_missing_strong_agent_benchmark"
STATUS_BLOCKED_XAI: Final[str] = "blocked_missing_xai_demonstration"
STATUS_BLOCKED_HUMAN_BENCHMARK: Final[str] = "blocked_missing_human_benchmark_claim"
STATUS_BLOCKED_RIGHTS: Final[str] = "blocked_missing_rights_clearance"
STATUS_BLOCKED_MANIFEST: Final[str] = "blocked_missing_release_manifest"
STATUS_BLOCKED_PUBPRIV: Final[str] = "blocked_public_private_boundary"
STATUS_OP_PREFLIGHT_VALIDATED: Final[str] = "operator_preflight_release_pack_validated"
STATUS_OP_DECLARED_VALIDATED: Final[str] = "operator_declared_release_pack_validated"
STATUS_SHOWCASE_CANDIDATE_PACKAGED: Final[str] = "showcase_release_candidate_packaged"
STATUS_SHOWCASE_RELEASE_AUTHORIZED: Final[str] = "showcase_release_authorized"

ALL_SHOWCASE_RELEASE_STATUSES: Final[tuple[str, ...]] = (
    STATUS_FIXTURE_CONTRACT_ONLY,
    STATUS_BLOCKED_M08_RECEIPT,
    STATUS_BLOCKED_PROMOTED_CP,
    STATUS_BLOCKED_STRONG_AGENT,
    STATUS_BLOCKED_XAI,
    STATUS_BLOCKED_HUMAN_BENCHMARK,
    STATUS_BLOCKED_RIGHTS,
    STATUS_BLOCKED_MANIFEST,
    STATUS_BLOCKED_PUBPRIV,
    STATUS_OP_PREFLIGHT_VALIDATED,
    STATUS_OP_DECLARED_VALIDATED,
    STATUS_SHOWCASE_CANDIDATE_PACKAGED,
    STATUS_SHOWCASE_RELEASE_AUTHORIZED,
)

# --- Gates R0–R14 ---
R0_ARTIFACT_INTEGRITY: Final[str] = "R0_artifact_integrity"
R1_CAMPAIGN_RECEIPT_BINDING: Final[str] = "R1_campaign_receipt_binding"
R2_CHECKPOINT_PROMOTION_BINDING: Final[str] = "R2_checkpoint_promotion_binding"
R3_CHECKPOINT_LINEAGE_BINDING: Final[str] = "R3_checkpoint_lineage_binding"
R4_STRONG_AGENT_SCORECARD_BINDING: Final[str] = "R4_strong_agent_scorecard_binding"
R5_XAI_DEMONSTRATION_BINDING: Final[str] = "R5_xai_demonstration_binding"
R6_HUMAN_BENCHMARK_CLAIM_BINDING: Final[str] = "R6_human_benchmark_claim_binding"
R7_RIGHTS_AND_REGISTER_POSTURE: Final[str] = "R7_rights_and_register_posture"
R8_PUBLIC_PRIVATE_BOUNDARY: Final[str] = "R8_public_private_boundary"
R9_RELEASE_MANIFEST_COMPLETENESS: Final[str] = "R9_release_manifest_completeness"
R10_CLAIM_TEXT_BOUNDARY: Final[str] = "R10_claim_text_boundary"
R11_REPRODUCIBILITY_SHA_BINDINGS: Final[str] = "R11_reproducibility_and_sha_bindings"
R12_RAW_ASSET_EXCLUSION: Final[str] = "R12_raw_asset_exclusion"
R13_OPERATOR_NOTES_REDACTION: Final[str] = "R13_operator_notes_redaction"
R14_V2_BOUNDARY: Final[str] = "R14_v2_boundary"

ALL_RELEASE_GATE_IDS: Final[tuple[str, ...]] = (
    R0_ARTIFACT_INTEGRITY,
    R1_CAMPAIGN_RECEIPT_BINDING,
    R2_CHECKPOINT_PROMOTION_BINDING,
    R3_CHECKPOINT_LINEAGE_BINDING,
    R4_STRONG_AGENT_SCORECARD_BINDING,
    R5_XAI_DEMONSTRATION_BINDING,
    R6_HUMAN_BENCHMARK_CLAIM_BINDING,
    R7_RIGHTS_AND_REGISTER_POSTURE,
    R8_PUBLIC_PRIVATE_BOUNDARY,
    R9_RELEASE_MANIFEST_COMPLETENESS,
    R10_CLAIM_TEXT_BOUNDARY,
    R11_REPRODUCIBILITY_SHA_BINDINGS,
    R12_RAW_ASSET_EXCLUSION,
    R13_OPERATOR_NOTES_REDACTION,
    R14_V2_BOUNDARY,
)

GATE_STATUS_PASS: Final[str] = "pass"
GATE_STATUS_WARNING: Final[str] = "warning"
GATE_STATUS_FAIL: Final[str] = "fail"
GATE_STATUS_BLOCKED: Final[str] = "blocked"
GATE_STATUS_NOT_EVALUATED: Final[str] = "not_evaluated"
GATE_STATUS_NOT_APPLICABLE: Final[str] = "not_applicable"

ALL_GATE_STATUSES: Final[tuple[str, ...]] = (
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    GATE_STATUS_FAIL,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_NOT_APPLICABLE,
)

NON_CLAIMS_V15_M12: Final[tuple[str, ...]] = (
    "V15-M12 does not train a checkpoint; does not promote a checkpoint; does not execute a long "
    "GPU campaign; does not run strong-agent benchmarks; does not run live SC2; does not run XAI "
    "inference; does not run human-panel matches; does not authorize showcase-agent, "
    "strong-agent, human-benchmark, ladder, or v2 claims on the default path; and does not commit "
    "model weights, checkpoint blobs, raw replays, videos, saliency tensors, participant records, "
    "private operator notes, or private paths.",
    "M12 packages governed release-pack metadata and SHA bindings only; "
    "v2 go/no-go remains V15-M13.",
)

OPERATOR_RELEASE_EVIDENCE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "contract_id",
        "evidence_bundle_id",
        "operator_public_notes",
        "rights_clearance_operator_declared",
    }
)


def default_m12_authorization_flags() -> dict[str, bool]:
    return {
        "showcase_agent_release_authorized": False,
        "public_showcase_claim_authorized": False,
        "strong_agent_claim_authorized": False,
        "human_benchmark_claim_authorized": False,
        "ladder_claim_authorized": False,
        "checkpoint_promoted_for_release": False,
        "xai_demonstration_bound": False,
        "human_panel_claim_bound": False,
        "rights_clearance_for_public_release": False,
        "v2_authorized": False,
    }


__all__ = [
    "ALL_GATE_STATUSES",
    "ALL_RELEASE_GATE_IDS",
    "ALL_SHOWCASE_RELEASE_STATUSES",
    "CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED",
    "CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK",
    "CONTRACT_VERSION",
    "EMITTER_MODULE_SHOWCASE_RELEASE",
    "FILENAME_SHOWCASE_RELEASE_BRIEF_MD",
    "FILENAME_SHOWCASE_RELEASE_PACK",
    "FIXTURE_RELEASE_PACK_ID",
    "GATE_STATUS_BLOCKED",
    "GATE_STATUS_FAIL",
    "GATE_STATUS_NOT_APPLICABLE",
    "GATE_STATUS_NOT_EVALUATED",
    "GATE_STATUS_PASS",
    "GATE_STATUS_WARNING",
    "MILESTONE_ID_V15_M12",
    "NON_CLAIMS_V15_M12",
    "OPERATOR_RELEASE_EVIDENCE_KEYS",
    "PLACEHOLDER_SHA256",
    "PROFILE_FIXTURE_CI",
    "PROFILE_ID_SHOWCASE_RELEASE_PACK",
    "PROFILE_OPERATOR_DECLARED",
    "PROFILE_OPERATOR_PREFLIGHT",
    "R0_ARTIFACT_INTEGRITY",
    "R1_CAMPAIGN_RECEIPT_BINDING",
    "R10_CLAIM_TEXT_BOUNDARY",
    "R11_REPRODUCIBILITY_SHA_BINDINGS",
    "R12_RAW_ASSET_EXCLUSION",
    "R13_OPERATOR_NOTES_REDACTION",
    "R14_V2_BOUNDARY",
    "R2_CHECKPOINT_PROMOTION_BINDING",
    "R3_CHECKPOINT_LINEAGE_BINDING",
    "R4_STRONG_AGENT_SCORECARD_BINDING",
    "R5_XAI_DEMONSTRATION_BINDING",
    "R6_HUMAN_BENCHMARK_CLAIM_BINDING",
    "R7_RIGHTS_AND_REGISTER_POSTURE",
    "R8_PUBLIC_PRIVATE_BOUNDARY",
    "R9_RELEASE_MANIFEST_COMPLETENESS",
    "REPORT_FILENAME_SHOWCASE_RELEASE_PACK",
    "REPORT_VERSION_SHOWCASE_RELEASE",
    "SEAL_KEY_SHOWCASE_RELEASE_PACK",
    "STATUS_BLOCKED_HUMAN_BENCHMARK",
    "STATUS_BLOCKED_M08_RECEIPT",
    "STATUS_BLOCKED_MANIFEST",
    "STATUS_BLOCKED_PROMOTED_CP",
    "STATUS_BLOCKED_PUBPRIV",
    "STATUS_BLOCKED_RIGHTS",
    "STATUS_BLOCKED_STRONG_AGENT",
    "STATUS_BLOCKED_XAI",
    "STATUS_FIXTURE_CONTRACT_ONLY",
    "STATUS_OP_DECLARED_VALIDATED",
    "STATUS_OP_PREFLIGHT_VALIDATED",
    "STATUS_SHOWCASE_CANDIDATE_PACKAGED",
    "STATUS_SHOWCASE_RELEASE_AUTHORIZED",
    "default_m12_authorization_flags",
]
