"""Deterministic replay↔execution equivalence charter payloads (M52 — charter only)."""

from __future__ import annotations

from typing import Any

from starlab.equivalence.equivalence_models import (
    CHARTER_FILENAME,
    CHARTER_REPORT_FILENAME,
    MISMATCH_KINDS_ORDERED,
    REPLAY_EXECUTION_EQUIVALENCE_CHARTER_REPORT_SCHEMA_VERSION,
    REPLAY_EXECUTION_EQUIVALENCE_CHARTER_SCHEMA_VERSION,
    RUNTIME_CONTRACT_REL_PATH,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def mismatch_taxonomy_entries() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    descriptions: dict[str, str] = {
        "missing_counterpart": (
            "A required paired artifact or slice exists on one side (replay trace vs "
            "execution trace) but has no governed counterpart under the comparison rules."
        ),
        "identity_mismatch": (
            "The same nominal identity (e.g. keyed ids, join keys) maps to different "
            "stable encodings between replay-derived and execution-derived surfaces."
        ),
        "ordering_mismatch": (
            "Order-sensitive comparisons disagree under the bounded ordering policy "
            "(e.g. sequence or partial order violations within the chartered window)."
        ),
        "count_mismatch": (
            "Cardinality or multiset counts disagree where the charter requires them to "
            "match (including grouped counts when in scope)."
        ),
        "bounded_semantic_divergence": (
            "Values differ within a chartered semantic domain where partial agreement is "
            "expressible (interpretive; does not automatically imply 'bug' without gate text)."
        ),
        "unavailable_by_design": (
            "Signal is intentionally absent or null because the governing contract marks "
            "it as unsupported on that side (contrast with missing counterpart)."
        ),
        "out_of_scope": (
            "Difference or absence is recorded but explicitly outside the M52 charter "
            "comparison surface (no equivalence claim)."
        ),
    }
    for kind in MISMATCH_KINDS_ORDERED:
        rows.append({"kind": kind, "description": descriptions[kind]})
    return rows


def build_replay_execution_equivalence_charter_artifact() -> dict[str, Any]:
    return {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_CHARTER_SCHEMA_VERSION,
        "milestone": "M52",
        "runtime_contract": RUNTIME_CONTRACT_REL_PATH,
        "bounded_claim_surface": (
            "This artifact is a governance charter and taxonomy boundary for future "
            "paired replay↔execution comparisons. It does not assert that any particular "
            "replay bytes match any particular execution trace. It defines what future "
            "M53/M54 work must prove under an explicit acceptance contract."
        ),
        "upstream_artifacts_required": [
            "Governed replay-side lineage: M04 replay_binding + opaque replay bytes "
            "(hashed; not required in CI fixtures beyond stated harness posture).",
            "M08+ replay parse / timeline / plane artifacts as chartered by the paired "
            "comparison family (versioned).",
            "M02 match_execution proof records and run identity / lineage seed JSON when "
            "comparing to a live or harness execution.",
            "Explicit comparison profile id (fixture label) selecting which planes are "
            "in scope for a given evidence run.",
        ],
        "comparison_identity_rules": [
            "Join paired runs on stable STARLAB ids: run_identity / lineage_seed fields "
            "as applicable, plus charter-declared replay_content_sha256 linkage for replay side.",
            "Reject ambiguous pairing: if multiple candidates match, emit missing_counterpart "
            "or identity_mismatch per governance (no silent pick).",
            "Schema-version gates: compared artifacts must advertise compatible "
            "schema_version / contract ids for the chartered profile.",
        ],
        "availability_classes": {
            "available": (
                "Field or entity is present on both sides and eligible for comparison under "
                "the active profile."
            ),
            "unavailable_by_design": (
                "Absent due to contract-defined omission (not a failure by itself)."
            ),
            "out_of_scope": (
                "Present or absent, but not part of the chartered equivalence claim surface "
                "for this milestone family."
            ),
            "mismatch": (
                "Compared under charter rules and found not equivalent (see mismatch taxonomy)."
            ),
        },
        "mismatch_taxonomy": mismatch_taxonomy_entries(),
        "future_m53_m54_proof_obligations": {
            "M53": (
                "Emit deterministic paired evidence artifacts for bounded profiles; still no "
                "Broad claim of universal equivalence."
            ),
            "M54": (
                "Audit hooks + acceptance gates that turn evidence into merge-bar statements "
                "only where explicitly satisfied; explicit residual non-claims."
            ),
        },
        "explicit_non_claims": [
            "Does not prove replay↔execution equivalence in any broad sense.",
            "Does not prove benchmark integrity, ladder strength, or match outcome semantics.",
            "Does not require live SC2 in CI; does not assert CI runner fidelity to local SC2.",
            "Does not subsume M19 cross-mode reconciliation (different proof family).",
        ],
    }


def build_replay_execution_equivalence_charter_report(
    *, charter_obj: dict[str, Any]
) -> dict[str, Any]:
    charter_hash = sha256_hex_of_canonical_json(charter_obj)
    return {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_CHARTER_REPORT_SCHEMA_VERSION,
        "charter_canonical_sha256": charter_hash,
        "charter_artifact": CHARTER_FILENAME,
        "report_artifact": CHARTER_REPORT_FILENAME,
        "emitter_module": "starlab.equivalence.emit_replay_execution_equivalence_charter",
        "status": "charter_only",
        "notes": (
            "M52 emits charter + report JSON for governance. Paired proof is explicitly "
            "deferred to M53/M54."
        ),
    }


def replay_execution_equivalence_charter_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    charter = build_replay_execution_equivalence_charter_artifact()
    report = build_replay_execution_equivalence_charter_report(charter_obj=charter)
    return charter, report
