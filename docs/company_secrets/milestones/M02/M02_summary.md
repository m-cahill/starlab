# 📌 Milestone Summary — M02: Deterministic Match Execution Harness

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M02 — Deterministic Match Execution Harness  
**Timeframe:** 2026-04-06 → **2026-04-06** (closed on `main` at merge + ledger closeout)  
**Status:** **Closed** on `main` — [PR #3](https://github.com/m-cahill/starlab/pull/3) merged **2026-04-06** (`2026-04-06T23:35:21Z`); authoritative PR-head CI on final tip `e88ca20424410cd99f834eeec92a5ec5d8034284` — run [`24055678613`](https://github.com/m-cahill/starlab/actions/runs/24055678613); post-merge `main` CI on merge commit — run [`24056523452`](https://github.com/m-cahill/starlab/actions/runs/24056523452). **Local evidence:** two successful `burnysc2` runs, **matching** normalized `artifact_hash` — **narrow same-machine harness only** (see `M02_determinism_check.md`).

---

## 1. Milestone Objective

Prove that STARLAB can run a **bounded, seeded** StarCraft II match slice under the M01 runtime boundary and emit a **STARLAB-owned deterministic execution proof artifact**, without claiming replay binding, canonical run artifacts, benchmark validity, or cross-host reproducibility.

Without M02, the project would have **no** governed execution harness or normalized proof artifact path beyond M01’s environment probe.

---

## 2. Scope Definition

### In Scope

- Runtime doc: `docs/runtime/match_execution_harness.md`
- Harness modules: `match_config`, `maps`, `artifacts`, `harness`, `run_match` CLI
- Adapters: **fake** (CI), **burnysc2** (optional extra `sc2-harness`)
- Tests: config, artifacts, fake harness, maps, governance alignment
- Ledger/README/environment_lock alignment for M02
- Milestone artifacts under `docs/company_secrets/milestones/M02/` (plan, toolcalls, run analysis, this summary, audit)

### Out of Scope

- Replay parsing / binding (M04+)
- Canonical run artifact v0 (M05)
- Benchmarks / tournament infrastructure
- Multi-client orchestration
- Cross-install or cross-host reproducibility certification
- Committing Blizzard binaries, maps, or replays

---

## 3. Work Executed

- Implemented JSON `MatchConfig`, map resolution helpers, `ExecutionProofRecord` + SHA-256 normalization, `run_match_execution`, BurnySc2 adapter (lazy SC2 imports), fake adapter.
- Added optional `pyproject.toml` extra `sc2-harness` (`burnysc2`).
- Extended governance tests for `match_execution_harness.md`.
- **Merged** **PR #3** to `main` (merge commit `53a24a4a6106168afe79e0a70d51a20bfef4ea18`); remote feature branch **deleted** after merge.
- **Local evidence (2026-04-06 recovery):** pysc2 `MoveToBeacon.SC2Map` in gitignored `_local_maps/`; explicit map paths resolved to **absolute** paths before CreateGame; two successful `run_match` invocations with matching `artifact_hash`.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local dev | `ruff`, `ruff format`, `mypy`, `pytest` — exit 0 on recorded runs. |
| PR-head CI | Run **`24055678613`** — **success** on head **`e88ca20424410cd99f834eeec92a5ec5d8034284`** — see `M02_run1.md`. |
| Post-merge `main` CI | Run **`24056523452`** — **success** on merge commit **`53a24a4a6106168afe79e0a70d51a20bfef4ea18`**. |
| Local burny | Two `run_match` runs — **exit 0**; **matching** `artifact_hash` `b23172cb457b7645d796c30cf36baf96229efa3af954190788370ba5ea464e53` — see `M02_local_execution_note.md`, `M02_determinism_check.md`, `M02_execution_proof_redacted.json`. |

---

## 5. CI / Automation Impact

- Workflow unchanged: single `governance` job; no `continue-on-error` weakening.
- CI installs **`[dev]` only** — SC2 / `burnysc2` not required in CI.

---

## 6. Issues & Exceptions

- **Node.js 20 deprecation annotation** on GitHub Actions (informational; not a failing check).
- No new failing checks introduced.

---

## 7. Deferred Work

| Item | Target | Notes |
|------|--------|------|
| Run identity / lineage | M03 | Next milestone (stubs only at M02 closeout) |
| Replay binding | M04+ | Explicitly out of M02 |

---

## 8. Governance Outcomes

- M01 boundary preserved; wrappers isolated under `starlab/sc2/adapters/`.
- Proof artifact schema v1 and hashing rules are STARLAB-owned and documented.
- **Narrow** claim: **controlled deterministic match execution** is **proved** only in the **same-machine, same-config, normalized hash** sense evidenced in M02 files — **not** cross-host or replay-bound.

---

## 9. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Harness + fake path + tests + docs | **Met** | Merged to `main` |
| Optional real adapter behind extra | **Met** | `sc2-harness` / `burnysc2_adapter.py` |
| CI green without SC2 | **Met** | PR-head + post-merge runs above |
| Local real execution + determinism check | **Met** | Two successful runs + matching hash (recorded host) |
| Merge to `main` | **Met** | PR #3 merged **2026-04-06** |

---

## 10. Final Verdict

**Milestone objectives met.** M02 is **closed** on `main` with merge commit `53a24a4a6106168afe79e0a70d51a20bfef4ea18`, green PR-head and post-merge CI, and **honest local evidence** for the **narrow** harness hash claim. **Do not** widen the claim to replay correctness, canonical run artifacts, benchmarks, or portability without new milestones and evidence.

---

## 11. Authorized Next Step

- **M03 — Run Identity & Lineage Seed** — planning and implementation **only** when authorized; stubs at `docs/company_secrets/milestones/M03/`.

---

## 12. Canonical References

| Reference | Value |
|-----------|--------|
| Final PR head | `e88ca20424410cd99f834eeec92a5ec5d8034284` |
| PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24055678613 |
| Merge commit | `53a24a4a6106168afe79e0a70d51a20bfef4ea18` |
| Post-merge `main` CI | https://github.com/m-cahill/starlab/actions/runs/24056523452 |
| PR | https://github.com/m-cahill/starlab/pull/3 |
| Plan | `docs/company_secrets/milestones/M02/M02_plan.md` |
| Run analysis | `M02_run1.md` |
