# PX2 — Industrial self-play campaign (runtime v1)

**Version:** v1 (PX2-M03 opening slice — contract, bridge, fixture smoke; **not** industrial execution proof)  
**Contract IDs (code):** `starlab.px2.self_play_campaign_contract.v1`, `starlab.px2.self_play_smoke_run.v1`  
**Related:** readiness / preflight `docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`; replay-bootstrap `docs/runtime/px2_neural_bootstrap_from_replays_v1.md` (PX2-M02); Terran surface `docs/runtime/px2_full_terran_runtime_action_surface_v1.md` (PX2-M01)

---

## 1. Purpose

This document defines the **public runtime posture** for **`PX2-M03` — Industrial Self-Play Campaign** on STARLAB: versioned **campaign contracts**, a **policy→runtime bridge** from the closed **PX2-M02** bootstrap policy to the **PX2-M01** Terran action surface, a **stub** snapshot/opponent pool with deterministic selection rules, **checkpoint/eval/promotion/rollback** fields at the contract level, and a **fixture-only** self-play **smoke** path suitable for CI.

**This slice exists to make opening `PX2-M03` operationally honest** — auditable infrastructure before any expensive operator-local run.

---

## 2. Boundary from PX2-M02

| Closed milestone | Delivers | Does **not** deliver |
| --- | --- | --- |
| **PX2-M02** | Governed replay-bootstrap dataset; `BootstrapTerranPolicy`; M18 flat feature adapter; legality-aware decode; offline eval; compile receipts | Self-play campaigns; industrial execution; strength proof |

**PX2-M03** builds **on** M02 by placing the same policy class inside **campaign-shaped** contracts and a reusable **bridge** that is not confined to offline eval scripts.

---

## 3. Relation to M49/M50/M51 governance patterns

The older **M49 / M50 / M51** stack remains a **useful governance precedent** for:

- Campaign and execution **contracts** and seals (`*_sha256`)
- **Checkpoint** discipline and operator-local **artifact layout** intentions
- **Preflight** and **receipt** hygiene

**Direct compatibility** between the legacy **sklearn-era** M49 campaign executor and a **PX2 `torch`** self-play loop is **not proved** in this slice and is **not** assumed. Adaptation or a PX2-native executor may be required; that work belongs **inside `PX2-M03`**, not as a pre-condition to this opening slice.

---

## 4. Campaign contract/profile

**Python:** `starlab.sc2.px2.self_play.campaign_contract` — `build_px2_self_play_campaign_artifacts`  
**Emitter CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_campaign_contract --output-dir …`

**Artifacts (typical basenames):**

- `px2_self_play_campaign_contract.json`
- `px2_self_play_campaign_contract_report.json`

**Minimum conceptual fields:**

- `campaign_id`, `campaign_profile_id` (with `contract_id` / sealed `campaign_sha256`)
- `seed_policy_ref` (bootstrap policy, feature adapter profile, deterministic seed in slice 1)
- `opponent_pool` / snapshot refs (stub)
- `opponent_selection_rule_id`
- `checkpoint_posture`, `eval_posture`, `promotion_posture`, `rollback_posture`
- `artifact_layout_expectations` under `out/` (operator-local; not merge-gate evidence)
- `runtime_modes`, explicit **`non_claims`**

---

## 5. Policy runtime bridge

**Python:** `starlab.sc2.px2.self_play.policy_runtime_bridge` — `bootstrap_policy_runtime_step`

**Required behavior:**

- Load or construct **`BootstrapTerranPolicy`** in a **bounded** way (slice 1: deterministic init + fixed seed; no committed weight fixtures required for smoke).
- Consume **M18-anchored** features via `features_tensor_from_observation` / `FEATURE_ADAPTER_PROFILE`.
- Run forward inference and **`decode_legality_aware`** (M02).
- Materialize **`TerranAction`**, then **`compile_terran_action`** → **`Px2InternalCommand`**, with **compile receipt** + **`receipt_sha256`** trace fields for smoke JSON.

This bridge is intentionally **not** a full RL or training abstraction.

---

## 6. Snapshot/opponent-pool stub

**Python:** `starlab.sc2.px2.self_play.snapshot_pool` — `build_default_opponent_pool_stub`

The opening implementation provides **named snapshot refs**, a **seed-policy** entry, and **opponent slots** for bookkeeping and tests. **Anti-collapse** and a full opponent pool are **partially specified** in the contract and **not** fully implemented in slice 1.

---

## 7. Checkpoint/eval/promotion/rollback posture

These appear as **explicit fields** on the campaign contract. The **fixture smoke run** may record **descriptive** outcomes only, for example:

- `checkpoint_would_emit` / `evaluation_would_run`
- `promotion_deferred_in_smoke`
- `rollback_not_triggered_in_smoke`

**Retention** and **operator-local layout** expectations are described at the contract level; long-run behavior is **deferred** to later **`PX2-M03`** execution.

---

## 8. Fixture-only smoke run

**Python:** `starlab.sc2.px2.self_play.smoke_run` — `run_px2_fixture_self_play_smoke`  
**Emitter CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_smoke_run --output-dir … --corpus-root …`

Uses a **PX2-M02-style** bundle corpus (e.g. test `tests/fixtures/px2_m02/corpus`) to **reuse** observation/game-state lineage. Emits:

- `px2_self_play_smoke_run.json` (sealed `smoke_sha256` where applicable)
- `px2_self_play_smoke_run_report.json`

The smoke path **does not** simulate a full SC2 match. It proves: contract load, bridge execution, opponent selection, decode/compile, and deterministic **bookkeeping** outputs.

---

## 9. Explicit non-claims

This slice **does not**:

- Prove **industrial** self-play execution or a **Blackwell** run
- Prove **autonomous strength**, ladder performance, or exploit closure
- Prove **executor compatibility** with M49/M50/M51 unchanged
- Replace **PX2-M04** / **PX2-M05** or open **v2**

**CI:** no live SC2, no GPU requirement, no long-running training loops in the default merge gate.

---

## 10. Operator-local future path

Later **`PX2-M03`** work may attach **operator-local** campaigns under `out/px2_self_play_campaigns/<campaign_id>/` (or as documented), with checkpoint/eval cycles, real opponent pools, and hardware-appropriate execution — **not** implied by this slice.

---

## Surface coverage (slice 1 vs later `PX2-M03`)

| Surface | Proved in slice 1 | Deferred to later `PX2-M03` work |
| --- | --- | --- |
| Versioned campaign contract + report JSON | Yes (emitters + seal) | Industrial campaign-specific profiles |
| Policy→runtime bridge (M02→M01) | Yes (CPU fixture path) | Production weight load, distributed inference |
| Snapshot/opponent pool | Stub + deterministic selection | Full pool, diversity metrics, anti-collapse enforcement |
| Checkpoint/eval/promotion/rollback | Contract + smoke placeholders | Real checkpoints, eval harness, promotion/rollback automation |
| Self-play smoke | Fixture-only, deterministic artifacts | Operator-local Blackwell-scale loops |
| M49/M50/M51 executor | N/A (reference only) | Optional adaptation or PX2-native executor |

---

## Code map (reference)

| Module | Role |
| --- | --- |
| `starlab.sc2.px2.self_play.campaign_contract` | Campaign JSON + seal |
| `starlab.sc2.px2.self_play.policy_runtime_bridge` | Bridge |
| `starlab.sc2.px2.self_play.snapshot_pool` | Opponent pool stub |
| `starlab.sc2.px2.self_play.opponent_selection` | Selection rule IDs + `select_opponent_ref` |
| `starlab.sc2.px2.self_play.smoke_run` | Smoke orchestration |
| `starlab.sc2.px2.self_play.emit_px2_self_play_campaign_contract` | Campaign emitter CLI |
| `starlab.sc2.px2.self_play.emit_px2_self_play_smoke_run` | Smoke emitter CLI |
