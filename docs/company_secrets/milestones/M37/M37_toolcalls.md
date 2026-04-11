# M37 toolcalls log

---

## Implementation (pre-merge)

Ledger recharter, coverage tests, CI/Makefile, `fail_under` discipline, governance alignment, PR #48 branch `m37-coverage-ci-hardening`.

---

## Merge / closeout (2026-04-11 UTC)

- Pushed branch; opened [PR #48](https://github.com/m-cahill/starlab/pull/48). First CI run **`24271229377`** failed (`tests`: POSIX basename vs Windows replay path) — fixed with `starlab.runs.identity._posix_path_name_for_identity`, commit `a38d3a7…`.
- Authoritative PR-head CI **`24271250678`** green; merged PR #48 (merge commit `d2474bd…`); merge-boundary **`main` CI** **`24271267848`** green.
- Tag **`v0.0.37-m37`** pushed on merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd`.
- Wrote **`M37_run1.md`**, **`M37_summary.md`**, **`M37_audit.md`**; updated **`docs/starlab.md`**, **`M37_plan.md`**, **`tests/test_governance_ci.py`** (current milestone **M38**).

---
