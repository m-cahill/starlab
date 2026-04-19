# PX1-M04 — CI / workflow analysis (run 1 — PR1 opening / contract & pack selection)

**Milestone:** PX1-M04 — Governed Demo Proof Pack & Winning Video — **PR1** (ledger + public runtime contract + canonical selection memo + pack checklist / pack freeze — **not** operator-local pack assembly; **not** closeout).

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| PR | [#92](https://github.com/m-cahill/starlab/pull/92) — `feat(governance): open PX1-M04 governed demo proof pack and winning video (PR1)` |
| **Final PR head SHA** | `e57dac36d44c073198d773c8a8abd54bec5b5b56` |
| **Merge commit on `main`** | `f5e4521d35e152c97eb07458b38fb296929b5aaf` |
| **Authoritative PR-head CI** | [`24637019658`](https://github.com/m-cahill/starlab/actions/runs/24637019658) — **success** |
| **Superseded / failed runs** | [`24623471026`](https://github.com/m-cahill/starlab/actions/runs/24623471026) — **failure** (`ruff format --check` on **`tests/test_governance_ci.py`** at prior PR head `f6c154c3…`; **not** merge authority) |
| **Merge-boundary `main` CI** | [`24637049478`](https://github.com/m-cahill/starlab/actions/runs/24637049478) — **success** (push for merge commit `f5e4521d…`) |

---

## 2. Verdict

- **CI:** **Green** on **final** PR head and on **merge-boundary** `main`.
- **Merge:** **Merged** **2026-04-19** — **`PX1-M04`** **open** on `main` per §1 / §7 / §11; **PX1-M05** / **v2** **not** opened.

---

## 3. Post-merge operator posture

- **Operator-local demo proof pack assembly** is **not** recorded here — follow **`PX1-M04_pack_checklist.md`** / **`PX1-M04_pack_freeze.md`** after local packaging steps.
- **Milestone closeout** (summary/audit) is a **separate** future PR when authorized.
