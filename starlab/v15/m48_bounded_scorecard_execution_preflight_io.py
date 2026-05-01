"""V15-M48 — bounded scorecard execution preflight / evidence gate.

Consumes sealed M47 upstream artifacts only (no recursive M46/M45 adjudication).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_io import emit_m47_fixture_ci
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    CONTRACT_ID_M47_SURFACE as UPSTREAM_CONTRACT_M47,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    FILENAME_MAIN_JSON as M47_FILENAME,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    M47_ALWAYS_FALSE_KEYS,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    PROFILE_M47_REFUSAL_GATE as UPSTREAM_PROFILE_M47,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED as M47_ROUTE_STATUS,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    STATUS_DESIGN_READY as M47_READY,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    STATUS_DESIGN_READY_WARNINGS as M47_READY_WARNINGS,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
    STATUS_DESIGN_REFUSED as M47_DESIGN_REFUSED,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    ALLOWED_CLAIM_DECISION_VALUES,
    BRIEF_FILENAME,
    CLAIM_BENCHMARK_REFUSED,
    CLAIM_PROMOTION_REFUSED,
    CLAIM_SCORECARD_REFUSED,
    CLAIM_STRENGTH_REFUSED,
    CLAIM_TOTAL_REFUSED,
    CONTRACT_ID_M48_PREFLIGHT,
    DIGEST_FIELD,
    EMITTER_MODULE_M48,
    EVIDENCE_MANIFEST_CONTRACT_ID,
    EVIDENCE_MODE_FIXTURE,
    EVIDENCE_MODE_OPERATOR_MANIFEST,
    FILENAME_MAIN_JSON,
    FIXTURE_MANIFEST_SHA_PLACEHOLDER,
    FORBIDDEN_FLAG_TO_REFUSAL,
    FORBIDDEN_MANIFEST_KEYS,
    GATE_INCOMPLETE,
    GATE_INVALID,
    GATE_SATISFIED,
    INTERPRETATION_M47_BINDING,
    M47_BODY_BOOL_KEYS,
    M48_ALWAYS_FALSE_KEYS,
    MILESTONE_LABEL_M48,
    NON_CLAIMS_M48,
    PROFILE_FIXTURE_CI,
    PROFILE_M48_EVIDENCE_GATE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_DECLARED_SHAPE,
    REFUSED_INVALID_M47,
    REFUSED_M47_FUTURE_SURFACE_ALLOWED,
    REFUSED_M47_FUTURE_SURFACE_NOT_SEPARATE,
    REFUSED_M47_HONESTY,
    REFUSED_M47_NOT_READY,
    REFUSED_M47_ROUTE_EXECUTED,
    REFUSED_M47_SCORECARD_PRESENT,
    REFUSED_MISSING_M47,
    REFUSED_REQUIRED_EVIDENCE_INVALID,
    REFUSED_REQUIRED_EVIDENCE_MISSING,
    REFUSED_SCORECARD_RESULTS_CLAIM,
    REFUSED_SCORECARD_TOTAL_CLAIM,
    REPORT_FILENAME,
    REQ_E0,
    REQ_E1,
    REQ_E2,
    REQ_E3,
    REQ_E4,
    REQ_E5,
    REQ_E6,
    REQ_E7,
    REQ_E8,
    REQ_E9,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_EVIDENCE_GAP,
    ROUTE_TO_M47_REMEDIATION,
    ROUTE_TO_SCORECARD_EXEC_SURFACE,
    SCHEMA_VERSION,
    SEMANTIC_SCOPE_REQ,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
    STATUS_PREFLIGHT_REFUSED,
    STATUS_REQUIRED_INVALID,
    STATUS_REQUIRED_MISSING,
    STATUS_REQUIRED_PRESENT,
)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def structural_m47_issues_for_m48(
    m47: dict[str, Any],
    *,
    require_canonical_seal: bool,
) -> list[str]:
    errs: list[str] = []
    if str(m47.get("contract_id", "")) != UPSTREAM_CONTRACT_M47:
        errs.append("m47_contract_id_mismatch")
    if str(m47.get("profile_id", "")) != UPSTREAM_PROFILE_M47:
        errs.append("m47_profile_id_mismatch")
    if require_canonical_seal and not _seal_ok(m47):
        errs.append("m47_seal_invalid")
    return errs


def honesty_violation_m47_body(m47: dict[str, Any]) -> bool:
    return any(m47.get(k) is True for k in M47_ALWAYS_FALSE_KEYS)


def _route_status_m47(m47: dict[str, Any]) -> str:
    rr = m47.get("route_recommendation")
    if not isinstance(rr, dict):
        return ""
    return str(rr.get("route_status") or "")


def _design_status_str(m47: dict[str, Any]) -> str:
    return str(m47.get("design_status") or "")


def _surface_design(m47: dict[str, Any]) -> dict[str, Any] | None:
    sd = m47.get("scorecard_surface_design")
    return sd if isinstance(sd, dict) else None


def surface_issues_for_m48(m47: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    sd = _surface_design(m47)
    if sd is None:
        errs.append("scorecard_surface_design_missing_or_invalid")
        return errs
    if str(sd.get("surface_status") or "") != "designed_not_executed":
        errs.append("m47_surface_status_not_designed_not_executed")
    if sd.get("future_result_surface_allowed_in_m47") is not False:
        errs.append("future_result_surface_allowed_in_m47_not_false")
    if sd.get("future_result_surface_requires_separate_milestone") is not True:
        errs.append("future_result_surface_requires_separate_milestone_not_true")
    return errs


def forbidden_keys_present(obj: Any, *, root: bool = True) -> list[str]:
    """Return forbidden keys found anywhere in nested dict/list JSON."""
    found: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in FORBIDDEN_MANIFEST_KEYS:
                found.append(k)
            found.extend(forbidden_keys_present(v, root=False))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(forbidden_keys_present(item, root=False))
    return found


def _sha_like(v: object) -> bool:
    if not isinstance(v, str):
        return False
    s = v.strip().lower()
    return len(s) == 64 and all(c in "0123456789abcdef" for c in s)


def _binding_sha_ok(block: object) -> bool:
    if not isinstance(block, dict):
        return False
    return _sha_like(block.get("artifact_sha256"))


def build_fixture_evidence_manifest() -> dict[str, Any]:
    h = FIXTURE_MANIFEST_SHA_PLACEHOLDER
    return {
        "contract_id": EVIDENCE_MANIFEST_CONTRACT_ID,
        "candidate_checkpoint_sha256": h,
        "benchmark_protocol_binding": {"artifact_sha256": h},
        "execution_receipt_binding": {"artifact_sha256": h},
        "match_or_episode_evidence_bindings": [{"artifact_sha256": h}],
        "threshold_policy_binding": {"artifact_sha256": h},
        "scorecard_metric_schema": {"declared_metric_groups": ["fixture_structural_placeholder"]},
        "failure_mode_schema": {"declared_failure_modes": ["fixture_structural_placeholder"]},
        "public_private_boundary": {"status": "declared"},
        "non_claims": [
            "not_scorecard_execution_evidence",
            "not_benchmark_pass_fail_result",
        ],
    }


def evaluate_evidence_manifest(manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    """Return (requirement rows, refusal codes)."""
    refs: list[str] = []
    reqs: list[dict[str, Any]] = []

    fk = forbidden_keys_present(manifest)
    if fk:
        refs.append(REFUSED_SCORECARD_RESULTS_CLAIM)

    def row(rid: str, status: str) -> dict[str, Any]:
        return {
            "requirement_id": rid,
            "status": status,
            "semantic_scope": SEMANTIC_SCOPE_REQ,
        }

    cid_ok = str(manifest.get("contract_id") or "") == EVIDENCE_MANIFEST_CONTRACT_ID
    reqs.append(row(REQ_E0, STATUS_REQUIRED_PRESENT if cid_ok else STATUS_REQUIRED_INVALID))
    if not cid_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_INVALID)

    ck_ok = _sha_like(manifest.get("candidate_checkpoint_sha256"))
    reqs.append(row(REQ_E1, STATUS_REQUIRED_PRESENT if ck_ok else STATUS_REQUIRED_MISSING))
    if not ck_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    b_ok = _binding_sha_ok(manifest.get("benchmark_protocol_binding"))
    reqs.append(row(REQ_E2, STATUS_REQUIRED_PRESENT if b_ok else STATUS_REQUIRED_MISSING))
    if not b_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    e_ok = _binding_sha_ok(manifest.get("execution_receipt_binding"))
    reqs.append(row(REQ_E3, STATUS_REQUIRED_PRESENT if e_ok else STATUS_REQUIRED_MISSING))
    if not e_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    meb = manifest.get("match_or_episode_evidence_bindings")
    me_ok = False
    if isinstance(meb, list) and len(meb) > 0:
        me_ok = all(isinstance(x, dict) and _sha_like(x.get("artifact_sha256")) for x in meb)
    st_me = STATUS_REQUIRED_PRESENT if me_ok else STATUS_REQUIRED_MISSING
    reqs.append(row(REQ_E4, st_me))
    if not me_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    sms = manifest.get("scorecard_metric_schema")
    sms_ok = isinstance(sms, (dict, list)) and (
        (isinstance(sms, dict) and len(sms) > 0) or (isinstance(sms, list) and len(sms) > 0)
    )
    reqs.append(
        row(REQ_E5, STATUS_REQUIRED_PRESENT if sms_ok else STATUS_REQUIRED_MISSING),
    )
    if not sms_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    tpb = manifest.get("threshold_policy_binding")
    t_ok = _binding_sha_ok(tpb)
    reqs.append(row(REQ_E6, STATUS_REQUIRED_PRESENT if t_ok else STATUS_REQUIRED_MISSING))
    if not t_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    ppb = manifest.get("public_private_boundary")
    pp_ok = isinstance(ppb, dict) and bool(ppb.get("status"))
    reqs.append(row(REQ_E7, STATUS_REQUIRED_PRESENT if pp_ok else STATUS_REQUIRED_MISSING))
    if not pp_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    fms = manifest.get("failure_mode_schema")
    f_ok = isinstance(fms, (dict, list)) and (
        (isinstance(fms, dict) and len(fms) > 0) or (isinstance(fms, list) and len(fms) > 0)
    )
    reqs.append(row(REQ_E8, STATUS_REQUIRED_PRESENT if f_ok else STATUS_REQUIRED_MISSING))
    if not f_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    nc = manifest.get("non_claims")
    nc_ok = False
    if isinstance(nc, list) and nc:
        texts = [str(x).lower() for x in nc]
        nc_ok = any("scorecard" in t or "benchmark" in t for t in texts)
    reqs.append(row(REQ_E9, STATUS_REQUIRED_PRESENT if nc_ok else STATUS_REQUIRED_MISSING))
    if not nc_ok:
        refs.append(REFUSED_REQUIRED_EVIDENCE_MISSING)

    return reqs, refs


def _m47_binding_summary(m47: dict[str, Any] | None) -> dict[str, Any]:
    if m47 is None:
        return {
            "contract_id": None,
            "profile_id": None,
            "artifact_sha256": None,
            "design_status": None,
            "surface_status": None,
            "future_result_surface_allowed_in_m47": None,
            "interpretation": INTERPRETATION_M47_BINDING,
        }
    sd = _surface_design(m47)
    surf = str(sd.get("surface_status") or "") if sd else ""
    fut = sd.get("future_result_surface_allowed_in_m47") if sd else None
    return {
        "contract_id": str(m47.get("contract_id") or ""),
        "profile_id": str(m47.get("profile_id") or ""),
        "artifact_sha256": str(m47.get(DIGEST_FIELD) or "").lower(),
        "design_status": _design_status_str(m47),
        "surface_status": surf,
        "future_result_surface_allowed_in_m47": fut,
        "interpretation": INTERPRETATION_M47_BINDING,
    }


def _m47_honesty_snapshot(m47: dict[str, Any] | None) -> dict[str, Any]:
    if m47 is None:
        return {}
    return {k: m47.get(k) for k in M47_BODY_BOOL_KEYS}


def _default_claim_decisions() -> dict[str, str]:
    return {
        "scorecard_results": CLAIM_SCORECARD_REFUSED,
        "benchmark_pass_fail": CLAIM_BENCHMARK_REFUSED,
        "scorecard_total": CLAIM_TOTAL_REFUSED,
        "strength_evaluation": CLAIM_STRENGTH_REFUSED,
        "checkpoint_promotion": CLAIM_PROMOTION_REFUSED,
    }


def _honesty_false_block_m48() -> dict[str, Any]:
    return {k: False for k in M48_ALWAYS_FALSE_KEYS}


@dataclass(frozen=True)
class M48Decision:
    preflight_status: str
    gate_status: str
    evidence_mode: str
    requirement_rows: tuple[dict[str, Any], ...]
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    route_next: str


def _unique_refs(codes: list[str]) -> tuple[dict[str, str], ...]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            out.append({"code": c, "detail": c})
    return tuple(out)


def decide_m48_upstream(
    m47: dict[str, Any] | None,
    *,
    manifest: dict[str, Any] | None,
    evidence_mode: str,
    skip_manifest: bool,
    require_canonical_seal: bool = True,
) -> M48Decision:
    refs_codes: list[str] = []
    warns: list[str] = []

    def bail(
        status: str,
        gate: str,
        codes: list[str],
        route: str,
        rows: tuple[dict[str, Any], ...] = (),
    ) -> M48Decision:
        return M48Decision(
            status,
            gate,
            evidence_mode,
            rows,
            _unique_refs(codes),
            tuple(warns),
            route,
        )

    if m47 is None:
        refs_codes.append(REFUSED_MISSING_M47)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    struct = structural_m47_issues_for_m48(m47, require_canonical_seal=require_canonical_seal)
    if struct:
        refs_codes.append(REFUSED_INVALID_M47)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    if m47.get("scorecard_results_produced") is True:
        refs_codes.append(REFUSED_M47_SCORECARD_PRESENT)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    if honesty_violation_m47_body(m47):
        refs_codes.append(REFUSED_M47_HONESTY)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    if _route_status_m47(m47) != M47_ROUTE_STATUS:
        refs_codes.append(REFUSED_M47_ROUTE_EXECUTED)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    surf_errs = surface_issues_for_m48(m47)
    if surf_errs:
        if any("future_result_surface_allowed_in_m47_not_false" in e for e in surf_errs):
            refs_codes.append(REFUSED_M47_FUTURE_SURFACE_ALLOWED)
        if any(
            "future_result_surface_requires_separate_milestone_not_true" in e for e in surf_errs
        ):
            refs_codes.append(REFUSED_M47_FUTURE_SURFACE_NOT_SEPARATE)
        if not refs_codes:
            refs_codes.append(REFUSED_INVALID_M47)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    ds = _design_status_str(m47)
    if ds == M47_DESIGN_REFUSED or (ds.startswith("refused_") and ds):
        refs_codes.append(REFUSED_M47_NOT_READY)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    preflight_ready = STATUS_PREFLIGHT_READY
    if ds == M47_READY_WARNINGS:
        preflight_ready = STATUS_PREFLIGHT_READY_WARNINGS
        uw = m47.get("warnings")
        if isinstance(uw, list):
            warns.extend(str(w) for w in uw)
        warns.append("m47_bounded_scorecard_result_surface_design_ready_with_warnings_carried")
    elif ds != M47_READY:
        refs_codes.append(REFUSED_M47_NOT_READY)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            refs_codes,
            ROUTE_TO_M47_REMEDIATION,
        )

    if skip_manifest:
        rows = ()
        return M48Decision(
            preflight_ready,
            GATE_SATISFIED,
            evidence_mode,
            rows,
            (),
            tuple(warns),
            ROUTE_TO_SCORECARD_EXEC_SURFACE,
        )

    if manifest is None:
        refs_codes.append(REFUSED_REQUIRED_EVIDENCE_MISSING)
        return bail(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INCOMPLETE,
            refs_codes,
            ROUTE_TO_EVIDENCE_GAP,
        )

    req_rows_list, ev_refs = evaluate_evidence_manifest(manifest)
    rows_t = tuple(req_rows_list)

    if ev_refs:
        gate = GATE_INVALID if REFUSED_SCORECARD_RESULTS_CLAIM in ev_refs else GATE_INCOMPLETE
        status_out = STATUS_PREFLIGHT_REFUSED
        route_out = ROUTE_TO_EVIDENCE_GAP
        merged = refs_codes + ev_refs
        return M48Decision(
            status_out,
            gate,
            evidence_mode,
            rows_t,
            _unique_refs(merged),
            tuple(warns),
            route_out,
        )

    return M48Decision(
        preflight_ready,
        GATE_SATISFIED,
        evidence_mode,
        rows_t,
        (),
        tuple(warns),
        ROUTE_TO_SCORECARD_EXEC_SURFACE,
    )


def seal_m48_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m48_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_scorecard_execution_preflight_report",
        "report_version": "m48",
        "milestone": MILESTONE_LABEL_M48,
        "contract_id": CONTRACT_ID_M48_PREFLIGHT,
        "profile_id": PROFILE_M48_EVIDENCE_GATE,
        DIGEST_FIELD: digest,
        "preflight_status": sealed.get("preflight_status"),
        "gate_status": (sealed.get("evidence_requirements_gate") or {}).get("gate_status"),
    }


def build_m48_brief_md(*, sealed: dict[str, Any]) -> str:
    m47b = sealed.get("m47_binding") or {}
    erg = sealed.get("evidence_requirements_gate") or {}
    cep = sealed.get("scorecard_execution_preflight") or {}
    claims = sealed.get("claim_decisions") or {}
    route = sealed.get("route_recommendation") or {}
    ncl = sealed.get("non_claims") or []
    miss_req = [
        r.get("requirement_id")
        for r in (erg.get("requirements") or [])
        if isinstance(r, dict)
        and r.get("status") in (STATUS_REQUIRED_MISSING, STATUS_REQUIRED_INVALID)
    ]

    lines = [
        "# V15-M48 bounded scorecard execution preflight brief",
        "",
        "## M47 binding summary",
        f"- `contract_id`: `{m47b.get('contract_id', '')}`",
        f"- `profile_id`: `{m47b.get('profile_id', '')}`",
        f"- `artifact_sha256`: `{m47b.get('artifact_sha256', '')}`",
        f"- `design_status`: `{m47b.get('design_status', '')}`",
        f"- `surface_status`: `{m47b.get('surface_status', '')}`",
        f"- `future_result_surface_allowed_in_m47`: "
        f"`{m47b.get('future_result_surface_allowed_in_m47', '')}`",
        f"- `interpretation`: `{m47b.get('interpretation', '')}`",
        "",
        "## M47 design interpretation",
        "- Sealed M47 surface-design readiness is **design / refusal bookkeeping only** — **not** "
        "scorecard execution results.",
        "",
        "## Evidence requirements gate",
        f"- `gate_status`: `{erg.get('gate_status', '')}`",
        f"- `evidence_mode`: `{erg.get('evidence_mode', '')}`",
        "",
        "## Missing or invalid evidence",
    ]
    if miss_req:
        lines.extend([f"- `{x}`" for x in miss_req])
    else:
        lines.append("- _(none listed)_")
    lines.extend(
        [
            "",
            "## Scorecard execution preflight status",
            f"- `preflight_surface_status`: `{cep.get('preflight_surface_status', '')}`",
            f"- `future_contract_id`: `{cep.get('future_contract_id', '')}`",
            f"- `scorecard_execution_allowed_in_m48`: "
            f"`{cep.get('scorecard_execution_allowed_in_m48', '')}`",
            f"- `m48_result_status`: `{cep.get('m48_result_status', '')}`",
            "",
            "## Claim refusals",
        ]
    )
    if isinstance(claims, dict):
        for k, v in sorted(claims.items()):
            lines.append(f"- `{k}` → `{v}`")
    lines.extend(
        [
            "",
            "## Route recommendation",
            f"- `next_route`: `{route.get('next_route', '')}`",
            f"- `route_status`: `{route.get('route_status', '')}`",
            "",
            "## Non-claims",
        ]
    )
    if isinstance(ncl, list):
        lines.extend([f"- `{x}`" for x in ncl])
    lines.extend(
        [
            "",
            "---",
            "",
            "This brief is a bounded scorecard execution preflight and evidence requirements gate. "
            "It is not scorecard execution, scorecard results, benchmark pass/fail evidence, "
            "strength evaluation, or checkpoint promotion.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M48 emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_SCORECARD_RESULTS_CLAIM


def _scorecard_execution_preflight_block() -> dict[str, Any]:
    return {
        "preflight_surface_status": "ready_not_executed",
        "future_contract_id": "starlab.v15.bounded_scorecard_result_execution.v1",
        "future_profile_id": "starlab.v15.m49.bounded_scorecard_result_execution_surface.v1",
        "future_result_surface_requires_separate_milestone": True,
        "scorecard_execution_allowed_in_m48": False,
        "m48_result_status": "no_scorecard_execution_in_m48",
    }


def _assemble_m48_body(
    *,
    profile: str,
    m47_plain: dict[str, Any] | None,
    decision: M48Decision,
) -> dict[str, Any]:
    snapshot = _m47_honesty_snapshot(m47_plain)
    refs_dicts = [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals]

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M48_PREFLIGHT,
        "profile_id": PROFILE_M48_EVIDENCE_GATE,
        "milestone": MILESTONE_LABEL_M48,
        "emitter_module": EMITTER_MODULE_M48,
        "profile": profile,
        "preflight_status": decision.preflight_status,
        "m47_binding": _m47_binding_summary(m47_plain),
        "m47_upstream_honesty_snapshot": snapshot,
        "evidence_requirements_gate": {
            "gate_status": decision.gate_status,
            "evidence_mode": decision.evidence_mode,
            "requirements": [dict(r) for r in decision.requirement_rows],
        },
        "scorecard_execution_preflight": _scorecard_execution_preflight_block(),
        "claim_decisions": _default_claim_decisions(),
        "route_recommendation": {
            "next_route": decision.route_next,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "refusals": refs_dicts,
        "warnings": list(decision.warnings),
        "non_claims": list(NON_CLAIMS_M48),
        **_honesty_false_block_m48(),
    }
    return body


def _emit_m48_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m48_report(sealed)))
    brief = build_m48_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m48_forbidden_flag_refusal(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
    refusal_code_override: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_override or refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    refs: tuple[dict[str, str], ...] = (
        {"code": primary, "detail": "forbidden_cli_flags:" + ",".join(bad)},
    )
    decision = M48Decision(
        STATUS_PREFLIGHT_REFUSED,
        GATE_INVALID,
        EVIDENCE_MODE_OPERATOR_MANIFEST,
        (),
        refs,
        (),
        ROUTE_TO_EVIDENCE_GAP,
    )
    body_pre = _assemble_m48_body(profile=profile, m47_plain=None, decision=decision)
    body_pre["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m48_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m48_artifacts(sealed, output_dir)


def emit_m48_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m47_upstream_fixture"
    emit_m47_fixture_ci(sub)
    m47_path = sub / M47_FILENAME
    m47_plain = _parse_json_object(m47_path)
    fx_manifest = build_fixture_evidence_manifest()
    decision = decide_m48_upstream(
        m47_plain,
        manifest=fx_manifest,
        evidence_mode=EVIDENCE_MODE_FIXTURE,
        skip_manifest=False,
        require_canonical_seal=True,
    )
    body = _assemble_m48_body(
        profile=PROFILE_FIXTURE_CI,
        m47_plain=m47_plain,
        decision=decision,
    )
    sealed = seal_m48_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m48_artifacts(sealed, output_dir)


def emit_m48_operator_preflight(
    output_dir: Path,
    *,
    m47_path: Path | None,
    manifest_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m47_plain: dict[str, Any] | None = None
    if m47_path is not None:
        rp = Path(m47_path).resolve()
        if rp.is_file():
            try:
                m47_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m47_plain = None

    manifest_plain: dict[str, Any] | None = None
    if manifest_path is not None:
        mp = Path(manifest_path).resolve()
        if mp.is_file():
            try:
                raw_m = json.loads(mp.read_text(encoding="utf-8"))
                manifest_plain = raw_m if isinstance(raw_m, dict) else None
            except (json.JSONDecodeError, OSError, UnicodeError):
                manifest_plain = None

    decision = decide_m48_upstream(
        m47_plain,
        manifest=manifest_plain,
        evidence_mode=EVIDENCE_MODE_OPERATOR_MANIFEST,
        skip_manifest=False,
        require_canonical_seal=True,
    )
    body = _assemble_m48_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m47_plain=m47_plain,
        decision=decision,
    )
    sealed = seal_m48_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m48_artifacts(sealed, output_dir)


def _validate_declared_overclaims(declared: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for k in M48_ALWAYS_FALSE_KEYS:
        if declared.get(k) is True:
            violations.append(f"declared_truth_on_{k}")

    cds = declared.get("claim_decisions")
    if isinstance(cds, dict):
        for key, val in cds.items():
            if val not in ALLOWED_CLAIM_DECISION_VALUES:
                violations.append(f"disallowed_claim_decision:{key}:{val}")

    return violations


def decide_m48_from_declared_m47_binding(mb: dict[str, Any]) -> dict[str, Any] | None:
    """Build synthetic upstream M47-shaped dict from declared binding + surface snapshot."""
    rr = mb.get("route_recommendation")
    rstat = str(rr.get("route_status") or "") if isinstance(rr, dict) else ""

    sd_in = mb.get("scorecard_surface_design")
    sd_out: dict[str, Any]
    if isinstance(sd_in, dict):
        sd_out = dict(sd_in)
    else:
        sd_out = {
            "surface_status": str(mb.get("surface_status") or ""),
            "future_result_surface_allowed_in_m47": mb.get("future_result_surface_allowed_in_m47"),
            "future_result_surface_requires_separate_milestone": mb.get(
                "future_result_surface_requires_separate_milestone"
            ),
        }

    synth: dict[str, Any] = {
        "contract_id": str(mb.get("contract_id") or ""),
        "profile_id": str(mb.get("profile_id") or ""),
        DIGEST_FIELD: str(mb.get(DIGEST_FIELD) or ""),
        "design_status": str(mb.get("design_status") or ""),
        "route_recommendation": {"route_status": rstat},
        "scorecard_surface_design": sd_out,
        "scorecard_results_produced": mb.get("scorecard_results_produced"),
    }
    for k in M47_BODY_BOOL_KEYS:
        if k not in synth:
            synth[k] = mb.get(k)
    return synth


def emit_m48_operator_declared(
    output_dir: Path,
    *,
    declared_preflight_path: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rp = Path(declared_preflight_path).resolve()
    raw = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("declared preflight must be a JSON object")
    declared_in = cast(dict[str, Any], redact_paths_in_value(raw))

    cid = str(declared_in.get("contract_id") or "")
    pid = str(declared_in.get("profile_id") or "")
    contract_ok = cid == CONTRACT_ID_M48_PREFLIGHT and pid == PROFILE_M48_EVIDENCE_GATE

    over = _validate_declared_overclaims(declared_in) if contract_ok else []

    if not contract_ok:
        refs = (
            {
                "code": REFUSED_DECLARED_SHAPE,
                "detail": f"contract_or_profile_mismatch:{cid!r}:{pid!r}",
            },
        )
        decision = M48Decision(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            EVIDENCE_MODE_OPERATOR_MANIFEST,
            (),
            tuple({"code": REFUSED_DECLARED_SHAPE, "detail": r["detail"]} for r in refs),
            (),
            ROUTE_TO_M47_REMEDIATION,
        )
        m47_plain_out: dict[str, Any] | None = None
    elif over:
        decision = M48Decision(
            STATUS_PREFLIGHT_REFUSED,
            GATE_INVALID,
            EVIDENCE_MODE_OPERATOR_MANIFEST,
            (),
            (
                {
                    "code": REFUSED_SCORECARD_TOTAL_CLAIM,
                    "detail": "declared_overclaim:" + ",".join(over),
                },
            ),
            (),
            ROUTE_TO_EVIDENCE_GAP,
        )
        m47_plain_out = None
    else:
        mb = declared_in.get("m47_binding")
        if not isinstance(mb, dict):
            decision = M48Decision(
                STATUS_PREFLIGHT_REFUSED,
                GATE_INVALID,
                EVIDENCE_MODE_OPERATOR_MANIFEST,
                (),
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m47_binding_missing_or_not_object",
                    },
                ),
                (),
                ROUTE_TO_M47_REMEDIATION,
            )
            m47_plain_out = None
        elif not str(mb.get("artifact_sha256") or "").strip():
            decision = M48Decision(
                STATUS_PREFLIGHT_REFUSED,
                GATE_INVALID,
                EVIDENCE_MODE_OPERATOR_MANIFEST,
                (),
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m47_binding_artifact_sha256_required",
                    },
                ),
                (),
                ROUTE_TO_M47_REMEDIATION,
            )
            m47_plain_out = None
        else:
            synth = decide_m48_from_declared_m47_binding(mb)
            manifest_src = declared_in.get("evidence_manifest_inline")
            manifest_plain = manifest_src if isinstance(manifest_src, dict) else None
            decision = decide_m48_upstream(
                synth,
                manifest=manifest_plain,
                evidence_mode=EVIDENCE_MODE_OPERATOR_MANIFEST,
                skip_manifest=manifest_plain is None,
                require_canonical_seal=False,
            )
            m47_plain_out = synth

    body = _assemble_m48_body(
        profile=PROFILE_OPERATOR_DECLARED,
        m47_plain=m47_plain_out,
        decision=decision,
    )

    mb_out = declared_in.get("m47_binding")
    if (
        isinstance(mb_out, dict)
        and contract_ok
        and not over
        and str(mb_out.get("artifact_sha256") or "").strip()
    ):
        sd_decl = mb_out.get("scorecard_surface_design")
        fut_allowed = None
        fut_sep = None
        surf_st = ""
        if isinstance(sd_decl, dict):
            surf_st = str(sd_decl.get("surface_status") or "")
            fut_allowed = sd_decl.get("future_result_surface_allowed_in_m47")
            fut_sep = sd_decl.get("future_result_surface_requires_separate_milestone")
        body["m47_binding"] = {
            "contract_id": mb_out.get("contract_id"),
            "profile_id": mb_out.get("profile_id"),
            "artifact_sha256": mb_out.get("artifact_sha256"),
            "design_status": mb_out.get("design_status"),
            "surface_status": surf_st,
            "future_result_surface_allowed_in_m47": fut_allowed,
            "interpretation": mb_out.get("interpretation") or INTERPRETATION_M47_BINDING,
        }
        if fut_sep is not None:
            body["m47_binding"]["future_result_surface_requires_separate_milestone"] = fut_sep

    body["declared_preflight_path_logical"] = "operator_supplied"
    sealed = seal_m48_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m48_artifacts(sealed, output_dir)


__all__ = (
    "M48Decision",
    "build_fixture_evidence_manifest",
    "build_m48_brief_md",
    "decide_m48_upstream",
    "emit_m48_fixture_ci",
    "emit_m48_forbidden_flag_refusal",
    "emit_m48_operator_declared",
    "emit_m48_operator_preflight",
    "evaluate_evidence_manifest",
    "forbidden_keys_present",
    "honesty_violation_m47_body",
    "refusal_code_from_forbidden_flags",
    "seal_m48_body",
    "structural_m47_issues_for_m48",
    "surface_issues_for_m48",
)
