# PX1 full industrial campaign execution evidence v1 (PX1-M01)

## Ledger posture (public source of truth)

This file is the **public runtime contract** for **PX1-M01 — Full Industrial Campaign Execution Evidence**. **Whether PX1-M01 is open or closed** on `main` is determined by **`docs/starlab.md`** (and the opening / closeout PRs), **not** by this document alone.

When the ledger lists **PX1-M01** as **closed**, this contract remains the **reference** for reading operator-local artifacts and the **frozen PX1 full-run threshold block** used for the authoritative run. **PX1-M02** does **not** open automatically when **PX1-M01** merges or closes — **not** even if **`threshold-met`**.

## Purpose

**PX1-M01** proves **one** bounded claim:

> Did STARLAB complete a **true full industrial-grade** governed campaign execution under a **newly frozen PX1 threshold package**, with an honest evidence tree and threshold declaration?

**PX1-M01** is **not** **PX1-M02** (play-quality), **not** **PX1-M03** (demo/video), and **not** **v2**.

## Frozen campaign identity (PX1-M01 — lock before authoritative execution)

These identifiers are **declared for the authoritative PX1-M01 run** and must **not** reuse the closed **PV1** campaign identity.

| Field | Value |
| --- | --- |
| `campaign_id` | `px1_m01_full_run_2026_04_17_a` |
| `execution_id` (primary) | `px1_m01_exec_001` |
| `runtime_mode` | `local_live_sc2` |
| Authoritative checkpoint ids | `tranche_a_close`, `tranche_b_close` (minimum); `full_run_close` — end-of-run seal when recorded |

**Rule:** Use **one** primary `execution_id` for the authoritative run unless an honest **governed resume** is required (continuity valid; invalidation count unchanged).

## Frozen full-run threshold block (PX1-M01)

**Status:** **Frozen** in **PX1-M01** before execution is treated as authoritative. **Do not** silently change these values after execution starts.

Repo inspection (**M49** `campaign_protocol` / `episode_budget` per phase): the default recommended block is **achievable** without code changes — **no** adjustment was required at freeze time.

| Field | Value |
| --- | --- |
| `full_run_min_tranches` | **2** |
| `full_run_min_bootstrap_episodes_per_tranche` | **6** |
| `full_run_min_bootstrap_episodes_total` | **12** |
| `full_run_min_completed_protocol_phases` | **4** (Tranche A bootstrap + Tranche A post-bootstrap + Tranche B bootstrap + Tranche B post-bootstrap — each **completed** only when in scope and evidenced) |
| `full_run_min_checkpoint_receipts` | **2** (`tranche_a_close`, `tranche_b_close`) |
| `full_run_min_watchable_validations` | **1** |
| `full_run_min_evidence_completeness` | **`complete`** (observability index ruleset posture — honest **`threshold-not-met`** if incomplete) |
| `full_run_required_runtime_mode` | `local_live_sc2` |
| `full_run_max_continuity_invalidations` | **0** |
| `full_run_required_post_bootstrap_phases` | **enabled** (`--post-bootstrap-protocol-phases` on the M50/M51 executor path where in scope) |
| `full_run_duration_target` | **One** declared full-run campaign instance anchored to **one** `campaign_id` and **one** primary `execution_id`; **governed resume** allowed only if continuity remains valid and invalidation count stays **zero** |

### Comparison to closed PV1 (context only — **not** reinterpretation)

The closed **PV1** full-run block used a smaller bootstrap scale (e.g. **6** episodes total across tranches) and **`threshold-not-met`** on **`full_run_duration_target`** due to **separate** operator sessions. **PX1-M01** uses a **larger** PX1 package and explicit duration/continuity rules — **not** a rewrite of **PV1** history.

## Continuity / resume semantics

- **Governed resume** is allowed only when **M50** resume rules permit, continuity stays valid, and **`full_run_max_continuity_invalidations`** remains **0**.
- **Pre-authoritative shakedown** runs are **non-authoritative** and **must not** satisfy threshold fields.
- Switching to a **fresh** `campaign_id` after an invalidation is honest; **do not** claim **`threshold-met`** across incomparable trees.

## Tranche posture vs full-run threshold posture

| Posture | Meaning |
| --- | --- |
| **Tranche** | Per-tranche **completed within scope** / not — recorded in **`tranche_a_operator_note.md`** and **`tranche_b_operator_note.md`** |
| **Full-run threshold** | **`threshold-met`** vs **`threshold-not-met`** vs the **frozen block** — **`full_run_threshold_declaration.md`** + **`px1_full_run_operator_note.md`**; **not** interchangeable with tranche notes |

Truthful combinations include tranche **within scope** + full-run **`threshold-not-met`** when the frozen bar is not met.

## Required evidence package (minimum)

At the **campaign root** and under **`campaign_runs/<execution_id>/`** as applicable:

- **M49:** `full_local_training_campaign_contract.json`, `campaign_preflight_receipt.json`
- **M50/M51:** `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json` (v2 when M51 applies); `campaign_execution_preflight_receipt.json` when the executor emits it
- **Phases:** per-phase `phase_receipt.json` files
- **Replay-binding** references where applicable
- **Watchable M44** validation artifact(s) under the M51 path
- **Observability:** `campaign_observability_index.json`, `campaign_observability_index_report.json`
- **Checkpoints:** preserved receipts under `checkpoints/tranche_a_close/` and `checkpoints/tranche_b_close/` (and root receipt copies per **PV1** bounded pattern if overwritten)
- **Operator (canonical basenames):** `tranche_a_operator_note.md`, `tranche_b_operator_note.md`, `px1_full_run_operator_note.md`, `full_run_threshold_declaration.md`

If root receipt filenames are overwritten by repeated emission, preserve per-checkpoint copies under subdirectories as in **PV1** bounded posture.

## Explicit non-claims

**PX1-M01** does **not** prove:

- **Play-quality** beyond bounded execution sanity (**PX1-M02**)
- **Demo / winning video** (**PX1-M03**)
- Ladder / public-strength claims
- Benchmark universality, replay↔execution universality, or live SC2 in CI as merge norm
- **Automatic** opening of **PX1-M02** when **PX1-M01** merges or closes

## PX1-M02 does not open automatically

**Merging** or **closing** **PX1-M01** **does not** authorize **PX1-M02**. Opening **PX1-M02** requires a **separate** governance decision and ledger update.

## Related

- `docs/runtime/px1_full_industrial_run_demo_charter_v1.md` (**PX1-M00**)
- `docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md` (closed **PV1** — historical)
- `docs/runtime/full_local_training_campaign_v1.md` (**M49**)
- `docs/runtime/industrial_hidden_rollout_mode_v1.md` (**M50** / **M51**)
- `tests/fixtures/px1_m01/px1_m01_campaign_protocol.json` (synthetic protocol mirror — **CI-safe**)
