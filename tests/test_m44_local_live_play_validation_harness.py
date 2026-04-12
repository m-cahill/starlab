"""M44 local live-play validation harness (fixture stub path)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from starlab.hierarchy.hierarchical_training_models import (
    HIERARCHICAL_TRAINING_RUN_FILENAME,
)
from starlab.hierarchy.hierarchical_training_pipeline import build_hierarchical_training_run
from starlab.runs.json_util import canonical_json_dumps
from starlab.runs.replay_binding import load_replay_binding
from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation
from starlab.training.training_program_io import build_agent_training_program_contract

REPO_ROOT = Path(__file__).resolve().parents[1]
M14_FIX = REPO_ROOT / "tests" / "fixtures" / "m14"
M26_FIX = REPO_ROOT / "tests" / "fixtures" / "m26"
MATCH_FAKE = REPO_ROOT / "tests" / "fixtures" / "match_fake_m02.json"

M44_SC2_MODULES = (
    "local_live_play_validation_models.py",
    "local_live_play_validation_io.py",
    "local_live_play_validation_harness.py",
    "emit_local_live_play_validation_run.py",
    "semantic_live_action_adapter.py",
)


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


def _build_m43_run_dir(tmp_path: Path) -> Path:
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
    return out


def test_m44_fixture_stub_emits_validation_and_binding(tmp_path: Path) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m44_out"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")

    r1 = run_local_live_play_validation(
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        runtime_mode="fixture_stub_ci",
    )
    assert (out / "local_live_play_validation_run.json").is_file()
    assert (out / "local_live_play_validation_run_report.json").is_file()
    assert (out / "replay_binding.json").is_file()
    assert (out / "replay" / "validation.SC2Replay").is_file()
    load_replay_binding(out / "replay_binding.json")

    r2 = run_local_live_play_validation(
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=tmp_path / "m44_out2",
        runtime_mode="fixture_stub_ci",
    )
    assert r1.validation_run["validation_run_sha256"] == r2.validation_run["validation_run_sha256"]


def test_m44_optional_video_metadata(tmp_path: Path) -> None:
    m43_dir = _build_m43_run_dir(tmp_path)
    out = tmp_path / "m44_vid"
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    vid = tmp_path / "clip.mp4"
    vid.write_bytes(b"fake-video-bytes-for-metadata-only")

    run_local_live_play_validation(
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        optional_video_path=vid,
        output_dir=out,
        runtime_mode="fixture_stub_ci",
    )
    run_obj = json.loads((out / "local_live_play_validation_run.json").read_text(encoding="utf-8"))
    media = run_obj.get("optional_media_registration")
    assert isinstance(media, dict)
    assert media.get("sha256")
    assert media.get("size_bytes") == len(b"fake-video-bytes-for-metadata-only")
    assert media.get("format") == "mp4"


def test_m44_sc2_modules_do_not_import_replays_or_s2protocol() -> None:
    forbidden_substrings = ("starlab.replays", "s2protocol")
    for module in M44_SC2_MODULES:
        text = (REPO_ROOT / "starlab" / "sc2" / module).read_text(encoding="utf-8")
        for sub in forbidden_substrings:
            assert sub not in text, f"{module} must not reference {sub}"
