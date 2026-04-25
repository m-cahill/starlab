"""Build, seal, and write V15-M04 XAI evidence pack + report (metadata-only)."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.xai_evidence_models import (
    ALTERNATIVE_RANK_ROW_FIELDS,
    ATTRIBUTION_ROW_FIELDS,
    CHECK_FAIL,
    CHECK_PASS,
    CHECKPOINT_IDENTITY_FIELDS,
    CONCEPT_ROW_FIELDS,
    CONTRACT_ID_XAI_EVIDENCE,
    COUNTERFACTUAL_ROW_FIELDS,
    CRITICAL_DECISION_ROW_FIELDS,
    DECISION_TRACE_ROW_FIELDS,
    EMITTER_MODULE_XAI,
    EVIDENCE_CI_FIXTURE,
    EVIDENCE_JSON_TOP_LEVEL_KEYS,
    EVIDENCE_NOT_EVALUATED,
    EVIDENCE_OPERATOR_DECLARED,
    EVIDENCE_OPERATOR_LOCAL_METADATA,
    EXPLANATION_REPORT_ROW_FIELDS,
    FILENAME_XAI_EVIDENCE,
    METHOD_VOCABULARY_EXAMPLES,
    MILESTONE_ID_V15_M04,
    NON_CLAIMS_V15_M04,
    OVERLAY_MANIFEST_ROW_FIELDS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    REPLAY_IDENTITY_FIELDS,
    REPORT_FILENAME_XAI_EVIDENCE,
    REPORT_VERSION_XAI_EVIDENCE,
    REQUIRED_LOGICAL_ARTIFACT_NAMES,
    SCENE_TYPE_VOCABULARY,
    SEAL_KEY_XAI_EVIDENCE,
    STATUS_VOCABULARY,
    UNCERTAINTY_ROW_FIELDS,
    XAI_STATUS_BLOCKED,
    XAI_STATUS_FIXTURE_ONLY,
    XAI_STATUS_OP_COMPLETE,
    XAI_STATUS_OP_INCOMPLETE,
)

EMITTER_MODULE = EMITTER_MODULE_XAI
PLACEHOLDER_SHA256: Final[str] = "0" * 64


def _vocab_tuples() -> dict[str, tuple[str, ...]]:
    return {k: tuple(v) for k, v in STATUS_VOCABULARY.items()}


def _in_vocab(group: str, value: str) -> bool:
    t = _vocab_tuples()
    if group not in t:
        return True
    return value in t[group]


def _validate_row_fields(row: Any, fields: tuple[str, ...], ctx: str) -> None:
    if not isinstance(row, dict):
        raise ValueError(f"{ctx} must be an object")
    for k in fields:
        if k not in row:
            raise ValueError(f"{ctx} missing field {k!r}")
    for k in row:
        if k not in fields:
            raise ValueError(f"{ctx} unknown field {k!r}")


def parse_evidence_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("evidence JSON must be a single object")
    unknown = set(raw) - set(EVIDENCE_JSON_TOP_LEVEL_KEYS)
    if unknown:
        raise ValueError(f"unknown top-level keys in evidence JSON: {sorted(unknown)}")
    return raw


def _carry_forward() -> list[dict[str, str]]:
    return [
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "pip-audit may require --ignore-vuln CVE-2026-3219 for the pip toolchain until "
                "PyPI publishes an audit-clean release. M04 re-check 2026-04-25: latest PyPI pip "
                "26.0.1 still the only current release; pip-audit may still report CVE-2026-3219. "
                "Leave the single narrow ignore; remove when a fixed pip is published."
            ),
        },
        {
            "item_id": "v15_m05_strong_agent_benchmark_protocol",
            "summary": "V15-M05 — Strong-agent benchmark protocol; not M04.",
        },
    ]


def _m04_attestation() -> str:
    return (
        "V15-M04 defines and emits the XAI evidence contract and fixture evidence-pack surface. "
        "It may validate fixture metadata and may normalize supplied operator-declared XAI "
        "metadata, but it does not execute model inference, does not generate real attribution "
        "or saliency maps, does not run counterfactual evaluation, does not parse real replays, "
        "does not verify checkpoint bytes, does not prove explanation faithfulness, does not run "
        "benchmarks, does not run human evaluation, does not execute GPU training or shakedown, "
        "does not authorize a long GPU run, does not approve real XAI assets for claim-critical "
        "use, does not open v2, and does not open PX2-M04/PX2-M05."
    )


def _check_results_fixture() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "m04_contract_fields_present",
            "description": (
                "Fixture XAI pack includes required M04 vocabulary and required fields map."
            ),
            "status": CHECK_PASS,
        },
        {
            "check_id": "m04_not_executing_inference",
            "description": "M04 does not run GPU training, XAI inference, or replay parsing.",
            "status": CHECK_PASS,
        },
    ]


def _default_replay_identity() -> dict[str, Any]:
    return {
        "replay_id": "",
        "replay_reference": "",
        "replay_sha256": PLACEHOLDER_SHA256,
        "replay_binding_status": "not_evaluated",
        "source_milestone": "",
        "notes": "operator partial: replay_identity not supplied in evidence JSON",
    }


def _default_checkpoint_identity() -> dict[str, Any]:
    return {
        "checkpoint_id": "",
        "checkpoint_reference": "",
        "checkpoint_lineage_manifest_sha256": PLACEHOLDER_SHA256,
        "checkpoint_hash_verification_status": "not_evaluated",
        "checkpoint_binding_status": "not_evaluated",
        "source_milestone": "",
        "notes": "operator partial: checkpoint_identity not supplied in evidence JSON",
    }


def _fixture_replay_identity() -> dict[str, Any]:
    return {
        "replay_id": "fixture:replay_001",
        "replay_reference": "fixture:logical/replay_ref",
        "replay_sha256": PLACEHOLDER_SHA256,
        "replay_binding_status": "fixture",
        "source_milestone": "V15-M04",
        "notes": "Fixture replay identity; not a real replay file.",
    }


def _fixture_checkpoint_identity() -> dict[str, Any]:
    return {
        "checkpoint_id": "fixture:checkpoint_001",
        "checkpoint_reference": "fixture:logical/checkpoint_ref",
        "checkpoint_lineage_manifest_sha256": PLACEHOLDER_SHA256,
        "checkpoint_hash_verification_status": "fixture",
        "checkpoint_binding_status": "fixture",
        "source_milestone": "V15-M04",
        "notes": "Fixture checkpoint identity; M04 does not read weight blobs.",
    }


def _fixture_decision_trace() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "gameloop": 120,
            "agent_perspective": "terran_fixture",
            "decision_type": "macro",
            "selected_action": "build_structure_fixture",
            "selected_action_label": "Fixture build action",
            "available_alternatives_count": 3,
            "state_summary_reference": "fixture:state_summary/001",
            "input_feature_references": "fixture:feature_refs/001",
            "policy_head": "fixture_head",
            "confidence": 0.5,
            "trace_status": "fixture",
            "notes": "Fixture decision trace row; not model output.",
        }
    ]


def _fixture_critical_index() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "criticality_reason": "Opening build / fixture",
            "scene_type": "fixture",
            "expected_review_status": "fixture_pending",
            "linked_trace_status": "fixture",
            "notes": "Fixture criticality index; not a human review result.",
        }
    ]


def _fixture_attribution() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "method_id": "fixture_method",
            "feature_group": "economy",
            "attribution_score": 0.1,
            "normalization_policy": "fixture_norm",
            "attribution_status": "fixture",
            "notes": "Fixture attribution; not a saliency map.",
        }
    ]


def _fixture_concepts() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "concept_id": "concept_fixture_01",
            "concept_label": "Fixture concept",
            "activation_score": 0.2,
            "concept_source": "fixture",
            "concept_status": "fixture",
            "notes": "Fixture concept row; not concept discovery output.",
        }
    ]


def _fixture_counterfactuals() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "counterfactual_id": "fixture_counterfactual_001",
            "changed_factor": "fixture_factor",
            "original_action": "a0",
            "counterfactual_action": "a1",
            "outcome_delta_summary": "Fixture delta; not a counterfactual run.",
            "counterfactual_status": "fixture",
            "notes": "Fixture row only.",
        }
    ]


def _fixture_alternatives() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "rank": 2,
            "action_id": "act_fixture_alt",
            "action_label": "Fixture alternative",
            "score": 0.1,
            "why_not_selected_summary": "Lower score in fixture",
            "ranking_status": "fixture",
            "notes": "Fixture alternative ranking; not real policy scores.",
        }
    ]


def _fixture_uncertainty() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "fixture_decision_001",
            "uncertainty_kind": "entropy",
            "uncertainty_value": 0.4,
            "threshold_policy": "fixture_thresholds",
            "uncertainty_status": "fixture",
            "notes": "Fixture uncertainty; not real calibration.",
        }
    ]


def _fixture_overlays() -> list[dict[str, Any]]:
    return [
        {
            "overlay_id": "overlay_fixture_001",
            "decision_id": "fixture_decision_001",
            "overlay_kind": "fixture_overlay",
            "overlay_reference": "fixture:overlay/ref",
            "path_disclosure": "logical_reference_only",
            "overlay_status": "fixture",
            "notes": "Fixture overlay manifest; no image rendered.",
        }
    ]


def _fixture_explanation_reports() -> list[dict[str, Any]]:
    return [
        {
            "report_id": "report_fixture_001",
            "report_format": "md",
            "report_reference": "fixture:xai_explanation_report/001",
            "path_disclosure": "logical_reference_only",
            "report_status": "fixture",
            "notes": "Fixture explanation report metadata; not a real report file.",
        }
    ]


def _required_fields_map() -> dict[str, list[str]]:
    return {
        "replay_identity": list(REPLAY_IDENTITY_FIELDS),
        "checkpoint_identity": list(CHECKPOINT_IDENTITY_FIELDS),
        "decision_trace_row": list(DECISION_TRACE_ROW_FIELDS),
        "critical_decision_index_row": list(CRITICAL_DECISION_ROW_FIELDS),
        "attribution_summary_row": list(ATTRIBUTION_ROW_FIELDS),
        "concept_activation_summary_row": list(CONCEPT_ROW_FIELDS),
        "counterfactual_probe_row": list(COUNTERFACTUAL_ROW_FIELDS),
        "alternative_action_ranking_row": list(ALTERNATIVE_RANK_ROW_FIELDS),
        "uncertainty_report_row": list(UNCERTAINTY_ROW_FIELDS),
        "replay_overlay_manifest_row": list(OVERLAY_MANIFEST_ROW_FIELDS),
        "xai_explanation_report_row": list(EXPLANATION_REPORT_ROW_FIELDS),
    }


def _status_vocabulary_object() -> dict[str, list[str]]:
    return {k: list(v) for k, v in STATUS_VOCABULARY.items()}


def build_xai_evidence_body_fixture() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID_XAI_EVIDENCE,
        "milestone_id": MILESTONE_ID_V15_M04,
        "generated_by": EMITTER_MODULE,
        "profile": PROFILE_FIXTURE_CI,
        "xai_evidence_status": XAI_STATUS_FIXTURE_ONLY,
        "long_gpu_run_authorized": False,
        "real_xai_inference_executed": False,
        "replay_bound": False,
        "checkpoint_bound": False,
        "checkpoint_bytes_verified": False,
        "explanation_faithfulness_validated": False,
        "evidence_scope": EVIDENCE_CI_FIXTURE,
        "xai_pack_identity": {
            "xai_pack_id": "fixture:starlab_v15_xai_evidence_pack_v1",
            "contract_id": CONTRACT_ID_XAI_EVIDENCE,
            "milestone_id": MILESTONE_ID_V15_M04,
        },
        "replay_identity": _fixture_replay_identity(),
        "checkpoint_identity": _fixture_checkpoint_identity(),
        "decision_trace": _fixture_decision_trace(),
        "critical_decision_index": _fixture_critical_index(),
        "attribution_summary": _fixture_attribution(),
        "concept_activation_summary": _fixture_concepts(),
        "counterfactual_probe_results": _fixture_counterfactuals(),
        "alternative_action_rankings": _fixture_alternatives(),
        "uncertainty_report": _fixture_uncertainty(),
        "replay_overlay_manifest": _fixture_overlays(),
        "xai_explanation_report": _fixture_explanation_reports(),
        "required_artifact_names": list(REQUIRED_LOGICAL_ARTIFACT_NAMES),
        "status_vocabulary": _status_vocabulary_object(),
        "scene_type_vocabulary": list(SCENE_TYPE_VOCABULARY),
        "method_vocabulary": list(METHOD_VOCABULARY_EXAMPLES),
        "path_disclosure_vocabulary": list(STATUS_VOCABULARY["path_disclosure"]),
        "required_fields": _required_fields_map(),
        "check_results": _check_results_fixture(),
        "m04_verification_attestation": _m04_attestation(),
        "non_claims": list(NON_CLAIMS_V15_M04),
        "carry_forward_items": _carry_forward(),
    }


def _get_list(
    data: dict[str, Any],
    key: str,
) -> list[dict[str, Any]]:
    v = data.get(key)
    if v is None:
        return []
    if not isinstance(v, list):
        raise ValueError(f"{key} must be a list or null")
    return [deepcopy(x) for x in v]


def _as_str(v: Any, field: str) -> str:
    if not isinstance(v, str):
        raise TypeError(f"{field} must be a string")
    return v


def _validate_enum_row(group: str, value: str, ctx: str) -> None:
    if not _in_vocab(group, value):
        raise ValueError(f"{ctx}: invalid {group} {value!r}")


def _validate_decision_row(row: dict[str, Any], i: int) -> None:
    ctx = f"decision_trace[{i}]"
    _validate_row_fields(row, DECISION_TRACE_ROW_FIELDS, ctx)
    _validate_enum_row("trace_status", str(row["trace_status"]), ctx)
    for fn in ("gameloop", "available_alternatives_count"):
        if not isinstance(row[fn], int) or isinstance(row[fn], bool):
            raise TypeError(f"{ctx} {fn} must be an int")
    if not isinstance(row["confidence"], (int, float)) or isinstance(row["confidence"], bool):
        raise TypeError(f"{ctx} confidence must be a number")


def _validate_critical_row(row: dict[str, Any], i: int) -> None:
    ctx = f"critical_decision_index[{i}]"
    _validate_row_fields(row, CRITICAL_DECISION_ROW_FIELDS, ctx)
    st = str(row["scene_type"])
    if st not in SCENE_TYPE_VOCABULARY:
        raise ValueError(f"{ctx} invalid scene_type {st!r}")
    _validate_enum_row("trace_status", str(row["linked_trace_status"]), ctx)


def _validate_attribution_row(row: dict[str, Any], i: int) -> None:
    ctx = f"attribution_summary[{i}]"
    _validate_row_fields(row, ATTRIBUTION_ROW_FIELDS, ctx)
    _validate_enum_row("attribution_status", str(row["attribution_status"]), ctx)
    if not isinstance(row["attribution_score"], (int, float)) or isinstance(
        row["attribution_score"], bool
    ):
        raise TypeError(f"{ctx} attribution_score must be a number")


def _validate_concept_row(row: dict[str, Any], i: int) -> None:
    ctx = f"concept_activation_summary[{i}]"
    _validate_row_fields(row, CONCEPT_ROW_FIELDS, ctx)
    _validate_enum_row("concept_status", str(row["concept_status"]), ctx)
    if not isinstance(row["activation_score"], (int, float)) or isinstance(
        row["activation_score"], bool
    ):
        raise TypeError(f"{ctx} activation_score must be a number")


def _validate_counterfactual_row(row: dict[str, Any], i: int) -> None:
    ctx = f"counterfactual_probe_results[{i}]"
    _validate_row_fields(row, COUNTERFACTUAL_ROW_FIELDS, ctx)
    _validate_enum_row("counterfactual_status", str(row["counterfactual_status"]), ctx)


def _validate_alternative_row(row: dict[str, Any], i: int) -> None:
    ctx = f"alternative_action_rankings[{i}]"
    _validate_row_fields(row, ALTERNATIVE_RANK_ROW_FIELDS, ctx)
    _validate_enum_row("ranking_status", str(row["ranking_status"]), ctx)
    if not isinstance(row["rank"], int) or isinstance(row["rank"], bool):
        raise TypeError(f"{ctx} rank must be an int")
    if not isinstance(row["score"], (int, float)) or isinstance(row["score"], bool):
        raise TypeError(f"{ctx} score must be a number")


def _validate_uncertainty_row(row: dict[str, Any], i: int) -> None:
    ctx = f"uncertainty_report[{i}]"
    _validate_row_fields(row, UNCERTAINTY_ROW_FIELDS, ctx)
    _validate_enum_row("uncertainty_status", str(row["uncertainty_status"]), ctx)
    if not isinstance(row["uncertainty_value"], (int, float)) or isinstance(
        row["uncertainty_value"], bool
    ):
        raise TypeError(f"{ctx} uncertainty_value must be a number")


def _validate_overlay_row(row: dict[str, Any], i: int) -> None:
    ctx = f"replay_overlay_manifest[{i}]"
    _validate_row_fields(row, OVERLAY_MANIFEST_ROW_FIELDS, ctx)
    _validate_enum_row("path_disclosure", str(row["path_disclosure"]), ctx)
    _validate_enum_row("overlay_status", str(row["overlay_status"]), ctx)


def _validate_explanation_row(row: dict[str, Any], i: int) -> None:
    ctx = f"xai_explanation_report[{i}]"
    _validate_row_fields(row, EXPLANATION_REPORT_ROW_FIELDS, ctx)
    _validate_enum_row("path_disclosure", str(row["path_disclosure"]), ctx)
    _validate_enum_row("report_status", str(row["report_status"]), ctx)


def _validate_replay_identity(obj: Any) -> dict[str, Any]:
    if not isinstance(obj, dict):
        raise ValueError("replay_identity must be an object")
    _validate_row_fields(obj, REPLAY_IDENTITY_FIELDS, "replay_identity")
    _validate_enum_row(
        "replay_binding_status",
        str(obj["replay_binding_status"]),
        "replay_identity",
    )
    return obj


def _validate_checkpoint_identity(obj: Any) -> dict[str, Any]:
    if not isinstance(obj, dict):
        raise ValueError("checkpoint_identity must be an object")
    _validate_row_fields(obj, CHECKPOINT_IDENTITY_FIELDS, "checkpoint_identity")
    _validate_enum_row(
        "checkpoint_hash_verification_status",
        str(obj["checkpoint_hash_verification_status"]),
        "checkpoint_identity",
    )
    _validate_enum_row(
        "checkpoint_binding_status",
        str(obj["checkpoint_binding_status"]),
        "checkpoint_identity",
    )
    return obj


def _operator_complete(
    replay: dict[str, Any],
    cp: dict[str, Any],
    sections: list[list[dict[str, Any]]],
) -> bool:
    if not str(replay.get("replay_id", "")).strip():
        return False
    if not str(cp.get("checkpoint_id", "")).strip():
        return False
    return all(len(s) >= 1 for s in sections)


def _resolve_binding_flags(replay: dict[str, Any], cp: dict[str, Any]) -> tuple[bool, bool, bool]:
    r_st = str(replay.get("replay_binding_status", ""))
    c_st = str(cp.get("checkpoint_binding_status", ""))
    r_ok = r_st in ("bound_external", "declared_only")
    c_ok = c_st in ("bound_external", "declared_only")
    r_b = r_ok and bool(str(replay.get("replay_id", "")).strip())
    c_b = c_ok and bool(str(cp.get("checkpoint_id", "")).strip())
    h_ver = str(cp.get("checkpoint_hash_verification_status", ""))
    c_bytes = h_ver == "verified_external"
    return r_b, c_b, c_bytes


def build_xai_evidence_body_operator(
    data: dict[str, Any],
    *,
    environment_lock_path: Path | None,
    checkpoint_lineage_path: Path | None,
) -> dict[str, Any]:
    prof = data.get("profile")
    if prof is not None and prof != "operator_declared":
        raise ValueError("evidence JSON profile, if set, must be 'operator_declared'")

    raw_ri = data.get("replay_identity")
    raw_cp = data.get("checkpoint_identity")
    replay = _default_replay_identity() if raw_ri is None else _validate_replay_identity(raw_ri)
    cp = _default_checkpoint_identity() if raw_cp is None else _validate_checkpoint_identity(raw_cp)

    if checkpoint_lineage_path is not None:
        lineage_sha = environment_lock_file_canonical_sha256(checkpoint_lineage_path)
        cp = {**cp, "checkpoint_lineage_manifest_sha256": lineage_sha}
    if environment_lock_path is not None:
        env_sha = environment_lock_file_canonical_sha256(environment_lock_path)
        ref = str(cp.get("checkpoint_reference", ""))
        cp = {
            **cp,
            "checkpoint_reference": (
                f"{ref} | m02_environment_lock_canonical_sha256={env_sha}"
                if ref
                else f"m02_environment_lock_canonical_sha256={env_sha}"
            ),
            "notes": (
                str(cp.get("notes", ""))
                + " | m02 environment lock file bound by canonical sha (path not stored)."
            ).strip(),
        }

    dt = _get_list(data, "decision_trace")
    cdi = _get_list(data, "critical_decision_index")
    attr = _get_list(data, "attribution_summary")
    conc = _get_list(data, "concept_activation_summary")
    cf = _get_list(data, "counterfactual_probe_results")
    alt = _get_list(data, "alternative_action_rankings")
    unc = _get_list(data, "uncertainty_report")
    ovl = _get_list(data, "replay_overlay_manifest")
    xrep = _get_list(data, "xai_explanation_report")

    for i, row in enumerate(dt):
        _validate_decision_row(row, i)
    for i, row in enumerate(cdi):
        _validate_critical_row(row, i)
    for i, row in enumerate(attr):
        _validate_attribution_row(row, i)
    for i, row in enumerate(conc):
        _validate_concept_row(row, i)
    for i, row in enumerate(cf):
        _validate_counterfactual_row(row, i)
    for i, row in enumerate(alt):
        _validate_alternative_row(row, i)
    for i, row in enumerate(unc):
        _validate_uncertainty_row(row, i)
    for i, row in enumerate(ovl):
        _validate_overlay_row(row, i)
    for i, row in enumerate(xrep):
        _validate_explanation_row(row, i)

    sections: list[list[dict[str, Any]]] = [dt, cdi, attr, conc, cf, alt, unc, ovl, xrep]
    explicit_status = data.get("xai_evidence_status")
    if explicit_status is not None and str(explicit_status) == XAI_STATUS_BLOCKED:
        xai_status: str = XAI_STATUS_BLOCKED
    elif _operator_complete(replay, cp, sections):
        xai_status = XAI_STATUS_OP_COMPLETE
    else:
        xai_status = XAI_STATUS_OP_INCOMPLETE

    ev_scope: str
    if xai_status == XAI_STATUS_BLOCKED:
        ev_scope = EVIDENCE_NOT_EVALUATED
    elif xai_status == XAI_STATUS_OP_COMPLETE:
        ev_scope = EVIDENCE_OPERATOR_DECLARED
    else:
        ev_scope = EVIDENCE_OPERATOR_LOCAL_METADATA

    r_inf = data.get("real_xai_inference_executed")
    r_bool = bool(r_inf) if r_inf is not None else False
    f_val = data.get("explanation_faithfulness_validated")
    f_bool = bool(f_val) if f_val is not None else False

    replay_b, cp_b, cp_bytes = _resolve_binding_flags(replay, cp)

    pack_id = data.get("xai_pack_id")
    pack_s = "operator:undeclared" if pack_id is None else _as_str(pack_id, "xai_pack_id")

    onotes = data.get("operator_notes")
    op_n = None if onotes is None else _as_str(onotes, "operator_notes")
    extra_non = data.get("non_claims")
    base_non = list(NON_CLAIMS_V15_M04)
    if extra_non is not None:
        if not isinstance(extra_non, list) or not all(isinstance(x, str) for x in extra_non):
            raise TypeError("non_claims must be a list of strings or null")
        base_non = base_non + [str(x) for x in extra_non]

    out: dict[str, Any] = {
        "contract_id": CONTRACT_ID_XAI_EVIDENCE,
        "milestone_id": MILESTONE_ID_V15_M04,
        "generated_by": EMITTER_MODULE,
        "profile": PROFILE_OPERATOR_DECLARED,
        "xai_evidence_status": xai_status,
        "long_gpu_run_authorized": False,
        "real_xai_inference_executed": r_bool,
        "replay_bound": replay_b,
        "checkpoint_bound": cp_b,
        "checkpoint_bytes_verified": cp_bytes,
        "explanation_faithfulness_validated": f_bool,
        "evidence_scope": ev_scope,
        "xai_pack_identity": {
            "xai_pack_id": pack_s,
            "contract_id": CONTRACT_ID_XAI_EVIDENCE,
            "milestone_id": MILESTONE_ID_V15_M04,
        },
        "replay_identity": replay,
        "checkpoint_identity": cp,
        "decision_trace": dt,
        "critical_decision_index": cdi,
        "attribution_summary": attr,
        "concept_activation_summary": conc,
        "counterfactual_probe_results": cf,
        "alternative_action_rankings": alt,
        "uncertainty_report": unc,
        "replay_overlay_manifest": ovl,
        "xai_explanation_report": xrep,
        "required_artifact_names": list(REQUIRED_LOGICAL_ARTIFACT_NAMES),
        "status_vocabulary": _status_vocabulary_object(),
        "scene_type_vocabulary": list(SCENE_TYPE_VOCABULARY),
        "method_vocabulary": list(METHOD_VOCABULARY_EXAMPLES),
        "path_disclosure_vocabulary": list(STATUS_VOCABULARY["path_disclosure"]),
        "required_fields": _required_fields_map(),
        "check_results": _check_results_operator(xai_status),
        "m04_verification_attestation": _m04_attestation(),
        "non_claims": base_non,
        "carry_forward_items": _carry_forward(),
    }
    if op_n is not None:
        out["operator_notes"] = op_n
    return out


def _check_results_operator(status: str) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "m04_operator_xai_status",
            "description": f"Operator evidence resolved to {status}.",
            "status": CHECK_PASS
            if status in (XAI_STATUS_OP_COMPLETE, XAI_STATUS_OP_INCOMPLETE, XAI_STATUS_BLOCKED)
            else CHECK_FAIL,
        }
    ]


def build_xai_evidence_body(
    profile: str,
    *,
    evidence_data: dict[str, Any] | None = None,
    environment_lock_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
) -> dict[str, Any]:
    if profile == PROFILE_FIXTURE_CI:
        return build_xai_evidence_body_fixture()
    if profile == PROFILE_OPERATOR_DECLARED:
        if evidence_data is None:
            raise ValueError("operator_declared profile requires evidence JSON data")
        return build_xai_evidence_body_operator(
            evidence_data,
            environment_lock_path=environment_lock_path,
            checkpoint_lineage_path=checkpoint_lineage_path,
        )
    raise ValueError(f"unknown profile: {profile!r}")


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_XAI_EVIDENCE
    assert body["milestone_id"] == MILESTONE_ID_V15_M04
    assert set(body["status_vocabulary"]["xai_evidence_status"]) == set(
        STATUS_VOCABULARY["xai_evidence_status"]
    )
    assert body["long_gpu_run_authorized"] is False


def seal_xai_evidence_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, SEAL_KEY_XAI_EVIDENCE: digest}


def build_xai_evidence_report(
    contract: dict[str, Any], *, emission_context: dict[str, Any] | None = None
) -> dict[str, Any]:
    digest = contract[SEAL_KEY_XAI_EVIDENCE]
    n_dt = len(contract["decision_trace"])
    n_cd = len(contract["critical_decision_index"])
    n_cf = len(contract["counterfactual_probe_results"])
    n_alt = len(contract["alternative_action_rankings"])
    rep: dict[str, Any] = {
        "report_version": REPORT_VERSION_XAI_EVIDENCE,
        "milestone_id": MILESTONE_ID_V15_M04,
        "xai_evidence_pack_sha256": digest,
        "contract_id": CONTRACT_ID_XAI_EVIDENCE,
        "profile": contract["profile"],
        "xai_evidence_status": contract["xai_evidence_status"],
        "decision_trace_count": n_dt,
        "critical_decision_count": n_cd,
        "counterfactual_count": n_cf,
        "alternative_action_count": n_alt,
        "non_claims_summary": {
            "count": len(contract["non_claims"]),
            "m04_does_not_authorize_long_run": contract["long_gpu_run_authorized"] is False,
        },
        "validation": {
            "contract_id_recognized": contract["contract_id"] == CONTRACT_ID_XAI_EVIDENCE,
            "seal_key_present": SEAL_KEY_XAI_EVIDENCE in contract,
            "m04_never_authorizes_long_run": contract["long_gpu_run_authorized"] is False,
        },
    }
    if emission_context is not None:
        rep["emission_context"] = emission_context
    return rep


def write_xai_evidence_artifacts(
    *,
    output_dir: Path,
    contract: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_XAI_EVIDENCE
    r_path = output_dir / REPORT_FILENAME_XAI_EVIDENCE
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_v15_xai_evidence_pack(
    output_dir: Path,
    *,
    profile: str,
    evidence_path: Path | None = None,
    environment_lock_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    emission_context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    evidence_data: dict[str, Any] | None = None
    if evidence_path is not None:
        evidence_data = parse_evidence_json(evidence_path)

    body = build_xai_evidence_body(
        profile,
        evidence_data=evidence_data,
        environment_lock_path=environment_lock_path,
        checkpoint_lineage_path=checkpoint_lineage_path,
    )
    if profile == PROFILE_OPERATOR_DECLARED and evidence_data is not None:
        body = redact_paths_in_value(body)
    _validate_body_invariants(body)

    sealed = seal_xai_evidence_body(body)
    ctx = emission_context
    if ctx is None and profile == PROFILE_FIXTURE_CI:
        ctx = {
            "emission_mode": "fixture",
            "emission_context_note": "deterministic; no model inference; no replay reads",
        }
    rep = build_xai_evidence_report(sealed, emission_context=ctx)
    c_path, r_path = write_xai_evidence_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
