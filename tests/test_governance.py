"""M00 governance smoke tests: repo wiring only; no runtime or SC2 claims."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_GOVERNANCE_DOCS = [
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


def test_starlab_ledger_exists() -> None:
    ledger = REPO_ROOT / "docs" / "starlab.md"
    assert ledger.is_file()


def test_ledger_names_deployment_targets() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Netlify" in text
    assert "Render" in text


def test_milestone_m00_directory_exists() -> None:
    m00 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M00"
    assert m00.is_dir()


def test_rights_register_exists() -> None:
    path = REPO_ROOT / "docs" / "rights_register.md"
    assert path.is_file()


def test_ci_workflow_exists() -> None:
    wf = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file()


def test_pyproject_exists() -> None:
    assert (REPO_ROOT / "pyproject.toml").is_file()


def test_ledger_has_m01_runtime_title_and_m32_map() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "SC2 Runtime Surface Decision & Environment Lock" in text
    assert "M32" in text
    assert "Platform Boundary Review & Multi-Environment Charter" in text
    assert "Governance, Runtime Surface, and Deterministic Run Substrate" in text


def test_ledger_canonical_corpus_promotion_rule() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Canonical corpus promotion" in text
    assert "canonical STARLAB corpus" in text


def test_od005_resolved_row() -> None:
    lines = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| OD-005"):
            assert "Resolved" in stripped
            assert "s2client-proto" in stripped or "s2client" in stripped.lower()
            return
    raise AssertionError("OD-005 row not found in ledger")


def test_current_milestone_is_m18() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    section = text.split("## 11. Current milestone")[1].split("## 12")[0]
    assert "M18" in section
    assert "Perceptual" in section or "perceptual" in section.lower()


def test_m17_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M17 |") and "Observation" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M17 milestone row not found or not complete")


def test_m12_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M12 |") and "Combat" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M12 milestone row not found or not complete")


def test_m13_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M13 |") and "Replay Slice" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M13 milestone row not found or not complete")


def _milestone_table_section() -> str:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    return text.split("## 7. Milestone table")[1].split("## 8")[0]


def test_m01_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M01 |") and "SC2 Runtime Surface Decision" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M01 milestone row not found")


def test_m02_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M02 |") and "Deterministic Match Execution Harness" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M02 milestone row not found")


def test_m03_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M03 |") and "Lineage Seed" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M03 milestone row not found")


def test_m04_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M04 |") and "Replay Binding" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M04 milestone row not found")


def test_m05_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M05 |") and "Canonical Run Artifact" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M05 milestone row not found")


def test_m06_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M06 |") and "Environment Drift" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M06 milestone row not found")


def test_m08_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M08 |") and "Replay Parser Substrate" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M08 milestone row not found")


def test_m09_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M09 |") and "Replay Metadata Extraction" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M09 milestone row not found")


def test_m03_stub_milestone_files_exist() -> None:
    m03 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M03"
    assert (m03 / "M03_plan.md").is_file()
    assert (m03 / "M03_toolcalls.md").is_file()


def test_m04_milestone_files_exist() -> None:
    m04 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M04"
    assert (m04 / "M04_plan.md").is_file()
    assert (m04 / "M04_toolcalls.md").is_file()


def test_m05_stub_milestone_files_exist() -> None:
    m05 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M05"
    assert (m05 / "M05_plan.md").is_file()
    assert (m05 / "M05_toolcalls.md").is_file()


def test_m06_stub_milestone_files_exist() -> None:
    m06 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M06"
    assert (m06 / "M06_plan.md").is_file()
    assert (m06 / "M06_toolcalls.md").is_file()


def test_m07_milestone_files_exist() -> None:
    m07 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M07"
    assert (m07 / "M07_plan.md").is_file()
    assert (m07 / "M07_toolcalls.md").is_file()
    assert (m07 / "M07_run1.md").is_file()
    assert (m07 / "M07_summary.md").is_file()
    assert (m07 / "M07_audit.md").is_file()


def test_starlab_runs_package_exists() -> None:
    runs_init = REPO_ROOT / "starlab" / "runs" / "__init__.py"
    assert runs_init.is_file()
    seed = REPO_ROOT / "starlab" / "runs" / "seed_from_proof.py"
    assert seed.is_file()


def test_m03_fixture_pair_exists() -> None:
    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "m02_match_config.json").is_file()
    assert (fx / "m02_match_execution_proof.json").is_file()


def test_m01_changelog_entry_present() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "### 2026-04-06 — M01 closeout" in text
    assert "OD-005" in text


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


def test_m07_opaque_replay_fixtures_exist() -> None:
    fx = REPO_ROOT / "tests" / "fixtures"
    assert (fx / "replay_m07_sample.SC2Replay").is_file()
    assert (fx / "replay_m07_generated.SC2Replay").is_file()


def test_m08_milestone_files_exist() -> None:
    m08 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M08"
    assert (m08 / "M08_plan.md").is_file()
    assert (m08 / "M08_toolcalls.md").is_file()
    assert (m08 / "M08_run1.md").is_file()
    assert (m08 / "M08_summary.md").is_file()
    assert (m08 / "M08_audit.md").is_file()


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


def test_m09_milestone_files_exist() -> None:
    m09 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M09"
    assert (m09 / "M09_plan.md").is_file()
    assert (m09 / "M09_toolcalls.md").is_file()
    assert (m09 / "M09_run1.md").is_file()
    assert (m09 / "M09_summary.md").is_file()
    assert (m09 / "M09_audit.md").is_file()


def test_m10_milestone_files_exist() -> None:
    m10 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M10"
    assert (m10 / "M10_plan.md").is_file()
    assert (m10 / "M10_toolcalls.md").is_file()
    assert (m10 / "M10_run1.md").is_file()
    assert (m10 / "M10_summary.md").is_file()
    assert (m10 / "M10_audit.md").is_file()


def test_m11_milestone_files_exist() -> None:
    m11 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M11"
    assert (m11 / "M11_plan.md").is_file()
    assert (m11 / "M11_toolcalls.md").is_file()
    assert (m11 / "M11_run1.md").is_file()
    assert (m11 / "M11_summary.md").is_file()
    assert (m11 / "M11_audit.md").is_file()


def test_m12_milestone_files_exist() -> None:
    m12 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M12"
    assert (m12 / "M12_plan.md").is_file()
    assert (m12 / "M12_toolcalls.md").is_file()
    assert (m12 / "M12_run1.md").is_file()
    assert (m12 / "M12_summary.md").is_file()
    assert (m12 / "M12_audit.md").is_file()


def test_m13_milestone_files_exist() -> None:
    m13 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M13"
    assert (m13 / "M13_plan.md").is_file()
    assert (m13 / "M13_toolcalls.md").is_file()
    assert (m13 / "M13_run1.md").is_file()
    assert (m13 / "M13_summary.md").is_file()
    assert (m13 / "M13_audit.md").is_file()


def test_m14_milestone_files_exist() -> None:
    m14 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M14"
    assert (m14 / "M14_plan.md").is_file()
    assert (m14 / "M14_toolcalls.md").is_file()
    assert (m14 / "M14_run1.md").is_file()
    assert (m14 / "M14_summary.md").is_file()
    assert (m14 / "M14_audit.md").is_file()


def test_m14_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M14 |") and "Replay Bundle" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M14 milestone row not found or not complete")


def test_m15_milestone_files_exist() -> None:
    m15 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M15"
    assert (m15 / "M15_plan.md").is_file()
    assert (m15 / "M15_toolcalls.md").is_file()
    assert (m15 / "M15_run1.md").is_file()
    assert (m15 / "M15_summary.md").is_file()
    assert (m15 / "M15_audit.md").is_file()


def test_m15_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M15 |") and "Canonical State" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M15 milestone row not found or not complete")


def test_m16_milestone_files_exist() -> None:
    m16 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M16"
    assert (m16 / "M16_plan.md").is_file()
    assert (m16 / "M16_toolcalls.md").is_file()
    assert (m16 / "M16_run1.md").is_file()
    assert (m16 / "M16_summary.md").is_file()
    assert (m16 / "M16_audit.md").is_file()


def test_m17_milestone_files_exist() -> None:
    m17 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M17"
    assert (m17 / "M17_plan.md").is_file()
    assert (m17 / "M17_toolcalls.md").is_file()
    assert (m17 / "M17_run1.md").is_file()
    assert (m17 / "M17_summary.md").is_file()
    assert (m17 / "M17_audit.md").is_file()


def test_m18_stub_milestone_files_exist() -> None:
    m18 = REPO_ROOT / "docs" / "company_secrets" / "milestones" / "M18"
    assert (m18 / "M18_plan.md").is_file()
    assert (m18 / "M18_toolcalls.md").is_file()


def test_m16_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M16 |") and "Structured State" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M16 milestone row not found or not complete")


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


def test_m10_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M10 |") and "Timeline" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M10 milestone row not found or not complete")


def test_m11_complete_in_milestone_table() -> None:
    for line in _milestone_table_section().splitlines():
        stripped = line.strip()
        if stripped.startswith("| M11 |") and "Build-Order" in stripped:
            assert "Complete" in stripped
            return
    raise AssertionError("M11 milestone row not found or not complete")


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
