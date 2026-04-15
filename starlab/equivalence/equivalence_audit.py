"""Deterministic replay↔execution equivalence audit payloads (M54 — consumes M53 evidence)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.equivalence.equivalence_gatepacks import (
    allowed_absence_policy_identity_binding_v1,
    evaluate_identity_binding_acceptance_v1,
    preview_identity_binding_evidence_sha256,
    resolve_gatepack_id_for_profile,
)
from starlab.equivalence.equivalence_models import (
    AUDIT_FILENAME,
    AUDIT_REPORT_FILENAME,
    AUDIT_RUNTIME_CONTRACT_REL_PATH,
    GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1,
    REPLAY_EXECUTION_EQUIVALENCE_AUDIT_REPORT_SCHEMA_VERSION,
    REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_evidence_object(path: Path) -> dict[str, Any]:
    """Load evidence JSON; must be a top-level object."""

    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = "evidence JSON top-level value must be an object"
        raise ValueError(msg)
    return obj


def load_evidence_report_object(path: Path) -> dict[str, Any]:
    """Load M53 evidence report JSON; must be a top-level object."""

    raw = path.read_text(encoding="utf-8")
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        msg = "evidence report JSON top-level value must be an object"
        raise ValueError(msg)
    return obj


def _count_gate_statuses(gate_results: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for g in gate_results:
        st = str(g.get("status", "unknown"))
        out[st] = out.get(st, 0) + 1
    return dict(sorted(out.items()))


def build_replay_execution_equivalence_audit_bundle(
    *,
    evidence: dict[str, Any],
    evidence_report: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Emit audit + audit report from in-memory M53 evidence (and optional M53 report)."""

    input_sha = preview_identity_binding_evidence_sha256(evidence)
    gate_results, profile_scope_status, merge_bar_language = (
        evaluate_identity_binding_acceptance_v1(
            evidence=evidence,
            evidence_report=evidence_report,
            input_evidence_sha256=input_sha,
        )
    )
    profile_id = evidence.get("profile_id")
    gatepack_id = resolve_gatepack_id_for_profile(str(profile_id) if profile_id is not None else "")
    policy: dict[str, Any] | None
    if gatepack_id == GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1:
        policy = allowed_absence_policy_identity_binding_v1()
    else:
        policy = None

    base_nc = evidence.get("non_claims")
    merged_nc: list[str] = []
    if isinstance(base_nc, list):
        merged_nc.extend(str(x) for x in base_nc)
    merged_nc.extend(
        [
            (
                "Replay↔execution equivalence is not proved globally; "
                "this audit is profile-scoped only."
            ),
            ("Does not assert benchmark integrity, live SC2 in CI, or ladder/public performance."),
            (
                "merge_bar_language is descriptive metadata only; "
                "it does not change repository branch protection."
            ),
        ]
    )

    summary_counts = _count_gate_statuses(gate_results)
    audit: dict[str, Any] = {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION,
        "milestone": "M54",
        "audit_contract_id": REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION,
        "runtime_contract": AUDIT_RUNTIME_CONTRACT_REL_PATH,
        "evidence_contract_id": evidence.get("schema_version"),
        "charter_contract_id": evidence.get("charter_contract_id"),
        "profile_id": profile_id,
        "profile_version": evidence.get("profile_version"),
        "gatepack_id": gatepack_id,
        "input_evidence_sha256": input_sha,
        "profile_scope_status": profile_scope_status,
        "merge_bar_language": merge_bar_language,
        "gate_results": gate_results,
        "allowed_absence_policy": policy,
        "residual_non_claims": merged_nc,
        "summary_counts": summary_counts,
    }
    report = build_replay_execution_equivalence_audit_report(audit_obj=audit)
    return audit, report


def build_replay_execution_equivalence_audit_report(*, audit_obj: dict[str, Any]) -> dict[str, Any]:
    audit_sha = sha256_hex_of_canonical_json(audit_obj)
    return {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_AUDIT_REPORT_SCHEMA_VERSION,
        "milestone": "M54",
        "audit_canonical_sha256": audit_sha,
        "audit_artifact": AUDIT_FILENAME,
        "report_artifact": AUDIT_REPORT_FILENAME,
        "emitter_module": "starlab.equivalence.emit_replay_execution_equivalence_audit",
        "profile_id": audit_obj.get("profile_id"),
        "gatepack_id": audit_obj.get("gatepack_id"),
        "profile_scope_status": audit_obj.get("profile_scope_status"),
        "merge_bar_language": audit_obj.get("merge_bar_language"),
        "gate_results_summary": audit_obj.get("summary_counts"),
        "residual_non_claims": audit_obj.get("residual_non_claims"),
        "notes": (
            "Bounded audit over M53 evidence JSON; not a universal equivalence theorem; "
            "not a repository merge gate."
        ),
    }
