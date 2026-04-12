"""Replay-imitation training: M26 + M14 → sklearn classifier + M41 run artifacts."""

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

from starlab.imitation.baseline_fit import collect_imitation_example_rows
from starlab.imitation.baseline_models import FEATURE_POLICY_ID as M27_FEATURE_POLICY_ID
from starlab.imitation.dataset_models import (
    LABEL_POLICY_ID as M26_LABEL_POLICY_ID_CONST,
)
from starlab.imitation.dataset_models import (
    SELECTION_POLICY_ID,
    SPLIT_POLICY_ID,
)
from starlab.imitation.replay_imitation_training_io import (
    compute_deterministic_run_id,
    minimal_report_from_run,
    seal_training_run_body,
    sha256_hex_file,
    write_replay_imitation_training_artifacts,
)
from starlab.imitation.replay_imitation_training_models import (
    ENCODING_POLICY_ID,
    MODEL_FAMILY,
    NON_CLAIMS_V1,
    REPLAY_IMITATION_TRAINING_RUN_VERSION,
    WEIGHTS_ARTIFACT_BASENAME,
    WEIGHTS_SUBDIR,
)
from starlab.training.training_program_io import build_agent_training_program_contract


def parse_context_signature_to_feature_dict(signature: str) -> dict[str, str]:
    """Parse M27 ``context_signature`` string into categorical key→value features."""

    out: dict[str, str] = {}
    for part in signature.split("|"):
        if "=" not in part:
            continue
        key, _, val = part.partition("=")
        if key:
            out[key] = val
    return out


TRAINER_CONFIG_V1: dict[str, Any] = {
    "kind": "sklearn.linear_model.LogisticRegression",
    "max_iter": 1000,
    "note": "multiclass uses multinomial loss with solver=lbfgs (sklearn>=1.3)",
    "solver": "lbfgs",
}

RUN_IDENTITY_VERSION = "starlab.replay_imitation_training_run_identity.v1"
SKLEARN_BUNDLE_SCHEMA = "starlab.m41.sklearn_bundle.v1"


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


def _split_metrics(
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


def build_replay_imitation_training_run(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    seed: int,
    training_program_contract: dict[str, Any] | None = None,
    run_id_override: str | None = None,
    emit_weights: bool = True,
    output_dir: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path | None]:
    """Train sklearn classifier and build run + report dicts; optionally write joblib weights.

    When ``emit_weights`` is True and ``output_dir`` is set, writes
    ``weights/replay_imitation_sklearn_bundle.joblib`` under ``output_dir``.
    """

    contract = training_program_contract or build_agent_training_program_contract()
    contract_sha = contract["contract_sha256"]
    contract_ver = contract["program_version"]

    rows, row_warnings = collect_imitation_example_rows(dataset=dataset, bundle_dirs=bundle_dirs)

    x_dicts = [parse_context_signature_to_feature_dict(sig) for _eid, _sp, _lab, sig in rows]
    y_all = [lab for _eid, _sp, lab, _sig in rows]

    train_idx = [i for i, r in enumerate(rows) if r[1] == "train"]
    if not train_idx:
        msg = "no training examples (split=train)"
        raise ValueError(msg)

    y_train_labels = [y_all[i] for i in train_idx]
    uniq_train_labels = set(y_train_labels)
    if len(uniq_train_labels) < 2:
        msg = "need at least two distinct labels on the train split for logistic regression"
        raise ValueError(msg)

    x_train = [x_dicts[i] for i in train_idx]
    vectorizer = DictVectorizer(sparse=False, sort=True)
    x_train_m = vectorizer.fit_transform(x_train)

    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train_labels)

    clf = LogisticRegression(
        max_iter=int(TRAINER_CONFIG_V1["max_iter"]),
        random_state=seed,
        solver=str(TRAINER_CONFIG_V1["solver"]),
    )
    clf.fit(x_train_m, y_train_enc)

    feature_names = list(vectorizer.get_feature_names_out())

    y_pred_by_eid: dict[str, str] = {}
    for i, row in enumerate(rows):
        eid = row[0]
        xd = x_dicts[i]
        xm = vectorizer.transform([xd])
        pred_enc = clf.predict(xm)[0]
        y_pred_by_eid[eid] = str(label_encoder.inverse_transform([pred_enc])[0])

    split_metrics = _split_metrics(rows=rows, y_pred_by_eid=y_pred_by_eid)

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

    identity: dict[str, Any] = {
        "dataset_sha256": dsha,
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "label_policy_id": lab_pol,
        "model_family": MODEL_FAMILY,
        "run_identity_version": RUN_IDENTITY_VERSION,
        "seed": seed,
        "selection_policy_id": sel_pol,
        "split_policy_id": spl_pol,
        "trainer_config": TRAINER_CONFIG_V1,
        "training_program_contract_sha256": contract_sha,
    }
    deterministic_run_id = compute_deterministic_run_id(identity_payload=identity)
    if run_id_override:
        run_id = run_id_override
        run_id_derivation = "operator_override"
    else:
        run_id = deterministic_run_id
        run_id_derivation = "deterministic_v1"

    label_vocab = [str(x) for x in label_encoder.classes_.tolist()]

    feature_schema: dict[str, Any] = {
        "context_signature_component_keys": sorted(
            {k for d in x_dicts for k in d.keys()},
        ),
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "label_vocabulary": label_vocab,
        "ordered_feature_names": feature_names,
    }

    all_warnings = sorted(
        set(row_warnings + [str(w) for w in dataset.get("warnings", []) if isinstance(w, str)])
    )

    sklearn_bundle: dict[str, Any] = {
        "classifier": clf,
        "dict_vectorizer": vectorizer,
        "encoding_policy_id": ENCODING_POLICY_ID,
        "feature_policy_id": M27_FEATURE_POLICY_ID,
        "label_encoder": label_encoder,
        "schema_version": SKLEARN_BUNDLE_SCHEMA,
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

    caveats = [
        "ci_validates_fixture_only_cpu_path_no_gpu_no_live_sc2",
        "weights_local_sidecar_not_repo",
    ]

    body_pre: dict[str, Any] = {
        "caveats": caveats,
        "deterministic_run_id": deterministic_run_id,
        "example_counts_by_split": example_counts_by_split,
        "feature_schema": feature_schema,
        "model_family": MODEL_FAMILY,
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
        "training_run_version": REPLAY_IMITATION_TRAINING_RUN_VERSION,
        "warnings": all_warnings,
        "weights_sidecar": weights_sidecar,
    }

    run = seal_training_run_body(body_pre)
    report = minimal_report_from_run(run)
    return run, report, weights_path


def write_replay_imitation_training_pipeline_artifacts(
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
    run, rep, _wp = build_replay_imitation_training_run(
        dataset=raw,
        bundle_dirs=bundle_dirs,
        emit_weights=emit_weights,
        output_dir=output_dir,
        run_id_override=run_id,
        seed=seed,
    )
    return write_replay_imitation_training_artifacts(
        output_dir=output_dir,
        report_body=rep,
        run_body=run,
    )
