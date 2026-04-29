"""V15-M39 two-hour operator run attempt — receipts, preflight, inventory helpers."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_models import (
    ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256,
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
)
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_models import (
    CONTRACT_ID_M38,
    GATE_ARTIFACT_DIGEST_FIELD,
    PROFILE_M38,
)
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_models import (
    FILENAME_MAIN_JSON as M38_MAIN_JSON,
)
from starlab.v15.m39_two_hour_operator_run_attempt_models import (
    CHECKLIST_FILENAME,
    CHECKPOINT_INVENTORY_FILENAME,
    CONTRACT_ID_M39,
    EMITTER_MODULE_M39,
    FILENAME_MAIN_JSON,
    M39_OUTPUT_ROOT_TOKEN,
    MILESTONE_LABEL_M39,
    NON_CLAIMS_M39,
    PROFILE_FIXTURE_CI,
    PROFILE_M39,
    PROFILE_OPERATOR_PREFLIGHT,
    PUBLIC_LEDGER_M29_ARTIFACT_SHA256,
    RECOMMENDED_NEXT_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    RUN_SCOPE,
    RUNNER_MODULE_M39,
    SCHEMA_VERSION,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_BLOCKED_CUDA,
    STATUS_PREFLIGHT_BLOCKED_DISK,
    STATUS_PREFLIGHT_BLOCKED_ENV,
    STATUS_PREFLIGHT_BLOCKED_LINEAGE,
    STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY,
    STATUS_PREFLIGHT_BLOCKED_NO_LAUNCH_CMD,
    STATUS_PREFLIGHT_BLOCKED_NO_M38,
    STATUS_PREFLIGHT_BLOCKED_RETENTION,
    STATUS_PREFLIGHT_BLOCKED_SC2,
    STATUS_PREFLIGHT_READY,
    STATUS_RUN_BLOCKED_PREFLIGHT,
    STATUS_RUN_COMPLETED_NO_CKPT,
    STATUS_RUN_COMPLETED_WITH_CKPT,
    STATUS_RUN_FAILED,
    STATUS_RUN_INTERRUPTED,
    TARGET_WALL_CLOCK_SECONDS,
    TELEMETRY_SUMMARY_FILENAME,
    TRANSCRIPT_FILENAME,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")


def _is_hex64(s: str) -> bool:
    t = str(s or "").strip().lower()
    return len(t) == 64 and all(c in _HEX64_CHARS for c in t)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _canonical_seal_ok(
    raw: dict[str, Any],
    *,
    digest_key: str = GATE_ARTIFACT_DIGEST_FIELD,
) -> bool:
    seal_in = raw.get(digest_key)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != digest_key}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def sha256_file_hex(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fb:
        while chunk := fb.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def seal_m39_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _claim_flags_all_false() -> dict[str, Any]:
    return {
        "two_hour_run_executed": False,
        "two_hour_run_completed": False,
        "benchmark_passed": False,
        "scorecard_results_produced": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "xai_execution_performed": False,
        "human_panel_execution_performed": False,
        "showcase_release_authorized": False,
        "v2_authorized": False,
        "t2_authorized": False,
        "t3_authorized": False,
    }


def _default_checkpoint_retention_fields() -> dict[str, Any]:
    return {
        "checkpoint_retention_enabled": True,
        "checkpoint_retention_max_retained": 0,
        "checkpoints_written_total": 0,
        "checkpoints_pruned_total": 0,
        "final_step_checkpoint_persisted": False,
    }


def _default_execution_telemetry_pub() -> dict[str, Any]:
    return {
        "training_update_count": 0,
        "sc2_backed_features_used": False,
        "transcript_captured": False,
        "transcript_artifact_filename": TRANSCRIPT_FILENAME,
        "transcript_absolute_path_redacted": True,
        "telemetry_summary_captured": False,
        "checkpoint_inventory_captured": False,
    }


def _default_upstream_bindings(*, m38_obj: dict[str, Any] | None) -> dict[str, Any]:
    m38_sha = None
    m39_ready = False
    if m38_obj is not None:
        m38_sha = str(m38_obj.get(GATE_ARTIFACT_DIGEST_FIELD) or "")
        if not _is_hex64(m38_sha):
            m38_sha = None
        m39_ready = bool(m38_obj.get("m39_launch_ready"))

    return {
        "m38_launch_rehearsal": {
            "artifact_sha256": m38_sha,
            "contract_id": CONTRACT_ID_M38,
            "profile_id": PROFILE_M38,
            "m39_launch_ready": m39_ready,
        },
        "m37_blocker_discovery": {"binding_status": "inherited_from_m38"},
        "m27_rollout": {"artifact_sha256": ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256},
        "m29_baseline_30min": {"artifact_sha256": PUBLIC_LEDGER_M29_ARTIFACT_SHA256},
    }


def validate_launch_command_text(txt: str) -> tuple[bool, str]:
    """Return (ok, failure_reason)."""
    raw = str(txt or "")
    low = raw.lower()
    norm = raw.replace("\\", "/")
    if "max-retained-checkpoints" not in low and "max_retained_checkpoints" not in low:
        return False, "missing_max_retained_checkpoints"
    if "7200" not in raw and "120" not in raw:
        return False, "missing_7200s_or_120min_horizon"
    if M39_OUTPUT_ROOT_TOKEN not in norm.lower():
        return False, "missing_m39_output_root_token"
    if ".venv" not in low and "venv/scripts" not in low and "virtualenv" not in low:
        return False, "missing_venv_python_hint"
    return True, "ok"


@dataclass(frozen=True)
class PreflightOutcome:
    status: str
    detail: str
    m38_obj: dict[str, Any] | None = None


def probe_cuda_available() -> tuple[bool, str]:
    try:
        import torch

        if torch.cuda.is_available():
            return True, "cuda_ok"
        return False, "torch_cuda_not_available"
    except Exception as exc:
        return False, f"torch_import_or_cuda_error:{type(exc).__name__}"


def probe_sc2_import() -> tuple[bool, str]:
    try:
        import importlib

        importlib.import_module("sc2")
        return True, "sc2_import_ok"
    except Exception as exc:
        return False, f"sc2_import_failed:{type(exc).__name__}"


def disk_and_output_writable(output_dir: Path, *, min_free_bytes: int) -> tuple[bool, str]:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        usage = shutil.disk_usage(output_dir)
        if usage.free < min_free_bytes:
            return False, "disk_free_below_threshold"
        probe = output_dir / ".m39_write_probe"
        probe.write_text("ok\n", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True, "writable"
    except OSError as exc:
        return False, f"os_error:{exc}"


def evaluate_operator_preflight(
    *,
    repo_root: Path,
    m38_launch_rehearsal_json: Path | None,
    m39_launch_command: Path | None,
    expected_candidate_sha256: str,
    skip_cuda_sc2: bool,
    min_free_bytes: int,
    output_dir: Path,
) -> PreflightOutcome:
    cand = str(expected_candidate_sha256 or "").strip().lower()
    if not _is_hex64(cand):
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_ENV, "invalid_expected_candidate_sha_cli")
    if cand != EXPECTED_PUBLIC_CANDIDATE_SHA256.lower():
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_LINEAGE, "expected_candidate_sha_mismatch")

    wr_ok, wr_why = disk_and_output_writable(output_dir, min_free_bytes=min_free_bytes)
    if not wr_ok:
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_DISK, wr_why)

    if m38_launch_rehearsal_json is None or not m38_launch_rehearsal_json.is_file():
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_NO_M38, "missing_m38_json_path")

    try:
        m38_obj = _parse_json_object(m38_launch_rehearsal_json.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_NO_M38, f"m38_json_unreadable:{exc}")

    if str(m38_obj.get("contract_id") or "") != CONTRACT_ID_M38:
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_NO_M38, "m38_contract_mismatch")
    if not _canonical_seal_ok(m38_obj):
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY, "m38_seal_mismatch")

    if not bool(m38_obj.get("m39_launch_ready")):
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_M38_NOT_READY, "m39_launch_ready_false")

    if m39_launch_command is None or not m39_launch_command.is_file():
        return PreflightOutcome(
            STATUS_PREFLIGHT_BLOCKED_NO_LAUNCH_CMD, "missing_launch_command_file"
        )

    cmd_txt = m39_launch_command.read_text(encoding="utf-8", errors="replace")
    cmd_ok, cmd_why = validate_launch_command_text(cmd_txt)
    if not cmd_ok:
        if cmd_why == "missing_max_retained_checkpoints":
            return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_RETENTION, cmd_why)
        return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_ENV, cmd_why)

    if not skip_cuda_sc2:
        cu_ok, _ = probe_cuda_available()
        if not cu_ok:
            return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_CUDA, "cuda_unavailable")
        sc_ok, _ = probe_sc2_import()
        if not sc_ok:
            return PreflightOutcome(STATUS_PREFLIGHT_BLOCKED_SC2, "sc2_unavailable")

    return PreflightOutcome(STATUS_PREFLIGHT_READY, "ok", m38_obj=m38_obj)


def build_checkpoint_inventory(
    output_dir: Path,
    *,
    extra_glob_roots: list[Path] | None = None,
) -> dict[str, Any]:
    roots = [output_dir]
    if extra_glob_roots:
        roots.extend(extra_glob_roots)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in ("**/*.pt", "**/*.pth"):
            for p in root.glob(pattern):
                if not p.is_file():
                    continue
                try:
                    rel = str(p.resolve().relative_to(output_dir.resolve()))
                except ValueError:
                    rel = p.name
                if rel in seen:
                    continue
                seen.add(rel)
                st = p.stat()
                rows.append(
                    {
                        "path_relative_to_m39_output_dir": rel.replace("\\", "/"),
                        "size_bytes": st.st_size,
                        "mtime_epoch": st.st_mtime,
                        "sha256": sha256_file_hex(p),
                    },
                )
    rows.sort(key=lambda r: float(r["mtime_epoch"]), reverse=True)
    final_rel = None
    classification = "no_checkpoint_files_observed"
    if rows:
        final_rel = str(rows[0]["path_relative_to_m39_output_dir"])
        classification = "newest_mtime_treated_as_final_candidate_guess"
    return {
        "scan_roots_relative": [str(r).replace("\\", "/") for r in roots],
        "checkpoint_files": rows,
        "final_checkpoint_guess_relative": final_rel,
        "classification_note": classification,
    }


def build_fixture_body(
    *,
    repo_root: Path,
    m38_obj: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = repo_root  # reserved for parity with other milestone emitters
    upstream = _default_upstream_bindings(m38_obj=m38_obj)
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M39,
        "profile_id": PROFILE_M39,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M39,
        "emitter_module": EMITTER_MODULE_M39,
        "runner_module": RUNNER_MODULE_M39,
        "run_status": STATUS_FIXTURE_ONLY,
        "run_scope": RUN_SCOPE,
        "operator_local_only": True,
        "target_wall_clock_seconds": int(TARGET_WALL_CLOCK_SECONDS),
        "observed_wall_clock_seconds": 0.0,
        "full_wall_clock_satisfied": False,
        "preflight_detail": None,
        "upstream_bindings": upstream,
        "candidate_checkpoint": {
            "source_candidate_sha256": EXPECTED_PUBLIC_CANDIDATE_SHA256,
            "final_candidate_sha256": None,
            "promotion_status": "not_promoted_candidate_only",
        },
        "checkpoint_retention": _default_checkpoint_retention_fields(),
        "execution_telemetry": _default_execution_telemetry_pub(),
        "launch_command_delta_detected": False,
        "claim_flags": _claim_flags_all_false(),
        "non_claims": list(NON_CLAIMS_M39),
        "recommended_next": RECOMMENDED_NEXT_SUCCESS,
    }


def build_m39_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_two_hour_operator_run_attempt_report",
        "report_version": "m39",
        "milestone": MILESTONE_LABEL_M39,
        "contract_id": CONTRACT_ID_M39,
        "profile_id": PROFILE_M39,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "run_status": sealed.get("run_status"),
    }


def build_m39_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("run_status", ""))
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return f"""# V15-M39 — 2-hour operator run attempt checklist

**Status:** `{st}`

## Non-claims

{nc_lines}

## Artifacts

- `{FILENAME_MAIN_JSON}`
- `{REPORT_FILENAME}`
- `{CHECKLIST_FILENAME}`
- `{TRANSCRIPT_FILENAME}`
- `{TELEMETRY_SUMMARY_FILENAME}`
- `{CHECKPOINT_INVENTORY_FILENAME}`

## Upstream

- Sealed **`{M38_MAIN_JSON}`** required for operator preflight / run.
"""


def _fixture_telemetry_summary() -> dict[str, Any]:
    return {
        "profile": PROFILE_FIXTURE_CI,
        "note": "fixture_schema_only_no_operator_run",
        "nvidia_smi_sampled": False,
        "torch_cuda_available": None,
    }


def _write_m39_bundle(
    output_dir: Path,
    sealed: dict[str, Any],
    *,
    transcript_text: str,
    telemetry_obj: dict[str, Any],
    inventory_obj: dict[str, Any],
) -> tuple[Path, Path, Path, Path, Path, Path]:
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_tr = output_dir / TRANSCRIPT_FILENAME
    p_tel = output_dir / TELEMETRY_SUMMARY_FILENAME
    p_inv = output_dir / CHECKPOINT_INVENTORY_FILENAME

    rep = build_m39_report(sealed)
    chk = build_m39_checklist_md(sealed)
    transcript_public = str(redact_paths_in_value(transcript_text))

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_tr.write_text(transcript_public, encoding="utf-8", newline="\n")
    p_tel.write_text(
        canonical_json_dumps(telemetry_obj),
        encoding="utf-8",
    )
    p_inv.write_text(canonical_json_dumps(inventory_obj), encoding="utf-8")

    blob = (
        canonical_json_dumps(sealed)
        + canonical_json_dumps(rep)
        + chk
        + transcript_public
        + canonical_json_dumps(telemetry_obj)
        + canonical_json_dumps(inventory_obj)
    )
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M39 emission leaked path patterns")
    return (p_main, p_rep, p_chk, p_tr, p_tel, p_inv)


def emit_m39_fixture(
    output_dir: Path,
    *,
    repo_root: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body_pre = build_fixture_body(repo_root=repo_root, m38_obj=None)
    sealed = seal_m39_body(redact_paths_in_value(body_pre))
    output_dir.mkdir(parents=True, exist_ok=True)
    inv = build_checkpoint_inventory(output_dir)
    paths = _write_m39_bundle(
        output_dir,
        sealed,
        transcript_text=(
            "fixture_schema_only_no_operator_run\n"
            "(no operator subprocess; no SC2; no training transcript)\n"
        ),
        telemetry_obj=_fixture_telemetry_summary(),
        inventory_obj=inv,
    )
    return sealed, paths


def emit_m39_operator_preflight(
    output_dir: Path,
    *,
    repo_root: Path,
    m38_launch_rehearsal_json: Path,
    m39_launch_command: Path,
    expected_candidate_sha256: str,
    skip_cuda_sc2: bool = False,
    min_free_disk_gb: float = 1.0,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    min_bytes = int(float(min_free_disk_gb) * (1024**3))
    outcome = evaluate_operator_preflight(
        repo_root=repo_root,
        m38_launch_rehearsal_json=m38_launch_rehearsal_json,
        m39_launch_command=m39_launch_command,
        expected_candidate_sha256=expected_candidate_sha256,
        skip_cuda_sc2=skip_cuda_sc2,
        min_free_bytes=max(min_bytes, 1_000_000),
        output_dir=output_dir,
    )

    m38 = outcome.m38_obj
    body = build_fixture_body(repo_root=repo_root, m38_obj=m38)
    body["profile"] = PROFILE_OPERATOR_PREFLIGHT
    body["run_status"] = outcome.status
    body["preflight_detail"] = outcome.detail
    body["target_wall_clock_seconds"] = int(TARGET_WALL_CLOCK_SECONDS)
    if outcome.status != STATUS_PREFLIGHT_READY:
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION

    if m38 is not None:
        m38_sha = str(m38.get(GATE_ARTIFACT_DIGEST_FIELD) or "")
        if _is_hex64(m38_sha):
            body["upstream_bindings"]["m38_launch_rehearsal"]["artifact_sha256"] = m38_sha
            body["upstream_bindings"]["m38_launch_rehearsal"]["m39_launch_ready"] = bool(
                m38.get("m39_launch_ready"),
            )

    sealed = seal_m39_body(redact_paths_in_value(body))
    output_dir.mkdir(parents=True, exist_ok=True)

    inv = build_checkpoint_inventory(output_dir)
    tel = {
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "preflight_detail": outcome.detail,
        "cuda_probe_skipped": skip_cuda_sc2,
    }
    if not skip_cuda_sc2:
        cu_ok, cu_note = probe_cuda_available()
        tel["torch_cuda_available"] = cu_ok
        tel["cuda_note"] = cu_note
        sc_ok, sc_note = probe_sc2_import()
        tel["sc2_import_ok"] = sc_ok
        tel["sc2_note"] = sc_note

    transcript = f"operator_preflight_only\nrun_status={outcome.status}\ndetail={outcome.detail}\n"
    paths = _write_m39_bundle(
        output_dir,
        sealed,
        transcript_text=transcript,
        telemetry_obj=tel,
        inventory_obj=inv,
    )
    return sealed, paths


def classify_run_outcome(
    *,
    return_code: int,
    observed_seconds: float,
    target_seconds: float,
    interrupted: bool,
    inventory: dict[str, Any],
    sc2_backed_features_used_guess: bool,
    retention_max_retained: int,
    _checkpoints_written: int,
    _checkpoints_pruned: int,
    final_persisted: bool,
) -> str:
    tol = 30.0
    wall_ok = observed_seconds + tol >= target_seconds
    has_ckpt = bool(inventory.get("checkpoint_files"))

    if interrupted:
        return STATUS_RUN_INTERRUPTED
    if return_code != 0:
        return STATUS_RUN_FAILED
    if not wall_ok:
        return STATUS_RUN_INTERRUPTED
    retention_active = retention_max_retained > 0
    if has_ckpt and sc2_backed_features_used_guess and retention_active and final_persisted:
        return STATUS_RUN_COMPLETED_WITH_CKPT
    return STATUS_RUN_COMPLETED_NO_CKPT


def merge_telemetry_from_m28_artifact(output_dir: Path) -> dict[str, Any]:
    """Best-effort ingest of sealed M28 training JSON under `output_dir`."""
    candidates = sorted(output_dir.glob("**/v15_sc2_backed_t1_candidate_training.json"))
    if not candidates:
        return {}
    try:
        obj = _parse_json_object(candidates[-1])
    except (OSError, json.JSONDecodeError, ValueError):
        return {}
    ta = obj.get("training_attempt")
    if not isinstance(ta, dict):
        return {}
    return {
        "m28_artifact_relative": str(candidates[-1].relative_to(output_dir)).replace("\\", "/"),
        "training_update_count": int(ta.get("training_update_count") or 0),
        "wall_clock_seconds": float(ta.get("wall_clock_seconds") or 0.0),
        "checkpoint_count": int(ta.get("checkpoint_count") or 0),
        "checkpoints_written_total": ta.get("checkpoints_written_total"),
        "checkpoints_pruned_total": ta.get("checkpoints_pruned_total"),
        "checkpoint_retention_max_retained": ta.get("checkpoint_retention_max_retained"),
        "sc2_backed_features_used": bool(ta.get("sc2_backed_features_used")),
    }


def emit_m39_operator_run_receipt(
    output_dir: Path,
    *,
    repo_root: Path,
    m38_launch_rehearsal_json: Path,
    m39_launch_command: Path,
    expected_candidate_sha256: str,
    max_retained_checkpoints: int,
    target_wall_clock_seconds: float,
    skip_cuda_sc2: bool,
    min_free_disk_gb: float,
    subprocess_result: subprocess.CompletedProcess[str] | None,
    observed_wall_seconds: float,
    interrupted: bool,
    launch_command_delta_detected: bool,
    transcript_text: str,
    preflight_outcome: PreflightOutcome | None = None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    min_bytes = int(float(min_free_disk_gb) * (1024**3))
    pre = (
        preflight_outcome
        if preflight_outcome is not None
        else evaluate_operator_preflight(
            repo_root=repo_root,
            m38_launch_rehearsal_json=m38_launch_rehearsal_json,
            m39_launch_command=m39_launch_command,
            expected_candidate_sha256=expected_candidate_sha256,
            skip_cuda_sc2=skip_cuda_sc2,
            min_free_bytes=max(min_bytes, 1_000_000),
            output_dir=output_dir,
        )
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    if pre.status != STATUS_PREFLIGHT_READY:
        body = build_fixture_body(repo_root=repo_root, m38_obj=pre.m38_obj)
        body["profile"] = PROFILE_OPERATOR_PREFLIGHT
        body["run_status"] = STATUS_RUN_BLOCKED_PREFLIGHT
        body["preflight_detail"] = pre.detail
        body["claim_flags"] = _claim_flags_all_false()
        body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
        sealed = seal_m39_body(redact_paths_in_value(body))
        inv = build_checkpoint_inventory(output_dir)
        tel = {"blocked_preflight": True, "preflight_status": pre.status}
        paths = _write_m39_bundle(
            output_dir,
            sealed,
            transcript_text=transcript_text or f"blocked_preflight:{pre.status}\n",
            telemetry_obj=tel,
            inventory_obj=inv,
        )
        return sealed, paths

    m38 = pre.m38_obj
    assert m38 is not None
    inventory = build_checkpoint_inventory(output_dir)
    m28_hints = merge_telemetry_from_m28_artifact(output_dir)

    ck_written = int(m28_hints.get("checkpoints_written_total") or 0)
    ck_pruned = int(m28_hints.get("checkpoints_pruned_total") or 0)
    ret_max = int(m28_hints.get("checkpoint_retention_max_retained") or max_retained_checkpoints)
    if ret_max <= 0:
        ret_max = max_retained_checkpoints
    sc2_used = bool(m28_hints.get("sc2_backed_features_used"))
    final_persisted = ck_written > 0 or bool(inventory.get("checkpoint_files"))

    rc = -1 if subprocess_result is None else int(subprocess_result.returncode)
    run_status = classify_run_outcome(
        return_code=rc,
        observed_seconds=observed_wall_seconds,
        target_seconds=target_wall_clock_seconds,
        interrupted=interrupted,
        inventory=inventory,
        sc2_backed_features_used_guess=sc2_used,
        retention_max_retained=ret_max,
        _checkpoints_written=ck_written,
        _checkpoints_pruned=ck_pruned,
        final_persisted=final_persisted,
    )

    body = build_fixture_body(repo_root=repo_root, m38_obj=m38)
    body["profile"] = "operator_local_two_hour_run"
    body["run_status"] = run_status
    body["target_wall_clock_seconds"] = int(target_wall_clock_seconds)
    body["observed_wall_clock_seconds"] = round(float(observed_wall_seconds), 3)
    body["full_wall_clock_satisfied"] = bool(
        observed_wall_seconds + 30.0 >= target_wall_clock_seconds,
    )
    body["launch_command_delta_detected"] = bool(launch_command_delta_detected)
    body["checkpoint_retention"] = {
        "checkpoint_retention_enabled": ret_max > 0,
        "checkpoint_retention_max_retained": ret_max,
        "checkpoints_written_total": ck_written,
        "checkpoints_pruned_total": ck_pruned,
        "final_step_checkpoint_persisted": final_persisted,
    }
    body["execution_telemetry"] = {
        "training_update_count": int(m28_hints.get("training_update_count") or 0),
        "sc2_backed_features_used": sc2_used,
        "transcript_captured": bool(transcript_text),
        "transcript_artifact_filename": TRANSCRIPT_FILENAME,
        "transcript_absolute_path_redacted": True,
        "telemetry_summary_captured": True,
        "checkpoint_inventory_captured": True,
        "m28_artifact_hints": m28_hints or None,
    }

    final_sha = None
    if inventory.get("checkpoint_files"):
        final_sha = str(inventory["checkpoint_files"][0].get("sha256"))
    body["candidate_checkpoint"]["final_candidate_sha256"] = final_sha

    flags = _claim_flags_all_false()
    flags["two_hour_run_executed"] = subprocess_result is not None
    flags["two_hour_run_completed"] = run_status in (
        STATUS_RUN_COMPLETED_WITH_CKPT,
        STATUS_RUN_COMPLETED_NO_CKPT,
    )
    body["claim_flags"] = flags
    body["recommended_next"] = (
        RECOMMENDED_NEXT_SUCCESS
        if run_status == STATUS_RUN_COMPLETED_WITH_CKPT
        else RECOMMENDED_NEXT_REMEDIATION
    )

    sealed = seal_m39_body(redact_paths_in_value(body))
    tel = {
        "profile": "operator_local_two_hour_run",
        "return_code": rc,
        "interrupted": interrupted,
        "m28_hints": m28_hints,
    }
    paths = _write_m39_bundle(
        output_dir,
        sealed,
        transcript_text=transcript_text,
        telemetry_obj=tel,
        inventory_obj=inventory,
    )
    return sealed, paths


def frozen_launch_command_to_cmdexe_line(launch_file: Path, *, repo_root: Path) -> str:
    """Join a frozen M38 .txt launch file into one cmd.exe-friendly shell line."""
    raw = launch_file.read_text(encoding="utf-8", errors="replace")
    lines: list[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("//"):
            continue
        s = re.sub(r"\s*\^\s*$", "", s)
        lines.append(s)
    joined = " ".join(lines)
    if not joined.strip():
        raise ValueError("empty_launch_command_after_comment_strip")
    rr = str(repo_root.resolve())
    cd_target = f'"{rr}"' if re.search(r"[\s&()]", rr) else rr
    return f"cmd.exe /V:OFF /C cd /d {cd_target} && {joined}"


def run_operator_subprocess(
    launch_file: Path,
    *,
    repo_root: Path,
    target_wall_clock_seconds: float,
    transcript_path: Path,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    """Run frozen launch via cmd.exe; stream combined output to `transcript_path`."""
    cmd_line = frozen_launch_command_to_cmdexe_line(launch_file, repo_root=repo_root)
    timeout = float(target_wall_clock_seconds) + 600.0
    interrupted = False
    proc = subprocess.Popen(
        cmd_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True,
        cwd=str(repo_root.resolve()),
    )
    assert proc.stdout is not None
    t0 = time.monotonic()
    rc = -1
    with transcript_path.open("w", encoding="utf-8", newline="\n") as tf:
        tf.write(f"m39_operator_transcript t0={t0}\n")
        tf.write(f"cmd_line={cmd_line}\n")
        tf.flush()
        try:
            for line in proc.stdout:
                tf.write(line)
                tf.flush()
        except KeyboardInterrupt:
            interrupted = True
            proc.terminate()
        try:
            rc = int(proc.wait(timeout=timeout))
        except subprocess.TimeoutExpired:
            proc.kill()
            rc = -9
    out_txt = transcript_path.read_text(encoding="utf-8", errors="replace")
    return (
        subprocess.CompletedProcess(args=cmd_line, returncode=rc, stdout=out_txt, stderr=""),
        interrupted,
    )


__all__ = [
    "PreflightOutcome",
    "build_checkpoint_inventory",
    "build_fixture_body",
    "emit_m39_fixture",
    "emit_m39_operator_preflight",
    "emit_m39_operator_run_receipt",
    "evaluate_operator_preflight",
    "frozen_launch_command_to_cmdexe_line",
    "merge_telemetry_from_m28_artifact",
    "run_operator_subprocess",
    "seal_m39_body",
    "validate_launch_command_text",
    "classify_run_outcome",
]
