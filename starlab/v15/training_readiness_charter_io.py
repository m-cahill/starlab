"""Build, seal, and write V15-M00 training readiness charter JSON + report."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.training_readiness_charter_models import (
    ARTIFACT_FAMILY_CONTRACT_IDS_V1,
    AUTHORIZATION_POSTURE_CHARTER_ONLY,
    MILESTONE_ID_V15_M00,
    NON_CLAIMS_V15_M00,
    TRAINING_READINESS_CHARTER_FILENAME,
    TRAINING_READINESS_CHARTER_REPORT_FILENAME,
    TRAINING_READINESS_CHARTER_REPORT_VERSION,
    TRAINING_READINESS_CHARTER_VERSION,
)


def long_gpu_run_gates_v1() -> list[dict[str, Any]]:
    """Structured long-GPU run gate definitions (moonshot §18)."""

    return [
        {
            "gate_id": "A",
            "name": "governance",
            "requirements": [
                "docs_starlab_md_updated_with_v15_pointer",
                "v15_charter_public",
                "claim_boundaries_frozen",
                "non_claims_explicit",
                "private_public_surfaces_defined",
            ],
        },
        {
            "gate_id": "B",
            "name": "environment",
            "requirements": [
                "gpu_detected_for_target_workstation",
                "cuda_pytorch_compatible",
                "sc2_runtime_available",
                "maps_available",
                "disk_space_sufficient",
                "dependency_versions_recorded",
            ],
        },
        {
            "gate_id": "C",
            "name": "data",
            "requirements": [
                "replay_data_manifests_exist",
                "data_hash_recorded",
                "rights_posture_recorded",
                "labels_reproducible",
                "no_unclear_provenance_in_core_training_set",
            ],
        },
        {
            "gate_id": "D",
            "name": "checkpoints",
            "requirements": [
                "checkpoint_hashing_works",
                "parent_child_lineage_works",
                "resume_from_checkpoint_tested",
                "rollback_tested",
                "promotion_rejection_states_tested",
            ],
        },
        {
            "gate_id": "E",
            "name": "evaluation",
            "requirements": [
                "benchmark_scorecard_frozen",
                "fixture_eval_works",
                "live_eval_path_available_where_needed",
                "prior_baselines_recorded",
            ],
        },
        {
            "gate_id": "F",
            "name": "xai",
            "requirements": [
                "xai_contract_frozen",
                "fixture_xai_pack_generated",
                "decision_trace_works",
                "report_generation_works",
            ],
        },
        {
            "gate_id": "G",
            "name": "operator",
            "requirements": [
                "runbook_exists",
                "stop_resume_procedure_tested",
                "artifact_retention_policy_recorded",
                "failure_handling_recorded",
            ],
        },
    ]


def evaluation_ladder_summary_v1() -> list[dict[str, str]]:
    """High-level evaluation ladder (moonshot §20, compact)."""

    return [
        {"id": "E0", "name": "artifact_integrity"},
        {"id": "E1", "name": "fixture_smoke"},
        {"id": "E2", "name": "scripted_baseline_tournament"},
        {"id": "E3", "name": "heuristic_baseline_tournament"},
        {"id": "E4", "name": "prior_starlab_checkpoint_comparison"},
        {"id": "E5", "name": "local_live_sc2_bounded_eval"},
        {"id": "E6", "name": "exploit_failure_mode_probe"},
        {"id": "E7", "name": "human_panel_benchmark"},
        {"id": "E8", "name": "xai_explanation_review"},
    ]


def xai_demonstration_surfaces_v1() -> dict[str, Any]:
    """Minimum XAI artifact names for v1.5 demonstration (moonshot §10 / §3 pillar 3)."""

    return {
        "minimum_artifact_basenames": [
            "xai_manifest.json",
            "replay_identity.json",
            "checkpoint_identity.json",
            "decision_trace.json",
            "critical_decision_index.json",
            "attribution_summary.json",
            "concept_activation_summary.json",
            "counterfactual_probe_results.json",
            "alternative_action_rankings.json",
            "uncertainty_report.json",
            "replay_overlay_manifest.json",
            "xai_explanation_report.md",
        ],
        "demo_coverage_requirements": [
            "at_least_one_win",
            "at_least_one_loss_or_failure_case",
            "at_least_one_macro_decision",
            "at_least_one_tactical_or_combat_decision",
            "at_least_one_scouting_or_uncertainty_decision",
            "at_least_one_counterfactual_explanation",
        ],
    }


def carry_forward_risks_v1() -> list[dict[str, str]]:
    """M32-family risks recorded for v1.5 (moonshot §15, compact)."""

    return [
        {
            "risk_id": "coverage_gate",
            "summary": "Meaningful coverage and merge-gate policy before training-heavy changes",
        },
        {
            "risk_id": "ci_tiering",
            "summary": ("Document fast/slow/operator-local CI split; default path stays truthful"),
        },
        {
            "risk_id": "json_io_dedup",
            "summary": "Converge or inventory JSON I/O duplication for long-run manifests",
        },
        {
            "risk_id": "architecture_overview",
            "summary": "Training-scale architecture / runbook clarity for operators",
        },
        {
            "risk_id": "provenance",
            "summary": "Replay, data, weights, benchmark provenance at training scale",
        },
    ]


def configuration_reproducibility_governance_v1() -> dict[str, Any]:
    """High-level config/repro fields v1.5 runs should bind (moonshot §12)."""

    return {
        "identity_fields": [
            "git_sha",
            "branch",
            "milestone",
            "python_version",
            "dependency_lock_or_hash",
            "cuda_version",
            "pytorch_version",
            "gpu_identity",
            "sc2_client_version",
            "map_pool",
            "run_seed_policy",
            "dataset_hash",
            "checkpoint_hash",
            "config_hash",
        ],
        "run_manifest_artifacts": [
            "training_manifest.json",
            "environment_manifest.json",
            "hardware_manifest.json",
            "dataset_manifest.json",
            "checkpoint_manifest.json",
            "evaluation_manifest.json",
            "xai_manifest.json",
            "human_benchmark_manifest.json",
            "rights_manifest.json",
        ],
    }


def v15_milestone_map_excerpt_v1() -> list[dict[str, str]]:
    """Milestone table excerpt starting at V15-M00 (moonshot §17)."""

    return [
        {"id": "V15-M00", "title": "Training Readiness Charter and Long GPU Run Gate"},
        {"id": "V15-M01", "title": "Training-Scale Provenance and Asset Registers"},
        {"id": "V15-M02", "title": "Long GPU Run Environment Lock"},
        {"id": "V15-M03", "title": "Checkpoint Lineage and Resume Discipline"},
        {"id": "V15-M04", "title": "XAI Evidence Contract v1"},
        {"id": "V15-M05", "title": "Strong-Agent Benchmark Protocol"},
        {"id": "V15-M06", "title": "Human Panel Benchmark Protocol"},
        {"id": "V15-M07", "title": "Training Smoke and Short GPU Shakedown"},
        {"id": "V15-M08", "title": "Long GPU Campaign Execution"},
        {"id": "V15-M09", "title": "Checkpoint Evaluation and Promotion"},
        {"id": "V15-M10", "title": "Replay-Native XAI Demonstration"},
        {"id": "V15-M11", "title": "Human Panel / Bounded Human Benchmark"},
        {"id": "V15-M12", "title": "Showcase Agent Release Pack"},
        {"id": "V15-M13", "title": "v2 Go / No-Go Decision"},
    ]


def build_training_readiness_charter_body() -> dict[str, Any]:
    """Canonical charter body (without seal field)."""

    return {
        "charter_version": TRAINING_READINESS_CHARTER_VERSION,
        "milestone_id": MILESTONE_ID_V15_M00,
        "program_phase": "v1.5",
        "primary_domain": "starcraft2_terran_1v1",
        "authorization_posture": AUTHORIZATION_POSTURE_CHARTER_ONLY,
        "public_authority_markdown": "docs/starlab-v1.5.md",
        "runtime_charter_markdown": "docs/runtime/v15_training_readiness_charter_v1.md",
        "non_claims": list(NON_CLAIMS_V15_M00),
        "artifact_family_contract_ids": list(ARTIFACT_FAMILY_CONTRACT_IDS_V1),
        "long_gpu_run_gates": long_gpu_run_gates_v1(),
        "evaluation_ladder": evaluation_ladder_summary_v1(),
        "xai_demonstration_surfaces": xai_demonstration_surfaces_v1(),
        "configuration_reproducibility_governance": configuration_reproducibility_governance_v1(),
        "carry_forward_risks": carry_forward_risks_v1(),
        "milestone_map_excerpt": v15_milestone_map_excerpt_v1(),
    }


def seal_training_readiness_charter(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "training_readiness_charter_sha256": digest}


def build_training_readiness_charter_report(charter: dict[str, Any]) -> dict[str, Any]:
    digest = charter["training_readiness_charter_sha256"]
    gates = charter["long_gpu_run_gates"]
    return {
        "report_version": TRAINING_READINESS_CHARTER_REPORT_VERSION,
        "milestone_id": MILESTONE_ID_V15_M00,
        "charter_version": TRAINING_READINESS_CHARTER_VERSION,
        "training_readiness_charter_sha256": digest,
        "validation": {
            "charter_version_recognized": charter["charter_version"]
            == TRAINING_READINESS_CHARTER_VERSION,
            "gate_count": len(gates),
            "expected_gate_count": 7,
            "artifact_family_count": len(charter["artifact_family_contract_ids"]),
            "expected_artifact_family_count": len(ARTIFACT_FAMILY_CONTRACT_IDS_V1),
        },
    }


def write_training_readiness_charter_artifacts(
    *,
    output_dir: Path,
    charter: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    c_path = output_dir / TRAINING_READINESS_CHARTER_FILENAME
    r_path = output_dir / TRAINING_READINESS_CHARTER_REPORT_FILENAME
    c_path.write_text(canonical_json_dumps(charter), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path


def emit_training_readiness_charter(
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    body = build_training_readiness_charter_body()
    sealed = seal_training_readiness_charter(body)
    rep = build_training_readiness_charter_report(sealed)
    c_path, r_path = write_training_readiness_charter_artifacts(
        output_dir=output_dir, charter=sealed, report=rep
    )
    return sealed, rep, c_path, r_path
