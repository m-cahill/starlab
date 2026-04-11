# 📌 Milestone Summary — M37: Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M37 — Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening  
**Timeframe:** 2026-04-10 → 2026-04-11 (closeout)  
**Status:** Closed  

---

## 1. Milestone Objective

Restore **material** test-coverage margin and make CI **evidence** easier to trust after prior milestones left the gate at **75.4%** while measured coverage had drifted. Without this milestone, the repository would lack an honest, branch-aware coverage story, a disciplined `fail_under` buffer, and visible merge-authoritative CI references for the audit/flagship campaign.

---

## 2. Scope Definition

### In Scope

- Targeted tests across `starlab` core modules and CLIs; no `omit` gaming.
- `pyproject.toml`: `fail_under` **78.0** (disciplined vs measured baseline on full suite).
- CI: coverage TOTAL in logs + `$GITHUB_STEP_SUMMARY`; Makefile `check` (lint + mypy + test).
- Ledger: 42-milestone arc; M38–M41 stubs; governance tests.
- Cross-platform fix: `starlab.runs.identity` basename normalization for Windows-style paths on Linux CI.

### Out of Scope

- M39 flagship proof-pack product implementation.
- Subprocess coverage attribution hacks; broad Ruff rule expansion.
- Chasing `runpy` `RuntimeWarning` noise (accepted as non-blocking for M37).

---

## 3. Work Executed

- **PR #48** merged to `main` (merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd`); final PR head `a38d3a7dcbb870f3d425e112f464f228889ae1c5`.
- Large test addition file `tests/test_m37_coverage_targets.py` and updates across existing test modules.
- `.github/workflows/ci.yml` step for step summary; `Makefile` `check` target; `pyproject.toml` coverage gate.
- Documentation: `docs/starlab.md` recharter fragments; `M38`–`M41` milestone stub files; `M37_fullaudit.md` artifact present in repo where applicable.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) — success (680 tests; coverage TOTAL **~80.34%**).
- **Merge-boundary `main` CI:** [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) — success.
- **Superseded:** [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — failure on first PR head; fixed before merge — **not** merge authority.
- Tag **`v0.0.37-m37`** on merge commit.

---

## 5. CI / Automation Impact

- Coverage gate **raised** from **75.4** to **78.0** (stronger minimum; measured total ~80%).
- CI continues to upload `coverage.xml`, JUnit, fieldtest artifact; governance aggregate job unchanged.

---

## 6. Issues & Exceptions

- One **superseded** red PR-head (POSIX `Path` vs Windows replay path) — **resolved** before merge; product-impacting only in the sense of identity normalization correctness on Linux.

---

## 7. Deferred Work

- Optional silence/refactor for `runpy` warnings — deferred unless CI requires it.
- **~85%** stretch coverage — explicitly **not** claimed.

---

## 8. Governance Outcomes

- Merge-authoritative CI IDs recorded in `M37_run1.md` and ledger.
- Honest coverage margin and gate discipline restored.

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not | Evidence |
| --- | --- | --- |
| Coverage ≥80% (branch-aware, CI) | Met (~80.34% authoritative PR-head) | CI log |
| `fail_under` disciplined | Met (78.0) | `pyproject.toml` |
| CI evidence (summary + logs) | Met | `ci.yml`, runs |
| Governance / 42 milestones | Met | `tests/test_governance_ci.py` |
| `make check` | Met | `Makefile` |

---

## 10. Final Verdict

Milestone objectives **met**. Safe to proceed to **M38** (stub charter).

---

## 11. Authorized Next Step

**M38** — Audit Closure VII — may begin on a dedicated branch when chartered; **no** M38 product code was added during this M37 closeout doc pass on `main` after merge (closeout commits are documentation + governance test alignment only).

---

## 12. Canonical References

- [PR #48](https://github.com/m-cahill/starlab/pull/48)
- Merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd`
- [`M37_run1.md`](M37_run1.md)
- CI: `24271250678`, `24271267848`; superseded `24271229377`
