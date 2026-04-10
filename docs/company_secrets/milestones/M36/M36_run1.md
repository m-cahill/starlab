# M36 CI run 1 — Audit Closure V (Governance Surface Rationalization and Documentation Density Control)

**Milestone:** M36  
**Purpose:** Authoritative GitHub Actions workflow runs for the M36 merge ([PR #47](https://github.com/m-cahill/starlab/pull/47)).

## Final PR head (merge gate)

* **SHA:** `63fe1168e8a4bb7961948526589aba3c0a01c9ba` (short `63fe116…`) — tip validated by authoritative PR-head CI below.
* **Merged via:** [PR #47](https://github.com/m-cahill/starlab/pull/47) — merge commit on `main` below.

## Merge commit

* **SHA:** `e73a53b28a4b6eeb3a2c19dd358d928c64806e89` (short `e73a53b…`)
* **Merged at (UTC):** `2026-04-10T22:23:02Z`
* **Merge method:** merge commit (GitHub **Create a merge commit**)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI** (unchanged)
* **Workflow run ID:** **`24266877684`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24266877684
* **Commit:** `63fe1168e8a4bb7961948526589aba3c0a01c9ba`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`** (aggregate; `needs` all five upstream jobs)

### Superseded PR-head (same PR; **not** merge authority)

* **None recorded** on the final PR head — the authoritative run is **`24266877684`**.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #47 to `main`; **authoritative** merge-boundary run)
* **headSha:** `e73a53b28a4b6eeb3a2c19dd358d928c64806e89`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24266906173`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24266906173
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

## Workflow inventory (authoritative PR-head + merge-boundary)

Workflow **`CI`** — parallel jobs:

| Job | Role |
| --- | ---- |
| `quality` | Ruff check, Ruff format check, Mypy |
| `smoke` | `pytest -m smoke` + upload **`pytest-smoke-junit.xml`** |
| `tests` | Full pytest + coverage + **`coverage.xml`** + **`pytest-junit.xml`** |
| `security` | pip-audit, CycloneDX SBOM, Gitleaks + SBOM artifact |
| `fieldtest` | `make fieldtest` → verify explorer JSON → upload **`fieldtest-output`** (`out/fieldtest/`) |
| `governance` | Aggregate (`needs` all upstream); **no** `continue-on-error` on required jobs |

## Pytest

* Full suite on merge-boundary `main` CI [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) — **616** tests passed (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged). After M36 doc-closeout commits on `main`, local `pytest -q` reports **617** passed (additional governance assertions).

## Milestone tag

* Annotated tag **`v0.0.36-m36`** on merge commit `e73a53b28a4b6eeb3a2c19dd358d928c64806e89` (milestone boundary — **not** a later doc-only tip).

## Non-merge-boundary runs (post-closeout)

* **Doc/governance closeout push** (`e4b306584a6cc0cb4a7f582c50f8fe3100094d8b`): **`CI`** run [`24267000568`](https://github.com/m-cahill/starlab/actions/runs/24267000568) — **success** — **not** merge-boundary authority for M36 implementation (authoritative product merge remains **`24266877684`** + **`24266906173`** on `e73a53b…`).

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24266877684` |
| Merge-boundary `main` run | `24266906173` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `63fe116…` / merge `e73a53b…` |

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `e73a53b…`. Superseded PR-head: **none** on final head.
