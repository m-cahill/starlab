"""Tests for V15-M55 bounded evaluation package preflight."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.v15.m55_bounded_evaluation_package_preflight_io import (
    OperatorDeclaredInputs,
    build_fixture_preflight,
    build_operator_declared_preflight,
    build_operator_preflight_blocked,
    evaluation_package_binding_sha256,
    seal_m55_body,
    sha256_file_hex,
    validate_sha256,
    write_preflight_artifacts,
)
from starlab.v15.m55_bounded_evaluation_package_preflight_models import (
    CANONICAL_UPSTREAM_M54_PACKAGE_ID,
    CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
    EMITTER_MODULE,
    FILENAME_MAIN_JSON,
    FORBIDDEN_FLAG_CLAIM_BENCHMARK,
    FORBIDDEN_FLAG_TORCH_LOAD,
    GATE_ARTIFACT_DIGEST_FIELD,
    PROFILE_FIXTURE_CI,
    PROFILE_OPERATOR_DECLARED,
    PROFILE_OPERATOR_PREFLIGHT,
    REPORT_CONTRACT_ID,
    REPORT_FILENAME,
    STATUS_BLOCKED_CLAIM_VIOLATION,
    STATUS_BLOCKED_IDENTITY_MISMATCH,
    STATUS_BLOCKED_MISSING_INPUT,
    STATUS_BLOCKED_PRIVATE_BOUNDARY,
    STATUS_READY,
)


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_fixture_deterministic_and_ready(tmp_path: Path) -> None:
    sealed1, paths1 = write_preflight_artifacts(
        tmp_path / "a", body_unsealed=build_fixture_preflight()
    )
    sealed2, paths2 = write_preflight_artifacts(
        tmp_path / "b", body_unsealed=build_fixture_preflight()
    )
    assert paths1[0].name == FILENAME_MAIN_JSON
    assert paths1[1].name == REPORT_FILENAME
    assert canonical_json_dumps(sealed1) == canonical_json_dumps(sealed2)
    assert sealed1["preflight_status"] == STATUS_READY
    assert sealed1["required_inputs"]["m54_package_sha256"] == CANONICAL_UPSTREAM_M54_PACKAGE_SHA256
    for _k, v in sealed1["claim_flags"].items():
        assert v is False
    rep = json.loads(paths1[1].read_text(encoding="utf-8"))
    assert rep["contract_id"] == REPORT_CONTRACT_ID
    assert rep["ready_for_next_step"] is True


def test_seal_roundtrip() -> None:
    body = build_fixture_preflight()
    sealed = seal_m55_body(body)
    digest = sealed[GATE_ARTIFACT_DIGEST_FIELD]
    base = {k: v for k, v in sealed.items() if k != GATE_ARTIFACT_DIGEST_FIELD}
    assert digest == sha256_hex_of_canonical_json(base)


def test_validate_sha256() -> None:
    h = "a" * 64
    assert validate_sha256(h) == h.lower()
    assert validate_sha256("A" * 64) == "a" * 64
    assert validate_sha256("g" * 64) is None
    assert validate_sha256("abc") is None


def test_operator_declared_happy_path(tmp_path: Path) -> None:
    man = tmp_path / "manifest.json"
    cand = tmp_path / "cand.json"
    score = tmp_path / "score.json"
    man.write_text(json.dumps({"kind": "manifest", "v": 1}), encoding="utf-8")
    cand.write_text(json.dumps({"candidate": "x"}), encoding="utf-8")
    score.write_text(json.dumps({"plan": "y"}), encoding="utf-8")
    md = sha256_file_hex(man)
    cd = sha256_file_hex(cand)
    sd = sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md,
        candidate_sha256=cd,
        scorecard_sha256=sd,
    )
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="starlab.eval_pkg.unit_test",
            evaluation_package_sha256=pkg,
            upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_READY


def test_operator_wrong_m54_sha_blocks(tmp_path: Path) -> None:
    man = tmp_path / "m.json"
    man.write_text("{}", encoding="utf-8")
    cand = tmp_path / "c.json"
    cand.write_text("{}", encoding="utf-8")
    score = tmp_path / "s.json"
    score.write_text("{}", encoding="utf-8")
    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md, candidate_sha256=cd, scorecard_sha256=sd
    )
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="e",
            evaluation_package_sha256=pkg,
            upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            upstream_m54_package_sha256="f" * 64,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_BLOCKED_IDENTITY_MISMATCH


def test_operator_wrong_m54_package_id_blocks(tmp_path: Path) -> None:
    man = tmp_path / "m.json"
    man.write_text("{}", encoding="utf-8")
    cand = tmp_path / "c.json"
    cand.write_text("{}", encoding="utf-8")
    score = tmp_path / "s.json"
    score.write_text("{}", encoding="utf-8")
    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md, candidate_sha256=cd, scorecard_sha256=sd
    )
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="e",
            evaluation_package_sha256=pkg,
            upstream_m54_package_id="wrong.id",
            upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_BLOCKED_IDENTITY_MISMATCH


def test_company_secrets_path_blocks(tmp_path: Path) -> None:
    man = tmp_path / "m.json"
    man.write_text('{"note": "docs/company_secrets/x"}', encoding="utf-8")
    cand = tmp_path / "c.json"
    cand.write_text("{}", encoding="utf-8")
    score = tmp_path / "s.json"
    score.write_text("{}", encoding="utf-8")
    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md, candidate_sha256=cd, scorecard_sha256=sd
    )
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="e",
            evaluation_package_sha256=pkg,
            upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_BLOCKED_PRIVATE_BOUNDARY


def test_claim_flag_in_json_blocks(tmp_path: Path) -> None:
    man = tmp_path / "m.json"
    man.write_text(json.dumps({"benchmark_pass_claimed": True}), encoding="utf-8")
    cand = tmp_path / "c.json"
    cand.write_text("{}", encoding="utf-8")
    score = tmp_path / "s.json"
    score.write_text("{}", encoding="utf-8")
    md, cd, sd = sha256_file_hex(man), sha256_file_hex(cand), sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md, candidate_sha256=cd, scorecard_sha256=sd
    )
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="e",
            evaluation_package_sha256=pkg,
            upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_BLOCKED_CLAIM_VIOLATION


def test_operator_preflight_profile_blocked(tmp_path: Path) -> None:
    body = build_operator_preflight_blocked()
    assert body["preflight_status"] == STATUS_BLOCKED_MISSING_INPUT
    sealed, _paths = write_preflight_artifacts(tmp_path / "op", body_unsealed=body)
    assert sealed["profile"] == PROFILE_OPERATOR_PREFLIGHT


def test_package_sha_mismatch_blocks(tmp_path: Path) -> None:
    man = tmp_path / "m.json"
    man.write_text("{}", encoding="utf-8")
    cand = tmp_path / "c.json"
    cand.write_text("{}", encoding="utf-8")
    score = tmp_path / "s.json"
    score.write_text("{}", encoding="utf-8")
    body = build_operator_declared_preflight(
        OperatorDeclaredInputs(
            evaluation_package_id="e",
            evaluation_package_sha256="a" * 64,
            upstream_m54_package_id=CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            upstream_m54_package_sha256=CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            evaluation_package_manifest=man,
            candidate_identity=cand,
            scorecard_readout_plan=score,
        ),
    )
    assert body["preflight_status"] == STATUS_BLOCKED_IDENTITY_MISMATCH


@pytest.mark.parametrize(
    "flag",
    [
        FORBIDDEN_FLAG_CLAIM_BENCHMARK,
        "--claim-strength",
        FORBIDDEN_FLAG_TORCH_LOAD,
    ],
)
def test_cli_forbidden_flags(tmp_path: Path, repo_root: Path, flag: str) -> None:
    out = tmp_path / "rf"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            PROFILE_OPERATOR_PREFLIGHT,
            "--output-dir",
            str(out),
            flag,
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["preflight_status"] == STATUS_BLOCKED_CLAIM_VIOLATION


def test_cli_fixture_writes_both(tmp_path: Path, repo_root: Path) -> None:
    out = tmp_path / "fx"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            PROFILE_FIXTURE_CI,
            "--output-dir",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert (out / FILENAME_MAIN_JSON).is_file()
    assert (out / REPORT_FILENAME).is_file()


def test_cli_operator_preflight_exit_3(tmp_path: Path, repo_root: Path) -> None:
    out = tmp_path / "pf"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            PROFILE_OPERATOR_PREFLIGHT,
            "--output-dir",
            str(out),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 3


def test_cli_malformed_sha_exit_2(tmp_path: Path, repo_root: Path) -> None:
    m = tmp_path / "m.json"
    c = tmp_path / "c.json"
    s = tmp_path / "s.json"
    m.write_text("{}", encoding="utf-8")
    c.write_text("{}", encoding="utf-8")
    s.write_text("{}", encoding="utf-8")
    out = tmp_path / "bad"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            PROFILE_OPERATOR_DECLARED,
            "--output-dir",
            str(out),
            "--evaluation-package-id",
            "x",
            "--evaluation-package-sha256",
            "not-valid-hex",
            "--upstream-m54-package-id",
            CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            "--upstream-m54-package-sha256",
            CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            "--evaluation-package-manifest",
            str(m),
            "--candidate-identity",
            str(c),
            "--scorecard-readout-plan",
            str(s),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2


def test_cli_operator_declared_ready(tmp_path: Path, repo_root: Path) -> None:
    man = tmp_path / "m.json"
    cand = tmp_path / "c.json"
    score = tmp_path / "s.json"
    man.write_text(json.dumps({"k": 1}), encoding="utf-8")
    cand.write_text(json.dumps({"k": 2}), encoding="utf-8")
    score.write_text(json.dumps({"k": 3}), encoding="utf-8")
    md = sha256_file_hex(man)
    cd = sha256_file_hex(cand)
    sd = sha256_file_hex(score)
    pkg = evaluation_package_binding_sha256(
        manifest_sha256=md, candidate_sha256=cd, scorecard_sha256=sd
    )
    out = tmp_path / "decl"
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            EMITTER_MODULE,
            "--profile",
            PROFILE_OPERATOR_DECLARED,
            "--output-dir",
            str(out),
            "--evaluation-package-id",
            "cli_pkg_test",
            "--evaluation-package-sha256",
            pkg,
            "--upstream-m54-package-id",
            CANONICAL_UPSTREAM_M54_PACKAGE_ID,
            "--upstream-m54-package-sha256",
            CANONICAL_UPSTREAM_M54_PACKAGE_SHA256,
            "--evaluation-package-manifest",
            str(man),
            "--candidate-identity",
            str(cand),
            "--scorecard-readout-plan",
            str(score),
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    sealed = json.loads((out / FILENAME_MAIN_JSON).read_text(encoding="utf-8"))
    assert sealed["preflight_status"] == STATUS_READY


def test_git_ls_files_company_secrets_empty(repo_root: Path) -> None:
    res = subprocess.run(
        ["git", "ls-files", "docs/company_secrets"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert res.stdout.strip() == ""
