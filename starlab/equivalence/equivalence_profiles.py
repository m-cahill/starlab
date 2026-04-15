"""Bounded replay↔execution equivalence comparison profiles (M53+)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from starlab.equivalence.equivalence_models import PROFILE_IDENTITY_BINDING_V1


@dataclass(frozen=True, slots=True)
class EquivalenceProfileSpec:
    """Registry entry: narrow bounded claim, join keys, inputs — no proof verdict."""

    profile_id: str
    profile_version: str
    bounded_claim: str
    join_keys: str
    required_artifacts: str
    non_claims: str


PROFILE_REGISTRY: Final[dict[str, EquivalenceProfileSpec]] = {
    PROFILE_IDENTITY_BINDING_V1: EquivalenceProfileSpec(
        profile_id=PROFILE_IDENTITY_BINDING_V1,
        profile_version="1",
        bounded_claim=(
            "Pairwise consistency of governance identity fields across M03 run_identity "
            "and lineage_seed with M04 replay_binding (opaque replay_content_sha256); "
            "recomputes replay_binding_id; does not parse replay semantics."
        ),
        join_keys=(
            "run_spec_id, execution_id, proof_artifact_hash, lineage_seed_id "
            "(governed STARLAB ids / hashes only; no filename-only joins)."
        ),
        required_artifacts=(
            "run_identity.json (M03), lineage_seed.json (M03), replay_binding.json (M04)."
        ),
        non_claims=(
            "Replay↔execution equivalence not proved; no gameplay semantics; no parser "
            "correctness; no canonical-state / observation equivalence; M02 proof bytes "
            "not re-validated beyond identity linkage."
        ),
    ),
}


def resolve_profile(profile_id: str) -> EquivalenceProfileSpec:
    if profile_id not in PROFILE_REGISTRY:
        msg = f"unknown equivalence profile: {profile_id!r}"
        raise ValueError(msg)
    return PROFILE_REGISTRY[profile_id]
