"""Build, seal, and write V15-M07 training run receipt + report (not long GPU campaign)."""

from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.checkpoint_lineage_models import CHECK_PASS
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.training_run_receipt_models import (
    CONTRACT_ID_TRAINING_RUN_RECEIPT,
    CONTRACT_VERSION,
    EMITTER_MODULE_TRAINING_RUN_RECEIPT,
    FILENAME_TRAINING_RUN_RECEIPT,
    FIXTURE_RUN_ID,
    MILESTONE_ID_V15_M07,
    NON_CLAIMS_V15_M07,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU,
    RECEIPT_DECLARED_JSON_TOP_LEVEL_KEYS,
    REPORT_FILENAME_TRAINING_RUN_RECEIPT,
    REPORT_VERSION_TRAINING_RUN,
    RUN_CLASS_FIXTURE_SMOKE,
    RUN_CLASS_OPERATOR_DECLARED,
    RUN_CLASS_OPERATOR_LOCAL_SHAKEDOWN,
    SEAL_KEY_TRAINING_RUN_RECEIPT,
)

SEAL = SEAL_KEY_TRAINING_RUN_RECEIPT

REDACT_TOKENS: Final[tuple[str, ...]] = (
    "REDACTED_ABSOLUTE_PATH",
    "REDACTED_CONTACT",
    "REDACTED_PII",
    "<REDACTED_ABSOLUTE_PATH>",
    "<REDACTED_CONTACT>",
    "<REDACTED_PII>",
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
        "api_token",
        "secret",
    }
)


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def default_authorization_flags() -> dict[str, bool]:
    return {
        "operator_local_execution_performed": False,
        "gpu_shakedown_performed": False,
        "short_training_run_performed": False,
        "checkpoint_write_verified": False,
        "resume_execution_verified": False,
        "rollback_execution_verified": False,
        "long_gpu_run_authorized": False,
        "strong_agent_claim_authorized": False,
        "human_benchmark_claim_authorized": False,
        "benchmark_execution_performed": False,
        "human_panel_execution_performed": False,
        "xai_review_performed": False,
        "v2_authorized": False,
    }


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
        return _EMAIL_RE.sub("<REDACTED_CONTACT>", obj)
    return obj


def redact_receipt_value(obj: Any) -> Any:
    """Redact absolute paths and obvious contact/secret-like fields in nested JSON."""
    p = redact_paths_in_value(obj)
    return _redact_contact_and_handles(p)


def _redaction_token_count(value: Any) -> int:
    s = canonical_json_dumps(value)
    return sum(s.count(t) for t in REDACT_TOKENS)


def clamp_m07_non_claim_flags(flags: Mapping[str, bool]) -> dict[str, bool]:
    """Force program-level and claim-related flags to false; keep explicit shakedown fields."""
    out = {**default_authorization_flags(), **dict(flags)}
    for k in (
        "long_gpu_run_authorized",
        "strong_agent_claim_authorized",
        "human_benchmark_claim_authorized",
        "benchmark_execution_performed",
        "human_panel_execution_performed",
        "xai_review_performed",
        "v2_authorized",
    ):
        out[k] = False
    return out


def authorization_flags_for_operator_declared(merged: Mapping[str, bool]) -> dict[str, bool]:
    """Metadata-only path: do not mark execution or shakedown as verified (always false)."""
    out = clamp_m07_non_claim_flags(merged)
    for k in (
        "operator_local_execution_performed",
        "gpu_shakedown_performed",
        "short_training_run_performed",
        "checkpoint_write_verified",
        "resume_execution_verified",
        "rollback_execution_verified",
    ):
        out[k] = False
    return out


def parse_declared_receipt_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("receipt JSON must be a single object")
    unknown = set(raw) - set(RECEIPT_DECLARED_JSON_TOP_LEVEL_KEYS)
    if unknown:
        raise ValueError(f"unknown top-level keys in declared receipt: {sorted(unknown)}")
    return raw


def _optional_sha_map(
    *,
    environment_lock_path: Path | None,
    checkpoint_lineage_path: Path | None,
    xai_evidence_path: Path | None,
    strong_agent_scorecard_path: Path | None,
    human_panel_benchmark_path: Path | None,
    training_config_path: Path | None,
    dataset_manifest_path: Path | None,
    rights_provenance_path: Path | None,
) -> dict[str, str | None]:
    out: dict[str, str | None] = {
        k: None
        for k in (
            "environment_lock_json_canonical_sha256",
            "checkpoint_lineage_json_canonical_sha256",
            "xai_evidence_json_canonical_sha256",
            "strong_agent_scorecard_json_canonical_sha256",
            "human_panel_benchmark_json_canonical_sha256",
            "training_config_json_canonical_sha256",
            "dataset_manifest_json_canonical_sha256",
            "rights_provenance_json_canonical_sha256",
        )
    }
    if environment_lock_path is not None:
        out["environment_lock_json_canonical_sha256"] = environment_lock_file_canonical_sha256(
            environment_lock_path
        )
    if checkpoint_lineage_path is not None:
        out["checkpoint_lineage_json_canonical_sha256"] = _json_file_canonical_sha256(
            checkpoint_lineage_path
        )
    if xai_evidence_path is not None:
        out["xai_evidence_json_canonical_sha256"] = _json_file_canonical_sha256(xai_evidence_path)
    if strong_agent_scorecard_path is not None:
        out["strong_agent_scorecard_json_canonical_sha256"] = _json_file_canonical_sha256(
            strong_agent_scorecard_path
        )
    if human_panel_benchmark_path is not None:
        out["human_panel_benchmark_json_canonical_sha256"] = _json_file_canonical_sha256(
            human_panel_benchmark_path
        )
    if training_config_path is not None:
        out["training_config_json_canonical_sha256"] = _json_file_canonical_sha256(
            training_config_path
        )
    if dataset_manifest_path is not None:
        out["dataset_manifest_json_canonical_sha256"] = _json_file_canonical_sha256(
            dataset_manifest_path
        )
    if rights_provenance_path is not None:
        out["rights_provenance_json_canonical_sha256"] = _json_file_canonical_sha256(
            rights_provenance_path
        )
    return out


def build_training_run_receipt_body_fixture(
    *,
    optional_sha: dict[str, str | None] | None = None,
) -> dict[str, Any]:
    """Deterministic fixture body (no PyTorch; no real checkpoint I/O)."""
    default_opt: dict[str, str | None] = {
        k: None
        for k in (
            "environment_lock_json_canonical_sha256",
            "checkpoint_lineage_json_canonical_sha256",
            "xai_evidence_json_canonical_sha256",
            "strong_agent_scorecard_json_canonical_sha256",
            "human_panel_benchmark_json_canonical_sha256",
            "training_config_json_canonical_sha256",
            "dataset_manifest_json_canonical_sha256",
            "rights_provenance_json_canonical_sha256",
        )
    }
    if optional_sha:
        default_opt.update(optional_sha)
    opt = default_opt
    auth = default_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_TRAINING_RUN_RECEIPT,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN,
        "milestone": MILESTONE_ID_V15_M07,
        "created_by": EMITTER_MODULE_TRAINING_RUN_RECEIPT,
        "run_id": FIXTURE_RUN_ID,
        "run_class": RUN_CLASS_FIXTURE_SMOKE,
        "profile": PROFILE_FIXTURE_CI,
        "execution_scope": "ci_fixture",
        "receipt_status": "fixture_ci",
        "repo_identity": {
            "git_branch": "fixture:deterministic",
            "git_sha256_placeholder": PLACEHOLDER_SHA256,
            "narrative": "Fixture repo identity; replace with real git metadata in operator paths.",
        },
        "environment_binding": {
            "posture": "fixture_ci",
            "long_gpu_environment_lock_bound": False,
            "notes": "M07 fixture does not run M02 environment probe in CI.",
        },
        "training_config_binding": {
            "logical_config_id": "fixture:m07_synthetic_config_placeholder",
            "config_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "dataset_binding": {
            "logical_dataset_id": "fixture:m07_synthetic_dataset_placeholder",
            "dataset_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "rights_binding": {
            "posture": "synthetic_fixture_only",
            "rights_provenance_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "checkpoint_lineage_binding": {
            "checkpoint_lineage_manifest_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "prior_protocol_bindings": {
            "narrative": (
                "Optional SHA bindings for M04/M05/M06 live in optional_bindings (JSON files only)."
            ),
        },
        "device_probe": {
            "status": "not_applicable_fixture",
            "torch_version": None,
            "cuda_available": None,
        },
        "sc2_probe": {
            "status": "not_run",
            "notes": "M07 default fixture does not launch SC2.",
        },
        "disk_probe": {
            "status": "not_evaluated",
        },
        "trainer_identity": {
            "trainer_kind": "none_fixture",
            "label": "No trainer executed in fixture_ci.",
        },
        "training_smoke": {
            "fixture_only": True,
            "synthetic_shakedown_label": "not_run",
            "max_steps": 0,
            "device_requested": "none",
        },
        "checkpoint_write_receipt": {
            "checkpoint_write_verification_status": "not_executed",
            "checkpoint_path_logical": None,
            "checkpoint_sha256": None,
        },
        "resume_receipt": {
            "resume_verification_status": "not_executed",
            "notes": "M07 fixture does not execute trainer resume.",
        },
        "rollback_receipt": {
            "rollback_verification_status": "not_executed",
            "notes": "M07 fixture does not execute rollback/promotion runtime.",
        },
        "artifact_integrity": {
            "checkpoint_blob_included": False,
            "receipt_artifact_role": "v15_training_run_receipt",
        },
        "provenance_gaps": [
            "No operator hardware probe in fixture_ci.",
            "No real checkpoint bytes hashed in fixture path.",
        ],
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator_declared": "redact_paths_contacts_secrets",
        },
        "optional_bindings": {k: opt.get(k) for k in sorted(opt.keys())},
        "operator_notes": None,
        "non_claims": list(NON_CLAIMS_V15_M07),
        "authorization_flags": auth,
        "m07_verification_attestation": (
            "V15-M07 fixture proves receipt/schema wiring only. It does not execute GPU shakedown, "
            "long training, or benchmarks."
        ),
        "check_results": [
            {
                "check_id": "m07_receipt_shape",
                "description": (
                    "Fixture body includes required v1.5 M07 training-run receipt fields."
                ),
                "status": CHECK_PASS,
            },
            {
                "check_id": "m07_no_long_gpu",
                "description": "long_gpu_run_authorized and claim flags are false in fixture.",
                "status": CHECK_PASS,
            },
        ],
    }


def build_training_run_receipt_body_operator_declared(
    data: dict[str, Any],
    *,
    optional_sha: dict[str, str | None],
) -> dict[str, Any]:
    body = build_training_run_receipt_body_fixture(optional_sha=optional_sha)
    rid = str(data.get("run_id") or "").strip() or f"op_declared:{uuid.uuid4().hex[:12]}"
    body["run_id"] = rid
    body["run_class"] = str(data.get("run_class") or RUN_CLASS_OPERATOR_DECLARED)
    body["profile"] = PROFILE_OPERATOR_DECLARED
    body["receipt_status"] = "operator_declared"
    body["execution_scope"] = str(data.get("execution_scope") or "operator_declared")
    ex_auth = data.get("authorization_flags")
    if isinstance(ex_auth, dict):
        merged: dict[str, bool] = {}
        for k, v in ex_auth.items():
            if isinstance(v, bool):
                merged[str(k)] = v
        body["authorization_flags"] = authorization_flags_for_operator_declared(merged)
    else:
        body["authorization_flags"] = authorization_flags_for_operator_declared({})
    for key in (
        "repo_identity",
        "device_probe",
        "training_smoke",
        "checkpoint_write_receipt",
        "training_config_binding",
        "dataset_binding",
        "rights_binding",
    ):
        if key in data and isinstance(data[key], (dict, type(None))):
            if data[key] is not None and isinstance(data[key], dict):
                body[key] = {**(body.get(key) or {}), **data[key]}
    if "operator_notes" in data and data["operator_notes"] is not None:
        body["operator_notes"] = str(data["operator_notes"])
    if isinstance(data.get("non_claims"), list):
        extra = [str(x) for x in data["non_claims"]]
        body["non_claims"] = list(NON_CLAIMS_V15_M07) + extra
    if isinstance(data.get("optional_bindings"), dict):
        ob = data["optional_bindings"]
        for k, v in ob.items():
            if k in body["optional_bindings"]:
                body["optional_bindings"][k] = v
    return body


def _run_synthetic_operator_shakedown(
    *,
    run_dir: Path,
    run_id: str,
    max_steps: int,
    device_str: str,
) -> dict[str, Any]:
    """Tiny synthetic training loop; imports torch only when called. Not model-quality evidence."""
    try:
        import torch
    except ImportError as e:
        raise RuntimeError(
            "PyTorch is required for --profile operator_local_short_gpu. "
            "Install torch in the operator environment, or use fixture_ci / operator_declared."
        ) from e

    if max_steps < 1:
        raise ValueError("max_steps must be >= 1 for operator_local_short_gpu")

    if device_str == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA requested but not available; refusing to emit fake GPU shakedown evidence."
            )
        device: Any = torch.device("cuda")
        gpu_name = torch.cuda.get_device_name(0) if torch.cuda.device_count() else ""
    else:
        device = torch.device("cpu")
        gpu_name = ""

    run_dir.mkdir(parents=True, exist_ok=True)
    ck_path = run_dir / "m07_synthetic_shakedown.pt"

    torch.manual_seed(42)
    if device_str == "cuda":
        torch.cuda.manual_seed_all(42)

    model = torch.nn.Linear(4, 2)
    model = model.to(device)
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    x = torch.randn(8, 4, device=device)
    y = torch.randn(8, 2, device=device)
    for _ in range(max_steps):
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(model(x), y)
        loss.backward()  # type: ignore[no-untyped-call]
        opt.step()
    # Save checkpoint
    torch.save({"model_state_dict": model.state_dict(), "step": max_steps}, ck_path)
    ck_hash = sha256_file(ck_path)
    # Resume: load and one more step
    blob = torch.load(ck_path, map_location=device, weights_only=False)
    model.load_state_dict(blob["model_state_dict"])
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    opt.zero_grad()
    loss2 = torch.nn.functional.mse_loss(model(x), y)
    loss2.backward()  # type: ignore[no-untyped-call]
    opt.step()
    resume_ok = bool(loss2.detach().isfinite().item())
    # Rollback: two loads from the same file should match (M07 wiring only, not M09)
    b1 = torch.load(ck_path, map_location=device, weights_only=False)
    b2 = torch.load(ck_path, map_location=device, weights_only=False)
    sd1 = b1.get("model_state_dict", b1) if isinstance(b1, dict) else b1
    sd2 = b2.get("model_state_dict", b2) if isinstance(b2, dict) else b2
    assert isinstance(sd1, dict) and isinstance(sd2, dict)
    rollback_ok = all(torch.equal(sd1[k], sd2[k]) for k in sd1 if k in sd2)
    return {
        "device_probe": {
            "status": "executed",
            "torch_version": torch.__version__,
            "cuda_available": bool(torch.cuda.is_available()),
            "device_requested": device_str,
            "device_resolved": str(device),
            "gpu_device_name_sanitized": gpu_name
            if (device_str == "cuda" and gpu_name and "/" not in gpu_name)
            else (gpu_name[:64] if gpu_name else None),
        },
        "trainer_identity": {
            "trainer_kind": "m07_synthetic_isolated",
            "module": "starlab.v15.training_run_receipt_io._run_synthetic_operator_shakedown",
            "label": "M07 synthetic trainer — shakedown wiring only, not gameplay or model quality",
        },
        "training_smoke": {
            "synthetic_shakedown_label": "m07_synthetic_mlp_regression_toy",
            "max_steps": max_steps,
            "device_requested": device_str,
            "loss_last": float(loss2.detach().cpu().item()),
        },
        "checkpoint_write_receipt": {
            "checkpoint_write_verification_status": "verified_synthetic_write",
            "checkpoint_path_logical": "m07_synthetic_shakedown.pt",
            "checkpoint_sha256": ck_hash,
            "notes": (
                "Checkpoint is a small synthetic .pt under operator output root (not for commits)."
            ),
        },
        "resume_receipt": {
            "resume_verification_status": "verified_synthetic_one_step" if resume_ok else "failed",
            "notes": "Loaded saved state_dict and performed one additional optimizer step.",
        },
        "rollback_receipt": {
            "rollback_verification_status": "verified_synthetic_reload"
            if rollback_ok
            else "inconclusive",
            "notes": (
                "Reloaded checkpoint from disk to confirm deterministic reload "
                "(not M09 promotion rollback)."
            ),
        },
        "artifact_integrity": {
            "checkpoint_blob_included": True,
            "checkpoint_sha256": ck_hash,
        },
        "provenance_gaps": [],
        "run_id": run_id,
        "authorization_flags_extra": {
            "operator_local_execution_performed": True,
            "short_training_run_performed": True,
            "checkpoint_write_verified": True,
            "resume_execution_verified": resume_ok,
            "rollback_execution_verified": rollback_ok,
            "gpu_shakedown_performed": bool(device_str == "cuda" and torch.cuda.is_available()),
        },
    }


def build_training_run_receipt_body_operator_local(
    *,
    optional_sha: dict[str, str | None],
    shakedown_fragment: dict[str, Any],
) -> dict[str, Any]:
    body = build_training_run_receipt_body_fixture(optional_sha=optional_sha)
    rid = str(shakedown_fragment.get("run_id") or "m07_operator")
    body["run_id"] = rid
    body["run_class"] = RUN_CLASS_OPERATOR_LOCAL_SHAKEDOWN
    body["profile"] = PROFILE_OPERATOR_LOCAL_SHORT_GPU
    body["receipt_status"] = "operator_local_short_gpu"
    body["execution_scope"] = "operator_local"
    auth = default_authorization_flags()
    extra = shakedown_fragment.get("authorization_flags_extra")
    if isinstance(extra, dict):
        for k, v in extra.items():
            if k in auth and isinstance(v, bool):
                auth[k] = v
    body["authorization_flags"] = clamp_m07_non_claim_flags(auth)
    for key in (
        "device_probe",
        "trainer_identity",
        "training_smoke",
        "checkpoint_write_receipt",
        "resume_receipt",
        "rollback_receipt",
    ):
        if key in shakedown_fragment:
            body[key] = shakedown_fragment[key]
    if "artifact_integrity" in shakedown_fragment:
        body["artifact_integrity"] = {
            **body["artifact_integrity"],
            **shakedown_fragment["artifact_integrity"],
        }
    prov = shakedown_fragment.get("provenance_gaps")
    if isinstance(prov, list):
        body["provenance_gaps"] = list(
            body.get("provenance_gaps", []),
        ) + [str(x) for x in prov]
    body["non_claims"] = list(NON_CLAIMS_V15_M07) + [
        (
            "Operator-local M07 shakedown uses an isolated synthetic trainer; "
            "not STARLAB gameplay training."
        )
    ]
    return body


def _validate_body_invariants(body: dict[str, Any]) -> None:
    assert body["contract_id"] == CONTRACT_ID_TRAINING_RUN_RECEIPT
    assert body["profile_id"] == PROFILE_ID_TRAINING_SMOKE_SHORT_GPU_SHAKEDOWN
    assert body["milestone"] == MILESTONE_ID_V15_M07
    af = body["authorization_flags"]
    if not isinstance(af, dict):
        raise TypeError("authorization_flags must be a dict")
    for k in (
        "long_gpu_run_authorized",
        "strong_agent_claim_authorized",
        "human_benchmark_claim_authorized",
        "benchmark_execution_performed",
        "human_panel_execution_performed",
        "xai_review_performed",
        "v2_authorized",
    ):
        if af.get(k) is not False:
            raise ValueError(f"M07 policy: {k} must be false in emitted receipt")


def seal_training_run_receipt_body(body_no_seal: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_no_seal)
    return {**body_no_seal, SEAL: digest}


def build_training_run_receipt_report(
    contract: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    digest = contract[SEAL]
    opt = contract.get("optional_bindings", {})
    opt_keys: list[str] = []
    if isinstance(opt, dict):
        opt_keys = sorted(k for k, v in opt.items() if v)
    return {
        "report_version": REPORT_VERSION_TRAINING_RUN,
        "milestone": MILESTONE_ID_V15_M07,
        "contract_id": contract["contract_id"],
        "profile_id": contract["profile_id"],
        "profile": contract["profile"],
        "run_id": contract["run_id"],
        "run_class": contract.get("run_class", ""),
        "artifact_sha256": digest,
        "redaction_count": redaction_count,
        "optional_binding_keys": opt_keys,
        "operator_local_shakedown_status": contract.get("operator_local_shakedown_status", "n/a"),
    }


def write_training_run_receipt_artifacts(
    *, output_dir: Path, contract: dict[str, Any], report: dict[str, Any]
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_TRAINING_RUN_RECEIPT
    r_path = output_dir / REPORT_FILENAME_TRAINING_RUN_RECEIPT
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_v15_training_run_receipt(
    output_dir: Path,
    *,
    profile: str,
    allow_operator_local: bool = False,
    declared_receipt_path: Path | None = None,
    run_id: str | None = None,
    max_steps: int = 10,
    device: str = "cuda",
    environment_lock_path: Path | None = None,
    checkpoint_lineage_path: Path | None = None,
    xai_evidence_path: Path | None = None,
    strong_agent_scorecard_path: Path | None = None,
    human_panel_benchmark_path: Path | None = None,
    training_config_path: Path | None = None,
    dataset_manifest_path: Path | None = None,
    rights_provenance_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    opt_sha = _optional_sha_map(
        environment_lock_path=environment_lock_path,
        checkpoint_lineage_path=checkpoint_lineage_path,
        xai_evidence_path=xai_evidence_path,
        strong_agent_scorecard_path=strong_agent_scorecard_path,
        human_panel_benchmark_path=human_panel_benchmark_path,
        training_config_path=training_config_path,
        dataset_manifest_path=dataset_manifest_path,
        rights_provenance_path=rights_provenance_path,
    )

    redact_count = 0
    olocal_status: str = "n/a"
    if profile == PROFILE_FIXTURE_CI:
        body = build_training_run_receipt_body_fixture(optional_sha=opt_sha)
    elif profile == PROFILE_OPERATOR_DECLARED:
        if declared_receipt_path is None:
            raise ValueError("operator_declared requires --receipt-json")
        data = parse_declared_receipt_json(declared_receipt_path)
        body = build_training_run_receipt_body_operator_declared(data, optional_sha=opt_sha)
        body = redact_receipt_value(body)
        redact_count = _redaction_token_count(body)
    elif profile == PROFILE_OPERATOR_LOCAL_SHORT_GPU:
        if not allow_operator_local:
            raise ValueError(
                "operator_local_short_gpu requires --allow-operator-local-execution "
                "(M07 is explicit, non-default)"
            )
        rid = (run_id or f"m07_{int(time.time())}").strip()
        sh = _run_synthetic_operator_shakedown(
            run_dir=output_dir, run_id=rid, max_steps=max_steps, device_str=device
        )
        olocal_status = "operator_local_short_gpu_completed"
        body = build_training_run_receipt_body_operator_local(
            optional_sha=opt_sha, shakedown_fragment=sh
        )
        body = redact_receipt_value(body)
        redact_count = _redaction_token_count(body)
        body["operator_local_shakedown_status"] = olocal_status
    else:
        raise ValueError(f"unknown profile: {profile!r}")

    if profile == PROFILE_FIXTURE_CI:
        body = redact_receipt_value(body)  # identity pass for fixture, keeps pipeline uniform
        redact_count = _redaction_token_count(body)

    if profile == PROFILE_FIXTURE_CI:
        body["operator_local_shakedown_status"] = "fixture_ci"
    elif profile == PROFILE_OPERATOR_DECLARED:
        body["operator_local_shakedown_status"] = "operator_declared_only"

    _validate_body_invariants(body)
    sealed = seal_training_run_receipt_body(body)
    rep = build_training_run_receipt_report(sealed, redaction_count=redact_count)
    c_path, r_path = write_training_run_receipt_artifacts(
        output_dir=output_dir, contract=sealed, report=rep
    )
    return sealed, rep, redact_count, c_path, r_path
