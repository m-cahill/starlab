# M44 — CI / workflow analysis (final)

**Milestone:** M44 — Local Live-Play Validation Harness v1  
**Status:** Closed on `main` (see `M44_summary.md` / `M44_audit.md`).

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#55](https://github.com/m-cahill/starlab/pull/55) — **M44: add local live-play validation harness v1** |
| **Branch** | `m44-local-live-play-validation-harness-v1` |
| **Final PR head SHA** | `dc8e74d98701c6080e525b8a79aa7aa4b7872867` |
| **Authoritative PR-head CI** | [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411) — **success** (all required jobs) |

---

## Superseded PR-head runs (not merge authority for final head `dc8e74d…`)

| Run ID | PR head (short) | Notes |
| ------ | ----------------- | ----- |
| [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) | `c8b989a…` | **Failure** — Ruff format (`quality` job); superseded by `dc8e74d…` (`fix(ci): ruff format M44 modules`). |

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `1b1067ad632643d2b14da05d510a7c2a263cc8ea` |
| **Merged at (UTC)** | **2026-04-12T18:13:50Z** (GitHub `mergedAt`) |
| **Branch after merge** | `m44-local-live-play-validation-harness-v1` **retained** on `origin` (not deleted) |
| **Merge-boundary `main` CI** | [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) — **success** on merge commit `1b1067a…` (`headSha` matches merge commit) |

### Merge-boundary `main` CI — job results ([`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884))

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

**Merge-boundary** authority for PR #55 remains [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) on merge commit `1b1067a…`.

| Run ID | `main` head | Role |
| ------ | ----------- | ---- |
| [`24313225285`](https://github.com/m-cahill/starlab/actions/runs/24313225285) | `e3d14f4d61a4293bc355a050deacc3170fecc3e2` (closeout commit) | **Non-merge-boundary** — documentation-only closeout + tag push; **not** PR #55 product merge authority. |
| [`24313253583`](https://github.com/m-cahill/starlab/actions/runs/24313253583) | `5e4456c7171033153137a641409c5f79eb5d4bbf` (ledger + `M44_run1` refinement) | **Non-merge-boundary** — documentation-only; **not** PR #55 product merge authority. |

Later `push` workflows on `main` after the rows above are **not** the PR #55 merge boundary unless explicitly rechartered — see Actions history on `main`.

---

## Historical workflow analysis (pre-merge)

The sections below preserved the **pre-merge** workflow inventory from the development branch where useful. **Authoritative** PR-head and merge facts are in the tables above.

### Step 1 — Workflow inventory (authoritative PR-head `24312599411`)

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
| `ruff format --check` | Pass (after superseded failure on `24312572604`) |
| `mypy starlab tests` | Pass |
| `pytest` | Pass (including `tests/test_m44_local_live_play_validation_harness.py`) |

---

## Tag

- **`v0.0.44-m44`** on merge commit `1b1067ad632643d2b14da05d510a7c2a263cc8ea`
