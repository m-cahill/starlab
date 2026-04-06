# Milestone Audit — M02: Deterministic Match Execution Harness

**Audit mode:** DELTA AUDIT  
**Milestone ID:** M02  
**Current SHA (PR head):** `290304a3ad3986029879c183f4e40159e7f5792c`  
**Diff range (informative):** `main...290304a3ad3986029879c183f4e40159e7f5792c` (merge base not re-resolved in this document)  
**Authoritative CI:** [CI run 24054732181](https://github.com/m-cahill/starlab/actions/runs/24054732181) — **success** (PR event, head SHA above)  
**Date:** 2026-04-06

---

## Executive summary

M02 adds a **bounded match harness**, a **deterministic proof artifact**, and **adapter isolation** (fake + BurnySc2). **PR-head CI is green** and **no CI weakening** was observed. A **2026-04-06 recovery** local **burnysc2** session is **documented** in `M02_local_execution_note.md` / `M02_determinism_check.md`: **two successful** runs wrote `match_execution_proof.json` with **matching** normalized `artifact_hash` (narrow same-machine harness; **not** cross-host). Earlier blocked session (missing install map) is **superseded** for evidence by this recovery. **No blocking code defects** identified from CI signal for the merged-intent delta.

---

## 1. Regression / risk scan (delta)

| Area | Finding | Severity |
|------|---------|----------|
| Dependency hygiene | Optional `burnysc2` not in default/CI install | OK — intentional |
| Adapter leakage | STARLAB models avoid `sc2` types on public surfaces | OK |
| CI truthfulness | Same gates as prior milestones; all passed | OK |
| Local evidence | Burny×2 **successful** runs + **matching** hashes **recorded** (recovery session; pysc2 mini-game map + absolute-path fix) | **OK for narrow harness evidence** — formal §10 “proved” rows still await merge/closeout on `main` |

---

## 2. Material improvements

- Executable proof path for future run identity / lineage work.
- Normalized artifact hashing decouples claims from raw upstream bytes.
- Fake adapter enables fast, SC2-free regression testing.

---

## 3. Minimal guardrails before M03

| Guardrail | Status |
|-----------|--------|
| Ledger must not mark “controlled deterministic match execution” **proved** without local evidence + **main** closeout | **Enforce at closeout** — local hash pair now exists; merge still pending |
| Keep `sc2-harness` optional | **Holds** |
| Do not expand CI to require SC2 | **Holds** |

---

## 4. CI / test / lint (record)

- **Lint/format/types:** Ruff + Mypy — pass (run `24054732181`).
- **Tests:** Pytest — pass; covers fake path, not live SC2.
- **Supply chain:** pip-audit, SBOM, Gitleaks — pass.

**Coverage:** No line-coverage gate in repo; acceptable for M02 scope.

---

## 5. Dependency delta

- **Default / CI:** unchanged transitive surface for core workflow (still `[dev]` only).
- **Optional:** `burnysc2` declared under `[project.optional-dependencies] sc2-harness` — must remain optional.

---

## 6. Verdict

**AUDIT RESULT:** ✅ **Approve merge from engineering/CI perspective** for PR #3 at SHA `290304a…`, conditioned on **maintaining honest ledger wording** until the **narrow** harness proof criteria are met (or honestly documented as not met).

**Do not** certify M02 **milestone closeout** until:

1. Merge + post-merge `main` CI (project convention), and  
2. **Successful** local real-execution + determinism record per M02 plan (two proof-producing runs, or honest mismatch between hashes).

**Deferred (explicit):** Replay binding, canonical run artifact, benchmarks — unchanged.

---

## 7. Sign-off note

This audit is **governance-facing**. It does **not** replace human review of PR #3 or local SC2 validation.
