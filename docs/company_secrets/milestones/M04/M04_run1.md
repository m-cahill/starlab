# M04 CI Run Analysis — Run 1

**Workflow:** CI  
**Run ID:** `24060734950`  
**Event:** `pull_request`  
**Branch:** `m04-replay-binding-to-run-identity`  
**PR:** [#5](https://github.com/m-cahill/starlab/pull/5)  
**Head SHA:** `6991978cb35172edda75f721149b1558d7ead226`  
**Conclusion:** **success**  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24060734950

---

## Job: `governance`

**Status:** success  
**Started:** 2026-04-07T02:07:09Z  
**Completed:** 2026-04-07T02:07:41Z  
**Duration:** ~32s  
**Job URL:** https://github.com/m-cahill/starlab/actions/runs/24060734950/job/70176300524

### Steps

| Step | Conclusion |
|------|-----------|
| Set up job | success |
| Checkout | success |
| Set up Python 3.11 | success |
| Install package (dev) | success |
| Ruff check | success |
| Ruff format check | success |
| Mypy | success |
| Pytest | success |
| pip-audit | success |
| CycloneDX SBOM | success |
| Upload SBOM artifact | success |
| Gitleaks | success |
| Job summary | success |

---

## Summary

All required CI checks passed on the first PR-head push for M04:

- **Ruff lint:** clean
- **Ruff format:** clean
- **Mypy strict:** clean (34 source files)
- **Pytest:** 84 tests pass (includes 22 new M04 tests: 15 in `test_replay_binding.py`, 7 in `test_bind_replay_cli.py`)
- **pip-audit:** no known vulnerabilities
- **CycloneDX SBOM:** generated and uploaded
- **Gitleaks:** no secrets detected

No CI failures, no flaky tests, no weakened checks.

---

## Post-merge `main` — merge commit (authoritative)

**Merge commit:** `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed`  
**Merged at (UTC):** 2026-04-07T02:17:04Z  
**Merge method:** merge commit (not squash)

**Workflow:** CI  
**Run ID:** `24060997255`  
**Event:** `push`  
**Branch:** `main`  
**Head SHA:** `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` (merge commit)  
**Conclusion:** **success**  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24060997255

This is the authoritative **post-merge `main`** CI run on the **M04 merge commit** (merge-boundary). Later documentation-only pushes may produce additional green runs; those are **not** merge-boundary events unless explicitly noted in `docs/starlab.md` §23.
