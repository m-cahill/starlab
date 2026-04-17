# PV1 Tranche B / full-run threshold evidence (v1)

## Ledger posture (public source of truth)

This file is a **governance runtime contract** for **PV1-M03**. It **does not** by itself mean **PV1-M03** is **closed** on `main`. **Milestone closure** requires an honest operator outcome, accurate **`docs/starlab.md`** ledger updates, and a **merge** to `main` per project rules — **not** implied by this document alone.

## Purpose

This contract defines **Tranche B** and **full-run threshold evaluation** for **PV1-M03 — Tranche B / Full-Run Completion Evidence**: operator-local governed execution on the closed **M49 / M50 / M51** machinery, with **PV1-M01** inspection artifacts at tranche boundaries and an explicit **`threshold-met`** or **`threshold-not-met`** declaration against a **frozen** threshold block.

**PV1** is post-v1 recharter (**not** “Phase VIII” of v1). There is **no M62**.

## Campaign identity and continuity

**PV1-M03** continues the **same** `campaign_id` as **PV1-M02** when aggregation across Tranche A + Tranche B is honest under the PV1 charter.

- The historical **`campaign_id`** may embed `tranche_a` in the string; that does **not** narrow tranche scope — it is a **naming artifact** from the first tranche milestone.
- **Tranche B** uses a **fresh** `execution_id` under `campaign_runs/<execution_id>/` so evidence trees stay separable while the **M49** contract lists **both** tranches.
- **Continuation execution:** run the executor with **`--skip-bootstrap-phases 1`** (when the sealed protocol orders `tranche_a` then `tranche_b`) so the second execution does **not** re-run Tranche A bootstrap; skipped phases emit **`skip_bootstrap_phases_prior_tranche_completed_in_other_execution`** in `phase_receipt.json`.

Switch to a **fresh** `campaign_id` only if a real **invalidation** makes same-root aggregation dishonest (contract/environment/lineage/replay-binding/seed-policy break outside declared rules). If that happens, **do not** claim `threshold-met` by mixing incomparable trees.

## Frozen kickoff (PV1-M03 — locked)

| Field | Value |
| --- | --- |
| `campaign_id` | `pv1_m02_tranche_a_2026_04_16` (continued) |
| Tranche B `execution_id` | `pv1_m03_exec_001` (fresh vs Tranche A) |
| Tranche A reference `execution_id` | `pv1_m02_exec_001` |
| `tranche_id` | `tranche_b` |
| `checkpoint_id` (tranche close) | `tranche_b_close` |
| `runtime_mode` | `local_live_sc2` |
| M51 post-bootstrap | **In scope** (`--post-bootstrap-protocol-phases`): weighted refit, orchestrated M42 skip, watchable M44 on refit |
| SC2 | Re-verify **`STARLAB_SC2_ROOT`** / maps before execution; if unavailable, **stop** and record blocker — **do not** fabricate evidence |

### Full-run threshold block (frozen — evaluate exactly this)

| Field | Value |
| --- | --- |
| `full_run_min_tranches` | **2** |
| `full_run_min_completed_protocol_phases` | **4** (Tranche A bootstrap + Tranche A post-bootstrap + Tranche B bootstrap + Tranche B post-bootstrap, each **completed** only if in scope and evidenced) |
| `full_run_min_checkpoint_receipts` | **2** (`tranche_a_close`, `tranche_b_close`) |
| `full_run_min_watchable_validations` | **2** (one watchable M44 path per tranche when M51 is in scope and refit prerequisites hold) |
| `full_run_min_evidence_completeness` | **`complete`** (PV1-M01 default ruleset posture — **not** vague prose) |
| `full_run_scale_target` | **≥ 6** bootstrap episodes **total** across Tranche A + Tranche B (3 + 3) |
| `full_run_duration_target` | **At least one operator session spanning both tranches with no continuity invalidation** (qualitative; prevents dishonest cross-session aggregation) |

### Threshold field → evaluation artifacts

| Threshold field | Primary evidence |
| --- | --- |
| `full_run_min_tranches` | `tranche_a_operator_note.md` + `tranche_b_operator_note.md` each **completed within scope**; PV1-M01 receipts for `tranche_a` / `tranche_a_close` and `tranche_b` / `tranche_b_close` |
| `full_run_min_completed_protocol_phases` | **4×** completed bootstrap or post-bootstrap slices: Tranche A `hidden_rollout_campaign_run` + M51 receipts under `pv1_m02_exec_001`; Tranche B under `pv1_m03_exec_001` (bootstrap `tranche_b` + refit/M42/watchable as completed/skipped honestly) |
| `full_run_min_checkpoint_receipts` | `tranche_checkpoint_receipt.json` (and reports) for both checkpoints at campaign root |
| `full_run_min_watchable_validations` | `**/local_live_play_validation_run.json` under **watchable** phases for **both** executions (typically `watchable_m44_validation` when refit succeeds) |
| `full_run_min_evidence_completeness` | `campaign_observability_index.json` / report: default ruleset **`complete`** (or honest **`threshold-not-met`**) |
| `full_run_scale_target` | Episode manifests / bootstrap runs: **6** episodes across `tranche_a` + `tranche_b` trees (sum of `episode_budget` satisfied) |
| `full_run_duration_target` | Operator assertion in `full_run_threshold_declaration.md` + continuity note in operator notes — **no** fabricated timestamps |

## Canonical operator artifacts

| Basename | Role |
| --- | --- |
| `tranche_b_operator_note.md` | Tranche B **completed / not completed within scope** + **continue / pause / stop** — **not** the threshold declaration |
| `full_run_threshold_declaration.md` | **`threshold-met`** or **`threshold-not-met`** vs the frozen block — **not** blended with tranche posture |

## Minimum evidence package (campaign root + executions)

- **M49:** `full_local_training_campaign_contract.json` (lists **both** tranches + M51 phases), `campaign_preflight_receipt.json`
- **M50/M51:** `campaign_runs/pv1_m02_exec_001/hidden_rollout_campaign_run.json`, `campaign_runs/pv1_m03_exec_001/hidden_rollout_campaign_run.json`, phase receipts, replay bindings, watchable validations as applicable; per execution, `campaign_execution_preflight_receipt.json` at the campaign root when the M50 executor runs extended preflight (honest record when preflight fails)
- **PV1-M01:** `campaign_observability_index.json` / reports; `tranche_checkpoint_receipt.json` for each tranche close
- **Operator:** `tranche_a_operator_note.md` (PV1-M02), `tranche_b_operator_note.md`, `full_run_threshold_declaration.md`

## Operational control

- **Stop:** executor failure, missing SC2/maps, or evidence that cannot be sealed honestly.
- **Pause:** operator stop-request file (M50) or explicit pause in operator note.
- **Invalidation:** any continuity break listed above → fresh campaign or **threshold-not-met** / not evaluable.

## `threshold-met` vs `threshold-not-met`

- **`threshold-met`:** **All** frozen threshold fields satisfied **simultaneously** for the declared `campaign_id` boundary, with artifacts on disk matching the table above — **declared**, not inferred post hoc.
- **`threshold-not-met`:** Operational runs may have finished, but one or more threshold fields fail, evidence is incomplete, or continuity is broken — **honest** closeout is allowed.

## Honest non-claims (PV1-M03)

Even if **`threshold-met`**, PV1-M03 does **not** prove: global benchmark integrity; universal replay↔execution equivalence; ladder/public strength; live SC2 in CI as merge norm; multi-environment readiness; **PV1-M04** unless separately opened.

## Related

- `docs/runtime/pv1_tranche_a_execution_evidence_v1.md` (PV1-M02)
- `docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md` (PV1-M01)
- `docs/runtime/full_local_training_campaign_v1.md` (M49)
- `docs/runtime/industrial_hidden_rollout_mode_v1.md` (M50 / M51)
- Reproducible protocol fixture: `tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json`
