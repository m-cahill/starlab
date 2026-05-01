"""Checkpoint → provisional action projection for V15-M52A (lazy torch; operator runner only)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def _fingerprint_state_dict(st: dict[str, Any]) -> int:
    """Deterministic small int from tensor payloads in a PyTorch state dict."""

    import torch

    acc = 5381
    for key in sorted(st.keys()):
        val = st[key]
        if torch.is_tensor(val):
            t = val.detach().cpu()
            acc = (acc * 33 + hash(key)) & 0xFFFFFFFF
            acc = (acc + int(t.numel())) & 0xFFFFFFFF
            if t.numel() > 0:
                acc = (acc + int(t.float().sum().item())) & 0xFFFFFFFF
    return acc


def load_checkpoint_state_dict(path: str, *, map_location: str) -> dict[str, Any]:
    """Load a checkpoint blob into a flat state dict (may wrap ``state_dict`` key)."""

    import torch

    blob: Any
    try:
        blob = torch.load(path, map_location=map_location, weights_only=True)
    except TypeError:
        blob = torch.load(path, map_location=map_location)
    if isinstance(blob, dict) and isinstance(blob.get("state_dict"), dict):
        inner = blob["state_dict"]
        if isinstance(inner, dict):
            return inner
    if isinstance(blob, dict):
        return blob
    raise ValueError("checkpoint_blob_not_state_dict")


def make_pick_action_index_from_state(st: dict[str, Any]) -> Callable[[int, int, int, int], int]:
    """Build ``provisional_safe_action_projection_v1`` closure (8-way vocabulary)."""

    seed = _fingerprint_state_dict(st)

    def pick_action_index(iteration: int, gl: int, minerals: int, vespene: int) -> int:
        mix = (seed + iteration * 17 + gl * 3 + minerals + vespene * 2) & 0x7FFFFFFF
        return int(mix % 8)

    return pick_action_index
