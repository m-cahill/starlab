"""Load `BootstrapTerranPolicy` weights for operator-local PX2-M03 slice 3."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Final

import torch

from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy

WEIGHT_MODE_INIT_ONLY: Final[str] = "init_only"
WEIGHT_MODE_WEIGHTS_FILE: Final[str] = "weights_file"


def sha256_hex_file(path: Path) -> str:
    """SHA-256 (hex) over raw file bytes."""

    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_policy_from_weights_file(
    *,
    weights_path: Path,
    map_location: str | torch.device = "cpu",
) -> BootstrapTerranPolicy:
    """Load ``BootstrapTerranPolicy`` from a ``torch.save`` state_dict file."""

    device = map_location if isinstance(map_location, torch.device) else torch.device(map_location)
    raw: Any = torch.load(weights_path, map_location=device, weights_only=True)
    if not isinstance(raw, dict):
        msg = "weights file must contain a torch state_dict (dict)"
        raise ValueError(msg)
    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    model.load_state_dict(raw)
    model.eval()
    return model


def build_policy_operator_local(
    *,
    init_only: bool,
    weights_path: Path | None,
    torch_seed: int,
    map_location: str | torch.device = "cpu",
) -> tuple[BootstrapTerranPolicy, dict[str, Any]]:
    """Return policy + weight-identity metadata for receipts.

    ``init_only=True``: fresh deterministic init (``torch.manual_seed``); ``weights_path`` must be
    ``None``. ``init_only=False``: load ``weights_path``; file must exist and load as state_dict.
    """

    if init_only:
        if weights_path is not None:
            msg = "weights_path must be None when init_only=True"
            raise ValueError(msg)
        torch.manual_seed(torch_seed)
        model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
        meta: dict[str, Any] = {
            "weight_mode": WEIGHT_MODE_INIT_ONLY,
            "weights_file_sha256": None,
            "weights_path_note": None,
        }
        return model, meta

    if weights_path is None:
        msg = "weights_path is required when init_only=False"
        raise ValueError(msg)
    resolved = weights_path.resolve()
    file_hash = sha256_hex_file(resolved)
    model = load_policy_from_weights_file(weights_path=resolved, map_location=map_location)
    meta = {
        "weight_mode": WEIGHT_MODE_WEIGHTS_FILE,
        "weights_file_sha256": file_hash,
        "weights_path_note": resolved.as_posix(),
    }
    return model, meta
