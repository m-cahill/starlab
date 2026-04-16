# PV1-M02 — CI / Workflow Analysis (Run 1)

**Milestone:** PV1-M02 — Tranche A Execution Evidence  
**PR:** [#76](https://github.com/m-cahill/starlab/pull/76) → `main`  
**Final PR head SHA:** `d6e0c9c572d26b1cbc4c8c8fb791c63c7717d574`  
**Merge commit SHA:** `1c79c06f70e12215da14d1b0e0b5b71beac11ffd`  
**Change type:** Governance + documentation (runtime contract, ledger, governance tests, protocol fixture); **no** operator `out/` committed.

---

## Workflow identity

| Field | Value |
| --- | --- |
| Workflow | `CI` (`.github/workflows/ci.yml`) |
| Authoritative PR-head run | [`24539086056`](https://github.com/m-cahill/starlab/actions/runs/24539086056) — **success** — trigger: `pull_request` — branch `pv1-m02-tranche-a-execution-evidence` @ `d6e0c9c…` |
| Merge-boundary `main` run | [`24539635014`](https://github.com/m-cahill/starlab/actions/runs/24539635014) — **success** — trigger: `push` to `main` @ merge commit `1c79c06…` |
| Superseded PR-head run | [`24539076254`](https://github.com/m-cahill/starlab/actions/runs/24539076254) — **cancelled** (earlier head before docs PR #76 link commit) — **not** merge authority |

---

## Change context

| Field | Value |
| --- | --- |
| Milestone objective | First substantive **bounded operator-local Tranche A execution evidence** (repo contract + ledger); preserve non-claims (no full-run, no PV1-M03 auto-open). |
| Run character | **Release-related** (milestone closure) + **governance** (ledger truthfulness). |

---

## Step 1 — Workflow inventory (PR-head run `24539086056`)

| Job / Check | Required? | Purpose | Pass/Fail | Notes |
| --- | --- | --- | --- | --- |
| `quality` | Yes | Ruff + format | **pass** | Merge-blocking |
| `smoke` | Yes | Smoke tests | **pass** | Merge-blocking |
| `tests` | Yes | Pytest suite | **pass** | Merge-blocking |
| `security` | Yes | pip-audit / policy | **pass** | Merge-blocking |
| `fieldtest` | Yes | Field-test fixture path | **pass** | Merge-blocking |
| `flagship` | Yes | Flagship checks | **pass** | Merge-blocking |
| `governance` | Yes | Governance aggregate | **pass** | Merge-blocking |

No `continue-on-error` merge gates observed on this run.

---

## Step 2 — Signal integrity (summary)

- **Tests:** Full pytest tier ran; failures would block merge — none.
- **Static gates:** Ruff / format enforced — green.
- **Coverage:** Inherited `fail_under` unchanged by this doc-only delta; governance tests updated for closed PV1-M02.

---

## Step 3 — Delta analysis

**Changed:** `docs/starlab.md`, `docs/runtime/pv1_tranche_a_execution_evidence_v1.md`, `tests/fixtures/pv1_m02/`, `tests/test_governance_*.py`, private milestone notes.  
**CI signals:** Directly exercised governance + doc tests; no product runtime path change.

---

## Step 4 — Failure analysis

**None** on authoritative PR head or merge-boundary `main` run.

---

## Step 5 — Invariants

- Required CI checks remained enforced for merge.
- Bounded-claim discipline preserved in ledger (no widening of benchmark / equivalence / ladder / live-SC2 defaults).
- **PV1-M03** not opened by this PR.

---

## Step 6 — Verdict

**Verdict:** PR-head CI [`24539086056`](https://github.com/m-cahill/starlab/actions/runs/24539086056) and merge-boundary [`main`](https://github.com/m-cahill/starlab/actions/runs/24539635014) CI are **green** and **audit-defensible** for merging **PV1-M02** governance closeout.

**Decision:** ✅ **Merge approved** (executed: PR #76 merged to `main`).

---

## Step 7 — Next actions

| Action | Owner | Milestone |
| --- | --- | --- |
| Ledger closeout + private summary/audit (this pass) | Cursor / operator | PV1-M02 |
| **Do not** open **PV1-M03** unless chartered | Human | — |
