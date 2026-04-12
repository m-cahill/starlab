"""M41 sklearn bundle predictor: parallel to FrozenImitationPredictor for M28/M42."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from starlab.imitation.replay_imitation_training_io import sha256_hex_file
from starlab.imitation.replay_imitation_training_pipeline import (
    SKLEARN_BUNDLE_SCHEMA,
    parse_context_signature_to_feature_dict,
)


@dataclass(frozen=True)
class TrainedRunPredictor:
    """Load M41 ``replay_imitation_sklearn_bundle.joblib``; predict from ``context_signature``."""

    _bundle: dict[str, Any]

    def predict(self, signature: str) -> tuple[str, bool]:
        """Return (predicted_label, used_fallback). Sklearn path always uses_fallback False."""

        xd = parse_context_signature_to_feature_dict(signature)
        vec = self._bundle["dict_vectorizer"]
        clf = self._bundle["classifier"]
        enc = self._bundle["label_encoder"]
        xm = vec.transform([xd])
        pred_enc = clf.predict(xm)[0]
        lab = str(enc.inverse_transform([pred_enc])[0])
        return lab, False

    @classmethod
    def from_joblib_path(cls, path: Path) -> TrainedRunPredictor:
        """Load and validate schema from disk."""

        raw = joblib.load(path)
        if not isinstance(raw, dict):
            msg = "M41 joblib weights must deserialize to a dict (sklearn bundle)"
            raise ValueError(msg)
        if raw.get("schema_version") != SKLEARN_BUNDLE_SCHEMA:
            msg = f"unsupported sklearn bundle schema_version {raw.get('schema_version')!r}"
            raise ValueError(msg)
        for k in ("classifier", "dict_vectorizer", "label_encoder"):
            if k not in raw:
                msg = f"M41 sklearn bundle missing {k!r}"
                raise ValueError(msg)
        return cls(_bundle=raw)


def resolve_m41_weights_path(*, training_run_dir: Path, training_run_body: dict[str, Any]) -> Path:
    """Resolve ``weights_sidecar.relative_path`` under ``training_run_dir``."""

    ws = training_run_body.get("weights_sidecar")
    if not isinstance(ws, dict):
        msg = "M41 training run requires weights_sidecar dict for TrainedRunPredictor loading"
        raise ValueError(msg)
    rel = ws.get("relative_path")
    if not isinstance(rel, str) or not rel:
        msg = "weights_sidecar.relative_path must be a non-empty string"
        raise ValueError(msg)
    return (training_run_dir / rel).resolve()


def verify_weights_sha256(*, weights_path: Path, training_run_body: dict[str, Any]) -> None:
    """Assert on-disk SHA matches ``weights_sidecar.artifact_sha256`` when present."""

    ws = training_run_body.get("weights_sidecar")
    if not isinstance(ws, dict):
        return
    expected = ws.get("artifact_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        return
    got = sha256_hex_file(weights_path)
    if got != expected:
        msg = f"M41 weights SHA mismatch: expected {expected}, got {got}"
        raise ValueError(msg)
