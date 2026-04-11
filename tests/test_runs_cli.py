"""M03 ``seed_from_proof`` CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from starlab.runs.seed_from_proof import (
    _find_repo_root,
    build_seed_from_paths,
)
from starlab.runs.seed_from_proof import (
    main as seed_main,
)

from tests.runpy_helpers import run_module_as_main

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def test_seed_from_proof_package_main_invokes_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "seed_from_proof",
            "--proof",
            str(proof),
            "--config",
            str(cfg),
            "--output-dir",
            str(tmp_path),
        ],
    )
    with pytest.raises(SystemExit) as exc:
        run_module_as_main("starlab.runs.seed_from_proof")
    assert exc.value.code == 0
    assert (tmp_path / "run_identity.json").is_file()


def test_seed_from_proof_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "starlab.runs.seed_from_proof", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--proof" in result.stdout


def test_seed_from_proof_writes_artifacts_without_fingerprint(tmp_path: Path) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    argv = [
        "--proof",
        str(proof),
        "--config",
        str(cfg),
        "--output-dir",
        str(tmp_path),
        "--no-environment-fingerprint",
    ]
    assert seed_main(argv) == 0
    ri = json.loads((tmp_path / "run_identity.json").read_text(encoding="utf-8"))
    assert ri.get("environment_fingerprint") is None


def test_seed_from_proof_writes_artifacts(tmp_path: Path) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    argv = [
        "--proof",
        str(proof),
        "--config",
        str(cfg),
        "--output-dir",
        str(tmp_path),
    ]
    assert seed_main(argv) == 0
    ri = tmp_path / "run_identity.json"
    ls = tmp_path / "lineage_seed.json"
    assert ri.is_file()
    assert ls.is_file()
    text_ri = ri.read_text(encoding="utf-8")
    assert "run_spec_id" in text_ri
    assert "starlab.run_identity.v1" in text_ri
    text_ls = ls.read_text(encoding="utf-8")
    assert "lineage_seed_id" in text_ls
    assert "starlab.lineage_seed.v1" in text_ls


def test_find_repo_root_falls_back_to_cwd_when_paths_outside_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Use repo ``cwd`` when proof/config paths are outside any tree with ``pyproject.toml``."""
    repo_root = Path(__file__).resolve().parents[1]
    nest = tmp_path / "outside_repo"
    nest.mkdir()
    p1 = nest / "a.json"
    p2 = nest / "b.json"
    p1.write_text("{}", encoding="utf-8")
    p2.write_text("{}", encoding="utf-8")
    monkeypatch.chdir(repo_root)
    assert _find_repo_root(p1, p2).resolve() == repo_root.resolve()


def test_find_repo_root_raises_when_no_pyproject_in_paths_or_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    nest = tmp_path / "deep" / "nest"
    nest.mkdir(parents=True)
    p = nest / "x.json"
    p.write_text("{}", encoding="utf-8")
    monkeypatch.chdir(nest)
    with pytest.raises(ValueError, match="could not locate repo root"):
        _find_repo_root(p, p)


def test_build_seed_from_paths_rejects_non_object_proof(tmp_path: Path) -> None:
    proof = tmp_path / "not_object.json"
    proof.write_text("[]", encoding="utf-8")
    cfg = FIXTURE_DIR / "m02_match_config.json"
    with pytest.raises(ValueError, match="proof root must be a JSON object"):
        build_seed_from_paths(
            proof_path=proof,
            config_path=cfg,
            env_path=None,
            include_fingerprint=True,
        )


def test_build_seed_from_paths_accepts_optional_env_json(tmp_path: Path) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    env = tmp_path / "env.json"
    env_payload = '{"base_build": "env-override", "data_version": "dv-override"}'
    env.write_text(env_payload, encoding="utf-8")
    ri, _ls = build_seed_from_paths(
        proof_path=proof,
        config_path=cfg,
        env_path=env,
        include_fingerprint=True,
    )
    fp = ri.get("environment_fingerprint") or {}
    assert fp.get("base_build") == "env-override"
    assert fp.get("data_version") == "dv-override"


def test_build_seed_from_paths_repo_relative_falls_back_when_proof_outside_repo() -> None:
    proof_src = FIXTURE_DIR / "m02_match_execution_proof.json"
    outside = Path(tempfile.gettempdir()) / "starlab_m37_seed_proof_outside_repo.json"
    outside.write_text(proof_src.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = FIXTURE_DIR / "m02_match_config.json"
    _ri, ls = build_seed_from_paths(
        proof_path=outside,
        config_path=cfg,
        env_path=None,
        include_fingerprint=False,
    )
    inputs = {r["logical_name"]: r.get("path") for r in ls["input_references"]}
    assert inputs["match_execution_proof"] == outside.as_posix()


def test_build_seed_from_paths_rejects_non_object_env(tmp_path: Path) -> None:
    proof = FIXTURE_DIR / "m02_match_execution_proof.json"
    cfg = FIXTURE_DIR / "m02_match_config.json"
    env = tmp_path / "env.json"
    env.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="env JSON root must be an object"):
        build_seed_from_paths(
            proof_path=proof,
            config_path=cfg,
            env_path=env,
            include_fingerprint=True,
        )


def test_seed_from_proof_rejects_bad_hash(tmp_path: Path) -> None:
    good = (FIXTURE_DIR / "m02_match_execution_proof.json").read_text(encoding="utf-8")
    bad = good.replace(
        "d8e2fcb2e227c7c3e7e908c0df140586572f7c8c25fb67db1be823f445062774",
        "0" * 64,
    )
    proof = tmp_path / "bad_proof.json"
    proof.write_text(bad, encoding="utf-8")
    cfg = FIXTURE_DIR / "m02_match_config.json"
    out = tmp_path / "out"
    out.mkdir()
    argv = ["--proof", str(proof), "--config", str(cfg), "--output-dir", str(out)]
    with pytest.raises(ValueError, match="artifact_hash"):
        seed_main(argv)
