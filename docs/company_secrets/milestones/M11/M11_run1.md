# M11 — CI / workflow evidence (run1)

**Milestone:** M11 — Build-Order & Economy Plane  
**Purpose:** Authoritative CI classification for **merge-gate PR-head** vs **merge-boundary `main`** vs non-merge-boundary doc-only runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#12](https://github.com/m-cahill/starlab/pull/12) |
| **Final PR head SHA** | `88ce7f9615c6c462b76674e1afb0734fc3dcc5be` |
| **Witnessed `pull_request` run** | [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) |
| **Conclusion** | **success** |
| **Workflow** | `CI` — job `governance` (Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks) |

**Authoritative green PR-head CI:** **yes** — a single completed **success** `pull_request` run on the final merge tip `88ce7f9…` is cited as merge authority for M11 (contrast M10, where the final tip had only a cancelled run).

---

## Authoritative post-merge `main` CI (merge boundary — merge commit)

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `38c15302badd49966b17f9195ddb139f6ae9a9b4` |
| **Workflow run ID** | `24106124347` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24106124347 |
| **Trigger** | `push` to `main` (merge of PR #12) |
| **Merged at (UTC)** | `2026-04-07T21:49:23Z` (GitHub merge timestamp) |

This run is the **witnessed merge-push** for the M11 merge commit **and is green** — no merge-boundary repair commit was required for M11.

---

## Non-merge-boundary runs (documentation / ledger closeout)

| Commit (short) | Workflow run | Conclusion | Notes |
| -------------- | ------------ | ---------- | ----- |
| *(pending)* | — | — | **At most one** post-merge closeout/ledger commit on `main` for M11; **not** a merge-boundary event unless the row records a PR merge. |

*Further doc-only pushes to `main` after this row may produce more green runs; add §23 bullets or short notes rather than extending this table indefinitely (M09 lesson).*

---

## Merge metadata (reference)

| Field | Value |
| ----- | ----- |
| **Merge method** | **Merge commit** (`Merge pull request #12 …`) |
| **Remote branch `m11-build-order-economy-plane`** | **Deleted** after merge |
