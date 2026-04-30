"""V15-M45 — bounded candidate evaluation execution surface (consumes sealed M44 preflight)."""

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
from starlab.v15.m44_bounded_evaluation_execution_preflight_io import (
    emit_m44_fixture_ci as emit_m44_fixture,
)
from starlab.v15.m44_bounded_evaluation_execution_preflight_models import (
    DIGEST_FIELD as M44_DIGEST_FIELD,
)
from starlab.v15.m45_bounded_candidate_evaluation_execution_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M44_PREFLIGHT,
    CONTRACT_ID_M45_EXECUTION,
    DIGEST_FIELD,
    EMITTER_MODULE_M45,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_TO_REFUSAL,
    INTERPRETATION_PREFLIGHT_BOOKKEEPING_ONLY,
    M44_DRY_RUN_PLAN_STATUS_EXPECTED,
    M44_STATUS_PREFLIGHT_READY,
    M44_STATUS_PREFLIGHT_READY_WARNINGS,
    MILESTONE_LABEL_M45,
    NON_CLAIMS_M45,
    NOT_INTERPRETED_AS_M44,
    PROFILE_FIXTURE_CI,
    PROFILE_M44_PREFLIGHT,
    PROFILE_M45_EXECUTION,
    PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_DISALLOWED_BENCHMARK_REQUEST,
    REFUSED_INVALID_M44_PREFLIGHT,
    REFUSED_M44_DRY_RUN_PLAN_NOT_CONSTRUCTED,
    REFUSED_M44_HONESTY_FLAGS_VIOLATION,
    REFUSED_M44_PREFLIGHT_NOT_READY,
    REFUSED_MISSING_M44_PREFLIGHT,
    REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    STATUS_EXECUTION_COMPLETED_SYNTHETIC,
    STATUS_EXECUTION_NOT_READY,
    STATUS_EXECUTION_SURFACE_READY,
    SYNTHETIC_EXECUTION_INTERPRETATION,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _m44_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(M44_DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != M44_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _preflight_status_str(m44: dict[str, Any]) -> str:
    return str(m44.get("preflight_status") or "")


def build_m44_interpretation(actual_preflight_status: str) -> dict[str, Any]:
    return {
        "preflight_status": actual_preflight_status,
        "interpretation": INTERPRETATION_PREFLIGHT_BOOKKEEPING_ONLY,
        "not_interpreted_as": list(NOT_INTERPRETED_AS_M44),
    }


def structural_m44_validation_issues(m44: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m44.get("contract_id", "")) != CONTRACT_ID_M44_PREFLIGHT:
        errs.append("m44_contract_id_mismatch")
    if str(m44.get("preflight_profile_id", "")) != PROFILE_M44_PREFLIGHT:
        errs.append("m44_preflight_profile_id_mismatch")
    if not _m44_seal_ok(m44):
        errs.append("m44_seal_invalid")
    return errs


def honesty_violation_m44(m44: dict[str, Any]) -> bool:
    return bool(
        m44.get("benchmark_execution_performed") is True
        or m44.get("evaluation_execution_performed") is True
        or m44.get("scorecard_results_produced") is True
        or m44.get("strength_evaluated") is True
        or m44.get("checkpoint_loaded") is True
        or m44.get("checkpoint_promoted") is True
        or m44.get("torch_load_invoked") is True
        or m44.get("live_sc2_executed") is True
    )


def dry_run_plan_constructed(m44: dict[str, Any]) -> bool:
    plan = m44.get("dry_run_plan")
    if not isinstance(plan, dict):
        return False
    return str(plan.get("plan_status", "")) == M44_DRY_RUN_PLAN_STATUS_EXPECTED


def candidate_sha_from_m44(m44: dict[str, Any]) -> str | None:
    plan = m44.get("dry_run_plan")
    if not isinstance(plan, dict):
        return None
    sha = str(plan.get("candidate_checkpoint_sha256") or "").strip().lower()
    return sha if _is_hex64(sha) else None


def warnings_from_m44(m44: dict[str, Any]) -> list[str]:
    w = m44.get("warnings")
    if isinstance(w, list):
        return sorted(set(str(x) for x in w))
    return []


@dataclass(frozen=True)
class M45Decision:
    execution_status: str
    refusals: tuple[dict[str, str], ...]
    warnings: tuple[str, ...]
    execution_receipt: dict[str, Any] | None
    bounded_execution_surface_invoked: bool
    synthetic_execution_receipt_emitted: bool


def decide_m45(
    *,
    profile: str,
    m44: dict[str, Any] | None,
    allow_operator_local_execution: bool,
    authorize_bounded_evaluation_execution: bool,
) -> M45Decision:
    refusals_list: list[dict[str, str]] = []

    def _ref(code: str, detail: str) -> None:
        refusals_list.append({"code": code, "detail": detail})

    if m44 is None:
        _ref(REFUSED_MISSING_M44_PREFLIGHT, "m44_preflight_json_missing_or_unreadable")
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    struct = structural_m44_validation_issues(m44)
    if struct:
        _ref(REFUSED_INVALID_M44_PREFLIGHT, ",".join(struct))
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    if honesty_violation_m44(m44):
        _ref(REFUSED_M44_HONESTY_FLAGS_VIOLATION, "m44_honesty_flags_must_remain_false")
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    ps = _preflight_status_str(m44)

    def _eligible_clean() -> bool:
        return ps == M44_STATUS_PREFLIGHT_READY

    def _eligible_warn() -> bool:
        return ps == M44_STATUS_PREFLIGHT_READY_WARNINGS

    if not (_eligible_clean() or _eligible_warn()):
        if ps.startswith("refused_"):
            _ref(REFUSED_M44_PREFLIGHT_NOT_READY, f"m44_upstream_refusal:{ps}")
        elif ps == "bounded_evaluation_execution_preflight_not_ready":
            _ref(REFUSED_M44_PREFLIGHT_NOT_READY, ps)
        else:
            _ref(REFUSED_M44_PREFLIGHT_NOT_READY, f"m44_preflight_status_not_eligible:{ps}")
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    if profile in (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT) and not _eligible_clean():
        _ref(
            REFUSED_M44_PREFLIGHT_NOT_READY,
            f"m45_strict_profiles_require_clean_preflight_ready:{ps}",
        )
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    if (
        profile == PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION
        and _eligible_warn()
        and not warnings_from_m44(m44)
    ):
        _ref(REFUSED_M44_PREFLIGHT_NOT_READY, "m44_warnings_status_without_carrier")
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    if not dry_run_plan_constructed(m44):
        _ref(REFUSED_M44_DRY_RUN_PLAN_NOT_CONSTRUCTED, "m44_dry_run_plan_not_constructed")
        return M45Decision(STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False)

    if profile == PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION:
        if not (allow_operator_local_execution and authorize_bounded_evaluation_execution):
            _ref(
                REFUSED_OPERATOR_LOCAL_NOT_AUTHORIZED,
                "operator_local_bounded_execution_requires_both_guard_flags",
            )
            return M45Decision(
                STATUS_EXECUTION_NOT_READY, tuple(refusals_list), (), None, False, False
            )

    warnings_t: tuple[str, ...] = ()
    if profile == PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION and _eligible_warn():
        warnings_t = tuple(warnings_from_m44(m44))

    cand_sha = candidate_sha_from_m44(m44)

    if profile == PROFILE_OPERATOR_LOCAL_BOUNDED_EXECUTION:
        receipt = _build_execution_receipt_synthetic(cand_sha)
        final_status = STATUS_EXECUTION_COMPLETED_SYNTHETIC
        invoked = True
        emitted = True
    else:
        receipt = _build_execution_receipt_not_executed(cand_sha)
        final_status = STATUS_EXECUTION_SURFACE_READY
        invoked = False
        emitted = False

    return M45Decision(final_status, tuple(refusals_list), warnings_t, receipt, invoked, emitted)


def _build_execution_receipt_not_executed(cand_sha: str | None) -> dict[str, Any]:
    return {
        "receipt_status": "not_executed_or_synthetic_only",
        "execution_mode": "fixture_or_preflight_metadata_only",
        "scorecard_mode": "none",
        "benchmark_mode": "none",
        "checkpoint_mode": "metadata_only_no_blob_load",
        "sc2_mode": "not_run",
        "candidate_checkpoint_sha256": cand_sha or "unknown",
    }


def _build_execution_receipt_synthetic(cand_sha: str | None) -> dict[str, Any]:
    return {
        "receipt_status": "synthetic_execution_receipt_emitted",
        "execution_mode": "operator_local_synthetic_bounded",
        "scorecard_mode": "none",
        "benchmark_mode": "none",
        "checkpoint_mode": "metadata_only_no_blob_load",
        "sc2_mode": "not_run",
        "candidate_checkpoint_sha256": cand_sha or "unknown",
        "interpretation": SYNTHETIC_EXECUTION_INTERPRETATION,
    }


def seal_m45_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m45_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_candidate_evaluation_execution_report",
        "report_version": "m45",
        "milestone": MILESTONE_LABEL_M45,
        "contract_id": CONTRACT_ID_M45_EXECUTION,
        "profile_id": PROFILE_M45_EXECUTION,
        DIGEST_FIELD: digest,
        "execution_status": sealed.get("execution_status"),
        "m44_preflight_status_summarized": (sealed.get("m44_binding") or {}).get(
            "preflight_status"
        ),
        "execution_receipt_status": (sealed.get("execution_receipt") or {}).get("receipt_status"),
        "bounded_execution_surface_invoked": sealed.get("bounded_execution_surface_invoked"),
        "synthetic_execution_receipt_emitted": sealed.get("synthetic_execution_receipt_emitted"),
    }


def _honesty_block() -> dict[str, Any]:
    return {
        "benchmark_passed": False,
        "benchmark_pass_fail_emitted": False,
        "scorecard_results_produced": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "torch_load_invoked": False,
        "checkpoint_blob_loaded": False,
        "live_sc2_executed": False,
        "xai_executed": False,
        "human_panel_executed": False,
        "showcase_released": False,
        "v2_authorized": False,
        "t2_t3_t4_t5_executed": False,
    }


def _m44_honesty_posture() -> dict[str, Any]:
    return {
        "m44_benchmark_execution_performed": False,
        "m44_evaluation_execution_performed": False,
        "m44_scorecard_results_produced": False,
        "m44_strength_evaluated": False,
        "m44_checkpoint_loaded": False,
        "m44_checkpoint_promoted": False,
        "m44_torch_load_invoked": False,
        "m44_live_sc2_executed": False,
    }


def build_m45_checklist_md(*, sealed: dict[str, Any]) -> str:
    interp = sealed.get("m44_preflight_interpretation") or {}
    receipt = sealed.get("execution_receipt") or {}
    warns = sealed.get("warnings") or []
    refs = sealed.get("refusals") or []
    m44_bind = sealed.get("m44_binding") or {}
    ps_m44 = str(m44_bind.get("preflight_status", "") or "")
    drp_status = str(m44_bind.get("dry_run_plan_status", "") or "")
    ni_list = interp.get("not_interpreted_as", []) or []
    not_interp_s = ", ".join(str(x) for x in ni_list)
    honesty = {k: sealed.get(k) for k in _honesty_block() if k in sealed}
    honesty.update({k: v for k, v in _honesty_block().items() if k not in sealed})
    lines = [
        "# V15-M45 bounded candidate evaluation execution checklist",
        "",
        "## M44 binding status (upstream)",
        f"- `m44_binding.preflight_status`: `{ps_m44}`",
        f"- `m44_binding.dry_run_plan_status`: `{drp_status}`",
        "",
        "## M44 preflight interpretation",
        "- M45 treats M44 `bounded_evaluation_execution_preflight_ready` as future preflight "
        "bookkeeping only. It is not benchmark success, benchmark pass/fail, evaluation "
        "execution, strength evaluation, scorecard results, or checkpoint promotion.",
        f"- `interpretation`: `{interp.get('interpretation', '')}`",
        f"- `not_interpreted_as`: {not_interp_s}",
        "",
        "## Execution receipt status",
        f"- `receipt_status`: `{receipt.get('receipt_status', '')}`",
        f"- `execution_mode`: `{receipt.get('execution_mode', '')}`",
        f"- `scorecard_mode`: `{receipt.get('scorecard_mode', '')}`",
        f"- `benchmark_mode`: `{receipt.get('benchmark_mode', '')}`",
        f"- `checkpoint_mode`: `{receipt.get('checkpoint_mode', '')}`",
        f"- `sc2_mode`: `{receipt.get('sc2_mode', '')}`",
        "",
        "## Always-false honesty flags (must remain false)",
        "```json",
        canonical_json_dumps(honesty),
        "```",
        "",
        "## M44 honesty posture carried forward",
        "```json",
        canonical_json_dumps(_m44_honesty_posture()),
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
            "- Future benchmark pass/fail, scorecard results, strength evaluation, checkpoint "
            "promotion, XAI review, human-panel evaluation, showcase release, v2 authorization, "
            "and T2–T5 ladder execution require **separately chartered** milestones.",
            "- M45 is **bounded execution/refusal bookkeeping** only.",
            "",
            "---",
            "",
            "This checklist is bounded execution/refusal bookkeeping. It is not benchmark "
            "pass/fail evidence, scorecard results, strength evaluation, or checkpoint promotion.",
            "",
            "No live SC2, checkpoint blob loading, torch.load, XAI, human-panel, showcase, v2, "
            "or T2–T5 execution is claimed by this artifact.",
        ],
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M45 emission leaked path patterns into public artifacts")


def refusal_code_from_forbidden_flags(flags: list[str]) -> str:
    fs = sorted(set(flags))
    for f in fs:
        if f in FORBIDDEN_FLAG_TO_REFUSAL:
            return FORBIDDEN_FLAG_TO_REFUSAL[f]
    return REFUSED_DISALLOWED_BENCHMARK_REQUEST


def emit_m45_forbidden_flag_refusal(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
    refusal_code_override: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    primary = refusal_code_override or refusal_code_from_forbidden_flags(triggered_flags)
    bad = sorted(set(triggered_flags))
    interp = build_m44_interpretation("unknown_upstream_preflight")
    honesty = _honesty_block()
    mh = _m44_honesty_posture()
    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M45_EXECUTION,
        "profile_id": PROFILE_M45_EXECUTION,
        "milestone": MILESTONE_LABEL_M45,
        "emitter_module": EMITTER_MODULE_M45,
        "profile": profile,
        **honesty,
        **mh,
        "execution_status": primary,
        "m44_binding": {
            "contract_id": CONTRACT_ID_M44_PREFLIGHT,
            "artifact_sha256": None,
            "preflight_status": None,
            "dry_run_plan_status": None,
        },
        "forbidden_execution_cli_flags_seen": bad,
        "m44_preflight_interpretation": interp,
        "execution_receipt": {
            "receipt_status": "not_executed_forbidden_flag_refusal",
            "execution_mode": "none",
            "scorecard_mode": "none",
            "benchmark_mode": "none",
            "checkpoint_mode": "none",
            "sc2_mode": "not_run",
        },
        "bounded_execution_surface_invoked": False,
        "synthetic_execution_receipt_emitted": False,
        "warnings": [],
        "refusals": [
            {"code": primary, "detail": "forbidden_cli_flags:" + ",".join(bad)},
        ],
        "non_claims": list(NON_CLAIMS_M45),
    }
    sealed = seal_m45_body(cast(dict[str, Any], redact_paths_in_value(body_pre)))
    return _emit_m45_artifacts(sealed, output_dir)


def _emit_m45_artifacts(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rep = cast(dict[str, Any], redact_paths_in_value(build_m45_report(sealed)))
    chk = build_m45_checklist_md(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_chk)


def _assemble_execution_body(
    *,
    profile: str,
    m44_plain: dict[str, Any] | None,
    decision: M45Decision,
    m44_path_logical: Any,
) -> dict[str, Any]:
    ps_m44 = _preflight_status_str(m44_plain) if m44_plain else ""
    digest44 = str(m44_plain.get(M44_DIGEST_FIELD) or "").lower() if m44_plain else ""
    drp = m44_plain.get("dry_run_plan") if m44_plain else None
    drp_status = str(drp.get("plan_status", "")) if isinstance(drp, dict) else ""

    interp = build_m44_interpretation(ps_m44 if ps_m44 else "missing_upstream_m44_preflight")
    honesty = _honesty_block()
    mh = _m44_honesty_posture()
    bind44 = {
        "contract_id": CONTRACT_ID_M44_PREFLIGHT,
        "artifact_sha256": digest44 if digest44 else None,
        "preflight_status": ps_m44 if ps_m44 else None,
        "dry_run_plan_status": drp_status if drp_status else None,
        "interpretation": INTERPRETATION_PREFLIGHT_BOOKKEEPING_ONLY,
    }
    refs = [{"code": r["code"], "detail": r["detail"]} for r in decision.refusals]
    warns = list(decision.warnings)
    receipt = decision.execution_receipt or {
        "receipt_status": "not_executed_refusal",
        "execution_mode": "none",
        "scorecard_mode": "none",
        "benchmark_mode": "none",
        "checkpoint_mode": "none",
        "sc2_mode": "not_run",
    }

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M45_EXECUTION,
        "profile_id": PROFILE_M45_EXECUTION,
        "milestone": MILESTONE_LABEL_M45,
        "emitter_module": EMITTER_MODULE_M45,
        "profile": profile,
        **honesty,
        **mh,
        "execution_status": decision.execution_status,
        "m44_binding": bind44,
        "m44_preflight_interpretation": interp,
        "execution_receipt": receipt,
        "bounded_execution_surface_invoked": decision.bounded_execution_surface_invoked,
        "synthetic_execution_receipt_emitted": decision.synthetic_execution_receipt_emitted,
        "warnings": warns,
        "refusals": refs,
        "non_claims": list(NON_CLAIMS_M45),
        "m44_preflight_path_logical": cast(
            dict[str, Any] | str, redact_paths_in_value(m44_path_logical)
        ),
    }
    return body


def emit_m45_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    upstream = output_dir / "m44_upstream_fixture"
    m44_sealed, _ = emit_m44_fixture(upstream)
    m44_path = upstream / "v15_bounded_evaluation_execution_preflight.json"
    m44_plain = _parse_json_object(m44_path)

    decision = decide_m45(
        profile=PROFILE_FIXTURE_CI,
        m44=m44_plain,
        allow_operator_local_execution=False,
        authorize_bounded_evaluation_execution=False,
    )
    body = _assemble_execution_body(
        profile=PROFILE_FIXTURE_CI,
        m44_plain=m44_plain,
        decision=decision,
        m44_path_logical="redacted:m44_fixture_upstream",
    )
    sealed = seal_m45_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m45_artifacts(sealed, output_dir)


def emit_m45_operator(
    output_dir: Path,
    *,
    profile: str,
    m44_preflight_path: Path | None,
    allow_operator_local_execution: bool = False,
    authorize_bounded_evaluation_execution: bool = False,
    operator_logical_hint: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)

    m44_plain: dict[str, Any] | None = None
    logical_m44_path: str | Path = operator_logical_hint or "unknown_m44_preflight_path"
    if m44_preflight_path is not None:
        rp = Path(m44_preflight_path).resolve()
        logical_m44_path = operator_logical_hint or (
            str(rp) if rp.is_file() else str(m44_preflight_path)
        )
        if rp.is_file():
            try:
                m44_plain = _parse_json_object(rp)
            except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
                m44_plain = None

    decision = decide_m45(
        profile=profile,
        m44=m44_plain,
        allow_operator_local_execution=allow_operator_local_execution,
        authorize_bounded_evaluation_execution=authorize_bounded_evaluation_execution,
    )

    body = _assemble_execution_body(
        profile=profile,
        m44_plain=m44_plain,
        decision=decision,
        m44_path_logical=logical_m44_path,
    )
    sealed = seal_m45_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _emit_m45_artifacts(sealed, output_dir)


__all__ = (
    "M45Decision",
    "build_m44_interpretation",
    "build_m45_checklist_md",
    "decide_m45",
    "emit_m45_fixture_ci",
    "emit_m45_forbidden_flag_refusal",
    "emit_m45_operator",
    "refusal_code_from_forbidden_flags",
    "seal_m45_body",
    "structural_m44_validation_issues",
)
