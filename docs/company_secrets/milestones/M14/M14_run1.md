# CI / Workflow Analysis — M14 (PR #15)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative merge-gate run (PR-head, final tip):** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) — **success**  
**Trigger:** `pull_request`  
**Branch:** `m14-replay-bundle-lineage-contract-v1`  
**Commit (final PR head):** `42e29f2a64fa4672dbd2df435a04836c379b5258`

**Merge-boundary post-merge `main` run:** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) — **success**  
**Trigger:** `push` to `main` (merge commit `8a0439a9a2970a74f3a5087390fc080f02852246`)

---

## Step 1 — Workflow inventory

| Job / Check        | Required? | Purpose                          | Pass/Fail |
| ------------------ | --------- | -------------------------------- | --------- |
| `governance` job   | Yes       | Full repo quality gate           | Pass      |
| Ruff check         | Yes       | Lint                             | Pass      |
| Ruff format check  | Yes       | Format                           | Pass      |
| Mypy               | Yes       | Types                            | Pass      |
| Pytest             | Yes       | Tests (265 tests at time of run) | Pass      |
| pip-audit          | Yes       | Dependency vulnerabilities       | Pass      |
| CycloneDX SBOM     | Yes       | SBOM                             | Pass      |
| Gitleaks           | Yes       | Secret scan                      | Pass      |

**Annotation (informational):** Node.js 20 deprecation notice on GitHub-hosted runners — does not fail the job; track for future workflow hygiene (not M14 scope).

---

## Step 2 — Signal integrity (summary)

- **Tests:** Unit/governance tests exercised M14 bundle generation, CLI, fixtures, and governance doc paths; no skips observed for required checks.
- **Static gates:** Ruff + Mypy aligned with `pyproject.toml`; no weakening.
- **Security:** pip-audit + Gitleaks + SBOM steps completed green.

---

## Step 3 — Delta vs baseline

M14 adds replay bundle modules, runtime contract, fixtures, and governance tests. CI signals directly cover changed Python and JSON fixtures.

---

## Step 4 — Failures

None on authoritative PR-head or merge-boundary `main` runs listed above.

---

## Step 5 — Invariants

- Required checks remained enforced; no `continue-on-error` on merge-blocking steps.
- No scope leakage into M15 product code in this PR.

---

## Step 6 — Verdict

**Verdict:** The PR-head `pull_request` run on the final tip is green and suitable as the merge gate; post-merge `main` CI on the merge boundary is green. **Merge approved** for M14 product merge + subsequent doc-only closeout commit.

---

## Step 7 — Next actions (post-merge)

- Closeout ledger + milestone docs on `main` (this document supports §23 / §18).
- Proceed under **M15** planning only per `docs/company_secrets/milestones/M15/` stubs — no M15 product code until authorized.
