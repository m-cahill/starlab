# Human benchmark register (v1.5)

**Milestone:** `V15-M01` — public register surface only.

## Purpose

Record **human-panel** and bounded human-benchmark **assets** (protocol bindings, anonymized aggregates, and references to private session records) under v1.5 governance.

## Scope

- `asset_class`: `human_panel_record`, and related `benchmark_asset` rows tied to human evaluation.
- Frozen protocol is **V15-M06**; M01 only provides the **register template**.

## Public / private boundary

**Human identities, raw replays, and session notes** default **private**. Public tables may hold protocol ids, aggregate statistics, and **non-identifying** references when explicitly cleared.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json`.

## Current status

**M01:** Surface only; **no** human benchmark execution claimed.

**V15-M06 (closed on `main`, [PR #127](https://github.com/m-cahill/starlab/pull/127)):** Freezes the **human-panel benchmark protocol** and the **`starlab.v15.human_panel_benchmark.v1`** **fixture** contract (`v15_human_panel_benchmark.json` + report; **authoritative PR-head** CI [`24924293130`](https://github.com/m-cahill/starlab/actions/runs/24924293130); **merge-boundary** [`24924371412`](https://github.com/m-cahill/starlab/actions/runs/24924371412)). It does **not** add real participant **rows** or public human-panel result **assets**; see `docs/runtime/v15_human_panel_benchmark_protocol_v1.md`.

**V15-M11 (closed on `main`, [PR #137](https://github.com/m-cahill/starlab/pull/137)):** Adds the **human panel execution** and **human-benchmark claim-decision** JSON surfaces (`starlab.v15.human_panel_execution.v1`, `starlab.v15.human_benchmark_claim_decision.v1`) and **`docs/runtime/v15_human_panel_bounded_benchmark_v1.md`**. Default honest posture remains **no** public **rows**; **not** a completed human panel in CI; **not** claim-critical public rows; see **`docs/starlab-v1.5.md`** (M11 non-claims). **V15-M12** is **closed** on `main` ([PR #138](https://github.com/m-cahill/starlab/pull/138)) — showcase release-pack surface may **bind** M11 claim-decision JSON by **SHA**; **no** new public human-benchmark **rows** by default (`docs/runtime/v15_showcase_agent_release_pack_v1.md`).

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows.* |

## Non-claims

M01 does **not** support “beats most humans” claims; see `docs/starlab-v1.5.md` standing non-claims.
