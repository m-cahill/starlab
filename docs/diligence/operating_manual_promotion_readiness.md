# Operating manual promotion readiness (M34 prep)

**Status:** Readiness checklist only — **does not** promote `docs/starlab_operating_manual_v0.md` to canonical **v1**.  
**Authority:** Subordinate to `docs/starlab.md` and `docs/runtime/*` contracts.

## What v0 already covers

- Executive identity and what STARLAB is / is not.  
- Core mental model (runs → lineage → replay planes → state → observation → evaluation).  
- Pointer to `docs/architecture.md` for packages and dependency direction.  
- Installation / `Makefile` targets and clone-to-run pointers.  
- CI tier meanings aligned with `docs/runtime/ci_tiering_field_test_readiness_v1.md`.  
- Field-test operator workflow and diligence session template pointer.  
- Explicit **non-canonical** status: draft, subordinate to the ledger.

## What still blocks canonical v1 promotion

- The ledger (`docs/starlab.md`) must remain the **single public source of truth** for milestone status, proofs, and non-claims; v1 would need a written rule set that does not contradict that hierarchy.  
- Runtime contracts under `docs/runtime/` remain authoritative for artifact shapes; the operating manual must not drift into new product or benchmark claims.  
- A promotion milestone would need explicit scope: version bump, cross-links from the ledger, and governance tests if the manual becomes a required artifact.  
- **M34 explicitly does not** perform v1 promotion (see `docs/starlab.md` §11 non-claims).

## Subordination to `docs/starlab.md`

The operating manual must **not** override:

- Milestone proof statements, CI topology, or deferred-issue resolutions.  
- Benchmark-integrity and live-SC2 **non-claims** unless a future milestone proves them.  
- The authority order in `docs/starlab.md` (vision → bicetb → ledger → README → code).

## Related references

- `docs/starlab_operating_manual_v0.md` — current draft.  
- `docs/audit/DeferredIssuesRegistry.md` — deferred and resolved diligence items.  
- `docs/starlab.md` — public ledger and M34 closeout notes on manual promotion prep.
