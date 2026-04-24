"""Build, seal, and write V15-M01 training asset registers JSON + report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.training_asset_register_models import (
    ASSET_CLASSES_V1,
    ASSET_ROW_REQUIRED_FIELDS_V1,
    CLAIM_USE_VOCABULARY_V1,
    MILESTONE_ID_V15_M01,
    NON_CLAIMS_V15_M01,
    PUBLIC_PRIVATE_POSTURE_VOCABULARY_V1,
    REDISTRIBUTION_POSTURE_VOCABULARY_V1,
    REVIEW_STATUS_VOCABULARY_V1,
    RIGHTS_POSTURE_VOCABULARY_V1,
    SOURCE_KIND_VOCABULARY_V1,
    STORAGE_POSTURE_VOCABULARY_V1,
    TRAINING_ASSET_REGISTERS_CONTRACT_VERSION,
    TRAINING_ASSET_REGISTERS_FILENAME,
    TRAINING_ASSET_REGISTERS_REPORT_FILENAME,
    TRAINING_ASSET_REGISTERS_REPORT_VERSION,
)


def required_registers_v1() -> list[dict[str, str]]:
    """Public register docs and optional private/local counterparts."""

    return [
        {
            "register_id": "training_asset",
            "public_doc": "docs/training_asset_register.md",
            "private_or_local_counterpart": (
                "Operator-local dataset manifests and paths under docs/company_secrets/ or out/ "
                "(never committed as raw corpora)"
            ),
        },
        {
            "register_id": "replay_corpus",
            "public_doc": "docs/replay_corpus_register.md",
            "private_or_local_counterpart": (
                "Operator-local replay corpus manifests; raw replay files stay local unless "
                "rights-cleared for public reference"
            ),
        },
        {
            "register_id": "model_weight",
            "public_doc": "docs/model_weight_register.md",
            "private_or_local_counterpart": (
                "Weight archives and checkpoints on operator storage; "
                "hash references in public docs only"
            ),
        },
        {
            "register_id": "checkpoint",
            "public_doc": "docs/checkpoint_asset_register.md",
            "private_or_local_counterpart": (
                "Checkpoint blobs under local_out or external_archive; "
                "lineage runtime deferred to V15-M03"
            ),
        },
        {
            "register_id": "human_benchmark",
            "public_doc": "docs/human_benchmark_register.md",
            "private_or_local_counterpart": (
                "Human-panel records with identities and raw paths — "
                "private by default (V15-M06 protocol)"
            ),
        },
        {
            "register_id": "xai_evidence",
            "public_doc": "docs/xai_evidence_register.md",
            "private_or_local_counterpart": (
                "Operator-local XAI packs until contract frozen (V15-M04)"
            ),
        },
        {
            "register_id": "rights",
            "public_doc": "docs/rights_register.md",
            "private_or_local_counterpart": (
                "Supplemental rights notes under docs/company_secrets/ (local-only)"
            ),
        },
    ]


def public_private_rules_v1() -> dict[str, Any]:
    """High-level public vs private posture for register rows."""

    return {
        "public_register_docs": (
            "Sparse, template-like tables only in M01 — no claim-critical asset rows committed."
        ),
        "default_private": (
            "raw_weights, raw_checkpoints, raw_replay_corpora, videos, human identities, "
            "unsanitized operator paths"
        ),
        "sanitized_public_reference": (
            "Hashes, contract ids, milestone ids, and governing doc pointers "
            "may appear in public docs when rights posture allows"
        ),
        "forbidden_public": (
            "Secrets, Blizzard client binaries, bulk third-party replay redistribution, "
            "uncleared human-panel PII"
        ),
    }


def hash_policy_v1() -> dict[str, str]:
    return {
        "primary_algorithm": "sha256",
        "canonical_json_module": "starlab.runs.json_util",
        "contract_seal_rule": (
            "training_asset_registers_sha256 covers the canonical JSON body "
            "excluding the seal field"
        ),
        "row_reference_rule": (
            "Each asset row records sha256_or_hash_reference for content-addressed blobs "
            "or a declared reference token when bytes are not in-repo"
        ),
    }


def carry_forward_items_v1() -> list[dict[str, str]]:
    return [
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "CI pip-audit may require narrow --ignore-vuln CVE-2026-3219 for pip "
                "until PyPI ships an audit-clean release; "
                "re-check each milestone (M01: still present on pip 26.0.1)."
            ),
        },
        {
            "item_id": "checkpoint_lineage_runtime",
            "summary": "V15-M03 implements checkpoint lineage / resume receipts — not M01.",
        },
        {
            "item_id": "xai_evidence_contract",
            "summary": "V15-M04 freezes XAI evidence pack shapes — M01 registers surface only.",
        },
    ]


def runtime_authority_refs_v1() -> dict[str, str]:
    return {
        "public_authority": "docs/starlab-v1.5.md",
        "runtime_contract_narrative": (
            "docs/runtime/v15_training_scale_provenance_asset_registers_v1.md"
        ),
        "prior_charter_runtime": "docs/runtime/v15_training_readiness_charter_v1.md",
    }


def _validate_contract_invariants(body: dict[str, Any]) -> None:
    """Internal consistency checks (emitter self-validation)."""

    assert body["contract_id"] == TRAINING_ASSET_REGISTERS_CONTRACT_VERSION
    assert body["milestone_id"] == MILESTONE_ID_V15_M01
    assert tuple(body["asset_classes"]) == ASSET_CLASSES_V1
    assert tuple(body["required_fields"]) == ASSET_ROW_REQUIRED_FIELDS_V1
    assert tuple(body["source_kind_vocabulary"]) == SOURCE_KIND_VOCABULARY_V1
    assert tuple(body["storage_posture_vocabulary"]) == STORAGE_POSTURE_VOCABULARY_V1
    assert tuple(body["public_private_posture_vocabulary"]) == PUBLIC_PRIVATE_POSTURE_VOCABULARY_V1
    assert tuple(body["rights_posture_vocabulary"]) == RIGHTS_POSTURE_VOCABULARY_V1
    assert tuple(body["redistribution_posture_vocabulary"]) == REDISTRIBUTION_POSTURE_VOCABULARY_V1
    assert tuple(body["claim_use_vocabulary"]) == CLAIM_USE_VOCABULARY_V1
    assert tuple(body["status_vocabulary"]) == REVIEW_STATUS_VOCABULARY_V1
    reg_docs = {r["public_doc"] for r in body["required_registers"]}
    for path in (
        "docs/training_asset_register.md",
        "docs/replay_corpus_register.md",
        "docs/model_weight_register.md",
        "docs/checkpoint_asset_register.md",
        "docs/human_benchmark_register.md",
        "docs/xai_evidence_register.md",
        "docs/rights_register.md",
    ):
        assert path in reg_docs


def build_training_asset_registers_body() -> dict[str, Any]:
    """Canonical contract body (without seal field)."""

    body: dict[str, Any] = {
        "contract_id": TRAINING_ASSET_REGISTERS_CONTRACT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M01,
        "generated_by": "starlab.v15.emit_v15_training_asset_registers",
        "authorization_posture": "register_contract_only_no_asset_approval_in_m01",
        "runtime_authority": runtime_authority_refs_v1(),
        "relationship_to_v15_m00": (
            "Implements the V15-M00 charter expectation that V15-M01+ provides training-scale "
            "registers and automation posture — without executing long GPU training or satisfying "
            "long_gpu_run_gates."
        ),
        "asset_classes": list(ASSET_CLASSES_V1),
        "required_registers": required_registers_v1(),
        "required_fields": list(ASSET_ROW_REQUIRED_FIELDS_V1),
        "status_vocabulary": list(REVIEW_STATUS_VOCABULARY_V1),
        "source_kind_vocabulary": list(SOURCE_KIND_VOCABULARY_V1),
        "storage_posture_vocabulary": list(STORAGE_POSTURE_VOCABULARY_V1),
        "public_private_posture_vocabulary": list(PUBLIC_PRIVATE_POSTURE_VOCABULARY_V1),
        "rights_posture_vocabulary": list(RIGHTS_POSTURE_VOCABULARY_V1),
        "redistribution_posture_vocabulary": list(REDISTRIBUTION_POSTURE_VOCABULARY_V1),
        "claim_use_vocabulary": list(CLAIM_USE_VOCABULARY_V1),
        "public_private_rules": public_private_rules_v1(),
        "hash_policy": hash_policy_v1(),
        "non_claims": list(NON_CLAIMS_V15_M01),
        "carry_forward_items": carry_forward_items_v1(),
    }
    _validate_contract_invariants(body)
    return body


def seal_training_asset_registers(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "training_asset_registers_sha256": digest}


def build_training_asset_registers_report(contract: dict[str, Any]) -> dict[str, Any]:
    digest = contract["training_asset_registers_sha256"]
    return {
        "report_version": TRAINING_ASSET_REGISTERS_REPORT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M01,
        "contract_id": TRAINING_ASSET_REGISTERS_CONTRACT_VERSION,
        "training_asset_registers_sha256": digest,
        "validation": {
            "contract_id_recognized": contract["contract_id"]
            == TRAINING_ASSET_REGISTERS_CONTRACT_VERSION,
            "asset_class_count": len(contract["asset_classes"]),
            "expected_asset_class_count": len(ASSET_CLASSES_V1),
            "required_register_count": len(contract["required_registers"]),
            "expected_required_register_count": len(required_registers_v1()),
            "required_field_count": len(contract["required_fields"]),
            "expected_required_field_count": len(ASSET_ROW_REQUIRED_FIELDS_V1),
            "vocabulary_lengths_match": (
                len(contract["source_kind_vocabulary"]) == len(SOURCE_KIND_VOCABULARY_V1)
                and len(contract["status_vocabulary"]) == len(REVIEW_STATUS_VOCABULARY_V1)
                and len(contract["claim_use_vocabulary"]) == len(CLAIM_USE_VOCABULARY_V1)
            ),
        },
    }


def write_training_asset_registers_artifacts(
    *,
    output_dir: Path,
    contract: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / TRAINING_ASSET_REGISTERS_FILENAME
    r_path = output_dir / TRAINING_ASSET_REGISTERS_REPORT_FILENAME
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_training_asset_registers(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    body = build_training_asset_registers_body()
    sealed = seal_training_asset_registers(body)
    rep = build_training_asset_registers_report(sealed)
    c_path, r_path = write_training_asset_registers_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
