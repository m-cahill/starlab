"""V15-M55 — bounded evaluation package preflight IO / builder logic."""

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
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    ALLOWED_NEXT_STEP,
    CANONICAL_UPSTREAM_M54_PACKAGE_ID,
    CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
    CHECK_ID_CLAIM_HYGIENE,
    CHECK_ID_MANIFEST_COMPLETE,
    CHECK_ID_PACKAGE_IDENTITY,
    CHECK_ID_PATH_HYGIENE,
    CHECK_ID_READOUT_READY,
    CHECK_ID_UPSTREAM_CLOSURE,
    CONTRACT_ID,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    FIXTURE_CANDIDATE_IDENTITY_SHA256,
    FIXTURE_EVALUATION_MANIFEST_SHA256,
    FIXTURE_PACKAGE_ID,
    FIXTURE_SCORECARD_READOUT_PLAN_SHA256,
    GATE_ARTIFACT_DIGEST_FIELD,
    MILESTONE,
    NON_CLAIMS,
    PREFLIGHT_ID_FIXTURE,
    PROFILE_FIXTURE_CI,
    PROFILE_M55,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REASON_CANDIDATE_FILE_MISSING,
    REASON_CLAIM_FLAG_TRUE,
    REASON_COMPANY_SECRETS_REF,
    REASON_INVALID_SHA256_FORMAT,
    REASON_MANIFEST_FILE_MISSING,
    REASON_MISSING_OPERATOR_ARG,
    REASON_OUT_PATH_REF,
    REASON_PACKAGE_SHA_MISMATCH,
    REASON_SCORECARD_FILE_MISSING,
    REASON_UPSTREAM_MISMATCH,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SOURCE_KIND_FIXTURE,
    SOURCE_KIND_OPERATOR,
    STATUS_BLOCKED_CLAIM_VIOLATION,
    STATUS_BLOCKED_IDENTITY_MISMATCH,
    STATUS_BLOCKED_INVALID_SHA256,
    STATUS_BLOCKED_MISSING_INPUT,
    STATUS_BLOCKED_PRIVATE_BOUNDARY,
    STATUS_READY,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")
_PATH_OUT_SEGMENT: Final[re.Pattern[str]] = re.compile(
    r"(?:^|[\\/])out(?:[\\/]|$)|[\\/]out[\\/]",
    re.IGNORECASE,
)


def validate_sha256(s: str) -> str | None:
    """Return normalized lowercase hex64, or None if invalid."""

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


def compute_json_sha256_if_path_given(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    return sha256_file_hex(path.resolve())


def evaluation_package_binding_sha256(
    *,
    manifest_sha256: str,
    candidate_sha256: str,
    scorecard_sha256: str,
) -> str:
    binding = {
        "candidate_identity_sha256": candidate_sha256.lower(),
        "evaluation_package_manifest_sha256": manifest_sha256.lower(),
        "scorecard_or_readout_plan_sha256": scorecard_sha256.lower(),
    }
    return sha256_hex_of_canonical_json(binding)


def _check_row(
    check_id: str,
    status: str,
    *,
    reason: str = "",
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": status,
        "reason": reason,
    }


def _claim_flags_template() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def seal_m55_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _boundary_violation_reason(raw_text: str) -> str | None:
    low = raw_text.lower()
    if "company_secrets" in low:
        return REASON_COMPANY_SECRETS_REF
    if _PATH_OUT_SEGMENT.search(raw_text):
        return REASON_OUT_PATH_REF
    if emission_has_private_path_patterns(raw_text):
        return REASON_OUT_PATH_REF
    return None


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def build_preflight_report(*, sealed: dict[str, Any]) -> dict[str, Any]:
    st = str(sealed.get("preflight_status") or "")
    blocked_reasons: list[str] = []
    for row in sealed.get("preflight_checks") or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("status")) != "passed" and str(row.get("reason")):
            blocked_reasons.append(str(row.get("reason")))
    ready = st == STATUS_READY
    summary = (
        "Bounded evaluation package preflight passed; structural readout readiness only."
        if ready
        else f"Bounded evaluation package preflight blocked: {st}."
    )
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "milestone": MILESTONE,
        "preflight_status": st,
        "summary": summary,
        "blocked_reasons": sorted(dict.fromkeys(blocked_reasons)),
        "ready_for_next_step": ready,
        "strongest_allowed_claim": (
            "The declared evaluation package passed bounded preflight checks for "
            "structural readout readiness only."
            if ready
            else "Preflight did not attest readout readiness; refusal reasons are machine-readable."
        ),
        "non_claims": list(NON_CLAIMS),
    }


def write_preflight_artifacts(
    output_dir: Path,
    *,
    body_unsealed: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Path, Path]]:
    sealed = seal_m55_body(cast(dict[str, Any], redact_paths_in_value(body_unsealed)))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_preflight_report(sealed=sealed)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep)
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M55 emission leaked path patterns")
    return sealed, (p_main, p_rep)


def _finalize_body(
    *,
    profile: str,
    preflight_status: str,
    checks: list[dict[str, Any]],
    input_package: dict[str, Any],
    required_inputs: dict[str, str],
    observed_inputs: dict[str, str | None],
    claim_flags: dict[str, bool],
    refusal_suffix: str = "",
) -> dict[str, Any]:
    pf_id = str(input_package.get("package_id") or "")
    preflight_id = f"{pf_id}{refusal_suffix}" if refusal_suffix else pf_id
    return {
        "contract_id": CONTRACT_ID,
        "profile_id": PROFILE_M55,
        "milestone": MILESTONE,
        "emitter_module": EMITTER_MODULE,
        "schema_version": SCHEMA_VERSION,
        "profile": profile,
        "preflight_id": preflight_id,
        "created_at_policy": "deterministic_or_omitted",
        "input_package": input_package,
        "required_inputs": required_inputs,
        "observed_inputs": observed_inputs,
        "preflight_checks": checks,
        "preflight_status": preflight_status,
        "allowed_next_step": ALLOWED_NEXT_STEP,
        "claim_flags": claim_flags,
        "non_claims": list(NON_CLAIMS),
    }


def build_fixture_preflight() -> dict[str, Any]:
    m54_sha = CANONICAL_UPSTREAM_M54_PACKAGE_SHA256
    man = FIXTURE_EVALUATION_MANIFEST_SHA256
    cand = FIXTURE_CANDIDATE_IDENTITY_SHA256
    score = FIXTURE_SCORECARD_READOUT_PLAN_SHA256
    pkg_sha = evaluation_package_binding_sha256(
        manifest_sha256=man,
        candidate_sha256=cand,
        scorecard_sha256=score,
    )
    input_package = {
        "package_id": FIXTURE_PACKAGE_ID,
        "package_sha256": pkg_sha,
        "declared_upstream_m54_package_sha256": m54_sha,
        "declared_upstream_m54_package_id": CANONICAL_UPSTREAM_M54_PACKAGE_ID,
        "source_kind": SOURCE_KIND_FIXTURE,
    }
    required_inputs = {
        "m54_package_sha256": m54_sha,
        "evaluation_package_manifest_sha256": man,
        "candidate_identity_sha256": cand,
        "scorecard_or_readout_plan_sha256": score,
    }
    observed_inputs: dict[str, str | None] = {
        "m54_package_sha256": m54_sha,
        "evaluation_package_manifest_sha256": man,
        "candidate_identity_sha256": cand,
        "scorecard_or_readout_plan_sha256": score,
    }
    checks = [
        _check_row(CHECK_ID_PACKAGE_IDENTITY, "passed"),
        _check_row(CHECK_ID_UPSTREAM_CLOSURE, "passed"),
        _check_row(CHECK_ID_MANIFEST_COMPLETE, "passed"),
        _check_row(CHECK_ID_PATH_HYGIENE, "passed"),
        _check_row(CHECK_ID_CLAIM_HYGIENE, "passed"),
        _check_row(CHECK_ID_READOUT_READY, "passed"),
    ]
    return _finalize_body(
        profile=PROFILE_FIXTURE_CI,
        preflight_status=STATUS_READY,
        checks=checks,
        input_package=input_package,
        required_inputs=required_inputs,
        observed_inputs=observed_inputs,
        claim_flags=_claim_flags_template(),
        refusal_suffix=f"_{PREFLIGHT_ID_FIXTURE}",
    )


@dataclass(frozen=True)
class OperatorDeclaredInputs:
    evaluation_package_id: str
    evaluation_package_sha256: str
    upstream_m54_package_id: str
    upstream_m54_package_sha256: str
    evaluation_package_manifest: Path
    candidate_identity: Path
    scorecard_readout_plan: Path


def build_operator_declared_preflight(inputs: OperatorDeclaredInputs) -> dict[str, Any]:
    problems: list[tuple[str, str, str]] = []

    eid = str(inputs.evaluation_package_id or "").strip()
    exp_pkg = validate_sha256(inputs.evaluation_package_sha256)
    up_m54 = validate_sha256(inputs.upstream_m54_package_sha256)
    up_id = str(inputs.upstream_m54_package_id or "").strip()

    if not eid:
        problems.append(
            (
                CHECK_ID_PACKAGE_IDENTITY,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_MISSING_OPERATOR_ARG,
            ),
        )
    if exp_pkg is None and str(inputs.evaluation_package_sha256 or "").strip():
        problems.append(
            (
                CHECK_ID_PACKAGE_IDENTITY,
                STATUS_BLOCKED_INVALID_SHA256,
                REASON_INVALID_SHA256_FORMAT,
            ),
        )
    elif exp_pkg is None:
        problems.append(
            (
                CHECK_ID_PACKAGE_IDENTITY,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_MISSING_OPERATOR_ARG,
            ),
        )
    if up_m54 is None and str(inputs.upstream_m54_package_sha256 or "").strip():
        problems.append(
            (
                CHECK_ID_UPSTREAM_CLOSURE,
                STATUS_BLOCKED_INVALID_SHA256,
                REASON_INVALID_SHA256_FORMAT,
            ),
        )
    elif up_m54 is None:
        problems.append(
            (
                CHECK_ID_UPSTREAM_CLOSURE,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_MISSING_OPERATOR_ARG,
            ),
        )
    if not up_id:
        problems.append(
            (
                CHECK_ID_UPSTREAM_CLOSURE,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_MISSING_OPERATOR_ARG,
            ),
        )

    man_path = inputs.evaluation_package_manifest.resolve()
    cand_path = inputs.candidate_identity.resolve()
    score_path = inputs.scorecard_readout_plan.resolve()

    man_d: str | None = None
    cand_d: str | None = None
    score_d: str | None = None

    for p in (man_path, cand_path, score_path):
        if not p.is_file():
            continue
        try:
            raw_txt = p.read_text(encoding="utf-8")
        except OSError:
            raw_txt = ""
        b_reason = _boundary_violation_reason(raw_txt)
        if b_reason is not None:
            problems.append(
                (CHECK_ID_PATH_HYGIENE, STATUS_BLOCKED_PRIVATE_BOUNDARY, b_reason),
            )
            break

    if not man_path.is_file():
        problems.append(
            (CHECK_ID_MANIFEST_COMPLETE, STATUS_BLOCKED_MISSING_INPUT, REASON_MANIFEST_FILE_MISSING)
        )
    else:
        try:
            _parse_json_object(man_path)
            man_d = sha256_file_hex(man_path)
        except (OSError, ValueError, json.JSONDecodeError):
            problems.append(
                (
                    CHECK_ID_MANIFEST_COMPLETE,
                    STATUS_BLOCKED_MISSING_INPUT,
                    REASON_MANIFEST_FILE_MISSING,
                )
            )
            man_d = None

    if not cand_path.is_file():
        problems.append(
            (
                CHECK_ID_MANIFEST_COMPLETE,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_CANDIDATE_FILE_MISSING,
            )
        )
    else:
        try:
            _parse_json_object(cand_path)
            cand_d = sha256_file_hex(cand_path)
        except (OSError, ValueError, json.JSONDecodeError):
            problems.append(
                (
                    CHECK_ID_MANIFEST_COMPLETE,
                    STATUS_BLOCKED_MISSING_INPUT,
                    REASON_CANDIDATE_FILE_MISSING,
                )
            )
            cand_d = None

    if not score_path.is_file():
        problems.append(
            (
                CHECK_ID_MANIFEST_COMPLETE,
                STATUS_BLOCKED_MISSING_INPUT,
                REASON_SCORECARD_FILE_MISSING,
            )
        )
    else:
        try:
            _parse_json_object(score_path)
            score_d = sha256_file_hex(score_path)
        except (OSError, ValueError, json.JSONDecodeError):
            problems.append(
                (
                    CHECK_ID_MANIFEST_COMPLETE,
                    STATUS_BLOCKED_MISSING_INPUT,
                    REASON_SCORECARD_FILE_MISSING,
                ),
            )
            score_d = None

    if up_m54 is not None and up_m54 != CANONICAL_UPSTREAM_M54_PACKAGE_SHA256.lower():
        problems.append(
            (
                CHECK_ID_UPSTREAM_CLOSURE,
                STATUS_BLOCKED_IDENTITY_MISMATCH,
                REASON_UPSTREAM_MISMATCH,
            )
        )
    if up_id and up_id != CANONICAL_UPSTREAM_M54_PACKAGE_ID:
        problems.append(
            (
                CHECK_ID_UPSTREAM_CLOSURE,
                STATUS_BLOCKED_IDENTITY_MISMATCH,
                REASON_UPSTREAM_MISMATCH,
            )
        )

    if man_d and cand_d and score_d:
        synth = evaluation_package_binding_sha256(
            manifest_sha256=man_d,
            candidate_sha256=cand_d,
            scorecard_sha256=score_d,
        )
        if exp_pkg is not None and synth != exp_pkg:
            problems.append(
                (
                    CHECK_ID_PACKAGE_IDENTITY,
                    STATUS_BLOCKED_IDENTITY_MISMATCH,
                    REASON_PACKAGE_SHA_MISMATCH,
                ),
            )

    claim_flags = _claim_flags_template()
    for p in (man_path, cand_path, score_path):
        if not p.is_file():
            continue
        try:
            obj = _parse_json_object(p)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if _object_has_true_claim_violation(obj):
            problems.append(
                (
                    CHECK_ID_CLAIM_HYGIENE,
                    STATUS_BLOCKED_CLAIM_VIOLATION,
                    REASON_CLAIM_FLAG_TRUE,
                ),
            )
            break

    merged = _merge_problems(problems)
    worst = _worst_status(merged)
    final_ready = worst == STATUS_READY
    checks = _rebuild_checks_from_problems(merged, final_ready=final_ready)

    required_inputs = {
        "m54_package_sha256": CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
        "evaluation_package_manifest_sha256": man_d or "",
        "candidate_identity_sha256": cand_d or "",
        "scorecard_or_readout_plan_sha256": score_d or "",
    }
    observed_inputs = {
        "m54_package_sha256": up_m54,
        "evaluation_package_manifest_sha256": man_d,
        "candidate_identity_sha256": cand_d,
        "scorecard_or_readout_plan_sha256": score_d,
    }
    input_package = {
        "package_id": eid,
        "package_sha256": exp_pkg or "",
        "declared_upstream_m54_package_sha256": up_m54 or "",
        "declared_upstream_m54_package_id": up_id,
        "source_kind": SOURCE_KIND_OPERATOR,
    }

    return _finalize_body(
        profile=PROFILE_OPERATOR_DECLARED,
        preflight_status=STATUS_READY if final_ready else worst,
        checks=checks,
        input_package=input_package,
        required_inputs=required_inputs,
        observed_inputs=observed_inputs,
        claim_flags=claim_flags,
    )


def _worst_status(merged: list[tuple[str, str, str]]) -> str:
    rank: dict[str, int] = {
        STATUS_READY: 0,
        STATUS_BLOCKED_MISSING_INPUT: 1,
        STATUS_BLOCKED_INVALID_SHA256: 2,
        STATUS_BLOCKED_IDENTITY_MISMATCH: 3,
        STATUS_BLOCKED_PRIVATE_BOUNDARY: 4,
        STATUS_BLOCKED_CLAIM_VIOLATION: 5,
    }
    worst = STATUS_READY
    for _cid, st, _reason in merged:
        if rank.get(st, 0) > rank[worst]:
            worst = st
    return worst


def _merge_problems(problems: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    rank: dict[str, int] = {
        STATUS_READY: 0,
        STATUS_BLOCKED_MISSING_INPUT: 1,
        STATUS_BLOCKED_INVALID_SHA256: 2,
        STATUS_BLOCKED_IDENTITY_MISMATCH: 3,
        STATUS_BLOCKED_PRIVATE_BOUNDARY: 4,
        STATUS_BLOCKED_CLAIM_VIOLATION: 5,
    }
    by_cid: dict[str, tuple[str, str]] = {}
    for cid, st, reason in problems:
        prev = by_cid.get(cid)
        if prev is None or rank.get(st, 0) >= rank.get(prev[0], 0):
            by_cid[cid] = (st, reason)
    return [(cid, st, r) for cid, (st, r) in sorted(by_cid.items(), key=lambda x: x[0])]


def _all_check_ids() -> tuple[str, ...]:
    return (
        CHECK_ID_PACKAGE_IDENTITY,
        CHECK_ID_UPSTREAM_CLOSURE,
        CHECK_ID_MANIFEST_COMPLETE,
        CHECK_ID_PATH_HYGIENE,
        CHECK_ID_CLAIM_HYGIENE,
    )


def _rebuild_checks_from_problems(
    problems: list[tuple[str, str, str]],
    *,
    final_ready: bool,
) -> list[dict[str, Any]]:
    by_id: dict[str, tuple[str, str]] = {}
    for cid, st, reason in problems:
        by_id[cid] = (st, reason)
    checks: list[dict[str, Any]] = []
    for cid in _all_check_ids():
        if cid in by_id:
            st, reason = by_id[cid]
            checks.append(_check_row(cid, "blocked", reason=reason))
        else:
            checks.append(_check_row(cid, "passed"))
    checks.append(
        _check_row(
            CHECK_ID_READOUT_READY,
            "passed" if final_ready else "blocked",
            reason="" if final_ready else "preflight_not_ready_for_bounded_readout",
        ),
    )
    return checks


def _object_has_true_claim_violation(obj: Any) -> bool:
    forbidden_keys = (
        "evaluation_executed",
        "benchmark_pass_claimed",
        "candidate_promoted",
        "strong_agent_claimed",
        "human_panel_claimed",
        "xai_demo_claimed",
        "v2_ready_claimed",
    )
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in forbidden_keys and v is True:
                return True
            if _object_has_true_claim_violation(v):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if _object_has_true_claim_violation(item):
                return True
    return False


def build_operator_preflight_blocked() -> dict[str, Any]:
    m54_sha = CANONICAL_UPSTREAM_M54_PACKAGE_SHA256
    input_package = {
        "package_id": "",
        "package_sha256": "",
        "declared_upstream_m54_package_sha256": "",
        "declared_upstream_m54_package_id": "",
        "source_kind": SOURCE_KIND_OPERATOR,
    }
    required_inputs = {
        "m54_package_sha256": m54_sha,
        "evaluation_package_manifest_sha256": "",
        "candidate_identity_sha256": "",
        "scorecard_or_readout_plan_sha256": "",
    }
    observed_inputs: dict[str, str | None] = {
        "m54_package_sha256": None,
        "evaluation_package_manifest_sha256": None,
        "candidate_identity_sha256": None,
        "scorecard_or_readout_plan_sha256": None,
    }
    reason = REASON_MISSING_OPERATOR_ARG
    na_path = "operator_preflight_without_file_inputs"
    checks = [
        _check_row(CHECK_ID_PACKAGE_IDENTITY, "blocked", reason=reason),
        _check_row(CHECK_ID_UPSTREAM_CLOSURE, "blocked", reason=reason),
        _check_row(CHECK_ID_MANIFEST_COMPLETE, "blocked", reason=reason),
        _check_row(CHECK_ID_PATH_HYGIENE, "not_applicable", reason=na_path),
        _check_row(CHECK_ID_CLAIM_HYGIENE, "passed"),
        _check_row(
            CHECK_ID_READOUT_READY,
            "blocked",
            reason="preflight_not_ready_for_bounded_readout",
        ),
    ]
    return _finalize_body(
        profile=PROFILE_OPERATOR_PREFLIGHT,
        preflight_status=STATUS_BLOCKED_MISSING_INPUT,
        checks=checks,
        input_package=input_package,
        required_inputs=required_inputs,
        observed_inputs=observed_inputs,
        claim_flags=_claim_flags_template(),
    )


def emit_forbidden_refusal(
    output_dir: Path, *, flags: list[str]
) -> tuple[dict[str, Any], tuple[Path, Path]]:
    body_raw = build_fixture_preflight()
    body_raw["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body_raw["preflight_status"] = STATUS_BLOCKED_CLAIM_VIOLATION
    body_raw["preflight_checks"] = [
        _check_row(
            CHECK_ID_CLAIM_HYGIENE,
            "blocked",
            reason=f"forbidden_cli_flag:{','.join(sorted(flags))}",
        ),
        *[
            _check_row(cid, "blocked", reason="blocked_due_to_forbidden_cli_flag")
            for cid in (
                CHECK_ID_PACKAGE_IDENTITY,
                CHECK_ID_UPSTREAM_CLOSURE,
                CHECK_ID_MANIFEST_COMPLETE,
                CHECK_ID_PATH_HYGIENE,
                CHECK_ID_READOUT_READY,
            )
        ],
    ]
    return write_preflight_artifacts(output_dir, body_unsealed=body_raw)


__all__ = [
    "OperatorDeclaredInputs",
    "build_fixture_preflight",
    "build_operator_declared_preflight",
    "build_operator_preflight_blocked",
    "build_preflight_report",
    "compute_json_sha256_if_path_given",
    "emit_forbidden_refusal",
    "evaluation_package_binding_sha256",
    "seal_m55_body",
    "sha256_file_hex",
    "validate_sha256",
    "write_preflight_artifacts",
]
