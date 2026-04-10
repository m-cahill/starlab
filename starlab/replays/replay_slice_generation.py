"""Pure slice generation: M10 + M11 + M12 governed JSON → slice records + report (M13)."""

# ruff: noqa: I001
from __future__ import annotations

from starlab.replays.replay_slice_generation_envelope import generate_replay_slices_envelope
from starlab.replays.replay_slice_generation_helpers import (
    RunStatus,
    slice_identity_payload_for_hash,
)

__all__ = [
    "RunStatus",
    "generate_replay_slices_envelope",
    "slice_identity_payload_for_hash",
]
