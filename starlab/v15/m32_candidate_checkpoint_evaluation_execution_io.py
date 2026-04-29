"""V15-M32 evaluation execution validation, sealing, emission."""

from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    build_fixture_m30_sealed_package,
    emission_has_private_path_patterns,
    emit_v15_m31_candidate_checkpoint_evaluation_harness_gate,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    CONTRACT_ID_M31_GATE,
    PROFILE_M31_DRY_RUN,
    SCORECARD_BOUND_IN_M31,
    SCORECARD_OPTIONAL_NOT_SUPPLIED,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_models import (
    STATUS_READY as M31_STATUS_READY,
)
from starlab.v15.m32_candidate_checkpoint_evaluation_execution_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M32_EVAL_EXEC,
    EMITTER_MODULE_M32,
    EXECUTION_MODE_FIXTURE,
    EXECUTION_MODE_METADATA_ONLY,
    EXECUTION_SCOPE_FIXTURE_METADATA,
    FILENAME_EXEC_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE_LABEL_M32,
    NON_CLAIMS_M32,
    PROFILE_M32_BOUNDED,
    RECOMMENDED_NEXT_DEFAULT,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SCORECARD_INHERITED_BOUND_IN_M31,
    SCORECARD_INHERITED_MISSING,
    SCORECARD_INHERITED_OPTIONAL_NOT_SUPPLIED,
    STATUS_FIXTURE_COMPLETED,
    STATUS_OPERATOR_LOCAL_METADATA_COMPLETED,
    STATUS_REFUSED_BLOCKERS,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _canonical_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get("artifact_sha256")
    wo = {k: v for k, v in raw.items() if k != "artifact_sha256"}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in or "").lower() == computed.lower()


def _blocked_sorted(reasons: list[str]) -> list[str]:
    return sorted(dict.fromkeys(reasons))


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def load_m31_harness_gate_json(path: Path) -> dict[str, Any]:
    """Parse sealed M31 harness gate JSON."""
    return _parse_json_object(path)


def build_fixture_m31_sealed_gate() -> dict[str, Any]:
    """Deterministic M31 gate body used by `--fixture-ci` (matches M31 fixture pipeline)."""
    with TemporaryDirectory() as td:
        out = Path(td) / "m31_gate"
        sealed, _, _, _ = emit_v15_m31_candidate_checkpoint_evaluation_harness_gate(
            out,
            m30_sealed=build_fixture_m30_sealed_package(),
            fixture_ci=True,
            m05_path=None,
        )
        return sealed


def scorecard_binding_status_m32(m31: dict[str, Any]) -> str:
    """Map M31 scorecard binding to M32 inherited label."""
    raw = m31.get("scorecard_binding_status")
    if raw is None:
        return SCORECARD_INHERITED_MISSING
    s = str(raw)
    if s == SCORECARD_BOUND_IN_M31:
        return SCORECARD_INHERITED_BOUND_IN_M31
    if s == SCORECARD_OPTIONAL_NOT_SUPPLIED:
        return SCORECARD_INHERITED_OPTIONAL_NOT_SUPPLIED
    return SCORECARD_INHERITED_MISSING


def validate_m31_for_m32(m31: dict[str, Any]) -> list[str]:
    """Sorted M32 blocker codes for consumption of a sealed M31 harness gate."""
    blocked: list[str] = []

    if not _canonical_seal_ok(m31):
        blocked.append("blocked_invalid_m31_contract")

    if str(m31.get("contract_id", "")) != CONTRACT_ID_M31_GATE:
        blocked.append("blocked_invalid_m31_contract")

    if str(m31.get("profile", "")) != PROFILE_M31_DRY_RUN:
        blocked.append("blocked_invalid_m31_profile")

    if str(m31.get("gate_status", "")) != M31_STATUS_READY:
        blocked.append("blocked_m31_gate_not_ready")

    if not bool(m31.get("evaluation_harness_ready")):
        blocked.append("blocked_m31_gate_not_ready")

    must_be_false = (
        ("evaluation_execution_performed", False),
        ("scorecard_execution_performed", False),
        ("strength_evaluated", False),
        ("checkpoint_promoted", False),
        ("benchmark_passed", False),
    )
    for key, expected in must_be_false:
        if m31.get(key) is not expected:
            blocked.append("blocked_m31_claim_flags_inconsistent")

    cand_o = m31.get("candidate_checkpoint")
    cand: dict[str, Any] = cand_o if isinstance(cand_o, dict) else {}
    cand_sha = str(cand.get("sha256") or "").lower()

    if not cand:
        blocked.append("blocked_m31_candidate_checkpoint_missing")
    elif not _is_hex64(cand_sha):
        blocked.append("blocked_m31_candidate_checkpoint_sha_missing")
    else:
        ps = cand.get("promotion_status")
        if ps is not None and str(ps) != "not_promoted_candidate_only":
            blocked.append("blocked_m31_candidate_checkpoint_not_candidate_only")

    drp_o = m31.get("dry_run_evaluation_plan")
    drp: dict[str, Any] = drp_o if isinstance(drp_o, dict) else {}
    if not drp:
        blocked.append("blocked_m31_dry_run_plan_missing")
    else:
        if str(drp.get("plan_status") or "") != "constructed_not_executed":
            blocked.append("blocked_m31_dry_run_plan_missing")
        if drp.get("candidate_loaded") is not False:
            blocked.append("blocked_m31_dry_run_plan_missing")
        if drp.get("matches_scheduled") is not False:
            blocked.append("blocked_m31_dry_run_plan_missing")
        if drp.get("scorecard_results_present") is not False:
            blocked.append("blocked_m31_dry_run_plan_missing")

    return _blocked_sorted(blocked)


def seal_m32_execution_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m32_execution_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_evaluation_execution_report",
        "report_version": "m32",
        "milestone": MILESTONE_LABEL_M32,
        "contract_id": CONTRACT_ID_M32_EVAL_EXEC,
        "profile": PROFILE_M32_BOUNDED,
        "artifact_sha256": digest,
        "execution_status": sealed.get("execution_status"),
        "evaluation_execution_performed": sealed.get("evaluation_execution_performed"),
        "blocked_reasons": sealed.get("blocked_reasons"),
    }


def build_m32_checklist_md(sealed: dict[str, Any]) -> str:
    br = sealed.get("blocked_reasons") or []
    st = str(sealed.get("execution_status", ""))
    ok_exec = str(st).endswith("_completed") and "refused" not in str(st).lower()
    mk = "[x]" if ok_exec else "[ ]"
    br_txt = ", ".join(str(x) for x in br) if br else "(none)"
    return (
        "# V15-M32 — candidate checkpoint bounded evaluation execution checklist\n\n"
        f"**`execution_status`:** `{st}`  \n"
        f"**`blocked_reasons`:** `{br_txt}`\n\n"
        "| Gate | Check |\n"
        "| --- | --- |\n"
        "| E0 — M31 harness gate seal + contract/profile valid | " + mk + " |\n"
        "| E1 — Bounded execution (fixture or metadata-only) | " + mk + " |\n"
        "| E2 — No checkpoint blob load; no candidate model load | " + mk + " |\n"
        "| E3 — No benchmark / strength / promotion claims | " + mk + " |\n\n"
        "Bounded evaluation execution ≠ strong-agent benchmark pass.\n"
    )


def _non_claim_bools_exec(success: bool) -> dict[str, bool]:
    return {
        "evaluation_execution_performed": success,
        "scorecard_execution_performed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "benchmark_passed": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_or_t3_authorized": False,
        "checkpoint_blob_io_performed": False,
        "candidate_model_loaded": False,
    }


def _bounded_case(max_cases: int) -> dict[str, Any]:
    return {
        "case_id": "fixture_eval_case_001",
        "case_type": "metadata_execution_probe",
        "case_status": "completed",
        "candidate_loaded": False,
        "match_executed": False,
        "score_produced": False,
        "purpose": "prove execution artifact flow without strength claim",
        "evaluation_case_index": 1,
        "evaluation_cases_cap": max_cases,
    }


def build_m32_execution_body_pre_seal(
    *,
    m31: dict[str, Any],
    fixture_ci: bool,
    max_evaluation_cases: int,
    blocker_codes: list[str],
) -> dict[str, Any]:
    cand_o = m31.get("candidate_checkpoint")
    cand_src: dict[str, Any] = cand_o if isinstance(cand_o, dict) else {}
    cand_sha = str(cand_src.get("sha256") or "").lower()
    promo = cand_src.get("promotion_status")
    promo_eff = str(promo) if promo is not None else "not_promoted_candidate_only"
    m31_art = str(m31.get("artifact_sha256") or "").lower()
    gs = str(m31.get("gate_status") or "")

    ready = len(blocker_codes) == 0
    nc = _non_claim_bools_exec(success=ready)
    if not ready:
        exe_status = STATUS_REFUSED_BLOCKERS
    elif fixture_ci:
        exe_status = STATUS_FIXTURE_COMPLETED
    else:
        exe_status = STATUS_OPERATOR_LOCAL_METADATA_COMPLETED

    score_m32 = scorecard_binding_status_m32(m31)

    bounded = {
        "result_status": "completed_not_strength_scored" if ready else "refused_or_blocked",
        "evaluation_cases_requested": max_evaluation_cases,
        "evaluation_cases_completed": max_evaluation_cases if ready else 0,
        "scorecard_results_present": False,
        "strength_score_present": False,
        "cases": [_bounded_case(max_evaluation_cases)] if ready else [],
    }

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M32_EVAL_EXEC,
        "milestone": MILESTONE_LABEL_M32,
        "profile": PROFILE_M32_BOUNDED,
        "emitter_module": EMITTER_MODULE_M32,
        "execution_status": exe_status,
        "execution_scope": EXECUTION_SCOPE_FIXTURE_METADATA,
        "fixture_ci": fixture_ci,
        "execution_mode": (EXECUTION_MODE_FIXTURE if fixture_ci else EXECUTION_MODE_METADATA_ONLY),
        "blocked_reasons": list(blocker_codes),
        "scorecard_binding_status": score_m32,
        "m31_harness_gate_binding": {
            "artifact_sha256": m31_art,
            "gate_status": gs,
            "profile": str(m31.get("profile") or ""),
        },
        "candidate_checkpoint": {
            "sha256": cand_sha,
            "promotion_status": promo_eff,
            "checkpoint_blob_io_performed": False,
            "candidate_model_loaded": False,
        },
        "bounded_execution_result": bounded,
        "recommended_next": RECOMMENDED_NEXT_DEFAULT,
        "non_claims": list(NON_CLAIMS_M32),
        **nc,
    }
    return body


def seal_with_path_hygiene_m32(body_pre: dict[str, Any]) -> dict[str, Any]:
    sealed = seal_m32_execution_body(body_pre)
    dump = canonical_json_dumps(sealed) + canonical_json_dumps(build_m32_execution_report(sealed))
    if emission_has_private_path_patterns(dump):
        extra = ["blocked_private_path_leak_detected"]
        rebuilt = dict(body_pre)
        merged = _blocked_sorted([*(rebuilt.get("blocked_reasons") or []), *extra])
        rebuilt["blocked_reasons"] = merged
        rebuilt["execution_status"] = STATUS_REFUSED_BLOCKERS
        nc_fail = _non_claim_bools_exec(success=False)
        for kf, vf in nc_fail.items():
            rebuilt[kf] = vf
        cap_raw = rebuilt.get("bounded_execution_result") or {}
        cap_e = cap_raw.get("evaluation_cases_requested") if isinstance(cap_raw, dict) else None
        eval_cap = int(cap_e) if isinstance(cap_e, int) else 1
        rebuilt["bounded_execution_result"] = {
            "result_status": "refused_or_blocked",
            "evaluation_cases_requested": eval_cap,
            "evaluation_cases_completed": 0,
            "scorecard_results_present": False,
            "strength_score_present": False,
            "cases": [],
        }
        sealed2 = seal_m32_execution_body(rebuilt)
        return sealed2
    return sealed


def emit_v15_m32_candidate_checkpoint_evaluation_execution(
    output_dir: Path,
    *,
    m31_gate: dict[str, Any],
    fixture_ci: bool,
    max_evaluation_cases: int,
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Validate M31 gate, seal M32 artifacts, write JSON/report/checklist."""
    blocker_codes = validate_m31_for_m32(m31_gate)
    body_pre = build_m32_execution_body_pre_seal(
        m31=m31_gate,
        fixture_ci=fixture_ci,
        max_evaluation_cases=max_evaluation_cases,
        blocker_codes=blocker_codes,
    )
    sealed = seal_with_path_hygiene_m32(body_pre)

    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m32_execution_report(sealed)
    chk = build_m32_checklist_md(sealed)

    p_exe = output_dir / FILENAME_EXEC_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    p_exe.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError(
            "M32 emitter produced path leakage; refuse to finalize output.",
        )

    return sealed, p_exe, p_rep, p_chk
