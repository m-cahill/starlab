# PX1-M03 — Candidate Strengthening & Demo Readiness Remediation (v1)

**Milestone:** `PX1-M03` — post-`PX1-M02` corrective remediation (not the governed winning-video milestone).  
**Primary candidate (unchanged id):** `px1_m01_weighted_refit_rl_bootstrap_v1` — same lineage as PX1-M01/PX1-M02; this milestone adds an **enriched bounded live action surface** only.

---

## 1. Why PX1-M03 exists

**PX1-M02** closed honestly with **`no-candidate-selected`**: the frozen bounded **`local_live_sc2`** evaluation did not justify selecting a demo-worthy candidate. Separately, the live BurnySc2 harness was effectively **non-playing** from an action-command perspective (no meaningful `action_count` growth).

**PX1-M03** answers:

> Can STARLAB strengthen the current bounded candidate enough, within a small audit-defensible remediation milestone, to justify a later governed demo attempt?

---

## 2. Bounded remediation objective

Within scope, improve **visible early-game behavior** so a human observer can fairly say the agent is **attempting to play StarCraft**, not only mining and queueing workers.

**In scope:**

- Hard-coded **Terran** macro essentials: worker train, supply depot, barracks, marine production.
- **Hybrid:** narrow **M43-driven** (coarse-label) **throttled** attack-move / combat attempts plus bounded periodic fallback, without a full semantic-action architecture rewrite.
- **Proof readability:** `action_count` (one increment per successful SC2 command issued in the hybrid path), **categorized tallies**, and a compact **behavior summary** on `match_execution_proof.json`.

**Out of scope:** new industrial campaign, ladder claims, benchmark-integrity expansion, replay↔execution expansion, default CI live SC2, automatic **PX1-M04** or **v2** opening.

---

## 3. Frozen PX1-M03 remediation protocol (deterministic artifacts)

Emit **before** authoritative reruns:

- `px1_demo_readiness_protocol.json`
- `px1_demo_readiness_protocol_report.json`

CLI:

```text
python -m starlab.sc2.emit_px1_demo_readiness_protocol --input <protocol_input.json> --output-dir <dir>
```

**Fixture (synthetic, CI-safe input shape):** `tests/fixtures/px1_m03/protocol_input_v1.json`

**Evaluation minima** (do **not** lower win thresholds vs **PX1-M02** protocol v2): see `frozen_parameters` in the protocol input — includes `minimum_matches_per_candidate_per_opponent_profile = 5`, overall win rate **0.60**, etc.

**Runtime mode:** `required_runtime_mode = local_live_sc2`.

---

## 4. What counts as “demo-ready within scope”

A **`demo-ready-candidate-selected`** outcome requires **all** of:

1. Frozen **win / evidence completeness** thresholds satisfied (as encoded in protocol + evidence emitters), **and**
2. Operator-local artifacts show **non-trivial early action-family diversity** (workers, supply, military structure, military unit, movement/combat family), **and**
3. `demo_readiness_declaration.md` at the evaluation root states exactly **`demo-ready-candidate-selected`** with honest limitations.

---

## 5. What still does **not** count as proved

- **Not** a governed winning demo or “winning video” milestone (**PX1-M04**).
- **Not** ladder / public strength.
- **Not** global benchmark integrity or replay↔execution equivalence.
- **Not** proof that the hierarchical weights alone “solved” RTS — hybrid scaffolding is explicit.

---

## 6. PX1-M04 does not open automatically

**PX1-M04** (*Governed Demo Proof Pack & Winning Video*) opens only under **separate explicit authorization** after **PX1-M03** evidence review — never implicitly from merge or closeout.

---

## 7. Evidence artifacts (operator-local)

After reruns:

- `px1_demo_readiness_evidence.json` + `px1_demo_readiness_evidence_report.json`
- `px1_demo_readiness_operator_note.md`
- `demo_readiness_declaration.md` — exactly one terminal line:
  - `demo-ready-candidate-selected`
  - `no-demo-ready-candidate-within-scope`

---

## 8. Match configuration: hybrid policy

PX1-M03 uses match configs with:

```json
"burnysc2_policy": "px1_m03_hybrid_v1"
```

See `tests/fixtures/px1_m03/match_opponent_profile_*_v2_hybrid.json` (same bounded horizons/seeds as PX1-M02 v2 profiles, plus hybrid policy).

---

## 9. Proof surface: live action tallies

Hybrid runs include `live_action_tallies` on **`match_execution_proof.json`**, e.g.:

- `worker_train_applied` / `worker_train_attempted`
- `supply_structure_applied` / `supply_structure_attempted`
- `military_structure_applied` / `military_structure_attempted`
- `military_unit_applied` / `military_unit_attempted`
- `scout_move_applied`
- `combat_or_attack_move_applied` / `combat_or_attack_move_attempted`
- `other_live_action_applied`

and `live_action_behavior_summary` (first successful game-loop markers and an operator-readable paragraph where applicable).
