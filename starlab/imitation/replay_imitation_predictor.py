"""Frozen M27 imitation predictor: signature table + global fallback (M27/M28)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from starlab.imitation.baseline_models import BASELINE_VERSION


@dataclass(frozen=True)
class FrozenImitationPredictor:
    """Lookup known signature → label; unknown → global fallback label."""

    signature_to_label: dict[str, str]
    fallback_label: str

    def predict(self, signature: str) -> tuple[str, bool]:
        """Return (predicted_label, used_fallback)."""

        if signature in self.signature_to_label:
            return self.signature_to_label[signature], False
        return self.fallback_label, True

    @classmethod
    def from_signature_mapping(
        cls,
        signature_to_label: dict[str, str],
        fallback_label: str,
    ) -> FrozenImitationPredictor:
        return cls(
            signature_to_label=dict(signature_to_label),
            fallback_label=fallback_label,
        )

    @classmethod
    def from_baseline_body(cls, baseline: dict[str, Any]) -> FrozenImitationPredictor:
        """Load predictor from a governed ``replay_imitation_baseline.json`` body."""

        bv = baseline.get("baseline_version")
        if bv != BASELINE_VERSION:
            msg = f"unsupported baseline_version {bv!r} (expected {BASELINE_VERSION!r})"
            raise ValueError(msg)

        fb = baseline.get("fallback_label")
        if not isinstance(fb, str) or not fb:
            msg = "baseline.fallback_label must be a non-empty string"
            raise ValueError(msg)

        table = baseline.get("signature_table")
        if not isinstance(table, list):
            msg = "baseline.signature_table must be an array"
            raise ValueError(msg)

        mapping: dict[str, str] = {}
        for row in table:
            if not isinstance(row, dict):
                msg = "signature_table rows must be objects"
                raise ValueError(msg)
            sig = row.get("context_signature")
            pred = row.get("predicted_label")
            if not isinstance(sig, str) or not isinstance(pred, str):
                msg = "signature_table row requires context_signature and predicted_label strings"
                raise ValueError(msg)
            mapping[sig] = pred

        return cls(signature_to_label=mapping, fallback_label=fb)
