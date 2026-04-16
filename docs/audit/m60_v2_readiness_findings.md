# M60 — v2 readiness audit findings (concise)

**Authority:** Subordinate to `docs/starlab.md`. This is a **short mapping** of older audit pressure points to **current `main`**, not a second full audit.

## M32-era items already resolved (do not reopen without regression evidence)

| Theme | Resolved by | Evidence (high level) |
| --- | --- | --- |
| Shared JSON I/O | **M34** | `starlab/_io.py`, DIR-003 in `DeferredIssuesRegistry.md` |
| Governance test monolith | **M34** | `tests/test_governance_*.py`, DIR-004 |
| Broad `except Exception` hygiene | **M34** | `docs/audit/broad_exception_boundaries.md`, DIR-005 |
| Dev dependency caps / Dependabot | **M34** | `pyproject.toml`, `.github/dependabot.yml`, DIR-006 |
| CI tiering / field-test artifacts | **M33** | `.github/workflows/ci.yml`, `docs/runtime/ci_tiering_field_test_readiness_v1.md` |
| Coverage gate / CI evidence hardening | **M37** | `pyproject.toml` `fail_under`, M37 closeout |
| Evaluation ↔ state bundle loading | **M35** | `starlab/evaluation/m14_bundle_loader.py` — single loader seam to `canonical_state_inputs` |
| `parser_io` / `replay_slice_generation` size | **M35+** | Split across focused modules (current files are small facades) |

## Current-main revalidation (M60)

- **Cross-layer coupling:** No regression — only `m14_bundle_loader.py` imports `starlab.state` under `starlab/evaluation/`.
- **Oversized hotspot:** `execute_full_local_training_campaign.py` was the largest mixed-responsibility training module; M60 **splits** orchestration helpers into `starlab/training/_full_local_training_campaign_execution.py` (private), preserving CLI and artifact contracts.

## M60 selected structural work

- **Hotspot:** `execute_full_local_training_campaign` (M50/M51 governed executor).
- **Change:** Private helper module for M50 bootstrap-only and M51 protocol phase execution; **no** new public API surface.

## Deferred beyond M61 (not M60)

- **M61** release lock & v1 proof pack (planned).
- **v2** multi-game / broader productization (explicitly after **M61** per ledger).
- Broad cleanup of other large files (e.g. training pipelines) without a scoped milestone charter.
