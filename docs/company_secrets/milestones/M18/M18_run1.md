# CI / Workflow Analysis — M18 (PR #19)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative merge-gate run (PR-head, final tip):** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) — **success**  
**Trigger:** `pull_request`  
**Branch:** `m18-perceptual-bridge-prototype`  
**Commit (final PR head):** `8d9f9e1f8343120dd32916fb23668fd0ecee3fa0`

**Merge-boundary post-merge `main` run:** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) — **success**  
**Trigger:** `push` to `main` (merge commit `59d2d6e2af08852d63e0c91a984000c11decfece`)

**Superseded (not merge authority):** none for M18 — single green PR-head on final tip.

---

## Step 1 — Workflow inventory

| Job / Check       | Required? | Purpose                 | Pass/Fail |
| ----------------- | --------- | ----------------------- | --------- |
| `governance` job  | Yes       | Full repo quality gate | Pass      |
| Ruff check        | Yes       | Lint                    | Pass      |
| Ruff format check | Yes       | Format                  | Pass      |
| Mypy              | Yes       | Types                   | Pass      |
| Pytest            | Yes       | Tests (322 at closeout) | Pass      |
| pip-audit         | Yes       | Dependency scan         | Pass      |
| CycloneDX SBOM    | Yes       | SBOM                    | Pass      |
| Gitleaks          | Yes       | Secret scan             | Pass      |

**Annotation (informational):** Node.js 20 deprecation notice on GitHub-hosted runners — does not fail the job; track for future workflow hygiene (not M18 scope).

---

## Step 2 — Signal integrity (summary)

- **Tests:** Governance + M18 perceptual bridge pipeline goldens, `jsonschema` validation of emitted observation, CLI tests; pytest warning from `s2protocol` `imp` deprecation in `tests/test_parse_replay_cli.py` — **pre-existing**, outside M18 observation modules.
- **Static gates:** Ruff + Mypy aligned with `pyproject.toml`; no new runtime dependencies for M18 (uses existing `jsonschema`).
- **Security:** pip-audit + Gitleaks + SBOM steps completed green.

---

## Step 3 — Delta vs baseline

M18 adds `perceptual_bridge_prototype_v1.md`, `starlab/observation/` materialization modules (no `starlab.replays` / `s2protocol`), `tests/fixtures/m18/`, and `tests/test_observation_surface_pipeline.py`. CI signals cover changed Python and JSON fixtures.

---

## Step 4 — Failures

None on authoritative PR-head (`24165977039`) or merge-boundary `main` (`24166004479`) runs listed above.

---

## Step 5 — Invariants

- Required checks remained enforced; no `continue-on-error` on merge-blocking steps.
- No scope leakage into M19 reconciliation; no replay parsing or bundle load in M18 observation modules.

---

## Step 6 — Verdict

**Verdict:** The PR-head `pull_request` run on the final tip is green and suitable as the merge gate; post-merge `main` CI on the merge boundary is green. **Merge approved** for M18 product merge.

---

## Step 7 — Next actions (post-merge)

- Closeout ledger + milestone docs on `main` (this document supports §23 / §18).
- Proceed under **M19** planning only per `docs/company_secrets/milestones/M19/` stubs — no M19 product code until authorized.
