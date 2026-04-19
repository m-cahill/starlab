# PX1-M03 — Plan

**Title:** Candidate Strengthening & Demo Readiness Remediation  
**Status:** Closed (opening [PR #90](https://github.com/m-cahill/starlab/pull/90); closeout [PR #CLOSEOUT_PR_NUM](https://github.com/m-cahill/starlab/pull/CLOSEOUT_PR_NUM))

## Objective

Corrective milestone after **PX1-M02** closed with **`no-candidate-selected`**: strengthen bounded **live** Terran early-game behavior (hybrid macro scaffold + narrow model/bounded combat) for primary candidate **`px1_m01_weighted_refit_rl_bootstrap_v1`**, improve proof readability (categorized tallies + behavior summary), freeze **PX1-M03** remediation protocol, run fresh bounded **`local_live_sc2`** evaluation under frozen rules, close honestly with **`demo-ready-candidate-selected`** or **`no-demo-ready-candidate-within-scope`**.

## Split PRs

1. **PR1 (this branch):** Open **PX1-M03** in `docs/starlab.md`, add public runtime `docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`, private operator/protocol docs, deterministic protocol artifact emitters, bounded code changes (BurnySc2 hybrid + proof tallies), fixtures updated with `burnysc2_policy`, governance tests. **Does not** claim demo-ready outcome.
2. **Operator-local:** Reruns under fresh series root; operator note + declaration.
3. **PR2:** Closeout after evidence exists.

## Locked scope (user)

- Hybrid **(c)**: hard-coded worker / supply / barracks / marine + small model-driven or bounded-rule combat/scout.
- Increment **`action_count`** per successful SC2 command; keep categorized tallies.
- Branch: `px1-m03-candidate-strengthening-demo-readiness`.
- Same candidate id; document enriched live surface only.
- Reuse PX1-M02 opponent v2 fixtures unless grounded reason to change.

## Out of scope

No new industrial campaign, no PX1-M04 auto-open, no v2 open, no live SC2 in default CI, no broad RTS rewrite.
