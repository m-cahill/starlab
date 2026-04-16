# v2 readiness — audit hardening v1 (M60)

**Status:** **Closed** on `main` (2026-04-16). [PR #71](https://github.com/m-cahill/starlab/pull/71). Merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`. Tag **`v0.0.60-m60`**.

**Milestone:** M60 — Audit hardening & v2 readiness v1  
**Phase:** VII  
**Runtime role:** Diligence and structural-boundary note for the M60 milestone (not a product artifact contract).

## Target scope

- **In scope:** One **current-main** structural hotspot relevant to **v2 readiness** (cleaner module boundaries before **M61** release lock), implemented in a **behavior-preserving** way with **tests** and a **short** audit mapping (`docs/audit/m60_v2_readiness_findings.md`).
- **Out of scope:** New research claims, new benchmark/equivalence/ladder performance claims, new artifact families, service-layer rewrites, multi-environment expansion, deployment work, or repo-wide refactors.

## Structural debt selected (M60)

- **Governed campaign executor decomposition:** `python -m starlab.training.execute_full_local_training_campaign` remains the **only** CLI entry for M50/M51 campaign execution. Phase execution logic for bootstrap-only (M50) and post-bootstrap protocol (M51) lives in **`starlab.training._full_local_training_campaign_execution`** (private module — **not** a supported import surface for downstream code).

## Behavior-preservation posture

- **No change** to governed JSON artifact shapes, CLI flags, exit codes, lockfile behavior, or M49/M50/M51 semantics described in `docs/runtime/full_local_training_campaign_v1.md` and `docs/runtime/industrial_hidden_rollout_mode_v1.md`.
- Refactor is **mechanical extraction** of helpers; orchestration order and phase receipts are unchanged.

## Regression-proof strategy

- Existing **`tests/test_m50_campaign_execution.py`** and **`tests/test_m51_campaign_execution.py`** remain the primary **end-to-end** proof paths for fixture campaigns (bootstrap-only and `--post-bootstrap-protocol-phases`).
- **`tests/test_m60_v2_readiness_guardrails.py`** holds **architectural** guardrails (e.g. evaluation↔state loader boundary; private executor module present).

## Explicit non-claims

- M60 does **not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder/public performance, or campaign success for operator-local runs.
- M60 does **not** re-audit or replace **M32**–**M37** closure work; it **references** what is already resolved and addresses **remaining** material structure only.
