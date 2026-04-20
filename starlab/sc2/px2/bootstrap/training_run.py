"""Local-first training helpers (fixture-sized batches for CI) — PX2-M02."""

from __future__ import annotations

from typing import Any

import torch

from starlab.sc2.px2.bootstrap.feature_adapter import (
    observation_dict_to_feature_tensor,
    observation_feature_dim,
    pad_or_trunc,
)
from starlab.sc2.px2.bootstrap.policy_model import (
    INDEX_BY_ACTION_ID,
    PRODUCER_INDEX,
    BootstrapTerranPolicy,
    training_loss,
)


def _feature_tensor(ex: dict[str, Any]) -> torch.Tensor:
    fv = ex.get("feature_vector")
    if isinstance(fv, list) and fv:
        return pad_or_trunc(torch.tensor(fv, dtype=torch.float32), observation_feature_dim())
    obs = ex.get("observation_surface")
    if isinstance(obs, dict):
        return pad_or_trunc(observation_dict_to_feature_tensor(obs), observation_feature_dim())
    msg = "example needs feature_vector or observation_surface"
    raise ValueError(msg)


def _arg_masks(action_id: str) -> tuple[bool, bool, bool, bool]:
    need_build = action_id in {
        "build_supply_depot",
        "build_barracks",
        "build_factory",
        "build_starport",
        "build_engineering_bay",
    }
    need_exp = action_id in {"build_refinery", "expand_command_center"}
    need_region = action_id in {
        "scout_to_region",
        "recheck_last_seen_region",
        "army_move_region",
        "army_attack_move_region",
        "army_regroup_region",
        "army_retreat_region",
        "cleanup_search_region",
    }
    need_prod = action_id in {
        "train_marine",
        "train_marauder",
        "train_siege_tank",
        "train_medivac",
        "train_viking",
        "produce_scv",
    }
    return need_build, need_exp, need_region, need_prod


def _indices_from_label(
    action_id: str,
    args: dict[str, Any],
) -> tuple[int | None, int | None, int | None, int]:
    bs = int(args["build_slot"]) if "build_slot" in args else None
    es = int(args["expansion_slot"]) if "expansion_slot" in args else None
    rs = int(args["region_slot"]) if "region_slot" in args else None
    pk = str(args.get("producer_key", "barracks_0"))
    pi = int(PRODUCER_INDEX.get(pk, 0))
    return bs, es, rs, pi


def build_batch_tensors(
    examples: list[dict[str, Any]],
    *,
    device: torch.device | None = None,
) -> tuple[dict[str, torch.Tensor], dict[str, torch.Tensor]]:
    """Stack tensors + masks for :func:`training_loss`."""

    dev = device or torch.device("cpu")
    feats = torch.stack([_feature_tensor(ex) for ex in examples], dim=0).to(dev)
    action_idx = []
    t_bs: list[int] = []
    t_es: list[int] = []
    t_rs: list[int] = []
    t_pi: list[int] = []
    nb = []
    ne = []
    nr = []
    np_ = []

    for ex in examples:
        lab = ex["label"]
        aid = str(lab["action_id"])
        args = dict(lab.get("arguments", {}))
        action_idx.append(INDEX_BY_ACTION_ID[aid])
        need_build, need_exp, need_region, need_prod = _arg_masks(aid)
        bsv, esv, rsv, piv = _indices_from_label(aid, args)
        nb.append(1.0 if need_build and bsv is not None else 0.0)
        ne.append(1.0 if need_exp and esv is not None else 0.0)
        nr.append(1.0 if need_region and rsv is not None else 0.0)
        np_.append(1.0 if need_prod else 0.0)
        t_bs.append(bsv if bsv is not None else 0)
        t_es.append(esv if esv is not None else 0)
        t_rs.append(rsv if rsv is not None else 0)
        t_pi.append(piv)

    batch: dict[str, torch.Tensor] = {
        "action_index": torch.tensor(action_idx, dtype=torch.long, device=dev),
        "true_build_slot": torch.tensor(t_bs, dtype=torch.long, device=dev),
        "true_expansion_slot": torch.tensor(t_es, dtype=torch.long, device=dev),
        "true_region_slot": torch.tensor(t_rs, dtype=torch.long, device=dev),
        "true_producer_index": torch.tensor(t_pi, dtype=torch.long, device=dev),
        "need_build": torch.tensor(nb, dtype=torch.float32, device=dev),
        "need_exp": torch.tensor(ne, dtype=torch.float32, device=dev),
        "need_region": torch.tensor(nr, dtype=torch.float32, device=dev),
        "need_prod": torch.tensor(np_, dtype=torch.float32, device=dev),
    }
    return batch, {"features": feats}


def run_bootstrap_training_step(
    model: BootstrapTerranPolicy,
    optimizer: torch.optim.Optimizer,
    examples: list[dict[str, Any]],
    *,
    device: torch.device | None = None,
) -> float:
    """Single gradient step over a (small) batch."""

    dev = device or torch.device("cpu")
    model.train()
    batch, tens = build_batch_tensors(examples, device=dev)
    out = model(tens["features"])
    loss = training_loss(
        out,
        action_index=batch["action_index"],
        true_build_slot=batch["true_build_slot"],
        true_expansion_slot=batch["true_expansion_slot"],
        true_region_slot=batch["true_region_slot"],
        true_producer_index=batch["true_producer_index"],
        need_build=batch["need_build"],
        need_exp=batch["need_exp"],
        need_region=batch["need_region"],
        need_prod=batch["need_prod"],
    )
    optimizer.zero_grad()
    loss.backward()  # type: ignore[no-untyped-call]
    optimizer.step()
    return float(loss.item())


def train_bootstrap_epochs(
    model: BootstrapTerranPolicy,
    train_ex: list[dict[str, Any]],
    *,
    epochs: int = 30,
    lr: float = 0.05,
    device: torch.device | None = None,
) -> None:
    """Fit on tiny fixture data (memorization smoke — not a strength claim)."""

    dev = device or torch.device("cpu")
    model.to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(epochs):
        _ = run_bootstrap_training_step(model, opt, train_ex, device=dev)


def action_only_accuracy(
    model: BootstrapTerranPolicy,
    examples: list[dict[str, Any]],
    device: torch.device | None = None,
) -> float:
    """Argmax action match rate (without legality masking)."""

    dev = device or torch.device("cpu")
    model.eval()
    correct = 0
    with torch.no_grad():
        for ex in examples:
            feats = _feature_tensor(ex).to(dev).unsqueeze(0)
            logits = model(feats)["action_logits"]
            pred = int(logits.argmax(dim=-1).item())
            true_aid = str(ex["label"]["action_id"])
            if INDEX_BY_ACTION_ID.get(true_aid) == pred:
                correct += 1
    return correct / max(len(examples), 1)
