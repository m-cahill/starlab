"""Build, seal, and write V15-M16 short GPU / environment evidence JSON + report + checklist."""

# ruff: noqa: E501

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.environment_lock_models import CONTRACT_ID_LONG_GPU_ENV
from starlab.v15.long_gpu_training_manifest_models import CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST
from starlab.v15.operator_evidence_preflight_models import (
    ALL_PREFLIGHT_GATE_IDS,
    ALL_SEQUENCE_IDS,
    CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
    STATUS_OPERATOR_EVIDENCE_NOT_STARTED,
)
from starlab.v15.short_gpu_environment_models import (
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
    EMITTER_MODULE_SHORT_GPU_ENVIRONMENT,
    EVIDENCE_STATUS_FIXTURE_ONLY,
    EVIDENCE_STATUS_OPERATOR_DECLARED,
    EVIDENCE_STATUS_PROBE_BLOCKED,
    EVIDENCE_STATUS_PROBE_SUCCESS,
    FILENAME_SHORT_GPU_ENV_CHECKLIST_MD,
    FILENAME_SHORT_GPU_ENV_EVIDENCE,
    FORBIDDEN_CHECKLIST_SUBSTRINGS,
    G0_M15,
    G1_REPO,
    G2_PYTHON,
    G3_DEPS,
    G4_TORCH,
    G5_CUDA,
    G6_GPU,
    G7_PROBE,
    G8_SC2,
    G9_DISK,
    G10_REDACT,
    G11_REGISTER,
    G12_M17,
    GATE_POSTURE_NOT_EVALUATED,
    GATE_POSTURE_PASS,
    GATE_POSTURE_PASS_FIXTURE,
    GATE_POSTURE_PASS_OR_NA,
    M17_BLOCKED_CUDA,
    M17_BLOCKED_PENDING,
    M17_READY_PLANNING,
    M17_READY_PREFLIGHT,
    MILESTONE_ID_V15_M16,
    NON_CLAIMS_V15_M16,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
    REGISTER_TOUCHPOINT_PATHS,
    REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE,
    REPORT_VERSION_SHORT_GPU_ENV,
    SEAL_KEY_ARTIFACT,
    SHORT_GPU_PROBE_BLOCKED_CUDA,
    SHORT_GPU_PROBE_BLOCKED_TORCH,
    SHORT_GPU_PROBE_FAILED,
    SHORT_GPU_PROBE_NOT_RUN,
    SHORT_GPU_PROBE_SUCCESS,
)
from starlab.v15.training_run_receipt_models import CONTRACT_ID_TRAINING_RUN_RECEIPT

_SEAL = SEAL_KEY_ARTIFACT


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def parse_m02_environment_lock(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M02 environment lock JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_LONG_GPU_ENV:
        raise ValueError(
            f"M02 binding: contract_id must be {CONTRACT_ID_LONG_GPU_ENV!r} (got {cid!r})"
        )
    return raw


def parse_m07_training_run_receipt(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M07 receipt JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_TRAINING_RUN_RECEIPT:
        raise ValueError(
            f"M07 binding: contract_id must be {CONTRACT_ID_TRAINING_RUN_RECEIPT!r} (got {cid!r})"
        )
    return raw


def parse_m08_long_gpu_manifest(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M08 manifest JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST:
        raise ValueError(
            f"M08 binding: contract_id must be {CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST!r} "
            f"(got {cid!r})"
        )
    return raw


def parse_m15_operator_evidence_preflight(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M15 preflight JSON must be a single object")
    cid = str(raw.get("contract_id", ""))
    if cid != CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT:
        raise ValueError(
            "M15 binding: contract_id must be "
            f"{CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT!r} (got {cid!r})"
        )
    st = str(raw.get("operator_evidence_collection_status", ""))
    if st != STATUS_OPERATOR_EVIDENCE_NOT_STARTED:
        raise ValueError(
            "M15 binding: operator_evidence_collection_status must be "
            f"{STATUS_OPERATOR_EVIDENCE_NOT_STARTED!r} for honest M16 binding (got {st!r})"
        )
    if raw.get("v2_authorized") is True:
        raise ValueError("M15 binding: v2_authorized must not be true for M16 binding")
    if raw.get("v2_recharter_authorized") is True:
        raise ValueError("M15 binding: v2_recharter_authorized must not be true for M16 binding")
    gates = raw.get("preflight_gates")
    if not isinstance(gates, list):
        raise ValueError("M15 binding: preflight_gates must be a list")
    got_g = {str(x.get("gate_id", "")) for x in gates if isinstance(x, dict)}
    missing_g = set(ALL_PREFLIGHT_GATE_IDS) - got_g
    if missing_g:
        raise ValueError(f"M15 binding: missing preflight gate_id entries: {sorted(missing_g)}")
    seq = raw.get("evidence_sequence")
    if not isinstance(seq, list):
        raise ValueError("M15 binding: evidence_sequence must be a list")
    got_s = {str(x.get("sequence_id", "")) for x in seq if isinstance(x, dict)}
    missing_s = set(ALL_SEQUENCE_IDS) - got_s
    if missing_s:
        raise ValueError(f"M15 binding: missing evidence_sequence sequence_id: {sorted(missing_s)}")
    return raw


def _m02_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "contract_id_expected": CONTRACT_ID_LONG_GPU_ENV,
        "m02_environment_lock_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply --m02-environment-lock-json to bind v15_long_gpu_environment_lock.json.",
    }


def _m07_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "contract_id_expected": CONTRACT_ID_TRAINING_RUN_RECEIPT,
        "m07_training_run_receipt_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply --m07-training-run-receipt-json to bind v15_training_run_receipt.json.",
    }


def _m08_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "contract_id_expected": CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
        "m08_long_gpu_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        "m08_manifest_role_readonly": "implementation_preflight_manifest_tooling",
        "note": "Supply --m08-long-gpu-manifest-json to bind v15_long_gpu_training_manifest.json; "
        "M08 does not assert a completed long GPU campaign without operator receipts.",
    }


def _m15_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "contract_id_expected": CONTRACT_ID_OPERATOR_EVIDENCE_COLLECTION_PREFLIGHT,
        "m15_operator_evidence_preflight_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply --m15-preflight-json to bind v15_operator_evidence_collection_preflight.json.",
    }


def _m02_binding_file(path: Path) -> dict[str, Any]:
    m02 = parse_m02_environment_lock(path)
    sha = _json_file_canonical_sha256(path)
    return {
        "binding_mode": "file_bound",
        "m02_environment_lock_json_canonical_sha256": sha,
        "m02_contract_id_readonly": str(m02.get("contract_id", "")),
        "note": "M02 does not authorize a long GPU run; SHA binding only.",
    }


def _m07_binding_file(path: Path) -> dict[str, Any]:
    m07 = parse_m07_training_run_receipt(path)
    sha = _json_file_canonical_sha256(path)
    prof = str(m07.get("profile", ""))
    return {
        "binding_mode": "file_bound",
        "m07_training_run_receipt_json_canonical_sha256": sha,
        "m07_contract_id_readonly": str(m07.get("contract_id", "")),
        "m07_emit_profile_readonly": prof,
        "m07_receipt_class_readonly": prof,
        "note": "M07 is a training smoke / shakedown receipt surface; do not reinterpret as M08 campaign.",
    }


def _m08_binding_file(path: Path) -> dict[str, Any]:
    m08 = parse_m08_long_gpu_manifest(path)
    sha = _json_file_canonical_sha256(path)
    return {
        "binding_mode": "file_bound",
        "m08_long_gpu_manifest_json_canonical_sha256": sha,
        "m08_contract_id_readonly": str(m08.get("contract_id", "")),
        "m08_manifest_role_readonly": "implementation_preflight_manifest_tooling",
        "note": "M08 manifest is preflight / tooling unless paired with valid operator campaign receipts.",
    }


def _m15_binding_file(path: Path) -> dict[str, Any]:
    m15 = parse_m15_operator_evidence_preflight(path)
    sha = _json_file_canonical_sha256(path)
    return {
        "binding_mode": "file_bound",
        "m15_operator_evidence_preflight_json_canonical_sha256": sha,
        "m15_contract_id_readonly": str(m15.get("contract_id", "")),
        "m15_operator_evidence_collection_status_readonly": str(
            m15.get("operator_evidence_collection_status", "")
        ),
    }


def _gate_row(
    gate_id: str,
    name: str,
    default_status: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "name": name,
        "default_status": default_status,
        "notes": notes,
    }


def _build_readiness_gates(
    *,
    m15_bound: bool,
    probe_ran: bool,
    probe_ok: bool,
    fixture_mode: bool,
) -> list[dict[str, Any]]:
    fx, ne, ps, pona = (
        GATE_POSTURE_PASS_FIXTURE,
        GATE_POSTURE_NOT_EVALUATED,
        GATE_POSTURE_PASS,
        (GATE_POSTURE_PASS_OR_NA),
    )
    g0 = fx if m15_bound else fx
    g0_note = (
        "M15 preflight JSON bound by canonical SHA-256."
        if m15_bound
        else "Fixture: bind M15 preflight with --m15-preflight-json when available."
    )
    g7_status = pona
    if probe_ran and probe_ok:
        g7_note = "Short GPU probe executed under dual CLI guards; bounded by --max-steps."
    elif probe_ran and not probe_ok:
        g7_note = "Probe attempted; honest blocked or failed posture recorded."
    else:
        g7_note = (
            "No operator-local probe in this emit; not applicable unless dual-guarded probe runs."
        )

    return [
        _gate_row(G0_M15, "M15 preflight bound or fixture placeholder used", g0, g0_note),
        _gate_row(
            G1_REPO,
            "Repo identity / branch / commit posture recorded",
            fx,
            "Fixture uses stable placeholders; operator paths are private by default.",
        ),
        _gate_row(
            G2_PYTHON,
            "Python version and platform posture recorded",
            fx,
            "Fixture records synthetic python/platform labels for CI determinism.",
        ),
        _gate_row(
            G3_DEPS,
            "Dependency lock/hash posture recorded",
            fx,
            "Fixture dependency fingerprint placeholder; real lock binds are operator-local.",
        ),
        _gate_row(
            G4_TORCH,
            "PyTorch import / version posture recorded",
            ne if fixture_mode else fx,
            "Not evaluated in default fixture CI; operator-local probe may record torch.",
        ),
        _gate_row(
            G5_CUDA,
            "CUDA availability posture recorded",
            ne if fixture_mode else fx,
            "Not evaluated in default fixture CI; operator-local probe may record CUDA.",
        ),
        _gate_row(
            G6_GPU,
            "GPU name / memory summary recorded when available",
            ne if fixture_mode else fx,
            "Fixture does not assume GPU; operator probe may record device summary.",
        ),
        _gate_row(
            G7_PROBE,
            "Short GPU probe bounded and explicitly authorized when run",
            g7_status,
            g7_note,
        ),
        _gate_row(
            G8_SC2,
            "SC2 client/map posture declared or explicitly not evaluated",
            ne,
            "M16 does not launch SC2; declare posture only.",
        ),
        _gate_row(
            G9_DISK,
            "Output / storage posture declared or fixture placeholder used",
            fx,
            "Fixture output-root policy placeholder; absolute paths stay private.",
        ),
        _gate_row(
            G10_REDACT,
            "Private path redaction / non-commit rules recorded",
            ps,
            "Absolute paths and operator trees must not be committed; use registers.",
        ),
        _gate_row(
            G11_REGISTER,
            "Rights and asset register touchpoints declared",
            ps,
            "Register list references public docs; no new claim-critical rows in M16 by default.",
        ),
        _gate_row(
            G12_M17,
            "Conservative M17 opening recommendation generated",
            ps,
            "Recommendation is planning/opening only; M17 owns long-run campaign evidence.",
        ),
    ]


def _public_private_boundary() -> dict[str, Any]:
    return {
        "public_safe": [
            "contract_ids",
            "logical_artifact_names",
            "sha256_bindings",
            "python_package_versions_redacted",
            "gate_ids_and_statuses",
            "non_claims",
            "sanitized_gpu_model_strings_when_intentionally_public",
        ],
        "private_local_only_by_default": [
            "absolute_paths",
            "sc2_install_path",
            "map_pack_paths",
            "local_output_root",
            "machine_hostname",
            "usernames",
            "raw_cuda_logs_with_paths",
            "model_weights",
            "checkpoint_blobs",
            "replay_files",
            "videos",
            "human_participant_data",
            "private_operator_notes",
        ],
    }


def _fixture_repo_identity() -> dict[str, Any]:
    return {
        "repo_label": "fixture_ci",
        "branch": "fixture_branch",
        "commit_sha": PLACEHOLDER_SHA256,
        "note": "Fixture placeholders; operator emits may override via declared JSON or git subprocess.",
    }


def _fixture_environment_summary() -> dict[str, Any]:
    return {
        "repository_identity": _fixture_repo_identity(),
        "python_version": "fixture_python_3_x",
        "platform": "fixture_platform",
        "dependency_lock_posture": "fixture_lock_placeholder",
        "dependency_fingerprint": PLACEHOLDER_SHA256,
    }


def _fixture_gpu_summary() -> dict[str, Any]:
    return {"posture": "not_evaluated_fixture_ci", "gpu_name": "", "memory_summary": ""}


def _fixture_torch_cuda_summary() -> dict[str, Any]:
    return {
        "torch_imported": False,
        "torch_version": "not_imported_fixture_ci",
        "cuda_available": False,
        "cuda_version": "not_evaluated",
    }


def _fixture_sc2_summary() -> dict[str, Any]:
    return {
        "sc2_client_posture": "not_evaluated",
        "map_pool_posture": "not_evaluated",
        "note": "M16 does not launch or introspect SC2 in fixture mode.",
    }


def _fixture_disk_summary() -> dict[str, Any]:
    return {
        "output_root_policy": "local_out_or_operator_declared",
        "absolute_paths_recorded": False,
    }


def _operator_notes_redaction_default() -> dict[str, Any]:
    return {
        "redaction_policy": "path_like_strings_redacted_in_declared_json",
        "private_notes_committed": False,
    }


def _try_git_repo_identity() -> dict[str, Any] | None:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        br = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if sha.returncode != 0 or br.returncode != 0:
            return None
        return {
            "repo_label": "git_working_copy",
            "branch": br.stdout.strip(),
            "commit_sha": sha.stdout.strip(),
            "note": "Captured via git rev-parse when available; may be synthetic in CI.",
        }
    except OSError:
        return None


def run_bounded_short_gpu_probe(
    *,
    device: str,
    max_steps: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str, str, bool]:
    """Run a minimal torch probe; return (torch_cuda_summary, gpu_summary, probe_steps, result, m17_rec, ok)."""
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")
    dev = device.lower().strip()
    if dev not in ("cuda", "cpu"):
        raise ValueError("device must be cuda or cpu")

    try:
        import torch  # noqa: PLC0415
    except ImportError:
        summary = {
            "torch_imported": False,
            "torch_version": "import_failed",
            "cuda_available": False,
            "cuda_version": "not_available",
        }
        gpu = {"posture": "torch_unavailable", "gpu_name": "", "memory_summary": ""}
        return (
            summary,
            gpu,
            {"steps_requested": max_steps, "steps_executed": 0, "device_requested": dev},
            SHORT_GPU_PROBE_BLOCKED_TORCH,
            M17_BLOCKED_PENDING,
            False,
        )

    cuda_avail = bool(torch.cuda.is_available())
    cuda_ver = ""
    if cuda_avail and torch.version.cuda:
        cuda_ver = str(torch.version.cuda)
    summary = {
        "torch_imported": True,
        "torch_version": str(torch.__version__),
        "cuda_available": cuda_avail,
        "cuda_version": cuda_ver or ("not_available" if not cuda_avail else ""),
    }

    if dev == "cuda" and not cuda_avail:
        gpu = {"posture": "cuda_unavailable", "gpu_name": "", "memory_summary": ""}
        return (
            summary,
            gpu,
            {"steps_requested": max_steps, "steps_executed": 0, "device_requested": dev},
            SHORT_GPU_PROBE_BLOCKED_CUDA,
            M17_BLOCKED_CUDA,
            False,
        )

    gpu_name = ""
    mem_s = ""
    if cuda_avail and dev == "cuda":
        try:
            gpu_name = str(torch.cuda.get_device_name(0))
            mem_s = str(torch.cuda.get_device_properties(0).total_memory)
        except (RuntimeError, AssertionError):
            gpu_name = "unavailable"
            mem_s = ""

    gpu = {
        "posture": "recorded_when_available",
        "gpu_name": redact_paths_in_value(gpu_name) if gpu_name else "",
        "memory_summary": mem_s,
    }

    steps_executed = 0
    last_val = 0.0
    try:
        for i in range(max_steps):
            if dev == "cuda" and cuda_avail:
                t = torch.zeros(2, 2, device="cuda")
                t = t + float(i + 1)
                last_val = float(t.sum().item())
            else:
                t = torch.zeros(2, 2, device="cpu")
                t = t + float(i + 1)
                last_val = float(t.sum().item())
            steps_executed += 1
        probe_steps = {
            "steps_requested": max_steps,
            "steps_executed": steps_executed,
            "device_requested": dev,
            "deterministic_probe_accumulator": last_val,
        }
        return (
            summary,
            gpu,
            probe_steps,
            SHORT_GPU_PROBE_SUCCESS,
            M17_READY_PLANNING,
            True,
        )
    except RuntimeError:
        probe_steps = {
            "steps_requested": max_steps,
            "steps_executed": steps_executed,
            "device_requested": dev,
        }
        return summary, gpu, probe_steps, SHORT_GPU_PROBE_FAILED, M17_BLOCKED_PENDING, False


def _load_operator_environment_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("operator environment JSON must be a single object")
    out = redact_paths_in_value(raw)
    if not isinstance(out, dict):
        raise ValueError("operator environment JSON redaction must preserve object root")
    return out


def build_short_gpu_environment_body(
    *,
    profile: str,
    operator_environment_path: Path | None,
    allow_operator_local_execution: bool,
    authorize_short_gpu_probe: bool,
    device: str,
    max_steps: int,
    m02_path: Path | None,
    m07_path: Path | None,
    m08_path: Path | None,
    m15_path: Path | None,
) -> dict[str, Any]:
    if profile == PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE:
        if not allow_operator_local_execution or not authorize_short_gpu_probe:
            raise ValueError(
                "operator_local_short_gpu_probe requires dual guards: "
                "allow_operator_local_execution and authorize_short_gpu_probe"
            )
    if profile == PROFILE_OPERATOR_DECLARED:
        if operator_environment_path is None:
            raise ValueError("operator_declared requires operator_environment_path")

    m15_bound = m15_path is not None
    probe_ran = profile == PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE
    operator_local_execution = probe_ran
    short_gpu_probe_performed = False
    short_gpu_probe_result = SHORT_GPU_PROBE_NOT_RUN
    m17_rec = M17_BLOCKED_PENDING
    evidence_status = EVIDENCE_STATUS_FIXTURE_ONLY
    torch_cuda_summary = _fixture_torch_cuda_summary()
    gpu_summary = _fixture_gpu_summary()
    probe_detail: dict[str, Any] = {}
    environment_summary = _fixture_environment_summary()
    sc2_environment_summary = _fixture_sc2_summary()
    disk_output_summary = _fixture_disk_summary()

    if profile == PROFILE_FIXTURE_CI:
        pass
    elif profile == PROFILE_OPERATOR_DECLARED:
        evidence_status = EVIDENCE_STATUS_OPERATOR_DECLARED
        declared = _load_operator_environment_json(operator_environment_path)  # type: ignore[arg-type]
        merged_env = declared.get("environment_summary")
        if isinstance(merged_env, dict):
            environment_summary = {**environment_summary, **merged_env}
        merged_repo = declared.get("repo_identity")
        if isinstance(merged_repo, dict):
            rid = environment_summary.get("repository_identity")
            if isinstance(rid, dict):
                environment_summary["repository_identity"] = {**rid, **merged_repo}
            else:
                environment_summary["repository_identity"] = merged_repo
        merged_sc2 = declared.get("sc2_environment_summary")
        if isinstance(merged_sc2, dict):
            sc2_environment_summary = {**sc2_environment_summary, **merged_sc2}
        merged_disk = declared.get("disk_output_summary")
        if isinstance(merged_disk, dict):
            disk_output_summary = {**disk_output_summary, **merged_disk}
        m17_rec = M17_READY_PREFLIGHT
    elif profile == PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE:
        evidence_status = EVIDENCE_STATUS_PROBE_BLOCKED
        git_id = _try_git_repo_identity()
        import platform as plat
        import sys

        environment_summary = {
            "repository_identity": git_id if git_id else _fixture_repo_identity(),
            "python_version": sys.version.split()[0],
            "platform": plat.platform(),
            "dependency_lock_posture": "not_evaluated_by_m16_emitter",
            "dependency_fingerprint": PLACEHOLDER_SHA256,
        }
        tcs, gpus, probe_detail, short_gpu_probe_result, m17_rec, ok = run_bounded_short_gpu_probe(
            device=device, max_steps=max_steps
        )
        torch_cuda_summary = tcs
        gpu_summary = gpus
        short_gpu_probe_performed = ok and short_gpu_probe_result == SHORT_GPU_PROBE_SUCCESS
        evidence_status = (
            EVIDENCE_STATUS_PROBE_SUCCESS
            if short_gpu_probe_performed
            else (EVIDENCE_STATUS_PROBE_BLOCKED)
        )
    else:
        raise ValueError(f"unknown profile: {profile!r}")

    probe_ok = short_gpu_probe_performed

    upstream: dict[str, Any] = {}
    if m02_path:
        upstream["m02_environment_lock"] = _m02_binding_file(m02_path)
    else:
        upstream["m02_environment_lock"] = _m02_placeholder()
    if m07_path:
        upstream["m07_training_run_receipt"] = _m07_binding_file(m07_path)
    else:
        upstream["m07_training_run_receipt"] = _m07_placeholder()
    if m08_path:
        upstream["m08_long_gpu_training_manifest"] = _m08_binding_file(m08_path)
    else:
        upstream["m08_long_gpu_training_manifest"] = _m08_placeholder()
    if m15_path:
        upstream["m15_operator_evidence_preflight"] = _m15_binding_file(m15_path)
    else:
        upstream["m15_operator_evidence_preflight"] = _m15_placeholder()

    if m15_path is None and profile == PROFILE_FIXTURE_CI:
        m17_rec = M17_BLOCKED_PENDING

    readiness_gates = _build_readiness_gates(
        m15_bound=m15_bound,
        probe_ran=probe_ran,
        probe_ok=probe_ok,
        fixture_mode=profile == PROFILE_FIXTURE_CI,
    )

    return {
        "contract_id": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
        "milestone": MILESTONE_ID_V15_M16,
        "emitter_module": EMITTER_MODULE_SHORT_GPU_ENVIRONMENT,
        "profile": profile,
        "evidence_status": evidence_status,
        "operator_local_execution_performed": operator_local_execution,
        "short_gpu_probe_performed": short_gpu_probe_performed,
        "short_gpu_probe_result": short_gpu_probe_result,
        "short_gpu_probe_detail": probe_detail,
        "m17_opening_recommendation": m17_rec,
        "long_gpu_run_authorized": False,
        "v2_authorized": False,
        "v2_recharter_authorized": False,
        "upstream_bindings": upstream,
        "environment_summary": environment_summary,
        "gpu_summary": gpu_summary,
        "torch_cuda_summary": torch_cuda_summary,
        "sc2_environment_summary": sc2_environment_summary,
        "disk_output_summary": disk_output_summary,
        "readiness_gates": readiness_gates,
        "public_private_boundary": _public_private_boundary(),
        "register_touchpoints": [{"register_doc": p} for p in REGISTER_TOUCHPOINT_PATHS],
        "non_claims": [NON_CLAIMS_V15_M16],
        "operator_notes_redaction": _operator_notes_redaction_default(),
    }


def seal_short_gpu_environment_body(body: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in body.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    sealed = dict(base)
    sealed[_SEAL] = digest
    return sealed


def build_short_gpu_environment_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_short_gpu_environment_evidence_report",
        "report_version": REPORT_VERSION_SHORT_GPU_ENV,
        "milestone": MILESTONE_ID_V15_M16,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": sealed.get(_SEAL) == digest,
        "primary_filename": FILENAME_SHORT_GPU_ENV_EVIDENCE,
        "checklist_markdown": FILENAME_SHORT_GPU_ENV_CHECKLIST_MD,
    }


def render_short_gpu_environment_checklist_md(sealed: dict[str, Any]) -> str:
    lines: list[str] = [
        "# V15-M16 — Short GPU / environment evidence (checklist)",
        "",
        "Governance checklist for bounded environment / short GPU evidence. **Not** a long GPU campaign "
        "receipt and **not** claim authorization.",
        "",
        "## Summary",
        "",
        f"- Contract: `{sealed.get('contract_id', '')}`",
        f"- Profile: `{sealed.get('profile', '')}`",
        f"- Evidence status: `{sealed.get('evidence_status', '')}`",
        f"- Operator-local execution: `{sealed.get('operator_local_execution_performed')!s}`",
        f"- Short GPU probe performed: `{sealed.get('short_gpu_probe_performed')!s}`",
        f"- Short GPU probe result: `{sealed.get('short_gpu_probe_result', '')}`",
        f"- M17 opening recommendation: `{sealed.get('m17_opening_recommendation', '')}`",
        f"- long_gpu_run_authorized: {sealed.get('long_gpu_run_authorized')!s} (must remain false in M16)",
        "",
        "## Upstream bindings (SHA posture)",
        "",
    ]
    ub = sealed.get("upstream_bindings")
    if isinstance(ub, dict):
        for key in sorted(ub.keys()):
            b = ub[key]
            if isinstance(b, dict):
                mode = b.get("binding_mode", "")
                lines.append(f"- **{key}**: `{mode}`")
    lines.extend(["", "## Readiness gates (G0–G12)", ""])
    gates = sealed.get("readiness_gates")
    if isinstance(gates, list):
        for g in gates:
            if isinstance(g, dict):
                lines.append(
                    f"- **{g.get('gate_id', '')}** — {g.get('name', '')} "
                    f"(`{g.get('default_status', '')}`)"
                )
    lines.extend(["", "## Non-claims", ""])
    nc = sealed.get("non_claims")
    if isinstance(nc, list):
        for item in nc:
            lines.append(f"- {item}")
    text = "\n".join(lines) + "\n"
    low = text.lower()
    for bad in FORBIDDEN_CHECKLIST_SUBSTRINGS:
        if bad in low:
            raise ValueError(f"checklist would contain forbidden phrase: {bad!r}")
    return text


def emit_v15_short_gpu_environment_evidence(
    output_dir: Path,
    *,
    profile: str = PROFILE_FIXTURE_CI,
    operator_environment_path: Path | None = None,
    allow_operator_local_execution: bool = False,
    authorize_short_gpu_probe: bool = False,
    device: str = "cuda",
    max_steps: int = 5,
    m02_path: Path | None = None,
    m07_path: Path | None = None,
    m08_path: Path | None = None,
    m15_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_short_gpu_environment_body(
        profile=profile,
        operator_environment_path=operator_environment_path,
        allow_operator_local_execution=allow_operator_local_execution,
        authorize_short_gpu_probe=authorize_short_gpu_probe,
        device=device,
        max_steps=max_steps,
        m02_path=m02_path,
        m07_path=m07_path,
        m08_path=m08_path,
        m15_path=m15_path,
    )
    sealed = seal_short_gpu_environment_body(body)
    report = build_short_gpu_environment_report(sealed)
    md = render_short_gpu_environment_checklist_md(sealed)
    pj = output_dir / FILENAME_SHORT_GPU_ENV_EVIDENCE
    pr = output_dir / REPORT_FILENAME_SHORT_GPU_ENV_EVIDENCE
    pm = output_dir / FILENAME_SHORT_GPU_ENV_CHECKLIST_MD
    pj.write_text(canonical_json_dumps(sealed), encoding="utf-8", newline="\n")
    pr.write_text(canonical_json_dumps(report), encoding="utf-8", newline="\n")
    pm.write_text(md, encoding="utf-8", newline="\n")
    return sealed, report, pj, pr, pm


__all__ = [
    "build_short_gpu_environment_body",
    "build_short_gpu_environment_report",
    "emit_v15_short_gpu_environment_evidence",
    "parse_m02_environment_lock",
    "parse_m07_training_run_receipt",
    "parse_m08_long_gpu_manifest",
    "parse_m15_operator_evidence_preflight",
    "render_short_gpu_environment_checklist_md",
    "run_bounded_short_gpu_probe",
    "seal_short_gpu_environment_body",
]
