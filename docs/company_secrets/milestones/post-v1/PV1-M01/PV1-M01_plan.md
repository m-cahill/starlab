# PV1-M01 — Campaign Observability & Checkpoint Discipline

## Goal

Pre-execution tooling milestone: deterministic **inspection/reference** helpers over existing **M49 / M50 / M51** campaign trees — tranche checkpoint receipts and a campaign-level observability index — without executing campaigns, without fabricating evidence, and without widening v1 non-claims.

## Scope (repo)

- `starlab.training` emitters: `emit_tranche_checkpoint_receipt`, `emit_campaign_observability_index`
- `docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`
- `docs/starlab.md`: ledger (current milestone, PV1 roadmap + evidence surfaces subtable)
- `tests/fixtures/pv1_m01/` + `tests/test_pv1_campaign_observability.py`
- Governance tests for ledger

## Non-goals

No Tranche A execution, no long-run campaigns, no benchmark/equivalence/ladder/live-SC2 claims, no opening PV1-M02 in the ledger.

## Definition of done

See acceptance criteria in the operator handoff; CI green (ruff, mypy, pytest).
