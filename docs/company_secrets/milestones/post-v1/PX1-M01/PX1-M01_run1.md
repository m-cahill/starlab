# PX1-M01 — CI / workflow analysis (run 1 — opening PR)

**Milestone:** PX1-M01 — Full Industrial Campaign Execution Evidence (opening / threshold-freeze PR only)  
**Mode:** PR-head validation + merge-boundary `main` verification  
**PR:** [PR #85](https://github.com/m-cahill/starlab/pull/85) — `feat(governance): open PX1-M01 full industrial campaign execution evidence`

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | **CI** (`.github/workflows/ci.yml`) |
| PR-head run | [`24589931847`](https://github.com/m-cahill/starlab/actions/runs/24589931847) |
| Trigger | `pull_request` |
| Branch | `px1-m01-full-industrial-campaign-execution-evidence` |
| Final PR head SHA | `135b5c9688a3d3a6b3274157d5f6130a83e66a34` |
| Merge commit (`main`) | `2b97b2afe556ad61a56b6604566ef935a70669d7` |
| Merge-boundary `main` run | [`24589979870`](https://github.com/m-cahill/starlab/actions/runs/24589979870) |
| Merge-boundary `main` head | `2b97b2afe556ad61a56b6604566ef935a70669d7` (matches merge commit) |

**Superseded runs:** none recorded as merge authority for this PR head.

---

## 2. Change context

| Field | Value |
| --- | --- |
| Objective | Open **PX1-M01** on ledger; freeze threshold; runtime + fixture + governance tests |
| Intent | Governance / documentation / tests only — **no** live SC2 execution |
| Run type | Release-related governance (ledger truthfulness) |

**Baseline:** `main` @ pre-PR state; invariants: **M00–M61** closed, **PV1** closed, **PX1-M00** closed, **v2** unopened.

---

## 3. Step 1 — Workflow inventory (PR-head run `24589931847`)

Merge-blocking aggregate: **`governance`** — required merge gate (aggregates `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship` per repo CI design).

Observed jobs (all **success**):

| Job / check area | Pass | Notes |
| --- | --- | --- |
| quality | ✓ | Ruff, format, etc. |
| smoke | ✓ | Pytest smoke + JUnit |
| tests | ✓ | Full test suite |
| security | ✓ | Includes gitleaks / supply-chain posture |
| fieldtest | ✓ | Fixture field test |
| flagship | ✓ | M39 flagship proof pack path |
| governance | ✓ | Aggregate merge gate |

**Annotations:** Node.js 20 deprecation notices on several actions — **informational**, did not fail jobs.

---

## 4. Signal integrity (summary)

| Category | Assessment |
| --- | --- |
| Tests | Full tier exercised on PR head; **921** tests passing locally pre-push; CI **success** |
| Static gates | Ruff / typing / policy jobs green on PR head |
| Coverage | Branch-aware gate unchanged; governance + runtime tests cover new PX1-M01 surfaces |
| Correctness | Docs-only + test assertions; **no** runtime execution path widened for live SC2 in default CI |

---

## 5. Merge-boundary `main` run (`24589979870`)

| Field | Value |
| --- | --- |
| Conclusion | **success** |
| Head SHA | `2b97b2afe556ad61a56b6604566ef935a70669d7` |

Validates merge commit on `main` after PR #85 merge.

---

## 6. Verdict

| Question | Answer |
| --- | --- |
| CI green on PR head? | **Yes** |
| Merge-boundary `main` green? | **Yes** |
| Merge-ready? | **Yes** (merged **2026-04-17**) |
| Fix required before merge? | **None** |

---

## 7. Residual risks / follow-ups

- **Low:** Node.js 20 action deprecation — track upstream action bumps separately.
- **Execution:** Live SC2 campaign **not** part of this PR — follow **`PX1-M01_execution_readiness.md`** before authoritative run.
