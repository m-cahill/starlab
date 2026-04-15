"""M54 replay↔execution equivalence audit (consumes M53 evidence; fixture-backed)."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from starlab.equivalence.emit_replay_execution_equivalence_audit import (
    write_replay_execution_equivalence_audit_artifacts,
)
from starlab.equivalence.equivalence_audit import build_replay_execution_equivalence_audit_bundle
from starlab.equivalence.equivalence_evidence import (
    build_identity_binding_evidence,
    build_replay_execution_equivalence_evidence_report,
)
from starlab.equivalence.equivalence_gatepacks import preview_identity_binding_evidence_sha256
from starlab.equivalence.equivalence_models import (
    CHARTER_CONTRACT_ID,
    GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1,
    PROFILE_IDENTITY_BINDING_V1,
    REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION,
    REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX_E2E = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_e2e"
FIX_BAD = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_identity_mismatch"
FIX_ORDER = REPO_ROOT / "tests" / "fixtures" / "m53_identity_binding_parent_order"


def _evidence_e2e() -> dict[str, Any]:
    return build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=FIX_E2E / "replay_binding.json",
        run_identity_path=FIX_E2E / "run_identity.json",
    )


def test_equivalence_audit_is_deterministic(tmp_path: Path) -> None:
    ev = _evidence_e2e()
    a1, r1 = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    a2, r2 = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert sha256_hex_of_canonical_json(a1) == sha256_hex_of_canonical_json(a2)
    assert sha256_hex_of_canonical_json(r1) == sha256_hex_of_canonical_json(r2)
    ev_path = tmp_path / "e.json"
    ev_path.write_text(canonical_json_dumps(ev), encoding="utf-8")
    p1 = write_replay_execution_equivalence_audit_artifacts(
        evidence_path=ev_path,
        evidence_report_path=None,
        output_dir=tmp_path / "a",
    )
    p2 = write_replay_execution_equivalence_audit_artifacts(
        evidence_path=ev_path,
        evidence_report_path=None,
        output_dir=tmp_path / "b",
    )
    assert p1[0].read_text(encoding="utf-8") == p2[0].read_text(encoding="utf-8")
    assert p1[1].read_text(encoding="utf-8") == p2[1].read_text(encoding="utf-8")


def test_identity_binding_gate_accepts_valid_evidence() -> None:
    ev = _evidence_e2e()
    audit, _rep = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert audit["schema_version"] == REPLAY_EXECUTION_EQUIVALENCE_AUDIT_SCHEMA_VERSION
    assert audit["profile_scope_status"] == "accepted_within_profile_scope"
    assert audit["merge_bar_language"] == "would_clear_profile_scope_gate"
    assert audit["gatepack_id"] == GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1
    assert audit["input_evidence_sha256"] == preview_identity_binding_evidence_sha256(ev)
    assert "allowed_absence_policy" in audit and audit["allowed_absence_policy"] is not None


def test_identity_binding_gate_rejects_identity_mismatch() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_BAD / "lineage_seed.json",
        replay_binding_path=FIX_BAD / "replay_binding.json",
        run_identity_path=FIX_BAD / "run_identity.json",
    )
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert audit["profile_scope_status"] == "rejected_within_profile_scope"
    assert audit["merge_bar_language"] == "would_block_profile_scope_gate"


def test_identity_binding_gate_rejects_ordering_mismatch() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_ORDER / "lineage_seed.json",
        replay_binding_path=FIX_ORDER / "replay_binding.json",
        run_identity_path=FIX_ORDER / "run_identity.json",
    )
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert audit["profile_scope_status"] == "rejected_within_profile_scope"


def test_identity_binding_gate_is_not_evaluable_when_evidence_incomplete() -> None:
    """Missing ``evidence_entries`` cannot be audited as a complete M53 document."""

    ev = {
        "schema_version": REPLAY_EXECUTION_EQUIVALENCE_EVIDENCE_SCHEMA_VERSION,
        "charter_contract_id": CHARTER_CONTRACT_ID,
        "profile_id": PROFILE_IDENTITY_BINDING_V1,
        "profile_version": "1",
    }
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert audit["profile_scope_status"] == "not_evaluable"
    assert audit["merge_bar_language"] == "no_profile_scope_decision"


def test_missing_replay_binding_rejects_audit() -> None:
    ev = build_identity_binding_evidence(
        lineage_seed_path=FIX_E2E / "lineage_seed.json",
        replay_binding_path=None,
        run_identity_path=FIX_E2E / "run_identity.json",
    )
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    assert audit["profile_scope_status"] == "rejected_within_profile_scope"
    assert audit["merge_bar_language"] == "would_block_profile_scope_gate"


def test_identity_binding_gate_is_not_evaluable_unknown_profile() -> None:
    ev = _evidence_e2e()
    ev2 = copy.deepcopy(ev)
    ev2["profile_id"] = "starlab.m53.profile.unknown_future_v1"
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev2, evidence_report=None)
    assert audit["profile_scope_status"] == "not_evaluable"
    assert audit["merge_bar_language"] == "no_profile_scope_decision"
    assert audit["gatepack_id"] is None
    assert audit["allowed_absence_policy"] is None


def test_unavailable_by_design_row_does_not_fail_gate() -> None:
    ev = _evidence_e2e()
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    replay_row = next(
        e for e in ev["evidence_entries"] if e["subject"] == "replay.replay_content_sha256"
    )
    assert replay_row["availability_class"] == "unavailable_by_design"
    assert audit["profile_scope_status"] == "accepted_within_profile_scope"


def test_out_of_scope_row_does_not_fail_gate() -> None:
    ev = _evidence_e2e()
    audit, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    excl = next(
        e
        for e in ev["evidence_entries"]
        if e["subject"] == "profile.excluded_gameplay_and_replay_parser_semantics"
    )
    assert excl["availability_class"] == "out_of_scope"
    assert audit["profile_scope_status"] == "accepted_within_profile_scope"


def test_optional_evidence_report_sha256_matches() -> None:
    ev = _evidence_e2e()
    rep = build_replay_execution_equivalence_evidence_report(evidence_obj=ev)
    audit_ok, _ = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=rep)
    gate = next(
        g
        for g in audit_ok["gate_results"]
        if g["gate_id"].endswith("optional_evidence_report_sha256")
    )
    assert gate["status"] == "pass"

    rep_bad = copy.deepcopy(rep)
    rep_bad["evidence_canonical_sha256"] = "0" * 64
    audit_fail, _ = build_replay_execution_equivalence_audit_bundle(
        evidence=ev, evidence_report=rep_bad
    )
    gate_fail = next(
        g
        for g in audit_fail["gate_results"]
        if g["gate_id"].endswith("optional_evidence_report_sha256")
    )
    assert gate_fail["status"] == "fail"
    assert audit_fail["profile_scope_status"] == "rejected_within_profile_scope"


def test_no_universal_equivalence_claim_in_audit_artifacts() -> None:
    ev = _evidence_e2e()
    audit, rep = build_replay_execution_equivalence_audit_bundle(evidence=ev, evidence_report=None)
    blob = json.dumps([audit, rep], sort_keys=True).lower()
    assert "equivalence proved" not in blob
    assert "globally accepted" not in blob
    assert "merge-ready" not in blob


def test_governance_docs_include_m54_runtime_doc() -> None:
    text = (REPO_ROOT / "tests" / "test_governance_docs.py").read_text(encoding="utf-8")
    assert "replay_execution_equivalence_audit_acceptance_gates_v1.md" in text


def test_ledger_current_milestone_is_m54() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "M54" in text and "Replay↔execution equivalence audit" in text


@pytest.mark.smoke
def test_starlab_md_lists_phase_vii_gatepack_table() -> None:
    text = (REPO_ROOT / "docs" / "starlab.md").read_text(encoding="utf-8")
    assert "Phase VII bounded equivalence gatepacks" in text
    assert GATEPACK_IDENTITY_BINDING_ACCEPTANCE_V1 in text
