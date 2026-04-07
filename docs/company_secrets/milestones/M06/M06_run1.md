# CI / Workflow Analysis — M06 (authoritative PR-head + post-merge `main`)

**Milestone:** M06 — Environment Drift & Runtime Smoke Matrix  
**Project:** STARLAB  
**Mode:** Milestone merge gate + post-merge verification

---

## A. PR-head CI (authoritative merge gate)

| Field | Value |
| ----- | ----- |
| **Workflow name** | CI |
| **Run ID** | `24064200725` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24064200725 |
| **Trigger** | `pull_request` |
| **Branch** | `m06-environment-drift-runtime-smoke-matrix` |
| **Head SHA (tested)** | `6f9ef463f90abe914f3c98c8977d49f8da0102cb` |
| **Conclusion** | **success** |
| **PR** | [#7](https://github.com/m-cahill/starlab/pull/7) |

### Job inventory (`governance`)

| Step | Required | Pass/Fail |
| ---- | -------- | --------- |
| Ruff check | yes | pass |
| Ruff format check | yes | pass |
| Mypy | yes | pass |
| Pytest | yes | pass |
| pip-audit | yes | pass |
| CycloneDX SBOM | yes | pass |
| Gitleaks | yes | pass |

No `continue-on-error` observed on required steps.

### What this run proves

- **M06 surface** (smoke matrix builder, drift evaluator, CLI, fixtures, governance tests) passes the **same** governance gates as prior milestones: lint, format, typing, tests, supply-chain scans.
- **Fixture-driven, SC2-free** validation of deterministic `runtime_smoke_matrix.json` and `environment_drift_report.json` emission paths.

### What this run does **not** prove

- **Cross-host reproducibility**, **cross-install portability**, **replay parser** correctness, **replay semantic** extraction, **replay provenance** finalization, **benchmark** integrity, or **live SC2** execution in CI — **explicit M06 non-claims** (see `docs/runtime/environment_drift_smoke_matrix.md`).

### Verdict (PR-head)

**Merge approved** — required checks green at final PR tip `6f9ef46…`.

---

## B. Post-merge `main` CI (merge-commit boundary)

| Field | Value |
| ----- | ----- |
| **Workflow name** | CI |
| **Run ID** | `24064229874` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24064229874 |
| **Trigger** | `push` to `main` |
| **Merge commit** | `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` |
| **Conclusion** | **success** |

**Distinction:** PR-head CI validates the **PR branch tip** before merge. Post-merge CI validates the **merge commit** on `main`.

---

## C. Failed runs (superseded)

Earlier PR-head run on branch tip **`714994a…`**: workflow run **`24064181198`** failed at **Ruff format check** (`starlab/sc2/environment_drift.py` needed `ruff format`). Resolved on tip **`6f9ef46…`** — **not** used as merge authority.

---

## D. PR / merge record

| Field | Value |
| ----- | ----- |
| **Merged at (GitHub)** | `2026-04-07T04:26:10Z` |
| **Merge method** | **Create a merge commit** |
| **Final PR head** | `6f9ef463f90abe914f3c98c8977d49f8da0102cb` |
| **Merge commit** | `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` |
| **Remote branch after merge** | **deleted** (`m06-environment-drift-runtime-smoke-matrix`) |
