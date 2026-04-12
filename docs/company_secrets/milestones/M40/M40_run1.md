# M40 — CI / workflow analysis (merge + main)

**Milestone:** M40 — Agent Training Program Charter & Artifact Contract  
**PR:** [#51](https://github.com/m-cahill/starlab/pull/51) — `M40: charter governed agent training program`  
**Branch:** `m40-agent-training-program-charter` (deleted on merge)

---

## 1. Workflow identity

| Field | Value |
| ----- | ----- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| **Authoritative PR-head run** | [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) |
| Trigger | `pull_request` |
| Final PR head SHA | `be47d913737f322bbf8e9e08a672561c71d322eb` |
| Conclusion | **success** |

| Field | Value |
| ----- | ----- |
| **Merge-boundary `main` run** | [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) |
| Trigger | `push` (merge of PR #51 to `main`) |
| Merge commit SHA | `44e8edc5bcce8dc99576bf2be542b273095e5072` |
| Merged at (UTC) | **2026-04-12T00:52:29Z** |
| Conclusion | **success** |

---

## 2. Superseded / not merge authority

| Run | SHA | Result | Note |
| --- | --- | --- | --- |
| [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) | `6690cd7f0ae79abe0db85695a0d20b4d7c48cdaf` | **failure** | **Ruff format check** failed. Corrected by `be47d91` (format-only). **Not** authoritative for merge. |

---

## 3. Required jobs — PR-head (`24295050784`)

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

## 4. Required jobs — merge-boundary `main` (`24295326123`)

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

## 5. Non-merge-boundary reference

Earlier successful `main` runs (e.g. M39 closeout docs at `24293224537`) are **historical** and **not** merge authority for M40 product merge.

---

## 6. Verdict

M40 PR and merge-boundary `main` CI are **green**. Safe to record **M40** closed on `main` with authoritative evidence above.
