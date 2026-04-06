# 📌 Milestone Summary — M02: Deterministic Match Execution Harness

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M02 — Deterministic Match Execution Harness  
**Timeframe:** 2026-04-06 → **Open** (implementation + pre-merge validation on branch; **not** closed on `main` at this document revision)  
**Status:** **Open** — PR [#3](https://github.com/m-cahill/starlab/pull/3) open; PR-head CI green; **local burny session recorded** — **two successful runs + `artifact_hash` pair not achieved** (map file missing on disk; see `M02_local_execution_note.md`)

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
- Opened **PR #3**; pushed branch `m02-deterministic-match-execution-harness`.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local (2026-04-06) | `ruff check .`, `ruff format --check .`, `mypy starlab tests`, `pytest` — all exit 0; `python -m starlab.sc2.run_match --help` exit 0. |
| PR-head CI | Run `24053526611` — **success** on head `061c2126cc59b3ce4d662c58240216343c21f71a` — see `M02_run1.md`. |
| Local burny (2026-04-06) | **`pip install -e ".[sc2-harness]"`** exit 0; **`python -m starlab.sc2 --redact`**: install/binary detected; **no** `Maps` dir at probe path; **two** `run_match` attempts with committed `m02_local_config.json` — **both failed** (map path not found); **no** `artifact_hash` — see `M02_local_execution_note.md`, `M02_determinism_check.md`. |
| **Missing for narrow harness proof** | Two **successful** local **burnysc2** runs emitting `match_execution_proof.json` and a **hash comparison** (match or honest mismatch) — **not** satisfied until a valid `.SC2Map` is available at the configured path (or config updated). |

---

## 5. CI / Automation Impact

- Workflow unchanged: still single `governance` job; no `continue-on-error` weakening.
- CI installs **`[dev]` only** — SC2 / `burnysc2` not required in CI.

---

## 6. Issues & Exceptions

- **Node.js 20 deprecation annotation** on GitHub Actions (informational; not a failing check).
- No new failing checks introduced.

---

## 7. Deferred Work

| Item | Target | Notes |
|------|--------|------|
| Local burny ×2 + determinism documentation | M02 closeout | Required before ledger marks “controlled deterministic match execution” as proved |
| Post-merge `main` CI row | §18 at merge | Not yet recorded (PR not merged) |

---

## 8. Governance Outcomes

- M01 boundary preserved; wrappers isolated under `starlab/sc2/adapters/`.
- Proof artifact schema v1 and hashing rules are STARLAB-owned and documented.
- Non-claims remain explicit in `docs/runtime/match_execution_harness.md` and ledger.

---

## 9. Exit Criteria Evaluation

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Harness + fake path + tests + docs | **Met** | Code + PR #3 + green PR-head CI |
| Optional real adapter behind extra | **Met** | `sc2-harness` / `burnysc2_adapter.py` |
| CI green without SC2 | **Met** | Run `24053526611` |
| Local real execution + determinism check | **Not met** | Evidence files record **blocked** session — no proof hashes |
| Merge to `main` | **Pending** | PR open |

---

## 10. Final Verdict

**Milestone implementation is in place and PR-head CI is green.** **Local evidence files are no longer empty templates** — they document a **real** burny attempt on Windows where **both runs failed before proof write** (missing map). M02 is **not** closeable as a **proof** milestone for the **narrow same-machine deterministic harness** claim until **two successful** runs yield comparable `artifact_hash` values (or a documented honest mismatch). Merge and post-merge `main` CI are still **pending** for formal ledger closeout.

---

## 11. Authorized Next Step

- Merge **PR #3** when human review is complete (CI already green at recorded tip).
- Run local burny evidence; then perform **formal closeout** (ledger §7/§18/§23, tag, M03 planning) per project workflow — **not** started here.

---

## 12. Canonical References

| Reference | Value |
|-----------|--------|
| Branch | `m02-deterministic-match-execution-harness` |
| PR | https://github.com/m-cahill/starlab/pull/3 |
| PR head (at CI) | `061c2126cc59b3ce4d662c58240216343c21f71a` |
| PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24053526611 |
| Plan | `docs/company_secrets/milestones/M02/M02_plan.md` |
| Run analysis | `M02_run1.md` |
