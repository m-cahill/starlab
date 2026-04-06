# 📌 Milestone Summary — M01: SC2 Runtime Surface Decision & Environment Lock

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M01 — SC2 Runtime Surface Decision & Environment Lock  
**Timeframe:** 2026-04-06 → 2026-04-06 (implementation + closeout prep on branch)  
**Status:** **Closed** (deliverables complete on branch; merge to `main` via [PR #2](https://github.com/m-cahill/starlab/pull/2) pending at documentation time)

---

## 1. Milestone Objective

Resolve **OD-005** by selecting STARLAB’s canonical StarCraft II runtime boundaries, documenting environment lock posture, and shipping a **typed, deterministic path/config probe** so M02 can build execution harness work without reopening foundational boundary decisions — **without** claiming match execution, replay parsing correctness, or benchmark validity.

> Without M01, the lab would lack a single, auditable contract for the SC2 surface and would risk ad-hoc dependency choices that erode governance and diligence posture.

---

## 2. Scope Definition

### In Scope

- Decision records: `docs/runtime/sc2_runtime_surface.md`, `docs/runtime/environment_lock.md`
- Code: `starlab/sc2/` (`models`, `env_probe`, lazy exports in `__init__.py`, `__main__` for `python -m starlab.sc2`)
- Tests: extended `tests/test_governance.py`; `tests/test_sc2_env_probe.py`
- Ledger and governance: `docs/starlab.md` (33-milestone map, phase names, OD-005 resolved, etc.), `docs/rights_register.md`, `docs/replay_data_provenance.md`, `README.md`, CI job summary label in `.github/workflows/ci.yml`
- Milestone artifacts under `docs/company_secrets/milestones/M01/` (plan, toolcalls, run analysis, summary, audit, optional redacted probe sample)
- **Zero** SC2 Python packages in `pyproject.toml`

### Out of Scope

- Match execution harness, bot orchestration, replay parser implementation, corpus ingestion, benchmarking, learned agents, hosted services, committing SC2 binaries/maps/replays

---

## 3. Work Executed

- **Documentation:** New runtime decision and environment lock docs; rights/provenance updates for Blizzard runtime and AI/ML license posture; ledger expanded to 33 milestones with renamed phases; canonical corpus promotion rule; README and ledger status aligned with PR-pending merge.
- **Code:** New `starlab.sc2` package with deterministic JSON probe; path normalization and env precedence; no SC2 process execution.
- **Tests:** 32 pytest tests; governance assertions for ledger + runtime docs; probe tests for determinism, precedence, partial config, redaction.
- **CI:** PR #2 head runs **24048416111**, **24048498203**, **24048576545** (implementation → closeout → evidence alignment) **success** — same workflow as M00 (Ruff, format, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks). See `docs/starlab.md` §18 for the witnessed table.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local | `ruff check .`, `ruff format --check .`, `mypy starlab tests`, `pytest` — all green at implementation commit; closeout commit is docs-only |
| Probe | `python -W error -m starlab.sc2.env_probe` — exit 0, JSON output |
| CI | Witnessed PR-head runs: [24048416111](https://github.com/m-cahill/starlab/actions/runs/24048416111), [24048498203](https://github.com/m-cahill/starlab/actions/runs/24048498203), [24048576545](https://github.com/m-cahill/starlab/actions/runs/24048576545) — all **success** (see §18 table) |

Post-merge `main` CI not yet recorded (merge pending).

---

## 5. CI / Automation Impact

- **Workflow:** `CI` unchanged in scope; job summary title updated to milestone-neutral **“STARLAB CI summary”** (truthfulness only).
- **Checks:** No removals; no `continue-on-error`; no weakened gates.

---

## 6. Issues & Exceptions

No new issues were introduced during this milestone that block merge from a CI perspective.

---

## 7. Deferred Work

| Item | Deferred to | Notes |
|------|-------------|------|
| Deterministic match execution proof | M02 | Explicit non-goal of M01 |
| `s2protocol` / runtime wiring as dependencies | M02+ | Documented; not added in M01 |
| Replay intake automation | M07+ | OD-003 refinement |

---

## 8. Governance Outcomes

- **OD-005 resolved** with a written decision matrix and explicit boundary (official protocol + `s2protocol`; adapters non-canonical).
- **Environment lock** documented; probe provides deterministic, testable detection of configured paths.
- **Rights/provenance** updated for SC2 client and Blizzard materials without committing assets.
- **Ledger** remains truthful about PR vs merge state (see §18 and README).

---

## 9. Exit Criteria Evaluation

| Criterion (from M01 plan) | Met / Partial / Not | Evidence |
|---------------------------|---------------------|----------|
| OD-005 resolved with decision doc | **Met** | `docs/runtime/sc2_runtime_surface.md`, `docs/starlab.md` §12 |
| Environment lock doc | **Met** | `docs/runtime/environment_lock.md` |
| Deterministic probe/spec in code | **Met** | `starlab/sc2/` + tests |
| Tests for probe + ledger | **Met** | 32 tests; pytest |
| Rights/provenance updates | **Met** | `docs/rights_register.md`, `docs/replay_data_provenance.md` |
| Ledger + README | **Met** | `docs/starlab.md`, `README.md` |
| CI green, gates not weakened | **Met** | Runs `24048416111`, `24048498203`, `24048576545` |
| No SC2 deps in pyproject | **Met** | `pyproject.toml` unchanged for SC2 |
| No execution / replay correctness claims | **Met** | Explicit in docs and ledger |

---

## 10. Final Verdict

**Milestone objectives met** for deliverables on branch `m01-sc2-runtime-surface-env-lock` with multiple green PR-head CI runs recorded in `docs/starlab.md` §18. **Merge to `main`** is the remaining governance step for full repo-wide “closed on main” status; post-merge CI and merge SHA must be recorded in §18. Confirm latest PR tip on [PR #2](https://github.com/m-cahill/starlab/pull/2) before merging.

---

## 11. Authorized Next Step

- **Merge [PR #2](https://github.com/m-cahill/starlab/pull/2)** when human review is complete.
- **Then** begin **M02 — Deterministic Match Execution Harness** on a new branch per milestone workflow.

---

## 12. Canonical References

| Reference | Value |
|-----------|--------|
| Branch | `m01-sc2-runtime-surface-env-lock` |
| PR tip at closeout prep | `88b06db78fa9cb2b71217c03c752232df3a743ba` (confirm on PR #2) |
| Base (`main`) | `725250018bb09ce84e772ded0c7a184cc7d764ea` |
| PR | https://github.com/m-cahill/starlab/pull/2 |
| CI (witnessed) | https://github.com/m-cahill/starlab/actions/runs/24048576545 (latest at prep; see §18 for full set) |
| Ledger | `docs/starlab.md` |
| Plan | `docs/company_secrets/milestones/M01/M01_plan.md` |
| Run analysis | `docs/company_secrets/milestones/M01/M01_run1.md` |

---
