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

## 2026-04-06 — Branch push & PR #8 (PR-head CI)

- **Branch:** `m07-replay-intake-policy-provenance-enforcement`
- **PR:** [#8](https://github.com/m-cahill/starlab/pull/8) — **M07: replay intake policy and provenance enforcement**
- **Implementation commit (M07 scope):** `ae909a392c67ce35d7865e1d1c76647963c988f7` — `feat(m07): replay intake policy and provenance enforcement`
- **Merge gate:** GitHub **CI** workflow on `pull_request` must be **success** for the PR tip at merge time (see PR **Checks** for current head SHA and run id).
- **PR-head CI runs witnessed (all success, chronological):** [`24065537231`](https://github.com/m-cahill/starlab/actions/runs/24065537231) → [`24065563616`](https://github.com/m-cahill/starlab/actions/runs/24065563616) → [`24065616533`](https://github.com/m-cahill/starlab/actions/runs/24065616533) → [`24065644646`](https://github.com/m-cahill/starlab/actions/runs/24065644646) → [`24065673229`](https://github.com/m-cahill/starlab/actions/runs/24065673229) → [`24065716156`](https://github.com/m-cahill/starlab/actions/runs/24065716156) → [`24065746526`](https://github.com/m-cahill/starlab/actions/runs/24065746526) → [`24065772651`](https://github.com/m-cahill/starlab/actions/runs/24065772651) → … → **authoritative PR-head (final tip):** [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) — **success** — head `a5188ad88bab688ab40136dea77a8b4d3caa0495`
- **Superseded failed runs:** none

---

## 2026-04-07 — Merge to `main` (PR #8) + post-merge CI

| Field | Value |
| ----- | ----- |
| **PR** | [#8](https://github.com/m-cahill/starlab/pull/8) |
| **Merge method** | Merge commit |
| **Merge commit** | `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` |
| **Merged at (GitHub)** | `2026-04-07T05:50:09Z` |
| **Final PR head (pre-merge)** | `a5188ad88bab688ab40136dea77a8b4d3caa0495` |
| **Remote branch deleted** | Yes (`m07-replay-intake-policy-provenance-enforcement`) |

**Authoritative CI (do not blur):**

| Category | Run | Conclusion | `headSha` / notes |
| -------- | --- | ---------- | ----------------- |
| **PR-head (merge gate, final tip)** | [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) | success | `a5188ad…` |
| **Post-merge `main` (merge boundary)** | [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) | success | `1c7bb0c…` (merge commit) |

**Later runs:** any **post-closeout** documentation-only push to `main` will produce additional CI — classify in `M07_run1.md` / §23 as **non-merge-boundary** when they appear.

**Closeout:** `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, `M07_plan.md` (**Status: Complete**), ledger `docs/starlab.md` — committed after merge as **doc follow-up** (CI run TBD at push time; **not** the merge-boundary run `24066550699`).
