"""M04 ``bind_replay`` CLI tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from starlab.runs.bind_replay import main as bind_main
from starlab.runs.replay_binding import REPLAY_BINDING_SCHEMA_VERSION
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

from tests.runpy_helpers import run_module_as_main

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
OPAQUE_REPLAY_FIXTURE = FIXTURE_DIR / "replay_m07_generated.SC2Replay"


def _generate_m03_artifacts(tmp_path: Path) -> tuple[Path, Path]:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    return ri_path, ls_path


def test_bind_replay_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "starlab.runs.bind_replay", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--run-identity" in result.stdout
    assert "--replay" in result.stdout


def test_bind_replay_writes_artifact(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path / "m03")
    out = tmp_path / "out"

    argv = [
        "--run-identity",
        str(ri_path),
        "--lineage-seed",
        str(ls_path),
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--output-dir",
        str(out),
    ]
    assert bind_main(argv) == 0

    rb = out / "replay_binding.json"
    assert rb.is_file()
    data = json.loads(rb.read_text(encoding="utf-8"))
    assert data["schema_version"] == REPLAY_BINDING_SCHEMA_VERSION
    assert len(data["replay_binding_id"]) == 64
    assert data["replay_reference"]["basename"] == "replay_m07_generated.SC2Replay"
    assert data["binding_mode"] == "opaque_content_sha256"


def test_bind_replay_deterministic_across_runs(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path / "m03")

    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"

    for out_dir in (out1, out2):
        argv = [
            "--run-identity",
            str(ri_path),
            "--lineage-seed",
            str(ls_path),
            "--replay",
            str(OPAQUE_REPLAY_FIXTURE),
            "--output-dir",
            str(out_dir),
        ]
        assert bind_main(argv) == 0

    text1 = (out1 / "replay_binding.json").read_text(encoding="utf-8")
    text2 = (out2 / "replay_binding.json").read_text(encoding="utf-8")
    assert text1 == text2


def test_bind_replay_rejects_missing_lineage_seed(tmp_path: Path) -> None:
    ri_path, _ls_path = _generate_m03_artifacts(tmp_path / "m03")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(ri_path),
        "--lineage-seed",
        str(tmp_path / "missing_lineage_seed.json"),
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--output-dir",
        str(out),
    ]
    assert bind_main(argv) == 1


def test_bind_replay_rejects_missing_run_identity(tmp_path: Path) -> None:
    _, ls_path = _generate_m03_artifacts(tmp_path / "m03")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(tmp_path / "nonexistent.json"),
        "--lineage-seed",
        str(ls_path),
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--output-dir",
        str(out),
    ]
    assert bind_main(argv) == 1


def test_bind_replay_rejects_missing_replay(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path / "m03")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(ri_path),
        "--lineage-seed",
        str(ls_path),
        "--replay",
        str(tmp_path / "nonexistent.SC2Replay"),
        "--output-dir",
        str(out),
    ]
    assert bind_main(argv) == 1


def test_bind_replay_rejects_malformed_run_identity(tmp_path: Path) -> None:
    _, ls_path = _generate_m03_artifacts(tmp_path / "m03")
    bad_ri = tmp_path / "bad_ri.json"
    bad_ri.write_text('{"not_a_valid_field": true}', encoding="utf-8")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(bad_ri),
        "--lineage-seed",
        str(ls_path),
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--output-dir",
        str(out),
    ]
    with pytest.raises(ValueError, match="missing required field"):
        bind_main(argv)


def test_bind_replay_package_main_help(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["bind_replay", "--help"])
    with pytest.raises(SystemExit) as exc:
        run_module_as_main("starlab.runs.bind_replay")
    assert exc.value.code == 0


def test_bind_replay_rejects_wrong_schema_version(tmp_path: Path) -> None:
    ri_path, ls_path = _generate_m03_artifacts(tmp_path / "m03")
    data = json.loads(ri_path.read_text(encoding="utf-8"))
    data["schema_version"] = "wrong.version"
    ri_path.write_text(json.dumps(data), encoding="utf-8")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(ri_path),
        "--lineage-seed",
        str(ls_path),
        "--replay",
        str(OPAQUE_REPLAY_FIXTURE),
        "--output-dir",
        str(out),
    ]
    with pytest.raises(ValueError, match="schema_version"):
        bind_main(argv)
