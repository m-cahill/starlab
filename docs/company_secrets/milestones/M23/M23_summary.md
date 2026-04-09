# 📌 Milestone Summary — M23: Evaluation Runner & Tournament Harness

**Project:** STARLAB  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Milestone:** M23 — Evaluation Runner & Tournament Harness  
**Timeframe:** 2026-04-09 → 2026-04-09  
**Status:** Closed  

---

## 1. Milestone Objective

Prove the **first governed evaluation consumer** of the M20 benchmark surface by loading one valid **`fixture_only`** M20 benchmark contract together with governed **M21** scripted and **M22** heuristic baseline suite artifacts, then deterministically emitting **`evaluation_tournament.json`** and **`evaluation_tournament_report.json`** with a **minimal round-robin harness** — without claiming benchmark integrity, leaderboard validity, replay↔execution equivalence, live SC2 execution, replay-derived scoring, attribution/diagnostics (**M24**), or evidence-pack packaging (**M25**).

Without this milestone, STARLAB would lack a **fixture-only** proof that baseline suites can be **consumed together** under a deterministic tournament harness with explicit non-claims.

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/evaluation_runner_tournament_harness_v1.md`
- Product modules under `starlab/evaluation/` (runner, tournament harness, CLI `emit_evaluation_tournament`)
- Artifacts: `evaluation_tournament.json`, `evaluation_tournament_report.json`
- Structural validation of M21/M22 suite inputs (no new suite JSON Schema in M23)
- Pairwise outcomes decided by **`scoring_role: primary`** metric only; full per-metric comparison rows recorded
- Points: 1.0 / 0.5 / 0.0 (win / draw / loss)
- Fixture-backed goldens under `tests/fixtures/m23/`; reuse shared M20 contract + M21/M22 expected suite JSON where practical
- Tests `tests/test_evaluation_tournament.py` including **M20 → M21/M22 emitters → M23** chain test
- AST import guard: no `starlab.replays`, `starlab.sc2`, or `s2protocol` in M23 evaluation modules
- Governance updates; Phase IV ledger; **M24** stubs only (`M24_plan.md`, `M24_toolcalls.md`)

### Out of Scope

- Benchmark integrity, leaderboard validity, replay↔execution equivalence
- Live SC2, replay parsing, attribution/diagnostics (**M24**), evidence packs (**M25**)
- New baseline subjects beyond M21/M22 fixed entrants; re-scoring or non-fixture measurement

---

## 3. Work Executed

- Implemented deterministic loading: M20 contract validation, M21/M22 suite structural gates, entrant flattening (`suite_id::subject_id`), canonical suite path strings (cwd-relative when under repo root).
- Implemented round-robin harness: `entrant_a`/`entrant_b` order from flattened entrant list; match IDs `starlab.evaluation_tournament.v1.match.NNNN`; standings sort by points, primary tie-break scalar, `entrant_id` lexicographic.
- Added CLI accepting repeated `--suite`; non-zero exit on invalid JSON, schema failures, or incompatible suites.
- Added goldens and comprehensive tests including E2E emission from M21/M22 suite emitters into M23 runner.

---

## 4. Validation & Evidence

- **PR:** [#24](https://github.com/m-cahill/starlab/pull/24) — merged **2026-04-09T07:41:53Z** (UTC).
- **Final PR head:** `f00711a3a2c16573f31492398de59387fe284711`
- **Merge commit:** `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`
- **Authoritative PR-head CI:** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) — success
- **Merge-boundary `main` CI:** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) — success
- Local / CI: Ruff, Ruff format, Mypy, Pytest (413 tests); one pre-existing `s2protocol` deprecation warning in replay CLI tests (unchanged).

---

## 5. CI / Automation Impact

- No workflow file changes; existing **CI** workflow unchanged.
- **M23** adds tests and `starlab/evaluation/` modules; governance extended for runtime doc, fixtures, and milestone closeout files.

---

## 6. Issues & Exceptions

| Issue | Resolution |
| ----- | ---------- |
| None blocking | — |

No superseded red PR-head runs on the final M23 merge tip.

---

## 7. Deferred Work

| Item | Deferred to | Notes |
| ---- | ------------- | ----- |
| Attribution / diagnostics / failure views | M24 | Stub only; no M24 product code in M23 |
| Baseline evidence pack | M25 | Explicit non-claim |
| Benchmark integrity / replay↔execution equivalence | Future | Explicit non-claims preserved |

---

## 8. Governance Outcomes

- **Provable:** STARLAB can load a valid **`fixture_only`** M20 contract and governed **M21/M22** suite artifacts, run a deterministic **fixture-only** round-robin tournament, and emit canonical tournament + report JSON with no replay/runtime-stack imports in `starlab/evaluation/` (test-enforced).
- **Still not provable:** benchmark integrity, leaderboard validity, M24 diagnostics, M25 evidence packs, live SC2 in CI — unchanged.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Runtime contract + deterministic tournament/report artifacts | Yes |
| Fixture-backed tests; goldens; import guard | Yes |
| Authoritative PR-head CI green | Yes ([`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859)) |
| Merge-boundary `main` CI green | Yes ([`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940)) |
| `docs/starlab.md` updated at closeout | Yes |
| M24 stubs only (no M24 product code) | Yes |

---

## 10. Final Verdict

Milestone objectives met. **M23 closed.** Authorized next planning target: **M24** (attribution / diagnostics / failure views — stubs only until authorized).

---

## 11. Authorized Next Step

- **M24 — Attribution, Diagnostics, and Failure Views:** planning stubs under `docs/company_secrets/milestones/M24/`; **no** M24 product code until a dedicated milestone plan and PR.

---

## 12. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/24  
- Final PR head: `f00711a3a2c16573f31492398de59387fe284711`  
- Merge commit: `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24178571859  
- Merge-boundary `main` CI: https://github.com/m-cahill/starlab/actions/runs/24178615940  
- Contract: `docs/runtime/evaluation_runner_tournament_harness_v1.md`  
- Ledger: `docs/starlab.md`  
- Run log: `M23_run1.md`
