"""One integration training step driven by rollup features from SC2 rollout summaries (V15-M27).

Not claiming learning — records an explicit integration-smoke or skipped posture.
"""

from __future__ import annotations

from typing import Any


def rollup_features_from_episodes(
    episodes: list[dict[str, Any]],
) -> list[float]:
    """Deterministic bounded feature vector for integration smoke."""

    if not episodes:
        return [0.0] * 6
    acts = [int(e.get("action_count") or 0) for e in episodes]
    obs_ct = [int(e.get("observation_count") or 0) for e in episodes]
    loops_m = []
    for e in episodes:
        gls = e.get("observed_game_loops")
        loops_m.append(int(gls) if gls is not None else 0)

    sum_a = float(sum(acts))
    mean_a = sum_a / max(len(acts), 1)
    nonempty = sum(1 for a in acts if a > 0)
    sum_obs = float(sum(obs_ct))
    max_lp = float(max(loops_m) if loops_m else 0)
    bounded = sum(
        1 for e in episodes if str(e.get("bounded_exit_reason") or "").startswith("bounded")
    )
    return [mean_a, sum_a, float(nonempty), sum_obs / max(sum_obs, 1.0), max_lp, float(bounded)]


def execute_rollout_derived_integration_training_smoke(
    features: list[float],
) -> dict[str, Any]:
    """Run a single optimizer step when PyTorch is available; else record skip."""

    if not features:
        features = [0.0]

    outcome: dict[str, Any] = {
        "kind": "integration_smoke_torch_sgd_step",
        "labeled": True,
        "features_dim": len(features),
        "not_claim": "integration_smoke_not_meaningful_learning",
    }

    try:
        import torch
        from torch import nn
    except ImportError:
        outcome["training_update_executed"] = False
        outcome["device"] = "unavailable"
        outcome["notes"] = "torch not installed"
        return outcome

    device_s = "cuda" if torch.cuda.is_available() else "cpu"
    outcome["device"] = device_s

    dtype = torch.float32
    x = torch.tensor([features], dtype=dtype, device=torch.device(device_s))
    target_scalar = (
        torch.abs(x[:, :1]).sum(dim=1, keepdim=True) * 0.01 + 0.5
    )  # depends on rollout features only

    model = nn.Linear(len(features), 1).to(dtype=dtype, device=device_s)
    model.train()

    lr = 1e-1
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    with torch.no_grad():
        y0 = model(x)
        loss_before = criterion(y0, target_scalar).detach().cpu().item()
    optimizer.zero_grad()
    y_pred = model(x)
    loss = criterion(y_pred, target_scalar)
    loss.backward()
    optimizer.step()

    optimizer.zero_grad()
    with torch.no_grad():
        y1 = model(x)
        loss_after = criterion(y1, target_scalar).detach().cpu().item()

    outcome.update(
        {
            "training_update_executed": True,
            "loss_before_first_step": float(loss_before),
            "loss_after_one_step": float(loss_after),
            "lr": float(lr),
        },
    )
    return outcome
