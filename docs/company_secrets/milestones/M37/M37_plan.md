# M37 Plan — Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening

**Milestone:** M37  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** In progress — see `docs/starlab.md` §7 / §11.

---

## Intent

Restore **material** test-coverage margin and make CI **evidence** easier to trust: raise total line coverage to **≥80%** on the branch (branch-aware measurement remains on; **~85%** is a **stretch** across the **M37**–**M39** campaign — not a guaranteed claim), set **`fail_under`** to roughly **measured baseline minus ~2** percentage points (rounded sensibly; **never** lower the gate below the prior value as a cheat), surface **branch** coverage in **CI** logs and **`$GITHUB_STEP_SUMMARY`**, use **`if: always()`** on diagnostically important **artifact uploads**, add **`make check`** (lint + typecheck + test), update **governance tests** to the **42**-milestone arc, and refresh **M38**–**M41** milestone stubs per §7.

---

## Non-goals

- **M39** flagship proof-pack **product** implementation (deferred to **M39**).
- Broad Ruff rule expansion, large refactors, subprocess coverage hacks, or casual **`omit`** gaming.

---

## Closeout

Updates to `docs/starlab.md` §23, CI run IDs, and optional `M37_run1.md` / tag **`v0.0.37-m37`** follow the M35/M36 pattern when this milestone merges to `main`.
