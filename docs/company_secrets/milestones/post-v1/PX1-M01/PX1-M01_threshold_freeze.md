# PX1-M01 — threshold freeze (authoritative)

**Frozen as of:** PX1-M01 opening PR (PR1) — **before** authoritative execution.

**Rule:** Do **not** change this block silently after execution starts. Any **emergency** re-freeze requires a **new** governed milestone decision and ledger update.

## Repo constraint check (at freeze)

- **M49** `campaign_protocol` phases support **`episode_budget`** per `bootstrap_episodes` phase — **6** per tranche (**12** total) is valid.
- **M50/M51** executor supports **`--post-bootstrap-protocol-phases`** and **`--skip-bootstrap-phases`** for honest multi-tranche continuation when needed.

**Result:** Recommended block applied **without** numeric adjustment.

## Frozen block (evaluate execution against this)

| Field | Value |
| --- | --- |
| `full_run_min_tranches` | 2 |
| `full_run_min_bootstrap_episodes_per_tranche` | 6 |
| `full_run_min_bootstrap_episodes_total` | 12 |
| `full_run_min_completed_protocol_phases` | 4 |
| `full_run_min_checkpoint_receipts` | 2 |
| `full_run_min_watchable_validations` | 1 |
| `full_run_min_evidence_completeness` | `complete` |
| `full_run_required_runtime_mode` | `local_live_sc2` |
| `full_run_max_continuity_invalidations` | 0 |
| `full_run_required_post_bootstrap_phases` | enabled |
| `full_run_duration_target` | One declared full-run campaign instance anchored to one `campaign_id` and one primary `execution_id`; governed resume allowed only if continuity remains valid and invalidation count stays zero |

## Frozen campaign identity (with threshold)

| Field | Value |
| --- | --- |
| `campaign_id` | `px1_m01_full_run_2026_04_17_a` |
| `execution_id` | `px1_m01_exec_001` |

## Checkpoint ids

- `tranche_a_close`
- `tranche_b_close`
- `full_run_close` (end-of-run seal when recorded)

Minimum **2** checkpoint receipts required for threshold (**tranche_a_close**, **tranche_b_close**).
