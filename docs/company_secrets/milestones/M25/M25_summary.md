# Milestone Summary — M25: Baseline Evidence Pack

**Project:** STARLAB  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Milestone:** M25 — Baseline Evidence Pack  
**Timeframe:** 2026-04-09 → 2026-04-09  
**Status:** Closed  

---

## 1. Milestone Objective

Prove a **deterministic, offline, fixture-only interpretive packaging layer** over governed **M21/M22** suite artifacts, one **M23** `evaluation_tournament.json`, and one **M24** `evaluation_diagnostics.json`, emitting **`baseline_evidence_pack.json`** and **`baseline_evidence_pack_report.json`** — **without** new benchmark semantics, **without** new scoring or diagnostics logic, **without** benchmark-integrity claims, and **without** replay execution, live SC2, or **M26** imitation work.

Without this milestone, STARLAB would lack a **governed evidence-pack surface** that ties the Phase IV chain together under explicit non-claims.

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/baseline_evidence_pack_v1.md`
- Product modules: `starlab/evaluation/evidence_pack_models.py`, `evidence_pack_views.py`, `emit_baseline_evidence_pack.py`
- Artifacts: `baseline_evidence_pack.json`, `baseline_evidence_pack_report.json`
- Entrant-scoped failure-view projection from M24; identity-first `evidence_refs`; canonical JSON + sorted warnings/non-claims
- Fixture-backed goldens under `tests/fixtures/m25/`; tests `tests/test_baseline_evidence_pack.py` including **M20 → M21/M22 → M23 → M24 → M25** chain
- AST import guard: no `starlab.replays`, `starlab.sc2`, or `s2protocol` in M25 evaluation modules
- Governance updates; Phase IV ledger; **M26** stubs (`M26_plan.md`, `M26_toolcalls.md`)

### Out of Scope

- New tournament or diagnostics semantics, re-ranking, or benchmark-integrity claims
- Replay↔execution equivalence, live SC2, raw replay or archive packaging
- **M26** imitation or learning product code

---

## 3. Work Executed

- Implemented validation and deterministic pack/report construction; M25-local `tournament_sha256` / `diagnostics_sha256` for packaging identity without changing M24’s governed inputs.
- Implemented CLI `python -m starlab.evaluation.emit_baseline_evidence_pack` with repeatable `--suite` inputs.
- Extended governance and ledger for Phase IV evidence-pack vocabulary and milestone closeout files.

---

## 4. Validation & Evidence

- **PR:** [#31](https://github.com/m-cahill/starlab/pull/31) — merged **2026-04-09T21:57:32Z** (UTC).
- **Final PR head:** `b132bfd53f0f31b81f6d2955ca659d5923cdd4b1`
- **Merge commit:** `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b`
- **Authoritative PR-head CI:** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) — success
- **Merge-boundary `main` CI:** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) — success
- Local / CI: Ruff, Ruff format, Mypy, Pytest (448 tests); one pre-existing `s2protocol` deprecation warning in replay CLI tests (unchanged).

---

## 5. CI / Automation Impact

- No workflow file changes; existing **CI** workflow unchanged.
- **M25** adds tests and `starlab/evaluation/` evidence-pack modules; governance extended for runtime doc, fixtures, and milestone closeout files.

---

## 6. Issues & Exceptions

| Issue | Resolution |
| ----- | ---------- |
| Superseded red PR-head runs (`24215241322`, `24215286216`) | Fixed governance test + docstring length before final green **24215322933** — **not** merge authority |

---

## 7. Deferred Work

| Item | Deferred to | Notes |
| ---- | ------------- | ----- |
| Replay-derived imitation baseline | M26 | Stub only; no M26 product code in M25 |
| Benchmark integrity / replay↔execution equivalence | Future | Explicit non-claims preserved |

---

## 8. Governance Outcomes

- **Provable:** STARLAB can combine governed **M21/M22 + M23 + M24** JSON into deterministic evidence-pack + report artifacts with no forbidden imports in M25 evaluation modules (test-enforced).
- **Still not provable:** benchmark integrity, live SC2 in CI, **M26** learning — unchanged.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Runtime contract + deterministic pack/report artifacts | Yes |
| Fixture-backed tests; goldens; import guard | Yes |
| Authoritative PR-head CI green | Yes ([`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933)) |
| Merge-boundary `main` CI green | Yes ([`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351)) |
| `docs/starlab.md` updated at closeout | Yes |
| M26 stub only (no M26 product code) | Yes |

---

## 10. Final Verdict

Milestone objectives met. **M25 closed.** Authorized next planning target: **M26** (replay-derived imitation baseline — stubs only until authorized).

---

## 11. Authorized Next Step

- **M26 — Replay-Derived Imitation Baseline:** planning stubs under `docs/company_secrets/milestones/M26/`; **no** M26 product code until a dedicated milestone plan and PR.

---

## 12. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/31  
- Final PR head: `b132bfd53f0f31b81f6d2955ca659d5923cdd4b1`  
- Merge commit: `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24215322933  
- Merge-boundary `main` CI: https://github.com/m-cahill/starlab/actions/runs/24215360351  
- Contract: `docs/runtime/baseline_evidence_pack_v1.md`  
- Ledger: `docs/starlab.md`  
- Run log: `M25_run1.md`
