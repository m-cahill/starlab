# Milestone Summary — M11: Build-Order & Economy Plane

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M11 — Build-Order & Economy Plane  
**Timeframe:** 2026-04-07 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Define and implement a **governed, deterministic build-order and economy plane** over **`replay_timeline.json`** (M10), with optional **supplemental** entity identity from **`replay_raw_parse.json` v2 `raw_event_streams`** only — **without** claiming combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, or broad upstream parser certification.

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_build_order_economy_extraction.md`
- Artifacts: `replay_build_order_economy.json`, `replay_build_order_economy_report.json`
- Modules: `build_order_economy_models.py`, `build_order_economy_catalog.py`, `build_order_economy_extraction.py`, `build_order_economy_io.py`, `extract_replay_build_order_economy.py`
- Conservative catalog; timeline ordering authority; unknown/unclassified reporting
- Fixture-driven CI under `tests/fixtures/m11/`
- Merge discipline: **green final PR-head CI** on tip [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) before merge ([PR #12](https://github.com/m-cahill/starlab/pull/12))

### Out of Scope

- Combat, scouting, visibility windows (M12)
- Exact resource stockpile reconstruction
- `s2protocol` / raw replay bytes / parser invocation inside M11 modules
- Live SC2 in CI; benchmark integrity

---

## 3. Work Executed

- Implemented extraction → report → CLI; optional lineage hashes; optional SHA check for supplemental raw parse vs timeline `source_raw_parse_sha256`
- Added governance tests and fixtures; narrow `docs/starlab.md` alignment (full ledger closeout in same commit batch as this summary)

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) — **success** on `88ce7f9615c6c462b76674e1afb0734fc3dcc5be`
- **Merge-boundary `main` CI:** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) — **success** on merge commit `38c15302badd49966b17f9195ddb139f6ae9a9b4`
- **PR:** [#12](https://github.com/m-cahill/starlab/pull/12); merged `2026-04-07T21:49:23Z`; remote branch **deleted**

---

## 5. What M11 Proves (narrow)

- **Deterministic** build-order steps and **cumulative economy checkpoints** from governed timeline (+ optional identity lookup)
- **Fixture-driven** CI for Ruff, Mypy, Pytest, and governance jobs on PR head and on merge-push `main`

---

## 6. What M11 Does Not Prove

- Combat/scouting semantics, exact macro accounting, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of third-party replay rights

---

## 7. Standing non-claim

Supplemental **`raw_event_streams`** are used **only** for non-PII entity names; **timeline ordering and semantics remain authoritative.**
