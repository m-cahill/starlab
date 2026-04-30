"""V15-M44 — bounded evaluation execution preflight (dry-run plan; consumes sealed M43)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m43_bounded_evaluation_gate_io import (
    FILENAME_FIXTURE_ENV as M43_FILENAME_FIXTURE_ENV,
)
from starlab.v15.m43_bounded_evaluation_gate_io import (
    FILENAME_FIXTURE_PROTOCOL,
    emit_m43_fixture,
    validate_environment_manifest_routing,
    validate_scorecard_protocol_routing,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M43_DIGEST,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    PROFILE_GATE as M43_GATE_PROFILE_EXPECTED,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    ROUTE_ID_FUTURE_BOUNDED,
    ROUTE_STATUS_DECLARED_NOT_EXECUTED,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M43_GATE,
    CONTRACT_ID_M44_PREFLIGHT,
    DIGEST_FIELD,
    EMITTER_MODULE_M44,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_CHECKPOINT_LOAD,
    FORBIDDEN_FLAG_LIVE_SC2,
    INTERPRETATION_ROUTING_ONLY,
    M43_STATUS_READY,
    M43_STATUS_READY_WARNINGS,
    MILESTONE_LABEL_M44,
    NON_CLAIMS_M44,
    NOT_INTERPRETED_AS_M43,
    PLAN_ID_EXPECTED,
    PLAN_STATUS_CONSTRUCTED,
    PROFILE_FIXTURE_CI,
    PROFILE_M44_PREFLIGHT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_CANDIDATE_IDENTITY_MISSING,
    REFUSED_CHECKPOINT_LOAD,
    REFUSED_DISALLOWED_EXECUTION,
    REFUSED_DRY_RUN_PLAN_INVALID,
    REFUSED_DRY_RUN_PLAN_MISSING,
    REFUSED_ENV_MANIFEST_INVALID,
    REFUSED_ENV_MANIFEST_MISSING,
    REFUSED_INVALID_M43_GATE,
    REFUSED_LIVE_SC2,
    REFUSED_M43_GATE_NOT_READY,
    REFUSED_M43_HONESTY_VIOLATION,
    REFUSED_M43_ROUTE_NOT_DECLARED,
    REFUSED_MISSING_M43_GATE,
    REFUSED_SCORECARD_PROTOCOL_INVALID,
    REFUSED_SCORECARD_PROTOCOL_MISSING,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    STATUS_PREFLIGHT_NOT_READY,
    STATUS_PREFLIGHT_READY,
    STATUS_PREFLIGHT_READY_WARNINGS,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _m43_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(M43_DIGEST)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != M43_DIGEST}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _gate_status_str(m43: dict[str, Any]) -> str:
    return str(m43.get("gate_status") or "")


def build_m43_status_interpretation(actual_gate_status: str) -> dict[str, Any]:
    return {
        "gate_status": actual_gate_status,
        "interpretation": INTERPRETATION_ROUTING_ONLY,
        "not_interpreted_as": list(NOT_INTERPRETED_AS_M43),
    }


def structural_m43_preflight_issues(m43: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m43.get("contract_id", "")) != CONTRACT_ID_M43_GATE:
        errs.append("m43_contract_id_mismatch")
    if str(m43.get("gate_profile_id", "")) != M43_GATE_PROFILE_EXPECTED:
        errs.append("m43_gate_profile_id_mismatch")
    if not _m43_seal_ok(m43):
        errs.append("m43_seal_invalid")
    return errs


def honesty_violation_m43(m43: dict[str, Any]) -> bool:
    return bool(
        m43.get("evaluation_executed") is True
        or m43.get("checkpoint_loaded") is True
        or m43.get("promotion_decision_made") is True
    )


def route_declared_ok(m43: dict[str, Any]) -> bool:
    route = m43.get("route")
    if not isinstance(route, dict):
        return False
    return (
        str(route.get("route_id")) == ROUTE_ID_FUTURE_BOUNDED
        and str(
            route.get(
                "route_status",
            )
        )
        == ROUTE_STATUS_DECLARED_NOT_EXECUTED
    )


def candidate_final_sha_from_m43(m43: dict[str, Any]) -> str | None:
    pack = m43.get("m42_package")
    if not isinstance(pack, dict):
        return None
    fin = str(pack.get("candidate_final_sha256") or "").strip().lower()
    return fin if _is_hex64(fin) else None


def warnings_from_m43(m43: dict[str, Any]) -> list[str]:
    pack = m43.get("m42_package")
    out: list[str] = []
    if isinstance(pack, dict):
        n = pack.get("m42_noncritical_warnings")
        if isinstance(n, list):
            out.extend(str(x) for x in n)
    return sorted(set(out))


@dataclass(frozen=True)
class M44DryRunEnvelope:
    plan_id_ok: bool
    scorecard: dict[str, Any] | None


def parse_dry_run_operator_envelope(raw: dict[str, Any]) -> tuple[str | None, M44DryRunEnvelope]:
    """Return refusal code or None, plus envelope."""
    pid = str(raw.get("plan_id") or "")
    ok = pid == PLAN_ID_EXPECTED
    prot = raw.get("scorecard_protocol")
    prot_d: dict[str, Any] | None = prot if isinstance(prot, dict) else None
    if prot is not None and prot_d is None:
        return REFUSED_DRY_RUN_PLAN_INVALID, M44DryRunEnvelope(False, None)
    return None, M44DryRunEnvelope(ok, prot_d)


def build_preflight_dry_run_plan_core(
    *,
    m43: dict[str, Any],
    source_gate_status: str,
    candidate_sha: str | None,
) -> dict[str, Any]:
    route = m43.get("route")
    rid = ROUTE_ID_FUTURE_BOUNDED
    if isinstance(route, dict) and route.get("route_id"):
        rid = str(route.get("route_id"))
    disallowed_now = (
        route.get("disallowed_now")
        if isinstance(route, dict) and isinstance(route.get("disallowed_now"), list)
        else []
    )
    dis_list = (
        [str(x) for x in disallowed_now]
        if disallowed_now
        else [
            "benchmark_execution",
            "scorecard_results",
            "torch_load",
            "checkpoint_blob_load",
            "live_sc2",
            "checkpoint_promotion",
        ]
    )
    cand = candidate_sha or "0000000000000000000000000000000000000000000000000000000000000000"
    return {
        "plan_id": PLAN_ID_EXPECTED,
        "plan_status": PLAN_STATUS_CONSTRUCTED,
        "source_gate_status": source_gate_status,
        "candidate_checkpoint_sha256": cand,
        "evaluation_route_id": rid,
        "planned_execution_profile": "future_operator_local_bounded_eval",
        "planned_ladder_stage": "future_bounded_candidate_evaluation",
        "planned_scorecard_mode": "metadata_only_not_results",
        "environment_prerequisite_status": "metadata_validated_not_executed",
        "protocol_prerequisite_status": "metadata_validated_not_results",
        "planned_artifact_filenames": [
            "future_bounded_evaluation_execution.json",
            "future_bounded_evaluation_execution_report.json",
        ],
        "prerequisite_bindings": {
            "environment_manifest": {
                "binding_status": "bound_metadata_only",
                "semantic_scope": "routing_precondition_not_execution",
            },
            "scorecard_protocol": {
                "binding_status": "bound_metadata_only",
                "semantic_scope": "protocol_precondition_not_results",
            },
        },
        "disallowed_now": sorted(dis_list),
    }


@dataclass(frozen=True)
class M44Decision:
    preflight_status: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    dry_run_plan: dict[str, Any] | None


def decide_m44(
    *,
    profile: str,
    m43: dict[str, Any] | None,
    dry_run_envelope: M44DryRunEnvelope | None,
    env_plain: dict[str, Any] | None,
    dry_run_path_present: bool,
    env_path_present: bool,
) -> M44Decision:
    refusals_list: list[dict[str, str]] = []

    def _ref(code: str, detail: str) -> None:
        refusals_list.append({"code": code, "detail": detail})

    if m43 is None:
        _ref(REFUSED_MISSING_M43_GATE, "m43_gate_json_missing_or_unreadable")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    struct = structural_m43_preflight_issues(m43)
    if struct:
        _ref(REFUSED_INVALID_M43_GATE, ",".join(struct))
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    if honesty_violation_m43(m43):
        _ref(REFUSED_M43_HONESTY_VIOLATION, "m43_honesty_flags_must_remain_false")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    gs = _gate_status_str(m43)

    def _eligible_clean() -> bool:
        return gs == M43_STATUS_READY

    def _eligible_warn() -> bool:
        return gs == M43_STATUS_READY_WARNINGS

    if not (_eligible_clean() or _eligible_warn()):
        if gs.startswith("refused_"):
            _ref(REFUSED_M43_GATE_NOT_READY, f"m43_upstream_refusal:{gs}")
        elif gs == "bounded_evaluation_gate_not_ready":
            _ref(REFUSED_M43_GATE_NOT_READY, gs)
        else:
            _ref(REFUSED_M43_GATE_NOT_READY, f"m43_gate_status_not_eligible:{gs}")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    if profile in (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT) and not _eligible_clean():
        _ref(REFUSED_M43_GATE_NOT_READY, f"m44_strict_profiles_require_clean_ready:{gs}")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    if profile == PROFILE_OPERATOR_DECLARED and _eligible_warn() and not warnings_from_m43(m43):
        _ref(REFUSED_M43_GATE_NOT_READY, "m43_warnings_status_without_carrier")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    if not route_declared_ok(m43):
        _ref(REFUSED_M43_ROUTE_NOT_DECLARED, "m43_future_route_not_declared_not_executed")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    cand = candidate_final_sha_from_m43(m43)
    if cand is None:
        _ref(REFUSED_CANDIDATE_IDENTITY_MISSING, "m42_candidate_final_sha256_missing")
        return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    # Profiles: prerequisite inputs
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        if not dry_run_path_present:
            _ref(REFUSED_DRY_RUN_PLAN_MISSING, "dry_run_plan_json_required")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if dry_run_envelope is None:
            _ref(REFUSED_DRY_RUN_PLAN_INVALID, "dry_run_plan_unparsed")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if not dry_run_envelope.plan_id_ok:
            _ref(REFUSED_DRY_RUN_PLAN_INVALID, "plan_id_mismatch")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if dry_run_envelope.scorecard is None:
            _ref(REFUSED_SCORECARD_PROTOCOL_MISSING, "scorecard_protocol_required_in_plan_json")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        p_reason = validate_scorecard_protocol_routing(dry_run_envelope.scorecard)
        if p_reason:
            _ref(
                REFUSED_SCORECARD_PROTOCOL_INVALID,
                f"protocol_validation:{p_reason}",
            )
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if not env_path_present:
            _ref(REFUSED_ENV_MANIFEST_MISSING, "evaluation_environment_json_required")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if env_plain is None:
            _ref(REFUSED_ENV_MANIFEST_MISSING, "environment_manifest_unreadable")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        e_reason = validate_environment_manifest_routing(env_plain)
        if e_reason:
            code = REFUSED_ENV_MANIFEST_INVALID
            _ref(code, f"environment_validation:{e_reason}")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    elif profile == PROFILE_OPERATOR_DECLARED:
        if not dry_run_path_present:
            _ref(REFUSED_DRY_RUN_PLAN_MISSING, "dry_run_plan_json_missing_operator_declared")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if dry_run_envelope is None:
            _ref(REFUSED_DRY_RUN_PLAN_INVALID, "dry_run_plan_unparsed")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if not dry_run_envelope.plan_id_ok:
            _ref(REFUSED_DRY_RUN_PLAN_INVALID, "plan_id_mismatch")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        sc = dry_run_envelope.scorecard
        if sc is None:
            _ref(
                REFUSED_SCORECARD_PROTOCOL_MISSING,
                "scorecard_protocol_missing_in_plan_json_declared_profile",
            )
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        pr_decl = validate_scorecard_protocol_routing(sc)
        if pr_decl:
            _ref(
                REFUSED_SCORECARD_PROTOCOL_INVALID,
                str(pr_decl),
            )
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

        if not env_path_present:
            _ref(REFUSED_ENV_MANIFEST_MISSING, "evaluation_environment_manifest_missing")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        if env_plain is None:
            _ref(REFUSED_ENV_MANIFEST_MISSING, "environment_manifest_unreadable")
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)
        erd = validate_environment_manifest_routing(env_plain)
        if erd:
            _ref(REFUSED_ENV_MANIFEST_INVALID, str(erd))
            return M44Decision(STATUS_PREFLIGHT_NOT_READY, tuple(refusals_list), (), None)

    warnings_t: tuple[str, ...] = ()
    if profile == PROFILE_OPERATOR_DECLARED and _eligible_warn():
        warnings_t = tuple(warnings_from_m43(m43))

    prem_status = STATUS_PREFLIGHT_READY
    if _eligible_warn():
        prem_status = STATUS_PREFLIGHT_READY_WARNINGS

    plan_body = build_preflight_dry_run_plan_core(
        m43=m43, source_gate_status=gs, candidate_sha=cand
    )
    return M44Decision(prem_status, tuple(refusals_list), warnings_t, plan_body)


PLAN_STATUS_REFUSED_STUB: Final[str] = "not_constructed_refused"


def seal_m44_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m44_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_evaluation_execution_preflight_report",
        "report_version": "m44",
        "milestone": MILESTONE_LABEL_M44,
        "contract_id": CONTRACT_ID_M44_PREFLIGHT,
        "preflight_profile_id": PROFILE_M44_PREFLIGHT,
        DIGEST_FIELD: digest,
        "preflight_status": sealed.get("preflight_status"),
        "m43_gate_status_summarized": (sealed.get("m43_binding") or {}).get("gate_status"),
        "dry_run_plan_status": (sealed.get("dry_run_plan") or {}).get("plan_status"),
    }


def _dry_run_stub_failed() -> dict[str, Any]:
    return {"plan_status": PLAN_STATUS_REFUSED_STUB}


def _honesty_block() -> dict[str, Any]:
    return {
        "benchmark_execution_performed": False,
        "evaluation_execution_performed": False,
        "scorecard_results_produced": False,
        "strength_evaluated": False,
        "checkpoint_loaded": False,
        "checkpoint_promoted": False,
        "torch_load_invoked": False,
        "live_sc2_executed": False,
    }


def _m43_honesty_posture() -> dict[str, Any]:
    return {
        "m43_evaluation_executed": False,
        "m43_checkpoint_loaded": False,
        "m43_promotion_decision_made": False,
    }


def build_m44_checklist_md(*, sealed: dict[str, Any]) -> str:
    interp = sealed.get("m43_status_interpretation") or {}
    plan = sealed.get("dry_run_plan") or {}
    warns = sealed.get("warnings") or []
    refs = sealed.get("refusals") or []
    binds = sealed.get("prerequisite_binding_summary") or {}
    gs_m43_binding = str((sealed.get("m43_binding") or {}).get("gate_status", "") or "")
    ni_list = interp.get("not_interpreted_as", []) or []
    not_interp_s = ", ".join(str(x) for x in ni_list)
    lines = [
        "# V15-M44 bounded evaluation execution preflight checklist",
        "",
        "## M43 gate status (upstream)",
        f"- `m43_binding.gate_status`: `{gs_m43_binding}`",
        "",
        "## M43 status interpretation",
        "- M44 treats M43 bounded_evaluation_gate_ready as routing eligibility only. It is "
        "not benchmark success, evaluation execution, strength evaluation, scorecard "
        "production, or checkpoint promotion.",
        f"- `interpretation`: `{interp.get('interpretation', '')}`",
        f"- `not_interpreted_as`: {not_interp_s}",
        "",
        "## Dry-run plan status",
        f"- `{plan.get('plan_status')}`",
        "",
        "## Prerequisite binding summary",
        "```json",
        canonical_json_dumps(binds if isinstance(binds, dict) else {}),
        "```",
        "",
        "## Preflight honesty flags (must remain false on this milestone)",
        "```json",
        canonical_json_dumps(
            {k: sealed.get(k) for k in _honesty_block() if k in sealed}
            | {k: v for k, v in _honesty_block().items() if k not in sealed},
        ),
        "```",
        "",
        "## M43 honesty posture carried forward",
        "```json",
        canonical_json_dumps(_m43_honesty_posture()),
        "```",
        "",
        "## Warning rows",
    ]
    if warns:
        for w in warns:
            lines.append(f"- {w}")
    else:
        lines.append("- (none)")
    lines.extend(["", "## Refusal rows"])
    if refs:
        for r in refs:
            if isinstance(r, dict):
                lines.append(f"- `{r.get('code')}` — {r.get('detail', '')}")
    else:
        lines.append("- (none)")
    lines.extend(
        [
            "",
            "## Non-claims",
        ],
    )
    ncl = sealed.get("non_claims") or []
    if isinstance(ncl, list):
        lines.extend([f"- `{x}`" for x in ncl])
    lines.extend(
        [
            "",
            "## Next milestone warning",
            "",
            "- Future bounded evaluation **execution** (matches, blobs, ladders, promotions) "
            "requires a **separately chartered** milestone. M44 is **dry-run / preflight only**.",
            "",
            "---",
            "",
            "**This checklist is a generated preflight summary. "
            "It is not benchmark execution evidence.**",
        ],
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M44 emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    if FORBIDDEN_FLAG_CHECKPOINT_LOAD in fs:
        return REFUSED_CHECKPOINT_LOAD
    if FORBIDDEN_FLAG_LIVE_SC2 in fs:
        return REFUSED_LIVE_SC2
    return REFUSED_DISALLOWED_EXECUTION


def emit_m44_disallowed_execution(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
    refusal_code_override: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_override or refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    interp = build_m43_status_interpretation("unknown_upstream_gate")
    honesty = _honesty_block()
    mh = _m43_honesty_posture()
    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M44_PREFLIGHT,
        "preflight_profile_id": PROFILE_M44_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M44,
        "emitter_module": EMITTER_MODULE_M44,
        "profile": profile,
        **honesty,
        **mh,
        "preflight_status": primary,
        "m43_binding": {
            "contract_id": CONTRACT_ID_M43_GATE,
            "artifact_sha256": None,
            "gate_status": None,
            "evaluation_executed": False,
            "checkpoint_loaded": False,
            "promotion_decision_made": False,
        },
        "disallowed_execution_cli_flags_seen": bad,
        "m43_status_interpretation": interp,
        "dry_run_plan": _dry_run_stub_failed(),
        "warnings": [],
        "refusals": [
            {"code": primary, "detail": "forbidden_cli_flags:" + ",".join(bad)},
        ],
        "prerequisite_binding_summary": {},
        "non_claims": list(NON_CLAIMS_M44),
    }
    sealed = seal_m44_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m44_artifacts(sealed, output_dir)


def _emit_m44_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m44_report(sealed)))
    chk = build_m44_checklist_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_chk)


def _binding_summary_from_plan(plan: dict[str, Any]) -> dict[str, Any]:
    pb = plan.get("prerequisite_bindings")
    return pb if isinstance(pb, dict) else {}


def _assemble_preflight_body(
    *,
    profile: str,
    m43_plain: dict[str, Any] | None,
    decision: M44Decision,
    preflight_when_not_ready: str,
    operator_dry_plan_shas: dict[str, str],
    m43_gate_path_logical: Any,
) -> dict[str, Any]:
    gs_m43 = _gate_status_str(m43_plain) if m43_plain else ""
    digest43 = str(m43_plain.get(M43_DIGEST) or "").lower() if m43_plain else ""

    interp = build_m43_status_interpretation(gs_m43 if gs_m43 else "missing_upstream_m43_gate")
    honesty = _honesty_block()
    mh = _m43_honesty_posture()
    bind43 = {
        "contract_id": CONTRACT_ID_M43_GATE,
        "artifact_sha256": digest43 if digest43 else None,
        "gate_status": gs_m43 if gs_m43 else None,
        "evaluation_executed": (m43_plain.get("evaluation_executed") is True)
        if m43_plain
        else False,
        "checkpoint_loaded": (m43_plain.get("checkpoint_loaded") is True) if m43_plain else False,
        "promotion_decision_made": (m43_plain.get("promotion_decision_made") is True)
        if m43_plain
        else False,
    }
    prem = decision.preflight_status if not decision.refusals else preflight_when_not_ready
    plan_out: dict[str, Any]
    if decision.dry_run_plan is not None:
        plan_out = dict(decision.dry_run_plan)
    else:
        plan_out = _dry_run_stub_failed()

    refs = [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals]
    warns = list(decision.warnings)
    prereq_summary = (
        _binding_summary_from_plan(plan_out)
        if decision.dry_run_plan is not None
        else {"environment_manifest": {}, "scorecard_protocol": {}}
    )
    if operator_dry_plan_shas:
        prereq_summary = {
            **prereq_summary,
            "routing_metadata_sha256_only": dict(operator_dry_plan_shas),
        }

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M44_PREFLIGHT,
        "preflight_profile_id": PROFILE_M44_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M44,
        "emitter_module": EMITTER_MODULE_M44,
        "profile": profile,
        **honesty,
        **mh,
        "preflight_status": prem,
        "m43_binding": bind43,
        "m43_status_interpretation": interp,
        "dry_run_plan": plan_out,
        "warnings": warns,
        "refusals": refs,
        "prerequisite_binding_summary": prereq_summary,
        "non_claims": list(NON_CLAIMS_M44),
        "m43_gate_path_logical": cast(
            dict[str, Any] | str, redact_paths_in_value(m43_gate_path_logical)
        ),
    }
    return body


def emit_m44_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    upstream = output_dir / "m43_upstream_fixture"
    emit_m43_fixture(upstream)
    gate_path = upstream / "v15_bounded_evaluation_gate.json"
    m43_plain = _parse_json_object(gate_path)
    env_path_f = upstream / M43_FILENAME_FIXTURE_ENV
    proto_path_f = upstream / FILENAME_FIXTURE_PROTOCOL
    env_plain = _parse_json_object(env_path_f)
    proto_plain = _parse_json_object(proto_path_f)
    dry_blob = {"plan_id": PLAN_ID_EXPECTED, "scorecard_protocol": proto_plain}
    err, env_d = parse_dry_run_operator_envelope(dry_blob)
    assert err is None and env_d is not None
    decision = decide_m44(
        profile=PROFILE_FIXTURE_CI,
        m43=m43_plain,
        dry_run_envelope=env_d,
        env_plain=env_plain,
        dry_run_path_present=True,
        env_path_present=True,
    )
    body = _assemble_preflight_body(
        profile=PROFILE_FIXTURE_CI,
        m43_plain=m43_plain,
        decision=decision,
        preflight_when_not_ready=STATUS_PREFLIGHT_NOT_READY,
        operator_dry_plan_shas={
            "dry_run_plan_envelope_digest": sha256_hex_of_canonical_json(dry_blob),
            "evaluation_environment_manifest_artifact_digest": sha256_hex_of_canonical_json(
                env_plain
            ),
        },
        m43_gate_path_logical="redacted:m43_fixture_upstream",
    )
    sealed = seal_m44_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m44_artifacts(sealed, output_dir)


def emit_m44_operator(
    output_dir: Path,
    *,
    profile: str,
    m43_gate_path: Path | None,
    dry_run_plan_path: Path | None,
    evaluation_environment_path: Path | None,
    operator_logical_hint: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)

    m43_plain: dict[str, Any] | None = None
    logical_m43_path: str | Path = operator_logical_hint or "unknown_m43_gate_path"
    if m43_gate_path is not None:
        rp = Path(m43_gate_path).resolve()
        logical_m43_path = operator_logical_hint or (
            str(rp) if rp.is_file() else str(m43_gate_path)
        )
        if rp.is_file():
            try:
                m43_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m43_plain = None

    dry_provided = dry_run_plan_path is not None
    env_provided = evaluation_environment_path is not None

    extra_refusals: list[dict[str, str]] = []
    meta_shas: dict[str, str] = {}
    envelope: M44DryRunEnvelope | None = None
    env_plain: dict[str, Any] | None = None

    if dry_provided and dry_run_plan_path is not None:
        dp = Path(dry_run_plan_path).resolve()
        if not dp.is_file():
            extra_refusals.append(
                {"code": REFUSED_DRY_RUN_PLAN_MISSING, "detail": "dry_run_plan_path_not_found"},
            )
        else:
            try:
                dre = _parse_json_object(dp)
                meta_shas["dry_run_plan_json_digest"] = sha256_hex_of_canonical_json(dre)
                err_d, envol = parse_dry_run_operator_envelope(dre)
                if err_d:
                    extra_refusals.append(
                        {"code": err_d, "detail": "dry_run_envelope_shape_invalid"},
                    )
                else:
                    envelope = envol
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError) as e:
                extra_refusals.append(
                    {"code": REFUSED_DRY_RUN_PLAN_INVALID, "detail": f"dry_run_json_invalid:{e}"},
                )
    if env_provided and evaluation_environment_path is not None:
        ep = Path(evaluation_environment_path).resolve()
        if not ep.is_file():
            extra_refusals.append(
                {
                    "code": REFUSED_ENV_MANIFEST_MISSING,
                    "detail": "evaluation_environment_path_not_found",
                },
            )
        else:
            try:
                env_plain = _parse_json_object(ep)
                meta_shas["evaluation_environment_json_digest"] = sha256_hex_of_canonical_json(
                    env_plain,
                )
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError) as e:
                extra_refusals.append(
                    {
                        "code": REFUSED_ENV_MANIFEST_INVALID,
                        "detail": f"environment_json_invalid:{e}",
                    },
                )
                env_plain = None

    decision = decide_m44(
        profile=profile,
        m43=m43_plain,
        dry_run_envelope=envelope,
        env_plain=env_plain,
        dry_run_path_present=dry_provided,
        env_path_present=env_provided,
    )

    merged_refs_list = [*extra_refusals, *[dict(r) for r in decision.refusals]]
    warn_t = tuple(decision.warnings)

    if merged_refs_list:
        final_pref = STATUS_PREFLIGHT_NOT_READY
        final_plan: dict[str, Any] | None = None
    else:
        final_pref = decision.preflight_status
        final_plan = decision.dry_run_plan

    merged = M44Decision(final_pref, tuple(merged_refs_list), warn_t, final_plan)

    body = _assemble_preflight_body(
        profile=profile,
        m43_plain=m43_plain,
        decision=merged,
        preflight_when_not_ready=STATUS_PREFLIGHT_NOT_READY,
        operator_dry_plan_shas=meta_shas,
        m43_gate_path_logical=logical_m43_path,
    )
    sealed = seal_m44_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m44_artifacts(sealed, output_dir)


__all__ = (
    "M44Decision",
    "M44DryRunEnvelope",
    "build_m43_status_interpretation",
    "build_m44_checklist_md",
    "build_preflight_dry_run_plan_core",
    "decide_m44",
    "emit_m44_disallowed_execution",
    "emit_m44_fixture_ci",
    "emit_m44_operator",
    "parse_dry_run_operator_envelope",
    "refusal_code_from_forbidden_flags",
    "seal_m44_body",
)
