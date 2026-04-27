"""Build, seal, and write V15-M17 long GPU campaign evidence + runbook + checklist."""

# ruff: noqa: E501

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.long_gpu_campaign_evidence_models import (
    ALL_READINESS_GATE_IDS,
    CAMPAIGN_EVIDENCE_STATUS_DECLARED,
    CAMPAIGN_EVIDENCE_STATUS_FIXTURE,
    CAMPAIGN_EVIDENCE_STATUS_LOCAL_GUARDS,
    CAMPAIGN_EVIDENCE_STATUS_PREFLIGHT,
    CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE,
    EMITTER_MODULE_LONG_GPU_CAMPAIGN_EVIDENCE,
    FILENAME_CAMPAIGN_RECEIPT,
    FILENAME_CLOSEOUT_CHECKLIST_MD,
    FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE,
    FILENAME_RUNBOOK_MD,
    GATE_POSTURE_BLOCKED_OR_FIXTURE,
    GATE_POSTURE_NOT_EVALUATED,
    GATE_POSTURE_PASS,
    GATE_POSTURE_PASS_FIXTURE,
    L0,
    L1,
    L2,
    L3,
    L4,
    L5,
    L6,
    L7,
    L8,
    L9,
    L10,
    L11,
    L12,
    L13,
    L14,
    L15,
    M18_DEPENDENCY_NOTE,
    MILESTONE_ID_V15_M17,
    NON_CLAIMS_V15_M17,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
    PROFILE_OPERATOR_PREFLIGHT,
    REGISTER_TOUCHPOINT_PATHS,
    REPORT_FILENAME_CAMPAIGN_RECEIPT,
    REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE,
    REPORT_VERSION_LONG_GPU_CAMPAIGN_EVIDENCE,
    SEAL_KEY_ARTIFACT,
)
from starlab.v15.long_gpu_training_manifest_io import (
    build_campaign_receipt_body_not_executed,
    build_campaign_receipt_report,
    seal_campaign_receipt_body,
)
from starlab.v15.long_gpu_training_manifest_models import (
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    MILESTONE_ID_V15_M08,
)
from starlab.v15.short_gpu_environment_models import (
    CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
    EVIDENCE_STATUS_PROBE_SUCCESS,
    M17_READY_PLANNING,
    M17_READY_PREFLIGHT,
    PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE,
    SHORT_GPU_PROBE_SUCCESS,
)

_SEAL = SEAL_KEY_ARTIFACT


def parse_m16_short_gpu_environment_for_m17(path: Path) -> tuple[str, dict[str, Any]]:
    """Validate M16 JSON for M17 preflight; return (canonical_sha256, sanitized summary)."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("M16 JSON must be a single object")
    if str(raw.get("contract_id", "")) != CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE:
        raise ValueError(
            f"M16 binding: contract_id must be {CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE!r}"
        )
    if str(raw.get("profile", "")) != PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE:
        raise ValueError(
            f"M16 binding: profile must be {PROFILE_OPERATOR_LOCAL_SHORT_GPU_PROBE!r} "
            "for operator preflight"
        )
    if str(raw.get("evidence_status", "")) != EVIDENCE_STATUS_PROBE_SUCCESS:
        raise ValueError("M16 binding: evidence_status must be operator_local_probe_success")
    if raw.get("operator_local_execution_performed") is not True:
        raise ValueError("M16 binding: operator_local_execution_performed must be true")
    if raw.get("short_gpu_probe_performed") is not True:
        raise ValueError("M16 binding: short_gpu_probe_performed must be true")
    if str(raw.get("short_gpu_probe_result", "")) != SHORT_GPU_PROBE_SUCCESS:
        raise ValueError("M16 binding: short_gpu_probe_result must be success")
    m17_rec = str(raw.get("m17_opening_recommendation", ""))
    if m17_rec not in (M17_READY_PLANNING, M17_READY_PREFLIGHT):
        raise ValueError(
            f"M16 binding: m17_opening_recommendation not compatible (got {m17_rec!r})"
        )
    if raw.get("long_gpu_run_authorized") is not False:
        raise ValueError("M16 binding: long_gpu_run_authorized must remain false")
    if raw.get("v2_authorized") is not False:
        raise ValueError("M16 binding: v2_authorized must be false")
    if raw.get("v2_recharter_authorized") is not False:
        raise ValueError("M16 binding: v2_recharter_authorized must be false")
    if raw.get("cuda_available") is not True:
        raise ValueError("M16 binding: cuda_available must be true when present for M17 preflight")
    if raw.get("torch_imported") is not True:
        raise ValueError("M16 binding: torch_imported must be true when present for M17 preflight")

    sha = sha256_hex_of_canonical_json(raw)
    summary = {
        "gpu_name": raw.get("gpu_name"),
        "gpu_memory_summary": raw.get("gpu_memory_summary"),
        "torch_version": raw.get("torch_version"),
        "cuda_version": raw.get("cuda_version"),
        "cuda_available": raw.get("cuda_available"),
        "m17_opening_recommendation": m17_rec,
    }
    return sha, summary


def _register_rows() -> list[dict[str, str]]:
    return [{"register_doc": p, "role": "touchpoint"} for p in REGISTER_TOUCHPOINT_PATHS]


def _build_readiness_gates(
    *,
    profile: str,
    m16_preflight_evaluated: bool,
) -> list[dict[str, str]]:
    def row(
        gate_id: str,
        name: str,
        default_status: str,
        notes: str,
    ) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "name": name,
            "default_status": default_status,
            "notes": notes,
        }

    l1 = GATE_POSTURE_NOT_EVALUATED if not m16_preflight_evaluated else GATE_POSTURE_PASS
    r = [
        row(
            L0,
            "M16 environment evidence bound or fixture placeholder used",
            GATE_POSTURE_PASS_FIXTURE,
            "Binds M16 short GPU evidence by canonical SHA when operator supplies JSON.",
        ),
        row(
            L1,
            "M16 CUDA / Torch / GPU probe success verified when operator evidence supplied",
            l1,
            "When M16 is bound for preflight, probe fields must show success (validated in code).",
        ),
        row(
            L2,
            "Private campaign output root declared / redacted",
            GATE_POSTURE_PASS_FIXTURE,
            "No raw private roots in public commits; use policy + redaction.",
        ),
        row(
            L3,
            "Long campaign requires explicit dual/triple guards",
            GATE_POSTURE_PASS,
            "M08 runner + M17 local profile require allow + authorize + confirm.",
        ),
        row(
            L4,
            "Campaign duration / stop policy declared",
            GATE_POSTURE_PASS_FIXTURE,
            "Manifest-driven; see campaign_plan in evidence JSON.",
        ),
        row(
            L5,
            "Checkpoint cadence / retention policy declared",
            GATE_POSTURE_PASS_FIXTURE,
            "Placeholder until operator campaign plan is bound.",
        ),
        row(
            L6,
            "Evaluation cadence / baseline policy declared or deferred",
            GATE_POSTURE_PASS_FIXTURE,
            "M18 evaluates candidates; M17 may defer eval cadence in fixture.",
        ),
        row(
            L7,
            "Dataset / replay / rights references declared or blocked",
            GATE_POSTURE_BLOCKED_OR_FIXTURE,
            "Default fixture does not assert cleared dataset rights.",
        ),
        row(
            L8,
            "Storage and archival policy declared",
            GATE_POSTURE_PASS_FIXTURE,
            "See storage_and_retention_policy.",
        ),
        row(
            L9,
            "Stop/resume/interruption policy declared",
            GATE_POSTURE_PASS_FIXTURE,
            "Interruption and resume receipts required on real long runs per plan.",
        ),
        row(
            L10,
            "Private paths and artifacts not committed",
            GATE_POSTURE_PASS,
            "Enforced by review + .gitignore; M17 does not commit operator outputs.",
        ),
        row(
            L11,
            "No strong-agent/human/v2/showcase claims",
            GATE_POSTURE_PASS,
            "Non-claims block in JSON and runtime doc.",
        ),
        row(
            L12,
            "Execution status recorded honestly",
            GATE_POSTURE_PASS_FIXTURE,
            "Fixture: no campaign; operator: receipts must match fact.",
        ),
        row(
            L13,
            "Receipt requirements declared (M08 receipt contract for execution)",
            GATE_POSTURE_PASS_FIXTURE,
            f"Use {CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT} for campaign receipts when executed.",
        ),
        row(
            L14,
            "M18 checkpoint/eval dependency declared",
            GATE_POSTURE_PASS,
            M18_DEPENDENCY_NOTE,
        ),
        row(
            L15,
            "Runtime, v1.5 doc, rights register, and tests aligned",
            GATE_POSTURE_PASS_FIXTURE,
            "CI validates emitter + docs references.",
        ),
    ]
    assert [x["gate_id"] for x in r] == list(ALL_READINESS_GATE_IDS)
    return r


def _default_campaign_plan() -> dict[str, Any]:
    return {
        "planned_wall_clock_hours": 12,
        "hard_stop_wall_clock_hours": 24,
        "checkpoint_cadence_minutes": 30,
        "eval_cadence_minutes": 60,
        "eval_cadence_note": "May defer eval to M18; not a default benchmark execution claim.",
        "resume_policy": "required",
        "interruption_receipts_policy": "required_if_interrupted",
        "private_output_root_posture": "out/v15_m17_long_gpu_campaign/run_001_redacted_in_public",
        "config_source": "operator_manifest_m08",
        "note": "Real duration comes from M08 campaign_plan.json; values here are governed defaults for preflight only.",
    }


def _default_checkpoint_policy() -> dict[str, Any]:
    return {
        "cadence": "operator_declared_in_m08_plan",
        "lineage_for_m18": [
            "checkpoint_id",
            "parent_checkpoint_id",
            "checkpoint_sha256",
            "training_step",
            "wall_clock_markers",
            "config_hash",
            "dataset_manifest_refs",
        ],
    }


def _default_eval_policy() -> dict[str, Any]:
    return {
        "posture": "deferred_to_m18_candidate_eval",
        "note": "M17 collects training campaign evidence; M18 runs checkpoint evaluation evidence.",
    }


def _default_interruption_policy() -> dict[str, Any]:
    return {
        "resume_required": True,
        "interruption_receipts": "required_if_interrupted",
        "operator_failure_handling": "quarantine_per_m08_runbook",
    }


def _default_storage_policy() -> dict[str, Any]:
    return {
        "public_commit_scope": "schemas_manifests_governance_json_only",
        "local_scope": "weights_checkpoints_logs_replays_under_out",
        "retention": "operator_archival_policy",
    }


def _default_rights_policy() -> dict[str, Any]:
    return {
        "posture": "blocked_or_incomplete_until_review",
        "registers": list(REGISTER_TOUCHPOINT_PATHS),
    }


def _default_public_private() -> dict[str, Any]:
    return {
        "public_safe": [
            "contract_id",
            "gate_id",
            "status_fields",
            "sha256_bindings",
            "sanitized_gpu_summary",
        ],
        "private_local_only_by_default": [
            "raw_model_weights",
            "checkpoint_blobs",
            "full_training_logs",
            "tensorboard_traces",
            "absolute_output_paths",
            "unredacted_m16_paths_in_public_commits",
        ],
    }


def _default_execution_guards() -> dict[str, Any]:
    return {
        "allow_operator_local_execution_required": True,
        "authorize_long_gpu_campaign_required": True,
        "confirm_private_artifacts_required": True,
        "m08_emitter": "starlab.v15.emit_v15_long_gpu_training_manifest",
        "m08_runner": "starlab.v15.run_v15_long_gpu_campaign",
        "m17_emitter_does_not_run_torch_training": True,
    }


def _upstream_placeholder() -> dict[str, Any]:
    return {
        "binding_mode": "fixture_placeholder",
        "contract_id_expected": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
        "m16_short_gpu_environment_json_canonical_sha256": PLACEHOLDER_SHA256,
        "note": "Supply M16 JSON via --m16-short-gpu-environment-json in operator_preflight profile.",
    }


def _non_claims_list() -> list[str]:
    return [NON_CLAIMS_V15_M17]


def build_long_gpu_campaign_evidence_body(
    *,
    profile: str,
    m16_path: Path | None = None,
    allow_operator_local_execution: bool = False,
    authorize_long_gpu_campaign: bool = False,
    confirm_private_artifacts: bool = False,
    operator_campaign_path: Path | None = None,
    planned_wall_clock_hours: int = 12,
) -> dict[str, Any]:
    m16_bound = False
    m16_summary: dict[str, Any] = {}
    m16_sha = PLACEHOLDER_SHA256
    upstream: dict[str, Any] = dict(_upstream_placeholder())

    if profile == PROFILE_OPERATOR_DECLARED:
        if operator_campaign_path is None:
            raise ValueError("operator_declared requires --operator-campaign-json")
        raw = json.loads(operator_campaign_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("operator campaign JSON must be a single object")
        red = redact_paths_in_value(raw)
        cid = str(red.get("contract_id", ""))
        if cid and cid != CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE:
            raise ValueError(
                f"operator_declared: contract_id must be {CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE!r} if set"
            )
        m16_eval = bool(
            isinstance(red.get("m16_environment_evidence_summary"), dict)
            and str(red.get("m16_json_canonical_sha256", "")) not in ("", PLACEHOLDER_SHA256)
        )
        rg = red.get("readiness_gates")
        got = (
            {str(x.get("gate_id", "")) for x in rg if isinstance(x, dict)}
            if isinstance(rg, list)
            else set()
        )
        if got != set(ALL_READINESS_GATE_IDS):
            red["readiness_gates"] = _build_readiness_gates(
                profile=profile, m16_preflight_evaluated=m16_eval
            )
        else:
            red["readiness_gates"] = redact_paths_in_value(rg)
        if "contract_id" not in red:
            red["contract_id"] = CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE
        if "milestone" not in red:
            red["milestone"] = MILESTONE_ID_V15_M17
        if "emitter_module" not in red:
            red["emitter_module"] = EMITTER_MODULE_LONG_GPU_CAMPAIGN_EVIDENCE
        red["profile"] = profile
        red["campaign_evidence_status"] = CAMPAIGN_EVIDENCE_STATUS_DECLARED
        if "register_touchpoints" not in red:
            red["register_touchpoints"] = _register_rows()
        if "non_claims" not in red:
            red["non_claims"] = _non_claims_list()
        if "public_private_boundary" not in red:
            red["public_private_boundary"] = _default_public_private()
        if "m16_json_canonical_sha256" not in red:
            red["m16_json_canonical_sha256"] = PLACEHOLDER_SHA256
        return cast(dict[str, Any], red)

    if profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN:
        if not (
            allow_operator_local_execution
            and authorize_long_gpu_campaign
            and confirm_private_artifacts
        ):
            raise ValueError(
                "operator_local_long_gpu_campaign requires triple guard: "
                "allow_operator_local_execution, authorize_long_gpu_campaign, "
                "confirm_private_artifacts"
            )
        if m16_path is None:
            raise ValueError(
                "operator_local_long_gpu_campaign requires --m16-short-gpu-environment-json"
            )

    m16_eval = False
    if m16_path is not None and profile in (
        PROFILE_OPERATOR_PREFLIGHT,
        PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
    ):
        m16_sha, m16_summary = parse_m16_short_gpu_environment_for_m17(m16_path)
        m16_bound = True
        m16_eval = True
        upstream = {
            "binding_mode": "m16_file_bound",
            "m16_short_gpu_environment_json_canonical_sha256": m16_sha,
            "m16_contract_id_readonly": CONTRACT_ID_SHORT_GPU_ENVIRONMENT_EVIDENCE,
        }

    if profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN:
        m17_opening = "ready_for_m08_delegation"
        ce_status = CAMPAIGN_EVIDENCE_STATUS_LOCAL_GUARDS
        l_started = False
        l_done = False
    elif profile == PROFILE_OPERATOR_PREFLIGHT:
        if m16_path is None:
            raise ValueError("operator_preflight requires --m16-short-gpu-environment-json")
        m17_opening = "ready_for_operator_authorization"
        ce_status = CAMPAIGN_EVIDENCE_STATUS_PREFLIGHT
        l_started = False
        l_done = False
    else:
        m17_opening = "fixture_only"
        ce_status = CAMPAIGN_EVIDENCE_STATUS_FIXTURE
        l_started = False
        l_done = False
        m16_eval = False

    if profile == PROFILE_FIXTURE_CI:
        upstream = _upstream_placeholder()

    campaign_plan = _default_campaign_plan()
    if profile != PROFILE_FIXTURE_CI:
        campaign_plan = dict(campaign_plan)
        campaign_plan["planned_wall_clock_hours"] = int(planned_wall_clock_hours)

    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_EVIDENCE,
        "milestone": MILESTONE_ID_V15_M17,
        "emitter_module": EMITTER_MODULE_LONG_GPU_CAMPAIGN_EVIDENCE,
        "profile": profile,
        "campaign_evidence_status": ce_status,
        "operator_local_execution_performed": profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN,
        "long_gpu_campaign_started": l_started,
        "long_gpu_campaign_completed": l_done,
        "long_gpu_run_authorized": False,
        "m17_campaign_opening_status": m17_opening,
        "v2_authorized": False,
        "v2_recharter_authorized": False,
        "upstream_bindings": upstream,
        "m16_environment_evidence_summary": (
            m16_summary
            if m16_bound
            else {
                "binding": "no_m16_file_in_fixture",
                "note": "Use operator_preflight to bind M16 by SHA.",
            }
        ),
        "m16_json_canonical_sha256": m16_sha,
        "campaign_plan": campaign_plan,
        "execution_guards": _default_execution_guards(),
        "checkpoint_policy": _default_checkpoint_policy(),
        "evaluation_policy": _default_eval_policy(),
        "interruption_resume_policy": _default_interruption_policy(),
        "storage_and_retention_policy": _default_storage_policy(),
        "rights_and_asset_policy": _default_rights_policy(),
        "readiness_gates": _build_readiness_gates(
            profile=profile, m16_preflight_evaluated=m16_eval
        ),
        "public_private_boundary": _default_public_private(),
        "register_touchpoints": _register_rows(),
        "non_claims": _non_claims_list(),
    }
    if profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN:
        body["m17_m08_delegation_note"] = (
            "M17 does not execute training. After preflight, run: python -m starlab.v15.run_v15_long_gpu_campaign "
            "with sealed M08 v15_long_gpu_training_manifest.json, matching campaign_plan.json, and output root — "
            "see docs/runtime/v15_long_gpu_campaign_evidence_v1.md and v15_long_gpu_campaign_execution_v1.md."
        )
    return body


def _seal(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != _SEAL}
    d = sha256_hex_of_canonical_json(out)
    sealed = dict(body)
    sealed[_SEAL] = d
    return sealed


def _build_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != _SEAL}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_long_gpu_campaign_evidence_report",
        "report_version": REPORT_VERSION_LONG_GPU_CAMPAIGN_EVIDENCE,
        "milestone": MILESTONE_ID_V15_M17,
        "primary_filename": FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE,
        "artifact_sha256": digest,
        "seal_field": _SEAL,
        "seal_value_matches_artifact": True,
    }


def _runbook_md() -> str:
    return f"""# V15-M17 long GPU campaign runbook (governance)

**Milestone:** {MILESTONE_ID_V15_M17}
**Non-claims:** {NON_CLAIMS_V15_M17}

## Operator flow (summary)

1. Ensure M16 short GPU probe success JSON exists (private path; SHA binding in M17 preflight only).
2. Emit M17 `operator_preflight` evidence in a private `out/` directory.
3. Emit / validate M08 `v15_long_gpu_training_manifest` + `campaign_plan.json` (see M08 runtime doc).
4. Run **only** with explicit guards: `python -m starlab.v15.run_v15_long_gpu_campaign` (see M08) — M17 does not wrap the trainer.

## Stop / resume

Follow `docs/runtime/v15_long_gpu_campaign_execution_v1.md` and M08 manifest stop/resume policy. M17 records planning posture and gates; M08 receipts record execution facts.

## M18

{M18_DEPENDENCY_NOTE}
"""


def _checklist_md() -> str:
    return f"""# V15-M17 long GPU campaign — closeout checklist (template)

- [ ] M16 evidence bound by canonical JSON SHA-256 in M17 preflight output.
- [ ] M08 long GPU manifest + campaign plan match (`campaign_plan_sha256`) before any run.
- [ ] M08 run used dual guards; private outputs not committed.
- [ ] If a real campaign completed: M08 `starlab.v15.long_gpu_campaign_receipt.v1` exists and is sealed; interruption/resume receipts present if applicable.
- [ ] No strong-agent, human-benchmark, showcase, ladder, or v2 claims added without governed downstream milestones.
- [ ] {M18_DEPENDENCY_NOTE}
"""


def _m17_stub_receipt(*, campaign_id: str, m16_sha: str) -> dict[str, Any]:
    """Stub receipt: M08 contract, M17 context; not_executed; deterministic fields."""
    base = build_campaign_receipt_body_not_executed(campaign_id=campaign_id)
    base = dict(base)
    base["milestone"] = MILESTONE_ID_V15_M17
    base["m17_evidence_footprint"] = {
        "m16_environment_json_canonical_sha256": m16_sha,
        "receipt_role": "m17_operator_local_guards_no_training",
        "m08_milestone_in_base_receipt": MILESTONE_ID_V15_M08,
    }
    base["provenance_gaps"] = list(base.get("provenance_gaps", [])) + [
        "M17 guard acknowledgment only; M08 training not invoked by M17 emitter.",
    ]
    return seal_campaign_receipt_body(base)


def emit_v15_long_gpu_campaign_evidence(
    output_dir: Path,
    *,
    profile: str = PROFILE_FIXTURE_CI,
    m16_path: Path | None = None,
    allow_operator_local_execution: bool = False,
    authorize_long_gpu_campaign: bool = False,
    confirm_private_artifacts: bool = False,
    operator_campaign_path: Path | None = None,
    planned_wall_clock_hours: int = 12,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, Path, Path]:
    """Write M17 campaign evidence JSON, report, runbook, checklist.

    `operator_local_long_gpu_campaign` also writes a deterministic not-executed M08-receipt contract stub
    (guards only; no training invoked by M17).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_long_gpu_campaign_evidence_body(
        profile=profile,
        m16_path=m16_path,
        allow_operator_local_execution=allow_operator_local_execution,
        authorize_long_gpu_campaign=authorize_long_gpu_campaign,
        confirm_private_artifacts=confirm_private_artifacts,
        operator_campaign_path=operator_campaign_path,
        planned_wall_clock_hours=planned_wall_clock_hours,
    )
    sealed = _seal(body)
    rep = _build_report(sealed)
    jp = output_dir / FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE
    rp = output_dir / REPORT_FILENAME_LONG_GPU_CAMPAIGN_EVIDENCE
    run = output_dir / FILENAME_RUNBOOK_MD
    chk = output_dir / FILENAME_CLOSEOUT_CHECKLIST_MD
    jp.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    rp.write_text(canonical_json_dumps(rep), encoding="utf-8")
    run.write_text(_runbook_md(), encoding="utf-8", newline="\n")
    chk.write_text(_checklist_md(), encoding="utf-8", newline="\n")

    if profile == PROFILE_OPERATOR_LOCAL_LONG_GPU_CAMPAIGN:
        m16_sha = str(sealed.get("m16_json_canonical_sha256", PLACEHOLDER_SHA256))
        rc = _m17_stub_receipt(
            campaign_id="v15_m17:operator_local:guards_acknowledged",
            m16_sha=m16_sha,
        )
        rrep = build_campaign_receipt_report(rc)
        (output_dir / FILENAME_CAMPAIGN_RECEIPT).write_text(
            canonical_json_dumps(rc), encoding="utf-8"
        )
        (output_dir / REPORT_FILENAME_CAMPAIGN_RECEIPT).write_text(
            canonical_json_dumps(rrep), encoding="utf-8"
        )
    return sealed, rep, jp, rp, run, chk


__all__ = [
    "build_long_gpu_campaign_evidence_body",
    "emit_v15_long_gpu_campaign_evidence",
    "parse_m16_short_gpu_environment_for_m17",
]
