# Hierarchical training pipeline (M43)

**Version:** `starlab.hierarchical_training_run.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11  
**Emitter:**  
`python -m starlab.hierarchy.emit_hierarchical_training_run --dataset <M26/replay_training_dataset.json> --bundle <M14_bundle_dir> ... --output-dir out/hierarchical_training_runs/<run_id>/`

## Purpose

M43 is the first **governed local-first hierarchical training** milestone: it consumes governed **M26** datasets and **M14** bundle directories, materializes **M27** `context_signature` features via the existing M16→M18 path, trains a small deterministic **scikit-learn** **manager** (signature → delegate) and **worker** models (signature → coarse semantic label per delegate partition) under the fixed **M30** delegate policy **`starlab.m30.delegate.fixed_four_v1`**, and emits governed JSON artifacts. It binds to the **M40** training-program contract via `training_program_contract_version` and `training_program_contract_sha256`, and records **M29** trace schema linkage via `interface_trace_schema_version`.

M43 does **not** claim benchmark integrity, live SC2 in CI, **M42** comparison integration, **M44** live-play validation, or **M45** RL — see `non_claims` in the emitted run JSON.

## Outputs

| File | Role |
| ---- | ---- |
| `hierarchical_training_run.json` | Full run record: contract binding, dataset identity, M29 interface trace schema version, M30 delegate policy id, manager/worker model family ids, seed, trainer config, split metrics (manager, worker-on-oracle-delegate, end-to-end label), **delegate_coverage** (per-delegate split counts, trained-worker flag, fallback flag), feature schema, optional weights sidecar metadata, non-claims |
| `hierarchical_training_run_report.json` | Compact summary linked by `training_run_sha256` |

Default layout:

```text
out/hierarchical_training_runs/<run_id>/
  hierarchical_training_run.json
  hierarchical_training_run_report.json
  weights/
    hierarchical_training_sklearn_bundle.joblib   # local-only; not in repo
```

## Local vs CI

- **CI:** fixture-only, CPU, **no GPU**, **no live SC2** — tests validate deterministic emission via `tests/test_m43_hierarchical_training_pipeline.py`.
- **Local:** full runs may use `out/hierarchical_training_runs/`; weights stay **local sidecars** referenced by path + SHA-256 in the run JSON.

## Feature and training policy

- **Feature policy:** `starlab.m27.feature.observation_signature_v1` (same signature family as M27/M41).
- **Encoding policy:** `starlab.m41.encoding.context_signature_onehot_v1` — parse `context_signature` into categorical components, one-hot encode with fixed ordering (`DictVectorizer` feature names).
- **Manager:** multinomial **LogisticRegression** over one-hot features → delegate id (or constant fallback when the train split has a single delegate class).
- **Workers:** per-delegate **LogisticRegression** over the same feature space, trained only on examples whose oracle delegate matches; **fallback** when a delegate has **no** train rows (global majority coarse label) or **one** distinct coarse label on the train split (constant label), recorded honestly in **delegate_coverage**.

## Non-claims

See `non_claims` in the emitted run JSON and M40 `agent_training_program_contract.json`.
