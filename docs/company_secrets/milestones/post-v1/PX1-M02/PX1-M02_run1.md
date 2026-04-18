# PX1-M02 — CI / workflow analysis (run 1 — opening PR1)

**Milestone:** PX1-M02 — Play-Quality Evaluation & Demo Candidate Selection (opening / protocol-freeze PR only)  
**Mode:** PR-head validation + merge-boundary `main` verification  
**PR:** [PR #88](https://github.com/m-cahill/starlab/pull/88) — `feat(governance): open PX1-M02 play-quality evaluation and demo candidate selection`

---

## 1. Workflow identity

| Field | Value |
| --- | --- |
| Workflow | **CI** (`.github/workflows/ci.yml`) |
| PR-head run | [`24594170354`](https://github.com/m-cahill/starlab/actions/runs/24594170354) |
| Trigger | `pull_request` |
| Branch | `px1-m02-play-quality-demo-candidate-selection` |
| Final PR head SHA | `f44c66add532cc73b5dfa99ca26eb7640f961ae6` |
| Merge commit (`main`) | `5521d8b8671e72a5f9297148ff972b13b75e408a` |
| Merge-boundary `main` run | [`24594198357`](https://github.com/m-cahill/starlab/actions/runs/24594198357) |
| Merge-boundary `main` head | `5521d8b8671e72a5f9297148ff972b13b75e408a` (matches merge commit) |

**Superseded runs (not merge authority for final PR head):**

| Run | Conclusion | Notes |
| --- | --- | --- |
| [`24594051547`](https://github.com/m-cahill/starlab/actions/runs/24594051547) | **failure** | Ruff format + branch-aware coverage below gate — repaired on branch |
| [`24594125553`](https://github.com/m-cahill/starlab/actions/runs/24594125553) | **failure** | Branch-aware coverage **77.98%** vs **78.0%** gate — repaired on branch |

---

## 2. Change context

| Field | Value |
| --- | --- |
| Objective | Open **PX1-M02** on ledger; freeze bounded play-quality protocol; runtime + fixture + deterministic emitters + governance tests |
| Intent | Governance / contract / tests only — **no** live SC2 evaluation series; **no** demo-candidate selection claim |
| Run type | Release-related governance (ledger truthfulness + protocol freeze) |

**Baseline:** `main` before PR #88; invariants: **M00–M61** closed, **PV1** closed, **PX1-M00** / **PX1-M01** closed, **v2** unopened, **PX1-M03+** unopened.

---

## 3. Step 1 — Workflow inventory (PR-head run `24594170354`)

Merge-blocking aggregate: **`governance`** — required merge gate (aggregates `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship` per repo CI design).

Observed jobs (all **success**):

| Job / check area | Pass | Notes |
| --- | --- | --- |
| quality | ✓ | Ruff check + format + Mypy |
| smoke | ✓ | Pytest smoke + JUnit |
| tests | ✓ | Full test suite + branch-aware coverage gate |
| security | ✓ | pip-audit, SBOM, gitleaks |
| fieldtest | ✓ | Fixture field test |
| flagship | ✓ | M39 flagship proof pack path |
| governance | ✓ | Aggregate merge gate |

**Annotations:** Node.js 20 deprecation notices on several actions — **informational**, did not fail jobs.

---

## 4. Signal integrity (summary)

| Category | Assessment |
| --- | --- |
| Tests | Full tier exercised on PR head; CI **success** |
| Static gates | Ruff / Mypy green on PR head |
| Coverage | Branch-aware gate **78.0%** minimum unchanged; final head clears gate with margin after targeted tests |
| Correctness | Contract + emitters + fixture-driven tests; **no** widening of live SC2 evaluation as default merge evidence |

---

## 5. Merge-boundary `main` run (`24594198357`)

| Field | Value |
| --- | --- |
| Conclusion | **success** |
| Head SHA | `5521d8b8671e72a5f9297148ff972b13b75e408a` |

Validates merge commit on `main` after PR #88 merge.

---

## 6. Verdict

| Question | Answer |
| --- | --- |
| CI green on PR head? | **Yes** |
| Merge-boundary `main` green? | **Yes** |
| Merge-ready? | **Yes** (merged **2026-04-18**) |
| Fix required before merge? | **None** (superseded failures addressed on branch before final head) |

> **Verdict:** The **final** PR-head run and merge-boundary `main` run are consistent **success** signals for this governance/protocol-freeze surface. **Green** here means the repository gates passed on the declared SHAs — **not** that bounded live SC2 play-quality evaluation has been executed or that a demo candidate is selected.

---

## 7. Residual risks / follow-ups

- **Low:** Node.js 20 GitHub Actions deprecation — track upstream action bumps separately.
- **Execution:** Bounded **`local_live_sc2`** play-quality evaluation series is **not** part of PR1 — follow **`PX1-M02_execution_readiness.md`** before authoritative operator evaluation.

Made-with: Cursor
