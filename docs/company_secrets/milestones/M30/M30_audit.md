# Milestone Audit — M30: First Learned Hierarchical Agent

**Project:** STARLAB  
**Milestone:** M30 — First Learned Hierarchical Agent  
**Merge:** [PR #36](https://github.com/m-cahill/starlab/pull/36) → `main`, merge commit `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf`  
**Authoritative CI:** PR-head [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) (**success**); merge-boundary `main` [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) (**success**)

## Scope discipline

| Check | Result |
| ----- | ------ |
| Offline / replay-derived only | **Pass** — fit consumes governed M26 + M14 bundles via in-process M16→M18 materialization; no live SC2 |
| Two-level hierarchy only | **Pass** — manager (signature→delegate) + worker ((delegate,signature)→label); no extra levels |
| Fixed four-delegate policy only | **Pass** — `DELEGATE_POLICY_ID` = `starlab.m30.delegate.fixed_four_v1`; checked-in map; not learned taxonomy |
| No benchmark / evaluation semantics | **Pass** — no M20 harness, no tournament; report metrics explicitly smoke-only |
| No M31 product | **Pass** — no replay explorer or M31 modules |

## CI truthfulness

* Final PR head `2a27445…` matches authoritative PR-head run **24223946664** (**success**).
* Merge commit `1c3a5f6…` matches merge-boundary push run **24223976390** (**success**).
* No superseded red PR-head cited as merge authority for M30.

## Import / boundary posture

* **Pass** — `tests/test_replay_hierarchical_imitation_agent.py::test_module_ast_import_guard` forbids `starlab.replays`, `starlab.sc2`, `s2protocol` in listed M30 hierarchy modules.

## Non-claims preserved

* Artifact and report **`non_claims`** include benchmark integrity, live SC2, raw action legality, replay execution equivalence, M31 replay explorer product, etc. (see `hierarchical_agent_models.NON_CLAIMS_V1`).

## Widening / creep

* **No** evidence of M31 product code, replay explorer UI, flagship proof pack, or benchmark-integrity claims in M30 scope.

## Ledger / governance

* `docs/starlab.md` updated for M30 closeout (status, §6–§11, §18, §20, §23).
* `M30_run1.md`, `M30_summary.md`, `M30_audit.md` present under `docs/company_secrets/milestones/M30/`.
* **M31** stubs only: `docs/company_secrets/milestones/M31/M31_plan.md`, `M31_toolcalls.md`.

## Verdict

**M30 scope is closed honestly on `main`:** narrow offline learned hierarchical imitation artifact + report, M29 trace compatibility, explicit non-claims, green PR-head + green merge-boundary CI as recorded in `M30_run1.md`.
