# STARLAB v1.5 — Training Readiness Charter (runtime)

**Contract id:** `starlab.v15.training_readiness_charter.v1`  
**Milestone:** `V15-M00`  
**Emission:** `python -m starlab.v15.emit_v15_training_readiness_charter --output-dir <dir>`

---

## Purpose

This document is the **runtime narrative** companion to the deterministic JSON charter (`v15_training_readiness_charter.json`). It does **not** authorize GPU training execution by itself; it records the **governance posture** and **long GPU run gate** structure for v1.5.

---

## Authorization posture (M00)

- **M00 emits** the training readiness charter and report only.
- **M00 does not** execute a long GPU campaign, run benchmarks, or produce XAI inference artifacts.

---

## Long GPU run gates (summary)

Gates **A**–**G** are defined in the JSON charter (`long_gpu_run_gates`): governance, environment, data, checkpoints, evaluation, XAI, operator. A long GPU training session should not be treated as “program-valid” until the program explicitly closes these gates in later milestones—this file does not claim they are green.

---

## Public authority

The **authoritative** human-readable v1.5 governance source is `docs/starlab-v1.5.md`. The strategic charter lives in `docs/starlab-v1.5moonshot.md`.

---

## Non-claims

See `docs/starlab-v1.5.md` *Standing non-claims* and the `non_claims` field in the JSON charter.
