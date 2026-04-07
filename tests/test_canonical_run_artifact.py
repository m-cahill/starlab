"""M05 canonical run artifact: coherence, hashes, determinism, e2e."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from starlab.runs.canonical_run_artifact import (
    CANONICAL_RUN_ARTIFACT_SCHEMA_VERSION,
    INCLUDED_ARTIFACTS,
    build_hashes_mapping,
    build_manifest_mapping,
    compute_artifact_hashes,
    compute_run_artifact_id,
    load_validated_upstream,
    validate_included_artifacts,
    validate_upstream_coherence,
    write_canonical_run_artifact_bundle,
)
from starlab.runs.replay_binding import (
    build_replay_binding_record,
    build_replay_reference,
    compute_replay_content_sha256,
    load_replay_binding,
    write_replay_binding,
)
from starlab.runs.seed_from_proof import build_seed_from_paths
from starlab.runs.writer import write_json_record

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
SYNTHETIC_REPLAY = FIXTURE_DIR / "synthetic_opaque_test.SC2Replay"
M05_EXPECTED = FIXTURE_DIR / "m05_expected"


def _m03_from_fixtures() -> tuple[dict[str, Any], dict[str, Any]]:
    ri, ls = build_seed_from_paths(
        config_path=FIXTURE_DIR / "m02_match_config.json",
        env_path=None,
        include_fingerprint=False,
        proof_path=FIXTURE_DIR / "m02_match_execution_proof.json",
    )
    return ri, ls


def _m04_record(ri: dict[str, Any], ls: dict[str, Any]) -> dict[str, Any]:
    sha = compute_replay_content_sha256(SYNTHETIC_REPLAY)
    ref = build_replay_reference(SYNTHETIC_REPLAY)
    return build_replay_binding_record(
        execution_id=ri["execution_id"],
        lineage_seed_id=ls["lineage_seed_id"],
        proof_artifact_hash=ri["proof_artifact_hash"],
        replay_content_sha256=sha,
        replay_reference=ref,
        run_spec_id=ri["run_spec_id"],
    )


def test_validate_included_artifacts_rejects_drift() -> None:
    with pytest.raises(ValueError, match="included_artifacts must match"):
        validate_included_artifacts(
            ["run_identity.json", "replay_binding.json", "lineage_seed.json"],
        )


def test_validate_included_artifacts_accepts_canonical() -> None:
    validate_included_artifacts(list(INCLUDED_ARTIFACTS))


def test_manifest_and_hashes_stable_unit() -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    validate_upstream_coherence(lineage_seed=ls, replay_binding=rb, run_identity=ri)
    m1 = build_manifest_mapping(lineage_seed=ls, replay_binding=rb, run_identity=ri)
    m2 = build_manifest_mapping(lineage_seed=ls, replay_binding=rb, run_identity=ri)
    assert m1 == m2
    assert m1["schema_version"] == CANONICAL_RUN_ARTIFACT_SCHEMA_VERSION
    assert m1["parent_references"] == []
    assert m1["included_artifacts"] == list(INCLUDED_ARTIFACTS)

    h1 = compute_artifact_hashes(
        lineage_seed=ls,
        manifest=m1,
        replay_binding=rb,
        run_identity=ri,
    )
    h2 = compute_artifact_hashes(
        lineage_seed=ls,
        manifest=m2,
        replay_binding=rb,
        run_identity=ri,
    )
    assert h1 == h2
    rid1 = compute_run_artifact_id(artifact_hashes=h1)
    rid2 = compute_run_artifact_id(artifact_hashes=h2)
    assert rid1 == rid2
    assert len(rid1) == 64

    hashes_rec = build_hashes_mapping(artifact_hashes=h1)
    assert hashes_rec["run_artifact_id"] == rid1


def test_coherence_rejects_run_spec_mismatch(tmp_path: Path) -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    bad = dict(rb)
    bad["run_spec_id"] = "0" * 64
    with pytest.raises(ValueError, match="run_spec_id mismatch"):
        validate_upstream_coherence(lineage_seed=ls, replay_binding=bad, run_identity=ri)


def test_coherence_rejects_proof_hash_mismatch(tmp_path: Path) -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    bad = dict(ls)
    bad["proof_artifact_hash"] = "f" * 64
    with pytest.raises(ValueError, match="proof_artifact_hash mismatch"):
        validate_upstream_coherence(lineage_seed=bad, replay_binding=rb, run_identity=ri)


def test_load_replay_binding_used_in_pipeline(tmp_path: Path) -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    rb_path = tmp_path / "replay_binding.json"
    write_replay_binding(tmp_path, rb)
    loaded = load_replay_binding(rb_path)
    assert loaded["replay_binding_id"] == rb["replay_binding_id"]


def test_write_bundle_rejects_existing_output_dir(tmp_path: Path) -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    write_json_record(rb_path, rb)
    out = tmp_path / "bundle"
    out.mkdir()
    with pytest.raises(ValueError, match="already exists"):
        write_canonical_run_artifact_bundle(
            lineage_seed_path=ls_path,
            output_dir=out,
            replay_binding_path=rb_path,
            run_identity_path=ri_path,
        )


def test_canonical_re_emission_not_raw_copy(tmp_path: Path) -> None:
    """Whitespace-only differences in inputs are normalized in the bundle."""

    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    write_json_record(rb_path, rb)

    messy = tmp_path / "messy_ri.json"
    messy.write_text(json.dumps(ri, indent=4), encoding="utf-8")

    out1 = tmp_path / "b1"
    out2 = tmp_path / "b2"
    write_canonical_run_artifact_bundle(
        lineage_seed_path=ls_path,
        output_dir=out1,
        replay_binding_path=rb_path,
        run_identity_path=ri_path,
    )
    write_canonical_run_artifact_bundle(
        lineage_seed_path=ls_path,
        output_dir=out2,
        replay_binding_path=rb_path,
        run_identity_path=messy,
    )
    assert (out1 / "run_identity.json").read_text(encoding="utf-8") == (
        out2 / "run_identity.json"
    ).read_text(encoding="utf-8")
    assert (out1 / "hashes.json").read_text(encoding="utf-8") == (out2 / "hashes.json").read_text(
        encoding="utf-8"
    )


def test_end_to_end_fixture_chain_matches_golden(tmp_path: Path) -> None:
    """M02 fixtures → M03 → M04 (synthetic replay) → M05; compare to golden snapshot."""

    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    write_json_record(rb_path, rb)

    load_validated_upstream(
        lineage_seed_path=ls_path,
        replay_binding_path=rb_path,
        run_identity_path=ri_path,
    )

    out = tmp_path / "canonical_bundle"
    write_canonical_run_artifact_bundle(
        lineage_seed_path=ls_path,
        output_dir=out,
        replay_binding_path=rb_path,
        run_identity_path=ri_path,
    )

    expected_manifest = json.loads((M05_EXPECTED / "manifest.json").read_text(encoding="utf-8"))
    expected_hashes = json.loads((M05_EXPECTED / "hashes.json").read_text(encoding="utf-8"))
    got_manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    got_hashes = json.loads((out / "hashes.json").read_text(encoding="utf-8"))
    assert got_manifest == expected_manifest
    assert got_hashes == expected_hashes

    out2 = tmp_path / "canonical_bundle_2"
    write_canonical_run_artifact_bundle(
        lineage_seed_path=ls_path,
        output_dir=out2,
        replay_binding_path=rb_path,
        run_identity_path=ri_path,
    )
    assert (out / "manifest.json").read_bytes() == (out2 / "manifest.json").read_bytes()
    assert (out / "hashes.json").read_bytes() == (out2 / "hashes.json").read_bytes()


def test_e2e_repeat_build_identical(tmp_path: Path) -> None:
    ri, ls = _m03_from_fixtures()
    rb = _m04_record(ri, ls)
    ri_path = tmp_path / "run_identity.json"
    ls_path = tmp_path / "lineage_seed.json"
    rb_path = tmp_path / "replay_binding.json"
    write_json_record(ri_path, ri)
    write_json_record(ls_path, ls)
    write_json_record(rb_path, rb)

    for name in ("c1", "c2"):
        d = tmp_path / name
        write_canonical_run_artifact_bundle(
            lineage_seed_path=ls_path,
            output_dir=d,
            replay_binding_path=rb_path,
            run_identity_path=ri_path,
        )
    t1 = (tmp_path / "c1" / "hashes.json").read_text(encoding="utf-8")
    t2 = (tmp_path / "c2" / "hashes.json").read_text(encoding="utf-8")
    assert t1 == t2
