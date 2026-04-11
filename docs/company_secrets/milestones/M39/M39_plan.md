# M39 Plan — Public Flagship Proof Pack

**Milestone:** M39  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** **Complete** — merged to `main` ([PR #50](https://github.com/m-cahill/starlab/pull/50)); see `M39_run1.md`, `M39_summary.md`, `M39_audit.md`, `docs/starlab.md` §11 / §18.

---

## Milestone intent

M39 turns the already-proved STARLAB substrate into **one coherent, reproducible, public-facing proof surface**. STARLAB stops being only “well-governed internally” and becomes **externally legible as a flagship lab artifact**. The work should package what is already proved — **not** smuggle in new training, new benchmark-integrity claims, or live-runtime claims. STARLAB remains a **lab-first, replay-native, evidence-first** research substrate.

The **public flagship proof pack** is shaped as a **public evidence index**, not a product UI or benchmark engine: emphasize **regeneration**, **bounded claims**, **provenance**, **non-claims**.

---

## Core objective

Deliver a **deterministic flagship proof pack** that a technically capable outsider can inspect and regenerate from the repo, demonstrating the strongest currently proved chain:

- governed evaluation evidence (**M25**),
- learned-agent evaluation (**M28**),
- hierarchical / explorer evidence surfaces (**M31**),
- CI-backed artifact reproducibility (**M33** tiering extended with **`flagship`**),
- explicit non-claims.

The proof pack should be **diligence-friendly**: clear public surface, explicit provenance posture, bounded claims, and no accidental leakage of crown-jewel internals or ambiguous rights posture.

---

## What M39 proves

M39 proves, narrowly, that STARLAB can present a **public, bounded, reproducible flagship evidence package** over already-governed artifacts.

## What M39 does not prove

- benchmark integrity  
- live SC2 in CI  
- replay↔execution equivalence  
- new agent-training results  
- a new training/testing track  

Agent training begins only after **M38** and **M39** are closed; M39 stays out of that lane.

---

## Slices (delivered)

### Slice A — Build the flagship proof-pack artifact

- Package: `starlab/flagship/`
- Entrypoint: `python -m starlab.flagship.emit_public_flagship_proof_pack`
- Optional: `make flagship`
- Output layout under `out/flagship/` (default):

  - `public_flagship_proof_pack.json`, `public_flagship_proof_pack_report.json`
  - `baseline/` (M25), `learned/` (M28), `explorer/` (M31)
  - `hashes.json` — **SHA-256 of generated outputs only**; provenance lives in `public_flagship_proof_pack.json`

**M25 path:** in-process emission via existing `write_baseline_evidence_pack_artifacts` from the **governed Phase-IV fixture graph** (same inputs as `tests/test_baseline_evidence_pack.py` golden path) for deterministic hashes across machines. A fresh M20–M24 chain from contract embeds cwd-sensitive `suite_path` in M23 and is **not** used for the flagship pack.

**M28 / M31:** in-process `write_learned_agent_evaluation_artifacts` and M31 explorer builder from governed fixtures (M16 bundle, M31 bundle, M30 agent).

### Slice B — Public proof narrative

- `docs/runtime/public_flagship_proof_pack_v1.md`
- `docs/flagship_proof_pack.md`

### Slice C — CI evidence

- New parallel **`flagship`** job (peer of **`fieldtest`**); **`governance`** depends on both.
- Generates pack, validates files, uploads **`flagship-proof-pack`** artifact.

---

## Deliverables (Cursor)

- `docs/company_secrets/milestones/M39/M39_plan.md` (this file)
- `docs/company_secrets/milestones/M39/M39_toolcalls.md`
- `starlab/flagship/` implementation
- `tests/test_m39_public_flagship_proof_pack.py`
- CI wiring for proof-pack generation and artifact upload
- Closeout artifacts **later** (post-merge): `M39_run1.md`, `M39_summary.md`, `M39_audit.md`

---

## Acceptance criteria

1. A single deterministic command regenerates the flagship proof pack from the repo.  
2. The proof pack includes regenerated evidence from **M25**, **M28**, and **M31** surfaces.  
3. The proof pack has a documented contract and an explicit non-claims section.  
4. CI generates and uploads the proof-pack artifact on authoritative PR-head and merge-boundary `main`.  
5. Public docs explain what the proof pack is, how to regenerate it, and what it does **not** claim.  
6. No gate weakening is introduced.  
7. No training-track work is introduced.  

---

## Guardrails

- No claim inflation.  
- No new benchmark semantics.  
- No hidden manual assembly.  
- No CI ambiguity (reproducible in CI).  
- No post-closeout churn if avoidable.  

---

## Branch / PR

- **Branch:** `m39-public-flagship-proof-pack`
- **PR title:** `M39: add public flagship proof pack`

---

## Closeout (later)

When M39 is ready to close, use `docs/company_secrets/prompts/summaryprompt.md` and `unifiedmilestoneauditpromptV2.md`; update `docs/starlab.md`; record PR number, SHAs, CI runs; seed **M40** stubs.
