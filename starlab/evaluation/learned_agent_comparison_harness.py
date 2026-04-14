"""Deterministic learned-agent comparison over M27 + M41 candidates (M42)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from starlab.evaluation.learned_agent_comparison_io import (
    seal_comparison_body,
    write_learned_agent_comparison_artifacts,
)
from starlab.evaluation.learned_agent_comparison_models import (
    CANDIDATE_SOURCE_M27,
    CANDIDATE_SOURCE_M41,
    COMPARISON_REPORT_VERSION,
    COMPARISON_VERSION,
    EVALUATION_SURFACE_ID,
    M42_METRIC_IDS_ORDERED,
    NON_CLAIMS_V1,
    RANKING_POLICY_ID,
)
from starlab.evaluation.learned_agent_evaluation import (
    _validate_m28_benchmark_contract,
    evaluate_predictor_on_test_split,
)
from starlab.evaluation.m14_bundle_loader import M14BundleLoader
from starlab.imitation.baseline_models import BASELINE_VERSION
from starlab.imitation.baseline_models import MODEL_FAMILY as M27_MODEL_FAMILY
from starlab.imitation.replay_imitation_predictor import FrozenImitationPredictor
from starlab.imitation.replay_imitation_training_models import (
    REPLAY_IMITATION_TRAINING_RUN_VERSION,
)
from starlab.imitation.trained_run_predictor import (
    TrainedRunPredictor,
    resolve_m41_weights_path,
    verify_weights_sha256,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


@dataclass(frozen=True)
class ComparisonCandidateSpec:
    """One row of comparison input: M27 baseline JSON or M41 training run + run root dir."""

    candidate_id: str
    source_type: str
    source_artifact_path: str
    baseline_body: dict[str, Any] | None = None
    training_run_body: dict[str, Any] | None = None
    training_run_dir: Path | None = None


def _validate_m27_against_dataset(baseline: dict[str, Any], dataset: dict[str, Any]) -> None:
    dsha = dataset.get("dataset_sha256")
    if baseline.get("training_dataset_sha256") != dsha:
        msg = "baseline.training_dataset_sha256 does not match dataset.dataset_sha256"
        raise ValueError(msg)
    if baseline.get("label_policy_id") != dataset.get("label_policy_id"):
        msg = "baseline.label_policy_id does not match dataset.label_policy_id"
        raise ValueError(msg)
    if baseline.get("model_family") != M27_MODEL_FAMILY:
        msg = f"baseline.model_family must be {M27_MODEL_FAMILY!r} for M42 v1"
        raise ValueError(msg)
    bv = baseline.get("baseline_version")
    if bv != BASELINE_VERSION:
        msg = f"unsupported baseline_version {bv!r}"
        raise ValueError(msg)


def _validate_m41_training_program_contract_identity(
    *,
    training_program_contract: dict[str, Any],
    candidates: list[ComparisonCandidateSpec],
) -> None:
    """Require M41 runs to match the active M40 charter used for this comparison (M48)."""

    tc_sha = training_program_contract.get("contract_sha256")
    tc_ver = training_program_contract.get("program_version")
    if not isinstance(tc_sha, str) or not isinstance(tc_ver, str):
        msg = "active training program contract must include contract_sha256 and program_version"
        raise ValueError(msg)

    for spec in candidates:
        if spec.source_type != CANDIDATE_SOURCE_M41:
            continue
        tr = spec.training_run_body
        if tr is None:
            continue
        r_sha = tr.get("training_program_contract_sha256")
        r_ver = tr.get("training_program_contract_version")
        if r_sha != tc_sha:
            msg = (
                f"M41 candidate {spec.candidate_id!r}: training_program_contract_sha256 "
                f"{r_sha!r} does not match active M40 training-program contract {tc_sha!r}"
            )
            raise ValueError(msg)
        if r_ver != tc_ver:
            msg = (
                f"M41 candidate {spec.candidate_id!r}: training_program_contract_version "
                f"{r_ver!r} does not match active M40 training-program contract {tc_ver!r}"
            )
            raise ValueError(msg)


def _validate_m41_against_dataset(training_run: dict[str, Any], dataset: dict[str, Any]) -> None:
    if training_run.get("training_run_version") != REPLAY_IMITATION_TRAINING_RUN_VERSION:
        msg = f"unsupported training_run_version {training_run.get('training_run_version')!r}"
        raise ValueError(msg)
    src = training_run.get("source_dataset")
    if not isinstance(src, dict):
        msg = "training_run.source_dataset must be an object"
        raise ValueError(msg)
    if src.get("dataset_sha256") != dataset.get("dataset_sha256"):
        msg = "M41 run source_dataset.dataset_sha256 does not match evaluation dataset"
        raise ValueError(msg)
    if src.get("label_policy_id") != dataset.get("label_policy_id"):
        msg = "M41 run source_dataset.label_policy_id does not match evaluation dataset"
        raise ValueError(msg)
    fs = training_run.get("feature_schema")
    if not isinstance(fs, dict) or not isinstance(fs.get("label_vocabulary"), list):
        msg = "M41 training run must include feature_schema.label_vocabulary"
        raise ValueError(msg)


def _pairwise_metric_deltas(
    *,
    candidate_rows: list[dict[str, Any]],
    fixed_order_ids: list[str],
) -> list[dict[str, Any]]:
    id_to_metrics: dict[str, dict[str, Any]] = {
        str(r["candidate_id"]): dict(r["metrics"]) for r in candidate_rows
    }
    out: list[dict[str, Any]] = []
    for i in range(len(fixed_order_ids)):
        for j in range(i + 1, len(fixed_order_ids)):
            a = fixed_order_ids[i]
            b = fixed_order_ids[j]
            ma = id_to_metrics[a]
            mb = id_to_metrics[b]
            out.append(
                {
                    "pair": [a, b],
                    "delta_accuracy": float(mb["accuracy"]) - float(ma["accuracy"]),
                    "delta_macro_f1": float(mb["macro_f1"]) - float(ma["macro_f1"]),
                    "delta_fallback_rate": float(mb["fallback_rate"]) - float(ma["fallback_rate"]),
                },
            )
    return out


def _rank_ids_by_policy(candidate_rows: list[dict[str, Any]]) -> list[str]:
    ranked = sorted(
        candidate_rows,
        key=lambda r: (
            -float(r["metrics"]["accuracy"]),
            -float(r["metrics"]["macro_f1"]),
            str(r["candidate_id"]),
        ),
    )
    return [str(r["candidate_id"]) for r in ranked]


def build_learned_agent_comparison_artifacts(
    *,
    benchmark_contract: dict[str, Any],
    dataset: dict[str, Any],
    bundle_dirs: list[Path],
    evaluation_split: str,
    training_program_contract: dict[str, Any],
    candidates: list[ComparisonCandidateSpec],
    bundle_loader: M14BundleLoader | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Compare M27 + M41 candidates on the shared M28 metric surface; emit comparison + report."""

    if evaluation_split != "test":
        msg = f"M42 v1 supports evaluation_split 'test' only, got {evaluation_split!r}"
        raise ValueError(msg)
    if not candidates:
        msg = "at least one candidate is required"
        raise ValueError(msg)

    if any(spec.source_type == CANDIDATE_SOURCE_M41 for spec in candidates):
        _validate_m41_training_program_contract_identity(
            training_program_contract=training_program_contract,
            candidates=candidates,
        )

    _validate_m28_benchmark_contract(benchmark_contract)
    benchmark_contract_sha256 = sha256_hex_of_canonical_json(benchmark_contract)
    benchmark_version = str(benchmark_contract["benchmark_version"])

    tc_sha = training_program_contract["contract_sha256"]
    tc_ver = training_program_contract["program_version"]

    dsha = dataset["dataset_sha256"]
    dver = dataset.get("dataset_version")
    if not isinstance(dsha, str):
        msg = "dataset.dataset_sha256 must be a string"
        raise ValueError(msg)

    candidate_rows: list[dict[str, Any]] = []
    fixed_order_ids: list[str] = []

    for spec in candidates:
        if spec.candidate_id in fixed_order_ids:
            msg = f"duplicate candidate_id {spec.candidate_id!r}"
            raise ValueError(msg)
        fixed_order_ids.append(spec.candidate_id)

        if spec.source_type == CANDIDATE_SOURCE_M27:
            if spec.baseline_body is None:
                msg = (
                    f"candidate {spec.candidate_id}: baseline_body required for m27_frozen_baseline"
                )
                raise ValueError(msg)
            _validate_m27_against_dataset(spec.baseline_body, dataset)
            m27_predictor = FrozenImitationPredictor.from_baseline_body(spec.baseline_body)
            vocab = spec.baseline_body.get("label_vocabulary")
            if not isinstance(vocab, list) or not all(isinstance(x, str) for x in vocab):
                msg = "baseline.label_vocabulary must be a non-empty string array"
                raise ValueError(msg)

            metrics, _warns, _yt, _yp, fb_count = evaluate_predictor_on_test_split(
                dataset=dataset,
                bundle_dirs=bundle_dirs,
                evaluation_split=evaluation_split,
                predict_sig=m27_predictor.predict,
                label_vocabulary=vocab,
                bundle_loader=bundle_loader,
            )
            bsha = spec.baseline_body.get("baseline_sha256")
            if not isinstance(bsha, str) or len(bsha) != 64:
                msg = "baseline.baseline_sha256 must be a 64-char hex string"
                raise ValueError(msg)
            row = {
                "candidate_id": spec.candidate_id,
                "candidate_source_type": CANDIDATE_SOURCE_M27,
                "metrics": {k: metrics[k] for k in M42_METRIC_IDS_ORDERED},
                "fallback_count": fb_count,
                "source_artifact": {
                    "artifact_kind": "replay_imitation_baseline",
                    "path": spec.source_artifact_path,
                    "sha256": bsha,
                },
            }
            candidate_rows.append(row)

        elif spec.source_type == CANDIDATE_SOURCE_M41:
            if spec.training_run_body is None or spec.training_run_dir is None:
                msg = (
                    f"candidate {spec.candidate_id}: "
                    "training_run_body and training_run_dir required"
                )
                raise ValueError(msg)
            tr = spec.training_run_body
            _validate_m41_against_dataset(tr, dataset)
            wpath = resolve_m41_weights_path(
                training_run_dir=spec.training_run_dir,
                training_run_body=tr,
            )
            if not wpath.is_file():
                msg = f"M41 weights file not found: {wpath}"
                raise ValueError(msg)
            verify_weights_sha256(weights_path=wpath, training_run_body=tr)
            m41_predictor = TrainedRunPredictor.from_joblib_path(wpath)
            fs = tr["feature_schema"]
            assert isinstance(fs, dict)
            lv = fs["label_vocabulary"]
            assert isinstance(lv, list)
            label_vocab = [str(x) for x in lv]

            metrics, _warns, _yt, _yp, fb_count = evaluate_predictor_on_test_split(
                dataset=dataset,
                bundle_dirs=bundle_dirs,
                evaluation_split=evaluation_split,
                predict_sig=m41_predictor.predict,
                label_vocabulary=label_vocab,
                bundle_loader=bundle_loader,
            )
            tr_sha = tr.get("training_run_sha256")
            if not isinstance(tr_sha, str) or len(tr_sha) != 64:
                msg = "training_run.training_run_sha256 must be a 64-char hex string"
                raise ValueError(msg)
            ws = tr.get("weights_sidecar")
            weights_meta: dict[str, Any] = {}
            if isinstance(ws, dict):
                if isinstance(ws.get("relative_path"), str):
                    weights_meta["relative_path"] = ws["relative_path"]
                if isinstance(ws.get("artifact_sha256"), str):
                    weights_meta["artifact_sha256"] = ws["artifact_sha256"]
            row = {
                "candidate_id": spec.candidate_id,
                "candidate_source_type": CANDIDATE_SOURCE_M41,
                "metrics": {k: metrics[k] for k in M42_METRIC_IDS_ORDERED},
                "fallback_count": fb_count,
                "source_artifact": {
                    "artifact_kind": "replay_imitation_training_run",
                    "path": spec.source_artifact_path,
                    "sha256": tr_sha,
                    "weights": weights_meta,
                },
            }
            candidate_rows.append(row)
        else:
            msg = f"unsupported candidate_source_type {spec.source_type!r}"
            raise ValueError(msg)

    ranked_ids = _rank_ids_by_policy(candidate_rows)
    pairwise = _pairwise_metric_deltas(
        candidate_rows=candidate_rows,
        fixed_order_ids=fixed_order_ids,
    )

    lineage = [
        {
            "candidate_id": r["candidate_id"],
            "candidate_source_type": r["candidate_source_type"],
            "source_sha256": r["source_artifact"]["sha256"],
        }
        for r in candidate_rows
    ]

    non_claims_sorted = sorted(set(NON_CLAIMS_V1))

    body_pre: dict[str, Any] = {
        "benchmark_contract_sha256": benchmark_contract_sha256,
        "benchmark_contract_version": benchmark_version,
        "candidate_rows": candidate_rows,
        "comparison_version": COMPARISON_VERSION,
        "dataset_sha256": dsha,
        "dataset_version": dver,
        "evaluation_split": evaluation_split,
        "evaluation_surface_id": EVALUATION_SURFACE_ID,
        "lineage": lineage,
        "non_claims": non_claims_sorted,
        "pairwise_metric_deltas": pairwise,
        "ranked_candidate_ids": ranked_ids,
        "ranking_policy_id": RANKING_POLICY_ID,
        "training_program_contract_sha256": tc_sha,
        "training_program_contract_version": tc_ver,
    }

    comparison = seal_comparison_body(body_pre)

    report: dict[str, Any] = {
        "comparison_id": comparison["comparison_id"],
        "ranked_candidate_ids": ranked_ids,
        "report_version": COMPARISON_REPORT_VERSION,
        "summary": {
            "benchmark_contract_sha256": benchmark_contract_sha256,
            "candidate_count": len(candidate_rows),
            "dataset_sha256": dsha,
            "ranking_policy_id": RANKING_POLICY_ID,
        },
        "pairwise_metric_deltas": pairwise,
        "candidate_metric_table": [
            {
                "candidate_id": r["candidate_id"],
                "candidate_source_type": r["candidate_source_type"],
                "metrics": r["metrics"],
            }
            for r in candidate_rows
        ],
        "non_claims": list(non_claims_sorted),
        "warnings": [
            "m42_fixture_or_local_comparison_only",
            "fallback_rate_recorded_not_used_in_ranking_v1",
        ],
    }

    return comparison, report


def write_learned_agent_comparison_from_paths(
    *,
    benchmark_contract_path: Path,
    dataset_path: Path,
    bundle_dirs: list[Path],
    training_program_contract: dict[str, Any],
    output_dir: Path,
    baseline_path: Path,
    m41_specs: list[tuple[str, Path, Path]],
    m27_candidate_id: str = "m27_frozen_baseline",
    bundle_loader: M14BundleLoader | None = None,
) -> tuple[Path, Path]:
    """Load JSON from disk: one M27 baseline plus optional M41 run paths."""

    import json

    raw_c = json.loads(benchmark_contract_path.read_text(encoding="utf-8"))
    raw_d = json.loads(dataset_path.read_text(encoding="utf-8"))
    raw_b = json.loads(baseline_path.read_text(encoding="utf-8"))
    if not isinstance(raw_c, dict) or not isinstance(raw_d, dict) or not isinstance(raw_b, dict):
        msg = "contract, dataset, and baseline JSON roots must be objects"
        raise ValueError(msg)

    cand_specs: list[ComparisonCandidateSpec] = [
        ComparisonCandidateSpec(
            candidate_id=m27_candidate_id,
            source_type=CANDIDATE_SOURCE_M27,
            source_artifact_path=str(baseline_path.resolve()),
            baseline_body=raw_b,
        ),
    ]
    for cid, run_path, run_dir in m41_specs:
        raw_run = json.loads(run_path.read_text(encoding="utf-8"))
        if not isinstance(raw_run, dict):
            msg = "M41 training run JSON root must be an object"
            raise ValueError(msg)
        cand_specs.append(
            ComparisonCandidateSpec(
                candidate_id=cid,
                source_type=CANDIDATE_SOURCE_M41,
                source_artifact_path=str(run_path.resolve()),
                training_run_body=raw_run,
                training_run_dir=run_dir.resolve(),
            ),
        )

    comp, rep = build_learned_agent_comparison_artifacts(
        benchmark_contract=raw_c,
        dataset=raw_d,
        bundle_dirs=bundle_dirs,
        evaluation_split="test",
        training_program_contract=training_program_contract,
        candidates=cand_specs,
        bundle_loader=bundle_loader,
    )

    return write_learned_agent_comparison_artifacts(
        comparison_body=comp,
        report_body=rep,
        output_dir=output_dir,
    )
