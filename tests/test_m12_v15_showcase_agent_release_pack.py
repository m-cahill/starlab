"""V15-M12 showcase agent release pack tests."""

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
    CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION,
    FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION,
    FILENAME_HUMAN_PANEL_EXECUTION,
)
from starlab.v15.long_gpu_training_manifest_io import emit_v15_long_gpu_training_manifest_fixture
from starlab.v15.long_gpu_training_manifest_models import FILENAME_CAMPAIGN_RECEIPT
from starlab.v15.showcase_release_io import (
    FORBIDDEN_BRIEF_SUBSTRINGS,
    emit_v15_showcase_agent_release_pack_fixture,
    emit_v15_showcase_agent_release_pack_operator_declared,
    emit_v15_showcase_agent_release_pack_operator_preflight,
)
from starlab.v15.showcase_release_models import (
    ALL_GATE_STATUSES,
    ALL_RELEASE_GATE_IDS,
    CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED,
    CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK,
    FILENAME_SHOWCASE_RELEASE_BRIEF_MD,
    FILENAME_SHOWCASE_RELEASE_PACK,
    REPORT_FILENAME_SHOWCASE_RELEASE_PACK,
    SEAL_KEY_SHOWCASE_RELEASE_PACK,
    STATUS_FIXTURE_CONTRACT_ONLY,
    default_m12_authorization_flags,
)
from starlab.v15.strong_agent_scorecard_io import emit_v15_strong_agent_scorecard
from starlab.v15.strong_agent_scorecard_models import (
    FILENAME_STRONG_AGENT_SCORECARD,
)
from starlab.v15.strong_agent_scorecard_models import (
    PROFILE_FIXTURE_CI as M05_PROFILE,
)
from starlab.v15.xai_demonstration_io import emit_v15_replay_native_xai_demonstration_fixture
from starlab.v15.xai_demonstration_models import FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION

REPO_ROOT = Path(__file__).resolve().parents[1]


def _emit_m11_claim(tmp_path: Path) -> Path:
    emit_v15_human_panel_execution_fixture(tmp_path)
    emit_v15_human_benchmark_claim_decision(
        tmp_path, tmp_path / FILENAME_HUMAN_PANEL_EXECUTION, strict=False
    )
    return tmp_path / FILENAME_HUMAN_BENCHMARK_CLAIM_DECISION


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
    m11_json = _emit_m11_claim(m11d)
    return {
        "m08": m08d / FILENAME_CAMPAIGN_RECEIPT,
        "m03": m03d / FILENAME_CHECKPOINT_LINEAGE,
        "m05": m05d / FILENAME_STRONG_AGENT_SCORECARD,
        "m09": prd / "v15_checkpoint_promotion_decision.json",
        "m10": m10d / FILENAME_REPLAY_NATIVE_XAI_DEMONSTRATION,
        "m11": m11_json,
    }


def test_default_fixture_emits_three_files(tmp_path: Path) -> None:
    emit_v15_showcase_agent_release_pack_fixture(tmp_path)
    assert (tmp_path / FILENAME_SHOWCASE_RELEASE_PACK).is_file()
    assert (tmp_path / REPORT_FILENAME_SHOWCASE_RELEASE_PACK).is_file()
    assert (tmp_path / FILENAME_SHOWCASE_RELEASE_BRIEF_MD).is_file()


def test_default_status_honest(tmp_path: Path) -> None:
    emit_v15_showcase_agent_release_pack_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    assert d["showcase_release_status"] == STATUS_FIXTURE_CONTRACT_ONLY
    assert d["contract_id"] == CONTRACT_ID_SHOWCASE_AGENT_RELEASE_PACK
    af = d["authorization_flags"]
    for k, v in default_m12_authorization_flags().items():
        assert af[k] is v


def test_gate_coverage_deterministic(tmp_path: Path) -> None:
    emit_v15_showcase_agent_release_pack_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    gates = d["release_gates"]
    assert [g["gate_id"] for g in gates] == list(ALL_RELEASE_GATE_IDS)
    assert len(gates) == 15
    for g in gates:
        assert g["status"] in ALL_GATE_STATUSES
    r1 = next(x for x in gates if x["gate_id"] == "R1_campaign_receipt_binding")
    assert r1["status"] == "blocked"
    r2 = next(x for x in gates if x["gate_id"] == "R2_checkpoint_promotion_binding")
    assert r2["status"] == "blocked"
    r6 = next(x for x in gates if x["gate_id"] == "R6_human_benchmark_claim_binding")
    assert r6["status"] == "blocked"


def test_upstream_binding_and_wrong_contract_fails(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    out = tmp_path / "out"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        out,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    pack = json.loads((out / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    ub = pack["upstream_bindings"]
    for key, p in (
        ("m08_campaign_receipt_json_canonical_sha256", paths["m08"]),
        ("m09_promotion_decision_json_canonical_sha256", paths["m09"]),
        ("m10_replay_native_xai_demonstration_json_canonical_sha256", paths["m10"]),
        ("m11_human_benchmark_claim_decision_json_canonical_sha256", paths["m11"]),
        ("m05_strong_agent_scorecard_json_canonical_sha256", paths["m05"]),
        ("m03_checkpoint_lineage_manifest_json_canonical_sha256", paths["m03"]),
    ):
        exp = sha256_hex_of_canonical_json(json.loads(p.read_text(encoding="utf-8")))
        assert ub[key] == exp
    bad = tmp_path / "bad_m09.json"
    bad.write_text(
        json.dumps({"contract_id": "wrong.contract", "promotion_status": "x"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="m09_promotion"):
        emit_v15_showcase_agent_release_pack_operator_preflight(
            tmp_path / "out2",
            paths["m08"],
            bad,
            paths["m10"],
            paths["m11"],
            paths["m05"],
            paths["m03"],
        )


def test_m11_claim_blocks_r6_on_preflight(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    out = tmp_path / "out"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        out,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    pack = json.loads((out / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    m11 = json.loads(paths["m11"].read_text(encoding="utf-8"))
    assert m11["contract_id"] == CONTRACT_ID_HUMAN_BENCHMARK_CLAIM_DECISION
    assert m11["authorization_flags"]["human_benchmark_claim_authorized"] is False
    r6 = next(
        x for x in pack["release_gates"] if x["gate_id"] == "R6_human_benchmark_claim_binding"
    )
    assert r6["status"] == "blocked"


def test_m09_promotion_blocks_r2_on_preflight(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    out = tmp_path / "out"
    emit_v15_showcase_agent_release_pack_operator_preflight(
        out,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    pack = json.loads((out / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    r2 = next(x for x in pack["release_gates"] if x["gate_id"] == "R2_checkpoint_promotion_binding")
    assert r2["status"] == "blocked"


def test_markdown_brief_deterministic_and_guarded(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    emit_v15_showcase_agent_release_pack_fixture(a)
    emit_v15_showcase_agent_release_pack_fixture(b)
    m1 = (a / FILENAME_SHOWCASE_RELEASE_BRIEF_MD).read_text(encoding="utf-8")
    m2 = (b / FILENAME_SHOWCASE_RELEASE_BRIEF_MD).read_text(encoding="utf-8")
    assert m1 == m2
    low = m1.lower()
    assert "non-claim" in low or "does not release" in low
    for phrase in FORBIDDEN_BRIEF_SUBSTRINGS:
        assert phrase.lower() not in low


def test_operator_declared_redaction(tmp_path: Path) -> None:
    paths = _emit_upstream_fixture_chain(tmp_path)
    ev = tmp_path / "evidence.json"
    ev.write_text(
        json.dumps(
            {
                "contract_id": CONTRACT_ID_OPERATOR_RELEASE_EVIDENCE_DECLARED,
                "evidence_bundle_id": "m12-test-bundle",
                "operator_public_notes": "Call x@example.com at C:\\Secret\\notes.txt",
                "rights_clearance_operator_declared": True,
            }
        ),
        encoding="utf-8",
    )
    out = tmp_path / "outd"
    emit_v15_showcase_agent_release_pack_operator_declared(
        out,
        ev,
        paths["m08"],
        paths["m09"],
        paths["m10"],
        paths["m11"],
        paths["m05"],
        paths["m03"],
    )
    raw = (out / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8")
    assert "example.com" not in raw
    assert "C:\\\\Secret" not in raw


def test_raw_asset_exclusion_fixture_paths(tmp_path: Path) -> None:
    emit_v15_showcase_agent_release_pack_fixture(tmp_path)
    raw = (tmp_path / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8")
    assert "C:\\\\" not in raw
    assert "/home/" not in raw
    assert ".sc2replay" not in raw.lower()
    assert ".ckpt" not in raw.lower()


def test_emit_cli_fixture(tmp_path: Path) -> None:
    o = tmp_path / "cliout"
    o.mkdir()
    p = subprocess.run(
        [
            sys.executable,
            "-m",
            "starlab.v15.emit_v15_showcase_agent_release_pack",
            "--output-dir",
            str(o),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert p.returncode == 0, p.stderr
    assert (o / FILENAME_SHOWCASE_RELEASE_PACK).is_file()


def test_seal_valid_fixture(tmp_path: Path) -> None:
    emit_v15_showcase_agent_release_pack_fixture(tmp_path)
    d = json.loads((tmp_path / FILENAME_SHOWCASE_RELEASE_PACK).read_text(encoding="utf-8"))
    ex = {k: v for k, v in d.items() if k != SEAL_KEY_SHOWCASE_RELEASE_PACK}
    assert d[SEAL_KEY_SHOWCASE_RELEASE_PACK] == sha256_hex_of_canonical_json(ex)
