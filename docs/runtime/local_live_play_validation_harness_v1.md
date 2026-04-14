# Local live-play validation harness (M44)

**Version:** `starlab.local_live_play_validation_run.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11  
**Emitter:**  
`python -m starlab.sc2.emit_local_live_play_validation_run --hierarchical-training-run-dir <M43_dir> --match-config <M02_match_config.json> --output-dir out/live_validation_runs/<run_id>/ --runtime-mode <fixture_stub_ci|local_live_sc2>`

## Purpose

M44 is the first **governed local live-play validation** milestone: it loads an **M43** `hierarchical_training_run.json` plus the **local-only** `joblib` weights, runs a **bounded M02 match harness** (fake adapter in CI; BurnySc2 locally when configured), emits **M44** validation JSON, writes a **replay file** (deterministic stub in fixture mode; real replay when available in local live mode), and binds that replay through **M04** `replay_binding.json`. An optional **bounded semantic-to-live action adapter** records how coarse labels map to conservative scripted action templates.

M44 does **not** claim benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or **M45** RL — see `non_claims` in the emitted run JSON.

## Outputs

| File | Role |
| ---- | ---- |
| `local_live_play_validation_run.json` | Full validation record: `runtime_mode`, candidate identity (M43 run path + SHA-256, weights SHA-256), M40/M29/M30 linkage, match summary, semantic adapter steps, replay + replay-binding fields, optional media metadata, non-claims |
| `local_live_play_validation_run_report.json` | Compact summary linked by `validation_run_sha256` |
| `match_execution_proof.json` | M02 proof (from harness) |
| `match_config.json` | Copy of the match config used |
| `run_identity.json` / `lineage_seed.json` | M03 seeds derived from proof + config |
| `replay/validation.SC2Replay` | Replay bytes (stub or copied live replay) |
| `replay_binding.json` | M04 binding record |

Default layout:

```text
out/live_validation_runs/<run_id>/
  local_live_play_validation_run.json
  local_live_play_validation_run_report.json
  match_execution_proof.json
  match_config.json
  run_identity.json
  lineage_seed.json
  replay/
    validation.SC2Replay
  replay_binding.json
  media/
    validation_video.mp4              # optional, operator-supplied
    validation_video_metadata.json    # optional (not required; metadata may live in run JSON only)
```

## Runtime modes

| `runtime_mode` | Match adapter | CI | Meaning |
| -------------- | ------------- | -- | ------- |
| `fixture_stub_ci` | `fake` | Yes (tests) | Deterministic stub `.SC2Replay` bytes; no live SC2 |
| `local_live_sc2` | `burnysc2` | No | Local StarCraft II via optional harness extras; replay copied when saved |

## Local vs CI

- **CI:** fixture-only CPU path — `runtime_mode=fixture_stub_ci`, `adapter=fake`, no GPU, no live SC2 — see `tests/test_m44_local_live_play_validation_harness.py`.
- **Local:** real M43 run directory under `out/hierarchical_training_runs/` (or equivalent); weights stay **local sidecars**; use `local_live_sc2` only on an operator machine with SC2 + optional `sc2-harness` extras.

## `match_execution` semantics (bounded burnysc2 vs fixture)

- **`fixture_stub_ci` / `adapter=fake`:** `match_execution.final_status` is **`ok`** (deterministic harness; no SC2 client `Result`).
- **`local_live_sc2` / `adapter=burnysc2`:** When the bounded harness completes the configured step cap (`bounded_exit` in the proof `status_sequence`), **`match_execution.final_status`** is **`ok`** — this is **governed validation success** (bounded contract completed), **not** a claim that the bot won the match. The literal SC2 client `Result` name (e.g. `Victory`, `Defeat`, `Tie`) is preserved separately as **`sc2_game_result`** on `match_execution_proof.json` and, when present, on **`match_execution.sc2_game_result`** in `local_live_play_validation_run.json`. Voluntary leave at the step cap often yields `Defeat` in SC2; that does **not** negate validation success for this milestone’s narrow plumbing proof.

## Semantic live action adapter

**Policy id:** `starlab.m44.semantic_live_action_adapter.v1`

Maps **(delegate_id, coarse semantic label)** to a small set of **scripted template ids** for bounded plumbing — **not** full action legality or strong gameplay.

## Optional video registration

If `--optional-video` is set, the emitter hashes the file and records **simple metadata** (`path`, `sha256`, `size_bytes`, `duration_seconds`, `format`; optional `resolution` / `codec` if extended later). Video is **supplementary**; the replay-backed artifact chain remains primary.

## Weights path vs `weights_sidecar` (M51 campaign refit)

`run_local_live_play_validation(..., weights_path=...)` normally requires the joblib SHA-256 to match `hierarchical_training_run.json` **`weights_sidecar.artifact_sha256`**. For **M51** watchable validation after an **M45 refit**, set **`enforce_weights_sidecar_sha256=False`** so a refit bundle path is accepted; the run JSON **`warnings`** list records `m51_weights_override` when the SHA differs.

## Non-claims

See `non_claims` in the emitted run JSON and M40 `agent_training_program_contract.json`.
