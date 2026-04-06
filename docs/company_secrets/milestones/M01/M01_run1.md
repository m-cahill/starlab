# M01 — CI workflow analysis (run 1)

This file records PR-head CI for **M01** on [PR #2](https://github.com/m-cahill/starlab/pull/2). Three green `pull_request` runs were witnessed on `m01-sc2-runtime-surface-env-lock` (implementation → closeout → evidence alignment). **Merge gating** should use the **latest** green run for the PR tip at merge time; GitHub’s PR UI is authoritative for the current OID.

---

## Run A — implementation

**Run ID:** `24048416111`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048416111  
**Head SHA:** `378c86425b63b7b0c048a011644333058a548e80`  
**Conclusion:** **success**

---

## Run B — closeout bundle

**Run ID:** `24048498203`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048498203  
**Head SHA:** `260c4e022db06a4e02f2827ec1efec8fa9b3c992`  
**Conclusion:** **success**

---

## Run C — evidence alignment (latest tip at closeout prep)

**Run ID:** `24048576545`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048576545  
**Head SHA:** `88b06db78fa9cb2b71217c03c752232df3a743ba`  
**Conclusion:** **success**

**Notes:** Updates `docs/starlab.md` §18 with the full witnessed PR-head CI table; `docs/company_secrets/milestones/M01/*` alignment.

---

## Workflow inventory (Run C — same job graph as A/B)

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|----------|
| `governance` job | Yes | Full governance pipeline | Pass | Merge-blocking |
| Checkout | Yes | Source at PR head | Pass | `actions/checkout@v4` |
| Set up Python 3.11 | Yes | Toolchain | Pass | |
| Install package (dev) | Yes | Editable install | Pass | |
| Ruff check | Yes | Lint | Pass | `ruff check starlab tests` |
| Ruff format check | Yes | Format | Pass | |
| Mypy | Yes | Types | Pass | |
| Pytest | Yes | Tests | Pass | |
| pip-audit | Yes | Supply chain | Pass | |
| CycloneDX SBOM + upload | Yes | SBOM | Pass | |
| Gitleaks | Yes | Secrets | Pass | |
| Job summary | Yes | Summary | Pass | “STARLAB CI summary” |

**Annotation (informational):** GitHub reported Node.js 20 deprecation notice for some actions — **not** a failure; track upstream action updates outside M01 scope.

---

## Signal integrity

- **Tests:** 32 passed on Run C head `88b06db…`.
- **Static gates:** Ruff, Mypy unchanged in behavior vs M00.
- **Coverage:** Not gated in CI (unchanged).

---

## Delta analysis

**Full PR diff (tip `88b06db…` vs `origin/main`):** `725250018bb09ce84e772ded0c7a184cc7d764ea...88b06db78fa9cb2b71217c03c752232df3a743ba` — 21 files (+/− per `git diff --stat origin/main...HEAD` at closeout prep).

---

## Verdict

> **Verdict:** Runs **A**, **B**, and **C** are **green** on their respective PR heads. **Run C** validates the latest tip at closeout prep (`88b06db…`). Required governance steps passed. **Merge approved** from a **CI / governance** standpoint (subject to human content review). Confirm the **current** PR head OID on GitHub before merge.

---

## Next actions

| Action | Owner |
|--------|--------|
| Merge PR #2 when ready | Human |
| Record merge SHA + post-merge `main` CI in `docs/starlab.md` §18 | After merge |

---

*Structure aligned with `docs/company_secrets/prompts/workflowprompt.md`.*
