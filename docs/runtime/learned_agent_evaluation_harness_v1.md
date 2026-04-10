# Learned-agent evaluation harness (M28) — runtime contract v1

## Purpose

Define the **bounded, offline** evaluation surface for a **frozen** M27 `replay_imitation_baseline.json` against a governed **M20** `fixture_only` benchmark contract, using held-out examples from a governed **M26** `replay_training_dataset.json` and referenced **M14** bundle directories.

This contract is **evaluation only**. It does **not** train models, assert benchmark integrity, run live SC2, or add tournament/diagnostics/evidence-pack semantics.

## Inputs

| Input | Role |
| ----- | ---- |
| Benchmark contract JSON | M20-validated; `measurement_surface` = `fixture_only`; `subject_kinds_allowed` includes `imitation`; four metric definitions (`accuracy`, `macro_f1`, `fallback_rate`, `example_count`) in fixed order |
| `replay_imitation_baseline.json` | Frozen M27 baseline; must match dataset `training_dataset_sha256` and `label_policy_id`; `model_family` as governed for M28 v1 |
| `replay_training_dataset.json` | M26 dataset; examples reference bundle ids and `observation_request` |
| M14 bundle directories | One directory per referenced `bundle_id`; **exact** set match — no missing and no extra `--bundle` paths |

## Held-out split (v1)

Evaluation uses **`split == "test"`** only, as recorded on the M26 dataset. No alternate partitioning.

## Materialization

Observations are produced via the existing in-process **M16 → M18** seam (`replay_observation_materialization`). M28 product modules do **not** parse replays or import `starlab.replays`, `starlab.sc2`, or `s2protocol`.

## Prediction

Predictions use the frozen baseline **signature table** and **global fallback** label (same rule as M27), via `replay_imitation_predictor`.

## Primary artifacts

| File | `schema_version` / version field |
| ---- | ---------------------------------- |
| `learned_agent_evaluation.json` | `starlab.learned_agent_evaluation.v1` |
| `learned_agent_evaluation_report.json` | `starlab.learned_agent_evaluation_report.v1` |

Both are **canonical JSON** (sorted keys, deterministic arrays). The evaluation artifact embeds one **M20-compatible** `scorecard` object validated against the benchmark scorecard schema.

## Metrics (v1)

| `metric_id` | Role | Notes |
| ----------- | ---- | ----- |
| `accuracy` | primary | Classification accuracy on the held-out split |
| `macro_f1` | secondary | Macro-averaged F1 over `label_vocabulary` from the baseline |
| `fallback_rate` | secondary | Fraction of predictions using global fallback |
| `example_count` | informational | Count of evaluated examples |

## Explicit non-claims

Embedded in artifacts (see `starlab.evaluation.learned_agent_models.NON_CLAIMS_V1`), including at minimum: not benchmark integrity, not leaderboard validity, not live SC2 execution, not replay↔execution equivalence, not M23–M25 surfaces.

## CLI

`python -m starlab.evaluation.emit_learned_agent_evaluation` with `--contract`, `--baseline`, `--dataset`, repeated `--bundle`, and `--output-dir`. Optional `--evaluation-split` defaults to `test` (only supported value in v1).
