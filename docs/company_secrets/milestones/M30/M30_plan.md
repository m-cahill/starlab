# M30 Plan — First Learned Hierarchical Agent

## Milestone identity

**Milestone:** M30 — First Learned Hierarchical Agent  
**Tag target:** `v0.0.30-m30`  
**Recommended branch:** `m30-first-learned-hierarchical-agent`  
**Recommended PR title:** `M30: first learned hierarchical agent`

## Objective

Prove the first **deterministic, offline, replay-derived learned hierarchical agent artifact** in STARLAB.

M30 instantiates the M29 hierarchy with a **small, auditable, imitation-style learned artifact** over governed replay data. It consumes governed **M26** replay training data and referenced **M14** bundle directories, reuses the existing **M16 → M18** observation materialization seam, and produces a frozen hierarchical agent artifact plus a compact report. M27 established the bounded replay-materialization seam; M29 established the two-level manager→worker interface that M30 instantiates.

## Why this is the right size

M28 proved a bounded offline evaluation harness for a **flat** learned subject; M29 proved only the **interface contract** for hierarchy. The narrowest honest M30 is: prove a **first learned hierarchical artifact**, not a full hierarchical evaluation program, not a replay explorer, and not a flagship proof pack.

## Scope boundaries (defaults)

- Offline only  
- Replay-derived only  
- Two levels only: one manager, one worker  
- No benchmark/evaluation semantics in M30  
- No live SC2  
- No raw action legality  
- Reuse M27 bounded observation-signature feature policy unless a tiny additive extension is clearly necessary  
- Fixed M30-owned delegate partition policy (not clustering)  
- Exactly four delegates in v1  
- No M31 product code  

## Delegate policy v1

**Policy id:** `starlab.m30.delegate.fixed_four_v1` (single constant in `starlab/hierarchy/delegate_policy.py`)

**Delegate catalog (stable IDs):**

| Delegate ID | Coarse labels (`starlab.m26.label.coarse_action_v1`) |
|-------------|------------------------------------------------------|
| `economy` | `economy_expand`, `economy_worker` |
| `production` | `production_unit`, `production_structure`, `research_upgrade` |
| `combat` | `army_move`, `army_attack` |
| `information` | `scout`, `other` |

Do **not** learn the delegate taxonomy from data in M30. Use a deterministic checked-in label→delegate mapping.

## Primary artifacts

| Artifact | Version |
|----------|---------|
| `replay_hierarchical_imitation_agent.json` | `starlab.replay_hierarchical_imitation_agent.v1` |
| `replay_hierarchical_imitation_agent_report.json` | `starlab.replay_hierarchical_imitation_agent_report.v1` |

Canonical JSON, deterministic, hash-stable on rerun.

## Learning semantics

1. For each governed M26 example, materialize one observation via **M16 → M18**.  
2. Derive one bounded context signature (M27 feature policy `starlab.m27.feature.observation_signature_v1`).  
3. Derive **manager target** by mapping coarse label → delegate via M30 map.  
4. Train **manager** as majority-per-signature delegate predictor on **training** split only.  
5. Train **worker** as majority-per-(delegate, signature) coarse-label predictor on **training** split only.  
6. Inference: manager predicts delegate → worker predicts coarse label within that delegate.  
7. Unseen signature: manager → global majority delegate; worker → delegate global majority label or documented global fallback.  

## Product layout

- `docs/runtime/replay_hierarchical_imitation_agent_v1.md`  
- `starlab/hierarchy/delegate_policy.py`  
- `starlab/hierarchy/hierarchical_agent_models.py`  
- `starlab/hierarchy/hierarchical_agent_fit.py`  
- `starlab/hierarchy/hierarchical_agent_predictor.py`  
- `starlab/hierarchy/emit_replay_hierarchical_imitation_agent.py`  
- `tests/test_replay_hierarchical_imitation_agent.py`  
- `tests/fixtures/m30/`  

## Tests

- Unit: delegate mapping totality, manager/worker fit and fallbacks, deterministic hash, import guard  
- E2E: governed M26 + M14 → agent + report; goldens  
- Trace: generated traces validate against M29 schema (compact proof set: one trace per delegate where data supports + fallback path)  
- Failure paths: missing bundle, dataset mismatch, unsupported label, empty train, malformed agent, schema violation  

## Acceptance criteria

- Deterministic `replay_hierarchical_imitation_agent.json` + report  
- Runtime contract doc matches implementation  
- Artifact anchors `interface_trace_schema_version` to M29 trace schema  
- Generated hierarchical traces validate against M29 schema  
- No forbidden imports in listed M30 modules  
- Fixture-backed E2E tests green; CI green  
- `docs/starlab.md` updated at closeout (§6, §7, §8, §10, §11, §18, §20, §23)  
- M31 remains stub-only after closeout  

## Out of scope / non-claims

Benchmark integrity, live SC2, replay↔execution equivalence, tournament semantics, diagnostics/evidence-pack surfaces, replay explorer UI, raw SC2 actions, legality masks, more than two hierarchy levels, learned delegate discovery, M31 product code, stronger agent-quality claims beyond bounded internal smoke metrics.

## Status

**Implementation in progress** on branch `m30-first-learned-hierarchical-agent` — product code, tests, fixtures, runtime contract, and ledger §11 artifact names; **PR + CI + closeout** follow normal workflow.
