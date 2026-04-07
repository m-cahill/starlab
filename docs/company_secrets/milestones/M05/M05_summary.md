# Milestone Summary — M05: Canonical Run Artifact v0

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M05 — Canonical Run Artifact v0  
**Timeframe:** 2026-04-07 → **2026-04-07**  
**Status:** **Closed on `main`**

---

## 1. Milestone Objective

Establish the first **canonical STARLAB run package boundary** by deterministically packaging existing **M03** + **M04** JSON records into a **content-addressed directory bundle** (`manifest.json`, `hashes.json`, canonical JSON re-emission), **without** claiming replay parsing, benchmark integrity, or raw replay/proof shipping.

---

## 2. Scope Definition

### In Scope

- Runtime contract: `docs/runtime/canonical_run_artifact_v0.md`
- Implementation: `starlab/runs/canonical_run_artifact.py`, `starlab/runs/build_canonical_run_artifact.py`, `load_replay_binding` in `starlab/runs/replay_binding.py`
- **M03 portability:** `starlab/runs/seed_from_proof.py` — repo-relative POSIX paths for `input_references[].path`; canonical JSON `content_sha256` for JSON fixtures (cross-OS CI stability)
- Tests: `tests/test_canonical_run_artifact.py`, `tests/test_build_canonical_run_artifact_cli.py`, golden `tests/fixtures/m05_expected/`, governance updates
- PR [#6](https://github.com/m-cahill/starlab/pull/6) merged to `main` with green CI

### Out of Scope

- Replay parser substrate (M08+), replay event extraction, **benchmark** semantics
- Raw replay bytes, raw proof JSON, raw match config **inside** the M05 bundle
- New live SC2 execution in CI
- M06 implementation

---

## 3. Work Executed

- Deterministic **directory bundle** writer (no archive format); fail if `--output-dir` exists; **included_artifacts** list guardrail (order-sensitive)
- CLI **`python -m starlab.runs.build_canonical_run_artifact`** (M03/M04 JSON inputs only)
- **`load_replay_binding`** validation (schema + recomputed `replay_binding_id`)
- Golden snapshot test for `manifest.json` / `hashes.json` after fixture portability fixes
- Public ledger + milestone plan/toolcalls updates

---

## 4. Validation & Evidence

| Layer | Evidence |
| ----- | -------- |
| PR-head CI | Run **`24062592376`** — **success** on `53ace08…` — merge gate |
| Post-merge `main` | Run **`24062610358`** — **success** on merge commit `bad27db…` |
| Post-closeout `main` (non–merge-boundary) | Run **`24062664914`** — **success** on `6edeb8a…` (ledger / M06 stubs) |
| Local | Ruff, pytest, mypy (before push) |

---

## 5. CI / Automation Impact

- **No** workflow weakening; **no** required check removed or `continue-on-error` on merge gates.

---

## 6. Issues & Exceptions

- **Superseded red PR-head runs** due to fixture path/CRLF drift — **resolved** on final tip (`53ace08…`); **not** a merge-boundary event.

---

## 7. Deferred Work

- **Replay parser / provenance** tightening — M07+ / M08+
- **Benchmark** contracts — later phases
- **M06** — environment drift & smoke matrix (stub only after closeout)

---

## 8. Governance Outcomes

**Proved on `main` (narrow, M05):**

- Deterministic **canonical run artifact v0** packaging of STARLAB-owned M03/M04 JSON with `run_artifact_id` and explicit **non-inclusion** of raw replay/proof/config in the bundle.

**Explicitly not proved:**

- Replay parser correctness, **replay↔proof semantic equivalence**, replay event extraction, benchmark integrity, cross-host reproducibility, new live SC2 execution in CI.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Contract + implementation + tests + CLI | **Met** |
| Deterministic outputs / golden stability | **Met** (after cross-OS portability fixes) |
| CI green (PR-head + post-merge `main`) | **Met** |
| Ledger updated | **Met** |
| M06 stub-only after closeout | **Met** |

---

## 10. Final Verdict

**M05 is closed on `main`.** Safe to proceed to **M06** planning only (no M06 implementation without explicit authorization).

---

## 11. Authorized Next Step

**M06 — Environment Drift & Runtime Smoke Matrix** — stub milestone files only until kickoff.

---

## 12. Canonical References

| Reference | Value |
| --------- | ----- |
| PR | https://github.com/m-cahill/starlab/pull/6 |
| Final PR head | `53ace08e2ec9d29c780f31593bd945e82e1dfcac` |
| Authoritative PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24062592376 |
| Merge commit | `bad27db36c135fd772e38dcafa64d6fa59577db0` |
| Merged at (UTC) | 2026-04-07T03:20:10Z |
| Merge method | **merge commit** |
| Post-merge `main` CI (merge boundary) | https://github.com/m-cahill/starlab/actions/runs/24062610358 |
| Post-closeout `main` CI (docs/governance push; not merge boundary) | https://github.com/m-cahill/starlab/actions/runs/24062664914 |
| Contract | `docs/runtime/canonical_run_artifact_v0.md` |
| Public ledger | `docs/starlab.md` |
