"""Learned-agent evaluation harness over frozen M27 baseline + M26 test split (M28)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from starlab.benchmarks.benchmark_contract_schema import validate_benchmark_contract
from starlab.benchmarks.benchmark_scorecard_schema import validate_benchmark_scorecard
from starlab.evaluation.learned_agent_metrics import accuracy, label_counts, macro_f1
from starlab.evaluation.learned_agent_models import (
    EVALUATION_REPORT_VERSION,
    EVALUATION_VERSION,
    M28_METRIC_IDS_ORDERED,
    NON_CLAIMS_V1,
)
from starlab.evaluation.m14_bundle_loader import M14BundleLoader, default_load_m14_bundle
from starlab.imitation.baseline_features import build_context_signature
from starlab.imitation.baseline_models import MODEL_FAMILY
from starlab.imitation.dataset_models import REPLAY_TRAINING_DATASET_VERSION
from starlab.imitation.replay_imitation_predictor import FrozenImitationPredictor
from starlab.imitation.replay_observation_materialization import (
    materialize_observation_for_observation_request,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def index_bundle_directories_for_dataset(
    *,
    bundle_dirs: list[Path],
    required_bundle_ids: set[str],
    bundle_loader: M14BundleLoader | None = None,
) -> dict[str, Path]:
    """Map ``bundle_id`` → resolved bundle directory path.

    Rejects ``--bundle`` directories whose manifest ``bundle_id`` is not listed in the dataset.
    Requires every ``required_bundle_id`` to appear exactly once.
    """

    if not required_bundle_ids:
        msg = "dataset references no bundle_id values"
        raise ValueError(msg)

    loader = bundle_loader if bundle_loader is not None else default_load_m14_bundle
    seen: dict[str, Path] = {}
    for d in sorted(bundle_dirs, key=lambda p: str(p.resolve())):
        bundle, err = loader(d)
        if bundle is None:
            msg = err or f"failed to load bundle directory {d}"
            raise ValueError(msg)
        bid = bundle.manifest.get("bundle_id")
        if not isinstance(bid, str) or not bid:
            msg = f"bundle manifest at {d} missing bundle_id"
            raise ValueError(msg)
        if bid not in required_bundle_ids:
            msg = f"extra --bundle not referenced by dataset: bundle_id {bid!r}"
            raise ValueError(msg)
        if bid in seen:
            msg = f"duplicate --bundle for bundle_id {bid!r}"
            raise ValueError(msg)
        seen[bid] = d.resolve()

    missing = required_bundle_ids - seen.keys()
    if missing:
        msg = f"missing --bundle for bundle_id(s): {sorted(missing)}"
        raise ValueError(msg)
    return seen


def evaluate_predictor_on_test_split(
    *,
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    evaluation_split: str,
    predict_sig: Callable[[str], tuple[str, bool]],
    label_vocabulary: Sequence[str],
    bundle_loader: M14BundleLoader | None = None,
) -> tuple[dict[str, float | int], list[str], list[str], list[str], int]:
    """M28 metric surface: evaluate one predictor on the held-out split (shared with M42).

    ``label_vocabulary`` supplies the macro-F1 label universe (baseline or M41 schema).

    Returns metric_values (four M28 keys), warnings, y_true, y_pred, fallback_count.
    """

    dv = dataset.get("dataset_version")
    if dv != REPLAY_TRAINING_DATASET_VERSION:
        msg = f"unsupported dataset_version {dv!r}"
        raise ValueError(msg)

    dsha = dataset.get("dataset_sha256")
    if not isinstance(dsha, str) or len(dsha) != 64:
        msg = "dataset.dataset_sha256 must be a 64-char hex string"
        raise ValueError(msg)

    examples = dataset.get("examples")
    if not isinstance(examples, list) or not examples:
        msg = "dataset.examples must be a non-empty array"
        raise ValueError(msg)

    required_ids: set[str] = set()
    for ex in examples:
        if isinstance(ex, dict):
            bid = ex.get("bundle_id")
            if isinstance(bid, str) and bid:
                required_ids.add(bid)

    bundle_index = index_bundle_directories_for_dataset(
        bundle_dirs=bundle_dirs,
        required_bundle_ids=required_ids,
        bundle_loader=bundle_loader,
    )

    all_warnings: list[str] = []
    dw = dataset.get("warnings")
    if isinstance(dw, list):
        for w in dw:
            if isinstance(w, str):
                all_warnings.append(w)

    y_true: list[str] = []
    y_pred: list[str] = []
    fallback_flags: list[bool] = []

    for ex in examples:
        if not isinstance(ex, dict):
            msg = "each example must be an object"
            raise ValueError(msg)
        if ex.get("split") != evaluation_split:
            continue

        eid = ex.get("example_id")
        lab = ex.get("target_semantic_kind")
        oreq = ex.get("observation_request")
        bid = ex.get("bundle_id")
        if not isinstance(eid, str) or not isinstance(lab, str):
            msg = f"example missing example_id or target_semantic_kind: {ex!r}"
            raise ValueError(msg)
        if not isinstance(oreq, dict):
            msg = f"example {eid}: observation_request must be an object"
            raise ValueError(msg)
        if not isinstance(bid, str):
            msg = f"example {eid}: bundle_id must be a string"
            raise ValueError(msg)

        bdir = bundle_index[bid]
        cs, obs, _rep, warns = materialize_observation_for_observation_request(
            bundle_dir=bdir,
            observation_request=oreq,
        )
        all_warnings.extend(warns)

        ppi = ex.get("perspective_player_index")
        ppi_i = int(ppi) if isinstance(ppi, int) and not isinstance(ppi, bool) else -1
        sig = build_context_signature(
            observation_frame=obs,
            canonical_state=cs,
            perspective_player_index=ppi_i,
        )
        pred, used_fb = predict_sig(sig)
        y_true.append(lab)
        y_pred.append(pred)
        fallback_flags.append(used_fb)

    if not y_true:
        msg = f"no examples with split={evaluation_split!r}"
        raise ValueError(msg)

    n = len(y_true)
    fb_count = sum(1 for f in fallback_flags if f)
    fb_rate = float(fb_count) / float(n) if n else 0.0
    acc = accuracy(y_true, y_pred)

    label_list = sorted(set(label_vocabulary))
    mf1 = macro_f1(y_true, y_pred, label_list)

    metric_values: dict[str, float | int] = {
        "accuracy": acc,
        "macro_f1": mf1,
        "fallback_rate": fb_rate,
        "example_count": n,
    }

    warnings_sorted = sorted(set(all_warnings))
    return metric_values, warnings_sorted, y_true, y_pred, fb_count


def _validate_m28_benchmark_contract(benchmark_contract: dict[str, Any]) -> None:
    errs = validate_benchmark_contract(benchmark_contract)
    if errs:
        msg = "invalid benchmark contract: " + "; ".join(errs)
        raise ValueError(msg)

    if benchmark_contract.get("measurement_surface") != "fixture_only":
        msg = "M28 v1 requires measurement_surface fixture_only"
        raise ValueError(msg)

    allowed = benchmark_contract.get("subject_kinds_allowed")
    if not isinstance(allowed, list) or "imitation" not in allowed:
        msg = "M28 v1 requires subject_kinds_allowed to include imitation"
        raise ValueError(msg)

    defs = benchmark_contract.get("metric_definitions")
    if not isinstance(defs, list) or len(defs) != len(M28_METRIC_IDS_ORDERED):
        msg = "M28 v1 benchmark contract must define exactly four metrics"
        raise ValueError(msg)

    got = tuple(str(d.get("metric_id", "")) for d in defs if isinstance(d, dict))
    if got != M28_METRIC_IDS_ORDERED:
        msg = (
            f"M28 v1 metric_definitions metric_id order must be {M28_METRIC_IDS_ORDERED!r}, "
            f"got {got!r}"
        )
        raise ValueError(msg)


def _build_embedded_scorecard(
    *,
    benchmark_contract: dict[str, Any],
    benchmark_contract_sha256: str,
    baseline_sha256: str,
    metric_values: dict[str, float | int],
) -> dict[str, Any]:
    bench_id = str(benchmark_contract["benchmark_id"])
    bench_version = str(benchmark_contract["benchmark_version"])
    defs: list[dict[str, Any]] = list(benchmark_contract["metric_definitions"])
    gating: list[dict[str, Any]] = list(benchmark_contract["gating_rules"])

    metric_rows: list[dict[str, Any]] = []
    for md in defs:
        mid = str(md["metric_id"])
        raw = metric_values[mid]
        val: float | int
        if isinstance(raw, bool):  # pragma: no cover
            msg = "boolean metric values are not supported"
            raise TypeError(msg)
        val = raw
        metric_rows.append(
            {
                "metric_id": mid,
                "unit": str(md["unit"]),
                "value": val,
            },
        )

    gating_outcomes: list[dict[str, Any]] = []
    for rule in gating:
        gating_outcomes.append(
            {
                "detail": None,
                "passed": True,
                "rule_id": str(rule["rule_id"]),
            },
        )

    warnings_sorted = sorted(
        {
            "starlab.m28.warning.fixture_only_learned_eval",
        },
    )
    non_claims_sorted = sorted(
        {
            "starlab.m20.scorecard_non_claim.not_benchmark_integrity",
            "starlab.m20.scorecard_non_claim.not_real_evaluation",
        },
    )

    scorecard: dict[str, Any] = {
        "aggregate_scores": [],
        "benchmark_contract_sha256": benchmark_contract_sha256,
        "benchmark_id": bench_id,
        "benchmark_version": bench_version,
        "comparability_status": "provisional",
        "evaluation_posture": "fixture_only",
        "gating_outcomes": gating_outcomes,
        "metric_rows": metric_rows,
        "non_claims": non_claims_sorted,
        "schema_version": "starlab.benchmark_scorecard.v1",
        "scoring_status": "scored",
        "subject_ref": {
            "subject_id": baseline_sha256,
            "subject_kind": "imitation",
        },
        "warnings": warnings_sorted,
    }

    errs = validate_benchmark_scorecard(scorecard)
    if errs:
        msg = "embedded scorecard failed validation: " + "; ".join(errs)
        raise ValueError(msg)
    return scorecard


def build_learned_agent_evaluation_artifacts(
    *,
    benchmark_contract: dict[str, Any],
    baseline: dict[str, Any],
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    evaluation_split: str = "test",
    bundle_loader: M14BundleLoader | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Evaluate frozen M27 baseline on governed held-out examples; emit evaluation + report."""

    if evaluation_split != "test":
        msg = f"M28 v1 supports evaluation_split 'test' only, got {evaluation_split!r}"
        raise ValueError(msg)

    _validate_m28_benchmark_contract(benchmark_contract)
    benchmark_contract_sha256 = sha256_hex_of_canonical_json(benchmark_contract)

    dv = dataset.get("dataset_version")
    if dv != REPLAY_TRAINING_DATASET_VERSION:
        msg = f"unsupported dataset_version {dv!r}"
        raise ValueError(msg)

    dsha = dataset.get("dataset_sha256")
    if not isinstance(dsha, str) or len(dsha) != 64:
        msg = "dataset.dataset_sha256 must be a 64-char hex string"
        raise ValueError(msg)

    label_policy_dataset = dataset.get("label_policy_id")
    if not isinstance(label_policy_dataset, str) or not label_policy_dataset:
        msg = "dataset.label_policy_id must be a non-empty string"
        raise ValueError(msg)

    if baseline.get("training_dataset_sha256") != dsha:
        msg = "baseline.training_dataset_sha256 does not match dataset.dataset_sha256"
        raise ValueError(msg)

    if baseline.get("label_policy_id") != label_policy_dataset:
        msg = "baseline.label_policy_id does not match dataset.label_policy_id"
        raise ValueError(msg)

    if baseline.get("model_family") != MODEL_FAMILY:
        msg = f"baseline.model_family must be {MODEL_FAMILY!r} for M28 v1"
        raise ValueError(msg)

    predictor = FrozenImitationPredictor.from_baseline_body(baseline)

    vocab = baseline.get("label_vocabulary")
    if not isinstance(vocab, list) or not all(isinstance(x, str) for x in vocab):
        msg = "baseline.label_vocabulary must be a non-empty string array"
        raise ValueError(msg)

    metric_values, warnings_sorted, y_true, y_pred, fb_count = evaluate_predictor_on_test_split(
        dataset=dataset,
        bundle_dirs=bundle_dirs,
        evaluation_split=evaluation_split,
        predict_sig=predictor.predict,
        label_vocabulary=vocab,
        bundle_loader=bundle_loader,
    )

    n = int(metric_values["example_count"])
    fb_rate = float(metric_values["fallback_rate"])

    baseline_sha256 = baseline.get("baseline_sha256")
    if not isinstance(baseline_sha256, str) or len(baseline_sha256) != 64:
        msg = "baseline.baseline_sha256 must be a 64-char hex string"
        raise ValueError(msg)

    scorecard = _build_embedded_scorecard(
        benchmark_contract=benchmark_contract,
        benchmark_contract_sha256=benchmark_contract_sha256,
        baseline_sha256=baseline_sha256,
        metric_values=metric_values,
    )

    feature_policy_id = baseline.get("feature_policy_id")
    if not isinstance(feature_policy_id, str) or not feature_policy_id:
        msg = "baseline.feature_policy_id must be a non-empty string"
        raise ValueError(msg)

    non_claims_sorted = sorted(set(NON_CLAIMS_V1))

    body_pre_hash: dict[str, Any] = {
        "baseline_sha256": baseline_sha256,
        "benchmark_contract_sha256": benchmark_contract_sha256,
        "evaluation_split": evaluation_split,
        "evaluation_version": EVALUATION_VERSION,
        "example_count": n,
        "fallback_count": fb_count,
        "fallback_rate": fb_rate,
        "feature_policy_id": feature_policy_id,
        "label_policy_id": label_policy_dataset,
        "metric_values": {k: metric_values[k] for k in sorted(metric_values.keys())},
        "model_family": MODEL_FAMILY,
        "non_claims": non_claims_sorted,
        "scorecard": scorecard,
        "subject_kind": "imitation",
        "training_dataset_sha256": dsha,
        "warnings": warnings_sorted,
    }

    evaluation_sha256 = sha256_hex_of_canonical_json(body_pre_hash)

    evaluation: dict[str, Any] = {
        **body_pre_hash,
        "evaluation_sha256": evaluation_sha256,
    }

    true_label_dist = label_counts(y_true)
    pred_label_dist = label_counts(y_pred)

    report: dict[str, Any] = {
        "baseline_sha256": baseline_sha256,
        "benchmark_contract_sha256": benchmark_contract_sha256,
        "evaluation_sha256": evaluation_sha256,
        "evaluation_split": evaluation_split,
        "example_count": n,
        "fallback_count": fb_count,
        "fallback_rate": fb_rate,
        "label_counts": {
            "predicted": pred_label_dist,
            "true": true_label_dist,
        },
        "materialization_warnings": list(warnings_sorted),
        "metric_summary": {k: metric_values[k] for k in sorted(metric_values.keys())},
        "non_claims": list(non_claims_sorted),
        "report_version": EVALUATION_REPORT_VERSION,
        "training_dataset_sha256": dsha,
    }

    return evaluation, report


def write_learned_agent_evaluation_artifacts(
    *,
    contract_path: Path,
    baseline_path: Path,
    dataset_path: Path,
    bundle_dirs: list[Path],
    output_dir: Path,
    evaluation_split: str = "test",
    bundle_loader: M14BundleLoader | None = None,
) -> tuple[Path, Path]:
    """Load JSON inputs from disk and write evaluation artifacts."""

    import json

    raw_c = json.loads(contract_path.read_text(encoding="utf-8"))
    raw_b = json.loads(baseline_path.read_text(encoding="utf-8"))
    raw_d = json.loads(dataset_path.read_text(encoding="utf-8"))
    if not isinstance(raw_c, dict) or not isinstance(raw_b, dict) or not isinstance(raw_d, dict):
        msg = "contract, baseline, and dataset JSON roots must be objects"
        raise ValueError(msg)

    ev, rep = build_learned_agent_evaluation_artifacts(
        benchmark_contract=raw_c,
        baseline=raw_b,
        dataset=raw_d,
        bundle_dirs=bundle_dirs,
        evaluation_split=evaluation_split,
        bundle_loader=bundle_loader,
    )

    from starlab.evaluation.learned_agent_models import (
        LEARNED_AGENT_EVALUATION_FILENAME,
        LEARNED_AGENT_EVALUATION_REPORT_FILENAME,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    ep = output_dir / LEARNED_AGENT_EVALUATION_FILENAME
    rp = output_dir / LEARNED_AGENT_EVALUATION_REPORT_FILENAME
    ep.write_text(canonical_json_dumps(ev), encoding="utf-8")
    rp.write_text(canonical_json_dumps(rep), encoding="utf-8")
    return ep, rp
