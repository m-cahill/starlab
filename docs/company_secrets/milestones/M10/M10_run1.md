# M10 — CI / workflow evidence (run1)

**Milestone:** M10 — Timeline & Event Extraction  
**Purpose:** Authoritative CI classification for merge gating vs post-merge `main` vs repair / closeout runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#11](https://github.com/m-cahill/starlab/pull/11) |
| **Final PR head SHA** | `cb066fe3f09b07f3390e85928c88f65a6e75cd6f` |
| **Witnessed `pull_request` run** | [`24104110934`](https://github.com/m-cahill/starlab/actions/runs/24104110934) |
| **Conclusion** | **cancelled** (merge landed while the workflow was starting; no green merge-gate run completed on the final tip) |

**Authoritative green PR-head CI:** **none** — the only `pull_request` run observed on the final merge tip was **cancelled**; there is **no** successful merge-gate run ID for `cb066fe…` to cite as merge authority.

---

## Authoritative post-merge `main` CI (merge boundary — merge commit)

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `cb3e581f70f85653477081eb1ef4772229f05983` |
| **Workflow run ID** | `24104111851` |
| **Conclusion** | **failure** (Mypy: `parser_io.py` redefinition, `timeline_io.py` missing annotation) |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24104111851 |
| **Trigger** | `push` to `main` (merge of PR #11) |
| **Merged at (UTC)** | `2026-04-07T20:58:46Z` (GitHub merge timestamp) |

This run is the **witnessed merge-push** for the M10 merge commit; it is **not** green and is **not** authoritative for “governed CI proves M10 on `main`.”

---

## Authoritative green `main` CI (M10 repair — supersedes merge-only failure)

| Field | Value |
| ----- | ----- |
| **Commit SHA** | `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b` |
| **Workflow run ID** | `24104197912` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24104197912 |
| **Trigger** | `push` to `main` (Mypy fix for M10) |

This is the **authoritative green `main` CI** demonstrating Ruff, Mypy, Pytest, and governance jobs on `main` after M10 landed, once Mypy issues were fixed. It is **not** a merge-boundary event (see `docs/starlab.md` §23).

**Workflow:** `CI` — job `governance` (Ruff, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks).

---

## Non-merge-boundary runs (documentation / ledger closeout)

| Commit (short) | Workflow run | Conclusion | Notes |
| -------------- | ------------ | ---------- | ----- |
| `f78a435…` | [`24104280039`](https://github.com/m-cahill/starlab/actions/runs/24104280039) | **success** | M10 closeout: ledger + `M10_run1` / summary / audit + governance test — **not** merge-boundary; **authoritative** green repair remains `cf2074e…` / `24104197912`. |

*Further doc-only pushes to `main` after this row may produce more green runs; add §23 bullets or short notes rather than extending this table indefinitely (M09 lesson).*

---

## Merge metadata (reference)

| Field | Value |
| ----- | ----- |
| **Merge method** | **Merge commit** (`Merge pull request #11 …`) |
| **Remote branch `m10-timeline-event-extraction`** | **Deleted** (not present on `origin` after merge) |
