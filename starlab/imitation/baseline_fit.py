"""Deterministic majority-label fit over context signatures (M27)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from starlab.imitation.baseline_features import build_context_signature
from starlab.imitation.baseline_models import (
    BASELINE_REPORT_VERSION,
    BASELINE_VERSION,
    FEATURE_POLICY_ID,
    MODEL_FAMILY,
    NON_CLAIMS_V1,
    REPLAY_IMITATION_BASELINE_FILENAME,
    REPLAY_IMITATION_BASELINE_REPORT_FILENAME,
)
from starlab.imitation.dataset_models import REPLAY_TRAINING_DATASET_VERSION
from starlab.imitation.replay_observation_materialization import (
    materialize_observation_for_observation_request,
    resolve_bundle_directory,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def _majority_label(counts: Counter[str]) -> str:
    if not counts:
        msg = "empty label counts for majority"
        raise ValueError(msg)
    best_n = max(counts.values())
    candidates = sorted([lab for lab, c in counts.items() if c == best_n])
    return candidates[0]


def _global_fallback_label(train_labels: list[str]) -> str:
    if not train_labels:
        msg = "no training labels"
        raise ValueError(msg)
    return _majority_label(Counter(train_labels))


def build_replay_imitation_baseline_artifacts(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Fit baseline + report from a governed M26 dataset + M14 bundle directories."""

    dv = dataset.get("dataset_version")
    if dv != REPLAY_TRAINING_DATASET_VERSION:
        msg = f"unsupported dataset_version {dv!r} (expected {REPLAY_TRAINING_DATASET_VERSION!r})"
        raise ValueError(msg)

    dsha = dataset.get("dataset_sha256")
    if not isinstance(dsha, str) or len(dsha) != 64:
        msg = "dataset.dataset_sha256 must be a 64-char hex string"
        raise ValueError(msg)

    examples = dataset.get("examples")
    if not isinstance(examples, list) or not examples:
        msg = "dataset.examples must be a non-empty array"
        raise ValueError(msg)

    label_policy_id = dataset.get("label_policy_id")
    if not isinstance(label_policy_id, str) or not label_policy_id:
        msg = "dataset.label_policy_id must be a non-empty string"
        raise ValueError(msg)

    all_warnings: list[str] = []
    dw = dataset.get("warnings")
    if isinstance(dw, list):
        for w in dw:
            if isinstance(w, str):
                all_warnings.append(w)

    bundle_index: dict[str, Path] = {}
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        bid = ex.get("bundle_id")
        if isinstance(bid, str) and bid:
            if bid not in bundle_index:
                bundle_index[bid] = resolve_bundle_directory(bundle_id=bid, bundle_dirs=bundle_dirs)

    rows: list[
        tuple[str, str, str, str, dict[str, Any]]
    ] = []  # example_id, split, label, signature, extra
    for ex in examples:
        if not isinstance(ex, dict):
            msg = "each example must be an object"
            raise ValueError(msg)
        eid = ex.get("example_id")
        sp = ex.get("split")
        lab = ex.get("target_semantic_kind")
        oreq = ex.get("observation_request")
        if not isinstance(eid, str) or not isinstance(sp, str) or not isinstance(lab, str):
            msg = f"example missing example_id, split, or target_semantic_kind: {ex!r}"
            raise ValueError(msg)
        if not isinstance(oreq, dict):
            msg = f"example {eid}: observation_request must be an object"
            raise ValueError(msg)

        bid = ex.get("bundle_id")
        if not isinstance(bid, str):
            msg = f"example {eid}: bundle_id must be a string"
            raise ValueError(msg)

        bdir = bundle_index[bid]
        cs, obs, _rep, warns = materialize_observation_for_observation_request(
            bundle_dir=bdir,
            observation_request=oreq,
        )
        all_warnings.extend(warns)
        sig = build_context_signature(
            observation_frame=obs,
            canonical_state=cs,
            perspective_player_index=int(ex.get("perspective_player_index", -1)),
        )
        rows.append((eid, sp, lab, sig, {}))

    train_labels = [lab for _eid, sp, lab, _sig, _ in rows if sp == "train"]
    fallback_label = _global_fallback_label(train_labels)

    # Per-signature label counts on training split only
    sig_train: dict[str, Counter[str]] = {}
    for _eid, sp, lab, sig, _ in rows:
        if sp != "train":
            continue
        sig_train.setdefault(sig, Counter())[lab] += 1

    sig_predicted: dict[str, str] = {}
    for sig, ctr in sorted(sig_train.items()):
        sig_predicted[sig] = _majority_label(ctr)

    signature_table: list[dict[str, Any]] = []
    for sig in sorted(sig_predicted.keys()):
        ctr = sig_train[sig]
        pred = sig_predicted[sig]
        support_by_label = {k: ctr[k] for k in sorted(ctr.keys())}
        signature_table.append(
            {
                "context_signature": sig,
                "predicted_label": pred,
                "support_by_label": support_by_label,
                "training_support": int(sum(ctr.values())),
            },
        )

    def predict_for_signature(sig: str) -> tuple[str, bool]:
        if sig in sig_predicted:
            return sig_predicted[sig], False
        return fallback_label, True

    split_totals: Counter[str] = Counter()
    split_agree: Counter[str] = Counter()
    split_fallback: Counter[str] = Counter()

    label_counts: Counter[str] = Counter()
    for _eid, sp, lab, _sig, _ in rows:
        split_totals[sp] += 1
        label_counts[lab] += 1

    for _eid, sp, lab, sig, _ in rows:
        pred, used_fb = predict_for_signature(sig)
        if pred == lab:
            split_agree[sp] += 1
        if used_fb:
            split_fallback[sp] += 1

    agreement_by_split: dict[str, Any] = {}
    for sp in sorted(split_totals.keys()):
        tot = split_totals[sp]
        ag = split_agree[sp]
        agreement_by_split[sp] = {
            "agreement_count": int(ag),
            "example_count": int(tot),
            "rate": float(ag) / float(tot) if tot else 0.0,
        }

    fallback_counts_by_split = {k: int(split_fallback[k]) for k in sorted(split_fallback.keys())}

    vocab = sorted({lab for _eid, _sp, lab, _sig, _ in rows})

    warnings_sorted = sorted(set(all_warnings))
    non_claims_sorted = sorted(set(NON_CLAIMS_V1))

    body_pre_hash: dict[str, Any] = {
        "fallback_label": fallback_label,
        "feature_policy_id": FEATURE_POLICY_ID,
        "label_policy_id": label_policy_id,
        "label_vocabulary": vocab,
        "model_family": MODEL_FAMILY,
        "non_claims": non_claims_sorted,
        "signature_table": signature_table,
        "training_dataset_sha256": dsha,
        "warnings": warnings_sorted,
        "baseline_version": BASELINE_VERSION,
    }

    baseline_sha256 = sha256_hex_of_canonical_json(body_pre_hash)

    baseline: dict[str, Any] = {
        **body_pre_hash,
        "baseline_sha256": baseline_sha256,
    }

    train_n = split_totals.get("train", 0)
    val_n = split_totals.get("validation", 0)
    test_n = split_totals.get("test", 0)

    report: dict[str, Any] = {
        "agreement_by_split": agreement_by_split,
        "baseline_sha256": baseline_sha256,
        "fallback_counts_by_split": fallback_counts_by_split,
        "fallback_label": fallback_label,
        "label_counts": {k: label_counts[k] for k in sorted(label_counts.keys())},
        "non_claims": list(non_claims_sorted),
        "report_version": BASELINE_REPORT_VERSION,
        "signature_count": len(signature_table),
        "test_example_count": int(test_n),
        "training_example_count": int(train_n),
        "validation_example_count": int(val_n),
        "warnings": list(warnings_sorted),
    }

    return baseline, report


def write_replay_imitation_baseline_artifacts(
    *,
    dataset_path: Path,
    bundle_dirs: list[Path],
    output_dir: Path,
) -> tuple[Path, Path]:
    raw = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "dataset JSON root must be an object"
        raise ValueError(msg)
    baseline, report = build_replay_imitation_baseline_artifacts(
        dataset=raw,
        bundle_dirs=bundle_dirs,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    bp = output_dir / REPLAY_IMITATION_BASELINE_FILENAME
    rp = output_dir / REPLAY_IMITATION_BASELINE_REPORT_FILENAME
    bp.write_text(canonical_json_dumps(baseline), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return bp, rp
