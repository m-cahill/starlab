# 📌 Milestone Summary — M21: Scripted Baseline Suite

**Project:** STARLAB  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Milestone:** M21 — Scripted Baseline Suite  
**Timeframe:** 2026-04-09 → 2026-04-09  
**Status:** Closed  

---

## 1. Milestone Objective

Prove the **first real consumer** of the M20 benchmark contract by loading one valid **`fixture_only`** benchmark contract, validating it with M20 `jsonschema` rules, emitting a deterministic **scripted baseline suite** artifact (`scripted_baseline_suite.json`) and companion report (`scripted_baseline_suite_report.json`) with embedded **M20-conformant scorecards** for a fixed small set of **scripted** subjects — without heuristic baselines, evaluation runner, tournament harness, benchmark integrity claims, replay↔execution equivalence claims, or live SC2 in CI.

Without this milestone, STARLAB would have schemas (M20) but no governed, CI-backed evidence that the contract surface can drive **fixture-only, scored** scorecard emission under explicit non-claims.

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/scripted_baseline_suite_v1.md`
- Product modules under `starlab/baselines/` (`scripted_baseline_models.py`, `scripted_baseline_suite.py`, `scripted_baseline_scorecards.py`, `emit_scripted_baseline_suite.py`)
- CLI `python -m starlab.baselines.emit_scripted_baseline_suite --benchmark-contract PATH --output-dir OUT`
- Artifacts: `scripted_baseline_suite.json`, `scripted_baseline_suite_report.json`
- Self-contained fixtures and goldens under `tests/fixtures/m21/`
- Tests `tests/test_scripted_baseline_suite.py`; governance updates; Phase IV ledger rows + baseline subject glossary in `docs/starlab.md`
- Closeout artifacts in `docs/company_secrets/milestones/M21/`

### Out of Scope

- Heuristic baselines (**M22**), evaluation runner / tournament harness (**M23**)
- Replay parsing, `starlab.replays`, `starlab.sc2`, `s2protocol` imports in M21 baseline modules (guarded by tests)
- Benchmark integrity, replay↔execution equivalence, live SC2 execution in CI

---

## 3. Work Executed

- Implemented deterministic suite assembly: contract validation, `measurement_surface: fixture_only` enforcement, **two** scripted subjects with fixed metric values, **one** fixture case catalog, embedded scorecards with locked posture (`evaluation_posture: fixture_only`, `scoring_status: scored`, `comparability_status: provisional`, `subject_kind: scripted`), sorted warnings/non_claims, gating outcomes aligned to contract rules.
- Added CLI and canonical JSON emission via `canonical_json_dumps`.
- Added fixture-backed goldens and tests including AST import guard; one **Ruff format** fix commit (`818002e…`) after initial red PR-head run (`24174444383`) — **not** merge authority; authoritative merge gate is **green PR-head** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912).

---

## 4. Validation & Evidence

- **PR:** [#22](https://github.com/m-cahill/starlab/pull/22) — merged **2026-04-09** (UTC `2026-04-09T05:41:36Z`).
- **Final PR head:** `818002e56b512e504c27f12aba8a39bc73627c82`
- **Merge commit:** `092d00a8aff720a1df9cbb1beec1cbf661546953`
- **Authoritative PR-head CI:** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) — success
- **Merge-boundary `main` CI:** [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) — success (push at merge commit `092d00a…`)
- Local: Ruff, Mypy, Pytest green before push; full CI matrix on GitHub as above.

---

## 5. CI / Automation Impact

- No workflow file changes; existing **CI** workflow unchanged.
- **M21** adds tests and modules; governance list extended with `scripted_baseline_suite_v1.md` and M21 fixture/module existence tests.

---

## 6. Issues & Exceptions

| Issue | Resolution |
| ----- | ---------- |
| First PR-head run (`24174444383`) failed **Ruff format** on `scripted_baseline_scorecards.py` | Fixed by `ruff format` + commit `818002e…`; superseded run is **not** merge authority |

No other new issues were introduced during this milestone.

---

## 7. Deferred Work

| Item | Deferred to | Notes |
| ---- | ----------- | ----- |
| Heuristic baseline suite | M22 | Explicitly out of scope for M21 |
| Evaluation runner / tournament harness | M23 | Explicitly out of scope for M21 |
| Benchmark integrity / replay↔execution equivalence | Future | Explicit non-claims preserved |

---

## 8. Governance Outcomes

- **Provable:** STARLAB can load a valid M20 benchmark contract (`fixture_only`), validate it, emit a deterministic suite + report with embedded scorecards that each pass `validate_benchmark_scorecard`, with no replay/runtime-stack imports in M21 baseline modules (test-enforced).
- **Still not provable:** benchmark integrity, heuristic baselines, runner, tournament harness, live SC2 in CI — unchanged.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Runtime contract + deterministic suite/report artifacts | Yes |
| Fixture-backed tests; goldens; no forbidden imports in M21 baseline modules | Yes |
| Authoritative PR-head CI green | Yes ([`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912)) |
| Merge-boundary `main` CI green | Yes ([`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486)) |
| `docs/starlab.md` updated at closeout | Yes |
| M22 stubs only (no M22 product code) | Yes |

---

## 10. Final Verdict

Milestone objectives met. **M21 closed.** Authorized next planning target: **M22** (stub only until authorized).

---

## 11. Authorized Next Step

- **M22 — Heuristic Baseline Suite:** planning stubs only (`docs/company_secrets/milestones/M22/M22_plan.md`, `M22_toolcalls.md`); **no** M22 product code until a dedicated milestone plan and PR.

---

## 12. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/22  
- Final PR head: `818002e56b512e504c27f12aba8a39bc73627c82`  
- Merge commit: `092d00a8aff720a1df9cbb1beec1cbf661546953`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24174468912  
- Merge-boundary `main` CI: https://github.com/m-cahill/starlab/actions/runs/24174498486  
- Contract: `docs/runtime/scripted_baseline_suite_v1.md`  
- Ledger: `docs/starlab.md`  
- Run log: `M21_run1.md`
