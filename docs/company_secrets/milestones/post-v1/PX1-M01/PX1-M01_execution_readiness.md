# PX1-M01 — execution readiness (checkpoint before live SC2)

**Status:** **Draft** after PR1 — update **local SC2 preflight** and paths when executing.

This document is the **deliberate checkpoint** before the authoritative operator-local run. **Do not** treat execution as authoritative until this readiness review is satisfied.

## Frozen threshold block

See **`PX1-M01_threshold_freeze.md`** and **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`** (identical values; **no** post-freeze silent edits).

## Campaign identity

| Field | Value |
| --- | --- |
| `campaign_id` | `px1_m01_full_run_2026_04_17_a` |
| `execution_id` | `px1_m01_exec_001` |
| `runtime_mode` | `local_live_sc2` |

## Checkpoint ids

- `tranche_a_close`
- `tranche_b_close`
- `full_run_close` (when recorded as end-of-run seal)

## Environment (Windows example)

```text
STARLAB_SC2_BIN=C:\Program Files (x86)\StarCraft II\StarCraft II.exe
STARLAB_SC2_ROOT=C:\Program Files (x86)\StarCraft II
```

## Local SC2 preflight

| Check | Status |
| --- | --- |
| M49 `campaign_preflight_receipt.json` emitted | **Pending** |
| M50 `campaign_execution_preflight_receipt.json` (on execute path) | **Pending** |
| SC2 binary / maps discoverable | **Pending** |

## Exact commands (after contract exists at `<campaign_root>`)

**1. Emit contract** (paths below are examples — use your M43 run, benchmark contract, match config):

```powershell
python -m starlab.training.emit_full_local_training_campaign_contract `
  --campaign-id px1_m01_full_run_2026_04_17_a `
  --output-dir <campaign_root> `
  --hierarchical-training-run-dir <path_to_m43_run> `
  --benchmark-contract <path_to_benchmark_contract.json> `
  --match-config <path_to_match_config.json> `
  --runtime-mode local_live_sc2 `
  --campaign-protocol-json tests/fixtures/px1_m01/px1_m01_campaign_protocol.json
```

**2. M49 preflight** (from repo root or with paths adjusted):

```powershell
python -m starlab.training.emit_full_local_training_campaign_preflight `
  --campaign-contract <campaign_root>/full_local_training_campaign_contract.json
```

**3. M50/M51 execute** (authoritative run):

```powershell
python -m starlab.training.execute_full_local_training_campaign `
  --campaign-contract <campaign_root>/full_local_training_campaign_contract.json `
  --campaign-root <campaign_root> `
  --execution-id px1_m01_exec_001 `
  --post-bootstrap-protocol-phases
```

**4. Observability + checkpoints** (after tree exists):

```powershell
python -m starlab.training.emit_campaign_observability_index --campaign-root <campaign_root>
python -m starlab.training.emit_tranche_checkpoint_receipt --campaign-root <campaign_root> ...
```

(Use **`PX1-M01_operator_checklist.md`** and **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`** for exact emit flags.)

## Sign-off

- [ ] Threshold block unchanged since PR1 freeze
- [ ] Preflight green
- [ ] Commands reviewed
- [ ] Proceed to live run
