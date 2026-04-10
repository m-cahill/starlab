# M34 CI run 1 — Audit Closure III (Structural Hygiene, Deferred Issues, Manual Prep)

**Milestone:** M34  
**Purpose:** Authoritative GitHub Actions workflow runs for the M34 merge ([PR #40](https://github.com/m-cahill/starlab/pull/40)).

## Final PR head (merge gate)

* **SHA:** `a748bd7cc0be2b7e2acb423e098190429ae6fe2a` (short `a748bd7…`) — second commit on the PR (M35 stub files for governance tests).
* **Merged via:** [PR #40](https://github.com/m-cahill/starlab/pull/40) — merge commit on `main` below.

## Merge commit

* **SHA:** `51e960d0c1c0eb20923836a8ac2400a59013bcc5` (short `51e960d…`)
* **Merged at (UTC):** `2026-04-10T19:47:02Z`
* **Message:** Merge pull request #40 from m-cahill/m34-audit-closure-iii-structural-hygiene-manual-prep
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m34-audit-closure-iii-structural-hygiene-manual-prep` — confirm on GitHub whether deleted (default: often deleted after merge)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI** (unchanged)
* **Workflow run ID:** **`24261065226`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24261065226
* **Commit:** `a748bd7cc0be2b7e2acb423e098190429ae6fe2a`
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`** (aggregate; `needs` all five upstream jobs)

### Superseded PR-head (same PR; **not** merge authority)

* **Run ID:** `24261032237` — **failure** on first tip `d1e92ae2a9b4e64326ebd68a5fe364f8f75a163f` — smoke + full tests failed: governance tests expected `docs/company_secrets/milestones/M35/M35_plan.md` and `M35_toolcalls.md` (missing from first commit). **Superseded** by **`24261065226`** on **`a748bd7…`** after adding M35 stub files. **Closeout-only / hygiene**, not a product regression on `main`.

### Superseded red PR-head (not merge authority)

* Covered by **`24261032237`** above (failure — **not** merge authority).

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #40 to `main`; **authoritative** merge-boundary run)
* **headSha:** `51e960d0c1c0eb20923836a8ac2400a59013bcc5`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24261102337`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24261102337
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**

## Workflow inventory (authoritative PR-head + merge-boundary)

Workflow **`CI`** — parallel jobs:

| Job | Role |
| --- | ---- |
| `quality` | Ruff check, Ruff format check, Mypy |
| `smoke` | `pytest -m smoke` + upload **`pytest-smoke-junit.xml`** |
| `tests` | Full pytest + coverage + **`coverage.xml`** + **`pytest-junit.xml`** |
| `security` | pip-audit, CycloneDX SBOM, Gitleaks + SBOM artifact |
| `fieldtest` | `make fieldtest` → verify `replay_explorer_surface.json` + `replay_explorer_surface_report.json` → upload **`fieldtest-output`** (`out/fieldtest/`) |
| `governance` | Aggregate (`needs` all upstream); **no** `continue-on-error` on required jobs |

All listed steps **merge-blocking** on both runs; artifact uploads use `if-no-files-found: error` where configured.

## Pytest

* **609** tests passed with coverage gate `fail_under = 75.4` (see `pyproject.toml`) on merge-boundary `main` CI [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) — **success** (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged).

## Milestone tag

* Annotated tag **`v0.0.34-m34`** on merge commit `51e960d0c1c0eb20923836a8ac2400a59013bcc5` (milestone boundary — **not** a later doc-only tip).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Non-merge-boundary runs (post-merge)

* **Dependabot** may open separate workflow runs on `main` after `.github/dependabot.yml` lands; those are **not** substitute merge authority for M34 product (authoritative remains **`24261065226`** + **`24261102337`**).
* **Doc closeout** commit `6dcf8079cebd06d4a3714d6d85932a2415241c05` — push `main` CI [`24261183636`](https://github.com/m-cahill/starlab/actions/runs/24261183636) — **success** — ledger/closeout markdown only; **not** substitute merge authority for M34 product (authoritative remains **`24261065226`** + **`24261102337`**).

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24261065226` |
| Merge-boundary `main` run | `24261102337` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `a748bd7…` / merge `51e960d…` |

### Change context

* **Milestone:** M34 — **Audit Closure III**: `starlab._io`, governance test split, DIR-005 documentation/validation, Dependabot + dev caps, operating-manual **promotion prep** (not v1); **DIR-003**–**DIR-006** resolved in registry; **not** M35 flagship proof pack product, **not** benchmark integrity, **not** live SC2 in CI.

### Baseline reference

* Trusted prior `main` at M33 closeout merge `975ac52…`.

### Verdict

* **Merge-safe** at final PR head; **merge-boundary `main` CI** green on `51e960d…`. First PR-head failure **`24261032237`** is **superseded** and **not** merge authority.
