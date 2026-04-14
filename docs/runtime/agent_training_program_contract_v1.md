# Agent training program contract (M40)

**Version:** `starlab.agent_training_program_contract.v1`  
**Ledger:** `docs/starlab.md` §6–§8, §11  
**Emitter:** `python -m starlab.training.emit_agent_training_program_contract --output-dir out/training_program`

## Purpose

M40 defines the **governed training-program posture** for Phase VI milestones **M40**–**M45**. It is a **charter and contract** milestone: it does **not** train models or commit weights.

## Outputs

| File | Role |
| ---- | ---- |
| `agent_training_program_contract.json` | Full contract: allowed upstreams, future artifact families, CI vs local policy, non-claims |
| `agent_training_program_contract_report.json` | Compact summary keyed by `contract_sha256` |

Default output directory: **`out/training_program/`** (gitignored locally; not part of `fieldtest` or `flagship`).

## Local vs CI

- **CI:** schema/contract validation, deterministic emission tests, fixture-only code paths — **no GPU training**, **no live SC2**.
- **Local:** training runs are **local-first**; reference hardware **RTX 5090 Blackwell** where relevant.

## Non-claims

The contract JSON includes explicit `non_claims` identifiers (not benchmark integrity, not replay↔execution equivalence, not live SC2 in CI, no ladder claims, etc.). They are **normative for program posture**, not mathematical proofs.

## Upstream surfaces

Future training milestones bind to governed artifacts from **M26**–**M31** and evaluation surfaces **M20**–**M25** / **M28** / **M39** as described in the emitted JSON — without upgrading those surfaces to new claims.

## Relation to M42 (learned-agent comparison)

**M42** records both the **M20 benchmark contract** identity (evaluation surface) and the **M40 training-program contract** identity (charter) on `learned_agent_comparison.json`. The M42 CLI accepts an optional **`--training-program-contract`** path to load this JSON from disk; otherwise it uses the same in-process default as `build_agent_training_program_contract()`. See `docs/runtime/learned_agent_comparison_harness_v1.md` — **M20** and **M40** are distinct; do not point **`--benchmark-contract`** at the M40 file.

## Relation to M49 (full local campaign charter)

**M49** full local training / bootstrap campaign contracts record **M40** `contract_sha256` / `program_version` plus a resolved on-disk path for operator preflight. See `docs/runtime/full_local_training_campaign_v1.md`.
