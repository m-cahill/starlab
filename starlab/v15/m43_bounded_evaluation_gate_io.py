"""V15-M43 — bounded evaluation gate (routing only; consumes sealed M42 JSON)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import (
    build_environment_lock_body,
    redact_paths_in_value,
    seal_environment_lock_body,
)
from starlab.v15.environment_lock_models import (
    CONTRACT_ID_LONG_GPU_ENV,
)
from starlab.v15.environment_lock_models import (
    PROFILE_FIXTURE_CI as ENV_PROFILE_FIXTURE_CI,
)
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_io import (
    _claim_flags_all_false_m42,
    seal_m42_body,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_io import (
    _gate_pack as m42_gate_pack,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    ANCHOR_M39_RECEIPT_SHA256,
    EMITTER_MODULE_M42,
    MILESTONE_LABEL_M42,
    SOURCE_CANDIDATE_LINEAGE_SHA256,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    CONTRACT_ID_EVAL_PACKAGE_FAMILY as M42_CONTRACT_ID,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M42DigestField,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    PROFILE_M42 as M42_PROFILE_ID,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    PROFILE_OPERATOR_PREFLIGHT as M42_PROFILE_OPERATOR_PREFLIGHT,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    SCHEMA_VERSION as M42_SCHEMA_VERSION,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_READY as M42_STATUS_READY,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    STATUS_READY_WARNINGS as M42_STATUS_READY_WARNINGS,
)
from starlab.v15.m43_bounded_evaluation_gate_models import (
    CONTRACT_ID_BOUNDED_EVAL_GATE,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M42_FILENAME_MAIN_CANONICAL,
    MILESTONE_LABEL_M43,
    NON_CLAIMS_M43,
    PROFILE_FIXTURE_CI,
    PROFILE_GATE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_BENCHMARK_PROTOCOL_MISSING,
    REFUSED_BENCHMARK_PROTOCOL_NOT_ALLOWED,
    REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY,
    REFUSED_CHECKPOINT_IDENTITY_MISSING,
    REFUSED_DISALLOWED_EXECUTION_REQUEST,
    REFUSED_ENVIRONMENT_PREREQUISITE_MISSING,
    REFUSED_INVALID_M42_PACKAGE,
    REFUSED_M42_PACKAGE_NOT_READY,
    REFUSED_MISSING_M42_PACKAGE,
    REPORT_FILENAME,
    ROUTE_ID_FUTURE_BOUNDED,
    ROUTE_STATUS_DECLARED_NOT_EXECUTED,
    SCHEMA_VERSION,
    STATUS_GATE_NOT_READY,
    STATUS_GATE_READY,
    STATUS_GATE_READY_WITH_WARNINGS,
)
from starlab.v15.strong_agent_scorecard_io import (
    build_strong_agent_scorecard_body_fixture,
    seal_strong_agent_scorecard_body,
)
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
    SEAL_KEY_STRONG_AGENT,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_ENV_SEAL_KEY: Final[str] = "long_gpu_environment_lock_sha256"

FIXTURE_M41_ARTIFACT_SHA256: Final[str] = "f" * 64

FILENAME_FIXTURE_PROTOCOL: Final[str] = "v15_m43_fixture_benchmark_protocol.json"
FILENAME_FIXTURE_ENV: Final[str] = "v15_m43_fixture_environment_manifest.json"

REDACTED_M42_PATH: Final[str] = "redacted:fixture_bundle"


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _canonical_seal_ok_m42(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(M42DigestField)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != M42DigestField}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _canonical_seal_ok_scorecard(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(SEAL_KEY_STRONG_AGENT)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != SEAL_KEY_STRONG_AGENT}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _canonical_seal_ok_env(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(_ENV_SEAL_KEY)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != _ENV_SEAL_KEY}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def validate_scorecard_protocol_routing(scorecard: dict[str, Any]) -> str | None:
    """Return refusal code if invalid; None if accepted as routing metadata."""
    if str(scorecard.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        return REFUSED_BENCHMARK_PROTOCOL_NOT_ALLOWED
    if str(scorecard.get("protocol_profile_id", "")) != PROTOCOL_PROFILE_ID:
        return REFUSED_BENCHMARK_PROTOCOL_NOT_ALLOWED
    if not _canonical_seal_ok_scorecard(scorecard):
        return REFUSED_BENCHMARK_PROTOCOL_NOT_ALLOWED
    return None


def validate_environment_manifest_routing(env: dict[str, Any]) -> str | None:
    if str(env.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_ENV:
        return REFUSED_ENVIRONMENT_PREREQUISITE_MISSING
    if not _canonical_seal_ok_env(env):
        return REFUSED_ENVIRONMENT_PREREQUISITE_MISSING
    return None


def build_synthetic_m42_package_ready_unsealed() -> dict[str, Any]:
    """Deterministic M42-shaped body (pre-seal) with clean ready status for M43 fixture paths."""
    gates = m42_gate_pack(
        p0=True,
        p1=True,
        p2=True,
        p3=True,
        p4=True,
        p5=True,
        p6=True,
        p7=True,
        p8=True,
        p9=True,
        p10=True,
    )
    src = SOURCE_CANDIDATE_LINEAGE_SHA256
    fin = ANCHOR_FINAL_CANDIDATE_SHA256
    return {
        "schema_version": M42_SCHEMA_VERSION,
        "contract_id": M42_CONTRACT_ID,
        "package_profile_id": M42_PROFILE_ID,
        "profile": M42_PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M42,
        "emitter_module": EMITTER_MODULE_M42,
        "package_status": M42_STATUS_READY,
        "evaluation_package_ready": True,
        "expected_m41_package_sha256_status": "verified_match",
        "upstream_bindings": {
            "m41_two_hour_run_package": {
                "artifact_sha256": FIXTURE_M41_ARTIFACT_SHA256,
                "contract_id": "starlab.v15.two_hour_run_package_evaluation_readiness.v1",
                "profile_id": "starlab.v15.m41.two_hour_run_package_evaluation_readiness.v1",
                "package_status": "package_ready_for_future_evaluation",
            },
            "m39_two_hour_run_receipt": {
                "artifact_sha256": ANCHOR_M39_RECEIPT_SHA256,
                "run_status": "two_hour_operator_run_completed_with_candidate_checkpoint",
                "full_wall_clock_satisfied": True,
            },
            "m05_scorecard_protocol": {"binding_status": "optional_not_supplied"},
        },
        "candidate_checkpoint": {
            "source_candidate_sha256": src,
            "final_candidate_sha256": fin,
            "candidate_role": "final_two_hour_candidate_checkpoint",
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_blob_loaded": False,
            "torch_load_performed": False,
            "checkpoint_file_sha256_verified": False,
            "final_checkpoint_file_binding": None,
        },
        "run_summary": {
            "target_wall_clock_seconds": 7200,
            "full_wall_clock_satisfied": True,
            "training_update_count": 0,
            "sc2_backed_features_used": False,
        },
        "evidence_bindings": {
            "telemetry_summary_bound": True,
            "checkpoint_inventory_bound": True,
            "transcript_metadata_bound": True,
            "retention_counters_bound": True,
        },
        "evaluation_routing": {
            "ready_for_m43_bounded_evaluation_gate": True,
            "recommended_next": "V15-M43_bounded_evaluation_gate_for_two_hour_candidate",
            "blocked_reasons": [],
        },
        "gates": gates,
        "claim_flags": _claim_flags_all_false_m42(),
        "non_claims": [
            "not_benchmark_pass",
            "not_strength_evaluation",
            "not_checkpoint_promotion",
        ],
        "cross_check_hints": {},
    }


def build_fixture_benchmark_protocol_sealed() -> dict[str, Any]:
    raw = build_strong_agent_scorecard_body_fixture()
    return seal_strong_agent_scorecard_body(raw)


def build_fixture_environment_manifest_sealed() -> dict[str, Any]:
    body = build_environment_lock_body(ENV_PROFILE_FIXTURE_CI)
    return seal_environment_lock_body(body)


def _default_route() -> dict[str, Any]:
    return {
        "route_id": ROUTE_ID_FUTURE_BOUNDED,
        "route_status": ROUTE_STATUS_DECLARED_NOT_EXECUTED,
        "allowed_future_profiles": [
            "fixture_ci_preflight",
            "operator_local_bounded_eval",
        ],
        "disallowed_now": [
            "benchmark_execution",
            "live_sc2_execution",
            "human_panel_execution",
            "checkpoint_promotion",
        ],
    }


def _m42_candidate_summary(m42: dict[str, Any]) -> dict[str, Any]:
    st = str(m42.get("package_status") or "")
    digest = str(m42.get(M42DigestField) or "").lower()
    fc = m42.get("candidate_checkpoint") or {}
    fc = fc if isinstance(fc, dict) else {}
    fin = str(fc.get("final_candidate_sha256") or "").lower()
    promo = str(fc.get("promotion_status") or "")
    nw = m42.get("noncritical_warnings")
    warn_list = list(nw) if isinstance(nw, list) else []
    out: dict[str, Any] = {
        "status": st,
        "sha256": digest if _is_hex64(digest) else None,
        "candidate_final_sha256": fin if _is_hex64(fin) else None,
        "candidate_source_sha256": str(fc.get("source_candidate_sha256") or "").lower()
        if _is_hex64(str(fc.get("source_candidate_sha256") or ""))
        else None,
        "candidate_posture": promo or "ambiguous",
        "upstream_m41_artifact_sha256": str(
            (
                (((m42.get("upstream_bindings") or {}).get("m41_two_hour_run_package")) or {}).get(
                    "artifact_sha256"
                )
            )
            or "",
        ).lower(),
    }
    if warn_list:
        out["m42_noncritical_warnings"] = list(warn_list)
    return cast(dict[str, Any], redact_paths_in_value(out))


def structural_m42_issues(m42: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if str(m42.get("contract_id", "")) != M42_CONTRACT_ID:
        errs.append("m42_contract_id_mismatch")
    if str(m42.get("package_profile_id", "")) != M42_PROFILE_ID:
        errs.append("m42_package_profile_id_mismatch")
    if not _canonical_seal_ok_m42(m42):
        errs.append("m42_seal_invalid")
    return errs


def candidate_identity_issues(m42: dict[str, Any]) -> list[str]:
    fc = m42.get("candidate_checkpoint") or {}
    if not isinstance(fc, dict):
        return ["candidate_checkpoint_missing"]
    src = str(fc.get("source_candidate_sha256") or "").strip().lower()
    fin = str(fc.get("final_candidate_sha256") or "").strip().lower()
    errs: list[str] = []
    if not _is_hex64(src):
        errs.append("source_candidate_sha_missing")
    if not _is_hex64(fin):
        errs.append("final_candidate_sha_missing")
    promo = str(fc.get("promotion_status") or "")
    blob = fc.get("checkpoint_blob_loaded") is True
    torch_l = fc.get("torch_load_performed") is True
    if promo != "not_promoted_candidate_only" or blob or torch_l:
        errs.append("candidate_not_candidate_only")
    return errs


def _strict_protocol_env(
    protocol: dict[str, Any],
    env: dict[str, Any],
    _pr: Any,
    _ref: Any,
) -> None:
    p_reason = validate_scorecard_protocol_routing(protocol)
    if p_reason:
        _pr("benchmark_protocol", "invalid", p_reason)
        _ref(p_reason, "benchmark_protocol_contract_or_seal_invalid")
    else:
        _pr("benchmark_protocol", "satisfied")
    e_reason = validate_environment_manifest_routing(env)
    if e_reason:
        _pr("environment_manifest", "invalid", e_reason)
        _ref(e_reason, "environment_manifest_contract_or_seal_invalid")
    else:
        _pr("environment_manifest", "satisfied")


def decide_gate(
    *,
    profile: str,
    m42: dict[str, Any] | None,
    protocol: dict[str, Any] | None,
    env: dict[str, Any] | None,
    m42_path_for_prereq: str | None,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Return gate_status, prerequisites, refusals, route."""
    prereqs: list[dict[str, Any]] = []
    refusals: list[dict[str, Any]] = []
    route = _default_route()

    def _pr(pid: str, status: str, detail: str | None = None) -> None:
        row: dict[str, Any] = {"prerequisite_id": pid, "status": status}
        if detail:
            row["detail"] = detail
        prereqs.append(row)

    def _ref(code: str, detail: str) -> None:
        refusals.append({"code": code, "detail": detail})

    if m42 is None:
        _pr("m42_package", "missing", m42_path_for_prereq)
        _ref(REFUSED_MISSING_M42_PACKAGE, "m42_package_json_missing_or_unreadable")
        return REFUSED_MISSING_M42_PACKAGE, prereqs, refusals, route

    struct = structural_m42_issues(m42)
    if struct:
        _pr("m42_structure", "invalid", ",".join(struct))
        _ref(REFUSED_INVALID_M42_PACKAGE, ",".join(struct))
        return REFUSED_INVALID_M42_PACKAGE, prereqs, refusals, route

    _pr("m42_package", "satisfied")

    pst = str(m42.get("package_status") or "")
    id_issues = candidate_identity_issues(m42)
    if id_issues:
        for iss in id_issues:
            if iss == "candidate_not_candidate_only":
                _ref(REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY, iss)
            else:
                _ref(REFUSED_CHECKPOINT_IDENTITY_MISSING, iss)
        codes_out = {r["code"] for r in refusals}
        primary = (
            REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY
            if REFUSED_CANDIDATE_NOT_CANDIDATE_ONLY in codes_out
            else REFUSED_CHECKPOINT_IDENTITY_MISSING
        )
        return primary, prereqs, refusals, route

    nw = m42.get("noncritical_warnings")
    warn_list = [str(x) for x in nw] if isinstance(nw, list) else []

    def _routing_prereqs_protocol_env() -> None:
        nonlocal protocol, env
        if profile in (PROFILE_FIXTURE_CI, PROFILE_OPERATOR_PREFLIGHT):
            assert protocol is not None and env is not None
            _strict_protocol_env(protocol, env, _pr, _ref)
            return
        if profile == PROFILE_OPERATOR_DECLARED:
            if protocol is None:
                _pr("benchmark_protocol", "missing")
                _ref(REFUSED_BENCHMARK_PROTOCOL_MISSING, "operator_declared_missing_protocol")
            else:
                p_reason = validate_scorecard_protocol_routing(protocol)
                if p_reason:
                    _pr("benchmark_protocol", "invalid", p_reason)
                    _ref(p_reason, "benchmark_protocol_contract_or_seal_invalid")
                else:
                    _pr("benchmark_protocol", "satisfied")
            if env is None:
                _pr("environment_manifest", "missing")
                _ref(
                    REFUSED_ENVIRONMENT_PREREQUISITE_MISSING,
                    "operator_declared_missing_environment_manifest",
                )
            else:
                e_reason = validate_environment_manifest_routing(env)
                if e_reason:
                    _pr("environment_manifest", "invalid", e_reason)
                    _ref(e_reason, "environment_manifest_contract_or_seal_invalid")
                else:
                    _pr("environment_manifest", "satisfied")

    if profile == PROFILE_FIXTURE_CI:
        if pst == M42_STATUS_READY:
            _routing_prereqs_protocol_env()
            if refusals:
                return STATUS_GATE_NOT_READY, prereqs, refusals, route
            return STATUS_GATE_READY, prereqs, refusals, route
        if pst == M42_STATUS_READY_WARNINGS:
            _ref(REFUSED_M42_PACKAGE_NOT_READY, "fixture_ci_rejects_m42_warnings_status")
            _pr("m42_clean_ready_status", "refused_non_clean_m42_ready")
            return REFUSED_M42_PACKAGE_NOT_READY, prereqs, refusals, route
        _ref(REFUSED_M42_PACKAGE_NOT_READY, f"m42_package_status_not_ready:{pst}")
        return REFUSED_M42_PACKAGE_NOT_READY, prereqs, refusals, route

    if profile == PROFILE_OPERATOR_PREFLIGHT:
        if pst != M42_STATUS_READY:
            _ref(REFUSED_M42_PACKAGE_NOT_READY, f"m42_status:{pst}")
            return REFUSED_M42_PACKAGE_NOT_READY, prereqs, refusals, route
        assert protocol is not None and env is not None
        _routing_prereqs_protocol_env()
        if refusals:
            return STATUS_GATE_NOT_READY, prereqs, refusals, route
        return STATUS_GATE_READY, prereqs, refusals, route

    assert profile == PROFILE_OPERATOR_DECLARED
    if pst == M42_STATUS_READY:
        _routing_prereqs_protocol_env()
        if refusals:
            return STATUS_GATE_NOT_READY, prereqs, refusals, route
        return STATUS_GATE_READY, prereqs, refusals, route

    if pst == M42_STATUS_READY_WARNINGS:
        if not warn_list:
            _ref(REFUSED_M42_PACKAGE_NOT_READY, "m42_warnings_status_without_warnings_list")
            return REFUSED_M42_PACKAGE_NOT_READY, prereqs, refusals, route
        _routing_prereqs_protocol_env()
        if refusals:
            return STATUS_GATE_NOT_READY, prereqs, refusals, route
        return STATUS_GATE_READY_WITH_WARNINGS, prereqs, refusals, route

    _ref(REFUSED_M42_PACKAGE_NOT_READY, f"m42_status:{pst}")
    return REFUSED_M42_PACKAGE_NOT_READY, prereqs, refusals, route


def seal_m43_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m43_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_bounded_evaluation_gate_report",
        "report_version": "m43",
        "milestone": MILESTONE_LABEL_M43,
        "contract_id": CONTRACT_ID_BOUNDED_EVAL_GATE,
        "gate_profile_id": PROFILE_GATE,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "gate_status": sealed.get("gate_status"),
        "evaluation_executed": sealed.get("evaluation_executed"),
        "checkpoint_loaded": sealed.get("checkpoint_loaded"),
        "promotion_decision_made": sealed.get("promotion_decision_made"),
    }


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M43 emission leaked path patterns into public artifacts")


def emit_m43_disallowed_execution(
    output_dir: Path,
    *,
    profile: str,
    triggered_flags: list[str],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    """Emit gate outcome when forbidden execution-like CLI flags are present."""
    output_dir.mkdir(parents=True, exist_ok=True)
    route = _default_route()
    flags_sorted = sorted(triggered_flags)
    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_BOUNDED_EVAL_GATE,
        "gate_profile_id": PROFILE_GATE,
        "milestone": MILESTONE_LABEL_M43,
        "profile": profile,
        "gate_status": REFUSED_DISALLOWED_EXECUTION_REQUEST,
        "evaluation_executed": False,
        "checkpoint_loaded": False,
        "promotion_decision_made": False,
        "m42_package_path_logical": "redacted:disallowed_execution_request",
        "m42_package_basename": None,
        "disallowed_execution_cli_flags_seen": flags_sorted,
        "m42_package": {
            "status": None,
            "candidate_posture": "unknown",
        },
        "route": route,
        "prerequisites": [
            {
                "prerequisite_id": "disallowed_execution_request",
                "status": "refused",
                "detail": "forbidden_cli_flags",
            },
        ],
        "refusals": [
            {
                "code": REFUSED_DISALLOWED_EXECUTION_REQUEST,
                "detail": "forbidden_cli_flags:" + ",".join(flags_sorted),
            },
        ],
        "non_claims": list(NON_CLAIMS_M43),
    }
    sealed = seal_m43_body(redact_paths_in_value(body_pre))
    rep = build_m43_report(sealed)
    p_gate = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_gate.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep)
    _assert_no_path_leak(blob)
    return sealed, (p_gate, p_rep)


def emit_m43_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    m42_unsealed = build_synthetic_m42_package_ready_unsealed()
    m42_sealed = seal_m42_body(redact_paths_in_value(m42_unsealed))
    proto = redact_paths_in_value(build_fixture_benchmark_protocol_sealed())
    env = redact_paths_in_value(build_fixture_environment_manifest_sealed())

    p_m42 = output_dir / M42_FILENAME_MAIN_CANONICAL
    p_proto = output_dir / FILENAME_FIXTURE_PROTOCOL
    p_env = output_dir / FILENAME_FIXTURE_ENV

    p_m42.write_text(canonical_json_dumps(m42_sealed), encoding="utf-8")
    p_proto.write_text(canonical_json_dumps(proto), encoding="utf-8")
    p_env.write_text(canonical_json_dumps(env), encoding="utf-8")

    m42_plain = json.loads(p_m42.read_text(encoding="utf-8"))
    proto_plain = json.loads(p_proto.read_text(encoding="utf-8"))
    env_plain = json.loads(p_env.read_text(encoding="utf-8"))

    st, prereqs, refusals, route = decide_gate(
        profile=PROFILE_FIXTURE_CI,
        m42=m42_plain,
        protocol=proto_plain,
        env=env_plain,
        m42_path_for_prereq=str(p_m42),
    )
    summary = _m42_candidate_summary(m42_plain)
    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_BOUNDED_EVAL_GATE,
        "gate_profile_id": PROFILE_GATE,
        "milestone": MILESTONE_LABEL_M43,
        "profile": PROFILE_FIXTURE_CI,
        "gate_status": st,
        "evaluation_executed": False,
        "checkpoint_loaded": False,
        "promotion_decision_made": False,
        "m42_package_path_logical": REDACTED_M42_PATH,
        "m42_package_basename": M42_FILENAME_MAIN_CANONICAL,
        "m42_fixture_companion_basenames": {
            "benchmark_protocol": FILENAME_FIXTURE_PROTOCOL,
            "environment_manifest": FILENAME_FIXTURE_ENV,
        },
        "m42_package": summary,
        "route": route,
        "prerequisites": prereqs,
        "refusals": refusals,
        "non_claims": list(NON_CLAIMS_M43),
    }
    sealed = seal_m43_body(redact_paths_in_value(body_pre))
    rep = build_m43_report(sealed)
    p_gate = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_gate.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep)
    _assert_no_path_leak(blob)
    return sealed, (p_m42, p_proto, p_env, p_gate, p_rep)


def _optional_protocol_env_paths(
    profile: str,
    benchmark_protocol_path: Path | None,
    environment_manifest_path: Path | None,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        assert benchmark_protocol_path is not None
        assert environment_manifest_path is not None
        return (
            _parse_json_object(Path(benchmark_protocol_path).resolve()),
            _parse_json_object(Path(environment_manifest_path).resolve()),
        )
    if profile == PROFILE_OPERATOR_DECLARED:
        proto = (
            _parse_json_object(Path(benchmark_protocol_path).resolve())
            if benchmark_protocol_path is not None and Path(benchmark_protocol_path).is_file()
            else None
        )
        env = (
            _parse_json_object(Path(environment_manifest_path).resolve())
            if environment_manifest_path is not None and Path(environment_manifest_path).is_file()
            else None
        )
        return proto, env
    return None, None


def emit_m43_operator(
    output_dir: Path,
    *,
    profile: str,
    m42_package_path: Path,
    benchmark_protocol_path: Path | None,
    environment_manifest_path: Path | None,
    operator_logical_m42_hint: str | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    rp = Path(m42_package_path).resolve()
    if rp.is_file():
        try:
            m42_plain = _parse_json_object(rp)
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError) as e:
            raise ValueError(f"m42_package_invalid_json:{e}") from e
    else:
        m42_plain = None

    proto_plain, env_plain = _optional_protocol_env_paths(
        profile,
        benchmark_protocol_path,
        environment_manifest_path,
    )

    path_hint = str(rp.name) if rp.is_file() else str(m42_package_path)
    st, prereqs, refusals, route = decide_gate(
        profile=profile,
        m42=m42_plain,
        protocol=proto_plain,
        env=env_plain,
        m42_path_for_prereq=str(redact_paths_in_value(path_hint)),
    )
    logical_path = operator_logical_m42_hint or (str(rp) if rp.is_file() else str(m42_package_path))
    summary = (
        _m42_candidate_summary(m42_plain)
        if m42_plain is not None
        else redact_paths_in_value(
            {
                "status": None,
                "sha256": None,
                "candidate_final_sha256": None,
                "candidate_source_sha256": None,
                "candidate_posture": "unknown",
                "upstream_m41_artifact_sha256": None,
            },
        )
    )
    body_pre: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_BOUNDED_EVAL_GATE,
        "gate_profile_id": PROFILE_GATE,
        "milestone": MILESTONE_LABEL_M43,
        "profile": profile,
        "gate_status": st,
        "evaluation_executed": False,
        "checkpoint_loaded": False,
        "promotion_decision_made": False,
        "m42_package_path_logical": redact_paths_in_value(logical_path),
        "m42_package_basename": rp.name,
        "m42_package": summary,
        "route": route,
        "prerequisites": prereqs,
        "refusals": refusals,
        "non_claims": list(NON_CLAIMS_M43),
    }
    if profile == PROFILE_OPERATOR_PREFLIGHT and proto_plain is not None and env_plain is not None:
        body_pre["routing_metadata_sha256_only"] = {
            "benchmark_protocol_artifact_sha256": sha256_hex_of_canonical_json(proto_plain),
            "environment_manifest_artifact_sha256": sha256_hex_of_canonical_json(env_plain),
        }
    elif proto_plain is not None:
        body_pre.setdefault("routing_metadata_sha256_only", {})[
            "benchmark_protocol_artifact_sha256"
        ] = sha256_hex_of_canonical_json(proto_plain)
    if env_plain is not None and profile == PROFILE_OPERATOR_DECLARED:
        body_pre.setdefault("routing_metadata_sha256_only", {})[
            "environment_manifest_artifact_sha256"
        ] = sha256_hex_of_canonical_json(env_plain)

    sealed = seal_m43_body(redact_paths_in_value(body_pre))
    rep = build_m43_report(sealed)
    output_dir.mkdir(parents=True, exist_ok=True)
    p_gate = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_gate.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep)
    _assert_no_path_leak(blob)
    return sealed, (p_gate, p_rep)


# --- Typed input surface (serialized into gate body indirectly via emit paths) ---
@dataclass(frozen=True)
class M43GatePrerequisite:
    prerequisite_id: str
    status: str
    detail: str | None = None


@dataclass(frozen=True)
class M43Refusal:
    code: str
    detail: str


@dataclass(frozen=True)
class M43EvaluationRoute:
    route_id: str
    route_status: str
    allowed_future_profiles: tuple[str, ...]
    disallowed_now: tuple[str, ...]


@dataclass(frozen=True)
class M43GateInput:
    profile: str
    m42_package_json: Path | None
    benchmark_protocol_json: Path | None
    environment_manifest_json: Path | None


@dataclass(frozen=True)
class M43GateDecision:
    gate_status: str
    evaluation_executed: bool
    checkpoint_loaded: bool
    promotion_decision_made: bool


@dataclass(frozen=True)
class M43GateReport:
    gate_status: str
    artifact_sha256: str
    refusals: tuple[M43Refusal, ...]


__all__ = [
    "M43EvaluationRoute",
    "M43GateDecision",
    "M43GatePrerequisite",
    "M43GateReport",
    "M43Refusal",
    "FILENAME_FIXTURE_ENV",
    "FILENAME_FIXTURE_PROTOCOL",
    "M42_FILENAME_MAIN_CANONICAL",
    "build_fixture_benchmark_protocol_sealed",
    "build_fixture_environment_manifest_sealed",
    "build_synthetic_m42_package_ready_unsealed",
    "decide_gate",
    "emit_m43_disallowed_execution",
    "emit_m43_operator",
    "seal_m43_body",
]
