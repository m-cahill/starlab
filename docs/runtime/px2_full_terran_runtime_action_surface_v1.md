# PX2 Full Terran Runtime & Action Surface v1

**Contract id:** `starlab.px2.terran_core.v1` (action schema: `starlab.px2.terran_action_schema.v1`; internal command: `starlab.px2.internal_command.v1`; compile receipt: `starlab.px2.compile_receipt.v1`)

**Milestone:** `PX2-M01 — Full Terran Runtime & Action Surface`

---

## 1. Purpose

This document defines the **public, versioned Terran full-game action/runtime surface** for **PX2**. It is the first substantive **runtime substrate** milestone after **`PX2-M00`** (governance-only charter). It exists so later milestones (**`PX2-M02`** replay bootstrap, **`PX2-M03`** industrial self-play) can attach learning and campaigns to a **governed** command surface instead of ad hoc demo patches.

**This milestone does not** prove agent strength, training success, Blackwell execution, or ladder performance.

---

## 2. Boundary from PX2-M00

- **`PX2-M00`** chartered **PX2**, Terran-first scope, scaffolding rules, and non-claims — **no** Terran runtime implementation.
- **`PX2-M01`** delivers the **Terran core v1** structured schema, legality/masking, placement/target vocabulary, compiler → internal commands, Burny bridge hints, and fixture-tested receipts — **not** policy intelligence baked into the runtime.

---

## 3. Relation to later milestones

| Milestone | Consumes this surface |
| --------- | ---------------------- |
| **PX2-M02** | Replay-bootstrap policy maps into structured Terran actions; compiler path for training/eval |
| **PX2-M03** | Industrial self-play uses the same surface for long campaigns |

**`PX2-M02` is not opened** by this document or by **`PX2-M01`** implementation landing on `main`.

---

## 4. Surface design principles

1. **Structured action families** — macro, production, scouting, combat, search — with **bounded arguments** (slots, regions, handles), not raw x/y clicks as the primary public interface.
2. **Legality / masks** — scaffolding may expose what is legal; it must **not** encode “attack this first” tactical policy.
3. **Additive versioning** — **`starlab.px2.terran_core.v1`** is a **new** surface; closed **PX1** / **M44** / demo adapters are **not** redefined.
4. **Intelligence-neutral** — no hand-authored tactical sequences substituting for learning.

---

## 5. Implementation map (code)

| Module | Role |
| ------ | ---- |
| `starlab/sc2/px2/terran_action_schema.py` | Terran core v1 action ids, families, validation |
| `starlab/sc2/px2/placement_targets.py` | Expansion/build slots, regions, cluster handles |
| `starlab/sc2/px2/terran_legality.py` | `GameStateSnapshot`, `legality_for`, `legal_mask` |
| `starlab/sc2/px2/action_compiler.py` | `compile_terran_action` → `Px2InternalCommand` |
| `starlab/sc2/px2/burny_bridge.py` | Semantic coarse-label hints (M44-style bridge, not raw BotAI) |
| `starlab/sc2/px2/runtime_receipts.py` | Deterministic compile receipts + SHA helper |

---

## 6. Compiler / executor posture

1. **Structured layer:** `TerranAction` (`action_id` + `arguments`) validated against Terran core v1.
2. **Internal command layer:** `Px2InternalCommand` — STARLAB-owned JSON-serializable record (`command_kind`, `payload`, optional `burny_bridge_hint`).
3. **Bridge:** `burny_bridge_hint` carries `semantic_coarse_label` aligned with `starlab/sc2/semantic_live_action_adapter.py` vocabulary for traceability; **PX2-M01** does **not** require live SC2 execution in CI.

---

## 7. One honest Terran full-game path (declared)

The following **logical path** is **represented** by the v1 action inventory (economy → supply/gas → core production → expansion → army → scout → attack/regroup/cleanup). Individual steps remain **policy-agnostic**; a later policy chooses the sequence.

1. **Opening economy:** `produce_scv`, `rebalance_workers`, `build_supply_depot`, `build_refinery`, `set_rally_point`, `idle_worker_recall`
2. **Core structures:** `build_barracks`, `build_factory`, `build_starport`, optional `build_engineering_bay`, `add_tech_lab` / `add_reactor`, `morph_orbital_command`
3. **Army:** `train_marine`, `train_marauder`, `train_siege_tank`, `train_medivac`, `train_viking`
4. **Expansion:** `expand_command_center` with `expansion_slot`
5. **Scouting:** `dispatch_worker_scout`, `dispatch_unit_scout`, `scout_to_region`, `recheck_last_seen_region`
6. **Combat / cleanup:** `army_move_region`, `army_attack_move_region`, `army_regroup_region`, `army_retreat_region`, `cleanup_search_region`
7. **Abilities (hooks):** `tank_siege`, `tank_unsiege`, `stim_units_hook`, `orbital_scan_hook`

---

## 8. PX2 Terran core v1 — action families (included vs deferred)

| Action family | Included in M01 | Deferred beyond M01 | Rationale |
| ------------- | ----------------- | --------------------- | --------- |
| Economy / workers | Yes (`produce_scv`, rebalance, rally, idle recall) | Fine-grained per-SCV pathing | Keep surface learnable; defer micro |
| Supply / gas / core structures | Yes (depot, refinery, rax/factory/starport, EB, addons, OC morph) | Full upgrade catalog | M01 = path honesty, not catalog completeness |
| Unit production | Yes (SCV, Marine, Marauder, Siege Tank, Medivac, Viking) | Ghost, Raven, BC, spell-heavy units | Spell-heavy / late-tech deferred per charter |
| Scouting | Yes (worker/unit dispatch, region slots, recheck) | Deep multi-prong vision fusion | Observation fusion is later |
| Expansion | Yes (`expand_command_center` + slot) | Automatic map analysis | Slot vocabulary only in M01 |
| Combat / search | Yes (move, attack-move, regroup, retreat, cleanup search) | Fine per-unit micro | Explicit deferral; no micro theorem |
| Abilities | Yes (siege/unsiege, stim hook, scan hook) | Full spell micro | Hooks only |

---

## 9. Deferred items (explicit)

- **Ghost / Raven / Battlecruiser**-class spell-heavy control
- **Advanced spell micro** and **per-unit tactical micro** as a primary surface
- **Broad upgrade catalog** beyond what the declared path requires
- **Multi-race** surfaces (Protoss/Zerg) — out of scope for **PX2-M01**
- **Replay learning, self-play campaigns, Blackwell runs** — later milestones only

---

## 10. Explicit non-claims

- **No** proof of autonomous strength or ladder rank
- **No** training pipeline or neural architecture milestone
- **No** Blackwell or long industrial execution as part of **PX2-M01**
- **No** demo refresh or proof pack
- **No** silent change to closed **PX1** / **v1** milestone semantics

---

## 11. References

- `docs/runtime/px2_autonomous_full_game_agent_charter_v1.md` — PX2 phase charter (**PX2-M00**)
- `docs/starlab.md` — authoritative ledger
