"""Bounded PyTorch updates conditioned on SC2 rollout feature vectors (V15-M28).

Does **not** claim meaningful policy improvement — wiring / receipts only.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.v15.sc2_backed_t1_candidate_training_models import TRAINING_CONDITION_LABEL


def _pick_device(device_pref: str) -> tuple[Any, str]:
    """Return (torch.device, device_label_str)."""

    try:
        import torch
    except ImportError:
        return None, "torch_missing"

    if device_pref == "cuda":
        if torch.cuda.is_available():
            return torch.device("cuda:0"), "cuda"
        return None, "cuda_unavailable"
    if device_pref == "cpu":
        return torch.device("cpu"), "cpu"
    # auto
    if torch.cuda.is_available():
        return torch.device("cuda:0"), "cuda"
    return torch.device("cpu"), "cpu"


def run_bounded_rollout_feature_training(
    features: list[float],
    *,
    min_updates: int,
    max_updates: int,
    checkpoint_cadence: int,
    checkpoint_dir: Path,
    wall_budget_seconds: float,
    seed: int,
    device_pref: str,
) -> dict[str, Any]:
    """Train a tiny network using rollout-derived features as batch input.

    Target scalar depends only on the SC2-derived feature tensor — ties receipts to rollout stats.

    Returns structured telemetry dict including checkpoints saved at cadence.
    """

    out: dict[str, Any] = {
        "training_condition_label": TRAINING_CONDITION_LABEL,
        "features_dim": len(features),
        "checkpoint_paths_with_sha256": [],
        "training_update_executed": False,
        "training_update_count": 0,
        "checkpoint_count": 0,
        "early_stop_reason": None,
        "wall_clock_seconds_observed": 0.0,
        "device": None,
        "failure_reason": None,
        "loss_tail": None,
    }

    try:
        import torch
        from torch import nn
    except ImportError as exc:
        out["failure_reason"] = f"torch_import_failed:{exc}"
        return out

    device, dev_label = _pick_device(device_pref)
    out["device"] = dev_label
    if device is None:
        out["failure_reason"] = dev_label
        return out

    torch.manual_seed(int(seed))

    dtype = torch.float32
    feat_tensor = torch.tensor([features], dtype=dtype, device=device)
    # Target anchored on rollout features — deterministic given feat_tensor.
    target_scalar = torch.mean(torch.abs(feat_tensor), dim=1, keepdim=True) * 0.001 + 0.42

    hid = max(8, min(64, len(features) * 2))
    model = nn.Sequential(
        nn.Linear(len(features), hid),
        nn.Tanh(),
        nn.Linear(hid, 1),
    ).to(device=device, dtype=dtype)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    loss_tail = None

    for step in range(max_updates):
        if time.monotonic() - t0 > wall_budget_seconds:
            out["early_stop_reason"] = "wall_clock_budget"
            break

        model.train()
        optimizer.zero_grad()
        pred = model(feat_tensor)
        loss = criterion(pred, target_scalar)
        loss.backward()
        optimizer.step()

        loss_tail = float(loss.detach().cpu().item())
        out["training_update_executed"] = True
        n_updates = step + 1
        out["training_update_count"] = n_updates

        at_boundary = n_updates % int(checkpoint_cadence) == 0 and n_updates > 0
        if at_boundary:
            ck_path = checkpoint_dir / f"candidate_checkpoint_step_{n_updates}.pt"
            torch.save({"model_state_dict": model.state_dict()}, ck_path)
            out["checkpoint_count"] = int(out["checkpoint_count"]) + 1
            cp_sha = sha256_hex_file(ck_path)
            out["checkpoint_paths_with_sha256"].append(
                {"path": str(ck_path.resolve()), "sha256": cp_sha, "training_step": n_updates},
            )

        if n_updates >= min_updates and loss_tail < 1e-12:
            # Extremely unlikely — kept for symmetry / deterministic convergence probes.
            out["early_stop_reason"] = "loss_floor_not_claim_learning"
            break

    out["wall_clock_seconds_observed"] = round(time.monotonic() - t0, 3)
    out["loss_tail"] = loss_tail

    if out["training_update_count"] < min_updates:
        out["failure_reason"] = out["failure_reason"] or "stopped_before_min_training_updates"

    return out
