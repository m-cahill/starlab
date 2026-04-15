"""Profile-scoped acceptance gate packs for replay↔execution equivalence audit (M54)."""

from __future__ import annotations

from typing import Any, Final

from starlab.equivalence.equivalence_models import (
    CHARTER_CONTRACT_ID,
    GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1,
    PROFILE_IDENTITY_BINDING_V1,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_REPORT_SCHEMA_VERSION,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json

_GATE_ID_PREFIX: Final[str] = "starlab.m54.gate.identity_binding"

# Subjects that must be present and “clean” (no disallowed mismatch kinds) for acceptance.
_IDENTITY_CHAIN_SUBJECTS: Final[tuple[str, ...]] = (
    "join.run_spec_id",
    "join.execution_id",
    "join.proof_artifact_hash",
    "join.lineage_seed_id",
    "join.config_hash",
    "replay_binding.replay_binding_id",
)

_ORDERED_SUBJECT: Final[str] = "parent_references.sequence_equality"

_SCHEMA_SUBJECTS: Final[tuple[str, ...]] = (
    "schema.run_identity.json",
    "schema.lineage_seed.json",
    "schema.replay_binding.json",
)

_ALLOWED_UNAVAILABLE_SUBJECT: Final[str] = "replay.replay_content_sha256"
_ALLOWED_OUT_OF_SCOPE_SUBJECT: Final[str] = "profile.excluded_gameplay_and_replay_parser_semantics"


def allowed_absence_policy_identity_binding_v1() -> dict[str, Any]:
    """Structured allowed-absence policy for ``identity_binding_v1`` (audit artifact field)."""

    return {
        "policy_version": "starlab.m54.allowed_absence_policy.identity_binding_v1",
        "profile_id": PROFILE_IDENTITY_BINDING_V1,
        "allowed_unavailable_by_design": [
            {
                "subject_id": _ALLOWED_UNAVAILABLE_SUBJECT,
                "side": "execution",
                "reason": (
                    "Opaque replay bytes are not stored on M03 execution artifacts; "
                    "replay_content_sha256 is replay-side authoritative per M04."
                ),
            }
        ],
        "allowed_out_of_scope": [
            {
                "subject_id": _ALLOWED_OUT_OF_SCOPE_SUBJECT,
                "side": "n/a",
                "reason": (
                    "Gameplay, parser, timeline, BOE, combat, and canonical-state semantics are "
                    "outside identity_binding_v1 (see M52 charter non-claims)."
                ),
            }
        ],
    }


def resolve_gatepack_id_for_profile(profile_id: str) -> str | None:
    """Map M53 ``profile_id`` to the M54 gate pack that audits it."""

    if profile_id == PROFILE_IDENTITY_BINDING_V1:
        return GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1
    return None


def _row(
    *,
    gate_id: str,
    description: str,
    status: str,
    subject_refs: list[str],
    reason_codes: list[str],
    notes: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "description": description,
        "status": status,
        "subject_refs": subject_refs,
        "reason_codes": reason_codes,
        "notes": notes,
    }


def _entry_map(evidence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for e in evidence.get("evidence_entries", []):
        if isinstance(e, dict) and "subject" in e:
            out[str(e["subject"])] = e
    return out


def _bad_mismatch(entry: dict[str, Any]) -> bool:
    """True if this row is an unexpected ``availability_class=mismatch`` surface."""

    return entry.get("availability_class") == "mismatch"


def evaluate_identity_binding_acceptance_v1(
    *,
    evidence: dict[str, Any],
    evidence_report: dict[str, Any] | None,
    input_evidence_sha256: str,
) -> tuple[list[dict[str, Any]], str, str]:
    """Return ``(gate_results, profile_scope_status, merge_bar_language)``."""

    results: list[dict[str, Any]] = []

    def add(g: dict[str, Any]) -> None:
        results.append(g)

    if not isinstance(evidence, dict):
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.evidence_document",
                description="Evidence JSON must deserialize to an object.",
                status="not_evaluable",
                subject_refs=[],
                reason_codes=["evidence.not_object"],
                notes="Top-level JSON value is not an object.",
            )
        )
        return results, "not_evaluable", "no_profile_scope_decision"

    schema_ver = evidence.get("schema_version")
    add(
        _row(
            gate_id=f"{_GATE_ID_PREFIX}.m53_evidence_schema_recognized",
            description="Evidence contract id (schema_version) matches M53 evidence v1.",
            status="pass"
            if schema_ver == REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION
            else "fail",
            subject_refs=["schema_version"],
            reason_codes=[]
            if schema_ver == REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION
            else ["evidence.schema_version.unrecognized"],
            notes="Expect starlab.replay_execution_equivalence_evidence.v1.",
        )
    )

    charter_id = evidence.get("charter_contract_id")
    add(
        _row(
            gate_id=f"{_GATE_ID_PREFIX}.charter_contract_recognized",
            description="charter_contract_id matches the M52 replay↔execution equivalence charter.",
            status="pass" if charter_id == CHARTER_CONTRACT_ID else "fail",
            subject_refs=["charter_contract_id"],
            reason_codes=[]
            if charter_id == CHARTER_CONTRACT_ID
            else ["charter.contract_id.mismatch"],
            notes=f"Expect {CHARTER_CONTRACT_ID!r}.",
        )
    )

    profile_id = evidence.get("profile_id")
    resolved = resolve_gatepack_id_for_profile(str(profile_id) if profile_id is not None else "")
    if resolved is None:
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.profile_supported_by_m54_gatepack",
                description=(
                    "profile_id is implemented by an M54 gate pack "
                    f"({GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1!r} for identity binding)."
                ),
                status="not_evaluable",
                subject_refs=["profile_id"],
                reason_codes=["profile.not_implemented_in_m54"],
                notes="Unknown or unsupported profile_id for M54 v1 gate packs.",
            )
        )
        # Remaining checks are not meaningful without a known profile.
        _finalize_summary(results)
        return results, "not_evaluable", "no_profile_scope_decision"

    add(
        _row(
            gate_id=f"{_GATE_ID_PREFIX}.gatepack_resolved_for_profile",
            description="Gate pack is selected for the named profile.",
            status="pass",
            subject_refs=["profile_id"],
            reason_codes=[],
            notes=f"Resolved gatepack {resolved!r}.",
        )
    )

    if evidence_report is None:
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.optional_evidence_report_sha256",
                description=(
                    "If an M53 evidence report is supplied, its evidence_canonical_sha256 "
                    "matches the canonical hash of the loaded evidence object."
                ),
                status="not_applicable",
                subject_refs=[],
                reason_codes=["evidence_report.not_provided"],
                notes="No --evidence-report path; cross-check skipped.",
            )
        )
    else:
        rep_schema = evidence_report.get("schema_version")
        rep_ok_schema = rep_schema == REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_REPORT_SCHEMA_VERSION
        rep_sha = evidence_report.get("evidence_canonical_sha256")
        sha_ok = isinstance(rep_sha, str) and rep_sha == input_evidence_sha256
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.optional_evidence_report_sha256",
                description=(
                    "M53 evidence report evidence_canonical_sha256 matches canonical evidence hash."
                ),
                status="pass" if (rep_ok_schema and sha_ok) else "fail",
                subject_refs=["evidence_canonical_sha256"],
                reason_codes=[]
                if (rep_ok_schema and sha_ok)
                else ["evidence_report.sha256_mismatch_or_invalid_schema"],
                notes=(
                    "Expect report schema starlab.replay_execution_equivalence_evidence_report.v1 "
                    "and matching evidence hash."
                ),
            )
        )

    entries = evidence.get("evidence_entries")
    if not isinstance(entries, list):
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.evidence_entries_present",
                description="Evidence contains an evidence_entries array.",
                status="not_evaluable",
                subject_refs=["evidence_entries"],
                reason_codes=["evidence_entries.missing_or_invalid"],
                notes="evidence_entries must be a JSON array.",
            )
        )
        _finalize_summary(results)
        return results, "not_evaluable", "no_profile_scope_decision"

    emap = _entry_map(evidence)

    nc = evidence.get("non_claims")
    add(
        _row(
            gate_id=f"{_GATE_ID_PREFIX}.residual_non_claims_preserved",
            description="M53 non_claims list is present (residual non-claims carried into audit).",
            status="pass" if isinstance(nc, list) and len(nc) > 0 else "fail",
            subject_refs=["non_claims"],
            reason_codes=[] if isinstance(nc, list) and len(nc) > 0 else ["non_claims.missing"],
            notes="Expect a non-empty non_claims array from M53 emission.",
        )
    )

    for subj in _SCHEMA_SUBJECTS:
        ent = emap.get(subj)
        if ent is None:
            add(
                _row(
                    gate_id=f"{_GATE_ID_PREFIX}.schema_row.{subj}",
                    description=f"Evidence entry exists for {subj!r} (governed schema tokens).",
                    status="fail",
                    subject_refs=[subj],
                    reason_codes=["evidence_entry.missing"],
                    notes="Required schema.* evidence row missing.",
                )
            )
            continue
        ok = ent.get("availability_class") == "available" and ent.get("mismatch_kind") is None
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.schema_row.{subj}",
                description=f"Schema token row {subj!r} is available (no mismatch).",
                status="pass" if ok else "fail",
                subject_refs=[subj],
                reason_codes=[] if ok else ["schema.governed_token.mismatch"],
                notes="Governed schema_version tokens must match the profile.",
            )
        )

    for subj in _IDENTITY_CHAIN_SUBJECTS:
        ent = emap.get(subj)
        if ent is None:
            add(
                _row(
                    gate_id=f"{_GATE_ID_PREFIX}.identity_chain.{subj}",
                    description=f"Evidence entry exists for {subj!r}.",
                    status="fail",
                    subject_refs=[subj],
                    reason_codes=["evidence_entry.missing"],
                    notes="Required join / binding evidence row missing.",
                )
            )
            continue
        mk = ent.get("mismatch_kind")
        bad = ent.get("availability_class") == "mismatch" and mk in (
            "identity_mismatch",
            "missing_counterpart",
        )
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.identity_chain.{subj}",
                description=f"No identity_mismatch or missing_counterpart on {subj!r}.",
                status="fail" if bad else "pass",
                subject_refs=[subj],
                reason_codes=[] if not bad else [f"mismatch.{mk}"],
                notes="Identity chain rows must agree under the profile.",
            )
        )

    # Ordered comparison: ordering_mismatch fails; other mismatches fail except handled upstream.
    ent_ord = emap.get(_ORDERED_SUBJECT)
    if ent_ord is None:
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.ordered_parent_references",
                description="parent_references.sequence_equality evidence row exists.",
                status="fail",
                subject_refs=[_ORDERED_SUBJECT],
                reason_codes=["evidence_entry.missing"],
                notes="Required ordered comparison row missing.",
            )
        )
    else:
        mk = ent_ord.get("mismatch_kind")
        bad_ord = ent_ord.get("availability_class") == "mismatch" and mk in (
            "ordering_mismatch",
            "identity_mismatch",
            "missing_counterpart",
            "count_mismatch",
        )
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.ordered_parent_references",
                description=(
                    "No ordering_mismatch (or other disallowed mismatch) on parent_references."
                ),
                status="fail" if bad_ord else "pass",
                subject_refs=[_ORDERED_SUBJECT],
                reason_codes=[] if not bad_ord else [f"mismatch.{mk}"],
                notes="Ordering is significant for this profile entry.",
            )
        )

    ent_u = emap.get(_ALLOWED_UNAVAILABLE_SUBJECT)
    if ent_u is None:
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.replay_content_sha256_policy",
                description="replay.replay_content_sha256 row exists and is unavailable_by_design.",
                status="fail",
                subject_refs=[_ALLOWED_UNAVAILABLE_SUBJECT],
                reason_codes=["evidence_entry.missing"],
                notes="Expected replay-side opaque hash row.",
            )
        )
    else:
        ok = (
            ent_u.get("availability_class") == "unavailable_by_design"
            and ent_u.get("mismatch_kind") is None
        )
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.replay_content_sha256_policy",
                description=(
                    "replay_content_sha256 follows unavailable_by_design "
                    "(execution absence allowed)."
                ),
                status="pass" if ok else "fail",
                subject_refs=[_ALLOWED_UNAVAILABLE_SUBJECT],
                reason_codes=[] if ok else ["replay.hash.policy_violation"],
                notes="Execution side does not store opaque replay bytes (M03).",
            )
        )

    ent_o = emap.get(_ALLOWED_OUT_OF_SCOPE_SUBJECT)
    if ent_o is None:
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.excluded_semantics_out_of_scope",
                description="Excluded semantics row exists and is out_of_scope.",
                status="fail",
                subject_refs=[_ALLOWED_OUT_OF_SCOPE_SUBJECT],
                reason_codes=["evidence_entry.missing"],
                notes="Expected explicit out-of-scope row for gameplay/parser semantics.",
            )
        )
    else:
        ok = (
            ent_o.get("availability_class") == "out_of_scope" and ent_o.get("mismatch_kind") is None
        )
        add(
            _row(
                gate_id=f"{_GATE_ID_PREFIX}.excluded_semantics_out_of_scope",
                description=(
                    "Gameplay/parser semantics row is explicitly out_of_scope (not a failure)."
                ),
                status="pass" if ok else "fail",
                subject_refs=[_ALLOWED_OUT_OF_SCOPE_SUBJECT],
                reason_codes=[] if ok else ["out_of_scope.policy_violation"],
                notes="Profile excludes broad replay semantics by design.",
            )
        )

    # No unexpected mismatch rows: every entry must either be clean, or match allowed policy rows.
    unexpected: list[str] = []
    for subj, ent in sorted(emap.items()):
        if subj in {_ALLOWED_UNAVAILABLE_SUBJECT, _ALLOWED_OUT_OF_SCOPE_SUBJECT}:
            continue
        if _bad_mismatch(ent):
            unexpected.append(subj)

    add(
        _row(
            gate_id=f"{_GATE_ID_PREFIX}.no_disallowed_mismatch_rows",
            description=(
                "No unexpected availability_class=mismatch rows outside allowed policy subjects."
            ),
            status="pass" if not unexpected else "fail",
            subject_refs=unexpected,
            reason_codes=["mismatch.unexpected_rows"] if unexpected else [],
            notes="Surfaces any residual mismatch rows not covered by explicit gates.",
        )
    )

    profile_status, merge_bar = _derive_verdicts(results)
    _finalize_summary(results)
    return results, profile_status, merge_bar


def _finalize_summary(results: list[dict[str, Any]]) -> None:
    """Stable ordering for deterministic JSON."""

    results.sort(key=lambda r: r["gate_id"])


def _derive_verdicts(gate_results: list[dict[str, Any]]) -> tuple[str, str]:
    statuses = [str(g["status"]) for g in gate_results]
    if "fail" in statuses:
        return "rejected_within_profile_scope", "would_block_profile_scope_gate"
    if "not_evaluable" in statuses:
        return "not_evaluable", "no_profile_scope_decision"
    return "accepted_within_profile_scope", "would_clear_profile_scope_gate"


def preview_identity_binding_evidence_sha256(evidence: dict[str, Any]) -> str:
    """Canonical SHA-256 of evidence object (for tests and report cross-check)."""

    return sha256_hex_of_canonical_json(evidence)
