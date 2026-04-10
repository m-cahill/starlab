# M31 CI run 1 — Replay Explorer / Operator Evidence Surface

**Milestone:** M31  
**Purpose:** Authoritative GitHub Actions workflow runs for the M31 merge ([PR #37](https://github.com/m-cahill/starlab/pull/37)).

## Final PR head (merge gate)

* **SHA:** `4972a56c335342fbf2f1c5fa179bb1920561317c` (short `4972a56…`)
* **Merged at (UTC):** `2026-04-10T04:24:58Z`

## Merge commit

* **SHA:** `41d62056e1956627b63152221932dc9c2423429c` (short `41d6205…`)
* **Message:** Merge pull request #37 from m-cahill/m31-replay-explorer-operator-evidence-surface
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m31-replay-explorer-operator-evidence-surface` **deleted** after merge

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24225153475`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24225153475

## Superseded red PR-head (not merge authority)

* None recorded for M31.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #37 to `main`; **authoritative** merge-boundary run)
* **headSha:** `41d62056e1956627b63152221932dc9c2423429c`
* **Workflow run ID:** `24226308356`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24226308356

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on authoritative PR-head (`24225153475`) and merge-boundary `main` (`24226308356`).

## Pytest

* **558** tests passed on merge-boundary `main` CI [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged; not introduced by M31 `starlab/explorer/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow name | CI |
| Authoritative PR-head run | `24225153475` |
| Merge-boundary `main` run | `24226308356` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | `m31-replay-explorer-operator-evidence-surface` @ `4972a56…` / `main` @ `41d6205…` |

### Change context

* **Milestone:** M31 — deterministic offline **replay explorer evidence surface** (`replay_explorer_surface.json` + report), bounded panels over M13 slices, M16→M18 materialization, M30 predictor + M29 trace compatibility; **no** web UI, **no** live SC2, **no** benchmark integrity, **no** M32 product.

### Baseline reference

* Trusted prior `main` at M30 merge tip (`1c3a5f6…`).

### Step 1 — Workflow inventory

All listed steps **merge-blocking**; none use `continue-on-error`.

### Step 2 — Signal integrity

* **Tests:** Full `pytest` — correctness signal for new explorer + governance tests.
* **Static gates:** Ruff, Mypy — unchanged posture.
* **Security:** pip-audit, Gitleaks, SBOM — unchanged.

### Step 3 — Delta

* New `starlab/explorer/`, fixtures, ledger rows — CI green on both runs.

### Step 4 — Failures

* None.

### Step 5 — Invariants

* Required checks enforced; no weakening.

### Step 6 — Verdict

> **Verdict:** PR-head **`24225153475`** and merge-boundary **`24226308356`** are **safe to treat as merge authority** for M31: both **success** on the documented SHAs.

**Merge approved:** ✅ (CI evidence only; merge completed per ledger).

### Step 7 — Next actions

* Closeout docs + ledger + tag `v0.0.31-m31` on merge commit; **M32** stub only — **no** M32 product code.

---

## Non-merge-boundary runs (post-closeout)

* *To be recorded only if a documentation-only push to `main` follows this closeout commit — such runs are **not** merge authority for M31 product.*
