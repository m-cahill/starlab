"""Build, seal, and emit V15-M20 real candidate checkpoint production gate artifacts."""

# ruff: noqa: E501

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.candidate_checkpoint_evaluation_package_models import PackageStatus
from starlab.v15.checkpoint_evaluation_readiness_models import (
    CONTRACT_ID_CANDIDATE_CHECKPOINT_MANIFEST as MID_MANIFEST,
)
from starlab.v15.long_gpu_training_manifest_io import seal_campaign_receipt_body
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
    CONTRACT_VERSION,
    MILESTONE_ID_V15_M08,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
    default_m08_authorization_flags,
)
from starlab.v15.operator_evidence_preflight_models import (
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
)
from starlab.v15.real_candidate_checkpoint_production_gate_models import (
    CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE,
    DEFAULT_BLOCKED_REASON_M16_NOT_PROBE_SUCCESS,
    DEFAULT_BLOCKED_REASON_MISSING_M16,
    DEFAULT_CLAIM_FLAGS,
    EMITTER_MODULE_REAL_CANDIDATE_GATE,
    FILENAME_GATE_JSON,
    FILENAME_RUNBOOK_MD,
    MILESTONE_ID_V15_M20,
    NON_CLAIMS_V15_M20,
    PROFILE_FIXTURE_DEFAULT,
    PROFILE_OPERATOR_PREFLIGHT,
    RECOMMENDED_NEXT_FORK_FIELD,
    REPORT_FILENAME_GATE_JSON,
    REPORT_VERSION,
    RUN_TIER_T1_30_MIN,
    SCHEMA_VERSION,
    SEAL_KEY_ARTIFACT,
    STATUS_FIXTURE_NO_OPERATOR_RUN,
    STATUS_OPERATOR_PREFLIGHT_BLOCKED,
    STATUS_T1_NOT_STARTED,
    STATUS_T1_PACKAGE_BLOCKED,
    STATUS_T1_PACKAGE_READY,
    STRONGEST_ALLOWED_CLAIM_M20,
)
from starlab.v15.short_gpu_environment_models import (
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
    EVIDENCE_STATUS_PROBE_SUCCESS,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
)

_SEAL_GATE = SEAL_KEY_ARTIFACT


def sha256_hex_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_obj_sha(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"expected JSON object: {path}")
    return sha256_hex_of_canonical_json(raw)


def seal_real_candidate_gate_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != _SEAL_GATE}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[_SEAL_GATE] = digest
    return sealed


def build_gate_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL_GATE}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_real_candidate_checkpoint_production_gate_report",
        "report_version": REPORT_VERSION,
        "milestone": MILESTONE_ID_V15_M20,
        "artifact_sha256": digest,
        "seal_field": _SEAL_GATE,
        "seal_value_matches_artifact": sealed.get(_SEAL_GATE) == digest,
        "primary_filename": FILENAME_GATE_JSON,
    }


def default_claim_flags() -> dict[str, bool]:
    return dict(DEFAULT_CLAIM_FLAGS)


def base_gate_body_template(
    *,
    gate_status: str,
    operator_run_performed: bool,
    candidate_checkpoint_produced: bool,
    candidate_kind: str,
    candidate_id: str | None,
    candidate_checkpoint_sha256: str | None,
    m08_campaign_receipt_sha256: str | None,
    m18_readiness_status: str | None,
    m19_package_status: str | None,
    ready_for_future_checkpoint_evaluation: bool,
    blocked_reasons: list[str],
    allowed_next_steps: list[str],
    operator_run_duration_observed_seconds: float | None,
    artifact_notes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE,
        "milestone_id": MILESTONE_ID_V15_M20,
        "run_tier": RUN_TIER_T1_30_MIN,
        "gate_status": gate_status,
        "operator_run_performed": operator_run_performed,
        "operator_run_duration_target_minutes": 30,
        "operator_run_duration_observed_seconds": operator_run_duration_observed_seconds,
        "candidate_checkpoint_produced": candidate_checkpoint_produced,
        "candidate_kind": candidate_kind,
        "candidate_id": candidate_id,
        "candidate_checkpoint_sha256": candidate_checkpoint_sha256,
        "m08_campaign_receipt_sha256": m08_campaign_receipt_sha256,
        "m18_readiness_status": m18_readiness_status,
        "m19_package_status": m19_package_status,
        "m19_recommended_next_fork": RECOMMENDED_NEXT_FORK_FIELD,
        "ready_for_future_checkpoint_evaluation": ready_for_future_checkpoint_evaluation,
        "claim_flags": default_claim_flags(),
        "blocked_reasons": blocked_reasons,
        "allowed_next_steps": allowed_next_steps,
        "non_claims": list(NON_CLAIMS_V15_M20),
        "strongest_allowed_claim_hint": STRONGEST_ALLOWED_CLAIM_M20,
        "emitter_module": EMITTER_MODULE_REAL_CANDIDATE_GATE,
        "profile": PROFILE_FIXTURE_DEFAULT,
    }
    if artifact_notes:
        body["artifact_notes"] = artifact_notes
    return body


def emit_fixture_default(output_dir: Path) -> tuple[dict[str, Any], Path, Path, Path]:
    body = base_gate_body_template(
        gate_status=STATUS_FIXTURE_NO_OPERATOR_RUN,
        operator_run_performed=False,
        candidate_checkpoint_produced=False,
        candidate_kind="none",
        candidate_id=None,
        candidate_checkpoint_sha256=None,
        m08_campaign_receipt_sha256=None,
        m18_readiness_status=None,
        m19_package_status=None,
        ready_for_future_checkpoint_evaluation=False,
        blocked_reasons=[],
        allowed_next_steps=[],
        operator_run_duration_observed_seconds=None,
    )
    return emit_gate_artifacts(output_dir, body)


def emit_gate_artifacts(
    output_dir: Path, body_without_seal: dict[str, Any]
) -> tuple[dict[str, Any], Path, Path, Path]:
    """Seal and write gate JSON, report JSON, runbook Markdown."""

    output_dir.mkdir(parents=True, exist_ok=True)
    sealed = seal_real_candidate_gate_body(body_without_seal)
    g_path = output_dir / FILENAME_GATE_JSON
    r_path = output_dir / REPORT_FILENAME_GATE_JSON
    rb_path = output_dir / FILENAME_RUNBOOK_MD
    g_path.write_text(canonical_json_dumps(sealed) + "\n", encoding="utf-8", newline="\n")
    r_path.write_text(
        canonical_json_dumps(build_gate_report(sealed)) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rb_path.write_text(build_runbook_markdown(sealed), encoding="utf-8", newline="\n")
    return sealed, g_path, r_path, rb_path


def build_runbook_markdown(sealed: dict[str, Any]) -> str:
    gs = sealed.get("gate_status", "")
    return (
        f"# V15-M20 — Real Candidate Checkpoint Production Gate\n\n"
        f"- Milestone: `{MILESTONE_ID_V15_M20}`\n"
        f"- Contract: `{CONTRACT_ID_REAL_CANDIDATE_CHECKPOINT_PRODUCTION_GATE}`\n"
        f"- Gate status: `{gs}`\n"
        f"- Run tier: `{RUN_TIER_T1_30_MIN}` (30-minute operator-local GPU checkpoint production)\n\n"
        "See `docs/runtime/v15_real_candidate_checkpoint_production_gate_v1.md` for operator commands "
        "and non-claims.\n"
    )


def validate_m16_operator_local_probe_success(path: Path) -> tuple[bool, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return False, f"m16_json_unreadable:{e}"
    if not isinstance(raw, dict):
        return False, "m16_not_object"
    if str(raw.get("contract_id", "")) != CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE:
        return False, "m16_contract_id_mismatch"
    prof = str(raw.get("profile", ""))
    if prof == PROFILE_FIXTURE_CI:
        return False, DEFAULT_BLOCKED_REASON_MISSING_M16
    if prof != PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE:
        return False, DEFAULT_BLOCKED_REASON_M16_NOT_PROBE_SUCCESS
    ev = str(raw.get("evidence_status", ""))
    if ev != EVIDENCE_STATUS_PROBE_SUCCESS:
        return False, DEFAULT_BLOCKED_REASON_M16_NOT_PROBE_SUCCESS
    return True, "ok"


def validate_m08_manifest(path: Path) -> tuple[bool, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return False, f"m08_manifest_unreadable:{e}"
    if not isinstance(raw, dict):
        return False, "m08_not_object"
    if str(raw.get("contract_id", "")) != CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST:
        return False, "m08_contract_id_mismatch"
    return True, "ok"


def validate_m15_preflight(path: Path) -> tuple[bool, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return False, f"m15_preflight_unreadable:{e}"
    if not isinstance(raw, dict):
        return False, "m15_not_object"
    if str(raw.get("contract_id", "")) != CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT:
        return False, "m15_contract_id_mismatch"
    return True, "ok"


def emit_operator_preflight_gate(
    output_dir: Path,
    *,
    m16_path: Path,
    m08_manifest_path: Path,
    m15_preflight_path: Path,
) -> tuple[dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    blocked: list[str] = []
    ok_m16, msg_m16 = validate_m16_operator_local_probe_success(m16_path)
    if not ok_m16:
        blocked.append(msg_m16)
    ok_m08, msg_m08 = validate_m08_manifest(m08_manifest_path)
    if not ok_m08:
        blocked.append(msg_m08)
    ok_m15, msg_m15 = validate_m15_preflight(m15_preflight_path)
    if not ok_m15:
        blocked.append(msg_m15)

    if blocked:
        gate_status = STATUS_OPERATOR_PREFLIGHT_BLOCKED
        allowed: list[str] = []
    else:
        gate_status = STATUS_T1_NOT_STARTED
        allowed = ["invoke_starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate_with_guards"]

    body = base_gate_body_template(
        gate_status=gate_status,
        operator_run_performed=False,
        candidate_checkpoint_produced=False,
        candidate_kind="none",
        candidate_id=None,
        candidate_checkpoint_sha256=None,
        m08_campaign_receipt_sha256=None,
        m18_readiness_status=None,
        m19_package_status=None,
        ready_for_future_checkpoint_evaluation=False,
        blocked_reasons=blocked,
        allowed_next_steps=allowed,
        operator_run_duration_observed_seconds=None,
        artifact_notes={
            "m16_json_sha256": _json_obj_sha(m16_path),
            "m08_manifest_sha256": _json_obj_sha(m08_manifest_path),
            "m15_preflight_sha256": _json_obj_sha(m15_preflight_path),
        },
    )
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    return emit_gate_artifacts(output_dir, body)


def discover_first_pytorch_checkpoint(root: Path) -> Path | None:
    found: list[Path] = []
    if not root.is_dir():
        return None
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        suf = p.suffix.lower()
        if suf in (".pt", ".pth"):
            found.append(p)
    if not found:
        return None
    found.sort(key=lambda x: str(x.resolve()))
    return found[0]


def build_candidate_manifest_body(
    *,
    candidate_id: str,
    checkpoint_path: Path,
    checkpoint_sha256: str,
    environment_manifest_sha256: str,
    dataset_manifest_sha256: str,
    evaluation_protocol_id: str,
    produced_by_run_id: str,
    source_campaign_receipt_sha256: str,
    source_training_manifest_sha256: str,
) -> dict[str, Any]:
    display_ref = f"candidate/{checkpoint_path.name}"
    return {
        "contract_id": MID_MANIFEST,
        "candidate_id": candidate_id,
        "primary_artifact_uri_or_reference": display_ref,
        "candidate_checkpoint_sha256": checkpoint_sha256,
        "environment_manifest_sha256": environment_manifest_sha256,
        "dataset_manifest_sha256": dataset_manifest_sha256,
        "evaluation_protocol_id": evaluation_protocol_id,
        "produced_by_run_id": produced_by_run_id,
        "produced_by_milestone": MILESTONE_ID_V15_M20,
        "source_campaign_receipt_sha256": source_campaign_receipt_sha256,
        "source_training_manifest_sha256": source_training_manifest_sha256,
        "non_claims": [
            "m20_candidate_manifest_metadata_only_not_strength_proof",
            "paths_are_logical_refs_absolute_paths_remain_private",
        ],
    }


def build_operator_completed_campaign_receipt(
    *,
    campaign_id: str,
    execution_id: str,
    checkpoint_id: str | None,
    checkpoint_sha256: str | None,
    manifest_sha256_bind: str | None,
) -> dict[str, Any]:
    auth = default_m08_authorization_flags()
    auth["long_gpu_campaign_execution_performed"] = True
    auth["long_gpu_campaign_completed"] = True
    ck_count = 1 if checkpoint_sha256 else 0
    hashes = [checkpoint_sha256] if checkpoint_sha256 else []
    extra_nc = (
        "t1_30_min_operator_local_campaign_receipt_metadata",
        "not_full_long_gpu_campaign_claim_by_duration_alone",
    )
    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "milestone": MILESTONE_ID_V15_M08,
        "campaign_id": campaign_id,
        "execution_id": execution_id,
        "checkpoint_count": ck_count,
        "checkpoint_hashes": hashes,
        "final_checkpoint_id": checkpoint_id,
        "final_checkpoint_sha256": checkpoint_sha256,
        "campaign_completion_status": "completed",
        "authorization_flags": auth,
        "non_claims": list(dict.fromkeys(list(extra_nc))),
        "artifact_notes": {"tier": RUN_TIER_T1_30_MIN},
    }
    if manifest_sha256_bind:
        body["artifact_notes"]["m08_training_manifest_sha256_observed"] = manifest_sha256_bind
    return seal_campaign_receipt_body(body)


def map_m19_status_to_gate(package_status: str) -> tuple[str, bool]:
    if package_status == str(PackageStatus.EVALUATION_PACKAGE_READY):
        return STATUS_T1_PACKAGE_READY, True
    return STATUS_T1_PACKAGE_BLOCKED, False


def write_checkpoint_sha_sidecar(checkpoint_path: Path, sha_hex: str) -> Path:
    out = checkpoint_path.parent / "checkpoint_file_sha256.txt"
    out.write_text(sha_hex + "\n", encoding="utf-8", newline="\n")
    return out


def derive_m18_status_str(readiness_json: dict[str, Any]) -> str:
    return str(readiness_json.get("readiness_status", ""))


def derive_m19_status_str(package_json: dict[str, Any]) -> str:
    return str(package_json.get("package_status", ""))


__all__ = [
    "build_candidate_manifest_body",
    "build_gate_report",
    "build_operator_completed_campaign_receipt",
    "build_runbook_markdown",
    "default_claim_flags",
    "derive_m18_status_str",
    "derive_m19_status_str",
    "discover_first_pytorch_checkpoint",
    "emit_gate_artifacts",
    "emit_operator_preflight_gate",
    "map_m19_status_to_gate",
    "seal_real_candidate_gate_body",
    "sha256_hex_bytes",
    "validate_m08_manifest",
    "validate_m15_preflight",
    "validate_m16_operator_local_probe_success",
    "write_checkpoint_sha_sidecar",
]
