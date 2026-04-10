"""Frozen hierarchical imitation predictor + M29 trace document builder (M30)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from starlab.hierarchy.delegate_policy import (
    build_delegate_catalog_entries,
    delegate_id_for_coarse_label,
)
from starlab.hierarchy.hierarchical_agent_models import (
    AGENT_VERSION,
    INTERFACE_TRACE_SCHEMA_VERSION,
)
from starlab.imitation.dataset_models import LABEL_POLICY_ID as M26_LABEL_POLICY_ID


@dataclass(frozen=True)
class FrozenHierarchicalImitationPredictor:
    """Two-level lookup: signature → delegate; (delegate, signature) → coarse label."""

    signature_to_delegate: dict[str, str]
    pair_to_label: dict[tuple[str, str], str]
    manager_fallback_delegate: str
    worker_fallback_by_delegate: dict[str, str]
    global_worker_fallback_label: str

    def predict(
        self,
        signature: str,
    ) -> tuple[str, str, bool, bool]:
        """Return (delegate_id, coarse_label, used_manager_fallback, used_worker_fallback)."""

        mgr_fb = signature not in self.signature_to_delegate
        delegate = (
            self.signature_to_delegate[signature] if not mgr_fb else self.manager_fallback_delegate
        )
        key = (delegate, signature)
        wrk_fb = key not in self.pair_to_label
        label = (
            self.pair_to_label[key]
            if not wrk_fb
            else self.worker_fallback_by_delegate.get(delegate, self.global_worker_fallback_label)
        )
        return delegate, label, mgr_fb, wrk_fb

    def build_trace_document_for_signature(
        self,
        *,
        context_signature: str,
        frame_ref: dict[str, Any],
    ) -> dict[str, Any]:
        """Emit ``schema_version`` + ``hierarchical_decision_trace`` for one frame."""

        delegate_id, coarse_label, _mgr_fb, _wrk_fb = self.predict(context_signature)

        delegates_catalog = build_delegate_catalog_entries()
        manager_response: dict[str, Any] = {
            "selected_delegate_id": delegate_id,
            "directive_kind": "m30_delegate",
            "option_id": "m30_v1",
        }
        delegate_descriptor = {"delegate_id": delegate_id, "delegate_role": "worker"}
        trace = {
            "manager_request": {
                "frame_ref": frame_ref,
                "delegates_catalog": delegates_catalog,
            },
            "manager_response": manager_response,
            "worker_request": {
                "frame_ref": frame_ref,
                "manager_response": manager_response,
                "delegate": delegate_descriptor,
            },
            "worker_response": {
                "label_policy_id": M26_LABEL_POLICY_ID,
                "semantic_coarse_label": coarse_label,
            },
        }
        return {
            "schema_version": INTERFACE_TRACE_SCHEMA_VERSION,
            "hierarchical_decision_trace": trace,
        }

    @classmethod
    def from_agent_body(cls, agent: dict[str, Any]) -> FrozenHierarchicalImitationPredictor:
        """Load from a governed ``replay_hierarchical_imitation_agent.json`` body."""

        av = agent.get("agent_version")
        if av != AGENT_VERSION:
            msg = f"unsupported agent_version {av!r} (expected {AGENT_VERSION!r})"
            raise ValueError(msg)

        sig_map: dict[str, str] = {}
        for row in agent.get("manager_signature_table", []):
            if not isinstance(row, dict):
                continue
            sig = row.get("context_signature")
            pred = row.get("predicted_delegate_id")
            if isinstance(sig, str) and isinstance(pred, str):
                sig_map[sig] = pred

        pair_to_label: dict[tuple[str, str], str] = {}
        wtables = agent.get("worker_signature_tables_by_delegate", {})
        if not isinstance(wtables, dict):
            msg = "worker_signature_tables_by_delegate must be an object"
            raise ValueError(msg)
        for did, rows in sorted(wtables.items()):
            if not isinstance(did, str) or not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                sig = row.get("context_signature")
                lab = row.get("predicted_label")
                if isinstance(sig, str) and isinstance(lab, str):
                    pair_to_label[(did, sig)] = lab

        mfd = agent.get("manager_fallback_delegate_id")
        if not isinstance(mfd, str) or not mfd:
            msg = "manager_fallback_delegate_id must be a non-empty string"
            raise ValueError(msg)

        wfbd = agent.get("worker_fallback_label_by_delegate", {})
        if not isinstance(wfbd, dict):
            msg = "worker_fallback_label_by_delegate must be an object"
            raise ValueError(msg)
        worker_fb: dict[str, str] = {}
        for k, v in sorted(wfbd.items()):
            if isinstance(k, str) and isinstance(v, str):
                worker_fb[k] = v

        gwf = agent.get("global_worker_fallback_label")
        if not isinstance(gwf, str) or not gwf:
            msg = "global_worker_fallback_label must be a non-empty string"
            raise ValueError(msg)

        return cls(
            signature_to_delegate=sig_map,
            pair_to_label=pair_to_label,
            manager_fallback_delegate=mfd,
            worker_fallback_by_delegate=worker_fb,
            global_worker_fallback_label=gwf,
        )


def true_delegate_for_example(target_semantic_kind: str) -> str:
    """Delegate id from supervised coarse label (training oracle)."""

    return delegate_id_for_coarse_label(target_semantic_kind)
