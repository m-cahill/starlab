# Milestone Summary — M03: Run Identity & Lineage Seed (pre-merge)

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M03 — Run Identity & Lineage Seed  
**Timeframe:** 2026-04-06 → **2026-04-07** (implementation + PR; **not** closed on `main` at this summary)  
**Status:** **Merge-ready on CI** — [PR #4](https://github.com/m-cahill/starlab/pull/4) **open**; authoritative PR-head CI run [`24058700007`](https://github.com/m-cahill/starlab/actions/runs/24058700007) — **success** on head `4dbd9ba7fd57aaf835592024ee0577352a918c9e`. **Merge to `main` and formal closeout are pending** user permission and follow-up ledger steps.

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
- Merge to `main` / post-merge `main` CI (tracked at closeout after merge)

---

## 3. Work Executed

- Implemented deterministic IDs (`run_spec_id`, `execution_id`, `lineage_seed_id`), path-stable config normalization, optional `EnvironmentFingerprint`, `ArtifactReference`, and writers for `run_identity.json` / `lineage_seed.json`.
- CLI: `python -m starlab.runs.seed_from_proof` (proof + config + output dir; optional env JSON).
- **`starlab.runs` package `__init__` does not import `seed_from_proof`** — avoids `runpy` warnings when using `-m starlab.runs.seed_from_proof`.
- Updated `docs/starlab.md`, `README.md`, and milestone plan/toolcalls; **M03_plan.md** contains the full approved plan.
- Opened **PR #4** from `m03-run-identity-lineage-seed`; pushed tip `4dbd9ba…`.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local | `ruff check .`, `ruff format --check .`, `mypy starlab tests`, `pytest` — exit 0 before push |
| PR-head CI | Run **`24058700007`** — **success** on **`4dbd9ba…`** — see `M03_run1.md` |
| Post-merge `main` | **Pending** — not applicable until merge |

---

## 5. Governance Outcomes

- M03 claims remain **narrow**: deterministic identity/lineage **seed** records from normalized proof + config; **not** replay-bound lineage, **not** canonical run artifact.
- **M04** milestone folder is **not** seeded in this step (optional at future closeout).

---

## 6. Exit Criteria (M03 closeout on `main`)

Full closeout requires merge to `main`, post-merge CI evidence, and ledger §7/§18/§23 updates — **deferred** until authorized.

---

## 7. Final Verdict (this step)

**M03 implementation is complete on the PR branch** and **PR-head CI is green** for the current tip. **Do not** treat M03 as **proved on `main`** until merge and closeout documentation.

---

## 8. Canonical References (this step)

| Reference | Value |
|-----------|--------|
| PR | https://github.com/m-cahill/starlab/pull/4 |
| PR head (at summary) | `4dbd9ba7fd57aaf835592024ee0577352a918c9e` |
| Authoritative PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24058700007 |
| Run analysis | `M03_run1.md` |
| Audit | `M03_audit.md` |
