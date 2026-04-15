"""Governance tests: expected modules and fixtures exist."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_starlab_runs_package_exists() -> None:
    runs_init = REPO_ROOT / "starlab" / "runs" / "__init__.py"
    assert runs_init.is_file()
    seed = REPO_ROOT / "starlab" / "runs" / "seed_from_proof.py"
    assert seed.is_file()


def test_m03_fixture_pair_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "m02_match_config.json").is_file()
    assert (fx / "m02_match_execution_proof.json").is_file()


def test_replay_binding_module_exists() -> None:
    rb = REPO_ROOT / "starlab" / "runs" / "replay_binding.py"
    assert rb.is_file()
    cli = REPO_ROOT / "starlab" / "runs" / "bind_replay.py"
    assert cli.is_file()


def test_canonical_run_artifact_modules_exist() -> None:
    cr = REPO_ROOT / "starlab" / "runs" / "canonical_run_artifact.py"
    assert cr.is_file()
    cli = REPO_ROOT / "starlab" / "runs" / "build_canonical_run_artifact.py"
    assert cli.is_file()


def test_m06_environment_drift_modules_exist() -> None:
    assert (REPO_ROOT / "starlab" / "sc2" / "environment_drift.py").is_file()
    assert (REPO_ROOT / "starlab" / "sc2" / "evaluate_environment_drift.py").is_file()
    assert (REPO_ROOT / "starlab" / "sc2" / "runtime_smoke_matrix.py").is_file()


def test_m07_replay_intake_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    assert (rp / "intake_models.py").is_file()
    assert (rp / "intake_policy.py").is_file()
    assert (rp / "intake_io.py").is_file()
    assert (rp / "intake_cli.py").is_file()


def test_m05_expected_golden_fixtures_exist() -> None:
    exp = REPO_ROOT / "tests" / "fixtures" / "m05_expected"
    assert (exp / "manifest.json").is_file()
    assert (exp / "hashes.json").is_file()


def test_m06_probe_fixtures_exist() -> None:
    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "probe_m06_valid.json").is_file()
    assert (fx / "probe_m06_warn.json").is_file()
    assert (fx / "probe_m06_fail_invalid_surface.json").is_file()
    assert (fx / "run_identity_m06_fingerprint.json").is_file()


def test_opaque_replay_fixtures_exist() -> None:
    """Governed opaque replay bytes used by M04/M05/M07/M08 tests (not Blizzard MPQ files)."""

    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "replay_m07_generated.SC2Replay").is_file()
    assert (fx / "replay_m07_sample.SC2Replay").is_file()


def test_m08_replay_parser_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "parse_replay.py",
        "parser_io.py",
        "parser_interfaces.py",
        "parser_models.py",
        "parser_normalization.py",
        "s2protocol_adapter.py",
    ):
        assert (rp / name).is_file()


def test_m15_canonical_state_modules_exist() -> None:
    st = REPO_ROOT / "starlab" / "state"
    for name in (
        "canonical_state_models.py",
        "canonical_state_catalog.py",
        "canonical_state_schema.py",
        "canonical_state_io.py",
        "emit_canonical_state_schema.py",
    ):
        assert (st / name).is_file()


def test_m15_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m15"
    assert fx.is_dir()
    assert (fx / "valid_canonical_state_example.json").is_file()
    assert (fx / "invalid_canonical_state_example_missing_required.json").is_file()
    assert (fx / "expected_canonical_state_schema.json").is_file()
    assert (fx / "expected_canonical_state_schema_report.json").is_file()


def test_m16_canonical_state_pipeline_modules_exist() -> None:
    st = REPO_ROOT / "starlab" / "state"
    for name in (
        "canonical_state_inputs.py",
        "canonical_state_derivation.py",
        "canonical_state_pipeline.py",
        "emit_canonical_state.py",
    ):
        assert (st / name).is_file()


def test_m16_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m16"
    assert fx.is_dir()
    assert (fx / "expected_canonical_state.json").is_file()
    assert (fx / "expected_canonical_state_report.json").is_file()
    b = fx / "bundle"
    assert (b / "replay_bundle_manifest.json").is_file()
    assert (b / "replay_metadata.json").is_file()


def test_m17_observation_surface_modules_exist() -> None:
    obs = REPO_ROOT / "starlab" / "observation"
    for name in (
        "observation_surface_models.py",
        "observation_surface_catalog.py",
        "observation_surface_schema.py",
        "observation_surface_io.py",
        "emit_observation_surface_schema.py",
    ):
        assert (obs / name).is_file()


def test_m17_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m17"
    assert fx.is_dir()
    assert (fx / "observation_surface_valid_example.json").is_file()
    assert (fx / "observation_surface_invalid_example_bad_schema_version.json").is_file()
    assert (fx / "expected_observation_surface_schema.json").is_file()
    assert (fx / "expected_observation_surface_schema_report.json").is_file()


def test_m18_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m18"
    assert fx.is_dir()
    assert (fx / "canonical_state.json").is_file()
    assert (fx / "canonical_state_report.json").is_file()
    assert (fx / "expected_observation_surface.json").is_file()
    assert (fx / "expected_observation_surface_report.json").is_file()


def test_m18_perceptual_bridge_modules_exist() -> None:
    obs = REPO_ROOT / "starlab" / "observation"
    for name in (
        "observation_surface_inputs.py",
        "observation_surface_derivation.py",
        "observation_surface_pipeline.py",
        "emit_observation_surface.py",
    ):
        assert (obs / name).is_file()


def test_m19_reconciliation_modules_exist() -> None:
    obs = REPO_ROOT / "starlab" / "observation"
    for name in (
        "observation_reconciliation_inputs.py",
        "observation_reconciliation_rules.py",
        "observation_reconciliation_pipeline.py",
        "audit_observation_surface.py",
    ):
        assert (obs / name).is_file()


def test_m19_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m19"
    assert fx.is_dir()
    assert (fx / "canonical_state.json").is_file()
    assert (fx / "observation_surface.json").is_file()
    assert (fx / "expected_observation_reconciliation_audit.json").is_file()
    assert (fx / "expected_observation_reconciliation_audit_report.json").is_file()


def test_m20_benchmark_modules_exist() -> None:
    bp = REPO_ROOT / "starlab" / "benchmarks"
    for name in (
        "benchmark_contract_models.py",
        "benchmark_contract_schema.py",
        "benchmark_scorecard_schema.py",
        "emit_benchmark_contracts.py",
    ):
        assert (bp / name).is_file()


def test_m20_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m20"
    assert fx.is_dir()
    assert (fx / "valid_benchmark_contract.json").is_file()
    assert (fx / "valid_benchmark_scorecard.json").is_file()
    assert (fx / "expected_benchmark_contract_schema.json").is_file()


def test_m21_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m21"
    assert fx.is_dir()
    assert (fx / "valid_benchmark_contract.json").is_file()
    assert (fx / "invalid_benchmark_contract.json").is_file()
    assert (fx / "expected_scripted_baseline_suite.json").is_file()
    assert (fx / "expected_scripted_baseline_suite_report.json").is_file()


def test_m21_baseline_modules_exist() -> None:
    bl = REPO_ROOT / "starlab" / "baselines"
    for name in (
        "scripted_baseline_models.py",
        "scripted_baseline_suite.py",
        "scripted_baseline_scorecards.py",
        "emit_scripted_baseline_suite.py",
    ):
        assert (bl / name).is_file()


def test_m22_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m22"
    assert fx.is_dir()
    assert (fx / "expected_heuristic_baseline_suite.json").is_file()
    assert (fx / "expected_heuristic_baseline_suite_report.json").is_file()


def test_m22_heuristic_baseline_modules_exist() -> None:
    bl = REPO_ROOT / "starlab" / "baselines"
    for name in (
        "heuristic_baseline_models.py",
        "heuristic_baseline_suite.py",
        "heuristic_baseline_scorecards.py",
        "emit_heuristic_baseline_suite.py",
    ):
        assert (bl / name).is_file()


def test_m23_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m23"
    assert fx.is_dir()
    assert (fx / "expected_evaluation_tournament.json").is_file()
    assert (fx / "expected_evaluation_tournament_report.json").is_file()


def test_m23_evaluation_modules_exist() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    for name in (
        "evaluation_runner_models.py",
        "evaluation_runner.py",
        "tournament_harness.py",
        "emit_evaluation_tournament.py",
    ):
        assert (ev / name).is_file()


def test_m24_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m24"
    assert fx.is_dir()
    assert (fx / "expected_evaluation_diagnostics.json").is_file()
    assert (fx / "expected_evaluation_diagnostics_report.json").is_file()
    assert (fx / "synthetic_tournament_draw.json").is_file()


def test_m24_evaluation_modules_exist() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    for name in (
        "diagnostics_models.py",
        "diagnostics_views.py",
        "emit_evaluation_diagnostics.py",
    ):
        assert (ev / name).is_file()


def test_m25_evidence_pack_modules_exist() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    for name in (
        "evidence_pack_models.py",
        "evidence_pack_views.py",
        "emit_baseline_evidence_pack.py",
    ):
        assert (ev / name).is_file()


def test_m26_imitation_modules_exist() -> None:
    im = REPO_ROOT / "starlab" / "imitation"
    for name in (
        "dataset_models.py",
        "dataset_views.py",
        "emit_replay_training_dataset.py",
    ):
        assert (im / name).is_file()


def test_m27_imitation_modules_exist() -> None:
    im = REPO_ROOT / "starlab" / "imitation"
    for name in (
        "baseline_models.py",
        "baseline_features.py",
        "baseline_fit.py",
        "emit_replay_imitation_baseline.py",
        "replay_observation_materialization.py",
        "replay_imitation_predictor.py",
    ):
        assert (im / name).is_file()


def test_m26_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m26"
    assert fx.is_dir()


def test_m27_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m27"
    assert fx.is_dir()
    assert (fx / "replay_imitation_baseline.json").is_file()
    assert (fx / "replay_imitation_baseline_report.json").is_file()


def test_m28_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m28"
    assert fx.is_dir()
    assert (fx / "benchmark_contract_m28.json").is_file()
    assert (fx / "learned_agent_evaluation.json").is_file()
    assert (fx / "learned_agent_evaluation_report.json").is_file()


def test_m28_evaluation_modules_exist() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    for name in (
        "learned_agent_evaluation.py",
        "learned_agent_metrics.py",
        "emit_learned_agent_evaluation.py",
        "learned_agent_models.py",
    ):
        assert (ev / name).is_file()


def test_m42_comparison_modules_exist() -> None:
    ev = REPO_ROOT / "starlab" / "evaluation"
    for name in (
        "learned_agent_comparison_harness.py",
        "learned_agent_comparison_io.py",
        "learned_agent_comparison_models.py",
        "emit_learned_agent_comparison.py",
    ):
        assert (ev / name).is_file()
    assert (REPO_ROOT / "starlab" / "imitation" / "trained_run_predictor.py").is_file()


def test_m49_full_local_training_campaign_modules_exist() -> None:
    tr = REPO_ROOT / "starlab" / "training"
    for name in (
        "full_local_training_campaign_models.py",
        "full_local_training_campaign_io.py",
        "full_local_training_campaign_preflight.py",
        "emit_full_local_training_campaign_contract.py",
        "emit_full_local_training_campaign_preflight.py",
    ):
        assert (tr / name).is_file()


def test_m50_campaign_execution_modules_exist() -> None:
    tr = REPO_ROOT / "starlab" / "training"
    for name in (
        "industrial_hidden_rollout_models.py",
        "campaign_execution_lock.py",
        "campaign_execution_io.py",
        "campaign_execution_preflight.py",
        "execute_full_local_training_campaign.py",
    ):
        assert (tr / name).is_file()


def test_m51_campaign_phase_receipt_module_exists() -> None:
    tr = REPO_ROOT / "starlab" / "training"
    assert (tr / "campaign_phase_receipt.py").is_file()


def test_m52_equivalence_charter_modules_exist() -> None:
    eq = REPO_ROOT / "starlab" / "equivalence"
    for name in (
        "equivalence_models.py",
        "equivalence_charter.py",
        "emit_replay_execution_equivalence_charter.py",
        "equivalence_gatepacks.py",
        "equivalence_audit.py",
        "emit_replay_execution_equivalence_audit.py",
    ):
        assert (eq / name).is_file()


def test_m29_hierarchy_modules_exist() -> None:
    hi = REPO_ROOT / "starlab" / "hierarchy"
    for name in (
        "hierarchical_interface_models.py",
        "hierarchical_interface_schema.py",
        "hierarchical_interface_io.py",
        "emit_hierarchical_agent_interface.py",
    ):
        assert (hi / name).is_file()


def test_m29_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m29"
    assert fx.is_dir()
    assert (fx / "expected_hierarchical_agent_interface_schema.json").is_file()
    assert (fx / "expected_hierarchical_agent_interface_schema_report.json").is_file()
    assert (fx / "valid_hierarchical_trace.json").is_file()


def test_m30_hierarchy_modules_exist() -> None:
    hi = REPO_ROOT / "starlab" / "hierarchy"
    for name in (
        "delegate_policy.py",
        "hierarchical_agent_models.py",
        "hierarchical_agent_fit.py",
        "hierarchical_agent_predictor.py",
        "emit_replay_hierarchical_imitation_agent.py",
    ):
        assert (hi / name).is_file()


def test_m30_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m30"
    assert fx.is_dir()
    assert (fx / "replay_hierarchical_imitation_agent.json").is_file()
    assert (fx / "replay_hierarchical_imitation_agent_report.json").is_file()


def test_m31_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m31"
    assert fx.is_dir()
    assert (fx / "expected_replay_explorer_surface.json").is_file()
    assert (fx / "expected_replay_explorer_surface_report.json").is_file()
    assert (fx / "bundle" / "replay_bundle_manifest.json").is_file()


def test_m31_explorer_modules_exist() -> None:
    ex = REPO_ROOT / "starlab" / "explorer"
    for name in (
        "replay_explorer_models.py",
        "replay_explorer_selection.py",
        "replay_explorer_builder.py",
        "replay_explorer_io.py",
        "emit_replay_explorer_surface.py",
    ):
        assert (ex / name).is_file()


def test_m09_metadata_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "metadata_models.py",
        "metadata_extraction.py",
        "metadata_io.py",
        "extract_replay_metadata.py",
    ):
        assert (rp / name).is_file()


def test_m10_timeline_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "timeline_models.py",
        "timeline_extraction.py",
        "timeline_io.py",
        "extract_replay_timeline.py",
    ):
        assert (rp / name).is_file()


def test_m10_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m10"
    assert fx.is_dir()
    assert (fx / "replay_raw_parse_timeline_happy.json").is_file()


def test_m11_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m11"
    assert fx.is_dir()
    assert (fx / "replay_raw_parse_m11_happy.json").is_file()
    assert (fx / "expected_replay_build_order_economy.json").is_file()


def test_m11_build_order_economy_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "build_order_economy_models.py",
        "build_order_economy_catalog.py",
        "build_order_economy_extraction.py",
        "build_order_economy_io.py",
        "extract_replay_build_order_economy.py",
    ):
        assert (rp / name).is_file()


def test_m12_combat_scouting_visibility_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "combat_scouting_visibility_models.py",
        "combat_scouting_visibility_catalog.py",
        "combat_scouting_visibility_extraction.py",
        "combat_scouting_visibility_io.py",
        "extract_replay_combat_scouting_visibility.py",
    ):
        assert (rp / name).is_file()


def test_m13_replay_slice_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "replay_slice_models.py",
        "replay_slice_catalog.py",
        "replay_slice_generation.py",
        "replay_slice_io.py",
        "extract_replay_slices.py",
    ):
        assert (rp / name).is_file()


def test_m14_replay_bundle_modules_exist() -> None:
    rp = REPO_ROOT / "starlab" / "replays"
    for name in (
        "replay_bundle_models.py",
        "replay_bundle_catalog.py",
        "replay_bundle_generation.py",
        "replay_bundle_io.py",
        "extract_replay_bundle.py",
    ):
        assert (rp / name).is_file()


def test_m12_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m12"
    assert fx.is_dir()
    assert (fx / "replay_raw_parse_m12_combined.json").is_file()
    assert (fx / "expected_replay_combat_scouting_visibility_combined.json").is_file()


def test_m13_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m13"
    assert fx.is_dir()
    assert (fx / "replay_timeline.json").is_file()
    assert (fx / "replay_build_order_economy.json").is_file()
    assert (fx / "replay_combat_scouting_visibility.json").is_file()
    assert (fx / "expected_replay_slices.json").is_file()
    assert (fx / "expected_replay_slices_report.json").is_file()


def test_m14_fixture_dir_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m14"
    assert fx.is_dir()
    assert (fx / "replay_metadata.json").is_file()
    assert (fx / "replay_timeline.json").is_file()
    assert (fx / "replay_build_order_economy.json").is_file()
    assert (fx / "replay_combat_scouting_visibility.json").is_file()
    assert (fx / "replay_slices.json").is_file()
    assert (fx / "expected_replay_bundle_manifest.json").is_file()
    assert (fx / "expected_replay_bundle_lineage.json").is_file()
    assert (fx / "expected_replay_bundle_contents.json").is_file()


def test_m09_fixture_raw_parse_fixtures_exist() -> None:
    fx = REPO_ROOT / "tests" / "fixtures" / "m09"
    assert (fx / "replay_raw_parse_valid.json").is_file()
    assert (fx / "replay_raw_parse_partial.json").is_file()
    assert (fx / "replay_parse_receipt_valid.json").is_file()
    assert (fx / "replay_parse_report_valid.json").is_file()
