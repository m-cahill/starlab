# Milestone Summary — M04: Replay Binding to Run Identity (closed on `main`)

**Project:** STARLAB  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Milestone:** M04 — Replay Binding to Run Identity  
**Timeframe:** 2026-04-07 → **2026-04-07**  
**Status:** **Complete on `main`**

---

## 1. Milestone Objective

Add a **narrow, deterministic, CI-safe replay binding surface** that links a replay file’s **opaque content identity** to existing **M03** records (`run_spec_id`, `execution_id`, `lineage_seed_id`, `proof_artifact_hash` from `run_identity.json`), emitting a reviewable **`replay_binding.json`** — **without** claiming replay parsing, replay semantics, canonical run packaging, or benchmark validity.

---

## 2. Scope Definition

### In Scope

- Runtime contract: `docs/runtime/replay_binding.md`
- Implementation: `starlab/runs/replay_binding.py` (hashing, record build, M03 artifact loaders), `starlab/runs/bind_replay.py` (CLI)
- Synthetic fixture: `tests/fixtures/synthetic_opaque_test.SC2Replay` (opaque bytes; not a Blizzard replay)
- Tests: `tests/test_replay_binding.py`, `tests/test_bind_replay_cli.py`; governance assertions in `tests/test_governance.py`
- PR [#5](https://github.com/m-cahill/starlab/pull/5) merged to `main` with green CI

### Out of Scope

- Replay parser substrate, metadata/timeline/event extraction
- Canonical run artifact v0 (**M05**)
- Benchmark semantics / leaderboard claims
- New live SC2 execution proof in CI (CI remains fixture-driven)

---

## 3. Work Executed

- Defined **`replay_binding.json`** schema (`starlab.replay_binding.v1`), deterministic **`replay_binding_id`** from canonical JSON over M03 IDs + `replay_content_sha256` (filename metadata not in hash).
- Implemented opaque-byte **`replay_content_sha256`**, informational **`replay_reference`** (basename, suffix, size_bytes), fixed **`binding_mode`**: `opaque_content_sha256`, static **`later_milestones`**, empty **`parent_references`**.
- CLI **`python -m starlab.runs.bind_replay`** with `--run-identity`, `--lineage-seed`, `--replay`, `--output-dir`; reads **`proof_artifact_hash` from M03 `run_identity.json`** (does not recompute from raw proof).
- **22** new tests (15 + 7); total pytest count **84** on final PR head.
- Public ledger `docs/starlab.md` updated at closeout (§10, §11, §18, §20, §23, Phase I artifact table, current non-claims block).
- **M05** stubs only: `docs/company_secrets/milestones/M05/M05_plan.md`, `M05_toolcalls.md`.

---

## 4. Validation & Evidence

| Layer | Evidence |
|-------|----------|
| Local | Ruff, Ruff format, Mypy strict, Pytest — green before merge |
| PR-head CI | Run **`24060734950`** — **success** on **`6991978…`** — see `M04_run1.md` |
| Post-merge `main` (merge commit) | Run **`24060997255`** — **success** on merge commit **`c38de5d…`** |
| Post-merge `main` (closeout doc push) | Run **`24061285459`** — **success** on **`c099752…`** (ledger / milestone artifacts; **not** merge-boundary) |

---

## 5. CI / Automation Impact

- No new workflows; existing **CI** workflow unchanged.
- No `continue-on-error` or weakened gates.

---

## 6. Issues & Exceptions

No new issues were introduced during this milestone that block closeout.

---

## 7. Deferred Work

- **Canonical run artifact v0** — **M05**
- **Replay parser substrate** — **M08** (Phase II)
- **Replay semantic equivalence** replay ↔ execution proof — not claimed

---

## 8. Governance Outcomes

**Proved on `main` (narrow, M04):**

- Deterministic **`replay_content_sha256`** for opaque replay bytes and deterministic **`replay_binding_id`** linking to M03 identity fields, with stable **`replay_binding.json`** emission (fixtures in CI).

**Explicitly not proved:**

- Replay parser correctness, replay↔proof semantic equivalence, replay event extraction, canonical run artifact v0, benchmark integrity, cross-host reproducibility, new live SC2 execution in CI.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
|-----------|-----|
| Contract doc + implementation + tests + CLI | **Met** |
| Deterministic outputs across repeated runs | **Met** |
| CI green (PR-head + post-merge `main`) | **Met** |
| Ledger updated | **Met** |
| M05 stub-only after closeout | **Met** |

---

## 10. Final Verdict

**M04 is closed on `main`.** Safe to proceed to **M05** planning only until authorized.

---

## 11. Authorized Next Step

**M05 — Canonical Run Artifact v0** — stub only until a new plan is approved; **no** M05 product implementation without explicit milestone authorization.

---

## 12. Canonical References

| Reference | Value |
|-----------|-------|
| PR | https://github.com/m-cahill/starlab/pull/5 |
| Final PR head | `6991978cb35172edda75f721149b1558d7ead226` |
| Authoritative PR-head CI | https://github.com/m-cahill/starlab/actions/runs/24060734950 |
| Merge commit | `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` |
| Merged at (UTC) | 2026-04-07T02:17:04Z |
| Post-merge `main` CI (merge) | https://github.com/m-cahill/starlab/actions/runs/24060997255 |
| Post-merge `main` CI (closeout docs) | https://github.com/m-cahill/starlab/actions/runs/24061285459 |
| Contract | `docs/runtime/replay_binding.md` |
| Run analysis | `M04_run1.md` |
| Public ledger | `docs/starlab.md` |
