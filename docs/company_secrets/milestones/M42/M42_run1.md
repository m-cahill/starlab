# M42 — CI / workflow analysis (merge + main)

**Milestone:** M42 — Learned-Agent Comparison Harness v1  
**PR:** [#53](https://github.com/m-cahill/starlab/pull/53) — `M42: add learned-agent comparison harness v1`  
**Branch:** `m42-learned-agent-comparison-harness-v1` (**deleted** on `origin` after merge)

---

## 1. Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run** | [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) |
| Trigger | `pull_request` |
| Final PR head SHA | `191a95511a7428b0c12c79edc978070c406ad736` |
| Conclusion | **success** |

| Field | Value |
| ----- | ----- |
| **Merge-boundary `main` run** | [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) |
| Trigger | `push` (merge of PR #53 to `main`) |
| Merge commit SHA | `3eb091aba832cb0a66066d6fca6db091eb53c8f5` |
| Merge-boundary `main` head SHA | `3eb091aba832cb0a66066d6fca6db091eb53c8f5` |
| Merged at (UTC) | **2026-04-12T06:02:16Z** |
| Conclusion | **success** |

---

## 2. Superseded / not merge authority (PR branch)

No superseded PR-head runs. The sole PR-head CI run [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) on final head `191a955…` is the **only** run and the authoritative merge evidence.

---

## 3. Required jobs — PR-head (`24298501553`)

| Job | Result |
| --- | ------ |
| `quality` | Pass |
| `smoke` | Pass |
| `tests` | Pass |
| `security` | Pass |
| `fieldtest` | Pass |
| `flagship` | Pass |
| `governance` | Pass |

**Annotations:** GitHub Actions Node.js 20 deprecation notices (informational; pre-existing posture).

---

## 4. Required jobs — merge-boundary `main` (`24300065842`)

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

## 5. Non-merge-boundary `main` runs

- **Prior `main` tip before M42 merge** (M41 closeout at `22f464a…`): CI on that commit — **not** M42 merge-boundary authority.
- **Closeout / ledger documentation pushes** to `main` **after** merge commit `3eb091a…` (if any): treat as **non-merge-boundary** for M42 product merge — they validate hygiene only; **merge-boundary** for M42 remains **`24300065842`** on **`3eb091a…`**.

---

## 6. Verdict

M42 PR-head and merge-boundary `main` CI are **green** with all required jobs passing. **Authoritative** evidence for merge discipline: PR-head **`24298501553`**, merge-boundary **`24300065842`**. Safe to record **M42** closed on `main` per closeout artifacts and tag **`v0.0.42-m42`** on merge commit `3eb091a…`.
