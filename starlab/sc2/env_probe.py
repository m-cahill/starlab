"""SC2 environment probe — path detection only; does not run matches or load SC2 libs."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from starlab.sc2.models import InterfaceModeSupport, Sc2ProbeResult, Sc2RuntimeSpec

_ENV_ROOT = "STARLAB_SC2_ROOT"
_ENV_BIN = "STARLAB_SC2_BIN"
_ENV_MAPS = "STARLAB_SC2_MAPS_DIR"
_ENV_REPLAYS = "STARLAB_SC2_REPLAYS_DIR"
_ENV_BASE_BUILD = "STARLAB_SC2_BASE_BUILD"
_ENV_DATA_VERSION = "STARLAB_SC2_DATA_VERSION"


def redact_path_str(path: str, *, home: Path | None = None) -> str:
    """Replace absolute home prefix with ``~`` for milestone artifacts (POSIX-style tail)."""

    home = home if home is not None else Path.home()
    try:
        p = Path(path).expanduser()
        resolved = p.resolve()
        home_res = home.resolve()
        try:
            rel = resolved.relative_to(home_res)
        except ValueError:
            return path.replace("\\", "/")
        return str(Path("~") / rel).replace("\\", "/")
    except OSError:
        return path.replace("\\", "/")


def normalize_path_str(path: str | None) -> str | None:
    """Return absolute normalized path string, or None if input is None/empty."""

    if path is None:
        return None
    stripped = path.strip()
    if not stripped:
        return None
    p = Path(stripped).expanduser()
    try:
        return str(p.resolve(strict=False))
    except OSError:
        return str(p)


def _find_binary_under_root(root: Path) -> Path | None:
    direct = [
        root / "SC2_x64.exe",
        root / "SC2.exe",
        root / "SC2",
    ]
    for c in direct:
        if c.is_file():
            return c
    versions = root / "Versions"
    if not versions.is_dir():
        return None
    for sub in sorted(versions.iterdir()):
        if not sub.is_dir():
            continue
        for name in ("SC2_x64.exe", "SC2.exe", "SC2"):
            candidate = sub / name
            if candidate.is_file():
                return candidate
    return None


def _derive_maps_dir(root: Path | None) -> str | None:
    if root is None:
        return None
    maps_dir = root / "Maps"
    return str(maps_dir.resolve(strict=False))


def _derive_replays_dir(root: Path | None) -> str | None:
    if root is None:
        return None
    replays_dir = root / "Replays"
    return str(replays_dir.resolve(strict=False))


def _read_env_paths() -> Mapping[str, str | None]:
    """Env var precedence: explicit BIN/MAPS/REPLAYS override; else derive from ROOT."""

    raw_root = os.environ.get(_ENV_ROOT)
    raw_bin = os.environ.get(_ENV_BIN)
    raw_maps = os.environ.get(_ENV_MAPS)
    raw_replays = os.environ.get(_ENV_REPLAYS)

    root_norm = normalize_path_str(raw_root)
    root_path = Path(root_norm) if root_norm is not None else None

    bin_norm = normalize_path_str(raw_bin)
    if bin_norm is None and root_path is not None:
        found = _find_binary_under_root(root_path)
        if found is not None:
            bin_norm = str(found.resolve(strict=False))

    maps_norm = normalize_path_str(raw_maps)
    if maps_norm is None:
        maps_norm = _derive_maps_dir(root_path)

    replays_norm = normalize_path_str(raw_replays)
    if replays_norm is None:
        replays_norm = _derive_replays_dir(root_path)

    return {
        "binary": bin_norm,
        "maps_dir": maps_norm,
        "replays_dir": replays_norm,
        "root": root_norm,
    }


def _read_version_hints() -> tuple[str | None, str | None]:
    base = os.environ.get(_ENV_BASE_BUILD)
    data = os.environ.get(_ENV_DATA_VERSION)
    b = base.strip() if base and base.strip() else None
    d = data.strip() if data and data.strip() else None
    return b, d


def _presence(paths: Mapping[str, str | None]) -> dict[str, bool]:
    out: dict[str, bool] = {}
    for key in sorted(paths):
        p = paths[key]
        if p is None:
            out[key] = False
        else:
            out[key] = Path(p).is_file() if key == "binary" else Path(p).is_dir()
    return out


def run_probe() -> Sc2ProbeResult:
    """Collect configured paths and presence flags without invoking SC2."""

    paths = _read_env_paths()
    base_build, data_version = _read_version_hints()
    present = _presence(paths)

    notes: list[str] = []
    if paths["root"] is None and paths["binary"] is None:
        notes.append("STARLAB_SC2_ROOT and STARLAB_SC2_BIN unset; no install path detected.")
    elif paths["binary"] is not None and not present["binary"]:
        notes.append("Binary path configured but file not found.")
    elif paths["root"] is not None and paths["binary"] is None:
        notes.append("STARLAB_SC2_ROOT set but no known binary layout found under root.")

    return Sc2ProbeResult(
        spec=Sc2RuntimeSpec(),
        interface_modes=InterfaceModeSupport(),
        paths=dict(paths),
        present=present,
        base_build=base_build,
        data_version=data_version,
        notes=tuple(sorted(notes)),
    )


def probe_result_to_mapping(result: Sc2ProbeResult, *, redact: bool = False) -> dict[str, Any]:
    """Convert a probe result to a JSON-serializable dict (sorted keys for determinism)."""

    def _sort_dict(d: dict[str, Any]) -> dict[str, Any]:
        return {k: _sort_value(v) for k, v in sorted(d.items())}

    def _sort_value(v: Any) -> Any:
        if isinstance(v, dict):
            return _sort_dict(v)
        if isinstance(v, list):
            return [_sort_value(x) for x in v]
        return v

    paths_out: dict[str, str | None] = {}
    for key in sorted(result.paths):
        val = result.paths[key]
        if redact and val is not None:
            paths_out[key] = redact_path_str(val)
        else:
            paths_out[key] = val

    present_sorted = {k: result.present[k] for k in sorted(result.present)}

    payload: dict[str, Any] = {
        "base_build": result.base_build,
        "data_version": result.data_version,
        "interface_modes": {
            "feature_layer_interface": result.interface_modes.feature_layer_interface,
            "raw_interface": result.interface_modes.raw_interface,
            "rendered_interface": result.interface_modes.rendered_interface,
        },
        "notes": sorted(result.notes),
        "paths": paths_out,
        "present": present_sorted,
        "spec": {
            "control_observation_surface": result.spec.control_observation_surface,
            "replay_decode_surface": result.spec.replay_decode_surface,
        },
    }
    return _sort_dict(payload)


def probe_result_to_json(result: Sc2ProbeResult, *, redact: bool = False) -> str:
    """Serialize probe result to deterministic JSON (sorted keys, trailing newline)."""

    mapping = probe_result_to_mapping(result, redact=redact)
    return json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="STARLAB SC2 environment probe (M01). Output is always deterministic JSON.",
    )
    parser.add_argument(
        "--redact",
        action="store_true",
        help="Redact user-specific absolute path prefixes in JSON output.",
    )
    args = parser.parse_args(argv)

    result = run_probe()
    print(probe_result_to_json(result, redact=args.redact), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
