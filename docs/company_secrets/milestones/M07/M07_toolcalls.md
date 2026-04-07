# M07 toolcalls log

---

## 2026-04-07 — Stub seeded (no implementation)

- **Purpose:** Milestone folder and stub plan created at **M06** closeout per project workflow.
- **Status:** No M07 implementation, tests, or feature code started.

---

## 2026-04-06 — M07 implementation (replay intake)

- **Purpose:** Land M07 replay intake policy, `starlab/replays/*`, contract doc, fixtures/tests, ledger updates, M08 stubs.
- **Status:** Implementation complete on branch; merge to `main` pending (PR TBD).

---

## 2026-04-06 — Pre-PR verification (continuation)

Commands run from repo root `c:\coding\starlab` (PowerShell), **before** branch push / PR open:

| Command | Outcome |
| ------- | ------- |
| `python -m pytest -q` | **Exit 0** — `149 passed` in ~1.65s |
| `ruff check .` | **Exit 0** — `All checks passed!` |
| `ruff format --check .` | **Exit 0** — `50 files already formatted` |
| `mypy starlab tests` | **Exit 0** — `Success: no issues found in 50 source files` |

Governance tests are included in pytest; M07 remains fixture-driven and SC2-free (no live SC2 in CI).

---

## 2026-04-06 — Branch push & PR #8 (authoritative PR-head CI)

- **Branch:** `m07-replay-intake-policy-provenance-enforcement`
- **Final PR head (tip):** `2d58d6b2ca159ca1535931d53170faddc8003860` (`docs(m07): record authoritative PR-head CI for tip 9f8d602`)
- **Earlier commits on same PR:** `ae909a392c67ce35d7865e1d1c76647963c988f7` (feat M07); subsequent docs-only toolcalls commits
- **PR:** [#8](https://github.com/m-cahill/starlab/pull/8) — **M07: replay intake policy and provenance enforcement**
- **Authoritative PR-head CI (merge gate, matches final tip `2d58d6b…`):** workflow **CI**, run [`24065716156`](https://github.com/m-cahill/starlab/actions/runs/24065716156), **conclusion: success** (`headSha` = `2d58d6b2ca159ca1535931d53170faddc8003860`)
- **Superseded PR-head runs (success, earlier tips):** [`24065537231`](https://github.com/m-cahill/starlab/actions/runs/24065537231) (`ae909a3…`); [`24065563616`](https://github.com/m-cahill/starlab/actions/runs/24065563616) (`7d4b9b9…`); [`24065616533`](https://github.com/m-cahill/starlab/actions/runs/24065616533) (`5af455b…`); [`24065644646`](https://github.com/m-cahill/starlab/actions/runs/24065644646) (`cdd9b12…`); [`24065673229`](https://github.com/m-cahill/starlab/actions/runs/24065673229) (`9f8d602…`)
- **Superseded failed runs:** none
