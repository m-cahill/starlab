"""Tests for SC2 path probe — fixtures only; no real SC2 required."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from starlab.sc2.env_probe import (
    normalize_path_str,
    probe_result_to_json,
    redact_path_str,
    run_probe,
)


@pytest.mark.smoke
def test_probe_json_is_deterministic(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("STARLAB_SC2_ROOT", raising=False)
    monkeypatch.delenv("STARLAB_SC2_BIN", raising=False)
    monkeypatch.delenv("STARLAB_SC2_MAPS_DIR", raising=False)
    monkeypatch.delenv("STARLAB_SC2_REPLAYS_DIR", raising=False)
    monkeypatch.delenv("STARLAB_SC2_BASE_BUILD", raising=False)
    monkeypatch.delenv("STARLAB_SC2_DATA_VERSION", raising=False)

    a = probe_result_to_json(run_probe())
    b = probe_result_to_json(run_probe())
    assert a == b
    json.loads(a)  # valid JSON


@pytest.mark.smoke
def test_env_precedence_binary_over_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "sc2"
    root.mkdir()
    versions = root / "Versions" / "base123"
    versions.mkdir(parents=True)
    derived_bin = versions / "SC2_x64.exe"
    derived_bin.write_bytes(b"\x00")

    explicit = tmp_path / "explicit.exe"
    explicit.write_bytes(b"\x00")

    monkeypatch.setenv("STARLAB_SC2_ROOT", str(root))
    monkeypatch.setenv("STARLAB_SC2_BIN", str(explicit))
    monkeypatch.delenv("STARLAB_SC2_MAPS_DIR", raising=False)
    monkeypatch.delenv("STARLAB_SC2_REPLAYS_DIR", raising=False)

    result = run_probe()
    assert result.paths["binary"] == str(explicit.resolve())
    assert result.present["binary"] is True


def test_root_derives_maps_and_replays(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "sc2"
    maps = root / "Maps"
    replays = root / "Replays"
    maps.mkdir(parents=True)
    replays.mkdir(parents=True)

    monkeypatch.setenv("STARLAB_SC2_ROOT", str(root))
    monkeypatch.delenv("STARLAB_SC2_BIN", raising=False)
    monkeypatch.delenv("STARLAB_SC2_MAPS_DIR", raising=False)
    monkeypatch.delenv("STARLAB_SC2_REPLAYS_DIR", raising=False)

    result = run_probe()
    assert result.paths["maps_dir"] == str(maps.resolve())
    assert result.paths["replays_dir"] == str(replays.resolve())
    assert result.present["maps_dir"] is True
    assert result.present["replays_dir"] is True


def test_partial_config_missing_binary_notes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    monkeypatch.setenv("STARLAB_SC2_ROOT", str(root))
    monkeypatch.delenv("STARLAB_SC2_BIN", raising=False)
    monkeypatch.delenv("STARLAB_SC2_MAPS_DIR", raising=False)
    monkeypatch.delenv("STARLAB_SC2_REPLAYS_DIR", raising=False)

    result = run_probe()
    assert result.present["binary"] is False
    assert any("no known binary layout" in n for n in result.notes)


def test_version_hints_from_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("STARLAB_SC2_ROOT", raising=False)
    monkeypatch.delenv("STARLAB_SC2_BIN", raising=False)
    monkeypatch.setenv("STARLAB_SC2_BASE_BUILD", " 12345 ")
    monkeypatch.setenv("STARLAB_SC2_DATA_VERSION", "abc")

    result = run_probe()
    assert result.base_build == "12345"
    assert result.data_version == "abc"


def test_redact_mode_changes_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    explicit = tmp_path / "explicit.exe"
    explicit.write_bytes(b"\x00")
    monkeypatch.setenv("STARLAB_SC2_BIN", str(explicit))
    monkeypatch.delenv("STARLAB_SC2_ROOT", raising=False)

    plain = json.loads(probe_result_to_json(run_probe(), redact=False))
    red = json.loads(probe_result_to_json(run_probe(), redact=True))

    assert isinstance(plain["paths"]["binary"], str)
    assert isinstance(red["paths"]["binary"], str)
    try:
        explicit.resolve().relative_to(Path.home().resolve())
    except ValueError:
        return
    assert red["paths"]["binary"].startswith("~")


def test_normalize_path_str_empty() -> None:
    assert normalize_path_str(None) is None
    assert normalize_path_str("   ") is None


def test_redact_path_str_no_crash() -> None:
    assert isinstance(redact_path_str(str(Path.home() / "x")), str)
