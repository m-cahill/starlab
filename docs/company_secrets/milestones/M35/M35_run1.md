# M35 CI run 1 — Audit Closure IV (Structural Decoupling and Module Decomposition)

**Milestone:** M35  
**Purpose:** Authoritative GitHub Actions workflow runs for the M35 merge ([PR #46](https://github.com/m-cahill/starlab/pull/46)).

## Final PR head (merge gate)

* **SHA:** `91e45ddfbb7a1f610ba25ac59a107c1b7e40af1a` (short `91e45dd…`) — tip after CI-fix commits (`d3a47f9` Ruff format, `91e45dd` Mypy `__all__`).
* **Merged via:** [PR #46](https://github.com/m-cahill/starlab/pull/46) — merge commit on `main` below.

## Merge commit

* **SHA:** `5b4d24b0eca578b70f2963f1561b99bc89fef033` (short `5b4d24b…`)
* **Merged at (UTC):** `2026-04-10T21:30:06Z`
* **Message:** Merge PR #46: M35 Audit Closure IV
* **Merge method:** merge commit (GitHub **Create a merge commit**)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI** (unchanged)
* **Workflow run ID:** **`24265022396`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24265022396
* **Commit:** `91e45ddfbb7a1f610ba25ac59a107c1b7e40af1a`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`** (aggregate; `needs` all five upstream jobs)

### Superseded PR-head (same PR; **not** merge authority)

* **Run ID:** `24264929015` — **failure** — Ruff format on `m14_bundle_loader.py` — repaired by commit `d3a47f9` — **not** merge authority.
* **Run ID:** `24264963434` — **failure** — Mypy: `load_json_object` not exported from `dataset_views` — repaired by commit `91e45dd` — **not** merge authority.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #46 to `main`; **authoritative** merge-boundary run)
* **headSha:** `5b4d24b0eca578b70f2963f1561b99bc89fef033`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24265056432`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24265056432
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

All listed steps **merge-blocking** on both runs; artifact uploads use `if-no-files-found: error` where configured.

## Pytest

* **613** tests passed with coverage gate `fail_under = 75.4` (see `pyproject.toml`) on merge-boundary `main` CI [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) — **success** (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged).

## Milestone tag

* Annotated tag **`v0.0.35-m35`** on merge commit `5b4d24b0eca578b70f2963f1561b99bc89fef033` (milestone boundary — **not** a later doc-only tip).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Non-merge-boundary runs (post-merge)

* **Doc closeout** on `main` after merge may trigger a separate **`CI`** run — **not** substitute merge authority for M35 product (authoritative remains **`24265022396`** + **`24265056432`**).

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24265022396` |
| Merge-boundary `main` run | `24265056432` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `91e45dd…` / merge `5b4d24b…` |

### Change context

* **Milestone:** M35 — **Audit Closure IV**: `M14BundleLoader`, `parser_io`, `replay_slice_generation`, observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39** + stubs; **not** M37 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI.

### Baseline reference

* Trusted prior `main` at M34 closeout merge `51e960d…`.

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `5b4d24b…`. Superseded PR-head runs **`24264929015`**, **`24264963434`** are **not** merge authority.
