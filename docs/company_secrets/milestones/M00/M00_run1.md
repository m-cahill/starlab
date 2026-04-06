# M00 — CI / Workflow analysis (run 1)

Analysis follows `docs/company_secrets/prompts/workflowprompt.md`.

---

## Inputs (mandatory)

| Field | Value |
|-------|--------|
| **Workflow name** | CI |
| **Run ID** | 24015581129 |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24015581129 |
| **Trigger** | `pull_request` (PR #1 → `main`) |
| **Branch** | `m00-governance-bootstrap` |
| **Commit SHA** | `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91` |
| **Milestone** | M00 — Governance bootstrap |
| **Run type** | Release-related (milestone merge gate) |
| **Baseline** | Prior trusted state: `main` @ `3f54e4e` (Initial commit) |

---

## Step 1 — Workflow inventory

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|-------|
| Checkout | Yes | Reproducible tree | Pass | `fetch-depth: 0` (Gitleaks history) |
| Set up Python 3.11 | Yes | Toolchain pin | Pass | Matches `pyproject.toml` |
| Install package (dev) | Yes | Editable install + dev deps | Pass | Upgrades `pip`/`setuptools` before audit |
| Ruff check | Yes | Lint | Pass | `starlab`, `tests` |
| Ruff format check | Yes | Format gate | Pass | |
| Mypy | Yes | Static types | Pass | `starlab`, `tests` |
| Pytest | Yes | Governance smoke tests | Pass | 15 tests |
| pip-audit | Yes | Supply-chain vulns | Pass | |
| CycloneDX SBOM | Yes | SBOM generation | Pass | `python -m cyclonedx_py environment` |
| Upload SBOM artifact | Yes | Evidence retention | Pass | |
| Gitleaks | Yes | Secret scan | Pass | |
| Job summary | Info | `GITHUB_STEP_SUMMARY` | Pass | |

No `continue-on-error` observed. All listed steps are merge-blocking for this workflow.

---

## Step 2 — Signal integrity

| Category | What it measures | Assessment |
|----------|------------------|--------------|
| **Tests** | Governance wiring only (`tests/test_governance.py`) | Measures presence of docs, CI file, milestones path — appropriate for M00. |
| **Coverage** | Not enforced in M00 | Acceptable; no application logic to cover. |
| **Static gates** | Ruff, Mypy | Enforce current Python surface. |
| **Security** | pip-audit, Gitleaks | Meaningful for installed dev env. |

---

## Step 3 — Delta vs baseline

- **Change:** Full repo bootstrap vs single-file `main`.
- **CI:** New workflow; no prior CI to compare.
- **Unexpected:** None; single green run on PR head.

---

## Step 4 — Failures

None.

---

## Step 5 — Invariants

- Required checks enforced.
- No weakened gates.
- M00 scope: governance-only; CI does not claim runtime/replay/benchmark behavior.

---

## Step 6 — Verdict

> **Verdict:** This run is a truthful governance signal for M00: lint, types, smoke tests, dependency audit, SBOM generation, and secret scanning all completed successfully on the PR head commit. It supports merge to `main` for this milestone.

**✅ Merge approved** (subject to human/branch protection policy on the repo).

---

## Step 7 — Next actions

| Action | Owner | Scope |
|--------|-------|-------|
| Merge PR #1 after review | Maintainer | M00 |
| Record merge + CI in `docs/starlab.md` | Maintainer / agent | Closeout |
| M01 environment lock | Next milestone | Not started until authorized |

---

## Annotation note

GitHub reported a **Node.js 20 deprecation** notice for Actions (informational). Does not fail the job; track for future workflow YAML bumps (pin newer action majors when available).
