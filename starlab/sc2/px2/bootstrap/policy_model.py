"""Small structured-action policy over PX2 Terran core v1 (PX2-M02)."""

from __future__ import annotations

from typing import Any, Final

import torch
import torch.nn as nn
import torch.nn.functional as F

from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim, pad_or_trunc
from starlab.sc2.px2.terran_action_schema import ALL_TERRAN_CORE_V1_ACTION_IDS

ORDERED_ACTION_IDS: Final[tuple[str, ...]] = tuple(sorted(ALL_TERRAN_CORE_V1_ACTION_IDS))
INDEX_BY_ACTION_ID: Final[dict[str, int]] = {a: i for i, a in enumerate(ORDERED_ACTION_IDS)}
ACTION_INDEX_BY_ID: Final[dict[int, str]] = {i: a for i, a in enumerate(ORDERED_ACTION_IDS)}

PRODUCER_KEYS: Final[tuple[str, ...]] = (
    "barracks_0",
    "factory_0",
    "starport_0",
    "command_center_0",
    "orbital_0",
)
PRODUCER_INDEX: Final[dict[str, int]] = {k: i for i, k in enumerate(PRODUCER_KEYS)}


class BootstrapTerranPolicy(nn.Module):
    """Encoder + multi-head outputs for action id and common argument slots."""

    def __init__(self, input_dim: int | None = None, hidden: int = 96) -> None:
        super().__init__()
        indim = input_dim or observation_feature_dim()
        self.fc1 = nn.Linear(indim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        n_act = len(ORDERED_ACTION_IDS)
        self.action_head = nn.Linear(hidden, n_act)
        self.build_slot_head = nn.Linear(hidden, 5)
        self.expansion_slot_head = nn.Linear(hidden, 5)
        self.region_slot_head = nn.Linear(hidden, 5)
        self.producer_head = nn.Linear(hidden, len(PRODUCER_KEYS))

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        if x.dim() == 1:
            x = x.unsqueeze(0)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return {
            "action_logits": self.action_head(x),
            "build_slot_logits": self.build_slot_head(x),
            "expansion_slot_logits": self.expansion_slot_head(x),
            "region_slot_logits": self.region_slot_head(x),
            "producer_logits": self.producer_head(x),
        }


def features_tensor_from_observation(obs: dict[str, Any]) -> torch.Tensor:
    from starlab.sc2.px2.bootstrap.feature_adapter import observation_dict_to_feature_tensor

    v = observation_dict_to_feature_tensor(obs)
    return pad_or_trunc(v, observation_feature_dim())


def training_loss(
    out: dict[str, torch.Tensor],
    *,
    action_index: torch.Tensor,
    true_build_slot: torch.Tensor | None,
    true_expansion_slot: torch.Tensor | None,
    true_region_slot: torch.Tensor | None,
    true_producer_index: torch.Tensor | None,
    need_build: torch.Tensor,
    need_exp: torch.Tensor,
    need_region: torch.Tensor,
    need_prod: torch.Tensor,
) -> torch.Tensor:
    """Masked multi-task loss."""

    loss = F.cross_entropy(out["action_logits"], action_index)
    if need_build.any() and true_build_slot is not None:
        loss = loss + (
            F.cross_entropy(out["build_slot_logits"], true_build_slot, reduction="none")
            * need_build.float()
        ).sum() / (need_build.float().sum() + 1e-8)
    if need_exp.any() and true_expansion_slot is not None:
        loss = loss + (
            F.cross_entropy(out["expansion_slot_logits"], true_expansion_slot, reduction="none")
            * need_exp.float()
        ).sum() / (need_exp.float().sum() + 1e-8)
    if need_region.any() and true_region_slot is not None:
        loss = loss + (
            F.cross_entropy(out["region_slot_logits"], true_region_slot, reduction="none")
            * need_region.float()
        ).sum() / (need_region.float().sum() + 1e-8)
    if need_prod.any() and true_producer_index is not None:
        loss = loss + (
            F.cross_entropy(out["producer_logits"], true_producer_index, reduction="none")
            * need_prod.float()
        ).sum() / (need_prod.float().sum() + 1e-8)
    return loss
