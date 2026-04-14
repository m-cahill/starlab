"""M45 self-play / RL bootstrap (fixture stub + deterministic artifacts)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from starlab.hierarchy.hierarchical_training_models import HIERARCHICAL_TRAINING_RUN_FILENAME
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps
from starlab.training.emit_self_play_rl_bootstrap_run import main as m45_main
from starlab.training.self_play_rl_bootstrap_models import (
    EPISODE_MANIFEST_VERSION,
    SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME,
    UPDATED_BUNDLE_BASENAME,
    UPDATED_POLICY_SUBDIR,
)
from starlab.training.self_play_rl_bootstrap_pipeline import run_self_play_rl_bootstrap
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
MATCH_FAKE = REPO_ROOT / "tests" / "fixtures" / "match_fake_m02.json"


def _materialize_m14_bundle_directory(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "replay_metadata.json",
        "replay_timeline.json",
        "replay_build_order_economy.json",
        "replay_combat_scouting_visibility.json",
        "replay_slices.json",
        "replay_metadata_report.json",
        "replay_slices_report.json",
    ):
        shutil.copy(M14_FIX / name, dest / name)
    shutil.copy(
        M14_FIX / "expected_replay_bundle_manifest.json",
        dest / "replay_bundle_manifest.json",
    )
    shutil.copy(
        M14_FIX / "expected_replay_bundle_lineage.json",
        dest / "replay_bundle_lineage.json",
    )
    shutil.copy(
        M14_FIX / "expected_replay_bundle_contents.json",
        dest / "replay_bundle_contents.json",
    )


def _build_m43_run_dir(tmp_path: Path) -> tuple[Path, Path]:
    bundle = tmp_path / "b1"
    _materialize_m14_bundle_directory(bundle)
    ds = json.loads((M26_FIX / "replay_training_dataset.json").read_text(encoding="utf-8"))
    c = build_agent_training_program_contract()
    out = tmp_path / "m43_run"
    out.mkdir(parents=True, exist_ok=True)
    run, _rep, _wp = build_hierarchical_training_run(
        bundle_dirs=[bundle],
        dataset=ds,
        emit_weights=True,
        output_dir=out,
        seed=42,
        training_program_contract=c,
    )
    (out / HIERARCHICAL_TRAINING_RUN_FILENAME).write_text(
        canonical_json_dumps(run),
        encoding="utf-8",
    )
    return out, bundle


def test_m45_fixture_bootstrap_deterministic(tmp_path: Path) -> None:
    m43_dir, bundle = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m45_out"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    ds_path = M26_FIX / "replay_training_dataset.json"

    r1 = run_self_play_rl_bootstrap(
        bundle_dirs=[bundle],
        dataset_path=ds_path,
        emit_updated_bundle=True,
        episodes=1,
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        runtime_mode="fixture_stub_ci",
        seed=7,
    )
    r2 = run_self_play_rl_bootstrap(
        bundle_dirs=[bundle],
        dataset_path=ds_path,
        emit_updated_bundle=True,
        episodes=1,
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=tmp_path / "m45_out2",
        runtime_mode="fixture_stub_ci",
        seed=7,
    )
    assert r1["bootstrap_run_sha256"] == r2["bootstrap_run_sha256"]
    assert (out / SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME).is_file()
    assert (out / "self_play_rl_bootstrap_run_report.json").is_file()
    assert (out / "bootstrap_dataset.json").is_file()
    job = out / UPDATED_POLICY_SUBDIR / UPDATED_BUNDLE_BASENAME
    assert job.is_file()
    run_obj = json.loads((out / SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME).read_text(encoding="utf-8"))
    assert run_obj["bootstrap_mode"] == "single_candidate_fixture_stub"
    assert run_obj["reward_policy_id"] == "starlab.m45.reward.validation_outcome_v1"
    assert run_obj["runtime_mode"] == "fixture_stub_ci"
    assert run_obj["updated_policy_bundle"] is not None


def test_m45_cli_module_smoke(tmp_path: Path) -> None:
    m43_dir, bundle = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m45_cli"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    ds_path = M26_FIX / "replay_training_dataset.json"
    rc = m45_main(
        [
            "--hierarchical-training-run-dir",
            str(m43_dir),
            "--match-config",
            str(tmp_path / "match.json"),
            "--output-dir",
            str(out),
            "--runtime-mode",
            "fixture_stub_ci",
            "--episodes",
            "1",
            "--dataset",
            str(ds_path),
            "--bundle-dir",
            str(bundle),
            "--emit-updated-bundle",
        ],
    )
    assert rc == 0
    assert (out / SELF_PLAY_RL_BOOTSTRAP_RUN_FILENAME).is_file()


def test_m47_multi_episode_fixture_distinct_validation_identities(tmp_path: Path) -> None:
    """Per-episode match seed (base+index) yields distinct M44 validation_run_sha256 (fixture)."""

    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    out = tmp_path / "m45_multi"
    run_self_play_rl_bootstrap(
        bundle_dirs=None,
        dataset_path=None,
        emit_updated_bundle=False,
        episodes=3,
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        runtime_mode="fixture_stub_ci",
        seed=100,
    )
    man_path = out / "episodes" / "episode_manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    assert man["episode_manifest_version"] == EPISODE_MANIFEST_VERSION
    assert man["episode_seed_policy"] == "base_seed_plus_episode_index"
    assert man["bootstrap_base_seed"] == 100
    ep_rows = man["episodes"]
    assert len(ep_rows) == 3
    shas = {str(er["validation_run_sha256"]) for er in ep_rows}
    assert len(shas) == 3
    rids = {str(er["run_id"]) for er in ep_rows}
    assert len(rids) == 3
    assert ep_rows[0]["episode_seed"] == 100
    assert ep_rows[1]["episode_seed"] == 101
    assert ep_rows[2]["episode_seed"] == 102
    run_rep = json.loads((out / "self_play_rl_bootstrap_run.json").read_text(encoding="utf-8"))
    ed = run_rep["episode_distinctness"]
    assert ed["configured_episode_count"] == 3
    assert ed["distinct_validation_run_sha256_count"] == 3
    assert ed["distinct_run_id_count"] == 3
    assert not run_rep.get("warnings")


def test_m45_training_modules_do_not_import_replays_or_s2protocol() -> None:
    forbidden_substrings = ("starlab.replays", "s2protocol")
    for name in (
        "self_play_rl_bootstrap_models.py",
        "self_play_rl_bootstrap_io.py",
        "self_play_rl_bootstrap_pipeline.py",
        "emit_self_play_rl_bootstrap_run.py",
    ):
        text = (REPO_ROOT / "starlab" / "training" / name).read_text(encoding="utf-8")
        for sub in forbidden_substrings:
            assert sub not in text, f"{name} must not reference {sub}"
