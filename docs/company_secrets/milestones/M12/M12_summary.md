# Milestone Summary — M12: Combat, Scouting, and Visibility Windows

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M12 — Combat, Scouting, and Visibility Windows  
**Timeframe:** 2026-04-07 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Define and implement a **governed, deterministic combat / scouting / visibility plane** over **`replay_timeline.json`** (M10) and **`replay_build_order_economy.json`** (M11), with optional **supplemental** identity / position / explicit visibility fields from **`replay_raw_parse.json` v2** only — **without** claiming replay slices (M13), true fog-of-war certification, replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_combat_scouting_visibility_extraction.md`
- Artifacts: `replay_combat_scouting_visibility.json`, `replay_combat_scouting_visibility_report.json`
- Modules: `combat_scouting_visibility_models.py`, `combat_scouting_visibility_catalog.py`, `combat_scouting_visibility_extraction.py`, `combat_scouting_visibility_io.py`, `extract_replay_combat_scouting_visibility.py`
- Fixed clustering: `COMBAT_WINDOW_GAP_LOOPS = 160`; timeline ordering authority; `observation_proxy` default; `explicit_visibility` only when upstream fields support it directly
- No `s2protocol`, parser CLIs, or raw replay bytes in M12 modules
- Fixture-driven CI under `tests/fixtures/m12/`
- Merge discipline: **green final PR-head CI** on tip [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) before merge ([PR #13](https://github.com/m-cahill/starlab/pull/13))

### Out of Scope

- Replay slice generation (M13)
- Certified fog-of-war truth
- `s2protocol` / raw replay bytes / parser invocation inside M12 modules
- Live SC2 in CI; benchmark integrity; replay↔execution equivalence

---

## 3. Work Executed

- Implemented extraction → report → CLI; conservative combat windows from death clusters; scouting first-seen observations; visibility intervals with explicit labeling
- Added governance tests and fixtures; ledger alignment in closeout pass

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) — **success** on `59adce3422a840692a4961278c995c5029da43bb`
- **Merge-boundary `main` CI:** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) — **success** on merge commit `78528958a616177b564e603c193fb0d7f8af734e`
- **PR:** [#13](https://github.com/m-cahill/starlab/pull/13); merged `2026-04-07T23:23:48Z`; remote branch **deleted**

---

## 5. What M12 Proves (narrow)

- **Deterministic** combat-window clustering (gap threshold), scouting first-seen signals, and visibility-related intervals with **`explicit_visibility`** vs **`observation_proxy`** labeling
- **Fixture-driven** CI for Ruff, Mypy, Pytest, and governance jobs on PR head and on merge-push `main`

---

## 6. What M12 Does Not Prove

- Replay slices, true fog-of-war certification, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of third-party replay rights

---

## 7. Standing non-claim

**Timeline ordering wins**; supplemental raw parse is **non-authoritative** for ordering. **Observation proxy** is **not** certified opponent vision or fog-of-war truth.
