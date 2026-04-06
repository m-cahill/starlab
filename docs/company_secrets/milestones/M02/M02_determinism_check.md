# M02 — Determinism check

**Status:** **COMPLETED for this machine — two proof artifacts, matching hashes.**

Two attempts on the **same machine** with the **same** committed config were executed. **Both runs** produced `match_execution_proof.json` with comparable normalized **`artifact_hash`** values. See `M02_local_execution_note.md` for map retrieval, environment, and commands.

This outcome supports the **narrow** same-config, same-machine harness claim for **STARLAB-owned normalized hashes**. It does **not** prove cross-host reproducibility, replay binding, benchmark validity, or canonical run artifact properties.

---

## Run 1

- **Output directory (intended):** `docs/company_secrets/milestones/M02/_local_runs/run1`
- **`artifact_hash`:** `b23172cb457b7645d796c30cf36baf96229efa3af954190788370ba5ea464e53`

## Run 2

- **Output directory (intended):** `docs/company_secrets/milestones/M02/_local_runs/run2`
- **`artifact_hash`:** `b23172cb457b7645d796c30cf36baf96229efa3af954190788370ba5ea464e53`

## Result

- [x] Hashes match
- [ ] Hashes differ — explanation recorded in milestone summary/audit
- [ ] **Neither run produced hashes** — comparison **not applicable** until two successful runs exist

## Notes

STARLAB compares **STARLAB-owned normalized proof hashes**, not raw replay bytes or absolute paths. **Replay binding, benchmarks, canonical run artifacts, and cross-host reproducibility** remain **out of scope** for this check.
