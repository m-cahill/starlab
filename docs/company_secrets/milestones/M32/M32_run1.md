# M32 CI run 1 — Audit Closure I (Coverage, Clone-to-Run, Manual Scaffold)

**Milestone:** M32  
**Purpose:** Authoritative GitHub Actions workflow runs for the M32 merge ([PR #38](https://github.com/m-cahill/starlab/pull/38)).

## Final PR head (merge gate)

* **SHA:** `0c3f6ce4ab674c6fcc00daa3af0a6efabb69c6ce` (short `0c3f6ce…`)
* **Merged at (UTC):** `2026-04-10T05:56:16Z`

## Merge commit

* **SHA:** `cf7219911a208da584537b4c08ab5811fa3f67de` (short `cf72199…`)
* **Message:** Merge pull request #38 from m-cahill/m32-audit-closure-coverage-clone-run-manual-scaffold
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m32-audit-closure-coverage-clone-run-manual-scaffold` **deleted** after merge (if GitHub default)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24228528798`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24228528798

## Superseded red PR-head (not merge authority)

* None recorded for M32.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #38 to `main`; **authoritative** merge-boundary run)
* **headSha:** `cf7219911a208da584537b4c08ab5811fa3f67de`
* **Workflow run ID:** `24228788230`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24228788230

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, **Pytest with coverage and JUnit** (`coverage.xml`, `pytest-junit.xml`), pip-audit, CycloneDX SBOM upload, **Upload coverage.xml**, **Upload pytest JUnit**, Upload SBOM artifact, Gitleaks — all **success** on authoritative PR-head (`24228528798`) and merge-boundary `main` (`24228788230`).

## Pytest

* **574** tests passed with coverage gate `fail_under = 75.4` (see `pyproject.toml`) on merge tip — merge-boundary `main` CI [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230) — **success** (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

### Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow name | CI |
| Authoritative PR-head run | `24228528798` |
| Merge-boundary `main` run | `24228788230` |
| Trigger | `pull_request` / `push` |
| Branch + SHA | `m32-audit-closure-coverage-clone-run-manual-scaffold` @ `0c3f6ce…` / `main` @ `cf72199…` |

### Change context

* **Milestone:** M32 — **Audit Closure I**: measured coverage + truthful gate in CI, `coverage.xml` + `pytest-junit.xml` artifacts, SHA-pinned GitHub Actions, smoke markers / `Makefile`, clone-to-run + diligence docs, public deferred registry, ledger recharter **M00–M37**; **no** M33 CI tiering product, **no** M35 flagship proof pack, **no** live SC2 in CI.

### Baseline reference

* Trusted prior `main` at M31 merge tip (`97490de…` docs-only or `41d6205…` M31 merge — product baseline is pre-M32 PR).

### Step 1 — Workflow inventory

All listed steps **merge-blocking**; none use `continue-on-error`. Coverage and JUnit uploads use `if-no-files-found: error`.

### Step 2 — Signal integrity

* **Tests:** Full `pytest` with **`--cov=starlab`** and **`[tool.coverage.report] fail_under = 75.4`** — correctness + coverage honesty.
* **Artifacts:** `coverage.xml`, `pytest-junit.xml` — required uploads succeeded.
* **Static gates:** Ruff, Mypy — unchanged posture.
* **Security:** pip-audit, Gitleaks, SBOM — unchanged.

### Step 3 — Delta

* CI workflow, `pyproject.toml`, `Makefile`, governance/smoke tests, docs — both runs green.

### Step 4 — Failures

* None.

### Step 5 — Invariants

* Required checks enforced; no weakening; coverage measures `starlab` package as configured.

### Step 6 — Verdict

> **Verdict:** PR-head **`24228528798`** and merge-boundary **`24228788230`** are **safe to treat as merge authority** for M32: both **success** on the documented SHAs.

**Merge approved:** ✅ (CI evidence only; merge completed per ledger).

### Step 7 — Next actions

* Closeout docs + ledger + tag `v0.0.32-m32` on **merge commit** `cf72199…`; **M33** stub only — **no** M33 product code.

---

## Non-merge-boundary runs (post-closeout)

* **Post-closeout** documentation / governance commits on `main` after the merge boundary may produce additional green CI runs — **not** product merge authority for M32 (authoritative remains [`24228528798`](https://github.com/m-cahill/starlab/actions/runs/24228528798) + [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230)). Record any such run ID in §23 when ledger-only pushes occur.
