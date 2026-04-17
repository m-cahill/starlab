# PV1-M04 — toolcalls / CI index

**Status:** **Active implementation** — append tool calls and CI run IDs as work proceeds; **record authoritative PR-head + merge-boundary `main` CI at merge** per project workflow.

| Field | Value |
| --- | --- |
| Milestone | PV1-M04 — Post-Campaign Analysis / Comparative Readout |
| Branch | *TBD* — recommended: `pv1-m04-post-campaign-readout` |
| Opened PR | *TBD* |
| Authoritative PR-head CI | *TBD* |
| Merge-boundary `main` CI | *TBD* |

## Commands (local dev — not CI)

- `ruff check starlab tests`
- `mypy starlab tests`
- `pytest` (plus any new `tests/test_pv1_campaign_readout.py` if added)

## Session log (append-only)

| Timestamp (UTC) | Tool / action | Purpose | Files / targets |
| --- | --- | --- | --- |
| 2026-04-16 | Implementation batch | PV1-M04 emitter + fixtures + ledger + tests | `starlab/training/pv1_post_campaign_readout.py`, `emit_pv1_post_campaign_readout.py`, `docs/runtime/pv1_post_campaign_readout_v1.md`, `docs/starlab.md`, `tests/fixtures/pv1_m04/`, `tests/test_pv1_post_campaign_readout.py`, `tests/test_governance_ci.py`, `PV1-M04_plan.md` |

## Notes

- **No** operator-local campaign execution in CI.
- Fill authoritative CI run IDs when the implementation PR is pushed and merged per `docs/company_secrets/prompts/workflowprompt.md`.
