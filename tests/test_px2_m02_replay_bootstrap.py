"""PX2-M02 — replay-bootstrap pipeline fixture tests (CPU, tiny train/eval)."""

from __future__ import annotations

import random
from pathlib import Path

import torch
from starlab.sc2.px2.bootstrap.dataset_contract import load_examples_from_dataset_file
from starlab.sc2.px2.bootstrap.emit_replay_bootstrap_dataset import emit_from_corpus
from starlab.sc2.px2.bootstrap.evaluate_bootstrap import evaluate_examples
from starlab.sc2.px2.bootstrap.feature_adapter import observation_feature_dim
from starlab.sc2.px2.bootstrap.policy_model import BootstrapTerranPolicy
from starlab.sc2.px2.bootstrap.replay_labeler import label_examples_from_bundle_directory
from starlab.sc2.px2.bootstrap.training_run import train_bootstrap_epochs

CORPUS = Path(__file__).resolve().parent / "fixtures" / "px2_m02" / "corpus"


def _seed_deterministic() -> None:
    random.seed(0)
    torch.manual_seed(0)


def test_labeler_emits_terran_examples() -> None:
    train_b = CORPUS / "replay_train_bundle"
    ex, skips = label_examples_from_bundle_directory(train_b)
    assert len(ex) == 3
    assert {e.action_id for e in ex} == {"build_refinery", "build_barracks", "train_marine"}
    assert all("skip" not in s[0] for s in skips)


def test_emit_dataset_json_roundtrip(tmp_path: Path) -> None:
    emit_from_corpus(CORPUS, tmp_path)
    ds_path = tmp_path / "px2_replay_bootstrap_dataset.json"
    examples = load_examples_from_dataset_file(ds_path)
    assert len(examples) == 5
    splits = {str(e["split"]) for e in examples}
    assert splits <= {"train", "eval"}
    train_n = sum(1 for e in examples if e["split"] == "train")
    eval_n = sum(1 for e in examples if e["split"] == "eval")
    assert train_n == 3 and eval_n == 2


def test_training_eval_end_to_end_beats_majority_baseline(tmp_path: Path) -> None:
    _seed_deterministic()
    emit_from_corpus(CORPUS, tmp_path)
    examples = load_examples_from_dataset_file(tmp_path / "px2_replay_bootstrap_dataset.json")
    train_ex = [e for e in examples if e["split"] == "train"]
    eval_ex = [e for e in examples if e["split"] == "eval"]
    assert len(train_ex) >= 1 and len(eval_ex) >= 1

    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    train_bootstrap_epochs(model, train_ex, epochs=200, lr=0.08, device=torch.device("cpu"))

    report = evaluate_examples(model, eval_ex, device=torch.device("cpu"))
    m = report.metrics
    assert float(m["baseline_majority_action_acc"]) <= 0.6
    assert float(m["accuracy_action_argmax_raw"]) >= float(m["baseline_majority_action_acc"])
    assert float(m["compile_success_rate"]) >= 0.99


def test_legality_decode_always_compiles_on_fixture(tmp_path: Path) -> None:
    _seed_deterministic()
    emit_from_corpus(CORPUS, tmp_path)
    examples = load_examples_from_dataset_file(tmp_path / "px2_replay_bootstrap_dataset.json")
    model = BootstrapTerranPolicy(input_dim=observation_feature_dim())
    train_bootstrap_epochs(model, examples, epochs=80, lr=0.1, device=torch.device("cpu"))
    report = evaluate_examples(model, examples, device=torch.device("cpu"))
    assert float(report.metrics["compile_success_rate"]) == 1.0
