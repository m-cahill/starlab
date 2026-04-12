# M45 — CI / workflow analysis (final)

**Milestone:** M45 — Self-Play / RL Bootstrap v1  
**Status:** Closed on `main` (see `M45_summary.md` / `M45_audit.md`).

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#56](https://github.com/m-cahill/starlab/pull/56) — **M45: add self-play / RL bootstrap v1** |
| **Branch** | `m45-self-play-rl-bootstrap-v1` |
| **Final PR head SHA** | `0e89081cd786b527951a98eb3e63b7677f8c8c00` |
| **Authoritative PR-head CI** | [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) — **success** (all required jobs) |

---

## Superseded PR-head runs (not merge authority for final head `0e89081…`)

| Run ID | PR head (short) | Notes |
| ------ | ----------------- | ----- |
| [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) | `3b192004812f5c3ba0d714ca095ca2ff948fbaaf` | **Failure** — Ruff format (`quality` job); superseded by `0e89081…` (ruff format fix on `emit_self_play_rl_bootstrap_run.py`). |

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `1a585b68ea7413852ce78c220c6512bba6a004d7` |
| **Merged at (UTC)** | **2026-04-12T20:07:19Z** (GitHub `mergedAt`) |
| **Branch after merge** | `m45-self-play-rl-bootstrap-v1` **retained** on `origin` (not deleted) |
| **Merge-boundary `main` CI** | [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) — **success** on merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7` (`headSha` matches merge commit) |

### Merge-boundary `main` CI — job results ([`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180))

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

**Merge-boundary** authority for PR #56 remains [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) on merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`.

| Run ID | `main` head | Role |
| ------ | ----------- | ---- |
| [`24315387918`](https://github.com/m-cahill/starlab/actions/runs/24315387918) | `879a878eb9d64884982e89e9cdff0e838260d353` (M45 closeout commit) | **Non-merge-boundary** — documentation + governance + milestone artifacts + tag push alignment; **not** PR #56 product merge authority. |

Further doc-only `main` pushes after the row above remain **non-merge-boundary** relative to PR #56 unless explicitly rechartered — see Actions history on `main`.

---

## Historical workflow analysis (pre-closeout)

### Step 1 — Workflow inventory (authoritative PR-head `24314869292`)

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
| `ruff format --check` | Pass (after superseded failure on `24314843956`) |
| `mypy starlab tests` | Pass |
| `pytest` | Pass (including `tests/test_m45_self_play_rl_bootstrap.py`) |

---

## Tag

- **`v0.0.45-m45`** on merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7` (applied at closeout; push follows repo tag discipline).
