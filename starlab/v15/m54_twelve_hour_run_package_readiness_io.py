"""V15-M54 — package / evaluation readiness over sealed V15-M53 evidence."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    CONTRACT_ID_M53,
    PROFILE_M53,
    STATUS_12H_COMPLETED_CKPT,
)
from starlab.v15.m54_twelve_hour_run_package_readiness_models import (
    ANCHOR_INPUT_CANDIDATE_CHECKPOINT_SHA256,
    ANCHOR_PHASE_A_MATCH_PROOF_SHA256,
    BINDING_FILENAME,
    BINDING_KIND_PHASE_A_ARTIFACT_HASH,
    BINDING_KIND_PHASE_A_RAW_FILE_SHA256,
    BINDING_REQUIRED_SENTENCE,
    BLOCKED_FINAL_CKPT_MISSING,
    BLOCKED_FINAL_CKPT_NOT_PERSISTED_M53,
    BLOCKED_FINAL_CKPT_SHA_MISMATCH,
    BLOCKED_FULL_WALL_CLOCK,
    BLOCKED_INVENTORY_MISSING,
    BLOCKED_INVENTORY_MISSING_FINAL,
    BLOCKED_M53_CONTRACT_INVALID,
    BLOCKED_M53_HAS_BLOCKERS,
    BLOCKED_M53_HAS_FAILURE_REASONS,
    BLOCKED_M53_NOT_COMPLETED,
    BLOCKED_M53_SHA_MISMATCH,
    BLOCKED_MISSING_M53_JSON,
    BLOCKED_PHASE_A_PROOF_HASH_MISMATCH,
    BLOCKED_PHASE_A_PROOF_MISSING,
    BLOCKED_RAW_SHA_MISMATCH,
    BLOCKED_TELEMETRY_MISSING,
    BLOCKED_TRANSCRIPT_MISSING,
    BRIEF_FILENAME,
    CHECKLIST_FILENAME,
    CONTRACT_ID_M54,
    EMITTER_MODULE_M54,
    FILENAME_MAIN_JSON,
    FINAL_CHECKPOINT_RELATIVE_PATH,
    GATE_ARTIFACT_DIGEST_FIELD,
    MANIFEST_FILENAME,
    MILESTONE_LABEL_M54,
    NON_CLAIMS_M54,
    PROFILE_FIXTURE_CI,
    PROFILE_M54,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REFUSED_FORBIDDEN,
    REPORT_FILENAME,
    ROUTE_BOUNDED_EVAL_PREFLIGHT,
    ROUTE_RECOMMENDED_NOT_EXECUTED,
    SCHEMA_VERSION,
    STATUS_BLOCKED,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
    STATUS_READY_WARNINGS,
    STATUS_REFUSED,
    TRANSCRIPT_SHORT_WARN_BYTES,
    WARNING_CHECKPOINT_CANDIDATE_ONLY,
    WARNING_FINAL_M53_REPLAY_FALSE,
    WARNING_M50_UPSTREAM,
    WARNING_PACKAGE_READY_NOT_EVAL,
    WARNING_PHASE_A_REPLAY_BUT_M53_FALSE,
    WARNING_RAW_ARTIFACT_HASH_MISSING,
    WARNING_TRANSCRIPT_SHORT,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")

M53_DIGEST_FIELD = GATE_ARTIFACT_DIGEST_FIELD


def _is_hex64(s: str) -> bool:
    t = str(s or "").strip().lower()
    return len(t) == 64 and all(c in _HEX64_CHARS for c in t)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _phase_a_embedded_artifact_hash(proof_obj: dict[str, Any]) -> str | None:
    ah = proof_obj.get("artifact_hash")
    if ah is None:
        return None
    t = str(ah).strip().lower()
    return t if _is_hex64(t) else None


def sha256_file_hex(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fb:
        while chunk := fb.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def _honesty_all_false() -> dict[str, Any]:
    return {
        "benchmark_passed": False,
        "benchmark_pass_fail_emitted": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "checkpoint_loaded_for_evaluation": False,
        "xai_executed": False,
        "human_panel_executed": False,
        "showcase_released": False,
        "v2_authorized": False,
        "t2_t3_t4_t5_executed": False,
    }


def seal_m54_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _m53_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(M53_DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != M53_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def build_m54_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_twelve_hour_run_package_readiness_report",
        "report_version": "m54",
        "milestone": MILESTONE_LABEL_M54,
        "contract_id": CONTRACT_ID_M54,
        "profile_id": PROFILE_M54,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "package_status": sealed.get("package_status"),
    }


def build_m54_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("package_status", ""))
    blk = sealed.get("blockers") or []
    warn = sealed.get("warnings") or []
    nc_raw = sealed.get("non_claims") or []
    blk_lines = "\n".join(f"- `{b}`" for b in blk) if isinstance(blk, list) and blk else "(none)"
    warn_lines = (
        "\n".join(f"- `{w}`" for w in warn) if isinstance(warn, list) and warn else "(none)"
    )
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return f"""# V15-M54 — 12-hour run package / evaluation readiness checklist

**`package_status`:** `{st}`

## Checkpoint binding statement

{BINDING_REQUIRED_SENTENCE}

## Blockers

{blk_lines}

## Warnings

{warn_lines}

## Non-claims

{nc_lines}

## Artifacts

- `{FILENAME_MAIN_JSON}`
- `{REPORT_FILENAME}`
- `{CHECKLIST_FILENAME}`
- `{BINDING_FILENAME}`
- `{MANIFEST_FILENAME}`
"""


def build_m54_binding_json(sealed: dict[str, Any]) -> dict[str, Any]:
    ccb = sealed.get("candidate_checkpoint_binding") or {}
    if not isinstance(ccb, dict):
        ccb = {}
    return {
        "contract_id": CONTRACT_ID_M54,
        "milestone": MILESTONE_LABEL_M54,
        "candidate_checkpoint_binding": {
            "input_candidate_checkpoint_sha256": ccb.get("input_candidate_checkpoint_sha256"),
            "produced_candidate_checkpoint_sha256": ccb.get("produced_candidate_checkpoint_sha256"),
            "promotion_status": "not_promoted_candidate_only",
            "binding_statement": BINDING_REQUIRED_SENTENCE,
            "torch_load_performed": False,
            "checkpoint_loaded_for_evaluation": False,
        },
    }


def build_m54_manifest(
    sealed: dict[str, Any], *, artifact_filenames: tuple[str, ...]
) -> dict[str, Any]:
    rd = sealed.get("readiness_decision") or {}
    if not isinstance(rd, dict):
        rd = {}
    return {
        "contract_id": CONTRACT_ID_M54,
        "milestone": MILESTONE_LABEL_M54,
        "package_status": sealed.get("package_status"),
        "artifact_filenames": list(artifact_filenames),
        "readiness_decision": rd,
        "routing_note": (
            "Readiness routing is recommended only; bounded evaluation package preflight "
            "is not executed by V15-M54."
        ),
    }


def build_m54_brief_md(sealed: dict[str, Any]) -> str:
    st = sealed.get("package_status")
    rd = sealed.get("readiness_decision") or {}
    rn = rd.get("recommended_next") if isinstance(rd, dict) else ""
    return f"""# V15-M54 — twelve-hour run package readiness (public-safe brief)

**Status:** `{st}`

**Recommended next:** `{rn}`

{BINDING_REQUIRED_SENTENCE}

This milestone does **not** execute benchmark pass/fail, strength evaluation, checkpoint promotion,
XAI, human-panel evaluation, showcase release, v2 authorization, or T2–T5 execution.
"""


def _inventory_lists_final_checkpoint(inv: dict[str, Any], *, produced_sha: str) -> bool:
    want_sha = produced_sha.strip().lower()
    suffix = FINAL_CHECKPOINT_RELATIVE_PATH.replace("\\", "/")
    rows = inv.get("checkpoint_files")
    if not isinstance(rows, list):
        return False
    for r in rows:
        if not isinstance(r, dict):
            continue
        rel = str(r.get("path_relative_to_m39_output_dir") or "").replace("\\", "/")
        if rel != suffix and not rel.endswith(suffix):
            continue
        if str(r.get("sha256") or "").strip().lower() == want_sha:
            return True
    return False


def _execution_summary_from_m53(m53: dict[str, Any]) -> dict[str, Any]:
    pb = m53.get("phase_b_12hour_run") or {}
    if not isinstance(pb, dict):
        pb = {}
    return {
        "observed_wall_clock_seconds": float(pb.get("observed_wall_clock_seconds") or 0.0),
        "full_wall_clock_satisfied": bool(pb.get("full_wall_clock_satisfied")),
        "training_update_count": int(pb.get("training_update_count") or 0),
        "checkpoints_written": int(pb.get("checkpoints_written_total") or 0),
        "checkpoints_pruned": int(pb.get("checkpoints_pruned_total") or 0),
        "checkpoints_retained": int(
            m53.get("checkpoints_retained") or pb.get("checkpoint_retention_max_retained") or 0
        ),
        "final_step_checkpoint_persisted": bool(pb.get("final_step_checkpoint_persisted")),
    }


def build_fixture_m54_body(*, package_status: str | None = None) -> dict[str, Any]:
    st = package_status or STATUS_FIXTURE_ONLY
    rec = RECOMMENDED_NEXT_SUCCESS if st == STATUS_READY else RECOMMENDED_NEXT_REMEDIATION
    route_next = RECOMMENDED_NEXT_SUCCESS if st == STATUS_READY else RECOMMENDED_NEXT_REMEDIATION
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M54,
        "profile_id": PROFILE_M54,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M54,
        "emitter_module": EMITTER_MODULE_M54,
        "package_status": st,
        "m53_binding": {
            "contract_id": CONTRACT_ID_M53,
            "artifact_sha256": None,
            "raw_file_sha256": None,
            "run_status": None,
        },
        "phase_a_binding": {
            "status": None,
            "proof_artifact_hash": None,
            "proof_raw_file_sha256": None,
            "proof_hash_binding_kind": None,
            "proof_hash_actual": None,
            "live_sc2_executed": False,
            "watchability_only": True,
        },
        "execution_summary": {
            "observed_wall_clock_seconds": 0.0,
            "full_wall_clock_satisfied": False,
            "training_update_count": 0,
            "checkpoints_written": 0,
            "checkpoints_pruned": 0,
            "checkpoints_retained": 0,
            "final_step_checkpoint_persisted": False,
        },
        "candidate_checkpoint_binding": {
            "input_candidate_checkpoint_sha256": None,
            "produced_candidate_checkpoint_sha256": None,
            "promotion_status": "not_promoted_candidate_only",
        },
        "operator_artifacts": {
            "checkpoint_inventory_captured": False,
            "telemetry_summary_captured": False,
            "transcript_captured": False,
            "phase_a_match_proof_captured": False,
            "final_m53_replay_saved": False,
            "phase_a_replay_saved": False,
        },
        "readiness_decision": {
            "recommended_next": route_next,
            "route_status": ROUTE_RECOMMENDED_NOT_EXECUTED,
            "route_to": ROUTE_BOUNDED_EVAL_PREFLIGHT
            if st == STATUS_READY
            else "route_to_remediation",
        },
        "warnings": [],
        "blockers": [],
        "honesty": _honesty_all_false(),
        "non_claims": list(NON_CLAIMS_M54),
        "recommended_next": rec,
    }


@dataclass(frozen=True)
class M54PreflightInputs:
    m53_run_json: Path
    expected_m53_run_sha256: str | None
    raw_m53_file_sha256: str | None
    m53_checkpoint_inventory_json: Path | None
    m53_telemetry_summary_json: Path | None
    m53_transcript_path: Path | None
    phase_a_match_proof_json: Path | None
    expected_phase_a_proof_sha256: str | None
    final_candidate_checkpoint_path: Path | None
    expected_final_candidate_checkpoint_sha256: str | None


def evaluate_m54_operator_preflight(inputs: M54PreflightInputs) -> dict[str, Any]:
    """Return an unsealed M54 body (still missing artifact_sha256). Caller seals + emits."""
    warnings: list[str] = [
        WARNING_M50_UPSTREAM,
        WARNING_PACKAGE_READY_NOT_EVAL,
        WARNING_CHECKPOINT_CANDIDATE_ONLY,
    ]
    blockers: list[str] = []

    body = build_fixture_m54_body(package_status=STATUS_BLOCKED)
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["warnings"] = []
    body["blockers"] = []

    def _finalize_blocked(extra: list[str]) -> dict[str, Any]:
        blk_u = tuple(sorted(set(extra)))
        body["blockers"] = list(blk_u)
        body["package_status"] = STATUS_BLOCKED
        body["readiness_decision"] = {
            "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
            "route_status": ROUTE_RECOMMENDED_NOT_EXECUTED,
            "route_to": "route_to_remediation",
        }
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        body["warnings"] = sorted(set(warnings))
        return body

    m53_path = inputs.m53_run_json
    if not m53_path.is_file():
        blockers.append(BLOCKED_MISSING_M53_JSON)
        return _finalize_blocked(blockers)

    raw_sha_expected: str | None = None
    if inputs.raw_m53_file_sha256:
        rx = str(inputs.raw_m53_file_sha256).strip().lower()
        if _is_hex64(rx):
            raw_sha_expected = rx
            disk_sha = sha256_file_hex(m53_path).lower()
            if disk_sha != raw_sha_expected:
                blockers.append(BLOCKED_RAW_SHA_MISMATCH)
                return _finalize_blocked(blockers)
        else:
            warnings.append(WARNING_RAW_ARTIFACT_HASH_MISSING)
    else:
        warnings.append(WARNING_RAW_ARTIFACT_HASH_MISSING)

    try:
        m53 = _parse_json_object(m53_path.resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        blockers.append(BLOCKED_M53_CONTRACT_INVALID)
        return _finalize_blocked(blockers)

    if (
        str(m53.get("contract_id") or "") != CONTRACT_ID_M53
        or str(m53.get("profile_id") or "") != PROFILE_M53
    ):
        blockers.append(BLOCKED_M53_CONTRACT_INVALID)
        return _finalize_blocked(blockers)

    if not _m53_seal_ok(m53):
        blockers.append(BLOCKED_M53_CONTRACT_INVALID)
        return _finalize_blocked(blockers)

    sealed_digest = str(m53.get(M53_DIGEST_FIELD) or "").strip().lower()
    exp_m53 = str(inputs.expected_m53_run_sha256 or "").strip().lower()
    if not (_is_hex64(exp_m53) and sealed_digest == exp_m53):
        blockers.append(BLOCKED_M53_SHA_MISMATCH)
        return _finalize_blocked(blockers)

    run_status = str(m53.get("run_status") or "")
    if run_status != STATUS_12H_COMPLETED_CKPT:
        blockers.append(BLOCKED_M53_NOT_COMPLETED)
        return _finalize_blocked(blockers)

    m53_blockers = m53.get("blockers") or []
    if isinstance(m53_blockers, list) and len(m53_blockers) > 0:
        blockers.append(BLOCKED_M53_HAS_BLOCKERS)
        return _finalize_blocked(blockers)

    m53_fail = m53.get("failure_reasons") or []
    if isinstance(m53_fail, list) and len(m53_fail) > 0:
        blockers.append(BLOCKED_M53_HAS_FAILURE_REASONS)
        return _finalize_blocked(blockers)

    pb = m53.get("phase_b_12hour_run") or {}
    if not isinstance(pb, dict):
        pb = {}
    if pb.get("full_wall_clock_satisfied") is not True:
        blockers.append(BLOCKED_FULL_WALL_CLOCK)
        return _finalize_blocked(blockers)
    if pb.get("final_step_checkpoint_persisted") is not True:
        blockers.append(BLOCKED_FINAL_CKPT_NOT_PERSISTED_M53)
        return _finalize_blocked(blockers)

    produced_from_m53 = str(pb.get("final_candidate_checkpoint_sha256") or "").strip().lower()
    exp_final = str(inputs.expected_final_candidate_checkpoint_sha256 or "").strip().lower()
    if _is_hex64(exp_final) and _is_hex64(produced_from_m53) and produced_from_m53 != exp_final:
        blockers.append(BLOCKED_FINAL_CKPT_SHA_MISMATCH)
        return _finalize_blocked(blockers)

    candidate_id = m53.get("candidate_identity") or {}
    if not isinstance(candidate_id, dict):
        candidate_id = {}
    input_ckpt_sha = str(candidate_id.get("candidate_checkpoint_sha256") or "").strip().lower()

    op_art_m53 = m53.get("operator_artifacts") or {}
    if not isinstance(op_art_m53, dict):
        op_art_m53 = {}

    phase_a = m53.get("phase_a_candidate_watch_smoke") or {}
    if not isinstance(phase_a, dict):
        phase_a = {}

    proof_path = inputs.phase_a_match_proof_json
    proof_raw_sha: str | None = None
    proof_semantic_hash: str | None = None
    phase_a_replay_saved = False
    if proof_path is None or not proof_path.is_file():
        blockers.append(BLOCKED_PHASE_A_PROOF_MISSING)
        return _finalize_blocked(blockers)
    resolved_proof = Path(proof_path).resolve()
    try:
        proof_raw_sha = sha256_file_hex(resolved_proof).lower()
    except OSError:
        blockers.append(BLOCKED_PHASE_A_PROOF_MISSING)
        return _finalize_blocked(blockers)
    try:
        proof_obj = _parse_json_object(resolved_proof)
    except (OSError, ValueError, json.JSONDecodeError):
        blockers.append(BLOCKED_PHASE_A_PROOF_MISSING)
        return _finalize_blocked(blockers)
    proof_semantic_hash = _phase_a_embedded_artifact_hash(proof_obj)
    phase_a_replay_saved = bool(proof_obj.get("replay_saved"))

    exp_proof = (
        str(
            inputs.expected_phase_a_proof_sha256 or ANCHOR_PHASE_A_MATCH_PROOF_SHA256,
        )
        .strip()
        .lower()
    )
    proof_hash_actual: str | None = None
    proof_binding_kind: str | None = None

    if not _is_hex64(exp_proof):
        blockers.append(BLOCKED_PHASE_A_PROOF_HASH_MISMATCH)
        body["phase_a_proof_hash_mismatch_detail"] = {
            "expected_phase_a_proof_sha256": exp_proof,
            "embedded_artifact_hash": proof_semantic_hash,
            "raw_file_sha256": proof_raw_sha,
            "reason": "expected_phase_a_proof_sha256_not_hex64",
        }
        pab = body.get("phase_a_binding")
        if isinstance(pab, dict):
            pab.update(
                {
                    "proof_artifact_hash": proof_semantic_hash,
                    "proof_raw_file_sha256": proof_raw_sha,
                    "proof_hash_binding_kind": None,
                    "proof_hash_actual": None,
                },
            )
        return _finalize_blocked(blockers)

    if proof_semantic_hash is not None and proof_semantic_hash == exp_proof:
        proof_binding_kind = BINDING_KIND_PHASE_A_ARTIFACT_HASH
        proof_hash_actual = proof_semantic_hash
    elif proof_raw_sha == exp_proof:
        proof_binding_kind = BINDING_KIND_PHASE_A_RAW_FILE_SHA256
        proof_hash_actual = proof_raw_sha
    else:
        blockers.append(BLOCKED_PHASE_A_PROOF_HASH_MISMATCH)
        body["phase_a_proof_hash_mismatch_detail"] = {
            "expected_phase_a_proof_sha256": exp_proof,
            "embedded_artifact_hash": proof_semantic_hash,
            "raw_file_sha256": proof_raw_sha,
        }
        pab = body.get("phase_a_binding")
        if isinstance(pab, dict):
            pab.update(
                {
                    "proof_artifact_hash": proof_semantic_hash,
                    "proof_raw_file_sha256": proof_raw_sha,
                    "proof_hash_binding_kind": None,
                    "proof_hash_actual": None,
                },
            )
        return _finalize_blocked(blockers)

    inv_path = inputs.m53_checkpoint_inventory_json
    if inv_path is None or not Path(inv_path).is_file():
        blockers.append(BLOCKED_INVENTORY_MISSING)
        return _finalize_blocked(blockers)
    try:
        inv = _parse_json_object(Path(inv_path).resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        blockers.append(BLOCKED_INVENTORY_MISSING)
        return _finalize_blocked(blockers)

    produced_sha_use = exp_final if _is_hex64(exp_final) else produced_from_m53
    if not _is_hex64(produced_sha_use):
        blockers.append(BLOCKED_FINAL_CKPT_SHA_MISMATCH)
        return _finalize_blocked(blockers)

    if not _inventory_lists_final_checkpoint(inv, produced_sha=produced_sha_use):
        blockers.append(BLOCKED_INVENTORY_MISSING_FINAL)
        return _finalize_blocked(blockers)

    tel_path = inputs.m53_telemetry_summary_json
    if tel_path is None or not Path(tel_path).is_file():
        blockers.append(BLOCKED_TELEMETRY_MISSING)
        return _finalize_blocked(blockers)
    try:
        tel_obj = _parse_json_object(Path(tel_path).resolve())
        tel_ok = isinstance(tel_obj, dict)
    except (OSError, ValueError, json.JSONDecodeError):
        tel_ok = False
    if not tel_ok:
        blockers.append(BLOCKED_TELEMETRY_MISSING)
        return _finalize_blocked(blockers)

    tr_path = inputs.m53_transcript_path
    if tr_path is None or not Path(tr_path).is_file():
        blockers.append(BLOCKED_TRANSCRIPT_MISSING)
        return _finalize_blocked(blockers)
    tr_sz = Path(tr_path).stat().st_size
    transcript_text_head = Path(tr_path).read_text(encoding="utf-8", errors="replace")[:4000]
    if tr_sz <= 0:
        blockers.append(BLOCKED_TRANSCRIPT_MISSING)
        return _finalize_blocked(blockers)
    low_head = transcript_text_head.lower()
    if tr_sz < TRANSCRIPT_SHORT_WARN_BYTES or "[redacted]" in low_head:
        warnings.append(WARNING_TRANSCRIPT_SHORT)

    ck_path = inputs.final_candidate_checkpoint_path
    if ck_path is None or not Path(ck_path).is_file():
        blockers.append(BLOCKED_FINAL_CKPT_MISSING)
        return _finalize_blocked(blockers)
    file_sha = sha256_file_hex(Path(ck_path).resolve()).lower()
    if file_sha != produced_sha_use:
        blockers.append(BLOCKED_FINAL_CKPT_SHA_MISMATCH)
        return _finalize_blocked(blockers)

    final_m53_replay = bool(op_art_m53.get("replay_saved"))
    if not final_m53_replay:
        warnings.append(WARNING_FINAL_M53_REPLAY_FALSE)
    if phase_a_replay_saved and not final_m53_replay:
        warnings.append(WARNING_PHASE_A_REPLAY_BUT_M53_FALSE)

    exec_summary = _execution_summary_from_m53(m53)
    retained_m53 = int(m53.get("checkpoints_retained") or 0)
    if retained_m53 > 0:
        exec_summary["checkpoints_retained"] = retained_m53

    phase_status = str(phase_a.get("status") or "candidate_watch_smoke_completed")

    body.clear()
    body.update(
        {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_M54,
            "profile_id": PROFILE_M54,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "milestone": MILESTONE_LABEL_M54,
            "emitter_module": EMITTER_MODULE_M54,
            "package_status": STATUS_READY,
            "m53_binding": {
                "contract_id": CONTRACT_ID_M53,
                "artifact_sha256": sealed_digest,
                "raw_file_sha256": raw_sha_expected,
                "run_status": run_status,
            },
            "phase_a_binding": {
                "status": phase_status,
                "proof_artifact_hash": proof_semantic_hash,
                "proof_raw_file_sha256": proof_raw_sha,
                "proof_hash_binding_kind": proof_binding_kind,
                "proof_hash_actual": proof_hash_actual,
                "live_sc2_executed": bool(phase_a.get("live_sc2_executed")),
                "watchability_only": True,
            },
            "execution_summary": exec_summary,
            "candidate_checkpoint_binding": {
                "input_candidate_checkpoint_sha256": (
                    input_ckpt_sha
                    if _is_hex64(input_ckpt_sha)
                    else ANCHOR_INPUT_CANDIDATE_CHECKPOINT_SHA256
                ),
                "produced_candidate_checkpoint_sha256": produced_sha_use,
                "promotion_status": "not_promoted_candidate_only",
            },
            "operator_artifacts": {
                "checkpoint_inventory_captured": True,
                "telemetry_summary_captured": True,
                "transcript_captured": True,
                "phase_a_match_proof_captured": True,
                "final_m53_replay_saved": final_m53_replay,
                "phase_a_replay_saved": phase_a_replay_saved,
            },
            "readiness_decision": {
                "recommended_next": RECOMMENDED_NEXT_SUCCESS,
                "route_status": ROUTE_RECOMMENDED_NOT_EXECUTED,
                "route_to": ROUTE_BOUNDED_EVAL_PREFLIGHT,
            },
            "warnings": [],
            "blockers": [],
            "honesty": _honesty_all_false(),
            "non_claims": list(NON_CLAIMS_M54),
            "recommended_next": RECOMMENDED_NEXT_SUCCESS,
        },
    )

    warn_u = sorted(set(warnings))
    body["warnings"] = warn_u
    if warn_u:
        body["package_status"] = STATUS_READY_WARNINGS

    return body


def emit_m54_bundle(
    output_dir: Path, *, body_unsealed: dict[str, Any]
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sealed = seal_m54_body(cast(dict[str, Any], redact_paths_in_value(body_unsealed)))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m54_report(sealed)
    chk = build_m54_checklist_md(sealed)
    binding = build_m54_binding_json(sealed)

    paths_order = (
        FILENAME_MAIN_JSON,
        REPORT_FILENAME,
        CHECKLIST_FILENAME,
        BINDING_FILENAME,
        MANIFEST_FILENAME,
        BRIEF_FILENAME,
    )
    manifest = build_m54_manifest(sealed, artifact_filenames=paths_order)
    brief = build_m54_brief_md(sealed)

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_bind = output_dir / BINDING_FILENAME
    p_man = output_dir / MANIFEST_FILENAME
    p_brief = output_dir / BRIEF_FILENAME

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_bind.write_text(canonical_json_dumps(binding), encoding="utf-8")
    p_man.write_text(canonical_json_dumps(manifest), encoding="utf-8")
    p_brief.write_text(brief, encoding="utf-8", newline="\n")

    blob = (
        canonical_json_dumps(sealed)
        + canonical_json_dumps(rep)
        + chk
        + canonical_json_dumps(binding)
    )
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M54 emission leaked path patterns")

    return sealed, (p_main, p_rep, p_chk, p_bind, p_man, p_brief)


def emit_m54_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body = build_fixture_m54_body(package_status=STATUS_FIXTURE_ONLY)
    body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
    rd = body.get("readiness_decision")
    if isinstance(rd, dict):
        rd["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        rd["route_to"] = "route_to_remediation"
    return emit_m54_bundle(output_dir, body_unsealed=body)


def emit_m54_forbidden_refusal(
    output_dir: Path, *, flags: list[str]
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body = build_fixture_m54_body(package_status=STATUS_REFUSED)
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["blockers"] = sorted({REFUSED_FORBIDDEN, *flags})
    body["warnings"] = []
    body["readiness_decision"] = {
        "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
        "route_status": ROUTE_RECOMMENDED_NOT_EXECUTED,
        "route_to": "route_to_remediation",
    }
    body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
    return emit_m54_bundle(output_dir, body_unsealed=body)


def emit_m54_operator_preflight_bundle(
    output_dir: Path,
    *,
    inputs: M54PreflightInputs,
) -> tuple[dict[str, Any], tuple[Path, ...], bool]:
    body = evaluate_m54_operator_preflight(inputs)
    sealed, paths = emit_m54_bundle(output_dir, body_unsealed=body)
    ok_pack = sealed.get("package_status") in (STATUS_READY, STATUS_READY_WARNINGS)
    return sealed, paths, ok_pack


def emit_m54_operator_declared(
    output_dir: Path, *, declared_json: Path
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    raw = _parse_json_object(declared_json.resolve())
    if str(raw.get("contract_id") or "") != CONTRACT_ID_M54:
        raise ValueError("declared package JSON contract_id mismatch for V15-M54")
    raw.pop(GATE_ARTIFACT_DIGEST_FIELD, None)
    raw.setdefault("profile", PROFILE_OPERATOR_DECLARED)
    raw.setdefault("honesty", _honesty_all_false())
    raw.setdefault("non_claims", list(NON_CLAIMS_M54))
    out_body = cast(dict[str, Any], redact_paths_in_value(raw))
    return emit_m54_bundle(output_dir, body_unsealed=out_body)


__all__ = [
    "M54PreflightInputs",
    "build_fixture_m54_body",
    "build_m54_binding_json",
    "build_m54_brief_md",
    "build_m54_checklist_md",
    "build_m54_manifest",
    "build_m54_report",
    "emit_m54_fixture_ci",
    "emit_m54_forbidden_refusal",
    "emit_m54_operator_preflight_bundle",
    "emit_m54_operator_declared",
    "emit_m54_bundle",
    "evaluate_m54_operator_preflight",
    "seal_m54_body",
    "sha256_file_hex",
]
