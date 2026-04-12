# 📌 Milestone Summary — M40: Agent Training Program Charter & Artifact Contract

**Project:** STARLAB  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Milestone:** M40 — Agent Training Program Charter & Artifact Contract  
**Timeframe:** 2026-04-11 (implementation) → 2026-04-12 (merge to `main`)  
**Status:** Closed  

---

## 1. Milestone Objective

STARLAB needed a **governed training-program posture** after **M39** so that Phase VI work would be **legible, bounded, and maintainable** before any real training pipelines or weights. Without M40, the repo risked ad hoc training experiments, unclear artifact ownership, and claims that outran evidence.

> Without M40, the project would lack a deterministic **contract surface** tying allowed training lanes (**M41**–**M45**) to upstream milestones (**M26**–**M31**, evaluation chains) and explicit **non-claims**.

---

## 2. Scope Definition

### In Scope

- Roadmap recharter in `docs/starlab.md`: **42 → 46** milestones (**M00**–**M45**); Phase VI as **M40**–**M45** training track; legacy substrate/platform review stubs deferred (§19 **FUT-005**).
- `starlab.training` package: `training_program_models.py`, `training_program_io.py`, `emit_agent_training_program_contract.py`.
- Deterministic artifacts: `agent_training_program_contract.json`, `agent_training_program_contract_report.json` (default under `out/training_program/`).
- `docs/runtime/agent_training_program_contract_v1.md`.
- Tests: `tests/test_m40_agent_training_program_contract.py`; governance updates (M39 complete row, M42–M45 stub folders, arc **46**).
- `README.md`, `docs/architecture.md` alignment.
- Stub milestone docs **M41**–**M45** (`*_plan.md`, `*_toolcalls.md` only).
- **OD-007** repositioned: deferred beyond active arc (no longer “target M41” in the old sense).

### Out of Scope

- Actual model training, weights in repo, live SC2 in CI, benchmark-integrity claims, ladder/live-play claims, self-play/RL implementation, local live-play harness implementation, changes to M20/M23/M25 evaluation semantics.

---

## 3. Work Executed

- **PR #51** merged to `main` (merge commit `44e8edc5bcce8dc99576bf2be542b273095e5072`; final PR head `be47d913737f322bbf8e9e08a672561c71d322eb`).
- **23 files** in initial merge + **1** follow-up style commit on the PR branch (`ruff format` for CI `quality`).
- Ledger, README, architecture, `.gitignore` (`out/training_program/`), company-secrets milestone stubs.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) — success (all required jobs).
- **Superseded:** [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) on `6690cd7` — Ruff format failure — **not** merge authority; fixed before merge.
- **Merge-boundary `main` CI:** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) on merge commit `44e8edc…` — success.
- Local: **701** tests; `ruff check`, `mypy` green before push.

---

## 5. CI / Automation Impact

- No new CI jobs; contract validated via existing **`tests`** lane.
- No gate weakening; `fail_under` unchanged.
- **Signal:** first PR run failed **only** on **`ruff format`** vs local `ruff check` — resolved by formatting `starlab/training` modules.

---

## 6. Issues & Exceptions

- **Superseded red PR-head** [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115): Ruff format — resolved before merge.
- **Node 20** deprecation annotations on actions — informational (pre-existing).

---

## 7. Deferred Work

- **M41**–**M45** product milestones — explicitly stub-only until chartered.
- **Legacy Phase VI stubs** (substrate review; platform boundary charter) — **FUT-005**, beyond **M00**–**M45**.
- **~85%** coverage stretch — unchanged.

---

## 8. Governance Outcomes

- Active arc is **truthfully** **46** milestones with a **written training-program contract** (JSON + report + runtime doc).
- **M39** completion is reflected in governance milestone-table tests.
- **Non-claims** are machine-listed in contract JSON and ledger.

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not | Evidence |
| --- | --- | --- |
| Roadmap recharter **42 → 46** | Met | `docs/starlab.md` §7 |
| Deterministic contract emission | Met | `starlab.training` + tests |
| M41–M45 stubs | Met | `docs/company_secrets/milestones/M41`–`M45` |
| CI green at merge | Met | `24295050784`, `24295326123` |
| No training implementation | Met | Scope |
| No weights / no benchmark-integrity upgrade | Met | Scope |

---

## 10. Final Verdict

Milestone objectives **met**. **M40** is **closed** on `main`. Proceed to **M41** only when chartered on its branch; **M41** remains **stub-only** until then.

---

## 11. Authorized Next Step

**M41** — **Replay-Imitation Training Pipeline v1** — next planned training milestone (**stub** until branch opens).

---

## 12. Canonical References

- [PR #51](https://github.com/m-cahill/starlab/pull/51)
- Final PR head: `be47d913737f322bbf8e9e08a672561c71d322eb`
- Merge commit: `44e8edc5bcce8dc99576bf2be542b273095e5072`
- CI: `24295050784` (PR-head), `24295326123` (merge-boundary `main`)
- Superseded: `24295030115` (not merge authority)
- `docs/starlab.md`, `docs/runtime/agent_training_program_contract_v1.md`, `M40_run1.md`
