"""Build, seal, and write V15-M06 human panel benchmark protocol (no human execution)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.human_panel_benchmark_models import (
    ALLOWED_FUTURE_CLAIM_BOUNDARY,
    CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
    CONTRACT_VERSION,
    DISALLOWED_CLAIM_SHAPES,
    EMITTER_MODULE_HUMAN_PANEL,
    EVIDENCE_REQ_ROW_FIELDS,
    EVIDENCE_REQUIREMENT_CLASS_IDS,
    EVIDENCE_SCOPE_FIXTURE,
    EVIDENCE_SCOPE_NOT_EVALUATED,
    EVIDENCE_SCOPE_OPERATOR,
    FILENAME_HUMAN_PANEL_BENCHMARK,
    MILESTONE_ID_V15_M06,
    NON_CLAIMS_V15_M06,
    PARTICIPANT_TIER_IDS,
    PARTICIPANT_TIER_ROW_FIELDS,
    PRIVACY_POSTURE_IDS,
    PRIVACY_POSTURE_ROW_FIELDS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROTOCOL_JSON_TOP_LEVEL_KEYS,
    PROTOCOL_PROFILE_ID_HUMAN_PANEL,
    PROTOCOL_STATUS_FIXTURE_ONLY,
    PROTOCOL_STATUS_OP_COMPLETE,
    PROTOCOL_STATUS_OP_INCOMPLETE,
    REPORT_FILENAME_HUMAN_PANEL_BENCHMARK,
    REPORT_VERSION_HUMAN_PANEL,
    SEAL_KEY_HUMAN_PANEL,
    THRESHOLD_OPTION_IDS,
    THRESHOLD_POLICY_ROW_FIELDS,
)
from starlab.v15.strong_agent_scorecard_models import CHECK_PASS

SEAL = SEAL_KEY_HUMAN_PANEL
REDACT_TOKENS: Final[tuple[str, ...]] = (
    "REDACTED_ABSOLUTE_PATH",
    "REDACTED_CONTACT",
    "REDACTED_PII",
)

_EMAIL_RE: Final[re.Pattern[str]] = re.compile(
    r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
)
_PHONEY_RAW_KEYS: Final[frozenset[str]] = frozenset(
    {
        "email",
        "phone",
        "mobile",
        "discord",
        "battle_tag",
        "battletag",
        "skype",
        "telegram",
    }
)


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def parse_protocol_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("protocol JSON must be a single object")
    unknown = set(raw) - set(PROTOCOL_JSON_TOP_LEVEL_KEYS)
    if unknown:
        raise ValueError(f"unknown top-level keys in protocol JSON: {sorted(unknown)}")
    return raw


def _validate_row(row: Any, fields: tuple[str, ...], ctx: str) -> None:
    if not isinstance(row, dict):
        raise ValueError(f"{ctx} must be an object")
    for k in fields:
        if k not in row:
            raise ValueError(f"{ctx} missing field {k!r}")
    for k in row:
        if k not in fields:
            raise ValueError(f"{ctx} unknown field {k!r}")


def redact_path_and_contact_in_value(obj: Any) -> Any:
    """Redact absolute paths and obvious contact / handle-like strings in nested JSON."""
    p = redact_paths_in_value(obj)
    return _redact_contact_and_handles(p)


def _redact_contact_and_handles(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            lk = k.lower() if isinstance(k, str) else k
            if isinstance(lk, str) and lk in _PHONEY_RAW_KEYS:
                out[k] = "<REDACTED_PII>" if v not in (None, "", [], {}) else v
            else:
                out[k] = _redact_contact_and_handles(v)
        return out
    if isinstance(obj, list):
        return [_redact_contact_and_handles(x) for x in obj]
    if isinstance(obj, str):
        t = _EMAIL_RE.sub("<REDACTED_CONTACT>", obj)
        return t
    return obj


def _redaction_token_count(value: Any) -> int:
    s = canonical_json_dumps(value)
    return sum(s.count(t) for t in REDACT_TOKENS)


def _privacy_rows_fixture() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pid in PRIVACY_POSTURE_IDS:
        rows.append(
            {
                "posture_id": pid,
                "enforcement": "required",
                "protocol_status": "defined",
                "notes": f"Posture {pid} is protocol-defined in M06; no execution.",
            }
        )
    return rows


def _tier_rows_fixture() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tid in PARTICIPANT_TIER_IDS:
        rows.append(
            {
                "tier_id": tid,
                "description": f"Synthetic protocol tier {tid} (no real participants).",
                "protocol_status": "defined",
                "notes": "Vocabulary only; M06 does not record live roster.",
            }
        )
    return rows


def _threshold_policy_fixture() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for oid in THRESHOLD_OPTION_IDS:
        out.append(
            {
                "option_id": oid,
                "description": f"Threshold policy option: {oid}",
                "protocol_status": "defined" if "no_claim" not in oid else "reserved",
                "notes": "M06 does not assert a threshold was met.",
            }
        )
    return out


def _evidence_requirements_fixture() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for eid in EVIDENCE_REQUIREMENT_CLASS_IDS:
        storage = (
            "private_local_only"
            if "private" in eid or eid in ("consent_receipts_private", "participant_roster_private")
            else "public_safe_summary"
        )
        out.append(
            {
                "evidence_class_id": eid,
                "required": True,
                "storage_posture": storage,
                "protocol_status": "defined",
                "notes": f"Requirement class {eid} for future execution milestones (M11+).",
            }
        )
    return out


def _carry_forward() -> list[dict[str, str]]:
    return [
        {
            "item_id": "v15_m11_human_panel_execution",
            "summary": "V15-M11 — bounded human panel execution; not M06.",
        },
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "Re-check at M06: use same narrow pip-audit --ignore-vuln CVE-2026-3219 until a "
                "fixed audit-clean pip release exists; see docs/starlab-v1.5.md §11."
            ),
        },
    ]


def _attestation() -> str:
    return (
        "V15-M06 defines and emits the human-panel benchmark protocol and fixture output. It does "
        "not recruit participants, does not run matches, does not process real identities, and "
        "does not authorize strong-agent, human-benchmark, benchmark, or long-GPU claims."
    )


def _match_rules_fixture() -> dict[str, Any]:
    return {
        "race": "Terran_first",
        "mode": "1v1",
        "map_pool": "declared_before_execution",
        "agent_checkpoint": "fixed_before_execution",
        "game_count": "predeclared",
        "replay_capture": "required",
        "disconnect_policy": "defined_in_operator_runbook",
        "pause_policy": "no_unauthorized_pause",
        "observer_policy": "declared",
        "rematch_policy": "declared",
        "forfeit_policy": "declared",
        "execution_status": "not_executed",
    }


def _session_rules_fixture() -> dict[str, Any]:
    return {
        "session_format": "declared",
        "scheduling": "operator_local",
        "recording": "required_where_declared",
        "execution_status": "not_executed",
    }


def _map_pool_policy_fixture() -> dict[str, Any]:
    return {
        "map_pool_id": "fixture:human_panel_map_pool_001",
        "freeze_before_execution": True,
        "map_ids": ["fixture_map_a", "fixture_map_b"],
        "rights_posture": "fixture_only",
        "execution_status": "not_executed",
    }


def build_human_panel_benchmark_body_fixture() -> dict[str, Any]:
    claim_boundary = {
        "allowed_shape": ALLOWED_FUTURE_CLAIM_BOUNDARY,
        "disallowed_shapes": list(DISALLOWED_CLAIM_SHAPES),
    }
    return {
        "contract_id": CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
        "contract_version": CONTRACT_VERSION,
        "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        "milestone_id": MILESTONE_ID_V15_M06,
        "generated_by": EMITTER_MODULE_HUMAN_PANEL,
        "profile": PROFILE_FIXTURE_CI,
        "human_panel_protocol_status": PROTOCOL_STATUS_FIXTURE_ONLY,
        "benchmark_execution_performed": False,
        "human_panel_execution_performed": False,
        "human_benchmark_claim_authorized": False,
        "strong_agent_claim_authorized": False,
        "long_gpu_run_authorized": False,
        "evidence_scope": EVIDENCE_SCOPE_FIXTURE,
        "benchmark_identity": {
            "benchmark_id": "starlab.v15.human_panel_benchmark.v1:fixture",
            "benchmark_name": "STARLAB v1.5 human panel benchmark (protocol fixture)",
            "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        },
        "participant_privacy_profile": _privacy_rows_fixture(),
        "participant_tiers": _tier_rows_fixture(),
        "eligibility_rules": [
            {
                "rule_id": "elig_fixture_1",
                "text": "Participant eligibility is protocol-defined; no real screening in M06.",
                "protocol_status": "defined",
            }
        ],
        "consent_requirements": [
            {
                "requirement_id": "consent_fixture_1",
                "text": "consent_record_required_for_execution; receipts stay private by default.",
                "protocol_status": "defined",
            }
        ],
        "session_rules": _session_rules_fixture(),
        "match_rules": _match_rules_fixture(),
        "map_pool_policy": _map_pool_policy_fixture(),
        "agent_identity_requirements": {
            "checkpoint_id_binding": "required",
            "pseudonym_in_public_artifacts": "required",
            "execution_status": "protocol_defined",
        },
        "checkpoint_binding_requirements": {
            "lineage_or_sha_ref": "required",
            "no_blob_read_in_m06": True,
            "execution_status": "not_executed",
        },
        "replay_capture_requirements": {
            "replay_capture": "required_for_execution_milestone",
            "manifest_required": True,
            "execution_status": "not_executed",
        },
        "result_policy": {
            "result_recording": "predeclared_schema_only",
            "no_public_match_results_in_m06": True,
        },
        "threshold_policy": _threshold_policy_fixture(),
        "evidence_requirements": _evidence_requirements_fixture(),
        "claim_boundary": claim_boundary,
        "non_claims": list(NON_CLAIMS_V15_M06),
        "optional_bindings": {
            "environment_lock_json_canonical_sha256": None,
            "checkpoint_lineage_json_canonical_sha256": None,
            "strong_agent_scorecard_json_canonical_sha256": None,
            "xai_evidence_json_canonical_sha256": None,
        },
        "redaction_policy": {
            "public_fixture": "no_names_emails_tags_ips_in_fixture_output",
            "operator_declared_emission": "redact_absolute_paths_and_contact_like_fields",
        },
        "m06_verification_attestation": _attestation(),
        "check_results": [
            {
                "check_id": "m06_protocol_vocabulary",
                "description": (
                    "Fixture includes tier, privacy, threshold, and evidence vocabulary."
                ),
                "status": CHECK_PASS,
            },
            {
                "check_id": "m06_no_execution",
                "description": "M06 does not perform human panel execution or live SC2.",
                "status": CHECK_PASS,
            },
        ],
        "carry_forward_items": _carry_forward(),
    }


def _default_privacy_row(self_id: str) -> dict[str, str]:
    return {
        "posture_id": self_id,
        "enforcement": "",
        "protocol_status": "",
        "notes": "",
    }


def _default_tier_row(tid: str) -> dict[str, str]:
    return {
        "tier_id": tid,
        "description": "",
        "protocol_status": "",
        "notes": "",
    }


def _default_operator_protocol() -> dict[str, Any]:
    return {
        "profile": PROFILE_OPERATOR_DECLARED,
        "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        "benchmark_id": "",
        "benchmark_name": "",
        "participant_privacy_profile": [_default_privacy_row(pid) for pid in PRIVACY_POSTURE_IDS],
        "participant_tiers": [_default_tier_row(tid) for tid in PARTICIPANT_TIER_IDS],
        "eligibility_rules": [],
        "consent_requirements": [],
        "session_rules": {},
        "match_rules": {},
        "map_pool_policy": {},
        "agent_identity_requirements": {},
        "checkpoint_binding_requirements": {},
        "replay_capture_requirements": {},
        "result_policy": {},
        "threshold_policy": [],
        "evidence_requirements": [],
        "claim_boundary": {
            "allowed_shape": "",
            "disallowed_shapes": [],
        },
        "non_claims": [],
        "redaction_policy": {"notes": ""},
        "operator_notes": "",
        "extension_flags": [],
    }


def merge_operator_protocol(overlay: dict[str, Any]) -> dict[str, Any]:
    base = _default_operator_protocol()
    for k, v in overlay.items():
        if k in ("claim_boundary",) and isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = {**base["claim_boundary"], **v}
        else:
            base[k] = v
    return base


def _privacy_complete(rows: list[Any]) -> bool:
    if not isinstance(rows, list) or len(rows) < 1:
        return False
    found: set[str] = set()
    for r in rows:
        if not isinstance(r, dict):
            return False
        pid = str(r.get("posture_id", ""))
        if pid in PRIVACY_POSTURE_IDS and str(r.get("protocol_status", "")).strip():
            found.add(pid)
    return found == set(PRIVACY_POSTURE_IDS)


def _tiers_complete(rows: list[Any]) -> bool:
    if not isinstance(rows, list) or len(rows) < 1:
        return False
    found: set[str] = set()
    for r in rows:
        if not isinstance(r, dict):
            return False
        tid = str(r.get("tier_id", ""))
        if tid in PARTICIPANT_TIER_IDS and str(r.get("protocol_status", "")).strip():
            found.add(tid)
    return found == set(PARTICIPANT_TIER_IDS)


def _threshold_complete(rows: list[Any]) -> bool:
    if not isinstance(rows, list) or len(rows) < 1:
        return False
    found: set[str] = set()
    for r in rows:
        if not isinstance(r, dict):
            return False
        oid = str(r.get("option_id", ""))
        if oid in THRESHOLD_OPTION_IDS and str(r.get("description", "")).strip():
            found.add(oid)
    return found == set(THRESHOLD_OPTION_IDS)


def _evidence_complete(rows: list[Any]) -> bool:
    if not isinstance(rows, list) or len(rows) < 1:
        return False
    found: set[str] = set()
    for r in rows:
        if not isinstance(r, dict):
            return False
        eid = str(r.get("evidence_class_id", ""))
        if eid in EVIDENCE_REQUIREMENT_CLASS_IDS and str(r.get("protocol_status", "")).strip():
            found.add(eid)
    return found == set(EVIDENCE_REQUIREMENT_CLASS_IDS)


def _operator_protocol_complete(data: dict[str, Any]) -> bool:
    if not str(data.get("benchmark_id", "")).strip():
        return False
    if not str(data.get("benchmark_name", "")).strip():
        return False
    if not _privacy_complete(data.get("participant_privacy_profile", [])):
        return False
    if not _tiers_complete(data.get("participant_tiers", [])):
        return False
    if not _threshold_complete(data.get("threshold_policy", [])):
        return False
    if not _evidence_complete(data.get("evidence_requirements", [])):
        return False
    cb = data.get("claim_boundary")
    if not isinstance(cb, dict):
        return False
    if not str(cb.get("allowed_shape", "")).strip():
        return False
    dlist = cb.get("disallowed_shapes")
    if not isinstance(dlist, list) or not all(isinstance(x, str) for x in dlist):
        return False
    ncl = data.get("non_claims")
    if not isinstance(ncl, list) or not ncl or not all(isinstance(x, str) for x in ncl):
        return False
    for name in (
        "eligibility_rules",
        "consent_requirements",
    ):
        arr = data.get(name)
        if not isinstance(arr, list) or len(arr) < 1:
            return False
    for key in (
        "session_rules",
        "match_rules",
        "map_pool_policy",
        "agent_identity_requirements",
        "checkpoint_binding_requirements",
        "replay_capture_requirements",
        "result_policy",
    ):
        v = data.get(key)
        if v is None or (isinstance(v, dict) and not v) or (isinstance(v, list) and not v):
            return False
    return True


def build_human_panel_benchmark_body_operator(
    data: dict[str, Any], *, optional_bindings: dict[str, str | None]
) -> dict[str, Any]:
    merged = merge_operator_protocol(data)
    complete = _operator_protocol_complete(merged)
    status = PROTOCOL_STATUS_OP_COMPLETE if complete else PROTOCOL_STATUS_OP_INCOMPLETE
    ev_scope = EVIDENCE_SCOPE_OPERATOR if complete else EVIDENCE_SCOPE_NOT_EVALUATED
    p_priv = merged["participant_privacy_profile"]
    p_tier = merged["participant_tiers"]
    if not isinstance(p_priv, list) or not isinstance(p_tier, list):
        raise TypeError("participant_privacy_profile and participant_tiers must be lists")
    for i, row in enumerate(p_priv):
        if len(row) > 0:
            _validate_row(row, PRIVACY_POSTURE_ROW_FIELDS, f"participant_privacy_profile[{i}]")
    for i, row in enumerate(p_tier):
        if len(row) > 0:
            _validate_row(row, PARTICIPANT_TIER_ROW_FIELDS, f"participant_tiers[{i}]")
    tpol = merged["threshold_policy"]
    if not isinstance(tpol, list):
        raise TypeError("threshold_policy must be a list")
    for i, row in enumerate(tpol):
        if not isinstance(row, dict):
            raise TypeError("threshold_policy row must be object")
        if len(row) > 0:
            _validate_row(row, THRESHOLD_POLICY_ROW_FIELDS, f"threshold_policy[{i}]")
    evr = merged["evidence_requirements"]
    if not isinstance(evr, list):
        raise TypeError("evidence_requirements must be a list")
    for i, row in enumerate(evr):
        if not isinstance(row, dict):
            raise TypeError("evidence_requirements row must be object")
        if len(row) > 0:
            _validate_row(row, EVIDENCE_REQ_ROW_FIELDS, f"evidence_requirements[{i}]")
    if complete:
        if not all(
            e in {r.get("evidence_class_id") for r in evr} for e in EVIDENCE_REQUIREMENT_CLASS_IDS
        ):
            raise ValueError("complete operator protocol must list all evidence class ids")
    ncl = merged.get("non_claims")
    op_extra: list[str] = [str(x) for x in ncl] if isinstance(ncl, list) else []
    non_claims = list(NON_CLAIMS_V15_M06) + op_extra
    onotes = merged.get("operator_notes", "")
    onotes_s: str | None = str(onotes) if str(onotes).strip() else None
    exflags = merged.get("extension_flags")
    ext: list[str] = [str(x) for x in exflags] if isinstance(exflags, list) else []

    out: dict[str, Any] = {
        "contract_id": CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
        "contract_version": CONTRACT_VERSION,
        "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        "milestone_id": MILESTONE_ID_V15_M06,
        "generated_by": EMITTER_MODULE_HUMAN_PANEL,
        "profile": str(merged.get("profile") or PROFILE_OPERATOR_DECLARED),
        "human_panel_protocol_status": status,
        "benchmark_execution_performed": False,
        "human_panel_execution_performed": False,
        "human_benchmark_claim_authorized": False,
        "strong_agent_claim_authorized": False,
        "long_gpu_run_authorized": False,
        "evidence_scope": ev_scope,
        "benchmark_identity": {
            "benchmark_id": str(merged.get("benchmark_id", "")),
            "benchmark_name": str(merged.get("benchmark_name", "")),
            "protocol_profile_id": PROTOCOL_PROFILE_ID_HUMAN_PANEL,
        },
        "participant_privacy_profile": p_priv,
        "participant_tiers": p_tier,
        "eligibility_rules": merged["eligibility_rules"],
        "consent_requirements": merged["consent_requirements"],
        "session_rules": merged["session_rules"],
        "match_rules": merged["match_rules"],
        "map_pool_policy": merged["map_pool_policy"],
        "agent_identity_requirements": merged["agent_identity_requirements"],
        "checkpoint_binding_requirements": merged["checkpoint_binding_requirements"],
        "replay_capture_requirements": merged["replay_capture_requirements"],
        "result_policy": merged["result_policy"],
        "threshold_policy": tpol,
        "evidence_requirements": evr,
        "claim_boundary": merged["claim_boundary"],
        "non_claims": non_claims,
        "optional_bindings": {
            "environment_lock_json_canonical_sha256": optional_bindings.get("environment_lock"),
            "checkpoint_lineage_json_canonical_sha256": optional_bindings.get("checkpoint_lineage"),
            "strong_agent_scorecard_json_canonical_sha256": optional_bindings.get(
                "strong_agent_scorecard"
            ),
            "xai_evidence_json_canonical_sha256": optional_bindings.get("xai_evidence"),
        },
        "redaction_policy": merged.get("redaction_policy", {"notes": ""}),
        "m06_verification_attestation": _attestation(),
        "check_results": [
            {
                "check_id": "m06_operator_protocol",
                "description": f"Operator protocol metadata resolved to {status}.",
                "status": CHECK_PASS,
            }
        ],
        "carry_forward_items": _carry_forward(),
    }
    if onotes_s is not None:
        out["operator_notes"] = onotes_s
    if ext:
        out["operator_extension_flags"] = ext
    return out


def build_human_panel_benchmark_body(
    profile: str,
    *,
    protocol_data: dict[str, Any] | None = None,
    optional_bindings: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    bind = optional_bindings or {
        "environment_lock": None,
        "checkpoint_lineage": None,
        "strong_agent_scorecard": None,
        "xai_evidence": None,
    }
    if profile == PROFILE_FIXTURE_CI:
        return build_human_panel_benchmark_body_fixture()
    if profile == PROFILE_OPERATOR_DECLARED:
        if protocol_data is None:
            raise ValueError("operator_declared profile requires --protocol-json data")
        return build_human_panel_benchmark_body_operator(protocol_data, optional_bindings=bind)
    raise ValueError(f"unknown profile: {profile!r}")


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_HUMAN_PANEL_BENCHMARK
    assert body["protocol_profile_id"] == PROTOCOL_PROFILE_ID_HUMAN_PANEL
    assert body["milestone_id"] == MILESTONE_ID_V15_M06
    for k in (
        "long_gpu_run_authorized",
        "benchmark_execution_performed",
        "human_panel_execution_performed",
        "human_benchmark_claim_authorized",
        "strong_agent_claim_authorized",
    ):
        assert body[k] is False


def seal_human_panel_benchmark_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, SEAL: digest}


def build_human_panel_benchmark_report(
    contract: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    digest = contract[SEAL]
    tiers = contract.get("participant_tiers", [])
    evr = contract.get("evidence_requirements", [])
    n_tiers = len(tiers) if isinstance(tiers, list) else 0
    n_ev = len(evr) if isinstance(evr, list) else 0
    bindings = contract.get("optional_bindings", {})
    opt_keys: list[str] = []
    if isinstance(bindings, dict):
        opt_keys = sorted(k for k, v in bindings.items() if v)
    return {
        "report_version": REPORT_VERSION_HUMAN_PANEL,
        "milestone_id": MILESTONE_ID_V15_M06,
        "contract_id": contract["contract_id"],
        "protocol_profile_id": contract["protocol_profile_id"],
        "profile": contract["profile"],
        "artifact_sha256": digest,
        "participant_tier_count": n_tiers,
        "evidence_requirement_count": n_ev,
        "claim_authorized": bool(
            contract.get("human_benchmark_claim_authorized")
            or contract.get("strong_agent_claim_authorized")
        ),
        "execution_performed": bool(
            contract.get("benchmark_execution_performed")
            or contract.get("human_panel_execution_performed")
        ),
        "redaction_count": redaction_count,
        "optional_binding_keys": opt_keys,
    }


def write_human_panel_artifacts(
    *, output_dir: Path, contract: dict[str, Any], report: dict[str, Any]
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_HUMAN_PANEL_BENCHMARK
    r_path = output_dir / REPORT_FILENAME_HUMAN_PANEL_BENCHMARK
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_v15_human_panel_benchmark(
    output_dir: Path,
    *,
    profile: str,
    protocol_path: Path | None = None,
    environment_lock_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    strong_agent_scorecard_path: Path | None = None,
    xai_evidence_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    """Emit sealed contract + report. Returns (sealed, report, redaction_count)."""
    optional_sha: dict[str, str | None] = {
        "environment_lock": None,
        "checkpoint_lineage": None,
        "strong_agent_scorecard": None,
        "xai_evidence": None,
    }
    if environment_lock_path is not None:
        optional_sha["environment_lock"] = environment_lock_file_canonical_sha256(
            environment_lock_path
        )
    if checkpoint_lineage_path is not None:
        optional_sha["checkpoint_lineage"] = _json_file_canonical_sha256(checkpoint_lineage_path)
    if strong_agent_scorecard_path is not None:
        optional_sha["strong_agent_scorecard"] = _json_file_canonical_sha256(
            strong_agent_scorecard_path
        )
    if xai_evidence_path is not None:
        optional_sha["xai_evidence"] = _json_file_canonical_sha256(xai_evidence_path)

    protocol_data: dict[str, Any] | None = None
    if protocol_path is not None:
        protocol_data = parse_protocol_json(protocol_path)

    body = build_human_panel_benchmark_body(
        profile, protocol_data=protocol_data, optional_bindings=optional_sha
    )
    redact_count = 0
    if profile == PROFILE_OPERATOR_DECLARED and protocol_data is not None:
        body = redact_path_and_contact_in_value(body)
        redact_count = _redaction_token_count(body)
    _validate_body_invariants(body)
    sealed = seal_human_panel_benchmark_body(body)
    rep = build_human_panel_benchmark_report(sealed, redaction_count=redact_count)
    c_path, r_path = write_human_panel_artifacts(output_dir=output_dir, contract=sealed, report=rep)
    return sealed, rep, redact_count, c_path, r_path
