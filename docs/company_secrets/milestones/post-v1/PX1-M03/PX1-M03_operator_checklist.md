# PX1-M03 — Operator checklist

## PR1 merged (code + ledger open)

1. Confirm `docs/starlab.md` lists **current milestone = PX1-M03**.
2. Read `docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`.
3. Emit frozen protocol JSON pair to evaluation `protocol/` directory.

## Before reruns

1. Verify SC2 + burnysc2 optional extras.
2. Confirm weights + M43 hierarchical run paths (same as PX1-M02 series driver).
3. Run evaluation series (script TBD / extend `scripts/px1_m02_run_evaluation_series.py` pattern for PX1-M03 protocol + evidence filenames) or manual parallel runs.
4. Ensure each run writes:
   - `px1_demo_readiness_operator_note.md`
   - `demo_readiness_declaration.md` (exactly one terminal line from the two allowed outcomes)

## After reruns

1. Emit `px1_demo_readiness_evidence.json` + report from observed aggregates + protocol path.
2. PR2 closeout: ledger + private summary/audit per prompts.
