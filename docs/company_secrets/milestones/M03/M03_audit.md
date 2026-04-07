# Milestone Audit — M03: Run Identity & Lineage Seed (pre-merge)

**Audit mode:** DELTA AUDIT (pre-merge)  
**Milestone ID:** M03  
**Branch:** `m03-run-identity-lineage-seed`  
**PR:** [#4](https://github.com/m-cahill/starlab/pull/4) — **open** (at audit time)  
**PR head (audit time):** `3e78e71a872086a787fe59c16fe6caa3ef6dbd99`  
**Authoritative PR-head CI:** [CI run 24058752461](https://github.com/m-cahill/starlab/actions/runs/24058752461) — **success**  
**Date:** 2026-04-07

---

## Executive summary

M03 adds **STARLAB-owned run identity and lineage seed** primitives on top of the M02 proof surface: `starlab/runs/`, runtime contract doc, CLI, fixtures, and tests. **PR #4** is **open** with **green** CI on the current PR tip. **No merge to `main`** has been performed in this audit step. **No** replay binding, **no** canonical run artifact v0, **no** benchmark claims.

**Audit Verdict:** **Green (CI)** — merge gate checks pass on the authoritative PR-head run; **formal “proved on `main`”** status awaits merge + closeout ledger updates.

---

## 1. Regression / risk scan (delta)

| Area | Finding | Severity |
|------|---------|----------|
| Dependency hygiene | No new default runtime deps; `[dev]` unchanged in intent | OK |
| SC2 boundary | `starlab.runs` consumes `starlab.sc2` proof/config parsers only; no SC2 client imports in `runs` | OK |
| CI truthfulness | Same gates as prior milestones; PR-head run **success** | OK |
| Claim discipline | Ledger and docs describe **in development** / **not on `main` yet** for M03 proof row | OK |

---

## 2. Material improvements

- Deterministic three-ID model (run spec / execution / lineage seed) with explicit JSON artifacts.
- Fixture-driven, SC2-free CI coverage for M03.
- CLI path for operators without requiring SC2 execution.

---

## 3. CI / test / lint (record)

- **Lint/format/types:** Ruff + Mypy — pass on PR-head `24058752461`.
- **Tests:** Pytest — 61 passed; includes M03 tests and governance.
- **Supply chain:** pip-audit, SBOM, Gitleaks — pass on PR-head run.

---

## 4. What is not proven here

- **Merge to `main`** and **post-merge `main` CI** — not recorded in this audit.
- **Replay binding** — explicitly out of scope (M04).
- **Canonical run artifact v0** — explicitly out of scope (M05).
- **New SC2 execution proof** — not part of M03 CI.

---

## 5. Verdict

**AUDIT RESULT:** **PR-head CI acceptable** for merge **from a governance automation perspective**. **Human merge and closeout** remain **separate** gated steps. **Do not** update `docs/starlab.md` §10 to “proved on `main`” for M03 until after merge and agreed closeout.

---

## Machine-readable appendix

```json
{
  "milestone": "M03",
  "mode": "DELTA_AUDIT_PRE_MERGE",
  "pr": 4,
  "pr_head": "3e78e71a872086a787fe59c16fe6caa3ef6dbd99",
  "authoritative_pr_head_ci": "24058752461",
  "verdict": "green_pr_head_ci",
  "merged_to_main": false
}
```
