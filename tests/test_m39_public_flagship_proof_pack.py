"""Tests for M39 public flagship proof pack."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from starlab.flagship.build_public_flagship_proof_pack import (
    default_source_paths,
    write_public_flagship_proof_pack,
)
from starlab.flagship.models import PROOF_PACK_FILENAME, PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1
from starlab.runs.json_util import canonical_json_dumps

REPO_ROOT = Path(__file__).resolve().parents[1]
FIX_M25 = REPO_ROOT / "tests" / "fixtures" / "m25"
FIX_M28 = REPO_ROOT / "tests" / "fixtures" / "m28"
FIX_M31 = REPO_ROOT / "tests" / "fixtures" / "m31"

_FLAGSHIP_SOURCES = [
    Path("starlab") / "flagship" / "models.py",
    Path("starlab") / "flagship" / "build_public_flagship_proof_pack.py",
    Path("starlab") / "flagship" / "emit_public_flagship_proof_pack.py",
]


def test_write_pack_matches_subordinate_goldens(tmp_path: Path) -> None:
    """Bundled surfaces match established M25 / M28 / M31 fixture goldens."""

    write_public_flagship_proof_pack(repo_root=REPO_ROOT, output_dir=tmp_path)

    m25_pack = json.loads(
        (tmp_path / "baseline" / "baseline_evidence_pack.json").read_text(encoding="utf-8")
    )
    m25_golden = json.loads((FIX_M25 / "baseline_evidence_pack.json").read_text(encoding="utf-8"))
    assert m25_pack["evidence_pack_version"] == m25_golden["evidence_pack_version"]
    assert m25_pack["benchmark_contract_sha256"] == m25_golden["benchmark_contract_sha256"]

    m28_ev = json.loads(
        (tmp_path / "learned" / "learned_agent_evaluation.json").read_text(encoding="utf-8")
    )
    m28_golden = json.loads((FIX_M28 / "learned_agent_evaluation.json").read_text(encoding="utf-8"))
    assert canonical_json_dumps(m28_ev) == canonical_json_dumps(m28_golden)

    m31_surf = json.loads(
        (tmp_path / "explorer" / "replay_explorer_surface.json").read_text(encoding="utf-8")
    )
    m31_golden = json.loads(
        (FIX_M31 / "expected_replay_explorer_surface.json").read_text(encoding="utf-8")
    )
    assert canonical_json_dumps(m31_surf) == canonical_json_dumps(m31_golden)


def test_deterministic_repeat(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    write_public_flagship_proof_pack(repo_root=REPO_ROOT, output_dir=d1)
    write_public_flagship_proof_pack(repo_root=REPO_ROOT, output_dir=d2)
    p1 = json.loads((d1 / PROOF_PACK_FILENAME).read_text(encoding="utf-8"))
    p2 = json.loads((d2 / PROOF_PACK_FILENAME).read_text(encoding="utf-8"))
    assert p1["proof_pack_sha256"] == p2["proof_pack_sha256"]
    assert (d1 / "hashes.json").read_text(encoding="utf-8") == (d2 / "hashes.json").read_text(
        encoding="utf-8",
    )


def test_hashes_cover_outputs_only(tmp_path: Path) -> None:
    write_public_flagship_proof_pack(repo_root=REPO_ROOT, output_dir=tmp_path)
    hashes = json.loads((tmp_path / "hashes.json").read_text(encoding="utf-8"))
    assert "public_flagship_proof_pack.json" in hashes
    assert "baseline/baseline_evidence_pack.json" in hashes
    assert all(isinstance(v, str) and len(v) == 64 for v in hashes.values())


def test_proof_pack_schema_keys(tmp_path: Path) -> None:
    write_public_flagship_proof_pack(repo_root=REPO_ROOT, output_dir=tmp_path)
    pack = json.loads((tmp_path / PROOF_PACK_FILENAME).read_text(encoding="utf-8"))
    ver = pack["proof_pack_version"]
    assert ver.startswith("starlab.public_flagship_proof_pack.")
    assert "source_provenance" in pack
    assert "m28_bundle_directory" in pack["source_provenance"]
    assert set(pack["non_claims"]) == set(PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1)
    assert "included_artifacts" in pack
    assert len(pack["included_artifacts"]) == 6


def test_default_source_paths_exist() -> None:
    paths = default_source_paths(REPO_ROOT)
    for key in (
        "m25_scripted_suite",
        "m25_heuristic_suite",
        "m25_tournament",
        "m25_diagnostics",
        "m28_benchmark_contract",
        "m28_baseline",
        "m28_dataset",
        "m28_bundle_dir",
        "m31_bundle_dir",
        "m31_agent",
    ):
        p = paths[key]
        assert p.exists(), key


def test_flagship_modules_have_no_runtime_stack_imports() -> None:
    root = REPO_ROOT
    forbidden = ("starlab.replays", "starlab.sc2", "s2protocol")
    for rel in _FLAGSHIP_SOURCES:
        text = (root / rel).read_text(encoding="utf-8")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not any(alias.name.startswith(prefix) for prefix in forbidden), (
                        f"{rel}: forbidden import {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                assert node.module is not None
                assert not any(
                    node.module == prefix or node.module.startswith(prefix + ".")
                    for prefix in forbidden
                ), f"{rel}: forbidden import from {node.module}"
