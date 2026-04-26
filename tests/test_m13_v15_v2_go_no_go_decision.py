"""V15-M13 v2 go / no-go decision tests."""

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
from starlab.v15.checkpoint_lineage_io import emit_checkpoint_lineage_manifest
from starlab.v15.checkpoint_lineage_models import FILENAME_CHECKPOINT_LINEAGE
from starlab.v15.checkpoint_lineage_models import PROFILE_FIXTURE_CI as CL_PROFILE
from starlab.v15.human_panel_execution_io import (
    emit_v15_human_benchmark_claim_decision,
    emit_v15_human_panel_execution_fixture,
)
from starlab.v15.human_panel_execution_models import (
    FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    FILENAME_HUMAN_PANEL_EXECUTION,
)
from starlab.v15.long_gpu_training_manifest_io import emit_v15_long_gpu_training_manifest_fixture
from starlab.v15.long_gpu_training_manifest_models import FILENAME_CAMPAIGN_RECEIPT
from starlab.v15.showcase_release_io import emit_v15_showcase_agent_release_pack_operator_preflight
from starlab.v15.showcase_release_models import FILENAME_SHOWCASE_RELEASE_PACK
from starlab.v15.strong_agent_scorecard_io import emit_v15_strong_agent_scorecard
from starlab.v15.strong_agent_scorecard_models import FILENAME_STRONG_AGENT_SCORECARD
from starlab.v15.strong_agent_scorecard_models import PROFILE_FIXTURE_CI as M05_PROFILE
from starlab.v15.v2_decision_io import (
    FORBIDDEN_BRIEF_SUBSTRINGS,
    build_v2_decision_body_operator_declared,
    emit_v15_v2_go_no_go_decision_fixture,
    emit_v15_v2_go_no_go_decision_operator_preflight,
    verify_upstream_cross_checks,
)
from starlab.v15.v2_decision_models import (
    ALL_GATE_STATUSES,
    ALL_V2_DECISION_GATE_IDS,
    CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED,
    CONTRACT_ID_V2_GO_NO_GO_DECISION,
    FILENAME_V2_GO_NO_GO_DECISION,
    FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD,
    OUTCOME_NO_GO,
    RECOMMENDED_NEXT_STEP_COLLECT,
    REPORT_FILENAME_V2_GO_NO_GO_DECISION,
    SEAL_KEY_V2_GO_NO_GO_DECISION,
    STATUS_FIXTURE_DECISION_ONLY,
    default_m13_authorization_flags,
)
from starlab.v15.xai_demonstration_io import emit_v15_replay_native_xai_demonstration_fixture
from starlab.v15.xai_demonstration_models import FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION

REPO_ROOT = Path(__file__).resolve().parents[1]


def _emit_m11_claim(tmp_path: Path) -> None:
    emit_v15_human_panel_execution_fixture(tmp_path)
    emit_v15_human_benchmark_claim_decision(
        tmp_path, tmp_path / FILENAME_HUMAN_PANEL_EXECUTION, strict=False
    )


def _emit_upstream_fixture_chain(tmp_path: Path) -> dict[str, Path]:
    m08d = tmp_path / "m08"
    emit_v15_long_gpu_training_manifest_fixture(m08d)
    m03d = tmp_path / "m03"
    emit_checkpoint_lineage_manifest(m03d, profile=CL_PROFILE)
    m05d = tmp_path / "m05"
    emit_v15_strong_agent_scorecard(m05d, profile=M05_PROFILE)
    evd = tmp_path / "ev"
    emit_v15_checkpoint_evaluation_fixture(evd)
    prd = tmp_path / "pr"
    emit_v15_checkpoint_promotion_decision(prd, evd / "v15_checkpoint_evaluation.json")
    m10d = tmp_path / "m10"
    emit_v15_replay_native_xai_demonstration_fixture(m10d)
    m11d = tmp_path / "m11"
    m11d.mkdir()
    _emit_m11_claim(m11d)
    return {
        "m08": m08d / FILENAME_CAMPAIGN_RECEIPT,
        "m03": m03d / FILENAME_CHECKPOINT_LINEAGE,
        "m05": m05d / FILENAME_STRONG_AGENT_SCORECARD,
        "m09": prd / "v15_checkpoint_promotion_decision.json",
        "m10": m10d / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "m11": m11d / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    }


def test_default_fixture_emits_expected_files(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path)
    assert (tmp_path / FILENAME_V2_GO_NO_GO_DECISION).is_file()
    assert (tmp_path / REPORT_FILENAME_V2_GO_NO_GO_DECISION).is_file()
    assert (tmp_path / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD).is_file()


def test_default_decision_is_honest(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8"))
    assert d["v2_decision_status"] == STATUS_FIXTURE_DECISION_ONLY
    assert d["contract_id"] == CONTRACT_ID_V2_GO_NO_GO_DECISION
    assert d["decision_outcome"] == OUTCOME_NO_GO
    assert d["recommended_next_step"] == RECOMMENDED_NEXT_STEP_COLLECT
    af = d["authorization_flags"]
    for k, v in default_m13_authorization_flags().items():
        assert af[k] is v


def test_gate_coverage_is_deterministic(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8"))
    gates = d["decision_gates"]
    assert [g["gate_id"] for g in gates] == list(ALL_V2_DECISION_GATE_IDS)
    assert len(gates) == 15
    for g in gates:
        assert g["status"] in ALL_GATE_STATUSES
    d1 = next(x for x in gates if x["gate_id"] == "D1_m12_release_pack_binding")
    assert d1["status"] == "blocked"


def test_m12_binding_sha_and_wrong_contract_fails(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    m12dir = tmp_path / "m12"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        m12dir,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    m12p = m12dir / FILENAME_SHOWCASE_RELEASE_PACK
    out = tmp_path / "dec"
    emit_v15_v2_go_no_go_decision_operator_preflight(out, m12p, {})
    pack = json.loads((out / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8"))
    exp_sha = sha256_hex_of_canonical_json(json.loads(m12p.read_text(encoding="utf-8")))
    assert pack["m12_showcase_release_pack_json_canonical_sha256"] == exp_sha

    bad = json.loads(m12p.read_text(encoding="utf-8"))
    bad["contract_id"] = "wrong.contract"
    badp = tmp_path / "bad_m12.json"
    badp.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="m12_release_pack"):
        emit_v15_v2_go_no_go_decision_operator_preflight(tmp_path / "o2", badp, {})


def test_fixture_m12_blocks_proceed_to_v2(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    m12dir = tmp_path / "m12"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        m12dir,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    m12p = m12dir / FILENAME_SHOWCASE_RELEASE_PACK
    out = tmp_path / "dec"
    emit_v15_v2_go_no_go_decision_operator_preflight(out, m12p, {})
    d = json.loads((out / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8"))
    assert d["decision_outcome"] == OUTCOME_NO_GO
    assert d["authorization_flags"]["v2_authorized"] is False


def test_optional_upstream_cross_check_wrong_contract_fails(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    m12dir = tmp_path / "m12"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        m12dir,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    m12 = json.loads((m12dir / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    bad_m09 = json.loads(paths["m09"].read_text(encoding="utf-8"))
    bad_m09["contract_id"] = "not.promotion"
    badp = tmp_path / "bad_m09.json"
    badp.write_text(json.dumps(bad_m09), encoding="utf-8")
    opt = {"m09_promotion_decision": badp}
    with pytest.raises(ValueError, match="m09_promotion"):
        verify_upstream_cross_checks(m12, opt)


def test_optional_upstream_sha_mismatch_fails(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    m12dir = tmp_path / "m12"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        m12dir,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    m12 = json.loads((m12dir / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    other_obj = json.loads(paths["m09"].read_text(encoding="utf-8"))
    other_obj["promotion_notes"] = "mutated-for-sha-mismatch-test"
    other = tmp_path / "other_m09.json"
    other.write_text(json.dumps(other_obj), encoding="utf-8")
    opt = {"m09_promotion_decision": other}
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        verify_upstream_cross_checks(m12, opt)


def test_markdown_brief_determinism_and_guardrails(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path / "a")
    emit_v15_v2_go_no_go_decision_fixture(tmp_path / "b")
    t1 = (tmp_path / "a" / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD).read_text(encoding="utf-8")
    t2 = (tmp_path / "b" / FILENAME_V2_GO_NO_GO_DECISION_BRIEF_MD).read_text(encoding="utf-8")
    assert t1 == t2
    low = t1.lower()
    assert "fixture decision validates" in low or "does not authorize v2" in low
    for sub in FORBIDDEN_BRIEF_SUBSTRINGS:
        assert sub not in low


def test_operator_declared_redaction(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    m12dir = tmp_path / "m12"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        m12dir,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    evp = tmp_path / "evidence.json"
    evp.write_text(
        json.dumps(
            {
                "contract_id": CONTRACT_ID_V2_DECISION_OPERATOR_EVIDENCE_DECLARED,
                "evidence_bundle_id": "bundle_x",
                "operator_public_notes": "Contact ops@example.com and C:\\Secret\\note.txt",
                "v2_recharter_scope_declared": True,
                "rights_clearance_operator_declared": True,
            }
        ),
        encoding="utf-8",
    )
    body, _r, _rc = build_v2_decision_body_operator_declared(
        m12dir / FILENAME_SHOWCASE_RELEASE_PACK,
        evp,
        {},
    )
    raw = json.dumps(body["operator_declared_v2_decision_evidence"])
    assert "example.com" not in raw
    assert "C:\\\\Secret" not in raw and "C:\\Secret" not in raw


def test_raw_json_no_absolute_paths_fixture(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path)
    raw = (tmp_path / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8")
    assert "C:\\" not in raw
    assert "/home/" not in raw.lower()
    assert ".sc2replay" not in raw.lower()


def test_emit_cli_fixture(tmp_path: Path) -> None:
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_v2_go_no_go_decision",
            "--output-dir",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, res.stderr
    assert (tmp_path / FILENAME_V2_GO_NO_GO_DECISION).is_file()


def test_seal_valid_fixture(tmp_path: Path) -> None:
    emit_v15_v2_go_no_go_decision_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_V2_GO_NO_GO_DECISION).read_text(encoding="utf-8"))
    seal = d.pop(SEAL_KEY_V2_GO_NO_GO_DECISION)
    assert seal == sha256_hex_of_canonical_json(d)
