"""V15-M35: smoke benchmark readiness over sealed M33 (and optional M05) JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    CONTRACT_ID_M33_PROBE,
    PROFILE_M33_PROBE,
    STATUS_PROBE_COMPLETED,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M35_READINESS,
    EMITTER_MODULE_M35,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE_LABEL_M35,
    NON_CLAIMS_M35,
    PROFILE_FIXTURE_CI,
    PROFILE_M35_READINESS,
    PROFILE_OPERATOR_PREFLIGHT,
    READINESS_SCOPE,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    STATUS_BLOCKED_INVALID_M33,
    STATUS_BLOCKED_M05,
    STATUS_BLOCKED_MISSING_M33,
    STATUS_BLOCKED_NOT_CUDA,
    STATUS_BLOCKED_SHA_MISMATCH,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
)
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    SEAL_KEY_STRONG_AGENT,
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


def _canonical_seal_ok(raw: dict[str, Any], *, seal_key: str) -> bool:
    seal_in = raw.get(seal_key)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != seal_key}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def load_m33_cuda_probe_json(path: Path) -> dict[str, Any]:
    return _parse_json_object(path)


def validate_m33_probe_sealed(m33: dict[str, Any]) -> bool:
    return _canonical_seal_ok(m33, seal_key=GATE_ARTIFACT_DIGEST_FIELD)


def validate_m05_scorecard_sealed(m05: dict[str, Any]) -> bool:
    if str(m05.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        return False
    if not _canonical_seal_ok(m05, seal_key=SEAL_KEY_STRONG_AGENT):
        return False
    if m05.get("benchmark_execution_performed") is not False:
        return False
    if m05.get("strong_agent_claim_authorized") is not False:
        return False
    return True


def _claim_flags_all_false() -> dict[str, bool]:
    return {
        "benchmark_execution_performed": False,
        "benchmark_passed": False,
        "scorecard_execution_performed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_authorized": False,
        "t3_authorized": False,
    }


def _m33_probe_digest(m33: dict[str, Any]) -> str:
    return str(m33.get(GATE_ARTIFACT_DIGEST_FIELD) or "").lower()


def _m05_digest(m05: dict[str, Any] | None) -> str | None:
    if m05 is None:
        return None
    wo = {k: v for k, v in m05.items() if k != SEAL_KEY_STRONG_AGENT}
    return sha256_hex_of_canonical_json(wo)


def seal_m35_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m35_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_smoke_benchmark_readiness_report",
        "report_version": "m35",
        "milestone": MILESTONE_LABEL_M35,
        "contract_id": CONTRACT_ID_M35_READINESS,
        "profile_id": PROFILE_M35_READINESS,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "readiness_status": sealed.get("readiness_status"),
    }


def build_m35_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("readiness_status", ""))
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
        "# V15-M35 — candidate checkpoint smoke benchmark readiness checklist\n\n"
        f"**`readiness_status`:** `{st}`  \n"
        f"**`readiness_scope`:** `{READINESS_SCOPE}`\n\n"
        "V15-M35 readiness is not benchmark execution; "
        "`smoke_benchmark_ready_for_future_execution` means the M34 CUDA-probed candidate can be "
        "routed into a future smoke benchmark execution surface, not that any benchmark was run "
        "or passed.\n\n"
        "| Gate | Name | Pass |\n"
        "| --- | --- | --- |\n"
        f"{gate_lines}\n"
        "## Non-claims\n\n"
        f"{nc_lines}\n"
    )


def _gate_pack(
    *,
    s0: bool,
    s1: bool,
    s2: bool,
    s3: bool,
    s4: bool,
    s5: bool,
    s6: bool,
) -> list[dict[str, Any]]:
    return [
        {"gate_id": "S0", "name": "M33 probe contract valid", "passed": s0},
        {"gate_id": "S1", "name": "M33 probe completed", "passed": s1},
        {"gate_id": "S2", "name": "Candidate SHA consistent", "passed": s2},
        {"gate_id": "S3", "name": "CUDA probe completed", "passed": s3},
        {"gate_id": "S4", "name": "Optional M05 scorecard protocol posture valid", "passed": s4},
        {"gate_id": "S5", "name": "Public/private boundary preserved", "passed": s5},
        {"gate_id": "S6", "name": "Non-claims preserved (claim flags false)", "passed": s6},
    ]


def build_fixture_m35_body() -> dict[str, Any]:
    gates = _gate_pack(
        s0=False,
        s1=False,
        s2=False,
        s3=False,
        s4=True,
        s5=True,
        s6=True,
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M35_READINESS,
        "profile_id": PROFILE_M35_READINESS,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M35,
        "emitter_module": EMITTER_MODULE_M35,
        "readiness_status": STATUS_FIXTURE_ONLY,
        "readiness_scope": READINESS_SCOPE,
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "candidate_checkpoint": {
            "sha256": "",
            "promotion_status": "not_applicable_fixture",
            "source_posture": "fixture_ci_no_candidate",
        },
        "upstream_bindings": {
            "m33_cuda_probe": {
                "path_redaction_status": "fixture_ci_skipped_no_m33_json",
                "artifact_sha256": "",
                "contract_id": CONTRACT_ID_M33_PROBE,
                "profile_id": PROFILE_M33_PROBE,
                "probe_status": "",
                "device_observed": "",
                "cuda_probe_performed": False,
            },
            "m05_scorecard_protocol": {
                "binding_status": "optional_not_supplied",
                "artifact_sha256": None,
            },
        },
        "smoke_benchmark_requirements": {
            "checkpoint_identity_bound": False,
            "checkpoint_cuda_probe_completed": False,
            "candidate_sha_consistent": False,
            "scorecard_protocol_bound_or_deferred": True,
            "benchmark_execution_performed": False,
            "scorecard_execution_performed": False,
            "strength_evaluated": False,
            "checkpoint_promoted": False,
        },
        "gates": gates,
        "claim_flags": _claim_flags_all_false(),
        "non_claims": list(NON_CLAIMS_M35),
    }


def evaluate_operator_preflight_m35(
    m33: dict[str, Any] | None,
    *,
    expected_candidate_sha256: str | None,
    m05: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build pre-body (before seal) from M33 (+ optional M05)."""
    claim_flags = _claim_flags_all_false()
    exp_arg = str(expected_candidate_sha256 or "").strip().lower() or None

    if m33 is None:
        m05_ok = m05 is None or validate_m05_scorecard_sealed(m05)
        gates = _gate_pack(
            s0=False,
            s1=False,
            s2=False,
            s3=False,
            s4=m05_ok,
            s5=True,
            s6=True,
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_M35_READINESS,
            "profile_id": PROFILE_M35_READINESS,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "milestone": MILESTONE_LABEL_M35,
            "emitter_module": EMITTER_MODULE_M35,
            "readiness_status": STATUS_BLOCKED_MISSING_M33,
            "readiness_scope": READINESS_SCOPE,
            "recommended_next": RECOMMENDED_NEXT_SUCCESS,
            "candidate_checkpoint": {
                "sha256": exp_arg or "",
                "promotion_status": "unknown_missing_m33",
                "source_posture": "m34_cuda_probed_candidate",
            },
            "upstream_bindings": {
                "m33_cuda_probe": {
                    "path_redaction_status": "missing_m33_json",
                    "artifact_sha256": "",
                    "contract_id": CONTRACT_ID_M33_PROBE,
                    "profile_id": PROFILE_M33_PROBE,
                    "probe_status": "",
                    "device_observed": "",
                    "cuda_probe_performed": False,
                },
                "m05_scorecard_protocol": {
                    "binding_status": (
                        "optional_not_supplied"
                        if m05 is None
                        else (
                            "bound_valid" if validate_m05_scorecard_sealed(m05) else "bound_invalid"
                        )
                    ),
                    "artifact_sha256": _m05_digest(m05),
                },
            },
            "smoke_benchmark_requirements": {
                "checkpoint_identity_bound": False,
                "checkpoint_cuda_probe_completed": False,
                "candidate_sha_consistent": False,
                "scorecard_protocol_bound_or_deferred": m05 is None
                or validate_m05_scorecard_sealed(m05),
                "benchmark_execution_performed": False,
                "scorecard_execution_performed": False,
                "strength_evaluated": False,
                "checkpoint_promoted": False,
            },
            "gates": gates,
            "claim_flags": claim_flags,
            "non_claims": list(NON_CLAIMS_M35),
        }

    m05_invalid = m05 is not None and not validate_m05_scorecard_sealed(m05)
    m33_valid = validate_m33_probe_sealed(m33)
    contract_ok = str(m33.get("contract_id", "")) == CONTRACT_ID_M33_PROBE
    profile_ok = str(m33.get("profile", "")) == PROFILE_M33_PROBE
    s0 = m33_valid and contract_ok and profile_ok

    probe_st = str(m33.get("probe_status") or "")
    s1 = s0 and probe_st == STATUS_PROBE_COMPLETED

    cand_sha = str(m33.get("candidate_checkpoint_sha256") or "").strip().lower()
    if exp_arg is None:
        exp_eff = cand_sha
    else:
        exp_eff = exp_arg
    s2 = s1 and _is_hex64(cand_sha) and _is_hex64(exp_eff) and cand_sha == exp_eff

    dev = str(m33.get("device_observed") or "").lower()
    cuda_done = m33.get("cuda_probe_performed") is True
    s3 = s2 and dev == "cuda" and cuda_done

    s4 = not m05_invalid
    s5 = True
    s6 = all(not v for v in claim_flags.values())

    if m05_invalid:
        status = STATUS_BLOCKED_M05
    elif not s0:
        status = STATUS_BLOCKED_INVALID_M33
    elif not s1:
        status = STATUS_BLOCKED_INVALID_M33
    elif not s2:
        status = STATUS_BLOCKED_SHA_MISMATCH
    elif not s3:
        status = STATUS_BLOCKED_NOT_CUDA
    else:
        status = STATUS_READY

    m05_binding = {
        "binding_status": (
            "optional_not_supplied"
            if m05 is None
            else ("bound_valid" if validate_m05_scorecard_sealed(m05) else "bound_invalid")
        ),
        "artifact_sha256": _m05_digest(m05),
    }

    requirements = {
        "checkpoint_identity_bound": s0 and _is_hex64(cand_sha),
        "checkpoint_cuda_probe_completed": s3,
        "candidate_sha_consistent": s2,
        "scorecard_protocol_bound_or_deferred": m05 is None or validate_m05_scorecard_sealed(m05),
        "benchmark_execution_performed": False,
        "scorecard_execution_performed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M35_READINESS,
        "profile_id": PROFILE_M35_READINESS,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M35,
        "emitter_module": EMITTER_MODULE_M35,
        "readiness_status": status,
        "readiness_scope": READINESS_SCOPE,
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        "candidate_checkpoint": {
            "sha256": cand_sha if _is_hex64(cand_sha) else "",
            "promotion_status": str(
                m33.get("candidate_checkpoint_promotion_status") or "not_promoted_candidate_only",
            ),
            "source_posture": "m34_cuda_probed_candidate",
        },
        "upstream_bindings": {
            "m33_cuda_probe": {
                "path_redaction_status": "redacted_or_not_recorded",
                "artifact_sha256": _m33_probe_digest(m33),
                "contract_id": CONTRACT_ID_M33_PROBE,
                "profile_id": PROFILE_M33_PROBE,
                "probe_status": probe_st,
                "device_observed": str(m33.get("device_observed") or ""),
                "cuda_probe_performed": bool(m33.get("cuda_probe_performed") is True),
            },
            "m05_scorecard_protocol": m05_binding,
        },
        "smoke_benchmark_requirements": requirements,
        "gates": _gate_pack(s0=s0, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6),
        "claim_flags": claim_flags,
        "non_claims": list(NON_CLAIMS_M35),
    }


def emit_m35_readiness_fixture(output_dir: Path) -> tuple[dict[str, Any], Path, Path, Path]:
    body_pre = build_fixture_m35_body()
    sealed = seal_m35_body(redact_paths_in_value(body_pre))
    if not isinstance(sealed, dict):
        raise TypeError("expected dict")

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    rep = build_m35_report(sealed)
    chk = build_m35_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M35 fixture emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk


def emit_m35_readiness_operator_preflight(
    output_dir: Path,
    *,
    m33_path: Path | None,
    expected_candidate_sha256: str | None = None,
    m05_path: Path | None = None,
) -> tuple[dict[str, Any], Path, Path, Path]:
    m33: dict[str, Any] | None = None
    if m33_path is not None and m33_path.is_file():
        m33 = load_m33_cuda_probe_json(m33_path)

    m05: dict[str, Any] | None = None
    if m05_path is not None and m05_path.is_file():
        m05 = _parse_json_object(m05_path)

    body_pre = evaluate_operator_preflight_m35(
        m33,
        expected_candidate_sha256=expected_candidate_sha256,
        m05=m05,
    )
    red = redact_paths_in_value(body_pre)
    if not isinstance(red, dict):
        raise TypeError("expected dict")
    sealed = seal_m35_body(red)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    rep = build_m35_report(sealed)
    chk = build_m35_checklist_md(sealed)

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M35 operator_preflight emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk
