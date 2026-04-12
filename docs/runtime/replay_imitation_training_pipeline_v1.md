# Replay-imitation training pipeline (M41)

**Version:** `starlab.replay_imitation_training_run.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11  
**Emitter:**  
`python -m starlab.imitation.emit_replay_imitation_training_run --dataset <M26/replay_training_dataset.json> --bundle <M14_bundle_dir> ... --output-dir out/training_runs/<run_id>/`

## Purpose

M41 is the first **governed local-first replay-imitation training** milestone: it consumes governed **M26** datasets and **M14** bundle directories, materializes **M27** `context_signature` features via the existing M16→M18 path, trains a small deterministic **scikit-learn** classifier (logistic regression on one-hot–encoded signature components), and emits governed JSON artifacts. It binds to the **M40** training-program contract via `training_program_contract_version` and `training_program_contract_sha256`.

M41 does **not** claim benchmark integrity, live SC2 in CI, superiority over M27 beyond recorded metrics, or public release of weights.

## Outputs

| File | Role |
| ---- | ---- |
| `replay_imitation_training_run.json` | Full run record: contract binding, dataset identity, policies, trainer config, seed, split metrics, **feature_schema** (ordered feature names, encoding policy, label vocabulary), optional weights sidecar metadata, non-claims |
| `replay_imitation_training_run_report.json` | Compact summary linked by `training_run_sha256` |

Default layout:

```text
out/training_runs/<run_id>/
  replay_imitation_training_run.json
  replay_imitation_training_run_report.json
  weights/
    replay_imitation_sklearn_bundle.joblib   # local-only; not in repo
```

## Local vs CI

- **CI:** fixture-only, CPU, **no GPU**, **no live SC2** — tests validate deterministic emission and schema-style fields via `tests/test_m41_replay_imitation_training_pipeline.py`.
- **Local:** full runs may use `out/training_runs/`; weights stay **local sidecars** referenced by path + SHA-256 in the run JSON.

## Feature policy

- **Feature policy:** `starlab.m27.feature.observation_signature_v1` (same signature family as M27).
- **Encoding policy:** `starlab.m41.encoding.context_signature_onehot_v1` — parse `context_signature` into categorical components, one-hot encode with fixed ordering (`DictVectorizer` feature names).
- **Labels:** `target_semantic_kind` from M26; label vocabulary recorded in `feature_schema.label_vocabulary`.

## Non-claims

See `non_claims` in the emitted run JSON and M40 `agent_training_program_contract.json`.
