"""V15-M42 — candidate checkpoint evaluation package from governed M41 run package."""

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
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M39_GATE_FIELD,
)
from starlab.v15.m41_two_hour_run_package_evaluation_readiness_models import (
    CONTRACT_ID_M41,
    PROFILE_M41,
)
from starlab.v15.m42_two_hour_candidate_checkpoint_evaluation_package_models import (
    ANCHOR_FINAL_CANDIDATE_SHA256,
    BINDINGS_INDEX_FILENAME,
    CHECKLIST_FILENAME,
    CONTRACT_ID_EVAL_PACKAGE_FAMILY,
    EMITTER_MODULE_M42,
    EXPECTED_M41_SHA_CLI_MISMATCH,
    EXPECTED_M41_SHA_OPTIONAL_NOT_SUPPLIED,
    EXPECTED_M41_SHA_VERIFIED_MATCH,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M41_READY_STATUSES,
    MILESTONE_LABEL_M42,
    NON_CLAIMS_M42,
    PROFILE_FIXTURE_CI,
    PROFILE_M42,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    ROUTING_PACKET_FILENAME,
    SCHEMA_VERSION,
    SOURCE_CANDIDATE_LINEAGE_SHA256,
    STATUS_BLOCKED_FINAL_MISMATCH,
    STATUS_BLOCKED_INVALID_M05,
    STATUS_BLOCKED_INVALID_M41,
    STATUS_BLOCKED_M39_RECEIPT_MISMATCH,
    STATUS_BLOCKED_M41_NOT_READY,
    STATUS_BLOCKED_MISSING_FINAL_INDEX,
    STATUS_BLOCKED_MISSING_M41,
    STATUS_BLOCKED_SOURCE_MISMATCH,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
    STATUS_READY_WARNINGS,
)
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
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


def _canonical_seal_ok_m41(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(GATE_ARTIFACT_DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _canonical_seal_ok_m05(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(SEAL_KEY_STRONG_AGENT)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != SEAL_KEY_STRONG_AGENT}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _canonical_seal_ok_using(raw: dict[str, Any], seal_key: str) -> bool:
    seal_in = raw.get(seal_key)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != seal_key}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def sha256_file_hex(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fb:
        while chunk := fb.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def _json_file_canonical_sha256_plain(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def _claim_flags_all_false_m42() -> dict[str, bool]:
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


def seal_m42_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def build_m42_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_m42_two_hour_candidate_checkpoint_evaluation_package_report",
        "report_version": "m42",
        "milestone": MILESTONE_LABEL_M42,
        "contract_id": CONTRACT_ID_EVAL_PACKAGE_FAMILY,
        "package_profile_id": PROFILE_M42,
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
    p10: bool,
) -> list[dict[str, Any]]:
    return [
        {"gate_id": "P0", "name": "M41 package bound", "passed": p0},
        {"gate_id": "P1", "name": "M41 status ready", "passed": p1},
        {"gate_id": "P2", "name": "M39 receipt inherited", "passed": p2},
        {"gate_id": "P3", "name": "Source candidate bound", "passed": p3},
        {"gate_id": "P4", "name": "Final candidate bound", "passed": p4},
        {"gate_id": "P5", "name": "Candidate role valid", "passed": p5},
        {"gate_id": "P6", "name": "Evidence companions bound", "passed": p6},
        {"gate_id": "P7", "name": "Optional M05 protocol valid", "passed": p7},
        {"gate_id": "P8", "name": "Public/private boundary", "passed": p8},
        {"gate_id": "P9", "name": "Non-claims preserved", "passed": p9},
        {"gate_id": "P10", "name": "Evaluation routing only", "passed": p10},
    ]


def build_m42_checklist_md(sealed: dict[str, Any]) -> str:
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
    return f"""# V15-M42 — two-hour candidate checkpoint evaluation package checklist

**`package_status`:** `{st}`

## Gate pack (P0–P10)

| Gate | Name | Pass |
| --- | --- | --- |
{gate_lines}
## Non-claims

{nc_lines}

## Artifacts

- `{FILENAME_MAIN_JSON}`
- `{REPORT_FILENAME}`
- `{CHECKLIST_FILENAME}`
- `{ROUTING_PACKET_FILENAME}`
- `{BINDINGS_INDEX_FILENAME}`
"""


def _routing_packet_md(sealed: dict[str, Any]) -> str:
    st = sealed.get("package_status")
    er = sealed.get("evaluation_routing") or {}
    rec = ""
    blk: list[Any] = []
    if isinstance(er, dict):
        rec = str(er.get("recommended_next") or "")
        br = er.get("blocked_reasons")
        blk = list(br) if isinstance(br, list) else []

    fc = sealed.get("candidate_checkpoint") or {}
    final_s = str(fc.get("final_candidate_sha256") or "") if isinstance(fc, dict) else ""

    ub = sealed.get("upstream_bindings") or {}
    m41_sha = ""
    if isinstance(ub, dict):
        mb = ub.get("m41_two_hour_run_package") or {}
        if isinstance(mb, dict):
            m41_sha = str(mb.get("artifact_sha256") or "")

    para = (
        "V15-M42 assembles the final candidate checkpoint from the completed V15-M39 "
        "two-hour run into a governed candidate-checkpoint evaluation package for future "
        "evaluation routing. It does not execute benchmark matches, evaluate strength, promote "
        "checkpoints, produce scorecard results, call torch.load, load checkpoint blobs, "
        "run XAI or human-panel evaluation, release a showcase agent, authorize v2, "
        "or execute T2/T3."
    )
    blk_txt = ", ".join(str(x) for x in blk) if blk else "(none)"
    return f"""# V15-M42 — candidate evaluation routing packet

{para}

| Field | Value |
| --- | --- |
| package_status | `{st}` |
| sealed M41 package artifact SHA-256 | `{m41_sha}` |
| final_candidate_sha256 (metadata) | `{final_s}` |
| recommended_next | `{rec}` |
| blocked_reasons | {blk_txt} |

See `{FILENAME_MAIN_JSON}` for the sealed contract body and
`{BINDINGS_INDEX_FILENAME}` for bindings.
"""


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


def _bindings_index(
    sealed: dict[str, Any],
    *,
    m05_binding: dict[str, Any],
    inherited_m05_note: str | None,
    final_ckpt_basename: str | None,
    final_ckpt_file_sha256: str | None,
    file_verify: bool,
    final_ckpt_binding_status: str | None,
) -> dict[str, Any]:
    fc = sealed.get("candidate_checkpoint") or {}
    src = str(fc.get("source_candidate_sha256") or "") if isinstance(fc, dict) else ""
    fin = str(fc.get("final_candidate_sha256") or "") if isinstance(fc, dict) else ""

    ub = sealed.get("upstream_bindings") or {}
    m41_entry: dict[str, Any] = {}
    m39_digest = ""
    if isinstance(ub, dict):
        m41b = ub.get("m41_two_hour_run_package") or {}
        if isinstance(m41b, dict):
            m41_entry = {
                "artifact_sha256": m41b.get("artifact_sha256"),
                "package_status": m41b.get("package_status"),
                "contract_id": m41b.get("contract_id"),
                "profile_id": m41b.get("profile_id"),
            }
        m39b = ub.get("m39_two_hour_run_receipt") or {}
        if isinstance(m39b, dict):
            m39_digest = str(m39b.get("artifact_sha256") or "")

    return {
        "milestone": MILESTONE_LABEL_M42,
        "contract_id": CONTRACT_ID_EVAL_PACKAGE_FAMILY,
        "package_profile_id": PROFILE_M42,
        "package_status": sealed.get("package_status"),
        "m41_binding": m41_entry,
        "m39_receipt_sha256_expected": m39_digest,
        "candidate_roles": [
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
        "m05_scorecard_binding": m05_binding,
        "m05_inherited_from_m41_note": inherited_m05_note,
        "final_checkpoint_file": (
            None
            if not final_ckpt_basename
            else {
                "path_basename_only": final_ckpt_basename,
                "file_sha256": final_ckpt_file_sha256,
                "checkpoint_file_sha256_verified_vs_expected_final": file_verify,
                "binding_detail": final_ckpt_binding_status,
            }
        ),
    }


def build_fixture_m42_body() -> dict[str, Any]:
    gates = _gate_pack(
        p0=False,
        p1=False,
        p2=False,
        p3=False,
        p4=False,
        p5=False,
        p6=False,
        p7=True,
        p8=True,
        p9=True,
        p10=True,
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_EVAL_PACKAGE_FAMILY,
        "package_profile_id": PROFILE_M42,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M42,
        "emitter_module": EMITTER_MODULE_M42,
        "package_status": STATUS_FIXTURE_ONLY,
        "evaluation_package_ready": False,
        "expected_m41_package_sha256_status": EXPECTED_M41_SHA_OPTIONAL_NOT_SUPPLIED,
        "upstream_bindings": {
            "m41_two_hour_run_package": {
                "artifact_sha256": None,
                "contract_id": CONTRACT_ID_M41,
                "profile_id": PROFILE_M41,
                "package_status": None,
            },
            "m39_two_hour_run_receipt": {
                "artifact_sha256": None,
                "run_status": None,
                "full_wall_clock_satisfied": None,
            },
            "m05_scorecard_protocol": {
                "binding_status": "optional_not_supplied",
            },
        },
        "candidate_checkpoint": {
            "source_candidate_sha256": SOURCE_CANDIDATE_LINEAGE_SHA256,
            "final_candidate_sha256": ANCHOR_FINAL_CANDIDATE_SHA256,
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
            "telemetry_summary_bound": False,
            "checkpoint_inventory_bound": False,
            "transcript_metadata_bound": False,
            "retention_counters_bound": False,
        },
        "evaluation_routing": {
            "ready_for_m43_bounded_evaluation_gate": False,
            "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
            "blocked_reasons": ["fixture_schema_only_no_operator_package"],
        },
        "gates": gates,
        "claim_flags": _claim_flags_all_false_m42(),
        "non_claims": list(NON_CLAIMS_M42),
        "cross_check_hints": {},
    }


@dataclass(frozen=True)
class M42OperatorInputs:
    m41_package_json: Path
    expected_m41_package_sha256: str | None
    expected_m39_artifact_sha256: str
    expected_source_candidate_sha256: str
    expected_final_candidate_sha256: str
    m39_run_json: Path | None
    m39_checkpoint_inventory_json: Path | None
    m39_telemetry_summary_json: Path | None
    m05_scorecard_json: Path | None
    authorize_final_checkpoint_file_sha256: bool
    final_candidate_checkpoint_path: Path | None
    ancillary_m39_present_without_m41: bool


def _extract_m41_m05_upstream(m41: dict[str, Any]) -> tuple[dict[str, Any] | None, bool]:
    """Return (binding dict subset, recognized) — no filesystem discovery."""
    ub = m41.get("upstream_bindings")
    if not isinstance(ub, dict):
        return None, False
    for key in ("m05_strong_agent_scorecard_protocol", "m05_scorecard_protocol"):
        cand = ub.get(key)
        if isinstance(cand, dict) and cand.get("contract_id") == CONTRACT_ID_STRONG_AGENT_SCORECARD:
            return cand, True
        if (
            isinstance(cand, dict)
            and cand.get(
                "artifact_sha256",
            )
            not in (None, "")
            and cand.get(
                "binding_status",
                "",
            ).startswith(
                ("bound_", "inherit"),
            )
        ):
            return cand, True
    nested = ub.get("m41_protocol_bindings") or ub.get("optional_protocol_bindings")
    if isinstance(nested, dict):
        mc = nested.get("m05") or nested.get("m05_scorecard")
        if isinstance(mc, dict) and mc.get("contract_id") == CONTRACT_ID_STRONG_AGENT_SCORECARD:
            return mc, True
    return None, False


def _evaluate_operator_m42(
    repo_root: Path, inp: M42OperatorInputs
) -> tuple[dict[str, Any], str | None]:
    """Build un-redacted operator body and optional M41-inherited M05 note."""
    _ = repo_root

    warnings: list[str] = []
    ancillary = inp.ancillary_m39_present_without_m41

    final_file_sha: str | None = None
    final_ckpt_binding_status: str | None = None
    ckpt_path_ok = inp.final_candidate_checkpoint_path
    if ckpt_path_ok is not None:
        p_ck = Path(ckpt_path_ok)
        if p_ck.is_file():
            if inp.authorize_final_checkpoint_file_sha256:
                final_file_sha = sha256_file_hex(p_ck)
            else:
                warnings.append(
                    "final_candidate_checkpoint_path_supplied_but_not_hashed",
                )
                final_ckpt_binding_status = (
                    "final_candidate_checkpoint_path_supplied_but_not_hashed"
                )
        else:
            warnings.append("final_checkpoint_path_missing_on_disk")

    fp = inp.m41_package_json
    if not fp.is_file():
        hint: dict[str, Any] = {}
        if ancillary:
            hint["direct_m39_operator_artifacts_seen_but_insufficient_without_m41"] = True
        body = build_fixture_m42_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_MISSING_M41
        body["evaluation_routing"] = {
            "ready_for_m43_bounded_evaluation_gate": False,
            "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
            "blocked_reasons": [STATUS_BLOCKED_MISSING_M41],
        }
        body["gates"] = _gate_pack(
            p0=False,
            p1=False,
            p2=False,
            p3=False,
            p4=False,
            p5=False,
            p6=False,
            p7=True,
            p8=True,
            p9=True,
            p10=False,
        )
        if hint:
            body["cross_check_hints"] = hint
        if warnings:
            body.setdefault("noncritical_warnings", []).extend(warnings)
        return body, None

    exp_m41_status = EXPECTED_M41_SHA_OPTIONAL_NOT_SUPPLIED
    try:
        m41_raw = _parse_json_object(Path(fp).resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        body = build_fixture_m42_body()
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["package_status"] = STATUS_BLOCKED_INVALID_M41
        body["expected_m41_package_sha256_status"] = exp_m41_status
        body["evaluation_routing"] = {
            "ready_for_m43_bounded_evaluation_gate": False,
            "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
            "blocked_reasons": [STATUS_BLOCKED_INVALID_M41],
        }
        body["gates"] = _gate_pack(
            p0=False,
            p1=False,
            p2=False,
            p3=False,
            p4=False,
            p5=False,
            p6=False,
            p7=True,
            p8=True,
            p9=True,
            p10=False,
        )
        if warnings:
            body.setdefault("noncritical_warnings", []).extend(warnings)
        return body, None

    if (
        str(m41_raw.get("contract_id") or "") != CONTRACT_ID_M41
        or str(
            m41_raw.get("profile_id") or "",
        )
        != PROFILE_M41
    ):
        body = _blocked_body_early(
            STATUS_BLOCKED_INVALID_M41,
            warnings,
            exp_m41_status,
            m41_raw if _canonical_seal_ok_m41(m41_raw) else None,
        )
        return body, None

    if not _canonical_seal_ok_m41(m41_raw):
        body = _blocked_body_early(
            STATUS_BLOCKED_INVALID_M41,
            warnings,
            exp_m41_status,
            None,
        )
        return body, None

    digest_file = str(m41_raw[GATE_ARTIFACT_DIGEST_FIELD]).strip().lower()

    exp_m41_opt = inp.expected_m41_package_sha256
    if exp_m41_opt:
        eo = str(exp_m41_opt).strip().lower()
        if _is_hex64(eo) and eo == digest_file:
            exp_m41_status = EXPECTED_M41_SHA_VERIFIED_MATCH
        elif _is_hex64(eo) and eo != digest_file:
            body = build_fixture_m42_body()
            body["profile"] = PROFILE_OPERATOR_PREFLIGHT
            body["package_status"] = STATUS_BLOCKED_INVALID_M41
            body["expected_m41_package_sha256_status"] = EXPECTED_M41_SHA_CLI_MISMATCH
            body["evaluation_routing"] = {
                "ready_for_m43_bounded_evaluation_gate": False,
                "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
                "blocked_reasons": [
                    "cli_expected_m41_package_sha256_mismatch",
                    STATUS_BLOCKED_INVALID_M41,
                ],
            }
            body["gates"] = _gate_pack(
                p0=True,
                p1=False,
                p2=False,
                p3=False,
                p4=False,
                p5=False,
                p6=False,
                p7=True,
                p8=True,
                p9=True,
                p10=False,
            )
            body["upstream_bindings"] = _upstream_from_m41(
                m41_raw,
                m41_digest=digest_file,
            )
            body["evaluation_package_ready"] = False
            if warnings:
                body.setdefault("noncritical_warnings", []).extend(warnings)
            return body, None

    pkg_st = str(m41_raw.get("package_status") or "")
    if not inp.expected_m41_package_sha256:
        exp_m41_status = EXPECTED_M41_SHA_OPTIONAL_NOT_SUPPLIED

    p0 = True
    p1 = pkg_st in M41_READY_STATUSES

    ub_m39_expected = (
        str(
            ((m41_raw.get("upstream_bindings") or {}).get("m39_two_hour_operator_run") or {}).get(
                "artifact_sha256"
            )
            or ""
        )
        .strip()
        .lower()
        if isinstance(m41_raw.get("upstream_bindings"), dict)
        else ""
    )

    cc = m41_raw.get("candidate_checkpoint") or {}
    cc = cc if isinstance(cc, dict) else {}

    src_m41 = str(cc.get("source_candidate_sha256") or "").strip().lower()
    final_m41 = str(cc.get("final_candidate_sha256") or "").strip().lower()

    exp_m39_cli = str(inp.expected_m39_artifact_sha256).strip().lower()
    exp_src_cli = str(inp.expected_source_candidate_sha256).strip().lower()
    exp_final_cli = str(inp.expected_final_candidate_sha256).strip().lower()

    p2 = bool(
        ub_m39_expected and _is_hex64(ub_m39_expected) and ub_m39_expected == exp_m39_cli,
    )
    p3 = bool(
        src_m41 and _is_hex64(exp_src_cli) and src_m41 == exp_src_cli,
    )
    p4 = bool(
        final_m41
        and _is_hex64(exp_final_cli)
        and final_m41 == exp_final_cli
        and _is_hex64(exp_final_cli),
    )
    promo = str(cc.get("promotion_status") or "")
    blob_loaded = cc.get("checkpoint_blob_loaded") is True
    torch_lp = cc.get("torch_load_performed") is True
    p5 = promo == "not_promoted_candidate_only" and not blob_loaded and not torch_lp

    ev = m41_raw.get("evidence_completeness") or {}
    ev = ev if isinstance(ev, dict) else {}

    telemetry_ok = bool(ev.get("telemetry_summary_bound"))
    inv_ok_ev = bool(ev.get("checkpoint_inventory_bound"))
    trans_ok = bool(ev.get("transcript_present"))

    rs = m41_raw.get("retention_summary") or {}
    rs = rs if isinstance(rs, dict) else {}
    retention_ok = (
        rs.get("checkpoint_retention_max_retained") is not None
        and rs.get("checkpoints_written_total") is not None
        and rs.get("checkpoints_pruned_total") is not None
        and rs.get("final_step_checkpoint_persisted") is not None
    )
    p6 = telemetry_ok and inv_ok_ev and trans_ok and retention_ok

    m05_upstream, _upstream_rec = _extract_m41_m05_upstream(m41_raw)
    inherited_m05_note: str | None = None

    cf_m41_raw = _claim_flags_all_false_m42()
    m41_claims = m41_raw.get("claim_flags")
    p9_ok = isinstance(m41_claims, dict) and all(m41_claims.get(k) is False for k in cf_m41_raw)

    p7_fail_m05_supplied = False
    m05_binding: dict[str, Any] = {"binding_status": "optional_not_supplied"}

    cli_m05_provided = inp.m05_scorecard_json is not None and inp.m05_scorecard_json.is_file()
    cli_m05_obj: dict[str, Any] | None = None
    cli_m05_digest: str | None = None
    if cli_m05_provided and inp.m05_scorecard_json is not None:
        try:
            cli_m05_obj = _parse_json_object(inp.m05_scorecard_json.resolve())
            cli_m05_digest = _json_file_canonical_sha256_plain(inp.m05_scorecard_json.resolve())
        except (OSError, ValueError, json.JSONDecodeError):
            cli_m05_obj = None
            cli_m05_digest = None
            p7_fail_m05_supplied = True

    if cli_m05_provided and cli_m05_obj is None:
        p7_fail_m05_supplied = True
        m05_binding = {
            "binding_status": "operator_supplied_invalid",
            "artifact_sha256": cli_m05_digest,
        }
    elif cli_m05_obj is not None:
        if str(cli_m05_obj.get("contract_id") or "") != CONTRACT_ID_STRONG_AGENT_SCORECARD:
            p7_fail_m05_supplied = True
        else:
            prof = cli_m05_obj.get("protocol_profile_id")
            if prof is not None and str(prof) != PROTOCOL_PROFILE_ID:
                p7_fail_m05_supplied = True
            elif not _canonical_seal_ok_m05(cli_m05_obj):
                p7_fail_m05_supplied = True
        if p7_fail_m05_supplied:
            m05_binding = {
                "binding_status": "operator_supplied_invalid",
                "artifact_sha256": cli_m05_digest,
            }
        else:
            m05_binding = {
                "binding_status": "bound_operator_supplied_cli",
                "artifact_sha256": cli_m05_digest,
                "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
                "protocol_profile_id": str(
                    cli_m05_obj.get("protocol_profile_id") or PROTOCOL_PROFILE_ID,
                ),
            }
    elif m05_upstream is not None:
        inherited_m05_note = "inherited_from_m41_upstream_bindings"
        m05_binding = {
            "binding_status": "optional_inherited_from_m41",
            **m05_upstream,
        }

    if cli_m05_provided:
        p7 = not p7_fail_m05_supplied
    else:
        p7 = True

    p8 = True
    p10 = True

    _optional_m39_issues: list[str] = []
    if inp.m39_run_json is not None and inp.m39_run_json.is_file():
        try:
            m39_cross = _parse_json_object(inp.m39_run_json.resolve())
        except (OSError, ValueError, json.JSONDecodeError):
            m39_cross = {}
            _optional_m39_issues.append("cross_check_m39_json_unreadable")
            p8 = False
        if isinstance(m39_cross, dict):
            if not _canonical_seal_ok_using(m39_cross, M39_GATE_FIELD):
                _optional_m39_issues.append("cross_check_m39_seal_invalid")
                p8 = False
            wo = str(m39_cross.get(M39_GATE_FIELD, "")).strip().lower()
            if _is_hex64(exp_m39_cli) and wo and wo != exp_m39_cli:
                _optional_m39_issues.append("cross_check_m39_digest_mismatch_vs_cli_expected")
                p8 = False

            raw_cc = m39_cross.get("candidate_checkpoint")
            mcc = raw_cc if isinstance(raw_cc, dict) else {}
            fs = str(mcc.get("final_candidate_sha256") or "").strip().lower()
            ss = str(mcc.get("source_candidate_sha256") or "").strip().lower()
            if fs and exp_final_cli and fs != exp_final_cli:
                _optional_m39_issues.append("cross_check_m39_final_sha_mismatch")
                p8 = False
            if ss and exp_src_cli and ss != exp_src_cli:
                _optional_m39_issues.append("cross_check_m39_source_sha_mismatch")
                p8 = False
            if str(m39_cross.get("run_status") or "") != STATUS_RUN_COMPLETED_WITH_CKPT:
                _optional_m39_issues.append("cross_check_m39_run_status_not_completed")
                p8 = False
            if (
                str(m39_cross.get("contract_id") or "") != CONTRACT_ID_M39
                or str(
                    m39_cross.get("profile_id") or "",
                )
                != PROFILE_M39
            ):
                _optional_m39_issues.append("cross_check_m39_contract_profile_mismatch")
                p8 = False

    if (
        inp.m39_checkpoint_inventory_json is not None
        and inp.m39_checkpoint_inventory_json.is_file()
    ):
        try:
            inv_c = _parse_json_object(inp.m39_checkpoint_inventory_json.resolve())
        except (OSError, ValueError, json.JSONDecodeError):
            inv_c = {}
            _optional_m39_issues.append("cross_check_inventory_unreadable")
            p8 = False
        if (
            inv_c
            and _is_hex64(exp_final_cli)
            and not _inventory_has_final_sha(inv_c, exp_final_cli)
        ):
            _optional_m39_issues.append("cross_check_inventory_missing_final_sha")
            p8 = False

    if inp.m39_telemetry_summary_json is not None and inp.m39_telemetry_summary_json.is_file():
        try:
            tel_c = _parse_json_object(inp.m39_telemetry_summary_json.resolve())
        except (OSError, ValueError, json.JSONDecodeError):
            tel_c = None
            _optional_m39_issues.append("cross_check_telemetry_unreadable")
            p8 = False
        if tel_c is not None and not isinstance(tel_c, dict):
            _optional_m39_issues.append("cross_check_telemetry_not_object")
            p8 = False

    if _optional_m39_issues:
        warnings.extend(_optional_m39_issues)

    if not _is_hex64(final_m41):
        p4 = False

    if p1 and not (final_m41 and _is_hex64(final_m41)):
        package_status = STATUS_BLOCKED_MISSING_FINAL_INDEX
    elif p7_fail_m05_supplied and cli_m05_provided:
        package_status = STATUS_BLOCKED_INVALID_M05
    elif not p1:
        package_status = STATUS_BLOCKED_M41_NOT_READY
    elif not p2:
        package_status = STATUS_BLOCKED_M39_RECEIPT_MISMATCH
    elif not p3:
        package_status = STATUS_BLOCKED_SOURCE_MISMATCH
    elif not p4:
        package_status = STATUS_BLOCKED_FINAL_MISMATCH
    elif not p5 or not p6 or not p7 or not p8 or not p9_ok:
        if not p6 or not p7:
            package_status = STATUS_BLOCKED_INVALID_M41
        elif not p5 or not p9_ok:
            package_status = STATUS_BLOCKED_INVALID_M41
        else:
            package_status = STATUS_BLOCKED_INVALID_M41
    else:
        package_status = STATUS_READY
        if warnings:
            package_status = STATUS_READY_WARNINGS

    if package_status == STATUS_BLOCKED_M39_RECEIPT_MISMATCH and not _is_hex64(exp_m39_cli):
        package_status = STATUS_BLOCKED_INVALID_M41

    run_sum_m41 = m41_raw.get("run_summary") or {}
    run_sum_m41 = run_sum_m41 if isinstance(run_sum_m41, dict) else {}
    ub_op = m41_raw.get("upstream_bindings") or {}
    ub_op = ub_op if isinstance(ub_op, dict) else {}
    m39_u = ub_op.get("m39_two_hour_operator_run") or {}
    m39_u = m39_u if isinstance(m39_u, dict) else {}
    fwc = m39_u.get("full_wall_clock_satisfied")

    evaluation_ready = package_status in (STATUS_READY, STATUS_READY_WARNINGS)

    chk_verified = False
    if inp.authorize_final_checkpoint_file_sha256 and final_file_sha and _is_hex64(exp_final_cli):
        chk_verified = final_file_sha.lower() == exp_final_cli

    if (
        inp.authorize_final_checkpoint_file_sha256
        and final_file_sha
        and _is_hex64(exp_final_cli)
        and not chk_verified
    ):
        package_status = STATUS_BLOCKED_FINAL_MISMATCH
        evaluation_ready = False
        if "final_checkpoint_file_sha_mismatch_vs_expected_final_metadata" not in warnings:
            warnings.append("final_checkpoint_file_sha_mismatch_vs_expected_final_metadata")

    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_EVAL_PACKAGE_FAMILY,
        "package_profile_id": PROFILE_M42,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M42,
        "emitter_module": EMITTER_MODULE_M42,
        "package_status": package_status,
        "evaluation_package_ready": evaluation_ready,
        "expected_m41_package_sha256_status": exp_m41_status,
        "upstream_bindings": _upstream_public(
            m41_raw=m41_raw,
            m41_digest=digest_file,
            m05_binding_public=m05_binding,
        ),
        "candidate_checkpoint": {
            "source_candidate_sha256": (
                src_m41 if _is_hex64(src_m41) else SOURCE_CANDIDATE_LINEAGE_SHA256
            ),
            "final_candidate_sha256": final_m41 if _is_hex64(final_m41) else None,
            "candidate_role": "final_two_hour_candidate_checkpoint",
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_blob_loaded": False,
            "torch_load_performed": False,
            "checkpoint_file_sha256_verified": chk_verified,
            "final_checkpoint_file_binding": final_ckpt_binding_status,
        },
        "run_summary": {
            "target_wall_clock_seconds": int(run_sum_m41.get("target_wall_clock_seconds") or 7200),
            "full_wall_clock_satisfied": bool(fwc)
            if fwc is not None
            else bool(m41_raw.get("full_wall_clock_satisfied")),
            "training_update_count": int(run_sum_m41.get("training_update_count") or 0),
            "sc2_backed_features_used": bool(run_sum_m41.get("sc2_backed_features_used")),
        },
        "evidence_bindings": {
            "telemetry_summary_bound": telemetry_ok,
            "checkpoint_inventory_bound": inv_ok_ev,
            "transcript_metadata_bound": trans_ok,
            "retention_counters_bound": retention_ok,
        },
        "evaluation_routing": {
            "ready_for_m43_bounded_evaluation_gate": evaluation_ready,
            "recommended_next": (
                RECOMMENDED_NEXT_SUCCESS if evaluation_ready else RECOMMENDED_NEXT_REMEDIATION
            ),
            "blocked_reasons": ([] if evaluation_ready else [package_status]),
        },
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
            p9=p9_ok,
            p10=p10 and evaluation_ready,
        ),
        "claim_flags": _claim_flags_all_false_m42(),
        "non_claims": list(NON_CLAIMS_M42),
        "cross_check_hints": (
            {"optional_direct_m39_cross_check_messages": _optional_m39_issues}
            if _optional_m39_issues
            else {}
        ),
    }
    if warnings:
        result["noncritical_warnings"] = list(warnings)
    return result, inherited_m05_note


def _blocked_body_early(
    status: str,
    warnings: list[str],
    exp_m41_st: str,
    m41_partial: dict[str, Any] | None,
) -> dict[str, Any]:
    body = build_fixture_m42_body()
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["package_status"] = status
    body["expected_m41_package_sha256_status"] = exp_m41_st
    body["evaluation_routing"] = {
        "ready_for_m43_bounded_evaluation_gate": False,
        "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
        "blocked_reasons": [status],
    }
    body["gates"] = _gate_pack(
        p0=m41_partial is not None,
        p1=False,
        p2=False,
        p3=False,
        p4=False,
        p5=False,
        p6=False,
        p7=True,
        p8=True,
        p9=True,
        p10=False,
    )
    if m41_partial is not None:
        digest = str(m41_partial.get(GATE_ARTIFACT_DIGEST_FIELD) or "")
        body["upstream_bindings"] = _upstream_from_m41(m41_partial, m41_digest=digest)
    body["evaluation_package_ready"] = False
    if warnings:
        body.setdefault("noncritical_warnings", []).extend(warnings)
    return body


def _upstream_from_m41(m41_raw: dict[str, Any], *, m41_digest: str) -> dict[str, Any]:
    pkg_status = str(m41_raw.get("package_status") or "")
    ub = m41_raw.get("upstream_bindings") or {}
    ub = ub if isinstance(ub, dict) else {}
    m39b = ub.get("m39_two_hour_operator_run") or {}
    m39b = m39b if isinstance(m39b, dict) else {}
    return {
        "m41_two_hour_run_package": {
            "artifact_sha256": m41_digest,
            "contract_id": CONTRACT_ID_M41,
            "profile_id": PROFILE_M41,
            "package_status": pkg_status,
        },
        "m39_two_hour_run_receipt": {
            "artifact_sha256": m39b.get("artifact_sha256"),
            "run_status": m39b.get("run_status"),
            "full_wall_clock_satisfied": m39b.get("full_wall_clock_satisfied"),
        },
        "m05_scorecard_protocol": {
            "binding_status": "optional_not_supplied",
        },
    }


def _upstream_public(
    *,
    m41_raw: dict[str, Any],
    m41_digest: str,
    m05_binding_public: dict[str, Any],
) -> dict[str, Any]:
    base = _upstream_from_m41(m41_raw, m41_digest=m41_digest)
    out = dict(base)
    out["m05_scorecard_protocol"] = dict(m05_binding_public)
    return out


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M42 emission leaked path patterns into public artifacts")


def emit_m42_fixture(
    output_dir: Path, *, repo_root: Path
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    del repo_root
    body_pre = build_fixture_m42_body()
    sealed = seal_m42_body(redact_paths_in_value(body_pre))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m42_report(sealed)
    chk = build_m42_checklist_md(sealed)
    pkt = _routing_packet_md(sealed)
    idx = _bindings_index(
        sealed,
        m05_binding={"binding_status": "optional_not_supplied"},
        inherited_m05_note=None,
        final_ckpt_basename=None,
        final_ckpt_file_sha256=None,
        file_verify=False,
        final_ckpt_binding_status=None,
    )

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkt = output_dir / ROUTING_PACKET_FILENAME
    p_idx = output_dir / BINDINGS_INDEX_FILENAME

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


def emit_m42_operator_preflight(
    output_dir: Path,
    *,
    repo_root: Path,
    inputs: M42OperatorInputs,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body_pre, inherited_note_eval = _evaluate_operator_m42(repo_root, inputs)

    fc = inputs.final_candidate_checkpoint_path
    fb: str | None = None
    fsha: str | None = None
    ck_note: str | None = None
    if fc is not None and Path(fc).is_file():
        fb = Path(fc).name
        if inputs.authorize_final_checkpoint_file_sha256:
            fsha = sha256_file_hex(Path(fc))
        ck_note = (
            None
            if inputs.authorize_final_checkpoint_file_sha256
            else "final_candidate_checkpoint_path_supplied_but_not_hashed"
        )

    m05_bind = dict(
        (body_pre.get("upstream_bindings") or {}).get("m05_scorecard_protocol") or {},
    )

    sealed = seal_m42_body(redact_paths_in_value(body_pre))
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = build_m42_report(sealed)
    chk = build_m42_checklist_md(sealed)
    pkt = _routing_packet_md(sealed)
    chk_ver = bool(sealed.get("candidate_checkpoint", {}).get("checkpoint_file_sha256_verified"))
    idx = _bindings_index(
        sealed,
        m05_binding=m05_bind,
        inherited_m05_note=inherited_note_eval,
        final_ckpt_basename=fb,
        final_ckpt_file_sha256=fsha,
        file_verify=chk_ver,
        final_ckpt_binding_status=ck_note,
    )

    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkt = output_dir / ROUTING_PACKET_FILENAME
    p_idx = output_dir / BINDINGS_INDEX_FILENAME

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
    "M42OperatorInputs",
    "build_fixture_m42_body",
    "build_m42_checklist_md",
    "build_m42_report",
    "emit_m42_fixture",
    "emit_m42_operator_preflight",
    "seal_m42_body",
    "sha256_file_hex",
]
