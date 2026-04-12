"""Hierarchical training: M26 + M14 → manager + worker sklearn + M43 run artifacts."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import joblib
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder

from starlab.hierarchy.delegate_policy import (
    DELEGATE_IDS,
    DELEGATE_POLICY_ID,
    delegate_id_for_coarse_label,
)
from starlab.hierarchy.hierarchical_interface_models import TRACE_DOCUMENT_SCHEMA_VERSION
from starlab.hierarchy.hierarchical_training_io import (
    compute_deterministic_run_id,
    minimal_report_from_run,
    seal_training_run_body,
    sha256_hex_file,
    write_hierarchical_training_artifacts,
)
from starlab.hierarchy.hierarchical_training_models import (
    ENCODING_POLICY_ID,
    HIERARCHICAL_TRAINING_RUN_VERSION,
    MANAGER_MODEL_FAMILY_ID,
    NON_CLAIMS_V1,
    RUN_IDENTITY_VERSION,
    SKLEARN_BUNDLE_SCHEMA,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
    WORKER_MODEL_FAMILY_ID,
)
from starlab.imitation.baseline_fit import collect_imitation_example_rows
from starlab.imitation.baseline_models import FEATURE_POLICY_ID as M27_FEATURE_POLICY_ID
from starlab.imitation.dataset_models import LABEL_POLICY_ID as M26_LABEL_POLICY_ID_CONST
from starlab.imitation.dataset_models import SELECTION_POLICY_ID, SPLIT_POLICY_ID
from starlab.imitation.replay_imitation_training_pipeline import (
    parse_context_signature_to_feature_dict,
)
from starlab.training.training_program_io import build_agent_training_program_contract

TRAINER_CONFIG_V1: dict[str, Any] = {
    "kind": "sklearn.linear_model.LogisticRegression",
    "max_iter": 1000,
    "note": "multiclass uses multinomial loss with solver=lbfgs (sklearn>=1.3)",
    "solver": "lbfgs",
}


def _majority_label(counts: Counter[str]) -> str:
    if not counts:
        msg = "empty label counts for majority"
        raise ValueError(msg)
    best_n = max(counts.values())
    candidates = sorted([lab for lab, c in counts.items() if c == best_n])
    return candidates[0]


def _bundle_lineage_refs(dataset: dict[str, Any]) -> list[dict[str, str]]:
    examples = dataset.get("examples")
    if not isinstance(examples, list):
        return []
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        bid = ex.get("bundle_id")
        lr = ex.get("lineage_root")
        if not isinstance(bid, str) or not isinstance(lr, str):
            continue
        key = (bid, lr)
        if key in seen:
            continue
        seen.add(key)
        out.append({"bundle_id": bid, "lineage_root": lr})
    out.sort(key=lambda x: (x["bundle_id"], x["lineage_root"]))
    return out


def _split_dict_metrics(
    *,
    rows: list[tuple[str, str, str, str]],
    y_pred_by_eid: dict[str, str],
) -> dict[str, Any]:
    splits: dict[str, list[tuple[str, str]]] = {}
    for eid, sp, lab, _sig in rows:
        splits.setdefault(sp, []).append((eid, lab))

    out: dict[str, Any] = {}
    for sp in sorted(splits.keys()):
        pairs = splits[sp]
        if not pairs:
            continue
        y_true = [lab for _eid, lab in pairs]
        y_pred = [y_pred_by_eid[eid] for eid, _lab in pairs]
        n = len(pairs)
        acc = float(accuracy_score(y_true, y_pred))
        f1m = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
        out[sp] = {
            "accuracy": acc,
            "example_count": n,
            "f1_macro": f1m,
        }
    return out


def build_hierarchical_training_run(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    seed: int,
    training_program_contract: dict[str, Any] | None = None,
    run_id_override: str | None = None,
    emit_weights: bool = True,
    output_dir: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path | None]:
    """Train hierarchical sklearn models; build run + report dicts; optional joblib bundle."""

    contract = training_program_contract or build_agent_training_program_contract()
    contract_sha = contract["contract_sha256"]
    contract_ver = contract["program_version"]

    rows, row_warnings = collect_imitation_example_rows(dataset=dataset, bundle_dirs=bundle_dirs)
    x_dicts = [parse_context_signature_to_feature_dict(sig) for _eid, _sp, _lab, sig in rows]
    y_coarse = [lab for _eid, _sp, lab, _sig in rows]
    y_delegate = [delegate_id_for_coarse_label(lab) for lab in y_coarse]

    train_idx = [i for i, r in enumerate(rows) if r[1] == "train"]
    if not train_idx:
        msg = "no training examples (split=train)"
        raise ValueError(msg)

    train_coarse = [y_coarse[i] for i in train_idx]
    global_majority_label = _majority_label(Counter(train_coarse))

    train_delegate_ids = [y_delegate[i] for i in train_idx]
    uniq_delegates_train = set(train_delegate_ids)
    if len(uniq_delegates_train) < 1:
        msg = "no delegate ids in train split"
        raise ValueError(msg)

    x_train = [x_dicts[i] for i in train_idx]
    vectorizer = DictVectorizer(sparse=False, sort=True)
    x_train_m = vectorizer.fit_transform(x_train)
    feature_names = list(vectorizer.get_feature_names_out())

    manager_clf: LogisticRegression | None = None
    manager_label_encoder: LabelEncoder | None = None
    manager_constant_delegate: str | None = None

    if len(uniq_delegates_train) >= 2:
        manager_label_encoder = LabelEncoder()
        y_m_enc = manager_label_encoder.fit_transform(train_delegate_ids)
        manager_clf = LogisticRegression(
            max_iter=int(TRAINER_CONFIG_V1["max_iter"]),
            random_state=seed,
            solver=str(TRAINER_CONFIG_V1["solver"]),
        )
        manager_clf.fit(x_train_m, y_m_enc)
    else:
        manager_constant_delegate = _majority_label(Counter(train_delegate_ids))

    def manager_predict_delegate(xm: Any) -> str:
        if manager_clf is not None and manager_label_encoder is not None:
            pred_enc = manager_clf.predict(xm)[0]
            return str(manager_label_encoder.inverse_transform([pred_enc])[0])
        assert manager_constant_delegate is not None
        return manager_constant_delegate

    # Worker models per delegate
    worker_entries: dict[str, Any] = {}
    for did in DELEGATE_IDS:
        idx_d = [i for i in train_idx if y_delegate[i] == did]
        train_labels_d = [y_coarse[i] for i in idx_d]
        n_train_d = len(idx_d)
        counts_by_split: dict[str, int] = {}
        for sp in ("train", "validation", "test"):
            counts_by_split[sp] = sum(
                1 for j, r in enumerate(rows) if r[1] == sp and y_delegate[j] == did
            )

        if n_train_d == 0:
            worker_entries[did] = {
                "classifier": None,
                "label_encoder": None,
                "fallback_label": global_majority_label,
                "coverage": {
                    "counts_by_split": counts_by_split,
                    "trained_worker": False,
                    "fallback_active": True,
                    "fallback_reason": "zero_train_examples",
                },
            }
            continue

        uniq_labs = set(train_labels_d)
        if len(uniq_labs) < 2:
            const_lab = _majority_label(Counter(train_labels_d))
            worker_entries[did] = {
                "classifier": None,
                "label_encoder": None,
                "fallback_label": const_lab,
                "coverage": {
                    "counts_by_split": counts_by_split,
                    "trained_worker": False,
                    "fallback_active": True,
                    "fallback_reason": "single_class_train",
                },
            }
            continue

        x_sub = vectorizer.transform([x_dicts[i] for i in idx_d])
        w_enc = LabelEncoder()
        y_w = w_enc.fit_transform(train_labels_d)
        w_clf = LogisticRegression(
            max_iter=int(TRAINER_CONFIG_V1["max_iter"]),
            random_state=seed,
            solver=str(TRAINER_CONFIG_V1["solver"]),
        )
        w_clf.fit(x_sub, y_w)
        worker_entries[did] = {
            "classifier": w_clf,
            "label_encoder": w_enc,
            "fallback_label": None,
            "coverage": {
                "counts_by_split": counts_by_split,
                "trained_worker": True,
                "fallback_active": False,
                "fallback_reason": None,
            },
        }

    def worker_predict_label(delegate_id: str, xd: dict[str, str]) -> str:
        we = worker_entries[delegate_id]
        xm = vectorizer.transform([xd])
        if we["classifier"] is not None and we["label_encoder"] is not None:
            pred_enc = we["classifier"].predict(xm)[0]
            return str(we["label_encoder"].inverse_transform([pred_enc])[0])
        assert we["fallback_label"] is not None
        return str(we["fallback_label"])

    y_pred_delegate_by_eid: dict[str, str] = {}
    y_pred_e2e_by_eid: dict[str, str] = {}
    y_pred_worker_oracle_by_eid: dict[str, str] = {}

    for i, row in enumerate(rows):
        eid = row[0]
        xd = x_dicts[i]
        xm = vectorizer.transform([xd])
        pred_del = manager_predict_delegate(xm)
        y_pred_delegate_by_eid[eid] = pred_del
        true_del = y_delegate[i]
        y_pred_worker_oracle_by_eid[eid] = worker_predict_label(true_del, xd)
        y_pred_e2e_by_eid[eid] = worker_predict_label(pred_del, xd)

    split_metrics = {
        "manager": _split_dict_metrics(rows=rows, y_pred_by_eid=y_pred_delegate_by_eid),
        "worker_conditioned_on_oracle_delegate": _split_dict_metrics(
            rows=rows,
            y_pred_by_eid=y_pred_worker_oracle_by_eid,
        ),
        "end_to_end_label": _split_dict_metrics(rows=rows, y_pred_by_eid=y_pred_e2e_by_eid),
    }

    split_totals: Counter[str] = Counter()
    for _eid, sp, _lab, _sig in rows:
        split_totals[sp] += 1
    example_counts_by_split = {k: int(split_totals[k]) for k in sorted(split_totals.keys())}

    dsha = dataset["dataset_sha256"]
    if not isinstance(dsha, str):
        msg = "dataset_sha256 must be a string"
        raise ValueError(msg)

    sel_pol = dataset.get("selection_policy_id", SELECTION_POLICY_ID)
    spl_pol = dataset.get("split_policy_id", SPLIT_POLICY_ID)
    lab_pol = dataset.get("label_policy_id", M26_LABEL_POLICY_ID_CONST)
    if not isinstance(sel_pol, str) or not isinstance(spl_pol, str) or not isinstance(lab_pol, str):
        msg = "dataset policy ids must be strings"
        raise ValueError(msg)

    roots = dataset.get("source_lineage_roots")
    if not isinstance(roots, list):
        roots_list: list[str] = []
    else:
        roots_list = [str(x) for x in roots if isinstance(x, str)]

    coarse_vocab = sorted({str(x) for x in y_coarse})

    identity: dict[str, Any] = {
        "dataset_sha256": dsha,
        "delegate_policy_id": DELEGATE_POLICY_ID,
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "label_policy_id": lab_pol,
        "manager_model_family_id": MANAGER_MODEL_FAMILY_ID,
        "run_identity_version": RUN_IDENTITY_VERSION,
        "seed": seed,
        "selection_policy_id": sel_pol,
        "split_policy_id": spl_pol,
        "trainer_config": TRAINER_CONFIG_V1,
        "training_program_contract_sha256": contract_sha,
        "worker_model_family_id": WORKER_MODEL_FAMILY_ID,
    }
    deterministic_run_id = compute_deterministic_run_id(identity_payload=identity)
    if run_id_override:
        run_id = run_id_override
        run_id_derivation = "operator_override"
    else:
        run_id = deterministic_run_id
        run_id_derivation = "deterministic_v1"

    feature_schema: dict[str, Any] = {
        "coarse_label_vocabulary": coarse_vocab,
        "context_signature_component_keys": sorted({k for d in x_dicts for k in d.keys()}),
        "delegate_ids": list(DELEGATE_IDS),
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "label_policy_id": lab_pol,
        "ordered_feature_names": feature_names,
    }

    delegate_coverage = [
        {
            "delegate_id": did,
            **worker_entries[did]["coverage"],
        }
        for did in DELEGATE_IDS
    ]

    sklearn_bundle: dict[str, Any] = {
        "delegate_policy_id": DELEGATE_POLICY_ID,
        "dict_vectorizer": vectorizer,
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "global_majority_label": global_majority_label,
        "manager": {
            "classifier": manager_clf,
            "constant_delegate_id": manager_constant_delegate,
            "label_encoder": manager_label_encoder,
        },
        "schema_version": SKLEARN_BUNDLE_SCHEMA,
        "workers": {
            did: {
                "classifier": worker_entries[did]["classifier"],
                "fallback_label": worker_entries[did]["fallback_label"],
                "label_encoder": worker_entries[did]["label_encoder"],
            }
            for did in DELEGATE_IDS
        },
    }

    weights_path: Path | None = None
    weights_sidecar: dict[str, Any] | None = None
    if emit_weights and output_dir is not None:
        wdir = output_dir / WEIGHTS_SUBDIR
        wdir.mkdir(parents=True, exist_ok=True)
        weights_path = wdir / WEIGHTS_ARTIFACT_BASENAME
        joblib.dump(sklearn_bundle, weights_path)
        rel = f"{WEIGHTS_SUBDIR}/{WEIGHTS_ARTIFACT_BASENAME}"
        sz = weights_path.stat().st_size
        weights_sidecar = {
            "artifact_sha256": sha256_hex_file(weights_path),
            "byte_size": int(sz),
            "format": "joblib",
            "relative_path": rel,
            "schema": SKLEARN_BUNDLE_SCHEMA,
        }

    all_warnings = sorted(
        set(row_warnings + [str(w) for w in dataset.get("warnings", []) if isinstance(w, str)])
    )

    caveats = [
        "ci_validates_fixture_only_cpu_path_no_gpu_no_live_sc2",
        "weights_local_sidecar_not_repo",
    ]

    manager_trained = manager_clf is not None

    body_pre: dict[str, Any] = {
        "caveats": caveats,
        "delegate_coverage": delegate_coverage,
        "delegate_policy_id": DELEGATE_POLICY_ID,
        "deterministic_run_id": deterministic_run_id,
        "example_counts_by_split": example_counts_by_split,
        "feature_schema": feature_schema,
        "global_majority_label_fallback": global_majority_label,
        "interface_trace_schema_version": TRACE_DOCUMENT_SCHEMA_VERSION,
        "manager_model_family_id": MANAGER_MODEL_FAMILY_ID,
        "manager_trained": manager_trained,
        "non_claims": sorted(NON_CLAIMS_V1),
        "run_id": run_id,
        "run_id_derivation": run_id_derivation,
        "seed": seed,
        "sklearn_version": sklearn.__version__,
        "source_dataset": {
            "dataset_sha256": dsha,
            "dataset_version": dataset.get("dataset_version"),
            "label_policy_id": lab_pol,
            "selection_policy_id": sel_pol,
            "source_lineage_roots": roots_list,
            "split_policy_id": spl_pol,
        },
        "bundle_lineage_refs": _bundle_lineage_refs(dataset),
        "split_metrics": split_metrics,
        "trainer_config": TRAINER_CONFIG_V1,
        "training_program_contract_sha256": contract_sha,
        "training_program_contract_version": contract_ver,
        "training_run_version": HIERARCHICAL_TRAINING_RUN_VERSION,
        "warnings": all_warnings,
        "weights_sidecar": weights_sidecar,
        "worker_model_family_id": WORKER_MODEL_FAMILY_ID,
    }

    run = seal_training_run_body(body_pre)
    report = minimal_report_from_run(run)
    return run, report, weights_path


def write_hierarchical_training_pipeline_artifacts(
    *,
    dataset_path: Path,
    bundle_dirs: list[Path],
    output_dir: Path,
    seed: int,
    run_id: str | None = None,
    emit_weights: bool = True,
) -> tuple[Path, Path]:
    """Load dataset JSON from disk, train, emit run + report (+ optional weights)."""

    raw = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "dataset JSON root must be an object"
        raise ValueError(msg)
    run, rep, _wp = build_hierarchical_training_run(
        bundle_dirs=bundle_dirs,
        dataset=raw,
        emit_weights=emit_weights,
        output_dir=output_dir,
        run_id_override=run_id,
        seed=seed,
    )
    return write_hierarchical_training_artifacts(
        output_dir=output_dir,
        report_body=rep,
        run_body=run,
    )
