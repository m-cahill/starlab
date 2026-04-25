"""Build, seal, and write V15-M08 long GPU training manifest + campaign receipt scaffolding."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.checkpoint_lineage_io import environment_lock_file_canonical_sha256
from starlab.v15.environment_lock_io import redact_paths_in_value
from starlab.v15.environment_lock_models import STATUS_FIXTURE_ONLY, STATUS_OPERATOR_LOCAL_READY
from starlab.v15.long_gpu_training_manifest_models import (
    CAMPAIGN_PLAN_REQUIRED_KEYS,
    CAMPAIGN_STATUS_FIXTURE,
    CAMPAIGN_STATUS_WAITING,
    CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
    CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
    CONTRACT_VERSION,
    EMITTER_MODULE_LONG_GPU_MANIFEST,
    FILENAME_CAMPAIGN_RECEIPT,
    FILENAME_LONG_GPU_TRAINING_MANIFEST,
    FIXTURE_CAMPAIGN_ID,
    GATE_BLOCKED,
    GATE_FIELD_NAMES,
    GATE_NOT_EVALUATED,
    GATE_PASS,
    GATE_WARNING,
    MANIFEST_OPERATOR_DECLARED_TOP_LEVEL_KEYS,
    MILESTONE_ID_V15_M08,
    NON_CLAIMS_V15_M08,
    PLACEHOLDER_SHA256,
    PROFILE_FIXTURE_CI,
    PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
    REPORT_FILENAME_CAMPAIGN_RECEIPT,
    REPORT_FILENAME_LONG_GPU_TRAINING_MANIFEST,
    REPORT_VERSION_MANIFEST,
    REPORT_VERSION_RECEIPT,
    SEAL_KEY_CAMPAIGN_RECEIPT,
    SEAL_KEY_MANIFEST,
    default_m08_authorization_flags,
)
from starlab.v15.training_run_receipt_io import redact_receipt_value
from starlab.v15.training_run_receipt_models import PROFILE_FIXTURE_CI as M07_PROFILE_FIXTURE_CI

SEAL_MANIFEST = SEAL_KEY_MANIFEST
SEAL_RECEIPT = SEAL_KEY_CAMPAIGN_RECEIPT


def _json_file_canonical_sha256(path: Path) -> str:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON must be a single object")
    return sha256_hex_of_canonical_json(raw)


def validate_campaign_plan(plan: Any) -> dict[str, Any]:
    if not isinstance(plan, dict):
        raise ValueError("campaign_plan must be a JSON object")
    missing = [k for k in CAMPAIGN_PLAN_REQUIRED_KEYS if k not in plan]
    if missing:
        raise ValueError(f"campaign_plan missing keys: {missing}")
    nc = plan.get("non_claims")
    if not isinstance(nc, list) or not nc:
        raise ValueError("campaign_plan.non_claims must be a non-empty list")
    return plan


def parse_declared_manifest_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("manifest JSON must be a single object")
    unknown = set(raw.keys()) - MANIFEST_OPERATOR_DECLARED_TOP_LEVEL_KEYS
    if unknown:
        raise ValueError(f"unknown top-level keys in declared manifest: {sorted(unknown)}")
    return raw


def redact_manifest_value(obj: Any) -> Any:
    p = redact_paths_in_value(obj)
    return redact_receipt_value(p)


def all_gates_not_evaluated() -> dict[str, str]:
    return {name: GATE_NOT_EVALUATED for name in GATE_FIELD_NAMES}


def m07_gpu_shakedown_satisfied(m07: dict[str, Any]) -> bool:
    if str(m07.get("profile", "")) == M07_PROFILE_FIXTURE_CI:
        return False
    af = m07.get("authorization_flags")
    if isinstance(af, dict) and af.get("gpu_shakedown_performed") is True:
        return True
    return False


def compute_preflight_gate_statuses(
    *,
    campaign_plan: dict[str, Any],
    environment_lock: dict[str, Any],
    m07_receipt: dict[str, Any],
    checkpoint_lineage: dict[str, Any],
    training_config: dict[str, Any],
    dataset_manifest: dict[str, Any],
    rights_manifest: dict[str, Any],
    strong_agent_scorecard: dict[str, Any] | None,
    xai_evidence: dict[str, Any] | None,
    human_panel_benchmark: dict[str, Any] | None,
) -> dict[str, str]:
    gates: dict[str, str] = {n: GATE_NOT_EVALUATED for n in GATE_FIELD_NAMES}

    if (
        isinstance(campaign_plan.get("non_claims"), list)
        and str(campaign_plan.get("milestone", "")) == MILESTONE_ID_V15_M08
    ):
        gates["gate_a_governance_status"] = GATE_PASS
    elif isinstance(campaign_plan.get("non_claims"), list):
        gates["gate_a_governance_status"] = GATE_WARNING
    else:
        gates["gate_a_governance_status"] = GATE_BLOCKED

    lock_status = str(environment_lock.get("environment_lock_status", ""))
    cuda = environment_lock.get("cuda_environment")
    cuda_ok = isinstance(cuda, dict) and cuda.get("cuda_available") is True
    if lock_status == STATUS_OPERATOR_LOCAL_READY and cuda_ok:
        gates["gate_b_environment_status"] = GATE_PASS
    elif lock_status == STATUS_OPERATOR_LOCAL_READY:
        gates["gate_b_environment_status"] = GATE_WARNING
    elif lock_status == STATUS_FIXTURE_ONLY:
        gates["gate_b_environment_status"] = GATE_NOT_EVALUATED
    else:
        gates["gate_b_environment_status"] = GATE_WARNING

    if dataset_manifest and rights_manifest and training_config:
        gates["gate_c_data_status"] = GATE_PASS
    else:
        gates["gate_c_data_status"] = GATE_BLOCKED

    lineage_rows = checkpoint_lineage.get("checkpoint_lineage")
    if isinstance(lineage_rows, list) and lineage_rows:
        gates["gate_d_checkpoint_status"] = GATE_PASS
    else:
        gates["gate_d_checkpoint_status"] = GATE_WARNING

    if strong_agent_scorecard or human_panel_benchmark:
        gates["gate_e_evaluation_status"] = GATE_PASS
    else:
        gates["gate_e_evaluation_status"] = GATE_WARNING

    gates["gate_f_xai_status"] = GATE_PASS if xai_evidence else GATE_WARNING

    if m07_gpu_shakedown_satisfied(m07_receipt):
        gates["gate_g_operator_status"] = GATE_PASS
    elif str(m07_receipt.get("profile", "")) == M07_PROFILE_FIXTURE_CI:
        gates["gate_g_operator_status"] = GATE_BLOCKED
    else:
        gates["gate_g_operator_status"] = GATE_WARNING

    return gates


def long_campaign_execution_allowed(
    gate_statuses: Mapping[str, Any],
    *,
    governance_override_missing_m07_gpu_shakedown: bool,
) -> tuple[bool, list[str]]:
    blockers: list[str] = []
    g = {k: str(gate_statuses.get(k, GATE_NOT_EVALUATED)) for k in GATE_FIELD_NAMES}

    def req(name: str, allowed: frozenset[str]) -> None:
        v = g.get(name, GATE_NOT_EVALUATED)
        if v not in allowed:
            blockers.append(f"{name}={v}")

    req("gate_a_governance_status", frozenset({GATE_PASS}))
    req("gate_b_environment_status", frozenset({GATE_PASS}))
    req("gate_c_data_status", frozenset({GATE_PASS}))
    req("gate_d_checkpoint_status", frozenset({GATE_PASS}))
    req("gate_e_evaluation_status", frozenset({GATE_PASS, GATE_WARNING}))
    req("gate_f_xai_status", frozenset({GATE_PASS, GATE_WARNING}))

    if g.get("gate_g_operator_status") != GATE_PASS:
        if not governance_override_missing_m07_gpu_shakedown:
            blockers.append("gate_g_operator_status!=pass (M07 GPU shakedown receipt required)")

    ok = not blockers
    return ok, blockers


def seal_long_gpu_training_manifest_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_MANIFEST}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_MANIFEST] = digest
    return sealed


def build_long_gpu_training_manifest_report(
    sealed: dict[str, Any], *, redaction_count: int
) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_MANIFEST}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_long_gpu_training_manifest_report",
        "report_version": REPORT_VERSION_MANIFEST,
        "milestone": MILESTONE_ID_V15_M08,
        "artifact_sha256": digest,
        "seal_field": SEAL_MANIFEST,
        "seal_value_matches_artifact": sealed.get(SEAL_MANIFEST) == digest,
        "redaction_events": int(redaction_count),
        "primary_filename": FILENAME_LONG_GPU_TRAINING_MANIFEST,
    }


def build_long_gpu_training_manifest_body_fixture() -> dict[str, Any]:
    auth = default_m08_authorization_flags()
    gates = all_gates_not_evaluated()
    return {
        "contract_id": CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "profile": PROFILE_FIXTURE_CI,
        "milestone": MILESTONE_ID_V15_M08,
        "created_by": EMITTER_MODULE_LONG_GPU_MANIFEST,
        "campaign_id": FIXTURE_CAMPAIGN_ID,
        "campaign_status": CAMPAIGN_STATUS_FIXTURE,
        "campaign_authorization": "fixture_ci_only",
        "campaign_plan_sha256": PLACEHOLDER_SHA256,
        "repo_identity": {
            "git_branch": "fixture:deterministic",
            "git_sha256_placeholder": PLACEHOLDER_SHA256,
            "narrative": "Fixture repo identity; replace in operator-local manifests.",
        },
        "operator_identity": {
            "posture": "fixture_ci",
            "operator_label": None,
        },
        "public_private_boundary": {
            "posture": "public_governance_only",
            "company_secrets_path_policy": "gitignored_local_only",
        },
        "environment_lock_binding": {
            "environment_lock_json_canonical_sha256": PLACEHOLDER_SHA256,
            "binding_status": "fixture_placeholder",
        },
        "m07_shakedown_binding": {
            "m07_training_run_receipt_sha256": PLACEHOLDER_SHA256,
            "m07_profile": "fixture_ci",
            "gpu_shakedown_evidence": False,
        },
        "training_config_binding": {
            "training_config_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "dataset_manifest_binding": {
            "dataset_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "rights_manifest_binding": {
            "rights_manifest_json_canonical_sha256": PLACEHOLDER_SHA256,
        },
        "checkpoint_lineage_binding": {
            "checkpoint_lineage_manifest_sha256": PLACEHOLDER_SHA256,
        },
        "strong_agent_protocol_binding": {
            "strong_agent_scorecard_json_canonical_sha256": None,
        },
        "xai_contract_binding": {
            "xai_evidence_pack_json_canonical_sha256": None,
        },
        "human_panel_protocol_binding": {
            "human_panel_benchmark_json_canonical_sha256": None,
        },
        "runbook_binding": {
            "primary_runbook_doc": "docs/runtime/v15_long_gpu_campaign_execution_v1.md",
            "binding_status": "fixture_reference_only",
        },
        "storage_policy": {"posture": "local_out_tree_only", "commit_weights": False},
        "checkpoint_policy": {"posture": "operator_local_hashes_only_in_public"},
        "evaluation_policy": {"posture": "cadence_receipts_local_only"},
        "xai_sample_policy": {"posture": "not_executed_in_m08"},
        "stop_resume_policy": {"posture": "inherited_from_m49_m50"},
        "failure_quarantine_policy": {"posture": "operator_local_review"},
        "m49_execution_binding": {
            "execute_module": "starlab.training.execute_full_local_training_campaign",
            "notes": "V15-M08 wraps M49–M51 executor; campaign_plan supplies contract path.",
        },
        "provenance_gaps": [
            "Fixture manifest does not bind a real campaign_plan.json.",
            "No operator-local GPU or M07 shakedown attestation in CI.",
        ],
        "gate_statuses": gates,
        "non_claims": list(NON_CLAIMS_V15_M08),
        "optional_bindings": {},
        "redaction_policy": {
            "fixture": "no_paths_or_secrets",
            "operator_paths": "redact_absolute_paths_and_contacts",
        },
        "authorization_flags": auth,
        "check_results": [
            {
                "check_id": "m08_manifest_shape",
                "description": "Fixture includes required V15-M08 manifest fields.",
                "status": "pass",
            },
            {
                "check_id": "m08_no_unauthorized_flags",
                "description": "long_gpu campaign authorization flags are false in fixture_ci.",
                "status": "pass",
            },
        ],
    }


def build_long_gpu_training_manifest_operator_preflight(
    *,
    campaign_plan: dict[str, Any],
    campaign_plan_sha256: str,
    environment_lock_path: Path,
    checkpoint_lineage_path: Path,
    m07_training_run_receipt_path: Path,
    training_config_path: Path,
    dataset_manifest_path: Path,
    rights_manifest_path: Path,
    strong_agent_scorecard_path: Path | None,
    xai_evidence_path: Path | None,
    human_panel_benchmark_path: Path | None,
) -> dict[str, Any]:
    el = json.loads(environment_lock_path.read_text(encoding="utf-8"))
    cl = json.loads(checkpoint_lineage_path.read_text(encoding="utf-8"))
    m07 = json.loads(m07_training_run_receipt_path.read_text(encoding="utf-8"))
    tc = json.loads(training_config_path.read_text(encoding="utf-8"))
    dm = json.loads(dataset_manifest_path.read_text(encoding="utf-8"))
    rm = json.loads(rights_manifest_path.read_text(encoding="utf-8"))
    sasc = (
        json.loads(strong_agent_scorecard_path.read_text(encoding="utf-8"))
        if strong_agent_scorecard_path
        else None
    )
    xai = json.loads(xai_evidence_path.read_text(encoding="utf-8")) if xai_evidence_path else None
    hpb = (
        json.loads(human_panel_benchmark_path.read_text(encoding="utf-8"))
        if human_panel_benchmark_path
        else None
    )

    if not isinstance(el, dict) or not isinstance(cl, dict) or not isinstance(m07, dict):
        raise ValueError("environment lock, lineage, and M07 receipt must be JSON objects")
    if not isinstance(tc, dict) or not isinstance(dm, dict) or not isinstance(rm, dict):
        raise ValueError("training config, dataset, and rights JSON must be objects")

    gates = compute_preflight_gate_statuses(
        campaign_plan=campaign_plan,
        environment_lock=el,
        m07_receipt=m07,
        checkpoint_lineage=cl,
        training_config=tc,
        dataset_manifest=dm,
        rights_manifest=rm,
        strong_agent_scorecard=sasc,
        xai_evidence=xai,
        human_panel_benchmark=hpb,
    )

    el_sha = environment_lock_file_canonical_sha256(environment_lock_path)
    opt: dict[str, str | None] = {
        "strong_agent_scorecard_json_canonical_sha256": (
            _json_file_canonical_sha256(strong_agent_scorecard_path)
            if strong_agent_scorecard_path
            else None
        ),
        "xai_evidence_pack_json_canonical_sha256": (
            _json_file_canonical_sha256(xai_evidence_path) if xai_evidence_path else None
        ),
        "human_panel_benchmark_json_canonical_sha256": (
            _json_file_canonical_sha256(human_panel_benchmark_path)
            if human_panel_benchmark_path
            else None
        ),
    }

    auth = default_m08_authorization_flags()
    ready, _ = long_campaign_execution_allowed(
        gates, governance_override_missing_m07_gpu_shakedown=False
    )
    campaign_status = CAMPAIGN_STATUS_WAITING if ready else CAMPAIGN_STATUS_FIXTURE

    body: dict[str, Any] = {
        "contract_id": CONTRACT_ID_LONG_GPU_TRAINING_MANIFEST,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "profile": "operator_preflight",
        "milestone": MILESTONE_ID_V15_M08,
        "created_by": EMITTER_MODULE_LONG_GPU_MANIFEST,
        "campaign_id": str(campaign_plan["campaign_id"]),
        "campaign_status": campaign_status,
        "campaign_authorization": "preflight_only_not_execution",
        "campaign_plan_sha256": campaign_plan_sha256,
        "repo_identity": {
            "git_branch": "not_evaluated_preflight",
            "git_sha256_placeholder": PLACEHOLDER_SHA256,
            "narrative": "Bind real git metadata in operator-local final manifests.",
        },
        "operator_identity": {
            "posture": "operator_preflight",
            "operator_label": str(campaign_plan.get("operator", "")),
        },
        "public_private_boundary": {
            "posture": str(campaign_plan.get("public_private_boundary", "operator_local_default")),
            "notes": "Sanitize before any public register row.",
        },
        "environment_lock_binding": {
            "environment_lock_json_canonical_sha256": el_sha,
            "environment_lock_status": el.get("environment_lock_status"),
        },
        "m07_shakedown_binding": {
            "m07_training_run_receipt_sha256": _json_file_canonical_sha256(
                m07_training_run_receipt_path
            ),
            "m07_profile": m07.get("profile"),
            "m07_contract_id": m07.get("contract_id"),
            "gpu_shakedown_evidence": m07_gpu_shakedown_satisfied(m07),
        },
        "training_config_binding": {
            "training_config_json_canonical_sha256": _json_file_canonical_sha256(
                training_config_path
            ),
        },
        "dataset_manifest_binding": {
            "dataset_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                dataset_manifest_path
            ),
        },
        "rights_manifest_binding": {
            "rights_manifest_json_canonical_sha256": _json_file_canonical_sha256(
                rights_manifest_path
            ),
        },
        "checkpoint_lineage_binding": {
            "checkpoint_lineage_manifest_sha256": _json_file_canonical_sha256(
                checkpoint_lineage_path
            ),
        },
        "strong_agent_protocol_binding": {
            "strong_agent_scorecard_json_canonical_sha256": opt[
                "strong_agent_scorecard_json_canonical_sha256"
            ],
        },
        "xai_contract_binding": {
            "xai_evidence_pack_json_canonical_sha256": opt[
                "xai_evidence_pack_json_canonical_sha256"
            ],
        },
        "human_panel_protocol_binding": {
            "human_panel_benchmark_json_canonical_sha256": opt[
                "human_panel_benchmark_json_canonical_sha256"
            ],
        },
        "runbook_binding": {
            "primary_runbook_doc": "docs/runtime/v15_long_gpu_campaign_execution_v1.md",
            "binding_status": "referenced",
        },
        "storage_policy": {
            "posture": str(campaign_plan.get("artifact_retention_policy", "operator_local"))
        },
        "checkpoint_policy": {"posture": "cadence_under_campaign_plan"},
        "evaluation_policy": {
            "posture": "interval_steps",
            "value": campaign_plan.get("evaluation_interval_steps"),
        },
        "xai_sample_policy": {
            "posture": "interval_steps",
            "value": campaign_plan.get("xai_sample_interval_steps"),
        },
        "stop_resume_policy": {
            "stop": campaign_plan.get("stop_policy"),
            "resume": campaign_plan.get("resume_policy"),
        },
        "failure_quarantine_policy": campaign_plan.get("failure_quarantine_policy"),
        "m49_execution_binding": {
            "m49_full_local_training_campaign_contract_path": campaign_plan.get(
                "m49_full_local_training_campaign_contract_path"
            ),
            "execute_module": "starlab.training.execute_full_local_training_campaign",
        },
        "provenance_gaps": [],
        "gate_statuses": gates,
        "non_claims": list(campaign_plan.get("non_claims", ())) + list(NON_CLAIMS_V15_M08),
        "optional_bindings": {k: v for k, v in sorted(opt.items()) if v is not None},
        "redaction_policy": {
            "operator_paths": "redact_absolute_paths_and_contacts",
        },
        "authorization_flags": auth,
        "check_results": [
            {
                "check_id": "m08_preflight_bindings",
                "description": "Canonical SHA-256 bindings computed for declared JSON inputs.",
                "status": "pass",
            }
        ],
    }
    return body


def build_campaign_receipt_body_not_executed(*, campaign_id: str) -> dict[str, Any]:
    auth = default_m08_authorization_flags()
    return {
        "contract_id": CONTRACT_ID_LONG_GPU_CAMPAIGN_RECEIPT,
        "contract_version": CONTRACT_VERSION,
        "profile_id": PROFILE_ID_LONG_GPU_CAMPAIGN_EXECUTION,
        "milestone": MILESTONE_ID_V15_M08,
        "campaign_id": campaign_id,
        "execution_id": "not_executed",
        "execution_start": None,
        "execution_end": None,
        "duration_seconds": None,
        "wall_clock_status": "not_started",
        "training_steps_completed": None,
        "episodes_completed": None,
        "checkpoint_count": 0,
        "checkpoint_hashes": [],
        "final_checkpoint_id": None,
        "final_checkpoint_sha256": None,
        "training_log_sha256": None,
        "eval_receipts": [],
        "resume_receipts": [],
        "rollback_receipts": [],
        "interruptions": [],
        "failure_quarantine_records": [],
        "artifact_inventory_sha256": None,
        "checkpoint_lineage_manifest_sha256": None,
        "operator_local_paths_redacted": True,
        "campaign_completion_status": "not_executed",
        "provenance_gaps": ["No operator-local long campaign execution recorded."],
        "authorization_flags": auth,
        "non_claims": list(NON_CLAIMS_V15_M08),
    }


def seal_campaign_receipt_body(body: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in body.items() if k != SEAL_RECEIPT}
    digest = sha256_hex_of_canonical_json(out)
    sealed = dict(out)
    sealed[SEAL_RECEIPT] = digest
    return sealed


def build_campaign_receipt_report(sealed: dict[str, Any]) -> dict[str, Any]:
    base = {k: v for k, v in sealed.items() if k != SEAL_RECEIPT}
    digest = sha256_hex_of_canonical_json(base)
    return {
        "report_kind": "v15_long_gpu_campaign_receipt_report",
        "report_version": REPORT_VERSION_RECEIPT,
        "milestone": MILESTONE_ID_V15_M08,
        "artifact_sha256": digest,
        "seal_field": SEAL_RECEIPT,
        "primary_filename": FILENAME_CAMPAIGN_RECEIPT,
    }


def emit_campaign_receipt_fixture(
    output_dir: Path, *, campaign_id: str
) -> tuple[dict[str, Any], Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_campaign_receipt_body_not_executed(campaign_id=campaign_id)
    sealed = seal_campaign_receipt_body(body)
    rep = build_campaign_receipt_report(sealed)
    cp = output_dir / FILENAME_CAMPAIGN_RECEIPT
    rp = output_dir / REPORT_FILENAME_CAMPAIGN_RECEIPT
    cp.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    rp.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, cp, rp


def emit_v15_long_gpu_training_manifest_fixture(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    body = build_long_gpu_training_manifest_body_fixture()
    sealed = seal_long_gpu_training_manifest_body(body)
    rep = build_long_gpu_training_manifest_report(sealed, redaction_count=0)
    c_path = output_dir / FILENAME_LONG_GPU_TRAINING_MANIFEST
    r_path = output_dir / REPORT_FILENAME_LONG_GPU_TRAINING_MANIFEST
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    emit_campaign_receipt_fixture(output_dir, campaign_id=FIXTURE_CAMPAIGN_ID)
    return sealed, rep, c_path, r_path


def emit_v15_long_gpu_training_manifest_operator_preflight(
    output_dir: Path,
    *,
    campaign_plan: dict[str, Any],
    environment_lock_path: Path,
    checkpoint_lineage_path: Path,
    m07_training_run_receipt_path: Path,
    training_config_path: Path,
    dataset_manifest_path: Path,
    rights_manifest_path: Path,
    strong_agent_scorecard_path: Path | None,
    xai_evidence_path: Path | None,
    human_panel_benchmark_path: Path | None,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    plan_sha = sha256_hex_of_canonical_json(campaign_plan)
    body = build_long_gpu_training_manifest_operator_preflight(
        campaign_plan=campaign_plan,
        campaign_plan_sha256=plan_sha,
        environment_lock_path=environment_lock_path,
        checkpoint_lineage_path=checkpoint_lineage_path,
        m07_training_run_receipt_path=m07_training_run_receipt_path,
        training_config_path=training_config_path,
        dataset_manifest_path=dataset_manifest_path,
        rights_manifest_path=rights_manifest_path,
        strong_agent_scorecard_path=strong_agent_scorecard_path,
        xai_evidence_path=xai_evidence_path,
        human_panel_benchmark_path=human_panel_benchmark_path,
    )
    sealed = seal_long_gpu_training_manifest_body(body)
    rep = build_long_gpu_training_manifest_report(sealed, redaction_count=0)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "campaign_plan.json").write_text(
        canonical_json_dumps(campaign_plan),
        encoding="utf-8",
    )
    c_path = output_dir / FILENAME_LONG_GPU_TRAINING_MANIFEST
    r_path = output_dir / REPORT_FILENAME_LONG_GPU_TRAINING_MANIFEST
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, c_path, r_path


def emit_v15_long_gpu_training_manifest_operator_declared(
    output_dir: Path,
    manifest_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], int, Path, Path]:
    raw = parse_declared_manifest_json(manifest_path)
    redacted = redact_manifest_value(raw)
    body_for_seal = dict(redacted)
    body_for_seal.pop(SEAL_MANIFEST, None)
    sealed = seal_long_gpu_training_manifest_body(body_for_seal)
    rc = 0
    rep = build_long_gpu_training_manifest_report(sealed, redaction_count=0)
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / FILENAME_LONG_GPU_TRAINING_MANIFEST
    r_path = output_dir / REPORT_FILENAME_LONG_GPU_TRAINING_MANIFEST
    c_path.write_text(canonical_json_dumps(sealed), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return sealed, rep, rc, c_path, r_path
