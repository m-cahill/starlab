"""Build, classify, seal, and emit V15-M18 checkpoint evaluation readiness artifacts."""

# ruff: noqa: E501

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import m08_campaign_receipt_valid_for_m09
from starlab.v15.checkpoint_evaluation_readiness_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
    CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS,
    EMITTER_MODULE_CHECKPOINT_EVALUATION_READINESS,
    FILENAME_CHECKPOINT_EVALUATION_READINESS,
    MILESTONE_ID_V15_M18,
    NON_CLAIMS_V15_M18,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_DEFAULT,
    REFUSAL_CHECKPOINT_COUNT_ZERO,
    REFUSAL_HASH_MISMATCH,
    REFUSAL_INVALID_SHA,
    REFUSAL_JOBLIB_ONLY,
    REFUSAL_MISSING_GOVERNED_RECEIPT,
    REFUSAL_MISSING_LINEAGE,
    REFUSAL_MISSING_MANIFEST_FIELDS,
    REFUSAL_NO_MANIFEST,
    REFUSAL_NOT_EXECUTED,
    REFUSAL_WATCHABILITY_ONLY,
    REPORT_FILENAME_CHECKPOINT_EVALUATION_READINESS,
    REPORT_SEMANTICS_READY,
    REPORT_VERSION,
    REQUIRED_INPUT_KEYS,
    SCHEMA_VERSION,
    SEAL_KEY_ARTIFACT,
    STRONGEST_ALLOWED_CLAIM_M18,
    CandidateKind,
    CandidateReadinessStatus,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")

_WATCHABILITY_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "watchability_only",
        "m44_watchability",
        "m44_run_evidence",
        "m50_campaign_plumbing",
        "sandbox_watchability",
    }
)


def _is_valid_hex64(s: str) -> bool:
    return bool(_HEX64.match(s))


def _primary_artifact_suffix(manifest: dict[str, Any]) -> str:
    ref = manifest.get("primary_artifact_uri_or_reference")
    if isinstance(ref, str) and ref.strip():
        lower = ref.strip().lower()
        if lower.endswith(".joblib"):
            return ".joblib"
        if lower.endswith(".pth"):
            return ".pth"
        if lower.endswith(".pt"):
            return ".pt"
        return Path(lower).suffix.lower()
    return ""


def _classify_candidate_kind(manifest: dict[str, Any]) -> CandidateKind:
    sfx = _primary_artifact_suffix(manifest)
    if sfx == ".joblib":
        return CandidateKind.SKLEARN_BUNDLE
    if sfx in (".pt", ".pth"):
        return CandidateKind.PYTORCH_CHECKPOINT
    if sfx:
        return CandidateKind.UNKNOWN_ARTIFACT
    return CandidateKind.UNKNOWN_ARTIFACT


def _manifest_watchability_only(manifest: dict[str, Any]) -> bool:
    if manifest.get("watchability_only") is True:
        return True
    classes = manifest.get("evidence_classes")
    if not isinstance(classes, list) or not classes:
        return False
    norm = {str(c).strip() for c in classes if str(c).strip()}
    if not norm:
        return False
    return norm <= _WATCHABILITY_CLASSES


def _lineage_row_for_candidate(
    lineage: dict[str, Any], *, candidate_id: str, sha256: str
) -> dict[str, Any] | None:
    rows = lineage.get("checkpoints")
    if not isinstance(rows, list):
        return None
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("checkpoint_id", "")) != candidate_id:
            continue
        if str(row.get("checkpoint_sha256", "")).lower() == sha256.lower():
            return row
    return None


def _parse_lineage_file(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("checkpoint lineage JSON must be an object")
    return raw


def _parse_manifest_file(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("candidate manifest JSON must be an object")
    return raw


def _parse_receipt_file(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("campaign receipt JSON must be an object")
    return raw


def inventory_local_root(root: Path, *, max_depth: int = 6) -> list[dict[str, Any]]:
    """Operator-local inventory only: extension counts; no hashing or promotion."""

    root = root.resolve()
    counts: dict[str, int] = {}
    scanned = 0
    if not root.is_dir():
        return [
            {
                "check_id": "local_inspection_root",
                "status": "error",
                "detail": "not_a_directory",
                "path": str(root),
            }
        ]

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        try:
            depth = len(p.relative_to(root).parts)
        except ValueError:
            continue
        if depth > max_depth:
            continue
        scanned += 1
        suf = p.suffix.lower()
        if suf:
            counts[suf] = counts.get(suf, 0) + 1

    return [
        {
            "check_id": "local_inspection_inventory",
            "status": "informational",
            "files_scanned_depth_lte": scanned,
            "max_depth": max_depth,
            "extension_counts": dict(sorted(counts.items())),
        }
    ]


def classify_readiness(
    *,
    candidate_manifest: dict[str, Any] | None,
    campaign_receipt: dict[str, Any] | None,
    checkpoint_lineage: dict[str, Any] | None,
    inspection_checks: list[dict[str, Any]],
) -> tuple[
    CandidateReadinessStatus,
    CandidateKind,
    str | None,
    str | None,
    str | None,
    int,
    list[str],
    list[str],
    list[dict[str, Any]],
    list[str],
]:
    """Return classification fragments for the readiness body (deterministic)."""

    refusal_reasons: list[str] = []
    evidence_checks: list[dict[str, Any]] = list(inspection_checks)
    missing_inputs: list[str] = []

    if candidate_manifest is None:
        refusal_reasons.append(REFUSAL_NO_MANIFEST)
        status = CandidateReadinessStatus.NO_CANDIDATE_REFUSAL
        return (
            status,
            CandidateKind.NONE,
            None,
            None,
            None,
            0,
            refusal_reasons,
            [
                "provide_governed_candidate_checkpoint_manifest",
                "provide_m08_consistent_completed_campaign_receipt",
                "run_real_checkpoint_producing_campaign_before_strength_evaluation",
            ],
            evidence_checks,
            missing_inputs,
        )

    cid = str(candidate_manifest.get("candidate_id", "")).strip() or None
    declared_sha = str(candidate_manifest.get("candidate_checkpoint_sha256", "")).strip()

    if _manifest_watchability_only(candidate_manifest):
        refusal_reasons.append(REFUSAL_WATCHABILITY_ONLY)
        return (
            CandidateReadinessStatus.NO_CANDIDATE_REFUSAL,
            CandidateKind.NONE,
            cid,
            None,
            None,
            0,
            refusal_reasons,
            [
                "provide_pytorch_checkpoint_manifest_with_governed_lineage_and_receipt",
                "run_real_checkpoint_producing_campaign_before_strength_evaluation",
            ],
            evidence_checks,
            [],
        )

    kind = _classify_candidate_kind(candidate_manifest)
    if kind == CandidateKind.SKLEARN_BUNDLE:
        refusal_reasons.append(REFUSAL_JOBLIB_ONLY)
        return (
            CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE,
            kind,
            cid,
            declared_sha if _is_valid_hex64(declared_sha) else None,
            None,
            0,
            refusal_reasons,
            [
                "provide_pytorch_checkpoint_candidate_for_evaluation_readiness",
                "do_not_infer_neural_checkpoint_from_sklearn_bundle_alone",
            ],
            evidence_checks,
            ["candidate_checkpoint_manifest"],
        )

    if campaign_receipt is not None:
        if str(campaign_receipt.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT:
            evidence_checks.append(
                {
                    "check_id": "campaign_receipt_contract",
                    "status": "fail",
                    "detail": "wrong_contract_id",
                }
            )
        ccs = str(campaign_receipt.get("campaign_completion_status", ""))
        if ccs == "not_executed":
            refusal_reasons.append(REFUSAL_NOT_EXECUTED)
            ck_count = int(campaign_receipt.get("checkpoint_count") or 0)
            return (
                CandidateReadinessStatus.NO_CANDIDATE_REFUSAL,
                kind,
                cid,
                declared_sha if _is_valid_hex64(declared_sha) else None,
                ccs,
                ck_count,
                refusal_reasons,
                [
                    "provide_m08_consistent_completed_campaign_receipt",
                    "run_real_checkpoint_producing_campaign_before_strength_evaluation",
                ],
                evidence_checks,
                ["campaign_receipt"],
            )
        ck_count = int(campaign_receipt.get("checkpoint_count") or 0)
        if ck_count == 0:
            refusal_reasons.append(REFUSAL_CHECKPOINT_COUNT_ZERO)
            return (
                CandidateReadinessStatus.NO_CANDIDATE_REFUSAL,
                kind,
                cid,
                declared_sha if _is_valid_hex64(declared_sha) else None,
                ccs,
                0,
                refusal_reasons,
                [
                    "provide_m08_consistent_completed_campaign_receipt",
                    "run_real_checkpoint_producing_campaign_before_strength_evaluation",
                ],
                evidence_checks,
                ["campaign_receipt"],
            )
    else:
        ck_count = 0

    if kind != CandidateKind.PYTORCH_CHECKPOINT:
        refusal_reasons.append("candidate_artifact_not_pytorch_checkpoint")
        return (
            CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE,
            kind,
            cid,
            declared_sha if _is_valid_hex64(declared_sha) else None,
            str(campaign_receipt.get("campaign_completion_status", ""))
            if campaign_receipt
            else None,
            ck_count,
            refusal_reasons,
            ["provide_pytorch_checkpoint_manifest_with_sha256"],
            evidence_checks,
            ["candidate_checkpoint_manifest"],
        )

    if not declared_sha or declared_sha == PLACEHOLDER_SHA256 or not _is_valid_hex64(declared_sha):
        refusal_reasons.append(REFUSAL_INVALID_SHA)
        return (
            CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE,
            kind,
            cid,
            None,
            str(campaign_receipt.get("campaign_completion_status", ""))
            if campaign_receipt
            else None,
            ck_count,
            refusal_reasons,
            ["provide_declared_non_placeholder_candidate_checkpoint_sha256"],
            evidence_checks,
            ["candidate_checkpoint_sha256"],
        )

    env_sha = str(candidate_manifest.get("environment_manifest_sha256", "")).strip()
    ds_sha = str(candidate_manifest.get("dataset_manifest_sha256", "")).strip()
    eval_proto = str(candidate_manifest.get("evaluation_protocol_id", "")).strip()
    missing_fields: list[str] = []
    if not env_sha or env_sha == PLACEHOLDER_SHA256 or not _is_valid_hex64(env_sha):
        missing_fields.append("environment_manifest")
    if not ds_sha or ds_sha == PLACEHOLDER_SHA256 or not _is_valid_hex64(ds_sha):
        missing_fields.append("dataset_manifest")
    if not eval_proto:
        missing_fields.append("evaluation_protocol")

    if campaign_receipt is None or not m08_campaign_receipt_valid_for_m09(campaign_receipt):
        refusal_reasons.append(REFUSAL_MISSING_GOVERNED_RECEIPT)
        return (
            CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE,
            kind,
            cid,
            declared_sha,
            str(campaign_receipt.get("campaign_completion_status", ""))
            if campaign_receipt
            else None,
            ck_count,
            refusal_reasons,
            [
                "provide_m08_consistent_completed_campaign_receipt",
                "align_checkpoint_hashes_with_receipt",
            ],
            evidence_checks,
            ["campaign_receipt"] + missing_fields,
        )

    receipt_hashes = campaign_receipt.get("checkpoint_hashes")
    if isinstance(receipt_hashes, list) and receipt_hashes:
        if not any(str(h).lower() == declared_sha.lower() for h in receipt_hashes):
            refusal_reasons.append(REFUSAL_HASH_MISMATCH)
            return (
                CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE,
                kind,
                cid,
                declared_sha,
                str(campaign_receipt.get("campaign_completion_status", "")),
                ck_count,
                refusal_reasons,
                ["align_manifest_sha256_with_m08_campaign_receipt_checkpoint_hashes"],
                evidence_checks,
                ["candidate_checkpoint_sha256", "campaign_receipt"],
            )

    if checkpoint_lineage is None:
        refusal_reasons.append(REFUSAL_MISSING_LINEAGE)
        return (
            CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE,
            kind,
            cid,
            declared_sha,
            str(campaign_receipt.get("campaign_completion_status", "")),
            ck_count,
            refusal_reasons,
            ["provide_checkpoint_lineage_manifest_with_matching_checkpoint_row"],
            evidence_checks,
            ["checkpoint_lineage_manifest"] + missing_fields,
        )

    if str(checkpoint_lineage.get("contract_id", "")) != CONTRACT_ID_CHECKPOINT_LINEAGE:
        evidence_checks.append(
            {
                "check_id": "lineage_contract",
                "status": "warning",
                "detail": "unexpected_contract_id",
            }
        )

    if not cid:
        refusal_reasons.append("candidate_id_missing_in_manifest")
        return (
            CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE,
            kind,
            None,
            declared_sha,
            str(campaign_receipt.get("campaign_completion_status", "")),
            ck_count,
            refusal_reasons,
            ["declare_candidate_id_matching_lineage_row"],
            evidence_checks,
            ["candidate_id"] + missing_fields,
        )

    row = _lineage_row_for_candidate(checkpoint_lineage, candidate_id=cid, sha256=declared_sha)
    if row is None:
        refusal_reasons.append(REFUSAL_HASH_MISMATCH)
        return (
            CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE,
            kind,
            cid,
            declared_sha,
            str(campaign_receipt.get("campaign_completion_status", "")),
            ck_count,
            refusal_reasons,
            ["fix_lineage_checkpoint_sha256_or_candidate_id_mismatch"],
            evidence_checks,
            ["checkpoint_lineage_manifest"],
        )

    if missing_fields:
        refusal_reasons.append(REFUSAL_MISSING_MANIFEST_FIELDS)
        return (
            CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE,
            kind,
            cid,
            declared_sha,
            str(campaign_receipt.get("campaign_completion_status", "")),
            ck_count,
            refusal_reasons,
            [
                "bind_environment_dataset_and_evaluation_protocol_in_manifest",
            ],
            evidence_checks,
            missing_fields,
        )

    evidence_checks.append(
        {"check_id": "readiness_gates", "status": "pass", "detail": "inputs_structurally_ready"}
    )
    training_completion = str(campaign_receipt.get("campaign_completion_status", ""))
    return (
        CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION,
        kind,
        cid,
        declared_sha,
        training_completion,
        ck_count,
        [],
        ["proceed_to_bounded_checkpoint_evaluation_milestone_when_authorized"],
        evidence_checks,
        [],
    )


def build_readiness_body(
    *,
    profile: str,
    candidate_manifest: dict[str, Any] | None,
    campaign_receipt: dict[str, Any] | None,
    checkpoint_lineage: dict[str, Any] | None,
    inspection_checks: list[dict[str, Any]],
) -> dict[str, Any]:
    (
        status,
        kind,
        candidate_id,
        cand_sha,
        campaign_receipt_status,
        checkpoint_count,
        refusal_reasons,
        allowed_next,
        evidence_checks,
        missing_inputs,
    ) = classify_readiness(
        candidate_manifest=candidate_manifest,
        campaign_receipt=campaign_receipt,
        checkpoint_lineage=checkpoint_lineage,
        inspection_checks=inspection_checks,
    )

    training_completion: str | None = None
    if campaign_receipt is not None:
        training_completion = str(campaign_receipt.get("campaign_completion_status", "")) or None

    required_present = list(REQUIRED_INPUT_KEYS)
    missing_set = set(missing_inputs)
    checks_out: list[dict[str, Any]] = []
    for key in sorted(evidence_checks, key=lambda x: str(x.get("check_id", ""))):
        checks_out.append(key)

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS,
        "milestone_id": MILESTONE_ID_V15_M18,
        "profile": profile,
        "readiness_status": str(status),
        "candidate_kind": str(kind),
        "candidate_id": candidate_id,
        "candidate_checkpoint_sha256": cand_sha,
        "campaign_receipt_status": campaign_receipt_status,
        "training_completion_status": training_completion,
        "checkpoint_count": checkpoint_count,
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M18,
        "required_inputs": required_present,
        "missing_inputs": sorted(missing_set),
        "evidence_classes_accepted_for_readiness": [
            "governed_m08_campaign_receipt_completed",
            "pytorch_checkpoint_artifact_with_sha256",
            "checkpoint_lineage_manifest_row_match",
            "environment_dataset_evaluation_bindings_in_manifest",
        ],
        "evidence_checks": checks_out,
        "refusal_reasons": sorted(refusal_reasons),
        "allowed_next_steps": list(allowed_next),
        "non_claims": list(NON_CLAIMS_V15_M18),
        "report_semantics_if_ready": REPORT_SEMANTICS_READY
        if status == CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION
        else None,
        "emitter_module": EMITTER_MODULE_CHECKPOINT_EVALUATION_READINESS,
    }
    return body


def seal_readiness_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_KEY_ARTIFACT}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_KEY_ARTIFACT] = digest
    return sealed


def build_readiness_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_ARTIFACT}
    digest = sha256_hex_of_canonical_json(base)
    status = str(sealed.get("readiness_status", ""))
    return {
        "report_kind": "v15_checkpoint_evaluation_readiness_report",
        "report_version": REPORT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M18,
        "contract_id": CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS,
        "artifact_sha256": digest,
        "seal_field": SEAL_KEY_ARTIFACT,
        "primary_filename": FILENAME_CHECKPOINT_EVALUATION_READINESS,
        "readiness_status": status,
        "candidate_kind": sealed.get("candidate_kind"),
        "refusal_reasons": sealed.get("refusal_reasons"),
        "missing_inputs": sealed.get("missing_inputs"),
        "next_milestone_posture": sealed.get("allowed_next_steps"),
        "non_claims": sealed.get("non_claims"),
        "strongest_allowed_claim_summary": STRONGEST_ALLOWED_CLAIM_M18,
        "ready_semantics": REPORT_SEMANTICS_READY
        if status == str(CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION)
        else None,
    }


def emit_v15_checkpoint_evaluation_readiness(
    output_dir: Path,
    *,
    profile: str = PROFILE_FIXTURE_DEFAULT,
    candidate_manifest: dict[str, Any] | None = None,
    campaign_receipt: dict[str, Any] | None = None,
    checkpoint_lineage: dict[str, Any] | None = None,
    inspection_checks: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    inv = inspection_checks or []
    body = build_readiness_body(
        profile=profile,
        candidate_manifest=candidate_manifest,
        campaign_receipt=campaign_receipt,
        checkpoint_lineage=checkpoint_lineage,
        inspection_checks=inv,
    )
    sealed = seal_readiness_body(body)
    report = build_readiness_report(sealed)
    p_body = output_dir / FILENAME_CHECKPOINT_EVALUATION_READINESS
    p_rep = output_dir / REPORT_FILENAME_CHECKPOINT_EVALUATION_READINESS
    p_body.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(report), encoding="utf-8")
    return sealed, p_body, p_rep


def load_campaign_receipt_optional(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return _parse_receipt_file(path)


def load_checkpoint_lineage_optional(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return _parse_lineage_file(path)


def load_candidate_manifest(path: Path) -> dict[str, Any]:
    m = _parse_manifest_file(path)
    if str(m.get("contract_id", "")) != CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST:
        raise ValueError(
            f"candidate manifest contract_id must be {CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST!r}"
        )
    return m
