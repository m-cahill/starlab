# M51 Plan — Governed Post-Bootstrap Phase Orchestration v1

**Status:** In progress (branch `m51-governed-post-bootstrap-phase-orchestration`).

## Milestone title

**M51 — Governed post-bootstrap phase orchestration v1**

## Objective

Extend the M50 governed campaign executor so it can optionally carry a campaign beyond bootstrap into post-bootstrap phases already described by the M49 protocol: optional weighted refit (separate orchestrated phase), post-refit M42 comparison (honest skip until M41-compatible candidates exist in contract), and one watchable M44 validation on the refit bundle.

## Locked implementation choices (2026-04-14)

- **Refit:** Separate phase after bootstrap; `emit_updated_bundle=False` during bootstrap; aggregate pseudo-label rows from all successfully completed bootstrap phases in execution order.
- **M42:** No harness extension in M51 — skip with `candidate_not_m41_comparison_compatible` when refit-only.
- **Watchable M44:** Refit joblib if refit succeeded; otherwise skip with explicit reason; **no** silent M43 fallback.
- **Receipts:** Per-phase `phase_receipt.json` plus aggregate `phase_receipts` on `hidden_rollout_campaign_run.json`.
- **CLI:** `--post-bootstrap-protocol-phases` (default off = M50 behavior).

## Out of scope

Benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, M42 semantic extension for M45 refit bundles, distributed execution.

## Acceptance

Backward-compatible default; fixture CI tests; documentation updates; non-claims preserved.
