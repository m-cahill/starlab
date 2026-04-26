"""V15-M11 human panel execution and bounded human-benchmark claim decision tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.v15.checkpoint_evaluation_io import (
    emit_v15_checkpoint_evaluation_fixture,
    emit_v15_checkpoint_promotion_decision,
)
from starlab.v15.human_panel_benchmark_io import emit_v15_human_panel_benchmark
from starlab.v15.human_panel_benchmark_models import (
    CONTRACT_ID_HUMAN_PANEL_BENCHMARK,
    FILENAME_HUMAN_PANEL_BENCHMARK,
    PROFILE_FIXTURE_CI,
)
from starlab.v15.human_panel_execution_io import (
    emit_v15_human_benchmark_claim_decision,
    emit_v15_human_panel_execution_fixture,
    emit_v15_human_panel_execution_operator_declared,
)
from starlab.v15.human_panel_execution_models import (
    ALL_CLAIM_DECISION_LABELS,
    ALL_GATE_STATUSES,
    CLAIM_DECISION_BLOCKED_PROMOTED_CP,
    CLAIM_DECISION_EVALUATED_NOT_AUTH,
    FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    FILENAME_HUMAN_PANEL_EXECUTION,
    HUMAN_PANEL_STATUS_FIXTURE_ONLY,
    REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    REPORT_FILENAME_HUMAN_PANEL_EXECUTION,
    SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION,
    SEAL_KEY_HUMAN_PANEL_EXECUTION,
    default_m11_authorization_flags,
)
from starlab.v15.xai_demonstration_io import emit_v15_replay_native_xai_demonstration_fixture
from starlab.v15.xai_demonstration_models import FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION

REPO_ROOT = Path(__file__).resolve().parents[1]


def _emit_fixture_execution_and_claim(tmp_path: Path) -> Path:
    emit_v15_human_panel_execution_fixture(tmp_path)
    emit_v15_human_benchmark_claim_decision(
        tmp_path, tmp_path / FILENAME_HUMAN_PANEL_EXECUTION, strict=False
    )
    return tmp_path / FILENAME_HUMAN_PANEL_EXECUTION


def test_default_fixture_emits_four_files(tmp_path: Path) -> None:
    _emit_fixture_execution_and_claim(tmp_path)
    for n in (
        FILENAME_HUMAN_PANEL_EXECUTION,
        REPORT_FILENAME_HUMAN_PANEL_EXECUTION,
        FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
        REPORT_FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    ):
        assert (tmp_path / n).is_file()


def test_default_status_honest(tmp_path: Path) -> None:
    _emit_fixture_execution_and_claim(tmp_path)
    d = json.loads((tmp_path / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8"))
    assert d["human_panel_status"] == HUMAN_PANEL_STATUS_FIXTURE_ONLY
    af = d["authorization_flags"]
    for k, v in default_m11_authorization_flags().items():
        assert af[k] is v
    c = json.loads((tmp_path / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION).read_text(encoding="utf-8"))
    assert c["claim_decision_label"] == CLAIM_DECISION_EVALUATED_NOT_AUTH
    caf = c["authorization_flags"]
    assert caf["human_benchmark_claim_authorized"] is False
    assert caf["v2_authorized"] is False
    assert caf.get("ladder_claim_authorized") is False
    assert caf.get("strong_agent_claim_authorized") is False


def test_gate_coverage_deterministic(tmp_path: Path) -> None:
    _emit_fixture_execution_and_claim(tmp_path)
    d = json.loads((tmp_path / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8"))
    gates = d["human_panel_gates"]
    ids = [g["gate_id"] for g in gates]
    assert len(ids) == 13
    for g in gates:
        assert g["status"] in ALL_GATE_STATUSES
    h2 = next(x for x in gates if x["gate_id"] == "H2_checkpoint_promotion_binding")
    assert h2["status"] == "blocked"
    assert "promoted" in h2["notes"].lower() or "blocked" in h2["notes"].lower()


def test_m06_protocol_binding_and_wrong_contract_fails(
    tmp_path: Path,
) -> None:
    m06d = tmp_path / "m06"
    emit_v15_human_panel_benchmark(m06d, profile=PROFILE_FIXTURE_CI)
    m06_json = m06d / FILENAME_HUMAN_PANEL_BENCHMARK
    emit_v15_checkpoint_evaluation_fixture(tmp_path / "ev")
    emit_v15_checkpoint_promotion_decision(
        tmp_path / "pr", tmp_path / "ev" / "v15_checkpoint_evaluation.json"
    )
    promo = tmp_path / "pr" / "v15_checkpoint_promotion_decision.json"
    m10d = tmp_path / "m10d"
    emit_v15_replay_native_xai_demonstration_fixture(m10d)
    m10_json = m10d / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    panel = tmp_path / "panel.json"
    panel.write_text(
        json.dumps(
            {
                "participant_count": 0,
                "match_count": 0,
                "threshold_frozen": False,
                "threshold_policy_id": "no_claim_without_threshold_freeze",
            }
        ),
        encoding="utf-8",
    )
    m11out = tmp_path / "m11"
    emit_v15_human_panel_execution_operator_declared(m11out, m06_json, promo, m10_json, panel)
    d = json.loads((m11out / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8"))
    b = d["m06_human_panel_benchmark_binding"]
    assert b["contract_id"] == CONTRACT_ID_HUMAN_PANEL_BENCHMARK
    sha_exp = sha256_hex_of_canonical_json(json.loads(m06_json.read_text(encoding="utf-8")))
    assert b["human_panel_benchmark_json_canonical_sha256"] == sha_exp
    b9 = d["m09_promotion_decision_binding"]
    assert len(str(b9["promotion_decision_json_canonical_sha256"])) == 64
    b10 = d["m10_replay_native_xai_demonstration_binding"]
    assert len(str(b10["replay_native_xai_demonstration_json_canonical_sha256"])) == 64
    bad = tmp_path / "bad_m06.json"
    bad.write_text(json.dumps({"contract_id": "wrong"}), encoding="utf-8")
    with pytest.raises(ValueError, match="M06"):
        emit_v15_human_panel_execution_operator_declared(
            tmp_path / "e2", bad, promo, m10_json, panel
        )


def test_operator_evidence_redaction(tmp_path: Path) -> None:
    m06d = tmp_path / "m06"
    emit_v15_human_panel_benchmark(m06d, profile=PROFILE_FIXTURE_CI)
    m06_json = m06d / FILENAME_HUMAN_PANEL_BENCHMARK
    emit_v15_checkpoint_evaluation_fixture(tmp_path / "ev")
    emit_v15_checkpoint_promotion_decision(
        tmp_path / "pr", tmp_path / "ev" / "v15_checkpoint_evaluation.json"
    )
    promo = tmp_path / "pr" / "v15_checkpoint_promotion_decision.json"
    m10d = tmp_path / "m10d"
    emit_v15_replay_native_xai_demonstration_fixture(m10d)
    m10_json = m10d / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    panel = tmp_path / "panel.json"
    panel.write_text(
        json.dumps(
            {
                "operator_notes": "Email: leak@example.com and C:\\\\Secret\\\\replay.SC2Replay",
                "participant_count": 0,
            }
        ),
        encoding="utf-8",
    )
    m11out = tmp_path / "m11"
    emit_v15_human_panel_execution_operator_declared(m11out, m06_json, promo, m10_json, panel)
    raw = (m11out / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8")
    assert "leak@example.com" not in raw
    assert "C:\\\\Secret" not in raw


def test_claim_label_blocked_when_m09_not_promoted(tmp_path: Path) -> None:
    m06d = tmp_path / "m06"
    emit_v15_human_panel_benchmark(m06d, profile=PROFILE_FIXTURE_CI)
    m06_json = m06d / FILENAME_HUMAN_PANEL_BENCHMARK
    emit_v15_checkpoint_evaluation_fixture(tmp_path / "ev")
    emit_v15_checkpoint_promotion_decision(
        tmp_path / "pr", tmp_path / "ev" / "v15_checkpoint_evaluation.json"
    )
    promo = tmp_path / "pr" / "v15_checkpoint_promotion_decision.json"
    m10d = tmp_path / "m10d"
    emit_v15_replay_native_xai_demonstration_fixture(m10d)
    m10_json = m10d / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION
    panel = tmp_path / "panel.json"
    panel.write_text(json.dumps({"participant_count": 0, "match_count": 0}), encoding="utf-8")
    m11out = tmp_path / "m11"
    emit_v15_human_panel_execution_operator_declared(m11out, m06_json, promo, m10_json, panel)
    emit_v15_human_benchmark_claim_decision(
        m11out, m11out / FILENAME_HUMAN_PANEL_EXECUTION, strict=False
    )
    c = json.loads((m11out / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION).read_text(encoding="utf-8"))
    assert c["claim_decision_label"] == CLAIM_DECISION_BLOCKED_PROMOTED_CP


def test_strict_fails_on_fixture(tmp_path: Path) -> None:
    _emit_fixture_execution_and_claim(tmp_path)
    with pytest.raises(ValueError, match="strict"):
        emit_v15_human_benchmark_claim_decision(
            tmp_path, tmp_path / FILENAME_HUMAN_PANEL_EXECUTION, strict=True
        )


def test_canonical_determinism(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    _emit_fixture_execution_and_claim(a)
    _emit_fixture_execution_and_claim(b)
    e1 = (a / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8")
    e2 = (b / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8")
    assert e1 == e2
    c1 = (a / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION).read_text(encoding="utf-8")
    c2 = (b / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION).read_text(encoding="utf-8")
    assert c1 == c2


def test_all_claim_labels_vocab() -> None:
    assert "authorized_bounded_human_benchmark_claim" in " ".join(ALL_CLAIM_DECISION_LABELS)
    assert "evaluated_not_authorized" in " ".join(ALL_CLAIM_DECISION_LABELS)


def test_seal_valid_fixture(tmp_path: Path) -> None:
    _emit_fixture_execution_and_claim(tmp_path)
    d = json.loads((tmp_path / FILENAME_HUMAN_PANEL_EXECUTION).read_text(encoding="utf-8"))
    ex = {k: v for k, v in d.items() if k != SEAL_KEY_HUMAN_PANEL_EXECUTION}
    assert d[SEAL_KEY_HUMAN_PANEL_EXECUTION] == sha256_hex_of_canonical_json(ex)
    c = json.loads((tmp_path / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION).read_text(encoding="utf-8"))
    c0 = {k: v for k, v in c.items() if k != SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION}
    assert c[SEAL_KEY_HUMAN_BENCHMARK_CLAIM_DECISION] == sha256_hex_of_canonical_json(c0)


def test_emit_clis_return_zero(tmp_path: Path) -> None:
    o1 = tmp_path / "o1"
    o1.mkdir()
    p1 = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_human_panel_execution",
            "--output-dir",
            str(o1),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert p1.returncode == 0, p1.stderr
    p2 = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_human_benchmark_claim_decision",
            "--human-panel-execution-json",
            str(o1 / FILENAME_HUMAN_PANEL_EXECUTION),
            "--output-dir",
            str(o1),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert p2.returncode == 0, p2.stderr
