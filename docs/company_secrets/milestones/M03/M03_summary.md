# Milestone Summary — M03: Run Identity & Lineage Seed (closed on `main`)

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M03 — Run Identity & Lineage Seed  
**Timeframe:** 2026-04-06 → **2026-04-07**  
**Status:** **Complete on `main`** — merged [PR #4](https://github.com/m-cahill/starlab/pull/4) **2026-04-07**; merge commit `6bfe6a7b32a004f62a491bf31573e12cd211118a`; final PR head `884055c34b78f182c704df5a10a9eced5515fa78` — authoritative PR-head CI [`24059095399`](https://github.com/m-cahill/starlab/actions/runs/24059095399) (**success**); post-merge `main` CI [`24059246337`](https://github.com/m-cahill/starlab/actions/runs/24059246337) (**success**) on merge commit. See `M03_run1.md`.

---

## 1. Milestone Objective

Establish deterministic STARLAB **run spec identity**, **execution identity**, and **lineage seed** records built on the M02 execution proof surface, with stable JSON artifacts and a small CLI, **without** claiming replay binding (M04), canonical run artifact v0 (M05), benchmark validity, or cross-host reproducibility.

---

## 2. Scope Definition

### In Scope

- Runtime contract: `docs/runtime/run_identity_lineage_seed.md`
- Package: `starlab/runs/` (identity hashing, lineage assembly, writers, `seed_from_proof` CLI)
- Tests: `tests/test_run_identity.py`, `tests/test_lineage_seed.py`, `tests/test_runs_cli.py`; governance extensions
- Fixtures: `tests/fixtures/m02_match_config.json`, `m02_match_execution_proof.json`

### Out of Scope

- Replay parsing / binding (M04)
- Canonical run artifact v0 (M05)
- Benchmarks / tournament infrastructure
- New SC2 execution proof in CI

---

## 3. Work Executed

- Implemented deterministic IDs (`run_spec_id`, `execution_id`, `lineage_seed_id`), path-stable config normalization, optional `EnvironmentFingerprint`, `ArtifactReference`, and writers for `run_identity.json` / `lineage_seed.json`.
- CLI: `python -m starlab.runs.seed_from_proof` (proof + config + output dir; optional env JSON).
- **`starlab.runs` package `__init__` does not import `seed_from_proof`** — avoids `runpy` warnings when using `-m starlab.runs.seed_from_proof`.
- Ledger/README and milestone artifacts updated; **`M04` stubs** seeded at M03 closeout (`M04_plan.md`, `M04_toolcalls.md`) — **no** M04 implementation.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local | `ruff check .`, `ruff format --check .`, `mypy starlab tests`, `pytest` — green before merge |
| Final PR-head CI | Run **`24059095399`** — **success** on **`884055c…`** — see `M03_run1.md` |
| Post-merge `main` (merge push) | Run **`24059246337`** — **success** on merge commit **`6bfe6a7…`** |
| Post-merge `main` (closeout push) | Run **`24059294330`** — **success** on **`43d99f6…`** |

---

## 5. Governance Outcomes (narrow claims only)

**Proved on `main` (M03):**

- Deterministic **run spec identity** and **execution identity** primitives from normalized match config + execution proof inputs.
- Deterministic **lineage seed** derivation and stable **`run_identity.json` / `lineage_seed.json`** emission from those inputs (fixtures in CI; optional local proof paths).

**Explicitly not proved (unchanged):**

- Replay capture / **binding** to run identity (M04).
- **Canonical run artifact** v0 packaging (M05).
- Benchmark semantics, cross-host reproducibility, new live SC2 execution proof in CI.

---

## 6. Exit Criteria

Met: merge to `main`, green post-merge `main` CI, ledger §10 / §18 / §23 / §20 / §11 updated, M04 stubs only.

---

## 7. Final Verdict

**M03 is closed on `main`** with CI evidence recorded in `M03_run1.md` and `docs/starlab.md` §18. **Next:** M04 planning only until authorized.

---

## 8. Canonical References

| Reference | Value |
|-----------|-------|
| PR | https://github.com/m-cahill/starlab/pull/4 |
| Final PR head | `884055c34b78f182c704df5a10a9eced5515fa78` |
| Authoritative PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24059095399 |
| Merge commit | `6bfe6a7b32a004f62a491bf31573e12cd211118a` |
| Post-merge `main` CI (merge) | https://github.com/m-cahill/starlab/actions/runs/24059246337 |
| Post-merge `main` CI (closeout) | https://github.com/m-cahill/starlab/actions/runs/24059294330 |
| Run analysis | `M03_run1.md` |
| Audit | `M03_audit.md` |
