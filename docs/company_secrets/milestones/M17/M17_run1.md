# CI / Workflow Analysis — M17 (PR #18)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative merge-gate run (PR-head, final tip):** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) — **success**  
**Trigger:** `pull_request`  
**Branch:** `m17-observation-surface-contract`  
**Commit (final PR head):** `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6`

**Merge-boundary post-merge `main` run:** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) — **success**  
**Trigger:** `push` to `main` (merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`)

**Superseded (not merge authority):** none for M17 — single green PR-head on final tip.

---

## Step 1 — Workflow inventory

| Job / Check       | Required? | Purpose                | Pass/Fail |
| ----------------- | --------- | ---------------------- | --------- |
| `governance` job  | Yes       | Full repo quality gate | Pass      |
| Ruff check        | Yes       | Lint                   | Pass      |
| Ruff format check | Yes       | Format                 | Pass      |
| Mypy              | Yes       | Types                  | Pass      |
| Pytest            | Yes       | Tests (310 at closeout) | Pass      |
| pip-audit         | Yes       | Dependency scan        | Pass      |
| CycloneDX SBOM    | Yes       | SBOM                   | Pass      |
| Gitleaks          | Yes       | Secret scan            | Pass      |

**Annotation (informational):** Node.js 20 deprecation notice on GitHub-hosted runners — does not fail the job; track for future workflow hygiene (not M17 scope).

---

## Step 2 — Signal integrity (summary)

- **Tests:** Governance + M17 observation schema/report goldens, `jsonschema` validation, CLI tests; no skips observed for required checks.
- **Static gates:** Ruff + Mypy aligned with `pyproject.toml`; no new runtime dependencies for M17 (uses existing `jsonschema`).
- **Security:** pip-audit + Gitleaks + SBOM steps completed green.

---

## Step 3 — Delta vs baseline

M17 adds `observation_surface_contract_v1.md`, `starlab/observation/` (contract-only — no materialization), `tests/fixtures/m17/`, and observation tests. CI signals cover changed Python and JSON fixtures.

---

## Step 4 — Failures

None on authoritative PR-head (`24164045530`) or merge-boundary `main` (`24164075167`) runs listed above.

---

## Step 5 — Invariants

- Required checks remained enforced; no `continue-on-error` on merge-blocking steps.
- No scope leakage into M18 perceptual bridge or canonical→observation materialization in this PR.

---

## Step 6 — Verdict

**Verdict:** The PR-head `pull_request` run on the final tip is green and suitable as the merge gate; post-merge `main` CI on the merge boundary is green. **Merge approved** for M17 product merge.

---

## Step 7 — Next actions (post-merge)

- Closeout ledger + milestone docs on `main` (this document supports §23 / §18).
- Proceed under **M18** planning only per `docs/company_secrets/milestones/M18/` stubs — no M18 product code until authorized.
