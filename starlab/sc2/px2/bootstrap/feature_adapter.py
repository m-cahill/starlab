"""M18-anchored bounded feature projection for PX2-M02 bootstrap models."""

from __future__ import annotations

from typing import Any, Final

import torch

from starlab.observation.observation_surface_catalog import ORDERED_SCALAR_FEATURE_NAMES

FEATURE_ADAPTER_PROFILE: Final[str] = "starlab.px2.bootstrap.feature_adapter.m18_flat_v1"

# resource_signal_category / race.actual / visibility / result.known
_RESOURCE_CAT_INDEX: Final[dict[str, int]] = {
    "low": 0,
    "medium": 1,
    "high": 2,
}
_RACE_INDEX: Final[dict[str, int]] = {
    "Terran": 0,
    "Protoss": 1,
    "Zerg": 2,
}
_VISIBILITY_INDEX: Final[dict[str, int]] = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "full": 3,
}
_RESULT_INDEX: Final[dict[str, int]] = {
    "unknown": 0,
    "win": 1,
    "loss": 2,
    "tie": 3,
}


def _scalar_map(name: str, value: Any) -> float:
    if name == "economy.resource_signal_category":
        if value is None:
            return 0.0
        return float(_RESOURCE_CAT_INDEX.get(str(value), 0))
    if name == "race.actual":
        return float(_RACE_INDEX.get(str(value), 0))
    if name == "visibility.proxy_level":
        return float(_VISIBILITY_INDEX.get(str(value), 0))
    if name == "result.known":
        return float(_RESULT_INDEX.get(str(value), 0))
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value) / 128.0
    return 0.0


def observation_dict_to_feature_tensor(observation_surface: dict[str, Any]) -> torch.Tensor:
    """Flatten governed M18/M17 observation frame into a fixed float32 vector.

    Uses ``scalar_features.ordered_entries`` (aligned to ``ORDERED_SCALAR_FEATURE_NAMES``),
    ``entity_rows`` row aggregates, and a coarse ``spatial_plane_family`` summary when present.
    """

    scalars: dict[str, Any] = {}
    sf = observation_surface.get("scalar_features")
    if isinstance(sf, dict):
        entries = sf.get("ordered_entries")
        if isinstance(entries, list):
            for ent in entries:
                if not isinstance(ent, dict):
                    continue
                n = ent.get("name")
                if isinstance(n, str):
                    scalars[n] = ent.get("value")

    vec: list[float] = []
    for name in ORDERED_SCALAR_FEATURE_NAMES:
        vec.append(_scalar_map(name, scalars.get(name)))

    er = observation_surface.get("entity_rows")
    row_count = 0.0
    if isinstance(er, dict):
        rows = er.get("rows")
        if isinstance(rows, list):
            row_count = float(len(rows)) / 32.0
            for row in rows[:16]:
                if not isinstance(row, dict):
                    continue
                c = row.get("count")
                vec.append(float(c) / 64.0 if isinstance(c, (int, float)) else 0.0)
    vec.append(row_count)

    while len(vec) < 32:
        vec.append(0.0)

    sp = observation_surface.get("spatial_plane_family")
    if isinstance(sp, dict):
        planes = sp.get("planes")
        if isinstance(planes, list) and planes:
            plane0 = planes[0]
            if isinstance(plane0, dict):
                gw = plane0.get("grid_width", 8)
                gh = plane0.get("grid_height", 8)
                ch = plane0.get("channel_count", 1)
                vec.append(float(gw) / 256.0)
                vec.append(float(gh) / 256.0)
                vec.append(float(ch) / 16.0)

    feat = torch.tensor(vec, dtype=torch.float32)
    return feat


def observation_feature_dim() -> int:
    """Return static dim used by ``BootstrapTerranPolicy`` (padded/truncated inside model)."""

    return 128


def pad_or_trunc(v: torch.Tensor, dim: int) -> torch.Tensor:
    if v.numel() >= dim:
        return v[:dim]
    out = torch.zeros(dim, dtype=torch.float32)
    out[: v.numel()] = v
    return out
