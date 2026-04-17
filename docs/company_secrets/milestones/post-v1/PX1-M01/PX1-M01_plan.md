# PX1-M01 — Full Industrial Campaign Execution Evidence — plan

**Status:** PR1 (opening) — governance, threshold freeze, runtime contract, checklist, fixture, tests. **Live SC2 execution** follows a separate **readiness checkpoint** (not this PR).

## Objective

Open **PX1-M01** on the public ledger; **freeze** the concrete PX1 full-run threshold block **before** any authoritative execution; publish **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; seed operator checklist + threshold freeze note; add **CI-safe** protocol fixture **`tests/fixtures/px1_m01/px1_m01_campaign_protocol.json`**; align governance tests.

**Definition of done (PR1):** Ledger + runtime + private artifacts + fixture + tests; **CI green**; **no** claim that the industrial run has completed; **no** live campaign execution in default CI.

## Frozen identities (PR1)

| Field | Value |
| --- | --- |
| `campaign_id` | `px1_m01_full_run_2026_04_17_a` |
| `execution_id` | `px1_m01_exec_001` |
| `runtime_mode` | `local_live_sc2` |

## Threshold package

Default target: recommended block in **`PX1-M01_threshold_freeze.md`** and public runtime doc. **Repo check:** M49 protocol supports per-phase `episode_budget`; **6+6** bootstrap episodes satisfies **`full_run_min_bootstrap_episodes_total` = 12** — **no numeric adjustment** at freeze.

## Out of scope (PR1)

- Authoritative operator-local run completion
- **`tranche_*_operator_note.md`**, **`px1_full_run_operator_note.md`**, **`full_run_threshold_declaration.md`** content from real execution (PR2 / execution phase)
- **PX1-M02** / **PX1-M03** / **v2** opening

## Execution path (after merge — operator-local, not default CI)

1. Emit M49 contract with **`--campaign-protocol-json`** pointing at **`tests/fixtures/px1_m01/px1_m01_campaign_protocol.json`** (or a copy under the campaign root as required by workflow).
2. Emit **`campaign_preflight_receipt.json`** (M49 preflight).
3. Run **`python -m starlab.training.execute_full_local_training_campaign`** with **`--post-bootstrap-protocol-phases`**, frozen **`--execution-id`**, **`local_live_sc2`** contract.
4. Emit observability index + checkpoint receipts per **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`**.
5. Write operator notes from **observed** results; **`full_run_threshold_declaration.md`** vs frozen block.

## PR split

- **PR1 (this branch):** open + freeze + docs + fixture + tests.
- **PR2:** closeout after real evidence; ledger honest **`threshold-met`** / **`threshold-not-met`**; **`current milestone`** → **None**; **PX1-M02** remains unopened unless separately authorized.

## References

- Locked answers (user): governance first; readiness report before live run; split PRs; operator notes from observation.
- `docs/runtime/px1_full_industrial_run_demo_charter_v1.md`
