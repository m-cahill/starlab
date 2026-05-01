"""V15-M50 — scorecard result readout / benchmark pass-fail refusal decision IO."""

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
from starlab.v15.m49_bounded_scorecard_result_execution_io import emit_m49_fixture_ci
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    CONTRACT_ID_M49_RESULT,
    M49_SUCCESS_FALSE_KEYS,
    PROFILE_M49_SURFACE,
)
from starlab.v15.m49_bounded_scorecard_result_execution_models import (
    FILENAME_MAIN_JSON as M49_FILENAME_MAIN_JSON,
)
from starlab.v15.m50_scorecard_result_readout_decision_models import (
    ALLOWED_BENCHMARK_DECISIONS,
    ALLOWED_PROMOTION_DECISIONS,
    BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY,
    BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD,
    BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
    BRIEF_FILENAME,
    CONTRACT_ID_M50_READOUT,
    DIGEST_FIELD,
    EMITTER_MODULE_M50,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    INTERPRETATION_M49_BINDING,
    M49_CONTRACT_FOR_BINDING,
    M49_PROFILE_FOR_BINDING,
    M49_STATUS_COMPLETED,
    M49_STATUS_COMPLETED_WARNINGS,
    M49_STATUS_REFUSED,
    M50_DECLARED_OVERCLAIM_KEYS,
    M50_HONESTY_FALSE_KEYS,
    MILESTONE_LABEL_M50,
    NON_CLAIMS_M50,
    PROFILE_FIXTURE_CI,
    PROFILE_M50_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    PROMOTION_REFUSED_M50_READOUT_ONLY,
    PROMOTION_REFUSED_PENDING_PASS_FAIL,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_DECLARED_SHAPE,
    REFUSED_M49_CONTRACT_INVALID,
    REFUSED_M49_RESULT_NOT_READY,
    REFUSED_M49_RESULT_REFUSED,
    REFUSED_M49_SHA_MISMATCH,
    REFUSED_MISSING_M49,
    REFUSED_MISSING_SCORECARD_FIELDS,
    REFUSED_UPSTREAM_HONESTY,
    REPORT_FILENAME,
    ROUTE_M49_REMEDIATION,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M51_WATCHABILITY,
    SCHEMA_VERSION,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_WARNINGS,
    STATUS_READOUT_REFUSED,
)

REASON_BENCHMARK_PENDING_SCOPE = "pending_authoritative_threshold_and_benchmark_execution_scope"
REASON_BENCHMARK_M49_BOUNDED = "m49_bounded_scorecard_fields_only_not_benchmark_pass_fail"
REASON_BENCHMARK_MISSING_READOUT = "missing_bounded_scorecard_fields_for_readout"
REASON_PROMOTION_PENDING = "pending_authoritative_benchmark_pass_fail_and_strength_evaluation"
REASON_PROMOTION_READOUT_ONLY = "m50_readout_refusal_only_not_promotion_decision"


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


def structural_m49_issues_for_m50(
    m49: dict[str, Any],
    *,
    require_canonical_seal: bool,
) -> list[str]:
    errs: list[str] = []
    if str(m49.get("contract_id", "")) != CONTRACT_ID_M49_RESULT:
        errs.append("m49_contract_id_mismatch")
    if str(m49.get("profile_id", "")) != PROFILE_M49_SURFACE:
        errs.append("m49_profile_id_mismatch")
    if require_canonical_seal and not _seal_ok(m49):
        errs.append("m49_seal_invalid")
    return errs


def m49_upstream_honesty_or_overclaim_violation(m49: dict[str, Any]) -> bool:
    return any(m49.get(k) is True for k in M49_SUCCESS_FALSE_KEYS)


def _honesty_false_block() -> dict[str, Any]:
    return {k: False for k in M50_HONESTY_FALSE_KEYS}


def _unique_refs(codes: list[str]) -> tuple[dict[str, str], ...]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            out.append({"code": c, "detail": c})
    return tuple(out)


@dataclass(frozen=True)
class M50Decision:
    readout_status: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    route_next: str
    scorecard_results_seen: bool
    scorecard_total: float | None
    win_rate: float | None
    bounded_fields_only: bool
    benchmark_decision: str
    benchmark_reason: str
    promotion_decision: str
    promotion_reason: str
    m49_digest_lower: str
    m49_result_status: str


def decide_m50_from_m49(
    m49: dict[str, Any] | None,
    *,
    expected_sha256_lower: str | None,
    require_canonical_seal: bool,
) -> M50Decision:
    def bail(
        status: str,
        codes: list[str],
        *,
        digest: str = "",
        rs: str = "",
        warns: tuple[str, ...] = (),
    ) -> M50Decision:
        return M50Decision(
            status,
            _unique_refs(codes),
            warns,
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            digest,
            rs,
        )

    if m49 is None:
        return bail(STATUS_READOUT_REFUSED, [REFUSED_MISSING_M49])

    digest = str(m49.get(DIGEST_FIELD) or "").lower()
    rs = str(m49.get("result_status") or "")

    struct = structural_m49_issues_for_m50(m49, require_canonical_seal=require_canonical_seal)
    if struct:
        return bail(
            STATUS_READOUT_REFUSED,
            [REFUSED_M49_CONTRACT_INVALID],
            digest=digest,
            rs=rs,
        )

    if expected_sha256_lower is not None and expected_sha256_lower.strip():
        exp = expected_sha256_lower.strip().lower()
        if not _sha_like(exp):
            return bail(
                STATUS_READOUT_REFUSED,
                [REFUSED_M49_SHA_MISMATCH],
                digest=digest,
                rs=rs,
            )
        if digest != exp:
            return bail(
                STATUS_READOUT_REFUSED,
                [REFUSED_M49_SHA_MISMATCH],
                digest=digest,
                rs=rs,
            )

    if m49_upstream_honesty_or_overclaim_violation(m49):
        return bail(STATUS_READOUT_REFUSED, [REFUSED_UPSTREAM_HONESTY], digest=digest, rs=rs)

    if rs == M49_STATUS_REFUSED:
        return bail(
            STATUS_READOUT_REFUSED,
            [REFUSED_M49_RESULT_REFUSED],
            digest=digest,
            rs=rs,
        )

    if rs != M49_STATUS_COMPLETED and rs != M49_STATUS_COMPLETED_WARNINGS:
        return bail(
            STATUS_READOUT_REFUSED,
            [REFUSED_M49_RESULT_NOT_READY],
            digest=digest,
            rs=rs,
        )

    warns_in = m49.get("warnings")
    wlist: list[str] = [str(x) for x in warns_in] if isinstance(warns_in, list) else []

    scr = m49.get("scorecard_result")
    if not isinstance(scr, dict):
        return bail(
            STATUS_READOUT_REFUSED,
            [REFUSED_MISSING_SCORECARD_FIELDS],
            digest=digest,
            rs=rs,
            warns=tuple(wlist),
        )

    st_raw = scr.get("scorecard_total")
    wr_raw = scr.get("win_rate")
    st: float | None
    wr: float | None
    try:
        st = float(st_raw) if st_raw is not None else None
    except (TypeError, ValueError):
        st = None
    try:
        wr = float(wr_raw) if wr_raw is not None else None
    except (TypeError, ValueError):
        wr = None

    produced = m49.get("scorecard_results_produced") is True
    metrics_ok = st is not None and wr is not None and 0.0 <= wr <= 1.0

    bench_dec = BENCHMARK_PASS_FAIL_REFUSED_M49_BOUNDED_ONLY
    bench_reason = REASON_BENCHMARK_M49_BOUNDED
    promo_dec = PROMOTION_REFUSED_M50_READOUT_ONLY
    promo_reason = REASON_PROMOTION_READOUT_ONLY

    readout_st = STATUS_READOUT_COMPLETED
    if not metrics_ok or not produced:
        readout_st = STATUS_READOUT_COMPLETED_WARNINGS
        bench_dec = BENCHMARK_PASS_FAIL_REFUSED_MISSING_SCORECARD
        bench_reason = REASON_BENCHMARK_MISSING_READOUT
        promo_dec = PROMOTION_REFUSED_PENDING_PASS_FAIL
        promo_reason = REASON_PROMOTION_PENDING
        wlist.append("m50_missing_or_non_finite_bounded_scorecard_fields_on_m49_success")

    seen = metrics_ok and produced

    return M50Decision(
        readout_st,
        (),
        tuple(wlist),
        ROUTE_TO_M51_WATCHABILITY,
        seen,
        st,
        wr,
        True,
        bench_dec,
        bench_reason,
        promo_dec,
        promo_reason,
        digest,
        rs,
    )


def seal_m50_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m50_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_scorecard_result_readout_decision_report",
        "report_version": "m50",
        "milestone": MILESTONE_LABEL_M50,
        "contract_id": CONTRACT_ID_M50_READOUT,
        "profile_id": PROFILE_M50_SURFACE,
        DIGEST_FIELD: digest,
        "readout_status": sealed.get("readout_status"),
    }


def build_m50_brief_md(*, sealed: dict[str, Any]) -> str:
    m49b = sealed.get("m49_binding") or {}
    sr = sealed.get("scorecard_readout") or {}
    bfd = sealed.get("benchmark_pass_fail_decision") or {}
    pd = sealed.get("promotion_decision") or {}
    route = sealed.get("route_recommendation") or {}
    ncl = sealed.get("non_claims") or []
    lines = [
        "# V15-M50 scorecard result readout decision brief",
        "",
        "## M49 binding summary",
        f"- `contract_id`: `{m49b.get('contract_id', '')}`",
        f"- `profile_id`: `{m49b.get('profile_id', '')}`",
        f"- `artifact_sha256`: `{m49b.get('artifact_sha256', '')}`",
        f"- `status`: `{m49b.get('status', '')}`",
        f"- `interpretation`: `{m49b.get('interpretation', '')}`",
        "",
        "## Bounded scorecard readout",
        f"- `scorecard_results_seen`: `{sr.get('scorecard_results_seen', '')}`",
        f"- `scorecard_total`: `{sr.get('scorecard_total', '')}`",
        f"- `win_rate`: `{sr.get('win_rate', '')}`",
        f"- `bounded_fields_only`: `{sr.get('bounded_fields_only', '')}`",
        "",
        "## Benchmark pass/fail decision",
        f"- `decision`: `{bfd.get('decision', '')}`",
        f"- `reason`: `{bfd.get('reason', '')}`",
        "",
        "## Promotion decision",
        f"- `decision`: `{pd.get('decision', '')}`",
        f"- `reason`: `{pd.get('reason', '')}`",
        "",
        "## Route recommendation",
        f"- `next_route`: `{route.get('next_route', '')}`",
        f"- `route_status`: `{route.get('route_status', '')}`",
        "",
        "## Non-claims",
    ]
    if isinstance(ncl, list):
        lines.extend([f"- `{x}`" for x in ncl])
    lines.extend(
        [
            "",
            "---",
            "",
            "This brief is a deterministic scorecard readout and benchmark pass/fail refusal "
            "decision over sealed V15-M49 artifacts. It is not benchmark execution, not "
            "authoritative benchmark pass/fail, not strength evaluation, and not checkpoint "
            "promotion.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M50 emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_BENCHMARK_PASS_CLAIM


def _m49_binding_summary(
    m49: dict[str, Any] | None, *, status_override: str | None
) -> dict[str, Any]:
    if m49 is None:
        return {
            "contract_id": None,
            "profile_id": None,
            "artifact_sha256": None,
            "status": status_override,
            "interpretation": INTERPRETATION_M49_BINDING,
        }
    st = status_override if status_override is not None else str(m49.get("result_status") or "")
    return {
        "contract_id": str(m49.get("contract_id") or ""),
        "profile_id": str(m49.get("profile_id") or ""),
        "artifact_sha256": str(m49.get(DIGEST_FIELD) or "").lower(),
        "status": st,
        "interpretation": INTERPRETATION_M49_BINDING,
    }


def _assemble_m50_body(
    *,
    profile: str,
    m49_plain: dict[str, Any] | None,
    decision: M50Decision,
) -> dict[str, Any]:
    refs_dicts = [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals]

    scorecard_readout = {
        "scorecard_results_seen": decision.scorecard_results_seen,
        "scorecard_total": decision.scorecard_total,
        "win_rate": decision.win_rate,
        "bounded_fields_only": decision.bounded_fields_only,
    }

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M50_READOUT,
        "profile_id": PROFILE_M50_SURFACE,
        "milestone": MILESTONE_LABEL_M50,
        "emitter_module": EMITTER_MODULE_M50,
        "profile": profile,
        "readout_status": decision.readout_status,
        "m49_binding": _m49_binding_summary(m49_plain, status_override=decision.m49_result_status),
        "scorecard_readout": scorecard_readout,
        "benchmark_pass_fail_decision": {
            "decision": decision.benchmark_decision,
            "reason": decision.benchmark_reason,
        },
        "promotion_decision": {
            "decision": decision.promotion_decision,
            "reason": decision.promotion_reason,
        },
        "route_recommendation": {
            "next_route": decision.route_next,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "refusals": refs_dicts,
        "warnings": list(decision.warnings),
        "non_claims": list(NON_CLAIMS_M50),
        **_honesty_false_block(),
    }
    return body


def _emit_m50_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m50_report(sealed)))
    brief = build_m50_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m50_forbidden_flag_refusal(
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
    decision = M50Decision(
        STATUS_READOUT_REFUSED,
        refs,
        (),
        ROUTE_M49_REMEDIATION,
        False,
        None,
        None,
        True,
        BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
        REASON_BENCHMARK_PENDING_SCOPE,
        PROMOTION_REFUSED_PENDING_PASS_FAIL,
        REASON_PROMOTION_PENDING,
        "",
        "",
    )
    body_pre = _assemble_m50_body(profile=profile, m49_plain=None, decision=decision)
    body_pre["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m50_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m50_artifacts(sealed, output_dir)


def emit_m50_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m49_upstream_fixture"
    emit_m49_fixture_ci(sub)
    m49_path = sub / M49_FILENAME_MAIN_JSON
    return emit_m50_operator_preflight(
        output_dir,
        m49_path=m49_path,
        expected_sha256_lower=None,
        profile=PROFILE_FIXTURE_CI,
    )


def emit_m50_operator_preflight(
    output_dir: Path,
    *,
    m49_path: Path | None,
    expected_sha256_lower: str | None,
    profile: str = PROFILE_OPERATOR_PREFLIGHT,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m49_plain: dict[str, Any] | None = None
    if m49_path is not None:
        rp = Path(m49_path).resolve()
        if rp.is_file():
            try:
                m49_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m49_plain = None

    decision = decide_m50_from_m49(
        m49_plain,
        expected_sha256_lower=expected_sha256_lower,
        require_canonical_seal=True,
    )
    body = _assemble_m50_body(
        profile=profile,
        m49_plain=m49_plain,
        decision=decision,
    )
    sealed = seal_m50_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m50_artifacts(sealed, output_dir)


def _validate_declared_overclaims(declared: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for k in M50_DECLARED_OVERCLAIM_KEYS:
        if declared.get(k) is True:
            violations.append(f"declared_truth_on_{k}")

    bfd = declared.get("benchmark_pass_fail_decision")
    if isinstance(bfd, dict):
        d = str(bfd.get("decision") or "")
        if d and d not in ALLOWED_BENCHMARK_DECISIONS:
            violations.append(f"disallowed_benchmark_decision:{d!r}")

    pr = declared.get("promotion_decision")
    if isinstance(pr, dict):
        d = str(pr.get("decision") or "")
        if d and d not in ALLOWED_PROMOTION_DECISIONS:
            violations.append(f"disallowed_promotion_decision:{d!r}")

    return violations


def _synthetic_m49_from_declared(declared_in: dict[str, Any]) -> dict[str, Any] | None:
    mb = declared_in.get("m49_binding")
    summ = declared_in.get("declared_m49_execution_summary")
    if not isinstance(mb, dict) or not isinstance(summ, dict):
        return None
    rs = str(summ.get("result_status") or "").strip()
    if not rs:
        return None
    scr = summ.get("scorecard_result")
    scr_d = scr if isinstance(scr, dict) else {}
    warns = summ.get("warnings")
    w = [str(x) for x in warns] if isinstance(warns, list) else []
    syn: dict[str, Any] = {
        "contract_id": CONTRACT_ID_M49_RESULT,
        "profile_id": PROFILE_M49_SURFACE,
        DIGEST_FIELD: str(mb.get("artifact_sha256") or "").lower(),
        "result_status": rs,
        "scorecard_result": scr_d,
        "warnings": w,
    }
    for k in M49_SUCCESS_FALSE_KEYS:
        syn[k] = summ.get(k, False)
    syn["scorecard_results_produced"] = summ.get("scorecard_results_produced")
    syn["scorecard_total_computed"] = summ.get("scorecard_total_computed")
    syn["win_rate_computed"] = summ.get("win_rate_computed")
    return syn


def emit_m50_operator_declared(
    output_dir: Path,
    *,
    declared_readout_path: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rp = Path(declared_readout_path).resolve()
    raw = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("declared readout must be a JSON object")
    declared_in = cast(dict[str, Any], redact_paths_in_value(raw))

    cid = str(declared_in.get("contract_id") or "")
    pid = str(declared_in.get("profile_id") or "")
    contract_ok = cid == CONTRACT_ID_M50_READOUT and pid == PROFILE_M50_SURFACE

    over = _validate_declared_overclaims(declared_in) if contract_ok else []

    def refuse(decision: M50Decision) -> tuple[dict[str, Any], tuple[Path, ...]]:
        syn_hold = _synthetic_m49_from_declared(declared_in)
        m49_for_bind: dict[str, Any] | None = syn_hold if isinstance(syn_hold, dict) else None
        body = _assemble_m50_body(
            profile=PROFILE_OPERATOR_DECLARED,
            m49_plain=m49_for_bind,
            decision=decision,
        )
        _merge_declared_m49_binding(declared_in, body)
        body["declared_readout_path_logical"] = "operator_supplied"
        sealed = seal_m50_body(cast(dict[str, Any], redact_paths_in_value(body)))
        return _emit_m50_artifacts(sealed, output_dir)

    if not contract_ok:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": f"contract_or_profile_mismatch:{cid!r}:{pid!r}",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    if over:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "declared_overclaim:" + ",".join(over),
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    mb = declared_in.get("m49_binding")
    if not isinstance(mb, dict):
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "m49_binding_missing_or_not_object",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    if str(mb.get("contract_id") or "") != M49_CONTRACT_FOR_BINDING:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "m49_binding_contract_id_mismatch",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    if str(mb.get("profile_id") or "") != M49_PROFILE_FOR_BINDING:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "m49_binding_profile_id_mismatch",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    if not _sha_like(mb.get("artifact_sha256")):
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "m49_binding_artifact_sha256_invalid",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    syn = _synthetic_m49_from_declared(declared_in)
    if syn is None:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": "declared_m49_execution_summary_missing_or_invalid",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    st_bind = str(mb.get("status") or "").strip()
    st_summ = str(syn.get("result_status") or "").strip()
    if st_bind and st_summ and st_bind != st_summ:
        decision = M50Decision(
            STATUS_READOUT_REFUSED,
            (
                {
                    "code": REFUSED_DECLARED_SHAPE,
                    "detail": f"m49_binding_status_mismatch:{st_bind!r}:{st_summ!r}",
                },
            ),
            (),
            ROUTE_M49_REMEDIATION,
            False,
            None,
            None,
            True,
            BENCHMARK_PASS_FAIL_REFUSED_PENDING_AUTHORITY,
            REASON_BENCHMARK_PENDING_SCOPE,
            PROMOTION_REFUSED_PENDING_PASS_FAIL,
            REASON_PROMOTION_PENDING,
            "",
            "",
        )
        return refuse(decision)

    decision = decide_m50_from_m49(
        syn,
        expected_sha256_lower=None,
        require_canonical_seal=False,
    )
    body = _assemble_m50_body(
        profile=PROFILE_OPERATOR_DECLARED,
        m49_plain=syn,
        decision=decision,
    )
    _merge_declared_m49_binding(declared_in, body)
    nc = declared_in.get("non_claims")
    if isinstance(nc, list) and nc:
        base_nc = list(body.get("non_claims") or [])
        body["non_claims"] = base_nc + [str(x) for x in nc]
    body["declared_readout_path_logical"] = "operator_supplied"
    sealed = seal_m50_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m50_artifacts(sealed, output_dir)


def _merge_declared_m49_binding(declared_in: dict[str, Any], body: dict[str, Any]) -> None:
    mb_keep = declared_in.get("m49_binding")
    if isinstance(mb_keep, dict):
        body["m49_binding"] = {
            "contract_id": mb_keep.get("contract_id"),
            "profile_id": mb_keep.get("profile_id"),
            "artifact_sha256": mb_keep.get("artifact_sha256"),
            "status": mb_keep.get("status"),
            "interpretation": mb_keep.get("interpretation") or INTERPRETATION_M49_BINDING,
        }


__all__ = (
    "M50Decision",
    "build_m50_brief_md",
    "decide_m50_from_m49",
    "emit_m50_fixture_ci",
    "emit_m50_forbidden_flag_refusal",
    "emit_m50_operator_declared",
    "emit_m50_operator_preflight",
    "m49_upstream_honesty_or_overclaim_violation",
    "refusal_code_from_forbidden_flags",
    "seal_m50_body",
    "structural_m49_issues_for_m50",
)
