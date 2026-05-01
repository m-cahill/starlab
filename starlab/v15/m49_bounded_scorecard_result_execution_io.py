"""V15-M49 — bounded scorecard result execution surface IO."""

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
from starlab.v15.m48_bounded_scorecard_execution_preflight_io import emit_m48_fixture_ci
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    CONTRACT_ID_M48_PREFLIGHT,
    M48_ALWAYS_FALSE_KEYS,
    PROFILE_M48_EVIDENCE_GATE,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    FILENAME_MAIN_JSON as M48_FILENAME_MAIN_JSON,
)
from starlab.v15.m48_bounded_scorecard_execution_preflight_models import (
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED as M48_ROUTE_STATUS_EXPECTED,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    ALLOWED_CLAIM_DECISION_VALUES,
    BRIEF_FILENAME,
    CLAIM_BENCHMARK_PENDING,
    CLAIM_HUMAN_REFUSED,
    CLAIM_PROMOTION_PENDING,
    CLAIM_SCORECARD_EMITTED_BOUNDED,
    CLAIM_SCORECARD_REFUSED_EMIT,
    CLAIM_SHOWCASE_REFUSED,
    CLAIM_STRENGTH_REFUSED,
    CLAIM_T2_T5_REFUSED,
    CLAIM_V2_REFUSED,
    CLAIM_XAI_REFUSED,
    CONTRACT_ID_M49_RESULT,
    DIGEST_FIELD,
    EMITTER_MODULE_M49,
    FILENAME_MAIN_JSON,
    FIXTURE_ARTIFACT_SHA_PLACEHOLDER,
    FORBIDDEN_FLAG_TO_REFUSAL,
    INTERPRETATION_M48_BINDING,
    INTERPRETATIONS_ARTIFACT,
    M48_STATUS_READY,
    M48_STATUS_READY_WARNINGS,
    M49_DECLARED_OVERCLAIM_KEYS,
    M49_SUCCESS_FALSE_KEYS,
    MILESTONE_LABEL_M49,
    NON_CLAIMS_M49,
    PROFILE_FIXTURE_CI,
    PROFILE_M49_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_CANDIDATE_MISMATCH,
    REFUSED_DECLARED_SHAPE,
    REFUSED_INVALID_M48,
    REFUSED_INVALID_METRICS,
    REFUSED_INVALID_RESULT_EVIDENCE,
    REFUSED_M48_HONESTY,
    REFUSED_M48_NOT_READY,
    REFUSED_M48_ROUTE_EXECUTED,
    REFUSED_M48_SCORECARD_ALREADY,
    REFUSED_MISSING_M48,
    REFUSED_MISSING_METRICS,
    REFUSED_MISSING_RESULT_EVIDENCE,
    REFUSED_MISSING_THRESHOLD,
    REFUSED_ROUTE_OUT_OF_SCOPE,
    REPORT_FILENAME,
    RESULT_MODE_FIXTURE,
    RESULT_MODE_OPERATOR_BOUND,
    RESULT_MODE_OPERATOR_DECLARED,
    ROUTE_EVIDENCE_GAP,
    ROUTE_M48_REMEDIATION,
    ROUTE_READOUT_PROMOTION_REFUSAL,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    SCHEMA_VERSION,
    SCORECARD_RESULT_EVIDENCE_CONTRACT_ID,
    STATUS_RESULT_COMPLETED,
    STATUS_RESULT_COMPLETED_WARNINGS,
    STATUS_RESULT_REFUSED,
    WARN_CANDIDATE_UPSTREAM_UNAVAILABLE,
    WARN_FORWARD_HINT_MISSING,
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


def _sha_like(v: object) -> bool:
    if not isinstance(v, str):
        return False
    s = v.strip().lower()
    return len(s) == 64 and all(c in "0123456789abcdef" for c in s)


def _binding_sha_ok(block: object) -> bool:
    if not isinstance(block, dict):
        return False
    return _sha_like(block.get("artifact_sha256"))


def structural_m48_issues_for_m49(
    m48: dict[str, Any],
    *,
    require_canonical_seal: bool,
) -> list[str]:
    errs: list[str] = []
    if str(m48.get("contract_id", "")) != CONTRACT_ID_M48_PREFLIGHT:
        errs.append("m48_contract_id_mismatch")
    if str(m48.get("profile_id", "")) != PROFILE_M48_EVIDENCE_GATE:
        errs.append("m48_profile_id_mismatch")
    if require_canonical_seal and not _seal_ok(m48):
        errs.append("m48_seal_invalid")
    return errs


def _route_status_m48(m48: dict[str, Any]) -> str:
    rr = m48.get("route_recommendation")
    if not isinstance(rr, dict):
        return ""
    return str(rr.get("route_status") or "")


def _scorecard_execution_preflight(m48: dict[str, Any]) -> dict[str, Any] | None:
    cep = m48.get("scorecard_execution_preflight")
    return cep if isinstance(cep, dict) else None


def honesty_violation_m48_gate(m48: dict[str, Any]) -> bool:
    return any(m48.get(k) is True for k in M48_ALWAYS_FALSE_KEYS)


def forward_hint_outcome(m48: dict[str, Any]) -> tuple[bool, bool, str | None]:
    """Return (ok, needs_warning_missing, refusal_code or None)."""
    cep = _scorecard_execution_preflight(m48)
    if cep is None:
        return True, True, None
    fc = cep.get("future_contract_id")
    fp = cep.get("future_profile_id")
    fc_s = str(fc).strip() if fc is not None else ""
    fp_s = str(fp).strip() if fp is not None else ""
    fc_missing = fc_s == ""
    fp_missing = fp_s == ""
    if fc_missing and fp_missing:
        return True, True, None
    if fc_missing ^ fp_missing:
        return False, False, REFUSED_ROUTE_OUT_OF_SCOPE
    if fc_s != CONTRACT_ID_M49_RESULT or fp_s != PROFILE_M49_SURFACE:
        return False, False, REFUSED_ROUTE_OUT_OF_SCOPE
    return True, False, None


def validate_m48_execution_preflight_block(m48: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    cep = _scorecard_execution_preflight(m48)
    if cep is None:
        errs.append("scorecard_execution_preflight_missing")
        return errs
    if str(cep.get("preflight_surface_status") or "") != "ready_not_executed":
        errs.append("preflight_surface_status_not_ready_not_executed")
    if cep.get("scorecard_execution_allowed_in_m48") is not False:
        errs.append("scorecard_execution_allowed_in_m48_not_false")
    if m48.get("scorecard_execution_performed") is not False:
        errs.append("scorecard_execution_performed_not_false")
    return errs


def upstream_candidate_sha_from_m48(m48: dict[str, Any]) -> str | None:
    paths: tuple[tuple[str, ...], ...] = (
        ("evidence_requirements_gate", "evidence_manifest_snapshot", "candidate_checkpoint_sha256"),
        ("evidence_manifest_snapshot", "candidate_checkpoint_sha256"),
        ("m47_binding", "candidate_checkpoint_sha256"),
        ("m47_upstream_honesty_snapshot", "candidate_checkpoint_sha256"),
    )
    for path in paths:
        d: Any = m48
        ok = True
        for p in path:
            if not isinstance(d, dict):
                ok = False
                break
            d = d.get(p)
        if ok and isinstance(d, str) and _sha_like(d):
            return d.strip().lower()
    return None


def build_fixture_scorecard_result_evidence(*, m48_digest_lower: str) -> dict[str, Any]:
    h = FIXTURE_ARTIFACT_SHA_PLACEHOLDER
    return {
        "contract_id": SCORECARD_RESULT_EVIDENCE_CONTRACT_ID,
        "candidate_checkpoint_sha256": h,
        "scorecard_protocol_binding": {"artifact_sha256": h},
        "m48_preflight_binding": {"artifact_sha256": m48_digest_lower},
        "execution_evidence_bindings": [
            {"artifact_sha256": h, "evidence_kind": "match_or_episode_evidence"},
        ],
        "metric_results": {
            "scorecard_total": 0.0,
            "win_rate": 0.0,
            "episode_count": 0,
            "valid_episode_count": 0,
        },
        "threshold_policy": {
            "policy_id": "declared_bounded_threshold_policy_v1",
            "pass_threshold": 0.0,
        },
        "public_private_boundary": {"status": "declared"},
        "non_claims": [],
    }


def evaluate_scorecard_result_evidence(
    evidence: dict[str, Any],
    *,
    m48_digest_expected: str,
) -> tuple[list[str], dict[str, Any] | None]:
    """Return (refusal codes, normalized metric snapshot or None)."""
    refs: list[str] = []
    if str(evidence.get("contract_id") or "") != SCORECARD_RESULT_EVIDENCE_CONTRACT_ID:
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None

    if not _sha_like(evidence.get("candidate_checkpoint_sha256")):
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None

    if not _binding_sha_ok(evidence.get("scorecard_protocol_binding")):
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None

    m48b = evidence.get("m48_preflight_binding")
    if (
        not _binding_sha_ok(m48b)
        or str(cast(dict[str, Any], m48b).get("artifact_sha256", "")).lower()
        != m48_digest_expected.lower()
    ):
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None

    eeb = evidence.get("execution_evidence_bindings")
    if not isinstance(eeb, list) or not eeb:
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None
    for item in eeb:
        if not isinstance(item, dict) or not _sha_like(item.get("artifact_sha256")):
            refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
            return refs, None
        ek = item.get("evidence_kind")
        if not isinstance(ek, str) or not ek.strip():
            refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
            return refs, None

    metrics = evidence.get("metric_results")
    if not isinstance(metrics, dict):
        refs.append(REFUSED_MISSING_METRICS)
        return refs, None

    st = metrics.get("scorecard_total")
    wr = metrics.get("win_rate")
    ec = metrics.get("episode_count")
    vec = metrics.get("valid_episode_count")

    if st is None and wr is None and ec is None and vec is None:
        refs.append(REFUSED_MISSING_METRICS)
        return refs, None

    try:
        st_f = float(st) if st is not None else None
    except (TypeError, ValueError):
        refs.append(REFUSED_INVALID_METRICS)
        return refs, None
    if st_f is None:
        refs.append(REFUSED_MISSING_METRICS)
        return refs, None

    try:
        wr_f = float(wr) if wr is not None else None
    except (TypeError, ValueError):
        refs.append(REFUSED_INVALID_METRICS)
        return refs, None
    if wr_f is None or not (0.0 <= wr_f <= 1.0):
        refs.append(REFUSED_INVALID_METRICS)
        return refs, None

    if ec is None or vec is None:
        refs.append(REFUSED_MISSING_METRICS)
        return refs, None
    if not isinstance(ec, int) or ec < 0:
        refs.append(REFUSED_INVALID_METRICS)
        return refs, None
    if not isinstance(vec, int) or vec < 0 or vec > ec:
        refs.append(REFUSED_INVALID_METRICS)
        return refs, None

    pol = evidence.get("threshold_policy")
    if not isinstance(pol, dict) or not str(pol.get("policy_id") or "").strip():
        refs.append(REFUSED_MISSING_THRESHOLD)
        return refs, None
    if pol.get("pass_threshold") is None:
        refs.append(REFUSED_MISSING_THRESHOLD)
        return refs, None

    ppb = evidence.get("public_private_boundary")
    if not isinstance(ppb, dict) or not str(ppb.get("status") or "").strip():
        refs.append(REFUSED_INVALID_RESULT_EVIDENCE)
        return refs, None

    snap = {
        "scorecard_total": st_f,
        "win_rate": wr_f,
        "episode_count": ec,
        "valid_episode_count": vec,
        "metric_results": dict(metrics),
        "threshold_policy": dict(pol),
    }
    if refs:
        return refs, None
    return [], snap


def _m48_binding_summary(m48: dict[str, Any] | None) -> dict[str, Any]:
    if m48 is None:
        return {
            "contract_id": None,
            "profile_id": None,
            "artifact_sha256": None,
            "preflight_status": None,
            "interpretation": INTERPRETATION_M48_BINDING,
        }
    return {
        "contract_id": str(m48.get("contract_id") or ""),
        "profile_id": str(m48.get("profile_id") or ""),
        "artifact_sha256": str(m48.get(DIGEST_FIELD) or "").lower(),
        "preflight_status": str(m48.get("preflight_status") or ""),
        "interpretation": INTERPRETATION_M48_BINDING,
    }


def _default_claim_decisions() -> dict[str, str]:
    return {
        "scorecard_results": CLAIM_SCORECARD_EMITTED_BOUNDED,
        "benchmark_pass_fail": CLAIM_BENCHMARK_PENDING,
        "strength_evaluation": CLAIM_STRENGTH_REFUSED,
        "checkpoint_promotion": CLAIM_PROMOTION_PENDING,
        "xai_execution": CLAIM_XAI_REFUSED,
        "human_panel_execution": CLAIM_HUMAN_REFUSED,
        "showcase_release": CLAIM_SHOWCASE_REFUSED,
        "v2_authorization": CLAIM_V2_REFUSED,
        "t2_t5_execution": CLAIM_T2_T5_REFUSED,
    }


def _claim_decisions_for_refusal() -> dict[str, str]:
    return {
        "scorecard_results": CLAIM_SCORECARD_REFUSED_EMIT,
        "benchmark_pass_fail": CLAIM_BENCHMARK_PENDING,
        "strength_evaluation": CLAIM_STRENGTH_REFUSED,
        "checkpoint_promotion": CLAIM_PROMOTION_PENDING,
        "xai_execution": CLAIM_XAI_REFUSED,
        "human_panel_execution": CLAIM_HUMAN_REFUSED,
        "showcase_release": CLAIM_SHOWCASE_REFUSED,
        "v2_authorization": CLAIM_V2_REFUSED,
        "t2_t5_execution": CLAIM_T2_T5_REFUSED,
    }


def _success_false_block() -> dict[str, Any]:
    return {k: False for k in M49_SUCCESS_FALSE_KEYS}


def _success_true_block() -> dict[str, Any]:
    out = _success_false_block()
    out.update(
        {
            "scorecard_results_produced": True,
            "scorecard_total_computed": True,
            "win_rate_computed": True,
        },
    )
    return out


def _refused_true_block() -> dict[str, Any]:
    out = _success_false_block()
    out.update(
        {
            "scorecard_results_produced": False,
            "scorecard_total_computed": False,
            "win_rate_computed": False,
        },
    )
    return out


def _unique_refs(codes: list[str]) -> tuple[dict[str, str], ...]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            out.append({"code": c, "detail": c})
    return tuple(out)


@dataclass(frozen=True)
class M49Decision:
    result_status: str
    result_mode: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    route_next: str
    scorecard_snapshot: dict[str, Any] | None
    candidate_sha: str | None


def decide_m49_from_m48_and_evidence(
    m48: dict[str, Any] | None,
    evidence: dict[str, Any] | None,
    *,
    result_mode: str,
    require_canonical_seal: bool,
) -> M49Decision:
    warns: list[str] = []

    def bail(
        status: str,
        codes: list[str],
        route: str,
        candidate: str | None = None,
    ) -> M49Decision:
        return M49Decision(
            status,
            result_mode,
            _unique_refs(codes),
            tuple(warns),
            route,
            None,
            candidate,
        )

    if m48 is None:
        return bail(STATUS_RESULT_REFUSED, [REFUSED_MISSING_M48], ROUTE_M48_REMEDIATION)

    struct = structural_m48_issues_for_m49(m48, require_canonical_seal=require_canonical_seal)
    if struct:
        return bail(
            STATUS_RESULT_REFUSED,
            [REFUSED_INVALID_M48],
            ROUTE_M48_REMEDIATION,
        )

    pf = str(m48.get("preflight_status") or "")
    if pf != M48_STATUS_READY and pf != M48_STATUS_READY_WARNINGS:
        return bail(
            STATUS_RESULT_REFUSED,
            [REFUSED_M48_NOT_READY],
            ROUTE_M48_REMEDIATION,
        )

    if pf == M48_STATUS_READY_WARNINGS:
        uw = m48.get("warnings")
        if isinstance(uw, list):
            warns.extend(str(w) for w in uw)
        warns.append("m48_bounded_scorecard_execution_preflight_ready_with_warnings_carried")

    if m48.get("scorecard_execution_performed") is True:
        return bail(
            STATUS_RESULT_REFUSED,
            [REFUSED_M48_SCORECARD_ALREADY],
            ROUTE_M48_REMEDIATION,
        )

    if honesty_violation_m48_gate(m48):
        return bail(STATUS_RESULT_REFUSED, [REFUSED_M48_HONESTY], ROUTE_M48_REMEDIATION)

    if _route_status_m48(m48) != M48_ROUTE_STATUS_EXPECTED:
        return bail(
            STATUS_RESULT_REFUSED,
            [REFUSED_M48_ROUTE_EXECUTED],
            ROUTE_M48_REMEDIATION,
        )

    cep_errs = validate_m48_execution_preflight_block(m48)
    if cep_errs:
        return bail(STATUS_RESULT_REFUSED, [REFUSED_INVALID_M48], ROUTE_M48_REMEDIATION)

    _, hint_warn_missing, hint_ref = forward_hint_outcome(m48)
    if hint_ref:
        return bail(STATUS_RESULT_REFUSED, [hint_ref], ROUTE_M48_REMEDIATION)
    if hint_warn_missing:
        warns.append(WARN_FORWARD_HINT_MISSING)

    m48_digest = str(m48.get(DIGEST_FIELD) or "").lower()
    if evidence is None:
        return bail(STATUS_RESULT_REFUSED, [REFUSED_MISSING_RESULT_EVIDENCE], ROUTE_EVIDENCE_GAP)

    ev_refs, snap = evaluate_scorecard_result_evidence(evidence, m48_digest_expected=m48_digest)
    if ev_refs:
        return bail(STATUS_RESULT_REFUSED, ev_refs, ROUTE_EVIDENCE_GAP)

    cand_ev = str(evidence.get("candidate_checkpoint_sha256") or "").lower()
    upstream_cand = upstream_candidate_sha_from_m48(m48)
    if upstream_cand is None:
        if result_mode == RESULT_MODE_OPERATOR_BOUND:
            warns.append(WARN_CANDIDATE_UPSTREAM_UNAVAILABLE)
    elif upstream_cand != cand_ev:
        return bail(
            STATUS_RESULT_REFUSED,
            [REFUSED_CANDIDATE_MISMATCH],
            ROUTE_EVIDENCE_GAP,
            cand_ev,
        )

    assert snap is not None
    status = STATUS_RESULT_COMPLETED
    if warns:
        status = STATUS_RESULT_COMPLETED_WARNINGS
    return M49Decision(
        status,
        result_mode,
        (),
        tuple(warns),
        ROUTE_READOUT_PROMOTION_REFUSAL,
        snap,
        cand_ev,
    )


def seal_m49_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m49_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_scorecard_result_execution_report",
        "report_version": "m49",
        "milestone": MILESTONE_LABEL_M49,
        "contract_id": CONTRACT_ID_M49_RESULT,
        "profile_id": PROFILE_M49_SURFACE,
        DIGEST_FIELD: digest,
        "result_status": sealed.get("result_status"),
        "result_mode": sealed.get("result_mode"),
    }


def build_m49_brief_md(*, sealed: dict[str, Any]) -> str:
    m48b = sealed.get("m48_binding") or {}
    scr = sealed.get("scorecard_result") or {}
    claims = sealed.get("claim_decisions") or {}
    route = sealed.get("route_recommendation") or {}
    ncl = sealed.get("non_claims") or []
    lines = [
        "# V15-M49 bounded scorecard result execution brief",
        "",
        "## M48 binding summary",
        f"- `contract_id`: `{m48b.get('contract_id', '')}`",
        f"- `profile_id`: `{m48b.get('profile_id', '')}`",
        f"- `artifact_sha256`: `{m48b.get('artifact_sha256', '')}`",
        f"- `preflight_status`: `{m48b.get('preflight_status', '')}`",
        f"- `interpretation`: `{m48b.get('interpretation', '')}`",
        "",
        "## M48 preflight interpretation",
        "- Sealed M48 preflight is **evidence routing / requirements only** — **not** prior "
        "authorization for benchmark pass/fail, strength evaluation, or promotion.",
        "",
        "## Scorecard result summary",
        f"- `result_status`: `{scr.get('result_status', '')}`",
        f"- `result_semantic_scope`: `{scr.get('result_semantic_scope', '')}`",
        f"- `candidate_checkpoint_sha256`: `{scr.get('candidate_checkpoint_sha256', '')}`",
        "",
        "## Metric result summary",
        f"- `scorecard_total`: `{scr.get('scorecard_total', '')}`",
        f"- `win_rate`: `{scr.get('win_rate', '')}`",
        f"- `episode_count`: `{scr.get('episode_count', '')}`",
        f"- `valid_episode_count`: `{scr.get('valid_episode_count', '')}`",
        "",
        "## Claim decisions",
    ]
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
            "This brief is a bounded scorecard result artifact. It is not benchmark pass/fail "
            "evidence, strength evaluation, checkpoint promotion, XAI, human-panel evidence, "
            "showcase release, v2 authorization, or T2–T5 execution.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M49 emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_BENCHMARK_PASS_CLAIM


def _scorecard_result_block(
    *,
    decision: M49Decision,
) -> dict[str, Any]:
    if decision.scorecard_snapshot is None:
        return {
            "result_status": "bounded_scorecard_result_declared",
            "result_semantic_scope": "bounded_scorecard_result_artifact_only",
            "candidate_checkpoint_sha256": None,
            "scorecard_total": None,
            "win_rate": None,
            "episode_count": None,
            "valid_episode_count": None,
            "metric_results": {},
            "threshold_policy": {},
            "pass_fail_interpretation": "not_emitted_in_m49",
        }
    snap = decision.scorecard_snapshot
    pol = snap.get("threshold_policy")
    pol_d = pol if isinstance(pol, dict) else {}
    return {
        "result_status": "bounded_scorecard_result_declared",
        "result_semantic_scope": "bounded_scorecard_result_artifact_only",
        "candidate_checkpoint_sha256": decision.candidate_sha,
        "scorecard_total": snap["scorecard_total"],
        "win_rate": snap["win_rate"],
        "episode_count": snap["episode_count"],
        "valid_episode_count": snap["valid_episode_count"],
        "metric_results": snap.get("metric_results") or {},
        "threshold_policy": pol_d,
        "pass_fail_interpretation": "not_emitted_in_m49",
    }


def _interpretations_list() -> list[str]:
    return list(INTERPRETATIONS_ARTIFACT)


def _assemble_m49_body(
    *,
    profile: str,
    m48_plain: dict[str, Any] | None,
    decision: M49Decision,
) -> dict[str, Any]:
    refs_dicts = [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals]
    if decision.result_status == STATUS_RESULT_REFUSED:
        claims = _claim_decisions_for_refusal()
        honesty = _refused_true_block()
        route = decision.route_next
    else:
        claims = _default_claim_decisions()
        honesty = _success_true_block()
        route = decision.route_next

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M49_RESULT,
        "profile_id": PROFILE_M49_SURFACE,
        "milestone": MILESTONE_LABEL_M49,
        "emitter_module": EMITTER_MODULE_M49,
        "profile": profile,
        "result_status": decision.result_status,
        "result_mode": decision.result_mode,
        "interpretations": _interpretations_list(),
        "m48_binding": _m48_binding_summary(m48_plain),
        "scorecard_result": _scorecard_result_block(decision=decision),
        "claim_decisions": claims,
        "route_recommendation": {
            "next_route": route,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "refusals": refs_dicts,
        "warnings": list(decision.warnings),
        "non_claims": list(NON_CLAIMS_M49),
        **honesty,
    }
    return body


def _emit_m49_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m49_report(sealed)))
    brief = build_m49_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m49_forbidden_flag_refusal(
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
    result_mode = (
        RESULT_MODE_FIXTURE if profile == PROFILE_FIXTURE_CI else RESULT_MODE_OPERATOR_BOUND
    )
    decision = M49Decision(
        STATUS_RESULT_REFUSED,
        result_mode,
        refs,
        (),
        ROUTE_EVIDENCE_GAP,
        None,
        None,
    )
    body_pre = _assemble_m49_body(
        profile=profile,
        m48_plain=None,
        decision=decision,
    )
    body_pre["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m49_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m49_artifacts(sealed, output_dir)


def emit_m49_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m48_upstream_fixture"
    emit_m48_fixture_ci(sub)
    m48_path = sub / M48_FILENAME_MAIN_JSON
    m48_plain = _parse_json_object(m48_path)
    digest = str(m48_plain.get(DIGEST_FIELD) or "").lower()
    evidence = build_fixture_scorecard_result_evidence(m48_digest_lower=digest)
    decision = decide_m49_from_m48_and_evidence(
        m48_plain,
        evidence,
        result_mode=RESULT_MODE_FIXTURE,
        require_canonical_seal=True,
    )
    body = _assemble_m49_body(
        profile=PROFILE_FIXTURE_CI,
        m48_plain=m48_plain,
        decision=decision,
    )
    sealed = seal_m49_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m49_artifacts(sealed, output_dir)


def emit_m49_operator_preflight(
    output_dir: Path,
    *,
    m48_path: Path | None,
    evidence_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m48_plain: dict[str, Any] | None = None
    if m48_path is not None:
        rp = Path(m48_path).resolve()
        if rp.is_file():
            try:
                m48_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m48_plain = None

    evidence_plain: dict[str, Any] | None = None
    if evidence_path is not None:
        ep = Path(evidence_path).resolve()
        if ep.is_file():
            try:
                raw_e = json.loads(ep.read_text(encoding="utf-8"))
                evidence_plain = raw_e if isinstance(raw_e, dict) else None
            except (json.JSONDecodeError, OSError, UnicodeError):
                evidence_plain = None

    decision = decide_m49_from_m48_and_evidence(
        m48_plain,
        evidence_plain,
        result_mode=RESULT_MODE_OPERATOR_BOUND,
        require_canonical_seal=True,
    )
    body = _assemble_m49_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m48_plain=m48_plain,
        decision=decision,
    )
    sealed = seal_m49_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m49_artifacts(sealed, output_dir)


def _validate_declared_overclaims(declared: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for k in M49_DECLARED_OVERCLAIM_KEYS:
        if declared.get(k) is True:
            violations.append(f"declared_truth_on_{k}")

    cds = declared.get("claim_decisions")
    if isinstance(cds, dict):
        for key, val in cds.items():
            if val not in ALLOWED_CLAIM_DECISION_VALUES:
                violations.append(f"disallowed_claim_decision:{key}:{val!r}")

    return violations


def emit_m49_operator_declared(
    output_dir: Path,
    *,
    declared_result_path: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rp = Path(declared_result_path).resolve()
    raw = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("declared result must be a JSON object")
    declared_in = cast(dict[str, Any], redact_paths_in_value(raw))

    cid = str(declared_in.get("contract_id") or "")
    pid = str(declared_in.get("profile_id") or "")
    contract_ok = cid == CONTRACT_ID_M49_RESULT and pid == PROFILE_M49_SURFACE

    over = _validate_declared_overclaims(declared_in) if contract_ok else []
    m48_out: dict[str, Any] | None
    decision: M49Decision

    if not contract_ok:
        decision = M49Decision(
            STATUS_RESULT_REFUSED,
            RESULT_MODE_OPERATOR_DECLARED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": f"contract_or_profile_mismatch:{cid!r}:{pid!r}",
                },
            ),
            (),
            ROUTE_M48_REMEDIATION,
            None,
            None,
        )
        m48_out = None
    elif over:
        decision = M49Decision(
            STATUS_RESULT_REFUSED,
            RESULT_MODE_OPERATOR_DECLARED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "declared_overclaim:" + ",".join(over),
                },
            ),
            (),
            ROUTE_EVIDENCE_GAP,
            None,
            None,
        )
        m48_out = None
    else:
        m48_bind = declared_in.get("m48_binding")
        if not isinstance(m48_bind, dict) or not str(m48_bind.get("artifact_sha256") or "").strip():
            decision = M49Decision(
                STATUS_RESULT_REFUSED,
                RESULT_MODE_OPERATOR_DECLARED,
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m48_binding_missing_or_invalid",
                    },
                ),
                (),
                ROUTE_M48_REMEDIATION,
                None,
                None,
            )
            m48_out = None
        else:
            m48_out = {
                "contract_id": str(m48_bind.get("contract_id") or CONTRACT_ID_M48_PREFLIGHT),
                "profile_id": str(m48_bind.get("profile_id") or PROFILE_M48_EVIDENCE_GATE),
                DIGEST_FIELD: str(m48_bind.get("artifact_sha256") or "").lower(),
                "preflight_status": str(m48_bind.get("preflight_status") or ""),
            }
            rs = str(declared_in.get("result_status") or "")
            warns_in = declared_in.get("warnings")
            wlist: list[str] = [str(x) for x in warns_in] if isinstance(warns_in, list) else []
            if rs == STATUS_RESULT_REFUSED:
                refs_in = declared_in.get("refusals")
                r_tup: tuple[dict[str, str], ...] = ()
                if isinstance(refs_in, list) and refs_in:
                    r_tup = tuple(
                        {"code": str(x.get("code", "")), "detail": str(x.get("detail", ""))}
                        for x in refs_in
                        if isinstance(x, dict)
                    )
                if not r_tup:
                    r_tup = (
                        {
                            "code": REFUSED_DECLARED_SHAPE,
                            "detail": "declared_refused_without_refusals",
                        },
                    )
                rr_decl = declared_in.get("route_recommendation")
                if isinstance(rr_decl, dict):
                    rn = str(rr_decl.get("next_route") or "").strip() or ROUTE_EVIDENCE_GAP
                else:
                    rn = ROUTE_EVIDENCE_GAP
                decision = M49Decision(
                    STATUS_RESULT_REFUSED,
                    RESULT_MODE_OPERATOR_DECLARED,
                    r_tup,
                    tuple(wlist),
                    rn,
                    None,
                    None,
                )
            elif rs in (STATUS_RESULT_COMPLETED, STATUS_RESULT_COMPLETED_WARNINGS):
                scr = declared_in.get("scorecard_result")
                if not isinstance(scr, dict):
                    decision = M49Decision(
                        STATUS_RESULT_REFUSED,
                        RESULT_MODE_OPERATOR_DECLARED,
                        (
                            {
                                "code": REFUSED_DECLARED_SHAPE,
                                "detail": "scorecard_result_missing_or_invalid",
                            },
                        ),
                        (),
                        ROUTE_EVIDENCE_GAP,
                        None,
                        None,
                    )
                    m48_out = m48_out  # keep binding for summary
                else:
                    cand_raw = scr.get("candidate_checkpoint_sha256")
                    cand_s = str(cand_raw).lower() if _sha_like(cand_raw) else ""
                    if not cand_s:
                        decision = M49Decision(
                            STATUS_RESULT_REFUSED,
                            RESULT_MODE_OPERATOR_DECLARED,
                            (
                                {
                                    "code": REFUSED_DECLARED_SHAPE,
                                    "detail": "candidate_checkpoint_sha256_required",
                                },
                            ),
                            (),
                            ROUTE_EVIDENCE_GAP,
                            None,
                            None,
                        )
                    else:
                        try:
                            st_v = scr.get("scorecard_total")
                            wr_v = scr.get("win_rate")
                            if st_v is None or wr_v is None:
                                raise ValueError("metrics")
                            st_f = float(st_v)
                            wr_f = float(wr_v)
                            ec = scr.get("episode_count")
                            vec = scr.get("valid_episode_count")
                            if (
                                not isinstance(ec, int)
                                or ec < 0
                                or not isinstance(vec, int)
                                or vec < 0
                                or vec > ec
                                or not (0.0 <= wr_f <= 1.0)
                            ):
                                raise ValueError("metrics")
                            pol = scr.get("threshold_policy")
                            if (
                                not isinstance(pol, dict)
                                or not str(pol.get("policy_id") or "").strip()
                                or pol.get("pass_threshold") is None
                            ):
                                raise ValueError("policy")
                        except (TypeError, ValueError):
                            decision = M49Decision(
                                STATUS_RESULT_REFUSED,
                                RESULT_MODE_OPERATOR_DECLARED,
                                (
                                    {
                                        "code": REFUSED_DECLARED_SHAPE,
                                        "detail": "scorecard_result_metric_fields_invalid",
                                    },
                                ),
                                (),
                                ROUTE_EVIDENCE_GAP,
                                None,
                                None,
                            )
                        else:
                            snap = {
                                "scorecard_total": st_f,
                                "win_rate": wr_f,
                                "episode_count": ec,
                                "valid_episode_count": vec,
                                "metric_results": scr.get("metric_results")
                                if isinstance(scr.get("metric_results"), dict)
                                else {},
                                "threshold_policy": dict(pol),
                            }
                            decision = M49Decision(
                                rs,
                                RESULT_MODE_OPERATOR_DECLARED,
                                (),
                                tuple(wlist),
                                ROUTE_READOUT_PROMOTION_REFUSAL,
                                snap,
                                cand_s,
                            )
            else:
                decision = M49Decision(
                    STATUS_RESULT_REFUSED,
                    RESULT_MODE_OPERATOR_DECLARED,
                    (
                        {
                            "code": REFUSED_DECLARED_SHAPE,
                            "detail": f"invalid_result_status:{rs!r}",
                        },
                    ),
                    (),
                    ROUTE_M48_REMEDIATION,
                    None,
                    None,
                )

    body = _assemble_m49_body(
        profile=PROFILE_OPERATOR_DECLARED,
        m48_plain=m48_out,
        decision=decision,
    )
    mb_keep = declared_in.get("m48_binding")
    if isinstance(mb_keep, dict) and contract_ok and not over:
        body["m48_binding"] = {
            "contract_id": mb_keep.get("contract_id"),
            "profile_id": mb_keep.get("profile_id"),
            "artifact_sha256": mb_keep.get("artifact_sha256"),
            "preflight_status": mb_keep.get("preflight_status"),
            "interpretation": mb_keep.get("interpretation") or INTERPRETATION_M48_BINDING,
        }

    nc = declared_in.get("non_claims")
    if isinstance(nc, list) and nc:
        base_nc = list(body.get("non_claims") or [])
        body["non_claims"] = base_nc + [str(x) for x in nc]

    body["declared_result_path_logical"] = "operator_supplied"
    sealed = seal_m49_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m49_artifacts(sealed, output_dir)


__all__ = (
    "M49Decision",
    "build_fixture_scorecard_result_evidence",
    "build_m49_brief_md",
    "decide_m49_from_m48_and_evidence",
    "emit_m49_fixture_ci",
    "emit_m49_forbidden_flag_refusal",
    "emit_m49_operator_declared",
    "emit_m49_operator_preflight",
    "evaluate_scorecard_result_evidence",
    "forward_hint_outcome",
    "honesty_violation_m48_gate",
    "refusal_code_from_forbidden_flags",
    "seal_m49_body",
    "structural_m48_issues_for_m49",
    "upstream_candidate_sha_from_m48",
    "validate_m48_execution_preflight_block",
)
