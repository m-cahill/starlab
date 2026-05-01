"""V15-M52B — twelve-hour launch rehearsal IO (no execution)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m51_live_candidate_watchability_harness_io import sha256_hex_file_optional
from starlab.v15.m52_candidate_live_adapter_spike_io import emit_m52a_fixture_ci
from starlab.v15.m52_candidate_live_adapter_spike_models import (
    FILENAME_MAIN_JSON as M52A_FILENAME,
)
from starlab.v15.m52_twelve_hour_launch_rehearsal_models import (
    BLOCKED_CKPT_SHA,
    BLOCKED_DISK_INSUFFICIENT,
    BLOCKED_DISK_UNKNOWN,
    BLOCKED_M52A_NOT_READY,
    BLOCKED_MAP,
    BLOCKED_MISSING_CKPT,
    BLOCKED_MISSING_M52A,
    BLOCKED_RETENTION,
    BLOCKED_SC2,
    CHECKLIST_FILENAME,
    CONTRACT_ID_M52A_UPSTREAM,
    CONTRACT_ID_M52B,
    DIGEST_FIELD,
    DISK_FIXTURE_NOT_INSPECTED,
    EMITTER_MODULE_M52B,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_12H,
    LAUNCH_CMD_FILENAME,
    MILESTONE_LABEL_M52B,
    NON_CLAIMS_M52B,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_FIXTURE_CI,
    PROFILE_ID_OPERATOR_DECLARED,
    PROFILE_ID_OPERATOR_PREFLIGHT,
    PROFILE_M52B_SURFACE,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REFUSED_CONTRACT,
    REFUSED_FORBIDDEN,
    REFUSED_M52A_SHA,
    REPORT_FILENAME,
    ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
    RUNBOOK_FILENAME,
    SCHEMA_VERSION,
    STATUS_BLOCKED,
    STATUS_FIXTURE_ONLY,
    STATUS_READY,
    STATUS_READY_WARNINGS,
    STATUS_REFUSED,
    STOP_RESUME_FILENAME,
)

M52A_READYISH: frozenset[str] = frozenset(
    {
        "candidate_live_adapter_preflight_ready",
        "candidate_live_adapter_preflight_ready_with_warnings",
        "candidate_live_adapter_spike_completed",
        "candidate_live_adapter_spike_completed_with_warnings",
    }
)

M52A_BLOCKISH: frozenset[str] = frozenset(
    {
        "candidate_live_adapter_preflight_blocked",
        "candidate_live_adapter_spike_blocked",
        "candidate_live_adapter_spike_failed",
    }
)


def _parse_json_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def _seal_ok(raw: dict[str, Any]) -> bool:
    seal_in = raw.get(DIGEST_FIELD)
    if seal_in is None:
        return False
    wo = {k: v for k, v in raw.items() if k != DIGEST_FIELD}
    computed = sha256_hex_of_canonical_json(wo)
    return str(seal_in).lower() == computed.lower()


def _sha_like(v: object) -> bool:
    if not isinstance(v, str):
        return False
    s = v.strip().lower()
    return len(s) == 64 and all(c in "0123456789abcdef" for c in s)


def _profile_catalog_id(short_profile: str) -> str:
    if short_profile == PROFILE_FIXTURE_CI:
        return PROFILE_ID_FIXTURE_CI
    if short_profile == PROFILE_OPERATOR_PREFLIGHT:
        return PROFILE_ID_OPERATOR_PREFLIGHT
    if short_profile == PROFILE_OPERATOR_DECLARED:
        return PROFILE_ID_OPERATOR_DECLARED
    return PROFILE_M52B_SURFACE


def seal_m52b_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[DIGEST_FIELD] = digest
    return sealed


def build_m52b_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != DIGEST_FIELD}
    return {
        "report_kind": "v15_twelve_hour_launch_rehearsal_report",
        "report_version": "m52b",
        "milestone": MILESTONE_LABEL_M52B,
        "contract_id": CONTRACT_ID_M52B,
        "profile_id": sealed.get("profile_id"),
        DIGEST_FIELD: sha256_hex_of_canonical_json(base),
        "rehearsal_status": sealed.get("rehearsal_status"),
    }


def _freeze_m53_launch_command() -> str:
    return (
        "python -m starlab.v15.run_v15_m53_twelve_hour_operator_run_attempt \\\n"
        "  --phase full-12hour \\\n"
        "  --m52-launch-rehearsal-json <path-to-v15_twelve_hour_launch_rehearsal.json> \\\n"
        "  --m52a-adapter-spike-json <path-to-v15_candidate_live_adapter_spike.json> \\\n"
        "  --m53-training-launch-command <path-to-resolved-m28-training-launch.txt> \\\n"
        "  --candidate-checkpoint-path <path-to-candidate.pt> \\\n"
        "  --expected-candidate-checkpoint-sha256 <sha256> \\\n"
        '  --sc2-root "<SC2_ROOT>" \\\n'
        '  --map-path "<MAP_PATH>" \\\n'
        "  --wall-clock-seconds 43200 \\\n"
        "  --max-retained-checkpoints 256 \\\n"
        "  --output-dir out/v15_m53/<run_id> \\\n"
        "  --allow-operator-local-execution \\\n"
        "  --authorize-12-hour-operator-run\n"
    )


def _runbook_md() -> str:
    return "\n".join(
        [
            "# V15-M53 twelve-hour operator run — runbook (frozen by M52B rehearsal)",
            "",
            "This runbook is a planning artifact from **V15-M52B**. It does **not** execute "
            "the 12-hour run. **V15-M53** owns execution.",
            "",
            "## Preconditions",
            "",
            "- Sealed `v15_twelve_hour_launch_rehearsal.json` from this rehearsal.",
            "- Candidate checkpoint path + SHA256 verified out-of-band.",
            "- SC2 install + map path available on operator host.",
            "- Disk budget cleared per rehearsal `disk_budget` block.",
            "",
            "## Launch",
            "",
            "- Use `v15_m53_launch_command.txt` as the canonical command template.",
            "- Replace placeholders only; do not add benchmark or promotion flags unless a future "
            "milestone explicitly authorizes them.",
            "",
            "## During run",
            "",
            "- Follow `v15_m53_operator_stop_resume_card.md`.",
            "- Preserve checkpoint manifests and training receipts per retention policy.",
            "",
            "## After run",
            "",
            "- Emit M53 receipts, update private audit notes, and sync public ledgers only with "
            "governed summaries (no raw private paths).",
            "",
            "---",
            "",
            "V15-M52 rehearses and freezes the governed 12-hour operator-run path. It does not "
            "execute the 12-hour run; V15-M53 owns the 12-hour operator attempt.",
            "",
        ]
    )


def _stop_resume_card_md() -> str:
    return "\n".join(
        [
            "# V15-M53 operator stop / resume card",
            "",
            "## Graceful stop",
            "",
            "- Stop the Python orchestrator first (Ctrl+C or equivalent); allow SC2 to exit "
            "cleanly when possible.",
            "- Do not delete partial checkpoints until you capture them in a checkpoint inventory "
            "JSON or list with paths + SHA256.",
            "",
            "## Preserve",
            "",
            "- Latest known-good checkpoint and its sidecar metadata.",
            "- `training_manifest`-class files, logs, and stop/resume receipts emitted by the "
            "runner.",
            "- This rehearsal JSON and frozen launch command snapshot.",
            "",
            "## Do not delete",
            "",
            "- Parent checkpoint lineage blobs until promotion/archival policy says otherwise.",
            "- Sealed milestone JSON upstream of the run without recording hashes elsewhere.",
            "",
            "## Resume vs interrupted",
            "",
            "- If the process exited cleanly with a resume token or manifest entry, resume only "
            "using the documented loader path for that campaign.",
            "- If interrupted uncleanly, classify as `interrupted` in operator notes; rehearse "
            "checkpoint integrity before resuming.",
            "",
            "## Partially corrupted checkpoint",
            "",
            "- Quarantine suspicious `.pt` / shard files; restore from last known-good hash; never "
            "resume training against a quarantined blob without a remediation milestone.",
            "",
            "## When to stop and escalate",
            "",
            "- Repeated SC2 crashes, GPU reset, or NaN loss without a known remedy.",
            "- Disk full or retention policy cannot be satisfied.",
            "- Any governance refusal emitted by the runner.",
            "",
            "## Transcript + inventory",
            "",
            "- Keep a timestamped operator transcript reference and a checkpoint inventory listing "
            "path logical keys (not necessarily public absolute paths).",
            "",
        ]
    )


def _checklist_md(*, sealed: dict[str, Any]) -> str:
    blocks = sealed.get("blockers") or []
    db = cast(dict[str, Any], (sealed.get("disk_budget") or {}) or {})
    disk_st = str(db.get("disk_budget_status", ""))
    lines = [
        "# V15 twelve-hour launch rehearsal checklist",
        "",
        f"- Rehearsal status: `{sealed.get('rehearsal_status', '')}`",
        f"- Disk budget status: `{disk_st}`",
        "",
        "## Blockers (if any)",
    ]
    if isinstance(blocks, list) and blocks:
        for b in blocks:
            lines.append(f"- `{b}`")
    else:
        lines.append("- *(none recorded)*")
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- [ ] `v15_twelve_hour_launch_rehearsal.json` sealed",
            "- [ ] `v15_m53_launch_command.txt` reviewed",
            "- [ ] `v15_m53_launch_runbook.md` reviewed",
            "- [ ] `v15_m53_operator_stop_resume_card.md` reviewed",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _assert_no_path_leak(blob: str) -> None:
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("V15-M52B emission leaked path patterns into public artifacts")


def _honesty_m52b() -> dict[str, Any]:
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
        "twelve_hour_run_executed": False,
    }


def validate_m52a_for_m52b(
    m52a: dict[str, Any] | None,
    *,
    expected_sha256_lower: str | None,
    require_canonical_seal: bool,
    allow_m52a_blocked_planning: bool,
) -> tuple[list[str], str, bool]:
    """Return (blocker_codes, digest, m52a_acceptable_for_watchability_chain)."""

    if m52a is None:
        return [BLOCKED_MISSING_M52A], "", False

    digest = str(m52a.get(DIGEST_FIELD) or "").lower()

    if str(m52a.get("contract_id", "")) != CONTRACT_ID_M52A_UPSTREAM:
        return [BLOCKED_MISSING_M52A], digest, False

    if require_canonical_seal and not _seal_ok(m52a):
        return [REFUSED_M52A_SHA], digest, False

    if expected_sha256_lower and expected_sha256_lower.strip():
        exp = expected_sha256_lower.strip().lower()
        if _sha_like(exp) and digest != exp:
            return [REFUSED_M52A_SHA], digest, False

    st = str(m52a.get("adapter_status") or "")
    if st == "fixture_schema_only_no_candidate_adapter_execution":
        if allow_m52a_blocked_planning:
            return [], digest, True
        return [BLOCKED_M52A_NOT_READY], digest, False

    if st in M52A_BLOCKISH:
        if allow_m52a_blocked_planning:
            return [], digest, True
        return [BLOCKED_M52A_NOT_READY], digest, False

    if st not in M52A_READYISH and st not in M52A_BLOCKISH:
        return [BLOCKED_M52A_NOT_READY], digest, False

    acceptable = st in M52A_READYISH
    return [], digest, acceptable


def emit_m52b_forbidden_refusal(
    output_dir: Path,
    *,
    profile_short: str,
    flags: list[str],
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    bl: set[str] = {REFUSED_FORBIDDEN}
    if FORBIDDEN_FLAG_12H in flags:
        bl.add("execute_12_hour_run_forbidden")
    blockers = sorted(bl)
    body = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M52B,
        "profile_id": _profile_catalog_id(profile_short),
        "profile_surface": PROFILE_M52B_SURFACE,
        "milestone": MILESTONE_LABEL_M52B,
        "emitter_module": EMITTER_MODULE_M52B,
        "profile": profile_short,
        "rehearsal_status": STATUS_REFUSED,
        "blockers": sorted(set(blockers)),
        "disk_budget": {"disk_budget_status": DISK_FIXTURE_NOT_INSPECTED},
        "m52a_binding": {"artifact_sha256": None, "adapter_status": None},
        "route_recommendation": {
            "route": "route_to_twelve_hour_operator_run_attempt",
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "honesty": _honesty_m52b(),
        "non_claims": list(NON_CLAIMS_M52B),
        "forbidden_cli_flags": sorted(set(flags)),
    }
    sealed = seal_m52b_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _write_m52b_tree(sealed, output_dir)


def _write_m52b_tree(
    sealed: dict[str, Any],
    output_dir: Path,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rep = cast(dict[str, Any], redact_paths_in_value(build_m52b_report(sealed)))
    paths: list[Path] = []
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_cmd = output_dir / LAUNCH_CMD_FILENAME
    p_run = output_dir / RUNBOOK_FILENAME
    p_sr = output_dir / STOP_RESUME_FILENAME

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(_checklist_md(sealed=sealed), encoding="utf-8")
    p_cmd.write_text(_freeze_m53_launch_command(), encoding="utf-8")
    p_run.write_text(_runbook_md(), encoding="utf-8")
    p_sr.write_text(_stop_resume_card_md(), encoding="utf-8")

    paths.extend([p_main, p_rep, p_chk, p_cmd, p_run, p_sr])
    blob = "".join(x.read_text(encoding="utf-8", errors="replace") for x in paths)
    _assert_no_path_leak(blob)
    return sealed, tuple(paths)


def emit_m52b_fixture_ci(output_dir: Path) -> tuple[dict[str, Any], tuple[Path, ...]]:
    sub = output_dir / "m52a_upstream_fixture"
    emit_m52a_fixture_ci(sub)
    m52a_path = sub / M52A_FILENAME
    return emit_m52b_operator_preflight(
        output_dir,
        m52a_path=m52a_path,
        m52a_plain_override=None,
        expected_m52a_sha256=None,
        profile_short=PROFILE_FIXTURE_CI,
        require_canonical_seal=True,
        allow_m52a_blocked_planning=True,
        m51_watchability_json=None,
        sc2_root=None,
        map_path=None,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=None,
        disk_root=None,
        estimated_checkpoint_mb=256.0,
        max_retained_checkpoints=256,
    )


def emit_m52b_operator_preflight(
    output_dir: Path,
    *,
    m52a_path: Path | None,
    m52a_plain_override: dict[str, Any] | None,
    expected_m52a_sha256: str | None,
    profile_short: str,
    require_canonical_seal: bool,
    allow_m52a_blocked_planning: bool,
    m51_watchability_json: Path | None,
    sc2_root: Path | None,
    map_path: Path | None,
    candidate_checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    disk_root: Path | None,
    estimated_checkpoint_mb: float | None,
    max_retained_checkpoints: int | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    m52a_plain: dict[str, Any] | None = m52a_plain_override
    if m52a_plain is None and m52a_path is not None and Path(m52a_path).is_file():
        try:
            m52a_plain = _parse_json_object(Path(m52a_path).resolve())
        except (json.JSONDecodeError, OSError, UnicodeError, ValueError):
            m52a_plain = None

    exp_m52a = str(expected_m52a_sha256).strip().lower() if expected_m52a_sha256 else None

    blockers, m52a_digest, chain_ok = validate_m52a_for_m52b(
        m52a_plain,
        expected_sha256_lower=exp_m52a,
        require_canonical_seal=require_canonical_seal,
        allow_m52a_blocked_planning=allow_m52a_blocked_planning,
    )

    warnings: list[str] = []

    adapter_st = None
    if m52a_plain:
        adapter_st = str(m52a_plain.get("adapter_status") or "")

    if m51_watchability_json is not None and Path(m51_watchability_json).is_file():
        _ = _parse_json_object(Path(m51_watchability_json).resolve())
    elif profile_short == PROFILE_OPERATOR_PREFLIGHT and m52a_plain is None:
        warnings.append("m51_watchability_json_not_supplied_enrichment_skipped")

    ck_path = Path(candidate_checkpoint_path).resolve() if candidate_checkpoint_path else None
    exp_ck = str(expected_candidate_sha256).strip().lower() if expected_candidate_sha256 else None

    if profile_short != PROFILE_FIXTURE_CI:
        if ck_path is None or not ck_path.is_file():
            blockers.append(BLOCKED_MISSING_CKPT)
        elif exp_ck and _sha_like(exp_ck):
            got = sha256_hex_file_optional(ck_path)
            if got != exp_ck:
                blockers.append(BLOCKED_CKPT_SHA)

    if profile_short != PROFILE_FIXTURE_CI:
        if sc2_root is None or not Path(sc2_root).is_dir():
            blockers.append(BLOCKED_SC2)
        if map_path is None or not Path(map_path).is_file():
            blockers.append(BLOCKED_MAP)

    if estimated_checkpoint_mb is None or max_retained_checkpoints is None:
        if profile_short != PROFILE_FIXTURE_CI:
            blockers.append(BLOCKED_RETENTION)
            blockers.append(BLOCKED_DISK_UNKNOWN)

    disk_status = DISK_FIXTURE_NOT_INSPECTED
    disk_block: dict[str, Any] = {"disk_budget_status": disk_status}

    if profile_short == PROFILE_FIXTURE_CI:
        disk_block = {
            "disk_budget_status": DISK_FIXTURE_NOT_INSPECTED,
            "note": "fixture_ci does not inspect operator disk",
        }
    elif disk_root is not None and Path(disk_root).exists():
        disk_status = "inspected"
        du = shutil.disk_usage(Path(disk_root).resolve())
        free_mb = du.free / (1024 * 1024)
        disk_block = {
            "disk_budget_status": disk_status,
            "free_space_mb": round(free_mb, 2),
        }
        if estimated_checkpoint_mb is not None and max_retained_checkpoints is not None:
            retained_mb = float(estimated_checkpoint_mb) * int(max_retained_checkpoints)
            telemetry_mb = retained_mb * 0.25
            need_mb = retained_mb + telemetry_mb
            disk_block["estimated_retained_checkpoint_mb"] = round(retained_mb, 2)
            disk_block["estimated_telemetry_overhead_mb"] = round(telemetry_mb, 2)
            disk_block["estimated_total_need_mb"] = round(need_mb, 2)
            if free_mb < need_mb:
                blockers.append(BLOCKED_DISK_INSUFFICIENT)
            elif free_mb < need_mb * 1.10:
                warnings.append("disk_budget_tight_margin")
    elif profile_short != PROFILE_FIXTURE_CI:
        disk_block["disk_budget_status"] = "disk_root_not_supplied"
        if BLOCKED_DISK_UNKNOWN not in blockers:
            blockers.append(BLOCKED_DISK_UNKNOWN)

    if profile_short == PROFILE_FIXTURE_CI:
        rehearsal_st = STATUS_FIXTURE_ONLY
    elif REFUSED_M52A_SHA in blockers:
        rehearsal_st = STATUS_REFUSED
    elif blockers:
        rehearsal_st = STATUS_BLOCKED
    elif warnings:
        rehearsal_st = STATUS_READY_WARNINGS
    else:
        rehearsal_st = STATUS_READY

    if rehearsal_st in (STATUS_READY, STATUS_READY_WARNINGS) and not chain_ok:
        warnings.append("m52a_adapter_watchability_chain_not_confirmed")

    if not chain_ok and rehearsal_st == STATUS_READY:
        rehearsal_st = STATUS_READY_WARNINGS

    blockers = sorted(set(blockers))

    m52a_binding = {
        "artifact_sha256": m52a_digest or None,
        "adapter_status": adapter_st,
        "contract_id": CONTRACT_ID_M52A_UPSTREAM,
    }

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M52B,
        "profile_id": _profile_catalog_id(profile_short),
        "profile_surface": PROFILE_M52B_SURFACE,
        "milestone": MILESTONE_LABEL_M52B,
        "emitter_module": EMITTER_MODULE_M52B,
        "profile": profile_short,
        "rehearsal_status": rehearsal_st,
        "blockers": blockers,
        "warnings": warnings,
        "m52a_binding": m52a_binding,
        "disk_budget": disk_block,
        "checkpoint_retention": {
            "max_retained_checkpoints": max_retained_checkpoints,
            "estimated_checkpoint_mb": estimated_checkpoint_mb,
        },
        "stop_resume_plan_frozen": True,
        "launch_command_frozen": True,
        "twelve_hour_run_executed_in_rehearsal": False,
        "route_recommendation": {
            "route": "route_to_twelve_hour_operator_run_attempt",
            "route_status": ROUTE_STATUS_RECOMMENDED_NOT_EXECUTED,
        },
        "honesty": _honesty_m52b(),
        "non_claims": list(NON_CLAIMS_M52B),
    }

    sealed = seal_m52b_body(cast(dict[str, Any], redact_paths_in_value(body)))
    return _write_m52b_tree(sealed, output_dir)


def emit_m52b_operator_declared(
    output_dir: Path,
    *,
    declared_path: Path,
    embedded_m52a_path: Path | None,
) -> tuple[dict[str, Any], tuple[Path, ...]]:
    raw = json.loads(Path(declared_path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("declared must be object")
    decl = cast(dict[str, Any], redact_paths_in_value(raw))

    cid = str(decl.get("contract_id") or "")
    pid = str(decl.get("profile_id") or "")
    if cid != CONTRACT_ID_M52B or pid not in (PROFILE_M52B_SURFACE, PROFILE_ID_OPERATOR_DECLARED):
        out_body: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "contract_id": CONTRACT_ID_M52B,
            "profile_id": PROFILE_ID_OPERATOR_DECLARED,
            "profile_surface": PROFILE_M52B_SURFACE,
            "milestone": MILESTONE_LABEL_M52B,
            "emitter_module": EMITTER_MODULE_M52B,
            "profile": PROFILE_OPERATOR_DECLARED,
            "rehearsal_status": STATUS_REFUSED,
            "blockers": [REFUSED_CONTRACT],
            "disk_budget": {"disk_budget_status": DISK_FIXTURE_NOT_INSPECTED},
            "m52a_binding": {},
            "honesty": _honesty_m52b(),
            "non_claims": list(NON_CLAIMS_M52B),
        }
        sealed = seal_m52b_body(cast(dict[str, Any], redact_paths_in_value(out_body)))
        return _write_m52b_tree(sealed, output_dir)

    m52a_plain: dict[str, Any] | None = None
    emb = decl.get("sealed_m52a")
    if isinstance(emb, dict):
        m52a_plain = emb
    elif embedded_m52a_path is not None and Path(embedded_m52a_path).is_file():
        m52a_plain = _parse_json_object(Path(embedded_m52a_path).resolve())

    exp = decl.get("expected_m52a_sha256")
    exp_s = str(exp).strip().lower() if isinstance(exp, str) and exp.strip() else None

    ec_raw = decl.get("estimated_checkpoint_mb")
    try:
        est_mb = float(ec_raw) if ec_raw is not None else None
    except (TypeError, ValueError):
        est_mb = None
    mr_raw = decl.get("max_retained_checkpoints")
    try:
        max_ret = int(mr_raw) if mr_raw is not None else None
    except (TypeError, ValueError):
        max_ret = None

    return emit_m52b_operator_preflight(
        output_dir,
        m52a_path=None,
        m52a_plain_override=m52a_plain,
        expected_m52a_sha256=exp_s,
        profile_short=PROFILE_OPERATOR_DECLARED,
        require_canonical_seal=False,
        allow_m52a_blocked_planning=bool(decl.get("allow_m52a_adapter_blocked_planning")),
        m51_watchability_json=None,
        sc2_root=None,
        map_path=None,
        candidate_checkpoint_path=None,
        expected_candidate_sha256=None,
        disk_root=None,
        estimated_checkpoint_mb=est_mb,
        max_retained_checkpoints=max_ret,
    )
