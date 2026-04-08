# M17 Plan — Observation Surface Contract

**Milestone:** M17 — Observation Surface Contract  
**Phase:** III — State, Representation, and Perception Bridge  
**Suggested branch:** `m17-observation-surface-contract`  
**Target tag:** `v0.0.17-m17`

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

## Status

**Implementation complete in-repo.** Record **PR / merge commit / authoritative PR-head CI / merge-boundary `main` CI** at merge boundary; update §18 and this plan with run evidence as needed.
