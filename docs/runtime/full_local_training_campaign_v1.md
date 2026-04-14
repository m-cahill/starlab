# Full local training / bootstrap campaign charter (M49)

**Contract version:** `starlab.full_local_training_campaign.v1`  
**Report version:** `starlab.full_local_training_campaign_report.v1`  
**Preflight receipt version:** `starlab.full_local_training_campaign_preflight_receipt.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11

## Role (normative)

M49 defines a **governed planning and evidence protocol** for a substantial **operator-local** Phase VI campaign across existing surfaces (**M40**–**M48**). It answers, *before* a long run:

- what is being chartered (identities, paths, budgets)
- what post-run artifacts are expected for audit
- what the campaign **does** and **does not** prove

This milestone is **charter + preflight + documentation + tests** — **not** the hours-long run itself, and **not** a merge gate on operator wall-clock time.

## Authorization posture (trust-critical)

Campaign JSON is **planned / defined / preflighted** only:

- It **does not** execute bootstrap, comparison, or validation.
- It **does not** guarantee completion, success, or learning outcomes.
- **`preflight_ok`** means deterministic readiness checks passed at preflight time — not that a future run will succeed.

The contract embeds `authorization_posture.status == "planned_charter_only"` with explicit meaning text.

## Artifact layout

Recommended root:

`out/training_campaigns/<campaign_id>/`

| File | Role |
| ---- | ---- |
| `full_local_training_campaign_contract.json` | Sealed charter: identities (hashes/versions) + resolved paths |
| `full_local_training_campaign_contract_report.json` | Compact summary keyed by `campaign_sha256` |
| `campaign_preflight_receipt.json` | Emitted by preflight CLI; lists checks + `preflight_ok` |
| `referenced_artifacts/m40_training_program/` | When `--training-program-contract` is omitted, default M40 JSON is written here |

## CLI

**Emit contract + report:**

```bash
python -m starlab.training.emit_full_local_training_campaign_contract \
  --campaign-id <id> \
  --output-dir out/training_campaigns/<campaign_id>/ \
  --hierarchical-training-run-dir <M43_DIR> \
  --benchmark-contract <M20_benchmark_contract.json> \
  --match-config <M02_match.json> \
  --runtime-mode fixture_stub_ci \
  [--training-program-contract <M40_agent_training_program_contract.json>] \
  [--weights <joblib_path>] \
  [--planned-weighted-refit --dataset <M26.json> --bundle-dir <M14_DIR> ...] \
  [--campaign-protocol-json <override.json>]
```

**Preflight (readiness gate):**

```bash
python -m starlab.training.emit_full_local_training_campaign_preflight \
  --campaign-contract out/training_campaigns/<id>/full_local_training_campaign_contract.json \
  --output-dir out/training_campaigns/<campaign_id>/
```

Preflight exit codes: **0** = all checks passed, **3** = one or more checks failed (receipt still written).

## Identity vs resolution

The contract uses the same **mixed posture** as other STARLAB surfaces:

- **Identity:** `contract_sha256`, `training_run_sha256`, `benchmark_contract_sha256`, `dataset_sha256`, `weights_sha256`, versions.
- **Resolution:** absolute `resolved_path` fields so operators can locate artifacts on disk.

Preflight validates **existence** and **hash coherence** where applicable.

## Campaign protocol (default)

The embedded default protocol includes:

- **Minimum governed full run:** 100 completed episodes (see `campaign_protocol.minimum_episodes_governed_full_run`).
- **Recommended default:** 250 total episodes (`recommended_default_total_episodes`).
- Phases: preflight → shakedown (5) → tranche A (50) → tranche B (50) → optional stretch → optional weighted refit → post-refit **M42** comparison → one watchable **M44** validation.

Override via `--campaign-protocol-json` (JSON object replacing the default `campaign_protocol` block).

## Evidence interpretation (M47 posture)

The contract includes an `evidence_interpretation` block:

- **Integration success** ≠ strong learning claims.
- **Distinct episode evidence** requires governed per-episode identities (M47 manifest / `validation_run_sha256`); configured episode counts alone are not multi-sample statistical evidence.
- **Refit eligibility** requires M26/M14 alignment with the M43 `source_dataset` when refit is planned.

## Runtime mode and match config

`--runtime-mode` must agree with the M02 match config adapter (**M44** rules):

| `runtime_mode` | Match config `adapter` |
| -------------- | ------------------------ |
| `fixture_stub_ci` | `fake` |
| `local_live_sc2` | `burnysc2` |

Preflight for `local_live_sc2` additionally checks Python **sc2** importability and **`run_probe()`** SC2 install root (see `docs/runtime/sc2_runtime_surface.md`).

## Cross-links

- **Diligence / campaign narrative:** `docs/diligence/phase_vi_integrated_test_campaign.md` (supplements this doc; not replaced by it).
- **M40:** `docs/runtime/agent_training_program_contract_v1.md`
- **M42 / M48:** `docs/runtime/learned_agent_comparison_harness_v1.md`
- **M45 / M47:** `docs/runtime/self_play_rl_bootstrap_v1.md`
- **M44:** `docs/runtime/local_live_play_validation_harness_v1.md`
- **M50 execution:** `docs/runtime/industrial_hidden_rollout_mode_v1.md`, `docs/diligence/industrial_hidden_rollout_operator_guide.md`

## M50 governed campaign execution (under this root)

When using the M50 executor (`python -m starlab.training.execute_full_local_training_campaign`), execution trees live at:

`out/training_campaigns/<campaign_id>/campaign_runs/<execution_id>/`

Typical files include `hidden_rollout_campaign_run.json`, `campaign_execution_manifest.json`, `campaign_heartbeat.json`, `campaign_resume_state.json`, per-phase M45 outputs under `phases/<phase_name>/`, optional `STOP_REQUEST` for graceful stop between phases, and PID lockfiles (`.starlab_campaign_output.lock` at the campaign root, `.campaign_execution.lock` under the execution directory). Extended execution preflight may write `campaign_execution_preflight_receipt.json` at the campaign root.

## M51 post-bootstrap phases (optional)

**Flag:** `--post-bootstrap-protocol-phases` (default **off** preserves M50 bootstrap-only behavior).

**Refit:** A distinct phase after bootstrap episodes aggregates pseudo-label rows from all **successfully completed** `bootstrap_episodes` phase directories (via each phase’s `bootstrap_dataset.json` and episode `local_live_play_validation_run.json` paths), then runs weighted re-fit into `phases/optional_weighted_refit/updated_policy/rl_bootstrap_candidate_bundle.joblib` when `m45_planned_bootstrap.planned_weighted_refit` is true and M26/M14 paths are present.

**M42:** The offline comparison phase is recorded with **`candidate_not_m41_comparison_compatible`** — M42 remains M27/M41-only; M51 does not treat M45 refit bundles as M41 candidates.

**Watchable M44:** One validation under `phases/watchable_m44_validation/` using the refit joblib; skipped if refit did not produce a bundle. The M44 harness may set `enforce_weights_sidecar_sha256=False` so refit SHA need not match `hierarchical_training_run.json` `weights_sidecar` (warning recorded on the validation run).

## Explicit non-claims

See `non_claims` in the contract JSON and `NON_CLAIMS_V1` in `starlab.training.full_local_training_campaign_models`. M49 does **not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or that a long campaign yields a strong policy by default.
