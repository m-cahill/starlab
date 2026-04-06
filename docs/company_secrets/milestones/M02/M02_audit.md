# Milestone Audit — M02: Deterministic Match Execution Harness

**Audit mode:** DELTA AUDIT  
**Milestone ID:** M02  
**Current SHA (PR head):** `5ec0ccb17c15f6b549da12719369ce1478e31212`  
**Diff range (informative):** `main...5ec0ccb17c15f6b549da12719369ce1478e31212` (merge base not re-resolved in this document)  
**Authoritative CI:** [CI run 24054529734](https://github.com/m-cahill/starlab/actions/runs/24054529734) — **success** (PR event, head SHA above)  
**Date:** 2026-04-06

---

## Executive summary

M02 adds a **bounded match harness**, a **deterministic proof artifact**, and **adapter isolation** (fake + BurnySc2). **PR-head CI is green** and **no CI weakening** was observed. **HIGH (still):** A **2026-04-06** local **burnysc2** session is **documented** in `M02_local_execution_note.md` / `M02_determinism_check.md`, but **both** harness attempts **failed** before writing `match_execution_proof.json` (configured map path missing on disk). The **narrow** same-machine deterministic harness claim is **not** substantiated — **no** `artifact_hash` pair. **No blocking code defects** identified from CI signal for the merged-intent delta.

---

## 1. Regression / risk scan (delta)

| Area | Finding | Severity |
|------|---------|----------|
| Dependency hygiene | Optional `burnysc2` not in default/CI install | OK — intentional |
| Adapter leakage | STARLAB models avoid `sc2` types on public surfaces | OK |
| CI truthfulness | Same gates as prior milestones; all passed | OK |
| Local evidence | Burny×2 **successful** runs + hash comparison **not** achieved (blocked: no map file) | **HIGH (governance)** — blocks honest “proved” claim; evidence files now record attempt |

---

## 2. Material improvements

- Executable proof path for future run identity / lineage work.
- Normalized artifact hashing decouples claims from raw upstream bytes.
- Fake adapter enables fast, SC2-free regression testing.

---

## 3. Minimal guardrails before M03

| Guardrail | Status |
|-----------|--------|
| Ledger must not mark “controlled deterministic match execution” **proved** without local evidence | **Enforce at closeout** |
| Keep `sc2-harness` optional | **Holds** |
| Do not expand CI to require SC2 | **Holds** |

---

## 4. CI / test / lint (record)

- **Lint/format/types:** Ruff + Mypy — pass (run `24054529734`).
- **Tests:** Pytest — pass; covers fake path, not live SC2.
- **Supply chain:** pip-audit, SBOM, Gitleaks — pass.

**Coverage:** No line-coverage gate in repo; acceptable for M02 scope.

---

## 5. Dependency delta

- **Default / CI:** unchanged transitive surface for core workflow (still `[dev]` only).
- **Optional:** `burnysc2` declared under `[project.optional-dependencies] sc2-harness` — must remain optional.

---

## 6. Verdict

**AUDIT RESULT:** ✅ **Approve merge from engineering/CI perspective** for PR #3 at SHA `5ec0ccb…`, conditioned on **maintaining honest ledger wording** until the **narrow** harness proof criteria are met (or honestly documented as not met).

**Do not** certify M02 **milestone closeout** until:

1. Merge + post-merge `main` CI (project convention), and  
2. **Successful** local real-execution + determinism record per M02 plan (two proof-producing runs, or honest mismatch between hashes).

**Deferred (explicit):** Replay binding, canonical run artifact, benchmarks — unchanged.

---

## 7. Sign-off note

This audit is **governance-facing**. It does **not** replace human review of PR #3 or local SC2 validation.
