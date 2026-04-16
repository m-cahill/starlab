"""Build PV1-M01 tranche checkpoint receipts and campaign observability index artifacts."""

from __future__ import annotations

from typing import Any

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.training.pv1_campaign_observability_models import (
    ALL_EVIDENCE_STATUSES_V1,
    CAMPAIGN_OBSERVABILITY_INDEX_FILENAME,
    CAMPAIGN_OBSERVABILITY_INDEX_REPORT_VERSION,
    CAMPAIGN_OBSERVABILITY_INDEX_VERSION,
    EVIDENCE_STATUS_COMPLETE,
    EVIDENCE_STATUS_INCOMPLETE,
    EVIDENCE_STATUS_MISSING_REQUIRED_EVIDENCE,
    EVIDENCE_STATUS_PAUSED,
    PV1_OBSERVABILITY_NON_CLAIMS_V1,
    TRANCHE_CHECKPOINT_RECEIPT_REPORT_VERSION,
    TRANCHE_CHECKPOINT_RECEIPT_VERSION,
)
from starlab.training.pv1_campaign_observability_scan import (
    CampaignObservabilityScan,
    scan_campaign_observability_tree,
    scan_to_jsonable,
)

# Required evidence checks: id -> human-stable required label (for missing refs).
_REQUIRED_DEFS: tuple[tuple[str, str], ...] = (
    ("campaign_contract", "full_local_training_campaign_contract.json (at campaign root)"),
    ("preflight_receipt", "campaign_preflight_receipt.json (at campaign root)"),
    ("hidden_rollout_run", "campaign_runs/<execution_id>/hidden_rollout_campaign_run.json"),
    ("phase_receipt", "at least one **/phase_receipt.json under campaign root"),
    ("replay_binding", "at least one **/replay_binding.json under campaign root"),
    (
        "watchable_validation",
        "at least one **/local_live_play_validation_run.json under campaign root",
    ),
)


def _eval_required(scan: CampaignObservabilityScan) -> tuple[list[str], list[str]]:
    """Return (satisfied requirement ids, missing requirement labels)."""

    satisfied: list[str] = []
    missing: list[str] = []

    if scan.campaign_contract_rel:
        satisfied.append("campaign_contract")
    else:
        missing.append(_required_label("campaign_contract"))

    if scan.preflight_receipt_rel:
        satisfied.append("preflight_receipt")
    else:
        missing.append(_required_label("preflight_receipt"))

    if scan.hidden_rollout_run_rels:
        satisfied.append("hidden_rollout_run")
    else:
        missing.append(_required_label("hidden_rollout_run"))

    if scan.phase_receipt_rels:
        satisfied.append("phase_receipt")
    else:
        missing.append(_required_label("phase_receipt"))

    if scan.replay_binding_rels:
        satisfied.append("replay_binding")
    else:
        missing.append(_required_label("replay_binding"))

    if scan.watchable_validation_rels:
        satisfied.append("watchable_validation")
    else:
        missing.append(_required_label("watchable_validation"))

    return sorted(satisfied), sorted(missing)


def _required_label(req_id: str) -> str:
    for rid, label in _REQUIRED_DEFS:
        if rid == req_id:
            return f"missing:{label}"
    return f"missing:{req_id}"


def _required_id_list() -> list[str]:
    return [rid for rid, _ in _REQUIRED_DEFS]


def _index_status_from_missing(missing: list[str]) -> str:
    if missing:
        return EVIDENCE_STATUS_MISSING_REQUIRED_EVIDENCE
    return EVIDENCE_STATUS_COMPLETE


def build_campaign_observability_index(
    *,
    campaign_root: Any,
    campaign_id_override: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (index.json body, index_report.json body)."""

    scan = scan_campaign_observability_tree(campaign_root)
    oid = campaign_id_override or scan.campaign_id
    satisfied, missing = _eval_required(scan)
    idx_status = _index_status_from_missing(missing)

    body_wo = {
        "artifact_kind": "pv1_campaign_observability_index",
        "campaign_id": oid,
        "campaign_observability_index_version": CAMPAIGN_OBSERVABILITY_INDEX_VERSION,
        "campaign_root": scan.campaign_root_resolved,
        "checkpoint_receipt_refs": list(scan.checkpoint_receipt_rels),
        "evidence_status_vocabulary": list(ALL_EVIDENCE_STATUSES_V1),
        "execution_refs": list(scan.execution_ids),
        "index_scan": scan_to_jsonable(scan),
        "index_status": idx_status,
        "missing_required_evidence": list(missing),
        "non_claims": list(PV1_OBSERVABILITY_NON_CLAIMS_V1),
        "phase_receipt_refs": list(scan.phase_receipt_rels),
        "product_filenames": {
            "campaign_observability_index": CAMPAIGN_OBSERVABILITY_INDEX_FILENAME,
        },
        "replay_binding_refs": list(scan.replay_binding_rels),
        "required_evidence_classes": _required_id_list(),
        "satisfied_evidence_classes": satisfied,
        "watchable_validation_refs": list(scan.watchable_validation_rels),
    }
    digest = sha256_hex_of_canonical_json(body_wo)
    index_body = {**body_wo, "index_sha256": digest}

    report = {
        "artifact_kind": "pv1_campaign_observability_index_report",
        "campaign_id": oid,
        "index_sha256": digest,
        "index_status": idx_status,
        "missing_required_evidence": list(missing),
        "non_claims": list(PV1_OBSERVABILITY_NON_CLAIMS_V1),
        "report_version": CAMPAIGN_OBSERVABILITY_INDEX_REPORT_VERSION,
        "summary": {
            "checkpoint_receipt_count": len(scan.checkpoint_receipt_rels),
            "execution_count": len(scan.execution_ids),
            "phase_receipt_count": len(scan.phase_receipt_rels),
            "replay_binding_count": len(scan.replay_binding_rels),
            "watchable_validation_count": len(scan.watchable_validation_rels),
        },
    }
    return index_body, report


def build_tranche_checkpoint_receipt(
    *,
    campaign_root: Any,
    tranche_id: str,
    checkpoint_id: str,
    operator_paused: bool,
    operator_incomplete: bool,
    operator_note: str | None,
    operator_note_ref: str | None,
    campaign_id_override: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (receipt.json, receipt_report.json) for a named tranche checkpoint boundary."""

    scan = scan_campaign_observability_tree(campaign_root)
    oid = campaign_id_override or scan.campaign_id
    _, missing = _eval_required(scan)

    if missing:
        cp_status = EVIDENCE_STATUS_MISSING_REQUIRED_EVIDENCE
    elif operator_paused:
        cp_status = EVIDENCE_STATUS_PAUSED
    elif operator_incomplete:
        cp_status = EVIDENCE_STATUS_INCOMPLETE
    else:
        cp_status = EVIDENCE_STATUS_COMPLETE

    required_labels = [label for _rid, label in _REQUIRED_DEFS]

    body_wo: dict[str, Any] = {
        "artifact_kind": "tranche_checkpoint_receipt",
        "campaign_id": oid,
        "checkpoint_evidence_status": cp_status,
        "checkpoint_id": checkpoint_id,
        "evidence_status_vocabulary": list(ALL_EVIDENCE_STATUSES_V1),
        "execution_refs": list(scan.execution_ids),
        "missing_evidence_refs": list(missing),
        "non_claims": list(PV1_OBSERVABILITY_NON_CLAIMS_V1),
        "operator_note": operator_note,
        "operator_note_ref": operator_note_ref,
        "phase_receipt_refs": list(scan.phase_receipt_rels),
        "required_evidence_refs": required_labels,
        "scan": scan_to_jsonable(scan),
        "tranche_checkpoint_receipt_version": TRANCHE_CHECKPOINT_RECEIPT_VERSION,
        "tranche_id": tranche_id,
        "watchable_validation_refs": list(scan.watchable_validation_rels),
    }
    digest = sha256_hex_of_canonical_json(body_wo)
    receipt_body = {**body_wo, "receipt_sha256": digest}

    report = {
        "artifact_kind": "tranche_checkpoint_receipt_report",
        "campaign_id": oid,
        "checkpoint_evidence_status": cp_status,
        "checkpoint_id": checkpoint_id,
        "missing_evidence_refs": list(missing),
        "non_claims": list(PV1_OBSERVABILITY_NON_CLAIMS_V1),
        "receipt_sha256": digest,
        "report_version": TRANCHE_CHECKPOINT_RECEIPT_REPORT_VERSION,
        "summary": {
            "execution_ids": list(scan.execution_ids),
            "tranche_id": tranche_id,
        },
        "tranche_id": tranche_id,
    }
    return receipt_body, report
