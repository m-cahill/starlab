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

## Explicit non-claims

See `non_claims` in the contract JSON and `NON_CLAIMS_V1` in `starlab.training.full_local_training_campaign_models`. M49 does **not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, or that a long campaign yields a strong policy by default.
