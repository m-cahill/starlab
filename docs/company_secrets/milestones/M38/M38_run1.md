# M38 CI run 1 — Audit Closure VII (Public Face Refresh, Governance Rationalization, and Code-Health Tightening)

**Milestone:** M38  
**Purpose:** Authoritative GitHub Actions workflow runs for the M38 merge ([PR #49](https://github.com/m-cahill/starlab/pull/49)).

## Final PR head (merge gate)

* **SHA:** `3e00641922fc11f7f906d9d163312993a83816c1` (short `3e00641…`) — tip validated by authoritative PR-head CI below.
* **Merged via:** [PR #49](https://github.com/m-cahill/starlab/pull/49) — merge commit on `main` below.

## Merge commit

* **SHA:** `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` (short `bf6bf4a…`)
* **Merged at (UTC):** `2026-04-11T21:21:43Z`
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Branch deleted after merge:** `m38-public-face-governance-code-health` (per merge options)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24272425346`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24272425346
* **Commit:** `3e00641922fc11f7f906d9d163312993a83816c1`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

### Superseded PR-head (same PR; **not** merge authority)

* **None** for final head `3e00641…`.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #49 to `main`; **authoritative** merge-boundary run)
* **headSha:** `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24291882960`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24291882960
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

## Coverage / gates

* **`[tool.coverage.report] fail_under`:** **78.0** (`pyproject.toml`) — unchanged by M38 (M37 gate).
* M38 did not change coverage thresholds; full suite green on both PR-head and merge-boundary runs.

## Pytest

* Full suite on authoritative PR-head CI — **682** tests passed (per CI; includes new governance + `runpy_helpers` tests).

## Milestone tag

* Annotated tag **`v0.0.38-m38`** on merge commit `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` (milestone boundary — record in ledger when tag is pushed).

## Non-merge-boundary runs

* None recorded for this closeout beyond the merge-boundary push run above. Any later doc-only pushes on `main` are **non-merge-boundary** unless explicitly chartered as product merges.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24272425346` |
| Merge-boundary `main` run | `24291882960` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `3e00641…` / merge `bf6bf4a…` |

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `bf6bf4a…`. **Superseded PR-head:** none for M38.
