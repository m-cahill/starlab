# Milestone Audit — V15-M07: Training Smoke and Short GPU Shakedown

**Mode:** **DELTA AUDIT**  
**Milestone ID:** V15-M07  
**current_sha (merge):** `b7e4dc7c891687aea0e92ef622ab48f007bdbefe`  
**diff_range:** pre-M07 `main` → M07 implementation merge; public closeout commits documented separately  
**CI:** [24925848388](https://github.com/m-cahill/starlab/actions/runs/24925848388) (PR head **success**); [24925929052](https://github.com/m-cahill/starlab/actions/runs/24925929052) (merge-boundary `main` **success**). **Failing / superseded runs used as merge authority:** **none**.  

**Test / lint (PR-head):** Ruff check, Ruff format, Mypy, full pytest + smoke — **success**.  
**Dependency delta:** No intentional broadening of CVE ignore list.  

**Date:** 2026-04-25  

---

## Required factual statements (M07)

- **V15-M07 is receipt/shakedown tooling only** (contract + fixture + optional operator paths + guarded synthetic local trainer).  
- **No** **V15-M08** long GPU **campaign**; **`long_gpu_run_authorized` false** throughout.  
- **No** checkpoint **promotion**; **no** strong-agent benchmark **execution**; **no** human-panel **matches**; **no** XAI **review**.  
- **No** human-benchmark or strong-agent **claim** **authorized**.  
- **No** model **weights** or **checkpoint** **blobs** committed.  
- **No** new real **public** **claim-critical** register **rows**.  
- **Operator-local short-GPU shakedown** for the public program record: **`operator_local_short_gpu_not_run`** (CUDA unavailable on closeout host — **not** fake evidence).  
- **V15-M08** — *Long GPU Campaign Execution* — **not** implemented; **not** started; **awaits** explicit plan approval only.

---

## Findings

### **LOW** — Ongoing `pip` CVE ignore (program-wide)

- **Observation:** Same **narrow** `pip` **CVE-2026-3219** ignore as prior V15 milestones; M07 re-check recorded in `docs/starlab-v1.5.md` §11.  
- **Risk:** Toolchain **until** fixed upstream.  
- **Mitigation:** Unchanged; **not** broadened; security job still runs full sequence.  
- **Carry-forward:** Remove when audit-clean `pip` exists.

### **INFORMATIONAL** — CI action / Node deprecations

- **Observation:** Some GitHub Actions emit **Node 20** end-of-life **annotations**.  
- **Impact:** **None** on required job **conclusion** for M07 runs.

---

## Verdict

- M07 **delta** matches **receipt + bounded optional shakedown tooling** scope: clear non-claims, no long campaign, no claim authorization, no committed weights, no public claim rows.  
- **No** HIGH or MEDIUM **open** issues for **M07** scope.  
- **Next (V15-M08):** do **not** start long GPU campaign or authorize long runs until **explicit** plan approval.

---

## Artifacts

- `V15-M07_run1.md`  
- `V15-M07_summary.md`  
- `V15-M07_toolcalls.md`  

---

## Explicit (audit boundary)

V15-M07 is **receipt/shakedown tooling only**; no V15-M08 long GPU campaign; **`long_gpu_run_authorized` false**; no checkpoint promoted; no strong-agent benchmark execution; no human-panel matches; no XAI review; no claim authorization; no weights/checkpoint blobs committed; no real public claim-critical register rows; **V15-M08** not implemented; operator shakedown **not run** in public record (`operator_local_short_gpu_not_run`).
