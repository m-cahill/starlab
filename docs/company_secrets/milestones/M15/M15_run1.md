# CI / Workflow Analysis — M15 (PR #16)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative merge-gate run (PR-head, final tip):** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) — **success**  
**Trigger:** `pull_request`  
**Branch:** `m15-canonical-state-schema-v1`  
**Commit (final PR head):** `abc8ffcd223536568fcf134b1e21273915cf1d4d`

**Merge-boundary post-merge `main` run:** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) — **success**  
**Trigger:** `push` to `main` (merge commit `b0f7132a54508f35d54406011cd3b37bce776927`)

**Superseded (not merge authority):** earlier PR-head run [`24121376545`](https://github.com/m-cahill/starlab/actions/runs/24121376545) — **failure** at **Mypy** (`import-untyped` for `jsonschema`); fixed on tip `abc8ffc…` with `types-jsonschema` in dev dependencies.

---

## Step 1 — Workflow inventory

| Job / Check        | Required? | Purpose                          | Pass/Fail |
| ------------------ | --------- | -------------------------------- | --------- |
| `governance` job   | Yes       | Full repo quality gate           | Pass      |
| Ruff check         | Yes       | Lint                             | Pass      |
| Ruff format check  | Yes       | Format                           | Pass      |
| Mypy               | Yes       | Types                            | Pass      |
| Pytest             | Yes       | Tests (279 tests at time of run) | Pass      |
| pip-audit          | Yes       | Dependency vulnerabilities       | Pass      |
| CycloneDX SBOM     | Yes       | SBOM                             | Pass      |
| Gitleaks           | Yes       | Secret scan                      | Pass      |

**Annotation (informational):** Node.js 20 deprecation notice on GitHub-hosted runners — does not fail the job; track for future workflow hygiene (not M15 scope).

---

## Step 2 — Signal integrity (summary)

- **Tests:** Governance + M15 schema/report golden tests, fixture validation, CLI tests; no skips observed for required checks.
- **Static gates:** Ruff + Mypy aligned with `pyproject.toml`; `jsonschema` runtime dep + `types-jsonschema` dev stub package.
- **Security:** pip-audit + Gitleaks + SBOM steps completed green.

---

## Step 3 — Delta vs baseline

M15 adds `starlab/state/`, runtime contract `docs/runtime/canonical_state_schema_v1.md`, `jsonschema` dependency, fixtures under `tests/fixtures/m15/`, and governance list updates. CI signals cover changed Python and JSON fixtures.

---

## Step 4 — Failures

None on authoritative PR-head (`24122064141`) or merge-boundary `main` (`24122092800`) runs listed above.

---

## Step 5 — Invariants

- Required checks remained enforced; no `continue-on-error` on merge-blocking steps.
- No scope leakage into M16 extraction pipeline in this PR.

---

## Step 6 — Verdict

**Verdict:** The PR-head `pull_request` run on the final tip is green and suitable as the merge gate; post-merge `main` CI on the merge boundary is green. **Merge approved** for M15 product merge + subsequent doc-only closeout commit.

---

## Step 7 — Next actions (post-merge)

- Closeout ledger + milestone docs on `main` (this document supports §23 / §18).
- Proceed under **M16** planning only per `docs/company_secrets/milestones/M16/` stubs — no M16 product code until authorized.
