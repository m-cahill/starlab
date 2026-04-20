# PX2 — Industrial self-play campaign (runtime v1)

**Version:** v1 — **slice 1** (contract, bridge, fixture smoke) + **slice 2** (execution skeleton, artifact tree, checkpoint/eval receipts) + **slice 3** (operator-local execution preflight, bounded real-weights smoke); **not** industrial campaign execution proof  
**Contract IDs (code):** `starlab.px2.self_play_campaign_contract.v1`, `starlab.px2.self_play_smoke_run.v1`, `starlab.px2.self_play_campaign_run.v1`, `starlab.px2.self_play_checkpoint_receipt.v1`, `starlab.px2.self_play_evaluation_receipt.v1`, `starlab.px2.self_play_execution_preflight.v1`, `starlab.px2.self_play_operator_local_smoke.v1`  
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

These appear as **explicit fields** on the campaign contract.

**Slice 1** — the **fixture smoke run** recorded **descriptive** placeholders only (`checkpoint_would_emit`, etc.).

**Slice 2** — bounded **checkpoint** and **evaluation** **receipt** JSON (+ reports) are emitted for fixture skeleton runs (see §8b). They make the control plane **more concrete** in-repo but are **not** industrial checkpoint persistence or real eval distributions. **Promotion** / **rollback** remain **stub** fields on the sealed campaign run (`promotion_posture_stub`, `rollback_posture_stub`).

**Retention** and **operator-local layout** expectations are described at the contract level; long-run behavior is **deferred** to later **`PX2-M03`** industrial execution.

---

## 8. Fixture-only smoke run

**Python:** `starlab.sc2.px2.self_play.smoke_run` — `run_px2_fixture_self_play_smoke`  
**Emitter CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_smoke_run --output-dir … --corpus-root …`

Uses a **PX2-M02-style** bundle corpus (e.g. test `tests/fixtures/px2_m02/corpus`) to **reuse** observation/game-state lineage. Emits:

- `px2_self_play_smoke_run.json` (sealed `smoke_sha256` where applicable)
- `px2_self_play_smoke_run_report.json`

The smoke path **does not** simulate a full SC2 match. It proves: contract load, bridge execution, opponent selection, decode/compile, and deterministic **bookkeeping** outputs.

---

## 8b. Slice 2 — Campaign execution skeleton (bounded, fixture-only)

**Python:** `starlab.sc2.px2.self_play.campaign_run` — `run_px2_campaign_execution_skeleton`  
**Emitter CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_campaign_execution_skeleton --output-dir … --corpus-root …`

**Purpose:** A **PX2-native** bounded loop that loads the slice-1 **campaign contract**, runs a **small multi-episode** fixture path (same **M02** corpus lineage as slice 1), uses the **policy bridge** and **opponent selection** per episode, and writes a **deterministic artifact tree** under a user-supplied directory.

**Typical files (not all are sealed):**

- `px2_self_play_campaign_run.json` / `px2_self_play_campaign_run_report.json` (sealed `run_sha256` on the run body)
- `run_manifest.json` — cadence overrides for skeleton (effective episode cadence so receipts appear in CI; **industrial runs** follow contract `checkpoint_posture` / `eval_posture` games, not these overrides)
- `checkpoint_receipts/ckpt_epNNN.json` + `*_report.json`
- `evaluation_receipts/eval_epNNN.json` + `*_report.json`

**Non-claims:** This is **slice-2 skeleton output**, **not** proof of a long industrial self-play campaign, **not** Blackwell completion, **not** ladder strength.

---

## 8c. Slice 3 — Operator-local execution preflight + bounded real-weights smoke

**Python:** `starlab.sc2.px2.self_play.execution_preflight` — `run_execution_preflight`; `starlab.sc2.px2.self_play.weight_loading` — `build_policy_operator_local`, `sha256_hex_file`; `starlab.sc2.px2.self_play.operator_local_smoke` — `run_operator_local_campaign_smoke`  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_execution_preflight …`; `python -m starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_smoke …`

**Purpose:** First **honest bridge** from fixture-only CI smoke to **operator-local readiness**: a **governed preflight receipt** (corpus root, output dir writable, policy weight mode, optional `torch`/platform notes) and a **small bounded** operator-local smoke that can load **real** `BootstrapTerranPolicy` **state_dict** from a user file (or use **explicit init-only** mode). Weight identity is recorded (**SHA-256** of the weights file + path note).

**Typical files:**

- `px2_self_play_execution_preflight.json` / `px2_self_play_execution_preflight_report.json` (sealed `preflight_sha256`)
- `px2_self_play_operator_local_smoke.json` / `px2_self_play_operator_local_smoke_report.json` (sealed `operator_local_smoke_sha256`)

**Non-claims:** Preflight is **readiness only** — **not** campaign success, **not** industrial completion, **not** Blackwell proof. Slice-3 smoke is **local-first**, **minutes-scale**, **not** the default merge-gate path. **Live SC2** and **GPU** remain **out of scope** for default CI.

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

## Surface coverage (slice 1 vs slice 2 vs slice 3 vs later `PX2-M03`)

| Surface | Slice 1 | Slice 2 | Slice 3 | Later industrial `PX2-M03` |
| --- | --- | --- | --- | --- |
| Campaign contract + report | Yes | Reused | Reused | Campaign-specific operator profiles |
| Policy→runtime bridge | Yes | Reused | Reused + **weight file / init-only** | Scaling, training loops |
| Opponent pool | Stub + selection | Same stub, multi-episode | Same stub | Full pool, anti-collapse |
| Checkpoint / eval | Contract placeholders | **Receipt JSON + reports** (fixture skeleton) | Same posture (optional) | Real persistence, real eval harness |
| Execution | Smoke JSON only | **Run manifest + sealed campaign run** | **Preflight + operator-local smoke** | Long runs, Blackwell-class intent |
| M49/M50/M51 | Reference | Reference | Reference | Optional adapter or native executor |

---

## Code map (reference)

| Module | Role |
| --- | --- |
| `starlab.sc2.px2.self_play.campaign_contract` | Campaign JSON + seal |
| `starlab.sc2.px2.self_play.policy_runtime_bridge` | Bridge |
| `starlab.sc2.px2.self_play.snapshot_pool` | Opponent pool stub |
| `starlab.sc2.px2.self_play.opponent_selection` | Selection rule IDs + `select_opponent_ref` |
| `starlab.sc2.px2.self_play.smoke_run` | Smoke orchestration |
| `starlab.sc2.px2.self_play.campaign_run` | Slice-2 execution skeleton |
| `starlab.sc2.px2.self_play.checkpoint_receipts` | Checkpoint receipt + report builders |
| `starlab.sc2.px2.self_play.evaluation_receipts` | Evaluation receipt + report builders |
| `starlab.sc2.px2.self_play.run_artifacts` | Manifest + JSON write helpers |
| `starlab.sc2.px2.self_play.emit_px2_self_play_campaign_contract` | Campaign emitter CLI |
| `starlab.sc2.px2.self_play.emit_px2_self_play_smoke_run` | Smoke emitter CLI |
| `starlab.sc2.px2.self_play.emit_px2_self_play_campaign_execution_skeleton` | Slice-2 skeleton emitter CLI |
| `starlab.sc2.px2.self_play.execution_preflight` | Slice-3 operator-local preflight |
| `starlab.sc2.px2.self_play.weight_loading` | Slice-3 policy weight load + file hash |
| `starlab.sc2.px2.self_play.operator_local_smoke` | Slice-3 bounded operator-local smoke |
| `starlab.sc2.px2.self_play.emit_px2_self_play_execution_preflight` | Preflight emitter CLI |
| `starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_smoke` | Operator-local smoke CLI |
