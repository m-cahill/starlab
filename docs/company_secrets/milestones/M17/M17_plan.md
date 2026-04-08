# M17 Plan — Observation Surface Contract

**Milestone:** M17 — Observation Surface Contract  
**Phase:** III — State, Representation, and Perception Bridge  
**Branch:** `m17-observation-surface-contract` (merged; remote deleted)  
**PR:** [#18](https://github.com/m-cahill/starlab/pull/18)  
**Target tag:** `v0.0.17-m17`  
**Status:** **Closed** (2026-04-08)

## Objective

Freeze the **observation surface semantics and schema** for **one** player-relative observation frame at **one** `gameloop`, bound to **M16 canonical state** as the sole semantic upstream, with deterministic schema + report emission, fixture-backed validation, and a small emit CLI — **without** bridge implementation, tensor materialization, or benchmark claims.

## Primary deliverables

1. **Runtime contract doc:** `docs/runtime/observation_surface_contract_v1.md`
2. **Product modules:** `starlab/observation/` — `observation_surface_models.py`, `observation_surface_catalog.py`, `observation_surface_schema.py`, `observation_surface_io.py`, `emit_observation_surface_schema.py`
3. **Governed artifacts:** `observation_surface_schema.json`, `observation_surface_schema_report.json` (one observation frame; deterministic emission)
4. **CLI:** `python -m starlab.observation.emit_observation_surface_schema --output-dir ... --example-fixture ...`
5. **Fixtures and tests:** valid/invalid observation fixtures, schema goldens, unit + CLI + governance coverage

## Locked design decisions (2026-04-08)

- **Entity rows:** hybrid — schema supports future per-entity fields; valid example uses **aggregated category** rows from M16 summaries only.
- **Spatial planes:** structural shape metadata only (`grid_height`, `grid_width`, `channel_count`, `channel_order`, optional `coordinate_frame`); **not** bound to M09 map dimensions.
- **Example fixture:** source-informed by `tests/fixtures/m16/expected_canonical_state.json`, **authored** as a contract example (not normative projection algorithm).
- **Action-mask families:** concrete initial set — `no_op`, `selection`, `camera_or_view`, `production`, `build`, `unit_command`, `research_or_upgrade` — family-level contract only.

## Merge evidence

- **Merge commit:** `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` — **2026-04-08T23:30:53Z** (UTC), merge method **merge commit**
- **Authoritative PR-head CI:** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) — **success** (final tip `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6`)
- **Merge-boundary `main` CI:** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) — **success**

## Closeout artifacts

- `M17_run1.md`, `M17_summary.md`, `M17_audit.md`, `M17_toolcalls.md` (finalized), ledger `docs/starlab.md`
