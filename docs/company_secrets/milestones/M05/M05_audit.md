# Milestone Audit — M05: Canonical Run Artifact v0 (closed on `main`)

**Audit mode:** DELTA AUDIT (post-merge)  
**Milestone ID:** M05  
**Branch:** `m05-canonical-run-artifact-v0` (**merged**; remote **deleted**)  
**PR:** [#6](https://github.com/m-cahill/starlab/pull/6) — **merged**  
**Final PR head:** `53ace08e2ec9d29c780f31593bd945e82e1dfcac` — PR-head CI [24062592376](https://github.com/m-cahill/starlab/actions/runs/24062592376) — **success**  
**Merge commit:** `bad27db36c135fd772e38dcafa64d6fa59577db0` — merged **2026-04-07T03:20:10Z** — post-merge `main` CI [24062610358](https://github.com/m-cahill/starlab/actions/runs/24062610358) — **success**  
**Post-closeout `main` (ledger / M06 stubs; not merge boundary):** `6edeb8af845d9cbfaed5c329c1c9a3398acac9dd` — CI [24062664914](https://github.com/m-cahill/starlab/actions/runs/24062664914) — **success**  
**Further doc-only `main` (§18/§23 CI cross-reference; not merge boundary):** `ebca1e964c0539c78165bfab72c249a2157402cc` — CI [24062700534](https://github.com/m-cahill/starlab/actions/runs/24062700534) — **success**  
**Date:** 2026-04-07

---

## 1. Header

- **Milestone:** M05 — Canonical Run Artifact v0  
- **Mode:** DELTA AUDIT  
- **Range:** `main` @ prior tip … `bad27db36c135fd772e38dcafa64d6fa59577db0` (merge of PR #6); closeout docs on `6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`  
- **CI Status:** Green (PR-head + post-merge `main` on merge commit; additional green run on post-closeout push — **not** merge authority)  
- **Audit Verdict:** **Green** — M05 remained **below** replay parser substrate, benchmark certification, and raw-asset shipping; **no** CI guardrail weakening observed.

---

## 2. Executive Summary (Delta-Focused)

**Improvements**

- First **canonical run package boundary** (`manifest.json`, `hashes.json`, `run_artifact_id`) over **STARLAB-owned JSON only**.
- Explicit **non-claims** in contract + ledger; **no** raw replay/proof/config in bundle.
- **M03** `seed_from_proof` hardened for **cross-OS CI**: repo-relative POSIX paths + canonical JSON digests for fixture `input_references` (reduces path/CRLF drift).

**Risks (managed / explicit)**

- **Semantic gap:** packaging does **not** prove replay bytes are “the” replay of the execution — **out of scope** (same class of honesty as M04).
- **Superseded failed PR-head runs** before portability fixes — **documented**; **not** merge authority.

**Single most important next action:** execute **M06** under its own plan — **no** parser/benchmark scope creep.

---

## 3. Claim Discipline

| Claim | Supported? |
| ----- | ---------- |
| Deterministic canonical bundle + `run_artifact_id` | **Yes** — tests + golden + CI |
| Replay parser / replay semantics | **No** — correctly deferred |
| Benchmark integrity | **No** — correctly deferred |
| Raw replay/proof in bundle | **No** — correctly excluded |

---

## 4. CI Truthfulness

- Required jobs unchanged; **no** `continue-on-error` on merge gates.
- **Pytest** failure on early PR tips **fixed** before merge — truth signal restored.
- Post-closeout push (`6edeb8a…`, run `24062664914`) re-validated the pipeline after ledger/milestone-only changes — **supplementary**, not a substitute for merge-commit CI.

---

## 5. Contract / Boundary Discipline

- `docs/runtime/canonical_run_artifact_v0.md` matches implementation.
- CLI accepts **only** M03/M04 JSON paths + `--output-dir` (no replay/proof paths).
- `included_artifacts` fixed list — **shape drift** rejected.

---

## 6. Follow-up Items (Deferred to M06+)

| ID | Item | Target |
| -- | ---- | ------ |
| NEXT-001 | Environment drift & smoke matrix | **M06** |
| NEXT-002 | Replay intake / provenance tightening | **M07** |
| NEXT-003 | Parser substrate | **M08** |

---

## 7. Score Trend

| Milestone | Arch | Mod | Health | CI | Sec | Perf | DX | Docs | Overall |
| --------- | ---- | --- | ------ | -- | --- | ---- | -- | ---- | ------- |
| M05 | 3.5 | 3.5 | + | + | + | + | + | + | 4.5 |

---

## Machine-readable appendix

```json
{
  "milestone": "M05",
  "mode": "DELTA_AUDIT_POST_MERGE",
  "pr": 6,
  "final_pr_head": "53ace08e2ec9d29c780f31593bd945e82e1dfcac",
  "authoritative_pr_head_ci": "24062592376",
  "merge_commit": "bad27db36c135fd772e38dcafa64d6fa59577db0",
  "post_merge_main_ci": "24062610358",
  "post_closeout_main_ci_non_merge_boundary": "24062664914",
  "further_doc_only_main_ci_non_merge_boundary": "24062700534",
  "verdict": "green_closed_on_main",
  "merged_to_main": true,
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "workflows": "unchanged",
    "contracts": "documented"
  },
  "issues": []
}
```
