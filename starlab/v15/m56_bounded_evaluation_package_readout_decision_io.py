"""V15-M56 — bounded evaluation package readout / decision IO."""

from __future__ import annotations

import hashlib
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
from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
    build_fixture_preflight,
    seal_m55_body,
)
from starlab.v15.m56_bounded_evaluation_package_readout_decision_models import (
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CHECKLIST_FILENAME,
    CONTRACT_ID,
    CONTRACT_ID_M54,
    CONTRACT_ID_M55,
    CONTRACT_ID_M56A,
    DECISION_BLOCKED_CANDIDATE_MISMATCH,
    DECISION_BLOCKED_CLAIM_FLAGS,
    DECISION_BLOCKED_INVALID_M55_CONTRACT,
    DECISION_BLOCKED_INVALID_M55_SEAL,
    DECISION_BLOCKED_M53_MISMATCH,
    DECISION_BLOCKED_M54_MISMATCH,
    DECISION_BLOCKED_M55_NOT_READY,
    DECISION_BLOCKED_MISSING_M55,
    DECISION_BLOCKED_PRIVATE_BOUNDARY,
    DECISION_READY,
    DECISION_REQUIRES_REMEDIATION,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M55_FORBIDDEN_TRUE_FLAGS,
    M55_STATUS_READY,
    M56A_CONTEXT_ABSENT,
    M56A_CONTEXT_ADAPTER_DECLARED,
    M56A_CONTEXT_SCAFFOLD,
    M56A_CONTEXT_STUB,
    M56A_GATING_NOT_A_GATE,
    MILESTONE,
    NON_CLAIMS,
    PROFILE_FIXTURE_CI,
    PROFILE_M56,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_MILESTONE,
    RECOMMENDED_NEXT_TITLE,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    ROUTE_NEXT,
    ROUTE_STATUS,
    SCHEMA_VERSION,
    STRONGEST_ALLOWED,
    WARNING_CROSS_CHECK_NO_M54_BODY,
    WARNING_M56A_ABSENT,
    WARNING_M56A_INVALID,
    WARNING_M56A_STUB,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")
_PATH_OUT_SEGMENT: Final[re.Pattern[str]] = re.compile(
    r"(?:^|[\\/])out(?:[\\/]|$)|[\\/]out[\\/]",
    re.IGNORECASE,
)
DIGEST_FIELD = GATE_ARTIFACT_DIGEST_FIELD


def validate_sha256(s: str) -> str | None:
    t = str(s or "").strip().lower()
    if len(t) != 64 or any(c not in _HEX64_CHARS for c in t):
        return None
    return t


def sha256_file_hex(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fb:
        while chunk := fb.read(chunk_size):
            h.update(chunk)
    return h.hexdigest().lower()


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def verify_m55_artifact_seal(sealed: dict[str, Any]) -> None:
    digest_in = sealed.get(DIGEST_FIELD)
    if digest_in is None or str(digest_in).strip() == "":
        raise ValueError(DECISION_BLOCKED_INVALID_M55_SEAL)
    wo = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    if str(digest_in).strip().lower() != computed.lower():
        raise ValueError(DECISION_BLOCKED_INVALID_M55_SEAL)


def load_m55_preflight(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(DECISION_BLOCKED_MISSING_M55)
    raw = _parse_json_object(path.resolve())
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M55:
        raise ValueError(DECISION_BLOCKED_INVALID_M55_CONTRACT)
    verify_m55_artifact_seal(raw)
    return raw


def m55_upstream_m54_sha(m55: dict[str, Any]) -> str:
    ip = m55.get("input_package") or {}
    if isinstance(ip, dict):
        v = str(ip.get("declared_upstream_m54_package_sha256") or "").strip().lower()
        if len(v) == 64:
            return v
    ri = m55.get("required_inputs") or {}
    if isinstance(ri, dict):
        v = str(ri.get("m54_package_sha256") or "").strip().lower()
        if len(v) == 64:
            return v
    return ""


def m55_claim_flags_violation(m55: dict[str, Any]) -> bool:
    cf = m55.get("claim_flags")
    if not isinstance(cf, dict):
        return False
    for k, v in cf.items():
        if k in M55_FORBIDDEN_TRUE_FLAGS and v is True:
            return True
    return False


def _boundary_violation_reason(raw_text: str) -> str | None:
    low = raw_text.lower()
    if "company_secrets" in low:
        return "company_secrets_reference"
    if _PATH_OUT_SEGMENT.search(raw_text):
        return "raw_out_path_reference"
    if emission_has_private_path_patterns(raw_text):
        return "private_path_pattern"
    return None


def verify_m54_readiness_seal(sealed: dict[str, Any]) -> None:
    digest_in = sealed.get(DIGEST_FIELD)
    if digest_in is None or str(digest_in).strip() == "":
        raise ValueError(DECISION_BLOCKED_INVALID_M55_CONTRACT)
    wo = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    if str(digest_in).strip().lower() != computed.lower():
        raise ValueError(DECISION_BLOCKED_INVALID_M55_CONTRACT)


def extract_m54_cross_checks(m54: dict[str, Any]) -> tuple[str, str]:
    mb = m54.get("m53_binding") or {}
    if not isinstance(mb, dict):
        mb = {}
    m53_art = str(mb.get("artifact_sha256") or "").strip().lower()
    ccb = m54.get("candidate_checkpoint_binding") or {}
    if not isinstance(ccb, dict):
        ccb = {}
    cand = str(ccb.get("produced_candidate_checkpoint_sha256") or "").strip().lower()
    return m53_art, cand


def load_m54_readiness_for_cross_check(path: Path, *, expected_package_sha: str) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError(DECISION_BLOCKED_M54_MISMATCH)
    raw_txt = path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        raise ValueError(DECISION_BLOCKED_PRIVATE_BOUNDARY)
    m54 = _parse_json_object(path.resolve())
    if str(m54.get("contract_id") or "") != CONTRACT_ID_M54:
        raise ValueError(DECISION_BLOCKED_M54_MISMATCH)
    verify_m54_readiness_seal(m54)
    got_pkg = str(m54.get(DIGEST_FIELD) or "").strip().lower()
    if got_pkg != expected_package_sha.lower():
        raise ValueError(DECISION_BLOCKED_M54_MISMATCH)
    return extract_m54_cross_checks(m54)


def classify_m56a_context(path: Path | None) -> tuple[str, str, str | None]:
    """Return (context_status, gating_status, optional note)."""
    if path is None:
        return M56A_CONTEXT_ABSENT, M56A_GATING_NOT_A_GATE, None
    if not path.is_file():
        return M56A_CONTEXT_ABSENT, M56A_GATING_NOT_A_GATE, None
    try:
        raw_txt = path.read_text(encoding="utf-8")
    except OSError:
        return "visual_watchability_context_invalid", M56A_GATING_NOT_A_GATE, WARNING_M56A_INVALID
    br = _boundary_violation_reason(raw_txt)
    if br:
        return "visual_watchability_context_invalid", M56A_GATING_NOT_A_GATE, WARNING_M56A_INVALID
    try:
        ctx = json.loads(raw_txt)
    except json.JSONDecodeError:
        return "visual_watchability_context_invalid", M56A_GATING_NOT_A_GATE, WARNING_M56A_INVALID
    if not isinstance(ctx, dict):
        return "visual_watchability_context_invalid", M56A_GATING_NOT_A_GATE, WARNING_M56A_INVALID
    if str(ctx.get("contract_id") or "") != CONTRACT_ID_M56A:
        return "visual_watchability_context_invalid", M56A_GATING_NOT_A_GATE, WARNING_M56A_INVALID
    wp = ctx.get("watchability_profile") or {}
    pol = ""
    vis = ""
    if isinstance(wp, dict):
        pol = str(wp.get("policy_source") or "")
        vis = str(wp.get("visual_confirmation_status") or "")
    if pol == "scaffold_watchability_policy":
        return M56A_CONTEXT_SCAFFOLD, M56A_GATING_NOT_A_GATE, None
    if vis in ("scaffold_watchability_confirmed_not_candidate_policy",):
        return M56A_CONTEXT_SCAFFOLD, M56A_GATING_NOT_A_GATE, None
    if pol == "fixture" or vis == "fixture_schema_only_no_live_sc2":
        return M56A_CONTEXT_STUB, M56A_GATING_NOT_A_GATE, None
    if pol == "candidate_live_adapter" or vis in (
        "visual_watchability_confirmed",
        "visual_watchability_confirmed_with_warnings",
    ):
        return M56A_CONTEXT_ADAPTER_DECLARED, M56A_GATING_NOT_A_GATE, None
    return "visual_watchability_context_supplied", M56A_GATING_NOT_A_GATE, None


def _claim_template() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def seal_m56_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def _m56a_warnings_for_context(status: str) -> list[str]:
    if status == M56A_CONTEXT_ABSENT:
        return [WARNING_M56A_ABSENT]
    if status in (M56A_CONTEXT_STUB, M56A_CONTEXT_SCAFFOLD):
        return [WARNING_M56A_STUB]
    return []


@dataclass(frozen=True)
class OperatorPreflightReadoutInputs:
    m55_preflight_json: Path
    expected_m54_package_sha256: str
    expected_m53_run_artifact_sha256: str
    expected_candidate_sha256: str
    m54_readiness_json: Path | None
    m56a_context_json: Path | None


def build_operator_preflight_readout_decision(
    inputs: OperatorPreflightReadoutInputs,
) -> dict[str, Any]:
    warnings: list[str] = []
    blocked: list[str] = []
    m55_sha_bind: str | None = None
    m56a_note: str | None = None

    ctx_stat, _gate, inv_note = classify_m56a_context(inputs.m56a_context_json)
    if inv_note:
        warnings.append(inv_note)
    warnings.extend(_m56a_warnings_for_context(ctx_stat))

    try:
        m55 = load_m55_preflight(inputs.m55_preflight_json.resolve())
    except ValueError as exc:
        code = str(exc)
        blocked.append(
            code
            if code
            in (
                DECISION_BLOCKED_MISSING_M55,
                DECISION_BLOCKED_INVALID_M55_CONTRACT,
                DECISION_BLOCKED_INVALID_M55_SEAL,
            )
            else DECISION_BLOCKED_INVALID_M55_CONTRACT,
        )
        return _blocked_readout_body(
            decision=_map_blocked_to_decision(blocked[0]),
            blocked=blocked,
            warnings=warnings,
            m55=m55_sha_bind,
            m55_obj=None,
            exp_m54=inputs.expected_m54_package_sha256,
            exp_m53=inputs.expected_m53_run_artifact_sha256,
            exp_cand=inputs.expected_candidate_sha256,
            m56a_ctx=ctx_stat,
            m56a_note=m56a_note or inv_note,
        )
    except (OSError, json.JSONDecodeError):
        blocked.append(DECISION_BLOCKED_INVALID_M55_CONTRACT)
        return _blocked_readout_body(
            decision=DECISION_BLOCKED_INVALID_M55_CONTRACT,
            blocked=blocked,
            warnings=warnings,
            m55=m55_sha_bind,
            m55_obj=None,
            exp_m54=inputs.expected_m54_package_sha256,
            exp_m53=inputs.expected_m53_run_artifact_sha256,
            exp_cand=inputs.expected_candidate_sha256,
            m56a_ctx=ctx_stat,
            m56a_note=m56a_note or inv_note,
        )

    m55_sha_bind = str(m55.get(DIGEST_FIELD) or "").strip().lower()

    if m55_claim_flags_violation(m55):
        blocked.append(DECISION_BLOCKED_CLAIM_FLAGS)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_CLAIM_FLAGS,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_all_false(),
            exp_m54=inputs.expected_m54_package_sha256,
            exp_m53=inputs.expected_m53_run_artifact_sha256,
            exp_cand=inputs.expected_candidate_sha256,
            m53_obs="",
            cand_obs="",
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )

    if str(m55.get("preflight_status") or "") != M55_STATUS_READY:
        blocked.append(DECISION_BLOCKED_M55_NOT_READY)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_M55_NOT_READY,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_blocked(),
            exp_m54=inputs.expected_m54_package_sha256,
            exp_m53=inputs.expected_m53_run_artifact_sha256,
            exp_cand=inputs.expected_candidate_sha256,
            m53_obs="",
            cand_obs="",
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )

    exp54 = validate_sha256(inputs.expected_m54_package_sha256)
    exp53 = validate_sha256(inputs.expected_m53_run_artifact_sha256)
    exp_c = validate_sha256(inputs.expected_candidate_sha256)
    if exp54 is None or exp53 is None or exp_c is None:
        blocked.append(DECISION_BLOCKED_M54_MISMATCH)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_M54_MISMATCH,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_blocked(),
            exp_m54=inputs.expected_m54_package_sha256,
            exp_m53=inputs.expected_m53_run_artifact_sha256,
            exp_cand=inputs.expected_candidate_sha256,
            m53_obs="",
            cand_obs="",
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )

    m55_m54 = m55_upstream_m54_sha(m55)
    if m55_m54 != exp54:
        blocked.append(DECISION_BLOCKED_M54_MISMATCH)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_M54_MISMATCH,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_partial(m54_ok=False),
            exp_m54=exp54,
            exp_m53=exp53,
            exp_cand=exp_c,
            m53_obs="",
            cand_obs="",
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )

    m53_observed = ""
    cand_observed = ""
    if inputs.m54_readiness_json is not None:
        try:
            m53_observed, cand_observed = load_m54_readiness_for_cross_check(
                inputs.m54_readiness_json.resolve(),
                expected_package_sha=exp54,
            )
        except ValueError as exc:
            code = str(exc)
            if code == DECISION_BLOCKED_PRIVATE_BOUNDARY:
                blocked.append(DECISION_BLOCKED_PRIVATE_BOUNDARY)
                dec = DECISION_BLOCKED_PRIVATE_BOUNDARY
            else:
                blocked.append(
                    DECISION_BLOCKED_M54_MISMATCH
                    if "m54" in code.lower()
                    else DECISION_BLOCKED_M53_MISMATCH,
                )
                dec = blocked[-1]
            return _finalize_readout_from_state(
                m55=m55,
                m55_digest=m55_sha_bind,
                decision=dec,
                blocked=blocked,
                warnings=warnings,
                preflight_summary=_preflight_summary_blocked(),
                exp_m54=exp54,
                exp_m53=exp53,
                exp_cand=exp_c,
                m53_obs=m53_observed,
                cand_obs=cand_observed,
                m56a_ctx=ctx_stat,
                m56a_note=inv_note,
            )
    else:
        warnings.append(WARNING_CROSS_CHECK_NO_M54_BODY)
        if exp53 != CANONICAL_M53_RUN_ARTIFACT_SHA256.lower():
            blocked.append(DECISION_BLOCKED_M53_MISMATCH)
            return _finalize_readout_from_state(
                m55=m55,
                m55_digest=m55_sha_bind,
                decision=DECISION_BLOCKED_M53_MISMATCH,
                blocked=blocked,
                warnings=warnings,
                preflight_summary=_preflight_summary_partial(m54_ok=True, m53_ok=False),
                exp_m54=exp54,
                exp_m53=exp53,
                exp_cand=exp_c,
                m53_obs="",
                cand_obs="",
                m56a_ctx=ctx_stat,
                m56a_note=inv_note,
            )
        if exp_c != CANONICAL_CANDIDATE_CHECKPOINT_SHA256.lower():
            blocked.append(DECISION_BLOCKED_CANDIDATE_MISMATCH)
            return _finalize_readout_from_state(
                m55=m55,
                m55_digest=m55_sha_bind,
                decision=DECISION_BLOCKED_CANDIDATE_MISMATCH,
                blocked=blocked,
                warnings=warnings,
                preflight_summary=_preflight_summary_partial(
                    m54_ok=True,
                    m53_ok=True,
                    cand_ok=False,
                ),
                exp_m54=exp54,
                exp_m53=exp53,
                exp_cand=exp_c,
                m53_obs="",
                cand_obs="",
                m56a_ctx=ctx_stat,
                m56a_note=inv_note,
            )
        m53_observed = exp53
        cand_observed = exp_c

    if m53_observed != exp53:
        blocked.append(DECISION_BLOCKED_M53_MISMATCH)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_M53_MISMATCH,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_partial(m54_ok=True, m53_ok=False),
            exp_m54=exp54,
            exp_m53=exp53,
            exp_cand=exp_c,
            m53_obs=m53_observed,
            cand_obs=cand_observed,
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )
    if cand_observed != exp_c:
        blocked.append(DECISION_BLOCKED_CANDIDATE_MISMATCH)
        return _finalize_readout_from_state(
            m55=m55,
            m55_digest=m55_sha_bind,
            decision=DECISION_BLOCKED_CANDIDATE_MISMATCH,
            blocked=blocked,
            warnings=warnings,
            preflight_summary=_preflight_summary_partial(
                m54_ok=True,
                m53_ok=True,
                cand_ok=False,
            ),
            exp_m54=exp54,
            exp_m53=exp53,
            exp_cand=exp_c,
            m53_obs=m53_observed,
            cand_obs=cand_observed,
            m56a_ctx=ctx_stat,
            m56a_note=inv_note,
        )

    return _finalize_readout_from_state(
        m55=m55,
        m55_digest=m55_sha_bind,
        decision=DECISION_READY,
        blocked=[],
        warnings=warnings,
        preflight_summary=_preflight_summary_ok(),
        exp_m54=exp54,
        exp_m53=exp53,
        exp_cand=exp_c,
        m53_obs=m53_observed,
        cand_obs=cand_observed,
        m56a_ctx=ctx_stat,
        m56a_note=inv_note,
    )


def _map_blocked_to_decision(code: str) -> str:
    mapping = {
        DECISION_BLOCKED_MISSING_M55: DECISION_BLOCKED_MISSING_M55,
        DECISION_BLOCKED_INVALID_M55_CONTRACT: DECISION_BLOCKED_INVALID_M55_CONTRACT,
        DECISION_BLOCKED_INVALID_M55_SEAL: DECISION_BLOCKED_INVALID_M55_SEAL,
    }
    return mapping.get(code, DECISION_BLOCKED_INVALID_M55_CONTRACT)


def _blocked_readout_body(
    *,
    decision: str,
    blocked: list[str],
    warnings: list[str],
    m55: str | None,
    m55_obj: dict[str, Any] | None,
    exp_m54: str,
    exp_m53: str,
    exp_cand: str,
    m56a_ctx: str,
    m56a_note: str | None,
) -> dict[str, Any]:
    pf = _preflight_summary_blocked()
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "input_bindings": {
            "m55_preflight_artifact_sha256": m55,
            "m55_contract_id": CONTRACT_ID_M55,
            "m55_preflight_status": (str(m55_obj.get("preflight_status") or "") if m55_obj else ""),
            "m54_package_sha256": exp_m54,
            "m53_run_artifact_sha256": exp_m53,
            "candidate_checkpoint_sha256": exp_cand,
            "m56a_context_sha256": None,
        },
        "readout": {
            "decision_status": decision,
            "decision_reason": _decision_reason(decision, blocked),
            "blocked_reasons": list(blocked),
            "warnings": list(warnings),
            "requires_remediation": decision == DECISION_REQUIRES_REMEDIATION,
        },
        "preflight_summary": pf,
        "m56a_context": {
            "context_status": m56a_ctx,
            "gating_status": M56A_GATING_NOT_A_GATE,
            "warning": (
                "M56A watchability context is observation-only and not benchmark evidence."
            ),
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_NEXT,
            "route_status": ROUTE_STATUS,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Future evaluation remains separately chartered.",
        },
    }


def _decision_reason(decision: str, blocked: list[str]) -> str:
    if blocked:
        return blocked[0]
    if decision == DECISION_READY:
        return "M55 preflight was ready, canonical anchors matched, and claim flags remained false."
    return decision


def _preflight_summary_all_false() -> dict[str, Any]:
    return {
        "package_identity_valid": False,
        "upstream_m54_anchor_valid": False,
        "candidate_identity_valid": False,
        "required_metadata_present": False,
        "private_boundary_preserved": False,
        "claim_flags_honest": False,
    }


def _preflight_summary_ok() -> dict[str, Any]:
    return {
        "package_identity_valid": True,
        "upstream_m54_anchor_valid": True,
        "candidate_identity_valid": True,
        "required_metadata_present": True,
        "private_boundary_preserved": True,
        "claim_flags_honest": True,
    }


def _preflight_summary_blocked() -> dict[str, Any]:
    return _preflight_summary_all_false()


def _preflight_summary_partial(
    *,
    m54_ok: bool = False,
    m53_ok: bool = False,
    cand_ok: bool | None = None,
) -> dict[str, Any]:
    if cand_ok is None:
        cand_ok = m53_ok and m54_ok
    return {
        "package_identity_valid": m54_ok,
        "upstream_m54_anchor_valid": m54_ok,
        "candidate_identity_valid": cand_ok,
        "required_metadata_present": m54_ok,
        "private_boundary_preserved": True,
        "claim_flags_honest": True,
    }


def _finalize_readout_from_state(
    *,
    m55: dict[str, Any],
    m55_digest: str,
    decision: str,
    blocked: list[str],
    warnings: list[str],
    preflight_summary: dict[str, Any],
    exp_m54: str,
    exp_m53: str,
    exp_cand: str,
    m53_obs: str,
    cand_obs: str,
    m56a_ctx: str,
    m56a_note: str | None,
) -> dict[str, Any]:
    requires_rem = decision in (
        DECISION_REQUIRES_REMEDIATION,
        DECISION_BLOCKED_M55_NOT_READY,
    )
    warn_note = "M56A watchability context is observation-only and not benchmark evidence." + (
        f" {m56a_note}" if m56a_note else ""
    )
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "input_bindings": {
            "m55_preflight_artifact_sha256": m55_digest,
            "m55_contract_id": CONTRACT_ID_M55,
            "m55_preflight_status": str(m55.get("preflight_status") or ""),
            "m54_package_sha256": exp_m54,
            "m53_run_artifact_sha256": exp_m53,
            "candidate_checkpoint_sha256": exp_cand,
            "m53_observed_from_m54_readiness": m53_obs or None,
            "candidate_observed_from_m54_readiness": cand_obs or None,
            "m56a_context_sha256": None,
        },
        "readout": {
            "decision_status": decision,
            "decision_reason": _decision_reason(decision, blocked),
            "blocked_reasons": list(blocked),
            "warnings": list(warnings),
            "requires_remediation": requires_rem,
        },
        "preflight_summary": preflight_summary,
        "m56a_context": {
            "context_status": m56a_ctx,
            "gating_status": M56A_GATING_NOT_A_GATE,
            "warning": warn_note,
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_NEXT,
            "route_status": ROUTE_STATUS,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Future evaluation remains separately chartered.",
        },
    }


def build_fixture_readout_decision() -> dict[str, Any]:
    m55_body = build_fixture_preflight()
    m55_sealed = seal_m55_body(cast(dict[str, Any], redact_paths_in_value(m55_body)))
    m55_d = str(m55_sealed.get(DIGEST_FIELD) or "").strip().lower()
    warnings = [WARNING_M56A_ABSENT]
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_FIXTURE_CI,
        "input_bindings": {
            "m55_preflight_artifact_sha256": m55_d,
            "m55_contract_id": CONTRACT_ID_M55,
            "m55_preflight_status": M55_STATUS_READY,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m56a_context_sha256": None,
        },
        "readout": {
            "decision_status": DECISION_READY,
            "decision_reason": "fixture_ci deterministic readout; canonical anchors synthesized.",
            "blocked_reasons": [],
            "warnings": warnings,
            "requires_remediation": False,
        },
        "preflight_summary": _preflight_summary_ok(),
        "m56a_context": {
            "context_status": M56A_CONTEXT_ABSENT,
            "gating_status": M56A_GATING_NOT_A_GATE,
            "warning": (
                "M56A watchability context is observation-only and not benchmark evidence."
            ),
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_NEXT,
            "route_status": ROUTE_STATUS,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Future evaluation remains separately chartered.",
        },
    }


@dataclass(frozen=True)
class OperatorDeclaredReadoutInputs:
    declared_readout_json: Path
    m55_preflight_json: Path
    expected_candidate_sha256: str


def _declared_overclaim(obj: Any) -> bool:
    keys_exec = frozenset(
        (
            "evaluation_executed",
            "benchmark_passed",
            "benchmark_execution_performed",
            "benchmark_pass_fail_emitted",
            "checkpoint_promoted",
            "strength_evaluated",
            "v2_authorized",
            "torch_load_invoked",
            "checkpoint_blob_loaded",
            "live_sc2_executed",
            "gpu_inference_executed",
            "xai_executed",
            "human_panel_executed",
        ),
    )
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys_exec and v is True:
                return True
            if k == "claim_flags" and isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 in keys_exec and v2 is True:
                        return True
                    if k2 in DEFAULT_CLAIM_FLAGS and v2 is True:
                        return True
            elif _declared_overclaim(v):
                return True
    elif isinstance(obj, list):
        return any(_declared_overclaim(x) for x in obj)
    return False


def build_operator_declared_readout_decision(
    inputs: OperatorDeclaredReadoutInputs,
) -> dict[str, Any]:
    warnings: list[str] = []
    blocked: list[str] = []
    try:
        decl_txt = inputs.declared_readout_json.read_text(encoding="utf-8")
    except OSError:
        blocked.append(DECISION_BLOCKED_INVALID_M55_CONTRACT)
        return _declared_blocked_stub(blocked, warnings)

    br = _boundary_violation_reason(decl_txt)
    if br:
        blocked.append(DECISION_BLOCKED_PRIVATE_BOUNDARY)
        return _declared_blocked_stub(blocked, warnings)

    try:
        declared = json.loads(decl_txt)
    except json.JSONDecodeError:
        blocked.append(DECISION_BLOCKED_INVALID_M55_CONTRACT)
        return _declared_blocked_stub(blocked, warnings)
    if not isinstance(declared, dict):
        blocked.append(DECISION_BLOCKED_INVALID_M55_CONTRACT)
        return _declared_blocked_stub(blocked, warnings)

    if _declared_overclaim(declared):
        blocked.append(DECISION_BLOCKED_CLAIM_FLAGS)
        return _declared_blocked_stub(blocked, warnings)

    exp_c = validate_sha256(inputs.expected_candidate_sha256)
    if exp_c is None:
        blocked.append(DECISION_BLOCKED_CANDIDATE_MISMATCH)
        return _declared_blocked_stub(blocked, warnings)

    try:
        m55 = load_m55_preflight(inputs.m55_preflight_json.resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        blocked.append(DECISION_BLOCKED_INVALID_M55_CONTRACT)
        return _declared_blocked_stub(blocked, warnings)

    if m55_claim_flags_violation(m55):
        blocked.append(DECISION_BLOCKED_CLAIM_FLAGS)
        return _declared_blocked_stub(blocked, warnings)

    if str(m55.get("preflight_status") or "") != M55_STATUS_READY:
        blocked.append(DECISION_BLOCKED_M55_NOT_READY)
        return _declared_blocked_stub(blocked, warnings)

    m55_d = str(m55.get(DIGEST_FIELD) or "").strip().lower()
    decl_cand = str(declared.get("declared_candidate_checkpoint_sha256") or "").strip().lower()
    if decl_cand != exp_c:
        blocked.append(DECISION_BLOCKED_CANDIDATE_MISMATCH)
        return _declared_blocked_stub(blocked, warnings)

    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_DECLARED,
        "input_bindings": {
            "m55_preflight_artifact_sha256": m55_d,
            "m55_contract_id": CONTRACT_ID_M55,
            "m55_preflight_status": str(m55.get("preflight_status") or ""),
            "m54_package_sha256": m55_upstream_m54_sha(m55),
            "m53_run_artifact_sha256": None,
            "candidate_checkpoint_sha256": exp_c,
            "m56a_context_sha256": None,
            "declared_readout_fields_acknowledged": sorted(declared.keys()),
        },
        "readout": {
            "decision_status": DECISION_READY,
            "decision_reason": "operator_declared metadata validated; M55 remained ready.",
            "blocked_reasons": [],
            "warnings": warnings,
            "requires_remediation": False,
        },
        "preflight_summary": _preflight_summary_ok(),
        "m56a_context": {
            "context_status": M56A_CONTEXT_ABSENT,
            "gating_status": M56A_GATING_NOT_A_GATE,
            "warning": (
                "M56A watchability context is observation-only and not benchmark evidence."
            ),
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_NEXT,
            "route_status": ROUTE_STATUS,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Future evaluation remains separately chartered.",
        },
    }


def _declared_blocked_stub(blocked: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_OPERATOR_DECLARED,
        "input_bindings": {
            "m55_preflight_artifact_sha256": None,
            "m55_contract_id": CONTRACT_ID_M55,
            "m55_preflight_status": "",
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m56a_context_sha256": None,
        },
        "readout": {
            "decision_status": blocked[0] if blocked else DECISION_BLOCKED_INVALID_M55_CONTRACT,
            "decision_reason": blocked[0] if blocked else "",
            "blocked_reasons": list(blocked),
            "warnings": list(warnings),
            "requires_remediation": False,
        },
        "preflight_summary": _preflight_summary_blocked(),
        "m56a_context": {
            "context_status": M56A_CONTEXT_ABSENT,
            "gating_status": M56A_GATING_NOT_A_GATE,
            "warning": (
                "M56A watchability context is observation-only and not benchmark evidence."
            ),
        },
        "claim_flags": _claim_template(),
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_NEXT,
            "route_status": ROUTE_STATUS,
            "recommended_next_milestone": RECOMMENDED_NEXT_MILESTONE,
            "recommended_next_title": RECOMMENDED_NEXT_TITLE,
            "route_note": "Future evaluation remains separately chartered.",
        },
    }


def build_readout_report(*, sealed: dict[str, Any]) -> dict[str, Any]:
    ro = sealed.get("readout") or {}
    dst = str(ro.get("decision_status") or "") if isinstance(ro, dict) else ""
    summ = str(ro.get("decision_reason") or "") if isinstance(ro, dict) else ""
    br = ro.get("blocked_reasons") if isinstance(ro, dict) else []
    wr = ro.get("warnings") if isinstance(ro, dict) else []
    if not isinstance(br, list):
        br = []
    if not isinstance(wr, list):
        wr = []
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "decision_status": dst,
        "summary": summ or f"M56 readout status: {dst}.",
        "strongest_allowed_claim": STRONGEST_ALLOWED,
        "non_claims": list(NON_CLAIMS),
        "blocked_reasons": [str(x) for x in br],
        "warnings": [str(x) for x in wr],
        "next_recommended_step": RECOMMENDED_NEXT_TITLE,
    }


def build_readout_checklist(*, sealed: dict[str, Any]) -> str:
    ro = sealed.get("readout") or {}
    ds = str(ro.get("decision_status") or "") if isinstance(ro, dict) else ""
    lines = [
        "# V15-M56 — Bounded evaluation package readout decision checklist",
        "",
        f"- **Decision status:** `{ds}`",
        "",
        "## Gates",
        "",
        "- [ ] R0 — M55 preflight JSON present",
        "- [ ] R1 — M55 contract id valid",
        "- [ ] R2 — M55 artifact seal valid",
        "- [ ] R3 — M55 preflight status read",
        "- [ ] R4 — M54 canonical package SHA matches",
        "- [ ] R5 — M53 run artifact SHA matches",
        "- [ ] R6 — candidate checkpoint SHA matches latest produced candidate",
        "- [ ] R7 — private/public boundary preserved",
        "- [ ] R8 — claim flags remain false",
        "- [ ] R9 — M56A context classified as non-gating",
        "- [ ] R10 — route recommendation is recommended_not_executed",
        "",
    ]
    return "\n".join(lines) + "\n"


def write_readout_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, Path, Path]]:
    sealed = seal_m56_body(cast(dict[str, Any], redact_paths_in_value(body_unsealed)))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_readout_report(sealed=sealed)
    chk = build_readout_checklist(sealed=sealed)

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M56 emission leaked path patterns")
    return sealed, (p_main, p_rep, p_chk)


__all__ = [
    "OperatorDeclaredReadoutInputs",
    "OperatorPreflightReadoutInputs",
    "build_fixture_readout_decision",
    "build_operator_declared_readout_decision",
    "build_operator_preflight_readout_decision",
    "build_readout_checklist",
    "build_readout_report",
    "classify_m56a_context",
    "load_m55_preflight",
    "seal_m56_body",
    "verify_m55_artifact_seal",
    "write_readout_artifacts",
]
