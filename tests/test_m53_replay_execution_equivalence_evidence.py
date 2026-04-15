"""M53 replay↔execution equivalence evidence (fixture-backed; no live SC2)."""

from __future__ import annotations

from pathlib import Path

import pytest
from starlab.equivalence.emit_replay_execution_equivalence_evidence import (
    write_replay_execution_equivalence_evidence_artifacts,
)
from starlab.equivalence.equivalence_evidence import (
    build_identity_binding_evidence,
    build_replay_execution_equivalence_evidence_report,
    replay_execution_equivalence_evidence_bundle_for_profile,
)
from starlab.equivalence.equivalence_models import (
    CHARTER_CONTRACT_ID,
    PROFILE_IDENTITY_BINDING_V1,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
)
from starlab.equivalence.equivalence_profiles import PROFILE_REGISTRY
from starlab.runs.json_util import sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX_E2E = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_e2e"
FIX_BAD = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_identity_mismatch"
FIX_ORDER = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_parent_order"


def test_equivalence_evidence_is_deterministic(tmp_path: Path) -> None:
    a, _ = replay_execution_equivalence_evidence_bundle_for_profile(
        profile_id=PROFILE_IDENTITY_BINDING_V1,
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    b, _ = replay_execution_equivalence_evidence_bundle_for_profile(
        profile_id=PROFILE_IDENTITY_BINDING_V1,
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    assert sha256_hex_of_canonical_json(a) == sha256_hex_of_canonical_json(b)


def test_emit_writes_deterministic_files(tmp_path: Path) -> None:
    p1 = write_replay_execution_equivalence_evidence_artifacts(
        lineage_seed=FIX_E2E / "lineage_seed.json",
        output_dir=tmp_path / "a",
        profile_id=PROFILE_IDENTITY_BINDING_V1,
        replay_binding=FIX_E2E / "replay_binding.json",
        run_identity=FIX_E2E / "run_identity.json",
    )
    p2 = write_replay_execution_equivalence_evidence_artifacts(
        lineage_seed=FIX_E2E / "lineage_seed.json",
        output_dir=tmp_path / "b",
        profile_id=PROFILE_IDENTITY_BINDING_V1,
        replay_binding=FIX_E2E / "replay_binding.json",
        run_identity=FIX_E2E / "run_identity.json",
    )
    assert p1[0].read_text(encoding="utf-8") == p2[0].read_text(encoding="utf-8")
    assert p1[1].read_text(encoding="utf-8") == p2[1].read_text(encoding="utf-8")


def test_identity_binding_profile_emits_expected_entries() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    assert ev["schema_version"] == REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION
    assert ev["charter_contract_id"] == CHARTER_CONTRACT_ID
    assert ev["profile_id"] == PROFILE_IDENTITY_BINDING_V1
    subjects = [e["subject"] for e in ev["evidence_entries"]]
    assert "join.run_spec_id" in subjects
    assert "replay.replay_content_sha256" in subjects
    assert "profile.excluded_gameplay_and_replay_parser_semantics" in subjects


def test_evidence_has_no_equivalence_passed_boolean() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    dumped = str(ev).lower()
    assert "equivalence_passed" not in dumped
    assert "merge_ready" not in dumped


def test_report_sha256_matches_evidence() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    rep = build_replay_execution_equivalence_evidence_report(evidence_obj=ev)
    assert rep["evidence_canonical_sha256"] == sha256_hex_of_canonical_json(ev)


def test_identity_mismatch_is_reported_explicitly() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_BAD / "lineage_seed.json",
        replay_binding_path=FIX_BAD / "replay_binding.json",
        run_identity_path=FIX_BAD / "run_identity.json",
    )
    mism = ev["mismatch_summary"]
    assert "identity_mismatch" in mism
    join = next(e for e in ev["evidence_entries"] if e["subject"] == "join.lineage_seed_id")
    assert join["mismatch_kind"] == "identity_mismatch"


def test_missing_counterpart_is_not_silent() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=None,
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    assert ev["mismatch_summary"].get("missing_counterpart", 0) >= 1
    kinds = [e.get("mismatch_kind") for e in ev["evidence_entries"]]
    assert "missing_counterpart" in kinds


def test_unavailable_by_design_and_out_of_scope_are_distinct() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    replay = next(
        e for e in ev["evidence_entries"] if e["subject"] == "replay.replay_content_sha256"
    )
    excluded = next(
        e
        for e in ev["evidence_entries"]
        if e["subject"] == "profile.excluded_gameplay_and_replay_parser_semantics"
    )
    assert replay["availability_class"] == "unavailable_by_design"
    assert excluded["availability_class"] == "out_of_scope"


def test_ordering_mismatch_parent_references() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_ORDER / "lineage_seed.json",
        replay_binding_path=FIX_ORDER / "replay_binding.json",
        run_identity_path=FIX_ORDER / "run_identity.json",
    )
    row = next(
        e for e in ev["evidence_entries"] if e["subject"] == "parent_references.sequence_equality"
    )
    assert row["mismatch_kind"] == "ordering_mismatch"


def test_profile_registry_is_stable() -> None:
    assert list(sorted(PROFILE_REGISTRY.keys())) == [PROFILE_IDENTITY_BINDING_V1]


def test_governance_docs_include_m53_runtime_doc() -> None:
    text = (REPO_ROOT / "tests" / "test_governance_docs.py").read_text(encoding="utf-8")
    assert "replay_execution_equivalence_evidence_surface_v1.md" in text


def test_ledger_current_milestone_is_m53() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "M53" in text and "Replay↔execution equivalence evidence surface" in text


@pytest.mark.smoke
def test_starlab_md_lists_phase_vii_profile_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Phase VII bounded equivalence profiles" in text
    assert PROFILE_IDENTITY_BINDING_V1 in text
    assert "starlab.m53.profile.identity_binding_v1" in text
