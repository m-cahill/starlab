# Milestone Audit — M17

**Milestone:** M17 — Observation Surface Contract  
**Mode:** DELTA AUDIT (default)  
**Range:** `dd9546f88ebcf9b454498eec83a14d742d17d070` (M16 merge on `main`) … `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` (M17 merge on `main`)  
**CI Status:** Green (authoritative PR-head + merge-boundary `main`)  
**Audit Verdict:** **Green** — narrow contract milestone; M16 upstream boundary respected; no materialization or replay coupling in observation modules.

---

## Executive Summary

**Improvements**

- **Governed observation surface contract:** deterministic `observation_surface_schema.json` + `observation_surface_schema_report.json`, `jsonschema` validation, contract doc `docs/runtime/observation_surface_contract_v1.md`.
- **Isolation:** `starlab/observation/` contains **no** canonical-state→observation materialization, **no** replay parse, **no** bundle load, **no** `s2protocol`.

**Risks**

- None material for M17 closeout; downstream consumers must not treat M17 as proving mask legality or full action-space coverage.

**Single most important next action**

- Keep **M18** scoped to **perceptual bridge / materialization** experiments without collapsing **M15 / M16 / M17** boundaries in docs or code.

---

## Delta Map & Blast Radius

| Area        | Change |
| ----------- | ------ |
| Contracts   | `docs/runtime/observation_surface_contract_v1.md` |
| Code        | `starlab/observation/*.py` |
| Tests       | `tests/test_observation_surface_schema.py`, `tests/test_emit_observation_surface_schema_cli.py`, `tests/fixtures/m17/`, `tests/test_governance.py` |
| Dependencies | None new (uses existing `jsonschema`) |

**Risk zones touched:** Observation contract (primary); no changes to `starlab/state/` pipeline semantics.

---

## Architecture & Modularity

### Keep

- Observation package separate from `starlab/state/` materialization; schema builders remain free of M16 runtime projection.

### Fix Now (≤ 90 min)

- None required for M17 closeout.

### Defer

- Canonical-state→observation materialization — **M18+**.

---

## CI/CD & Workflow Integrity

- Required checks enforced on `pull_request` and `push`.
- **Authoritative PR-head:** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) — success (final tip `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6`).
- **Merge-boundary `main`:** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) — success.
- **Superseded:** none for M17.

---

## Tests & Coverage (Delta-Only)

- Observation schema/report determinism, fixture validation, CLI paths, governance file presence; **310** tests at closeout.

---

## Security & Supply Chain

- No new runtime dependencies; pip-audit green on authoritative runs.

---

## Top Issues

| ID     | Category | Severity | Notes |
| ------ | -------- | -------- | ----- |
| —      | —        | —        | No blocking issues for M17 closeout. |

---

## Deferred Issues Registry (append)

| ID       | Issue                         | Discovered (M#) | Deferred To | Reason           | Blocker? | Exit Criteria      |
| -------- | ----------------------------- | --------------- | ----------- | ---------------- | -------- | ------------------ |
| D-M17-001 | Perceptual bridge prototype | M17             | M18         | Out of M17 scope | No       | M18 defines bridge |

---

## Score Trend (suggested)

| Dimension   | Delta |
| ----------- | ----- |
| Architecture | + (clear Phase III contract boundary) |
| Governance   | + (contract + non-claims) |
| Evidence     | + (PR-head + merge-boundary green) |
| CI           | + (no superseded red PR-head for M17) |

---

## Audit Sign-Off

M17 **DELTA AUDIT** — **PASS** for closeout. Materialization, perceptual bridge, and benchmark claims remain **not proved** per ledger.
