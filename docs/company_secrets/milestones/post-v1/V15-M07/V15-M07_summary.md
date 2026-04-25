# Milestone Summary — V15-M07: Training Smoke and Short GPU Shakedown

**Project:** STARLAB  
**Phase:** v1.5 (V15)  
**Milestone:** V15-M07 — Training Smoke and Short GPU Shakedown  
**Timeframe:** 2026-04-25 (implementation merge + public closeout)  
**Status:** **Closed** on `main` (implementation [PR #129](https://github.com/m-cahill/starlab/pull/129)); public doc closeout via follow-on PR per repo pattern  

---

## 1. Milestone Objective

Define and ship the **governed training-run receipt** for short training smoke, optional **operator_declared** validation/redaction, and optional **guarded** **operator_local_short_gpu** (lazy PyTorch, isolated **synthetic** MLP only — no SC2/PX2 training pipelines) — **before** any V15-M08 long GPU campaign, checkpoint promotion, or claim authorization.

---

## 2. Scope

### In scope

- `starlab.v15.training_run_receipt.v1` with `starlab.v15.training_smoke_short_gpu_shakedown.v1`; `v15_training_run_receipt.json` + report; `python -m starlab.v15.emit_v15_training_run_receipt`
- `docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`, governance in `docs/starlab-v1.5.md` / `docs/starlab.md`, register **notes** (no new claim-critical public **rows**)
- Tests: `tests/test_m07_v15_training_run_receipt.py`, governance tests

### Out of scope (explicit; remain true at closure)

- **V15-M07 is receipt/shakedown tooling only:** no **V15-M08** long GPU campaign; **`long_gpu_run_authorized` false**; no checkpoint **promotion**; no strong-agent benchmark **execution**; no human-panel **matches**; no XAI **review**; no human-benchmark or strong-agent **claim** authorization; no model **weights** or **checkpoint** blobs committed; no real public **claim-critical** register **rows**; **V15-M08** was only **stubbed** / not implemented. No v2; no **PX2-M04** / **PX2-M05** opened by M07.

**Operator-local GPU shakedown (this program record):** **`operator_local_short_gpu_not_run`** on closeout host (CUDA **unavailable**); no fake evidence.

---

## 3. Work executed

- Landed on `main` via [PR #129](https://github.com/m-cahill/starlab/pull/129) (merge `b7e4dc7c891687aea0e92ef622ab48f007bdbefe`).

### CI evidence

- **Authoritative PR-head:** [24925848388](https://github.com/m-cahill/starlab/actions/runs/24925848388) — head `c05f3e1429674f24d8a4efd06e358490e5060ad1` — **success**.
- **Merge-boundary `main`:** [24925929052](https://github.com/m-cahill/starlab/actions/runs/24925929052) on `b7e4dc7c…` — **success**.

---

## 4. Security / pip

- **CVE-2026-3219** (`pip`): no broadening of `pip-audit` ignore; single narrow `--ignore-vuln` for `pip` as recorded in `docs/starlab-v1.5.md` §11 (M07 re-check recorded). **Carry-forward:** remove when a fixed, audit-clean `pip` is available.

---

## 5. References

- **PR:** https://github.com/m-cahill/starlab/pull/129  
- **Merge:** `b7e4dc7c891687aea0e92ef622ab48f007bdbefe`  
- **Workflow:** `V15-M07_run1.md`  

**Explicit (non-claims at closure):** V15-M07 is **receipt/shakedown tooling only**; no V15-M08 long GPU campaign; **`long_gpu_run_authorized` false**; no checkpoint promoted; no strong-agent or human-panel benchmark execution; no XAI review; no claim authorization; no weights/checkpoint blobs committed; no real public claim-critical register rows; **V15-M08** not implemented; operator-local shakedown **not run** in public record (`operator_local_short_gpu_not_run`).
