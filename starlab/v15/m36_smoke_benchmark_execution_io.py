"""V15-M36: smoke benchmark execution surface over sealed M35 readiness JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    CONTRACT_ID_M35_READINESS,
    PROFILE_M35_READINESS,
    STATUS_READY,
)
from starlab.v15.m36_smoke_benchmark_execution_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M36_EXECUTION,
    EMITTER_MODULE_M36,
    EXECUTION_SCOPE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE_LABEL_M36,
    NON_CLAIMS_M36,
    PROFILE_FIXTURE_CI,
    PROFILE_M36_SURFACE,
    PROFILE_OPERATOR_BOUNDED_SMOKE,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SMOKE_POLICY_PREFLIGHT_ONLY,
    SMOKE_POLICY_SYNTHETIC_BOUNDED,
    STATUS_BLOCKED_INVALID_M35,
    STATUS_BLOCKED_MISSING_M35,
    STATUS_BLOCKED_NOT_READY,
    STATUS_BLOCKED_SHA_MISMATCH,
    STATUS_COMPLETED_SYNTHETIC,
    STATUS_FIXTURE_ONLY,
    STATUS_READY_BUT_NOT_RUN,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")


def _is_hex64(s: str) -> bool:
    t = str(s or "").strip().lower()
    return len(t) == 64 and all(c in _HEX64_CHARS for c in t)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _canonical_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(GATE_ARTIFACT_DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _claim_flags_m36() -> dict[str, Any]:
    """M36 claim surface; benchmark_execution_performed stays false everywhere."""
    return {
        "benchmark_execution_performed": False,
        "benchmark_passed": False,
        "scorecard_results_produced": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_authorized": False,
        "t3_authorized": False,
    }


def _smoke_execution_block(
    *,
    performed: bool,
    step_count: int,
    policy_id: str,
    mode: str,
    receipt_digest: str | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "smoke_execution_performed": performed,
        "smoke_step_count": step_count,
        "smoke_policy_id": policy_id,
        "execution_mode": mode,
    }
    if receipt_digest is not None:
        out["synthetic_bounded_smoke_receipt_sha256"] = receipt_digest
    return out


def _m35_upstream_binding(m35: dict[str, Any]) -> dict[str, Any]:
    seal = str(m35.get(GATE_ARTIFACT_DIGEST_FIELD) or "").lower()
    return {
        "artifact_sha256": seal,
        "contract_id": str(m35.get("contract_id", "")),
        "profile_id": str(m35.get("profile_id", "")),
        "readiness_status": str(m35.get("readiness_status", "")),
    }


def seal_m36_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m36_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_smoke_benchmark_execution_report",
        "report_version": "m36",
        "milestone": MILESTONE_LABEL_M36,
        "contract_id": CONTRACT_ID_M36_EXECUTION,
        "profile_id": PROFILE_M36_SURFACE,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "execution_status": sealed.get("execution_status"),
    }


def build_m36_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("execution_status", ""))
    gates = sealed.get("gates") or []
    gate_lines = ""
    if isinstance(gates, list):
        for g in gates:
            if isinstance(g, dict):
                gid = g.get("gate_id", "")
                nm = g.get("name", "")
                ps = g.get("passed", False)
                mk = "[x]" if ps else "[ ]"
                gate_lines += f"| {gid} | {nm} | {mk} |\n"
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return (
        "# V15-M36 — smoke benchmark execution checklist\n\n"
        f"**`execution_status`:** `{st}`  \n"
        f"**`execution_scope`:** `{EXECUTION_SCOPE}`\n\n"
        "V15-M36 is a smoke execution bookkeeping surface: it **does not** assert benchmark pass, "
        "strength, scorecard results, checkpoint promotion, 2-hour run, live SC2 outcomes, "
        "XAI/human/showcase/v2/T2/T3.\n\n"
        "| Gate | Name | Pass |\n"
        "| --- | --- | --- |\n"
        f"{gate_lines}\n"
        "## Non-claims\n\n"
        f"{nc_lines}\n"
    )


def _gate_pack(
    *,
    x0: bool,
    x1: bool,
    x2: bool,
    x3: bool,
    x4: bool,
    x5: bool,
    x6: bool,
) -> list[dict[str, Any]]:
    return [
        {"gate_id": "X0", "name": "M35 readiness contract valid", "passed": x0},
        {"gate_id": "X1", "name": "Candidate checkpoint SHA bound consistently", "passed": x1},
        {
            "gate_id": "X2",
            "name": "M35 readiness posture supports smoke execution route",
            "passed": x2,
        },
        {
            "gate_id": "X3",
            "name": "Smoke execution bounded (fixture/preflight no-run or synthetic bounded)",
            "passed": x3,
        },
        {"gate_id": "X4", "name": "No strength / promotion benchmark claims", "passed": x4},
        {"gate_id": "X5", "name": "Public/private boundary preserved", "passed": x5},
        {"gate_id": "X6", "name": "Non-claims present / claim posture honest", "passed": x6},
    ]


def _m35_claim_and_requirements_ok(m35: dict[str, Any]) -> bool:
    cf = m35.get("claim_flags")
    if not isinstance(cf, dict):
        return False
    for key in (
        "benchmark_execution_performed",
        "benchmark_passed",
        "scorecard_execution_performed",
        "strength_evaluated",
        "checkpoint_promoted",
    ):
        if cf.get(key) is not False:
            return False
    sm = m35.get("smoke_benchmark_requirements")
    if isinstance(sm, dict):
        for key in (
            "benchmark_execution_performed",
            "scorecard_execution_performed",
            "strength_evaluated",
            "checkpoint_promoted",
        ):
            if sm.get(key) is not False:
                return False
    return True


def _analyze_m35(
    m35: dict[str, Any] | None,
    *,
    expected_candidate_sha256: str | None,
) -> tuple[str, dict[str, Any] | None, dict[str, Any] | None, str]:
    """Return canonical status prefix, upstream binding when possible, candidate block."""
    if m35 is None:
        cand = {"sha256": "", "promotion_status": "unknown_missing_m35_readiness"}
        return STATUS_BLOCKED_MISSING_M35, None, cand, ""

    if not _canonical_seal_ok(m35):
        return STATUS_BLOCKED_INVALID_M35, None, None, ""

    cid = str(m35.get("contract_id", ""))
    pid = str(m35.get("profile_id", ""))

    if cid != CONTRACT_ID_M35_READINESS or pid != PROFILE_M35_READINESS:
        return STATUS_BLOCKED_INVALID_M35, None, None, ""

    cand_obj = m35.get("candidate_checkpoint")
    if not isinstance(cand_obj, dict):
        return STATUS_BLOCKED_INVALID_M35, None, None, ""

    cand_sha = str(cand_obj.get("sha256") or "").strip().lower()
    rst = str(m35.get("readiness_status", ""))

    exp_arg = str(expected_candidate_sha256 or "").strip().lower() or None
    if exp_arg is None:
        eff = cand_sha
    else:
        eff = exp_arg

    if rst != STATUS_READY:
        up = _m35_upstream_binding(m35)
        prom = str(cand_obj.get("promotion_status") or "not_promoted_candidate_only")
        return STATUS_BLOCKED_NOT_READY, up, {"sha256": cand_sha, "promotion_status": prom}, ""

    if not _is_hex64(cand_sha) or not _is_hex64(eff):
        up = _m35_upstream_binding(m35)
        return STATUS_BLOCKED_INVALID_M35, up, None, ""

    if cand_sha != eff:
        up = _m35_upstream_binding(m35)
        return (
            STATUS_BLOCKED_SHA_MISMATCH,
            up,
            {
                "sha256": cand_sha,
                "promotion_status": "sha_mismatch",
            },
            "",
        )

    if not _m35_claim_and_requirements_ok(m35):
        up = _m35_upstream_binding(m35)
        return STATUS_BLOCKED_INVALID_M35, up, None, ""

    up = _m35_upstream_binding(m35)
    cand_out = {
        "sha256": cand_sha if _is_hex64(cand_sha) else "",
        "promotion_status": str(cand_obj.get("promotion_status") or "not_promoted_candidate_only"),
    }
    return STATUS_READY_BUT_NOT_RUN, up, cand_out, ""


def _synthetic_smoke_digest(m35_upstream: dict[str, Any]) -> str:
    body = {
        "m36_synthetic_bounded_smoke": True,
        "m35_readiness_artifact_sha256_bound": str(m35_upstream.get("artifact_sha256", "")),
        "smoke_step_index": 0,
    }
    return sha256_hex_of_canonical_json(body)


def build_fixture_m36_body() -> dict[str, Any]:
    gates = _gate_pack(
        x0=False,
        x1=False,
        x2=False,
        x3=True,
        x4=True,
        x5=True,
        x6=True,
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M36_EXECUTION,
        "profile_id": PROFILE_M36_SURFACE,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M36,
        "emitter_module": EMITTER_MODULE_M36,
        "execution_status": STATUS_FIXTURE_ONLY,
        "execution_scope": EXECUTION_SCOPE,
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "candidate_checkpoint": {
            "sha256": "",
            "promotion_status": "not_applicable_fixture",
        },
        "upstream_bindings": {
            "m35_readiness": {
                "artifact_sha256": "",
                "contract_id": CONTRACT_ID_M35_READINESS,
                "profile_id": PROFILE_M35_READINESS,
                "readiness_status": "",
            },
        },
        "smoke_execution": _smoke_execution_block(
            performed=False,
            step_count=0,
            policy_id=SMOKE_POLICY_PREFLIGHT_ONLY,
            mode="fixture_ci",
        ),
        "claim_flags": _claim_flags_m36(),
        "gates": gates,
        "non_claims": list(NON_CLAIMS_M36),
    }


def build_operator_preflight_body(
    m35: dict[str, Any] | None,
    *,
    expected_candidate_sha256: str | None,
) -> dict[str, Any]:
    st, upstream, cand, _ = _analyze_m35(
        m35,
        expected_candidate_sha256=expected_candidate_sha256,
    )

    if st == STATUS_READY_BUT_NOT_RUN:
        gates = _gate_pack(
            x0=True,
            x1=True,
            x2=True,
            x3=True,
            x4=True,
            x5=True,
            x6=True,
        )
    elif st == STATUS_BLOCKED_MISSING_M35:
        gates = _gate_pack(
            x0=False,
            x1=False,
            x2=False,
            x3=True,
            x4=True,
            x5=True,
            x6=True,
        )
    elif st == STATUS_BLOCKED_INVALID_M35:
        gates = _gate_pack(
            x0=False,
            x1=False,
            x2=False,
            x3=False,
            x4=True,
            x5=True,
            x6=True,
        )
    elif st == STATUS_BLOCKED_NOT_READY:
        gates = _gate_pack(x0=False, x1=True, x2=False, x3=True, x4=True, x5=True, x6=True)
    elif st == STATUS_BLOCKED_SHA_MISMATCH:
        gates = _gate_pack(x0=True, x1=False, x2=False, x3=True, x4=True, x5=True, x6=True)
    else:
        gates = _gate_pack(x0=False, x1=False, x2=False, x3=True, x4=True, x5=True, x6=True)

    if cand is None and st != STATUS_BLOCKED_MISSING_M35:
        cand = {"sha256": "", "promotion_status": "not_applicable_blocked"}

    if upstream is None:
        upstream_out = {
            "m35_readiness": {
                "artifact_sha256": "",
                "contract_id": CONTRACT_ID_M35_READINESS,
                "profile_id": PROFILE_M35_READINESS,
                "readiness_status": "",
            },
        }
    else:
        upstream_out = {"m35_readiness": upstream}

    exec_st = STATUS_READY_BUT_NOT_RUN if st == STATUS_READY_BUT_NOT_RUN else st

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M36_EXECUTION,
        "profile_id": PROFILE_M36_SURFACE,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M36,
        "emitter_module": EMITTER_MODULE_M36,
        "execution_status": exec_st,
        "execution_scope": EXECUTION_SCOPE,
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "candidate_checkpoint": cand,
        "upstream_bindings": upstream_out,
        "smoke_execution": _smoke_execution_block(
            performed=False,
            step_count=0,
            policy_id=SMOKE_POLICY_PREFLIGHT_ONLY,
            mode="operator_preflight",
        ),
        "claim_flags": _claim_flags_m36(),
        "gates": gates,
        "non_claims": list(NON_CLAIMS_M36),
    }


def build_bounded_synthetic_body(
    m35: dict[str, Any],
    *,
    expected_candidate_sha256: str | None,
    max_smoke_steps: int,
) -> dict[str, Any]:
    st, upstream, cand, _ = _analyze_m35(
        m35,
        expected_candidate_sha256=expected_candidate_sha256,
    )
    if upstream is None or cand is None or st != STATUS_READY_BUT_NOT_RUN:
        raise ValueError(f"bounded synthetic requires valid M35 readiness; got_status={st!r}")

    if max_smoke_steps < 1:
        raise ValueError("max_smoke_steps must be >= 1")

    receipt = _synthetic_smoke_digest(upstream)
    gates = _gate_pack(
        x0=True,
        x1=True,
        x2=True,
        x3=True,
        x4=True,
        x5=True,
        x6=True,
    )

    bounded_steps = min(1, max_smoke_steps)
    smoke = _smoke_execution_block(
        performed=True,
        step_count=bounded_steps,
        policy_id=SMOKE_POLICY_SYNTHETIC_BOUNDED,
        mode=PROFILE_OPERATOR_BOUNDED_SMOKE,
        receipt_digest=receipt,
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M36_EXECUTION,
        "profile_id": PROFILE_M36_SURFACE,
        "profile": PROFILE_OPERATOR_BOUNDED_SMOKE,
        "milestone": MILESTONE_LABEL_M36,
        "emitter_module": EMITTER_MODULE_M36,
        "execution_status": STATUS_COMPLETED_SYNTHETIC,
        "execution_scope": EXECUTION_SCOPE,
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "candidate_checkpoint": cand,
        "upstream_bindings": {"m35_readiness": upstream},
        "smoke_execution": smoke,
        "claim_flags": _claim_flags_m36(),
        "gates": gates,
        "non_claims": list(NON_CLAIMS_M36),
    }


def emit_m36_fixture(output_dir: Path) -> tuple[dict[str, Any], Path, Path, Path]:
    body_pre = build_fixture_m36_body()
    sealed = seal_m36_body(redact_paths_in_value(body_pre))
    if not isinstance(sealed, dict):
        raise TypeError("expected dict")
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    rep = build_m36_report(sealed)
    chk = build_m36_checklist_md(sealed)
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M36 fixture emission leaked path patterns")
    return sealed, p_main, p_rep, p_chk


def emit_m36_operator_preflight(
    output_dir: Path,
    *,
    m35_path: Path | None,
    expected_candidate_sha256: str | None = None,
) -> tuple[dict[str, Any], Path, Path, Path]:
    m35_obj: dict[str, Any] | None = None
    if m35_path is not None and m35_path.is_file():
        m35_obj = _parse_json_object(m35_path.resolve())

    body_pre = build_operator_preflight_body(
        m35_obj,
        expected_candidate_sha256=expected_candidate_sha256,
    )
    red = redact_paths_in_value(body_pre)
    if not isinstance(red, dict):
        raise TypeError("expected dict")
    sealed = seal_m36_body(red)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    rep = build_m36_report(sealed)
    chk = build_m36_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M36 operator_preflight emission leaked path patterns")
    return sealed, p_main, p_rep, p_chk


def emit_m36_bounded_synthetic_smoke(
    output_dir: Path,
    *,
    m35_path: Path,
    expected_candidate_sha256: str | None,
    max_smoke_steps: int,
) -> tuple[dict[str, Any], Path, Path, Path]:
    m35_obj = _parse_json_object(m35_path.resolve())
    body_pre = build_bounded_synthetic_body(
        m35_obj,
        expected_candidate_sha256=expected_candidate_sha256,
        max_smoke_steps=max_smoke_steps,
    )
    red = redact_paths_in_value(body_pre)
    if not isinstance(red, dict):
        raise TypeError("expected dict")
    sealed = seal_m36_body(red)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    rep = build_m36_report(sealed)
    chk = build_m36_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M36 bounded_smoke emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk
