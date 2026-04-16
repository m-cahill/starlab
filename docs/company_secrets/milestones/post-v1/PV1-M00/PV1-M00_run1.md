# PV1-M00 — CI / workflow analysis (run 1)

**Milestone:** PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria  
**Change type:** Governance / documentation only (ledger + private milestone docs + governance tests).

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | **CI** (`ci.yml`) |
| **Authoritative PR-head run** | [`24531908110`](https://github.com/m-cahill/starlab/actions/runs/24531908110) |
| Trigger | `pull_request` |
| Branch | `pv1-m00-charter-post-v1-industrial-campaign` |
| **Head SHA (PR)** | `2f80cfa9c1d329b520ebb99280bb12c21bfaa81d` |
| Conclusion | **success** |

### Jobs (PR-head)

| Job | Result | Notes |
| --- | --- | --- |
| quality | pass | Ruff, format |
| smoke | pass | Includes governance smoke |
| tests | pass | Full pytest |
| security | pass | pip-audit, gitleaks, etc. |
| fieldtest | pass | Fixture explorer |
| flagship | pass | M39 proof pack |
| governance | pass | Aggregate merge gate |

**Superseded runs:** None identified as merge authority for the final head (single green PR-head run).

---

## 2. Merge-boundary `main` CI

| Field | Value |
| --- | --- |
| Run | [`24532016096`](https://github.com/m-cahill/starlab/actions/runs/24532016096) |
| Event | `push` (merge to `main`) |
| **Merge commit** | `77118675a6f9f76e7cd466269c8d2a19ace3552f` |
| Conclusion | **success** |

Merge-boundary run validates the same **CI** workflow on `main` after PR **#73** merge.

---

## 3. Signal integrity

- **Tests:** Full suite passed on PR head; change surface is docs + governance tests only — no new product code paths.
- **Lint / types:** Green on PR workflow (quality job).
- **No** weakened gates or `continue-on-error` on required checks observed for this run.

---

## 4. Merge readiness

- **PR:** [#73](https://github.com/m-cahill/starlab/pull/73) — **merged** to `main`.
- **CI:** Green on **PR head** and **merge-boundary `main`**.
- **Fixes needed before merge:** None (governance-only).

---

## 5. Annotations / noise

- Node.js 20 deprecation warnings on GitHub Actions (informational; not introduced by PV1-M00).
