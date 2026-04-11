# M37 Plan — Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening

**Milestone:** M37  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** **Complete** — merged to `main` (see closeout below).

---

## Intent

Restore **material** test-coverage margin and make CI **evidence** easier to trust: raise total line coverage to **≥80%** on the branch (branch-aware measurement remains on; **~85%** is a **stretch** across the **M37**–**M39** campaign — not a guaranteed claim), set **`fail_under`** to roughly **measured baseline minus ~2** percentage points (rounded sensibly; **never** lower the gate below the prior value as a cheat), surface **branch** coverage in **CI** logs and **`$GITHUB_STEP_SUMMARY`**, use **`if: always()`** on diagnostically important **artifact uploads**, add **`make check`** (lint + typecheck + test), update **governance tests** to the **42**-milestone arc, and refresh **M38**–**M41** milestone stubs per §7.

---

## Non-goals

- **M39** flagship proof-pack **product** implementation (deferred to **M39**).
- Broad Ruff rule expansion, large refactors, subprocess coverage hacks, or casual **`omit`** gaming.

---

## Closeout (authoritative)

| Field | Value |
| --- | --- |
| **PR** | [PR #48](https://github.com/m-cahill/starlab/pull/48) |
| **Final PR head SHA** | `a38d3a7dcbb870f3d425e112f464f228889ae1c5` |
| **Merge commit SHA** | `d2474bd365290a9c77f854b13d36a5ea1d8777cd` |
| **Merged at (UTC)** | `2026-04-11T01:15:16Z` |
| **Authoritative PR-head CI** | [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) — **success** |
| **Merge-boundary `main` CI** | [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) — **success** |
| **Superseded (not merge authority)** | [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — **failure** on first PR head |
| **Tag** | **`v0.0.37-m37`** on merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd` |
| **Measured coverage (CI TOTAL, branch-aware)** | **~80.34%** (authoritative PR-head `tests` job) |
| **`fail_under` (pyproject)** | **78.0** |
| **Run evidence** | [`M37_run1.md`](M37_run1.md) |
| **Summary / audit** | [`M37_summary.md`](M37_summary.md), [`M37_audit.md`](M37_audit.md) |
