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
- **Final PR head (tip):** `5af455b48684472ae7d8480f734ae09a83e5561f` (`docs(m07): clarify final PR head vs superseded PR-head CI run`)
- **Earlier commits on same PR:** `ae909a392c67ce35d7865e1d1c76647963c988f7` (feat M07), `7d4b9b90a3104014c6245e665bc54c9bdd6114a7` (toolcalls: PR #8 + first CI id)
- **PR:** [#8](https://github.com/m-cahill/starlab/pull/8) — **M07: replay intake policy and provenance enforcement**
- **Authoritative PR-head CI (merge gate, final tip `5af455b…`):** workflow **CI**, run [`24065616533`](https://github.com/m-cahill/starlab/actions/runs/24065616533), **conclusion: success** (`headSha` = `5af455b48684472ae7d8480f734ae09a83e5561f`)
- **Superseded PR-head runs (success, not final tip):** [`24065537231`](https://github.com/m-cahill/starlab/actions/runs/24065537231) (head `ae909a3…`); [`24065563616`](https://github.com/m-cahill/starlab/actions/runs/24065563616) (head `7d4b9b9…`)
- **Superseded failed runs:** none
