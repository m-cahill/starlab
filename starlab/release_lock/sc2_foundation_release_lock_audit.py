"""Evaluate SC2 foundation v1 proof pack → release-lock audit JSON + report (M61)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.release_lock.release_lock_models import (
    AUDIT_CONTRACT_V1,
    AUDIT_REPORT_CONTRACT_V1,
    CAMPAIGN_LENGTH_OPERATOR_FULL_RUN,
    M61_AUDIT_REQUIRED_NON_CLAIM_MARKERS,
    PROOF_PACK_CONTRACT_V1,
    RELEASE_SCOPE_NOT_EVALUABLE,
    RELEASE_SCOPE_NOT_READY,
    RELEASE_SCOPE_READY,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def load_proof_pack(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("proof pack must be a JSON object")
    return data


def verify_proof_pack_integrity(obj: dict[str, Any]) -> tuple[bool, str]:
    """Return (ok, message) comparing embedded proof_pack_sha256 to canonical JSON hash."""

    declared = obj.get("proof_pack_sha256")
    if not isinstance(declared, str) or len(declared) != 64:
        return False, "missing_or_invalid_proof_pack_sha256"
    body = {k: v for k, v in obj.items() if k != "proof_pack_sha256"}
    calc = sha256_hex_of_canonical_json(body)
    if calc != declared:
        return False, f"sha256_mismatch expected={declared} computed={calc}"
    return True, "ok"


def build_sc2_foundation_release_lock_audit_bundle(
    proof_pack: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (audit.json body, audit_report.json body)."""

    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append(
            {"check_id": check_id, "detail": detail, "passed": bool(passed)},
        )

    integrity_ok, integrity_msg = verify_proof_pack_integrity(proof_pack)
    add("proof_pack_sha256_self_consistent", integrity_ok, integrity_msg)

    contract_ok = proof_pack.get("contract_id") == PROOF_PACK_CONTRACT_V1
    add("proof_pack_contract_id", contract_ok, str(proof_pack.get("contract_id")))

    non_claims = proof_pack.get("non_claims")
    nc_set = set(non_claims) if isinstance(non_claims, list) else set()
    req_nc = True
    missing_nc: list[str] = []
    for marker in M61_AUDIT_REQUIRED_NON_CLAIM_MARKERS:
        if marker not in nc_set:
            req_nc = False
            missing_nc.append(marker)
    add(
        "explicit_non_claims_minimum_set",
        req_nc,
        "missing: " + ", ".join(missing_nc) if missing_nc else "ok",
    )

    decl = proof_pack.get("campaign_threshold_declaration")
    decl_ok = (
        isinstance(decl, dict)
        and decl.get("campaign_length_class") == CAMPAIGN_LENGTH_OPERATOR_FULL_RUN
        and decl.get("threshold_satisfied") is True
    )
    add(
        "operator_declared_full_run_threshold_satisfied",
        decl_ok,
        "campaign_threshold_declaration must declare operator_declared_full_run with "
        "threshold_satisfied true",
    )

    cre = proof_pack.get("campaign_release_evidence")
    derived_ok = isinstance(cre, dict)
    derived = cre.get("campaign_run_derived") if isinstance(cre, dict) else None
    post_boot = (
        isinstance(derived, dict)
        and derived.get("post_bootstrap_protocol_phases_enabled") is True
    )
    add(
        "post_bootstrap_protocol_phases_executed",
        bool(derived_ok and post_boot),
        "post_bootstrap_protocol_phases_enabled must be true on the campaign run",
    )

    watch_ok = (
        isinstance(derived, dict) and derived.get("watchable_m44_phase_executed") is True
    )
    add(
        "watchable_m44_validation_executed",
        bool(watch_ok),
        "watchable_m44_validation phase receipt must report executed true",
    )

    # Tie-break: M44 validation summary should exist with a final_status when available
    wv = cre.get("watchable_validation_summary") if isinstance(cre, dict) else None
    m44_fs_ok = isinstance(wv, dict) and isinstance(wv.get("final_status"), str)
    add(
        "watchable_m44_has_final_status",
        m44_fs_ok,
        "watchable_validation_summary.final_status should be present from match_execution",
    )

    if not integrity_ok or not contract_ok:
        scope = RELEASE_SCOPE_NOT_EVALUABLE
        lang = "release_lock_not_evaluable_proof_pack_malformed_or_untrusted"
    else:
        hard_fail = (
            not req_nc
            or not decl_ok
            or not post_boot
            or not watch_ok
            or not m44_fs_ok
        )
        if hard_fail:
            scope = RELEASE_SCOPE_NOT_READY
            lang = "release_lock_not_ready_within_explicit_m61_scope"
        else:
            scope = RELEASE_SCOPE_READY
            lang = "release_lock_ready_within_m61_declared_scope_and_non_claims"

    audit_body: dict[str, Any] = {
        "campaign_evidence_status": (
            "satisfied" if (post_boot and watch_ok and m44_fs_ok) else "incomplete_or_blocked"
        ),
        "contract_id": AUDIT_CONTRACT_V1,
        "proof_pack_sha256": proof_pack.get("proof_pack_sha256"),
        "release_scope_id": proof_pack.get("release_scope_id"),
        "release_scope_status": scope,
        "required_evidence_checks": sorted(checks, key=lambda c: str(c["check_id"])),
        "unresolved_gaps": proof_pack.get("unresolved_gaps")
        if isinstance(proof_pack.get("unresolved_gaps"), list)
        else [],
        "watchability_status": (
            "replay_backed_validation_present"
            if watch_ok and m44_fs_ok
            else "blocked_or_incomplete"
        ),
    }
    audit_sha = sha256_hex_of_canonical_json(audit_body)
    audit_out = {**audit_body, "audit_sha256": audit_sha}

    report: dict[str, Any] = {
        "contract_id": AUDIT_REPORT_CONTRACT_V1,
        "referenced_audit_sha256": audit_sha,
        "release_lock_language": lang,
        "release_scope_status": scope,
        "summary": {
            "audit_sha256": audit_sha,
            "proof_pack_sha256": proof_pack.get("proof_pack_sha256"),
        },
    }
    return audit_out, report


def write_sc2_foundation_release_lock_audit_artifacts(
    *,
    proof_pack_path: Path,
    output_dir: Path,
) -> tuple[Path, Path]:
    pack = load_proof_pack(proof_pack_path)
    audit, report = build_sc2_foundation_release_lock_audit_bundle(pack)
    output_dir.mkdir(parents=True, exist_ok=True)
    from starlab.release_lock.release_lock_models import AUDIT_FILENAME, AUDIT_REPORT_FILENAME

    a_path = output_dir / AUDIT_FILENAME
    r_path = output_dir / AUDIT_REPORT_FILENAME
    a_path.write_text(canonical_json_dumps(audit), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return a_path, r_path
