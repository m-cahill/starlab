# M47 Plan — Bootstrap Episode Distinctness & Operator Ergonomics

**Milestone:** M47  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Branch:** `m47-bootstrap-episode-distinctness-ergonomics` (suggested)  
**Status:** Complete (closed on `main`; see `M47_run1.md` / `M47_summary.md` / `M47_audit.md`)

## Governance recharter (user-directed, 2026-04-13)

The public ledger previously labeled **M47** as **Learned-agent comparison contract-path alignment (stub)**. That scope is **deferred** to **M48** (stub). **M47** is rechartered to **Bootstrap Episode Distinctness & Operator Ergonomics** — formal governance event; see `docs/starlab.md` §23 changelog.

## Objective

Make local multi-episode **M45** campaigns **honest to interpret** and **more likely to produce distinct episode evidence**, without widening STARLAB’s claims.

## In scope

1. **Interpretation rule (docs):** `episode_count_configured` ≠ N independent samples unless governed identities differ; use **`validation_run_sha256`** (minimum) and **`run_id`** (preferred); separate **integration success** from **sample diversity** claims.
2. **Episode diversity (product):** Per-episode M02 **`seed`** = **`bootstrap_base_seed + episode_index`** via copied match config JSON per episode (`bootstrap_match_config.json`); **`starlab.m47.episode_manifest.v2`** with distinctness fields and collapse **warnings**.
3. **Operator guidance:** `docs/runtime/self_play_rl_bootstrap_v1.md` — watchable vs bootstrap-bounded vs extended campaign; what counts as a **good** learning-oriented read.

## Out of scope

- **M42** `--contract` path alignment (**M48** stub)
- Benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder claims
- Large RL features beyond seed/diversity and reporting

## Deliverables

- `docs/runtime/self_play_rl_bootstrap_v1.md`, `docs/starlab.md`
- `starlab/training/self_play_rl_bootstrap_pipeline.py`, `emit_self_play_rl_bootstrap_run.py`, `self_play_rl_bootstrap_io.py`, `self_play_rl_bootstrap_models.py`
- Tests: `tests/test_m45_self_play_rl_bootstrap.py`, governance tests
- `docs/company_secrets/milestones/M48/` stub only

## Acceptance

See user prompt acceptance criteria; CI fixture-only; no live SC2 in CI.
