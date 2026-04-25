"""Build, seal, and write V15-M03 checkpoint lineage manifest + report."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_models import (
    CHECK_PASS,
    CHECK_WARNING,
    CHECKPOINT_ROW_REQUIRED_FIELDS,
    CONTRACT_ID_CHECKPOINT_LINEAGE,
    CONTRACT_ID_M02_ENV_LOCK,
    EMITTER_MODULE_CHECKPOINT_LINEAGE,
    EVIDENCE_CI_FIXTURE,
    EVIDENCE_OPERATOR_DECLARED,
    EVIDENCE_OPERATOR_LOCAL_METADATA,
    FILENAME_CHECKPOINT_LINEAGE,
    INTERRUPTION_RECEIPT_REQUIRED_FIELDS,
    LINEAGE_JSON_TOP_LEVEL_KEYS,
    LINEAGE_STATUS_FIXTURE_ONLY,
    LINEAGE_STATUS_OP_COMPLETE,
    LINEAGE_STATUS_OP_INCOMPLETE,
    MILESTONE_ID_V15_M03,
    NON_CLAIMS_V15_M03,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    REPORT_FILENAME_CHECKPOINT_LINEAGE,
    REPORT_VERSION_CHECKPOINT_LINEAGE,
    RESUME_RECEIPT_REQUIRED_FIELDS,
    ROLLBACK_RECEIPT_REQUIRED_FIELDS,
    STATUS_VOCABULARY,
)
from starlab.v15.environment_lock_io import redact_paths_in_value

_SEAL_KEY: Final[str] = "checkpoint_lineage_manifest_sha256"

_PLACEHOLDER_SHA256: Final[str] = "0" * 64


def _vocab_tuples() -> dict[str, tuple[str, ...]]:
    return {k: tuple(v) for k, v in STATUS_VOCABULARY.items()}


def _validate_in_vocab(name: str, value: str) -> bool:
    vocab = _vocab_tuples()
    if name not in vocab:
        return True
    return value in vocab[name]


def environment_lock_file_canonical_sha256(path: Path) -> str:
    """SHA-256 of canonical JSON of parsed M02 (or any) environment-lock file."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("environment lock JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def parse_lineage_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("lineage JSON must be a single object")
    unknown = set(raw) - set(LINEAGE_JSON_TOP_LEVEL_KEYS)
    if unknown:
        raise ValueError(f"unknown top-level keys in lineage JSON: {sorted(unknown)}")
    return raw


def _fixture_checkpoints() -> list[dict[str, Any]]:
    base_non_claims = ["fixture_metadata_not_real_checkpoint_file"]
    return [
        {
            "checkpoint_id": "fixture-root",
            "checkpoint_role": "fixture",
            "checkpoint_storage_posture": "repo_fixture",
            "checkpoint_path_disclosure": "logical_reference_only",
            "checkpoint_uri_or_reference": "fixture:checkpoint_lineage/v1/root",
            "checkpoint_sha256": _PLACEHOLDER_SHA256,
            "hash_verification_status": "fixture",
            "parent_checkpoint_id": None,
            "training_run_id": "fixture:training_run_v1",
            "environment_lock_sha256": _PLACEHOLDER_SHA256,
            "dataset_manifest_sha256": _PLACEHOLDER_SHA256,
            "model_config_sha256": _PLACEHOLDER_SHA256,
            "step": 0,
            "episode": 0,
            "wall_clock_elapsed": "PT0S",
            "promotion_status": "fixture_only",
            "created_by_event": "fixture_emission",
            "non_claims": list(base_non_claims),
        },
        {
            "checkpoint_id": "fixture-child",
            "checkpoint_role": "fixture",
            "checkpoint_storage_posture": "repo_fixture",
            "checkpoint_path_disclosure": "logical_reference_only",
            "checkpoint_uri_or_reference": "fixture:checkpoint_lineage/v1/child",
            "checkpoint_sha256": _PLACEHOLDER_SHA256,
            "hash_verification_status": "fixture",
            "parent_checkpoint_id": "fixture-root",
            "training_run_id": "fixture:training_run_v1",
            "environment_lock_sha256": _PLACEHOLDER_SHA256,
            "dataset_manifest_sha256": _PLACEHOLDER_SHA256,
            "model_config_sha256": _PLACEHOLDER_SHA256,
            "step": 1,
            "episode": 0,
            "wall_clock_elapsed": "PT0S",
            "promotion_status": "fixture_only",
            "created_by_event": "fixture_emission",
            "non_claims": list(base_non_claims),
        },
    ]


def _fixture_interruption() -> list[dict[str, Any]]:
    return [
        {
            "interruption_id": "fixture-intr-1",
            "training_run_id": "fixture:training_run_v1",
            "checkpoint_id": "fixture-child",
            "reason": "fixture_interruption",
            "interruption_step": 1,
            "interruption_episode": 0,
            "operator_declared_at": "1970-01-01T00:00:00Z",
            "receipt_status": "fixture",
            "notes": "Fixture receipt shape only; not a real training interruption event.",
        }
    ]


def _fixture_resume() -> list[dict[str, Any]]:
    return [
        {
            "resume_id": "fixture-resume-1",
            "training_run_id": "fixture:training_run_v1",
            "from_checkpoint_id": "fixture-child",
            "resume_step": 1,
            "resume_episode": 0,
            "resume_policy": "fixture",
            "resume_verification_status": "fixture",
            "notes": "Fixture resume receipt shape; M03 does not prove trainer execution.",
        }
    ]


def _fixture_rollback() -> list[dict[str, Any]]:
    return [
        {
            "rollback_id": "fixture-rollback-1",
            "training_run_id": "fixture:training_run_v1",
            "from_checkpoint_id": "fixture-child",
            "to_checkpoint_id": "fixture-root",
            "rollback_reason": "fixture",
            "rollback_policy": "fixture",
            "rollback_verification_status": "fixture",
            "notes": "Fixture rollback receipt shape; M03 does not execute rollback.",
        }
    ]


def _carry_forward() -> list[dict[str, str]]:
    return [
        {
            "item_id": "pip_cve_2026_3219",
            "summary": (
                "pip-audit may require --ignore-vuln CVE-2026-3219 for the pip toolchain until "
                "PyPI publishes an audit-clean release. M03 re-check 2026-04-25: latest PyPI pip "
                "26.0.1 still reported CVE-2026-3219 to pip-audit."
            ),
        },
        {
            "item_id": "v15_m04_xai_evidence_contract",
            "summary": "V15-M04 — XAI evidence contract; not M03.",
        },
    ]


def _check_results_fixture() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "m03_lineage_fields_present",
            "description": (
                "Fixture checkpoint rows include required M03 lineage fields (metadata-only)."
            ),
            "status": CHECK_PASS,
        },
        {
            "check_id": "m03_not_executing_trainer",
            "description": "M03 does not run GPU training, resume, or rollback execution.",
            "status": CHECK_PASS,
        },
    ]


def _m03_attestation() -> str:
    return (
        "V15-M03 defines and emits the checkpoint lineage and resume-discipline surface. "
        "It may validate fixture metadata and may normalize supplied operator-declared "
        "checkpoint lineage metadata, but it does not create checkpoint blobs, does not "
        "verify checkpoint bytes by default, does not execute trainer resume, does not "
        "execute rollback, does not promote a strong checkpoint, does not run evaluation, "
        "does not execute GPU training or shakedown, does not authorize a long GPU run, "
        "does not approve real assets for claim-critical use, does not open v2, and does "
        "not open PX2-M04/PX2-M05. Any verified_external status in receipts or hashes is "
        "operator-declared pass-through; M03 does not perform independent external verification. "
        "A checkpoint lineage manifest is not a proof that checkpoint bytes exist unless the "
        "hash verification status says so under a declared verification path. "
        "A resume receipt is not proof that training resumed unless the resume verification "
        "status says so under a declared verification path, and M03 still does not "
        "independently verify execution."
    )


def build_checkpoint_lineage_body_fixture() -> dict[str, Any]:
    cps = _fixture_checkpoints()
    return {
        "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
        "milestone_id": MILESTONE_ID_V15_M03,
        "generated_by": EMITTER_MODULE_CHECKPOINT_LINEAGE,
        "profile": PROFILE_FIXTURE_CI,
        "lineage_manifest_status": LINEAGE_STATUS_FIXTURE_ONLY,
        "long_gpu_run_authorized": False,
        "checkpoint_bytes_verified": False,
        "resume_execution_verified": False,
        "rollback_execution_verified": False,
        "evidence_scope": EVIDENCE_CI_FIXTURE,
        "training_run_identity": {
            "training_run_id": "fixture:training_run_v1",
            "label": "fixture training run (metadata only)",
        },
        "environment_lock_reference": {
            "reference_kind": "fixture_placeholder",
            "m02_contract_id": None,
            "environment_lock_json_canonical_sha256": None,
            "logical_label": "fixture:environment_lock_unbound",
        },
        "dataset_reference": {
            "reference_kind": "fixture_placeholder",
            "logical_label": "fixture:dataset_unbound",
        },
        "model_config_reference": {
            "reference_kind": "fixture_placeholder",
            "logical_label": "fixture:model_config_unbound",
        },
        "checkpoint_lineage": cps,
        "interruption_receipts": _fixture_interruption(),
        "resume_receipts": _fixture_resume(),
        "rollback_receipts": _fixture_rollback(),
        "lineage_manifest_status_vocabulary": list(STATUS_VOCABULARY["lineage_manifest_status"]),
        "checkpoint_role_vocabulary": list(STATUS_VOCABULARY["checkpoint_role"]),
        "promotion_status_vocabulary": list(STATUS_VOCABULARY["promotion_status"]),
        "hash_verification_status_vocabulary": list(STATUS_VOCABULARY["hash_verification_status"]),
        "resume_verification_status_vocabulary": list(
            STATUS_VOCABULARY["resume_verification_status"]
        ),
        "rollback_verification_status_vocabulary": list(
            STATUS_VOCABULARY["rollback_verification_status"]
        ),
        "receipt_status_vocabulary": list(STATUS_VOCABULARY["receipt_status"]),
        "storage_posture_vocabulary": list(STATUS_VOCABULARY["checkpoint_storage_posture"]),
        "path_disclosure_vocabulary": list(STATUS_VOCABULARY["checkpoint_path_disclosure"]),
        "required_fields": {
            "checkpoint_row": list(CHECKPOINT_ROW_REQUIRED_FIELDS),
            "interruption_receipt": list(INTERRUPTION_RECEIPT_REQUIRED_FIELDS),
            "resume_receipt": list(RESUME_RECEIPT_REQUIRED_FIELDS),
            "rollback_receipt": list(ROLLBACK_RECEIPT_REQUIRED_FIELDS),
        },
        "check_results": _check_results_fixture(),
        "m03_verification_attestation": _m03_attestation(),
        "non_claims": list(NON_CLAIMS_V15_M03),
        "carry_forward_items": _carry_forward(),
    }


def _as_str(v: Any, field: str) -> str:
    if not isinstance(v, str):
        raise TypeError(f"{field} must be a string")
    return v


def _as_str_or_null(v: Any, field: str) -> str | None:
    if v is None:
        return None
    return _as_str(v, field)


def _validate_checkpoint_row(row: Any, *, ctx: str) -> None:
    if not isinstance(row, dict):
        raise ValueError(f"{ctx} must be an object")
    for k in CHECKPOINT_ROW_REQUIRED_FIELDS:
        if k not in row:
            raise ValueError(f"{ctx} missing field {k!r}")
    for k in row:
        if k not in CHECKPOINT_ROW_REQUIRED_FIELDS:
            raise ValueError(f"{ctx} unknown field {k!r}")


def _typecheck_checkpoint_row(row: dict[str, Any], ctx: str) -> None:
    if not isinstance(row.get("non_claims"), list) or not all(
        isinstance(x, str) for x in row.get("non_claims", [])
    ):
        raise TypeError(f"{ctx} non_claims must be a list of strings")
    if not isinstance(row.get("step"), int) or isinstance(row["step"], bool):
        raise TypeError(f"{ctx} step must be an int")
    if not isinstance(row.get("episode"), int) or isinstance(row["episode"], bool):
        raise TypeError(f"{ctx} episode must be an int")


def _validate_receipt_row(
    row: Any,
    fields: tuple[str, ...],
    ctx: str,
) -> None:
    if not isinstance(row, dict):
        raise ValueError(f"{ctx} must be an object")
    for k in fields:
        if k not in row:
            raise ValueError(f"{ctx} missing field {k!r}")
    for k in row:
        if k not in fields:
            raise ValueError(f"{ctx} unknown field {k!r}")


def _enum_ok(group: str, value: str) -> bool:
    return _validate_in_vocab(group, value)


def _all_checkpoint_enums_ok(row: dict[str, Any]) -> bool:
    if not _enum_ok("checkpoint_role", str(row["checkpoint_role"])):
        return False
    if not _enum_ok("hash_verification_status", str(row["hash_verification_status"])):
        return False
    if not _enum_ok("promotion_status", str(row["promotion_status"])):
        return False
    if not _enum_ok("checkpoint_storage_posture", str(row["checkpoint_storage_posture"])):
        return False
    if not _enum_ok("checkpoint_path_disclosure", str(row["checkpoint_path_disclosure"])):
        return False
    return True


def _receipt_group_enum_ok(kind: str, row: dict[str, Any]) -> bool:
    if kind == "interruption":
        v = str(row.get("receipt_status", ""))
        return _enum_ok("receipt_status", v)
    if kind == "resume":
        v = str(row.get("resume_verification_status", ""))
        return _enum_ok("resume_verification_status", v)
    if kind == "rollback":
        v = str(row.get("rollback_verification_status", ""))
        return _enum_ok("rollback_verification_status", v)
    return False


def _lineage_completeness(
    checkpoints: list[dict[str, Any]],
    intr: list[dict[str, Any]],
    res: list[dict[str, Any]],
    roll: list[dict[str, Any]],
) -> tuple[bool, str | None]:
    if not checkpoints:
        return False, "no_checkpoints"
    ids = {c["checkpoint_id"] for c in checkpoints}
    for c in checkpoints:
        if not _all_checkpoint_enums_ok(c):
            return False, "invalid_enum_checkpoint"
        pid = c.get("parent_checkpoint_id")
        if pid is not None and pid not in ids:
            return False, "dangling_parent_checkpoint"
    for lst, fields, knd in (
        (intr, INTERRUPTION_RECEIPT_REQUIRED_FIELDS, "interruption"),
        (res, RESUME_RECEIPT_REQUIRED_FIELDS, "resume"),
        (roll, ROLLBACK_RECEIPT_REQUIRED_FIELDS, "rollback"),
    ):
        for r in lst:
            if not _receipt_group_enum_ok(knd, r):
                return False, f"invalid_enum_{knd}"
    return True, None


def build_checkpoint_lineage_body_operator(
    data: dict[str, Any],
    *,
    environment_lock_path: Path | None,
) -> dict[str, Any]:
    prof = data.get("profile")
    if prof is not None and prof != "operator_declared":
        raise ValueError("lineage JSON profile, if set, must be 'operator_declared'")

    cps_in = data.get("checkpoints")
    if cps_in is None:
        cps_in = []
    if not isinstance(cps_in, list):
        raise ValueError("lineage JSON checkpoints must be a list")
    checkpoint_rows: list[dict[str, Any]] = [deepcopy(x) for x in cps_in]
    for i, row in enumerate(checkpoint_rows):
        _validate_checkpoint_row(row, ctx=f"checkpoints[{i}]")
        _typecheck_checkpoint_row(row, ctx=f"checkpoints[{i}]")

    intr_in = data.get("interruption_receipts")
    if intr_in is None:
        intr_in = []
    if not isinstance(intr_in, list):
        raise ValueError("interruption_receipts must be a list or null")
    intr: list[dict[str, Any]] = [deepcopy(x) for x in intr_in]
    for i, row in enumerate(intr):
        _validate_receipt_row(
            row, INTERRUPTION_RECEIPT_REQUIRED_FIELDS, f"interruption_receipts[{i}]"
        )

    res_in = data.get("resume_receipts")
    if res_in is None:
        res_in = []
    if not isinstance(res_in, list):
        raise ValueError("resume_receipts must be a list or null")
    res: list[dict[str, Any]] = [deepcopy(x) for x in res_in]
    for i, row in enumerate(res):
        _validate_receipt_row(row, RESUME_RECEIPT_REQUIRED_FIELDS, f"resume_receipts[{i}]")

    roll_in = data.get("rollback_receipts")
    if roll_in is None:
        roll_in = []
    if not isinstance(roll_in, list):
        raise ValueError("rollback_receipts must be a list or null")
    roll: list[dict[str, Any]] = [deepcopy(x) for x in roll_in]
    for i, row in enumerate(roll):
        _validate_receipt_row(row, ROLLBACK_RECEIPT_REQUIRED_FIELDS, f"rollback_receipts[{i}]")

    env_ref_top = data.get("environment_lock_reference")
    training_run_id = _as_str_or_null(data.get("training_run_id"), "training_run_id")
    ds_ref = data.get("dataset_reference")
    mc_ref = data.get("model_config_reference")
    if ds_ref is not None and not isinstance(ds_ref, (dict, str)):
        raise TypeError("dataset_reference must be object, string, or null")
    if mc_ref is not None and not isinstance(mc_ref, (dict, str)):
        raise TypeError("model_config_reference must be object, string, or null")

    env_lock_hash: str | None = None
    if environment_lock_path is not None:
        env_lock_hash = environment_lock_file_canonical_sha256(environment_lock_path)
        for row in checkpoint_rows:
            row["environment_lock_sha256"] = env_lock_hash

    env_out: dict[str, Any]
    if environment_lock_path is not None and env_lock_hash is not None:
        env_out = {
            "reference_kind": "m02_file_canonical_sha256",
            "m02_contract_id": CONTRACT_ID_M02_ENV_LOCK,
            "environment_lock_json_canonical_sha256": env_lock_hash,
            "source_file": "operator_supplied_path_not_committed",
        }
        if env_ref_top is not None:
            env_out["operator_environment_lock_reference"] = env_ref_top
    else:
        if isinstance(env_ref_top, dict):
            env_out = {**env_ref_top}
        elif env_ref_top is None:
            env_out = {
                "reference_kind": "operator_declared",
                "m02_contract_id": None,
                "environment_lock_json_canonical_sha256": None,
            }
        else:
            env_out = {
                "reference_kind": "operator_declared",
                "logical_reference": str(env_ref_top),
            }

    if training_run_id is None or training_run_id == "":
        lineage_status = LINEAGE_STATUS_OP_INCOMPLETE
    else:
        ok, _why = _lineage_completeness(checkpoint_rows, intr, res, roll)
        lineage_status = LINEAGE_STATUS_OP_COMPLETE if ok else LINEAGE_STATUS_OP_INCOMPLETE

    all_verified = bool(checkpoint_rows) and all(
        str(c.get("hash_verification_status")) == "verified_external" for c in checkpoint_rows
    )
    ev_scope = EVIDENCE_OPERATOR_DECLARED
    if lineage_status == LINEAGE_STATUS_OP_INCOMPLETE:
        ev_scope = EVIDENCE_OPERATOR_LOCAL_METADATA

    onotes = data.get("operator_notes")
    op_n = None if onotes is None else _as_str(onotes, "operator_notes")

    out: dict[str, Any] = {
        "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
        "milestone_id": MILESTONE_ID_V15_M03,
        "generated_by": EMITTER_MODULE_CHECKPOINT_LINEAGE,
        "profile": PROFILE_OPERATOR_DECLARED,
        "lineage_manifest_status": lineage_status,
        "long_gpu_run_authorized": False,
        "checkpoint_bytes_verified": all_verified,
        "resume_execution_verified": False,
        "rollback_execution_verified": False,
        "evidence_scope": ev_scope,
        "training_run_identity": {
            "training_run_id": training_run_id,
            "label": "operator_declared",
        },
        "environment_lock_reference": env_out,
        "dataset_reference": (None if ds_ref is None else deepcopy(ds_ref)),
        "model_config_reference": (None if mc_ref is None else deepcopy(mc_ref)),
        "checkpoint_lineage": checkpoint_rows,
        "interruption_receipts": intr,
        "resume_receipts": res,
        "rollback_receipts": roll,
        "lineage_manifest_status_vocabulary": list(STATUS_VOCABULARY["lineage_manifest_status"]),
        "checkpoint_role_vocabulary": list(STATUS_VOCABULARY["checkpoint_role"]),
        "promotion_status_vocabulary": list(STATUS_VOCABULARY["promotion_status"]),
        "hash_verification_status_vocabulary": list(STATUS_VOCABULARY["hash_verification_status"]),
        "resume_verification_status_vocabulary": list(
            STATUS_VOCABULARY["resume_verification_status"]
        ),
        "rollback_verification_status_vocabulary": list(
            STATUS_VOCABULARY["rollback_verification_status"]
        ),
        "receipt_status_vocabulary": list(STATUS_VOCABULARY["receipt_status"]),
        "storage_posture_vocabulary": list(STATUS_VOCABULARY["checkpoint_storage_posture"]),
        "path_disclosure_vocabulary": list(STATUS_VOCABULARY["checkpoint_path_disclosure"]),
        "required_fields": {
            "checkpoint_row": list(CHECKPOINT_ROW_REQUIRED_FIELDS),
            "interruption_receipt": list(INTERRUPTION_RECEIPT_REQUIRED_FIELDS),
            "resume_receipt": list(RESUME_RECEIPT_REQUIRED_FIELDS),
            "rollback_receipt": list(ROLLBACK_RECEIPT_REQUIRED_FIELDS),
        },
        "check_results": _check_results_operator(lineage_status, bool(checkpoint_rows)),
        "m03_verification_attestation": _m03_attestation(),
        "non_claims": list(NON_CLAIMS_V15_M03),
        "carry_forward_items": _carry_forward(),
    }
    if op_n is not None:
        out["operator_notes"] = op_n
    return out


def _check_results_operator(status: str, has_cp: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "check_id": "m03_lineage_status",
            "description": f"Operator declared lineage status resolved to {status}.",
            "status": CHECK_PASS,
        }
    ]
    if not has_cp:
        rows.append(
            {
                "check_id": "m03_checkpoint_lineage_non_empty",
                "description": "No checkpoint rows; lineage is incomplete by definition.",
                "status": CHECK_WARNING,
            }
        )
    return rows


def build_checkpoint_lineage_body(
    profile: str,
    *,
    lineage_data: dict[str, Any] | None = None,
    environment_lock_path: Path | None = None,
) -> dict[str, Any]:
    if profile == PROFILE_FIXTURE_CI:
        if environment_lock_path is not None:
            # Allow but document: fixture ignores env lock for deterministic seal
            pass
        return build_checkpoint_lineage_body_fixture()
    if profile == PROFILE_OPERATOR_DECLARED:
        if lineage_data is None:
            raise ValueError("operator_declared profile requires lineage JSON data")
        return build_checkpoint_lineage_body_operator(
            lineage_data, environment_lock_path=environment_lock_path
        )
    raise ValueError(f"unknown profile: {profile!r}")


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_CHECKPOINT_LINEAGE
    assert body["milestone_id"] == MILESTONE_ID_V15_M03
    assert set(body["promotion_status_vocabulary"]) == set(STATUS_VOCABULARY["promotion_status"])
    assert set(body["hash_verification_status_vocabulary"]) == set(
        STATUS_VOCABULARY["hash_verification_status"]
    )
    assert set(body["storage_posture_vocabulary"]) == set(
        STATUS_VOCABULARY["checkpoint_storage_posture"]
    )
    assert set(body["path_disclosure_vocabulary"]) == set(
        STATUS_VOCABULARY["checkpoint_path_disclosure"]
    )
    assert body["long_gpu_run_authorized"] is False
    assert body["resume_execution_verified"] is False
    assert body["rollback_execution_verified"] is False


def seal_checkpoint_lineage_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, _SEAL_KEY: digest}


def build_checkpoint_lineage_report(
    contract: dict[str, Any], *, emission_context: dict[str, Any] | None = None
) -> dict[str, Any]:
    digest = contract[_SEAL_KEY]
    n_intr = len(contract["interruption_receipts"])
    n_res = len(contract["resume_receipts"])
    n_roll = len(contract["rollback_receipts"])
    n_cp = len(contract["checkpoint_lineage"])
    rep: dict[str, Any] = {
        "report_version": REPORT_VERSION_CHECKPOINT_LINEAGE,
        "milestone_id": MILESTONE_ID_V15_M03,
        "contract_id": CONTRACT_ID_CHECKPOINT_LINEAGE,
        "checkpoint_lineage_manifest_sha256": digest,
        "profile": contract["profile"],
        "lineage_manifest_status": contract["lineage_manifest_status"],
        "checkpoint_count": n_cp,
        "receipt_counts": {
            "interruption": n_intr,
            "resume": n_res,
            "rollback": n_roll,
        },
        "non_claims_summary": {
            "count": len(contract["non_claims"]),
            "m03_does_not_authorize_long_run": contract["long_gpu_run_authorized"] is False,
        },
        "validation": {
            "contract_id_recognized": contract["contract_id"] == CONTRACT_ID_CHECKPOINT_LINEAGE,
            "seal_key_present": _SEAL_KEY in contract,
            "m03_never_authorizes_long_run": contract["long_gpu_run_authorized"] is False,
        },
    }
    if emission_context is not None:
        rep["emission_context"] = emission_context
    return rep


def write_checkpoint_lineage_artifacts(
    *,
    output_dir: Path,
    contract: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_CHECKPOINT_LINEAGE
    r_path = output_dir / REPORT_FILENAME_CHECKPOINT_LINEAGE
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_checkpoint_lineage_manifest(
    output_dir: Path,
    *,
    profile: str,
    lineage_path: Path | None = None,
    environment_lock_path: Path | None = None,
    emission_context: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    lineage_data: dict[str, Any] | None = None
    if lineage_path is not None:
        lineage_data = parse_lineage_json(lineage_path)

    body = build_checkpoint_lineage_body(
        profile,
        lineage_data=lineage_data,
        environment_lock_path=environment_lock_path,
    )
    if profile == PROFILE_OPERATOR_DECLARED and lineage_data is not None:
        body = redact_paths_in_value(body)
    _validate_body_invariants(body)

    sealed = seal_checkpoint_lineage_body(body)
    ctx = emission_context
    if ctx is None and profile == PROFILE_FIXTURE_CI:
        ctx = {
            "emission_mode": "fixture",
            "emission_context_note": "deterministic; no host paths; no checkpoint file reads",
        }
    rep = build_checkpoint_lineage_report(sealed, emission_context=ctx)
    c_path, r_path = write_checkpoint_lineage_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
