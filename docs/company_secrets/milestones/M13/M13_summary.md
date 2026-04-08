# 📌 Milestone Summary — M13: Replay Slice Generator

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M13 — Replay Slice Generator  
**Timeframe:** 2026-04-07 → 2026-04-08  
**Status:** Closed  

---

## 1. Milestone Objective

Establish a **deterministic, governed replay slice-definition plane** that turns **governed** M10–M12 JSON artifacts into **metadata-only temporal span records** (`replay_slices.json`, `replay_slices_report.json`) with lineage checks and fixture-backed CI — **without** raw replay clipping, benchmark integrity claims, replay↔execution equivalence, fog-of-war truth, live SC2 in CI, or M14 bundle packaging.

> Without M13, STARLAB would lack a reproducible, hash-linked **slice definition** surface between the combat/scouting plane (M12) and future bundle/lineage work (M14).

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_slice_generation.md`
- Artifacts: `replay_slices.json`, `replay_slices_report.json`
- Modules: `replay_slice_models.py`, `replay_slice_catalog.py`, `replay_slice_generation.py`, `replay_slice_io.py`, `extract_replay_slices.py`
- Slice families v1: `combat_window`, `scouting_observation`; fixed padding 160; combat anchor = window **start**
- No `replay_raw_parse.json` read in M13 v1; no `s2protocol`; no parser CLI in M13 modules
- Fixtures under `tests/fixtures/m13/`; tests `test_replay_slices.py`, `test_replay_slices_cli.py`; governance updates
- PR [#14](https://github.com/m-cahill/starlab/pull/14); **green PR-head** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047); **green merge-push `main`** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177)

### Out of Scope

- Raw `.SC2Replay` clipping or rewriting
- Benchmark labels, simulation, full visibility/FOW reconstruction
- M14 replay bundle & lineage contract v1 (stub only after closeout)
- Live SC2 in CI

---

## 3. Work Executed

- Implemented pure generation over `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json` with canonical-hash lineage validation, overlap enrichment (M11 steps, M12 visibility windows as context only), deterministic `slice_id` from stable semantic fields (excludes overlaps / overlap-derived tags), CLI and golden fixtures.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) — **success** on `6231b19cd7067130fd3324dcd3070172333ba766`
- **Merge-boundary `main` CI:** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) — **success** on merge commit `f86e36837e81b8552639c5a885a13a773b96215c`
- **PR:** [#14](https://github.com/m-cahill/starlab/pull/14); merged `2026-04-08T01:20:38Z`; merge commit `f86e36837e81b8552639c5a885a13a773b96215c`; remote branch **deleted**

---

## 5. What M13 Proves (narrow)

- **Deterministic, lineage-linked** metadata slice definitions over governed M10–M12 JSON, with reporting and governance tests on `main`.

---

## 6. What M13 Does Not Prove

- Raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI, or **M14** replay bundle / lineage packaging.

---

## 7. Standing non-claim

**Timeline ordering** and upstream M12 semantics remain authoritative; visibility overlap in slices is **context only** and does not strengthen `observation_proxy` into certified vision truth.
