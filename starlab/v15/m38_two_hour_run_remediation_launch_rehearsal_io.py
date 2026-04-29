"""V15-M38 remediation / launch rehearsal — sealed JSON, runbook, launch command."""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_io import (
    _has_explicit_checkpoint_volume_controls,
)
from starlab.v15.m37_two_hour_run_blocker_discovery_models import CONTRACT_ID_M37_DISCOVERY
from starlab.v15.m38_two_hour_run_remediation_launch_rehearsal_models import (
    CHECKLIST_FILENAME,
    CONTRACT_ID_M38,
    EMITTER_MODULE_M38,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    LAUNCH_COMMAND_FILENAME,
    M39_MAX_WALL_CLOCK_MINUTES,
    M39_TARGET_WALL_CLOCK_SECONDS,
    MILESTONE_LABEL_M38,
    NON_CLAIMS_M38,
    OPTIONAL_ENRICHED,
    OPTIONAL_NOT_SUPPLIED,
    PROFILE_FIXTURE_CI,
    PROFILE_M38,
    PROFILE_OPERATOR_PREFLIGHT,
    PROFILE_OPERATOR_REHEARSAL,
    RECOMMENDED_NEXT,
    REPORT_FILENAME,
    RUNBOOK_FILENAME,
    SCHEMA_VERSION,
    STATUS_BLOCKED_CHECKPOINT,
    STATUS_BLOCKED_CRITICAL,
    STATUS_BLOCKED_NO_M37,
    STATUS_BLOCKED_RUNNER,
    STATUS_COMPLETED_DEFERRED,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STATUS_READY_M39,
    STOP_RESUME_CARD_FILENAME,
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
    raw: dict[str, Any], *, digest_key: str = GATE_ARTIFACT_DIGEST_FIELD
) -> bool:
    seal_in = raw.get(digest_key)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != digest_key}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _claim_flags_false() -> dict[str, Any]:
    return {
        "two_hour_run_executed": False,
        "benchmark_execution_performed": False,
        "benchmark_pass_claimed": False,
        "strength_evaluated": False,
        "checkpoint_promoted": False,
        "scorecard_results_claimed": False,
        "xai_executed": False,
        "human_panel_executed": False,
        "showcase_released": False,
        "v2_authorized": False,
        "t2_authorized": False,
        "t3_authorized": False,
    }


def seal_m38_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _m28_accepts_wall_clock(repo_root: Path) -> bool:
    p = repo_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py"
    if not p.is_file():
        return False
    return "--max-wall-clock-minutes" in p.read_text(encoding="utf-8", errors="replace")


def _m28_accepts_max_retained(repo_root: Path) -> bool:
    p = repo_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py"
    if not p.is_file():
        return False
    t = p.read_text(encoding="utf-8", errors="replace")
    return "--max-retained-checkpoints" in t or "max_retained_checkpoints" in t


def _retention_implementation_ok(repo_root: Path) -> bool:
    train = repo_root / "starlab" / "v15" / "sc2_backed_t1_training_execution.py"
    if not train.is_file():
        return False
    t = train.read_text(encoding="utf-8", errors="replace")
    return (
        "max_retained_checkpoints" in t
        and "checkpoints_pruned_total" in t
        and "_apply_checkpoint_retention" in t
    )


def _checkpoint_volume_remediated(repo_root: Path) -> bool:
    return (
        _has_explicit_checkpoint_volume_controls(repo_root)
        and _m28_accepts_max_retained(repo_root)
        and _retention_implementation_ok(repo_root)
    )


def _collect_blocker_resolutions(
    *,
    m37: dict[str, Any] | None,
    retention_ok: bool,
    runner_ok: bool,
) -> tuple[list[dict[str, Any]], bool, bool]:
    resolutions: list[dict[str, Any]] = []
    ck_unresolved = False
    runner_unresolved = False

    blockers: list[dict[str, Any]] = []
    if m37 is not None:
        raw = m37.get("blockers")
        if isinstance(raw, list):
            blockers = [b for b in raw if isinstance(b, dict)]

    seen: set[str] = set()

    for b in blockers:
        bid = str(b.get("blocker_id") or "")
        if not bid or bid in seen:
            continue
        seen.add(bid)
        if bid == "checkpoint_cadence_too_high":
            if retention_ok:
                resolutions.append(
                    {
                        "blocker_id": bid,
                        "status": "remediated",
                        "rationale": (
                            "Repo implements checkpoint retention / cadence caps on the M28 path "
                            "(max_retained_checkpoints + pruning telemetry)."
                        ),
                    },
                )
            else:
                ck_unresolved = True
                resolutions.append(
                    {
                        "blocker_id": bid,
                        "status": "still_open",
                        "rationale": "Checkpoint volume controls missing or incomplete.",
                    },
                )
            continue
        if bid == "m29_wrapper_name_or_contract_too_30min_specific":
            if runner_ok:
                resolutions.append(
                    {
                        "blocker_id": bid,
                        "status": "remediated",
                        "rationale": (
                            "M39 launch freezes direct M28 invocation with 120-minute wall clock; "
                            "M29 horizon classifier is not used for M39 receipts."
                        ),
                    },
                )
            else:
                runner_unresolved = True
                resolutions.append(
                    {
                        "blocker_id": bid,
                        "status": "still_open",
                        "rationale": "M28 wall-clock CLI not available for 7200s-class launch.",
                    },
                )
            continue
        sev = str(b.get("severity") or "")
        st = str(b.get("status") or "")
        if st in ("resolved", "closed", "waived"):
            resolutions.append(
                {"blocker_id": bid, "status": "deferred", "rationale": "Upstream M37 closed."},
            )
            continue
        resolutions.append(
            {
                "blocker_id": bid,
                "status": "still_open" if sev in ("critical", "high") else "deferred_noncritical",
                "rationale": str(b.get("evidence") or "carried from M37"),
            },
        )

    return resolutions, ck_unresolved, runner_unresolved


def _critical_high_open(m37: dict[str, Any] | None, resolutions: list[dict[str, Any]]) -> bool:
    if m37 is None:
        return False
    rs_ids = {str(r["blocker_id"]) for r in resolutions if r.get("status") == "still_open"}
    for b in m37.get("blockers") or []:
        if not isinstance(b, dict):
            continue
        bid = str(b.get("blocker_id") or "")
        if bid not in rs_ids:
            continue
        if str(b.get("severity") or "") in ("critical", "high"):
            return True
    return False


def _storage_blocker_from_m37(m37: dict[str, Any] | None) -> bool:
    if m37 is None:
        return False
    for b in m37.get("blockers") or []:
        if not isinstance(b, dict):
            continue
        if str(b.get("blocker_id") or "") == "disk_free_below_threshold":
            return str(b.get("status") or "") != "resolved"
        if (
            str(b.get("category") or "") == "disk_output"
            and str(b.get("severity") or "") == "critical"
        ):
            return True
    return False


def _build_checkpoint_retention_policy(repo_root: Path) -> dict[str, Any]:
    return {
        "checkpoint_interval_control": "checkpoint_cadence_updates_cli_on_m28",
        "max_retained_checkpoints_cli": (
            "m28 --max-retained-checkpoints (default 128; STARLAB_MAX_RETAINED_CHECKPOINTS)"
        ),
        "checkpoint_retention_code_module": "starlab.v15.sc2_backed_t1_training_execution",
        "always_persist_final_step": True,
        "telemetry_fields": (
            "checkpoints_written_total, checkpoints_pruned_total, checkpoint_retention_max_retained"
        ),
        "code_level_retention_enforced": _retention_implementation_ok(repo_root),
        "m28_launch_accepts_max_retained_flag": _m28_accepts_max_retained(repo_root),
    }


def _build_runner_compatibility(repo_root: Path) -> dict[str, Any]:
    m28_ok = _m28_accepts_wall_clock(repo_root)
    return {
        "m28_accepts_max_wall_clock_minutes_cli": m28_ok,
        "m39_recommended_launch_path": "direct_m28_two_hour_operator_run",
        "m29_outcome_classifier_not_used_for_m39": True,
        "7200_second_wall_clock_seconds": M39_TARGET_WALL_CLOCK_SECONDS,
        "7200_second_equivalent_wall_clock_minutes": M39_MAX_WALL_CLOCK_MINUTES,
    }


def _telemetry_plan_stub() -> dict[str, Any]:
    return {
        "nvidia_smi_sampling": (
            "Operator: nvidia-smi dmon or 60s interval CSV alongside transcript."
        ),
        "transcript_path": "out/v15_m39_2hour_operator_run/<run_id>/m39_operator_transcript.txt",
        "retention_counters_in_training_attempt": True,
    }


def _stop_resume_plan_stub() -> dict[str, Any]:
    return {
        "interrupt_classification": "keyboard_interrupt_vs_wall_budget_vs_process_kill",
        "partial_run_label": "PARTIAL_RUN_OPERATOR_INTERRUPT",
        "resume_posture": (
            "M28 does not auto-resume; relaunch with fresh RUN_ID or manual lineage note."
        ),
        "receipt_fields": (
            "early_stop_reason, wall_clock_seconds, checkpoint_paths_with_sha256 tail"
        ),
    }


def _storage_policy_stub() -> dict[str, Any]:
    return {
        "public_output_root_pattern": "out/v15_m39_2hour_operator_run/<run_id>/",
        "checkpoint_subdir": "checkpoints/",
        "backup_posture": "Operator-local; never commit out/ or weights.",
        "gitignore_alignment": "out/, *.pt, docs/company_secrets/",
    }


def frozen_m39_launch_command_text() -> str:
    return (
        "# STARLAB V15-M39 — frozen launch command (DO NOT RUN IN M38 CI)\r\n"
        "# Replace <OPERATOR_SEALED_M27_JSON> and <RUN_ID>; use repo .venv on Windows.\r\n"
        "\r\n"
        r".\.venv\Scripts\python.exe -m starlab.v15.run_v15_m28_sc2_backed_t1_candidate_training ^"
        "\r\n"
        "  --allow-operator-local-execution ^\r\n"
        "  --authorize-sc2-backed-t1-candidate-training ^\r\n"
        "  --m27-sc2-rollout-json <OPERATOR_SEALED_M27_JSON> ^\r\n"
        r"  --output-dir out\v15_m39_2hour_operator_run\<RUN_ID>\ ^"
        "\r\n"
        f"  --max-wall-clock-minutes {M39_MAX_WALL_CLOCK_MINUTES:g} ^\r\n"
        f"  --min-wall-clock-minutes {M39_MAX_WALL_CLOCK_MINUTES:g} ^\r\n"
        "  --checkpoint-cadence-updates 500 ^\r\n"
        "  --max-retained-checkpoints 256 ^\r\n"
        "  --require-full-wall-clock ^\r\n"
        "  --disable-loss-floor-early-stop ^\r\n"
        "  --continue-after-checkpoint ^\r\n"
        "  --device auto\r\n"
        "\r\n"
        "# Optional env override for default cap:\r\n"
        "# set STARLAB_MAX_RETAINED_CHECKPOINTS=256\r\n"
        "\r\n"
        "# M38/M39 non-claims: not benchmark pass; not strength; not promotion; two-hour only.\r\n"
    )


def build_m39_launch_runbook_md(*, rehearsal_status: str, m39_launch_ready: bool) -> str:
    return f"""# V15-M39 launch runbook (frozen draft)

**Emitted by:** `V15-M38` — *2-Hour Run Remediation & Launch Rehearsal*
**M38 rehearsal status:** `{rehearsal_status}`
**M39 launch ready (governed):** `{m39_launch_ready}`

## Purpose

Operator-local **7200-second** (120-minute) SC2-backed T1 continuation using **direct M28**
invocation. This runbook does **not** execute training inside CI.

## Preconditions

- Sealed M27 rollout JSON path available.
- CUDA / SC2 operator posture verified outside this document.
- Disk budget for `out/v15_m39_2hour_operator_run/<run_id>/`.
- Checkpoint retention: use `--max-retained-checkpoints` and optional
  `STARLAB_MAX_RETAINED_CHECKPOINTS`.

## Launch

See **`{LAUNCH_COMMAND_FILENAME}`** beside this artifact.
Do not substitute M29 for evidence classification.

## Telemetry

- Capture `nvidia-smi` or equivalent power/thermal samples per operator policy.
- Preserve `v15_sc2_backed_t1_candidate_training.json` sealed artifact.

## Stop / partial run

See **`{STOP_RESUME_CARD_FILENAME}`**.

## Public / private boundary

- Do not commit `out/`, weights, private paths, or `docs/company_secrets/`.

## Non-claims

- Not a benchmark pass; not T2/T3; not strength evaluation; not checkpoint promotion; not XAI;
  not human-panel; not showcase; not v2.
"""


def build_stop_resume_card_md() -> str:
    return """# V15-M39 operator stop / resume card

## Stop (graceful)

- Prefer interrupt once; record wall-clock and last `training_update_count` from transcript.

## Partial run classification

| Signal | Label |
| --- | --- |
| Wall budget hit | `wall_clock_budget` |
| Keyboard interrupt | `operator_interrupt` (manual note) |
| Process killed | `hard_kill` (manual note) |

## Resume

- **No automatic resume** in M28: start a new `RUN_ID` or document manual continuation policy
  locally.
- Bind new receipts under a fresh output directory to avoid seal collisions.

## M38 note

M38 rehearsal only validates filesystem / command wiring — not the full 2-hour run.
"""


def build_m38_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("rehearsal_status", ""))
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return f"""# V15-M38 — Remediation & launch rehearsal checklist

**Status:** `{st}`

## Non-claims

{nc_lines}

## Upstream

- **M37 sealed JSON:** required for operator preflight.

## Artifacts

- `{FILENAME_MAIN_JSON}`
- `{REPORT_FILENAME}`
- `{CHECKLIST_FILENAME}`
- `{RUNBOOK_FILENAME}`
- `{LAUNCH_COMMAND_FILENAME}`
- `{STOP_RESUME_CARD_FILENAME}`
"""


def build_m38_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_two_hour_run_remediation_launch_rehearsal_report",
        "report_version": "m38",
        "milestone": MILESTONE_LABEL_M38,
        "contract_id": CONTRACT_ID_M38,
        "profile_id": PROFILE_M38,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "rehearsal_status": sealed.get("rehearsal_status"),
        "m39_launch_ready": sealed.get("m39_launch_ready"),
    }


def build_fixture_body(repo_root: Path) -> dict[str, Any]:
    ck_policy = _build_checkpoint_retention_policy(repo_root)
    runner = _build_runner_compatibility(repo_root)
    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M38,
        "profile_id": PROFILE_M38,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M38,
        "emitter_module": EMITTER_MODULE_M38,
        "rehearsal_status": STATUS_FIXTURE_SCHEMA_ONLY,
        "upstream_bindings": {
            "m37_blocker_discovery": {
                "binding_status": OPTIONAL_NOT_SUPPLIED,
                "expected_contract_id": CONTRACT_ID_M37_DISCOVERY,
                "artifact_sha256": None,
            },
            "m37_remediation_map_md": OPTIONAL_NOT_SUPPLIED,
            "m37_m39_runbook_draft_md": OPTIONAL_NOT_SUPPLIED,
        },
        "blocker_resolution_summary": [],
        "checkpoint_retention_policy": ck_policy,
        "runner_compatibility": runner,
        "storage_policy": _storage_policy_stub(),
        "telemetry_plan": _telemetry_plan_stub(),
        "stop_resume_plan": _stop_resume_plan_stub(),
        "operator_local_rehearsal": {
            "rehearsal_performed": False,
            "rehearsal_seconds_budget": None,
            "rehearsal_notes": None,
        },
        "m39_launch_command_frozen": True,
        "m39_launch_command_filename": LAUNCH_COMMAND_FILENAME,
        "m39_launch_ready": False,
        "claim_flags": _claim_flags_false(),
        "non_claims": list(NON_CLAIMS_M38),
        "recommended_next": RECOMMENDED_NEXT,
    }


def emit_m38_fixture(
    output_dir: Path,
    *,
    repo_root: Path | None = None,
) -> tuple[dict[str, Any], Path, Path, Path, Path, Path, Path]:
    rr = repo_root or Path(__file__).resolve().parents[2]
    body_pre = build_fixture_body(rr)
    sealed = seal_m38_body(redact_paths_in_value(body_pre))
    if not isinstance(sealed, dict):
        raise TypeError("expected dict")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = _write_m38_bundle(output_dir, sealed)
    return (sealed, *paths)


def _write_m38_bundle(
    output_dir: Path, sealed: dict[str, Any]
) -> tuple[Path, Path, Path, Path, Path, Path]:
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_run = output_dir / RUNBOOK_FILENAME
    p_cmd = output_dir / LAUNCH_COMMAND_FILENAME
    p_card = output_dir / STOP_RESUME_CARD_FILENAME

    rep = build_m38_report(sealed)
    chk = build_m38_checklist_md(sealed)
    rb = build_m39_launch_runbook_md(
        rehearsal_status=str(sealed.get("rehearsal_status", "")),
        m39_launch_ready=bool(sealed.get("m39_launch_ready")),
    )
    cmd = frozen_m39_launch_command_text()
    card = build_stop_resume_card_md()

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_run.write_text(rb, encoding="utf-8", newline="\n")
    p_cmd.write_text(cmd, encoding="utf-8", newline="\n")
    p_card.write_text(card, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk + rb + cmd + card
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M38 emission leaked path patterns")
    return (p_main, p_rep, p_chk, p_run, p_cmd, p_card)


def emit_m38_operator_preflight(
    output_dir: Path,
    *,
    repo_root: Path,
    m37_blocker_discovery_json: Path,
    m37_remediation_map_md: Path | None = None,
    m37_m39_runbook_draft_md: Path | None = None,
) -> tuple[dict[str, Any], Path, Path, Path, Path, Path, Path]:
    m37_obj = _parse_json_object(m37_blocker_discovery_json.resolve())
    if str(m37_obj.get("contract_id") or "") != CONTRACT_ID_M37_DISCOVERY:
        body_bad: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_M38,
            "profile_id": PROFILE_M38,
            "profile": PROFILE_OPERATOR_PREFLIGHT,
            "milestone": MILESTONE_LABEL_M38,
            "emitter_module": EMITTER_MODULE_M38,
            "rehearsal_status": STATUS_BLOCKED_NO_M37,
            "upstream_bindings": {
                "m37_blocker_discovery": {
                    "binding_status": "invalid_contract",
                    "expected_contract_id": CONTRACT_ID_M37_DISCOVERY,
                    "artifact_sha256": None,
                },
                "m37_remediation_map_md": OPTIONAL_NOT_SUPPLIED,
                "m37_m39_runbook_draft_md": OPTIONAL_NOT_SUPPLIED,
            },
            "blocker_resolution_summary": [],
            "checkpoint_retention_policy": _build_checkpoint_retention_policy(repo_root),
            "runner_compatibility": _build_runner_compatibility(repo_root),
            "storage_policy": _storage_policy_stub(),
            "telemetry_plan": _telemetry_plan_stub(),
            "stop_resume_plan": _stop_resume_plan_stub(),
            "operator_local_rehearsal": {
                "rehearsal_performed": False,
                "rehearsal_seconds_budget": None,
                "rehearsal_notes": None,
            },
            "m39_launch_command_frozen": True,
            "m39_launch_command_filename": LAUNCH_COMMAND_FILENAME,
            "m39_launch_ready": False,
            "claim_flags": _claim_flags_false(),
            "non_claims": list(NON_CLAIMS_M38),
            "recommended_next": RECOMMENDED_NEXT,
        }
        sealed_bad = seal_m38_body(redact_paths_in_value(body_bad))
        output_dir.mkdir(parents=True, exist_ok=True)
        return (sealed_bad, *_write_m38_bundle(output_dir, sealed_bad))

    if not _canonical_seal_ok(m37_obj):
        raise ValueError("M37 blocker discovery JSON seal mismatch")

    bind_sha = str(m37_obj.get(GATE_ARTIFACT_DIGEST_FIELD) or "")
    map_st = OPTIONAL_NOT_SUPPLIED
    draft_st = OPTIONAL_NOT_SUPPLIED
    map_note = None
    draft_note = None
    if m37_remediation_map_md is not None and m37_remediation_map_md.is_file():
        map_st = OPTIONAL_ENRICHED
        map_note = "remediation_map_md_bytes_read_for_operator_reporting_only"
    if m37_m39_runbook_draft_md is not None and m37_m39_runbook_draft_md.is_file():
        draft_st = OPTIONAL_ENRICHED
        draft_note = "m39_runbook_draft_md_bytes_read_for_operator_reporting_only"

    retention_ok = _checkpoint_volume_remediated(repo_root)
    runner_ok = _m28_accepts_wall_clock(repo_root)
    resolutions, ck_open, runner_open = _collect_blocker_resolutions(
        m37=m37_obj,
        retention_ok=retention_ok,
        runner_ok=runner_ok,
    )

    storage_bad = _storage_blocker_from_m37(m37_obj)
    crit = _critical_high_open(m37_obj, resolutions)

    rehearsal_status = STATUS_READY_M39
    m39_ready = True

    if ck_open:
        rehearsal_status = STATUS_BLOCKED_CHECKPOINT
        m39_ready = False
    elif runner_open:
        rehearsal_status = STATUS_BLOCKED_RUNNER
        m39_ready = False
    elif crit or storage_bad:
        rehearsal_status = STATUS_BLOCKED_CRITICAL
        m39_ready = False
    elif any(r.get("status") == "deferred_noncritical" for r in resolutions):
        rehearsal_status = STATUS_COMPLETED_DEFERRED

    summary = (
        m37_obj.get("readiness_summary")
        if isinstance(m37_obj.get("readiness_summary"), dict)
        else {}
    )
    cbc = int(summary.get("critical_blocker_count") or 0) if summary else 0
    hbc = int(summary.get("high_blocker_count") or 0) if summary else 0
    if cbc > 0 or hbc > 0:
        if rehearsal_status == STATUS_READY_M39:
            rehearsal_status = STATUS_BLOCKED_CRITICAL
            m39_ready = False

    ck_policy = dict(_build_checkpoint_retention_policy(repo_root))
    ck_policy["m37_checkpoint_pruned_total_hint"] = 0
    ck_policy["m37_checkpoint_written_total_hint"] = 0

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M38,
        "profile_id": PROFILE_M38,
        "profile": PROFILE_OPERATOR_PREFLIGHT,
        "milestone": MILESTONE_LABEL_M38,
        "emitter_module": EMITTER_MODULE_M38,
        "rehearsal_status": rehearsal_status,
        "upstream_bindings": {
            "m37_blocker_discovery": {
                "binding_status": "bound_sealed_json",
                "contract_id": CONTRACT_ID_M37_DISCOVERY,
                "resolved_path_digest": (bind_sha[:16] + "…") if bind_sha else None,
                "artifact_sha256": bind_sha if _is_hex64(bind_sha) else None,
            },
            "m37_remediation_map_md": map_st,
            "m37_remediation_map_note": map_note,
            "m37_m39_runbook_draft_md": draft_st,
            "m37_m39_runbook_draft_note": draft_note,
        },
        "blocker_resolution_summary": resolutions,
        "checkpoint_retention_policy": ck_policy,
        "runner_compatibility": _build_runner_compatibility(repo_root),
        "storage_policy": _storage_policy_stub(),
        "telemetry_plan": _telemetry_plan_stub(),
        "stop_resume_plan": _stop_resume_plan_stub(),
        "operator_local_rehearsal": {
            "rehearsal_performed": False,
            "rehearsal_seconds_budget": None,
            "rehearsal_notes": None,
        },
        "m39_launch_command_frozen": True,
        "m39_launch_command_filename": LAUNCH_COMMAND_FILENAME,
        "m39_launch_ready": m39_ready,
        "claim_flags": _claim_flags_false(),
        "non_claims": list(NON_CLAIMS_M38),
        "recommended_next": RECOMMENDED_NEXT,
    }

    sealed = seal_m38_body(redact_paths_in_value(body))
    output_dir.mkdir(parents=True, exist_ok=True)
    return (sealed, *_write_m38_bundle(output_dir, sealed))


def emit_m38_operator_rehearsal(
    output_dir: Path,
    *,
    repo_root: Path,
    m37_blocker_discovery_json: Path,
    max_rehearsal_seconds: float,
    m37_remediation_map_md: Path | None = None,
    m37_m39_runbook_draft_md: Path | None = None,
) -> tuple[dict[str, Any], Path, Path, Path, Path, Path, Path]:
    sealed_base, p_main, p_rep, p_chk, p_run, p_cmd, p_card = emit_m38_operator_preflight(
        output_dir,
        repo_root=repo_root,
        m37_blocker_discovery_json=m37_blocker_discovery_json,
        m37_remediation_map_md=m37_remediation_map_md,
        m37_m39_runbook_draft_md=m37_m39_runbook_draft_md,
    )
    t0 = time.monotonic()
    out_root = output_dir / "m38_rehearsal_scratch"
    out_root.mkdir(parents=True, exist_ok=True)
    probe = out_root / "rehearsal_write_probe.txt"
    probe.write_text("m38_rehearsal_only\n", encoding="utf-8")
    nv_ok = False
    try:
        proc = subprocess.run(
            ["nvidia-smi", "-L"],
            capture_output=True,
            text=True,
            timeout=min(15.0, max(1.0, max_rehearsal_seconds)),
            check=False,
        )
        nv_ok = proc.returncode == 0
    except OSError:
        nv_ok = False
    elapsed = time.monotonic() - t0

    sealed = dict(sealed_base)
    sealed["profile"] = PROFILE_OPERATOR_REHEARSAL
    orch = sealed.get("operator_local_rehearsal")
    if not isinstance(orch, dict):
        orch = {}
    orch = dict(orch)
    orch["rehearsal_performed"] = True
    orch["rehearsal_seconds_budget"] = float(max_rehearsal_seconds)
    orch["rehearsal_notes"] = {
        "scratch_dir_relative": "m38_rehearsal_scratch",
        "write_probe_ok": probe.is_file(),
        "nvidia_smi_available": nv_ok,
        "elapsed_seconds": round(elapsed, 3),
        "non_claim": "rehearsal_only_not_two_hour_run",
    }
    sealed["operator_local_rehearsal"] = orch
    sealed = seal_m38_body(redact_paths_in_value(sealed))
    _write_m38_bundle(output_dir, sealed)
    return (sealed, p_main, p_rep, p_chk, p_run, p_cmd, p_card)
