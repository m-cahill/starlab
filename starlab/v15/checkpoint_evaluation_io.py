"""Build, seal, and write V15-M09 checkpoint evaluation + promotion decision artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_models import (
    ALL_GATE_IDS,
    CONTRACT_ID_CHECKPOINT_EVALUATION,
    CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
    CONTRACT_VERSION,
    EMITTER_MODULE_CHECKPOINT_EVALUATION,
    EMITTER_MODULE_PROMOTION_DECISION,
    EVALUATION_DECLARED_TOP_LEVEL_KEYS,
    EVALUATION_STATUS_BLOCKED_NO_CANDIDATE,
    EVALUATION_STATUS_BLOCKED_NO_RECEIPT,
    EVALUATION_STATUS_BLOCKED_PREFLIGHT,
    EVALUATION_STATUS_NOT_EVALUATED_FIXTURE,
    FILENAME_CHECKPOINT_EVALUATION,
    FILENAME_CHECKPOINT_PROMOTION,
    FIXTURE_CANDIDATE_CHECKPOINT_ID,
    FIXTURE_EVALUATION_ID,
    G0_ARTIFACT_INTEGRITY,
    G1_LINEAGE_CONSISTENCY,
    G2_ENVIRONMENT_BINDING,
    G3_DATASET_RIGHTS_BINDING,
    G4_CHECKPOINT_HASH_VERIFICATION,
    G5_LOAD_SMOKE,
    G6_RESUME_CONTINUATION,
    G7_EVAL_CADENCE,
    G8_BASIC_METRIC_THRESHOLDS,
    G9_FAILURE_PROBE,
    G10_NON_CLAIM_BOUNDARY,
    GATE_STATUS_BLOCKED,
    GATE_STATUS_FAIL,
    GATE_STATUS_NOT_APPLICABLE,
    GATE_STATUS_NOT_EVALUATED,
    GATE_STATUS_PASS,
    GATE_STATUS_WARNING,
    MILESTONE_ID_V15_M09,
    NON_CLAIMS_V15_M09,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION,
    PROMOTION_STATUS_BLOCKED,
    PROMOTION_STATUS_BLOCKED_CAMPAIGN,
    PROMOTION_STATUS_BLOCKED_CANDIDATE,
    PROMOTION_STATUS_NOT_PROMOTED,
    REPORT_FILENAME_CHECKPOINT_EVALUATION,
    REPORT_FILENAME_CHECKPOINT_PROMOTION,
    REPORT_VERSION_EVALUATION,
    REPORT_VERSION_PROMOTION,
    SEAL_KEY_CHECKPOINT_EVALUATION,
    SEAL_KEY_CHECKPOINT_PROMOTION,
    default_m09_evaluation_authorization_flags,
)
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.environment_lock_models import STATUS_FIXTURE_ONLY, STATUS_OPERATOR_LOCAL_READY
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
)
from starlab.v15.training_run_receipt_io import _redaction_token_count, redact_receipt_value

_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def redact_checkpoint_evaluation_value(obj: Any) -> Any:
    p = redact_paths_in_value(obj)
    return redact_receipt_value(p)


def m08_campaign_receipt_valid_for_m09(receipt: dict[str, Any]) -> bool:
    if str(receipt.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT:
        return False
    if str(receipt.get("campaign_completion_status", "")) == "not_executed":
        return False
    af = receipt.get("authorization_flags")
    if isinstance(af, dict) and af.get("long_gpu_campaign_completed") is True:
        return True
    st = str(receipt.get("campaign_completion_status", ""))
    if st in ("completed", "operator_local_completed"):
        return True
    return False


def _gate_row(gate_id: str, status: str, notes: str) -> dict[str, Any]:
    return {"gate_id": gate_id, "status": status, "notes": notes}


def _all_gates(status: str, note: str) -> list[dict[str, Any]]:
    return [_gate_row(g, status, note) for g in ALL_GATE_IDS]


def seal_checkpoint_evaluation_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_KEY_CHECKPOINT_EVALUATION}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_KEY_CHECKPOINT_EVALUATION] = digest
    return sealed


def build_checkpoint_evaluation_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_CHECKPOINT_EVALUATION}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_checkpoint_evaluation_report",
        "report_version": REPORT_VERSION_EVALUATION,
        "milestone": MILESTONE_ID_V15_M09,
        "artifact_sha256": digest,
        "seal_field": SEAL_KEY_CHECKPOINT_EVALUATION,
        "seal_value_matches_artifact": sealed.get(SEAL_KEY_CHECKPOINT_EVALUATION) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_CHECKPOINT_EVALUATION,
    }


def build_checkpoint_evaluation_body_fixture() -> dict[str, Any]:
    auth = default_m09_evaluation_authorization_flags()
    gates = _all_gates(
        GATE_STATUS_NOT_EVALUATED,
        "fixture_ci: no real M08 campaign receipt or candidate checkpoint evidence.",
    )
    return {
        "contract_id": CONTRACT_ID_CHECKPOINT_EVALUATION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_ID_V15_M09,
        "created_by": EMITTER_MODULE_CHECKPOINT_EVALUATION,
        "evaluation_id": FIXTURE_EVALUATION_ID,
        "candidate_checkpoint_id": FIXTURE_CANDIDATE_CHECKPOINT_ID,
        "candidate_checkpoint_role": "non_candidate_placeholder",
        "evaluation_status": EVALUATION_STATUS_NOT_EVALUATED_FIXTURE,
        "evidence_scope": "fixture_ci_only",
        "m08_training_manifest_binding": {
            "m08_training_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m08_campaign_receipt_binding": {
            "m08_campaign_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "checkpoint_lineage_binding": {
            "checkpoint_lineage_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "checkpoint_metadata_binding": {
            "candidate_metadata_json_canonical_sha256": PLACEHOLDER_SHA256,
            "checkpoint_sha256_declared": PLACEHOLDER_SHA256,
        },
        "environment_lock_binding": {
            "environment_lock_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "training_config_binding": {
            "training_config_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "dataset_manifest_binding": {
            "dataset_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "rights_manifest_binding": {
            "rights_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "strong_agent_protocol_binding": {
            "strong_agent_scorecard_json_canonical_sha256": None,
        },
        "xai_contract_binding": {
            "xai_evidence_pack_json_canonical_sha256": None,
        },
        "human_panel_protocol_binding": {
            "human_panel_benchmark_json_canonical_sha256": None,
        },
        "artifact_integrity": {
            "status": "fixture",
            "notes": "Deterministic fixture; no real inputs.",
        },
        "lineage_consistency": {
            "status": "not_evaluated",
            "notes": "No lineage cross-check in fixture.",
        },
        "checkpoint_hash_verification": {
            "status": "not_evaluated",
            "notes": "M09 does not read checkpoint blobs in fixture_ci.",
        },
        "load_smoke": {
            "status": "not_executed",
            "notes": "No checkpoint load in fixture_ci.",
        },
        "resume_or_continuation_receipt": {
            "status": "not_evaluated",
            "notes": "No resume proof in fixture.",
        },
        "evaluation_metrics": {"posture": "no_metrics_fixture_only"},
        "evaluation_gates": gates,
        "failure_probes": {"posture": "not_executed_in_fixture"},
        "provenance_gaps": [
            "V15-M08 public record: no completed long GPU campaign (no M08 campaign receipt).",
            "No candidate checkpoint available for evaluation on fixture path.",
        ],
        "non_claims": list(NON_CLAIMS_V15_M09),
        "authorization_flags": auth,
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator_declared": "redact_absolute_paths_and_contacts",
        },
        "optional_bindings": {},
    }


def parse_declared_checkpoint_evaluation(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("evaluation JSON must be a single object")
    unknown = set(raw.keys()) - EVALUATION_DECLARED_TOP_LEVEL_KEYS
    if unknown:
        raise ValueError(f"unknown top-level keys in declared evaluation: {sorted(unknown)}")
    return raw


def compute_gates_for_preflight(
    *,
    m08_training_manifest: dict[str, Any],
    m08_campaign_receipt: dict[str, Any],
    checkpoint_lineage: dict[str, Any],
    candidate_metadata: dict[str, Any],
    environment_lock: dict[str, Any],
) -> tuple[list[dict[str, Any]], str, list[str], bool]:
    """Returns (gate rows, eval_status, provenance_gaps, receipt_valid)."""

    gaps: list[str] = []
    receipt_valid = m08_campaign_receipt_valid_for_m09(m08_campaign_receipt)
    if not receipt_valid:
        gaps.append("M08 campaign receipt does not record a completed long GPU campaign.")
        base_status = EVALUATION_STATUS_BLOCKED_NO_RECEIPT
    else:
        base_status = EVALUATION_STATUS_BLOCKED_PREFLIGHT

    m_ok = (
        str(m08_training_manifest.get("contract_id", "")) == CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST
    )
    r_ok = str(m08_campaign_receipt.get("contract_id", "")) == CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
    g0 = GATE_STATUS_PASS if m_ok and r_ok else GATE_STATUS_FAIL

    cand_id = str(candidate_metadata.get("candidate_checkpoint_id", ""))
    sha = str(candidate_metadata.get("checkpoint_sha256", ""))
    lineage_rows = checkpoint_lineage.get("checkpoint_lineage")
    g1 = GATE_STATUS_NOT_EVALUATED
    if isinstance(lineage_rows, list) and cand_id and lineage_rows:
        for row in lineage_rows:
            if isinstance(row, dict) and str(row.get("checkpoint_id", "")) == cand_id:
                g1 = GATE_STATUS_PASS
                break
        if g1 != GATE_STATUS_PASS:
            g1 = GATE_STATUS_FAIL
    elif not cand_id:
        g1 = GATE_STATUS_FAIL

    lock_st = str(environment_lock.get("environment_lock_status", ""))
    if lock_st == STATUS_OPERATOR_LOCAL_READY:
        g2: str = GATE_STATUS_PASS
    elif lock_st == STATUS_FIXTURE_ONLY:
        g2 = GATE_STATUS_WARNING
    else:
        g2 = GATE_STATUS_WARNING

    g3 = GATE_STATUS_PASS
    g4 = (
        GATE_STATUS_PASS if _HEX64.match(sha) and sha != PLACEHOLDER_SHA256 else GATE_STATUS_BLOCKED
    )
    if not _HEX64.match(sha) or sha == PLACEHOLDER_SHA256:
        gaps.append("Candidate checkpoint metadata must declare a non-placeholder SHA-256.")

    g5 = GATE_STATUS_NOT_EVALUATED
    g6 = GATE_STATUS_NOT_EVALUATED
    g7 = GATE_STATUS_NOT_EVALUATED
    g8 = GATE_STATUS_NOT_EVALUATED
    g9 = GATE_STATUS_NOT_APPLICABLE
    g10 = GATE_STATUS_PASS

    gates = [
        _gate_row(
            G0_ARTIFACT_INTEGRITY,
            g0,
            "M08 manifest and campaign receipt contract_ids.",
        ),
        _gate_row(
            G1_LINEAGE_CONSISTENCY, g1, "Candidate id present in checkpoint lineage when possible."
        ),
        _gate_row(G2_ENVIRONMENT_BINDING, g2, f"environment_lock_status={lock_st!r}."),
        _gate_row(
            G3_DATASET_RIGHTS_BINDING,
            g3,
            "Preflight: SHA bindings present for dataset/rights JSON.",
        ),
        _gate_row(
            G4_CHECKPOINT_HASH_VERIFICATION,
            g4,
            "Metadata checkpoint_sha256 (non-placeholder); no blob read in preflight.",
        ),
        _gate_row(
            G5_LOAD_SMOKE,
            g5,
            "Preflight / dry-run: load_smoke not executed (no checkpoint blob I/O).",
        ),
        _gate_row(
            G6_RESUME_CONTINUATION,
            g6,
            "Resume/continuation not evaluated in preflight-only surface.",
        ),
        _gate_row(
            G7_EVAL_CADENCE,
            g7,
            "Eval cadence not evaluated in preflight-only surface.",
        ),
        _gate_row(
            G8_BASIC_METRIC_THRESHOLDS,
            g8,
            "Metric thresholds not evaluated in preflight-only surface.",
        ),
        _gate_row(G9_FAILURE_PROBE, g9, "Not applicable in preflight binding pass."),
        _gate_row(
            G10_NON_CLAIM_BOUNDARY,
            g10,
            "M09 non-claim posture preserved; no strong-agent claim.",
        ),
    ]
    if not cand_id or not _HEX64.match(sha):
        if base_status != EVALUATION_STATUS_BLOCKED_NO_RECEIPT:
            base_status = EVALUATION_STATUS_BLOCKED_NO_CANDIDATE
        gaps.append("Missing candidate_checkpoint_id or valid checkpoint_sha256 in metadata.")
    return gates, base_status, gaps, receipt_valid


def promotion_blocked_by_gates(evaluation_gates: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """Returns (blocked, blockers) using frozen promotion requirements."""

    gmap = {str(x.get("gate_id", "")): str(x.get("status", "")) for x in evaluation_gates}
    blockers: list[str] = []

    def req(gid: str, allowed: frozenset[str]) -> None:
        st = gmap.get(gid, GATE_STATUS_NOT_EVALUATED)
        if st not in allowed:
            blockers.append(f"{gid}={st} (required one of {sorted(allowed)})")

    req(G0_ARTIFACT_INTEGRITY, frozenset({GATE_STATUS_PASS}))
    req(G1_LINEAGE_CONSISTENCY, frozenset({GATE_STATUS_PASS}))
    req(G2_ENVIRONMENT_BINDING, frozenset({GATE_STATUS_PASS, GATE_STATUS_WARNING}))
    req(G3_DATASET_RIGHTS_BINDING, frozenset({GATE_STATUS_PASS}))
    req(G4_CHECKPOINT_HASH_VERIFICATION, frozenset({GATE_STATUS_PASS}))
    req(G5_LOAD_SMOKE, frozenset({GATE_STATUS_PASS}))
    req(G8_BASIC_METRIC_THRESHOLDS, frozenset({GATE_STATUS_PASS, GATE_STATUS_WARNING}))
    req(G10_NON_CLAIM_BOUNDARY, frozenset({GATE_STATUS_PASS}))
    return (bool(blockers), blockers, gmap)


def seal_checkpoint_promotion_decision_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_KEY_CHECKPOINT_PROMOTION}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_KEY_CHECKPOINT_PROMOTION] = digest
    return sealed


def build_checkpoint_promotion_decision_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_CHECKPOINT_PROMOTION}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_checkpoint_promotion_decision_report",
        "report_version": REPORT_VERSION_PROMOTION,
        "milestone": MILESTONE_ID_V15_M09,
        "artifact_sha256": digest,
        "seal_field": SEAL_KEY_CHECKPOINT_PROMOTION,
        "seal_value_matches_artifact": sealed.get(SEAL_KEY_CHECKPOINT_PROMOTION) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_CHECKPOINT_PROMOTION,
    }


def build_promotion_decision_from_evaluation(sealed_eval: dict[str, Any]) -> dict[str, Any]:
    """Map evaluation to promotion: M09 does not authorize real promotion on default paths."""
    eid = str(sealed_eval.get("evaluation_id", ""))
    cid = str(sealed_eval.get("candidate_checkpoint_id", ""))
    gates_in = sealed_eval.get("evaluation_gates")
    gates: list[dict[str, Any]] = gates_in if isinstance(gates_in, list) else []
    _blocked, gate_blockers, gmap = promotion_blocked_by_gates(gates)
    profile = str(sealed_eval.get("profile", ""))
    st_ev = str(sealed_eval.get("evaluation_status", ""))
    eval_af = sealed_eval.get("authorization_flags")
    if not isinstance(eval_af, dict):
        eval_af = default_m09_evaluation_authorization_flags()

    blockers = list(gate_blockers)
    pstat: str
    if profile == PROFILE_FIXTURE_CI or st_ev == EVALUATION_STATUS_NOT_EVALUATED_FIXTURE:
        pstat = PROMOTION_STATUS_BLOCKED
        blockers.append("fixture_ci does not produce promotable evidence")
    elif st_ev == EVALUATION_STATUS_BLOCKED_NO_RECEIPT:
        pstat = PROMOTION_STATUS_BLOCKED_CAMPAIGN
    elif st_ev == EVALUATION_STATUS_BLOCKED_NO_CANDIDATE:
        pstat = PROMOTION_STATUS_BLOCKED_CANDIDATE
    else:
        pstat = PROMOTION_STATUS_NOT_PROMOTED
    if profile in ("operator_declared", "operator_preflight", "operator_local_evaluation"):
        blockers.append(
            "no verified execution on M09 surface; operator_declared is normalization only"
        )
    pauth2 = {
        "checkpoint_candidate_available": bool(eval_af.get("checkpoint_candidate_available")),
        "checkpoint_bytes_verified": bool(eval_af.get("checkpoint_bytes_verified")),
        "checkpoint_evaluation_performed": bool(eval_af.get("checkpoint_evaluation_performed")),
        "checkpoint_promotion_performed": False,
        "promoted_checkpoint_selected": False,
        "benchmark_execution_performed": bool(eval_af.get("benchmark_execution_performed")),
        "strong_agent_claim_authorized": False,
        "human_panel_execution_performed": bool(eval_af.get("human_panel_execution_performed")),
        "human_benchmark_claim_authorized": False,
        "xai_review_performed": bool(eval_af.get("xai_review_performed")),
        "long_gpu_campaign_completed": bool(eval_af.get("long_gpu_campaign_completed")),
        "v2_authorized": bool(eval_af.get("v2_authorized")),
    }
    ncs = list(NON_CLAIMS_V15_M09) + [
        "Promotion is not a strong-agent, human, or v2 claim.",
    ]
    return {
        "contract_id": CONTRACT_ID_CHECKPOINT_PROMOTION_DECISION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION,
        "milestone": MILESTONE_ID_V15_M09,
        "created_by": EMITTER_MODULE_PROMOTION_DECISION,
        "promotion_decision_id": f"{eid}:promotion_decision",
        "evaluation_id": eid,
        "candidate_checkpoint_id": cid,
        "promotion_status": pstat,
        "promotion_scope": "v15_downstream_milestones_m10_m12",
        "promotion_reason": "M09 gate and evidence posture; this repository surface never promotes",
        "promotion_blockers": list(dict.fromkeys(b for b in blockers if b)),
        "required_gates": list(ALL_GATE_IDS),
        "gate_summary": gmap,
        "promoted_for": [],
        "not_promoted_for": [
            "strong_agent_claim",
            "human_benchmark_claim",
            "xai_faithfulness_proof",
            "v2_opening",
        ],
        "downstream_allowed_uses": {
            "when_not_promoted": [
                "document blocked posture honestly",
            ],
        },
        "downstream_disallowed_uses": {
            "by_default": [
                "strong_agent_pass_claim",
                "public_human_panel_majority_without_protocol_evidence",
            ],
        },
        "checkpoint_register_recommendation": "no_public_row_add_without_evidence_and_review",
        "model_weight_register_recommendation": "no_public_row_add_without_evidence_and_review",
        "rights_review_status": "not_evaluated_in_default_paths",
        "operator_notes": "",
        "non_claims": ncs,
        "authorization_flags": pauth2,
        "redaction_policy": {"operator": "redact_absolute_paths_and_contacts"},
        "optional_bindings": {},
    }


def _preflight_body(
    *,
    evaluation_id: str,
    prof: str,
    m08_manifest_path: Path,
    m08_receipt_path: Path,
    checkpoint_lineage_path: Path,
    candidate_metadata_path: Path,
    environment_lock_path: Path,
    training_config_path: Path,
    dataset_manifest_path: Path,
    rights_manifest_path: Path,
    strong_agent_path: Path | None,
    xai_path: Path | None,
    human_panel_path: Path | None,
) -> dict[str, Any]:
    m08_training_manifest = json.loads(m08_manifest_path.read_text(encoding="utf-8"))
    m08_receipt = json.loads(m08_receipt_path.read_text(encoding="utf-8"))
    checkpoint_lineage = json.loads(checkpoint_lineage_path.read_text(encoding="utf-8"))
    candidate_metadata = json.loads(candidate_metadata_path.read_text(encoding="utf-8"))
    environment_lock = json.loads(environment_lock_path.read_text(encoding="utf-8"))

    g_rows, st_ev, gaps, _rv = compute_gates_for_preflight(
        m08_training_manifest=m08_training_manifest,
        m08_campaign_receipt=m08_receipt,
        checkpoint_lineage=checkpoint_lineage,
        candidate_metadata=candidate_metadata,
        environment_lock=environment_lock,
    )
    c_sha = str(candidate_metadata.get("checkpoint_sha256", ""))
    cp_meta_sha = _json_file_canonical_sha256(candidate_metadata_path)
    bind_receipt: dict[str, Any] = {
        "m08_campaign_receipt_json_canonical_sha256": _json_file_canonical_sha256(m08_receipt_path),
        "binding_status": "preflight_bind",
        "campaign_completion_status_observed": m08_receipt.get("campaign_completion_status"),
    }
    opt_sasc = _json_file_canonical_sha256(strong_agent_path) if strong_agent_path else None
    opt_xai = _json_file_canonical_sha256(xai_path) if xai_path else None
    opt_h = _json_file_canonical_sha256(human_panel_path) if human_panel_path else None

    auth = default_m09_evaluation_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_CHECKPOINT_EVALUATION,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_CHECKPOINT_EVALUATION_PROMOTION,
        "profile": prof,
        "milestone": MILESTONE_ID_V15_M09,
        "created_by": EMITTER_MODULE_CHECKPOINT_EVALUATION,
        "evaluation_id": evaluation_id,
        "candidate_checkpoint_id": str(candidate_metadata.get("candidate_checkpoint_id", "")),
        "candidate_checkpoint_role": str(
            candidate_metadata.get("candidate_checkpoint_role", "current_candidate")
        ),
        "evaluation_status": st_ev,
        "evidence_scope": "operator_preflight_bindings_only"
        if "preflight" in prof
        else "operator_local_dry_run",
        "m08_training_manifest_binding": {
            "m08_training_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                m08_manifest_path
            ),
            "contract_id": m08_training_manifest.get("contract_id"),
        },
        "m08_campaign_receipt_binding": bind_receipt,
        "checkpoint_lineage_binding": {
            "checkpoint_lineage_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                checkpoint_lineage_path
            ),
        },
        "checkpoint_metadata_binding": {
            "candidate_metadata_json_canonical_sha256": cp_meta_sha,
            "checkpoint_sha256_declared": c_sha,
        },
        "environment_lock_binding": {
            "environment_lock_json_canonical_sha256": environment_lock_file_canonical_sha256(
                environment_lock_path
            ),
        },
        "training_config_binding": {
            "training_config_json_canonical_sha256": _json_file_canonical_sha256(
                training_config_path
            ),
        },
        "dataset_manifest_binding": {
            "dataset_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                dataset_manifest_path
            ),
        },
        "rights_manifest_binding": {
            "rights_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                rights_manifest_path
            ),
        },
        "strong_agent_protocol_binding": {
            "strong_agent_scorecard_json_canonical_sha256": opt_sasc,
        },
        "xai_contract_binding": {
            "xai_evidence_pack_json_canonical_sha256": opt_xai,
        },
        "human_panel_protocol_binding": {
            "human_panel_benchmark_json_canonical_sha256": opt_h,
        },
        "artifact_integrity": {
            "status": "bound",
            "notes": "Canonical SHA-256 bindings for declared JSON only.",
        },
        "lineage_consistency": {"status": "see_gates", "notes": "G1 in evaluation_gates."},
        "checkpoint_hash_verification": {
            "status": "metadata_only",
            "notes": "No blob I/O; see G4.",
        },
        "load_smoke": {
            "status": "not_executed",
            "notes": "M09 dry-run / preflight does not load blobs.",
        },
        "resume_or_continuation_receipt": {
            "status": "not_evaluated",
            "notes": "M09 preflight surface.",
        },
        "evaluation_metrics": {"posture": "no_expensive_eval"},
        "evaluation_gates": g_rows,
        "failure_probes": {"posture": "not_run"},
        "provenance_gaps": gaps,
        "non_claims": list(NON_CLAIMS_V15_M09),
        "authorization_flags": auth,
        "redaction_policy": {
            "operator_preflight": "redact_paths_contacts_secrets",
        },
        "optional_bindings": {},
    }


def emit_v15_checkpoint_evaluation_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_checkpoint_evaluation_body_fixture()
    sealed = seal_checkpoint_evaluation_body(body)
    rep = build_checkpoint_evaluation_report(sealed, redaction_count=0)
    c_path = output_dir / FILENAME_CHECKPOINT_EVALUATION
    r_path = output_dir / REPORT_FILENAME_CHECKPOINT_EVALUATION
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path


def emit_v15_checkpoint_evaluation_operator_preflight(
    output_dir: Path,
    *,
    m08_training_manifest: Path,
    m08_campaign_receipt: Path,
    checkpoint_lineage: Path,
    candidate_checkpoint_metadata: Path,
    environment_lock: Path,
    training_config: Path,
    dataset_manifest: Path,
    rights_manifest: Path,
    strong_agent_scorecard: Path | None,
    xai_evidence: Path | None,
    human_panel_benchmark: Path | None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    body = _preflight_body(
        evaluation_id="v15_m09:operator_preflight:local",
        prof="operator_preflight",
        m08_manifest_path=m08_training_manifest,
        m08_receipt_path=m08_campaign_receipt,
        checkpoint_lineage_path=checkpoint_lineage,
        candidate_metadata_path=candidate_checkpoint_metadata,
        environment_lock_path=environment_lock,
        training_config_path=training_config,
        dataset_manifest_path=dataset_manifest,
        rights_manifest_path=rights_manifest,
        strong_agent_path=strong_agent_scorecard,
        xai_path=xai_evidence,
        human_panel_path=human_panel_benchmark,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    sealed = seal_checkpoint_evaluation_body(body)
    rep = build_checkpoint_evaluation_report(sealed, redaction_count=0)
    c_path = output_dir / FILENAME_CHECKPOINT_EVALUATION
    r_path = output_dir / REPORT_FILENAME_CHECKPOINT_EVALUATION
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path


def emit_v15_checkpoint_evaluation_operator_local_evaluation(
    output_dir: Path,
    *,
    m08_training_manifest: Path,
    m08_campaign_receipt: Path,
    checkpoint_lineage: Path,
    candidate_checkpoint_metadata: Path,
    environment_lock: Path,
    training_config: Path,
    dataset_manifest: Path,
    rights_manifest: Path,
    strong_agent_scorecard: Path | None,
    xai_evidence: Path | None,
    human_panel_benchmark: Path | None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    body = _preflight_body(
        evaluation_id="v15_m09:operator_local_evaluation:dry_run",
        prof="operator_local_evaluation",
        m08_manifest_path=m08_training_manifest,
        m08_receipt_path=m08_campaign_receipt,
        checkpoint_lineage_path=checkpoint_lineage,
        candidate_metadata_path=candidate_checkpoint_metadata,
        environment_lock_path=environment_lock,
        training_config_path=training_config,
        dataset_manifest_path=dataset_manifest,
        rights_manifest_path=rights_manifest,
        strong_agent_path=strong_agent_scorecard,
        xai_path=xai_evidence,
        human_panel_path=human_panel_benchmark,
    )
    body["provenance_gaps"] = list(body.get("provenance_gaps", [])) + [
        "operator_local_evaluation: dry-run only; no checkpoint load without future authorization.",
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    sealed = seal_checkpoint_evaluation_body(body)
    rep = build_checkpoint_evaluation_report(sealed, redaction_count=0)
    c_path = output_dir / FILENAME_CHECKPOINT_EVALUATION
    r_path = output_dir / REPORT_FILENAME_CHECKPOINT_EVALUATION
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path


def emit_v15_checkpoint_evaluation_operator_declared(
    output_dir: Path, evaluation_json: Path
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, int]:
    raw = parse_declared_checkpoint_evaluation(evaluation_json)
    raw.pop(SEAL_KEY_CHECKPOINT_EVALUATION, None)
    red = redact_checkpoint_evaluation_value(raw)
    if not isinstance(red, dict):
        raise ValueError("redacted value must be object")
    rc = _redaction_token_count(red)
    out_dir = output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    sealed = seal_checkpoint_evaluation_body(red)
    rep = build_checkpoint_evaluation_report(sealed, redaction_count=rc)
    c_path = out_dir / FILENAME_CHECKPOINT_EVALUATION
    r_path = out_dir / REPORT_FILENAME_CHECKPOINT_EVALUATION
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path, rc


def emit_v15_checkpoint_promotion_decision(
    output_dir: Path,
    evaluation_json: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, int]:
    ev = json.loads(evaluation_json.read_text(encoding="utf-8"))
    if not isinstance(ev, dict):
        raise ValueError("evaluation must be a JSON object")
    body = build_promotion_decision_from_evaluation(ev)
    body.pop(SEAL_KEY_CHECKPOINT_PROMOTION, None)
    out_dir = output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    red = redact_checkpoint_promotion_value(body)
    out_body = red if isinstance(red, dict) else body
    rcount = _redaction_token_count(out_body) if isinstance(out_body, dict) else 0
    sealed = seal_checkpoint_promotion_decision_body(out_body)
    rep = build_checkpoint_promotion_decision_report(sealed, redaction_count=rcount)
    c_path = out_dir / FILENAME_CHECKPOINT_PROMOTION
    r_path = out_dir / REPORT_FILENAME_CHECKPOINT_PROMOTION
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path, rcount


def redact_checkpoint_promotion_value(obj: Any) -> Any:
    return redact_receipt_value(redact_paths_in_value(obj))
