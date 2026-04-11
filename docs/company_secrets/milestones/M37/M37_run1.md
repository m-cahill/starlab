# M37 CI run 1 — Audit Closure VI (Coverage Margin Recovery and CI Evidence Hardening)

**Milestone:** M37  
**Purpose:** Authoritative GitHub Actions workflow runs for the M37 merge ([PR #48](https://github.com/m-cahill/starlab/pull/48)).

## Final PR head (merge gate)

* **SHA:** `a38d3a7dcbb870f3d425e112f464f228889ae1c5` (short `a38d3a7…`) — tip validated by authoritative PR-head CI below (includes cross-platform identity basename fix after first CI attempt).
* **Merged via:** [PR #48](https://github.com/m-cahill/starlab/pull/48) — merge commit on `main` below.

## Merge commit

* **SHA:** `d2474bd365290a9c77f854b13d36a5ea1d8777cd` (short `d2474bd…`)
* **Merged at (UTC):** `2026-04-11T01:15:16Z`
* **Merge method:** merge commit (GitHub **Create a merge commit**)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24271250678`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24271250678
* **Commit:** `a38d3a7dcbb870f3d425e112f464f228889ae1c5`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

### Superseded PR-head (same PR; **not** merge authority)

* **`24271229377`** — **failure** on first PR head `bb55dc428961e037cee8a639c9bc06a467d61977` — **`tests`** job: `test_normalize_identity_helpers_cover_battle_net_map_and_replay_basename` (Windows-style replay path; `Path.name` on POSIX did not split on `\`). Fixed in `a38d3a7…` — **not** merge authority.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #48 to `main`; **authoritative** merge-boundary run)
* **headSha:** `d2474bd365290a9c77f854b13d36a5ea1d8777cd`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24271267848`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24271267848
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

## Coverage (authoritative PR-head `tests` job)

* **TOTAL** (branch-aware, `pytest-cov`): **~80.34%** reported in CI log for run **`24271250678`** (supersedes pre-merge local **80.00%** snapshot; same gate **`fail_under` = 78.0**).
* **`[tool.coverage.report] fail_under`:** **78.0** (`pyproject.toml`).

## Pytest

* Full suite on authoritative PR-head CI — **680** tests passed (**7** `runpy` `RuntimeWarning`s — non-blocking, accepted for M37).

## Milestone tag

* Annotated tag **`v0.0.37-m37`** on merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd` (milestone boundary — **not** a later doc-only tip).

## Non-merge-boundary runs (post-closeout)

* **None recorded** at initial M37 closeout — doc-only follow-ups on `main` after this commit would each produce additional **non-merge-boundary** runs (same distinction as M36).

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24271250678` |
| Merge-boundary `main` run | `24271267848` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `a38d3a7…` / merge `d2474bd…` |

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `d2474bd…`. Superseded PR-head: **`24271229377`** (failure — **not** merge authority).
