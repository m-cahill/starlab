"""V15-M61 — v1.5 release-lock / showcase video proof-pack constants."""

from __future__ import annotations

from typing import Final

CONTRACT_ID: Final[str] = "starlab.v15.m61.release_lock_proof_pack.v1"
CONTRACT_ID_REPORT: Final[str] = "starlab.v15.m61.release_lock_proof_pack_report.v1"
CONTRACT_ID_CAPTURE_MANIFEST: Final[str] = "starlab.v15.m61.showcase_video_capture_manifest.v1"

PROFILE_ID: Final[str] = "starlab.v15.m61.release_lock_showcase_video_proof_pack_update.v1"
MILESTONE: Final[str] = "V15-M61"
EMITTER_MODULE: Final[str] = "starlab.v15.emit_v15_m61_release_lock_proof_pack"

FILENAME_PROOF_PACK_JSON: Final[str] = "v15_m61_release_lock_proof_pack.json"
FILENAME_PROOF_PACK_REPORT_JSON: Final[str] = "v15_m61_release_lock_proof_pack_report.json"
FILENAME_PROOF_PACK_MD: Final[str] = "v15_m61_release_lock_proof_pack.md"
FILENAME_CAPTURE_MANIFEST_JSON: Final[str] = "v15_m61_showcase_video_capture_manifest.json"
FILENAME_CAPTURE_CHECKLIST_MD: Final[str] = "v15_m61_showcase_video_capture_checklist.md"

PROFILE_FIXTURE_CI: Final[str] = "fixture_ci"
PROFILE_OPERATOR_PREFLIGHT: Final[str] = "operator_preflight"
PROFILE_OPERATOR_DECLARED: Final[str] = "operator_declared"
PROFILE_OPERATOR_RELEASE_LOCK: Final[str] = "operator_release_lock"

CANONICAL_CANDIDATE_CHECKPOINT_SHA256: Final[str] = (
    "7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90"
)

RELEASE_LOCK_STATUS_FIXTURE: Final[str] = "fixture_schema_only_release_lock_shape"
RELEASE_LOCK_STATUS_LOCKED: Final[str] = "v1_5_bounded_showcase_evidence_locked"
RELEASE_LOCK_STATUS_PREFLIGHT: Final[str] = "operator_preflight_validated_not_release_locked"

CAPTURE_STATUS_FIXTURE_NO_VIDEO: Final[str] = "fixture_schema_only_no_video"
CAPTURE_STATUS_OPERATOR_CAPTURED: Final[str] = "operator_video_captured"

SCOPE_BOUNDED_SHOWCASE: Final[str] = "bounded_showcase_evidence_package_only"

FIXTURE_PLACEHOLDER_SHA256: Final[str] = "0" * 64

STRONGEST_ALLOWED_CLAIM: Final[str] = (
    "STARLAB v1.5 is locked as a bounded showcase-evidence proof pack with governed "
    "training, packaging, watchability, adapter-smoke, lock-decision, and showcase-video "
    "evidence; this is not benchmark pass/fail, strength evaluation, checkpoint "
    "promotion, 72-hour authorization, or v2 authorization."
)

NON_CLAIMS: Final[tuple[str, ...]] = (
    "V15-M61 does not execute benchmark matches.",
    "V15-M61 does not compute benchmark pass/fail.",
    "V15-M61 does not evaluate strength.",
    "V15-M61 does not promote the checkpoint.",
    "V15-M61 does not execute new training.",
    "V15-M61 does not authorize a 72-hour run.",
    "V15-M61 does not authorize v2 or v2 recharter.",
    "The showcase video is demonstration evidence only.",
)

SESSION_SOURCES_ALLOWED: Final[frozenset[str]] = frozenset(
    (
        "existing_m57a_replay",
        "existing_m58_adapter_smoke_replay",
        "new_m61_showcase_capture",
        "V15-M57A/V15-M58/M52A-derived-or-new-M61-capture",
    )
)
