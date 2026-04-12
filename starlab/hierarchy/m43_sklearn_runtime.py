"""Load M43 hierarchical sklearn joblib bundle and run inference (local validation only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from starlab.hierarchy.delegate_policy import DELEGATE_IDS
from starlab.hierarchy.hierarchical_training_models import SKLEARN_BUNDLE_SCHEMA
from starlab.imitation.replay_imitation_training_pipeline import (
    parse_context_signature_to_feature_dict,
)


def load_hierarchical_sklearn_bundle(path: Path) -> dict[str, Any]:
    """Load ``hierarchical_training_sklearn_bundle.joblib`` from disk."""

    raw = joblib.load(path)
    if not isinstance(raw, dict):
        msg = "M43 sklearn bundle root must be a dict"
        raise ValueError(msg)
    sv = raw.get("schema_version")
    if sv != SKLEARN_BUNDLE_SCHEMA:
        msg = (
            f"unsupported M43 sklearn bundle schema_version: {sv!r} "
            f"(expected {SKLEARN_BUNDLE_SCHEMA!r})"
        )
        raise ValueError(msg)
    for key in ("dict_vectorizer", "manager", "workers", "global_majority_label"):
        if key not in raw:
            msg = f"M43 sklearn bundle missing key: {key}"
            raise ValueError(msg)
    return raw


def predict_delegate_and_coarse_label(
    bundle: dict[str, Any],
    context_signature: str,
) -> tuple[str, str]:
    """Return (predicted_delegate_id, predicted_coarse_label) for one ``context_signature``."""

    xd = parse_context_signature_to_feature_dict(context_signature)
    vectorizer = bundle["dict_vectorizer"]
    xm = vectorizer.transform([xd])

    mgr = bundle["manager"]
    clf = mgr.get("classifier")
    enc = mgr.get("label_encoder")
    const_del = mgr.get("constant_delegate_id")
    if clf is not None and enc is not None:
        pred_enc = clf.predict(xm)[0]
        delegate_id = str(enc.inverse_transform([pred_enc])[0])
    else:
        if const_del is None:
            msg = "M43 bundle manager has no classifier and no constant_delegate_id"
            raise ValueError(msg)
        delegate_id = str(const_del)

    if delegate_id not in bundle["workers"]:
        msg = f"delegate_id {delegate_id!r} missing from workers map"
        raise ValueError(msg)

    we = bundle["workers"][delegate_id]
    w_clf = we.get("classifier")
    w_enc = we.get("label_encoder")
    fb = we.get("fallback_label")
    xw = vectorizer.transform([xd])
    if w_clf is not None and w_enc is not None:
        pred_w = w_clf.predict(xw)[0]
        coarse = str(w_enc.inverse_transform([pred_w])[0])
    else:
        if fb is None:
            msg = f"worker for delegate {delegate_id!r} has no classifier and no fallback_label"
            raise ValueError(msg)
        coarse = str(fb)

    return delegate_id, coarse


def assert_workers_cover_delegates(bundle: dict[str, Any]) -> None:
    """Raise if workers map does not cover the fixed four-delegate catalog."""

    workers = bundle["workers"]
    if not isinstance(workers, dict):
        msg = "bundle workers must be a dict"
        raise ValueError(msg)
    for did in DELEGATE_IDS:
        if did not in workers:
            msg = f"M43 bundle workers missing delegate {did!r}"
            raise ValueError(msg)
