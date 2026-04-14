# 📌 Milestone Summary — M48: Learned-agent comparison contract-path alignment

**Project:** STARLAB  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Milestone:** M48 — Learned-agent comparison contract-path alignment  
**Timeframe:** 2026-04-13 (plan / recharter context) → 2026-04-14 (merge + closeout)  
**Status:** Closed on `main`

---

## 1. Milestone Objective

**M42** compared **M27** and **M41** candidates using a shared **M28** metric surface, but the word “contract” overloaded the **M20 benchmark contract** (on-disk JSON) and the **M40 training-program charter** (often built in-process). **M41** runs record `training_program_contract_sha256` / `training_program_contract_version`, while **M42** did not offer a clear, auditable way to align comparison-time M40 identity with each candidate’s recorded identity.

Without this milestone, operators could not **prove** which benchmark contract and which training-program charter were active at comparison time, or **fail closed** when those identities disagreed with **M41** metadata.

---

## 2. Scope Definition

### In Scope

- **CLI:** `emit_learned_agent_comparison` — **`--benchmark-contract`**, **`--contract`** alias, **`--training-program-contract`**.
- **Harness:** `learned_agent_comparison_harness` — `benchmark_contract_path` parameter; strict M41 vs active M40 identity check.
- **I/O:** `training_program_io` — load M40 JSON from disk; verify embedded digest vs body hash.
- **Docs:** `docs/runtime/learned_agent_comparison_harness_v1.md`, cross-links in M40/M20 runtime docs; `docs/starlab.md` governance lines.
- **Tests:** `tests/test_m42_learned_agent_comparison.py`, governance tests as needed.

### Out of Scope

- Benchmark math, new M28 metrics, ranking policy changes.
- Training algorithm or **M41** pipeline semantics beyond contract identity alignment.
- Live SC2, `out/` commits, operator campaigns.
- **M49** product work (stub only after closeout).

---

## 3. Work Executed

- Implemented explicit **M20** benchmark path and optional **M40** on-disk load; preserved default in-process M40 generation.
- Added **strict** comparison of active M40 `contract_sha256` / `program_version` to each **M41** candidate’s recorded fields when `--m41` is used.
- Extended unit tests for CLI paths, disk load, match, and mismatch (`ValueError`).
- Updated runtime and ledger documentation for two-contract clarity.

---

## 4. Validation & Evidence

- **CI:** Authoritative PR-head [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299) on `d94bc02…` — **success** (full test matrix + governance aggregate).
- **Merge-boundary:** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on merge commit `cdd023c…` — **success**.
- **Local:** Full `pytest` suite green on implementation branch before merge (749 tests).

---

## 5. CI / Automation Impact

No workflow file changes. Existing **CI** jobs exercised changed Python modules and governance tests. No enforcement weakening.

---

## 6. Issues & Exceptions

No new issues were introduced during this milestone.

---

## 7. Deferred Work

- Broader **M42** ergonomics or comparison UX beyond contract-path alignment — **not** started; track only if a future milestone authorizes it.
- **M49** — placeholder stub only (see `M49_plan.md`).

---

## 8. Governance Outcomes

- **Ambiguity removed:** “Benchmark contract” vs “training-program charter” are distinct flags and documented surfaces.
- **Auditability:** M41 candidate runs are **rejected** on clear charter identity mismatch when compared under strict policy.
- **Backward compatibility:** `--contract` retained as alias for `--benchmark-contract` where both agree.

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not met | Evidence |
| --------- | ------------------------ | -------- |
| Explicit M20 benchmark path | Met | `--benchmark-contract` + help text |
| Optional M40 disk path | Met | `--training-program-contract` + loader |
| M41 identity alignment | Met | Strict `ValueError` in harness |
| Docs + tests | Met | Runtime + governance + `test_m42_*` |
| No scope creep | Met | No benchmark/training semantics expansion |

---

## 10. Final Verdict

Milestone objectives met. Safe to record M48 closed on `main` and proceed with **M49** as stub-only current milestone until rechartered.

---

## 11. Authorized Next Step

**M49** — stub placeholder in `docs/company_secrets/milestones/M49/` — **no** implementation authorized by this milestone.

---

## 12. Canonical References

- Merge commit: `cdd023cb388ae99c3649978857e07af04c17df50`
- PR: [#59](https://github.com/m-cahill/starlab/pull/59)
- Final PR head: `d94bc02c78bf75605edc4d28473f48cac986e53c`
- PR-head CI: [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299)
- Merge-boundary CI: [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946)
- Tag: `v0.0.48-m48` on `cdd023c…`
- Artifacts: `M48_plan.md`, `M48_toolcalls.md`, `M48_run1.md`, `M48_summary.md`, `M48_audit.md`
