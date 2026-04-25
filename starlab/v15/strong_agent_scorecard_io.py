"""Build, seal, and write V15-M05 strong-agent scorecard (protocol only; no benchmark execution)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.strong_agent_scorecard_models import (
    BASELINE_SUBJECT_FIELDS,
    BENCHMARK_STATUS_FIXTURE_ONLY,
    BENCHMARK_STATUS_OP_COMPLETE,
    BENCHMARK_STATUS_OP_INCOMPLETE,
    CANDIDATE_SUBJECT_FIELDS,
    CHECK_PASS,
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    EMITTER_MODULE_STRONG_AGENT,
    EVIDENCE_REQUIREMENT_FIELDS,
    EVIDENCE_SCOPE_FIXTURE_PROTOCOL,
    EVIDENCE_SCOPE_NOT_EVALUATED,
    EVIDENCE_SCOPE_OPERATOR_DECLARED,
    FAILURE_PROBE_FIELDS,
    FILENAME_STRONG_AGENT_SCORECARD,
    GATE_THRESHOLD_FIELDS,
    LADDER_STAGE_IDS,
    LADDER_STAGE_TITLES,
    MAP_POOL_FIELDS,
    MILESTONE_ID_V15_M05,
    NON_CLAIMS_V15_M05,
    OPPONENT_POOL_FIELDS,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROTOCOL_JSON_TOP_LEVEL_KEYS,
    PROTOCOL_PROFILE_ID,
    REPORT_FILENAME_STRONG_AGENT_SCORECARD,
    REPORT_VERSION_STRONG_AGENT,
    REQUIRED_SCORECARD_METRIC_NAMES,
    SCORECARD_FIELD_DEF_FIELDS,
    SEAL_KEY_STRONG_AGENT,
    STATUS_VOCABULARY,
    XAI_REQUIREMENT_FIELDS,
)
from starlab.v15.xai_evidence_models import CONTRACT_ID_XAI_EVIDENCE

SEAL = SEAL_KEY_STRONG_AGENT
_METRIC_VOCAB: Final[tuple[str, ...]] = REQUIRED_SCORECARD_METRIC_NAMES
_GATE_VOCAB: Final[tuple[str, ...]] = (
    "win_rate",
    "loss_rate",
    "min_games",
    "confidence_interval_policy",
    "scouting_score_floor",
    "xai_trace_coverage",
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


def _vocab_object() -> dict[str, list[str]]:
    return {k: list(v) for k, v in STATUS_VOCABULARY.items()}


def _metric_vocab_object() -> dict[str, str]:
    return {m: f"strong_agent scorecard metric / protocol field: {m}" for m in _METRIC_VOCAB}


def _gate_vocab_object() -> dict[str, str]:
    return {g: f"gate or threshold target vocabulary entry: {g}" for g in _GATE_VOCAB}


def _evidence_kind_vocab_object() -> dict[str, str]:
    t = _vocab_object()["evidence_kind"]
    return {k: f"evidence class: {k}" for k in t}


def _validate_row(row: Any, fields: tuple[str, ...], ctx: str) -> None:
    if not isinstance(row, dict):
        raise ValueError(f"{ctx} must be an object")
    for k in fields:
        if k not in row:
            raise ValueError(f"{ctx} missing field {k!r}")
    for k in row:
        if k not in fields:
            raise ValueError(f"{ctx} unknown field {k!r}")


def _stages_for_fixture() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for sid in LADDER_STAGE_IDS:
        st: str
        if sid == "E7_human_panel_reserved":
            st = "not_evaluated"
        elif sid == "E8_xai_review_reserved":
            st = "not_evaluated"
        elif sid in ("E0_artifact_integrity", "E1_fixture_smoke"):
            st = "fixture"
        else:
            st = "defined"
        out.append(
            {
                "stage_id": sid,
                "stage_name": LADDER_STAGE_TITLES[sid],
                "stage_status": st,
                "owner_milestone": (
                    "V15-M06+"
                    if sid == "E7_human_panel_reserved"
                    else ("V15-M10+" if sid == "E8_xai_review_reserved" else "TBD")
                ),
                "notes": (
                    "Fixture ladder row; M05 does not execute this stage."
                    if st == "fixture"
                    else "Defined only in M05; not executed in M05."
                ),
            }
        )
    return out


def _scorecard_field_definitions_fixture() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name in REQUIRED_SCORECARD_METRIC_NAMES:
        rows.append(
            {
                "field_name": name,
                "field_type": "ratio" if "rate" in name or name.endswith("_score") else "count",
                "required": True,
                "description": (
                    f"Protocol field `{name}` for strong-agent scorecard "
                    "(no measured value in M05)."
                ),
                "status": "defined",
            }
        )
    return rows


def _gates_fixture() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "gate_win_rate_floor",
            "gate_name": "Minimum win rate vs declared opponent pool (protocol-only)",
            "metric_name": "win_rate",
            "comparison": ">=",
            "threshold_value": "declared_in_operator_protocol",
            "required": True,
            "gate_status": "fixture",
            "notes": "Fixture threshold placeholder; M05 does not evaluate.",
        },
        {
            "gate_id": "gate_invalid_action_ceiling",
            "gate_name": "Maximum invalid action rate (safety / legality)",
            "metric_name": "invalid_action_rate",
            "comparison": "<=",
            "threshold_value": "declared_in_operator_protocol",
            "required": True,
            "gate_status": "not_evaluated",
            "notes": "Gate defined for later evaluation milestones.",
        },
    ]


def _evidence_req_fixture() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "ev_env_lock",
            "evidence_kind": "environment_lock",
            "required": True,
            "source_contract": "starlab.v15.long_gpu_environment_lock.v1",
            "evidence_status": "fixture",
            "notes": "Binds to M02 environment lock by SHA when available.",
        },
        {
            "evidence_id": "ev_lineage",
            "evidence_kind": "checkpoint_lineage",
            "required": True,
            "source_contract": "starlab.v15.checkpoint_lineage_manifest.v1",
            "evidence_status": "fixture",
            "notes": "Metadata-only lineage; no weight blob I/O in M05.",
        },
        {
            "evidence_id": "ev_xai_pack",
            "evidence_kind": "xai_evidence_pack",
            "required": True,
            "source_contract": CONTRACT_ID_XAI_EVIDENCE,
            "evidence_status": "not_evaluated",
            "notes": "XAI pack contract; real inference is out of scope for M05.",
        },
    ]


def _probes_fixture() -> list[dict[str, Any]]:
    return [
        {
            "probe_id": "probe_exploit_economy",
            "probe_kind": "exploit_economy",
            "required": True,
            "probe_status": "not_evaluated",
            "notes": "Failure-mode probe reserved for later execution milestones.",
        }
    ]


def _xai_req_fixture() -> list[dict[str, Any]]:
    return [
        {
            "xai_requirement_id": "xair_trace_coverage",
            "required_artifact": "decision_trace.json (logical; XAI contract)",
            "required": True,
            "source_contract": CONTRACT_ID_XAI_EVIDENCE,
            "requirement_status": "defined",
            "notes": "M05 may require trace coverage in protocol; M10+ executes XAI review.",
        }
    ]


def _reserved_human_panel() -> dict[str, Any]:
    return {
        "reserved": True,
        "owner_milestone": "V15-M06",
        "execution_performed": False,
        "claim_authorized": False,
        "non_claim": ("Human-panel benchmark execution is not part of M05; reserved for V15-M06+."),
    }


def _xai_review_reserved() -> dict[str, Any]:
    return {
        "reserved": True,
        "owner_milestone": "V15-M10+",
        "review_performed": False,
        "faithfulness_validated": False,
        "non_claim": (
            "Real XAI review and faithfulness validation are reserved for V15-M10+; "
            "M05 is protocol only."
        ),
    }


def _required_fields_map() -> dict[str, list[str]]:
    return {
        "contract": [
            "contract_id",
            "protocol_profile_id",
            "milestone_id",
            "benchmark_protocol_status",
            "benchmark_identity",
        ],
        "operator_protocol_json": list(PROTOCOL_JSON_TOP_LEVEL_KEYS),
        "candidate_subject": list(CANDIDATE_SUBJECT_FIELDS),
        "baseline_subject_row": list(BASELINE_SUBJECT_FIELDS),
        "map_pool": list(MAP_POOL_FIELDS),
        "opponent_pool": list(OPPONENT_POOL_FIELDS),
        "gate_row": list(GATE_THRESHOLD_FIELDS),
        "scorecard_field_row": list(SCORECARD_FIELD_DEF_FIELDS),
        "evidence_requirement": list(EVIDENCE_REQUIREMENT_FIELDS),
        "failure_probe": list(FAILURE_PROBE_FIELDS),
        "xai_requirement": list(XAI_REQUIREMENT_FIELDS),
    }


def _check_results_fixture() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "m05_protocol_fields",
            "description": (
                "Fixture strong-agent scorecard includes ladder, vocabularies, and non-claims."
            ),
            "status": CHECK_PASS,
        },
        {
            "check_id": "m05_no_benchmark_execution",
            "description": "M05 does not run benchmarks, live SC2, or checkpoint evaluation.",
            "status": CHECK_PASS,
        },
    ]


def _carry_forward() -> list[dict[str, str]]:
    return [
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "Re-check 2026-04-24 (M05): `pip index versions pip` still shows 26.0.1 as latest; "
                "no newer audit-clean pip on PyPI observed — keep the single pip-audit "
                "`--ignore-vuln CVE-2026-3219` until a fixed release exists."
            ),
        },
        {
            "item_id": "v15_m06_human_panel_protocol",
            "summary": "V15-M06+ — Human panel benchmark protocol; not M05.",
        },
    ]


def _attestation() -> str:
    return (
        "V15-M05 defines and emits the strong-agent benchmark protocol and scorecard contract. "
        "It may validate fixture protocol metadata and may normalize supplied operator-declared "
        "protocol metadata, but it does not execute benchmarks, does not run live SC2, and does "
        "not evaluate a checkpoint, does not select or promote a strong agent, does not run XAI "
        "review, and does not run human-panel evaluation, does not execute GPU training or "
        "shakedown, does not authorize a long GPU run, does not approve real assets for "
        "claim-critical use, does "
        "not open v2, and does not open PX2-M04/PX2-M05."
    )


def build_strong_agent_scorecard_body_fixture() -> dict[str, Any]:
    candidate = {
        "subject_id": "fixture_candidate",
        "subject_kind": "fixture_candidate",
        "checkpoint_id": "fixture:checkpoint_reference_only",
        "checkpoint_lineage_manifest_sha256": PLACEHOLDER_SHA256,
        "environment_lock_sha256": PLACEHOLDER_SHA256,
        "training_run_reference": "fixture:training_run",
        "claim_use": "fixture_protocol_only",
        "subject_status": "fixture",
        "notes": "Fixture metadata only; not an evaluated or promoted agent.",
    }
    baselines = [
        {
            "subject_id": "fixture_scripted_baseline",
            "subject_kind": "scripted_baseline",
            "baseline_family": "m21_scripted_baseline_suite",
            "source_milestone": "M21",
            "scorecard_reference": "logical:scripted_baseline_suite",
            "subject_status": "fixture",
            "notes": "Fixture baseline; not a measured tournament result.",
        },
        {
            "subject_id": "fixture_heuristic_baseline",
            "subject_kind": "heuristic_baseline",
            "baseline_family": "m22_heuristic_baseline_suite",
            "source_milestone": "M22",
            "scorecard_reference": "logical:heuristic_baseline_suite",
            "subject_status": "fixture",
            "notes": "Fixture baseline; not a measured tournament result.",
        },
    ]
    mpool = {
        "map_pool_id": "fixture:map_pool_001",
        "map_pool_name": "Fixture map pool (protocol only)",
        "map_ids": ["fixture_map_a", "fixture_map_b"],
        "map_source": "fixture_logical",
        "rights_posture": "fixture_only",
        "map_pool_status": "fixture",
        "notes": "No real map files or live SC2 in M05.",
    }
    opool = {
        "opponent_pool_id": "fixture:opponent_pool_001",
        "opponent_kinds": ["scripted_baseline", "heuristic_baseline", "fixture_agent"],
        "opponent_ids": ["fixture_opponent_1", "fixture_opponent_2"],
        "pool_status": "fixture",
        "notes": "Synthetic opponents for protocol shape only.",
    }
    return {
        "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
        "milestone_id": MILESTONE_ID_V15_M05,
        "generated_by": EMITTER_MODULE_STRONG_AGENT,
        "profile": PROFILE_FIXTURE_CI,
        "benchmark_protocol_status": BENCHMARK_STATUS_FIXTURE_ONLY,
        "benchmark_execution_performed": False,
        "strong_agent_claim_authorized": False,
        "long_gpu_run_authorized": False,
        "candidate_checkpoint_evaluated": False,
        "human_panel_included": False,
        "live_sc2_included": False,
        "xai_review_performed": False,
        "evidence_scope": EVIDENCE_SCOPE_FIXTURE_PROTOCOL,
        "benchmark_identity": {
            "benchmark_id": "starlab.v15.strong_agent_benchmark.v1:fixture",
            "benchmark_name": "STARLAB v1.5 strong-agent benchmark (protocol fixture)",
            "protocol_profile_id": PROTOCOL_PROFILE_ID,
        },
        "evaluation_ladder": _stages_for_fixture(),
        "candidate_subject": candidate,
        "baseline_subjects": baselines,
        "map_pool": mpool,
        "opponent_pool": opool,
        "scorecard_fields": _scorecard_field_definitions_fixture(),
        "gate_thresholds": _gates_fixture(),
        "evidence_requirements": _evidence_req_fixture(),
        "failure_mode_probes": _probes_fixture(),
        "xai_requirements": _xai_req_fixture(),
        "reserved_human_panel_section": _reserved_human_panel(),
        "xai_review_reserved": _xai_review_reserved(),
        "optional_bindings": {
            "checkpoint_lineage_json_canonical_sha256": None,
            "xai_evidence_json_canonical_sha256": None,
            "environment_lock_json_canonical_sha256": None,
        },
        "status_vocabulary": _vocab_object(),
        "subject_kind_vocabulary": list(STATUS_VOCABULARY["subject_kind"]),
        "metric_vocabulary": _metric_vocab_object(),
        "gate_vocabulary": _gate_vocab_object(),
        "evidence_kind_vocabulary": _evidence_kind_vocab_object(),
        "required_fields": _required_fields_map(),
        "check_results": _check_results_fixture(),
        "m05_verification_attestation": _attestation(),
        "non_claims": list(NON_CLAIMS_V15_M05),
        "carry_forward_items": _carry_forward(),
    }


def _is_nonempty_val(x: Any) -> bool:
    if x is None:
        return False
    if isinstance(x, (list, dict, str)) and len(x) == 0:
        return False
    return True


def _default_candidate_subject() -> dict[str, str]:
    return {k: "" for k in CANDIDATE_SUBJECT_FIELDS}


def _default_map_pool() -> dict[str, Any]:
    return {
        "map_pool_id": "",
        "map_pool_name": "",
        "map_ids": [],
        "map_source": "",
        "rights_posture": "",
        "map_pool_status": "",
        "notes": "",
    }


def _default_opponent_pool() -> dict[str, Any]:
    return {
        "opponent_pool_id": "",
        "opponent_kinds": [],
        "opponent_ids": [],
        "pool_status": "",
        "notes": "",
    }


def _default_human_panel_reserved() -> dict[str, Any]:
    return {
        "reserved": True,
        "owner_milestone": "V15-M06",
        "execution_performed": False,
        "claim_authorized": False,
        "non_claim": "Placeholder; complete operator protocol should replace with declared text.",
    }


def _default_operator_protocol() -> dict[str, Any]:
    return {
        "profile": PROFILE_OPERATOR_DECLARED,
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
        "benchmark_id": "",
        "benchmark_name": "",
        "evaluation_ladder": [],
        "candidate_subject": _default_candidate_subject(),
        "baseline_subjects": [],
        "map_pool": _default_map_pool(),
        "opponent_pool": _default_opponent_pool(),
        "scorecard_fields": [],
        "gate_thresholds": [],
        "evidence_requirements": [],
        "failure_mode_probes": [],
        "xai_requirements": [],
        "human_panel_reserved": _default_human_panel_reserved(),
        "operator_notes": "",
        "non_claims": [],
    }


def merge_operator_protocol(overlay: dict[str, Any]) -> dict[str, Any]:
    """Merge operator JSON over defaults: object sections get shallow-merged with defaults."""

    base = _default_operator_protocol()
    for k, v in overlay.items():
        if k == "candidate_subject" and isinstance(v, dict):
            base[k] = {**_default_candidate_subject(), **v}
        elif k == "map_pool" and isinstance(v, dict):
            base[k] = {**_default_map_pool(), **v}
        elif k == "opponent_pool" and isinstance(v, dict):
            base[k] = {**_default_opponent_pool(), **v}
        elif k == "human_panel_reserved" and isinstance(v, dict):
            base[k] = {**_default_human_panel_reserved(), **v}
        else:
            base[k] = v
    return base


def _operator_protocol_complete(data: dict[str, Any]) -> bool:
    for k in PROTOCOL_JSON_TOP_LEVEL_KEYS:
        if k not in data:
            return False
    if not _is_nonempty_val(data.get("benchmark_id")) or not _is_nonempty_val(
        data.get("benchmark_name")
    ):
        return False
    el = data.get("evaluation_ladder")
    if not isinstance(el, list) or len(el) < 1:
        return False
    for st in el:
        if not isinstance(st, dict):
            return False
        for req in ("stage_id", "stage_name", "stage_status"):
            if req not in st or not str(st[req]).strip():
                return False
    cs = data.get("candidate_subject")
    if not isinstance(cs, dict):
        return False
    for f in CANDIDATE_SUBJECT_FIELDS:
        if f == "notes":
            continue
        if f not in cs or not str(cs.get(f, "")).strip():
            return False
    bs = data.get("baseline_subjects")
    if not isinstance(bs, list) or len(bs) < 1:
        return False
    for i, row in enumerate(bs):
        if not isinstance(row, dict):
            return False
        try:
            _validate_row(row, BASELINE_SUBJECT_FIELDS, f"baseline_subjects[{i}]")
        except ValueError:
            return False
    mp = data.get("map_pool")
    if not isinstance(mp, dict):
        return False
    try:
        _validate_row(mp, MAP_POOL_FIELDS, "map_pool")
    except ValueError:
        return False
    op_ = data.get("opponent_pool")
    if not isinstance(op_, dict):
        return False
    try:
        _validate_row(op_, OPPONENT_POOL_FIELDS, "opponent_pool")
    except ValueError:
        return False
    for name in (
        "scorecard_fields",
        "gate_thresholds",
        "evidence_requirements",
        "failure_mode_probes",
        "xai_requirements",
    ):
        arr = data.get(name)
        if not isinstance(arr, list) or len(arr) < 1:
            return False
    hpr = data.get("human_panel_reserved")
    if not isinstance(hpr, dict) or not hpr:
        return False
    ncl = data.get("non_claims")
    if not isinstance(ncl, list) or not all(isinstance(x, str) for x in ncl):
        return False

    # All required scorecard metrics declared when lists are well-formed
    sc = data.get("scorecard_fields")
    if not isinstance(sc, list):
        return False
    for i, row in enumerate(sc):
        if not isinstance(row, dict):
            return False
        try:
            _validate_row(row, SCORECARD_FIELD_DEF_FIELDS, f"scorecard_fields[{i}]")
        except ValueError:
            return False
    present = {str(r.get("field_name", "")) for r in sc if isinstance(r, dict)}
    for req in REQUIRED_SCORECARD_METRIC_NAMES:
        if req not in present:
            return False
    return True


def build_strong_agent_scorecard_body_operator(
    data: dict[str, Any],
    *,
    optional_bindings: dict[str, str | None],
) -> dict[str, Any]:
    merged = merge_operator_protocol(data)
    complete = _operator_protocol_complete(merged)
    status = BENCHMARK_STATUS_OP_COMPLETE if complete else BENCHMARK_STATUS_OP_INCOMPLETE
    ev_scope = EVIDENCE_SCOPE_OPERATOR_DECLARED if complete else EVIDENCE_SCOPE_NOT_EVALUATED

    el = merged["evaluation_ladder"]
    if not isinstance(el, list):
        raise TypeError("evaluation_ladder must be a list")
    for i, st in enumerate(el):
        if not isinstance(st, dict):
            raise TypeError("evaluation_ladder row must be object")
        for req in ("stage_id", "stage_name", "stage_status"):
            if req not in st:
                raise ValueError(f"evaluation_ladder[{i}] missing {req!r}")
    cs = merged["candidate_subject"]
    if not isinstance(cs, dict):
        raise TypeError("candidate_subject must be object")
    _validate_row(cs, CANDIDATE_SUBJECT_FIELDS, "candidate_subject")
    baselines = merged["baseline_subjects"]
    if not isinstance(baselines, list):
        raise TypeError("baseline_subjects must be a list")
    for i, row in enumerate(baselines):
        if not isinstance(row, dict):
            raise TypeError("baseline row must be object")
        if len(row) > 0:
            _validate_row(row, BASELINE_SUBJECT_FIELDS, f"baseline_subjects[{i}]")
    mp = merged["map_pool"]
    if not isinstance(mp, dict):
        raise TypeError("map_pool must be object")
    _validate_row(mp, MAP_POOL_FIELDS, "map_pool")
    opool = merged["opponent_pool"]
    if not isinstance(opool, dict):
        raise TypeError("opponent_pool must be object")
    _validate_row(opool, OPPONENT_POOL_FIELDS, "opponent_pool")
    for key, fields, label in (
        ("scorecard_fields", SCORECARD_FIELD_DEF_FIELDS, "scorecard_fields"),
        ("gate_thresholds", GATE_THRESHOLD_FIELDS, "gate_thresholds"),
        ("evidence_requirements", EVIDENCE_REQUIREMENT_FIELDS, "evidence_requirements"),
        ("failure_mode_probes", FAILURE_PROBE_FIELDS, "failure_mode_probes"),
        ("xai_requirements", XAI_REQUIREMENT_FIELDS, "xai_requirements"),
    ):
        arr = merged[key]
        if not isinstance(arr, list):
            raise TypeError(f"{key} must be a list")
        for i, row in enumerate(arr):
            if not isinstance(row, dict):
                raise TypeError(f"{key}[{i}] must be object")
            if len(row) > 0:
                _validate_row(row, fields, f"{label}[{i}]")

    if complete:
        score_rows = merged["scorecard_fields"]
        present = {str(r.get("field_name", "")) for r in score_rows if isinstance(r, dict)}
        for req in REQUIRED_SCORECARD_METRIC_NAMES:
            if req not in present:
                raise ValueError(
                    f"complete operator protocol must list all required scorecard field names; "
                    f"missing {req!r}"
                )

    hpanel = merged["human_panel_reserved"]
    if not isinstance(hpanel, dict):
        raise TypeError("human_panel_reserved must be object")
    onotes = merged.get("operator_notes", "")
    onotes_s: str | None = str(onotes) if str(onotes).strip() else None
    ncl = merged.get("non_claims")
    op_extra: list[str] = [str(x) for x in ncl] if isinstance(ncl, list) else []
    non_claims = list(NON_CLAIMS_V15_M05) + op_extra

    return {
        "contract_id": CONTRACT_ID_STRONG_AGENT_SCORECARD,
        "protocol_profile_id": PROTOCOL_PROFILE_ID,
        "milestone_id": MILESTONE_ID_V15_M05,
        "generated_by": EMITTER_MODULE_STRONG_AGENT,
        "profile": str(merged.get("profile") or PROFILE_OPERATOR_DECLARED),
        "benchmark_protocol_status": status,
        "benchmark_execution_performed": False,
        "strong_agent_claim_authorized": False,
        "long_gpu_run_authorized": False,
        "candidate_checkpoint_evaluated": False,
        "human_panel_included": False,
        "live_sc2_included": False,
        "xai_review_performed": False,
        "evidence_scope": ev_scope,
        "benchmark_identity": {
            "benchmark_id": str(merged.get("benchmark_id", "")),
            "benchmark_name": str(merged.get("benchmark_name", "")),
            "protocol_profile_id": PROTOCOL_PROFILE_ID,
        },
        "evaluation_ladder": el,
        "candidate_subject": cs,
        "baseline_subjects": baselines,
        "map_pool": mp,
        "opponent_pool": opool,
        "scorecard_fields": merged["scorecard_fields"],
        "gate_thresholds": merged["gate_thresholds"],
        "evidence_requirements": merged["evidence_requirements"],
        "failure_mode_probes": merged["failure_mode_probes"],
        "xai_requirements": merged["xai_requirements"],
        "reserved_human_panel_section": hpanel,
        "xai_review_reserved": _xai_review_reserved(),
        "optional_bindings": {
            "checkpoint_lineage_json_canonical_sha256": optional_bindings.get("checkpoint_lineage"),
            "xai_evidence_json_canonical_sha256": optional_bindings.get("xai_evidence"),
            "environment_lock_json_canonical_sha256": optional_bindings.get("environment_lock"),
        },
        "status_vocabulary": _vocab_object(),
        "subject_kind_vocabulary": list(STATUS_VOCABULARY["subject_kind"]),
        "metric_vocabulary": _metric_vocab_object(),
        "gate_vocabulary": _gate_vocab_object(),
        "evidence_kind_vocabulary": _evidence_kind_vocab_object(),
        "required_fields": _required_fields_map(),
        "check_results": [
            {
                "check_id": "m05_operator_protocol",
                "description": f"Operator protocol metadata resolved to {status}.",
                "status": CHECK_PASS,
            }
        ],
        "m05_verification_attestation": _attestation(),
        "non_claims": non_claims,
        "carry_forward_items": _carry_forward(),
        **({"operator_notes": onotes_s} if onotes_s is not None else {}),
    }


def build_strong_agent_scorecard_body(
    profile: str,
    *,
    protocol_data: dict[str, Any] | None = None,
    optional_bindings: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    bind = optional_bindings or {
        "checkpoint_lineage": None,
        "xai_evidence": None,
        "environment_lock": None,
    }
    if profile == PROFILE_FIXTURE_CI:
        return build_strong_agent_scorecard_body_fixture()
    if profile == PROFILE_OPERATOR_DECLARED:
        if protocol_data is None:
            raise ValueError("operator_declared profile requires --protocol-json data")
        return build_strong_agent_scorecard_body_operator(protocol_data, optional_bindings=bind)
    raise ValueError(f"unknown profile: {profile!r}")


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_STRONG_AGENT_SCORECARD
    assert body["protocol_profile_id"] == PROTOCOL_PROFILE_ID
    assert body["milestone_id"] == MILESTONE_ID_V15_M05
    assert body["long_gpu_run_authorized"] is False
    assert body["benchmark_execution_performed"] is False
    assert body["strong_agent_claim_authorized"] is False


def seal_strong_agent_scorecard_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, SEAL: digest}


def build_strong_agent_scorecard_report(contract: dict[str, Any]) -> dict[str, Any]:
    digest = contract[SEAL]
    ladder = contract["evaluation_ladder"]
    n_stages = len(ladder) if isinstance(ladder, list) else 0
    n_base = len(contract["baseline_subjects"])
    n_gates = len(contract["gate_thresholds"])
    n_fields = len(contract["scorecard_fields"])
    return {
        "report_version": REPORT_VERSION_STRONG_AGENT,
        "milestone_id": MILESTONE_ID_V15_M05,
        SEAL: digest,
        "contract_id": contract["contract_id"],
        "protocol_profile_id": contract["protocol_profile_id"],
        "profile": contract["profile"],
        "benchmark_protocol_status": contract["benchmark_protocol_status"],
        "stage_count": n_stages,
        "baseline_subject_count": n_base,
        "gate_count": n_gates,
        "scorecard_field_count": n_fields,
        "non_claims_summary": {
            "count": len(contract["non_claims"]),
            "m05_does_not_authorize_benchmark_execution": contract["benchmark_execution_performed"]
            is False,
            "m05_does_not_authorize_strong_agent_claim": contract["strong_agent_claim_authorized"]
            is False,
            "m05_does_not_authorize_long_gpu_run": contract["long_gpu_run_authorized"] is False,
        },
    }


def write_strong_agent_artifacts(
    *, output_dir: Path, contract: dict[str, Any], report: dict[str, Any]
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_STRONG_AGENT_SCORECARD
    r_path = output_dir / REPORT_FILENAME_STRONG_AGENT_SCORECARD
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_v15_strong_agent_scorecard(
    output_dir: Path,
    *,
    profile: str,
    protocol_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    xai_evidence_path: Path | None = None,
    environment_lock_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    optional_sha: dict[str, str | None] = {
        "checkpoint_lineage": None,
        "xai_evidence": None,
        "environment_lock": None,
    }
    if checkpoint_lineage_path is not None:
        optional_sha["checkpoint_lineage"] = _json_file_canonical_sha256(checkpoint_lineage_path)
    if xai_evidence_path is not None:
        optional_sha["xai_evidence"] = _json_file_canonical_sha256(xai_evidence_path)
    if environment_lock_path is not None:
        optional_sha["environment_lock"] = environment_lock_file_canonical_sha256(
            environment_lock_path
        )

    protocol_data: dict[str, Any] | None = None
    if protocol_path is not None:
        protocol_data = parse_protocol_json(protocol_path)

    body = build_strong_agent_scorecard_body(
        profile, protocol_data=protocol_data, optional_bindings=optional_sha
    )
    if profile == PROFILE_OPERATOR_DECLARED and protocol_data is not None:
        body = redact_paths_in_value(body)
    if profile == PROFILE_FIXTURE_CI:
        # fixture ignores optional file bindings
        if any(
            p is not None
            for p in (checkpoint_lineage_path, xai_evidence_path, environment_lock_path)
        ):
            # caller should warn; ensure fixture body keeps null bindings
            pass

    _validate_body_invariants(body)
    sealed = seal_strong_agent_scorecard_body(body)
    rep = build_strong_agent_scorecard_report(sealed)
    c_path, r_path = write_strong_agent_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
