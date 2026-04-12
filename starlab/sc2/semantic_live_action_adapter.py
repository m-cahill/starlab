"""Bounded semantic-to-live action mapping for M44 (conservative scripted templates)."""

from __future__ import annotations

from typing import Any

SEMANTIC_LIVE_ACTION_ADAPTER_POLICY_ID = "starlab.m44.semantic_live_action_adapter.v1"

# Narrow v1: one safe template id per coarse semantic label (scripted stub semantics only).
_COARSE_LABEL_TO_TEMPLATE: dict[str, str] = {
    "army_attack": "starlab.m44.template.combat_attack_stub_v1",
    "army_move": "starlab.m44.template.combat_move_stub_v1",
    "economy_expand": "starlab.m44.template.economy_expand_stub_v1",
    "economy_worker": "starlab.m44.template.economy_worker_stub_v1",
    "other": "starlab.m44.template.information_idle_stub_v1",
    "production_structure": "starlab.m44.template.production_structure_stub_v1",
    "production_unit": "starlab.m44.template.production_unit_stub_v1",
    "research_upgrade": "starlab.m44.template.production_research_stub_v1",
    "scout": "starlab.m44.template.information_scout_stub_v1",
}


def map_semantic_to_live_action(
    *,
    delegate_id: str,
    coarse_label: str,
) -> dict[str, Any]:
    """Map hierarchical outputs to a bounded scripted action template record."""

    template_id = _COARSE_LABEL_TO_TEMPLATE.get(coarse_label)
    if template_id is None:
        template_id = "starlab.m44.template.fallback_unknown_coarse_stub_v1"
    return {
        "action_template_id": template_id,
        "coarse_semantic_label": coarse_label,
        "delegate_id": delegate_id,
        "kind": "bounded_scripted_stub",
        "semantic_live_action_adapter_policy_id": SEMANTIC_LIVE_ACTION_ADAPTER_POLICY_ID,
    }
