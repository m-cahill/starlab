# M01 — CI workflow analysis (run 1)

**Workflow:** CI (`ci.yml`)  
**Run ID:** `24048416111`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24048416111  
**Trigger:** `pull_request`  
**Branch:** `m01-sc2-runtime-surface-env-lock`  
**Head SHA:** `378c86425b63b7b0c048a011644333058a548e80`  
**PR:** [#2](https://github.com/m-cahill/starlab/pull/2) — *M01: SC2 runtime surface decision and environment lock*  
**Conclusion:** **success**  
**Analyzed:** 2026-04-06 (UTC)

**Milestone context:** M01 — SC2 runtime surface decision & environment lock (decision docs, environment lock, typed probe, ledger/governance updates). **Not** match execution or replay parsing proof.

**Baseline reference:** `origin/main` at `725250018bb09ce84e772ded0c7a184cc7d764ea` (pre-M01 merge).

---

## 1. Workflow inventory

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
|-------------|-----------|---------|-----------|----------|
| `governance` job (single job) | Yes | Full governance pipeline | Pass | Merge-blocking for this repo’s CI gate |
| Checkout | Yes | Source at PR head | Pass | `actions/checkout@v4`, `fetch-depth: 0` |
| Set up Python 3.11 | Yes | Toolchain | Pass | `actions/setup-python@v5`, cache pip |
| Install package (dev) | Yes | Editable install + dev deps | Pass | `pip install -e ".[dev]"` |
| Ruff check | Yes | Lint | Pass | `ruff check starlab tests` |
| Ruff format check | Yes | Format | Pass | `ruff format --check starlab tests` |
| Mypy | Yes | Static typing | Pass | `mypy starlab tests` |
| Pytest | Yes | Tests | Pass | `pytest -q` |
| pip-audit | Yes | Supply chain | Pass | `python -m pip_audit` |
| CycloneDX SBOM | Yes | SBOM artifact | Pass | `cyclonedx_py environment -o sbom.json` |
| Upload SBOM artifact | Yes | Artifact retention | Pass | `actions/upload-artifact@v4`; `if-no-files-found: error` |
| Gitleaks | Yes | Secret leak scan | Pass | `gitleaks/gitleaks-action@v2` |
| Job summary | Yes | Human-readable summary | Pass | Writes “STARLAB CI summary” to `$GITHUB_STEP_SUMMARY` |

**No `continue-on-error`** observed on required steps. No required checks muted or bypassed.

---

## 2. Signal integrity

### A) Tests

- **Tier:** Unit / governance smoke (pytest on `tests/`).
- **Result:** All tests passed on the PR head (32 tests).
- **Scope:** Covers governance doc presence, ledger strings, SC2 probe determinism and env precedence — appropriate for M01; no SC2 binary execution in CI (by design).

### B) Coverage

- **Enforced in CI:** No explicit coverage gate in workflow; not a coverage milestone.
- **Assessment:** Acceptable for M01; new logic has dedicated tests.

### C) Static / policy gates

- Ruff, Mypy enforce current Python 3.11 + strict typing on `starlab` + `tests`.
- Gitleaks + pip-audit + SBOM align with M00 governance posture.

### D) Performance / benchmarks

- Not present. N/A.

---

## 3. Delta analysis (change impact)

**Diff:** `725250018bb09ce84e772ded0c7a184cc7d764ea...378c86425b63b7b0c048a011644333058a548e80` — 18 files, +1327 / −117 lines (per `git diff --stat`).

**Direct CI impact:**  
- Workflow job summary text only (M00 → milestone-neutral label).  
- All steps still execute the same commands; no gate removal.

**Unexpected deltas:** None observed. Green run on first PR-head execution for this push.

---

## 4. Failure analysis

**None.** No failures in this run.

---

## 5. Invariants & guardrails

| Invariant | Held? |
|-----------|--------|
| Required CI checks enforced | Yes |
| No `continue-on-error` on merge-critical steps | Yes |
| No new SC2 runtime dependencies in `pyproject.toml` | Yes (verified in diff) |
| No licensed game assets committed | Yes |

---

## 6. Verdict

> **Verdict:** This PR-head run is **green** with all required governance steps passing on commit `378c86425b63b7b0c048a011644333058a548e80`. The signals match the declared M01 scope (docs + probe + tests + governance). No evidence of weakened gates or misleading success.

**Merge recommendation:** **Merge approved** from a **CI / governance** standpoint, subject to human review of content (not CI).

---

## 7. Next actions

| Action | Owner | Notes |
|--------|--------|------|
| Human code review + merge PR #2 | Human | When satisfied |
| Record merge SHA + post-merge `main` CI run in `docs/starlab.md` §18 | Human or agent post-merge | Do not fabricate |
| Run M02 on new branch after merge | Human | Per milestone plan |

---

*Analysis produced using structure from `docs/company_secrets/prompts/workflowprompt.md`.*
