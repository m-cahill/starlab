# PX1-M04 — Pack freeze (governance)

**Purpose:** Separate **what PR1 freezes in-repo** from **what operators finalize locally** before closeout.

## Frozen by PR1 (repository)

- Public runtime **`docs/runtime/px1_governed_demo_proof_pack_v1.md`** — vocabulary, non-claims, inventory rules.
- Ledger entries in **`docs/starlab.md`** — **PX1-M04** **open**; **PX1-M03** remains **closed** with successful remediation; **PX1-M05** / **v2** **unopened**.
- Private **`PX1-M04_canonical_demo_selection.md`** — **initial** canonical primary run selection and rationale (revision requires explicit memo update).
- **`PX1-M04_pack_checklist.md`** — acceptance structure for later verification.

## Not frozen by PR1 (operator-local completion)

- Physical copying or mirroring of large binaries into any release tree.
- Final attestation that all hashes were re-verified on a clean machine (done before PR2).

## Revision policy

- Changing the **canonical primary run** after PR1: update **`PX1-M04_canonical_demo_selection.md`** with date, reason, and new references — **no silent edits**.
