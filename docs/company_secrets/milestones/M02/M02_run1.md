# M02 — CI workflow analysis (PR-head + merge closeout)

## A) Authoritative PR-head CI (final tip before merge)

**Workflow:** `CI` (`.github/workflows/ci.yml`)  
**Authoritative run ID (final PR head):** `24055678613`  
**URL:** https://github.com/m-cahill/starlab/actions/runs/24055678613  
**Trigger:** `pull_request`  
**Branch:** `m02-deterministic-match-execution-harness`  
**Head SHA (merge gate):** `e88ca20424410cd99f834eeec92a5ec5d8034284`  
**PR:** [#3 — M02: deterministic match execution harness](https://github.com/m-cahill/starlab/pull/3) (merged)  
**Conclusion:** **success**  
**Recorded:** 2026-04-06

**Superseded PR-head run (older tip, not the merge gate):** `24054732181` on `290304a3ad3986029879c183f4e40159e7f5792c` — success (historical).

---

## B) Merge record

| Field | Value |
|-------|--------|
| **Merged at (UTC)** | `2026-04-06T23:35:21Z` |
| **Merge method** | **Merge commit** (not squash) |
| **Merge commit SHA** | `53a24a4a6106168afe79e0a70d51a20bfef4ea18` |
| **PR final state** | **MERGED** |
| **Head branch** | `m02-deterministic-match-execution-harness` — **deleted** after merge (GitHub default for `gh pr merge --delete-branch`) |

---

## C) Authoritative post-merge `main` CI (merge commit)

| Field | Value |
|-------|--------|
| **Event** | `push` to `main` |
| **Workflow** | **CI** |
| **Run ID** | `24056523452` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24056523452 |
| **Head SHA** | `53a24a4a6106168afe79e0a70d51a20bfef4ea18` (merge commit) |
| **Conclusion** | **success** |

*Later documentation-only pushes to `main` (e.g. M02 closeout ledger alignment) re-run CI; treat those as follow-up rows in `docs/starlab.md` §18, distinct from the merge-boundary run above.*

---

## 1. Workflow identity (PR-head inputs)

| Field | Value |
|-------|--------|
| Workflow name | CI |
| Run ID | 24055678613 |
| Trigger | PR against `main` |
| Commit | `e88ca20…` (final PR tip) |
| Milestone | M02 — Deterministic Match Execution Harness |
| Intent | Land harness + local evidence + docs + tests; keep CI SC2-free |

**Baseline:** prior trusted green on `main` (M01 era); this run validates the M02 delta including map-resolution fix and evidence files.

---

## 2. Step 1 — Workflow inventory

Single job: **`governance`**.

| Step / check | Merge-blocking | Purpose | Result |
|--------------|----------------|---------|--------|
| Checkout | Yes | Reproducible source | Pass |
| Python 3.11 | Yes | Version lock | Pass |
| `pip install -e ".[dev]"` | Yes | Dev deps only (no `sc2-harness`) | Pass |
| Ruff check | Yes | Lint | Pass |
| Ruff format --check | Yes | Format | Pass |
| Mypy | Yes | Types | Pass |
| Pytest | Yes | Tests (includes fake adapter; no SC2) | Pass |
| pip-audit | Yes | Supply chain | Pass |
| CycloneDX SBOM + upload | Yes | SBOM artifact | Pass |
| Gitleaks | Yes | Secret scan | Pass |
| Job summary | Informational | Markdown summary | Pass |

No `continue-on-error` on required checks.  
**Annotation (informational):** Node.js 20 deprecation notice for GitHub Actions — does not fail the job.

---

## 3. Step 2 — Signal integrity

### Tests

- **Tier:** unit / governance smoke + SC2 harness fake path + probe tests.
- **What CI proves:** Config parsing, artifact hashing, fake-adapter harness, map helpers, governance doc presence — all without a StarCraft II install.
- **What CI does not prove:** Live `burnysc2` execution (optional extra); cross-host reproducibility; replay binding; benchmark validity.

### Local evidence (out of CI)

- **Recorded** under `docs/company_secrets/milestones/M02/`: two successful same-machine `burnysc2` runs, matching normalized `artifact_hash` — **narrow** harness claim only.

---

## 4. Step 3 — Delta (M02 scope)

**Changed surface:** `starlab/sc2` harness modules, adapters, tests, runtime docs, ledger/README alignment, milestone evidence.

---

## 5. Step 5 — Invariants

- Required checks remain enforced; none weakened for M02.
- No benchmark or replay-scope expansion in CI.

---

## 6. Step 6 — Verdict

> **Verdict:** Final PR-head run **`24055678613`** on **`e88ca20…`** is **green** and was the **authoritative merge gate**. Post-merge **`24056523452`** on merge commit **`53a24a4…`** is **green**. Merge is **consistent with** governance CI. Local real-execution evidence supports the **narrow** same-machine harness claim only.

**Merge from CI/governance:** ✅ **Merged** — PR #3 closed with green checks on the final tip.

---

## 7. Step 7 — Next actions (post–M02 merge)

| Owner | Action |
|-------|--------|
| Project | M03 planning / implementation per `docs/company_secrets/milestones/M03/M03_plan.md` when authorized — **stubs only** at closeout. |
