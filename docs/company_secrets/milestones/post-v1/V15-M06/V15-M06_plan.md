# V15-M06 Plan — Human Panel Benchmark Protocol

**Project:** STARLAB  
**Phase:** v1.5 / V15  
**Milestone:** `V15-M06`  
**Title:** Human Panel Benchmark Protocol  
**Status:** Approved for implementation (2026-04-25); branch `v15-m06-human-panel-benchmark-protocol`  
**Location:** `docs/company_secrets/...` may be local-only; do not require commit.

## 0. Milestone intent

Freeze the **Human Panel Benchmark Protocol** contract: participant tiers, consent/privacy posture, session/match rules, threshold vocabulary, evidence requirements, claim boundary, and non-claims. **No** human execution, no real participant rows in public registers, no “beats most humans” **claim** **authorization**.

## 1. Artifacts (implemented)

- **Contract id:** `starlab.v15.human_panel_benchmark.v1`  
- **Protocol profile id:** `starlab.v15.human_panel_benchmark_protocol.v1`  
- **Files:** `v15_human_panel_benchmark.json`, `v15_human_panel_benchmark_report.json`  
- **Code:** `starlab/v15/human_panel_benchmark_models.py`, `human_panel_benchmark_io.py`, `emit_v15_human_panel_benchmark.py`  
- **Doc:** `docs/runtime/v15_human_panel_benchmark_protocol_v1.md`  
- **Tests:** `tests/test_m06_v15_human_panel_benchmark.py`, `tests/test_governance_ci.py`

## 2. Out of scope

Human-panel execution, recruitment, real identities, GPU training, long GPU, SC2, XAI review, v2, PX2-M04/M05 opening, public register data rows, **M11** (execution) work.

## 3. Next

**Closeout** after green PR and merge: update CI run IDs, merge SHA, set M06 **closed** in public docs, stub **V15-M07** per standard prompts. **V15-M07** — Training Smoke and Short GPU Shakedown — **not** started until explicit plan approval.

---

_Full operational checklist, CLI flags, and acceptance criteria: see milestone implementation PR and `docs/starlab-v1.5.md` (M06 non-claims, artifact §6, §11 pip note)._
