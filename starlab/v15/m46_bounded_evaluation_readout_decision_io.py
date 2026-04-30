"""V15-M46 — bounded evaluation readout / promotion-refusal decision (consumes sealed M45)."""

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
from starlab.v15.m45_bounded_candidate_evaluation_execution_io import emit_m45_fixture_ci
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    ALLOWED_CLAIM_DECISION_VALUES,
    BRIEF_FILENAME,
    CLAIM_BENCHMARK_REFUSED,
    CLAIM_HUMAN_PANEL_REFUSED,
    CLAIM_PROMOTION_REFUSED,
    CLAIM_SCORECARD_REFUSED,
    CLAIM_SHOWCASE_REFUSED,
    CLAIM_STRENGTH_REFUSED,
    CLAIM_T2_T5_REFUSED,
    CLAIM_V2_REFUSED,
    CLAIM_XAI_REFUSED,
    CONTRACT_ID_M45_EXECUTION,
    CONTRACT_ID_M46_READOUT,
    DIGEST_FIELD,
    EMITTER_MODULE_M46,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    INTERPRETATION_M45_BINDING,
    M45_HONESTY_BOOL_KEYS,
    M45_STATUS_COMPLETED_SYNTHETIC,
    M45_STATUS_NOT_READY,
    M45_STATUS_SURFACE_READY,
    MILESTONE_LABEL_M46,
    NON_CLAIMS_M46,
    PROFILE_FIXTURE_CI,
    PROFILE_M45_EXECUTION,
    PROFILE_M46_READOUT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    PROMOTION_REFUSAL_REASON_DEFAULT,
    PROMOTION_REFUSED_INSUFFICIENT,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_DECLARED_SHAPE,
    REFUSED_INVALID_M45,
    REFUSED_M45_HONESTY,
    REFUSED_M45_NOT_READY,
    REFUSED_M45_SYNTHETIC_OVERINTERPRET,
    REFUSED_MISSING_M45,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_BENCHMARK_DESIGN,
    ROUTE_TO_M45_REMEDIATION,
    SCHEMA_VERSION,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_SYNTH_WARNING,
    STATUS_READOUT_REFUSED,
)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _m45_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def structural_m45_issues(m45: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m45.get("contract_id", "")) != CONTRACT_ID_M45_EXECUTION:
        errs.append("m45_contract_id_mismatch")
    if str(m45.get("profile_id", "")) != PROFILE_M45_EXECUTION:
        errs.append("m45_profile_id_mismatch")
    if not _m45_seal_ok(m45):
        errs.append("m45_seal_invalid")
    return errs


def honesty_violation_m45(m45: dict[str, Any]) -> bool:
    return any(m45.get(k) is True for k in M45_HONESTY_BOOL_KEYS)


def synthetic_receipt_overinterpreted(m45: dict[str, Any]) -> bool:
    if m45.get("synthetic_execution_receipt_emitted") is not True:
        return False
    rec = m45.get("execution_receipt")
    if not isinstance(rec, dict):
        return False
    bm = rec.get("benchmark_mode")
    sm = rec.get("scorecard_mode")
    if bm not in (None, "none"):
        return True
    if sm not in (None, "none"):
        return True
    return False


def _execution_status_str(m45: dict[str, Any]) -> str:
    return str(m45.get("execution_status") or "")


def _synthetic_receipt_status(m45: dict[str, Any]) -> str:
    if m45.get("synthetic_execution_receipt_emitted") is True:
        return "synthetic_execution_receipt_emitted"
    return "no_synthetic_receipt"


def _default_claim_decisions() -> dict[str, str]:
    return {
        "benchmark_pass_fail": CLAIM_BENCHMARK_REFUSED,
        "scorecard_results": CLAIM_SCORECARD_REFUSED,
        "strength_evaluation": CLAIM_STRENGTH_REFUSED,
        "checkpoint_promotion": CLAIM_PROMOTION_REFUSED,
        "xai": CLAIM_XAI_REFUSED,
        "human_panel": CLAIM_HUMAN_PANEL_REFUSED,
        "showcase": CLAIM_SHOWCASE_REFUSED,
        "v2": CLAIM_V2_REFUSED,
        "t2_t5": CLAIM_T2_T5_REFUSED,
    }


def _honesty_false_block() -> dict[str, Any]:
    return {k: False for k in M45_HONESTY_BOOL_KEYS}


def _m45_snapshot(m45: dict[str, Any]) -> dict[str, Any]:
    return {k: m45.get(k) for k in M45_HONESTY_BOOL_KEYS}


@dataclass(frozen=True)
class M46Decision:
    decision_status: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    route_next: str
    route_warning: str | None


def decide_m46_from_m45(m45: dict[str, Any] | None) -> M46Decision:
    refs: list[dict[str, str]] = []

    def _ref(code: str, detail: str) -> None:
        refs.append({"code": code, "detail": detail})

    if m45 is None:
        _ref(REFUSED_MISSING_M45, "m45_execution_json_missing_or_unreadable")
        return M46Decision(
            STATUS_READOUT_REFUSED,
            tuple(refs),
            (),
            ROUTE_TO_M45_REMEDIATION,
            None,
        )

    struct = structural_m45_issues(m45)
    if struct:
        _ref(REFUSED_INVALID_M45, ",".join(struct))
        return M46Decision(
            STATUS_READOUT_REFUSED,
            tuple(refs),
            (),
            ROUTE_TO_M45_REMEDIATION,
            None,
        )

    if honesty_violation_m45(m45):
        _ref(REFUSED_M45_HONESTY, "m45_honesty_flags_must_remain_false")
        return M46Decision(
            STATUS_READOUT_REFUSED,
            tuple(refs),
            (),
            ROUTE_TO_M45_REMEDIATION,
            None,
        )

    if synthetic_receipt_overinterpreted(m45):
        _ref(
            REFUSED_M45_SYNTHETIC_OVERINTERPRET,
            "m45_synthetic_receipt_carrier_overclaims_benchmark_or_scorecard_modes",
        )
        return M46Decision(
            STATUS_READOUT_REFUSED,
            tuple(refs),
            (),
            ROUTE_TO_M45_REMEDIATION,
            None,
        )

    es = _execution_status_str(m45)
    if es == M45_STATUS_NOT_READY or es.startswith("refused_"):
        detail = es if es else "missing_execution_status"
        _ref(REFUSED_M45_NOT_READY, detail)
        return M46Decision(
            STATUS_READOUT_REFUSED,
            tuple(refs),
            (),
            ROUTE_TO_M45_REMEDIATION,
            None,
        )

    warns: list[str] = []
    if es == M45_STATUS_SURFACE_READY:
        return M46Decision(
            STATUS_READOUT_COMPLETED,
            tuple(refs),
            (),
            ROUTE_TO_BENCHMARK_DESIGN,
            None,
        )

    if es == M45_STATUS_COMPLETED_SYNTHETIC:
        warns.append(
            "m45_bounded_candidate_evaluation_execution_completed_synthetic_is_synthetic_receipt_only"
        )
        return M46Decision(
            STATUS_READOUT_COMPLETED_SYNTH_WARNING,
            tuple(refs),
            tuple(warns),
            ROUTE_TO_BENCHMARK_DESIGN,
            "synthetic_execution_bookkeeping_only_not_benchmark_execution",
        )

    _ref(REFUSED_M45_NOT_READY, f"m45_execution_status_not_eligible:{es}")
    return M46Decision(
        STATUS_READOUT_REFUSED,
        tuple(refs),
        (),
        ROUTE_TO_M45_REMEDIATION,
        None,
    )


def seal_m46_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m46_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_evaluation_readout_decision_report",
        "report_version": "m46",
        "milestone": MILESTONE_LABEL_M46,
        "contract_id": CONTRACT_ID_M46_READOUT,
        "profile_id": PROFILE_M46_READOUT,
        DIGEST_FIELD: digest,
        "decision_status": sealed.get("decision_status"),
        "m45_execution_status_summarized": (sealed.get("m45_binding") or {}).get(
            "execution_status"
        ),
    }


def build_m46_brief_md(*, sealed: dict[str, Any]) -> str:
    m45b = sealed.get("m45_binding") or {}
    claims = sealed.get("claim_decisions") or {}
    promo = sealed.get("promotion_decision") or {}
    route = sealed.get("route_recommendation") or {}
    ncl = sealed.get("non_claims") or []
    lines = [
        "# V15-M46 bounded evaluation readout decision brief",
        "",
        "## M45 binding summary",
        f"- `contract_id`: `{m45b.get('contract_id', '')}`",
        f"- `profile_id`: `{m45b.get('profile_id', '')}`",
        f"- `artifact_sha256`: `{m45b.get('artifact_sha256', '')}`",
        f"- `execution_status`: `{m45b.get('execution_status', '')}`",
        f"- `synthetic_receipt_status`: `{m45b.get('synthetic_receipt_status', '')}`",
        "",
        "## M45 execution-status interpretation",
        f"- `interpretation`: `{m45b.get('interpretation', '')}`",
        "",
        "## Claim decisions",
    ]
    for k, v in sorted(claims.items()) if isinstance(claims, dict) else []:
        lines.append(f"- `{k}` → `{v}`")
    lines.extend(
        [
            "",
            "## Promotion refusal decision",
            f"- `promotion_status`: `{promo.get('promotion_status', '')}`",
            f"- `reason`: {promo.get('reason', '')}",
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
            "This brief is a readout/refusal decision over bounded execution bookkeeping. It is "
            "not benchmark pass/fail evidence, scorecard results, strength evaluation, or "
            "checkpoint promotion.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M46 emission leaked path patterns into public artifacts")


def _assemble_m46_body(
    *,
    profile: str,
    m45_plain: dict[str, Any] | None,
    decision: M46Decision,
) -> dict[str, Any]:
    digest45 = ""
    bind45: dict[str, Any] = {
        "contract_id": None,
        "profile_id": None,
        "artifact_sha256": None,
        "execution_status": None,
        "synthetic_receipt_status": None,
        "interpretation": INTERPRETATION_M45_BINDING,
    }
    snapshot: dict[str, Any] = {}
    if m45_plain is not None:
        digest45 = str(m45_plain.get(DIGEST_FIELD) or "").lower()
        snapshot = _m45_snapshot(m45_plain)
        bind45 = {
            "contract_id": CONTRACT_ID_M45_EXECUTION,
            "profile_id": PROFILE_M45_EXECUTION,
            "artifact_sha256": digest45 if digest45 else None,
            "execution_status": _execution_status_str(m45_plain),
            "synthetic_receipt_status": _synthetic_receipt_status(m45_plain),
            "interpretation": INTERPRETATION_M45_BINDING,
        }

    route_warn = decision.route_warning
    route_warnings = [route_warn] if route_warn else []

    promo_status = PROMOTION_REFUSED_INSUFFICIENT
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M46_READOUT,
        "profile_id": PROFILE_M46_READOUT,
        "milestone": MILESTONE_LABEL_M46,
        "emitter_module": EMITTER_MODULE_M46,
        "profile": profile,
        "decision_status": decision.decision_status,
        "m45_binding": bind45,
        "m45_upstream_honesty_snapshot": snapshot,
        "claim_decisions": _default_claim_decisions(),
        "promotion_decision": {
            "promotion_status": promo_status,
            "reason": PROMOTION_REFUSAL_REASON_DEFAULT,
        },
        "route_recommendation": {
            "next_route": decision.route_next,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
            "route_warnings": route_warnings,
        },
        "refusals": [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals],
        "warnings": list(decision.warnings),
        "non_claims": list(NON_CLAIMS_M46),
        **_honesty_false_block(),
    }
    return body


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_BENCHMARK_PASS_CLAIM


def emit_m46_forbidden_flag_refusal(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
    refusal_code_override: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_override or refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    bind45 = {
        "contract_id": None,
        "profile_id": None,
        "artifact_sha256": None,
        "execution_status": None,
        "synthetic_receipt_status": None,
        "interpretation": INTERPRETATION_M45_BINDING,
    }
    refs = [{"code": primary, "detail": "forbidden_cli_flags:" + ",".join(bad)}]
    decision = M46Decision(STATUS_READOUT_REFUSED, tuple(refs), (), ROUTE_TO_M45_REMEDIATION, None)
    body_pre = _assemble_m46_body(profile=profile, m45_plain=None, decision=decision)
    body_pre["m45_binding"] = bind45
    body_pre["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m46_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m46_artifacts(sealed, output_dir)


def _emit_m46_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m46_report(sealed)))
    brief = build_m46_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m46_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m45_upstream_fixture"
    m45_sealed, _ = emit_m45_fixture_ci(sub)
    m45_path = sub / "v15_bounded_candidate_evaluation_execution.json"
    m45_plain = _parse_json_object(m45_path)
    decision = decide_m46_from_m45(m45_plain)
    body = _assemble_m46_body(
        profile=PROFILE_FIXTURE_CI,
        m45_plain=m45_plain,
        decision=decision,
    )
    sealed = seal_m46_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m46_artifacts(sealed, output_dir)


def emit_m46_operator_preflight(
    output_dir: Path,
    *,
    m45_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m45_plain: dict[str, Any] | None = None
    if m45_path is not None:
        rp = Path(m45_path).resolve()
        if rp.is_file():
            try:
                m45_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m45_plain = None
    decision = decide_m46_from_m45(m45_plain)
    body = _assemble_m46_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m45_plain=m45_plain,
        decision=decision,
    )
    sealed = seal_m46_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m46_artifacts(sealed, output_dir)


def _validate_declared_overclaims(declared: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for k in M45_HONESTY_BOOL_KEYS:
        if declared.get(k) is True:
            violations.append(f"declared_truth_on_{k}")

    cds = declared.get("claim_decisions")
    if isinstance(cds, dict):
        for _key, val in cds.items():
            if val not in ALLOWED_CLAIM_DECISION_VALUES:
                violations.append(f"disallowed_claim_decision:{_key}:{val}")

    promo = declared.get("promotion_decision")
    if isinstance(promo, dict):
        ps = str(promo.get("promotion_status") or "")
        if ps and ps not in (
            PROMOTION_REFUSED_INSUFFICIENT,
            "promotion_not_considered_no_scorecard_results",
        ):
            violations.append(f"disallowed_promotion_status:{ps}")

    if str(declared.get("decision_status") or "") == STATUS_READOUT_COMPLETED:
        mb = declared.get("m45_binding")
        if isinstance(mb, dict):
            es = str(mb.get("execution_status") or "")
            if es == M45_STATUS_COMPLETED_SYNTHETIC:
                warns = declared.get("warnings")
                synth_warn_ok = isinstance(warns, list) and any(
                    "synthetic" in str(w).lower() for w in warns
                )
                if not synth_warn_ok:
                    violations.append(
                        "completed_without_synthetic_warning_for_synthetic_m45_binding"
                    )

    return violations


def _decision_from_declared_m45_binding(
    m45_bind: dict[str, Any],
    *,
    extra_refs: tuple[dict[str, str], ...],
) -> M46Decision:
    es = str(m45_bind.get("execution_status") or "")
    if es == M45_STATUS_SURFACE_READY:
        return M46Decision(
            STATUS_READOUT_COMPLETED,
            extra_refs,
            (),
            ROUTE_TO_BENCHMARK_DESIGN,
            None,
        )
    if es == M45_STATUS_COMPLETED_SYNTHETIC:
        return M46Decision(
            STATUS_READOUT_COMPLETED_SYNTH_WARNING,
            extra_refs,
            (
                "m45_bounded_candidate_evaluation_execution_completed_synthetic_is_synthetic_receipt_only",
            ),
            ROUTE_TO_BENCHMARK_DESIGN,
            "synthetic_execution_bookkeeping_only_not_benchmark_execution",
        )
    if es == M45_STATUS_NOT_READY or (es.startswith("refused_") and es):
        _refs = list(extra_refs) + [
            {"code": REFUSED_M45_NOT_READY, "detail": es or "missing_upstream_execution_status"}
        ]
        return M46Decision(STATUS_READOUT_REFUSED, tuple(_refs), (), ROUTE_TO_M45_REMEDIATION, None)
    _refs = list(extra_refs) + [
        {
            "code": REFUSED_M45_NOT_READY,
            "detail": f"unexpected_declared_execution_status:{es!r}",
        }
    ]
    return M46Decision(STATUS_READOUT_REFUSED, tuple(_refs), (), ROUTE_TO_M45_REMEDIATION, None)


def emit_m46_operator_declared(
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
    contract_ok = cid == CONTRACT_ID_M46_READOUT and pid == PROFILE_M46_READOUT

    over = _validate_declared_overclaims(declared_in) if contract_ok else []
    over_refs: tuple[dict[str, str], ...] = ()
    if over:
        over_refs = (
            {
                "code": REFUSED_BENCHMARK_PASS_CLAIM,
                "detail": "declared_overclaim:" + ",".join(over),
            },
        )

    if not contract_ok:
        refs = (
            {
                "code": REFUSED_DECLARED_SHAPE,
                "detail": f"contract_or_profile_mismatch:{cid!r}:{pid!r}",
            },
        )
        decision = M46Decision(STATUS_READOUT_REFUSED, refs, (), ROUTE_TO_M45_REMEDIATION, None)
    elif over_refs:
        decision = M46Decision(
            STATUS_READOUT_REFUSED, over_refs, (), ROUTE_TO_M45_REMEDIATION, None
        )
    else:
        m45_bind = declared_in.get("m45_binding")
        if not isinstance(m45_bind, dict):
            decision = M46Decision(
                STATUS_READOUT_REFUSED,
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m45_binding_missing_or_not_object",
                    },
                ),
                (),
                ROUTE_TO_M45_REMEDIATION,
                None,
            )
        elif not str(m45_bind.get("artifact_sha256") or "").strip():
            decision = M46Decision(
                STATUS_READOUT_REFUSED,
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m45_binding_artifact_sha256_required",
                    },
                ),
                (),
                ROUTE_TO_M45_REMEDIATION,
                None,
            )
        else:
            decision = _decision_from_declared_m45_binding(m45_bind, extra_refs=())

    m45_bind_out = declared_in.get("m45_binding")
    body = _assemble_m46_body(
        profile=PROFILE_OPERATOR_DECLARED,
        m45_plain=None,
        decision=decision,
    )
    if isinstance(m45_bind_out, dict):
        body["m45_binding"] = {
            "contract_id": m45_bind_out.get("contract_id"),
            "profile_id": m45_bind_out.get("profile_id"),
            "artifact_sha256": m45_bind_out.get("artifact_sha256"),
            "execution_status": m45_bind_out.get("execution_status"),
            "synthetic_receipt_status": m45_bind_out.get("synthetic_receipt_status"),
            "interpretation": m45_bind_out.get("interpretation") or INTERPRETATION_M45_BINDING,
        }
    body["declared_readout_path_logical"] = "operator_supplied"
    sealed = seal_m46_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m46_artifacts(sealed, output_dir)


__all__ = (
    "M46Decision",
    "build_m46_brief_md",
    "decide_m46_from_m45",
    "emit_m46_fixture_ci",
    "emit_m46_forbidden_flag_refusal",
    "emit_m46_operator_declared",
    "emit_m46_operator_preflight",
    "honesty_violation_m45",
    "refusal_code_from_forbidden_flags",
    "seal_m46_body",
    "structural_m45_issues",
    "synthetic_receipt_overinterpreted",
)
