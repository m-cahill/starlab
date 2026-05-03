"""V15-M56A — visual watchability confirmation builders and artifact writers."""

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
from starlab.v15.m51_live_candidate_watchability_harness_models import CONTRACT_ID_M51
from starlab.v15.m52_candidate_live_adapter_spike_models import CONTRACT_ID_M52A
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    CONTRACT_ID_M53,
    PROFILE_M53,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_models import CONTRACT_ID_M54
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    CONTRACT_ID as CONTRACT_ID_M55,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    STATUS_READY as M55_STATUS_READY,
)
from starlab.v15.m56a_latest_candidate_visual_watchability_confirmation_models import (
    ADAPTER_BLOCKED,
    ADAPTER_MISSING,
    ADAPTER_NOT_USED,
    ADAPTER_OPERATOR_DECLARED,
    CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
    CANONICAL_M53_RUN_ARTIFACT_SHA256,
    CANONICAL_M54_PACKAGE_SHA256,
    CHECKLIST_FILENAME,
    CONTRACT_ID,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE,
    EVIDENCE_CONTRACT_DECLARED,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE,
    MODE_FIXTURE_CI,
    MODE_OPERATOR_DECLARED,
    MODE_OPERATOR_LOCAL,
    MODE_OPERATOR_PREFLIGHT,
    NON_CLAIMS,
    POLICY_BLOCKED,
    POLICY_CANDIDATE_LIVE,
    POLICY_FIXTURE,
    POLICY_SCAFFOLD,
    PROFILE_FIXTURE_CI,
    PROFILE_M56A,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL,
    PROFILE_OPERATOR_PREFLIGHT,
    REASON_BLOCKED_CANDIDATE_MISMATCH,
    REASON_BLOCKED_CLAIM_VIOLATION,
    REASON_BLOCKED_M53_MISMATCH,
    REASON_BLOCKED_M54_MISMATCH,
    REASON_BLOCKED_M55_CONTRACT,
    REASON_BLOCKED_M55_NOT_READY,
    REASON_BLOCKED_MISSING_M55,
    REASON_BLOCKED_PRIVATE_BOUNDARY,
    REASON_BLOCKED_WATCHABILITY_PATH,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    ROUTE_M56_READOUT,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    SCHEMA_VERSION,
    STATUS_BLOCKED_ADAPTER,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED,
    STATUS_PREFLIGHT_READY,
    STATUS_SCAFFOLD_CONFIRMED,
    STATUS_VISUAL_CONFIRMED_WARNINGS,
    STRONGEST_ALLOWED_DEFAULT,
    STRONGEST_ALLOWED_OPERATOR_DECLARED_LIVE,
    STRONGEST_ALLOWED_SCAFFOLD,
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


def _seal_ok(obj: dict[str, Any], *, digest_field: str = DIGEST_FIELD) -> bool:
    seal_in = obj.get(digest_field)
    if seal_in is None:
        return False
    wo = {k: v for k, v in obj.items() if k != digest_field}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _m55_upstream_m54_sha(m55: dict[str, Any]) -> str:
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


def _load_m55(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(REASON_BLOCKED_MISSING_M55)
    raw = _parse_json_object(path.resolve())
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M55:
        raise ValueError(REASON_BLOCKED_M55_CONTRACT)
    if not _seal_ok(raw):
        raise ValueError(REASON_BLOCKED_M55_CONTRACT)
    return raw


def _boundary_violation_reason(raw_text: str) -> str | None:
    low = raw_text.lower()
    if "company_secrets" in low:
        return REASON_BLOCKED_PRIVATE_BOUNDARY
    if _PATH_OUT_SEGMENT.search(raw_text):
        return REASON_BLOCKED_PRIVATE_BOUNDARY
    if emission_has_private_path_patterns(raw_text):
        return REASON_BLOCKED_PRIVATE_BOUNDARY
    return None


def _validate_m54_file(path: Path, *, expected_sha: str) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(REASON_BLOCKED_M54_MISMATCH)
    raw_txt = path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        raise ValueError(br)
    m54 = _parse_json_object(path.resolve())
    if str(m54.get("contract_id") or "") != CONTRACT_ID_M54:
        raise ValueError(REASON_BLOCKED_M54_MISMATCH)
    if not _seal_ok(m54):
        raise ValueError(REASON_BLOCKED_M54_MISMATCH)
    got = str(m54.get(DIGEST_FIELD) or "").strip().lower()
    if got != expected_sha.lower():
        raise ValueError(REASON_BLOCKED_M54_MISMATCH)
    return m54


def _validate_m53_file(path: Path, *, expected_sha: str) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(REASON_BLOCKED_M53_MISMATCH)
    raw_txt = path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        raise ValueError(br)
    m53 = _parse_json_object(path.resolve())
    if str(m53.get("contract_id") or "") != CONTRACT_ID_M53:
        raise ValueError(REASON_BLOCKED_M53_MISMATCH)
    if str(m53.get("profile_id") or "") != PROFILE_M53:
        raise ValueError(REASON_BLOCKED_M53_MISMATCH)
    if not _seal_ok(m53):
        raise ValueError(REASON_BLOCKED_M53_MISMATCH)
    got = str(m53.get(DIGEST_FIELD) or "").strip().lower()
    if got != expected_sha.lower():
        raise ValueError(REASON_BLOCKED_M53_MISMATCH)
    return m53


def _validate_m51_file(path: Path) -> str:
    if not path.is_file():
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    raw_txt = path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        raise ValueError(br)
    m51 = _parse_json_object(path.resolve())
    if str(m51.get("contract_id") or "") != CONTRACT_ID_M51:
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    if not _seal_ok(m51):
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    return sha256_file_hex(path.resolve())


def _validate_m52a_file(path: Path) -> str:
    if not path.is_file():
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    raw_txt = path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        raise ValueError(br)
    m52a = _parse_json_object(path.resolve())
    if str(m52a.get("contract_id") or "") != CONTRACT_ID_M52A:
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    if not _seal_ok(m52a):
        raise ValueError(REASON_BLOCKED_WATCHABILITY_PATH)
    return sha256_file_hex(path.resolve())


def seal_m56a_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def _claim_flags_template() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def _has_true_m56a_claim(obj: Any) -> bool:
    keys = frozenset(DEFAULT_CLAIM_FLAGS.keys())
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and v is True:
                return True
            if k == "claim_flags" and isinstance(v, dict):
                if _has_true_m56a_claim(v):
                    return True
            elif _has_true_m56a_claim(v):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if _has_true_m56a_claim(item):
                return True
    return False


def _m54_produced_candidate_sha(m54: dict[str, Any]) -> str:
    ccb = m54.get("candidate_checkpoint_binding") or {}
    if not isinstance(ccb, dict):
        return ""
    return str(ccb.get("produced_candidate_checkpoint_sha256") or "").strip().lower()


def build_fixture_confirmation() -> dict[str, Any]:
    return _finalize_body(
        profile=PROFILE_FIXTURE_CI,
        mode=MODE_FIXTURE_CI,
        policy_source=POLICY_FIXTURE,
        adapter_status=ADAPTER_NOT_USED,
        visual_status=STATUS_FIXTURE_ONLY,
        blocked_reasons=(),
        warnings=(),
        input_bindings={
            "m55_preflight_sha256": None,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m51_watchability_json_sha256": None,
            "m52a_adapter_spike_json_sha256": None,
        },
        operator_observation=_operator_observation_fixture(),
        artifact_references=_artifact_refs_empty(),
        claim_flags=_claim_flags_template(),
    )


def _operator_observation_fixture() -> dict[str, Any]:
    return {
        "live_sc2_executed": False,
        "replay_saved": False,
        "video_metadata_supplied": False,
        "watchability_notes_supplied": False,
        "observed_action_count": None,
        "observed_duration_seconds": None,
        "observed_final_status": None,
        "sc2_game_result": None,
    }


def _artifact_refs_empty() -> dict[str, Any]:
    return {
        "replay_binding_sha256": None,
        "replay_file_reference": None,
        "video_metadata_reference": None,
        "watchability_run_json_sha256": None,
    }


def _finalize_body(
    *,
    profile: str,
    mode: str,
    policy_source: str,
    adapter_status: str,
    visual_status: str,
    blocked_reasons: tuple[str, ...],
    warnings: tuple[str, ...],
    input_bindings: dict[str, Any],
    operator_observation: dict[str, Any],
    artifact_references: dict[str, Any],
    claim_flags: dict[str, bool],
) -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M56A,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": profile,
        "blocked_reasons": list(blocked_reasons),
        "warnings": list(warnings),
        "input_bindings": input_bindings,
        "watchability_profile": {
            "mode": mode,
            "policy_source": policy_source,
            "candidate_policy_adapter_status": adapter_status,
            "visual_confirmation_status": visual_status,
        },
        "operator_observation": operator_observation,
        "artifact_references": artifact_references,
        "claim_flags": claim_flags,
        "non_claims": list(NON_CLAIMS),
        "route_recommendation": {
            "route": ROUTE_M56_READOUT,
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
    }


@dataclass(frozen=True)
class PreflightInputs:
    m55_preflight_json: Path
    m54_package_json: Path
    m53_run_json: Path
    expected_m54_package_sha256: str
    expected_candidate_sha256: str
    m51_watchability_json: Path | None
    m52a_adapter_spike_json: Path | None


def build_operator_preflight_confirmation(inputs: PreflightInputs) -> dict[str, Any]:
    blocked: list[str] = []
    warns: list[str] = []

    try:
        m55 = _load_m55(inputs.m55_preflight_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        r = str(exc)
        if r in (REASON_BLOCKED_MISSING_M55, REASON_BLOCKED_M55_CONTRACT):
            blocked.append(r)
        else:
            blocked.append(REASON_BLOCKED_M55_CONTRACT)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=None,
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    if str(m55.get("preflight_status") or "") != M55_STATUS_READY:
        blocked.append(REASON_BLOCKED_M55_NOT_READY)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    m55_upstream = _m55_upstream_m54_sha(m55)
    exp54 = validate_sha256(inputs.expected_m54_package_sha256)
    exp_cand = validate_sha256(inputs.expected_candidate_sha256)
    if exp54 is None or exp_cand is None:
        blocked.append(REASON_BLOCKED_M54_MISMATCH)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    if m55_upstream != exp54 or exp54 != CANONICAL_M54_PACKAGE_SHA256.lower():
        blocked.append(REASON_BLOCKED_M54_MISMATCH)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    try:
        m54 = _validate_m54_file(inputs.m54_package_json, expected_sha=exp54)
    except ValueError as exc:
        blocked.append(str(exc))
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    produced = _m54_produced_candidate_sha(m54)
    if produced != exp_cand or exp_cand != CANONICAL_CANDIDATE_CHECKPOINT_SHA256.lower():
        blocked.append(REASON_BLOCKED_CANDIDATE_MISMATCH)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    try:
        _validate_m53_file(
            inputs.m53_run_json,
            expected_sha=CANONICAL_M53_RUN_ARTIFACT_SHA256,
        )
    except ValueError as exc:
        blocked.append(str(exc))
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    m51_digest: str | None = None
    m52a_digest: str | None = None
    if inputs.m51_watchability_json is None and inputs.m52a_adapter_spike_json is None:
        blocked.append(REASON_BLOCKED_WATCHABILITY_PATH)
        return _blocked_preflight_body(
            blocked=tuple(blocked),
            warnings=tuple(warns),
            input_bindings_partial=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
        )

    if inputs.m51_watchability_json is not None:
        try:
            m51_digest = _validate_m51_file(inputs.m51_watchability_json)
        except ValueError as exc:
            blocked.append(str(exc))
            return _blocked_preflight_body(
                blocked=tuple(blocked),
                warnings=tuple(warns),
                input_bindings_partial=_bindings_partial_for_failure(
                    m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                    m51_sha=None,
                    m52a_sha=None,
                ),
            )

    if inputs.m52a_adapter_spike_json is not None:
        try:
            m52a_digest = _validate_m52a_file(inputs.m52a_adapter_spike_json)
        except ValueError as exc:
            blocked.append(str(exc))
            return _blocked_preflight_body(
                blocked=tuple(blocked),
                warnings=tuple(warns),
                input_bindings_partial=_bindings_partial_for_failure(
                    m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                    m51_sha=m51_digest,
                    m52a_sha=None,
                ),
            )

    if m52a_digest:
        policy = POLICY_CANDIDATE_LIVE
        warns.append("m52a_records_candidate_live_adapter_spike_not_trained_policy_proof")
    else:
        policy = POLICY_SCAFFOLD
        warns.append("m51_scaffold_watchability_only_real_candidate_adapter_missing")

    m55_sha = sha256_file_hex(inputs.m55_preflight_json.resolve())

    return _finalize_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        mode=MODE_OPERATOR_PREFLIGHT,
        policy_source=policy,
        adapter_status=ADAPTER_MISSING,
        visual_status=STATUS_PREFLIGHT_READY,
        blocked_reasons=(),
        warnings=tuple(warns),
        input_bindings={
            "m55_preflight_sha256": m55_sha,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m51_watchability_json_sha256": m51_digest,
            "m52a_adapter_spike_json_sha256": m52a_digest,
        },
        operator_observation=_operator_observation_fixture(),
        artifact_references=_artifact_refs_empty(),
        claim_flags=_claim_flags_template(),
    )


def _bindings_partial_for_failure(
    *,
    m55_sha: str | None,
    m51_sha: str | None,
    m52a_sha: str | None,
) -> dict[str, Any]:
    return {
        "m55_preflight_sha256": m55_sha,
        "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
        "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
        "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
        "m51_watchability_json_sha256": m51_sha,
        "m52a_adapter_spike_json_sha256": m52a_sha,
    }


def _blocked_preflight_body(
    *,
    blocked: tuple[str, ...],
    warnings: tuple[str, ...],
    input_bindings_partial: dict[str, Any],
) -> dict[str, Any]:
    return _finalize_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        mode=MODE_OPERATOR_PREFLIGHT,
        policy_source=POLICY_BLOCKED,
        adapter_status=ADAPTER_BLOCKED,
        visual_status=STATUS_PREFLIGHT_BLOCKED,
        blocked_reasons=blocked,
        warnings=warnings,
        input_bindings=input_bindings_partial,
        operator_observation=_operator_observation_fixture(),
        artifact_references=_artifact_refs_empty(),
        claim_flags=_claim_flags_template(),
    )


@dataclass(frozen=True)
class DeclaredInputs:
    watchability_evidence_json: Path
    m55_preflight_json: Path
    expected_candidate_sha256: str


def build_operator_declared_confirmation(inputs: DeclaredInputs) -> dict[str, Any]:
    exp = validate_sha256(inputs.expected_candidate_sha256)
    if exp is None:
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CANDIDATE_MISMATCH,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=None,
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    try:
        m55 = _load_m55(inputs.m55_preflight_json)
    except (OSError, ValueError, json.JSONDecodeError):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_M55_CONTRACT,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=None,
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    if str(m55.get("preflight_status") or "") != M55_STATUS_READY:
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_M55_NOT_READY,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    ev_path = inputs.watchability_evidence_json
    if not ev_path.is_file():
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_WATCHABILITY_PATH,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    raw_txt = ev_path.read_text(encoding="utf-8")
    br = _boundary_violation_reason(raw_txt)
    if br:
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(br,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    try:
        ev = _parse_json_object(ev_path.resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    cid = str(ev.get("contract_id") or "")
    if cid != EVIDENCE_CONTRACT_DECLARED:
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    if _has_true_m56a_claim(ev):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    declared_ckpt = str(ev.get("declared_candidate_checkpoint_sha256") or "").strip().lower()
    if declared_ckpt != exp:
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CANDIDATE_MISMATCH,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    policy = str(ev.get("policy_source") or "")
    if policy not in (POLICY_SCAFFOLD, POLICY_CANDIDATE_LIVE):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    live = ev.get("live_sc2_executed")
    if not isinstance(live, bool):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    if policy == POLICY_CANDIDATE_LIVE:
        visual = STATUS_VISUAL_CONFIRMED_WARNINGS
        adapter_st = ADAPTER_OPERATOR_DECLARED
        warns: tuple[str, ...] = (
            "operator_declared_candidate_live_adapter attest_must_be_operator_true",
        )
        strongest_note = STRONGEST_ALLOWED_OPERATOR_DECLARED_LIVE
    else:
        visual = STATUS_SCAFFOLD_CONFIRMED
        adapter_st = ADAPTER_MISSING
        warns = ("operator_declared_scaffold_policy_not_trained_candidate",)
        strongest_note = STRONGEST_ALLOWED_SCAFFOLD

    replay_b = ev.get("replay_saved")
    video_m = ev.get("video_metadata_supplied")
    notes = ev.get("watchability_notes_supplied")
    if (
        not isinstance(replay_b, bool)
        or not isinstance(video_m, bool)
        or not isinstance(
            notes,
            bool,
        )
    ):
        return _finalize_body(
            profile=PROFILE_OPERATOR_DECLARED,
            mode=MODE_OPERATOR_DECLARED,
            policy_source=POLICY_BLOCKED,
            adapter_status=ADAPTER_BLOCKED,
            visual_status=STATUS_PREFLIGHT_BLOCKED,
            blocked_reasons=(REASON_BLOCKED_CLAIM_VIOLATION,),
            warnings=(),
            input_bindings=_bindings_partial_for_failure(
                m55_sha=sha256_file_hex(inputs.m55_preflight_json.resolve()),
                m51_sha=None,
                m52a_sha=None,
            ),
            operator_observation=_operator_observation_fixture(),
            artifact_references=_artifact_refs_empty(),
            claim_flags=_claim_flags_template(),
        )

    op_obs = {
        "live_sc2_executed": live,
        "replay_saved": replay_b,
        "video_metadata_supplied": video_m,
        "watchability_notes_supplied": notes,
        "observed_action_count": ev.get("observed_action_count"),
        "observed_duration_seconds": ev.get("observed_duration_seconds"),
        "observed_final_status": ev.get("observed_final_status"),
        "sc2_game_result": ev.get("sc2_game_result"),
    }
    art_ref = {
        "replay_binding_sha256": ev.get("replay_binding_sha256"),
        "replay_file_reference": ev.get("replay_file_reference"),
        "video_metadata_reference": ev.get("video_metadata_reference"),
        "watchability_run_json_sha256": ev.get("watchability_run_json_sha256"),
    }

    m55_sha = sha256_file_hex(inputs.m55_preflight_json.resolve())

    body = _finalize_body(
        profile=PROFILE_OPERATOR_DECLARED,
        mode=MODE_OPERATOR_DECLARED,
        policy_source=policy,
        adapter_status=adapter_st,
        visual_status=visual,
        blocked_reasons=(),
        warnings=warns,
        input_bindings={
            "m55_preflight_sha256": m55_sha,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m51_watchability_json_sha256": None,
            "m52a_adapter_spike_json_sha256": None,
        },
        operator_observation=op_obs,
        artifact_references=art_ref,
        claim_flags=_claim_flags_template(),
    )
    body["_strongest_allowed_override"] = strongest_note
    return body


def build_runner_stub_scaffold_confirmation(
    *,
    m55_preflight_sha256: str | None,
) -> dict[str, Any]:
    warns = (
        "m56a_runner_stub_live_sc2_not_invoked",
        "invoke_starlab.v15.run_v15_m51_live_candidate_watchability_harness_for_live_sc2",
    )
    return _finalize_body(
        profile=PROFILE_OPERATOR_LOCAL,
        mode=MODE_OPERATOR_LOCAL,
        policy_source=POLICY_SCAFFOLD,
        adapter_status=ADAPTER_MISSING,
        visual_status=STATUS_VISUAL_CONFIRMED_WARNINGS,
        blocked_reasons=(),
        warnings=warns,
        input_bindings={
            "m55_preflight_sha256": m55_preflight_sha256,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m51_watchability_json_sha256": None,
            "m52a_adapter_spike_json_sha256": None,
        },
        operator_observation=_operator_observation_fixture(),
        artifact_references=_artifact_refs_empty(),
        claim_flags=_claim_flags_template(),
    )


def build_runner_refused_missing_adapter(*, m55_preflight_sha256: str | None) -> dict[str, Any]:
    return _finalize_body(
        profile=PROFILE_OPERATOR_LOCAL,
        mode=MODE_OPERATOR_LOCAL,
        policy_source=POLICY_BLOCKED,
        adapter_status=ADAPTER_MISSING,
        visual_status=STATUS_BLOCKED_ADAPTER,
        blocked_reasons=("watchability_blocked_missing_candidate_live_policy_adapter",),
        warnings=(),
        input_bindings={
            "m55_preflight_sha256": m55_preflight_sha256,
            "m54_package_sha256": CANONICAL_M54_PACKAGE_SHA256,
            "m53_run_artifact_sha256": CANONICAL_M53_RUN_ARTIFACT_SHA256,
            "candidate_checkpoint_sha256": CANONICAL_CANDIDATE_CHECKPOINT_SHA256,
            "m51_watchability_json_sha256": None,
            "m52a_adapter_spike_json_sha256": None,
        },
        operator_observation=_operator_observation_fixture(),
        artifact_references=_artifact_refs_empty(),
        claim_flags=_claim_flags_template(),
    )


def build_confirmation_report(*, sealed: dict[str, Any]) -> dict[str, Any]:
    wp = sealed.get("watchability_profile") or {}
    visual = str(wp.get("visual_confirmation_status") or "")
    mode = str(wp.get("mode") or "")
    blocked = list(sealed.get("blocked_reasons") or [])
    warns = list(sealed.get("warnings") or [])
    summary = (
        f"Visual watchability confirmation status: {visual}. "
        f"This is observation evidence only, not benchmark execution."
    )
    if blocked:
        summary = f"Watchability confirmation blocked: {', '.join(blocked)}."
    override = sealed.get("_strongest_allowed_override")
    if override is not None:
        strongest = str(override)
    elif visual == STATUS_SCAFFOLD_CONFIRMED:
        strongest = STRONGEST_ALLOWED_SCAFFOLD
    elif visual == STATUS_VISUAL_CONFIRMED_WARNINGS and mode == MODE_OPERATOR_LOCAL:
        strongest = STRONGEST_ALLOWED_SCAFFOLD
    else:
        strongest = STRONGEST_ALLOWED_DEFAULT
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "visual_confirmation_status": visual,
        "summary": summary,
        "strongest_allowed_claim": strongest,
        "blocked_reasons": blocked,
        "warnings": warns,
        "checklist_summary": [
            "W0 — M55 preflight binding present",
            "W1 — M54 package anchor matches canonical SHA",
            "W2 — candidate checkpoint identity matches V15-M53/V15-M54 produced checkpoint",
            "W3 — watchability policy source declared",
            "W4 — candidate-live adapter status declared",
            "W5 — replay save status declared",
            "W6 — optional video metadata declared or explicitly absent",
            "W7 — public/private boundary preserved",
            "W8 — all non-visual claim flags false",
            "W9 — route recommendation remains recommended_not_executed",
        ],
        "next_recommended_step": "V15-M56_bounded_evaluation_package_readout_decision",
    }


def build_confirmation_checklist_md(*, sealed: dict[str, Any]) -> str:
    wp = sealed.get("watchability_profile") or {}
    visual = str(wp.get("visual_confirmation_status") or "")
    br = sealed.get("blocked_reasons") or []
    warns = sealed.get("warnings") or []
    lines = [
        "# V15-M56A — Latest candidate visual watchability confirmation checklist",
        "",
        f"**Milestone:** {MILESTONE}",
        f"**Visual confirmation status:** `{visual}`",
        "",
        "## Gates",
        "",
        "- [ ] **W0** — M55 preflight binding present",
        "- [ ] **W1** — M54 package anchor matches canonical SHA",
        "- [ ] **W2** — Candidate checkpoint identity matches V15-M53/V15-M54 produced checkpoint",
        "- [ ] **W3** — Watchability policy source declared",
        "- [ ] **W4** — Candidate-live adapter status declared",
        "- [ ] **W5** — Replay save status declared",
        "- [ ] **W6** — Optional video metadata declared or explicitly absent",
        "- [ ] **W7** — Public/private boundary preserved",
        "- [ ] **W8** — All non-visual claim flags false",
        "- [ ] **W9** — Route recommendation remains `recommended_not_executed`",
        "",
    ]
    if br:
        lines.extend(["## Blocked reasons", ""])
        for x in br:
            lines.append(f"- `{x}`")
        lines.append("")
    if warns:
        lines.extend(["## Warnings", ""])
        for x in warns:
            lines.append(f"- `{x}`")
        lines.append("")
    lines.extend(
        [
            "## Non-claims",
            "",
        ]
    )
    for nc in NON_CLAIMS:
        lines.append(f"- {nc}")
    lines.append("")
    return "\n".join(lines)


def write_confirmation_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, Path, Path]]:
    # Preserve internal override for report (strip before seal)
    strongest_override = body_unsealed.get("_strongest_allowed_override")
    body_for_seal = {k: v for k, v in body_unsealed.items() if not k.startswith("_")}
    sealed = seal_m56a_body(cast(dict[str, Any], redact_paths_in_value(body_for_seal)))
    output_dir.mkdir(parents=True, exist_ok=True)

    if strongest_override is not None:
        sealed_read = dict(sealed)
        sealed_read["_strongest_allowed_override"] = strongest_override
    else:
        sealed_read = sealed

    rep = build_confirmation_report(sealed=sealed_read)
    if strongest_override:
        rep["strongest_allowed_claim"] = str(strongest_override)

    chk = build_confirmation_checklist_md(sealed=sealed_read)

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M56A emission leaked path patterns")
    return sealed, (p_main, p_rep, p_chk)


def emit_forbidden_refusal(
    output_dir: Path, *, flags: list[str]
) -> tuple[dict[str, Any], tuple[Path, Path, Path]]:
    body = build_fixture_confirmation()
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["blocked_reasons"] = [f"forbidden_cli_flag:{','.join(sorted(flags))}"]
    body["watchability_profile"] = {
        "mode": MODE_OPERATOR_PREFLIGHT,
        "policy_source": POLICY_BLOCKED,
        "candidate_policy_adapter_status": ADAPTER_BLOCKED,
        "visual_confirmation_status": STATUS_PREFLIGHT_BLOCKED,
    }
    return write_confirmation_artifacts(output_dir, body_unsealed=body)


__all__ = [
    "DeclaredInputs",
    "PreflightInputs",
    "build_confirmation_checklist_md",
    "build_confirmation_report",
    "build_fixture_confirmation",
    "build_operator_declared_confirmation",
    "build_operator_preflight_confirmation",
    "build_runner_refused_missing_adapter",
    "build_runner_stub_scaffold_confirmation",
    "emit_forbidden_refusal",
    "seal_m56a_body",
    "sha256_file_hex",
    "validate_sha256",
    "write_confirmation_artifacts",
]
