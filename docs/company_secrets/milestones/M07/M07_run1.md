# M07 — CI run 1 (workflow analysis)

**Milestone:** M07 — Replay Intake Policy & Provenance Enforcement  
**Project:** STARLAB  
**Analysis format:** `docs/company_secrets/prompts/workflowprompt.md`

---

## A. Authoritative PR-head CI (merge gate)

These runs are **`pull_request`** triggers on branch `m07-replay-intake-policy-provenance-enforcement`. They are **not** post-merge `main` runs.

| Field | Value |
| ----- | ----- |
| **Final PR head SHA** | `a5188ad88bab688ab40136dea77a8b4d3caa0495` |
| **Authoritative PR-head run (final tip)** | [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) |
| **Conclusion** | **success** |
| **`headSha` match** | Yes — matches final PR tip |

**Earlier PR-head runs (all success, superseded by later pushes on the same PR):**  
`24065537231`, `24065563616`, `24065616533`, `24065644646`, `24065673229`, `24065716156`, `24065746526`, `24065772651`, and others — see `M07_toolcalls.md`. None failed on the merge path.

**Superseded failed runs:** none on PR #8.

---

## B. Authoritative post-merge `main` CI (merge boundary)

| Field | Value |
| ----- | ----- |
| **PR** | [#8](https://github.com/m-cahill/starlab/pull/8) — **M07: replay intake policy and provenance enforcement** |
| **Merge method** | Merge commit |
| **Merge commit SHA** | `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` |
| **Merged at (GitHub)** | `2026-04-07T05:50:09Z` |
| **Remote branch deleted** | Yes (`m07-replay-intake-policy-provenance-enforcement`) |

| Field | Value |
| ----- | ----- |
| **Post-merge `main` CI run** | [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) |
| **Trigger** | `push` to `main` (merge commit) |
| **Conclusion** | **success** |
| **`headSha`** | `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` (merge commit) |

This run is the **authoritative post-merge `main`** evidence for the M07 merge boundary.

---

## C. Non-merge-boundary CI (doc / ledger follow-up)

These runs are **`push`** triggers on `main` **after** the merge commit; they are **not** the merge-boundary post-merge run.

| # | Commit | Workflow run | Conclusion | Notes |
| - | ------ | ------------ | ---------- | ----- |
| 1 | `2ccac7ed1d9d3fc3c466916f41f1c4d6e9d6a2cc` | [`24066606427`](https://github.com/m-cahill/starlab/actions/runs/24066606427) | **success** | Milestone closeout artifacts + ledger (first doc push after merge) |
| 2 | `20a18706fe0c7338fbe4e1922e1a84ae7dc800d9` | [`24066644075`](https://github.com/m-cahill/starlab/actions/runs/24066644075) | **success** | Record run **24066606427** in `M07_run1` / §18; changelog hygiene — **not** merge-boundary |

**Classification:** both rows are **ledger / documentation only** — **not** merge-boundary events. **Authoritative** merge-boundary post-merge `main` CI remains [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) on merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`.

*Any further doc-only push (including a commit that records this table) may produce additional green runs — classify as **non-merge-boundary** unless the push is itself a PR merge to `main`.*

---

## D. Workflow inventory (representative — CI job)

For run [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699): job **governance** — Ruff check, Ruff format, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — **all required steps passed** (merge gate posture unchanged).

---

## E. Verdict

**Green** — PR-head and post-merge `main` CI both **success**. M07 merge is **suitable for ledger closeout** from a CI truth-signal perspective.
