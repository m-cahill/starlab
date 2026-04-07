# M09 — CI / workflow evidence (run1)

**Milestone:** M09 — Replay Metadata Extraction  
**Purpose:** Authoritative CI classification for merge gating vs post-merge `main` vs follow-up documentation runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#10](https://github.com/m-cahill/starlab/pull/10) |
| **Final PR head SHA** | `3f161dea12a9b7ffb6dbe01c73b01f351a7219da` |
| **Workflow run ID** | `24101861888` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24101861888 |
| **Trigger** | `pull_request` (CI on PR branch at merge tip) |

This run is the **authoritative merge gate** for the M09 feature branch before merge to `main`.

**Superseded PR-head runs:** none observed for the final merge tip — a single green `pull_request` run at `3f161de…` is merge authority.

---

## Authoritative post-merge `main` CI (merge boundary)

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` |
| **Workflow run ID** | `24101900950` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24101900950 |
| **Trigger** | `push` to `main` (merge of PR #10) |
| **Merged at (UTC)** | `2026-04-07T20:05:59Z` (GitHub merge timestamp) |

This run validates **`main` at the merge commit** immediately after PR #10 landed. It is the **authoritative post-merge `main` CI** for the M09 merge boundary.

**Workflow:** `CI` — job `governance` (Ruff, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks).

---

## Merge metadata (reference)

| Field | Value |
| ----- | ----- |
| **Merge method** | **Merge commit** (`Merge pull request #10 …`) |
| **Remote branch `m09-replay-metadata-extraction`** | **Deleted** (per `gh pr merge --delete-branch`) |

---

## Non-merge-boundary runs (documentation / ledger closeout)

After the merge commit, any additional `push` to `main` that updates only milestone closeout docs, `docs/starlab.md`, or `M09_toolcalls.md` hygiene **is not** a merge-boundary event.

### Non-merge-boundary (doc-only / ledger-only)

| Commit | Workflow run | Conclusion | Notes |
| ------ | ------------ | ---------- | ----- |
| `147b1f4810ad2e0dbb926c7a971748c4db68bdbc` | [`24102029092`](https://github.com/m-cahill/starlab/actions/runs/24102029092) | **success** | M09 closeout: `M09_run1.md`, `M09_summary.md`, `M09_audit.md`, `docs/starlab.md`, M10 stubs — **not** a merge-boundary event. |
| `44a0bce631854e6039442ca49609228a0650adf3` | [`24102071251`](https://github.com/m-cahill/starlab/actions/runs/24102071251) | **success** | Ledger §23 / `M09_run1` non-merge-boundary CI row sync — **not** a merge-boundary event. |
| `2d3bc95d97b14a01d40d41b84565f270ca6b22ab` | [`24102113672`](https://github.com/m-cahill/starlab/actions/runs/24102113672) | **success** | Follow-up §23 / `M09_run1` row for prior non-merge-boundary commit — **not** a merge-boundary event. |

**Authoritative merge-boundary** post-merge `main` CI for M09 remains **`24101900950`** on merge commit **`fc9b442…`** (above).

*Further documentation-only pushes to `main` after this table may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary events.*
