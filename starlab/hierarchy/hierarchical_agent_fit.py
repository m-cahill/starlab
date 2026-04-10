"""Fit deterministic hierarchical imitation tables from M26 + M14 (M30)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from starlab.hierarchy.delegate_policy import (
    COARSE_LABEL_TO_DELEGATE_ID,
    DELEGATE_IDS,
    DELEGATE_POLICY_ID,
    assert_delegate_mapping_total,
    delegate_id_for_coarse_label,
)
from starlab.hierarchy.hierarchical_agent_models import (
    AGENT_VERSION,
    FEATURE_POLICY_ID,
    INTERFACE_TRACE_SCHEMA_VERSION,
    MANAGER_MODEL_FAMILY,
    NON_CLAIMS_V1,
    REPLAY_HIERARCHICAL_IMITATION_AGENT_FILENAME,
    REPLAY_HIERARCHICAL_IMITATION_AGENT_REPORT_FILENAME,
    REPORT_VERSION,
    WORKER_MODEL_FAMILY,
)
from starlab.hierarchy.hierarchical_agent_predictor import FrozenHierarchicalImitationPredictor
from starlab.imitation.baseline_features import build_context_signature
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


def _global_majority_delegate(train_delegates: list[str]) -> str:
    if not train_delegates:
        msg = "no training delegates"
        raise ValueError(msg)
    return _majority_label(Counter(train_delegates))


def _global_majority_label(train_labels: list[str]) -> str:
    if not train_labels:
        msg = "no training labels"
        raise ValueError(msg)
    return _majority_label(Counter(train_labels))


def build_replay_hierarchical_imitation_agent_artifacts(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Fit agent + report from a governed M26 dataset + M14 bundle directories."""

    assert_delegate_mapping_total()

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

    rows: list[tuple[str, str, str, str, str]] = []
    # example_id, split, coarse_label, signature, delegate_id (oracle)
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
        if lab not in COARSE_LABEL_TO_DELEGATE_ID:
            msg = f"unsupported target_semantic_kind for M30 delegate map: {lab!r}"
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
        del_id = delegate_id_for_coarse_label(lab)
        rows.append((eid, sp, lab, sig, del_id))

    train_rows = [(eid, sp, lab, sig, did) for eid, sp, lab, sig, did in rows if sp == "train"]
    if not train_rows:
        msg = "no training split examples"
        raise ValueError(msg)

    train_labels = [lab for _eid, _sp, lab, _sig, _ in train_rows]
    train_delegates = [did for _eid, _sp, _lab, _sig, did in train_rows]
    manager_fallback = _global_majority_delegate(train_delegates)
    global_worker_fallback = _global_majority_label(train_labels)

    # Manager: signature -> delegate counts (training only)
    sig_mgr: dict[str, Counter[str]] = {}
    for _eid, _sp, _lab, sig, did in train_rows:
        sig_mgr.setdefault(sig, Counter())[did] += 1
    sig_to_delegate: dict[str, str] = {}
    for sig in sorted(sig_mgr.keys()):
        sig_to_delegate[sig] = _majority_label(sig_mgr[sig])

    manager_signature_table: list[dict[str, Any]] = []
    for sig in sorted(sig_to_delegate.keys()):
        ctr = sig_mgr[sig]
        pred = sig_to_delegate[sig]
        support_by_delegate = {k: ctr[k] for k in sorted(ctr.keys())}
        manager_signature_table.append(
            {
                "context_signature": sig,
                "predicted_delegate_id": pred,
                "support_by_delegate": support_by_delegate,
                "training_support": int(sum(ctr.values())),
            },
        )

    # Worker: (delegate, signature) -> label counts (training only)
    pair_ctr: dict[tuple[str, str], Counter[str]] = {}
    for _eid, _sp, lab, sig, did in train_rows:
        pair_ctr.setdefault((did, sig), Counter())[lab] += 1
    pair_to_label: dict[tuple[str, str], str] = {}
    for key in sorted(pair_ctr.keys()):
        pair_to_label[key] = _majority_label(pair_ctr[key])

    worker_signature_tables_by_delegate: dict[str, list[dict[str, Any]]] = {
        d: [] for d in DELEGATE_IDS
    }
    for did, sig in sorted(pair_to_label.keys()):
        ctr = pair_ctr[(did, sig)]
        pred = pair_to_label[(did, sig)]
        support_by_label = {k: ctr[k] for k in sorted(ctr.keys())}
        worker_signature_tables_by_delegate[did].append(
            {
                "context_signature": sig,
                "predicted_label": pred,
                "support_by_label": support_by_label,
                "training_support": int(sum(ctr.values())),
            },
        )

    # Worker fallback per delegate: majority label among training rows for that delegate
    labels_by_delegate: dict[str, list[str]] = {d: [] for d in DELEGATE_IDS}
    for _eid, _sp, lab, _sig, did in train_rows:
        labels_by_delegate[did].append(lab)
    worker_fallback_by_delegate: dict[str, str] = {}
    for did in DELEGATE_IDS:
        lbs = labels_by_delegate[did]
        if lbs:
            worker_fallback_by_delegate[did] = _global_majority_label(lbs)
        else:
            worker_fallback_by_delegate[did] = global_worker_fallback

    delegate_label_mapping = [
        {"coarse_semantic_label": lab, "delegate_id": COARSE_LABEL_TO_DELEGATE_ID[lab]}
        for lab in sorted(COARSE_LABEL_TO_DELEGATE_ID.keys())
    ]

    delegate_catalog = [
        {
            "delegate_id": did,
            "description": {
                "combat": "Army move and attack coarse labels",
                "economy": "Economy expansion and worker coarse labels",
                "information": "Scouting, residual, and other coarse labels",
                "production": "Production and research coarse labels",
            }[did],
        }
        for did in DELEGATE_IDS
    ]

    predictor = FrozenHierarchicalImitationPredictor(
        signature_to_delegate=sig_to_delegate,
        pair_to_label=pair_to_label,
        manager_fallback_delegate=manager_fallback,
        worker_fallback_by_delegate=worker_fallback_by_delegate,
        global_worker_fallback_label=global_worker_fallback,
    )

    split_totals: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    delegate_counts: Counter[str] = Counter()
    for _eid, sp, lab, _sig, did in rows:
        split_totals[sp] += 1
        label_counts[lab] += 1
        delegate_counts[did] += 1

    mgr_agree: Counter[str] = Counter()
    wrk_agree: Counter[str] = Counter()
    e2e_agree: Counter[str] = Counter()
    mgr_fb: Counter[str] = Counter()
    wrk_fb: Counter[str] = Counter()

    for _eid, sp, lab, sig, true_del in rows:
        pred_del, pred_lab, um, uw = predictor.predict(sig)
        if pred_del == true_del:
            mgr_agree[sp] += 1
        if pred_lab == lab:
            wrk_agree[sp] += 1
        if pred_del == true_del and pred_lab == lab:
            e2e_agree[sp] += 1
        if um:
            mgr_fb[sp] += 1
        if uw:
            wrk_fb[sp] += 1

    def _rates(agree: Counter[str], totals: Counter[str]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for sp in sorted(totals.keys()):
            tot = totals[sp]
            ag = agree[sp]
            out[sp] = {
                "agreement_count": int(ag),
                "example_count": int(tot),
                "rate": float(ag) / float(tot) if tot else 0.0,
            }
        return out

    warnings_sorted = sorted(set(all_warnings))
    non_claims_sorted = sorted(set(NON_CLAIMS_V1))

    body_pre_hash: dict[str, Any] = {
        "agent_version": AGENT_VERSION,
        "delegate_catalog": delegate_catalog,
        "delegate_label_mapping": delegate_label_mapping,
        "delegate_policy_id": DELEGATE_POLICY_ID,
        "feature_policy_id": FEATURE_POLICY_ID,
        "global_worker_fallback_label": global_worker_fallback,
        "interface_trace_schema_version": INTERFACE_TRACE_SCHEMA_VERSION,
        "label_policy_id": label_policy_id,
        "manager_fallback_delegate_id": manager_fallback,
        "manager_model_family": MANAGER_MODEL_FAMILY,
        "manager_signature_table": manager_signature_table,
        "non_claims": non_claims_sorted,
        "training_dataset_sha256": dsha,
        "warnings": warnings_sorted,
        "worker_fallback_label_by_delegate": {
            k: worker_fallback_by_delegate[k] for k in sorted(worker_fallback_by_delegate.keys())
        },
        "worker_model_family": WORKER_MODEL_FAMILY,
        "worker_signature_tables_by_delegate": {
            k: worker_signature_tables_by_delegate[k]
            for k in sorted(worker_signature_tables_by_delegate.keys())
        },
    }

    agent_sha256 = sha256_hex_of_canonical_json(body_pre_hash)

    agent: dict[str, Any] = {
        **body_pre_hash,
        "agent_sha256": agent_sha256,
    }

    train_n = split_totals.get("train", 0)
    val_n = split_totals.get("validation", 0)
    test_n = split_totals.get("test", 0)

    report: dict[str, Any] = {
        "agent_sha256": agent_sha256,
        "delegate_counts": {k: delegate_counts[k] for k in sorted(delegate_counts.keys())},
        "delegate_policy_id": DELEGATE_POLICY_ID,
        "end_to_end_agreement_by_split": _rates(e2e_agree, split_totals),
        "feature_policy_id": FEATURE_POLICY_ID,
        "governed_asset_classes": {
            "code": {
                "description": "STARLAB Python modules under starlab/hierarchy/ (M30 scope)",
                "kind": "repository_source",
            },
            "dataset": {
                "description": "Governed M26 replay_training_dataset.json (hashed)",
                "kind": "replay_training_dataset",
                "training_dataset_sha256": dsha,
            },
            "delegate_policy": {
                "delegate_policy_id": DELEGATE_POLICY_ID,
                "kind": "checked_in_mapping",
            },
            "derived_labels": {
                "description": "Coarse labels from M26; delegate partition from M30 policy",
                "kind": "supervised_targets",
                "label_policy_id": label_policy_id,
            },
            "replays": {
                "description": "Referenced M14 bundle directories (hashed bundle members)",
                "kind": "governed_replay_bundles",
            },
        },
        "label_counts": {k: label_counts[k] for k in sorted(label_counts.keys())},
        "label_policy_id": label_policy_id,
        "manager_agreement_by_split": _rates(mgr_agree, split_totals),
        "manager_fallback_counts_by_split": {k: int(mgr_fb[k]) for k in sorted(mgr_fb.keys())},
        "non_claims": list(non_claims_sorted),
        "report_version": REPORT_VERSION,
        "test_example_count": int(test_n),
        "training_example_count": int(train_n),
        "validation_example_count": int(val_n),
        "warnings": list(warnings_sorted),
        "worker_agreement_by_split": _rates(wrk_agree, split_totals),
        "worker_fallback_counts_by_split": {k: int(wrk_fb[k]) for k in sorted(wrk_fb.keys())},
    }

    return agent, report


def write_replay_hierarchical_imitation_agent_artifacts(
    *,
    dataset_path: Path,
    bundle_dirs: list[Path],
    output_dir: Path,
) -> tuple[Path, Path]:
    raw = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "dataset JSON root must be an object"
        raise ValueError(msg)
    agent, report = build_replay_hierarchical_imitation_agent_artifacts(
        dataset=raw,
        bundle_dirs=bundle_dirs,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    ap = output_dir / REPLAY_HIERARCHICAL_IMITATION_AGENT_FILENAME
    rp = output_dir / REPLAY_HIERARCHICAL_IMITATION_AGENT_REPORT_FILENAME
    ap.write_text(canonical_json_dumps(agent), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ap, rp


def select_proof_trace_examples(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    agent: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return a small set of M29 trace documents (one delegate where possible + fallback)."""

    predictor = FrozenHierarchicalImitationPredictor.from_agent_body(agent)
    examples = dataset.get("examples")
    if not isinstance(examples, list):
        return []

    bundle_index: dict[str, Path] = {}
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        bid = ex.get("bundle_id")
        if isinstance(bid, str) and bid and bid not in bundle_index:
            bundle_index[bid] = resolve_bundle_directory(bundle_id=bid, bundle_dirs=bundle_dirs)

    seen_delegate: set[str] = set()
    traces: list[dict[str, Any]] = []

    # Prefer one train example per delegate (oracle delegate from label)
    for ex in sorted(
        examples, key=lambda e: str(e.get("example_id", "")) if isinstance(e, dict) else ""
    ):
        if not isinstance(ex, dict):
            continue
        if ex.get("split") != "train":
            continue
        lab = ex.get("target_semantic_kind")
        oreq = ex.get("observation_request")
        if not isinstance(lab, str) or not isinstance(oreq, dict):
            continue
        did = delegate_id_for_coarse_label(lab)
        if did in seen_delegate:
            continue
        bid = ex.get("bundle_id")
        if not isinstance(bid, str):
            continue
        bdir = bundle_index[bid]
        cs, obs, _rep, _w = materialize_observation_for_observation_request(
            bundle_dir=bdir,
            observation_request=oreq,
        )
        sig = build_context_signature(
            observation_frame=obs,
            canonical_state=cs,
            perspective_player_index=int(ex.get("perspective_player_index", -1)),
        )
        frame_ref = {
            "bundle_id": oreq.get("bundle_id"),
            "lineage_root": oreq.get("lineage_root"),
            "gameloop": oreq.get("gameloop"),
            "perspective_player_index": oreq.get("perspective_player_index"),
        }
        traces.append(
            predictor.build_trace_document_for_signature(context_signature=sig, frame_ref=frame_ref)
        )
        seen_delegate.add(did)
        if len(seen_delegate) >= len(DELEGATE_IDS):
            break

    # Fallback-path trace: unseen signature forces manager + worker fallbacks (frame_ref real)
    if examples:
        ex0 = next((e for e in examples if isinstance(e, dict)), None)
        if ex0 and isinstance(ex0.get("observation_request"), dict):
            oreq = ex0["observation_request"]
            frame_ref = {
                "bundle_id": oreq.get("bundle_id"),
                "lineage_root": oreq.get("lineage_root"),
                "gameloop": oreq.get("gameloop"),
                "perspective_player_index": oreq.get("perspective_player_index"),
            }
            traces.append(
                predictor.build_trace_document_for_signature(
                    context_signature=(
                        "m30_proof_unseen_signature|"
                        "army_count_bucket=b0|base_count_bucket=b0|game_phase_bucket=very_early|"
                        "opponent_race=none|perspective_race=none|supply_used_bucket=b0|"
                        "upgrade_progress_presence=no|visible_enemy_presence_bucket=none|"
                        "worker_count_bucket=b0"
                    ),
                    frame_ref=frame_ref,
                ),
            )

    return traces
