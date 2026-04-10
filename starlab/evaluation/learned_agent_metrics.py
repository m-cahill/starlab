"""Deterministic metrics for learned-agent evaluation (M28)."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence


def accuracy(y_true: Sequence[str], y_pred: Sequence[str]) -> float:
    """Fraction of matching labels."""

    if len(y_true) != len(y_pred):
        msg = "y_true and y_pred length mismatch"
        raise ValueError(msg)
    n = len(y_true)
    if n == 0:
        return 0.0
    return sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == p) / float(n)


def _per_class_f1(y_true: Sequence[str], y_pred: Sequence[str], cls: str) -> float:
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == cls and p == cls)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != cls and p == cls)
    fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == cls and p != cls)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    if precision + recall == 0.0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


def macro_f1(y_true: Sequence[str], y_pred: Sequence[str], labels: Sequence[str]) -> float:
    """Macro-averaged F1 over ``labels`` (including classes with zero support)."""

    if len(y_true) != len(y_pred):
        msg = "y_true and y_pred length mismatch"
        raise ValueError(msg)
    if not labels:
        return 0.0
    f1s = [_per_class_f1(y_true, y_pred, c) for c in labels]
    return sum(f1s) / float(len(labels))


def label_counts(labels: Sequence[str]) -> dict[str, int]:
    """Sorted key order applied by caller for determinism."""

    ctr = Counter(labels)
    return {k: int(ctr[k]) for k in sorted(ctr.keys())}
