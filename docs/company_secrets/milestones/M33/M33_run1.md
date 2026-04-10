# M33 CI run 1 — Audit Closure II (CI Tiering, Architecture Surface, Field-Test Readiness)

**Milestone:** M33  
**Purpose:** Authoritative GitHub Actions workflow runs for the M33 merge ([PR #39](https://github.com/m-cahill/starlab/pull/39)).

## Final PR head (merge gate)

* **SHA:** `6640c69b64dfc8a905a24535bbf86a8fba10d7e9` (short `6640c69…`) — includes `M33_toolcalls.md` log entry for PR push.
* **Merged via:** [PR #39](https://github.com/m-cahill/starlab/pull/39) — merge commit on `main` below.

## Merge commit

* **SHA:** `975ac52fff206f9ceb1b0be66a0e7f1c7386a248` (short `975ac52…`)
* **Merged at (UTC):** `2026-04-10T18:02:21Z`
* **Message:** Merge pull request #39 from m-cahill/m33-audit-closure-ii-ci-tiering-field-test-readiness
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m33-audit-closure-ii-ci-tiering-field-test-readiness` **deleted** after merge (GitHub default)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow name:** **CI** (unchanged)
* **Workflow run ID:** **`24231313561`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24231313561
* **Jobs (all success):** `quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`** (aggregate; `needs` all five upstream jobs)

### Superseded PR-head (same PR; **not** merge authority for final tip)

* **Run ID:** `24231252478` — **success** on earlier tip `b758e6d37d1df0e3c31d9bd2429357130ed485f0` (M33 product commit only, before `M33_toolcalls.md` follow-up). **Superseded** by **`24231313561`** on **`6640c69…`**.

### Superseded red PR-head (not merge authority)

* **None recorded** for M33.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #39 to `main`; **authoritative** merge-boundary run)
* **headSha:** `975ac52fff206f9ceb1b0be66a0e7f1c7386a248`
* **Workflow name:** **CI**
* **Workflow run ID:** **`24256871132`**
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24256871132
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

* **591** tests passed with coverage gate `fail_under = 75.4` (see `pyproject.toml`) on merge-boundary `main` CI [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) — **success** (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow name | **CI** |
| Authoritative PR-head run | `24231313561` |
| Merge-boundary `main` run | `24256871132` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | PR head `6640c69…` / merge `975ac52…` |

### Change context

* **Milestone:** M33 — **Audit Closure II**: explicit parallel CI tiers, fixture-only field-test CI artifact, expanded architecture / operator / diligence docs, governance tests; **DIR-001**, **DIR-002**, **DIR-007** resolved in registry; **not** M34 structural hygiene, **not** M35 flagship proof pack, **not** live SC2 in CI.

### Baseline reference

* Trusted prior `main` at M32 closeout tip (`e9b9f5f…` / doc-only lines); product merge **M32** `cf72199…`.

### Step 1 — Workflow inventory

All jobs **required**; none use `continue-on-error` on merge-blocking tiers.

### Step 2 — Signal integrity

* **Tests:** Full suite in `tests` job; smoke in `smoke` job; coverage line gate + JUnit artifacts.
* **Field-test:** fixture-only M31 explorer; directory upload after explicit file checks.
* **Security:** pip-audit, SBOM, Gitleaks unchanged in intent.

### Step 3 — Delta

* `.github/workflows/ci.yml` + docs + tests — both authoritative PR-head and merge-boundary **success**.

### Step 4 — Failures

* None.

### Step 5 — Invariants

* Workflow name **`CI`** and final job **`governance`** preserved; checks not weakened.

### Step 6 — Verdict

> **Verdict:** PR-head **`24231313561`** and merge-boundary **`24256871132`** are **safe to treat as merge authority** for M33: both **success** on the documented SHAs.

**Merge approved:** ✅ (merge completed; merge-boundary **success**).

### Step 7 — Next actions

* Ledger closeout + tag `v0.0.33-m33` on merge commit **`975ac52…`**; **M34** stub only — **no** M34 product code.

---

## Non-merge-boundary runs (post-closeout)

* **Doc-only closeout push** (`e98f30c…` — ledger + M33/M34 docs + governance tests): workflow run [`24257044304`](https://github.com/m-cahill/starlab/actions/runs/24257044304) — **failure** (`quality` / Ruff E501 on long line in `tests/test_m33_audit_closure.py`). **Not** merge authority for M33 product (authoritative remains **`24231313561`** + **`24256871132`**).
* **Repair push** (`c5835a3…` — Ruff line wrap): workflow run [`24257093617`](https://github.com/m-cahill/starlab/actions/runs/24257093617) — **success**. **Not** merge-boundary authority for M33 **product**; documents honest post-closeout CI on `main` after ledger closeout.
