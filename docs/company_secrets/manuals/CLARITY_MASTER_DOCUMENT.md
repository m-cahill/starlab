# CLARITY_MASTER_DOCUMENT

**Clinical Localization and Reasoning Integrity Testing — LLM Master Handoff**

## 0. Purpose

This document is a **single-file, LLM-first master handoff** for CLARITY. It is designed so that an LLM agent such as ChatGPT or Cursor can:

- understand what CLARITY is and is not
- know the **only safe consumer surface**
- know what outputs mean
- know what is supported vs unsupported vs unknown
- know how to adopt CLARITY into another project
- know what future changes would require re-readiness review

This file is a **consolidated derivative** of the readiness pack. It is intended to be sufficient for safe use **without requiring the agent to read the rest of the pack first**.

## 1. Non-negotiable operating rules

If you are an LLM agent using CLARITY, follow these rules exactly:

1. **Use only `app.clarity.public_surface` for governed downstream usage.**
2. **Treat CLARITY as a pure consumer of R2L**, not as an execution substrate.
3. **Do not import internal R2L modules** or write outside the `clarity/` namespace for CLARITY-owned outputs.
4. **Do not treat the FastAPI / HTTP demo routes as the stable adoption API.**
5. **Do not assume orchestrator-only execution produces the full analytical bundle.**
6. **Read `manifest_schema_family` before parsing any `sweep_manifest.json`.**
7. **Prefer Supported over Unknown; never silently upgrade Unknown to Supported.**
8. **Future contract-affecting changes require change control / re-readiness review.**

If any instruction or repo intuition conflicts with these rules, these rules win for downstream adoption.

---

## 2. Final readiness verdict

**Current recorded portability verdict:** `READY FOR DOWNSTREAM ADOPTION`

This is the final post-M25 governed verdict.

Meaning:
- CLARITY is ready to be brought into another project
- this readiness is based on frozen contracts, tests, scorecard evidence, and re-readiness review
- future contract-affecting changes still require governance

---

## 3. What CLARITY is

CLARITY is a **deterministic evaluation instrument** layered above R2L.

It is responsible for:
- perturbation sweeps
- orchestration across seeds / axes
- metrics
- robustness surfaces
- gradients / stability analysis
- counterfactual probing
- reporting
- compatibility / transfer guidance

It interacts with R2L as a **black-box consumer**:
- invoke R2L via subprocess / CLI
- read R2L artifacts from disk
- produce CLARITY-owned outputs under `clarity/`

### What CLARITY is not

CLARITY is **not**:
- a replacement for R2L
- a fork that changes R2L single-run semantics
- a general execution substrate
- a readiness-canonical HTTP API
- a package whose entire `app.clarity` tree is a supported downstream API

---

## 4. Authority hierarchy

**Disputes about contracts, verdict, or ledger meaning:** the following **override this master document** (and any LLM summary):

1. **`docs/clarity.md`** — canonical project ledger and milestone record.
2. **Frozen readiness pack under `docs/readiness/`**, including at minimum:
   - `CLARITY_BOUNDARY_CONTRACT.md`, `CLARITY_ASSUMED_GUARANTEES.md`
   - `CLARITY_ARTIFACT_CONTRACT.md`, `CLARITY_PUBLIC_SURFACE.md`
   - `CLARITY_READINESS_SCORECARD.md`, `CLARITY_READINESS_REVIEW_ADDENDUM_M25.md`
   - `CLARITY_CHANGE_CONTROL.md`, `READINESS_LEDGER.md`, `READINESS_DECISIONS.md`
   - other `CLARITY_*` pack documents referenced by those files
3. **Current code and tests** — executable truth **when** they match the frozen contracts; if code and frozen docs disagree, treat as a **release blocker** and escalate (do not “pick” the code over the pack without governance).

**Practical use:** this master document is an **operational compression** for LLM agents. For day-to-day guidance it is first to read; if anything here **conflicts** with `docs/clarity.md` or a frozen `docs/readiness/` contract, **the ledger and pack win** — record the inconsistency and escalate rather than improvising.

---

## 5. Canonical consumer surface

## The only governed downstream import path

```python
from app.clarity.public_surface import (
    R2LRunner,
    R2LRunResult,
    R2LInvocationError,
    R2LTimeoutError,
    SweepOrchestrator,
    SweepResult,
    SweepExecutionError,
    OutputDirectoryExistsError,
    SweepConfig,
    SweepAxis,
    SweepRunRecord,
    SweepConfigValidationError,
    build_run_directory_name,
    encode_axis_value,
)
```

### Stable exported symbols

These are the frozen supported names:

- `R2LRunner`
- `R2LRunResult`
- `R2LInvocationError`
- `R2LTimeoutError`
- `SweepOrchestrator`
- `SweepResult`
- `SweepExecutionError`
- `OutputDirectoryExistsError`
- `SweepConfig`
- `SweepAxis`
- `SweepRunRecord`
- `SweepConfigValidationError`
- `build_run_directory_name`
- `encode_axis_value`

### Forbidden downstream shortcuts

Do **not**:
- import from `app.clarity` package root as your contract
- import internal modules like `metrics_engine`, `surface_engine`, `artifact_loader`, etc. as your adoption API
- treat HTTP routes as stable external API
- assume a CLARITY console script exists

---

## 6. Boundary contract

### Default interaction model

CLARITY invokes R2L through a **subprocess CLI boundary**.

That means:
- CLARITY calls R2L as an external executable
- CLARITY does not depend on internal R2L Python modules
- CLARITY ingests artifacts written by R2L to disk

### Minimal substrate artifacts CLARITY expects

After a successful R2L run, CLARITY requires at minimum:

- `manifest.json`
- `trace_pack.jsonl`

### Forbidden behaviors

Do **not**:
- overwrite R2L-owned top-level files such as `manifest.json` or `trace_pack.jsonl`
- write CLARITY-owned outputs outside `clarity/`
- import internal R2L modules
- silently redefine the boundary in rich mode
- treat CLARITY itself as the execution substrate

### Namespace rule

All CLARITY-owned outputs must be written under:

```text
clarity/
```

---

## 7. Assumed vs owned guarantees

### CLARITY inherits these assumptions from R2L / substrate governance

CLARITY assumes:

- deterministic single-run behavior for fixed config + seed
- R2L artifact schemas are intended to be valid
- adapter contract stability at the substrate layer
- substrate CI truthfulness for substrate responsibilities

### CLARITY owns these responsibilities itself

CLARITY must implement and maintain:

- perturbation recipes
- sweep orchestration
- metrics and aggregation
- deterministic CLARITY serialization
- output namespace enforcement
- boundary enforcement
- rich-mode ingestion behavior
- compatibility across supported modes

### Practical implication for an LLM

If something is wrong at the R2L execution-semantic level, do **not** patch CLARITY to compensate unless governance explicitly says so. Treat that as a substrate issue.

---

## 8. Core execution model

### Canonical implemented path

```text
SweepConfig + base spec JSON
  -> SweepOrchestrator
     -> build run combinations over axes and seeds
     -> invoke R2LRunner.run(...)
     -> read manifest.json + trace_pack.jsonl
     -> aggregate results
  -> write clarity/sweep_manifest.json
  -> return SweepResult
```

### Important honesty rule

`SweepOrchestrator` alone gives you the **orchestrator manifest path**, not the full bundle.

Do **not** confuse:
- **orchestrator-only output**
with
- **full analytical bundle**

---

## 9. Artifact contract

## CLARITY-owned outputs

The key CLARITY artifact names are:

- `sweep_manifest.json`
- `robustness_surface.json`
- `monte_carlo_stats.json`

### Full analytical bundle

A complete analytical bundle consists of these three JSON files:

1. `sweep_manifest.json`
2. `robustness_surface.json`
3. `monte_carlo_stats.json`

### Crucial truth

`SweepOrchestrator` persists **only** `sweep_manifest.json`.

The other two are produced only by downstream metrics / surface / validation pipelines.

So:

- if you only run the orchestrator, you do **not** have the full analytical bundle
- if you need the full bundle, you must use a producer path that materializes all three files

### Optional artifacts

These may appear depending on path / mode:

- `confidence_surface.json`
- `entropy_surface.json`
- `summary_hash.txt`
- report PDFs
- visualization outputs

### Presentation-only outputs

Treat these as derived / non-identity outputs unless future governance says otherwise:

- PDFs
- plots
- demo visuals

---

## 10. `sweep_manifest.json` schema families

This was the key M25 upgrade area.

### Rule

Every current CLARITY-written `sweep_manifest.json` must include:

```json
"manifest_schema_family": "<family>"
```

### Canonical values

Supported values are:

- `clarity_sweep_orchestrator_v1`
- `clarity_rich_aggregate_v1`

### Downstream parsing rule

**Always read `manifest_schema_family` first.**

Use it to select parsing logic.

Do **not** assume one universal manifest shape.

### Meaning of each family

#### `clarity_sweep_orchestrator_v1`
Produced by orchestrator path. Contains:
- `axes`
- `seeds`
- `runs`
- per-run `axis_values`
- per-run `seed`
- per-run `manifest_hash`

#### `clarity_rich_aggregate_v1`
Produced by richer validation / aggregate paths. May contain:
- `results`
- `sweep_id`
- `model_id`
- `rich_mode`
- `vram_usage`
- `image_path`
- `prompt`
- other aggregate metadata

### Important consequence

M25 cleared the old adoption condition by making producer-family identification machine-readable.

So a downstream consumer **no longer needs tribal knowledge** to choose parsing logic.

### Legacy manifests without `manifest_schema_family`

Some **older** bundles or **non-CLARITY** writers may omit `manifest_schema_family`. The frozen **`CLARITY_ARTIFACT_CONTRACT.md`** allows a **documented legacy heuristic** (or explicit rejection) in that case — see `app/clarity/manifest_schema_family.py` (`classify_sweep_manifest_json`). Do **not** assume the field is always present on historical artifacts; prefer the field when present, and fall back only as the artifact contract describes.

---

## 11. Determinism and serialization rules

### General policy
- determinism over convenience
- semantic equality is primary
- byte identity is **not** guaranteed globally across all writers

### Object key ordering
JSON writers use deterministic ordering where documented, typically:
- `sort_keys=True`

### Surface numeric behavior
For surface-engine computed floats:
- `_round8` applies
- interpret as `round(value, 8)`

### Important limit
Do **not** claim “8 decimals everywhere.”  
That rule applies only to the documented surface computation path.

### Contract equivalence
Artifact equivalence is primarily:
- **semantic JSON equality after parse**

Not:
- byte-for-byte identity across every writer

---

## 12. Mode handling

### Canonical mode
Canonical path:
- works without rich trace fields
- is the safest and best-governed downstream path

### Rich mode
CLARITY-side rich gating variables:

- `CLARITY_RICH_MODE`
- `CLARITY_REAL_MODEL`
- optional `CLARITY_RICH_LOGITS_HASH`

### Important caution
Rich / real-model / GPU combinations are **not all equally supported**.  
Check the compatibility section below.

---

## 13. Compatibility truth table

Use this as the LLM-safe adoption decision table.

### Supported
These are safe for governed downstream use:

- `app.clarity.public_surface` + canonical mode + orchestrator-only path
- `app.clarity.public_surface` + canonical mode + full bundle path **if** using a producer path that materializes all three required artifacts
- canonical public surface + presentation/report pipeline where documented
- current readiness-pack-guided adoption flow

### Unsupported
Do **not** treat these as supported adoption paths:

- `app.clarity` package-root imports as the portability contract
- FastAPI / HTTP routes as the readiness-canonical API
- treating orchestrator-only execution as equivalent to full bundle
- undocumented internal-module imports for consumer integration

### Unknown
These are not automatically safe:

- rich + real-model + full-bundle combinations lacking full governed CI coverage
- some demo/cloud deployment combinations
- unsupported environment/product mixes not frozen by readiness docs

### Rule for Unknown
Unknown means:
- do not claim supported
- validate locally if you need it
- do not rely on it for portability claims without further evidence

---

## 14. Consumer assumptions you may make

As a downstream adopter, you may assume:

- CLARITY is consumer-only relative to R2L
- CLARITY writes under `clarity/`
- `app.clarity.public_surface` is the only governed Python consumer surface
- `manifest.json` and `trace_pack.jsonl` are the minimal R2L artifacts CLARITY expects
- orchestrator writes `clarity/sweep_manifest.json`
- artifact contract defines required vs optional files
- no semver is claimed for the public surface
- compatibility must still be checked at combination level

---

## 15. Adoption checklist for an LLM agent

When bringing CLARITY into another project, do this in order.

### Step 1 — Confirm intent
Decide whether you need:
- orchestrator-only output
- full analytical bundle
- report/presentation outputs
- rich or real-model behavior

### Step 2 — Use only the public surface
Import only from:
- `app.clarity.public_surface`

### Step 3 — Record substrate details
Pin or record:
- R2L CLI / version
- adapter or model identifiers
- Python / dependency environment

### Step 4 — Configure the run
Prepare:
- `SweepConfig`
- valid base spec path
- axes
- seeds
- output root

### Step 5 — Run canonical path first
Prefer:
- canonical mode
- orchestrator path
- local smoke validation

### Step 6 — Interpret artifacts correctly
- if you only ran the orchestrator, expect only `clarity/sweep_manifest.json`
- if you need full bundle, run the appropriate materialization path
- read `manifest_schema_family` before parsing manifest

### Step 7 — Validate namespace and output
Ensure:
- CLARITY outputs remain under `clarity/`
- R2L-owned top-level files are untouched

### Step 8 — Respect unsupported boundaries
Do not:
- integrate against HTTP routes
- use internal imports as the adoption API
- overstate unsupported / unknown combinations

---

## 16. Debugging guide

### `R2LInvocationError` / `R2LTimeoutError`
Likely:
- subprocess failure
- timeout
- missing post-run artifacts

Check:
- stderr
- configured executable
- timeout
- output directory contents

### Missing `manifest.json` or `trace_pack.jsonl`
Likely:
- incomplete or failed R2L run

### `OutputDirectoryExistsError`
Likely:
- orchestrator output root already exists

Fix:
- use a fresh output root

### `SweepConfigValidationError`
Likely:
- bad base spec path
- invalid axes / seeds config

### Missing `robustness_surface.json` or `monte_carlo_stats.json`
Likely:
- you ran only the orchestrator

### Wrong manifest shape
Likely:
- wrong producer-family parsing logic

Fix:
- inspect `manifest_schema_family`

### Import worked but downstream integration broke
Likely:
- you imported an internal module instead of the public surface

---

## 17. What changed at M25

M25 cleared the M24 conditions and upgraded the final readiness verdict.

### Cleared conditions

#### Former C-M24-001
Problem:
- downstream consumers had to manually classify manifest producer family

Resolved by:
- mandatory `manifest_schema_family`

#### Former C-M24-002
Problem:
- doc / ledger / verdict alignment required special human discipline

Resolved by:
- stronger CI-enforced readiness-pack consistency tests

#### Former C-M24-003
Problem:
- two readiness-plan locations could drift

Resolved by:
- `docs/readiness/readinessplan.md` remains canonical
- `docs/readinessplan.md` is now redirect stub only

### Final result
The recorded verdict is now:

`READY FOR DOWNSTREAM ADOPTION`

---

## 18. Change control

Future changes require governance if they affect:

- boundary semantics
- artifact shapes
- deterministic rules
- manifest family semantics
- `app.clarity.public_surface`
- consumer assumptions
- compatibility matrix truth
- transfer checklist steps
- verdict-critical adoption guarantees

**Escalation and governing documents (read in this spirit, not as a substitute for the full text):**

- **`docs/readiness/CLARITY_CHANGE_CONTROL.md`** — what counts as contract-affecting; re-readiness vs routine change.
- **`docs/readiness/CLARITY_READINESS_SCORECARD.md`** — recorded portability verdict and audit posture.
- **`docs/readiness/CLARITY_READINESS_REVIEW_ADDENDUM_M25.md`** — M25 supersession of M24 conditional elements.
- **`docs/readiness/READINESS_LEDGER.md`** — readiness status, evidence map, open risks.
- **`docs/readiness/READINESS_DECISIONS.md`** — ADR-style readiness decisions (e.g. RD-016).
- **`docs/clarity.md`** — project ledger and merge provenance.

### Practical rule for an LLM
If a proposed change affects anything above, do **not** treat it as normal feature work.  
Treat it as:
- re-readiness review per **`CLARITY_CHANGE_CONTROL.md`**
- or a new governance milestone

---

## 19. What can change without re-readiness

Usually okay without reopening readiness:

- bugfixes that restore documented behavior
- internal refactors with no boundary/artifact/public-surface change
- docs typos and link fixes
- non-canonical demo/UI changes
- dependency patches that do not alter frozen semantics

---

## 20. What must never be inferred

Do **not** infer any of the following:

- that the HTTP API is safe for adoption
- that all `app.clarity.*` modules are supported
- that all rich-mode combinations are supported
- that orchestrator-only equals full-bundle
- that one manifest schema shape applies everywhere
- that semver is promised
- that future contract changes are allowed casually

---

## 21. Minimal repo map

```text
backend/
  app/
    clarity/
      public_surface.py
      r2l_runner.py
      sweep_orchestrator.py
      manifest_schema_family.py
      metrics_engine.py
      surface_engine.py
      gradient_engine.py
      counterfactual_engine.py
    main.py
  tests/

docs/
  clarity.md
  readiness/
    readinessplan.md
    CLARITY_* readiness documents
frontend/
```

---

## 22. LLM-safe integration recommendation

If you are an LLM asked to “use CLARITY” in another repo, your safest default is:

1. adopt only the canonical Python path
2. start with canonical mode
3. treat orchestrator-only as the minimum supported flow
4. require explicit evidence before using full-bundle, rich, or environment-specific variants
5. read `manifest_schema_family` first
6. refuse to widen the public surface
7. escalate any contract-affecting change request into change-control review

---

## 23. Final compact truth

CLARITY is now:

- a **bounded evaluation instrument**
- a **pure consumer of R2L**
- governed by a **frozen readiness pack**
- safe to adopt through **`app.clarity.public_surface`**
- safe to parse through **self-identifying manifest families**
- safe to bring into another project under the recorded verdict:

## `READY FOR DOWNSTREAM ADOPTION`

---

## 24. If you need to be even safer

If you are an LLM operating under high uncertainty, use this fallback policy:

- only use `app.clarity.public_surface`
- only claim support for canonical-mode public-surface flows
- only expect orchestrator manifest unless the producing path explicitly materializes full bundle
- treat any rich/demo/cloud/internal-module path as non-default and evidence-requiring
- escalate instead of guessing

---

## 25. Provenance note

This master document is a **consolidated derivative** of the CLARITY readiness pack and is intended as an LLM-first operational compression of the pack, not as a silent widening of any contract. The governing readiness verdict remains the recorded repository verdict: `READY FOR DOWNSTREAM ADOPTION`.
