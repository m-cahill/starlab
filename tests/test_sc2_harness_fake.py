"""Fake-adapter harness (CI-safe)."""

from __future__ import annotations

from pathlib import Path

from starlab.sc2.artifacts import compute_artifact_hash
from starlab.sc2.harness import run_match_execution
from starlab.sc2.match_config import BoundedHorizon, MapSpec, MatchConfig


def test_fake_harness_twice_same_hash() -> None:
    cfg = MatchConfig(
        schema_version="1",
        adapter="fake",
        seed=99,
        bounded_horizon=BoundedHorizon(5, 1),
        map=MapSpec(discover_under_maps_dir=True),
    )
    a = run_match_execution(cfg)
    b = run_match_execution(cfg)
    assert a.ok and a.proof is not None
    assert b.ok and b.proof is not None
    assert compute_artifact_hash(a.proof) == compute_artifact_hash(b.proof)


def test_run_match_cli_writes_file(tmp_path: Path) -> None:
    from starlab.sc2.run_match import main

    fixture = Path(__file__).resolve().parent / "fixtures" / "match_fake_m02.json"
    code = main(["--config", str(fixture), "--output-dir", str(tmp_path)])
    assert code == 0
    proof = tmp_path / "match_execution_proof.json"
    assert proof.is_file()
    text = proof.read_text(encoding="utf-8")
    assert "artifact_hash" in text
