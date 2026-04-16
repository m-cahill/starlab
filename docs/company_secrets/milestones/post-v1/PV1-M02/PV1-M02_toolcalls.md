# PV1-M02 — tool call log

Milestone-local tool/logging surface per `.cursorrules`. Entries record intent; timestamps UTC.

**Status:** **Implementation** — integration branch `pv1-m02-tranche-a-execution-evidence`.

| timestamp (ISO-8601 UTC) | tool / action | purpose | target |
| --- | --- | --- | --- |
| 2026-04-16T00:00:00Z | init | seed milestone log | this file |
| 2026-04-16T12:00:00Z | shell | verify git state before branch | repo root |
| 2026-04-16T12:00:00Z | python | early SC2 / env probe for PV1-M02 precondition | starlab.sc2.env_probe |
| 2026-04-16T16:10:00Z | shell | checkout main, pull, create `pv1-m02-tranche-a-execution-evidence` | git |
| 2026-04-16T16:11:00Z | python | SC2 probe default vs `STARLAB_SC2_ROOT` | env_probe, live_sc2_binary_available |
| 2026-04-16T16:12:00Z | write | add reproducible `pv1_m02_campaign_protocol.json` | tests/fixtures/pv1_m02/ |
| 2026-04-16T16:13:00Z | python | emit M49 contract + preflight | emit_full_local_training_campaign_* |
| 2026-04-16T16:17:00Z | python | run M50/M51 executor `--post-bootstrap-protocol-phases` | execute_full_local_training_campaign |
| 2026-04-16T16:18:00Z | python | emit PV1-M01 index + tranche checkpoint | emit_campaign_observability_index, emit_tranche_checkpoint_receipt |
| 2026-04-16T16:19:00Z | write | operator note `tranche_a_operator_note.md` | out/training_campaigns/pv1_m02_tranche_a_2026_04_16/ |
| 2026-04-16T16:20:00Z | write | runtime contract | docs/runtime/pv1_tranche_a_execution_evidence_v1.md |
| 2026-04-16T16:21:00Z | str_replace | ledger §1 quick scan, roadmap, §11, §23, Start Here | docs/starlab.md |
| 2026-04-16T16:22:00Z | str_replace | governance tests + fixture test | tests/test_governance_*.py |
| 2026-04-16T16:23:00Z | shell | ruff, pytest, mypy | CI validation |
