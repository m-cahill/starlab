# PX1-M01 — operator checklist

**Milestone:** Full Industrial Campaign Execution Evidence  
**Threshold doc:** `docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`  
**Freeze:** `PX1-M01_threshold_freeze.md`  
**Ledger:** **PX1-M01** is **closed** on `main`; **`current milestone`** = **None** — see `docs/starlab.md` (§1 quick scan, §11, §23).

## Before authoritative execution

- [ ] Ledger lists **PX1-M01** **open** and threshold block **frozen** (PR1 merged).
- [ ] **`STARLAB_SC2_BIN`** / **`STARLAB_SC2_ROOT`** set for local SC2 (example: `C:\Program Files (x86)\StarCraft II\...`).
- [ ] Fresh **`campaign_id`** / **`execution_id`** — **not** PV1 identities (`px1_m01_full_run_2026_04_17_a` / `px1_m01_exec_001`).
- [ ] Campaign protocol shape: `tranche_a` → `tranche_b` → `optional_weighted_refit` → M51 tail (`watchable_m44_validation`, etc.) — mirror **`tests/fixtures/px1_m01/px1_m01_campaign_protocol.json`** for planning.
- [ ] Emit **`full_local_training_campaign_contract.json`** + report (`python -m starlab.training.emit_full_local_training_campaign_contract` … **`--runtime-mode local_live_sc2`** … **`--campaign-protocol-json`** …).
- [ ] Emit **`campaign_preflight_receipt.json`** (M49 preflight CLI).
- [ ] Run M50 executor preflight path (extended preflight on execute unless explicitly skipped in tests only).

## Execution (single primary execution_id)

- [ ] `python -m starlab.training.execute_full_local_training_campaign --campaign-contract <path/to/full_local_training_campaign_contract.json> --campaign-root <campaign_root> --execution-id px1_m01_exec_001 --post-bootstrap-protocol-phases`
- [ ] If continuation is required, use **`--allow-resume`** / **`--skip-bootstrap-phases`** only under governed resume rules; track invalidations (**must** stay **0**).

## After run (evidence)

- [ ] `hidden_rollout_campaign_run.json`, phase receipts, watchable M44 artifacts as applicable.
- [ ] `campaign_observability_index.json` + report.
- [ ] Checkpoint receipts under `checkpoints/tranche_a_close/`, `checkpoints/tranche_b_close/`.
- [ ] **`tranche_a_operator_note.md`**, **`tranche_b_operator_note.md`**, **`px1_full_run_operator_note.md`**, **`full_run_threshold_declaration.md`** — from **observed** facts only.

## PR2 closeout

- [x] Honest **`threshold-met`** or **`threshold-not-met`** (operator-local: **`threshold-met`**).
- [x] **`PX1-M02`** remains **unopened** unless separately authorized.
- [x] **`v2`** remains **unopened**.
- [x] Ledger updated: **`PX1-M01`** **closed**; **`current milestone`** = **None** (governance closeout PR — see `docs/starlab.md` / `PX1-M01_run2.md`).
