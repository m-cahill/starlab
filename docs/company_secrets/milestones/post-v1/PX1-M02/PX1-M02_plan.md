# PX1-M02 — Plan: Play-Quality Evaluation & Demo Candidate Selection

**Status:** PR1 (open / freeze / readiness) — **in progress** on branch `px1-m02-play-quality-demo-candidate-selection`.

## Objective

Open **PX1-M02** in the public ledger; freeze a **bounded, evidence-backed** play-quality evaluation protocol; evaluate coherent **PX1-M01** candidate(s); select or honestly decline a **demo-worthy** candidate; preserve non-claims; **do not** open **PX1-M03** or **v2**.

## Locked scope

### In scope

- Ledger + runtime **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**
- Deterministic **`px1_play_quality_protocol*.json`** + **`px1_play_quality_evidence*.json`** emitters
- **Candidate pool:** post-bootstrap weighted-refit bundle as **sole primary** candidate unless inspection finds a second coherent comparable surface (no forced pre-refit comparison)
- **Opponent profiles:** two bounded profiles (scripted-style + heuristic-style labels) via frozen repo-relative M02 match configs — **not** ladder claims
- Private operator docs: plan, protocol freeze, checklist, execution readiness, toolcalls
- Minimal tests + fixtures under **`tests/fixtures/px1_m02/`**

### Out of scope

- Industrial full-run threshold work (**PX1-M01** only)
- Winning video / demo proof pack (**PX1-M03**)
- **v2**
- Default CI live SC2 evaluation
- Ladder/public-strength claims

## PR split

1. **PR1 (this branch):** open milestone, freeze protocol, emitters, docs, fixtures/tests — **no** authoritative operator evaluation claims yet.
2. **Operator-local evaluation** after merge: run bounded **`local_live_sc2`** series per checklist.
3. **PR2 (later):** closeout with real evidence, honest **`candidate-selected`** or **`no-candidate-selected`**, ledger reset **`current milestone`** → **None**.

## Definition of done (full milestone — PR1 + operator + PR2)

Per acceptance criteria in the milestone charter: ledger, runtime contract, frozen protocol, evaluation, evidence artifacts, operator note + declaration, honest closeout, **PX1-M03** remains unopened unless separately authorized, CI green.
