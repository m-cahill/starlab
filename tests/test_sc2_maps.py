"""Map resolution helpers."""

from __future__ import annotations

from pathlib import Path

from starlab.sc2.maps import discover_first_map_sorted, resolve_local_map_path


def test_discover_sorted_order(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "m1.SC2Map").write_bytes(b"x")
    (tmp_path / "b" / "m2.SC2Map").write_bytes(b"y")
    first = discover_first_map_sorted(tmp_path)
    assert first.name == "m1.SC2Map"


def test_explicit_path_key(tmp_path: Path) -> None:
    maps_root = tmp_path / "Maps"
    maps_root.mkdir()
    mp = maps_root / "Tut" / "Hello.SC2Map"
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_bytes(b"z")
    r = resolve_local_map_path(maps_root=maps_root, explicit_path=str(mp), discover=False)
    assert "Hello.SC2Map" in r.logical_key
    assert r.resolution == "explicit_path"
