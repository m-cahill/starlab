"""M05 ``build_canonical_run_artifact`` CLI tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from starlab.runs.build_canonical_run_artifact import main as build_main
from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_content_sha256,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
OPAQUE_REPLAY_FIXTURE = FIXTURE_DIR / "replay_m07_generated.SC2Replay"


def _write_upstream(tmp_path: Path) -> tuple[Path, Path, Path]:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    rb = build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=compute_replay_content_sha256(OPAQUE_REPLAY_FIXTURE),
        replay_reference=build_replay_reference(OPAQUE_REPLAY_FIXTURE),
        run_spec_id=ri["run_spec_id"],
    )
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    write_json_record(rb_path, rb)
    return ri_path, ls_path, rb_path


def test_build_canonical_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "starlab.runs.build_canonical_run_artifact", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--run-identity" in result.stdout
    assert "--replay-binding" in result.stdout


def test_build_canonical_writes_bundle(tmp_path: Path) -> None:
    ri_path, ls_path, rb_path = _write_upstream(tmp_path / "up")
    out = tmp_path / "out"
    argv = [
        "--run-identity",
        str(ri_path),
        "--lineage-seed",
        str(ls_path),
        "--replay-binding",
        str(rb_path),
        "--output-dir",
        str(out),
    ]
    assert build_main(argv) == 0
    assert (out / "manifest.json").is_file()
    assert (out / "hashes.json").is_file()
    assert (out / "run_identity.json").is_file()
    assert (out / "lineage_seed.json").is_file()
    assert (out / "replay_binding.json").is_file()
    data = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "starlab.canonical_run_artifact.v0"
    assert data["external_references"]["replay_bytes_included"] is False


def test_build_canonical_deterministic_across_runs(tmp_path: Path) -> None:
    ri_path, ls_path, rb_path = _write_upstream(tmp_path / "up")
    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    for out in (out1, out2):
        assert (
            build_main(
                [
                    "--run-identity",
                    str(ri_path),
                    "--lineage-seed",
                    str(ls_path),
                    "--replay-binding",
                    str(rb_path),
                    "--output-dir",
                    str(out),
                ],
            )
            == 0
        )
    assert (out1 / "hashes.json").read_bytes() == (out2 / "hashes.json").read_bytes()


def test_build_canonical_rejects_missing_run_identity(tmp_path: Path) -> None:
    _, ls_path, rb_path = _write_upstream(tmp_path / "up")
    out = tmp_path / "out"
    assert (
        build_main(
            [
                "--run-identity",
                str(tmp_path / "missing.json"),
                "--lineage-seed",
                str(ls_path),
                "--replay-binding",
                str(rb_path),
                "--output-dir",
                str(out),
            ],
        )
        == 1
    )


def test_build_canonical_rejects_mismatched_upstream(tmp_path: Path) -> None:
    ri_path, ls_path, rb_path = _write_upstream(tmp_path / "up")
    bad_ls = tmp_path / "bad_ls.json"
    data = json.loads(ls_path.read_text(encoding="utf-8"))
    data["lineage_seed_id"] = "0" * 64
    bad_ls.write_text(json.dumps(data), encoding="utf-8")
    out = tmp_path / "out"
    assert (
        build_main(
            [
                "--run-identity",
                str(ri_path),
                "--lineage-seed",
                str(bad_ls),
                "--replay-binding",
                str(rb_path),
                "--output-dir",
                str(out),
            ],
        )
        == 1
    )


def test_build_canonical_rejects_existing_output_dir(tmp_path: Path) -> None:
    ri_path, ls_path, rb_path = _write_upstream(tmp_path / "up")
    out = tmp_path / "out"
    out.mkdir()
    assert (
        build_main(
            [
                "--run-identity",
                str(ri_path),
                "--lineage-seed",
                str(ls_path),
                "--replay-binding",
                str(rb_path),
                "--output-dir",
                str(out),
            ],
        )
        == 1
    )


def test_build_canonical_rejects_malformed_replay_binding(tmp_path: Path) -> None:
    ri_path, ls_path, _rb_path = _write_upstream(tmp_path / "up")
    bad_rb = tmp_path / "bad_rb.json"
    bad_rb.write_text('{"schema_version": "starlab.replay_binding.v1"}', encoding="utf-8")
    out = tmp_path / "out"
    assert (
        build_main(
            [
                "--run-identity",
                str(ri_path),
                "--lineage-seed",
                str(ls_path),
                "--replay-binding",
                str(bad_rb),
                "--output-dir",
                str(out),
            ],
        )
        == 1
    )
