# PX2 — Industrial self-play campaign (runtime v1)

**Version:** v1 — **slice 1** (contract, bridge, fixture smoke) + **slice 2** (execution skeleton, artifact tree, checkpoint/eval receipts) + **slice 3** (operator-local execution preflight, bounded real-weights smoke) + **slice 4** (bounded multi-step continuity, sealed linkage, promotion/rollback receipt surfaces) + **slice 5** (operator-local campaign-root manifest, expanded opponent pool, deterministic rotation / selection recording) + **slice 6** (preflight logical-path seal normalization, canonical operator-local campaign-root smoke path) + **slice 7** (first bounded operator-local non-Blackwell real-run execution record) + **slice 8** (bounded operator-local multi-run session under one campaign root) + **slice 9** (bounded session + one governed promotion/rollback execution step) + **slice 10** (bounded current-candidate carry-forward after session transition) + **slice 11** (bounded continuation run that consumes `px2_self_play_current_candidate.json`) + **slice 12** (bounded post-continuation current-candidate re-anchoring) + **slice 13** (bounded second continuation hop on the refreshed pointer + optional symmetric re-anchor) + **slice 14** (bounded operator-local run explicitly **seeded** from the latest **`px2_self_play_current_candidate.json`** as the declared starting source of truth) + **slice 15** (bounded post–pointer-seeded **handoff** record declaring the slice-14 seeded run as the governed lineage source for the next bounded step); **not** industrial campaign execution proof  
**Contract IDs (code):** `starlab.px2.self_play_campaign_contract.v1`, `starlab.px2.self_play_smoke_run.v1`, `starlab.px2.self_play_campaign_run.v1`, `starlab.px2.self_play_checkpoint_receipt.v1`, `starlab.px2.self_play_evaluation_receipt.v1`, `starlab.px2.self_play_execution_preflight.v1`, `starlab.px2.self_play_operator_local_smoke.v1`, `starlab.px2.self_play_campaign_continuity.v1`, `starlab.px2.self_play_promotion_receipt.v1`, `starlab.px2.self_play_rollback_receipt.v1`, `starlab.px2.self_play_campaign_root_manifest.v1`, `starlab.px2.self_play_operator_local_real_run.v1`, `starlab.px2.self_play_operator_local_session.v1`, `starlab.px2.self_play_operator_local_session_transition.v1`, `starlab.px2.self_play_current_candidate.v1`, `starlab.px2.self_play_continuation_run.v1`, `starlab.px2.self_play_current_candidate_reanchor.v1`, `starlab.px2.self_play_second_hop_continuation.v1`, `starlab.px2.self_play_pointer_seeded_run.v1`, `starlab.px2.self_play_pointer_seeded_handoff.v1`  
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

**Slice 4** — explicit **promotion** and **rollback** **receipt** JSON (+ reports) per continuity step (see §8d), linked to eval/checkpoint seals — transitions remain **deterministic/stubbed**; **not** **PX2-M04** exploit closure.

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

- `px2_self_play_execution_preflight.json` / `px2_self_play_execution_preflight_report.json` (sealed `preflight_sha256` over **`preflight_seal_basis`** — logical corpus/output/weights identity; **slice 6** — absolute paths remain in JSON and in `operator_absolute_paths_advisory` on the report, **not** in the seal)
- `px2_self_play_operator_local_smoke.json` / `px2_self_play_operator_local_smoke_report.json` (sealed `operator_local_smoke_sha256`)

**Non-claims:** Preflight is **readiness only** — **not** campaign success, **not** industrial completion, **not** Blackwell proof. Slice-3 smoke is **local-first**, **minutes-scale**, **not** the default merge-gate path. **Live SC2** and **GPU** remain **out of scope** for default CI. **Slice 6** refines **what** is sealed (logical-path basis) **without** claiming full machine portability of every JSON field.

---

## 8d. Slice 4 — Multi-step continuity + sealed linkage (operator-local)

**Python:** `starlab.sc2.px2.self_play.campaign_continuity` — `run_operator_local_campaign_continuity`; `starlab.sc2.px2.self_play.promotion_receipts` / `starlab.sc2.px2.self_play.rollback_receipts`; extended checkpoint/eval builders in `checkpoint_receipts` / `evaluation_receipts`; layout helpers in `run_artifacts` (`default_operator_local_slice4_subdirs`, `ensure_operator_local_slice4_layout`).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_campaign_continuity …`

**Purpose:** A **small fixed** number of continuity steps (2–3 clamped) after slice-3 **preflight**, with **checkpoint → evaluation** linkage, **promotion** and **rollback** receipts per step, and a **continuity chain** seal. Later steps link to **prior** checkpoint/eval seals; all steps record **campaign**, **run**, **preflight**, and **weight identity**.

**Operator-local layout (under the run root you pass to `--output-dir`):**

| Relative path | Role |
| --- | --- |
| `px2_self_play_execution_preflight.json` (+ `_report`) | Slice-3 preflight (reused) |
| `px2_self_play_campaign_continuity.json` (+ `_report`) | Sealed continuity run summary (`continuity_sha256`) |
| `continuity_chain.json` | Ordered step seals + `continuity_chain_sha256` |
| `run_manifest.json` | Slice-4 manifest (`operator_local_layout` map) |
| `checkpoint_receipts/ckpt_stepNNN.json` (+ `_report`) | Per-step checkpoint receipts (slice-4 linkage fields) |
| `evaluation_receipts/eval_stepNNN.json` (+ `_report`) | Per-step eval receipts (link to same-step checkpoint seal) |
| `promotion_receipts/promotion_stepNNN.json` (+ `_report`) | Explicit promotion decisions (stub transition logic id) |
| `rollback_receipts/rollback_stepNNN.json` (+ `_report`) | Explicit rollback posture (default `triggered: false` on stub path) |

**Non-claims:** **Continuity proof** only — **not** industrial long-run self-play; **not** Blackwell; **not** real promotion/exploit policy (**PX2-M04** remains separate); **not** merge-gate CI.

---

## 8e. Slice 5 — Operator-local campaign root manifest + opponent rotation hardening

**Python:** `starlab.sc2.px2.self_play.campaign_root` — `run_slice5_operator_local_campaign`, `ensure_operator_local_campaign_root_layout`, `recommended_operator_out_campaign_root_path`; `starlab.sc2.px2.self_play.campaign_root_manifest` — `build_px2_self_play_campaign_root_manifest_artifacts`; `starlab.sc2.px2.self_play.snapshot_pool` — `build_slice5_opponent_pool`, `opponent_battle_ref_ids`, `opponent_pool_identity_sha256`; `starlab.sc2.px2.self_play.opponent_rotation` — `build_opponent_rotation_trace`; `starlab.sc2.px2.self_play.opponent_selection` — `OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB` (deterministic weighted expansion + step index).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_slice5_campaign_root --campaign-root … --corpus-root …`

**Purpose:** A **governed operator-local campaign root** that (1) holds **opponent-pool metadata** (`opponent_pool/px2_opponent_pool_metadata.json` with `opponent_pool_identity_sha256`), (2) runs **bounded slice-4-class continuity** under `runs/<run_id>/` (same receipt folders as §8d), and (3) seals a **campaign-root manifest** at the root binding `campaign_id`, **linked** `campaign_contract_sha256`, **canonical** `root_path_expected` pattern (`out/px2_self_play_campaigns/<campaign_id>/`), **allowed** top-level subdirectories, **per-run** continuity references, and **opponent-pool identity**. Continuity JSON records **`opponent_rotation_trace`** per episode for audit bookkeeping.

**Operator-local layout (campaign root — mirror under a temp or `out/` tree; nothing here is merge-gate CI proof):**

| Relative path | Role |
| --- | --- |
| `px2_self_play_campaign_root_manifest.json` (+ `_report`) | Sealed campaign-root manifest (`campaign_root_manifest_sha256`) |
| `opponent_pool/px2_opponent_pool_metadata.json` | Bounded expanded pool + identity seal — **not** a full anti-collapse system |
| `runs/<run_id>/` | One continuity run root — contains §8d layout (`checkpoint_receipts/`, `evaluation_receipts/`, `promotion_receipts/`, `rollback_receipts/`, preflight, continuity JSON, `run_manifest.json`, `continuity_chain.json`) |

**Non-claims:** **Still not** the industrial self-play campaign; **not** Blackwell-scale execution; **not** gameplay-diversity or ladder-strength proof; **not** merge-gate default CI; opponent rotation is **traceability / bookkeeping**, not an anti-collapse product.

---

## 8f. Slice 6 — Preflight seal normalization + canonical operator-local campaign-root smoke path

**Python:** `starlab.sc2.px2.self_play.path_identity` — `build_preflight_seal_basis`, logical path helpers; `starlab.sc2.px2.self_play.execution_preflight` — `preflight_seal_basis` + `preflight_sha256`; `starlab.sc2.px2.self_play.canonical_operator_local_run` — `resolve_canonical_campaign_root`, `run_canonical_operator_local_campaign_root_smoke` (slice-6 `execution_kind` via `campaign_root`).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_canonical_campaign_root_smoke --corpus-root … [--base-dir …] --init-only` (or `--weights …` for bounded real-weights continuity).

**Purpose:** (1) **Seal normalization** — `preflight_sha256` hashes only **`preflight_seal_basis`** (contract id, `preflight_seal_version`, logical corpus ref under `tests/fixtures/…` when applicable, run-scoped output identity, basename-only weights when used, stable check id/status list, etc.). Absolute `corpus_root` / `output_dir` / `weights_path` strings remain in emitted preflight JSON for operators; the **report** includes **`operator_absolute_paths_advisory`** for the same. (2) **Canonical golden path** — bounded smoke under **`out/px2_self_play_campaigns/<campaign_id>/`** (resolved from `--base-dir`, defaulting to the process working directory), reusing the **slice-5** layout (`opponent_pool/`, `runs/<run_id>/` with §8d receipts) but tagged with **`execution_kind`** `px2_m03_slice6_canonical_operator_local_campaign_root_smoke_v1` and profile `px2_m03_slice6_canonical_campaign_root_smoke_v1`.

**Non-claims:** **Not** industrial long-run self-play; **not** Blackwell default; **not** merge-gate CI; **not** full portability of every artifact field — only the **designed** sealed preflight basis is stable across temp roots when inputs match logically.

---

## 8g. Slice 7 — First bounded operator-local non-Blackwell real-run execution record

**Python:** `starlab.sc2.px2.self_play.operator_local_real_run` — `run_bounded_operator_local_real_run`; `starlab.sc2.px2.self_play.operator_local_real_run_record` — `build_px2_self_play_operator_local_real_run_artifacts` (sealed **`operator_local_real_run_sha256`** over a logical **seal basis**, no absolute paths in the hash input).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_real_run --corpus-root … [--base-dir …] --init-only` (or `--weights …`).

**Purpose:** Runs the **same** campaign-root + continuity receipt tree as slices **5–6** (under `out/px2_self_play_campaigns/<campaign_id>/`), with **`execution_kind`** `px2_m03_slice7_bounded_operator_local_real_run_v1`, then writes **top-level** `px2_self_play_operator_local_real_run.json` + `_report.json` binding campaign-, preflight-, continuity-, manifest-, weight-, and pool identities. **Optional operator note:** convention documented in JSON as `operator_note_convention` — place a human note at `out/px2_self_play_campaigns/<campaign_id>/px2_operator_local_real_run_operator_note.md` (not sealed; not required).

**Non-claims:** **Not** industrial self-play campaign; **not** Blackwell-scale / long-wall-clock; **not** ladder strength; **not** merge-gate CI — this is the **smallest first-class** bounded **real filesystem** execution record, not scale proof.

---

## 8h. Slice 8 — Bounded operator-local multi-run session (one campaign root)

**Python:** `starlab.sc2.px2.self_play.operator_local_session` — `run_bounded_operator_local_session`; `starlab.sc2.px2.self_play.operator_local_session_record` — `build_px2_self_play_operator_local_session_artifacts` (sealed **`operator_local_session_sha256`**).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session --corpus-root … [--base-dir …] --init-only` (or `--weights …`).

**Purpose:** Runs **two or more** bounded slice-5-class continuity passes under the **same** `out/px2_self_play_campaigns/<campaign_id>/` tree with **distinct** `run_id`s (`runs/<run_id>/…` each). Writes one **aggregated** `px2_self_play_campaign_root_manifest.json` listing **all** runs, then **per-run** `runs/<run_id>/px2_self_play_operator_local_real_run.json` (slice-8 **`execution_kind`**, seal includes the **final** root-manifest hash), and **top-level** `px2_self_play_operator_local_session.json` + `_report.json` binding ordered run ids and per-run real-run seals. **Optional operator note:** `operator_note_convention` → `px2_operator_local_session_operator_note.md` under the campaign root (not sealed).

**Non-claims:** **Not** industrial self-play; **not** long-horizon Blackwell execution; **not** ladder strength; **not** merge-gate default CI — **session bookkeeping** across multiple tiny bounded runs, not scale proof.

---

## 8i. Slice 9 — Bounded session + one governed promotion/rollback execution step

**Python:** `starlab.sc2.px2.self_play.operator_local_session_transition` — `run_bounded_operator_local_session_with_transition`; `starlab.sc2.px2.self_play.operator_local_session_transition_record` — `build_px2_self_play_operator_local_session_transition_artifacts` (sealed **`operator_local_session_transition_sha256`**).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session_transition --corpus-root … --transition promotion|rollback [--base-dir …] --init-only` (or `--weights …`).

**Purpose:** Runs the **slice-8** multi-run session (same tree), then records **one** deterministic **session-level** transition — **`promotion`** (stub: bind to **last** run’s **final** promotion / checkpoint / eval lineage) or **`rollback`** (stub: bind **current** candidate to **first** run’s **first** checkpoint, with a **reference** to the **last** run’s final rollback receipt for audit). **Not** **PX2-M04** exploit closure; **not** strength certification; **not** broader ranking semantics.

**Non-claims:** **Not** industrial campaign; **not** exploit resolution; **not** merge-gate default CI — operational **receipt linkage** only.

---

## 8j. Slice 10 — Bounded current-candidate carry-forward after session transition

**Python:** `starlab.sc2.px2.self_play.current_candidate` — `run_bounded_operator_local_session_transition_with_current_candidate`; `next_run_preflight_hints_from_current_candidate`; `starlab.sc2.px2.self_play.current_candidate_record` — `build_px2_self_play_current_candidate_artifacts` (sealed **`current_candidate_sha256`**).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_current_candidate --corpus-root … --transition promotion|rollback [--base-dir …] --init-only` (or `--weights …`).

**Purpose:** After the **slice-9** transition, records **`px2_self_play_current_candidate.json`** (+ report) binding **session** + **transition** seals to a deterministic **anchor** (continuity `run_id`, step index, **checkpoint receipt** SHA, **`weight_identity`**) so the **next** bounded operator-local preflight/run can **read** carry-forward state **without** re-deriving the full session. **Not** “best policy” globally; **not** **PX2-M04** exploit closure; **not** industrial execution.

**Non-claims:** **Not** industrial campaign; **not** strength certification; **not** merge-gate default CI — **pointer + lineage** only.

---

## 8k. Slice 11 — Bounded continuation run consuming the current-candidate pointer

**Python:** `starlab.sc2.px2.self_play.continuation_run` — `validate_current_candidate_for_continuation_run`, `run_bounded_continuation_run_consuming_current_candidate`, `merge_campaign_root_manifest_after_continuation_run`; `starlab.sc2.px2.self_play.continuation_run_record` — `build_px2_self_play_continuation_run_artifacts` (sealed **`continuation_run_sha256`** over a logical seal basis).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_continuation_run --campaign-root … --campaign-id … --continuation-run-id … --corpus-root … --init-only` (or `--weights …`).

**Purpose:** After **slice 10**, the next bounded operator-local step **must** **load** **`px2_self_play_current_candidate.json`**, **check** that declared **campaign**, **session**, **transition**, **manifest**, and **weight** hints **match** the run inputs, then run **one** **slice-5-class** continuity pass (`execution_kind` **`px2_m03_slice11_bounded_continuation_run_consuming_candidate_v1`**) **without** overwriting the multi-run **campaign-root manifest** (the run **merges** a new `runs/<run_id>/` reference). Emits **`px2_self_play_continuation_run.json`** + **`px2_self_play_continuation_run_report.json`** with **`consumption_status`** **`consumed_ok`** or **`rejected_mismatch`** (explicit **`mismatch_reasons`**). **Not** industrial execution; **not** **PX2-M04** exploit closure.

**Non-claims:** **Not** industrial self-play campaign; **not** global best-policy semantics; **not** merge-gate default CI — **consumption bookkeeping** for the next bounded step only.

---

## 8l. Slice 12 — Bounded post-continuation current-candidate re-anchoring

**Python:** `starlab.sc2.px2.self_play.current_candidate_reanchor` — `run_bounded_current_candidate_reanchor_after_continuation`; `starlab.sc2.px2.self_play.current_candidate_reanchor_record` — `build_px2_self_play_current_candidate_reanchor_artifacts` (sealed **`current_candidate_reanchor_sha256`**); refreshes **`px2_self_play_current_candidate.json`** with **`execution_kind`** **`px2_m03_slice12_bounded_current_candidate_reanchor_after_continuation_v1`** and record version **`px2_m03_slice12_current_candidate_reanchor_after_continuation_v1`**.  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_current_candidate_reanchor --campaign-root … --campaign-id …`

**Purpose:** After **`consumed_ok`** slice-11 **`px2_self_play_continuation_run.json`**, **re-point** the campaign cursor by emitting a **new** sealed **`px2_self_play_current_candidate.json`** whose **anchor** is the **continuation run’s** final checkpoint / **`weight_identity`**, plus **`px2_self_play_current_candidate_reanchor.json`** (+ report) binding **prior** current-candidate seal, **continuation-run** seal, and **refreshed** current-candidate seal. **Rejects** (honest **`reanchor_status`**) when continuation was not **`consumed_ok`** or required files are missing. **Not** industrial execution; **not** **PX2-M04** exploit closure.

**Non-claims:** **Not** industrial campaign; **not** strength proof; **not** merge-gate default CI — **pointer refresh** after a bounded continuation only.

---

## 8m. Slice 13 — Bounded second-hop continuation (and optional symmetric re-anchor)

**Python:** `starlab.sc2.px2.self_play.second_hop_continuation` — `validate_post_slice12_state_for_second_hop`, `run_bounded_second_hop_continuation_after_slice12` (snapshots **`px2_self_play_first_hop_continuation_snapshot.json`** + **`px2_self_play_slice12_reanchor_snapshot.json`**, then second **`run_bounded_continuation_run_consuming_current_candidate`** with **`execution_kind`** **`px2_m03_slice13_bounded_second_hop_continuation_consuming_candidate_v1`**); `starlab.sc2.px2.self_play.second_hop_continuation_record` — `build_px2_self_play_second_hop_continuation_artifacts` (sealed **`second_hop_continuation_sha256`**); **`current_candidate_reanchor.run_bounded_current_candidate_reanchor_after_second_hop`** when **`symmetric_reanchor`** is enabled (refreshes **`px2_self_play_current_candidate.json`** with **`execution_kind`** **`px2_m03_slice13_bounded_current_candidate_reanchor_after_second_hop_v1`** / record version **`px2_m03_slice13_current_candidate_reanchor_after_second_hop_v1`**).  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_second_hop_continuation --campaign-root … --campaign-id … --corpus-root … --init-only` (optional `--no-symmetric-reanchor`).

**Purpose:** After **slice 12**, prove **repeatability**: run **one** additional bounded continuation that **consumes** the **post-slice-12** **`px2_self_play_current_candidate.json`**, emit **`px2_self_play_second_hop_continuation.json`** (+ report) binding **prior** current-candidate, **first-hop** continuation, **slice-12** re-anchor, and **second-hop** continuation seals, then optionally **re-anchor** again so the **cursor** advances **twice** under the same operator-local root — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Non-claims:** **Not** industrial campaign; **not** multi-hop strength proof; **not** merge-gate default CI — **bounded hop bookkeeping** only.

---

## 8n. Slice 14 — Bounded pointer-seeded operator-local run (`px2_self_play_pointer_seeded_run.json`)

**Python:** `starlab.sc2.px2.self_play.pointer_seeded_run` — `verify_loaded_current_candidate_self_seal`, `run_bounded_pointer_seeded_operator_local_run`; `starlab.sc2.px2.self_play.pointer_seeded_run_record` — `build_px2_self_play_pointer_seeded_run_artifacts` (sealed **`pointer_seeded_run_sha256`**); continuity + root manifest use **`execution_kind`** **`px2_m03_slice14_bounded_pointer_seeded_from_current_candidate_v1`**.  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_pointer_seeded_run --campaign-root … --campaign-id … --pointer-seeded-run-id … --corpus-root … --init-only` (or `--weights …`).

**Purpose:** After slices **10–13** established carry-forward, consumption, re-anchor, and second-hop continuation, **slice 14** binds the **next** bounded operator-local pass to the **latest** **`px2_self_play_current_candidate.json`** as the **declared seed** (not merely an optional hint): the loader **recomputes** the current-candidate **self-seal**, **re-applies** **`validate_current_candidate_for_continuation_run`**, then runs **one** **slice-5-class** continuity pass and appends the manifest. Emits **`px2_self_play_pointer_seeded_run.json`** + **`px2_self_play_pointer_seeded_run_report.json`** with **`seeding_status`** **`seeded_ok`** or **`rejected_mismatch`** / **`rejected_missing_pointer`** and explicit **`seed_semantics`**. The manifest may include a **`seed_source_file_byte_sha256_advisory`** (not sealed) because the on-disk JSON can embed path-advisory fields. **Not** industrial execution; **not** **PX2-M04** exploit closure.

**Non-claims:** **Not** industrial self-play campaign; **not** global best-policy certification; **not** merge-gate default CI — **declared-seed bookkeeping** for one bounded local pass only.

---

## 8o. Slice 15 — Bounded post–pointer-seeded handoff (`px2_self_play_pointer_seeded_handoff.json`)

**Python:** `starlab.sc2.px2.self_play.pointer_seeded_handoff` — `verify_loaded_pointer_seeded_run_self_seal`, `run_bounded_pointer_seeded_handoff`; `starlab.sc2.px2.self_play.pointer_seeded_handoff_record` — `build_px2_self_play_pointer_seeded_handoff_artifacts` (sealed **`pointer_seeded_handoff_sha256`**); **`handoff_execution_kind`** **`px2_m03_slice15_bounded_post_pointer_seeded_handoff_v1`**.  
**CLI:** `python -m starlab.sc2.px2.self_play.emit_px2_self_play_pointer_seeded_handoff --campaign-root … --campaign-id …`

**Purpose:** After **slice 14** produced a **`seeded_ok`** **`px2_self_play_pointer_seeded_run.json`**, **slice 15** is the first bounded step that treats that **artifact** (not merely “a pointer existed elsewhere”) as the **declared governed lineage source** for what follows: **revalidate** the pointer-seeded **self-seal**, **re-check** continuity + campaign-root manifest **SHAs** against the on-disk tree, **bind** **`prior_pointer_seeded_run_sha256`**, **`slice14_resulting_continuity_sha256`**, and manifest/contract/opponent identity at handoff, and emit **`px2_self_play_pointer_seeded_handoff.json`** + **`px2_self_play_pointer_seeded_handoff_report.json`** with explicit **`declared_next_step_source_lineage`** and **`non_claims`**. **Rejects** missing/stale/tampered pointer-seeded or continuity/manifest linkage **honestly** (`handoff_status` + `rejection_reasons`). **Not** a second slice-5 continuity execution round by default (this slice is **validation + handoff record**); **not** industrial execution; **not** **PX2-M04** exploit closure.

**Non-claims:** **Not** industrial self-play campaign; **not** exploit closure; **not** merge-gate default CI — **lineage handoff bookkeeping** for the next bounded step only.

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

Later **`PX2-M03`** industrial execution is expected to **reuse** the **slice-5/6/7/8/9/10/11/12/13/14/15** campaign-root discipline: canonical `out/px2_self_play_campaigns/<campaign_id>/`, `runs/<run_id>/` continuity trees, `opponent_pool/` metadata, sealed root + continuity manifests, **slice-6** preflight **logical** seal basis, **slice-7** bounded **real-run** record JSON, **slice-8** **multi-run** session records, **slice-9** **session transition** receipts, **slice-10** **current-candidate** carry-forward, **slice-11** **current-candidate consumption** / continuation receipts, **slice-12** **post-continuation current-candidate re-anchoring**, **slice-13** **second-hop** continuation + optional symmetric re-anchor, **slice-14** **pointer-seeded** bounded pass receipts, and **slice-15** **post–pointer-seeded handoff** records — then add **long-run** checkpoint/eval cycles and hardware-appropriate execution — **not** implied by slices 1–15 alone.

---

## Surface coverage (slice 1 vs slice 2 vs slice 3 vs slice 4 vs slice 5 vs slice 6 vs slice 7 vs slice 8 vs slice 9 vs slice 10 vs slice 11 vs slice 12 vs slice 13 vs slice 14 vs slice 15 vs later `PX2-M03`)

| Surface | Slice 1 | Slice 2 | Slice 3 | Slice 4 | Slice 5 | Slice 6 | Slice 7 | Slice 8 | Slice 9 | Slice 10 | Slice 11 | Slice 12 | Slice 13 | Slice 14 | Slice 15 | Later industrial `PX2-M03` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Campaign contract + report | Yes | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Campaign-specific operator profiles |
| Policy→runtime bridge | Yes | Reused | Reused + **weight file / init-only** | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Reused | Scaling, training loops |
| Opponent pool | Stub + selection | Same stub, multi-episode | Same stub | Same stub | **Expanded bounded pool + identity seal** | Same | Same | Same | Same | Same | Same | Same | Same | Same | Same | Full pool, anti-collapse |
| Checkpoint / eval | Contract placeholders | **Receipt JSON + reports** (fixture skeleton) | Same posture (optional) | **Linked** checkpoint/eval per step | Same (under `runs/<run_id>/`) | Same | Same | Same | Same | **Anchor** to selected checkpoint receipt | **Consumed** anchor in continuation record | **Re-anchored** to continuation final step | **Second-hop** consumed + re-anchored | **Declared-seed** snapshot from current-candidate anchor | N/A (validates slice-14 continuity seals) | Real persistence, real eval harness |
| Promotion / rollback | Contract placeholders | Stub on campaign run | N/A | **Dedicated receipt JSON + reports** | Same | Same | Same | Same | **Session-level stub transition + receipt lineage** | **Carry-forward** binds transition → candidate pointer | **Continuation** after validated consumption | **Re-anchor** refresh (not new transition) | **Symmetric re-anchor** (not new transition) | N/A (same lineage checks as slice 11) | N/A | Real policy |
| Campaign root / traceability | N/A | N/A | N/A | Single run root | **Root manifest + pool metadata + rotation traces** | **Canonical smoke + logical preflight seal basis** | **Top-level real-run record + optional operator note** | **Multi-run root manifest + session JSON + per-run real-run under `runs/`** | **+ `px2_self_play_operator_local_session_transition.json`** | **+ `px2_self_play_current_candidate.json`** | **+ `px2_self_play_continuation_run.json`** (manifest append) | **+ `px2_self_play_current_candidate_reanchor.json`** | **+ `px2_self_play_second_hop_continuation.json`** (+ snapshots) | **+ `px2_self_play_pointer_seeded_run.json`** (declared seed bound) | **+ `px2_self_play_pointer_seeded_handoff.json`** (slice-14 lineage handoff) | Industrial bookkeeping |
| Execution | Smoke JSON only | **Run manifest + sealed campaign run** | **Preflight + operator-local smoke** | **Preflight + multi-step continuity + chain seal** | **Campaign root + continuity under `runs/`** | **Bounded canonical smoke (slice-6 kind)** | **Bounded real run (slice-7 kind)** | **Bounded multi-run session (slice-8 kind)** | **Bounded session + transition (slice-9 kind)** | **Transition + candidate pointer (slice-10 kind)** | **Continuation run consuming candidate (slice-11 kind)** | **Re-anchor current-candidate (slice-12 kind)** | **Second-hop continuation (+ optional re-anchor)** (slice-13 kind) | **Pointer-seeded bounded run (slice-14 kind)** | **Handoff validation + record (slice-15 kind)** | Long runs, Blackwell-class intent |
| Preflight seal | N/A | N/A | Full JSON + seal | Reused | Reused | **Logical-path `preflight_seal_basis`** | Reused | Reused | Reused | Hints via **`next_run_preflight_hints_from_current_candidate`** | Validated vs **current-candidate** fields | Refreshed **`px2_self_play_current_candidate.json`** | Same + **second-hop** lineage | **Self-seal** + same validation path | N/A | Industrial preflight |
| Real-run execution record | N/A | N/A | N/A | N/A | N/A | N/A | **`px2_self_play_operator_local_real_run.json`** (root) | **Per-run** `…/runs/<run_id>/px2_self_play_operator_local_real_run.json` + **`px2_self_play_operator_local_session.json`** | Same + **transition** record | Same + **current-candidate** record | Same + **continuation-run** record | Same + **re-anchor** record | Same + **second-hop** record | Same + **pointer-seeded-run** record | **+ `px2_self_play_pointer_seeded_handoff.json`** | Industrial run ledgers |
| M49/M50/M51 | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Reference | Optional adapter or native executor |

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
| `starlab.sc2.px2.self_play.campaign_continuity` | Slice-4 multi-step continuity orchestration |
| `starlab.sc2.px2.self_play.promotion_receipts` | Promotion receipt + report builders |
| `starlab.sc2.px2.self_play.rollback_receipts` | Rollback receipt + report builders |
| `starlab.sc2.px2.self_play.emit_px2_self_play_campaign_continuity` | Slice-4 continuity CLI |
| `starlab.sc2.px2.self_play.campaign_root` | Slice-5 campaign-root orchestration |
| `starlab.sc2.px2.self_play.campaign_root_manifest` | Sealed campaign-root manifest |
| `starlab.sc2.px2.self_play.opponent_rotation` | Per-step opponent rotation trace |
| `starlab.sc2.px2.self_play.emit_px2_self_play_slice5_campaign_root` | Slice-5 campaign-root CLI |
| `starlab.sc2.px2.self_play.path_identity` | Slice-6 preflight logical-path seal basis |
| `starlab.sc2.px2.self_play.canonical_operator_local_run` | Slice-6 canonical campaign-root smoke orchestration |
| `starlab.sc2.px2.self_play.emit_px2_self_play_canonical_campaign_root_smoke` | Slice-6 canonical campaign-root smoke CLI |
| `starlab.sc2.px2.self_play.operator_local_real_run` | Slice-7 bounded operator-local real-run orchestration |
| `starlab.sc2.px2.self_play.operator_local_real_run_record` | Slice-7 real-run JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_real_run` | Slice-7 bounded real-run CLI |
| `starlab.sc2.px2.self_play.operator_local_session` | Slice-8 bounded multi-run session orchestration |
| `starlab.sc2.px2.self_play.operator_local_session_record` | Slice-8 session JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session` | Slice-8 bounded session CLI |
| `starlab.sc2.px2.self_play.operator_local_session_transition` | Slice-9 session + promotion/rollback step |
| `starlab.sc2.px2.self_play.operator_local_session_transition_record` | Slice-9 transition JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_operator_local_session_transition` | Slice-9 session-transition CLI |
| `starlab.sc2.px2.self_play.current_candidate` | Slice-10 transition + current-candidate carry-forward |
| `starlab.sc2.px2.self_play.current_candidate_record` | Slice-10 current-candidate JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_current_candidate` | Slice-10 current-candidate CLI |
| `starlab.sc2.px2.self_play.continuation_run` | Slice-11 continuation run + current-candidate validation |
| `starlab.sc2.px2.self_play.continuation_run_record` | Slice-11 continuation-run JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_continuation_run` | Slice-11 continuation-run CLI |
| `starlab.sc2.px2.self_play.current_candidate_reanchor` | Slice-12 post-continuation re-anchor orchestration |
| `starlab.sc2.px2.self_play.current_candidate_reanchor_record` | Slice-12 re-anchor JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_current_candidate_reanchor` | Slice-12 re-anchor CLI |
| `starlab.sc2.px2.self_play.second_hop_continuation` | Slice-13 second-hop continuation orchestration |
| `starlab.sc2.px2.self_play.second_hop_continuation_record` | Slice-13 second-hop continuation JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_second_hop_continuation` | Slice-13 second-hop continuation CLI |
| `starlab.sc2.px2.self_play.pointer_seeded_run` | Slice-14 pointer-seeded bounded run orchestration |
| `starlab.sc2.px2.self_play.pointer_seeded_run_record` | Slice-14 pointer-seeded run JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_pointer_seeded_run` | Slice-14 pointer-seeded run CLI |
| `starlab.sc2.px2.self_play.pointer_seeded_handoff` | Slice-15 post–pointer-seeded handoff orchestration |
| `starlab.sc2.px2.self_play.pointer_seeded_handoff_record` | Slice-15 handoff JSON + seal |
| `starlab.sc2.px2.self_play.emit_px2_self_play_pointer_seeded_handoff` | Slice-15 handoff CLI |
