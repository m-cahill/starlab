# M39 CI run 1 — Public Flagship Proof Pack

**Milestone:** M39  
**Purpose:** Authoritative GitHub Actions workflow runs for the M39 merge ([PR #50](https://github.com/m-cahill/starlab/pull/50)).

## Final PR head (merge gate)

* **SHA:** `2c3fce7d3820bbfdfb655deedd3c0bb980ddc45b` (short `2c3fce7…`) — tip validated by authoritative PR-head CI below.
* **Merged via:** [PR #50](https://github.com/m-cahill/starlab/pull/50) — merge commit on `main` below.

## Merge commit

* **SHA:** `ca97027cf1827942a25c886f04b5db56b8b9fe7b` (short `ca97027…`)
* **Merged at (UTC):** `2026-04-11T22:36:41Z`
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Branch deleted after merge:** `m39-public-flagship-proof-pack` (per merge options)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24292861437`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24292861437
* **Commit:** `2c3fce7d3820bbfdfb655deedd3c0bb980ddc45b`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship`, `governance`

### Superseded PR-head (same PR; **not** merge authority)

* **None** for final head `2c3fce7…`.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #50 to `main`; **authoritative** merge-boundary run)
* **headSha:** `ca97027cf1827942a25c886f04b5db56b8b9fe7b`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24293162871`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24293162871
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship`, `governance`

## Coverage / gates

* **`[tool.coverage.report] fail_under`:** **78.0** (`pyproject.toml`) — unchanged by M39 (M37 gate).
* M39 did not change coverage thresholds; full suite green on both PR-head and merge-boundary runs.

## Pytest

* Full suite on authoritative PR-head CI — **691** tests passed (per local parity with PR head; CI aligns).

## Milestone tag

* Annotated tag **`v0.0.39-m39`** on merge commit `ca97027cf1827942a25c886f04b5db56b8b9fe7b` (milestone boundary — record when tag is pushed).

## Non-merge-boundary runs

* **None** recorded for this closeout push (ledger updates may trigger follow-on `main` runs — **not** merge authority for M39 product merge unless explicitly listed in a later closeout).

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24292861437` |
| Merge-boundary `main` run | `24293162871` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `2c3fce7…` / merge `ca97027…` |

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `ca97027…`. **Superseded PR-head:** none for M39 final head.
