# PV1-M03 — Operator execution checklist (Tranche B / full-run threshold)

**Status:** **Historical operator recipe.** **PV1-M03** is **closed** on `main` (implementation [PR #77](https://github.com/m-cahill/starlab/pull/77); closeout [PR #78](https://github.com/m-cahill/starlab/pull/78)). **Tranche B** may be **completed within scope**; **full-run threshold** may still be **`threshold-not-met`** if the frozen **`full_run_duration_target`** is not satisfied — see **`docs/starlab.md`** for current ledger. This checklist does **not** open **PV1-M04**.

**Authoritative contracts:** `docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md` (public), `docs/starlab.md` (ledger).

---

## 1. Preconditions

- [ ] **Repository:** working tree matches **`main`** at or after merge **`9105a7ee6dff47acfb409f4cd08ca2693e98f9f1`** (PR **#77** implementation). Pull before working.
- [ ] **Tranche A:** `campaign_runs/pv1_m02_exec_001/` completed honestly for the frozen **`campaign_id`** below **or** you have documented **invalidation** per the runtime doc (do **not** mix incomparable trees for **`threshold-met`**).
- [ ] **Sealed M49 contract** lists **both** `tranche_a` and `tranche_b` `bootstrap_episodes` phases (plus M51 phases if in scope). Reconcile with **`tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json`** if re-emitting the contract (paths frozen at emit time — see M49 emitters).

---

## 2. Frozen kickoff (PV1-M03 — do not drift)

| Field | Value |
| --- | --- |
| `campaign_id` | `pv1_m02_tranche_a_2026_04_16` (continued — name may embed `tranche_a`) |
| Tranche B `execution_id` | **`pv1_m03_exec_001`** |
| Tranche A reference `execution_id` | **`pv1_m02_exec_001`** |
| `tranche_id` (Tranche B boundary) | **`tranche_b`** |
| `checkpoint_id` (Tranche B close) | **`tranche_b_close`** |
| `runtime_mode` | **`local_live_sc2`** (must match match config + M44 adapter policy) |
| M51 | **In scope:** `--post-bootstrap-protocol-phases` (weighted refit → M42 orchestration → watchable M44 when eligible) |

**Frozen threshold block** — evaluate **`threshold-met`** only against the table in **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`** (do not paraphrase numbers in declarations).

---

## 3. SC2 and environment

- [ ] **`STARLAB_SC2_ROOT`** (and binary layout per `docs/runtime/sc2_runtime_surface.md` / `starlab.sc2` env probe) resolves on this host.
- [ ] **Match config** map paths exist where the contract’s **`match_config_path`** points; **StarCraft II** can load the scenario for **`local_live_sc2`**.
- [ ] If **`emit_full_local_training_campaign_preflight`** or **execution** preflight reports **`preflight_ok`: false** (e.g. SC2 install probe, map resolution): **stop**, record the blocker in **`tranche_b_operator_note.md`**, declare **`threshold-not-met`** or **not evaluable** in **`full_run_threshold_declaration.md`** as appropriate — **do not** fabricate execution evidence.

---

## 4. Campaign root layout (local)

Use one stable campaign directory (example):

`out/training_campaigns/pv1_m02_tranche_a_2026_04_16/`

Expect at least before Tranche B:

- `full_local_training_campaign_contract.json`
- `campaign_preflight_receipt.json` (M49)
- `campaign_runs/pv1_m02_exec_001/` (Tranche A execution tree)

---

## 5. Command sequence (grounded in `main` CLIs)

**Protocol reference (read-only):** `tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json`

### 5a. M49 preflight (deterministic contract checks)

```bash
python -m starlab.training.emit_full_local_training_campaign_preflight \
  --campaign-contract <CAMP_ROOT>/full_local_training_campaign_contract.json \
  --output-dir <CAMP_ROOT>
```

Inspect **`campaign_preflight_receipt.json`** — **`preflight_ok`** must be **true** before execution unless you are intentionally stopping with an honest failure record.

### 5b. M50 / M51 executor — Tranche B continuation

Skip **Tranche A’s** `bootstrap_episodes` block (already completed under **`pv1_m02_exec_001`**); run **Tranche B** bootstrap + post-bootstrap protocol phases under a **fresh** execution id.

```bash
python -m starlab.training.execute_full_local_training_campaign \
  --campaign-contract <CAMP_ROOT>/full_local_training_campaign_contract.json \
  --campaign-root <CAMP_ROOT> \
  --execution-id pv1_m03_exec_001 \
  --skip-bootstrap-phases 1 \
  --post-bootstrap-protocol-phases \
  --requested-visibility-mode minimized
```

**Notes:**

- **`--skip-bootstrap-phases`** takes an **integer** `N`: skip the first **`N`** protocol phases with **`kind`:** **`bootstrap_episodes`** in order (not the `preflight` gate). With the default PV1-M03 fixture order (`tranche_a` then `tranche_b`), **`1`** skips **`tranche_a`** and runs **`tranche_b`**.
- **Do not** pass **`--skip-execution-preflight`** for real operator runs (tests only). On failure, inspect **`campaign_execution_preflight_receipt.json`** at **`<CAMP_ROOT>`** and stderr.
- If a **partial** tree exists for **`pv1_m03_exec_001`**, follow M50 quarantine / **`--allow-resume`** policy per **`docs/runtime/industrial_hidden_rollout_mode_v1.md`** — do not blindly delete evidence.

### 5c. Re-emit contract (only if required)

If the sealed contract does **not** yet include **`tranche_b`**, emit from the repo using the frozen protocol file (paths are operator-supplied):

```bash
python -m starlab.training.emit_full_local_training_campaign_contract \
  --campaign-id pv1_m02_tranche_a_2026_04_16 \
  --output-dir <CAMP_ROOT> \
  --hierarchical-training-run-dir <M43_RUN_DIR> \
  --benchmark-contract <BENCHMARK_CONTRACT.json> \
  --match-config <MATCH.json> \
  --runtime-mode local_live_sc2 \
  --planned-weighted-refit \
  --dataset <M26_replay_training_dataset.json> \
  --bundle-dir <M14_BUNDLE_DIR> \
  --campaign-protocol-json <REPO_ROOT>/tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json
```

Use the repository root for **`<REPO_ROOT>`** (or an absolute path to the fixture). Then re-run **§5a** and **§5b**. **Changing** `campaign_sha256` mid-stream may break honest aggregation — prefer governance review before re-sealing.

---

## 6. PV1-M01 inspection emitters (after execution material exists)

Scan only; they **do not** fabricate missing files:

```bash
python -m starlab.training.emit_campaign_observability_index \
  --campaign-root <CAMP_ROOT>

python -m starlab.training.emit_tranche_checkpoint_receipt \
  --campaign-root <CAMP_ROOT> \
  --tranche-id tranche_b \
  --checkpoint-id tranche_b_close \
  --operator-note-ref tranche_b_operator_note.md
```

Repeat or adjust **`--paused` / `--incomplete`** flags per actual operator posture.

---

## 7. Operator-authored files (campaign root)

| File | Purpose |
| --- | --- |
| **`tranche_b_operator_note.md`** | Tranche B **completed / not completed within scope** + **continue / pause / stop** — not the threshold verdict |
| **`full_run_threshold_declaration.md`** | Explicit **`threshold-met`** or **`threshold-not-met`** vs the **frozen** block — **not** blended with tranche posture |

---

## 8. Decide **`threshold-met`** vs **`threshold-not-met`**

- **`threshold-met`:** **All** frozen fields in the runtime doc satisfied **simultaneously** for the **`campaign_id`** boundary, with artifacts on disk matching the evidence table — **declared** honestly.
- **`threshold-not-met`:** Any required field fails, evidence incomplete, continuity broken, or SC2 preconditions failed — still a valid honest outcome.

---

## 9. If SC2 preconditions fail again

1. Record **failure mode** in **`tranche_b_operator_note.md`** (environment, probe output paths, **`preflight_ok`** details).
2. Do **not** claim **`threshold-met`**.
3. In **`full_run_threshold_declaration.md`**, declare **`threshold-not-met`** (or **not evaluable**) — **not** a **`PV1-M03_summary.md` / audit** closeout; milestone remains **open** until a chartered governance step says otherwise.

---

## 10. Related commands (reference)

| Module | Role |
| --- | --- |
| `starlab.training.emit_full_local_training_campaign_contract` | M49 contract + report |
| `starlab.training.emit_full_local_training_campaign_preflight` | M49 **`campaign_preflight_receipt.json`** |
| `starlab.training.execute_full_local_training_campaign` | M50/M51 executor |
| `starlab.training.emit_campaign_observability_index` | PV1-M01 index |
| `starlab.training.emit_tranche_checkpoint_receipt` | PV1-M01 checkpoint binding |
