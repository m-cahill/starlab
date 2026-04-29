"""V15-M37 two-hour run blocker discovery — sealed JSON + reports (audit only)."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Final

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.full_30min_sc2_backed_t1_run_models import CONTRACT_ID as CONTRACT_ID_M29_FULL_RUN
from starlab.v15.m31_candidate_checkpoint_evaluation_harness_gate_io import (
    emission_has_private_path_patterns,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    CONTRACT_ID_M33_PROBE,
)
from starlab.v15.m33_candidate_checkpoint_model_load_cuda_probe_models import (
    GATE_ARTIFACT_DIGEST_FIELD as M33_DIGEST,
)
from starlab.v15.m35_candidate_checkpoint_smoke_benchmark_readiness_models import (
    CONTRACT_ID_M35_READINESS,
    PROFILE_M35_READINESS,
)
from starlab.v15.m36_smoke_benchmark_execution_models import CONTRACT_ID_M36_EXECUTION
from starlab.v15.m37_two_hour_run_blocker_discovery_models import (
    ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256,
    CHECKLIST_FILENAME,
    CONTRACT_ID_M37_DISCOVERY,
    DEFAULT_TARGET_WALL_CLOCK_SECONDS,
    EMITTER_MODULE_M37,
    EXPECTED_PUBLIC_CANDIDATE_SHA256,
    FILENAME_MAIN_JSON,
    GATE_ARTIFACT_DIGEST_FIELD,
    M36_BINDING_ENRICHED,
    M36_BINDING_OPTIONAL_NOT_SUPPLIED,
    MILESTONE_LABEL_M37,
    NON_CLAIMS_M37,
    PROFILE_FIXTURE_CI,
    PROFILE_M37_OPERATOR_READINESS,
    PROFILE_OPERATOR_AUDIT,
    PUBLIC_LEDGER_M29_CHECKPOINT_COUNT,
    PUBLIC_LEDGER_M29_OBSERVED_WALL_CLOCK_SECONDS,
    PUBLIC_LEDGER_M29_TRAINING_UPDATE_COUNT,
    RECOMMENDED_NEXT,
    REMEDIATION_MAP_FILENAME,
    REPORT_FILENAME,
    RUNBOOK_DRAFT_FILENAME,
    SCHEMA_VERSION,
    STATUS_BLOCKED_MISSING_REQUIRED_INPUTS,
    STATUS_COMPLETED_READY_M38,
    STATUS_FIXTURE_SCHEMA_ONLY,
    STORAGE_RISK_CRITICAL,
    STORAGE_RISK_HIGH,
    STORAGE_RISK_MEDIUM,
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


def _claim_flags_all_false() -> dict[str, Any]:
    return {
        "two_hour_run_executed": False,
        "benchmark_execution_performed": False,
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


def seal_m37_body(body: dict[str, Any]) -> dict[str, Any]:
    wo = {k: v for k, v in body.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(wo)
    sealed = dict(wo)
    sealed[GATE_ARTIFACT_DIGEST_FIELD] = digest
    return sealed


def _extract_candidate_sha_from_obj(obj: dict[str, Any]) -> str:
    cand = obj.get("candidate_checkpoint")
    if isinstance(cand, dict):
        s = str(cand.get("sha256") or "").strip().lower()
        if _is_hex64(s):
            return s
    for key in ("candidate_checkpoint_sha256", "upstream_candidate_checkpoint_sha256"):
        s = str(obj.get(key) or "").strip().lower()
        if _is_hex64(s):
            return s
    return ""


def _m29_candidate_sha_best_effort(m29: dict[str, Any]) -> str:
    c_op = str(m29.get("candidate_checkpoint_sha256_operator_local") or "").strip().lower()
    c_up = str(m29.get("upstream_m28_candidate_checkpoint_sha256_reference") or "").strip().lower()
    if _is_hex64(c_op):
        return c_op
    if _is_hex64(c_up):
        return c_up
    nested = m29.get("candidate_checkpoint")
    if isinstance(nested, dict):
        s = str(nested.get("sha256") or "").strip().lower()
        if _is_hex64(s):
            return s
    return ""


def _extract_m29_cadence_fields(m29: dict[str, Any]) -> tuple[float, int, int, str]:
    wc = float(m29.get("observed_wall_clock_seconds") or 0.0)
    ck = int(m29.get("checkpoint_count") or 0)
    tu = int(m29.get("training_update_count") or 0)
    if wc > 0 and ck > 0:
        return wc, ck, tu, "m29_json_fields"
    return (
        PUBLIC_LEDGER_M29_OBSERVED_WALL_CLOCK_SECONDS,
        PUBLIC_LEDGER_M29_CHECKPOINT_COUNT,
        PUBLIC_LEDGER_M29_TRAINING_UPDATE_COUNT,
        "ledger_fallback_constants",
    )


def _checkpoint_cadence_unknown_blocker() -> dict[str, Any]:
    return {
        "blocker_id": "checkpoint_cadence_unknown",
        "category": "checkpoint_cadence_storage",
        "severity": "high",
        "status": "open",
        "evidence": (
            "Could not derive checkpoint cadence from sealed M29 JSON fields or ledger fallbacks."
        ),
        "m38_action": (
            "Supply sealed M29 JSON with observed_wall_clock_seconds and checkpoint_count "
            "or document cadence explicitly."
        ),
    }


def _has_explicit_checkpoint_volume_controls(repo_root: Path) -> bool:
    needles = (
        "checkpoint_retention",
        "max_checkpoint",
        "max_retained",
        "prune_checkpoint",
        "delete_checkpoint",
        "checkpoint_budget",
        "rotate_checkpoint",
    )
    targets = (
        repo_root / "starlab" / "v15" / "sc2_backed_t1_training_execution.py",
        repo_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py",
    )
    for p in targets:
        if not p.is_file():
            continue
        txt = p.read_text(encoding="utf-8", errors="replace").lower()
        if any(n in txt for n in needles):
            return True
    return False


def extrapolate_checkpoint_storage_risk(
    *,
    observed_wall_clock_seconds: float,
    checkpoint_count: float,
    target_wall_clock_seconds: float,
    cadence_source: str,
    repo_root: Path,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    retention_controls = _has_explicit_checkpoint_volume_controls(repo_root)
    tel: dict[str, Any] = {
        "cadence_source": cadence_source,
        "observed_wall_clock_seconds": observed_wall_clock_seconds,
        "checkpoint_count_observed": int(checkpoint_count),
        "target_wall_clock_seconds": float(target_wall_clock_seconds),
        "checkpoint_retention_controls_detected_in_repo": retention_controls,
    }
    blocker: dict[str, Any] | None = None

    if observed_wall_clock_seconds <= 0 or checkpoint_count <= 0:
        tel["checkpoints_per_second"] = None
        tel["checkpoints_per_minute"] = None
        tel["estimated_checkpoints_for_target_wall_clock"] = None
        tel["estimated_multiplier_vs_m29_wall_clock_ratio"] = None
        tel["storage_risk_classification"] = "unknown"
        return tel, _checkpoint_cadence_unknown_blocker()

    cps = float(checkpoint_count) / float(observed_wall_clock_seconds)
    cpm = cps * 60.0
    ratio = float(target_wall_clock_seconds) / float(observed_wall_clock_seconds)
    est_ckpts = float(checkpoint_count) * ratio

    tel["checkpoints_per_second"] = round(cps, 6)
    tel["checkpoints_per_minute"] = round(cpm, 6)
    tel["estimated_checkpoints_for_target_wall_clock"] = int(round(est_ckpts))
    tel["estimated_multiplier_vs_m29_wall_clock_ratio"] = round(ratio, 6)

    if retention_controls:
        tel["storage_risk_classification"] = STORAGE_RISK_MEDIUM
        return tel, None

    if est_ckpts >= 150_000:
        tel["storage_risk_classification"] = STORAGE_RISK_CRITICAL
        sev = "critical"
    elif est_ckpts >= 50_000:
        tel["storage_risk_classification"] = STORAGE_RISK_HIGH
        sev = "high"
    else:
        tel["storage_risk_classification"] = STORAGE_RISK_MEDIUM
        sev = "medium"

    blocker = {
        "blocker_id": "checkpoint_cadence_too_high",
        "category": "checkpoint_cadence_storage",
        "severity": sev,
        "status": "open",
        "evidence": (
            f"M29-equivalent cadence extrapolates to ~{int(round(est_ckpts))} checkpoints "
            f"for {target_wall_clock_seconds:.0f}s wall clock ({cadence_source}); "
            "no checkpoint pruning / retention controls detected in training runner paths."
        ),
        "m38_action": (
            "Add cadence caps, pruning, archival rotation, or prove bounded artifact volume "
            "before M39."
        ),
    }
    return tel, blocker


def _runner_compatibility_scan(repo_root: Path) -> dict[str, Any]:
    m29_path = repo_root / "starlab" / "v15" / "run_v15_m29_full_30min_sc2_backed_t1_run.py"
    m28_path = repo_root / "starlab" / "v15" / "run_v15_m28_sc2_backed_t1_candidate_training.py"
    out: dict[str, Any] = {
        "m29_horizon_classification_uses_1800_second_literal": False,
        "m28_accepts_max_wall_clock_minutes_cli": False,
        "m29_default_max_wall_clock_minutes_30": False,
        "7200_second_compatibility_classification": "unknown",
        "notes": [],
    }
    if m29_path.is_file():
        t = m29_path.read_text(encoding="utf-8", errors="replace")
        if "1800.0" in t and "horizon_ok" in t:
            out["m29_horizon_classification_uses_1800_second_literal"] = True
        if "--max-wall-clock-minutes" in t and "default=30.0" in t.replace(" ", ""):
            out["m29_default_max_wall_clock_minutes_30"] = True
    if m28_path.is_file():
        t2 = m28_path.read_text(encoding="utf-8", errors="replace")
        out["m28_accepts_max_wall_clock_minutes_cli"] = "--max-wall-clock-minutes" in t2

    if out["m29_horizon_classification_uses_1800_second_literal"]:
        out["7200_second_compatibility_classification"] = "blocked_or_requires_m38_wrapper"
        out["notes"].append(
            "M29 outcome classification compares against a 30-minute horizon (1800s); "
            "a 7200s run likely needs a dedicated wrapper or generalized horizon policy in M38."
        )
    elif out["m28_accepts_max_wall_clock_minutes_cli"]:
        out["7200_second_compatibility_classification"] = "likely_parameterizable_via_m28"
        out["notes"].append(
            "M28 runner exposes --max-wall-clock-minutes; M38 should confirm bounds and receipts."
        )

    return out


def _runner_compatibility_blockers(scan: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if scan.get("m29_horizon_classification_uses_1800_second_literal"):
        out.append(
            {
                "blocker_id": "m29_wrapper_name_or_contract_too_30min_specific",
                "category": "runner_compatibility",
                "severity": "high",
                "status": "open",
                "evidence": (
                    "run_v15_m29_full_30min_sc2_backed_t1_run.py classifies outcomes using "
                    "a fixed 1800s horizon check; 7200s M39 semantics are not yet first-class."
                ),
                "m38_action": (
                    "Add a 2-hour wrapper or generalize horizon checks and evidence contract."
                ),
            },
        )
    return out


def _run_control_posture_scan(repo_root: Path) -> dict[str, Any]:
    hits: dict[str, bool] = {
        "interrupt_receipt_keyword": False,
        "resume_receipt_keyword": False,
        "operator_transcript_keyword": False,
        "lockfile_keyword": False,
    }
    root = repo_root / "starlab" / "v15"
    if not root.is_dir():
        return {"keyword_hits": hits, "classification": "unknown"}
    for p in root.rglob("*.py"):
        if "test_" in p.name:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        if "interrupt" in t and "receipt" in t:
            hits["interrupt_receipt_keyword"] = True
        if "resume" in t and "receipt" in t:
            hits["resume_receipt_keyword"] = True
        if "transcript" in t:
            hits["operator_transcript_keyword"] = True
        if "lockfile" in t or ".lock" in t:
            hits["lockfile_keyword"] = True
    classified = "partial_keywords_only"
    if not any(hits.values()):
        classified = "no_keyword_evidence_in_v15_python_surface"
    return {"keyword_hits": hits, "classification": classified}


def _git_porcelain(repo_root: Path) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        text = (proc.stdout or "").strip()
        clean = len(text) == 0
        return clean, text
    except OSError:
        return False, "git_status_failed"


def _git_branch(repo_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return (proc.stdout or "").strip()
    except OSError:
        return ""


def _git_ls_files_tracked(repo_root: Path, pattern: str) -> list[str]:
    try:
        proc = subprocess.run(
            ["git", "ls-files", pattern],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    except OSError:
        return []


def _private_governance_probe(repo_root: Path) -> dict[str, Any]:
    cs = repo_root / "docs" / "company_secrets"
    readme = cs / "README.md"
    prompts = cs / "prompts"
    want_prompts = ("workflowprompt.md", "summaryprompt.md", "unifiedmilestoneauditpromptV2.md")
    missing_prompts: list[str] = []
    present_prompts: list[str] = []
    for name in want_prompts:
        pp = (prompts / name) if prompts.is_dir() else (cs / name)
        if pp.is_file():
            present_prompts.append(name)
        else:
            missing_prompts.append(name)

    m37_priv = cs / "milestones" / "post-v1" / "V15-M37"

    tracked_cs = _git_ls_files_tracked(repo_root, "docs/company_secrets")
    tracked_out = _git_ls_files_tracked(repo_root, "out")

    return {
        "company_secrets_dir_exists": cs.is_dir(),
        "company_secrets_readme_exists": readme.is_file(),
        "company_secrets_prompts_dir_exists": prompts.is_dir(),
        "prompt_presence_by_basename": {
            "present": present_prompts,
            "missing_expected_basenames": missing_prompts,
        },
        "private_milestone_folder_v15_m37_exists": m37_priv.is_dir(),
        "git_ls_files_company_secrets_nonempty_tracked_risk": len(tracked_cs) > 0,
        "git_ls_files_out_nonempty_tracked_risk": len(tracked_out) > 0,
        "tracked_company_secrets_paths_count": len(tracked_cs),
        "tracked_out_paths_count": len(tracked_out),
    }


def _environment_probe_allow_imports() -> dict[str, Any]:
    snap: dict[str, Any] = {
        "python_version": None,
        "torch_version": None,
        "cuda_available": None,
        "gpu_name": None,
        "torch_probe_error": None,
        "sc2_import_ok": None,
        "sc2_import_error": None,
        "nvidia_smi_available": None,
        "nvidia_smi_head": None,
    }
    import sys

    snap["python_version"] = sys.version.split()[0]

    try:
        import torch

        snap["torch_version"] = str(torch.__version__)
        snap["cuda_available"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            snap["gpu_name"] = str(torch.cuda.get_device_name(0))
        else:
            snap["gpu_name"] = None
    except Exception as exc:
        snap["torch_probe_error"] = str(exc)

    try:
        import importlib

        importlib.import_module("sc2")
        snap["sc2_import_ok"] = True
    except Exception as exc:
        snap["sc2_import_ok"] = False
        snap["sc2_import_error"] = str(exc)

    try:
        proc = subprocess.run(
            ["nvidia-smi", "-L"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        snap["nvidia_smi_available"] = proc.returncode == 0
        snap["nvidia_smi_head"] = (proc.stdout or "").strip().splitlines()[:3]
    except OSError:
        snap["nvidia_smi_available"] = False

    return snap


def build_fixture_body() -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    gates = [
        {"gate_id": "R0", "name": "Workspace", "status": "not_applicable"},
        {"gate_id": "R1", "name": "Private governance surface", "status": "not_applicable"},
        {"gate_id": "R2", "name": "CUDA environment", "status": "unknown"},
        {"gate_id": "R3", "name": "SC2 surface", "status": "unknown"},
        {"gate_id": "R4", "name": "Candidate identity", "status": "unknown"},
        {"gate_id": "R5", "name": "Artifact chain", "status": "unknown"},
        {"gate_id": "R6", "name": "Runner compatibility (7200s)", "status": "unknown"},
        {"gate_id": "R7", "name": "Checkpoint cadence / volume", "status": "unknown"},
        {"gate_id": "R8", "name": "Disk / retention", "status": "unknown"},
        {"gate_id": "R9", "name": "Stop/resume posture", "status": "unknown"},
        {"gate_id": "R10", "name": "Monitoring / telemetry plan", "status": "unknown"},
        {"gate_id": "R11", "name": "Runbook draft", "status": "pass"},
        {"gate_id": "R12", "name": "Non-claims / claim flags", "status": "pass"},
    ]

    cadence_fixture = extrapolate_checkpoint_storage_risk(
        observed_wall_clock_seconds=PUBLIC_LEDGER_M29_OBSERVED_WALL_CLOCK_SECONDS,
        checkpoint_count=float(PUBLIC_LEDGER_M29_CHECKPOINT_COUNT),
        target_wall_clock_seconds=DEFAULT_TARGET_WALL_CLOCK_SECONDS,
        cadence_source="ledger_fallback_constants",
        repo_root=repo_root,
    )[0]

    return {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M37_DISCOVERY,
        "profile_id": PROFILE_M37_OPERATOR_READINESS,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_LABEL_M37,
        "emitter_module": EMITTER_MODULE_M37,
        "audit_status": STATUS_FIXTURE_SCHEMA_ONLY,
        "target_run": {
            "target_milestone": "V15-M39",
            "run_class": "two_hour_sc2_backed_t1_continuation_candidate_training",
            "target_wall_clock_seconds": DEFAULT_TARGET_WALL_CLOCK_SECONDS,
            "operator_local_only": True,
            "ci_execution_allowed": False,
        },
        "candidate_checkpoint": {
            "sha256": EXPECTED_PUBLIC_CANDIDATE_SHA256,
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_file_hash_verified": False,
            "checkpoint_path_supplied": False,
        },
        "m36_smoke_execution_binding_status": M36_BINDING_OPTIONAL_NOT_SUPPLIED,
        "checkpoint_cadence_and_storage": cadence_fixture,
        "runner_compatibility": _runner_compatibility_scan(repo_root),
        "run_control_posture_scan": _run_control_posture_scan(repo_root),
        "readiness_summary": {
            "critical_blocker_count": 0,
            "high_blocker_count": 0,
            "medium_blocker_count": 0,
            "low_blocker_count": 0,
            "informational_blocker_count": 0,
            "m38_required": True,
            "m39_attempt_recommended_now": False,
        },
        "blockers": [],
        "gates": gates,
        "claim_flags": _claim_flags_all_false(),
        "non_claims": list(NON_CLAIMS_M37),
        "recommended_next": RECOMMENDED_NEXT,
    }


def build_m37_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_two_hour_run_blocker_discovery_report",
        "report_version": "m37",
        "milestone": MILESTONE_LABEL_M37,
        "contract_id": CONTRACT_ID_M37_DISCOVERY,
        "profile_id": PROFILE_M37_OPERATOR_READINESS,
        GATE_ARTIFACT_DIGEST_FIELD: digest,
        "audit_status": sealed.get("audit_status"),
    }


def build_m37_checklist_md(sealed: dict[str, Any]) -> str:
    st = str(sealed.get("audit_status", ""))
    gates = sealed.get("gates") or []
    rows = ""
    if isinstance(gates, list):
        for g in gates:
            if isinstance(g, dict):
                gid = g.get("gate_id", "")
                nm = g.get("name", "")
                gs = g.get("status", "")
                rows += f"| {gid} | {nm} | {gs} |\n"
    nc_raw = sealed.get("non_claims") or []
    nc_lines = (
        "\n".join(f"- {item}" for item in nc_raw)
        if isinstance(nc_raw, list) and nc_raw
        else "(none)"
    )
    return (
        "# V15-M37 — two-hour run blocker discovery checklist\n\n"
        f"**`audit_status`:** `{st}`  \n"
        "**Reminder:** V15-M37 does **not** execute the 2-hour run.\n\n"
        "| Gate | Name | Status |\n"
        "| --- | --- | --- |\n"
        f"{rows}\n"
        "## Non-claims\n\n"
        f"{nc_lines}\n"
    )


def build_m38_remediation_map_md(blockers: list[dict[str, Any]]) -> str:
    lines = [
        "# V15-M38 remediation map (draft)",
        "",
        "Generated by **`starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery`**.",
        "",
        "Open blockers:",
        "",
    ]
    opens = [b for b in blockers if str(b.get("status")) == "open"]
    if not opens:
        lines.append("(none)")
        lines.append("")
        return "\n".join(lines)
    for b in opens:
        bid = b.get("blocker_id", "")
        sev = b.get("severity", "")
        act = b.get("m38_action", "")
        lines.append(f"- **`{bid}`** ({sev}): {act}")
    lines.append("")
    return "\n".join(lines)


def build_m39_runbook_draft_md(*, audit_status: str) -> str:
    return (
        "# V15-M39 candidate runbook — draft (non-final)\n\n"
        f"**Audit posture:** `{audit_status}` — **draft only** until **V15-M38** "
        "freezes commands.\n\n"
        "## Target run\n\n"
        "- **Class:** `two_hour_sc2_backed_t1_continuation_candidate_training`\n"
        "- **Wall clock:** **7200** seconds\n"
        "- **Operator-local only** — **no** merge-gate CI long run\n\n"
        "## Expected command family (non-binding)\n\n"
        "- Inspect **`runner_compatibility`** from **V15-M37** sealed JSON.\n"
        "- **`run_v15_m29_full_30min_*`** naming reflects **30-minute** semantics — "
        "**M38** must confirm **7200s** wrappers.\n\n"
        "## Required inputs\n\n"
        "- Sealed **M27/M28/M29/M33/M35** lineage consistent with candidate SHA "
        f"`{EXPECTED_PUBLIC_CANDIDATE_SHA256}` unless superseded.\n\n"
        "## Preflight\n\n"
        "- Run **`emit_v15_m37_two_hour_run_blocker_discovery`** operator audit.\n\n"
        "## Stop / resume\n\n"
        "- Formal interrupt/resume receipts remain **M38** scope.\n\n"
        "## Non-claims\n\n"
        "- Not benchmark pass; not strength evaluation; not checkpoint promotion; "
        "not XAI/human/showcase/v2; not T2/T3.\n"
    )


def _finalize_blockers_and_summary(
    blockers: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "informational": 0}
    for b in blockers:
        s = str(b.get("severity", "")).lower()
        if s in counts:
            counts[s] += 1
    summary = {
        "critical_blocker_count": counts["critical"],
        "high_blocker_count": counts["high"],
        "medium_blocker_count": counts["medium"],
        "low_blocker_count": counts["low"],
        "informational_blocker_count": counts["informational"],
        "m38_required": True,
        "m39_attempt_recommended_now": False,
    }
    return blockers, summary


def build_operator_audit_body(
    *,
    repo_root: Path,
    output_dir: Path,
    allow_operator_local_inspection: bool,
    candidate_checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    authorize_checkpoint_file_sha256: bool,
    m27_rollout_json: Path | None,
    m28_training_json: Path | None,
    m29_full_run_json: Path | None,
    m34_cuda_probe_json: Path | None,
    m35_readiness_json: Path | None,
    m36_smoke_execution_json: Path | None,
    target_wall_clock_seconds: float,
    min_free_disk_gb: float,
) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []

    exp_sha = (
        str(expected_candidate_sha256).strip().lower()
        if expected_candidate_sha256
        else EXPECTED_PUBLIC_CANDIDATE_SHA256
    )
    if not _is_hex64(exp_sha):
        blockers.append(
            {
                "blocker_id": "invalid_expected_candidate_sha_cli",
                "category": "candidate_identity",
                "severity": "critical",
                "status": "open",
                "evidence": "--expected-candidate-sha256 must be a 64-char lowercase hex string.",
                "m38_action": "Provide the canonical candidate SHA256 binding.",
            },
        )

    audit_status = STATUS_COMPLETED_READY_M38

    runner_scan = _runner_compatibility_scan(repo_root)
    blockers.extend(_runner_compatibility_blockers(runner_scan))
    run_ctrl = _run_control_posture_scan(repo_root)

    git_clean = True
    git_branch = ""
    porcelain = ""
    env_snap: dict[str, Any] = {}
    disk_free_gb: float | None = None
    output_writable = True

    gov = _private_governance_probe(repo_root)

    if allow_operator_local_inspection:
        git_clean, porcelain = _git_porcelain(repo_root)
        git_branch = _git_branch(repo_root)
        env_snap = _environment_probe_allow_imports()
        try:
            usage = shutil.disk_usage(str(output_dir.resolve()))
            disk_free_gb = round(usage.free / (1024**3), 3)
        except OSError:
            disk_free_gb = None
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            probe = output_dir / ".m37_write_probe"
            probe.write_text("ok\n", encoding="utf-8")
            probe.unlink(missing_ok=True)
            output_writable = True
        except OSError:
            output_writable = False

        if not git_clean:
            blockers.append(
                {
                    "blocker_id": "dirty_worktree_unrelated_changes",
                    "category": "workspace_git_hygiene",
                    "severity": "medium",
                    "status": "open",
                    "evidence": "git status --porcelain is non-empty.",
                    "m38_action": "Clean unrelated edits before operator receipts.",
                },
            )

        if gov["tracked_company_secrets_paths_count"] > 0:
            blockers.append(
                {
                    "blocker_id": "private_files_tracked",
                    "category": "workspace_git_hygiene",
                    "severity": "critical",
                    "status": "open",
                    "evidence": (
                        "git ls-files docs/company_secrets lists tracked paths "
                        f"({gov['tracked_company_secrets_paths_count']})."
                    ),
                    "m38_action": "Untrack private governance paths; enforce gitignore posture.",
                },
            )

        if gov["tracked_out_paths_count"] > 0:
            blockers.append(
                {
                    "blocker_id": "output_root_paths_tracked",
                    "category": "workspace_git_hygiene",
                    "severity": "high",
                    "status": "open",
                    "evidence": "git ls-files out reports tracked paths.",
                    "m38_action": "Keep generated outputs untracked.",
                },
            )

        if disk_free_gb is not None and disk_free_gb + 1e-9 < float(min_free_disk_gb):
            blockers.append(
                {
                    "blocker_id": "disk_free_below_threshold",
                    "category": "disk_posture",
                    "severity": "high",
                    "status": "open",
                    "evidence": (
                        f"Free disk ~{disk_free_gb} GiB below configured minimum "
                        f"{min_free_disk_gb} GiB."
                    ),
                    "m38_action": "Free disk / relocate artifact roots before M39.",
                },
            )

        if not output_writable:
            blockers.append(
                {
                    "blocker_id": "output_root_not_writable",
                    "category": "disk_posture",
                    "severity": "critical",
                    "status": "open",
                    "evidence": "Could not write/delete probe file under output dir.",
                    "m38_action": "Fix filesystem permissions / choose writable root.",
                },
            )

        if env_snap.get("torch_probe_error"):
            blockers.append(
                {
                    "blocker_id": "torch_import_failed",
                    "category": "environment_cuda_python",
                    "severity": "critical",
                    "status": "open",
                    "evidence": str(env_snap.get("torch_probe_error")),
                    "m38_action": "Repair venv/torch installation.",
                },
            )
        elif env_snap.get("cuda_available") is False:
            blockers.append(
                {
                    "blocker_id": "torch_cuda_unavailable",
                    "category": "environment_cuda_python",
                    "severity": "high",
                    "status": "open",
                    "evidence": "torch.cuda.is_available() returned false.",
                    "m38_action": "Restore CUDA-visible GPU stack for SC2-backed training.",
                },
            )

        if env_snap.get("nvidia_smi_available") is False:
            blockers.append(
                {
                    "blocker_id": "nvidia_smi_unavailable",
                    "category": "environment_cuda_python",
                    "severity": "medium",
                    "status": "open",
                    "evidence": "nvidia-smi probe failed or binary unavailable.",
                    "m38_action": "Verify NVIDIA driver tooling for long telemetry sampling.",
                },
            )

        if env_snap.get("sc2_import_ok") is False:
            blockers.append(
                {
                    "blocker_id": "sc2_import_unavailable",
                    "category": "sc2_surface",
                    "severity": "high",
                    "status": "open",
                    "evidence": str(env_snap.get("sc2_import_error") or "sc2 import failed"),
                    "m38_action": "Restore python-sc2 / Burny dependency wiring.",
                },
            )

        if gov["prompt_presence_by_basename"]["missing_expected_basenames"]:
            miss = gov["prompt_presence_by_basename"]["missing_expected_basenames"]
            blockers.append(
                {
                    "blocker_id": "missing_private_prompt_basenames_optional",
                    "category": "private_governance_surface",
                    "severity": "low",
                    "status": "open",
                    "evidence": f"Expected prompt basenames missing locally: {miss}",
                    "m38_action": "Restore prompts from backups when closing milestones privately.",
                },
            )

        if env_snap.get("nvidia_smi_available"):
            blockers.append(
                {
                    "blocker_id": "nvidia_smi_telemetry_not_planned",
                    "category": "thermal_resource_monitoring",
                    "severity": "low",
                    "status": "open",
                    "evidence": "nvidia-smi present; scripted telemetry sampling not asserted.",
                    "m38_action": "Add timestamped GPU util/temp/power sampling for M39.",
                },
            )

    # --- Artifact loads ---
    m29_obj: dict[str, Any] | None = None
    if m29_full_run_json is not None:
        if m29_full_run_json.is_file():
            m29_obj = _parse_json_object(m29_full_run_json.resolve())
        else:
            blockers.append(
                {
                    "blocker_id": "missing_m29_json",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": f"M29 JSON path not readable: {m29_full_run_json}",
                    "m38_action": "Supply sealed M29 full-run JSON.",
                },
            )
    else:
        blockers.append(
            {
                "blocker_id": "missing_m29_json",
                "category": "artifact_chain_seals",
                "severity": "high",
                "status": "open",
                "evidence": "--m29-full-run-json not supplied.",
                "m38_action": "Provide sealed M29 JSON for lineage + cadence.",
            },
        )

    m33_probe: dict[str, Any] | None = None
    if m34_cuda_probe_json is not None:
        if m34_cuda_probe_json.is_file():
            m33_probe = _parse_json_object(m34_cuda_probe_json.resolve())
        else:
            blockers.append(
                {
                    "blocker_id": "missing_m34_m33_probe",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": f"M33/M34 CUDA probe JSON not readable: {m34_cuda_probe_json}",
                    "m38_action": "Emit or supply sealed CUDA probe JSON.",
                },
            )
    else:
        blockers.append(
            {
                "blocker_id": "missing_m34_m33_probe",
                "category": "artifact_chain_seals",
                "severity": "high",
                "status": "open",
                "evidence": "--m34-cuda-probe-json not supplied.",
                "m38_action": "Provide sealed M33/M34 CUDA probe JSON.",
            },
        )

    m35_obj: dict[str, Any] | None = None
    if m35_readiness_json is not None:
        if m35_readiness_json.is_file():
            m35_obj = _parse_json_object(m35_readiness_json.resolve())
        else:
            blockers.append(
                {
                    "blocker_id": "missing_m35_readiness",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": f"M35 readiness JSON not readable: {m35_readiness_json}",
                    "m38_action": "Emit M35 readiness JSON.",
                },
            )
    else:
        blockers.append(
            {
                "blocker_id": "missing_m35_readiness",
                "category": "artifact_chain_seals",
                "severity": "high",
                "status": "open",
                "evidence": "--m35-readiness-json not supplied.",
                "m38_action": "Emit sealed M35 readiness JSON.",
            },
        )

    m36_obj: dict[str, Any] | None = None
    m36_status = M36_BINDING_OPTIONAL_NOT_SUPPLIED
    if m36_smoke_execution_json is not None:
        if m36_smoke_execution_json.is_file():
            m36_obj = _parse_json_object(m36_smoke_execution_json.resolve())
            m36_status = M36_BINDING_ENRICHED
        else:
            blockers.append(
                {
                    "blocker_id": "m36_smoke_json_path_invalid",
                    "category": "artifact_chain_seals",
                    "severity": "low",
                    "status": "open",
                    "evidence": f"M36 path not readable: {m36_smoke_execution_json}",
                    "m38_action": "Fix path or omit M36 enrichment.",
                },
            )
    else:
        blockers.append(
            {
                "blocker_id": "m36_smoke_artifact_not_supplied_optional",
                "category": "artifact_chain_seals",
                "severity": "informational",
                "status": "open",
                "evidence": "M36 smoke execution JSON not supplied — optional enrichment only.",
                "m38_action": "Optionally attach sealed M36 smoke execution JSON.",
            },
        )

    _ = m27_rollout_json
    _ = m28_training_json

    if m29_obj is not None:
        if str(m29_obj.get("contract_id") or "") != CONTRACT_ID_M29_FULL_RUN:
            blockers.append(
                {
                    "blocker_id": "contract_id_mismatch_m29",
                    "category": "artifact_chain_seals",
                    "severity": "critical",
                    "status": "open",
                    "evidence": "M29 JSON contract_id mismatch.",
                    "m38_action": "Bind sealed M29 artifact.",
                },
            )
        elif not _canonical_seal_ok(m29_obj):
            blockers.append(
                {
                    "blocker_id": "seal_mismatch_m29",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": "M29 artifact_sha256 canonical seal invalid.",
                    "m38_action": "Re-emit sealed M29 JSON.",
                },
            )
        u27 = str(m29_obj.get("upstream_m27_artifact_sha256") or "").strip().lower()
        if u27 and _is_hex64(u27) and u27 != ANCHOR_UPSTREAM_M27_ARTIFACT_SHA256.lower():
            blockers.append(
                {
                    "blocker_id": "m29_upstream_m27_anchor_mismatch_optional",
                    "category": "artifact_chain_seals",
                    "severity": "medium",
                    "status": "open",
                    "evidence": "M29 upstream_m27_artifact_sha256 differs from public anchor.",
                    "m38_action": "Reconcile rollout seal vs ledger anchors.",
                },
            )

    if m33_probe is not None:
        if str(m33_probe.get("contract_id") or "") != CONTRACT_ID_M33_PROBE:
            blockers.append(
                {
                    "blocker_id": "contract_id_mismatch_m33_probe",
                    "category": "artifact_chain_seals",
                    "severity": "critical",
                    "status": "open",
                    "evidence": "Probe JSON contract_id not M33 CUDA probe.",
                    "m38_action": "Supply sealed M33 probe JSON.",
                },
            )
        if not _canonical_seal_ok(m33_probe, digest_key=M33_DIGEST):
            blockers.append(
                {
                    "blocker_id": "seal_mismatch_m33_probe",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": "M33 CUDA probe artifact_sha256 seal invalid.",
                    "m38_action": "Re-emit probe JSON.",
                },
            )

    if m35_obj is not None:
        if str(m35_obj.get("contract_id") or "") != CONTRACT_ID_M35_READINESS:
            blockers.append(
                {
                    "blocker_id": "contract_id_mismatch_m35",
                    "category": "artifact_chain_seals",
                    "severity": "critical",
                    "status": "open",
                    "evidence": "M35 readiness contract_id mismatch.",
                    "m38_action": "Bind sealed M35 readiness JSON.",
                },
            )
        if str(m35_obj.get("profile_id") or "") != PROFILE_M35_READINESS:
            blockers.append(
                {
                    "blocker_id": "profile_id_mismatch_m35",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": "M35 readiness profile_id mismatch.",
                    "m38_action": "Re-emit readiness JSON.",
                },
            )
        if not _canonical_seal_ok(m35_obj):
            blockers.append(
                {
                    "blocker_id": "seal_mismatch_m35",
                    "category": "artifact_chain_seals",
                    "severity": "high",
                    "status": "open",
                    "evidence": "M35 readiness artifact_sha256 seal invalid.",
                    "m38_action": "Re-emit readiness JSON.",
                },
            )

    if m36_obj is not None:
        if str(m36_obj.get("contract_id") or "") != CONTRACT_ID_M36_EXECUTION:
            blockers.append(
                {
                    "blocker_id": "contract_id_mismatch_m36",
                    "category": "artifact_chain_seals",
                    "severity": "medium",
                    "status": "open",
                    "evidence": "M36 smoke execution contract_id mismatch.",
                    "m38_action": "Use sealed M36 smoke benchmark execution JSON.",
                },
            )

    cand_lineage_shas: dict[str, str] = {}
    if m29_obj:
        cand_lineage_shas["m29"] = _m29_candidate_sha_best_effort(m29_obj)
    if m33_probe:
        cand_lineage_shas["m33"] = _extract_candidate_sha_from_obj(m33_probe)
    if m35_obj:
        cand_lineage_shas["m35"] = _extract_candidate_sha_from_obj(m35_obj)
    if m36_obj:
        cand_lineage_shas["m36"] = _extract_candidate_sha_from_obj(m36_obj)

    uniq_vals = [v for v in cand_lineage_shas.values() if _is_hex64(v)]
    if len(set(uniq_vals)) > 1:
        blockers.append(
            {
                "blocker_id": "candidate_lineage_mismatch",
                "category": "candidate_lineage",
                "severity": "critical",
                "status": "open",
                "evidence": f"Inconsistent candidate SHA across chain keys: {cand_lineage_shas}",
                "m38_action": "Reconcile sealed JSON chain to one candidate SHA.",
            },
        )

    for label, sha in cand_lineage_shas.items():
        if _is_hex64(sha) and sha != exp_sha:
            blockers.append(
                {
                    "blocker_id": f"candidate_sha_mismatch_vs_expected_{label}",
                    "category": "candidate_identity",
                    "severity": "critical",
                    "status": "open",
                    "evidence": f"{label} candidate sha256 {sha} != expected {exp_sha}",
                    "m38_action": "Align operator flags with sealed candidate binding.",
                },
            )

    checkpoint_file_verified = False
    if candidate_checkpoint_path is not None:
        p = candidate_checkpoint_path.resolve()
        if not p.is_file():
            blockers.append(
                {
                    "blocker_id": "candidate_checkpoint_missing",
                    "category": "candidate_identity",
                    "severity": "high",
                    "status": "open",
                    "evidence": f"Candidate checkpoint path missing: {p.name}",
                    "m38_action": "Restore local candidate .pt path for M39.",
                },
            )
        elif authorize_checkpoint_file_sha256:
            file_sha = sha256_file_hex(p)
            checkpoint_file_verified = True
            if file_sha.lower() != exp_sha:
                blockers.append(
                    {
                        "blocker_id": "candidate_sha_mismatch_file_hash",
                        "category": "candidate_identity",
                        "severity": "critical",
                        "status": "open",
                        "evidence": "SHA-256 of .pt file does not match expected candidate hash.",
                        "m38_action": "Verify artifact path / expected hash binding.",
                    },
                )
        else:
            blockers.append(
                {
                    "blocker_id": "candidate_checkpoint_not_hash_authorized",
                    "category": "candidate_identity",
                    "severity": "medium",
                    "status": "open",
                    "evidence": (
                        "Checkpoint path present but --authorize-checkpoint-file-sha256 not set."
                    ),
                    "m38_action": "Authorize file hashing when fingerprinting weights.",
                },
            )

    wc_obs = PUBLIC_LEDGER_M29_OBSERVED_WALL_CLOCK_SECONDS
    ck_count = float(PUBLIC_LEDGER_M29_CHECKPOINT_COUNT)
    tu_count = PUBLIC_LEDGER_M29_TRAINING_UPDATE_COUNT
    cad_src = "ledger_fallback_constants_no_m29_json_loaded"
    if m29_obj:
        wc_obs, ck_int, tu_count, cad_src = _extract_m29_cadence_fields(m29_obj)
        ck_count = float(ck_int)

    cadence_telemetry, cadence_blocker = extrapolate_checkpoint_storage_risk(
        observed_wall_clock_seconds=float(wc_obs),
        checkpoint_count=float(ck_count),
        target_wall_clock_seconds=float(target_wall_clock_seconds),
        cadence_source=cad_src,
        repo_root=repo_root,
    )
    if cadence_blocker is not None:
        blockers.append(cadence_blocker)

    if m29_full_run_json is None and m34_cuda_probe_json is None:
        audit_status = STATUS_BLOCKED_MISSING_REQUIRED_INPUTS

    if allow_operator_local_inspection and run_ctrl["classification"].startswith("no_keyword"):
        blockers.append(
            {
                "blocker_id": "run_control_keywords_not_observed_v15_surface",
                "category": "run_control_interruption_resume",
                "severity": "medium",
                "status": "open",
                "evidence": "Limited interrupt/resume receipt keywords in scanned v15 modules.",
                "m38_action": "Define stop/resume receipts for long runs.",
            },
        )

    blockers, readiness_summary = _finalize_blockers_and_summary(blockers)

    # --- Gates ---
    r5_fail = any(
        b.get("category") == "artifact_chain_seals" and b.get("severity") in ("critical", "high")
        for b in blockers
    )
    lin_fail = any(b.get("blocker_id") == "candidate_lineage_mismatch" for b in blockers)
    disk_fail = any(b.get("blocker_id") == "disk_free_below_threshold" for b in blockers)

    gates = [
        {"gate_id": "R0", "name": "Workspace", "status": "pass" if git_clean else "fail"},
        {
            "gate_id": "R1",
            "name": "Private governance surface",
            "status": (
                "pass"
                if gov["company_secrets_dir_exists"]
                and not gov["git_ls_files_company_secrets_nonempty_tracked_risk"]
                else ("unknown" if not allow_operator_local_inspection else "fail")
            ),
        },
        {
            "gate_id": "R2",
            "name": "CUDA environment",
            "status": (
                "pass"
                if allow_operator_local_inspection
                and env_snap.get("cuda_available")
                and not env_snap.get("torch_probe_error")
                else ("unknown" if not allow_operator_local_inspection else "fail")
            ),
        },
        {
            "gate_id": "R3",
            "name": "SC2 import surface",
            "status": (
                "pass"
                if allow_operator_local_inspection and env_snap.get("sc2_import_ok")
                else ("unknown" if not allow_operator_local_inspection else "fail")
            ),
        },
        {"gate_id": "R4", "name": "Candidate identity", "status": "fail" if lin_fail else "pass"},
        {
            "gate_id": "R5",
            "name": "Artifact chain / seals",
            "status": "fail" if r5_fail else "pass",
        },
        {
            "gate_id": "R6",
            "name": "Runner compatibility (7200s)",
            "status": (
                "fail"
                if runner_scan["m29_horizon_classification_uses_1800_second_literal"]
                else "unknown"
            ),
        },
        {
            "gate_id": "R7",
            "name": "Checkpoint cadence",
            "status": "fail" if cadence_blocker is not None else "pass",
        },
        {"gate_id": "R8", "name": "Disk / retention", "status": "fail" if disk_fail else "pass"},
        {
            "gate_id": "R9",
            "name": "Stop/resume posture",
            "status": (
                "unknown" if run_ctrl["classification"].startswith("no_keyword") else "pass"
            ),
        },
        {"gate_id": "R10", "name": "Monitoring plan", "status": "unknown"},
        {"gate_id": "R11", "name": "Runbook draft", "status": "pass"},
        {"gate_id": "R12", "name": "Non-claims", "status": "pass"},
    ]

    body: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": CONTRACT_ID_M37_DISCOVERY,
        "profile_id": PROFILE_M37_OPERATOR_READINESS,
        "profile": PROFILE_OPERATOR_AUDIT,
        "milestone": MILESTONE_LABEL_M37,
        "emitter_module": EMITTER_MODULE_M37,
        "audit_status": audit_status,
        "workspace_git": {
            "branch": git_branch,
            "porcelain_nonempty": not git_clean,
            "porcelain_snippet": porcelain[:500],
        },
        "private_governance_probe": gov,
        "operator_inspection_allowed": bool(allow_operator_local_inspection),
        "target_run": {
            "target_milestone": "V15-M39",
            "run_class": "two_hour_sc2_backed_t1_continuation_candidate_training",
            "target_wall_clock_seconds": float(target_wall_clock_seconds),
            "operator_local_only": True,
            "ci_execution_allowed": False,
        },
        "optional_inputs_present": {
            "m27_rollout_json": bool(m27_rollout_json and m27_rollout_json.is_file()),
            "m28_training_json": bool(m28_training_json and m28_training_json.is_file()),
            "m29_full_run_json": m29_obj is not None,
            "m34_m33_cuda_probe_json": m33_probe is not None,
            "m35_readiness_json": m35_obj is not None,
            "m36_smoke_execution_json": m36_obj is not None,
        },
        "candidate_checkpoint": {
            "sha256": exp_sha,
            "promotion_status": "not_promoted_candidate_only",
            "checkpoint_file_hash_verified": checkpoint_file_verified,
            "checkpoint_path_supplied": candidate_checkpoint_path is not None,
        },
        "m36_smoke_execution_binding_status": m36_status,
        "candidate_lineage_shas_observed": cand_lineage_shas,
        "environment_snapshot": env_snap,
        "disk_free_gib": disk_free_gb,
        "min_free_disk_gib_config": float(min_free_disk_gb),
        "output_directory": str(output_dir).replace("\\", "/"),
        "output_directory_writable": output_writable,
        "checkpoint_cadence_and_storage": cadence_telemetry,
        "training_update_count_reference": tu_count,
        "runner_compatibility": runner_scan,
        "run_control_posture_scan": run_ctrl,
        "readiness_summary": readiness_summary,
        "blockers": blockers,
        "gates": gates,
        "claim_flags": _claim_flags_all_false(),
        "non_claims": list(NON_CLAIMS_M37),
        "recommended_next": RECOMMENDED_NEXT,
    }
    return body


def emit_m37_fixture(output_dir: Path) -> tuple[dict[str, Any], Path, Path, Path, Path, Path]:
    body_pre = build_fixture_body()
    sealed = seal_m37_body(redact_paths_in_value(body_pre))
    if not isinstance(sealed, dict):
        raise TypeError("expected dict")
    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_rem = output_dir / REMEDIATION_MAP_FILENAME
    p_run = output_dir / RUNBOOK_DRAFT_FILENAME
    rep = build_m37_report(sealed)
    chk = build_m37_checklist_md(sealed)
    rem = build_m38_remediation_map_md(list(sealed.get("blockers") or []))
    runb = build_m39_runbook_draft_md(audit_status=str(sealed.get("audit_status", "")))

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_rem.write_text(rem, encoding="utf-8", newline="\n")
    p_run.write_text(runb, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk + rem + runb
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M37 fixture emission leaked path patterns")
    return sealed, p_main, p_rep, p_chk, p_rem, p_run


def emit_m37_operator_audit(
    output_dir: Path,
    *,
    repo_root: Path,
    allow_operator_local_inspection: bool,
    candidate_checkpoint_path: Path | None,
    expected_candidate_sha256: str | None,
    authorize_checkpoint_file_sha256: bool,
    m27_rollout_json: Path | None,
    m28_training_json: Path | None,
    m29_full_run_json: Path | None,
    m34_cuda_probe_json: Path | None,
    m35_readiness_json: Path | None,
    m36_smoke_execution_json: Path | None,
    target_wall_clock_seconds: float,
    min_free_disk_gb: float,
) -> tuple[dict[str, Any], Path, Path, Path, Path, Path]:
    body_pre = build_operator_audit_body(
        repo_root=repo_root,
        output_dir=output_dir,
        allow_operator_local_inspection=allow_operator_local_inspection,
        candidate_checkpoint_path=candidate_checkpoint_path,
        expected_candidate_sha256=expected_candidate_sha256,
        authorize_checkpoint_file_sha256=authorize_checkpoint_file_sha256,
        m27_rollout_json=m27_rollout_json,
        m28_training_json=m28_training_json,
        m29_full_run_json=m29_full_run_json,
        m34_cuda_probe_json=m34_cuda_probe_json,
        m35_readiness_json=m35_readiness_json,
        m36_smoke_execution_json=m36_smoke_execution_json,
        target_wall_clock_seconds=target_wall_clock_seconds,
        min_free_disk_gb=min_free_disk_gb,
    )
    red = redact_paths_in_value(body_pre)
    if not isinstance(red, dict):
        raise TypeError("expected dict")
    sealed = seal_m37_body(red)

    output_dir.mkdir(parents=True, exist_ok=True)
    p_main = output_dir / FILENAME_MAIN_JSON
    p_rep = output_dir / REPORT_FILENAME
    p_chk = output_dir / CHECKLIST_FILENAME
    p_rem = output_dir / REMEDIATION_MAP_FILENAME
    p_run = output_dir / RUNBOOK_DRAFT_FILENAME

    rep = build_m37_report(sealed)
    chk = build_m37_checklist_md(sealed)
    rem = build_m38_remediation_map_md(list(sealed.get("blockers") or []))
    runb = build_m39_runbook_draft_md(audit_status=str(sealed.get("audit_status", "")))

    p_main.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    p_rep.write_text(canonical_json_dumps(rep), encoding="utf-8")
    p_chk.write_text(chk, encoding="utf-8", newline="\n")
    p_rem.write_text(rem, encoding="utf-8", newline="\n")
    p_run.write_text(runb, encoding="utf-8", newline="\n")

    blob = canonical_json_dumps(sealed) + canonical_json_dumps(rep) + chk + rem + runb
    if emission_has_private_path_patterns(blob):
        raise RuntimeError("M37 operator audit emission leaked path patterns")

    return sealed, p_main, p_rep, p_chk, p_rem, p_run
