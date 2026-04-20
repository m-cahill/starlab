"""Stub opponent / snapshot pool for opening PX2-M03 (honest partial)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from starlab.runs.json_util import sha256_hex_of_canonical_json


@dataclass(frozen=True, slots=True)
class SnapshotRef:
    """Named snapshot slot (policy or opponent stand-in)."""

    ref_id: str
    role: str
    notes: str = ""


@dataclass(frozen=True, slots=True)
class OpponentPoolStub:
    """Minimal pool: seed policy ref + opponent slots (stub — extend in later M03 work)."""

    seed_policy_ref_id: str
    snapshot_refs: tuple[SnapshotRef, ...]
    anti_collapse_guardrail_notes: str


DEFAULT_SEED_REF: Final[str] = "px2_m03_seed_bootstrap_policy"


def build_default_opponent_pool_stub(*, campaign_tag: str = "slice1") -> OpponentPoolStub:
    """Deterministic default pool for fixture smoke and contract emission."""

    tag = campaign_tag.strip() or "slice1"
    return OpponentPoolStub(
        seed_policy_ref_id=DEFAULT_SEED_REF,
        snapshot_refs=(
            SnapshotRef(
                ref_id=DEFAULT_SEED_REF,
                role="seed_bootstrap_policy",
                notes=(
                    "Closed PX2-M02 BootstrapTerranPolicy class; "
                    "weights via deterministic init in slice 1."
                ),
            ),
            SnapshotRef(
                ref_id=f"{tag}_opponent_snapshot_a",
                role="opponent_stub",
                notes="Placeholder opponent identity for selection bookkeeping tests.",
            ),
            SnapshotRef(
                ref_id=f"{tag}_opponent_snapshot_b",
                role="opponent_stub",
                notes="Second slot for round-robin selection tests.",
            ),
        ),
        anti_collapse_guardrail_notes=(
            "Descriptive only in slice 1: diversity / collapse monitoring is not implemented; "
            "fields exist in campaign contract for later PX2-M03 work."
        ),
    )


def opponent_pool_to_json_dict(pool: OpponentPoolStub) -> dict[str, Any]:
    return {
        "seed_policy_ref_id": pool.seed_policy_ref_id,
        "snapshot_refs": [
            {"ref_id": r.ref_id, "role": r.role, "notes": r.notes} for r in pool.snapshot_refs
        ],
        "anti_collapse_guardrail_notes": pool.anti_collapse_guardrail_notes,
        "stub_posture": "partial_opponent_pool_opening_m03",
    }


ROLE_SEED_BOOTSTRAP: Final[str] = "seed_bootstrap_policy"
ROLE_FROZEN_SEED_SNAPSHOT: Final[str] = "frozen_seed_snapshot"
ROLE_OPPONENT_STUB: Final[str] = "opponent_stub"


def build_slice5_opponent_pool(*, campaign_tag: str = "slice5") -> OpponentPoolStub:
    """Expanded bounded pool for slice 5 — multiple named opponent labels + frozen seed slot."""

    tag = campaign_tag.strip() or "slice5"
    return OpponentPoolStub(
        seed_policy_ref_id=DEFAULT_SEED_REF,
        snapshot_refs=(
            SnapshotRef(
                ref_id=DEFAULT_SEED_REF,
                role=ROLE_SEED_BOOTSTRAP,
                notes="Closed PX2-M02 BootstrapTerranPolicy; deterministic init in bounded runs.",
            ),
            SnapshotRef(
                ref_id=f"{tag}_frozen_seed_snapshot",
                role=ROLE_FROZEN_SEED_SNAPSHOT,
                notes="Deterministic frozen-seed snapshot stand-in — not live ladder.",
            ),
            SnapshotRef(
                ref_id=f"{tag}_opponent_label_alpha",
                role=ROLE_OPPONENT_STUB,
                notes="Named opponent stub alpha — bookkeeping only.",
            ),
            SnapshotRef(
                ref_id=f"{tag}_opponent_label_beta",
                role=ROLE_OPPONENT_STUB,
                notes="Named opponent stub beta — bookkeeping only.",
            ),
            SnapshotRef(
                ref_id=f"{tag}_opponent_label_gamma",
                role=ROLE_OPPONENT_STUB,
                notes="Named opponent stub gamma — bookkeeping only.",
            ),
        ),
        anti_collapse_guardrail_notes=(
            "Slice-5 expanded pool — still not full anti-collapse; not industrial diversity proof."
        ),
    )


def opponent_battle_ref_ids(pool: OpponentPoolStub) -> tuple[str, ...]:
    """Refs used for opponent rotation (excludes seed bootstrap policy only)."""

    return tuple(r.ref_id for r in pool.snapshot_refs if r.role != ROLE_SEED_BOOTSTRAP)


def opponent_pool_identity_sha256(pool: OpponentPoolStub) -> str:
    """Deterministic identity seal for opponent-pool bookkeeping (not ladder proof)."""

    return sha256_hex_of_canonical_json(opponent_pool_to_json_dict(pool))


DEFAULT_SLICE5_WEIGHTED_FROZEN_WEIGHTS: Final[tuple[int, ...]] = (2, 1, 1, 1)
