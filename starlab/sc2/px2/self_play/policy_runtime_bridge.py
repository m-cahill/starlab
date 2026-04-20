"""Reusable M02 policy → M01 legality + compiler bridge (PX2-M03)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from starlab.sc2.px2 import (
    GameStateSnapshot,
    Px2InternalCommand,
    TerranAction,
    compile_terran_action,
)
from starlab.sc2.px2.bootstrap.evaluate_bootstrap import decode_legality_aware
from starlab.sc2.px2.bootstrap.feature_adapter import FEATURE_ADAPTER_PROFILE
from starlab.sc2.px2.bootstrap.game_state_presets import snapshot_dict_to_dataclass_kwargs
from starlab.sc2.px2.bootstrap.policy_model import (
    BootstrapTerranPolicy,
    features_tensor_from_observation,
)
from starlab.sc2.px2.runtime_receipts import build_compile_receipt, receipt_sha256


def _state_from_snapshot(d: dict[str, Any]) -> GameStateSnapshot:
    return GameStateSnapshot(**snapshot_dict_to_dataclass_kwargs(d))


@dataclass(frozen=True, slots=True)
class PolicyRuntimeBridgeReceipt:
    """One policy→runtime step: decode + compile trace for audits and smoke JSON."""

    feature_adapter_profile: str
    terran_action: TerranAction
    compile_receipt: dict[str, Any]
    compile_receipt_sha256: str
    internal_command: Px2InternalCommand
    decode_ok: bool

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "feature_adapter_profile": self.feature_adapter_profile,
            "terran_action": self.terran_action.to_json_dict(),
            "compile_receipt_sha256": self.compile_receipt_sha256,
            "decode_ok": self.decode_ok,
            "internal_command_kind": self.internal_command.command_kind,
        }


def bootstrap_policy_runtime_step(
    model: BootstrapTerranPolicy,
    observation_surface: dict[str, Any],
    game_state_snapshot: dict[str, Any],
    *,
    max_try: int = 32,
) -> PolicyRuntimeBridgeReceipt:
    """Forward M02 policy on M18 features, legality-aware decode, M01 compile.

    Does not train; does not launch SC2. Raises if decode finds no legal action
    (fixture tests should use states where at least one head is legal).
    """

    state = _state_from_snapshot(game_state_snapshot)
    features = features_tensor_from_observation(observation_surface)
    if features.dim() == 1:
        features = features.unsqueeze(0)
    action = decode_legality_aware(
        model,
        features,
        state,
        max_try=max_try,
    )
    if action is None:
        msg = "decode_legality_aware returned no legal action"
        raise RuntimeError(msg)
    cmd = compile_terran_action(action, state)
    receipt = build_compile_receipt(action=action, state=state, include_legality=True)
    digest = receipt_sha256(receipt)
    return PolicyRuntimeBridgeReceipt(
        feature_adapter_profile=FEATURE_ADAPTER_PROFILE,
        terran_action=action,
        compile_receipt=receipt,
        compile_receipt_sha256=digest,
        internal_command=cmd,
        decode_ok=True,
    )
