"""M16 canonical state pipeline tests (fixture JSON; no raw replay, no s2protocol)."""

from __future__ import annotations

import json
import runpy
import shutil
import sys
from pathlib import Path

import pytest
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.state.canonical_state_inputs import load_m14_bundle
from starlab.state.canonical_state_pipeline import (
    materialize_canonical_state,
)

FIX = Path(__file__).resolve().parent / "fixtures" / "m16"
BUNDLE = FIX / "bundle"


def test_load_m14_bundle_happy() -> None:
    bundle, err = load_m14_bundle(BUNDLE)
    assert err is None
    assert bundle is not None
    assert bundle.manifest.get("bundle_id")


def test_materialize_matches_golden() -> None:
    bundle, err = load_m14_bundle(BUNDLE)
    assert err is None
    assert bundle is not None
    frame, report, _warnings = materialize_canonical_state(bundle, target_gameloop=1200)

    exp_f = json.loads((FIX / "expected_canonical_state.json").read_text(encoding="utf-8"))
    exp_r = json.loads((FIX / "expected_canonical_state_report.json").read_text(encoding="utf-8"))
    assert json.loads(canonical_json_dumps(frame)) == exp_f
    assert json.loads(canonical_json_dumps(report)) == exp_r


def test_deterministic_repeat_emission() -> None:
    bundle, err = load_m14_bundle(BUNDLE)
    assert err is None
    assert bundle is not None
    f1, r1, _ = materialize_canonical_state(bundle, target_gameloop=1200)
    f2, r2, _ = materialize_canonical_state(bundle, target_gameloop=1200)
    assert sha256_hex_of_canonical_json(f1) == sha256_hex_of_canonical_json(f2)
    assert sha256_hex_of_canonical_json(r1) == sha256_hex_of_canonical_json(r2)


def test_out_of_range_gameloop_raises() -> None:
    bundle, err = load_m14_bundle(BUNDLE)
    assert err is None
    assert bundle is not None
    with pytest.raises(ValueError, match="exceeds replay_length_loops"):
        materialize_canonical_state(bundle, target_gameloop=1201)


def test_missing_primary_artifact_fails(tmp_path: Path) -> None:
    d = tmp_path / "partial"
    shutil.copytree(BUNDLE, d)
    (d / "replay_slices.json").unlink()
    bundle, err = load_m14_bundle(d)
    assert bundle is None
    assert err is not None
    assert "replay_slices.json" in err.lower() or "artifact" in err.lower()


def test_manifest_hash_mismatch_fails(tmp_path: Path) -> None:
    d = tmp_path / "bad"
    shutil.copytree(BUNDLE, d)
    mp = json.loads((d / "replay_bundle_manifest.json").read_text(encoding="utf-8"))
    mp["artifact_hashes"] = dict(mp["artifact_hashes"])
    mp["artifact_hashes"]["replay_metadata.json"] = "0" * 64
    (d / "replay_bundle_manifest.json").write_text(canonical_json_dumps(mp), encoding="utf-8")
    bundle, err = load_m14_bundle(d)
    assert bundle is None
    assert err is not None
    assert "hash mismatch" in err.lower()


def test_bundle_id_mismatch_in_contents_fails(tmp_path: Path) -> None:
    d = tmp_path / "bid"
    shutil.copytree(BUNDLE, d)
    c = json.loads((d / "replay_bundle_contents.json").read_text(encoding="utf-8"))
    c["bundle_id"] = "f" * 64
    (d / "replay_bundle_contents.json").write_text(canonical_json_dumps(c), encoding="utf-8")
    bundle, err = load_m14_bundle(d)
    assert bundle is None
    assert err is not None
    assert "bundle_id" in err.lower()


def test_emit_canonical_state_package_main_help(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["emit_canonical_state", "--help"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("starlab.state.emit_canonical_state", run_name="__main__")
    assert exc.value.code == 0


def test_emit_cli_writes_artifacts(tmp_path: Path) -> None:
    from starlab.state.emit_canonical_state import main

    out = tmp_path / "out"
    code = main(
        [
            "--bundle-dir",
            str(BUNDLE),
            "--gameloop",
            "1200",
            "--output-dir",
            str(out),
        ],
    )
    assert code == 0
    assert (out / "canonical_state.json").is_file()
    assert (out / "canonical_state_report.json").is_file()


def test_emit_cli_failure_bad_gameloop(tmp_path: Path) -> None:
    from starlab.state.emit_canonical_state import main

    out_dir = tmp_path / "out2"
    code = main(
        [
            "--bundle-dir",
            str(BUNDLE),
            "--gameloop",
            "999999",
            "--output-dir",
            str(out_dir),
        ],
    )
    assert code == 2
