# M43 — CI / workflow analysis (final)

**Milestone:** M43 — Hierarchical Training Pipeline v1  
**Status:** Closed on `main` (see `M43_summary.md` / `M43_audit.md`).

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#54](https://github.com/m-cahill/starlab/pull/54) — **M43: add hierarchical training pipeline v1** |
| **Branch** | `m43-hierarchical-training-pipeline-v1` |
| **Final PR head SHA** | `ffc428454939702fbe9c100ace9e109ee0c51605` |
| **Authoritative PR-head CI** | [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558) — **success** (all required jobs) |

---

## Superseded PR-head runs (not merge authority for final head `ffc4284…`)

These runs were **green** on earlier PR heads during iteration; they are **superseded** for the actual merged tip:

| Run ID | PR head (short) | Notes |
| ------ | ----------------- | ----- |
| [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922) | `7167744…` | Doc iteration |
| [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086) | `2f46bb6…` | |
| [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928) | `719929d…` | |
| [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) | `e0df26c…` | First full M43 implementation push |

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `8850e378a584c9821eeab3e8c72bc499d590b308` |
| **Merged at (UTC)** | **2026-04-12T07:25:40Z** (GitHub `mergedAt`; merge commit author date aligned) |
| **Branch after merge** | `m43-hierarchical-training-pipeline-v1` **retained** on `origin` (not deleted) |
| **Merge-boundary `main` CI** | [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) — **success** on merge commit `8850e37…` (headSha matches merge commit) |

### Merge-boundary `main` CI — job results ([`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897))

| Job | Result |
| --- | ------ |
| `quality` | Pass |
| `smoke` | Pass |
| `tests` | Pass |
| `security` | Pass |
| `fieldtest` | Pass |
| `flagship` | Pass |
| `governance` | Pass |

---

## Non-merge-boundary `main` runs (post-merge)

**Merge-boundary** authority for PR #54 remains [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) on merge commit `8850e37…`. Later `push` workflows on `main` (ledger closeout, governance tweaks, etc.) are **not** that merge boundary unless explicitly rechartered — see Actions history on `main` for individual run IDs.

---

## Historical workflow analysis (pre-merge)

The sections below preserved the **pre-merge** workflow inventory (steps 1–7) from the development branch. **Authoritative** PR-head and merge facts are in the tables above.

### Step 1 — Workflow inventory (authoritative PR-head `24300864558`)

| Job / Check | Pass/Fail |
| ----------- | --------- |
| `quality` | Pass |
| `smoke` | Pass |
| `tests` | Pass |
| `security` | Pass |
| `fieldtest` | Pass |
| `flagship` | Pass |
| `governance` | Pass |

### Annotations (non-blocking)

- GitHub Actions **Node.js 20** deprecation **annotations** on Actions (informational).

### Local validation (pre-merge)

| Check | Result |
| ----- | ------ |
| `ruff check starlab tests` | Pass |
| `mypy starlab tests` | Pass |
| `pytest` | 724 passed; 1 DeprecationWarning from `s2protocol` (third-party) |

---

## Tag

- **`v0.0.43-m43`** on merge commit `8850e378a584c9821eeab3e8c72bc499d590b308`
