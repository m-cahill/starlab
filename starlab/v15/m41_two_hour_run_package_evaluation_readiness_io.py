"""V15-M41 — package / evaluation readiness over sealed M39 and companion artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    CONTRACT_ID_M39,
    PROFILE_M39,
    STATUS_RUN_COMPLETED_WITH_CKPT,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    CANDIDATE_INDEX_FILENAME,
    CHECKLIST_FILENAME,
    CONTRACT_ID_M41,
    EMITTER_MODULE_M41,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M39_CLAIM_KEYS_MUST_REMAIN_FALSE,
    MILESTONE_LABEL_M41,
    NON_CLAIMS_M41,
    PACKET_FILENAME,
    PROFILE_FIXTURE_CI,
    PROFILE_M41,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    SCHEMA_VERSION,
    SOURCE_CANDIDATE_LINEAGE_SHA256,
    STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH,
    STATUS_BLOCKED_INVALID_M39,
    STATUS_BLOCKED_M39_NOT_COMPLETED,
    STATUS_BLOCKED_MISSING_INVENTORY,
    STATUS_BLOCKED_MISSING_M39,
    STATUS_BLOCKED_MISSING_TELEMETRY,
    STATUS_BLOCKED_MISSING_TRANSCRIPT,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
    STATUS_READY_WARNINGS,
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


def sha256_file_hex(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fb:
        while chunk := fb.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def _claim_flags_all_false_m41() -> dict[str, bool]:
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


def seal_m41_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m41_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_two_hour_run_package_evaluation_readiness_report",
        "report_version": "m41",
        "milestone": MILESTONE_LABEL_M41,
        "contract_id": CONTRACT_ID_M41,
        "profile_id": PROFILE_M41,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "package_status": sealed.get("package_status"),
    }


def _gate_pack(
    *,
    p0: bool,
    p1: bool,
    p2: bool,
    p3: bool,
    p4: bool,
    p5: bool,
    p6: bool,
    p7: bool,
    p8: bool,
    p9: bool,
) -> list[dict[str, Any]]:
    return [
        {"gate_id": "P0", "name": "M39 receipt bound", "passed": p0},
        {"gate_id": "P1", "name": "M39 contract valid", "passed": p1},
        {"gate_id": "P2", "name": "Run completed", "passed": p2},
        {"gate_id": "P3", "name": "Wall-clock satisfied", "passed": p3},
        {"gate_id": "P4", "name": "Final candidate present", "passed": p4},
        {"gate_id": "P5", "name": "Retention evidence", "passed": p5},
        {"gate_id": "P6", "name": "Companion evidence", "passed": p6},
        {"gate_id": "P7", "name": "M39 non-claim flags preserved", "passed": p7},
        {"gate_id": "P8", "name": "Public/private boundary", "passed": p8},
        {"gate_id": "P9", "name": "Evaluation readiness only", "passed": p9},
    ]


def build_m41_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("package_status", ""))
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
    return f"""# V15-M41 — 2-hour run package & evaluation readiness checklist

**`package_status`:** `{st}`

## Gate pack (P0–P9)

| Gate | Name | Pass |
| --- | --- | --- |
{gate_lines}
## Non-claims

{nc_lines}

## Artifacts

- `{FILENAME_MAIN_JSON}`
- `{REPORT_FILENAME}`
- `{CHECKLIST_FILENAME}`
- `{PACKET_FILENAME}`
- `{CANDIDATE_INDEX_FILENAME}`
"""


def _build_evaluation_packet_md(sealed: dict[str, Any]) -> str:
    st = sealed.get("package_status")
    m39_sha = ""
    ub = sealed.get("upstream_bindings") or {}
    if isinstance(ub, dict):
        m39b = ub.get("m39_two_hour_operator_run") or {}
        if isinstance(m39b, dict):
            m39_sha = str(m39b.get("artifact_sha256") or "")
    fc = sealed.get("candidate_checkpoint") or {}
    final_s = str(fc.get("final_candidate_sha256") or "") if isinstance(fc, dict) else ""
    src_s = str(fc.get("source_candidate_sha256") or "") if isinstance(fc, dict) else ""
    para1 = (
        "V15-M41 packages the completed V15-M39 two-hour run for future evaluation routing. "
        "It does not execute benchmark matches, evaluate strength, promote checkpoints, "
        "produce scorecard results, run XAI or human-panel evaluation, release a showcase "
        "agent, authorize v2, or execute T2/T3."
    )
    fn_main = FILENAME_MAIN_JSON
    fn_idx = CANDIDATE_INDEX_FILENAME
    footer = f"See `{fn_main}` for the sealed contract body and `{fn_idx}` for roles."
    return f"""# V15-M41 — evaluation readiness packet

{para1}

| Field | Value |
| --- | --- |
| package_status | `{st}` |
| M39 receipt SHA-256 | `{m39_sha}` |
| source_candidate_sha256 (lineage anchor) | `{src_s}` |
| final_candidate_sha256 (two-hour candidate) | `{final_s}` |
| promotion | candidate-only — not promoted in this milestone |

{footer}
"""


def _candidate_index(
    sealed: dict[str, Any],
    *,
    final_file_basename: str | None,
    final_file_sha256: str | None,
    final_file_hashing_authorized: bool,
) -> dict[str, Any]:
    fc = sealed.get("candidate_checkpoint") or {}
    src = str(fc.get("source_candidate_sha256") or "") if isinstance(fc, dict) else ""
    fin = str(fc.get("final_candidate_sha256") or "") if isinstance(fc, dict) else ""
    entry_file: dict[str, Any] | None = None
    if final_file_basename:
        entry_file = {"path_basename_only": final_file_basename}
        if final_file_hashing_authorized and final_file_sha256:
            entry_file["file_sha256"] = final_file_sha256
        else:
            entry_file["file_sha256"] = None
            entry_file["note"] = "hashing_not_authorized_or_not_computed"
    return {
        "milestone": MILESTONE_LABEL_M41,
        "contract_id": CONTRACT_ID_M41,
        "profile_id": PROFILE_M41,
        "package_status": sealed.get("package_status"),
        "candidates": [
            {
                "role": "source_candidate_lineage_anchor",
                "sha256": src,
                "promotion_status": "not_promoted_candidate_only",
            },
            {
                "role": "final_two_hour_candidate_checkpoint",
                "sha256": fin,
                "promotion_status": "not_promoted_candidate_only",
            },
        ],
        "final_checkpoint_file": entry_file,
    }


def _inventory_has_final_sha(inv: dict[str, Any], final_sha: str) -> bool:
    fin = str(final_sha or "").strip().lower()
    rows = inv.get("checkpoint_files")
    if not isinstance(rows, list):
        return False
    for r in rows:
        if not isinstance(r, dict):
            continue
        if str(r.get("sha256") or "").strip().lower() == fin:
            return True
    return False


def _m39_claim_subset_ok(m39: dict[str, Any]) -> bool:
    cf = m39.get("claim_flags")
    if not isinstance(cf, dict):
        return False
    for k in M39_CLAIM_KEYS_MUST_REMAIN_FALSE:
        if cf.get(k) is not False:
            return False
    return True


def _retention_ok(m39: dict[str, Any]) -> bool:
    cr = m39.get("checkpoint_retention")
    if not isinstance(cr, dict):
        return False
    if cr.get("checkpoint_retention_max_retained") is None:
        return False
    if cr.get("checkpoints_written_total") is None:
        return False
    if cr.get("checkpoints_pruned_total") is None:
        return False
    if cr.get("final_step_checkpoint_persisted") is None:
        return False
    return True


def _run_summary_from_m39(m39: dict[str, Any]) -> dict[str, Any]:
    et = m39.get("execution_telemetry") or {}
    if not isinstance(et, dict):
        et = {}
    return {
        "target_wall_clock_seconds": int(m39.get("target_wall_clock_seconds") or 0),
        "observed_wall_clock_seconds": float(m39.get("observed_wall_clock_seconds") or 0.0),
        "training_update_count": int(et.get("training_update_count") or 0),
        "sc2_backed_features_used": bool(et.get("sc2_backed_features_used")),
    }


def _retention_summary_from_m39(m39: dict[str, Any]) -> dict[str, Any]:
    cr = m39.get("checkpoint_retention") or {}
    if not isinstance(cr, dict):
        cr = {}
    return {
        "checkpoint_retention_max_retained": int(cr.get("checkpoint_retention_max_retained") or 0),
        "checkpoints_written_total": int(cr.get("checkpoints_written_total") or 0),
        "checkpoints_pruned_total": int(cr.get("checkpoints_pruned_total") or 0),
        "final_step_checkpoint_persisted": bool(cr.get("final_step_checkpoint_persisted")),
    }


def build_fixture_m41_body() -> dict[str, Any]:
    gates = _gate_pack(
        p0=False,
        p1=False,
        p2=False,
        p3=False,
        p4=False,
        p5=False,
        p6=False,
        p7=False,
        p8=True,
        p9=True,
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M41,
        "profile_id": PROFILE_M41,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M41,
        "emitter_module": EMITTER_MODULE_M41,
        "package_status": STATUS_FIXTURE_ONLY,
        "evaluation_ready": False,
        "upstream_bindings": {
            "m39_two_hour_operator_run": {
                "artifact_sha256": None,
                "contract_id": CONTRACT_ID_M39,
                "profile_id": PROFILE_M39,
                "run_status": None,
                "full_wall_clock_satisfied": None,
            },
        },
        "run_summary": {
            "target_wall_clock_seconds": 7200,
            "observed_wall_clock_seconds": 0.0,
            "training_update_count": 0,
            "sc2_backed_features_used": False,
        },
        "candidate_checkpoint": {
            "source_candidate_sha256": SOURCE_CANDIDATE_LINEAGE_SHA256,
            "final_candidate_sha256": None,
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_blob_loaded": False,
            "torch_load_performed": False,
        },
        "retention_summary": {
            "checkpoint_retention_max_retained": 0,
            "checkpoints_written_total": 0,
            "checkpoints_pruned_total": 0,
            "final_step_checkpoint_persisted": False,
        },
        "evidence_completeness": {
            "m39_receipt_bound": False,
            "telemetry_summary_bound": False,
            "checkpoint_inventory_bound": False,
            "transcript_present": False,
            "private_paths_redacted_from_public_fields": True,
        },
        "gates": gates,
        "claim_flags": _claim_flags_all_false_m41(),
        "non_claims": list(NON_CLAIMS_M41),
        "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
    }


@dataclass(frozen=True)
class OperatorInputs:
    m39_run_json: Path
    m39_telemetry_summary_json: Path
    m39_checkpoint_inventory_json: Path
    m39_transcript: Path
    expected_m39_artifact_sha256: str
    expected_final_candidate_sha256: str
    authorize_final_checkpoint_file_sha256: bool
    final_candidate_checkpoint_path: Path | None


def evaluate_operator_package(
    repo_root: Path,
    inputs: OperatorInputs,
) -> tuple[dict[str, Any], list[str], str | None, str | None]:
    """Return (body_pre_redact, warnings, final_basename, final_file_sha)."""
    _ = repo_root
    warnings: list[str] = []
    final_basename: str | None = None
    final_sha_file: str | None = None

    fp = inputs.final_candidate_checkpoint_path
    if fp is not None:
        p = Path(fp)
        if p.is_file():
            final_basename = p.name
            if inputs.authorize_final_checkpoint_file_sha256:
                final_sha_file = sha256_file_hex(p)
            else:
                warnings.append("final_checkpoint_path_present_without_hash_authorization")
        else:
            warnings.append("final_checkpoint_path_missing_on_disk")

    m39_path = inputs.m39_run_json
    if not m39_path.is_file():
        body = build_fixture_m41_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_MISSING_M39
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        return body, warnings, final_basename, final_sha_file

    try:
        m39 = _parse_json_object(m39_path.resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        body = build_fixture_m41_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_INVALID_M39
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        return body, warnings, final_basename, final_sha_file

    exp_digest = str(inputs.expected_m39_artifact_sha256 or "").strip().lower()
    if not _is_hex64(exp_digest):
        body = build_fixture_m41_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_INVALID_M39
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        return body, warnings, final_basename, final_sha_file

    if not _canonical_seal_ok(m39):
        body = build_fixture_m41_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_INVALID_M39
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        return body, warnings, final_basename, final_sha_file

    digest_in_file = str(m39.get(GATE_ARTIFACT_DIGEST_FIELD) or "").strip().lower()
    if digest_in_file != exp_digest:
        body = build_fixture_m41_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_INVALID_M39
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        return body, warnings, final_basename, final_sha_file

    p0 = True
    p1 = (
        str(m39.get("contract_id") or "") == CONTRACT_ID_M39
        and str(
            m39.get("profile_id") or "",
        )
        == PROFILE_M39
    )
    run_st = str(m39.get("run_status") or "")
    p2 = run_st == STATUS_RUN_COMPLETED_WITH_CKPT
    p3 = m39.get("full_wall_clock_satisfied") is True

    cc = m39.get("candidate_checkpoint") or {}
    if not isinstance(cc, dict):
        cc = {}
    src_in_m39 = str(cc.get("source_candidate_sha256") or "").strip().lower()
    final_in_m39 = str(cc.get("final_candidate_sha256") or "").strip().lower()
    exp_final = str(inputs.expected_final_candidate_sha256 or "").strip().lower()

    if _is_hex64(src_in_m39) and src_in_m39 != SOURCE_CANDIDATE_LINEAGE_SHA256.lower():
        warnings.append("m39_source_candidate_sha_differs_from_public_lineage_anchor")

    p5 = _retention_ok(m39)
    p7 = _m39_claim_subset_ok(m39)

    tel_ok = inputs.m39_telemetry_summary_json.is_file()
    tel_parsed = False
    if tel_ok:
        try:
            tel_obj = _parse_json_object(inputs.m39_telemetry_summary_json.resolve())
            tel_parsed = isinstance(tel_obj, dict)
        except (OSError, ValueError, json.JSONDecodeError):
            tel_parsed = False

    inv_ok = inputs.m39_checkpoint_inventory_json.is_file()
    inv: dict[str, Any] = {}
    inv_parsed = False
    if inv_ok:
        try:
            inv = _parse_json_object(inputs.m39_checkpoint_inventory_json.resolve())
            inv_parsed = isinstance(inv, dict)
        except (OSError, ValueError, json.JSONDecodeError):
            inv = {}
            inv_parsed = False

    tr_ok = inputs.m39_transcript.is_file() and inputs.m39_transcript.stat().st_size > 0

    sha_matches_expected = (
        _is_hex64(final_in_m39) and _is_hex64(exp_final) and (final_in_m39 == exp_final)
    )
    in_inventory = inv_parsed and _inventory_has_final_sha(inv, exp_final)
    p4 = sha_matches_expected and in_inventory

    p6 = tel_ok and tel_parsed and inv_ok and inv_parsed and tr_ok

    p8 = True
    p9 = True

    package_status = STATUS_READY
    if not p1:
        package_status = STATUS_BLOCKED_INVALID_M39
    elif not p2 or not p3:
        package_status = STATUS_BLOCKED_M39_NOT_COMPLETED
    elif not _is_hex64(exp_final):
        package_status = STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH
    elif not tel_ok or not tel_parsed:
        package_status = STATUS_BLOCKED_MISSING_TELEMETRY
    elif not inv_ok or not inv_parsed:
        package_status = STATUS_BLOCKED_MISSING_INVENTORY
    elif not sha_matches_expected:
        package_status = STATUS_BLOCKED_CANDIDATE_SHA_MISMATCH
    elif not in_inventory:
        package_status = STATUS_BLOCKED_MISSING_INVENTORY
    elif not tr_ok:
        package_status = STATUS_BLOCKED_MISSING_TRANSCRIPT
    elif not p5:
        package_status = STATUS_BLOCKED_INVALID_M39
    elif not p7:
        package_status = STATUS_BLOCKED_INVALID_M39
    else:
        package_status = STATUS_READY
        if warnings:
            package_status = STATUS_READY_WARNINGS

    evaluation_ready = package_status in (STATUS_READY, STATUS_READY_WARNINGS)

    evidence = {
        "m39_receipt_bound": p0 and p1,
        "telemetry_summary_bound": tel_ok and tel_parsed,
        "checkpoint_inventory_bound": inv_ok and inv_parsed,
        "transcript_present": tr_ok,
        "private_paths_redacted_from_public_fields": True,
    }

    tr_sz = int(inputs.m39_transcript.stat().st_size) if tr_ok else 0

    transcript_meta = {
        "transcript_present": tr_ok,
        "transcript_size_bytes": tr_sz,
        "transcript_contents_not_copied_to_package_json": True,
    }

    final_for_body = final_in_m39 if _is_hex64(final_in_m39) else None

    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M41,
        "profile_id": PROFILE_M41,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M41,
        "emitter_module": EMITTER_MODULE_M41,
        "package_status": package_status,
        "evaluation_ready": evaluation_ready,
        "upstream_bindings": {
            "m39_two_hour_operator_run": {
                "artifact_sha256": digest_in_file,
                "contract_id": CONTRACT_ID_M39,
                "profile_id": PROFILE_M39,
                "run_status": run_st,
                "full_wall_clock_satisfied": bool(m39.get("full_wall_clock_satisfied")),
            },
        },
        "run_summary": _run_summary_from_m39(m39),
        "candidate_checkpoint": {
            "source_candidate_sha256": SOURCE_CANDIDATE_LINEAGE_SHA256,
            "final_candidate_sha256": final_for_body,
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_blob_loaded": False,
            "torch_load_performed": False,
        },
        "retention_summary": _retention_summary_from_m39(m39),
        "evidence_completeness": evidence,
        "transcript_metadata": transcript_meta,
        "gates": _gate_pack(
            p0=p0,
            p1=p1,
            p2=p2,
            p3=p3,
            p4=p4,
            p5=p5,
            p6=p6,
            p7=p7,
            p8=p8,
            p9=p9,
        ),
        "claim_flags": _claim_flags_all_false_m41(),
        "non_claims": list(NON_CLAIMS_M41),
        "recommended_next": (
            RECOMMENDED_NEXT_SUCCESS if evaluation_ready else RECOMMENDED_NEXT_REMEDIATION
        ),
    }

    return result, warnings, final_basename, final_sha_file


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M41 emission leaked path patterns into public artifacts")


def emit_m41_fixture(
    output_dir: Path, *, repo_root: Path
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    _ = repo_root
    body_pre = build_fixture_m41_body()
    sealed = seal_m41_body(redact_paths_in_value(body_pre))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m41_report(sealed)
    chk = build_m41_checklist_md(sealed)
    pkt = _build_evaluation_packet_md(sealed)
    idx = _candidate_index(
        sealed,
        final_file_basename=None,
        final_file_sha256=None,
        final_file_hashing_authorized=False,
    )

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkt = output_dir / PACKET_FILENAME
    p_idx = output_dir / CANDIDATE_INDEX_FILENAME

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_pkt.write_text(pkt, encoding="utf-8", newline="\n")
    p_idx.write_text(canonical_json_dumps(idx), encoding="utf-8")

    blob = (
        canonical_json_dumps(sealed)
        + canonical_json_dumps(rep)
        + chk
        + pkt
        + canonical_json_dumps(idx)
    )
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_chk, p_pkt, p_idx)


def emit_m41_operator_preflight(
    output_dir: Path,
    *,
    repo_root: Path,
    inputs: OperatorInputs,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body_pre, warnings, fb, fsha = evaluate_operator_package(repo_root, inputs)

    if warnings:
        body_pre["noncritical_warnings"] = list(warnings)

    sealed = seal_m41_body(redact_paths_in_value(body_pre))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m41_report(sealed)
    chk = build_m41_checklist_md(sealed)
    pkt = _build_evaluation_packet_md(sealed)
    idx = _candidate_index(
        sealed,
        final_file_basename=fb,
        final_file_sha256=fsha,
        final_file_hashing_authorized=inputs.authorize_final_checkpoint_file_sha256,
    )

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkt = output_dir / PACKET_FILENAME
    p_idx = output_dir / CANDIDATE_INDEX_FILENAME

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_pkt.write_text(pkt, encoding="utf-8", newline="\n")
    p_idx.write_text(canonical_json_dumps(idx), encoding="utf-8")

    blob = (
        canonical_json_dumps(sealed)
        + canonical_json_dumps(rep)
        + chk
        + pkt
        + canonical_json_dumps(idx)
    )
    _assert_no_path_leak(blob)
    return sealed, (p_main, p_rep, p_chk, p_pkt, p_idx)


__all__ = [
    "OperatorInputs",
    "build_fixture_m41_body",
    "build_m41_report",
    "build_m41_checklist_md",
    "emit_m41_fixture",
    "emit_m41_operator_preflight",
    "evaluate_operator_package",
    "seal_m41_body",
    "sha256_file_hex",
]
