"""Bounded PyTorch updates conditioned on SC2 rollout feature vectors (V15-M28).

Does **not** claim meaningful policy improvement — wiring / receipts only.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from starlab.hierarchy.hierarchical_training_io import sha256_hex_file
from starlab.v15.sc2_backed_t1_candidate_training_models import TRAINING_CONDITION_LABEL


def _apply_checkpoint_retention(
    entries: list[dict[str, Any]],
    max_retained: int | None,
) -> tuple[list[dict[str, Any]], int]:
    """Enforce an on-disk checkpoint cap while preserving boundary checkpoints.

    When *max_retained* is 1, only the newest checkpoint (highest *training_step*) is kept.
    When *max_retained* >= 2, the lowest and highest *training_step* are protected; oldest
    intermediates are deleted first until the cap is satisfied.
    Returns ``(retained_entries, pruned_count)``.
    """

    if max_retained is None or len(entries) <= max_retained:
        return entries, 0
    cap = max(1, int(max_retained))
    pruned = 0
    work = sorted(entries, key=lambda e: int(e["training_step"]))
    while len(work) > cap:
        if cap == 1:
            idx = 0
        elif len(work) <= 2:
            break
        else:
            idx = 1
        victim = work.pop(idx)
        try:
            Path(str(victim["path"])).unlink(missing_ok=True)
        except OSError:
            pass
        pruned += 1
    return work, pruned


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
    disable_loss_floor_early_stop: bool = False,
    require_full_wall_clock: bool = False,
    max_retained_checkpoints: int | None = None,
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
        "disable_loss_floor_early_stop": disable_loss_floor_early_stop,
        "require_full_wall_clock_training": bool(require_full_wall_clock),
        # checkpoint_retention: bounded on-disk volume (M38 / M39 launch safety)
        "checkpoint_retention_max_retained": max_retained_checkpoints,
        "checkpoints_written_total": 0,
        "checkpoints_pruned_total": 0,
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

    # Full-horizon mode: iterate until wall_budget_seconds elapses unless a safety ceiling
    # is hit — default M28 budgets use max_updates as the tighter bound.
    if require_full_wall_clock:
        effective_cap = max(10**9, int(max_updates))
    else:
        effective_cap = int(max_updates)

    for step in range(effective_cap):
        elapsed = time.monotonic() - t0
        if elapsed >= wall_budget_seconds:
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
            out["checkpoints_written_total"] = int(out["checkpoints_written_total"]) + 1
            out["checkpoint_count"] = int(out["checkpoint_count"]) + 1
            cp_sha = sha256_hex_file(ck_path)
            out["checkpoint_paths_with_sha256"].append(
                {"path": str(ck_path.resolve()), "sha256": cp_sha, "training_step": n_updates},
            )
            retained, pr = _apply_checkpoint_retention(
                list(out["checkpoint_paths_with_sha256"]),
                max_retained_checkpoints,
            )
            out["checkpoint_paths_with_sha256"] = retained
            out["checkpoints_pruned_total"] = int(out["checkpoints_pruned_total"]) + pr
            out["checkpoint_count"] = len(retained)

        skip_loss_floor = bool(disable_loss_floor_early_stop) or bool(require_full_wall_clock)
        if (not skip_loss_floor) and n_updates >= min_updates and loss_tail < 1e-12:
            # Extremely unlikely — kept for symmetry / deterministic convergence probes.
            out["early_stop_reason"] = "loss_floor_not_claim_learning"
            break

    out["loss_tail"] = loss_tail

    # Final-step checkpoint when the last update is not already persisted at cadence.
    final_n = int(out["training_update_count"])
    cps: list[dict[str, Any]] = list(out["checkpoint_paths_with_sha256"])
    last_saved_step = int(cps[-1]["training_step"]) if cps else -1
    if final_n > 0 and last_saved_step != final_n and out.get("failure_reason") is None:
        ck_path = checkpoint_dir / f"candidate_checkpoint_step_{final_n}_final.pt"
        torch.save({"model_state_dict": model.state_dict()}, ck_path)
        out["checkpoints_written_total"] = int(out["checkpoints_written_total"]) + 1
        cp_sha = sha256_hex_file(ck_path)
        cps.append(
            {"path": str(ck_path.resolve()), "sha256": cp_sha, "training_step": final_n},
        )
        retained, pr = _apply_checkpoint_retention(cps, max_retained_checkpoints)
        out["checkpoint_paths_with_sha256"] = retained
        out["checkpoints_pruned_total"] = int(out["checkpoints_pruned_total"]) + pr
        out["checkpoint_count"] = len(retained)

    out["wall_clock_seconds_observed"] = round(time.monotonic() - t0, 3)

    if out["training_update_count"] < min_updates:
        out["failure_reason"] = out["failure_reason"] or "stopped_before_min_training_updates"

    return out
