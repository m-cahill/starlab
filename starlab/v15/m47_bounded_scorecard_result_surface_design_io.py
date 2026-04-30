"""V15-M47 — bounded scorecard result surface design / refusal gate (consumes sealed M46)."""

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
from starlab.v15.m46_bounded_evaluation_readout_decision_io import emit_m46_fixture_ci
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    CONTRACT_ID_M46_READOUT,
    PROFILE_M46_READOUT,
    PROMOTION_NOT_CONSIDERED,
    PROMOTION_REFUSED_INSUFFICIENT,
    STATUS_READOUT_COMPLETED,
    STATUS_READOUT_COMPLETED_SYNTH_WARNING,
    STATUS_READOUT_REFUSED,
)
from starlab.v15.m46_bounded_evaluation_readout_decision_models import (
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED as M46_ROUTE_STATUS,
)
from starlab.v15.m47_bounded_scorecard_result_surface_design_models import (
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
    CONTRACT_ID_M47_SURFACE,
    DIGEST_FIELD,
    EMITTER_MODULE_M47,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    INTERPRETATION_M46_BINDING,
    M46_BODY_BOOL_KEYS,
    M47_ALWAYS_FALSE_KEYS,
    MILESTONE_LABEL_M47,
    NON_CLAIMS_M47,
    PROFILE_FIXTURE_CI,
    PROFILE_M47_REFUSAL_GATE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_BENCHMARK_PASS_CLAIM,
    REFUSED_DECLARED_SHAPE,
    REFUSED_INVALID_M46,
    REFUSED_M46_HONESTY,
    REFUSED_M46_NOT_COMPLETED,
    REFUSED_M46_PROMOTION_NOT_REFUSED,
    REFUSED_M46_ROUTE_EXECUTED,
    REFUSED_M46_SCORECARD_PRESENT,
    REFUSED_MISSING_M46,
    REFUSED_SCORECARD_RESULTS_CLAIM,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    ROUTE_TO_M46_REMEDIATION,
    ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
    SCHEMA_VERSION,
    STATUS_DESIGN_READY,
    STATUS_DESIGN_READY_WARNINGS,
    STATUS_DESIGN_REFUSED,
)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _m46_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def structural_m46_issues_for_m47(m46: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m46.get("contract_id", "")) != CONTRACT_ID_M46_READOUT:
        errs.append("m46_contract_id_mismatch")
    if str(m46.get("profile_id", "")) != PROFILE_M46_READOUT:
        errs.append("m46_profile_id_mismatch")
    if not _m46_seal_ok(m46):
        errs.append("m46_seal_invalid")
    return errs


def honesty_violation_m46_body(m46: dict[str, Any]) -> bool:
    return any(m46.get(k) is True for k in M46_BODY_BOOL_KEYS)


def _route_status(m46: dict[str, Any]) -> str:
    rr = m46.get("route_recommendation")
    if not isinstance(rr, dict):
        return ""
    return str(rr.get("route_status") or "")


def _promotion_status(m46: dict[str, Any]) -> str:
    pr = m46.get("promotion_decision")
    if not isinstance(pr, dict):
        return ""
    return str(pr.get("promotion_status") or "")


def _decision_status_str(m46: dict[str, Any]) -> str:
    return str(m46.get("decision_status") or "")


ALLOWED_M46_PROMOTION: frozenset[str] = frozenset(
    {PROMOTION_REFUSED_INSUFFICIENT, PROMOTION_NOT_CONSIDERED}
)


def build_scorecard_surface_design_block() -> dict[str, Any]:
    return {
        "surface_status": "designed_not_executed",
        "future_result_surface_allowed_in_m47": False,
        "future_result_surface_requires_separate_milestone": True,
        "future_contract_id": "starlab.v15.bounded_scorecard_result_execution.v1",
        "future_profile_id": "starlab.v15.m48.bounded_scorecard_execution_preflight.v1",
        "future_result_artifact_names": [
            "v15_bounded_scorecard_result_execution.json",
            "v15_bounded_scorecard_result_execution_report.json",
            "v15_bounded_scorecard_result_execution_brief.md",
        ],
        "required_future_inputs": [
            "sealed_benchmark_protocol",
            "sealed_candidate_identity",
            "sealed_execution_receipt",
            "sealed_match_or_episode_evidence",
            "scorecard_metric_results",
            "public_private_boundary_report",
        ],
        "required_future_metric_groups": [
            "artifact_integrity",
            "candidate_identity",
            "execution_validity",
            "baseline_scope",
            "gameplay_outcome_summary",
            "scorecard_metric_results",
            "threshold_decision",
            "failure_mode_probe_summary",
            "xai_or_human_panel_dependencies",
            "claim_boundaries",
        ],
        "future_required_fields": [
            "scorecard_contract_id",
            "scorecard_profile_id",
            "candidate_checkpoint_sha256",
            "candidate_lineage_binding",
            "benchmark_protocol_binding",
            "execution_receipt_binding",
            "match_or_episode_evidence_bindings",
            "opponent_or_baseline_scope",
            "map_pool_scope",
            "metric_results",
            "threshold_policy",
            "pass_fail_interpretation",
            "failure_mode_results",
            "non_claims",
            "public_private_boundary",
            "artifact_sha256",
        ],
        "result_fields_not_present_in_m47": [
            "benchmark_passed",
            "win_rate",
            "scorecard_total",
            "threshold_pass_fail",
            "strength_rating",
            "promotion_decision",
        ],
        "m47_result_status": "no_scorecard_results_in_m47",
    }


def _default_claim_decisions() -> dict[str, str]:
    return {
        "scorecard_results": CLAIM_SCORECARD_REFUSED,
        "benchmark_pass_fail": CLAIM_BENCHMARK_REFUSED,
        "strength_evaluation": CLAIM_STRENGTH_REFUSED,
        "checkpoint_promotion": CLAIM_PROMOTION_REFUSED,
        "xai": CLAIM_XAI_REFUSED,
        "human_panel": CLAIM_HUMAN_PANEL_REFUSED,
        "showcase": CLAIM_SHOWCASE_REFUSED,
        "v2": CLAIM_V2_REFUSED,
        "t2_t5": CLAIM_T2_T5_REFUSED,
    }


def _honesty_false_block_m47() -> dict[str, Any]:
    return {k: False for k in M47_ALWAYS_FALSE_KEYS}


def _m46_honesty_snapshot(m46: dict[str, Any]) -> dict[str, Any]:
    return {k: m46.get(k) for k in M46_BODY_BOOL_KEYS}


def _m46_binding_summary(m46: dict[str, Any] | None) -> dict[str, Any]:
    if m46 is None:
        return {
            "contract_id": None,
            "profile_id": None,
            "artifact_sha256": None,
            "decision_status": None,
            "promotion_status": None,
            "interpretation": INTERPRETATION_M46_BINDING,
        }
    pr = m46.get("promotion_decision")
    ps = ""
    if isinstance(pr, dict):
        ps = str(pr.get("promotion_status") or "")
    return {
        "contract_id": str(m46.get("contract_id") or ""),
        "profile_id": str(m46.get("profile_id") or ""),
        "artifact_sha256": str(m46.get(DIGEST_FIELD) or "").lower(),
        "decision_status": _decision_status_str(m46),
        "promotion_status": ps,
        "interpretation": INTERPRETATION_M46_BINDING,
    }


@dataclass(frozen=True)
class M47Decision:
    design_status: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    route_next: str


def decide_m47_from_m46(m46: dict[str, Any] | None) -> M47Decision:
    refs: list[dict[str, str]] = []

    def _ref(code: str, detail: str) -> None:
        refs.append({"code": code, "detail": detail})

    if m46 is None:
        _ref(REFUSED_MISSING_M46, "m46_readout_json_missing_or_unreadable")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    struct = structural_m46_issues_for_m47(m46)
    if struct:
        _ref(REFUSED_INVALID_M46, ",".join(struct))
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    if m46.get("scorecard_results_produced") is True:
        _ref(REFUSED_M46_SCORECARD_PRESENT, "m46_claimed_scorecard_results_true")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    if honesty_violation_m46_body(m46):
        _ref(REFUSED_M46_HONESTY, "m46_honesty_flags_must_remain_false")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    rstat = _route_status(m46)
    if rstat != M46_ROUTE_STATUS:
        _ref(
            REFUSED_M46_ROUTE_EXECUTED,
            f"m46_route_status_not_recommended_not_executed:{rstat!r}",
        )
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    pstat = _promotion_status(m46)
    if pstat not in ALLOWED_M46_PROMOTION:
        _ref(
            REFUSED_M46_PROMOTION_NOT_REFUSED,
            f"disallowed_m46_promotion_status:{pstat!r}",
        )
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    ds = _decision_status_str(m46)
    if ds == STATUS_READOUT_REFUSED or (ds.startswith("refused_") and ds):
        _ref(REFUSED_M46_NOT_COMPLETED, ds or "m46_readout_refused")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    warns: list[str] = []
    if ds == STATUS_READOUT_COMPLETED:
        return M47Decision(
            STATUS_DESIGN_READY,
            tuple(refs),
            (),
            ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
        )

    if ds == STATUS_READOUT_COMPLETED_SYNTH_WARNING:
        upstream = m46.get("warnings")
        if isinstance(upstream, list):
            warns.extend(str(w) for w in upstream)
        warns.append("m46_bounded_evaluation_readout_completed_with_synthetic_only_warning_carried")
        return M47Decision(
            STATUS_DESIGN_READY_WARNINGS,
            tuple(refs),
            tuple(warns),
            ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
        )

    _ref(REFUSED_M46_NOT_COMPLETED, f"m46_decision_status_not_eligible:{ds!r}")
    return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)


def decide_m47_from_declared_m46_binding(mb: dict[str, Any]) -> M47Decision:
    """Validate operator_declared `m46_binding` without requiring a sealed M46 artifact."""
    refs: list[dict[str, str]] = []

    def _ref(code: str, detail: str) -> None:
        refs.append({"code": code, "detail": detail})

    cid = str(mb.get("contract_id") or "")
    pid = str(mb.get("profile_id") or "")
    if cid and cid != CONTRACT_ID_M46_READOUT:
        _ref(REFUSED_INVALID_M46, f"declared_m46_contract_id_mismatch:{cid!r}")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)
    if pid and pid != PROFILE_M46_READOUT:
        _ref(REFUSED_INVALID_M46, f"declared_m46_profile_id_mismatch:{pid!r}")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    if mb.get("scorecard_results_produced") is True:
        _ref(REFUSED_M46_SCORECARD_PRESENT, "declared_binding_claimed_scorecard_results_true")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    rr = mb.get("route_recommendation")
    rstat = str(rr.get("route_status") or "") if isinstance(rr, dict) else ""
    if rstat != M46_ROUTE_STATUS:
        _ref(
            REFUSED_M46_ROUTE_EXECUTED,
            f"m46_route_status_not_recommended_not_executed:{rstat!r}",
        )
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    pr = mb.get("promotion_decision")
    pstat = (
        str(pr.get("promotion_status") or "")
        if isinstance(pr, dict)
        else str(mb.get("promotion_status") or "")
    )
    if pstat not in ALLOWED_M46_PROMOTION:
        _ref(
            REFUSED_M46_PROMOTION_NOT_REFUSED,
            f"disallowed_m46_promotion_status:{pstat!r}",
        )
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    for k in M46_BODY_BOOL_KEYS:
        if k == "scorecard_results_produced":
            continue
        if mb.get(k) is True:
            _ref(REFUSED_M46_HONESTY, f"declared_m46_binding_truth_on_{k}")
            return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    ds = str(mb.get("decision_status") or "")
    if ds == STATUS_READOUT_REFUSED or (ds.startswith("refused_") and ds):
        _ref(REFUSED_M46_NOT_COMPLETED, ds or "m46_readout_refused")
        return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)

    if ds == STATUS_READOUT_COMPLETED:
        return M47Decision(
            STATUS_DESIGN_READY,
            tuple(refs),
            (),
            ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
        )

    if ds == STATUS_READOUT_COMPLETED_SYNTH_WARNING:
        warns_in = mb.get("warnings")
        warns: list[str] = []
        if isinstance(warns_in, list):
            warns.extend(str(w) for w in warns_in)
        warns.append("m46_bounded_evaluation_readout_completed_with_synthetic_only_warning_carried")
        return M47Decision(
            STATUS_DESIGN_READY_WARNINGS,
            tuple(refs),
            tuple(warns),
            ROUTE_TO_SCORECARD_EXEC_PREFLIGHT,
        )

    _ref(REFUSED_M46_NOT_COMPLETED, f"m46_decision_status_not_eligible:{ds!r}")
    return M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)


def seal_m47_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m47_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_scorecard_result_surface_design_report",
        "report_version": "m47",
        "milestone": MILESTONE_LABEL_M47,
        "contract_id": CONTRACT_ID_M47_SURFACE,
        "profile_id": PROFILE_M47_REFUSAL_GATE,
        DIGEST_FIELD: digest,
        "design_status": sealed.get("design_status"),
        "m46_decision_status_summarized": (sealed.get("m46_binding") or {}).get("decision_status"),
    }


def build_m47_brief_md(*, sealed: dict[str, Any]) -> str:
    m46b = sealed.get("m46_binding") or {}
    sdesign = sealed.get("scorecard_surface_design") or {}
    sd_ok = isinstance(sdesign, dict)
    claims = sealed.get("claim_decisions") or {}
    route = sealed.get("route_recommendation") or {}
    ncl = sealed.get("non_claims") or []
    rfi = sdesign.get("required_future_inputs") if sd_ok else None

    lines = [
        "# V15-M47 bounded scorecard result surface design brief",
        "",
        "## M46 binding summary",
        f"- `contract_id`: `{m46b.get('contract_id', '')}`",
        f"- `profile_id`: `{m46b.get('profile_id', '')}`",
        f"- `artifact_sha256`: `{m46b.get('artifact_sha256', '')}`",
        f"- `decision_status`: `{m46b.get('decision_status', '')}`",
        f"- `promotion_status`: `{m46b.get('promotion_status', '')}`",
        f"- `interpretation`: `{m46b.get('interpretation', '')}`",
        "",
        "## M46 readout interpretation",
        "- Sealed M46 readout completion is **readout/refusal bookkeeping only** — not scorecard "
        "results or benchmark pass/fail.",
        "",
        "## Scorecard surface design",
        f"- `surface_status`: `{sdesign.get('surface_status', '') if sd_ok else ''}`",
        f"- `future_contract_id`: `{sdesign.get('future_contract_id', '') if sd_ok else ''}`",
        f"- `future_profile_id`: `{sdesign.get('future_profile_id', '') if sd_ok else ''}`",
        f"- `m47_result_status`: `{sdesign.get('m47_result_status', '') if sd_ok else ''}`",
        "",
        "## Future required result inputs",
    ]
    if isinstance(rfi, list):
        lines.extend([f"- `{x}`" for x in rfi])
    else:
        lines.append("- _(see sealed JSON `scorecard_surface_design.required_future_inputs`)_")
    lines.extend(
        [
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
            "This brief defines a future bounded scorecard result surface and refusal gate. It is "
            "not scorecard results, benchmark pass/fail evidence, strength evaluation, or "
            "checkpoint promotion.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M47 emission leaked path patterns into public artifacts")


def _assemble_m47_body(
    *,
    profile: str,
    m46_plain: dict[str, Any] | None,
    decision: M47Decision,
) -> dict[str, Any]:
    snapshot = _m46_honesty_snapshot(m46_plain) if m46_plain is not None else {}

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M47_SURFACE,
        "profile_id": PROFILE_M47_REFUSAL_GATE,
        "milestone": MILESTONE_LABEL_M47,
        "emitter_module": EMITTER_MODULE_M47,
        "profile": profile,
        "design_status": decision.design_status,
        "m46_binding": _m46_binding_summary(m46_plain),
        "m46_upstream_honesty_snapshot": snapshot,
        "scorecard_surface_design": build_scorecard_surface_design_block(),
        "claim_decisions": _default_claim_decisions(),
        "route_recommendation": {
            "next_route": decision.route_next,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "refusals": [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals],
        "warnings": list(decision.warnings),
        "non_claims": list(NON_CLAIMS_M47),
        **_honesty_false_block_m47(),
    }
    return body


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_SCORECARD_RESULTS_CLAIM


def emit_m47_forbidden_flag_refusal(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
    refusal_code_override: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_override or refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    refs: list[dict[str, str]] = [
        {"code": primary, "detail": "forbidden_cli_flags:" + ",".join(bad)}
    ]
    decision = M47Decision(STATUS_DESIGN_REFUSED, tuple(refs), (), ROUTE_TO_M46_REMEDIATION)
    body_pre = _assemble_m47_body(profile=profile, m46_plain=None, decision=decision)
    body_pre["forbidden_execution_cli_flags_seen"] = bad
    sealed = seal_m47_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m47_artifacts(sealed, output_dir)


def _emit_m47_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m47_report(sealed)))
    brief = build_m47_brief_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_brf = output_dir / BRIEF_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_brf.write_text(brief, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + brief
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_brf)


def emit_m47_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m46_upstream_fixture"
    emit_m46_fixture_ci(sub)
    m46_path = sub / "v15_bounded_evaluation_readout_decision.json"
    m46_plain = _parse_json_object(m46_path)
    decision = decide_m47_from_m46(m46_plain)
    body = _assemble_m47_body(
        profile=PROFILE_FIXTURE_CI,
        m46_plain=m46_plain,
        decision=decision,
    )
    sealed = seal_m47_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m47_artifacts(sealed, output_dir)


def emit_m47_operator_preflight(
    output_dir: Path,
    *,
    m46_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m46_plain: dict[str, Any] | None = None
    if m46_path is not None:
        rp = Path(m46_path).resolve()
        if rp.is_file():
            try:
                m46_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m46_plain = None
    decision = decide_m47_from_m46(m46_plain)
    body = _assemble_m47_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        m46_plain=m46_plain,
        decision=decision,
    )
    sealed = seal_m47_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m47_artifacts(sealed, output_dir)


def _validate_declared_overclaims(declared: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for k in M47_ALWAYS_FALSE_KEYS:
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
        if ps and ps not in ALLOWED_M46_PROMOTION:
            violations.append(f"disallowed_promotion_status:{ps}")

    return violations


def emit_m47_operator_declared(
    output_dir: Path,
    *,
    declared_surface_path: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rp = Path(declared_surface_path).resolve()
    raw = json.loads(rp.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("declared surface must be a JSON object")
    declared_in = cast(dict[str, Any], redact_paths_in_value(raw))

    cid = str(declared_in.get("contract_id") or "")
    pid = str(declared_in.get("profile_id") or "")
    contract_ok = cid == CONTRACT_ID_M47_SURFACE and pid == PROFILE_M47_REFUSAL_GATE

    over = _validate_declared_overclaims(declared_in) if contract_ok else []
    over_refs: tuple[dict[str, str], ...] = ()
    if over:
        over_refs = (
            {
                "code": REFUSED_BENCHMARK_PASS_CLAIM,
                "detail": "declared_overclaim:" + ",".join(over),
            },
        )

    m46_plain_out: dict[str, Any] | None = None
    if not contract_ok:
        refs = (
            {
                "code": REFUSED_DECLARED_SHAPE,
                "detail": f"contract_or_profile_mismatch:{cid!r}:{pid!r}",
            },
        )
        decision = M47Decision(STATUS_DESIGN_REFUSED, refs, (), ROUTE_TO_M46_REMEDIATION)
    elif over_refs:
        decision = M47Decision(
            STATUS_DESIGN_REFUSED,
            over_refs,
            (),
            ROUTE_TO_M46_REMEDIATION,
        )
    else:
        mb = declared_in.get("m46_binding")
        if not isinstance(mb, dict):
            decision = M47Decision(
                STATUS_DESIGN_REFUSED,
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m46_binding_missing_or_not_object",
                    },
                ),
                (),
                ROUTE_TO_M46_REMEDIATION,
            )
        elif not str(mb.get("artifact_sha256") or "").strip():
            decision = M47Decision(
                STATUS_DESIGN_REFUSED,
                (
                    {
                        "code": REFUSED_DECLARED_SHAPE,
                        "detail": "m46_binding_artifact_sha256_required",
                    },
                ),
                (),
                ROUTE_TO_M46_REMEDIATION,
            )
        else:
            m46_plain_out = {k: declared_in.get(k) for k in M46_BODY_BOOL_KEYS}
            decision = decide_m47_from_declared_m46_binding(mb)

    body = _assemble_m47_body(
        profile=PROFILE_OPERATOR_DECLARED,
        m46_plain=m46_plain_out,
        decision=decision,
    )
    mb_out = declared_in.get("m46_binding")
    if (
        isinstance(mb_out, dict)
        and contract_ok
        and not over_refs
        and str(mb_out.get("artifact_sha256") or "").strip()
    ):
        pr = mb_out.get("promotion_decision")
        ps: str | None = None
        if isinstance(pr, dict):
            ps = str(pr.get("promotion_status") or "") or None
        if ps is None:
            ps = str(mb_out.get("promotion_status") or "") or None
        body["m46_binding"] = {
            "contract_id": mb_out.get("contract_id"),
            "profile_id": mb_out.get("profile_id"),
            "artifact_sha256": mb_out.get("artifact_sha256"),
            "decision_status": mb_out.get("decision_status"),
            "promotion_status": ps,
            "interpretation": mb_out.get("interpretation") or INTERPRETATION_M46_BINDING,
        }
    body["declared_scorecard_surface_path_logical"] = "operator_supplied"
    sealed = seal_m47_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m47_artifacts(sealed, output_dir)


__all__ = (
    "M47Decision",
    "build_m47_brief_md",
    "build_scorecard_surface_design_block",
    "decide_m47_from_declared_m46_binding",
    "decide_m47_from_m46",
    "emit_m47_fixture_ci",
    "emit_m47_forbidden_flag_refusal",
    "emit_m47_operator_declared",
    "emit_m47_operator_preflight",
    "honesty_violation_m46_body",
    "refusal_code_from_forbidden_flags",
    "seal_m47_body",
    "structural_m46_issues_for_m47",
)
