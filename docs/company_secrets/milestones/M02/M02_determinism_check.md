# M02 — Determinism check

**Status:** **PENDING — not performed in Cursor / CI.**

Two runs on the **same machine** with the **same config** must be executed locally; then compare **normalized** `artifact_hash` values from each `match_execution_proof.json`. See `docs/runtime/match_execution_harness.md`.

Until this section is filled, M02 **must not** be described as having completed the **local deterministic harness proof** in the public ledger.

---

## Run 1 (template)

- Output directory: `<fill>`
- `artifact_hash`: `<fill>`

## Run 2 (template)

- Output directory: `<fill>`
- `artifact_hash`: `<fill>`

## Result (template)

- [ ] Hashes match
- [ ] Hashes differ — explanation recorded in milestone summary/audit

## Notes

STARLAB compares **STARLAB-owned normalized proof hashes**, not raw replay bytes or absolute paths.
