"""Map path resolution — explicit config first, then deterministic discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ResolvedMap:
    """How a .SC2Map was chosen for the harness."""

    logical_key: str
    resolution: str
    map_path: Path


def _is_playable_sc2_map(p: Path) -> bool:
    """True if ``p`` is a file map or a directory ``*.SC2Map`` bundle (common on disk)."""

    if not p.exists():
        return False
    if p.is_file():
        return p.suffix.lower() == ".sc2map"
    return p.is_dir() and p.name.lower().endswith(".sc2map")


def _stable_key_under_maps_root(maps_root: Path, map_path: Path) -> str:
    try:
        rel = map_path.resolve().relative_to(maps_root.resolve())
        return f"Maps/{rel.as_posix()}"
    except ValueError:
        return map_path.name


def discover_first_map_sorted(maps_dir: Path) -> Path:
    """Return the first `.SC2Map` in deterministic sorted order under ``maps_dir``."""

    if not maps_dir.is_dir():
        raise FileNotFoundError(f"maps directory does not exist: {maps_dir}")
    candidates: list[Path] = []
    for p in maps_dir.rglob("*.SC2Map"):
        if _is_playable_sc2_map(p):
            candidates.append(p)
    candidates.sort(key=lambda x: x.as_posix().lower())
    if not candidates:
        raise FileNotFoundError(f"no .SC2Map files found under {maps_dir}")
    return candidates[0]


def resolve_local_map_path(
    *,
    maps_root: Path | None,
    explicit_path: str | None,
    discover: bool,
) -> ResolvedMap:
    """
    Resolve a playable map path.

    - If ``explicit_path`` is set, use that path (``.SC2Map`` file or directory bundle; must exist).
    - If ``discover`` is True, pick the first sorted ``*.SC2Map`` under ``maps_root``.
    """

    if explicit_path is not None:
        # Absolute path required: python-sc2's Map passes this to CreateGame; relative
        # paths are incorrectly resolved under install Maps/ (see burnysc2 adapter).
        p = Path(explicit_path).expanduser().resolve()
        if not _is_playable_sc2_map(p):
            raise FileNotFoundError(f"configured map path not found: {p}")
        if maps_root is not None:
            key = _stable_key_under_maps_root(maps_root, p)
        else:
            key = p.name
        return ResolvedMap(logical_key=key, resolution="explicit_path", map_path=p)

    if discover:
        if maps_root is None:
            raise ValueError(
                "discover_under_maps_dir requires a resolved maps directory "
                "(STARLAB_SC2_MAPS_DIR or ROOT/Maps)",
            )
        found = discover_first_map_sorted(maps_root)
        key = _stable_key_under_maps_root(maps_root, found)
        return ResolvedMap(logical_key=key, resolution="maps_dir_discover", map_path=found)

    raise ValueError("resolve_local_map_path: nothing to resolve")
