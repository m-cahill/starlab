# PX2 Neural Bootstrap from Replays v1

**Contract ids:** `starlab.px2.replay_bootstrap_dataset.v1` (dataset), `starlab.px2.replay_bootstrap_dataset_report.v1` (report)

**Milestone:** `PX2-M02 — Neural Bootstrap from Replays`

---

## 1. Purpose

`PX2-M01` delivered the **versioned Terran core v1** runtime: structured `TerranAction` targets, legality/masking, compiler path, and receipts — **without** learning. **`PX2-M02`** is the **first PX2 learning milestone**: a **governed replay-bootstrap** path that maps conservative replay-derived supervision into that same **M01** surface, trains a **first neural policy**, and evaluates it honestly on **held-out replay identities** with **legality-aware decode** and **compile** checks — **not** autonomous strength, **not** self-play, **not** Blackwell campaigns.

---

## 2. Boundary from PX2-M01

| Layer | Milestone | Role |
| ----- | --------- | ---- |
| Runtime / action substrate | **PX2-M01** | `starlab.px2.terran_core.v1`, compiler, receipts |
| Replay supervision + first policy | **PX2-M02** (this doc) | Labeler, dataset, neural bootstrap, offline eval |
| Industrial self-play | **PX2-M03** (planned) | Long campaign — **out of scope** here |

---

## 3. Upstream dependencies

| Surface | Role |
| ------- | ---- |
| M14 replay bundle manifest | Bundle identity, lineage hooks |
| M11 build-order / economy | Primary **conservative** label signal (structure/unit events) |
| M16 canonical state | Terran filter (`race_actual`), perspective player |
| M18 observation surface | **Semantic anchor** for model inputs (bounded flat adapter) |
| PX2-M01 | **Only** public action target — `TerranAction` + `compile_terran_action` |

---

## 4. Conservative replay labeling (mapping table)

High-precision rules only; ambiguous or unsupported rows are **skipped** with explicit reasons in the dataset report.

| Replay signal source | Mapped PX2 action family | Conservative mapping rule | Skip condition |
| -------------------- | ------------------------ | ------------------------- | -------------- |
| BOE: structure `Barracks` + `started` | `production_structure` | `build_barracks` + `build_slot` default `0` | Non-Terran perspective player |
| BOE: structure `Factory` + `started` | `production_structure` | `build_factory` + `build_slot` `0` | Missing Terran CC prerequisite in labeler view (skip) |
| BOE: structure `Starport` + `started` | `production_structure` | `build_starport` + `build_slot` `0` | Same |
| BOE: structure `SupplyDepot` + `started` | `supply_structure` | `build_supply_depot` + `build_slot` `0` | Same |
| BOE: structure `EngineeringBay` + `started` | `production_structure` | `build_engineering_bay` + `build_slot` `0` | Same |
| BOE: structure `Refinery` + `started` | `gas` | `build_refinery` + `expansion_slot` `0` | Same |
| BOE: unit `Marine` + `completed` | `unit_production` | `train_marine` + `producer_key` `barracks_0` | Same |
| BOE: unit `Marauder` / `SiegeTank` / `Medivac` / `Viking` + `completed` | `unit_production` | Matching `train_*` + default producer key | Same |
| BOE: unit `SCV` / `Reaper` / non-M01 catalog | — | — | **Skip** (`unsupported_or_ambiguous_unit`) |
| Combat / micro timelines | — | — | **Out of scope** for M02 (no tactical relabeling) |

---

## 5. Dataset contract

- **Terran-only:** examples are dropped if canonical perspective has no `race_actual == Terran` player.
- **Split policy:** **deterministic replay-level** assignment:  
  `sha256("{split_salt}:{source_replay_identity}").hexdigest()[0] < "8"` → `train`, else `eval` (default salt `px2_m02_replay_split_v1`). **Replay-level** assignment avoids trivial leakage when a replay appears once.
- **Artifacts:** `px2_replay_bootstrap_dataset.json`, `px2_replay_bootstrap_dataset_report.json` — coverage by `action_id`, skip reasons, upstream bundle ids.
- **Local-first:** large tensors stay under `out/` by convention; CI uses **tiny** committed fixtures.

---

## 6. Model posture

- **Encoder:** MLP over **M18-flat** features (fixed dim, see `starlab.sc2.px2.bootstrap.feature_adapter`).
- **Heads:** `action_id` (full Terran core v1 inventory) + auxiliary slots (`build_slot`, `expansion_slot`, `region_slot`, `producer_key` index) with **masked** losses where applicable.
- **No** value network, **no** RL loop in M02.

---

## 7. Eval posture

- **Raw metrics:** argmax action accuracy vs label (train/eval splits).
- **Legality-aware decode:** scan down sorted `action_id` logits; **materialize** args from aux heads; accept first **`legality_for` + `TerranAction` valid** pair.
- **Compile:** `compile_terran_action` on decoded action — report **compile success rate**.
- **Baselines:** majority `action_id` and majority **action family** on the eval slice — model must **beat** trivial baselines on held-out identities.

---

## 8. Deferred (explicit)

- Self-play / RL campaigns (**PX2-M03**)
- Blackwell-scale execution
- Multi-race PX2 surfaces
- Demo refresh / proof pack (**PX2-M05**)
- Full value / RL stack

---

## 9. Non-claims

- **Not** proof of ladder or autonomous strength.
- **Not** industrial self-play or Blackwell evidence.
- **Not** replay↔execution equivalence or benchmark universality.
- **Not** opening **PX2-M03** or **v2** by this milestone narrative alone.

---

## 10. Code map

| Module | Role |
| ------ | ---- |
| `starlab/sc2/px2/bootstrap/replay_labeler.py` | BOE → `TerranAction` (conservative) |
| `starlab/sc2/px2/bootstrap/dataset_contract.py` | Dataset/report JSON helpers + split |
| `starlab/sc2/px2/bootstrap/feature_adapter.py` | M18 → flat tensor |
| `starlab/sc2/px2/bootstrap/policy_model.py` | `BootstrapTerranPolicy` |
| `starlab/sc2/px2/bootstrap/training_run.py` | Local / CI-smoke training |
| `starlab/sc2/px2/bootstrap/evaluate_bootstrap.py` | Baselines, decode, compile stats |
| `starlab/sc2/px2/bootstrap/emit_replay_bootstrap_dataset.py` | CLI: emit dataset artifacts |
