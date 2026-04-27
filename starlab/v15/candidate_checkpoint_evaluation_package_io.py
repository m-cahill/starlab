"""Build, seal, and emit V15-M19 candidate checkpoint evaluation package artifacts."""

# ruff: noqa: E501

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
    EMITTER_MODULE,
    FILENAME_PACKAGE,
    M20_FORK_INCOMPLETE_ID,
    M20_FORK_INCOMPLETE_TITLE,
    M20_FORK_INVALID_ID,
    M20_FORK_INVALID_TITLE,
    M20_FORK_MISSING_ID,
    M20_FORK_MISSING_TITLE,
    M20_FORK_READY_ID,
    M20_FORK_READY_TITLE,
    MILESTONE_ID_V15_M19,
    NON_CLAIMS_V15_M19,
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    READY_SEMANTICS_M19,
    REASON_ENV_CONTRACT,
    REASON_HASH_MISMATCH,
    REASON_INVALID_M18_CONTRACT,
    REASON_JOBLIB,
    REASON_NOT_EXECUTED,
    REASON_SCORECARD_CONTRACT,
    REPORT_FILENAME,
    REPORT_VERSION,
    REQUIRED_INPUT_LIST,
    SCHEMA_VERSION,
    SEAL_KEY_ARTIFACT,
    STRONGEST_ALLOWED_CLAIM_M19,
    PackageStatus,
)
from starlab.v15.checkpoint_evaluation_io import m08_campaign_receipt_valid_for_m09
from starlab.v15.checkpoint_evaluation_readiness_io import (
    _classify_candidate_kind,
    _lineage_row_for_candidate,
)
from starlab.v15.checkpoint_evaluation_readiness_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST,
    CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS,
    REFUSAL_JOBLIB_ONLY,
    CandidateKind,
    CandidateReadinessStatus,
)
from starlab.v15.checkpoint_lineage_models import CONTRACT_ID_CHECKPOINT_LINEAGE
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.environment_lock_models import CONTRACT_ID_LONG_GPU_ENV
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT
from starlab.v15.strong_agent_scorecard_models import (
    CONTRACT_ID_STRONG_AGENT_SCORECARD,
    PROTOCOL_PROFILE_ID,
)

_HEX64: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")


def _is_hex64(s: str) -> bool:
    return bool(s and _HEX64.match(s.lower()))


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON file must be a single object")
    return sha256_hex_of_canonical_json(raw)


def _parse_json_object_path(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return raw


def _m18_readiness_to_status(s: str) -> CandidateReadinessStatus | None:
    try:
        return CandidateReadinessStatus(s)
    except ValueError:
        return None


def _recommended_m20_fork(
    status: PackageStatus,
) -> dict[str, str]:
    if status == PackageStatus.EVALUATION_PACKAGE_READY:
        return {
            "fork_id": M20_FORK_READY_ID,
            "title": M20_FORK_READY_TITLE,
            "rationale": "Package assembly succeeded; a future milestone may run checkpoint "
            "evaluation under frozen protocol.",
        }
    if status == PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE:
        return {
            "fork_id": M20_FORK_MISSING_ID,
            "title": M20_FORK_MISSING_TITLE,
            "rationale": "No governed candidate checkpoint chain; focus on real checkpoint production "
            "or M18 readiness before evaluation-input work.",
        }
    if status == PackageStatus.BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS:
        return {
            "fork_id": M20_FORK_INCOMPLETE_ID,
            "title": M20_FORK_INCOMPLETE_TITLE,
            "rationale": "Readiness or bindings are partial; remediate required manifests and receipts "
            "before a scorecard milestone.",
        }
    return {
        "fork_id": M20_FORK_INVALID_ID,
        "title": M20_FORK_INVALID_TITLE,
        "rationale": "Evidence is contradictory or hash-inconsistent; replace or realign the candidate "
        "package before evaluation.",
    }


def _claim_flags_all_false() -> dict[str, bool]:
    return {
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "benchmark_passed": False,
        "xai_claim_authorized": False,
        "human_benchmark_claim_authorized": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
    }


def _extract_m18_fields(m18: dict[str, Any]) -> dict[str, Any]:
    rs = str(m18.get("readiness_status", ""))
    parsed = _m18_readiness_to_status(rs)
    m18_ready = parsed == CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION
    if "ready_for_future_evaluation" in m18:
        v = m18.get("ready_for_future_evaluation")
        if isinstance(v, bool):
            m18_ready = v
    refusal = m18.get("refusal_reasons")
    m18_refusals: list[str] = []
    if isinstance(refusal, list):
        m18_refusals = [str(x) for x in refusal]
    return {
        "m18_readiness_status": rs,
        "candidate_id": m18.get("candidate_id"),
        "candidate_kind": m18.get("candidate_kind"),
        "candidate_checkpoint_sha256": m18.get("candidate_checkpoint_sha256"),
        "m18_ready_for_future_evaluation": m18_ready,
        "m18_refusal_reasons": m18_refusals,
    }


def _map_m18_to_package_baseline(
    m18_status: CandidateReadinessStatus | None,
) -> PackageStatus:
    if m18_status is None:
        return PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
    if m18_status == CandidateReadinessStatus.NO_CANDIDATE_REFUSAL:
        return PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
    if m18_status == CandidateReadinessStatus.INVALID_OR_UNSUPPORTED_CANDIDATE:
        return PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
    if m18_status == CandidateReadinessStatus.CANDIDATE_EVIDENCE_INCOMPLETE:
        return PackageStatus.BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS
    if m18_status == CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION:
        return PackageStatus.EVALUATION_PACKAGE_READY
    return PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE


def _default_fixture_body() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
        "milestone_id": MILESTONE_ID_V15_M19,
        "profile": PROFILE_FIXTURE_DEFAULT,
        "package_status": str(PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE),
        "ready_for_future_checkpoint_evaluation": False,
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
        "ready_semantics": READY_SEMANTICS_M19,
        "candidate_id": None,
        "candidate_kind": str(CandidateKind.NONE),
        "candidate_checkpoint_sha256": None,
        "m18_readiness_status": str(CandidateReadinessStatus.NO_CANDIDATE_REFUSAL),
        "m18_ready_for_future_evaluation": False,
        "m18_refusal_reasons": [],
        "input_bindings": {
            "m18_readiness_sha256": None,
            "candidate_manifest_sha256": None,
            "campaign_receipt_sha256": None,
            "checkpoint_lineage_sha256": None,
            "environment_manifest_sha256": None,
            "dataset_manifest_sha256": None,
            "evaluation_protocol_sha256": None,
        },
        "required_inputs": list(REQUIRED_INPUT_LIST),
        "provided_inputs": [],
        "missing_inputs": list(REQUIRED_INPUT_LIST),
        "blocked_reasons": [
            "no_m18_readiness_json_supplied",
            "no_governed_candidate_checkpoint_package",
        ],
        "allowed_next_steps": [
            "produce_governed_pytorch_checkpoint_candidate",
            "produce_completed_m08_campaign_receipt",
            "rerun_m18_readiness_after_candidate_package_exists",
        ],
        "non_claims": list(NON_CLAIMS_V15_M19),
        **_claim_flags_all_false(),
        "recommended_m20_fork": _recommended_m20_fork(
            PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE
        ),
        "emitter_module": EMITTER_MODULE,
    }


def _validate_scorecard_m05(s: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if str(s.get("contract_id", "")) != CONTRACT_ID_STRONG_AGENT_SCORECARD:
        out.append(REASON_SCORECARD_CONTRACT)
    if str(s.get("protocol_profile_id", "")) != PROTOCOL_PROFILE_ID:
        out.append(REASON_SCORECARD_CONTRACT)
    return list(dict.fromkeys(out))


def _validate_m02_lock(env: dict[str, Any]) -> list[str]:
    if str(env.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_ENV:
        return [REASON_ENV_CONTRACT]
    return []


def _final_status_from_m18_and_blocked(
    m18_parsed: CandidateReadinessStatus | None,
    blocked: list[str],
) -> tuple[PackageStatus, list[str]]:
    ublocked = list(dict.fromkeys(blocked))
    if REFUSAL_JOBLIB_ONLY in ublocked or REASON_JOBLIB in ublocked:
        return PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE, sorted(ublocked)
    if REASON_NOT_EXECUTED in ublocked:
        return PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE, sorted(ublocked)
    if (
        REASON_HASH_MISMATCH in ublocked
        or REASON_SCORECARD_CONTRACT in ublocked
        or REASON_ENV_CONTRACT in ublocked
        or any("mismatch" in x for x in ublocked)
    ):
        return PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE, sorted(ublocked)
    if m18_parsed == CandidateReadinessStatus.CANDIDATE_READY_FOR_EVALUATION:
        if not ublocked:
            return PackageStatus.EVALUATION_PACKAGE_READY, []
        return PackageStatus.BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS, sorted(ublocked)
    return _map_m18_to_package_baseline(m18_parsed), sorted(ublocked)


def _cross_validate_operator_preflight(
    m18: dict[str, Any],
    *,
    manifest: dict[str, Any],
    campaign_receipt: dict[str, Any],
    checkpoint_lineage: dict[str, Any],
    environment_manifest: dict[str, Any],
    dataset_manifest: dict[str, Any],  # noqa: ARG001 — reserved; manifest binds by SHA
    evaluation_protocol: dict[str, Any],
    bindings: Mapping[str, str | None],
) -> tuple[PackageStatus, list[str], list[str], list[dict[str, Any]]]:
    m18_parsed = _m18_readiness_to_status(str(m18.get("readiness_status", "")))
    checks: list[dict[str, Any]] = []
    blocked: list[str] = []

    man_cid = str(manifest.get("candidate_id", "")).strip()
    man_sha = str(manifest.get("candidate_checkpoint_sha256", "")).strip()
    m18_cid = m18.get("candidate_id")
    m18_cs = m18.get("candidate_checkpoint_sha256")
    if m18_cid is not None and str(m18_cid).strip() and man_cid and str(m18_cid) != man_cid:
        blocked.append("m18_candidate_id_mismatch_vs_manifest")
        checks.append({"check_id": "m18_vs_manifest_candidate_id", "status": "fail"})

    if (
        m18_cs is not None
        and str(m18_cs).strip()
        and man_sha
        and str(m18_cs).lower() != man_sha.lower()
    ):
        blocked.append("m18_candidate_sha_mismatch_vs_manifest")
        checks.append({"check_id": "m18_vs_manifest_sha", "status": "fail"})

    kind = _classify_candidate_kind(manifest)
    if kind == CandidateKind.SKLEARN_BUNDLE:
        blocked.append(REFUSAL_JOBLIB_ONLY)
        blocked.append(REASON_JOBLIB)
        checks.append({"check_id": "candidate_kind_sklearn_bundle", "status": "fail"})

    ccs = str(campaign_receipt.get("campaign_completion_status", ""))
    if ccs == "not_executed" or int(campaign_receipt.get("checkpoint_count") or 0) == 0:
        blocked.append(REASON_NOT_EXECUTED)
        checks.append({"check_id": "campaign_receipt_not_executed_or_zero_ck", "status": "fail"})

    if not m08_campaign_receipt_valid_for_m09(campaign_receipt):
        if REASON_NOT_EXECUTED not in blocked:
            blocked.append(REASON_NOT_EXECUTED)
        checks.append({"check_id": "m08_receipt_not_valid_for_m09_semantics", "status": "fail"})

    env_sha = str(manifest.get("environment_manifest_sha256", "")).strip()
    ds_sha = str(manifest.get("dataset_manifest_sha256", "")).strip()
    bind_env = bindings.get("environment_manifest_sha256")
    bind_ds = bindings.get("dataset_manifest_sha256")
    if bind_env and _is_hex64(env_sha) and env_sha.lower() != str(bind_env).lower():
        blocked.append("environment_manifest_sha256_mismatch")
        status_note = "fail"
        checks.append({"check_id": "manifest_env_sha_vs_file", "status": status_note})

    if bind_ds and _is_hex64(ds_sha) and ds_sha.lower() != str(bind_ds).lower():
        blocked.append("dataset_manifest_sha256_mismatch")
        checks.append({"check_id": "manifest_dataset_sha_vs_file", "status": "fail"})

    if man_sha and _is_hex64(man_sha):
        rhashes = campaign_receipt.get("checkpoint_hashes")
        if isinstance(rhashes, list) and rhashes:
            if not any(str(h).lower() == man_sha.lower() for h in rhashes):
                blocked.append(REASON_HASH_MISMATCH)
                checks.append(
                    {"check_id": "manifest_sha_vs_receipt_checkpoint_hashes", "status": "fail"}
                )

    if man_cid and man_sha and _is_hex64(man_sha):
        row = _lineage_row_for_candidate(checkpoint_lineage, candidate_id=man_cid, sha256=man_sha)
        if row is None:
            blocked.append(REASON_HASH_MISMATCH)
            checks.append({"check_id": "lineage_row_for_candidate", "status": "fail"})

    blocked.extend(_validate_scorecard_m05(evaluation_protocol))
    if any(x in blocked for x in (REASON_SCORECARD_CONTRACT,)):
        checks.append({"check_id": "strong_agent_scorecard_contract", "status": "fail"})

    blocked.extend(_validate_m02_lock(environment_manifest))
    if REASON_ENV_CONTRACT in blocked:
        checks.append({"check_id": "m02_environment_lock_contract", "status": "fail"})

    ev_proto = str(manifest.get("evaluation_protocol_id", "")).strip()
    if ev_proto and str(evaluation_protocol.get("protocol_profile_id", "")) != ev_proto:
        blocked.append("evaluation_protocol_id_mismatch_manifest_vs_scorecard")
        checks.append({"check_id": "manifest_eval_protocol_id_vs_scorecard", "status": "fail"})

    st, br = _final_status_from_m18_and_blocked(m18_parsed, blocked)
    if st == PackageStatus.EVALUATION_PACKAGE_READY:
        allowed = [
            "open_future_checkpoint_evaluation_milestone_on_operator_authorization",
        ]
    elif st == PackageStatus.BLOCKED_MISSING_CANDIDATE_CHECKPOINT_EVIDENCE:
        allowed = [
            "produce_governed_pytorch_checkpoint_candidate",
            "produce_completed_m08_campaign_receipt",
            "rerun_m18_readiness_after_candidate_package_exists",
        ]
    elif st == PackageStatus.BLOCKED_INCOMPLETE_EVALUATION_PACKAGE_INPUTS:
        allowed = [
            "bind_missing_manifests_and_m08_receipt",
            "align_lineage_and_campaign_hashes",
        ]
    else:
        allowed = [
            "replace_invalid_candidate_or_rebuild_manifests",
            "align_hashes_across_m03_m08_m18",
        ]
    if not checks:
        checks.append(
            {
                "check_id": "m19_package_cross_validation",
                "status": "pass" if st == PackageStatus.EVALUATION_PACKAGE_READY else "fail",
            }
        )
    return st, br, allowed, checks


def build_operator_preflight_body(
    *,
    m18_path: Path,
    candidate_manifest_path: Path,
    campaign_receipt_path: Path,
    checkpoint_lineage_path: Path,
    environment_manifest_path: Path,
    dataset_manifest_path: Path,
    evaluation_protocol_path: Path,
) -> dict[str, Any]:
    m18 = _parse_json_object_path(m18_path)
    m18_sha = _json_file_canonical_sha256(m18_path)

    if str(m18.get("contract_id", "")) != CONTRACT_ID_CHECKPOINT_EVALUATION_READINESS:
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
            "milestone_id": MILESTONE_ID_V15_M19,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "package_status": str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE),
            "ready_for_future_checkpoint_evaluation": False,
            "ready_semantics": None,
            "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
            "blocked_reasons": sorted({REASON_INVALID_M18_CONTRACT}),
            "allowed_next_steps": ["supply_starlab_m18_checkpoint_evaluation_readiness_json"],
            "non_claims": list(NON_CLAIMS_V15_M19),
            **_claim_flags_all_false(),
            "recommended_m20_fork": _recommended_m20_fork(
                PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
            ),
            "emitter_module": EMITTER_MODULE,
            **_extract_m18_fields(m18),
            "input_bindings": {
                "m18_readiness_sha256": m18_sha,
                "candidate_manifest_sha256": None,
                "campaign_receipt_sha256": None,
                "checkpoint_lineage_sha256": None,
                "environment_manifest_sha256": None,
                "dataset_manifest_sha256": None,
                "evaluation_protocol_sha256": None,
            },
            "required_inputs": list(REQUIRED_INPUT_LIST),
            "provided_inputs": ["m18_readiness_json"],
            "missing_inputs": [x for x in REQUIRED_INPUT_LIST if x != "m18_readiness_json"],
        }

    manifest = _parse_json_object_path(candidate_manifest_path)
    if str(manifest.get("contract_id", "")) != CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST:
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
            "milestone_id": MILESTONE_ID_V15_M19,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "package_status": str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE),
            "ready_for_future_checkpoint_evaluation": False,
            "ready_semantics": None,
            "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
            "blocked_reasons": ["invalid_candidate_checkpoint_manifest_contract_id"],
            "allowed_next_steps": ["fix_candidate_manifest_contract_id"],
            "non_claims": list(NON_CLAIMS_V15_M19),
            **_claim_flags_all_false(),
            "recommended_m20_fork": _recommended_m20_fork(
                PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
            ),
            "emitter_module": EMITTER_MODULE,
            **_extract_m18_fields(m18),
            "input_bindings": {
                "m18_readiness_sha256": m18_sha,
                "candidate_manifest_sha256": _json_file_canonical_sha256(candidate_manifest_path),
                "campaign_receipt_sha256": None,
                "checkpoint_lineage_sha256": None,
                "environment_manifest_sha256": None,
                "dataset_manifest_sha256": None,
                "evaluation_protocol_sha256": None,
            },
            "required_inputs": list(REQUIRED_INPUT_LIST),
            "provided_inputs": ["m18_readiness_json", "candidate_checkpoint_manifest"],
            "missing_inputs": [
                x
                for x in REQUIRED_INPUT_LIST
                if x not in ("m18_readiness_json", "candidate_checkpoint_manifest")
            ],
        }

    campaign = _parse_json_object_path(campaign_receipt_path)
    lineage = _parse_json_object_path(checkpoint_lineage_path)
    env = _parse_json_object_path(environment_manifest_path)
    ds = _parse_json_object_path(dataset_manifest_path)
    score = _parse_json_object_path(evaluation_protocol_path)
    man_sha = _json_file_canonical_sha256(candidate_manifest_path)
    rec_sha = _json_file_canonical_sha256(campaign_receipt_path)
    lin_sha = _json_file_canonical_sha256(checkpoint_lineage_path)
    env_f_sha = _json_file_canonical_sha256(environment_manifest_path)
    ds_f_sha = _json_file_canonical_sha256(dataset_manifest_path)
    sc_sha = _json_file_canonical_sha256(evaluation_protocol_path)

    bindings: dict[str, str | None] = {
        "m18_readiness_sha256": m18_sha,
        "candidate_manifest_sha256": man_sha,
        "campaign_receipt_sha256": rec_sha,
        "checkpoint_lineage_sha256": lin_sha,
        "environment_manifest_sha256": env_f_sha,
        "dataset_manifest_sha256": ds_f_sha,
        "evaluation_protocol_sha256": sc_sha,
    }

    if str(campaign.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT:
        m18f = _extract_m18_fields(m18)
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
            "milestone_id": MILESTONE_ID_V15_M19,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "package_status": str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE),
            "ready_for_future_checkpoint_evaluation": False,
            "ready_semantics": None,
            "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
            **m18f,
            "input_bindings": dict(bindings),
            "required_inputs": list(REQUIRED_INPUT_LIST),
            "provided_inputs": [x for x in REQUIRED_INPUT_LIST],
            "missing_inputs": [],
            "blocked_reasons": ["invalid_long_gpu_campaign_receipt_contract_id"],
            "allowed_next_steps": ["fix_governance_json_contract_ids"],
            "non_claims": list(NON_CLAIMS_V15_M19),
            **_claim_flags_all_false(),
            "recommended_m20_fork": _recommended_m20_fork(
                PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
            ),
            "emitter_module": EMITTER_MODULE,
        }

    if str(lineage.get("contract_id", "")) != CONTRACT_ID_CHECKPOINT_LINEAGE:
        m18f = _extract_m18_fields(m18)
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
            "milestone_id": MILESTONE_ID_V15_M19,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "package_status": str(PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE),
            "ready_for_future_checkpoint_evaluation": False,
            "ready_semantics": None,
            "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
            **m18f,
            "input_bindings": dict(bindings),
            "required_inputs": list(REQUIRED_INPUT_LIST),
            "provided_inputs": [x for x in REQUIRED_INPUT_LIST],
            "missing_inputs": [],
            "blocked_reasons": ["invalid_checkpoint_lineage_contract_id"],
            "allowed_next_steps": ["fix_governance_json_contract_ids"],
            "non_claims": list(NON_CLAIMS_V15_M19),
            **_claim_flags_all_false(),
            "recommended_m20_fork": _recommended_m20_fork(
                PackageStatus.BLOCKED_INVALID_CANDIDATE_PACKAGE
            ),
            "emitter_module": EMITTER_MODULE,
        }

    st, br, allowed, cross = _cross_validate_operator_preflight(
        m18,
        manifest=manifest,
        campaign_receipt=campaign,
        checkpoint_lineage=lineage,
        environment_manifest=env,
        dataset_manifest=ds,
        evaluation_protocol=score,
        bindings=bindings,
    )
    m18f = _extract_m18_fields(m18)
    ready = st == PackageStatus.EVALUATION_PACKAGE_READY
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
        "milestone_id": MILESTONE_ID_V15_M19,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "package_status": str(st),
        "ready_for_future_checkpoint_evaluation": ready,
        "ready_semantics": READY_SEMANTICS_M19 if ready else None,
        "strongest_allowed_claim": STRONGEST_ALLOWED_CLAIM_M19,
        **m18f,
        "candidate_id": m18f.get("candidate_id") or manifest.get("candidate_id"),
        "candidate_kind": str(m18f.get("candidate_kind") or _classify_candidate_kind(manifest)),
        "candidate_checkpoint_sha256": m18f.get("candidate_checkpoint_sha256")
        or manifest.get("candidate_checkpoint_sha256"),
        "input_bindings": dict(bindings),
        "required_inputs": list(REQUIRED_INPUT_LIST),
        "provided_inputs": list(REQUIRED_INPUT_LIST),
        "missing_inputs": [],
        "blocked_reasons": br,
        "cross_validation_checks": cross,
        "allowed_next_steps": allowed,
        "non_claims": list(NON_CLAIMS_V15_M19),
        **_claim_flags_all_false(),
        "recommended_m20_fork": _recommended_m20_fork(st),
        "emitter_module": EMITTER_MODULE,
    }


def seal_package_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_KEY_ARTIFACT}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_KEY_ARTIFACT] = digest
    return sealed


def build_package_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_KEY_ARTIFACT}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_candidate_checkpoint_evaluation_package_report",
        "report_version": REPORT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M19,
        "contract_id": CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE,
        "artifact_sha256": digest,
        "seal_field": SEAL_KEY_ARTIFACT,
        "primary_filename": FILENAME_PACKAGE,
        "package_status": sealed.get("package_status"),
        "ready_for_future_checkpoint_evaluation": sealed.get(
            "ready_for_future_checkpoint_evaluation"
        ),
        "m18_readiness_status": sealed.get("m18_readiness_status"),
        "missing_inputs": sealed.get("missing_inputs"),
        "blocked_reasons": sealed.get("blocked_reasons"),
        "allowed_next_steps": sealed.get("allowed_next_steps"),
        "non_claims": sealed.get("non_claims"),
        "recommended_m20_fork": sealed.get("recommended_m20_fork"),
    }


def build_checklist_markdown(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("package_status", ""))
    mark = "[x]" if st == "evaluation_package_ready" else "[ ]"
    fork = sealed.get("recommended_m20_fork")
    if isinstance(fork, dict) and fork.get("title"):
        ftitle = str(fork.get("title", ""))
    else:
        ftitle = "see package report"
    return (
        f"# V15-M19 — Candidate checkpoint evaluation package assembly checklist\n\n"
        f"**`package_status`:** `{st}`\n\n"
        f"| Gate | Check |\n| --- | --- |\n"
        f"| P0 — M18 readiness binding | {mark} M18 JSON bound by SHA |\n"
        f"| P1 — Candidate manifest present | {mark} `candidate_checkpoint_manifest` |\n"
        f"| P2 — Completed campaign receipt present | {mark} M08 `completed` receipt semantics |\n"
        f"| P3 — Checkpoint lineage binding | {mark} M03 lineage row for candidate |\n"
        f"| P4 — Environment binding | {mark} M02 environment lock + manifest SHA |\n"
        f"| P5 — Dataset binding | {mark} dataset manifest + manifest SHA |\n"
        f"| P6 — Evaluation protocol binding | {mark} M05 strong-agent scorecard JSON |\n"
        f"| P7 — Cross-artifact SHA consistency | {mark} manifest/lineage/receipt alignment |\n"
        f"| P8 — Non-claim / public-private boundary | {mark} claim flags false |\n"
        f"| P9 — M20 fork recommendation | {mark} {ftitle} |\n\n"
        "V15-M19 assembles evaluation inputs. It does not run candidate checkpoint evaluation.\n"
    )


def _build_body_for_profile(
    profile: str,
    *,
    m18_path: Path | None = None,
    candidate_manifest_path: Path | None = None,
    campaign_receipt_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    environment_manifest_path: Path | None = None,
    dataset_manifest_path: Path | None = None,
    evaluation_protocol_path: Path | None = None,
) -> dict[str, Any]:
    if profile == PROFILE_FIXTURE_DEFAULT:
        return _default_fixture_body()
    if profile == PROFILE_OPERATOR_PREFLIGHT:
        assert m18_path is not None
        assert candidate_manifest_path is not None
        assert campaign_receipt_path is not None
        assert checkpoint_lineage_path is not None
        assert environment_manifest_path is not None
        assert dataset_manifest_path is not None
        assert evaluation_protocol_path is not None
        return build_operator_preflight_body(
            m18_path=m18_path,
            candidate_manifest_path=candidate_manifest_path,
            campaign_receipt_path=campaign_receipt_path,
            checkpoint_lineage_path=checkpoint_lineage_path,
            environment_manifest_path=environment_manifest_path,
            dataset_manifest_path=dataset_manifest_path,
            evaluation_protocol_path=evaluation_protocol_path,
        )
    raise ValueError(f"unsupported profile: {profile!r}")


def emit_v15_candidate_checkpoint_evaluation_package(
    output_dir: Path,
    *,
    profile: str = PROFILE_FIXTURE_DEFAULT,
    m18_path: Path | None = None,
    candidate_manifest_path: Path | None = None,
    campaign_receipt_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    environment_manifest_path: Path | None = None,
    dataset_manifest_path: Path | None = None,
    evaluation_protocol_path: Path | None = None,
) -> tuple[dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = _build_body_for_profile(
        profile,
        m18_path=m18_path,
        candidate_manifest_path=candidate_manifest_path,
        campaign_receipt_path=campaign_receipt_path,
        checkpoint_lineage_path=checkpoint_lineage_path,
        environment_manifest_path=environment_manifest_path,
        dataset_manifest_path=dataset_manifest_path,
        evaluation_protocol_path=evaluation_protocol_path,
    )
    sealed = seal_package_body(body)
    rep = build_package_report(sealed)
    checklist = build_checklist_markdown(sealed)
    p_pkg = output_dir / FILENAME_PACKAGE
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkg.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(checklist, encoding="utf-8", newline="\n")
    return sealed, p_pkg, p_rep, p_chk


def emit_operator_declared_package(
    output_dir: Path,
    *,
    package_json: Path,
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Normalize operator package JSON, redact path-like strings, re-seal (metadata-only)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = _parse_json_object_path(package_json)
    if str(raw.get("contract_id", "")) != CONTRACT_ID_CANDIDATE_CHECKPOINT_EVALUATION_PACKAGE:
        raise ValueError("operator_declared package JSON must be starlab M19 contract")
    red = redact_paths_in_value(raw)
    if not isinstance(red, dict):
        raise TypeError("expected object after redaction")
    red["profile"] = PROFILE_OPERATOR_DECLARED
    red["milestone_id"] = MILESTONE_ID_V15_M19
    ncl = (
        [str(x) for x in red.get("non_claims", [])]
        if isinstance(red.get("non_claims"), list)
        else []
    )
    for n in NON_CLAIMS_V15_M19:
        if n not in ncl:
            ncl.append(n)
    red["non_claims"] = ncl
    for k, v in _claim_flags_all_false().items():
        if k not in red:
            red[k] = v
    if "ready_for_future_checkpoint_evaluation" not in red:
        red["ready_for_future_checkpoint_evaluation"] = str(red.get("package_status", "")) == str(
            PackageStatus.EVALUATION_PACKAGE_READY
        )
    sealed = seal_package_body(red)
    rep = build_package_report(sealed)
    checklist = build_checklist_markdown(sealed)
    p_pkg = output_dir / FILENAME_PACKAGE
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_pkg.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(checklist, encoding="utf-8", newline="\n")
    return sealed, p_pkg, p_rep, p_chk
