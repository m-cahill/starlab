# CI / Workflow Analysis — M16 (PR #17)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative merge-gate run (PR-head, final tip):** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) — **success**  
**Trigger:** `pull_request`  
**Branch:** `m16-structured-state-pipeline`  
**Commit (final PR head):** `11fb0803b8fa0343c08d9c3bda06929092a437d1`

**Merge-boundary post-merge `main` run:** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) — **success**  
**Trigger:** `push` to `main` (merge commit `dd9546f88ebcf9b454498eec83a14d742d17d070`)

**Superseded (not merge authority):** earlier PR-head run [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) — **failure** at **Ruff format check**; fixed on tip `11fb080…` (`style(state): ruff format canonical_state_inputs`).

---

## Step 1 — Workflow inventory

| Job / Check       | Required? | Purpose                | Pass/Fail |
| ----------------- | --------- | ---------------------- | --------- |
| `governance` job  | Yes       | Full repo quality gate | Pass      |
| Ruff check        | Yes       | Lint                   | Pass      |
| Ruff format check | Yes       | Format                 | Pass      |
| Mypy              | Yes       | Types                  | Pass      |
| Pytest            | Yes       | Tests (295 at closeout) | Pass      |
| pip-audit         | Yes       | Dependency scan        | Pass      |
| CycloneDX SBOM    | Yes       | SBOM                   | Pass      |
| Gitleaks          | Yes       | Secret scan            | Pass      |

**Annotation (informational):** Node.js 20 deprecation notice on GitHub-hosted runners — does not fail the job; track for future workflow hygiene (not M16 scope).

---

## Step 2 — Signal integrity (summary)

- **Tests:** Governance + M16 pipeline golden tests, bundle load/integrity tests, CLI tests; no skips observed for required checks.
- **Static gates:** Ruff + Mypy aligned with `pyproject.toml`; no new runtime dependencies for M16 (uses existing `jsonschema`).
- **Security:** pip-audit + Gitleaks + SBOM steps completed green.

---

## Step 3 — Delta vs baseline

M16 adds `canonical_state_pipeline_v1.md`, pipeline modules under `starlab/state/`, `tests/fixtures/m16/`, and `tests/test_canonical_state_pipeline.py`. CI signals cover changed Python and JSON fixtures.

---

## Step 4 — Failures

None on authoritative PR-head (`24160830775`) or merge-boundary `main` (`24160871811`) runs listed above.

---

## Step 5 — Invariants

- Required checks remained enforced; no `continue-on-error` on merge-blocking steps.
- No scope leakage into M17 observation surface or perceptual bridge in this PR.

---

## Step 6 — Verdict

**Verdict:** The PR-head `pull_request` run on the final tip is green and suitable as the merge gate; post-merge `main` CI on the merge boundary is green. **Merge approved** for M16 product merge.

---

## Step 7 — Next actions (post-merge)

- Closeout ledger + milestone docs on `main` (this document supports §23 / §18).
- Proceed under **M17** planning only per `docs/company_secrets/milestones/M17/` stubs — no M17 product code until authorized.
