# M02 — Determinism check (template)

**Goal:** Same config, two runs on the **same machine**, compare **normalized** `artifact_hash` in `match_execution_proof.json`.

## Run 1

- Output directory: `run1/`
- `artifact_hash`: `<fill>`

## Run 2

- Output directory: `run2/`
- `artifact_hash`: `<fill>`

## Result

- [ ] Hashes match — local deterministic harness claim is supported for this configuration.
- [ ] Hashes differ — document why (timing, non-deterministic upstream fields, etc.) and **do not** overstate the milestone.

## Notes

STARLAB compares **STARLAB-owned normalized proof hashes**, not raw replay bytes or absolute paths.
