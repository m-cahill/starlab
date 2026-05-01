"""V15-M53 — twelve-hour operator run attempt IO (fixture, preflight, receipts)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m39_two_hour_operator_run_attempt_io import (
    build_checkpoint_inventory,
    merge_telemetry_from_m28_artifact,
    run_operator_subprocess,
)
from starlab.v15.m51_live_candidate_watchability_harness_io import sha256_hex_file_optional
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    GUARD_AUTHORIZE_ADAPTER_SPIKE as GUARD_M52A_AUTHORIZE_ADAPTER_SPIKE,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_io import M52A_BLOCKISH, M52A_READYISH
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    CONTRACT_ID_M52B,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    DIGEST_FIELD as M52B_DIGEST_FIELD,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    STATUS_FIXTURE_ONLY as M52B_STATUS_FIXTURE_ONLY,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    STATUS_READY as M52B_STATUS_READY,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    STATUS_READY_WARNINGS as M52B_STATUS_READY_WARNINGS,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    STATUS_REFUSED as M52B_STATUS_REFUSED,
)
from starlab.v15.m53_twelve_hour_operator_run_attempt_models import (
    CHECKLIST_FILENAME,
    CHECKPOINT_INVENTORY_FILENAME,
    CONTRACT_ID_M53,
    EMITTER_MODULE_M53,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    GUARD_ALLOW_OPERATOR_LOCAL,
    M52A_CONTRACT_ID,
    M52A_FILENAME,
    M52B_FILENAME,
    MILESTONE_LABEL_M53,
    NON_CLAIMS_M53,
    PHASE_A_BLOCKED,
    PHASE_A_COMPLETED,
    PHASE_A_COMPLETED_WARNINGS,
    PHASE_A_FAILED,
    PHASE_A_NOT_PERFORMED,
    PHASE_A_SKIPPED_ACK,
    PROFILE_FIXTURE_CI,
    PROFILE_M53,
    PROFILE_OPERATOR_12H_RUN,
    RECOMMENDED_NEXT_REMEDIATION,
    RECOMMENDED_NEXT_SUCCESS,
    REPORT_FILENAME,
    RUN_SCOPE,
    RUNNER_MODULE_M53,
    SCHEMA_VERSION,
    STATUS_12H_BLOCKED,
    STATUS_12H_COMPLETED_CKPT,
    STATUS_12H_COMPLETED_NO_CKPT,
    STATUS_12H_COMPLETED_WARNINGS,
    STATUS_12H_FAILED,
    STATUS_12H_INTERRUPTED_NO_RESUME,
    STATUS_12H_INTERRUPTED_RESUME,
    STATUS_FIXTURE_ONLY,
    STATUS_PREFLIGHT_READY,
    TARGET_WALL_CLOCK_SECONDS_DEFAULT,
    TELEMETRY_SUMMARY_FILENAME,
    TRANSCRIPT_FILENAME,
)

_HEX64_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")

BLOCKED_M52_MISSING: Final[str] = "blocked_m52_launch_rehearsal_missing"
BLOCKED_M52_INVALID: Final[str] = "blocked_m52_launch_rehearsal_invalid"
BLOCKED_M52_NOT_READY: Final[str] = "blocked_m52_launch_rehearsal_not_ready"
BLOCKED_M52_SHA: Final[str] = "blocked_m52_sha_mismatch"
BLOCKED_PHASE_A_MISSING: Final[str] = "blocked_candidate_watch_smoke_missing"
BLOCKED_PHASE_A_FAILED: Final[str] = "blocked_candidate_watch_smoke_failed"
BLOCKED_CKPT_MISSING: Final[str] = "blocked_candidate_checkpoint_missing"
BLOCKED_CKPT_SHA: Final[str] = "blocked_candidate_checkpoint_sha_mismatch"
BLOCKED_SC2: Final[str] = "blocked_sc2_root_missing"
BLOCKED_MAP: Final[str] = "blocked_map_missing"
BLOCKED_DISK_UNKNOWN: Final[str] = "blocked_disk_budget_unknown"
BLOCKED_DISK_INSUFFICIENT: Final[str] = "blocked_disk_budget_insufficient"
BLOCKED_RETENTION: Final[str] = "blocked_checkpoint_retention_unset"
BLOCKED_STOP_RESUME: Final[str] = "blocked_stop_resume_plan_missing"
BLOCKED_DUAL_SMOKE: Final[str] = "blocked_operator_authorization_missing"
BLOCKED_DUAL_12H: Final[str] = "blocked_operator_authorization_missing"

FAILED_LIVE_SC2: Final[str] = "failed_live_sc2_runtime_error"
FAILED_SUBPROCESS: Final[str] = "failed_training_subprocess_error"
FAILED_INVENTORY: Final[str] = "failed_checkpoint_inventory_missing"
FAILED_FINAL_CKPT: Final[str] = "failed_final_checkpoint_not_persisted"
FAILED_TRANSCRIPT: Final[str] = "failed_transcript_missing"

REFUSED_FORBIDDEN: Final[str] = "refused_forbidden_overclaim_flag"


def _is_hex64(s: str) -> bool:
    t = str(s or "").strip().lower()
    return len(t) == 64 and all(c in _HEX64_CHARS for c in t)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def m52b_seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(M52B_DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != M52B_DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def seal_m53_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _honesty_all_false() -> dict[str, Any]:
    return {
        "benchmark_passed": False,
        "benchmark_pass_fail_emitted": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "xai_executed": False,
        "human_panel_executed": False,
        "showcase_released": False,
        "v2_authorized": False,
        "t2_t3_t4_t5_executed": False,
    }


def validate_m53_training_launch_command_text(txt: str) -> tuple[bool, str]:
    raw = str(txt or "")
    low = raw.lower()
    norm = raw.replace("\\", "/")
    if "max-retained-checkpoints" not in low and "max_retained_checkpoints" not in low:
        return False, "missing_max_retained_checkpoints"
    if "43200" not in raw and "720" not in low:
        return False, "missing_12h_horizon_hint"
    if ".venv" not in low and "venv/scripts" not in low and "virtualenv" not in low:
        return False, "missing_venv_python_hint"
    if "run_v15_m28_sc2_backed_t1_candidate_training" not in norm.replace(" ", ""):
        if "m28" not in low or "sc2_backed" not in low.replace("_", ""):
            return False, "missing_m28_training_module_hint"
    return True, "ok"


@dataclass(frozen=True)
class M53PreflightOutcome:
    ok: bool
    status: str
    detail: str
    blockers: tuple[str, ...]
    m52_obj: dict[str, Any] | None = None
    m52_digest: str | None = None


def _m52_operator_ready(rehearsal_status: str) -> bool:
    return rehearsal_status in (M52B_STATUS_READY, M52B_STATUS_READY_WARNINGS)


def evaluate_m53_operator_preflight(
    *,
    m52_launch_rehearsal_json: Path | None,
    expected_m52_sha256: str | None,
    m52a_adapter_spike_json: Path | None,
    expected_m52a_sha256: str | None,
    candidate_checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    sc2_root: Path | None,
    map_path: Path | None,
    disk_root: Path | None,
    estimated_checkpoint_mb: float | None,
    max_retained_checkpoints: int | None,
    skip_disk_strict: bool = False,
) -> M53PreflightOutcome:
    blockers: list[str] = []

    if m52_launch_rehearsal_json is None or not m52_launch_rehearsal_json.is_file():
        return M53PreflightOutcome(
            False,
            STATUS_12H_BLOCKED,
            "missing_m52_json",
            (BLOCKED_M52_MISSING,),
            None,
            None,
        )

    try:
        m52 = _parse_json_object(m52_launch_rehearsal_json.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return M53PreflightOutcome(
            False,
            STATUS_12H_BLOCKED,
            f"m52_unreadable:{exc}",
            (BLOCKED_M52_INVALID,),
            None,
            None,
        )

    if str(m52.get("contract_id") or "") != CONTRACT_ID_M52B:
        blockers.append(BLOCKED_M52_INVALID)
        return M53PreflightOutcome(
            False, STATUS_12H_BLOCKED, "contract", tuple(blockers), m52, None
        )

    if not m52b_seal_ok(m52):
        blockers.append(BLOCKED_M52_INVALID)
        return M53PreflightOutcome(False, STATUS_12H_BLOCKED, "seal", tuple(blockers), m52, None)

    digest = str(m52.get(M52B_DIGEST_FIELD) or "").lower()
    if expected_m52_sha256 and _is_hex64(expected_m52_sha256):
        if digest != expected_m52_sha256.strip().lower():
            blockers.append(BLOCKED_M52_SHA)
            return M53PreflightOutcome(
                False,
                STATUS_12H_BLOCKED,
                "m52_sha",
                tuple(blockers),
                m52,
                digest,
            )

    rh = str(m52.get("rehearsal_status") or "")
    if rh in (M52B_STATUS_REFUSED, M52B_STATUS_FIXTURE_ONLY):
        blockers.append(BLOCKED_M52_NOT_READY)
    elif not _m52_operator_ready(rh):
        blockers.append(BLOCKED_M52_NOT_READY)

    if not bool(m52.get("stop_resume_plan_frozen")):
        blockers.append(BLOCKED_STOP_RESUME)

    if m52a_adapter_spike_json is not None and Path(m52a_adapter_spike_json).is_file():
        try:
            m52a = _parse_json_object(Path(m52a_adapter_spike_json).resolve())
        except (OSError, ValueError, json.JSONDecodeError):
            m52a = {}
        if str(m52a.get("contract_id") or "") != M52A_CONTRACT_ID:
            blockers.append(BLOCKED_PHASE_A_MISSING)
        else:
            expa = str(expected_m52a_sha256).strip().lower() if expected_m52a_sha256 else None
            ad = str(m52a.get(M52B_DIGEST_FIELD) or "").lower()
            if expa and _is_hex64(expa) and ad != expa:
                blockers.append(BLOCKED_PHASE_A_FAILED)
            st = str(m52a.get("adapter_status") or "")
            if st not in M52A_READYISH:
                blockers.append(BLOCKED_PHASE_A_FAILED)

    ck = Path(candidate_checkpoint_path).resolve() if candidate_checkpoint_path else None
    exp_ck = str(expected_candidate_sha256).strip().lower() if expected_candidate_sha256 else None
    if ck is None or not ck.is_file():
        blockers.append(BLOCKED_CKPT_MISSING)
    elif exp_ck and _is_hex64(exp_ck):
        got = sha256_hex_file_optional(ck)
        if got != exp_ck:
            blockers.append(BLOCKED_CKPT_SHA)

    if sc2_root is None or not Path(sc2_root).is_dir():
        blockers.append(BLOCKED_SC2)
    if map_path is None or not Path(map_path).is_file():
        blockers.append(BLOCKED_MAP)

    if max_retained_checkpoints is None or int(max_retained_checkpoints) <= 0:
        blockers.append(BLOCKED_RETENTION)

    if not skip_disk_strict:
        if disk_root is None or not Path(disk_root).exists():
            blockers.append(BLOCKED_DISK_UNKNOWN)
        elif estimated_checkpoint_mb is not None and max_retained_checkpoints is not None:
            du = shutil.disk_usage(Path(disk_root).resolve())
            free_mb = du.free / (1024 * 1024)
            need_mb = float(estimated_checkpoint_mb) * int(max_retained_checkpoints) * 1.25
            if free_mb < need_mb:
                blockers.append(BLOCKED_DISK_INSUFFICIENT)

    blockers_u = tuple(sorted(set(blockers)))
    if blockers_u:
        return M53PreflightOutcome(
            False,
            STATUS_12H_BLOCKED,
            "preflight_blockers",
            blockers_u,
            m52,
            digest or None,
        )
    return M53PreflightOutcome(
        True,
        STATUS_PREFLIGHT_READY,
        "ok",
        (),
        m52,
        digest or None,
    )


def m52a_derives_phase_a_status(adapter_status: str) -> str:
    if adapter_status == "candidate_live_adapter_spike_completed_with_warnings":
        return PHASE_A_COMPLETED_WARNINGS
    if adapter_status in (
        "candidate_live_adapter_spike_completed",
        "candidate_live_adapter_preflight_ready",
        "candidate_live_adapter_preflight_ready_with_warnings",
    ):
        if "warning" in adapter_status:
            return PHASE_A_COMPLETED_WARNINGS
        if adapter_status.startswith("candidate_live_adapter_preflight_ready"):
            return PHASE_A_COMPLETED_WARNINGS
        return PHASE_A_COMPLETED
    if adapter_status in (
        "candidate_live_adapter_spike_blocked",
        "candidate_live_adapter_preflight_blocked",
    ):
        return PHASE_A_BLOCKED
    if adapter_status == "candidate_live_adapter_spike_failed":
        return PHASE_A_FAILED
    return PHASE_A_NOT_PERFORMED


def load_m52a_phase_gate(
    m52a_path: Path | None,
    *,
    expected_sha256: str | None,
    skip_acknowledged: bool,
) -> tuple[str, tuple[str, ...], dict[str, Any] | None]:
    blockers: list[str] = []
    if skip_acknowledged:
        return PHASE_A_SKIPPED_ACK, (), None

    if m52a_path is None or not m52a_path.is_file():
        return PHASE_A_NOT_PERFORMED, (BLOCKED_PHASE_A_MISSING,), None

    try:
        obj = _parse_json_object(m52a_path.resolve())
    except (OSError, ValueError, json.JSONDecodeError):
        return PHASE_A_FAILED, (BLOCKED_PHASE_A_FAILED,), None

    if str(obj.get("contract_id") or "") != M52A_CONTRACT_ID:
        return PHASE_A_FAILED, (BLOCKED_PHASE_A_FAILED,), None

    ad = str(obj.get(M52B_DIGEST_FIELD) or "").lower()
    ex = str(expected_sha256 or "").strip().lower()
    if ex and _is_hex64(ex) and ad != ex:
        blockers.append(BLOCKED_PHASE_A_FAILED)

    st = str(obj.get("adapter_status") or "")
    if st in M52A_BLOCKISH:
        phase_st = PHASE_A_BLOCKED if "blocked" in st else PHASE_A_FAILED
        blockers.append(BLOCKED_PHASE_A_FAILED)
        return phase_st, tuple(sorted(set(blockers))), obj

    if st not in M52A_READYISH:
        blockers.append(BLOCKED_PHASE_A_FAILED)
        phase_st = PHASE_A_FAILED
    else:
        phase_st = m52a_derives_phase_a_status(st)

    if blockers:
        phase_st = PHASE_A_FAILED

    return phase_st, tuple(sorted(set(blockers))), obj


def build_m53_fixture_body(*, run_id: str | None = None) -> dict[str, Any]:
    rid = run_id or f"m53_fixture_{uuid.uuid4().hex[:12]}"
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M53,
        "profile_id": PROFILE_M53,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M53,
        "emitter_module": EMITTER_MODULE_M53,
        "runner_module": RUNNER_MODULE_M53,
        "run_status": STATUS_FIXTURE_ONLY,
        "run_id": rid,
        "run_scope": RUN_SCOPE,
        "m52_binding": {
            "contract_id": CONTRACT_ID_M52B,
            "artifact_sha256": None,
            "rehearsal_status": None,
        },
        "phase_a_candidate_watch_smoke": {
            "status": PHASE_A_NOT_PERFORMED,
            "m52a_artifact_sha256": None,
            "live_sc2_executed": False,
            "candidate_adapter_label": None,
            "watchability_only": True,
        },
        "phase_b_12hour_run": {
            "twelve_hour_run_executed": False,
            "requested_wall_clock_seconds": TARGET_WALL_CLOCK_SECONDS_DEFAULT,
            "observed_wall_clock_seconds": 0.0,
            "full_wall_clock_satisfied": False,
            "training_update_count": 0,
            "checkpoints_written_total": 0,
            "checkpoints_pruned_total": 0,
            "final_step_checkpoint_persisted": False,
            "final_candidate_checkpoint_sha256": None,
            "checkpoint_retention_max_retained": 256,
        },
        "candidate_identity": {
            "candidate_checkpoint_sha256": None,
            "promotion_status": "not_promoted_candidate_only",
        },
        "operator_artifacts": {
            "transcript_captured": False,
            "telemetry_summary_captured": False,
            "checkpoint_inventory_captured": False,
            "replay_saved": False,
        },
        "honesty": _honesty_all_false(),
        "non_claims": list(NON_CLAIMS_M53),
        "blockers": [],
        "failure_reasons": [],
        "recommended_next": RECOMMENDED_NEXT_REMEDIATION,
    }


def build_m53_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_twelve_hour_operator_run_attempt_report",
        "report_version": "m53",
        "milestone": MILESTONE_LABEL_M53,
        "contract_id": CONTRACT_ID_M53,
        "profile_id": PROFILE_M53,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "run_status": sealed.get("run_status"),
    }


def build_m53_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("run_status", ""))
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return f"""# V15-M53 — 12-hour operator run attempt checklist

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

- Sealed **`{M52B_FILENAME}`** required for operator paths.
- Sealed **`{M52A_FILENAME}`** required for Phase B unless Phase A skip acknowledged.
"""


def _write_m53_bundle(
    output_dir: Path,
    sealed: dict[str, Any],
    *,
    transcript_text: str,
    telemetry_obj: dict[str, Any],
    inventory_obj: dict[str, Any],
) -> tuple[Path, ...]:
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_tr = output_dir / TRANSCRIPT_FILENAME
    p_tel = output_dir / TELEMETRY_SUMMARY_FILENAME
    p_inv = output_dir / CHECKPOINT_INVENTORY_FILENAME

    rep = build_m53_report(sealed)
    chk = build_m53_checklist_md(sealed)
    tr_pub = str(redact_paths_in_value(transcript_text))

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_tr.write_text(tr_pub, encoding="utf-8", newline="\n")
    p_tel.write_text(canonical_json_dumps(telemetry_obj), encoding="utf-8")
    p_inv.write_text(canonical_json_dumps(inventory_obj), encoding="utf-8")

    blob = (
        canonical_json_dumps(sealed)
        + canonical_json_dumps(rep)
        + chk
        + tr_pub
        + canonical_json_dumps(telemetry_obj)
        + canonical_json_dumps(inventory_obj)
    )
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M53 emission leaked path patterns")
    return (p_main, p_rep, p_chk, p_tr, p_tel, p_inv)


def emit_m53_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body = build_m53_fixture_body()
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
    inv = build_checkpoint_inventory(output_dir)
    paths = _write_m53_bundle(
        output_dir,
        sealed,
        transcript_text=(
            f"{STATUS_FIXTURE_ONLY}\n"
            "(no operator subprocess; no SC2; no checkpoint load; no 12-hour run)\n"
        ),
        telemetry_obj={"profile": PROFILE_FIXTURE_CI, "note": STATUS_FIXTURE_ONLY},
        inventory_obj=inv,
    )
    return sealed, paths


def emit_m53_operator_preflight_bundle(
    output_dir: Path,
    *,
    pre: M53PreflightOutcome,
    profile_short: str,
    wall_clock_seconds: int = TARGET_WALL_CLOCK_SECONDS_DEFAULT,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body = build_m53_fixture_body()
    body["profile"] = profile_short
    if pre.m52_obj is not None:
        body["m52_binding"] = {
            "contract_id": CONTRACT_ID_M52B,
            "artifact_sha256": pre.m52_digest,
            "rehearsal_status": pre.m52_obj.get("rehearsal_status"),
        }
    body["run_status"] = STATUS_PREFLIGHT_READY if pre.ok else STATUS_12H_BLOCKED
    body["blockers"] = list(pre.blockers)
    body["phase_b_12hour_run"]["requested_wall_clock_seconds"] = int(wall_clock_seconds)
    body["recommended_next"] = RECOMMENDED_NEXT_SUCCESS if pre.ok else RECOMMENDED_NEXT_REMEDIATION
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
    inv = build_checkpoint_inventory(output_dir)
    tel = {"profile": profile_short, "preflight_ok": pre.ok, "detail": pre.detail}
    tr = f"operator_preflight\nstatus={body['run_status']}\ndetail={pre.detail}\n"
    paths = _write_m53_bundle(
        output_dir,
        sealed,
        transcript_text=tr,
        telemetry_obj=tel,
        inventory_obj=inv,
    )
    return sealed, paths


def emit_m53_forbidden_refusal(
    output_dir: Path,
    *,
    flags: list[str],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    body = build_m53_fixture_body()
    body["run_status"] = STATUS_12H_BLOCKED
    body["blockers"] = [REFUSED_FORBIDDEN, *sorted(set(flags))]
    body["failure_reasons"] = [REFUSED_FORBIDDEN]
    body["recommended_next"] = RECOMMENDED_NEXT_REMEDIATION
    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
    inv = build_checkpoint_inventory(output_dir)
    paths = _write_m53_bundle(
        output_dir,
        sealed,
        transcript_text=f"{REFUSED_FORBIDDEN}\n{flags}\n",
        telemetry_obj={"refused_forbidden_flags": flags},
        inventory_obj=inv,
    )
    return sealed, paths


def classify_phase_b_status(
    *,
    return_code: int,
    observed_seconds: float,
    target_seconds: float,
    interrupted: bool,
    inventory: dict[str, Any],
    m28_hints: dict[str, Any],
    retention_max_retained: int,
    transcript_non_empty: bool,
    transcript_required_strict: bool,
) -> tuple[str, list[str]]:
    tol = 30.0
    wall_ok = observed_seconds + tol >= target_seconds
    has_ckpt = bool(inventory.get("checkpoint_files"))
    reasons: list[str] = []

    ck_written = int(m28_hints.get("checkpoints_written_total") or 0)
    sc2_used = bool(m28_hints.get("sc2_backed_features_used"))
    ret_max = int(m28_hints.get("checkpoint_retention_max_retained") or retention_max_retained)
    final_persisted = ck_written > 0 or bool(has_ckpt)
    training_updates = int(m28_hints.get("training_update_count") or 0)

    if interrupted:
        return STATUS_12H_INTERRUPTED_RESUME, [
            "operator_interrupt_keybrd_or_signal",
        ]
    if return_code != 0:
        return STATUS_12H_FAILED, [FAILED_SUBPROCESS]
    if transcript_required_strict and not transcript_non_empty:
        return STATUS_12H_FAILED, [FAILED_TRANSCRIPT]
    if not wall_ok:
        return STATUS_12H_INTERRUPTED_NO_RESUME, ["wall_clock_short_of_target"]
    if not transcript_non_empty:
        reasons.append(FAILED_TRANSCRIPT)
    if not has_ckpt and training_updates == 0:
        return STATUS_12H_COMPLETED_NO_CKPT, reasons or [FAILED_FINAL_CKPT]
    if has_ckpt and sc2_used and ret_max > 0 and final_persisted:
        st = STATUS_12H_COMPLETED_WARNINGS if reasons else STATUS_12H_COMPLETED_CKPT
        return st, reasons
    if not final_persisted:
        return STATUS_12H_FAILED, [FAILED_FINAL_CKPT]
    return STATUS_12H_COMPLETED_NO_CKPT, reasons


def emit_m53_phase_b_operator_receipt(
    output_dir: Path,
    *,
    repo_root: Path,
    pre: M53PreflightOutcome,
    phase_a_status: str,
    phase_a_blockers: tuple[str, ...],
    phase_a_m52a_sha: str | None,
    candidate_sha256: str,
    training_launch_file: Path | None,
    target_wall_clock_seconds: float,
    max_retained_checkpoints: int,
    subprocess_result: subprocess.CompletedProcess[str] | None,
    observed_wall_seconds: float,
    interrupted: bool,
    transcript_text: str,
    resume_from: Path | None,
    skip_phase_a_ack: bool,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    _ = repo_root
    output_dir.mkdir(parents=True, exist_ok=True)

    def _m52_bind() -> dict[str, Any]:
        return {
            "contract_id": CONTRACT_ID_M52B,
            "artifact_sha256": pre.m52_digest,
            "rehearsal_status": pre.m52_obj.get("rehearsal_status") if pre.m52_obj else None,
        }

    def _early_blocked(
        blockers: list[str],
        *,
        tr: str,
        tel: dict[str, Any],
    ) -> tuple[dict[str, Any], tuple[Path, ...]]:
        body = build_m53_fixture_body()
        body["run_status"] = STATUS_12H_BLOCKED
        body["blockers"] = blockers
        body["m52_binding"] = _m52_bind()
        sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
        inv = build_checkpoint_inventory(output_dir)
        return sealed, _write_m53_bundle(
            output_dir,
            sealed,
            transcript_text=tr,
            telemetry_obj=tel,
            inventory_obj=inv,
        )

    tcmd_txt = ""
    if training_launch_file is not None and training_launch_file.is_file():
        tcmd_txt = training_launch_file.read_text(encoding="utf-8", errors="replace")
    if not tcmd_txt.strip():
        return _early_blocked(
            ["blocked_missing_m53_training_launch_command"],
            tr=transcript_text or "blocked_missing_m53_training_launch_command\n",
            tel={"missing_launch": True},
        )

    cmd_ok, cmd_why = validate_m53_training_launch_command_text(tcmd_txt)
    if not cmd_ok:
        return _early_blocked(
            [f"blocked_training_launch_invalid:{cmd_why}"],
            tr=f"blocked_launch_command:{cmd_why}\n",
            tel={"launch_command_validation": cmd_why},
        )

    if not pre.ok:
        body = build_m53_fixture_body()
        body["run_status"] = STATUS_12H_BLOCKED
        body["blockers"] = list(pre.blockers)
        body["m52_binding"] = _m52_bind()
        sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
        inv = build_checkpoint_inventory(output_dir)
        return sealed, _write_m53_bundle(
            output_dir,
            sealed,
            transcript_text=transcript_text,
            telemetry_obj={"blocked_preflight": True},
            inventory_obj=inv,
        )

    gate_ok = (
        phase_a_status
        in (
            PHASE_A_COMPLETED,
            PHASE_A_COMPLETED_WARNINGS,
            PHASE_A_SKIPPED_ACK,
        )
        and not phase_a_blockers
    )
    if not gate_ok:
        body = build_m53_fixture_body()
        body["run_status"] = STATUS_12H_BLOCKED
        body["blockers"] = list(phase_a_blockers) or [BLOCKED_PHASE_A_MISSING]
        body["phase_a_candidate_watch_smoke"]["status"] = phase_a_status
        body["m52_binding"] = _m52_bind()
        sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
        inv = build_checkpoint_inventory(output_dir)
        return sealed, _write_m53_bundle(
            output_dir,
            sealed,
            transcript_text=transcript_text,
            telemetry_obj={"phase_a_blocked": True},
            inventory_obj=inv,
        )

    inventory = build_checkpoint_inventory(output_dir)
    m28_hints = merge_telemetry_from_m28_artifact(output_dir)
    rc = -1 if subprocess_result is None else int(subprocess_result.returncode)
    tr_nonempty = bool(str(transcript_text or "").strip())
    run_status, reasons = classify_phase_b_status(
        return_code=rc,
        observed_seconds=float(observed_wall_seconds),
        target_seconds=float(target_wall_clock_seconds),
        interrupted=interrupted,
        inventory=inventory,
        m28_hints=m28_hints,
        retention_max_retained=max_retained_checkpoints,
        transcript_non_empty=tr_nonempty,
        transcript_required_strict=True,
    )

    body = build_m53_fixture_body()
    body["profile"] = PROFILE_OPERATOR_12H_RUN
    body["run_status"] = run_status
    body["m52_binding"] = {
        "contract_id": CONTRACT_ID_M52B,
        "artifact_sha256": pre.m52_digest,
        "rehearsal_status": pre.m52_obj.get("rehearsal_status") if pre.m52_obj else None,
    }
    body["phase_a_candidate_watch_smoke"] = {
        "status": phase_a_status,
        "m52a_artifact_sha256": phase_a_m52a_sha,
        "live_sc2_executed": phase_a_status not in (PHASE_A_SKIPPED_ACK, PHASE_A_NOT_PERFORMED),
        "candidate_adapter_label": "real_candidate_live_adapter_spike"
        if phase_a_status in (PHASE_A_COMPLETED, PHASE_A_COMPLETED_WARNINGS)
        else None,
        "watchability_only": True,
        "skip_phase_a_acknowledged": bool(skip_phase_a_ack),
    }
    pbj = body["phase_b_12hour_run"]
    assert isinstance(pbj, dict)
    pbj["twelve_hour_run_executed"] = subprocess_result is not None
    pbj["requested_wall_clock_seconds"] = int(target_wall_clock_seconds)
    pbj["observed_wall_clock_seconds"] = round(float(observed_wall_seconds), 3)
    pbj["full_wall_clock_satisfied"] = bool(
        observed_wall_seconds + 30.0 >= float(target_wall_clock_seconds),
    )
    pbj["training_update_count"] = int(m28_hints.get("training_update_count") or 0)
    pbj["checkpoints_written_total"] = int(m28_hints.get("checkpoints_written_total") or 0)
    pbj["checkpoints_pruned_total"] = int(m28_hints.get("checkpoints_pruned_total") or 0)
    pbj["checkpoint_retention_max_retained"] = max_retained_checkpoints
    ck_files = inventory.get("checkpoint_files") or []
    final_sha = None
    if isinstance(ck_files, list) and ck_files:
        final_sha = str(ck_files[0].get("sha256"))
    pbj["final_candidate_checkpoint_sha256"] = final_sha
    pbj["final_step_checkpoint_persisted"] = bool(final_sha)

    body["candidate_identity"]["candidate_checkpoint_sha256"] = candidate_sha256
    body["operator_artifacts"] = {
        "transcript_captured": tr_nonempty,
        "telemetry_summary_captured": True,
        "checkpoint_inventory_captured": True,
        "replay_saved": False,
    }
    body["failure_reasons"] = reasons
    body["honesty"] = _honesty_all_false()
    body["recommended_next"] = (
        RECOMMENDED_NEXT_SUCCESS
        if run_status == STATUS_12H_COMPLETED_CKPT
        else RECOMMENDED_NEXT_REMEDIATION
    )
    if resume_from is not None:
        body["phase_b_12hour_run"]["resume_from_logical"] = resume_from.name

    sealed = seal_m53_body(cast(dict[str, Any], redact_paths_in_value(body)))
    paths = _write_m53_bundle(
        output_dir,
        sealed,
        transcript_text=transcript_text,
        telemetry_obj={
            "profile": PROFILE_OPERATOR_12H_RUN,
            "return_code": rc,
            "interrupted": interrupted,
            "m28_hints": m28_hints,
        },
        inventory_obj=inventory,
    )

    if interrupted:
        resume_dir = output_dir / "resume"
        resume_dir.mkdir(parents=True, exist_ok=True)
        rid = str(body.get("run_id") or "")
        receipt = {
            "contract_id": CONTRACT_ID_M53,
            "kind": "v15_m53_interruption_receipt",
            "run_id": rid,
            "run_status": run_status,
            "observed_wall_clock_seconds": observed_wall_seconds,
        }
        (resume_dir / "v15_m53_interruption_receipt.json").write_text(
            canonical_json_dumps(receipt),
            encoding="utf-8",
        )

    return sealed, paths


def run_phase_a_m52a_subprocess(
    *,
    repo_root: Path,
    m51_json: Path,
    smoke_out: Path,
    candidate_checkpoint: Path,
    expected_candidate_sha256: str,
    sc2_root: Path,
    map_path: Path,
    device: str,
    game_step: int,
    max_game_steps: int,
    save_replay: bool,
    operator_note: Path | None,
) -> subprocess.CompletedProcess[str]:
    cmd: list[str] = [
        sys.executable,
        "-m",
        "starlab.v15.run_v15_m52_candidate_live_adapter_spike",
        GUARD_ALLOW_OPERATOR_LOCAL,
        GUARD_M52A_AUTHORIZE_ADAPTER_SPIKE,
        "--m51-watchability-json",
        str(m51_json.resolve()),
        "--output-dir",
        str(smoke_out.resolve()),
        "--candidate-checkpoint-path",
        str(candidate_checkpoint.resolve()),
        "--expected-candidate-checkpoint-sha256",
        str(expected_candidate_sha256),
        "--sc2-root",
        str(sc2_root.resolve()),
        "--map-path",
        str(map_path.resolve()),
        "--device",
        str(device),
        "--game-step",
        str(int(game_step)),
        "--max-game-steps",
        str(int(max_game_steps)),
    ]
    if save_replay:
        cmd.append("--save-replay")
    if operator_note is not None:
        cmd.extend(["--operator-note", str(operator_note.resolve())])
    return subprocess.run(
        cmd,
        cwd=str(repo_root.resolve()),
        capture_output=True,
        text=True,
        check=False,
    )


def run_phase_b_training_subprocess(
    launch_file: Path,
    *,
    repo_root: Path,
    target_wall_clock_seconds: float,
    transcript_path: Path,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    return run_operator_subprocess(
        launch_file,
        repo_root=repo_root,
        target_wall_clock_seconds=target_wall_clock_seconds,
        transcript_path=transcript_path,
    )


__all__ = [
    "M53PreflightOutcome",
    "BLOCKED_CKPT_MISSING",
    "BLOCKED_CKPT_SHA",
    "BLOCKED_DISK_INSUFFICIENT",
    "BLOCKED_DISK_UNKNOWN",
    "BLOCKED_DUAL_12H",
    "BLOCKED_DUAL_SMOKE",
    "BLOCKED_MAP",
    "BLOCKED_M52_INVALID",
    "BLOCKED_M52_MISSING",
    "BLOCKED_M52_NOT_READY",
    "BLOCKED_M52_SHA",
    "BLOCKED_PHASE_A_FAILED",
    "BLOCKED_PHASE_A_MISSING",
    "BLOCKED_RETENTION",
    "BLOCKED_SC2",
    "BLOCKED_STOP_RESUME",
    "FAILED_FINAL_CKPT",
    "FAILED_SUBPROCESS",
    "FAILED_TRANSCRIPT",
    "PHASE_A_SKIPPED_ACK",
    "REFUSED_FORBIDDEN",
    "build_m53_checklist_md",
    "build_m53_fixture_body",
    "build_m53_report",
    "classify_phase_b_status",
    "emit_m53_fixture_ci",
    "emit_m53_forbidden_refusal",
    "emit_m53_operator_preflight_bundle",
    "emit_m53_phase_b_operator_receipt",
    "evaluate_m53_operator_preflight",
    "load_m52a_phase_gate",
    "m52a_derives_phase_a_status",
    "m52b_seal_ok",
    "run_phase_a_m52a_subprocess",
    "run_phase_b_training_subprocess",
    "seal_m53_body",
    "validate_m53_training_launch_command_text",
]
