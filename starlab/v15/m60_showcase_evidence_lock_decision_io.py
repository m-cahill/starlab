"""V15-M60 — deterministic showcase-evidence lock decision IO."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.m59_adapter_smoke_readout_models import (
    READOUT_BENCHMARK_NOT_EVIDENCE,
    SCHEMA_VERSION_READOUT,
)
from starlab.v15.m60_showcase_evidence_lock_decision_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CONTRACT_ID,
    CONTRACT_ID_M53,
    CONTRACT_ID_M54,
    CONTRACT_ID_M55,
    CONTRACT_ID_M56,
    CONTRACT_ID_M56A,
    CONTRACT_ID_M57,
    CONTRACT_ID_M57A,
    CONTRACT_ID_M58,
    CONTRACT_ID_REPORT,
    DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED,
    DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
    FILENAME_DECISION_JSON,
    LOCK_CLASS_BOUNDED_SHOWCASE,
    LOCK_CLASS_NO_LOCK_MISSING_EVIDENCE,
    LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY,
    MILESTONE,
    NEXT_MILESTONE_M61,
    NEXT_ROUTE_M60_REMEDIATION,
    NEXT_ROUTE_M61_RELEASE_LOCK,
    NON_CLAIMS,
    PROFILE_ID,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    STATUS_CLOSED,
    STRONGEST_ALLOWED_CLAIM_LOCK,
)

_FORBIDDEN_DECLARED_KEYS: Final[tuple[str, ...]] = (
    "checkpoint_path",
    "private_path",
    "operator_absolute_path",
    "company_secrets",
)

_DEFAULT_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "benchmark_passed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "ladder_public_performance_claim_authorized": False,
    "human_panel_claim_authorized": False,
    "showcase_evidence_lock_recommended": True,
    "release_lock_executed": False,
    "seventy_two_hour_authorized": False,
    "v2_authorized": False,
    "v2_recharter_authorized": False,
}

_REMEDIATE_CLAIM_FLAGS: Final[dict[str, bool]] = {
    "benchmark_passed": False,
    "strength_evaluated": False,
    "checkpoint_promoted": False,
    "ladder_public_performance_claim_authorized": False,
    "human_panel_claim_authorized": False,
    "showcase_evidence_lock_recommended": False,
    "release_lock_executed": False,
    "seventy_two_hour_authorized": False,
    "v2_authorized": False,
    "v2_recharter_authorized": False,
}


def _fixture_upstream_evidence() -> dict[str, Any]:
    return {
        "m53_12_hour_training_execution": {
            "status": STATUS_CLOSED,
            "evidence_class": "training_execution_evidence_only",
            "contract_id_declared_public": CONTRACT_ID_M53,
            "artifact_sha256": CANONICAL_M53_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        },
        "m54_package_readiness": {
            "status": STATUS_CLOSED,
            "evidence_class": "package_and_readiness_routing_only",
            "contract_id_declared_public": CONTRACT_ID_M54,
            "artifact_sha256": CANONICAL_M54_PACKAGE_SHA256,
        },
        "m55_preflight": {
            "status": STATUS_CLOSED,
            "evidence_class": "structural_preflight_only",
            "contract_id_declared_public": CONTRACT_ID_M55,
        },
        "m56_readout": {
            "status": STATUS_CLOSED,
            "evidence_class": "bounded_readout_only",
            "contract_id_declared_public": CONTRACT_ID_M56,
        },
        "m56a_visual_watch": {
            "status": STATUS_CLOSED,
            "evidence_class": "watchability_observation_only",
            "contract_id_declared_public": CONTRACT_ID_M56A,
        },
        "m57a_visual_watch": {
            "status": STATUS_CLOSED,
            "evidence_class": "watchability_observation_only",
            "contract_id_declared_public": CONTRACT_ID_M57A,
        },
        "m57_charter": {
            "status": STATUS_CLOSED,
            "evidence_class": "charter_dry_run_only",
            "contract_id_declared_public": CONTRACT_ID_M57,
        },
        "m58_adapter_smoke": {
            "status": STATUS_CLOSED,
            "evidence_class": "bounded_adapter_smoke_only",
            "contract_id_declared_public": CONTRACT_ID_M58,
        },
        "m59_readout_refusal": {
            "status": STATUS_CLOSED,
            "evidence_class": "benchmark_overclaim_refusal",
            "contract_id_declared_public": SCHEMA_VERSION_READOUT,
        },
    }


def evaluate_lock_gates(
    *,
    upstream: dict[str, Any],
    overclaim_blocked: bool,
) -> tuple[bool, list[str]]:
    """Return (all gates pass, list of failing gate IDs)."""

    violations: list[str] = []

    req = (
        ("m53_12_hour_training_execution", "training_execution_evidence_only"),
        ("m54_package_readiness", "package_and_readiness_routing_only"),
        ("m55_preflight", "structural_preflight_only"),
        ("m56_readout", "bounded_readout_only"),
        ("m59_readout_refusal", "benchmark_overclaim_refusal"),
    )
    visual_ok = False
    m56a = upstream.get("m56a_visual_watch")
    if isinstance(m56a, dict) and m56a.get("status") == STATUS_CLOSED:
        visual_ok = True
    m57a = upstream.get("m57a_visual_watch")
    if isinstance(m57a, dict) and m57a.get("status") == STATUS_CLOSED:
        visual_ok = True
    if not visual_ok:
        violations.append("G4_missing_visual_watchability_evidence")

    for key, ev_class in req:
        u = upstream.get(key)
        if not isinstance(u, dict):
            violations.append(f"missing_upstream_block:{key}")
            continue
        if u.get("status") != STATUS_CLOSED:
            violations.append(f"not_closed:{key}")
        if str(u.get("evidence_class") or "") != ev_class:
            violations.append(f"evidence_class_mismatch:{key}")

    optional = (
        ("m57_charter", "charter_dry_run_only"),
        ("m58_adapter_smoke", "bounded_adapter_smoke_only"),
    )
    for key, ev_class in optional:
        u = upstream.get(key)
        if not isinstance(u, dict):
            violations.append(f"missing_upstream_block:{key}")
            continue
        if u.get("status") != STATUS_CLOSED:
            violations.append(f"not_closed:{key}")
        if str(u.get("evidence_class") or "") != ev_class:
            violations.append(f"evidence_class_mismatch:{key}")

    m53 = upstream.get("m53_12_hour_training_execution")
    if isinstance(m53, dict):
        cand = str(m53.get("candidate_checkpoint_sha256") or "").strip().lower()
        if cand != CANONICAL_CANDIDATE_CHECKPOINT_SHA256:
            violations.append("G2_candidate_binding_mismatch_m53")

    m54 = upstream.get("m54_package_readiness")
    if isinstance(m54, dict):
        art = str(m54.get("artifact_sha256") or "").strip().lower()
        if art != CANONICAL_M54_PACKAGE_SHA256:
            violations.append("G2_m54_package_sha_mismatch")

    if overclaim_blocked:
        violations.append("G7_overclaim_flag_true_fixture_guard")

    if violations:
        return False, sorted(violations)
    return True, []


def build_lock_recommended_body(
    *,
    upstream_evidence: dict[str, Any],
    gate_evaluation: tuple[bool, list[str]],
) -> dict[str, Any]:
    gates_ok, failures = gate_evaluation
    assert gates_ok and not failures

    locks = dict(_DEFAULT_CLAIM_FLAGS)
    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_ID,
        "milestone": MILESTONE,
        "decision_status": DECISION_STATUS_SHOWCASE_LOCK_RECOMMENDED,
        "lock_class": LOCK_CLASS_BOUNDED_SHOWCASE,
        "upstream_evidence": upstream_evidence,
        "gate_evaluation": {
            "all_gates_passed": True,
            "violations_sorted": [],
            "public_private_boundary_intact": True,
            "m61_route_scope_release_lock_proof_pack_only": True,
        },
        "lock_decision": {
            "v15_lock_recommended": True,
            "release_lock_allowed_in_m60": False,
            "next_milestone": NEXT_MILESTONE_M61,
            "next_route": NEXT_ROUTE_M61_RELEASE_LOCK,
            "next_route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "lock_scope": LOCK_SCOPE_BOUNDED_SHOWCASE_ONLY,
        },
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_LOCK,
        "claim_flags": locks,
        "non_claims": list(NON_CLAIMS),
    }
    return body


def build_continue_remediate_body(
    *,
    violations: list[str],
    upstream_evidence: dict[str, Any],
    reason_primary: str,
) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_ID,
        "milestone": MILESTONE,
        "decision_status": DECISION_STATUS_CONTINUE_REMEDIATE_RECOMMENDED,
        "lock_class": LOCK_CLASS_NO_LOCK_MISSING_EVIDENCE,
        "upstream_evidence": upstream_evidence,
        "gate_evaluation": {
            "all_gates_passed": False,
            "violations_sorted": sorted(violations),
        },
        "lock_decision": {
            "v15_lock_recommended": False,
            "release_lock_allowed_in_m60": False,
            "next_milestone": "V15-M60A",
            "next_route": NEXT_ROUTE_M60_REMEDIATION,
            "next_route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "remediation_primary_reason": reason_primary,
        },
        "strongest_allowed_claim": (
            "V15-M60 routes to remediation: upstream closure or governance gate failed "
            "for a bounded showcase-evidence lock recommendation."
        ),
        "claim_flags": dict(_REMEDIATE_CLAIM_FLAGS),
        "non_claims": list(NON_CLAIMS),
    }


def validate_m59_readout_blob(blob: dict[str, Any]) -> tuple[bool, str]:
    if str(blob.get("milestone") or "") != "V15-M59":
        return False, "m59 milestone mismatch"
    if str(blob.get("schema_version") or "") != SCHEMA_VERSION_READOUT:
        return False, "m59 schema_version mismatch"
    ro = blob.get("readout")
    if not isinstance(ro, dict):
        return False, "m59 readout missing"
    if str(ro.get("benchmark_status") or "") != READOUT_BENCHMARK_NOT_EVIDENCE:
        return False, "m59 benchmark_status must refuse benchmark-as-evidence"
    rc = blob.get("refused_claims")
    if not isinstance(rc, dict):
        return False, "m59 refused_claims missing"
    bp = rc.get("benchmark_pass_claim")
    if bp is not True:
        return False, "m59 must refuse benchmark_pass_claim"
    return True, ""


def load_and_validate_m59_path(path: Path) -> tuple[bool, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, str(exc)
    if not isinstance(raw, dict):
        return False, "m59 json root must be object"
    return validate_m59_readout_blob(raw)


def declared_metadata_forbidden(blob: dict[str, Any]) -> str | None:
    """Return error string if forbidden keys/strings appear."""

    def walk(obj: object) -> str | None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                lk = str(k).lower()
                if any(fk in lk for fk in _FORBIDDEN_DECLARED_KEYS):
                    return f"forbidden key in declared metadata: {k!r}"
                err = walk(v)
                if err:
                    return err
        elif isinstance(obj, list):
            for item in obj:
                err = walk(item)
                if err:
                    return err
        elif isinstance(obj, str):
            low = obj.lower()
            if "company_secrets" in low:
                return "declared metadata must not reference company_secrets"
            if "..\\" in obj or "../" in obj:
                return "declared metadata must not contain path traversal"
        return None

    return walk(blob)


def validate_operator_declared_ack(blob: dict[str, Any]) -> tuple[bool, str]:
    if set(blob.keys()) != {"m53_m59_public_closure_acknowledged"}:
        return (
            False,
            "declared metadata must contain only {'m53_m59_public_closure_acknowledged': true}",
        )
    if blob.get("m53_m59_public_closure_acknowledged") is not True:
        return False, "closure acknowledgement must be true"
    err = declared_metadata_forbidden(blob)
    if err:
        return False, err
    return True, ""


def build_decision_report(
    decision_body: dict[str, Any],
    *,
    m59_digest: str | None = None,
) -> dict[str, Any]:
    rep: dict[str, Any] = {
        "contract_id": CONTRACT_ID_REPORT,
        "milestone": MILESTONE,
        "decision_status": decision_body.get("decision_status"),
        "lock_class": decision_body.get("lock_class"),
        "summary": {
            "lock_decision": decision_body.get("lock_decision"),
            "claim_flags": decision_body.get("claim_flags"),
            "strongest_allowed_claim": decision_body.get("strongest_allowed_claim"),
            "gate_evaluation": decision_body.get("gate_evaluation"),
        },
        "non_claims": decision_body.get("non_claims"),
        "non_claim_inventory": (
            "no_benchmark_execution no_strength no_promotion "
            "no_human_panel_claim no_release_lock_here no_72h no_v2"
        ).split(),
        "decision_canonical_sha256": sha256_hex_of_canonical_json(decision_body),
    }
    if m59_digest:
        rep["validated_m59_readout_canonical_sha256"] = m59_digest
    return rep


def write_decision_artifacts(
    output_dir: Path,
    *,
    body: dict[str, Any],
    m59_digest: str | None = None,
) -> tuple[Path, Path]:
    out = output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    decision_p = out / FILENAME_DECISION_JSON
    report_p = out / REPORT_FILENAME
    decision_p.write_text(canonical_json_dumps(body), encoding="utf-8")
    report_p.write_text(
        canonical_json_dumps(build_decision_report(body, m59_digest=m59_digest)),
        encoding="utf-8",
    )
    return decision_p, report_p


def build_fixture_decision_body() -> dict[str, Any]:
    up = _fixture_upstream_evidence()
    ok, fails = evaluate_lock_gates(upstream=up, overclaim_blocked=False)
    return build_lock_recommended_body(
        upstream_evidence=up,
        gate_evaluation=(ok, fails),
    )
