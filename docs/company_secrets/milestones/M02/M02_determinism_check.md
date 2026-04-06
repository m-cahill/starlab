# M02 — Determinism check

**Status:** **NOT COMPLETED — blocked (no proof artifacts).**

Two attempts on the **same machine** with the **same** committed config were executed. **Neither run** produced `match_execution_proof.json`, so **no** normalized `artifact_hash` values exist to compare. See `M02_local_execution_note.md` for the failure mode (configured map path not found on disk).

This outcome **does not** prove nondeterminism; it proves **the harness never reached proof emission** for this environment.

---

## Run 1

- **Output directory (intended):** `docs/company_secrets/milestones/M02/_local_runs/run1`
- **`artifact_hash`:** **N/A** — no `match_execution_proof.json` produced (harness exited with error before write).

## Run 2

- **Output directory (intended):** `docs/company_secrets/milestones/M02/_local_runs/run2`
- **`artifact_hash`:** **N/A** — same as run 1.

## Result

- [ ] Hashes match
- [ ] Hashes differ — explanation recorded in milestone summary/audit
- [x] **Neither run produced hashes** — comparison **not applicable** until two successful runs exist

## Notes

STARLAB compares **STARLAB-owned normalized proof hashes**, not raw replay bytes or absolute paths. **Replay binding, benchmarks, canonical run artifacts, and cross-host reproducibility** remain **out of scope** for this check.
