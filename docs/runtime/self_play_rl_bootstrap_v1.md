# Self-play / RL bootstrap run contract (M45)

**Version:** `starlab.self_play_rl_bootstrap_run.v1`  
**Report version:** `starlab.self_play_rl_bootstrap_run_report.v1`

## Role

M45 is the **first governed self-play / RL bootstrap surface** for STARLAB. It consumes a **governed M43** hierarchical training candidate (plus local `joblib` weights), drives **bounded rollout collection** through the **M44** local live-play validation harness, records rollout and reward metadata, optionally performs **one conservative weighted re-fit** over the existing sklearn logistic-regression family, and emits **deterministic JSON artifacts** for audit.

This milestone is **bootstrap-only**. It does **not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or a full RL program.

## Output layout

Recommended root:

`out/rl_bootstrap_runs/<run_id>/`

```text
out/rl_bootstrap_runs/<run_id>/
  self_play_rl_bootstrap_run.json
  self_play_rl_bootstrap_run_report.json
  bootstrap_dataset.json
  episodes/
    episode_manifest.json
    e000/
      bootstrap_match_config.json   # per-episode M02 config (seed varies)
      local_live_play_validation_run.json
      ...
  updated_policy/
    rl_bootstrap_candidate_bundle.joblib   # optional, local-only
```

## CLI

```bash
python -m starlab.training.emit_self_play_rl_bootstrap_run \
  --hierarchical-training-run-dir <M43_DIR> \
  --match-config <M02_MATCH_JSON> \
  --output-dir out/rl_bootstrap_runs/<run_id>/ \
  --runtime-mode fixture_stub_ci \
  [--episodes N] \
  [--seed 42] \
  [--emit-updated-bundle --dataset <M26_DATASET.json> --bundle-dir <M14_BUNDLE_DIR> ...]
```

**Episode defaults:** if `--episodes` is omitted, **1** for `fixture_stub_ci` and **5** for `local_live_sc2`.

**`--seed` (bootstrap base seed):** Used as **`random_state`** for optional weighted **LogisticRegression** re-fit when `--emit-updated-bundle` is set. For each episode `i` (0-based), the bootstrap loop writes `episodes/eNNN/bootstrap_match_config.json` with M02 **`seed` = `--seed` + `i`** (`episode_seed_policy`: `base_seed_plus_episode_index`). The **fake** fixture adapter records that seed in the execution proof; **burnysc2** passes it through as **`random_seed`**. Fixture mode stays deterministic and bounded; varying seed changes governed **M44** identities (`validation_run_sha256`, `run_id`) so multi-episode runs are easier to interpret as **distinct episodes** when the harness produces distinct proofs.

**Weighted re-fit:** requires `--emit-updated-bundle`, `--dataset` (must match `hierarchical_training_run.source_dataset.dataset_sha256`), and at least one `--bundle-dir` (same M14 bundles used to build the M43 run).

## `bootstrap_mode` (bounded enum)

| Value | Meaning |
| ----- | ------- |
| `single_candidate_fixture_stub` | Single M43 candidate; M44 `fixture_stub_ci` |
| `single_candidate_local_live` | Single M43 candidate; M44 `local_live_sc2` (operator machine) |
| `mirror_self_play_local` | Reserved; **not** implemented in M45 v1 |

## Policy IDs (v1)

| Field | Default ID |
| ----- | ------------ |
| `reward_policy_id` | `starlab.m45.reward.validation_outcome_v1` |
| `update_policy_id` | `starlab.m45.update.weighted_logistic_refit_v1` |

**Reward (v1):** primary signal from M44 `match_execution.final_status` (`ok` → 1.0; otherwise 0.0) plus a small deterministic step-count shaping term (capped). For **bounded burnysc2** runs, `final_status` is **`ok`** when the M44 harness completed the step cap (validation contract success); the literal SC2 `Result` is **not** used for reward — see `sc2_game_result` on the M44 proof if needed for forensics. **Not** victory, **not** ladder performance.

## Campaign interpretation & episode distinctness (M47)

**Do not** treat **`episode_count_configured` = N** as **N** independent statistical samples or **N** guaranteed distinct rollouts unless **episode-level governed identities** differ.

**Minimum distinctness (governed):** compare **`validation_run_sha256`** per episode (in `episodes/episode_manifest.json` and each `local_live_play_validation_run.json`). Prefer also checking distinct **`run_id`** on each M44 run.

**What a multi-episode campaign does prove:** **integration success** — the bootstrap pipeline completed and emitted governed JSON under the configured `runtime_mode` / policies.

**What it does not prove by itself:** **sample diversity**, **policy robustness**, **benchmark strength**, or **statistical** claims about refit or learning. Those require explicit experimental design beyond “more episodes with the same identities.”

**Episode manifest (v2):** `episode_manifest_version` **`starlab.m47.episode_manifest.v2`** includes **`episode_seed_policy`**, **`bootstrap_base_seed`**, per-episode **`episode_seed`**, **`distinct_episode_identities`** (`distinct_validation_run_sha256_count`, `distinct_run_id_count`), and optional **`warnings`** when configured episodes **collapse** to repeated identities (e.g. `m47_episode_validation_run_sha256_collapsed: …`). The sealed bootstrap run and report include a compact **`episode_distinctness`** block for the same counts.

**Versioning:** **`starlab.m45.episode_manifest.v1`** is superseded by **v2** for manifests emitted after this interpretation/diversity update; v1 semantics remain valid for historical runs.

## Operator ergonomics: configs vs campaigns

| Concept | Role |
| -------- | ------ |
| **Watchable / operator-visible live validation** | Longer horizon, human review (e.g. video); optimized for **inspection**, not for bootstrap reward variance or tight step caps. |
| **Bootstrap-bounded config** | M02 **`bounded_horizon`** / adapter settings aligned with **M45** reward policy and validation **`ok`** semantics (see M44/M46 docs). |
| **Extended bootstrap campaign** | Many episodes under `out/rl_bootstrap_runs/` — read **`episode_manifest.json`** and **`episode_distinctness`** before treating the run as multi-sample evidence. |
| **“Good” for learning-oriented reads** | Distinct **`validation_run_sha256`** (and preferably **`run_id`**) across episodes **or** an explicit **integration-only** / repetition stance documented by the operator. |

## Binding and non-claims

Runs must record:

- **M40:** `training_program_contract_sha256` / `training_program_contract_version` (via M43 candidate)
- **M43:** hierarchical training run path + SHA-256; weights path + SHA-256; `interface_trace_schema_version`; `delegate_policy_id`
- **M44:** `runtime_mode`; substrate reference to `starlab.local_live_play_validation_run.v1` and `starlab.m44.semantic_live_action_adapter.v1`

Explicit **non-claims** are listed in the artifact (`non_claims`) and mirror the ledger: no benchmark integrity, no replay↔execution equivalence, no live SC2 in CI, no ladder claims, no weights in repo, no implication of a full RL product beyond this bounded bootstrap.

## Bootstrap dataset summary

`bootstrap_dataset.json` holds a compact manifest pointer (`bootstrap_dataset_version`), episode manifest reference, and `rows_ingested_for_refit` when rollouts produced steps.
