"""Governance tests: required documentation and placeholder files exist."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_GOVERNANCE_DOCS = [
    "docs/starlab_archive.md",
    "docs/architecture.md",
    "docs/getting_started_clone_to_run.md",
    "docs/starlab_operating_manual_v0.md",
    "docs/audit/DeferredIssuesRegistry.md",
    "docs/public_private_boundary.md",
    "docs/replay_data_provenance.md",
    "docs/rights_register.md",
    "docs/branding_and_naming.md",
    "docs/deployment/deployment_posture.md",
    "docs/deployment/env_matrix.md",
    "docs/runtime/sc2_runtime_surface.md",
    "docs/runtime/environment_lock.md",
    "docs/runtime/match_execution_harness.md",
    "docs/runtime/run_identity_lineage_seed.md",
    "docs/runtime/replay_binding.md",
    "docs/runtime/canonical_run_artifact_v0.md",
    "docs/runtime/environment_drift_smoke_matrix.md",
    "docs/runtime/replay_intake_policy.md",
    "docs/runtime/replay_parser_substrate.md",
    "docs/runtime/replay_metadata_extraction.md",
    "docs/runtime/replay_timeline_event_extraction.md",
    "docs/runtime/replay_build_order_economy_extraction.md",
    "docs/runtime/replay_combat_scouting_visibility_extraction.md",
    "docs/runtime/replay_slice_generation.md",
    "docs/runtime/replay_bundle_lineage_contract.md",
    "docs/runtime/canonical_state_schema_v1.md",
    "docs/runtime/canonical_state_pipeline_v1.md",
    "docs/runtime/observation_surface_contract_v1.md",
    "docs/runtime/perceptual_bridge_prototype_v1.md",
    "docs/runtime/observation_reconciliation_audit_v1.md",
    "docs/runtime/benchmark_contract_scorecard_v1.md",
    "docs/runtime/benchmark_integrity_charter_v1.md",
    "docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md",
    "docs/runtime/scripted_baseline_suite_v1.md",
    "docs/runtime/heuristic_baseline_suite_v1.md",
    "docs/runtime/evaluation_runner_tournament_harness_v1.md",
    "docs/runtime/evaluation_diagnostics_failure_views_v1.md",
    "docs/runtime/baseline_evidence_pack_v1.md",
    "docs/runtime/replay_training_dataset_v1.md",
    "docs/runtime/replay_imitation_baseline_v1.md",
    "docs/runtime/learned_agent_evaluation_harness_v1.md",
    "docs/runtime/hierarchical_agent_interface_v1.md",
    "docs/runtime/replay_hierarchical_imitation_agent_v1.md",
    "docs/runtime/replay_explorer_surface_v1.md",
    "docs/runtime/public_flagship_proof_pack_v1.md",
    "docs/runtime/agent_training_program_contract_v1.md",
    "docs/runtime/replay_imitation_training_pipeline_v1.md",
    "docs/runtime/learned_agent_comparison_harness_v1.md",
    "docs/runtime/replay_execution_equivalence_charter_v1.md",
    "docs/runtime/replay_execution_equivalence_evidence_surface_v1.md",
    "docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md",
    "docs/runtime/clone_to_run_smoke_v1.md",
    "docs/runtime/ci_tiering_field_test_readiness_v1.md",
    "docs/diligence/field_test_checklist.md",
    "docs/diligence/field_test_session_template.md",
    "docs/diligence/operating_manual_promotion_readiness.md",
    "docs/audit/broad_exception_boundaries.md",
]

_PLACEHOLDER_READMES = [
    "frontend/README.md",
    "backend/README.md",
    "ops/README.md",
]


@pytest.mark.parametrize("relative", _GOVERNANCE_DOCS)
def test_governance_doc_exists(relative: str) -> None:
    path = REPO_ROOT / relative
    assert path.is_file(), f"missing governance doc: {relative}"


@pytest.mark.parametrize("relative", _PLACEHOLDER_READMES)
def test_placeholder_readme_exists(relative: str) -> None:
    path = REPO_ROOT / relative
    assert path.is_file(), f"missing placeholder: {relative}"
