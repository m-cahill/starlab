# Milestone Summary — M17: Observation Surface Contract

**Project:** STARLAB  
**Phase:** III — State, Representation, and Perception Bridge  
**Milestone:** M17 — Observation Surface Contract  
**Timeframe:** 2026-04-08 → 2026-04-08  
**Status:** Closed  

---

## 1. Milestone Objective

Prove a **narrow, governed agent-facing observation contract** for **exactly one** player-relative observation frame at **one** `gameloop`, with **deterministic** `observation_surface_schema.json` and `observation_surface_schema_report.json`, `jsonschema` validation over fixtures, and a small emit CLI — with **M16 `canonical_state.json` as the sole semantic upstream** for observation design — **without** canonical-state→observation materialization, perceptual bridge (M18), replay parsing, bundle loading in observation modules, benchmark integrity, or live SC2 in CI.

Without M17, STARLAB would lack a **governed observation surface** distinct from M15 schema-only state and M16 bundle→frame materialization.

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/observation_surface_contract_v1.md`
- Product modules: `starlab/observation/` (`observation_surface_models.py`, `observation_surface_catalog.py`, `observation_surface_schema.py`, `observation_surface_io.py`, `emit_observation_surface_schema.py`)
- Artifacts: `observation_surface_schema.json`, `observation_surface_schema_report.json` (deterministic emission)
- CLI: `python -m starlab.observation.emit_observation_surface_schema`
- Fixtures and goldens under `tests/fixtures/m17/`
- Tests: `tests/test_observation_surface_schema.py`, `tests/test_emit_observation_surface_schema_cli.py`, governance updates
- PR [#18](https://github.com/m-cahill/starlab/pull/18); **authoritative green PR-head** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530); **merge-boundary `main`** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167)

### Out of Scope

- Canonical-state → observation **projection** / materialization (M18+)
- Perceptual bridge, pixels, image-space transforms
- Raw `.SC2Replay`, `replay_raw_parse.json`, `s2protocol`, M14 bundle loading in M17 modules
- Full SC2 action coverage, mask legality computation, dynamic mask generation
- Replay↔execution equivalence, benchmark integrity, live SC2 in CI

---

## 3. Work Executed

- Defined observation frame JSON Schema (metadata, viewpoint, ordered scalars, entity rows, spatial plane family, action-mask families) with Draft 2020-12 validation.
- Implemented deterministic schema/report emission and CLI; added valid/invalid fixtures and goldens; example observation JSON is source-informed by M16 golden fixture, authored as a contract example (not a normative projection algorithm).
- Updated `docs/starlab.md`, governance tests, and seeded **M18** milestone stubs (plan + toolcalls only).

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) — **success** on `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6`
- **Merge-boundary `main` CI:** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) — **success** on merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`
- **PR:** [#18](https://github.com/m-cahill/starlab/pull/18); merged **2026-04-08T23:30:53Z**; merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`; merge method **merge commit**; remote branch `m17-observation-surface-contract` **deleted**

---

## 5. CI / Automation Impact

- No workflow file changes; governance job remained merge-blocking.

---

## 6. Issues & Exceptions

- None on authoritative PR-head or merge-boundary `main` runs.

---

## 7. Deferred Work

- **M18 — Perceptual bridge prototype** — stub only; no M18 product code in M17.

---

## 8. Governance Outcomes

- Phase III now has a **contract-level observation surface** with explicit non-claims; boundaries preserved: **M15** schema-only, **M16** bundle→frame, **M17** observation contract, **M18** bridge/materialization.

---

## 9. Exit Criteria Evaluation

| Criterion (from M17 plan) | Met |
| --------------------------- | --- |
| Deterministic schema + report | Met |
| One player-relative frame at one gameloop | Met |
| jsonschema validation (fixtures) | Met |
| No materialization / replay / bundle load in M17 modules | Met |
| M16 canonical state as upstream (contract doc) | Met |
| Tests + CI green | Met |

---

## 10. Final Verdict

Milestone objectives met. **M17 closed.** Current milestone → **M18** (stub).

---

## 11. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/18  
- Merge commit: `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24164045530  
- Merge `main` CI: https://github.com/m-cahill/starlab/actions/runs/24164075167  
- Contract: `docs/runtime/observation_surface_contract_v1.md`  
- Ledger: `docs/starlab.md`
