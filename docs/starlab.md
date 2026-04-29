# STARLAB — Canonical Project Ledger

**Governance recharter (2026-04-13 — user-directed):** The ledger stub **M47 — Learned-agent comparison contract-path alignment** was **deferred** to **M48** (**now closed** on `main`). **M47** was rechartered to **Bootstrap Episode Distinctness & Operator Ergonomics** — M45 multi-episode **interpretation** rules, **per-episode** M02 `seed` (`bootstrap_base_seed + episode_index`), **`starlab.m47.episode_manifest.v2`**, distinctness/collapse reporting, and operator guidance — **not** benchmark integrity; **M42** contract-path alignment delivered as **M48** (see **M48** / **M49** below).

**M47 — Bootstrap Episode Distinctness & Operator Ergonomics:** **closed** on `main` ([PR #58](https://github.com/m-cahill/starlab/pull/58); merge commit `ebc5de0864ef6231d13efa741150d73c1ef1b98b`; merged **2026-04-14T00:47:56Z** (UTC); **final PR head** `4a8fb3e2f7aad95d2cde5b6b77577db25e42e91e`; **authoritative PR-head CI** [`24374720293`](https://github.com/m-cahill/starlab/actions/runs/24374720293); **merge-boundary `main` CI** [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on merge commit `ebc5de0…` — **success**; tag **`v0.0.47-m47`**; branch `m47-bootstrap-episode-distinctness-ergonomics` **retained** on `origin`; see §18 / `M47_run1.md`). **Narrow:** per-episode M02 **`seed`**, **`starlab.m47.episode_manifest.v2`**, **`episode_distinctness`** / collapse **warnings**, operator/runtime interpretation — **not** benchmark integrity.

**M48 — Learned-agent comparison contract-path alignment:** **closed** on `main` ([PR #59](https://github.com/m-cahill/starlab/pull/59); merge commit `cdd023cb388ae99c3649978857e07af04c17df50`; merged **2026-04-14T02:21:43Z** (UTC); **final PR head** `d94bc02c78bf75605edc4d28473f48cac986e53c`; **authoritative PR-head CI** [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299); **merge-boundary `main` CI** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on merge commit `cdd023c…` — **success**; tag **`v0.0.48-m48`**; branch `m48-learned-agent-comparison-contract-path-alignment` **deleted** after merge; see §18 / `M48_run1.md`). **Narrow:** **`--benchmark-contract`** (M20; alias **`--contract`**); optional **`--training-program-contract`** (M40 on-disk JSON); **strict** M41-recorded `training_program_contract_sha256` / `training_program_contract_version` vs active M40 — **`ValueError`** on mismatch. Runtime: `docs/runtime/learned_agent_comparison_harness_v1.md`.

**M49 — Full local training / bootstrap campaign charter & evidence protocol:** **closed** on `main` ([PR #60](https://github.com/m-cahill/starlab/pull/60); merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed`; **final PR head** `2780de11bccd6a51cba3a1d14b24a0433e776873`; **authoritative PR-head CI** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623); **merge-boundary `main` CI** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) — **success**; tag **`v0.0.49-m49`**; branch `m49-full-local-training-campaign-charter` **deleted** after merge; see §18 / `M49_run1.md`). Governed campaign contract + preflight receipt (`starlab.training` emitters), runtime `docs/runtime/full_local_training_campaign_v1.md` — **charter / preflight only**; **not** proof that a long local campaign was executed; **not** automatic execution or success of operator runs.

**M50 — Industrial-scale hidden rollout mode & governed campaign execution v1:** **closed** on `main` ([PR #61](https://github.com/m-cahill/starlab/pull/61); merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b`; merged **2026-04-14T21:48:43Z** (UTC); **final PR head** `a6f0b90045a01908d4a57682bd41743826e5d543`; **authoritative PR-head CI** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763); **merge-boundary `main` CI** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) on merge commit `a0430d3…` — **success**; tag **`v0.0.50-m50`**; branch `m50-industrial-hidden-rollout-mode` **retained** on `origin`; see §18 / `M50_run1.md`). **Narrow:** governed campaign executor over M49 + M45 phases, PID lockfiles, honest requested vs resolved visibility, extended execution preflight, heartbeat / stop / quarantine-first resume — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance.

**M51 — Governed post-bootstrap phase orchestration v1:** **closed** on `main` ([PR #62](https://github.com/m-cahill/starlab/pull/62); merge commit `1e88466eb2635385b7ad56e666c45436a12f0b59`; merged **2026-04-15T00:14:35Z** (UTC); **final PR head** `f812f8098608f8c3ae45c51f12f8f40f7fbe083c`; **authoritative PR-head CI** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222); **merge-boundary `main` CI** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on merge commit `1e88466…` — **success**; tag **`v0.0.51-m51`**; branch `m51-governed-post-bootstrap-phase-orchestration` **deleted** after merge; see §18 / `M51_run1.md`). **Narrow:** optional `--post-bootstrap-protocol-phases` on the campaign executor (aggregated weighted refit phase, orchestrated M42 skip with `candidate_not_m41_comparison_compatible`, one watchable M44 on refit weights; `hidden_rollout_campaign_run.v2`, per-phase `phase_receipt.json`) — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance, **not** extension of M42 to treat M45 refit bundles as M41 candidates.

**M52 — V1 endgame recharter & replay↔execution equivalence charter v1:** **closed** on `main` ([PR #63](https://github.com/m-cahill/starlab/pull/63); merge commit `c80a47bedcc5e607e45381d401411d9aa5e2f10b`; merged **2026-04-15T03:41:47Z** (UTC); **final PR head** `11ba11e0c1bcb39baaec130105a1955cfcf4d703`; **authoritative PR-head CI** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983); **merge-boundary `main` CI** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on merge commit `c80a47b…` — **success**; tag **`v0.0.52-m52`**; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge; see §18 / `M52_run1.md`). **Narrow:** ledger recharter **M00**–**M61**; Phase VII; runtime `docs/runtime/replay_execution_equivalence_charter_v1.md`; `starlab.equivalence` deterministic charter/report JSON — **not** paired replay↔execution proof, **not** benchmark integrity, **not** live SC2 in CI, **not** ladder/public performance.

**M53 — Replay↔execution equivalence evidence surface v1:** **closed** on `main` ([PR #64](https://github.com/m-cahill/starlab/pull/64); merge commit `99bd43da41ac5a4d22a3eb2f438bc8ebe93b591d`; merged **2026-04-15T05:39:22Z** (UTC); **final PR head** `ec166ff4108af939755d5578a408b07e6a9d6bb1`; **authoritative PR-head CI** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924); **merge-boundary `main` CI** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on merge commit `99bd43d…` — **success**; tag **`v0.0.53-m53`**; branch `m53-replay-execution-equivalence-evidence-surface` **deleted** after merge; see §18 / `M53_run1.md`). **Narrow:** runtime `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`; `starlab.equivalence` deterministic `replay_execution_equivalence_evidence.json` / report; profile **`starlab.m53.profile.identity_binding_v1`**; explicit artifact-path CLI — **not** universal replay↔execution equivalence, **not** M54 audit gates, **not** benchmark integrity, **not** live SC2 in CI, **not** ladder/public performance.

**M54 — Replay↔execution equivalence audit & acceptance gates v1:** **closed** on `main` ([PR #65](https://github.com/m-cahill/starlab/pull/65); merge commit `773dd1982f28f92512785ce0ab349b7c625f4c3d`; merged **2026-04-15T07:38:15Z** (UTC); **final PR head** `70f4f2d51049948197863e76e806cc1adbc903aa`; **authoritative PR-head CI** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561); **merge-boundary `main` CI** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on merge commit `773dd19…` — **success**; tag **`v0.0.54-m54`**; branch `m54-replay-execution-equivalence-audit-acceptance-gates` **deleted** after merge; see §18 / `M54_run1.md`). **Narrow:** runtime `docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md`; `starlab.equivalence` deterministic `replay_execution_equivalence_audit.json` / report; gate pack **`starlab.m54.gatepack.identity_binding_acceptance_v1`**; profile-scoped `profile_scope_status` + descriptive `merge_bar_language` only — **not** global replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** ladder/public performance, **not** repository branch-protection automation.

**M55 — Benchmark integrity charter & split-governance controls v1:** **closed** on `main` ([PR #66](https://github.com/m-cahill/starlab/pull/66); merge commit `625dd756f09ceb4aebe8d5f3c60ea216f9cab98e`; merged **2026-04-15T19:01:02Z** (UTC); **final PR head** `f7b1306de78b0a27b7f6095be55125630ded0aaa`; **authoritative PR-head CI** [`24472349322`](https://github.com/m-cahill/starlab/actions/runs/24472349322); **merge-boundary `main` CI** [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on merge commit `625dd75…` — **success**; tag **`v0.0.55-m55`**; branch `m55-benchmark-integrity-charter-split-governance-controls` **retained** on `origin`; superseded **failure** PR-head [`24472253485`](https://github.com/m-cahill/starlab/actions/runs/24472253485) — Ruff format — **not** merge authority). **Narrow:** runtime `docs/runtime/benchmark_integrity_charter_v1.md`; `starlab.benchmark_integrity` deterministic charter/report JSON; contract **`starlab.benchmark_integrity_charter.v1`** — **charter, vocabulary, and split_governance_controls only** — **not** benchmark integrity proved; **not** M56 evidence/reproducibility gates; **not** a substitute for **M52**–**M54** replay↔execution equivalence.

**M56 — Benchmark integrity evidence & reproducibility gates v1:** **closed** on `main` ([PR #67](https://github.com/m-cahill/starlab/pull/67); merge commit `bd7da9a6229fa067217dd04db918972a5ec73caf`; merged **2026-04-15T20:07:56Z** (UTC); **final PR head** `2c5d23b063f42bddecdc175721e8233e71938984`; **authoritative PR-head CI** [`24474743293`](https://github.com/m-cahill/starlab/actions/runs/24474743293); **merge-boundary `main` CI** [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843) on merge commit `bd7da9a…` — **success**; tag **`v0.0.56-m56`**; branch `m56-benchmark-integrity-evidence-reproducibility-gates` **retained** on `origin`; superseded **failure** PR-head [`24474659745`](https://github.com/m-cahill/starlab/actions/runs/24474659745) — Ruff format — **not** merge authority). **Narrow:** runtime `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md`; `starlab.benchmark_integrity` deterministic evidence + reproducibility gates JSON; **exactly one** bounded scope **`starlab.m56.scope.fixture_only_baseline_chain_v1`**; **exactly one** gate pack **`starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`** — **fixture-only offline M21–M25 chain** — **not** global benchmark integrity proof; **not** substitution for **M52**–**M54** replay↔execution equivalence.

**M57 — Narrow live SC2 in CI charter & controlled runner v1:** **closed** on `main` ([PR #68](https://github.com/m-cahill/starlab/pull/68); merge commit `29c383f85f380d2eb2a6b2a411aa7c3262f2bc0d`; merged **2026-04-15T21:32:49Z** (UTC); **final PR head** `eaff0104f140c2468bc6382984cd7e25f7323aa7`; **authoritative PR-head CI** [`24479060243`](https://github.com/m-cahill/starlab/actions/runs/24479060243); **merge-boundary `main` CI** [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on merge commit `29c383f…` — **success**; tag **`v0.0.57-m57`**; branch `m57-live-sc2-in-ci-charter-controlled-runner` **retained** on `origin`; see §18 / `M57_run1.md`). **Narrow:** runtime `docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md`; `starlab.sc2` charter + controlled-runner receipt wrapping **`run_local_live_play_validation`** (**M44**); **exactly one** runner profile **`starlab.m57.runner_profile.m44_single_validation_v1`**; **M43** candidates + explicit weights only; optional **`.github/workflows/live-sc2-controlled-runner.yml`** (`workflow_dispatch` only) — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof; **not** substitution for **M52**–**M54** replay↔execution equivalence; **not** benchmark integrity.

**M58 — Live SC2 in CI hardening & cost guardrails v1:** **closed** on `main` ([PR #69](https://github.com/m-cahill/starlab/pull/69); merge commit `3a6f13910dc8056cb0d88161796dd5fe7888629d`; merged **2026-04-16T01:14:18Z** (UTC); **final PR head** `4d8fa3e6cb067b9784efc01f7668f777078b5a2d`; **authoritative PR-head CI** [`24485185914`](https://github.com/m-cahill/starlab/actions/runs/24485185914); **merge-boundary `main` CI** [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247) on merge commit `3a6f139…` — **success**; tag **`v0.0.58-m58`**; branch `m58-live-sc2-in-ci-hardening-cost-guardrails` **retained** on `origin`; see §18 / `M58_run1.md`). **Narrow:** hardens the **closed M57** surface only — **one** guardrail profile **`starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1`**; deterministic guardrails + preflight receipts; hardened optional **`workflow_dispatch`** workflow — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof; **not** ladder/public **performance** proof (**M59** is the separate bounded descriptive protocol + evidence layer — see below).

**M59 — Ladder/public evaluation protocol & evidence surface v1:** **closed** on `main` ([PR #70](https://github.com/m-cahill/starlab/pull/70); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; merged **2026-04-16T02:45:33Z** (UTC); **final PR head** `074598af81b1c4ce7f3702b4002daacf9adb6bf3`; **authoritative PR-head CI** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360); **merge-boundary `main` CI** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on merge commit `319bc3d…` — **success**; tag **`v0.0.59-m59`**; branch `m59-ladder-public-evaluation-protocol-evidence-surface-v1` **deleted** after merge; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority; see §18 / `M59_run1.md`). **Narrow:** runtime `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md`; `starlab.sc2` deterministic **`ladder_public_evaluation_protocol.json`** / **`ladder_public_evaluation_protocol_report.json`** + **`ladder_public_evaluation_evidence.json`** / **`ladder_public_evaluation_evidence_report.json`**; bounded profile **`starlab.m59.protocol_profile.single_candidate_public_eval_v1`** — **not** ladder/public **performance** proof; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion.

**M60 — Audit hardening & v2 readiness v1:** **closed** on `main` ([PR #71](https://github.com/m-cahill/starlab/pull/71); merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`; merged **2026-04-16T03:57:51Z** (UTC); **final PR head** `c7f615639bc1b26d6d2813bc55f078a048cab405`; **authoritative PR-head CI** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150); **merge-boundary `main` CI** [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939) on merge commit `9ef4e04…` — **success**; tag **`v0.0.60-m60`** on merge commit `9ef4e04…`; branch `m60-audit-hardening-v2-readiness` **deleted** after merge; see §18). **Narrow:** structural/diligence — `docs/audit/m60_v2_readiness_findings.md`, `docs/runtime/v2_readiness_audit_hardening_v1.md`, private **`starlab.training._full_local_training_campaign_execution`**, **`tests/test_m60_v2_readiness_guardrails.py`** — **not** a new governed product artifact family; **not** replay↔execution equivalence; **not** benchmark integrity; **not** live SC2 in CI; **not** ladder/public performance.

**M61 — SC2 foundation release lock & v1 proof pack:** **closed** on `main` ([PR #72](https://github.com/m-cahill/starlab/pull/72); merge commit `35d7734d14113adf206390f153f517a93d7d41ba` merged **2026-04-16T05:33:27Z** (UTC); **final PR head** `bb5a216e83f6048cfa0ad9b437d74d367ff59a5b`; **authoritative PR-head CI** [`24493016581`](https://github.com/m-cahill/starlab/actions/runs/24493016581); **merge-boundary `main` CI** [`24493963087`](https://github.com/m-cahill/starlab/actions/runs/24493963087) on merge commit `35d7734…` — **success**; tag **`v0.0.61-m61`** on merge commit `35d7734…`). **In repo:** `starlab.release_lock` proof pack + audit emitters; `docs/runtime/sc2_foundation_release_lock_v1.md`. **Operator-local evidence (2026-04-16):** governed **M49→M50→M51** campaign **`m61_evidence_2026_04_16_a`**, execution **`m61_exec_001`**, **`--post-bootstrap-protocol-phases`**, weighted refit, watchable **M44** + replay; deterministic proof pack + audit with **`release_scope_status`: `ready_within_scope`** (representative proof_pack_sha256 **`9b505f8a930a61b44aacb1f875525c201ad202a304908bbc56b2f417a45d7bea`** — raw tree under **`out/`**, **not** committed). **Narrow:** bounded **v1** release lock within **M61** declared scope — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance. **No M62** stub — any **v2** work requires explicit recharter (**not** a continuation of **M00–M61** numbering). Post-v1 phases use **`PV1-MNN`** / **`PX1-MNN`** (**not** **M62**). **Post-v1 (PV1)** (closed) and **Post-PV1 (PX1)** roadmaps: see sections below §7. See §11; local-only closeout under `docs/company_secrets/milestones/M61/`.

**M46 — Bounded live validation final-status semantics:** **closed** on `main` ([PR #57](https://github.com/m-cahill/starlab/pull/57); merge commit `b925130d2e6bb9b2586139b17d100285e89b8e54`; merged **2026-04-13T18:12:03Z** (UTC); **final PR head** `ddb18f4cf5e74af2cf3a0f657b66911c93bb97a8`; **authoritative PR-head CI** [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005); **merge-boundary `main` CI** on merge commit [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) — **failure** (`pip-audit` / pytest CVE — **not** M46 semantics); **repaired green `main` CI** [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) on `1b7b25e…` (pytest **≥9.0.3** — CI hygiene); tag **`v0.0.46-m46`**; **post-closeout `main` CI** [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) on `1b33acd…` — **success** (ledger + tag push — **not** PR #57 merge authority); branch `recharter/m44-bounded-live-final-status-semantics` **retained** on `origin`; see §18 / `M46_run1.md`). **Narrow:** bounded **burnysc2** harness runs emit `match_execution.final_status="ok"` at bounded step-cap exit; literal SC2 `Result` in **`sc2_game_result`** — **not** match victory, **not** ladder strength, **not** benchmark integrity, **not** live SC2 in CI.

**Status:** **v1 planned foundation-completion arc complete** — **M00–M61** **closed** on `main` (see §7 / §11). **M61** — SC2 foundation release lock — **closed** with merge + first-class operator-local campaign evidence and **`ready_within_scope`** audit (see §11). **No M62** stub. **M60** — **Audit hardening & v2 readiness v1** — **closed** on `main` ([PR #71](https://github.com/m-cahill/starlab/pull/71); merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`; **authoritative PR-head CI** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150); **merge-boundary `main` CI** [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939); tag **`v0.0.60-m60`**). **M59** — **Ladder/public evaluation protocol & evidence surface v1** — **closed** on `main` ([PR #70](https://github.com/m-cahill/starlab/pull/70); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; authoritative **PR-head CI** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360); **merge-boundary `main` CI** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014); tag **`v0.0.59-m59`** on merge commit `319bc3d…` — **success**; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority). **Phase VII** — **not** ladder/public **performance** proof; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion; **not** satisfied by **M58** guardrails/preflight alone as ladder evidence. **M58** — **Live SC2 in CI hardening & cost guardrails v1** — **closed** on `main` ([PR #69](https://github.com/m-cahill/starlab/pull/69); merge commit `3a6f13910dc8056cb0d88161796dd5fe7888629d`; **final PR head** `4d8fa3e6cb067b9784efc01f7668f777078b5a2d`; **authoritative PR-head CI** [`24485185914`](https://github.com/m-cahill/starlab/actions/runs/24485185914); **merge-boundary `main` CI** [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247); tag **`v0.0.58-m58`**; see §18 / `M58_run1.md`). **M57** — **Narrow live SC2 in CI charter & controlled runner v1** — **closed** on `main` ([PR #68](https://github.com/m-cahill/starlab/pull/68); merge commit `29c383f85f380d2eb2a6b2a411aa7c3262f2bc0d`; merged **2026-04-15T21:32:49Z** (UTC); **final PR head** `eaff0104f140c2468bc6382984cd7e25f7323aa7`; **authoritative PR-head CI** [`24479060243`](https://github.com/m-cahill/starlab/actions/runs/24479060243); **merge-boundary `main` CI** [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on merge commit `29c383f…` — **success**; tag **`v0.0.57-m57`**; see §18 / `M57_run1.md`). **Narrow:** one runner profile **`starlab.m57.runner_profile.m44_single_validation_v1`**; **M43** + explicit weights; **M44** wrap — **not** M52–M54 equivalence substitute. **M56** — **Benchmark integrity evidence & reproducibility gates v1** — **closed** on `main` ([PR #67](https://github.com/m-cahill/starlab/pull/67); merge commit `bd7da9a6229fa067217dd04db918972a5ec73caf`; **final PR head** `2c5d23b063f42bddecdc175721e8233e71938984`; **authoritative PR-head CI** [`24474743293`](https://github.com/m-cahill/starlab/actions/runs/24474743293); **merge-boundary `main` CI** [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843); tag **`v0.0.56-m56`**; see §18 / `M56_run1.md` — **not** global benchmark integrity proof; **not** substitution for **M52**–**M54** replay↔execution equivalence). **M55** — **Benchmark integrity charter & split-governance controls v1** — **closed** on `main` ([PR #66](https://github.com/m-cahill/starlab/pull/66); merge commit `625dd756f09ceb4aebe8d5f3c60ea216f9cab98e`; merged **2026-04-15T19:01:02Z** (UTC); **final PR head** `f7b1306de78b0a27b7f6095be55125630ded0aaa`; **authoritative PR-head CI** [`24472349322`](https://github.com/m-cahill/starlab/actions/runs/24472349322); **merge-boundary `main` CI** [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on merge commit `625dd75…` — **success**; tag **`v0.0.55-m55`**; branch `m55-benchmark-integrity-charter-split-governance-controls` **retained** on `origin`; superseded **failure** PR-head [`24472253485`](https://github.com/m-cahill/starlab/actions/runs/24472253485) — Ruff format — **not** merge authority for final head; see §18 / `M55_run1.md` — **charter-only** — **not** benchmark integrity proved; **not** a substitute for closed **M52**–**M54** replay↔execution equivalence). **M54** — **Replay↔execution equivalence audit & acceptance gates v1** — **closed** on `main` ([PR #65](https://github.com/m-cahill/starlab/pull/65); merge commit `773dd1982f28f92512785ce0ab349b7c625f4c3d`; **final PR head** `70f4f2d51049948197863e76e806cc1adbc903aa`; **authoritative PR-head CI** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561); **merge-boundary `main` CI** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865); tag **`v0.0.54-m54`**; see §18 / `M54_run1.md`). Deterministic audit JSON + report over **M53** evidence; gate pack **`starlab.m54.gatepack.identity_binding_acceptance_v1`**; profile-scoped outcomes + descriptive merge-bar language only — **not** universal replay↔execution equivalence, **not** benchmark integrity. Folder: `docs/company_secrets/milestones/M54/`. **M53** — **Replay↔execution equivalence evidence surface v1** — **closed** on `main` ([PR #64](https://github.com/m-cahill/starlab/pull/64); merge commit `99bd43da41ac5a4d22a3eb2f438bc8ebe93b591d`; merged **2026-04-15T05:39:22Z** (UTC); **final PR head** `ec166ff4108af939755d5578a408b07e6a9d6bb1`; **authoritative PR-head CI** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924); **merge-boundary `main` CI** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334); tag **`v0.0.53-m53`**; branch `m53-replay-execution-equivalence-evidence-surface` **deleted** after merge; see §18 / `M53_run1.md`). Runtime `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`; `python -m starlab.equivalence.emit_replay_execution_equivalence_evidence` — bounded **evidence** JSON + report — **not** M54 audit gates, **not** universal replay↔execution equivalence. Folder: `docs/company_secrets/milestones/M53/`. **M52** — **V1 endgame recharter & replay↔execution equivalence charter v1** — **closed** on `main` ([PR #63](https://github.com/m-cahill/starlab/pull/63); merge commit `c80a47bedcc5e607e45381d401411d9aa5e2f10b`; **final PR head** `11ba11e0c1bcb39baaec130105a1955cfcf4d703`; **authoritative PR-head CI** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983); **merge-boundary `main` CI** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211); tag **`v0.0.52-m52`**; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge; see §18 / `M52_run1.md`). **M51** — **Governed post-bootstrap phase orchestration v1** — **closed** on `main` ([PR #62](https://github.com/m-cahill/starlab/pull/62); merge commit `1e88466eb2635385b7ad56e666c45436a12f0b59`; **final PR head** `f812f8098608f8c3ae45c51f12f8f40f7fbe083c`; **authoritative PR-head CI** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222); **merge-boundary `main` CI** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114); tag **`v0.0.51-m51`**; branch `m51-governed-post-bootstrap-phase-orchestration` **deleted** after merge; see §18 / `M51_run1.md`). **M50** — **Industrial-scale hidden rollout mode & governed campaign execution v1** — **closed** on `main` ([PR #61](https://github.com/m-cahill/starlab/pull/61); merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b`; **final PR head** `a6f0b90045a01908d4a57682bd41743826e5d543`; **authoritative PR-head CI** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763); **merge-boundary `main` CI** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487); tag **`v0.0.50-m50`**; branch `m50-industrial-hidden-rollout-mode` **retained** on `origin`; see §18 / `M50_run1.md`). Governed executor, PID locks, honest visibility posture, extended preflight — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance. **M49** — **Full local training / bootstrap campaign charter & evidence protocol** — **closed** on `main` ([PR #60](https://github.com/m-cahill/starlab/pull/60); merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed`; **final PR head** `2780de11bccd6a51cba3a1d14b24a0433e776873`; **authoritative PR-head CI** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623); **merge-boundary `main` CI** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315); tag **`v0.0.49-m49`**; branch `m49-full-local-training-campaign-charter` **deleted** after merge; see §18 / `M49_run1.md`). **M48** — **Learned-agent comparison contract-path alignment** — **closed** on `main` ([PR #59](https://github.com/m-cahill/starlab/pull/59); merge commit `cdd023cb388ae99c3649978857e07af04c17df50`; **final PR head** `d94bc02c78bf75605edc4d28473f48cac986e53c`; **authoritative PR-head CI** [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299); **merge-boundary `main` CI** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946); tag **`v0.0.48-m48`**; branch `m48-learned-agent-comparison-contract-path-alignment` **deleted**; see §18 / `M48_run1.md`). **M47** — **Bootstrap Episode Distinctness & Operator Ergonomics** — **closed** on `main`. **M46** **closed** on `main`. **M45** — **Self-Play / RL Bootstrap v1** — **closed** on `main` ([PR #56](https://github.com/m-cahill/starlab/pull/56); **final PR head** `0e89081cd786b527951a98eb3e63b7677f8c8c00`; **authoritative PR-head CI** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292); **merge commit** `1a585b68ea7413852ce78c220c6512bba6a004d7`; merged **2026-04-12T20:07:19Z** (UTC); **merge-boundary `main` CI** [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180); tag **`v0.0.45-m45`**; **superseded** **failure** PR-head [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — Ruff format — **not** merge authority; see §18 / `M45_run1.md`). **M00–M61** is **closed** on `main` (Phase VI training / execution track **M40**–**M51** includes **M51** post-bootstrap orchestration; **M52** closes Phase VII replay↔execution **charter** milestone; **M53** closes Phase VII replay↔execution **evidence surface**; **M54** closes Phase VII **profile-scoped audit / acceptance-gate** layer over M53 evidence; **M55** closes Phase VII **benchmark-integrity charter + split-governance controls**; **M56** closes Phase VII **benchmark-integrity bounded evidence + reproducibility gates** (fixture-only baseline chain — **not** global benchmark integrity proof); **M57** closes Phase VII **narrow live-SC2-in-CI charter + controlled runner** (bounded **M44** wrap — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof); **M58** closes Phase VII **live-SC2-in-CI hardening + cost guardrails** around the same **M57** surface — **not** widening live-SC2 claim boundary; **not** universal replay↔execution equivalence); **M59** closes Phase VII **bounded descriptive ladder/public evaluation protocol + evidence** — **not** ladder/public **performance** proof; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion); **M60** closes Phase VII **audit hardening & v2 readiness** (structural/diligence — private campaign executor split + guardrails + short audit mapping — **not** new governed product artifact family; **not** equivalence/benchmark/ladder/live-SC2 performance claims); **M61** closes Phase VII **SC2 foundation release lock** with operator-local proof pack + audit **`ready_within_scope`** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance. The *Remaining v1 proof-track map* below is **historical** — all Phase VII rows are **complete** on `main`. Narrow bounded proof: first **governed self-play / RL bootstrap** surface (`starlab.training` + **M44** rollout substrate); **local-first**; **fixture-only** SC2 in **CI** — **not** benchmark integrity, **not** replay↔execution equivalence, **not** ladder performance. The **Phase VI integrated test campaign** remains a **post-M45** operator-local follow-on — see `docs/diligence/phase_vi_integrated_test_campaign.md`. **M44** — **Local Live-Play Validation Harness v1** — **merged** to `main` ([PR #55](https://github.com/m-cahill/starlab/pull/55); **final PR head** `dc8e74d98701c6080e525b8a79aa7aa4b7872867`; **authoritative PR-head CI** [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411); **merge commit** `1b1067ad632643d2b14da05d510a7c2a263cc8ea`; merged **2026-04-12T18:13:50Z** (UTC); **merge-boundary `main` CI** [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884); tag **`v0.0.44-m44`** on merge commit `1b1067a…`; branch `m44-local-live-play-validation-harness-v1` **retained** on `origin`; **superseded** **failure** PR-head [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) on `c8b989a…` — Ruff format — **not** merge authority; see §18 / `M44_run1.md`; closeout `M44_summary.md` / `M44_audit.md`). **M43** — **Hierarchical Training Pipeline v1** — **merged** to `main` ([PR #54](https://github.com/m-cahill/starlab/pull/54); **final PR head** `ffc428454939702fbe9c100ace9e109ee0c51605`; **authoritative PR-head CI** [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558); **merge commit** `8850e378a584c9821eeab3e8c72bc499d590b308`; merged **2026-04-12T07:25:40Z** (UTC); **merge-boundary `main` CI** [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897); tag **`v0.0.43-m43`** on merge commit `8850e37…`; superseded PR-head runs on feature branch — [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — **not** merge authority for final head `ffc4284…`; see §18 / `M43_run1.md`; closeout `M43_summary.md` / `M43_audit.md`). **M42** — **Learned-Agent Comparison Harness v1** — **merged** to `main` ([PR #53](https://github.com/m-cahill/starlab/pull/53); **final PR head** `191a95511a7428b0c12c79edc978070c406ad736`; **authoritative PR-head CI** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553); **merge commit** `3eb091aba832cb0a66066d6fca6db091eb53c8f5`; merged **2026-04-12T06:02:16Z** (UTC); **merge-boundary `main` CI** [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842); tag **`v0.0.42-m42`** on merge commit `3eb091a…`; branch `m42-learned-agent-comparison-harness-v1` **deleted** after merge; superseded PR-head runs: none — sole run on final head; see §18 / `M42_run1.md`; closeout `M42_summary.md` / `M42_audit.md`). **M41** — **Replay-Imitation Training Pipeline v1** — **merged** to `main` ([PR #52](https://github.com/m-cahill/starlab/pull/52); **final PR head** `7c092eda7fe6554a2168968ffddbe37e929159e4`; **authoritative PR-head CI** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733); **merge commit** `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`; merged **2026-04-12T02:58:11Z** (UTC); **merge-boundary `main` CI** [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820); tag **`v0.0.41-m41`** on merge commit `5e0add12…`; branch `m41-replay-imitation-training-pipeline-v1` **retained** on `origin`; superseded PR-head runs on that branch — [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190) on `4f85583…`, [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — **not** merge authority for final head `7c092ed…`; see §18 / `M41_run1.md`; closeout `M41_summary.md` / `M41_audit.md`). **M40** — **Agent Training Program Charter & Artifact Contract** — **merged** to `main` ([PR #51](https://github.com/m-cahill/starlab/pull/51); **final PR head** `be47d913737f322bbf8e9e08a672561c71d322eb`; **authoritative PR-head CI** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784); **merge commit** `44e8edc5bcce8dc99576bf2be542b273095e5072`; **merge-boundary `main` CI** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123); tag **`v0.0.40-m40`** on merge commit `44e8edc…`; superseded PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) on `6690cd7f0ae79abe0db85695a0d20b4d7c48cdaf` — Ruff format — **not** merge authority; see §18 / `M40_run1.md`; closeout `M40_summary.md` / `M40_audit.md`). **Post-M39 training roadmap:** after **M39** closeout, the program **rechartered** Phase VI from the former two-stub plan (substrate review; platform boundary charter) into a **six-milestone governed training sequence** (**M40**–**M45**); the earlier Phase VI stub concepts are **deferred beyond the current active arc** (§19). **M39** — **Public Flagship Proof Pack** — **merged** to `main` ([PR #50](https://github.com/m-cahill/starlab/pull/50); **final PR head** `2c3fce7d3820bbfdfb655deedd3c0bb980ddc45b`; **authoritative PR-head CI** [`24292861437`](https://github.com/m-cahill/starlab/actions/runs/24292861437); **merge commit** `ca97027cf1827942a25c886f04b5db56b8b9fe7b`; **merge-boundary `main` CI** [`24293162871`](https://github.com/m-cahill/starlab/actions/runs/24293162871); tag **`v0.0.39-m39`** on merge commit `ca97027…`; see §18 / `M39_run1.md`; closeout `M39_summary.md` / `M39_audit.md`). **M38** — **Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening** — **merged** to `main` ([PR #49](https://github.com/m-cahill/starlab/pull/49); **authoritative PR-head CI** [`24272425346`](https://github.com/m-cahill/starlab/actions/runs/24272425346) on `3e00641…`; **merge-boundary post-merge `main` CI** [`24291882960`](https://github.com/m-cahill/starlab/actions/runs/24291882960) on `bf6bf4a…`; tag **`v0.0.38-m38`** on merge commit `bf6bf4a…`; superseded PR-head: none recorded — **not** merge authority; see §18 / `M38_run1.md`). **M37** — **Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening** — **merged** to `main` ([PR #48](https://github.com/m-cahill/starlab/pull/48); **authoritative PR-head CI** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) on `a38d3a7…`; **merge-boundary post-merge `main` CI** [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) on `d2474bd…`; tag **`v0.0.37-m37`** on merge commit `d2474bd…`; superseded **failure** PR-head [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — **not** merge authority; see §18 / `M37_run1.md`). The program is running a **three-milestone audit/flagship campaign** (**M37**–**M39**; **M37**–**M38** complete): reaching **~85%** test coverage (line + branch in CI) is a **stretch target**, not a guaranteed claim at any milestone boundary. **M36** — **Audit Closure V — Governance Surface Rationalization and Documentation Density Control** — **merged** to `main` ([PR #47](https://github.com/m-cahill/starlab/pull/47); **authoritative green PR-head CI** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **merge-boundary post-merge `main` CI** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; tag **`v0.0.36-m36`** on merge commit `e73a53b…`; superseded PR-head: none recorded — **not** merge authority; see §18 / `M36_run1.md`). **M35** — **Audit Closure IV** — **merged** to `main` ([PR #46](https://github.com/m-cahill/starlab/pull/46); **authoritative PR-head CI** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396); **merge-boundary `main` CI** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432); tag **`v0.0.35-m35`**). At **M34** closure the planned arc was **46 milestones (M00–M45)**; the active program arc is now **62 (M00–M61)** — see §7. **M34** — **Audit Closure III** — shared JSON I/O (`starlab._io`), governance test split, Dependabot + dev dependency caps, operating-manual promotion prep docs, **DIR-003**–**DIR-006** closed (`docs/audit/DeferredIssuesRegistry.md`); **DIR-005** closed by **documentation-only** validation (no unjustified non-adapter broad catches remain; see `docs/audit/broad_exception_boundaries.md`). **Merged** to `main` ([PR #40](https://github.com/m-cahill/starlab/pull/40); **authoritative green PR-head CI** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **merge-boundary post-merge `main` CI** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; tag **`v0.0.34-m34`** on merge commit `51e960d…`; superseded **failure** PR-head [`24261032237`](https://github.com/m-cahill/starlab/actions/runs/24261032237) — **not** merge authority; see §18 / `M34_run1.md`). **Not** M39 flagship proof-pack product work, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1. M00–**M49** merged to `main` ([PR #1](https://github.com/m-cahill/starlab/pull/1) through [PR #60](https://github.com/m-cahill/starlab/pull/60)); **M46** **closed** on `main` (see §18 / `M46_run1.md`); **M47** **closed** on `main` (see §18 / `M47_run1.md`); **M48** **closed** on `main` (see §18 / `M48_run1.md`); **M49** **closed** on `main` (see §18 / `M49_run1.md`). **M33** — **Audit Closure II** — explicit parallel **`CI`** jobs (`quality`, `smoke`, `tests`, `security`, `fieldtest`, aggregate **`governance`**), **`fieldtest-output`** CI artifact (`out/fieldtest/` with required explorer JSON), `docs/runtime/ci_tiering_field_test_readiness_v1.md` + expanded architecture / operator / diligence docs + **DIR-001/002/007** resolutions ([PR #39](https://github.com/m-cahill/starlab/pull/39); **authoritative green PR-head CI** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **merge-boundary post-merge `main` CI** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md`) — **proved on `main`** (narrow: CI tiering + fixture field-test artifact readiness; **not** M34 structural hygiene product work, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity, **not** operating manual v1). **M32** — **Audit Closure I** — measured coverage + JUnit CI artifacts + SHA-pinned actions + smoke/`Makefile` + clone-to-run / field-test docs + public `docs/audit/DeferredIssuesRegistry.md` + arc **M00–M41** (current ledger; M32 closeout text may cite an older bound — historical) ([PR #38](https://github.com/m-cahill/starlab/pull/38); **authoritative green PR-head CI** [`24228528798`](https://github.com/m-cahill/starlab/actions/runs/24228528798) on `0c3f6ce…`; **merge-boundary post-merge `main` CI** [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230) on `cf72199…`; see §18 / `M32_run1.md`) — **proved on `main`** (narrow: governance / diligence baseline; **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity). **M31** — **`replay_explorer_surface.json`** / **`replay_explorer_surface_report.json`** ([PR #37](https://github.com/m-cahill/starlab/pull/37); **authoritative green PR-head CI** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **merge-boundary post-merge `main` CI** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; see §18 / `M31_run1.md`) — **proved on `main`** (narrow: offline bounded replay explorer evidence surface over governed bundles; **not** benchmark integrity, **not** live SC2, **not** web UI, **not** M39 flagship proof pack). **M30** — **`replay_hierarchical_imitation_agent.json`** / **`replay_hierarchical_imitation_agent_report.json`** ([PR #36](https://github.com/m-cahill/starlab/pull/36); **authoritative green PR-head CI** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **merge-boundary post-merge `main` CI** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; see §18 / `M30_run1.md`) — **proved on `main`** (narrow: offline two-level learned hierarchical imitation; fixed delegate policy `starlab.m30.delegate.fixed_four_v1`; **not** benchmark integrity). **M29** — **`hierarchical_agent_interface_schema.json`** / **`hierarchical_agent_interface_schema_report.json`** ([PR #35](https://github.com/m-cahill/starlab/pull/35); **authoritative green PR-head CI** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **merge-boundary post-merge `main` CI** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; see §18 / `M29_run1.md`) — **proved on `main`** (narrow: offline two-level interface contract; **not** learned hierarchical agent; **not** benchmark integrity). **Superseded** red PR-head [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) (Ruff format — **not** merge authority, **M29**). **M10** merge commit `cb3e581f70f85653477081eb1ef4772229f05983` — merge-push `main` CI [`24104111851`](https://github.com/m-cahill/starlab/actions/runs/24104111851) (**failure** — Mypy); **authoritative green `main`** after M10 repair (`cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b`): [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912) (**success**). **M09** merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` — authoritative post-merge `main` CI on merge push [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) (**success**). **M08** merge commit `b99233e807177d65737beaba5246efa67a3edce2` — authoritative post-merge `main` CI [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**). **M07** merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` — authoritative post-merge `main` CI on merge push [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**). **M06** merge commit `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` — post-merge `main` CI on merge push [`24064229874`](https://github.com/m-cahill/starlab/actions/runs/24064229874) (**success**). **M05** merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0` — post-merge `main` CI [`24062610358`](https://github.com/m-cahill/starlab/actions/runs/24062610358) (**success**). **M05** closeout / ledger push on `main` (`6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`): CI [`24062664914`](https://github.com/m-cahill/starlab/actions/runs/24062664914) (**success**). Follow-up ledger cross-reference (`ebca1e964c0539c78165bfab72c249a2157402cc`): CI [`24062700534`](https://github.com/m-cahill/starlab/actions/runs/24062700534) (**success**) — **not** merge-boundary events. **Replay intake / provenance enforcement** (narrow, M07), **governed replay parser substrate** (narrow, M08 — deterministic parse artifacts; `s2protocol` isolated), **stable normalized replay metadata** (narrow, M09 — pure extraction over M08 artifacts), and **governed event/timeline extraction** (narrow, M10 — deterministic timeline artifacts; optional `raw_event_streams` on `replay_raw_parse.json` v2) are **proved on `main`** (M10 merge-push CI failed Mypy; **green `main`** restored on repair commit — see §18). **Governed build-order / economy plane** (narrow, M11 — `replay_build_order_economy.json` / `replay_build_order_economy_report.json`; [PR #12](https://github.com/m-cahill/starlab/pull/12) merge commit `38c15302badd49966b17f9195ddb139f6ae9a9b4`; **authoritative green PR-head CI** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) (**success**); **merge-boundary post-merge `main` CI** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) (**success**)) is **proved on `main`**. **Governed combat / scouting / visibility windows** (narrow, M12 — `replay_combat_scouting_visibility.json` / `replay_combat_scouting_visibility_report.json`; [PR #13](https://github.com/m-cahill/starlab/pull/13) merge commit `78528958a616177b564e603c193fb0d7f8af734e`; **authoritative green PR-head CI** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) (**success**); **merge-boundary post-merge `main` CI** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) (**success**)) is **proved on `main`**. **Governed replay slice definitions** (narrow, M13 — `replay_slices.json` / `replay_slices_report.json`; [PR #14](https://github.com/m-cahill/starlab/pull/14) merge commit `f86e36837e81b8552639c5a885a13a773b96215c`; **authoritative green PR-head CI** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) (**success**); **merge-boundary post-merge `main` CI** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) (**success**)) is **proved on `main`**. **Governed replay bundle & lineage contract** (narrow, M14 — `replay_bundle_manifest.json` / `replay_bundle_lineage.json` / `replay_bundle_contents.json`; [PR #15](https://github.com/m-cahill/starlab/pull/15) merge commit `8a0439a9a2970a74f3a5087390fc080f02852246`; **authoritative green PR-head CI** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) (**success**); **merge-boundary post-merge `main` CI** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) (**success**)) is **proved on `main`**. **Governed canonical state schema v1** (narrow, M15 — `canonical_state_schema.json` / `canonical_state_schema_report.json`; [PR #16](https://github.com/m-cahill/starlab/pull/16) merge commit `b0f7132a54508f35d54406011cd3b37bce776927`; **authoritative green PR-head CI** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) (**success**); **merge-boundary post-merge `main` CI** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) (**success**)) is **proved on `main`**. **Governed structured state pipeline** (narrow, M16 — `canonical_state.json` / `canonical_state_report.json` from M14 bundles; [PR #17](https://github.com/m-cahill/starlab/pull/17) merge commit `dd9546f88ebcf9b454498eec83a14d742d17d070`; **authoritative green PR-head CI** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) (**success**); **merge-boundary post-merge `main` CI** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) (**success**)) is **proved on `main`**. **Governed observation surface contract** (narrow, M17 — `observation_surface_schema.json` / `observation_surface_schema_report.json`; [PR #18](https://github.com/m-cahill/starlab/pull/18) merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76`; **authoritative green PR-head CI** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) (**success**); **merge-boundary post-merge `main` CI** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) (**success**)) is **proved on `main`**. **Governed perceptual bridge prototype** (narrow, M18 — deterministic `observation_surface.json` / `observation_surface_report.json` from M16 `canonical_state.json`; [PR #19](https://github.com/m-cahill/starlab/pull/19) merge commit `59d2d6e2af08852d63e0c91a984000c11decfece`; **authoritative green PR-head CI** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) (**success**); **merge-boundary post-merge `main` CI** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) (**success**)) is **proved on `main`**. **Governed cross-mode reconciliation audit** (narrow, M19 — deterministic `observation_reconciliation_audit.json` / `observation_reconciliation_audit_report.json` for one paired M16 `canonical_state.json` + M18 `observation_surface.json`; [PR #20](https://github.com/m-cahill/starlab/pull/20) merge commit `9e855329fc50f4f00db9c857f982d18ef93e4e65`; **authoritative green PR-head CI** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) (**success**); **merge-boundary post-merge `main` CI** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) (**success**); see §18 / `M19_run1.md`) is **proved on `main`**. **Governed benchmark contract + scorecard schemas** (narrow, M20 — `benchmark_contract_schema.json` / `benchmark_contract_schema_report.json` / `benchmark_scorecard_schema.json` / `benchmark_scorecard_schema_report.json`; [PR #21](https://github.com/m-cahill/starlab/pull/21); **authoritative green PR-head CI** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) (**success**); **merge-boundary post-merge `main` CI** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) (**success**); see §18 / `M20_run1.md`) is **proved on `main`**. **Governed scripted baseline suite** (narrow, M21 — `scripted_baseline_suite.json` / `scripted_baseline_suite_report.json`; [PR #22](https://github.com/m-cahill/starlab/pull/22); **authoritative green PR-head CI** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) on `818002e…`; **merge-boundary post-merge `main` CI** [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) on `092d00a…`; see §18 / `M21_run1.md`) is **proved on `main`**. **Governed heuristic baseline suite** (narrow, M22 — `heuristic_baseline_suite.json` / `heuristic_baseline_suite_report.json`; [PR #23](https://github.com/m-cahill/starlab/pull/23); **authoritative green PR-head CI** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) on `96aba18…`; **merge-boundary post-merge `main` CI** [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) on `470afa8…`; see §18 / `M22_run1.md`). **Governed evaluation runner + tournament harness** (narrow, M23 — `evaluation_tournament.json` / `evaluation_tournament_report.json`; [PR #24](https://github.com/m-cahill/starlab/pull/24); **authoritative green PR-head CI** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) on `f00711a…`; **merge-boundary post-merge `main` CI** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) on `b8857d2…`; see §18 / `M23_run1.md`) is **proved on `main`**. **M24** — **`evaluation_diagnostics.json`** / **`evaluation_diagnostics_report.json`** over governed **M23** ([PR #27](https://github.com/m-cahill/starlab/pull/27); **authoritative green PR-head CI** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) on `5caf1fb…`; **merge-boundary post-merge `main` CI** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) on `7b4d3b4…`; see §18 / `M24_run1.md`) is **proved on `main`**. **M25** — **`baseline_evidence_pack.json`** / **`baseline_evidence_pack_report.json`** over governed **M21/M22 → M23 → M24** ([PR #31](https://github.com/m-cahill/starlab/pull/31); **authoritative green PR-head CI** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on `b132bfd…`; **merge-boundary post-merge `main` CI** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) on `f03c7bf…`; see §18 / `M25_run1.md`) is **proved on `main`**. **M26** — **`replay_training_dataset.json`** / **`replay_training_dataset_report.json`** over governed **M14** replay bundles ([PR #32](https://github.com/m-cahill/starlab/pull/32); **authoritative green PR-head CI** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on `d8d3c4c…`; **merge-boundary post-merge `main` CI** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) on `e83a849…`; see §18 / `M26_run1.md`) is **proved on `main`**. **M27** — **`replay_imitation_baseline.json`** / **`replay_imitation_baseline_report.json`** over governed **M26** + **M14** ([PR #33](https://github.com/m-cahill/starlab/pull/33); **authoritative green PR-head CI** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) on `65dcd2f…`; **merge-boundary post-merge `main` CI** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) on `49b4582…`; see §18 / `M27_run1.md`) is **proved on `main`** — **first** deterministic offline **replay-derived trained imitation baseline** artifact (majority-label-per-signature; explicit non-claims). **M28** — **`learned_agent_evaluation.json`** / **`learned_agent_evaluation_report.json`** over **M20** + frozen **M27** + **M26** + **M14** ([PR #34](https://github.com/m-cahill/starlab/pull/34); **authoritative green PR-head CI** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) on `c7ca6e6…`; **merge-boundary post-merge `main` CI** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) on `1ef6365…`; see §18 / `M28_run1.md`) is **proved on `main`**. **Superseded** red PR-head [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) (Ruff format — **not** merge authority, **M27**). **Superseded** red PR-head [`24215241322`](https://github.com/m-cahill/starlab/actions/runs/24215241322) (pytest — **not** merge authority, **M25**). **Superseded** red PR-head [`24215286216`](https://github.com/m-cahill/starlab/actions/runs/24215286216) (Ruff — **not** merge authority, **M25**). **Superseded** red PR-head [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) (Ruff format — **not** merge authority, **M21**). **Superseded** red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority, **M16**). **Replay↔execution equivalence** and **benchmark integrity** remain **not** proved.  
**License:** Source-available (evaluation and verification only); see `LICENSE`  
**Governance Model:** Milestone-Driven, CI-Enforced  
**Audit Posture:** Active Governance Signal  
**Primary historical ledger (v1 / PV1 / PX1 / PX2):** `docs/starlab.md`  
**v1.5 arc (V15) — authoritative public governance:** `docs/starlab-v1.5.md` (strategic anchor: `docs/starlab-v1.5moonshot.md`; M02 environment lock: `docs/runtime/v15_long_gpu_run_environment_lock_v1.md`; M03 checkpoint lineage / resume discipline: `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`; M04 XAI evidence contract: `docs/runtime/v15_xai_evidence_contract_v1.md`; M05 strong-agent benchmark protocol: `docs/runtime/v15_strong_agent_benchmark_protocol_v1.md`; M06 human panel benchmark protocol: `docs/runtime/v15_human_panel_benchmark_protocol_v1.md`; M07 training smoke / short GPU shakedown: `docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`; M08 long GPU campaign execution: `docs/runtime/v15_long_gpu_campaign_execution_v1.md`; M09 checkpoint evaluation / promotion: `docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`; M10 replay-native XAI demonstration: `docs/runtime/v15_replay_native_xai_demonstration_v1.md`; M11 human panel execution / bounded human-benchmark claim decision: `docs/runtime/v15_human_panel_bounded_benchmark_v1.md`; M12 showcase agent release pack: `docs/runtime/v15_showcase_agent_release_pack_v1.md`; M13 v2 go/no-go decision: `docs/runtime/v15_v2_go_no_go_decision_v1.md`; M14 evidence remediation / operator acquisition readiness: `docs/runtime/v15_evidence_remediation_operator_acquisition_v1.md` — **V15-M14** **closed** on `main` ([PR #140](https://github.com/m-cahill/starlab/pull/140); PR-head CI [`24963376499`](https://github.com/m-cahill/starlab/actions/runs/24963376499); merge [`24965189902`](https://github.com/m-cahill/starlab/actions/runs/24965189902)); **remediation_plan_ready**; **operator_evidence_not_collected**; planning only; **no** operator execution or v2 authorization); **M15** operator evidence collection preflight: `docs/runtime/v15_operator_evidence_collection_preflight_v1.md` — **V15-M15** **closed** on `main` ([PR #141](https://github.com/m-cahill/starlab/pull/141); PR-head [`24966701437`](https://github.com/m-cahill/starlab/actions/runs/24966701437); merge [`24967008755`](https://github.com/m-cahill/starlab/actions/runs/24967008755)) (preflight/sequencing **only**; **not** operator evidence collection; **v2** **not** authorized; details in **`docs/starlab-v1.5.md`**); **M16** short GPU / environment evidence: `docs/runtime/v15_short_gpu_environment_evidence_v1.md` — **V15-M16** **closed** on `main` ([PR #142](https://github.com/m-cahill/starlab/pull/142); PR-head [`24968275296`](https://github.com/m-cahill/starlab/actions/runs/24968275296); merge [`24968604458`](https://github.com/m-cahill/starlab/actions/runs/24968604458)) (bounded environment / short-GPU evidence **surface ready**; default fixture **CI-safe**; **not** long GPU campaign; **not** committed operator evidence; **`docs/starlab-v1.5.md`**); **M17** long GPU campaign evidence: `docs/runtime/v15_long_gpu_campaign_evidence_v1.md` — **V15-M17** **closed** on `main` ([PR #143](https://github.com/m-cahill/starlab/pull/143); PR-head [`24971298575`](https://github.com/m-cahill/starlab/actions/runs/24971298575); merge [`24971687346`](https://github.com/m-cahill/starlab/actions/runs/24971687346) on `d52e411c…`) (`starlab.v15.long_gpu_campaign_evidence.v1`; evidence / preflight **surface ready**; M08 `run_v15_long_gpu_campaign` for real runs; M16 + M08 handoff; default **`long_gpu_run_authorized` false**; **`docs/starlab-v1.5.md`**); **M18** checkpoint evaluation readiness / refusal: `docs/runtime/v15_checkpoint_evaluation_readiness_v1.md` — **V15-M18** **closed** on `main` ([PR #150](https://github.com/m-cahill/starlab/pull/150); merge `e58e249e…`; PR-head [`25023439537`](https://github.com/m-cahill/starlab/actions/runs/25023439537); merge-boundary [`25023582158`](https://github.com/m-cahill/starlab/actions/runs/25023582158)) (**readiness/refusal**; default **`no_candidate_refusal`**; **`docs/starlab-v1.5.md`**). **M19** candidate checkpoint evaluation **package** assembly: `docs/runtime/v15_candidate_checkpoint_evaluation_package_v1.md` — **V15-M19** **closed** on `main` ([PR #151](https://github.com/m-cahill/starlab/pull/151); PR-head [`25025083247`](https://github.com/m-cahill/starlab/actions/runs/25025083247); merge-boundary [`25025427887`](https://github.com/m-cahill/starlab/actions/runs/25025427887)) (package assembly / refusal only; see **`docs/starlab-v1.5.md`**; **not** checkpoint evaluation; **not** strength); **M20** real candidate checkpoint production gate: `docs/runtime/v15_real_candidate_checkpoint_production_gate_v1.md` — **V15-M20** **closed** on `main` ([PR #152](https://github.com/m-cahill/starlab/pull/152); merge `018e2dd242bfc565e29117affe7d545e356a41fc` merged **2026-04-28T00:55:15Z** UTC; PR-head CI [`25027412708`](https://github.com/m-cahill/starlab/actions/runs/25027412708); merge-boundary [`25027870414`](https://github.com/m-cahill/starlab/actions/runs/25027870414)) (`starlab.v15.real_candidate_checkpoint_production_gate.v1`; **`emit_v15_real_candidate_checkpoint_production_gate`**; **`run_v15_t1_30min_candidate_checkpoint_gate`**; **`fixture_no_operator_run`** default; T1 **30-minute** gate tooling **only** — **full T1 GPU run not performed** in merge CI))

---

## Current truth (quick scan)

This table is a **navigation aid** only. Authoritative milestone narrative, CI run IDs, and non-claims remain in §1 (status paragraph), §6–§7, §11, and §18.

| Topic | Position in this ledger |
| ----- | ------------------------ |
| Program arc | **62 milestones (M00–M61)** — **all closed** on `main`; **M61** completes the planned **v1** foundation-completion arc (see §7). |
| Last closed milestone (v1 arc) | **M61** — SC2 foundation release lock & v1 proof pack (merge + operator-local **`ready_within_scope`** evidence; see §11 / §18). |
| Last closed milestone (post-v1) | **PV1-M04** — Post-Campaign Analysis / Comparative Readout — **closed** on `main` (implementation [PR #79](https://github.com/m-cahill/starlab/pull/79); closeout [PR #81](https://github.com/m-cahill/starlab/pull/81)). Prior: **PV1-M03** — Tranche B / Full-Run Completion Evidence — **closed** on `main` (implementation [PR #77](https://github.com/m-cahill/starlab/pull/77); closeout [PR #78](https://github.com/m-cahill/starlab/pull/78)). Prior: **PV1-M02** — **closed** ([PR #76](https://github.com/m-cahill/starlab/pull/76)); **PV1-M01** — **closed** ([PR #74](https://github.com/m-cahill/starlab/pull/74)). |
| Post-v1 (PV1) | **PV1 — Long Industrial Campaign & Scaling Evidence** — **closed** post-v1 phase (**not** “Phase VIII” of v1). Public roadmap table: **Post-v1 (PV1)** section (below §7). **v1** arc **M00–M61** remains **closed** and **historical**. |
| Post-PV1 (PX1) | **PX1 — Full Industrial Run & Demonstration Proof** — **closed** on `main` through **PX1-M04** (see roadmap below). **Not** autonomous full-game strength development — that is **PX2**. Public roadmap: **Post-PV1 (PX1)** (below §7). **v2** is **not** opened by **PX1** closeout; **`PX1-M05`** remains **optional** (**defer**red until chartered). |
| Post-PX1 (PX2) | **PX2 — Autonomous Full-Game Skill Development** — **new** post-PX1 capability phase after **closed** **PX1** (**not** “Phase VIII”; **no** **M62**; **not** a stealth extension of **PX1** packaging). **Ledger (v1.5 M08+):** **`V15-M00`** through **`V15-M28`** **closed** on `main` for **declared scope** (**V15-M26** [PR #162](https://github.com/m-cahill/starlab/pull/162); merge `393adb7f…`; outcome **`t1_checkpoint_plumbing_completed_but_sc2_training_not_yet_meaningful`** — **synthetic CUDA** **`.pt`** **plumbing**; **SC2 rollout path** smoke/bootstrap — **not** meaningful **SC2** training); (**M08** implementation [PR #133](https://github.com/m-cahill/starlab/pull/133); M09 implementation [PR #135](https://github.com/m-cahill/starlab/pull/135); M10 implementation [PR #136](https://github.com/m-cahill/starlab/pull/136); M11 implementation [PR #137](https://github.com/m-cahill/starlab/pull/137); M12 implementation [PR #138](https://github.com/m-cahill/starlab/pull/138); M13 implementation [PR #139](https://github.com/m-cahill/starlab/pull/139); M14 implementation [PR #140](https://github.com/m-cahill/starlab/pull/140) — evidence remediation; **`docs/runtime/v15_evidence_remediation_operator_acquisition_v1.md`**; **remediation_plan_ready**; **not** operator evidence collection; M15 implementation [PR #141](https://github.com/m-cahill/starlab/pull/141) — *Operator Evidence Collection Preflight*; **`docs/runtime/v15_operator_evidence_collection_preflight_v1.md`**; preflight/sequencing only; **not** operator evidence collection; M16 implementation [PR #142](https://github.com/m-cahill/starlab/pull/142) — *Short GPU / Environment Evidence*; **`docs/runtime/v15_short_gpu_environment_evidence_v1.md`**; bounded evidence **surface ready**; **not** long GPU campaign; M17 implementation [PR #143](https://github.com/m-cahill/starlab/pull/143) — *Long GPU Campaign Evidence*; **`docs/runtime/v15_long_gpu_campaign_evidence_v1.md`**; evidence/preflight **surface ready**; **not** a merge-bar long-run completion; M18 implementation [PR #150](https://github.com/m-cahill/starlab/pull/150) — *Checkpoint evaluation readiness / refusal*; **`docs/runtime/v15_checkpoint_evaluation_readiness_v1.md`**; **readiness/refusal** only; default **`no_candidate_refusal`**; M19 implementation [PR #151](https://github.com/m-cahill/starlab/pull/151) — *Candidate checkpoint evaluation package assembly*; **`docs/runtime/v15_candidate_checkpoint_evaluation_package_v1.md`**; **package assembly / SHA cross-checks**; **not** strength evaluation); M21 implementation [PR #153](https://github.com/m-cahill/starlab/pull/153) — *Operator T1 30-Minute GPU Run Execution & Evidence Capture*; **`docs/runtime/v15_operator_t1_30min_gpu_run_execution_v1.md`**; tooling + dry-run preflight **closed**; **full T1** **not** merge CI); **`V15-M08`** — *Long GPU Campaign Execution* — **`implementation_ready_waiting_for_operator_run`** (manifest + preflight + guarded runner; see **`docs/starlab-v1.5.md`**, **`docs/runtime/v15_long_gpu_campaign_execution_v1.md`**); **no** merge-bar operator long-run **completed** claim without receipts. Public roadmap: **Post-PX1 (PX2)** (below §7). Phase charter (**PX2-M00**): **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`**. Terran runtime/action surface (**PX2-M01**): **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`**. Replay bootstrap / first learned policy (**PX2-M02**): **`docs/runtime/px2_neural_bootstrap_from_replays_v1.md`**. **PX2-M03** opened only after a **positive** readiness/preflight decision — **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**. **`docs/runtime/px2_industrial_self_play_campaign_v1.md`**: **slice 1** — contract/profile, bridge, fixture smoke; **slice 2** — execution skeleton, artifact tree, checkpoint/eval receipts; **slice 3** — operator-local execution preflight + bounded real-weights smoke; **slice 4** — bounded multi-step continuity + sealed linkage + promotion/rollback receipts; **slice 5** — operator-local campaign-root manifest + opponent-pool rotation hardening; **slice 6** — preflight logical-path seal normalization + canonical operator-local campaign-root smoke path; **slice 7** — first bounded operator-local non-Blackwell real-run execution record; **slice 8** — bounded operator-local multi-run session under one campaign root; **slice 9** — bounded session + one governed promotion/rollback execution step; **slice 10** — bounded **current-candidate carry-forward** after session transition; **slice 11** — bounded **continuation run** that **consumes** **`px2_self_play_current_candidate.json`** (`px2_self_play_continuation_run.json`); **slice 12** — bounded **post-continuation current-candidate re-anchoring** (`px2_self_play_current_candidate_reanchor.json`, refreshed **`px2_self_play_current_candidate.json`**) — **slice 13** — bounded **second continuation hop** on the refreshed pointer + optional symmetric re-anchor (`px2_self_play_second_hop_continuation.json`, snapshots + refreshed **`px2_self_play_current_candidate.json`**) — **slice 14** — bounded **pointer-seeded** operator-local run (`px2_self_play_pointer_seeded_run.json`, declared seed = latest **`px2_self_play_current_candidate.json`**) — **slice 15** — bounded **post–pointer-seeded handoff** (`px2_self_play_pointer_seeded_handoff.json`, governed lineage from slice-14 pointer-seeded run) — **slice 16** — bounded **handoff-anchored** operator-local run (`px2_self_play_handoff_anchored_run.json`, declared anchor = slice-15 handoff). **After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale** (`px2_self_play_bounded_substantive_execution.json`, runtime §8q — **not** a numbered slice). **not** industrial campaign execution (still **later** in **`PX2-M03`**). **PX2-M03** does **not** auto-open merely because **PX2-M02** closed — it requires that readiness decision. **Ledger (2026-04-26):** **PX2** is **transition-complete**; **v1.5** is the **active program line** (public authority: **docs/starlab-v1.5.md**). **V15-M00** through **`V15-M27`** are **closed** on `main` (**V15-M26** — [PR #162](https://github.com/m-cahill/starlab/pull/162); merge `393adb7fb91536c16927b93216bc7045981061e5`; PR-head [`25046959088`](https://github.com/m-cahill/starlab/actions/runs/25046959088); merge-boundary [`25047132158`](https://github.com/m-cahill/starlab/actions/runs/25047132158)) (**[PR #152](https://github.com/m-cahill/starlab/pull/152)** — *Real Candidate Checkpoint Production Gate*: tooling + **`fixture_no_operator_run`**; **full T1** GPU run **not** performed as part of merge CI; **V15-M21** [PR #153](https://github.com/m-cahill/starlab/pull/153) — tooling + dry-run preflight **closed**; **`t1_30min_run_not_started`** default; **full T1** **not** merge CI); **V15-M22** — **closed** on main ([PR #154](https://github.com/m-cahill/starlab/pull/154); PR-head [`25031597888`](https://github.com/m-cahill/starlab/actions/runs/25031597888); merge-boundary [`25031726394`](https://github.com/m-cahill/starlab/actions/runs/25031726394)); **operator_preflight_blocked** / **`torch_cuda_unavailable`** (**M22**). **`V15-M23`** — **closed** on `main` ([PR #156](https://github.com/m-cahill/starlab/pull/156); PR-head [`25032909816`](https://github.com/m-cahill/starlab/actions/runs/25032909816); merge-boundary [`25033137726`](https://github.com/m-cahill/starlab/actions/runs/25033137726)) — CUDA **`.venv`**; **RTX** **5090**; default **PATH** **Python** **CPU-only**; **no** real **T1** claim in **M23**. **`V15-M24`** — **closed** on `main` ([PR #159](https://github.com/m-cahill/starlab/pull/159)) — **`operator_preflight_blocked` / `missing_private_manifest_inputs`**. **M26 closeout:** **`t1_30min_checkpoint_produced_package_ready`** (**synthetic CUDA** **`.pt`** **plumbing** — **no** promotion; **SC2 rollout path** still trivial); Attempt A **`t1_30min_completed_without_candidate_checkpoint`**; **`sc2-harness`** for **`local_live_sc2`**. **V15-M08** — **implementation surface merged**; **no** operator-local long campaign **completed** on main. **PX2** did **not** run a **long GPU training session** as a program deliverable. |
| Last closed milestone (v1.5) | **`V15-M31`** — *Candidate Checkpoint Evaluation Harness Dry-Run / Strength Scorecard Execution Gate* — **closed** on `main` ([PR #167](https://github.com/m-cahill/starlab/pull/167); merge `6fa7efc9372aa2e5015b0fbc87878d87dd867cc5`; PR-head [`25092872655`](https://github.com/m-cahill/starlab/actions/runs/25092872655); merge-boundary [`25093208089`](https://github.com/m-cahill/starlab/actions/runs/25093208089) — **success**) — **`starlab.v15.candidate_checkpoint_evaluation_harness_gate.v1`** + **`starlab.v15.m31.evaluation_harness_dry_run_gate.v1`** — dry-run harness gate / metadata routing only — **`evaluation_harness_ready` ≠ `benchmark_passed`**. **`docs/starlab-v1.5.md`** **§V15-M31**; **`docs/runtime/v15_candidate_checkpoint_evaluation_harness_gate_v1.md`**. **Prior receipts:** **`V15-M30`** sealed evaluation package (**§V15-M30**). |
| M26 public narrative anchor (v1.5) | **M26 completed T1 checkpoint-production plumbing and produced a candidate checkpoint via synthetic CUDA, but the SC2 rollout path remained bounded smoke/bootstrap only and is not yet meaningful SC2 training.** Authoritative table: **`docs/starlab-v1.5.md`** **§V15-M26**. |
| Last closed milestone (PX1 arc) | **PX1-M04** — Governed Demo Proof Pack & Winning Video — **closed** on `main` (milestone closeout [PR #93](https://github.com/m-cahill/starlab/pull/93)). **Prior:** **PX1-M03** — Candidate Strengthening & Demo Readiness Remediation — **closed** on `main` (closeout [PR #91](https://github.com/m-cahill/starlab/pull/91)). **Prior:** **PX1-M02** — Play-Quality Evaluation & Demo Candidate Selection — **closed** on `main` (closeout [PR #89](https://github.com/m-cahill/starlab/pull/89)). **Prior:** **PX1-M01** — Full Industrial Campaign Execution Evidence — **closed** on `main` (closeout [PR #87](https://github.com/m-cahill/starlab/pull/87)). **Prior:** **PX1-M00** — Full Industrial Run & Demonstration Charter — **closed** on `main` (implementation [PR #83](https://github.com/m-cahill/starlab/pull/83); closeout [PR #84](https://github.com/m-cahill/starlab/pull/84)). **Governance-first** charter only (**PX1-M00**) — **no** campaign execution; **no** demo recording; **did not** open **PX1-M04**+ or **v2** at PX1-M00 closeout. |
| PV1 campaign outcome (bounded, operator-local) | Tranche A **completed within scope**; Tranche B **completed within scope**; full-run threshold **`threshold-not-met`** — frozen **`full_run_duration_target`** **not** met (**separate** operator sessions; **not** reinterpreted). Anchored by closed **PV1-M02**/**PV1-M03** evidence — **not** merge-gate proof. |
| Last closed milestone (PX2 arc) | **PX2-M03** — Industrial Self-Play Campaign — **closed** on the ledger (governed **transition** closeout; implementation + bounded self-play / operator-local surfaces on `main` per **`px2_industrial_self_play_campaign_v1.md`**) — private notes under **`docs/company_secrets/milestones/post-v1/PX2-M03/`** (may be local-only). **Prior:** **PX2-M02** — Neural Bootstrap from Replays — **closed** on `main` ([PR #96](https://github.com/m-cahill/starlab/pull/96)). **Prior:** **PX2-M01** — Full Terran Runtime & Action Surface — **closed** on `main` ([PR #95](https://github.com/m-cahill/starlab/pull/95)). **Prior:** **PX2-M00** — Autonomous Full-Game Agent Charter & Success Criteria — **closed** on `main` (governance closeout [PR #94](https://github.com/m-cahill/starlab/pull/94)). **PX2-M00** — governance charter only — **not** Terran runtime. **PX2-M01** — Terran runtime/action substrate — **not** training. **PX2-M02** — first replay-bootstrap learning over **M01** — **not** self-play; **not** strength proof. **PX2** did **not** complete a **long GPU** training **campaign** as a program outcome. |
| Current milestone | **`V15-M32`** — *bounded candidate checkpoint evaluation execution* (**`docs/starlab-v1.5.md`** **`§V15-M32`**; **`python -m starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution`**; **`docs/runtime/v15_candidate_checkpoint_evaluation_execution_v1.md`**) — fixture or operator metadata-only over sealed **`§V15-M31`** — **not** benchmark pass / strength / promotion; merge to `main` pending |
| v1.5 ID anchors (M00–M33 proposed, quick-scan governance) | Navigation-only compact IDs for governance tests: **`V15-M00`**, **`V15-M01`**, **`V15-M02`**, **`V15-M06`**, **`V15-M07`**, **`V15-M08`**, **`V15-M09`**, **`V15-M10`**, **`V15-M11`**, **`V15-M12`**, **`V15-M13`**, **`V15-M14`**, **`V15-M15`**, **`V15-M16`**, **`V15-M17`**, **`V15-M18`**, **`V15-M19`**, **`V15-M20`**, **`V15-M21`**, **`V15-M22`**, **`V15-M23`**, **`V15-M24`**, **`V15-M25`**, **`V15-M26`**, **`V15-M27`**, **`V15-M28`**, **`V15-M29`**, **`V15-M30`**, **`V15-M31`**, **`V15-M32`**, **`V15-M33`**. **Authoritative** narrative, CI links, and non-claims: **`docs/starlab-v1.5.md`**. |
| PV1 execution evidence (operator-local) | Tranche A: **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`**, **`tranche_a_operator_note.md`**. Tranche B / full-run threshold: **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`**, **`tranche_b_operator_note.md`**, **`full_run_threshold_declaration.md`** — **not** default CI evidence; **not** a substitute for merge-gate proof. |
| PX1 industrial run status (PX1-M01) | **closed** — **authoritative** operator-local run under **`local_live_sc2`**; **`campaign_id`** `px1_m01_full_run_2026_04_17_a`; **`execution_id`** `px1_m01_exec_001`; Tranche A **completed within scope**; Tranche B **completed within scope**; full-run **`threshold-met`** — anchored by operator-local evidence paths in **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`** — **not** default CI; **not** merge-gate proof. |
| PX1-M01 execution evidence (operator-local) | **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; **`tranche_a_operator_note.md`**, **`tranche_b_operator_note.md`**, **`px1_full_run_operator_note.md`**, **`full_run_threshold_declaration.md`**; checkpoint receipts under **`checkpoints/tranche_a_close/`**, **`checkpoints/tranche_b_close/`** — **not** default CI; **not** merge-gate proof. |
| PX1 play-quality status (PX1-M02) | **closed** — bounded **`local_live_sc2`** evaluation under frozen **protocol profile v2** completed with trustworthy artifacts; honest **`no-candidate-selected`** (**0**/**10** wins in final authoritative series); public runtime **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**; **not** ladder proof; **not** **PX1-M03** (demo/video); **protocol profile v1** historical/non-discriminating; **v2** authoritative for evaluation narrative. |
| PX1 demo-candidate evidence (operator-local basenames) | **`px1_play_quality_operator_note.md`**, **`demo_candidate_selection_declaration.md`**, **`px1_play_quality_protocol.json`**, **`px1_play_quality_evidence.json`** (and deterministic `*_report.json` companions where emitted) — **not** default CI; see **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**. |
| PX1 demo readiness status (PX1-M03) | **closed** — bounded hybrid **`local_live_sc2`** remediation + frozen **`px1_demo_readiness_*`** protocol; authoritative operator-local series **`demo-ready-candidate-selected`** for **`px1_m01_weighted_refit_rl_bootstrap_v1`** (including **≥1** replay-backed **watchable** win with registered optional media — operator-local paths under `out/`); public runtime **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`**. **Not** **PX1-M04** (governed winning demo / video pack). |
| PX1 remediation evidence (operator-local basenames) | **`px1_demo_readiness_operator_note.md`**, **`demo_readiness_declaration.md`**, **`px1_demo_readiness_protocol.json`**, **`px1_demo_readiness_evidence.json`** (and deterministic `*_report.json` companions where emitted) — **not** default CI; see **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`**. |
| PX1 demo pack status (PX1-M04) | **closed** — governed **demo proof pack** + winning-video **packaging** recorded on `main` (closeout [PR #93](https://github.com/m-cahill/starlab/pull/93)); public runtime **`docs/runtime/px1_governed_demo_proof_pack_v1.md`**; canonical run/video **references** remain operator-local — **not** merge-gate CI proof. |
| Next planned follow-on | Roadmap only: **`V15-M33`** — *candidate checkpoint model-load and CUDA inference probe* (**provisional** on **`docs/starlab-v1.5.md`**) — **not** opened automatically by **`V15-M32`** merge; **not** a benchmark pass. |
| Phase VI pipeline (compact) | **M40** contract → **M41** flat training run → **M42** comparison → **M43** hierarchical training → **M44** local live-play → **M45** self-play / RL → **M46** bounded live `final_status` / `sc2_game_result` semantics → **M47** bootstrap episode distinctness / operator ergonomics → **M48** M42 contract-path alignment (**closed** on `main`) → **M49** full local campaign charter + preflight (**closed** on `main`) → **M50** hidden rollout execution + supervision (**closed** on `main`) → **M51** post-bootstrap phase orchestration (**closed** on `main`) — **Phase VI complete** on `main`. |
| Phase VII pipeline (compact) | **M52**–**M61** — **all closed** on `main` — trust, equivalence, benchmark integrity, live SC2-in-CI posture, ladder/public evaluation protocol, audit hardening, **v1 release lock** (**M61** operator-local **`ready_within_scope`**) — see §6; **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance proof. |
| Offline artifact → local runtime (Phase VI scan) | **M40** contract → **M41** flat training → **M42** comparison → **M43** hierarchical training → **M44** local live-play → **M45** self-play / RL |
| Phase VI local vs CI | Flat training runs **`out/training_runs/`** (M41); hierarchical runs **`out/hierarchical_training_runs/`** (M43); comparison **`out/comparisons/`** (M42); live validation **`out/live_validation_runs/`** (M44); bootstrap runs **`out/rl_bootstrap_runs/`** (M45); full local campaign charter **`out/training_campaigns/`** (M49) + optional **`campaign_runs/<execution_id>/`** (M50 executor). All **local-first**. CI validates **fixture-only** CPU paths (**no** GPU training; **no** live SC2). |
| Test coverage | ~**80%** branch-aware total (M37 authoritative PR-head); **`fail_under` = 78.0** in `pyproject.toml`. **~85%** is a **stretch target**, not a guaranteed claim. |
| Still **not** proved today (present tense) | **Benchmark integrity** (global / beyond bounded milestone scope), **replay↔execution equivalence** (global / gameplay-semantic), **live SC2 in CI as default merge-gate / global proof**, **ladder / public performance**, **statistical significance of ranking** (M42 does **not** claim this), **operating manual v1** — see §11 *explicit non-claims*. **M61** **closed** with operator-local evidence + **`ready_within_scope`** **does not** change these boundaries — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance. The *Remaining v1 proof-track map* below is **historical** — all Phase VII rows are **complete** on `main`. **PX1-class posture (present tense):** **PX1-M02** **closed** with **`no-candidate-selected`** (**preserved**). **PX1-M03** **closed** with **`demo-ready-candidate-selected`** — **remediation** chapter complete (**not** reinterpreted as global strength). **PX1-M04** **closed** — **governed demo proof pack / winning-video packaging** complete on `main` — **not** default tuning; **not** ladder proof; **not** **v2**. **PX1-M01** **closed** with **`threshold-met`** — **not** play-quality proof. **PX1-M00** is a **governance charter** — **does not** claim play-quality or demo proof are satisfied. **PX2-M00** **closed** ([PR #94](https://github.com/m-cahill/starlab/pull/94)) — **charter / success-criteria freeze** recorded — **not** proof of autonomous full-game strength. **`PX2-M01`** **closed** ([PR #95](https://github.com/m-cahill/starlab/pull/95)) — Terran runtime/action substrate delivered (**not** training; **not** Blackwell; **not** strength proof). **`PX2-M02`** **closed** on `main` ([PR #96](https://github.com/m-cahill/starlab/pull/96)) — first replay-bootstrap learning milestone (**not** self-play; **not** strength proof). **`PX2-M03`** — **closed** on the ledger (readiness **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**) — **slice 1** wiring + smoke; **slice 2** bounded **execution skeleton** + **checkpoint/eval receipt** artifacts; **slice 3** **preflight** + bounded **real-weights** operator-local smoke; **slice 4** multi-step **continuity** + sealed linkage + **promotion/rollback** receipts; **slice 5** **campaign-root manifest** + opponent-pool **rotation hardening**; **slice 6** **preflight seal normalization** + **canonical operator-local campaign-root smoke**; **slice 7** **bounded operator-local real-run** execution record; **slice 8** **bounded operator-local multi-run session**; **slice 9** **bounded session + promotion/rollback execution step**; **slice 10** **current-candidate carry-forward**; **slice 11** **continuation run consuming current-candidate**; **slice 12**–**slice 15** bounded re-anchor / second-hop / pointer-seeded / post–pointer-seeded handoff; **slice 16** **handoff-anchored** bounded operator-local run; **bounded substantive** §8q (`px2_self_play_bounded_substantive_execution.json`). After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale. — **not** industrial campaign completion; **not** Blackwell evidence in CI; **not** a long-GPU program outcome. **`V15-M00`** through **`V15-M25`** **closed** on `main` (M10: [PR #136](https://github.com/m-cahill/starlab/pull/136) — replay-native XAI **demonstration/report** surface, **not** real inference; M11: [PR #137](https://github.com/m-cahill/starlab/pull/137) — human-panel execution + claim-decision **surface**, **not** merge-bar human run; M12: [PR #138](https://github.com/m-cahill/starlab/pull/138) — showcase release-pack **surface**, **not** a default agent release; M13: [PR #139](https://github.com/m-cahill/starlab/pull/139) — v2 go/no-go **decision** **surface**, default **no-go**; M14: [PR #140](https://github.com/m-cahill/starlab/pull/140) — evidence **remediation plan** + operator acquisition **readiness**, **not** operator collection; M15: [PR #141](https://github.com/m-cahill/starlab/pull/141) — *Operator Evidence Collection Preflight* — preflight/sequencing only, **not** operator evidence collection; M16: [PR #142](https://github.com/m-cahill/starlab/pull/142) — short GPU / environment evidence **surface ready**, **not** long campaign; M17: [PR #143](https://github.com/m-cahill/starlab/pull/143) — long GPU **evidence / preflight** **surface**, **not** merge-bar long-run **completion**; M18: [PR #150](https://github.com/m-cahill/starlab/pull/150) — checkpoint **readiness/refusal**, **not** strength evaluation; M19: [PR #151](https://github.com/m-cahill/starlab/pull/151) — **package assembly / SHA cross-checks**, **not** strength); **`V15-M20`** **closed** ([PR #152](https://github.com/m-cahill/starlab/pull/152); **`fixture_no_operator_run`**; **full T1** GPU run **not** merge CI); **`V15-M21`** — **closed** ([PR #153](https://github.com/m-cahill/starlab/pull/153); tooling + dry-run preflight **closed**; **`t1_30min_run_not_started`** default; **full T1** **not** merge CI); **V15-M22** — **closed** on main ([PR #154](https://github.com/m-cahill/starlab/pull/154); PR-head [`25031597888`](https://github.com/m-cahill/starlab/actions/runs/25031597888); merge-boundary [`25031726394`](https://github.com/m-cahill/starlab/actions/runs/25031726394)); **operator_preflight_blocked** / **`torch_cuda_unavailable`** (historical **M22**); **`V15-M23`** — **closed** on `main` ([PR #156](https://github.com/m-cahill/starlab/pull/156); PR-head [`25032909816`](https://github.com/m-cahill/starlab/actions/runs/25032909816); merge-boundary [`25033137726`](https://github.com/m-cahill/starlab/actions/runs/25033137726)); CUDA **`.venv`** + **RTX** **5090**; default **PATH** **Python** **CPU-only**; **no** real **T1** in **M23**; **`V15-M24`** **closed** on `main` ([PR #159](https://github.com/m-cahill/starlab/pull/159)) — operator-local **`operator_preflight_blocked` / `missing_private_manifest_inputs`** (see **`docs/starlab-v1.5.md`**); **`V15-M26`** **closed** on `main` ([PR #162](https://github.com/m-cahill/starlab/pull/162); merge `393adb7f…`; PR-head [`25046959088`](https://github.com/m-cahill/starlab/actions/runs/25046959088); merge-boundary [`25047132158`](https://github.com/m-cahill/starlab/actions/runs/25047132158)) — bounded **T1** + synthetic CUDA **`t1_30min_checkpoint_produced_package_ready`** (**candidate** **`.pt`** **`cb375b77a92f6f07b406d8579a60f3539568be12877808d600826c049e146e78`**) — **PX2** did **not** perform a **long GPU training run** as a program deliverable. |

### Phase boundary matrix (post-v1 phases)

Short orientation: what each phase **proved** vs **did not** prove, and its milestone namespace. **Why a new phase:** **PV1** separated long industrial-campaign evidence from **v1** substrate closure; **PX1** separated demo/industrial proof from **PV1**; **PX2** separates autonomous full-game capability development from **PX1** packaging — each avoids scope drift and overclaim.

| Phase | What it proved | What it did *not* prove | Milestone namespace |
| --- | --- | --- | --- |
| **v1** | Governed replay-native SC2 substrate through **M61**; deterministic artifact families; bounded training/eval surfaces | Global benchmark integrity; universal replay↔execution equivalence; ladder/public performance; merge-gate live SC2 as global proof | **M00–M61** |
| **PV1** | Long industrial campaign discipline; operator-local scaling/tranche evidence; comparative readout | Autonomous full-game agent strength; post-PX1 capability program | **PV1-M00**–**PV1-M04** |
| **PX1** | Full industrial run execution evidence; bounded play-quality/remediation; governed demo proof **packaging** | Autonomous full-game skill program (reserved for **PX2**); **PX1-M04** did **not** open **PX1-M05** or **v2** | **PX1-M00**–**PX1-M04**; **PX1-M05** optional |
| **v1.5 (V15)** | **`V15-M00`** through **`V15-M28`** **closed** on `main` (**`V15-M27`** [PR #163](https://github.com/m-cahill/starlab/pull/163); merge `960f925af…`; PR-head [`25078974410`](https://github.com/m-cahill/starlab/actions/runs/25078974410); merge-boundary [`25079150705`](https://github.com/m-cahill/starlab/actions/runs/25079150705); **`sc2_rollout_training_loop_integration_completed`** — **`docs/starlab-v1.5.md`** **§V15-M27**; **`V15-M28`** [PR #164](https://github.com/m-cahill/starlab/pull/164); merge `35d59f11…`; PR-head [`25083196925`](https://github.com/m-cahill/starlab/actions/runs/25083196925); merge-boundary [`25083354466`](https://github.com/m-cahill/starlab/actions/runs/25083354466); operator-local **`sc2_backed_candidate_training_completed_with_candidate_checkpoint`** sample — **`docs/starlab-v1.5.md`** **§V15-M28**); **`V15-M29`** — *Full 30-Minute SC2-Backed T1 Candidate Run & Evaluation Package Gate* — **operator-local receipts closed** (bounded full-wall-clock ~**1800 s** evidence; **`§V15-M29`** **`docs/starlab-v1.5.md`**); **`V15-M30`** — *SC2-Backed Candidate Checkpoint Evaluation Package* — **emitter + SHA-bind tooling** (`emit_v15_m30_sc2_backed_candidate_checkpoint_evaluation_package`; **`docs/runtime/v15_sc2_backed_candidate_checkpoint_evaluation_package_v1.md`**); **`V15-M31`** — roadmap placeholder — evaluation harness / strength execution (**charter only** until opened). **`V15-M20`** [PR #152](https://github.com/m-cahill/starlab/pull/152); **`fixture_no_operator_run`**; **full T1** **not** merge CI; **`V15-M21`** [PR #153](https://github.com/m-cahill/starlab/pull/153); **`docs/runtime/v15_operator_t1_30min_gpu_run_execution_v1.md`** — execution/evidence tooling + dry-run preflight **closed**; **`t1_30min_run_not_started`** default; **full T1** **not** merge CI. **`V15-M22`** — **closed** on `main` ([PR #154](https://github.com/m-cahill/starlab/pull/154); PR-head [`25031597888`](https://github.com/m-cahill/starlab/actions/runs/25031597888); merge-boundary [`25031726394`](https://github.com/m-cahill/starlab/actions/runs/25031726394)); **`torch_cuda_unavailable`** — follow **`recommended_m22_fork`** / **`recommended_m20_fork`** (**§V15-M22** / **§V15-M21** / **§V15-M19** in **`docs/starlab-v1.5.md`**); **`V15-M23`** **closed** on `main` ([PR #156](https://github.com/m-cahill/starlab/pull/156)) — CUDA **`.venv`** (**not** real **T1**); **`V15-M24`** **closed** on `main` ([PR #159](https://github.com/m-cahill/starlab/pull/159)) — **`missing_private_manifest_inputs`**; **M19** [PR #151](https://github.com/m-cahill/starlab/pull/151) / **`docs/runtime/v15_candidate_checkpoint_evaluation_package_v1.md`** — package assembly (merge `e9a40a21…`; PR-head [`25025083247`](https://github.com/m-cahill/starlab/actions/runs/25025083247)); **M18** [PR #150](https://github.com/m-cahill/starlab/pull/150) / **`docs/runtime/v15_checkpoint_evaluation_readiness_v1.md`** — readiness/refusal (merge `e58e249e…`; PR-head [`25023439537`](https://github.com/m-cahill/starlab/actions/runs/25023439537)); closed **`V15-M16`** *Short GPU / Environment Evidence Collection* — **`docs/runtime/v15_short_gpu_environment_evidence_v1.md`** ([PR #142](https://github.com/m-cahill/starlab/pull/142)); closed **`V15-M17`** *Long GPU Campaign Evidence* — **[PR #143](https://github.com/m-cahill/starlab/pull/143)** / **`docs/runtime/v15_long_gpu_campaign_evidence_v1.md`** (evidence / preflight **surface**; **not** a default long-run **completion** claim); closed **M15** ([PR #141](https://github.com/m-cahill/starlab/pull/141)) — *Operator Evidence Collection Preflight* — preflight/sequencing only — **`docs/runtime/v15_operator_evidence_collection_preflight_v1.md`** (**not** operator evidence collection; **not** v2). Prior closed **M14** ([PR #140](https://github.com/m-cahill/starlab/pull/140)) — evidence remediation + operator acquisition **readiness** only — **`docs/runtime/v15_evidence_remediation_operator_acquisition_v1.md`**. (M11: [PR #137](https://github.com/m-cahill/starlab/pull/137); M10: [PR #136](https://github.com/m-cahill/starlab/pull/136); M09: [PR #135](https://github.com/m-cahill/starlab/pull/135); M08: [PR #133](https://github.com/m-cahill/starlab/pull/133); M07: [PR #129](https://github.com/m-cahill/starlab/pull/129); M06: [PR #127](https://github.com/m-cahill/starlab/pull/127); M12: [PR #138](https://github.com/m-cahill/starlab/pull/138); M13: [PR #139](https://github.com/m-cahill/starlab/pull/139)). **`V15-M08`** — **`implementation_ready_waiting_for_operator_run`**. **`V15-M11`** — human-panel **execution** + **claim-decision** **surface** — **`docs/runtime/v15_human_panel_bounded_benchmark_v1.md`**; **closed** on `main`; **not** a merge-bar human run. **`V15-M12`** — showcase release-pack **surface** — **`docs/runtime/v15_showcase_agent_release_pack_v1.md`**. **`V15-M13`** — v2 go/no-go **decision** — **`docs/runtime/v15_v2_go_no_go_decision_v1.md`**. **`V15-M09`** / **`V15-M10`** — see checkpoint / XAI runtime docs; **default** honest paths remain **blocked** / **fixture** where declared. M07: training-run **receipt** + shakedown **tooling** — **not** long campaign. M06: protocol + `fixture_ci` + optional **operator_declared** — **not** human-panel **match execution**; see **`docs/runtime/v15_human_panel_benchmark_protocol_v1.md`**. **Closed:** **`V15-M26`** on [PR #162](https://github.com/m-cahill/starlab/pull/162); see **`docs/starlab-v1.5.md`** (**`V15-M25`** **closed** — [PR #160](https://github.com/m-cahill/starlab/pull/160); **`V15-M24`** **closed**; **`V15-M23`** **closed**; **`V15-M21`** closed; **`V15-M20`** runtime **`docs/runtime/v15_real_candidate_checkpoint_production_gate_v1.md`**). | Full GPU run + **strong-agent** eval + XAI + **human-panel** eval — **chartered in v1.5**, not satisfied by **PX2** alone; **M14** **closed** as **remediation planning** only (**not** operator collection); **M15** **closed** as preflight/sequencing only | **V15-M13** is the **final planned** public V15 **decision** **milestone** (closed); **M14** **closed** — **readiness** / inventory / gap plan; **M15** **closed** — preflight/sequencing; **M16** **closed** as bounded short GPU / environment evidence **surface**; **M17** **closed** as long GPU **evidence / preflight** **surface**; **M18** — [PR #150](https://github.com/m-cahill/starlab/pull/150) (**readiness/refusal**); **M19** [PR #151](https://github.com/m-cahill/starlab/pull/151) (**package assembly** — **closed**); **M20** **closed** ([PR #152](https://github.com/m-cahill/starlab/pull/152); **`fixture_no_operator_run`**; **full T1** **not** merge CI); **M21** **closed** ([PR #153](https://github.com/m-cahill/starlab/pull/153); tooling + dry-run preflight only; **full T1** **not** merge CI); **M22** **closed** on `main` ([PR #154](https://github.com/m-cahill/starlab/pull/154)); **M23** **closed** on `main` ([PR #156](https://github.com/m-cahill/starlab/pull/156)) — CUDA **`.venv`** (**not** real **T1**); **M24** **closed** on `main` ([PR #159](https://github.com/m-cahill/starlab/pull/159); honest **`missing_private_manifest_inputs`**); **M11** **metadata** **surface** (not a default-benchmark pass) |
| **PX2** | **PX2-M00**–**PX2-M03** **closed**; **transition-complete** (bounded self-play / operator-local **surfaces** — **not** long-GPU program deliverable) | **PX2-M04**/**M05** (planned, not auto-open); **v1.5** carries unresolved **M32**-class structural risks (coverage gate, CI **tiering** vs default path, **JSON I/O** dedup, **architecture** overview, training-scale **provenance**) | **PX2-M00**–**PX2-M05** (roadmap) |

**Phase VI — default M49 protocol phases vs executor coverage (M50 / M51):** Reference only; full semantics in `docs/runtime/full_local_training_campaign_v1.md` and `docs/runtime/industrial_hidden_rollout_mode_v1.md`.

| M49 protocol phase (default `phase` names) | M50 default CLI (`execute_full_local_training_campaign`) | M51 optional CLI (`--post-bootstrap-protocol-phases`) |
| --- | --- | --- |
| `preflight` (`kind`: gate) | Not run by executor (use preflight emitters separately). | Phase receipt: skipped (`gate_phase_charter_only_not_executed_by_executor`). |
| `bootstrap_episodes` (e.g. shakedown, tranches) | **Runs** (`emit_updated_bundle=False`). | **Runs** same; refit input aggregated from completed bootstrap phase dirs. |
| `optional_weighted_refit` (`kind`: optional) | **Not run** (bootstrap-only default). | **Runs** as separate phase when planned + M26/M14 prerequisites hold; emits `updated_policy/rl_bootstrap_candidate_bundle.joblib`. |
| `post_refit_m42_comparison` (`kind`: offline) | **Not run**. | Orchestration only: **skipped** with `candidate_not_m41_comparison_compatible` (M42 remains M27/M41; refit bundle not auto-wrapped as M41). |
| `watchable_m44_validation` (`kind`: operator_review) | **Not run**. | **Runs** one M44 using **refit** joblib when refit succeeded; **no** silent fallback to original M43 weights. |

### STARLAB **v1** — governed substrate boundary (not a blanket “prove everything later”)

In this ledger, **v1** means the **governed, replay-native, local-first SC2 research substrate** through the **planned v1 foundation-completion arc** (**M52**–**M61**, **Phase VII**), culminating in **`M61` — SC2 foundation release lock & v1 proof pack** — still **not** a ladder-first product promise.

**Present tense (honest):** **Benchmark integrity** (global / beyond bounded milestone scope), **replay↔execution equivalence** (global / gameplay-semantic), **live SC2 in CI as default merge-gate proof**, and **ladder/public performance** remain **not** proved **by default**. The **planned v1 foundation-completion arc** (**M52**–**M61**) is **closed** on `main`; closure **does not** silently upgrade those global claims — see quick-scan *Still not proved today* and §11 *explicit non-claims*.

| **v1 means (closed arc — substrate + bounded milestone surfaces)** | **v1 does *not* mean yet (still not proved by default)** |
| ----- | ----- |
| Governed, replay-native, local-first SC2 research substrate; Phase VI training/execution (**M40**–**M51**) **closed** on `main` | **Benchmark integrity** — **not** proved today |
| Deterministic artifacts and operator-facing evidence surfaces; **M54** profile-scoped audit predicates only where implemented | **Replay↔execution equivalence** (global / gameplay-semantic) — **not** proved today |
| Bounded local validation where a milestone explicitly says so | **Live SC2 in CI** as default merge CI proof — **not** proved today |
| Governed bootstrap (**M45**) and campaign execution (**M49**–**M51**) with honest receipts | **Ladder / public performance** as a proved claim — **not** proved today |

#### Remaining v1 proof-track map (historical — Phase VII **complete** on `main`)

Compact roadmap for **Phase VII** — **all rows closed** in §7; this table records **intent**, not open work.

| Track | Milestones | Intent (high level) |
| ----- | ---------- | ------------------- |
| Replay↔execution equivalence | **M52**–**M54** | Charter (**M52**) → evidence surface (**M53**) → audit / acceptance gates (**M54**) |
| Benchmark integrity | **M55**–**M56** | Split-governance charter (**M55**) → evidence + reproducibility gates (**M56**) |
| Live SC2 in CI | **M57**–**M58** | Narrow charter + controlled runner (**M57**) → hardening + cost guardrails (**M58**) |
| Ladder / public evaluation | **M59** | Protocol + evidence surface (bounded) |
| Audit / platform readiness | **M60** | Targeted audit hardening for **v2** readiness (**not** vague cleanup) |
| Release lock | **M61** | SC2 foundation release lock & **v1** proof pack |

#### Phase VII bounded equivalence profiles (M53+)

Compact index of **implemented or planned** comparison profiles. **M54** remains audit / acceptance gates — **not** implied by this table.

| profile_id | bounded claim | join keys | required artifacts | non-claims |
| --- | --- | --- | --- | --- |
| `starlab.m53.profile.identity_binding_v1` | M03/M04 **identity chain** consistency + `replay_binding_id` recompute + opaque `replay_content_sha256` (replay-side); **no** gameplay semantics | `run_spec_id`, `execution_id`, `proof_artifact_hash`, `lineage_seed_id` (governed ids/hashes only) | `run_identity.json`, `lineage_seed.json`, `replay_binding.json` | Universal replay↔execution equivalence **not** proved; parser/timeline/BOE/combat/state **out of scope**; **M54** audit is profile-scoped only; **not** benchmark integrity / live SC2 in CI / ladder |

#### Phase VII bounded equivalence gatepacks (M54+)

| gatepack_id | profile_id | allowed absences | fail conditions (summary) | residual non-claims |
| --- | --- | --- | --- | --- |
| `starlab.m54.gatepack.identity_binding_acceptance_v1` | `starlab.m53.profile.identity_binding_v1` | `replay.replay_content_sha256` → execution unavailable_by_design; excluded semantics → out_of_scope | identity/order mismatch on required join keys; missing required evidence rows; optional M53 report SHA mismatch | Universal equivalence **not** audited; benchmark integrity / live SC2 / ladder **out of scope** |

#### Phase VII bounded benchmark-integrity scopes (M56+)

| scope_id | bounded chain | required artifacts (explicit paths) | non-claims |
| --- | --- | --- | --- |
| `starlab.m56.scope.fixture_only_baseline_chain_v1` | M21–M25 fixture-only offline baseline | `scripted_baseline_suite.json`, `heuristic_baseline_suite.json`, `evaluation_tournament.json`, `evaluation_diagnostics.json`, `baseline_evidence_pack.json` | Global benchmark integrity **not** proved; learned/replay-corpus/live/ladder tracks **out of scope** |

#### Phase VII bounded benchmark-integrity gatepacks (M56+)

| gatepack_id | scope_id | fail conditions (summary) | residual non-claims |
| --- | --- | --- | --- |
| `starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1` | `starlab.m56.scope.fixture_only_baseline_chain_v1` | contract/subject/posture/score drift; corpus canonical implication in fixture-only scope | Benchmark integrity **not** globally proved; M52–M54 equivalence **out of scope** |

#### Phase VII bounded live-SC2-in-CI runner profiles (M57+)

| runner_profile_id | bounded execution | substrate | non-claims |
| --- | --- | --- | --- |
| `starlab.m57.runner_profile.m44_single_validation_v1` | One M44 validation run; one M43 candidate; one output dir; one replay-binding chain | `run_local_live_play_validation` (**M44**) | Global live SC2 in CI **not** proved as merge norm; **M58** adds **guardrails + preflight** — **not** new runner profiles |

#### Phase VII bounded live-SC2-in-CI guardrail profiles (M58+)

| guardrail_profile_id | hardens | paired runner profile | non-claims |
| --- | --- | --- | --- |
| `starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1` | Preflight receipt + policy caps (30m timeout, 7d artifact retention, fleet label + lock posture, explicit live confirmation) | `starlab.m57.runner_profile.m44_single_validation_v1` | **Not** a second execution profile; **not** merge-gate live SC2; **not** ladder (**M59**) |

#### Phase VII artifact-contract index (M52–M61)

Compact index of **primary** governed JSON contracts and the **strongest allowed claim** at each milestone — **not** merge-bar semantics; **not** universal proof of equivalence, benchmark integrity, live SC2 in CI, or ladder strength.

| Milestone | Contract ids (primary) | Primary artifact filenames | Strongest allowed claim |
| --------- | ------------------------ | -------------------------- | ----------------------- |
| M52 | `starlab.replay_execution_equivalence_charter.v1` | `replay_execution_equivalence_charter.json` (+ report) | Charter + deterministic JSON — **not** paired equivalence proof |
| M53 | `starlab.replay_execution_equivalence_evidence.v1` | `replay_execution_equivalence_evidence.json` (+ report) | Bounded identity-binding evidence — **not** universal equivalence |
| M54 | `starlab.replay_execution_equivalence_audit.v1` | `replay_execution_equivalence_audit.json` (+ report) | Profile-scoped audit outcomes — **not** universal equivalence |
| M55 | `starlab.benchmark_integrity_charter.v1` | `benchmark_integrity_charter.json` (+ report) | Charter + split controls — **not** benchmark integrity proved |
| M56 | `starlab.benchmark_integrity_evidence.v1`; `starlab.benchmark_integrity_reproducibility_gates.v1` | `benchmark_integrity_evidence.json`; `benchmark_integrity_reproducibility_gates.json` (+ reports) | Fixture-only baseline chain reproducibility — **not** global benchmark integrity |
| M57 | `starlab.live_sc2_in_ci_charter.v1`; `starlab.live_sc2_in_ci_controlled_runner_receipt.v1` | `live_sc2_in_ci_charter.json`; `live_sc2_in_ci_controlled_runner_receipt.json` (+ reports) | Bounded M44 wrap — **not** merge-gate live SC2 proof |
| M58 | `starlab.live_sc2_in_ci_hardening_guardrails.v1`; `starlab.live_sc2_in_ci_preflight_receipt.v1` | `live_sc2_in_ci_hardening_guardrails.json`; `live_sc2_in_ci_preflight_receipt.json` (+ reports) | Hardening + preflight for M57 profile — **not** ladder evaluation |
| M59 | `starlab.ladder_public_evaluation_protocol.v1`; `starlab.ladder_public_evaluation_evidence.v1` | `ladder_public_evaluation_protocol.json`; `ladder_public_evaluation_evidence.json` (+ reports) | Descriptive public/ladder-shaped evidence packaging — **not** ladder strength proof |
| M60 | *(no new governed JSON contract family)* | `docs/audit/m60_v2_readiness_findings.md`; `docs/runtime/v2_readiness_audit_hardening_v1.md` | Structural/diligence milestone — **not** new product artifact claims |
| M61 | `starlab.sc2_foundation_v1_proof_pack.v1`; `starlab.sc2_foundation_release_lock_audit.v1` | `sc2_foundation_v1_proof_pack.json`; `sc2_foundation_release_lock_audit.json` (+ reports) | Within-scope release lock packaging over prior milestone anchors + one operator-local industrial campaign profile — **`ready_within_scope`** only when post-bootstrap phases, watchable **M44**, and operator-declared full-run threshold are honestly evidenced — **not** benchmark universality; **not** replay↔execution universality; **not** ladder strength |

**M61 release-evidence matrix (compact):** governance mirror for what the proof pack may admit as release-lock evidence.

| Evidence source | Required / optional | Local-only / repo-visible | Strongest allowed claim |
| --- | --- | --- | --- |
| Prior milestone anchors via `foundation_track_refs` (e.g. `v0.0.39-m39` … `v0.0.60-m60`) | **Required** (explicit list) | Repo-visible tags + optional SHAs in proof-pack JSON | Honest pointer to **closed milestone surfaces** — **not** re-proving their bounded claims |
| **M39** public flagship proof narrative | **Optional** pointer in `foundation_track_refs` | Repo-visible | Flagship offline substrate story — **not** Phase VI training completeness |
| **M49** `full_local_training_campaign_contract.json` + `campaign_preflight_receipt.json` | **Required** paths | Local operator artifacts (`out/training_campaigns/…`); proof pack holds paths + hashes | Governed **charter + preflight** tied to the executed campaign — **not** automatic CI execution proof |
| **M50/M51** `hidden_rollout_campaign_run.json` (industrial executor) | **Required** | Local operator artifacts under campaign root | One governed **hidden rollout** execution record — **not** benchmark integrity |
| **M51** post-bootstrap protocol phases enabled | **Required** on path claiming `ready_within_scope` | Receipts on campaign run + phase dirs | Refit / skip-M42 / **watchable M44** orchestration as recorded — **not** M42 semantic extension to refit bundles |
| **M44** watchable validation JSON + **M04** `replay_binding.json` + validation replay | **Required** | Local paths; replay + weights typically **local-only** | Replay-backed watchable validation row — **not** ladder outcome proof |
| Video metadata / operator watch notes | **Optional** | Local paths | Supplementary context — **not** sole primary proof |
| CI (`ruff`/`mypy`/`pytest` + M61 fixture tests) | **Required** for merge hygiene | Repo-visible | Emitter + audit **mechanics** correct — **not** operator heavy campaign |

**M61 operator-local closure** (`release_scope_status`: `ready_within_scope`) for the **M00–M61 v1 arc** was **satisfied** by operator-local execution (**campaign** `m61_evidence_2026_04_16_a`, **execution** `m61_exec_001`) with governed **M49→M50→M51** path, **`--post-bootstrap-protocol-phases`**, watchable **M44**, proof pack + audit emission — raw `out/` remains **local-only** (**not** committed).

#### **v2** (begins after **M61**)

**v2** is for **multi-game expansion**, **AURORA/audio learning**, and **broader productization** — explicitly **outside** the **M00**–**M61** v1 foundation-completion arc unless the ledger is rechartered.

**Phase VI operator glossary (compact):**

| Term | Meaning |
| ---- | ------- |
| **shakedown** | Short bounded run to validate wiring (tooling, paths, harness) before a longer operator campaign. |
| **tranche** | A named slice of work within a phase or campaign (e.g. a milestone-sized batch or operator step sequence). |
| **full local campaign** | Operator-local multi-stage training/bootstrap sequence over Phase VI surfaces; **M49** authorizes **contract + preflight + protocol** only — **not** proof that the full wall-clock campaign was executed on `main`. |
| **bootstrap run artifact** | Governed **M45** outputs (`self_play_rl_bootstrap_run.json` / report and related files under **`out/rl_bootstrap_runs/`**) — distinct from **M49** **`out/training_campaigns/`** campaign contract layout. |

**Operator campaign ladder (local, M49-style live/bootstrap campaigns):** A practical sequence for governed evidence — **not** a merge obligation on `main`. Interpret multi-episode work through **distinct episode identities** (**M47**), not raw episode count alone.

1. **Shakedown** — Short run (e.g. few episodes) to validate wiring, paths, and harness before scaling.  
2. **Tranche A** — First substantive bounded slice (e.g. first sealed multi-episode live bootstrap under one output tree); checkpoint for sealing, distinctness, and operator notes.  
3. **Tranche B** — Next bounded slice (same discipline: one process per output dir, same env/SC2 posture); stop for analysis before optional further steps.  
4. **Governed full-run threshold** — Operator-defined bar (e.g. episode budget, campaign goals) before treating a run as the long “full” local campaign slice; **M49** charter authorizes protocol — **not** proof that a long wall-clock run already occurred.

---

## Start Here

1. Read `docs/starlab-vision.md` for the moonshot framing and long-range thesis.  
2. Read `docs/bicetb.md` for licensing, provenance, and diligence posture (“clean enough to buy”).  
3. Read this file for current status, phase structure, milestone history, and project rules.  
4. For a **clone-to-run** engineer path, read `docs/getting_started_clone_to_run.md` and `docs/architecture.md`.  
5. Read governance docs: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/deployment_posture.md`, `docs/runtime/sc2_runtime_surface.md`, `docs/runtime/environment_lock.md`, `docs/runtime/match_execution_harness.md` (M02 proof surface), `docs/runtime/run_identity_lineage_seed.md` (M03 run identity / lineage seed contract), `docs/runtime/replay_binding.md` (M04 replay binding contract), `docs/runtime/canonical_run_artifact_v0.md` (M05 canonical run package boundary), `docs/runtime/environment_drift_smoke_matrix.md` (M06 environment drift / smoke matrix contract), `docs/runtime/replay_intake_policy.md` (M07 replay intake / provenance gate), `docs/runtime/replay_parser_substrate.md` (M08 replay parser substrate contract), `docs/runtime/replay_metadata_extraction.md` (M09 replay metadata extraction contract), `docs/runtime/replay_timeline_event_extraction.md` (M10 replay timeline / event extraction contract), `docs/runtime/replay_build_order_economy_extraction.md` (M11 build-order / economy contract), `docs/runtime/replay_combat_scouting_visibility_extraction.md` (M12 combat / scouting / visibility contract), and `docs/runtime/replay_slice_generation.md` (M13 replay slice definitions contract), and `docs/runtime/replay_bundle_lineage_contract.md` (M14 replay bundle / lineage packaging contract), and `docs/runtime/canonical_state_schema_v1.md` (M15 canonical state schema contract), and `docs/runtime/canonical_state_pipeline_v1.md` (M16 canonical state pipeline contract), and `docs/runtime/observation_surface_contract_v1.md` (M17 observation surface contract), and `docs/runtime/perceptual_bridge_prototype_v1.md` (M18 perceptual bridge prototype contract), and `docs/runtime/observation_reconciliation_audit_v1.md` (M19 cross-mode reconciliation audit contract), and `docs/runtime/benchmark_contract_scorecard_v1.md` (M20 benchmark contract + scorecard contract), and `docs/runtime/scripted_baseline_suite_v1.md` (M21 scripted baseline suite contract), and `docs/runtime/heuristic_baseline_suite_v1.md` (M22 heuristic baseline suite contract), and `docs/runtime/evaluation_runner_tournament_harness_v1.md` (M23 evaluation runner + tournament harness contract), and `docs/runtime/evaluation_diagnostics_failure_views_v1.md` (M24 evaluation diagnostics + failure views contract), and `docs/runtime/baseline_evidence_pack_v1.md` (M25 baseline evidence pack contract), and `docs/runtime/replay_training_dataset_v1.md` (M26 replay training dataset contract), and `docs/runtime/replay_imitation_baseline_v1.md` (M27 replay imitation baseline contract), and `docs/runtime/learned_agent_evaluation_harness_v1.md` (M28 learned-agent evaluation harness contract), and `docs/runtime/hierarchical_agent_interface_v1.md` (M29 hierarchical agent interface contract), and `docs/runtime/replay_hierarchical_imitation_agent_v1.md` (M30 replay hierarchical imitation agent contract), and `docs/runtime/replay_explorer_surface_v1.md` (M31 replay explorer / operator evidence surface contract), and `docs/runtime/public_flagship_proof_pack_v1.md` (M39 public flagship proof pack contract), and `docs/runtime/agent_training_program_contract_v1.md` (M40 agent training program contract), and `docs/runtime/replay_imitation_training_pipeline_v1.md` (M41 replay-imitation training pipeline contract), and `docs/runtime/learned_agent_comparison_harness_v1.md` (M42 learned-agent comparison harness contract), and `docs/runtime/hierarchical_training_pipeline_v1.md` (M43 hierarchical training pipeline contract), and `docs/runtime/local_live_play_validation_harness_v1.md` (M44 local live-play validation harness contract), and `docs/runtime/self_play_rl_bootstrap_v1.md` (M45 self-play / RL bootstrap contract), and `docs/runtime/full_local_training_campaign_v1.md` (M49 full local campaign charter), and `docs/runtime/industrial_hidden_rollout_mode_v1.md` (M50 industrial hidden rollout contract), and `docs/runtime/replay_execution_equivalence_charter_v1.md` (M52 replay↔execution equivalence charter), and `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md` (M53 replay↔execution equivalence evidence surface), and `docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md` (M54 replay↔execution equivalence audit / acceptance gates), and `docs/runtime/benchmark_integrity_charter_v1.md` (M55 benchmark integrity charter), and `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md` (M56 benchmark integrity evidence + reproducibility gates), and `docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md` (M57 live SC2 in CI charter / controlled runner), and `docs/runtime/live_sc2_in_ci_hardening_cost_guardrails_v1.md` (M58 live SC2 in CI hardening + cost guardrails), and `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md` (M59 ladder/public evaluation protocol & evidence surface), and `docs/runtime/ci_tiering_field_test_readiness_v1.md` (M33 CI tiering + field-test readiness contract), and `docs/runtime/pv1_post_campaign_readout_v1.md` (PV1-M04 post-campaign comparative readout).  
6. Treat this document as the public-facing source of truth and update it at every milestone closeout.  
7. Local testing is expected to use an RTX 5090 Blackwell where relevant.  
8. After the closed **v1** arc (**M00–M61**), read **Post-v1 (PV1) — Long Industrial Campaign & Scaling Evidence** (below §7) for the **closed** **PV1** roadmap — **not** a continuation of v1 milestone numbering (**no M62**). For **inspection-only** helpers over `out/training_campaigns/<campaign_id>/` trees (checkpoint receipts + observability index), read **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`** — **not** a substitute for operator execution evidence. For **PV1-M02** bounded **Tranche A** operator-local execution evidence (minimum package, kickoff freeze, **`tranche_a_operator_note.md`** convention), read **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`** — **operator-local by default**, **not** default CI. For **PV1-M03** **Tranche B** and **full-run threshold** evaluation (frozen threshold block, **`tranche_b_operator_note.md`**, **`full_run_threshold_declaration.md`**), read **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`** — **operator-local by default**, **not** default CI. For **PV1-M04** post-campaign comparative readout (**aggregation only**), read **`docs/runtime/pv1_post_campaign_readout_v1.md`** — **not** new execution evidence; **not** threshold reinterpretation.  
9. After **PV1**, read **Post-PV1 (PX1) — Full Industrial Run & Demonstration Proof** (below §7) for the **PX1** roadmap and charter context — **separate** from **PV1**; **not** “Phase VIII.” Read **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`** for the public PX1 phase charter (**PX1-M00**). For **PX1-M01** full industrial campaign execution evidence (frozen threshold package, evidence contract, non-claims), read **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**. **v2** does **not** begin in **PX1-M00**.  
10. After **PX1**, read **Post-PX1 (PX2) — Autonomous Full-Game Skill Development** (below §7) for the **PX2** roadmap — **separate** from **PX1** packaging closure; **not** “Phase VIII”; **no** **M62**. Read **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`** for the public **PX2** phase charter (**PX2-M00** **closed** on `main` — [PR #94](https://github.com/m-cahill/starlab/pull/94)). Read **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`** for the **PX2-M01** Terran runtime/action surface (**PX2-M01** **closed** on `main` — [PR #95](https://github.com/m-cahill/starlab/pull/95)). Read **`docs/runtime/px2_neural_bootstrap_from_replays_v1.md`** for **`PX2-M02`** replay-bootstrap learning (**closed** on `main` — [PR #96](https://github.com/m-cahill/starlab/pull/96)). Read **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`** for the **PX2-M03** opening preflight — **`PX2-M03`** does **not** auto-open merely because **`PX2-M02`** closed. Read **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** for the **PX2-M03** industrial self-play campaign **v1** surface — **slice 1** (contract, bridge, fixture smoke), **slice 2** (execution skeleton, artifact tree, checkpoint/eval receipts), **slice 3** (operator-local preflight + bounded real-weights smoke), **slice 4** (multi-step continuity + sealed linkage + promotion/rollback receipts), **slice 5** (operator-local campaign-root manifest + opponent-pool rotation hardening), **slice 6** (preflight logical-path seal normalization + canonical operator-local campaign-root smoke path), **slice 7** (first bounded operator-local non-Blackwell real-run execution record), **slice 8** (bounded operator-local multi-run session under one campaign root), **slice 9** (bounded session + one governed promotion/rollback execution step), **slice 10** (bounded current-candidate carry-forward after session transition), **slice 11** (bounded continuation run consuming **`px2_self_play_current_candidate.json`**), **slice 12** (bounded post-continuation current-candidate re-anchoring), **slice 13** (bounded second continuation hop + optional symmetric re-anchor), **slice 14** (bounded pointer-seeded run declaring latest **`px2_self_play_current_candidate.json`** as seed — `px2_self_play_pointer_seeded_run.json`), **slice 15** (bounded post–pointer-seeded handoff — `px2_self_play_pointer_seeded_handoff.json`), **slice 16** (bounded handoff-anchored operator-local run — `px2_self_play_handoff_anchored_run.json`); **after slice 16** — **bounded substantive execution** (`px2_self_play_bounded_substantive_execution.json`, §8q). After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale. — **not** industrial Blackwell-scale execution (**still** within **`PX2-M03`** implementation line). **Ledger (2026-04-23):** **`PX2-M03`** **closed** / **transition-complete**; **`current milestone`** = **`V15-M00`** (**v1.5** planning stub) — **`PX2-M04`** / **`PX2-M05`** **planned only**; **PX2** did **not** perform a long **GPU** training run.

**Post-M39 training roadmap (governance):** Phase VI was rechartered to **M40**–**M45** — charter (**M40**), then replay-imitation training, learned-agent comparison, hierarchical training, local live-play validation, and self-play / RL bootstrap — see §6–§8. Former Phase VI ideas (**SC2 Substrate Review & Expansion Decision**; **Platform Boundary Review & Multi-Environment Charter**) are **deferred beyond the current active arc** (§19). **Phase VI integrated test campaign** follows **M45** closeout — framed as post-M45 follow-on in `docs/diligence/phase_vi_integrated_test_campaign.md`, **not** as an earlier-milestone proof obligation.

---

## 1. Project identity (one sentence)

STARLAB is a **governed, replay-native RTS research lab** that begins with StarCraft II and aims to create a reproducible, benchmarkable, evidence-first substrate for hierarchical, perception-grounded, multi-agent research.

---

## 2. Authority hierarchy

When documents or implementation disagree, use this order:

1. **`docs/starlab-vision.md`** — moonshot, ambition, thesis, and long-range scope  
2. **`docs/bicetb.md`** — “clean enough to buy” operating rules for ownership, licensing, provenance, and public/private boundaries  
3. **`docs/starlab.md` (this file)** — current project state, milestone status, phase map, authority record  
4. **README** — public front door and short-form project identity  
5. **Implementation** — must satisfy the above; defects are tracked against the docs, not the reverse

**Rule:** this file is the **canonical public ledger**, not the full philosophical brief. The vision document provides altitude; this document records reality.

---

## 3. Vision anchor (brief)

STARLAB treats RTS research as a **systems problem first** and an **agent problem second**.

The project is not just about training an agent. It is about building a lab surface where runs, replays, artifacts, benchmarks, and evaluation can be tied together in a governed and inspectable way.

---

## 4. Build posture (brief)

STARLAB is being built to be **clean enough to buy**.

That means the project should become:

- ownable  
- legible  
- separable  
- defensible  
- maintainable  
- low-friction to diligence  

This posture affects licensing, contributor policy, provenance, documentation, dependency hygiene, and public/private boundary decisions.

---

## 5. Current program surface

As of project initialization, STARLAB is defined as:

- a **research substrate**, not a ladder-first bot effort
- **SC2-first**, with future multi-environment potential
- **replay-native** and **benchmark-first**
- **evidence-first**, with milestone-sized validation
- **acquisition-aware**, but not prematurely over-corporatized

### Working posture

- Lab-first  
- Benchmark-first  
- Evidence-first  
- Small-milestone-first  
- Honest non-claims over inflated capability claims  

### Current hardware posture

- **Local GPU:** RTX 5090 Blackwell (where local GPU-backed work is relevant)

---

## 6. Phase map (high level)

The current program is expected to proceed through the following phases.

### Phase I — Governance, Runtime Surface, and Deterministic Run Substrate

Focus:

- repo governance (M00)
- SC2 runtime boundary decision and environment lock (M01)
- deterministic match execution harness (**M02** — complete on `main`)
- run identity and lineage seed (**M03** — complete on `main`); replay binding (**M04** — complete on `main`); canonical run artifact v0 (**M05** — complete on `main`)
- environment drift and runtime smoke matrix (**M06** — complete on `main`)

#### Phase I — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase I boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M02 | `match_execution_proof` (normalized hash / proof record) | M01 runtime boundary + harness | Proof record only (no replay package) | Replay binding, canonical run package, cross-host reproducibility |
| M03 | `run_identity.json`, `lineage_seed.json` | M02 proof + match config (deterministic IDs) | STARLAB JSON artifacts | Replay binding, canonical run artifact v0, benchmarks |
| M04 | `replay_binding.json` | M03 `run_identity` / `lineage_seed` + opaque replay bytes (`replay_content_sha256`) | M03 JSON + `replay_binding.json` (replay bytes hashed, not shipped) | Replay parser semantics, replay↔proof equivalence, canonical run artifact v0, benchmarks |
| M05 | `manifest.json`, `hashes.json`, plus M03/M04 JSON (directory bundle) | M03 + M04 JSON only | **Included:** STARLAB-owned JSON only. **External:** raw replay bytes, raw proof/config (never in bundle) | Parser substrate (M08), full benchmark semantics (later) |
| M06 | `runtime_smoke_matrix.json`, `environment_drift_report.json` | M01 probe JSON; optional M03 `environment_fingerprint` | STARLAB JSON artifacts (fixture-driven in CI) | Replay parser, provenance closure, benchmark integrity, cross-host portability, live SC2 in CI |

#### Phase II — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase II boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M07 | `replay_intake_receipt.json`, `replay_intake_report.json` | Opaque replay bytes + declared intake metadata; optional M03/M04/M05 JSON | STARLAB JSON artifacts; replay bytes hashed, not parsed | Replay parser semantics, semantic extraction, benchmark integrity, cross-host portability, live SC2 in CI |
| M08 | `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json` | M07 intake artifacts (optional hash linkage); M04 `replay_binding` (optional); `s2protocol` via adapter | STARLAB JSON; fixture-driven CI default; raw sections + capability flags | Stable normalized metadata contract (M09), timeline/event semantics (M10), broad parser correctness, build-order extraction, benchmark integrity, live SC2 in CI |
| M09 | `replay_metadata.json`, `replay_metadata_report.json` | M08 `replay_raw_parse.json` (+ optional parse receipt/report for linkage) | STARLAB JSON; fixture-driven CI default; smaller public metadata surface than raw parse | Event/timeline semantics (M10), build-order extraction (M11), broad parser correctness, benchmark integrity, live SC2 in CI |
| M10 | `replay_timeline.json`, `replay_timeline_report.json` | M08 `replay_raw_parse.json` (v2 `raw_event_streams` + optional lineage receipts) | STARLAB JSON; fixture-driven CI default; bounded semantic kinds | Build-order / economy (M11), combat/scouting, broad parser correctness, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M11 | `replay_build_order_economy.json`, `replay_build_order_economy_report.json` | M10 `replay_timeline.json` (primary); optional M08 v2 `replay_raw_parse.json` `raw_event_streams` for entity identity only | STARLAB JSON; fixture-driven CI default; conservative catalog | Combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M12 | `replay_combat_scouting_visibility.json`, `replay_combat_scouting_visibility_report.json` | M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` (required); optional M08 v2 `replay_raw_parse.json` for identity / position / explicit visibility fields only | STARLAB JSON; fixture-driven CI default; conservative combat/scouting/proxy visibility | Replay slice definitions (M13), true fog-of-war certification, replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M13 | `replay_slices.json`, `replay_slices_report.json` | M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` + M12 `replay_combat_scouting_visibility.json` (required); optional reports/metadata for enrichment only; **no** `replay_raw_parse.json` in M13 v1 | STARLAB JSON; fixture-driven CI default; metadata-only temporal spans | Replay bundle / lineage packaging (M14), raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI |
| M14 | `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json` | M09–M13 primary governed JSON (required); optional `*_report.json`; optional M07/M08 receipts for lineage context only | STARLAB JSON only; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** archive requirement in v1 | Structured state pipeline (M16+), replay↔execution equivalence, benchmark integrity, live SC2 in CI |

#### Phase III — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase III boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M15 | `canonical_state_schema.json`, `canonical_state_schema_report.json` | JSON Schema + report for one **canonical state frame** at one `gameloop`; semantics bounded to M09–M14 replay-derived posture (counts, categories, proxy visibility — not exact banked resources or fog-of-war truth) | STARLAB JSON; emitted deterministically; validated in CI with `jsonschema`; **no** `s2protocol`, **no** parser CLI, **no** raw replay bytes in M15 modules | Replay-to-state **materialization** (M16), observation surface contract (M17), perceptual bridge (M18), replay↔execution equivalence, benchmark integrity, live SC2 in CI |
| M16 | `canonical_state.json`, `canonical_state_report.json` | M14 bundle (`replay_bundle_*.json`) + M09–M13 primary JSON; validates emitted state against M15 schema; one frame per CLI invocation | STARLAB JSON; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol` in M16 modules | Observation surface (M17), perceptual bridge (M18), multi-frame tensors / action masks, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, live SC2 in CI |
| M17 | `observation_surface_schema.json`, `observation_surface_schema_report.json` | M16 **`canonical_state.json`** (semantic upstream for observation design); one **player-relative** observation frame at one `gameloop`; optional `canonical_state_report.json` for provenance hashes only | STARLAB JSON; emitted deterministically; validated in CI with `jsonschema`; **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol`, **no** M14 bundle load in M17 modules, **no** canonical→observation **materialization** pipeline | Perceptual bridge prototype (M18), tensor materialization, replay↔execution equivalence, benchmark integrity, exact resources, certified fog-of-war truth, mask legality computation, live SC2 in CI |
| M18 | `observation_surface.json`, `observation_surface_report.json` | M16 **`canonical_state.json`** (required); optional **`canonical_state_report.json`** for hash cross-check + warning propagation; one player-relative observation frame per CLI invocation | STARLAB JSON; validates emitted observation against **M17** JSON Schema; **no** M14 bundle load, **no** raw replay bytes, **no** `replay_raw_parse.json`, **no** `s2protocol` in M18 observation modules | Full mask legality / SC2 action coverage, multi-frame tensors, replay↔execution equivalence, benchmark integrity, certified fog-of-war truth, live SC2 in CI |
| M19 | `observation_reconciliation_audit.json`, `observation_reconciliation_audit_report.json` | One M16 **`canonical_state.json`** + one M18 **`observation_surface.json`** (same `gameloop` / `perspective_player_index`); optional **`canonical_state_report.json`** and **`observation_surface_report.json`** for hash cross-checks + upstream warnings | STARLAB JSON; **no** replay parsing, **no** M14 bundle load, **no** `s2protocol` in M19 observation modules | Benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, live SC2 in CI, **M20** benchmark contract semantics |

#### Phase IV — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase IV boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M20 | `benchmark_contract_schema.json`, `benchmark_contract_schema_report.json`, `benchmark_scorecard_schema.json`, `benchmark_scorecard_schema_report.json` | Governed JSON Schemas + reports for one benchmark contract and one scorecard (`jsonschema` validation); optional fixture hashes in reports | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M20 `starlab/benchmarks/` modules | Scripted baselines (**M21**), heuristic baselines (**M22**), evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M21 | `scripted_baseline_suite.json`, `scripted_baseline_suite_report.json` | One M20-validated **`fixture_only`** benchmark contract; embedded M20 scorecards for a fixed ordered set of **scripted** subjects; deterministic catalogs | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M21 `starlab/baselines/` modules | Heuristic baselines (**M22**), evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M22 | `heuristic_baseline_suite.json`, `heuristic_baseline_suite_report.json` | One M20-validated **`fixture_only`** benchmark contract; embedded M20 scorecards for a fixed ordered set of **heuristic** subjects; deterministic catalogs | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M22 `starlab/baselines/` modules | Evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M23 | `evaluation_tournament.json`, `evaluation_tournament_report.json` | M20 **`fixture_only`** benchmark contract + one or more governed **M21/M22** suite artifacts; deterministic entrant catalog + round-robin harness over embedded scorecards | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M23 `starlab/evaluation/` modules | Diagnostics views (**M24**), baseline evidence pack (**M25**), benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M24 | `evaluation_diagnostics.json`, `evaluation_diagnostics_report.json` | One governed **M23** `evaluation_tournament.json` (`fixture_only`); deterministic entrant/match/standing explanations + failure-view surfaces (**interpretive** — does not re-score) | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M24 `starlab/evaluation/` modules | Baseline evidence pack (**M25**), benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M25 | `baseline_evidence_pack.json`, `baseline_evidence_pack_report.json` | Governed **M21/M22** suite artifacts + one **M23** `evaluation_tournament.json` + one **M24** `evaluation_diagnostics.json` (same fixture-only chain); deterministic packaging + entrant cross-references (**interpretive** — does not re-score or re-diagnose) | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M25 `starlab/evaluation/` modules | Benchmark integrity, new evaluation semantics, replay↔execution equivalence, live SC2 in CI, **M26** replay training dataset contract, **M27** imitation baseline |

**Phase IV boundary (M20–M25):** **M20** defines benchmark contract + scorecard schemas. **M21** and **M22** are **fixture-only baseline suite emitters** (scripted vs heuristic subjects). **M23** consumes those suites and proves a **fixture-only evaluation runner + tournament harness** (deterministic tournament artifacts). **M24** consumes **M23** output and emits **diagnostic / failure-view** JSON — **interpretive**. **M25** packages the governed **M21/M22 → M23 → M24** chain into **`baseline_evidence_pack.json`** / **`baseline_evidence_pack_report.json`** — **interpretive packaging only**; it does **not** upgrade benchmark-integrity claims. Remains **not** benchmark integrity, **not** live SC2 execution, **not** replay↔execution equivalence. **M26** replay training dataset contract is **Phase V** (see §6 Phase V boundary); **M27** imitation baseline or learning is **not** in Phase IV.

#### Phase V — artifact contracts by milestone (compact)

| Milestone | Primary artifact(s) | Binds to / upstream | Included vs external (Phase V boundary) | Explicitly **not** proved here |
| --------- | -------------------- | --------------------- | ---------------------------------------- | ------------------------------ |
| M26 | `replay_training_dataset.json`, `replay_training_dataset_report.json` | One or more governed **M14** bundle directories (`replay_bundle_manifest.json` / `replay_bundle_lineage.json` / `replay_bundle_contents.json` + M09–M13 primary JSON); optional per-bundle M07 `replay_intake_receipt.json` | STARLAB JSON only; **no** `starlab.sc2`, **no** `s2protocol`, **no** raw replay bytes, **no** replay parser execution in M26 `starlab/imitation/` modules | Model training, **M27** imitation baseline, benchmark integrity, replay↔execution equivalence, live SC2 in CI |
| M27 | `replay_imitation_baseline.json`, `replay_imitation_baseline_report.json` | One governed **M26** `replay_training_dataset.json` + referenced governed **M14** bundle directories; observation materialization via **M16 → M18** in-process pipelines only | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M27 baseline modules under `starlab/imitation/`; **no** shell-out to `emit_canonical_state` / `emit_observation_surface` in M27 product code | Benchmark integrity, leaderboard validity, live SC2 in CI, hierarchical control, replay↔execution equivalence, imitation quality beyond internal smoke metrics |
| M28 | `learned_agent_evaluation.json`, `learned_agent_evaluation_report.json` | One M20-valid **`fixture_only`** benchmark contract + frozen **M27** `replay_imitation_baseline.json` + governed **M26** `replay_training_dataset.json` + referenced **M14** bundle dirs; **M16 → M18** materialization + `replay_imitation_predictor`; held-out **`split == "test"`** only in v1 | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M28 `starlab/evaluation/` modules | Benchmark integrity, leaderboard validity, live SC2 in CI, M23 tournament, M24 diagnostics, M25 evidence pack, replay parser in M28 modules, stronger imitation claims than explicit metrics |
| M29 | `hierarchical_agent_interface_schema.json`, `hierarchical_agent_interface_schema_report.json` | JSON Schema + report for **offline** **frame-scoped** **two-level** trace documents (`schema_version` + `hierarchical_decision_trace`); worker **`semantic_coarse_label`** enum owned by M29, aligned 1:1 to **`starlab.m26.label.coarse_action_v1`**; **`label_policy_id`** on `worker_response` anchors the policy family | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M29 `starlab/hierarchy/` modules | Learned hierarchical agent (**M30**), training, benchmark integrity, live SC2, raw action legality, multi-level hierarchy beyond two, multi-worker routing |
| M30 | `replay_hierarchical_imitation_agent.json`, `replay_hierarchical_imitation_agent_report.json` | Governed **M26** `replay_training_dataset.json` + referenced **M14** bundles; **M16 → M18** materialization + M27 observation signatures; fixed **M30** delegate partition (`starlab.m30.delegate.fixed_four_v1`); traces anchor to **`starlab.hierarchical_agent_interface_trace.v1`** | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M30 `starlab/hierarchy/` modules | Benchmark integrity, live SC2, replay explorer / operator evidence surface (**M31**), public flagship proof pack (**M39**), learned delegate discovery, raw action legality |
| M31 | `replay_explorer_surface.json`, `replay_explorer_surface_report.json` | Governed **M14** bundle JSON + frozen **M30** `replay_hierarchical_imitation_agent.json`; **M16 → M18** materialization; **M29** hierarchical trace validation; bounded M10–M12 excerpts | STARLAB JSON; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M31 `starlab/explorer/` modules | Benchmark integrity, live SC2, web UI, replay↔execution equivalence, **M39** public flagship proof pack product |

**Phase II slice / bundle boundary (M13 vs M14):** an M13 **slice** is a **metadata-defined temporal span** over already-governed JSON (addressable `[start_gameloop, end_gameloop]` with lineage). **M14** is where **bundle packaging** and **lineage contract v1** for replay bundles belong — not M13. M13 does not ship clipped replay bytes or M14-style bundles.

### Phase II — Replay Intake, Provenance, and Data Plane

Focus:

- replay intake policy and provenance enforcement
- parser substrate and metadata/timeline/event extraction
- build-order/economy and combat/scouting planes
- replay slices, bundles, and lineage contracts

### Phase III — State, Representation, and Perception Bridge

Focus:

- canonical state schema and structured pipeline
- observation surface contract
- perceptual bridge prototype
- cross-mode reconciliation and representation audit

### Phase IV — Benchmark Contracts, Baselines, and Evaluation

Focus:

- benchmark contracts and scorecard semantics
- scripted and heuristic baselines
- evaluation runner and tournament harness
- attribution/diagnostics and baseline evidence packs

### Phase V — Learning Paths, Evidence Surfaces, and Flagship Proof

Focus:

- replay corpus governance / training dataset contract (**M26**)
- replay-derived imitation baseline (**M27**)
- learned-agent evaluation harness (**M28**)
- hierarchical agent interface (**M29**) and first learned hierarchical agent (**M30**)
- replay explorer / operator evidence surface (**M31**)
- audit closure milestones (**M32–M34**) — coverage visibility, clone-to-run / field-test posture, CI tiering, structural hygiene (corrective program; **not** flagship proof-pack product by themselves)
- audit closure IV — structural decoupling and module decomposition (**M35**); audit closure V — governance surface rationalization and documentation density control (**M36**)
- audit closure VI — coverage margin recovery and CI evidence hardening (**M37**)
- audit closure VII — public face refresh, governance rationalization, and code-health tightening (**M38**)
- public flagship proof pack (**M39** — **closed** on `main`; deterministic pack + CI **`flagship`**; see §11)

### Phase VI — Governed Agent Training, Comparison, and Local Validation

Focus:

- agent training program charter and artifact contract (**M40** — **closed** on `main`; see §11)
- replay-imitation training pipeline (**M41** — **closed** on `main`: deterministic run/report JSON + local sklearn weights; CI fixture-only)
- learned-agent comparison harness (**M42** — **closed** on `main`: compare **M27** vs **M41** on **M28** offline metrics; **local-first**; CI **fixture-only**; **no** live-play expansion here)
- hierarchical training pipeline (**M43** — **closed** on `main`: two-level sklearn manager + workers over M26+M14; `hierarchical_training_run.json` / report under `out/hierarchical_training_runs/`; CI fixture-only; continuity with **M29**/**M30**; **no** live-play expansion here)
- local live-play validation harness (**M44** — **closed** on `main`: bounded local harness + semantic-to-live adapter + replay-backed validation artifacts + optional video registration; **fixture-only** CI; **no** live SC2 in CI; see §11 / §18)
- self-play / RL bootstrap (**M45** — **closed** on `main`: governed bootstrap loop over **M44** rollout substrate; bounded rollout / reward / optional weighted re-fit; **no** live SC2 in CI; **full Phase VI integrated test campaign** is **post-M45** — see §11)
- bounded live **final_status** / **`sc2_game_result`** semantics (**M46** — **closed** on `main`: aligns bounded **burnysc2** validation success with fixture **`ok`**; **not** game victory — see §11)
- bootstrap **episode distinctness** / **operator ergonomics** (**M47** — **closed** on `main`: per-episode M02 `seed`, `starlab.m47.episode_manifest.v2`, `episode_distinctness` / collapse **warnings**, interpretation rules — **not** benchmark strength, **not** sample diversity proof by itself)
- **M42** contract-path alignment (**M48** — **closed** on `main`; [PR #59](https://github.com/m-cahill/starlab/pull/59); see §18 / `M48_run1.md`)
- full local training / bootstrap **campaign charter** + **preflight** (**M49** — **closed** on `main`: contract + preflight emitters + runtime doc + fixture tests — **not** long local campaign execution as merge evidence; see §11 / §18)
- industrial-scale **hidden rollout** + **governed campaign execution** (**M50** — **closed** on `main`: executor over M49 + M45, PID locks, honest requested vs resolved visibility, extended execution preflight — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance; see §11 / §18)
- optional **post-bootstrap protocol phases** on the same executor (**M51** — **closed** on `main`: aggregated refit → honest M42 skip → watchable M44 on refit; phase receipts — **not** M42 semantics extension for refit bundles, **not** benchmark integrity; see §11 / §18)

**Phase VI artifact family (compact):** **M40** — training-program **contract** artifacts (`agent_training_program_contract.json` / report); **M41** — **flat training run** artifacts (`replay_imitation_training_run.json` / report + optional local weights under `out/training_runs/`); **M42** — **comparison** artifacts (`learned_agent_comparison.json` / report under `out/comparisons/`); **M43** — **hierarchical training run** artifacts (`hierarchical_training_run.json` / report + optional local weights under `out/hierarchical_training_runs/`); **M44** — **live validation** artifacts (`local_live_play_validation_run.json` / report + `replay_binding.json` + `replay/validation.SC2Replay` under `out/live_validation_runs/`); **M45** — **bootstrap** artifacts (`self_play_rl_bootstrap_run.json` / report + `bootstrap_dataset.json` + per-episode M44 outputs under `out/rl_bootstrap_runs/`, optional `updated_policy/rl_bootstrap_candidate_bundle.joblib`); **M46** — **no** new artifact family — **field semantics** in existing **M44** proof/run JSON (`final_status`, `sc2_game_result`) — **M40**–**M46** **closed** on `main`; **M47** extends **M45** manifest/report semantics (`episode_distinctness`, warnings on collapsed identities) — **M40**–**M47** **closed** on `main`; **M48** **closed** on `main` (**M42** contract-path alignment). **M49** — **full local campaign** charter (`full_local_training_campaign_contract.json` / report + `campaign_preflight_receipt.json` under `out/training_campaigns/<campaign_id>/`); runtime: `docs/runtime/full_local_training_campaign_v1.md` — **closed** on `main` (**not** long wall-clock campaign execution as merge evidence). **M50** — **governed campaign execution** artifacts under `out/training_campaigns/<campaign_id>/campaign_runs/<execution_id>/` (executor CLI; locks; visibility receipts) — **closed** on `main` (**not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI). **M51** — same execution tree plus optional **post-bootstrap** phases (refit joblib, phase receipts, `hidden_rollout_campaign_run` v2 fields) when `--post-bootstrap-protocol-phases` is set — **closed** on `main` (**not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI). Training and comparison remain **local-first**; CI stays **fixture-only** (no GPU training, no live SC2, no weights in-repo).

### Phase VII — Trust, Equivalence, Benchmark Integrity, and Release Lock

Focus:

- **M52** — V1 endgame recharter & replay↔execution equivalence charter v1 (`docs/runtime/replay_execution_equivalence_charter_v1.md`, `starlab.equivalence`, deterministic charter/report JSON) — **closed** on `main` — **charter / contract only**; **not** paired equivalence proof.
- **M53** — Replay↔execution equivalence evidence surface v1 (**closed** on `main` — bounded evidence profiles; evidence-only JSON — **not** merge-bar semantics).
- **M54** — Replay↔execution equivalence audit & acceptance gates v1 (**closed** on `main` — consumes M53 evidence; deterministic audit + gate pack; profile-scoped outcomes; **not** universal equivalence).
- **M55** — Benchmark integrity charter & split-governance controls v1 (**closed** on `main` — charter + split-governance controls JSON; contract **`starlab.benchmark_integrity_charter.v1`**; **not** benchmark integrity proved; see **Benchmark integrity track** below).
- **M56** — Benchmark integrity evidence & reproducibility gates v1 (**closed** on `main` — runtime `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md`; `starlab.benchmark_integrity` deterministic `benchmark_integrity_evidence.json` / report + `benchmark_integrity_reproducibility_gates.json` / report; scope **`starlab.m56.scope.fixture_only_baseline_chain_v1`**; gate pack **`starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`**; explicit path CLIs — **not** global benchmark integrity proof; see §18 / `M56_run1.md`).

#### Benchmark integrity track (M55 / M56)

| Track | Milestone | Role |
| ----- | --------- | ---- |
| Benchmark integrity | M55 | charter / controls |
| Benchmark integrity | M56 | evidence / reproducibility gates |

**Ledger note:** **M55** defines benchmark-integrity vocabulary, **split_governance_controls**, and **evidence_classes_reserved_for_m56** (future obligations, **not** satisfied by emitting charter JSON). **M56** introduces reproducibility evidence and benchmark-integrity **gate** families. This track is **adjacent but distinct** from the **M52**–**M54** replay↔execution equivalence track (**closed** on `main`).

#### Phase VII track separation (equivalence vs benchmark integrity)

- **Replay↔execution equivalence** uses **M52** (charter) → **M53** (evidence) → **M54** (audit / acceptance gates over M53 evidence).
- **Benchmark integrity** uses **M55** (charter / split governance) → **M56** (evidence / reproducibility gates). **M55** does **not** subsume **M52**–**M54** semantics and does **not** claim equivalence results.

- **M57** — Narrow live SC2 in CI charter & controlled runner v1 (**closed** on `main` — runtime + `starlab.sc2` charter/receipt emitters + optional manual `workflow_dispatch` workflow; **not** merge-gate live SC2; **not** global live-SC2-in-CI proof).
- **M58** — Live SC2 in CI hardening & cost guardrails v1 (**closed** on `main` — runtime + guardrails JSON + preflight receipt + hardened manual workflow; **not** merge-gate live SC2 — follows **M57**).
- **M59** — Ladder/public evaluation protocol & evidence surface v1 (**closed** on `main` — runtime + `starlab.sc2` protocol/evidence emitters + fixture tests — **not** ladder/public **performance** proof; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion).
- **M60** — Audit hardening & v2 readiness v1 (**closed** on `main` — [PR #71](https://github.com/m-cahill/starlab/pull/71); merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`; tag **`v0.0.60-m60`**) — targeted structural debt **relevant to v2 readiness** (private campaign-execution split + guardrails + short audit mapping; historical anchor **M32** revalidated — see `docs/audit/m60_v2_readiness_findings.md`).
- **M61** — SC2 foundation release lock & v1 proof pack (**closed** on `main` — proof pack + audit machinery in repo + operator-local campaign evidence + audit **`ready_within_scope`** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance).

---

## 7. Milestone table

Planned program arc (**62 milestones**, **M00**–**M61**) — **all closed** on `main` (**M52**–**M61** Phase VII **complete**, including **M61** operator-local **`ready_within_scope`** release-lock evidence; tags through **`v0.0.61-m61`** on PR #72 merge commit **`35d7734…`**; **M51** **closed** on `main`):

**Ledger archival policy:** Chronologically older per-milestone table notes (M01–M27) are archived verbatim to `docs/starlab_archive.md` to keep this document readable as current-state truth; **no** history was removed.

| Milestone | Name | Phase | Status | Tag | Audit Score |
| --------- | ---- | ----- | ------ | --- | ----------- |
| M00 | Governance Bootstrap & Ledger Initialization | I | Complete | v0.0.0-m00 | — |
| M01 | SC2 Runtime Surface Decision & Environment Lock | I | Complete | v0.0.1-m01 | — |
| M02 | Deterministic Match Execution Harness | I | Complete | v0.0.2-m02 | — |
| M03 | Run Identity & Lineage Seed | I | Complete | v0.0.3-m03 | — |
| M04 | Replay Binding to Run Identity | I | Complete | v0.0.4-m04 | — |
| M05 | Canonical Run Artifact v0 | I | Complete | v0.0.5-m05 | — |
| M06 | Environment Drift & Runtime Smoke Matrix | I | Complete | v0.0.6-m06 | — |
| M07 | Replay Intake Policy & Provenance Enforcement | II | Complete | v0.0.7-m07 | — |
| M08 | Replay Parser Substrate | II | Complete | v0.0.8-m08 | — |
| M09 | Replay Metadata Extraction | II | Complete | v0.0.9-m09 | — |
| M10 | Timeline & Event Extraction | II | Complete | v0.0.10-m10 | — |
| M11 | Build-Order & Economy Plane | II | Complete | v0.0.11-m11 | — |
| M12 | Combat, Scouting, and Visibility Windows | II | Complete | v0.0.12-m12 | — |
| M13 | Replay Slice Generator | II | Complete | v0.0.13-m13 | — |
| M14 | Replay Bundle & Lineage Contract v1 | II | Complete | v0.0.14-m14 | — |
| M15 | Canonical State Schema v1 | III | Complete | v0.0.15-m15 | — |
| M16 | Structured State Pipeline | III | Complete | v0.0.16-m16 | — |
| M17 | Observation Surface Contract | III | Complete | v0.0.17-m17 | — |
| M18 | Perceptual Bridge Prototype | III | Complete | v0.0.18-m18 | — |
| M19 | Cross-Mode Reconciliation & Representation Audit | III | Complete | v0.0.19-m19 | — |
| M20 | Benchmark Contract & Scorecard Semantics | IV | Complete | v0.0.20-m20 | — |
| M21 | Scripted Baseline Suite | IV | Complete | v0.0.21-m21 | — |
| M22 | Heuristic Baseline Suite | IV | Complete | v0.0.22-m22 | — |
| M23 | Evaluation Runner & Tournament Harness | IV | Complete | v0.0.23-m23 | — |
| M24 | Attribution, Diagnostics, and Failure Views | IV | Complete | v0.0.24-m24 | — |
| M25 | Baseline Evidence Pack | IV | Complete | v0.0.25-m25 | — |
| M26 | Replay Corpus Governance & Training Dataset Contract | V | Complete | v0.0.26-m26 | — |
| M27 | Replay-Derived Imitation Baseline | V | Complete | v0.0.27-m27 | — |
| M28 | Learned-Agent Evaluation Harness | V | Complete | v0.0.28-m28 | — |
| M29 | Hierarchical Agent Interface Layer | V | Complete | v0.0.29-m29 | — |
| M30 | First Learned Hierarchical Agent | V | Complete | v0.0.30-m30 | — |
| M31 | Replay Explorer / Operator Evidence Surface | V | Complete | v0.0.31-m31 | — |
| M32 | Audit Closure I — Coverage, Clone-to-Run Baseline, and Operating Manual Scaffold | V | Complete | v0.0.32-m32 | — |
| M33 | Audit Closure II — CI Tiering, Architecture Surface, and Field-Test Readiness | V | Complete | v0.0.33-m33 | — |
| M34 | Audit Closure III — Structural Hygiene, Deferred-Issue Closure, and Operating Manual Promotion Prep | V | Complete | v0.0.34-m34 | — |
| M35 | Audit Closure IV — Structural Decoupling and Module Decomposition | V | Complete | v0.0.35-m35 | — |
| M36 | Audit Closure V — Governance Surface Rationalization and Documentation Density Control | V | Complete | v0.0.36-m36 | — |
| M37 | Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening | V | Complete | v0.0.37-m37 | — |
| M38 | Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening | V | Complete | v0.0.38-m38 | — |
| M39 | Public Flagship Proof Pack | V | Complete | v0.0.39-m39 | — |
| M40 | Agent Training Program Charter & Artifact Contract | VI | Complete | v0.0.40-m40 | — |
| M41 | Replay-Imitation Training Pipeline v1 | VI | Complete | v0.0.41-m41 | — |
| M42 | Learned-Agent Comparison Harness v1 | VI | Complete | v0.0.42-m42 | — |
| M43 | Hierarchical Training Pipeline v1 | VI | Complete | v0.0.43-m43 | — |
| M44 | Local Live-Play Validation Harness v1 | VI | Complete | v0.0.44-m44 | — |
| M45 | Self-Play / RL Bootstrap v1 | VI | Complete | v0.0.45-m45 | — |
| M46 | Bounded Live Validation Final-Status Semantics | VI | Complete | v0.0.46-m46 | — |
| M47 | Bootstrap Episode Distinctness & Operator Ergonomics | VI | Complete | v0.0.47-m47 | — |
| M48 | Learned-Agent Comparison Contract-Path Alignment | VI | Complete | v0.0.48-m48 | — |
| M49 | Full Local Training / Bootstrap Campaign Charter & Evidence Protocol | VI | Complete | v0.0.49-m49 | — |
| M50 | Industrial-scale hidden rollout & governed campaign execution v1 | VI | Complete | v0.0.50-m50 | — |
| M51 | Governed post-bootstrap phase orchestration v1 | VI | Complete | v0.0.51-m51 | — |
| M52 | V1 Endgame Recharter & Replay↔Execution Equivalence Charter v1 | VII | Complete | v0.0.52-m52 | — |
| M53 | Replay↔Execution Equivalence Evidence Surface v1 | VII | Complete | v0.0.53-m53 | — |
| M54 | Replay↔Execution Equivalence Audit & Acceptance Gates v1 | VII | Complete | v0.0.54-m54 | — |
| M55 | Benchmark Integrity Charter & Split-Governance Controls v1 | VII | Complete | v0.0.55-m55 | — |
| M56 | Benchmark Integrity Evidence & Reproducibility Gates v1 | VII | Complete | v0.0.56-m56 | — |
| M57 | Narrow Live SC2 in CI Charter & Controlled Runner v1 | VII | Complete | v0.0.57-m57 | — |
| M58 | Live SC2 in CI Hardening & Cost Guardrails v1 | VII | Complete | v0.0.58-m58 | — |
| M59 | Ladder/Public Evaluation Protocol & Evidence Surface v1 | VII | Complete | v0.0.59-m59 | — |
| M60 | Audit Hardening & v2 Readiness v1 | VII | Complete | v0.0.60-m60 | — |
| M61 | SC2 Foundation Release Lock & v1 Proof Pack | VII | Complete | v0.0.61-m61 | — |

**Rule:** milestone names may tighten over time, but scope should remain small and reversible by default.

**Historical note (M37 full audit):** the **M37** full-audit artifacts (`M37_fullaudit.md` / JSON), where present, may read **“proceed to flagship”** under an older milestone numbering. The program **later rechartered** the arc to **42 milestones** and inserted corrective work (**M37**–**M38**) before **M39** flagship — audit files are **historical evidence**; this ledger records the **governance decision** without rewriting those documents. After **M39** closeout, the planned arc was **rechartered again** to **46 milestones (M00–M45)** — see §23 changelog (**2026-04-11 — Planned program arc revised to 46 milestones**).

**M01–M27 milestone table notes (historical detail):** Verbatim **§7** notes for **M01** through **M27** are preserved in `docs/starlab_archive.md` (subordinate to this ledger); use them when you need the full “Complete” semantics and non-claims for those milestones.

**M28 note:** **M28** is **merged** to `main` (see §18). **M28** adds **learned-agent evaluation** — deterministic `learned_agent_evaluation.json` + `learned_agent_evaluation_report.json` from a governed **M20** `fixture_only` contract + frozen **M27** baseline + **M26** dataset + **M14** bundles; runtime contract `docs/runtime/learned_agent_evaluation_harness_v1.md`, modules + CLI under `starlab/evaluation/` + `replay_imitation_predictor` under `starlab/imitation/`; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M28 evaluation modules — see §6 Phase V artifact row. **Not** benchmark integrity, **not** M23 tournament semantics, **not** M24/M25 surfaces, **not** live SC2 in CI, **not** replay parser execution in M28 modules, **not** stronger imitation claims than explicit metrics.

**M29 note:** **M29** is **merged** to `main` (see §18). **M29** adds **hierarchical agent interface** — deterministic `hierarchical_agent_interface_schema.json` + `hierarchical_agent_interface_schema_report.json`; runtime contract `docs/runtime/hierarchical_agent_interface_v1.md`, modules + CLI under `starlab/hierarchy/`; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M29 hierarchy modules — see §6 Phase V artifact row. **Green PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **green merge-push `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; superseded red PR-head [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) (Ruff format — **not** merge authority). **Not** learned hierarchical agent (**M30**), **not** benchmark integrity, **not** live SC2 in CI.

**M30 note:** **M30** is **merged** to `main` (see §18). **M30** adds **first learned hierarchical imitation agent** — deterministic `replay_hierarchical_imitation_agent.json` + `replay_hierarchical_imitation_agent_report.json` from governed **M26** + **M14** via **M16 → M18** materialization + fixed delegate policy **`starlab.m30.delegate.fixed_four_v1`**; runtime contract `docs/runtime/replay_hierarchical_imitation_agent_v1.md`, modules + CLI under `starlab/hierarchy/`; **green PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **green merge-push `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; see §18 / `M30_run1.md`. **Not** benchmark integrity, **not** live SC2 in CI, **not** M31 replay explorer product, **not** flagship proof pack.

**M31 note:** **M31** is **merged** to `main` (see §18). **M31** adds **replay explorer / operator evidence surface** — deterministic `replay_explorer_surface.json` + `replay_explorer_surface_report.json` from governed **M14** bundles + frozen **M30** agent + **M16 → M18** materialization + **M29** trace validation; runtime contract `docs/runtime/replay_explorer_surface_v1.md`, modules + CLI under `starlab/explorer/`; **green PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **green merge-push `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; see §18 / `M31_run1.md`. **Not** benchmark integrity, **not** live SC2 in CI, **not** web UI, **not** M39 flagship proof pack product.

**M33 note:** **M33** is **merged** to `main` (see §18). **M33** adds **explicit parallel CI tiering** (workflow **`CI`**, jobs **`quality`** / **`smoke`** / **`tests`** / **`security`** / **`fieldtest`**, final **`governance`**) + **fixture-only** **`fieldtest-output`** CI artifact + **`docs/runtime/ci_tiering_field_test_readiness_v1.md`** + expanded **`docs/architecture.md`**, **`docs/starlab_operating_manual_v0.md`**, clone-to-run / smoke / checklist / session template; **DIR-001**, **DIR-002**, **DIR-007** resolved in `docs/audit/DeferredIssuesRegistry.md`; coverage gate **unchanged** at **75.4**; **green PR-head** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **green merge-push `main`** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md`. **Not** M34 structural hygiene product work, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity, **not** operating manual v1.

**M34 note:** **M34** is **merged** to `main` ([PR #40](https://github.com/m-cahill/starlab/pull/40); **authoritative PR-head CI** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **merge-boundary `main` CI** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; tag **`v0.0.34-m34`**; see §18 / `M34_run1.md`). **M34** closes **DIR-003** (`starlab._io`), **DIR-004** (governance test modules), **DIR-005** (**documentation-only** — all remaining `except Exception` sites validated as adapter/untrusted boundaries; see `docs/audit/broad_exception_boundaries.md`), **DIR-006** (dev dependency upper bounds + `.github/dependabot.yml`). Adds **`docs/diligence/operating_manual_promotion_readiness.md`** (manual remains **non-canonical** v0; **promotion prep only**). Coverage gate **unchanged** at **75.4**. **Not** M39 flagship proof-pack product work, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1 promotion.

**M35 note:** **M35** is **merged** to `main` ([PR #46](https://github.com/m-cahill/starlab/pull/46); **authoritative PR-head CI** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **merge-boundary `main` CI** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) on `5b4d24b…`; tag **`v0.0.35-m35`**; superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) — **not** merge authority; see §18 / `M35_run1.md`). **M35** delivers **structural decoupling** — `M14BundleLoader`, `parser_io` / `replay_slice_generation` / observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39** + **M36–M39** stubs, governance test updates. Coverage gate **unchanged** at **75.4**. **Not** M39 flagship proof-pack product work, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1.

**M37 note:** **M37** is **merged** to `main` ([PR #48](https://github.com/m-cahill/starlab/pull/48); **authoritative PR-head CI** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) on `a38d3a7…`; **merge-boundary `main` CI** [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) on `d2474bd…`; tag **`v0.0.37-m37`**; superseded **failure** PR-head [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — **not** merge authority; see §18 / `M37_run1.md`). **M37** raises **branch-aware** coverage to **~80.34%** (authoritative PR-head) and sets **`fail_under`** to **78.0**; adds **`make check`**, CI **`$GITHUB_STEP_SUMMARY`** coverage TOTAL line, governance alignment to **42** milestones, **`starlab.runs.identity`** cross-platform basename normalization — **~85%** remains a **stretch**, **not** a claim. **Not** M39 flagship proof-pack **product**, **not** benchmark integrity, **not** live SC2 in CI.

**M38 note:** **M38** is **merged** to `main` ([PR #49](https://github.com/m-cahill/starlab/pull/49); **authoritative PR-head CI** [`24272425346`](https://github.com/m-cahill/starlab/actions/runs/24272425346) on `3e00641…`; **merge-boundary `main` CI** [`24291882960`](https://github.com/m-cahill/starlab/actions/runs/24291882960) on `bf6bf4a…`; tag **`v0.0.38-m38`**; superseded PR-head: none; see §18 / `M38_run1.md`). **Proved (narrow, M38):** `README.md` + ledger **Current truth (quick scan)**; governance test dedup + **M07**/**M37** milestone-table row checks; `tests/runpy_helpers.py` + test adoption. **Not** M39 flagship proof-pack **product**, **not** benchmark integrity, **not** live SC2 in CI, **not** gate weakening.

**M39 note:** **M39** is **merged** to `main` ([PR #50](https://github.com/m-cahill/starlab/pull/50); **authoritative PR-head CI** [`24292861437`](https://github.com/m-cahill/starlab/actions/runs/24292861437) on `2c3fce7…`; **merge-boundary `main` CI** [`24293162871`](https://github.com/m-cahill/starlab/actions/runs/24293162871) on `ca97027…`; tag **`v0.0.39-m39`**; superseded PR-head: none; see §18 / `M39_run1.md`). **Proved (narrow, M39):** public flagship **proof pack** — `starlab.flagship`, `make flagship`, CI **`flagship`** + artifact **`flagship-proof-pack`**, runtime + narrative docs; assembles **M25** / **M28** / **M31** JSON under explicit **non_claims** — **not** benchmark integrity, **not** live SC2 in CI, **not** training-track work, **not** Phase VI product beyond **M39**.

**M42 note:** **M42** is **merged** to `main` ([PR #53](https://github.com/m-cahill/starlab/pull/53); **authoritative PR-head CI** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) on `191a955…`; **merge-boundary `main` CI** [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) on `3eb091a…`; tag **`v0.0.42-m42`**; superseded PR-head runs: none — sole run on final head; see §18 / `M42_run1.md`). **Proved (narrow, M42):** first governed **learned-agent comparison harness** — `starlab.evaluation` comparison modules + CLI, `learned_agent_comparison.json` / report, `TrainedRunPredictor`, M28 metric surface reuse, ranking policy `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI; **M43** hierarchical training is **out of scope** for **M42** (delivered in a separate milestone).

**M44 note:** **M44** is **merged** to `main` ([PR #55](https://github.com/m-cahill/starlab/pull/55); **authoritative PR-head CI** [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411) on `dc8e74d…`; **merge-boundary `main` CI** [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) on `1b1067a…`; tag **`v0.0.44-m44`**; **superseded** **failure** PR-head [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) on `c8b989a…` — Ruff format — **not** merge authority; see §18 / `M44_run1.md`). **Proved (narrow, M44):** first governed **local live-play validation harness** — `starlab.sc2` harness + emitter, `local_live_play_validation_run.json` / report, `m43_sklearn_runtime`, bounded adapter **`starlab.m44.semantic_live_action_adapter.v1`**, replay-backed chain (M02/M03/M04), `runtime_mode` `fixture_stub_ci` \| `local_live_sc2`, optional video metadata — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** **M45** RL product.

**M45 note:** **M45** is **merged** to `main` ([PR #56](https://github.com/m-cahill/starlab/pull/56); **authoritative PR-head CI** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) on `0e89081…`; **merge-boundary `main` CI** [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) on `1a585b6…`; tag **`v0.0.45-m45`**; **superseded** **failure** PR-head [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — Ruff format — **not** merge authority; see §18 / `M45_run1.md`). **Proved (narrow, M45):** first governed **self-play / RL bootstrap** surface — `starlab.training` bootstrap pipeline + CLI `python -m starlab.training.emit_self_play_rl_bootstrap_run`, `self_play_rl_bootstrap_run.json` / report, `bootstrap_dataset.json`, **M44** rollout substrate, **M43** candidate + local `joblib`, conservative optional weighted re-fit, bounded `runtime_mode` / `bootstrap_mode` / `reward_policy_id` / `update_policy_id` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** completion of the **Phase VI integrated test campaign** (post-M45).

**M46 note:** **M46** is **merged** to `main` ([PR #57](https://github.com/m-cahill/starlab/pull/57); **authoritative PR-head CI** [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005) on `ddb18f4…`; **merge-boundary `main` CI** [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) on `b925130…` — **failure** (`pip-audit` / pytest CVE); **repaired green `main` CI** [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) on `1b7b25e…` (pytest **≥9.0.3** — CI hygiene); tag **`v0.0.46-m46`**; **post-closeout `main` CI** [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) on `1b33acd…` — **success** (ledger + tag — **not** merge authority); branch `recharter/m44-bounded-live-final-status-semantics` **retained**; see §18 / `M46_run1.md`). **Proved (narrow, M46):** bounded **burnysc2** **`match_execution.final_status="ok"`** at step-cap exit + **`sc2_game_result`** for literal SC2 `Result` — **not** victory, **not** ladder, **not** benchmark integrity. **M42** `--contract` path alignment is **M48** (**closed** on `main`; see §18 / `M48_run1.md`).

**M49 note:** **M49** is **merged** to `main` ([PR #60](https://github.com/m-cahill/starlab/pull/60); **authoritative PR-head CI** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623) on `2780de1…`; **merge-boundary `main` CI** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) on `cad5f2b…`; tag **`v0.0.49-m49`**; superseded **failure** PR-head [`24381216946`](https://github.com/m-cahill/starlab/actions/runs/24381216946), [`24381253831`](https://github.com/m-cahill/starlab/actions/runs/24381253831) — **not** merge authority for final head; see §18 / `M49_run1.md`). **Proved (narrow, M49):** governed **full local training campaign** contract + **preflight** emitters, runtime `docs/runtime/full_local_training_campaign_v1.md`, fixture tests — **not** execution of a long local campaign, **not** learning outcomes proof, **not** live SC2 in CI.

**M50 note:** **M50** is **merged** to `main` ([PR #61](https://github.com/m-cahill/starlab/pull/61); **authoritative PR-head CI** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763) on `a6f0b90…`; **merge-boundary `main` CI** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) on `a0430d3…`; tag **`v0.0.50-m50`**; branch `m50-industrial-hidden-rollout-mode` **retained** on `origin`; see §18 / `M50_run1.md`). **Proved (narrow, M50):** governed **campaign execution** CLI over M49 + M45, PID lockfiles, honest **requested** vs **resolved** visibility, extended execution preflight, execution artifacts under `out/training_campaigns/<campaign_id>/campaign_runs/<execution_id>/` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance.

**M51 note:** **M51** is **merged** to `main` ([PR #62](https://github.com/m-cahill/starlab/pull/62); **authoritative PR-head CI** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222) on `f812f80…`; **merge-boundary `main` CI** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on `1e88466…`; tag **`v0.0.51-m51`**; branch `m51-governed-post-bootstrap-phase-orchestration` **deleted** after merge; see §18 / `M51_run1.md`). **Proved (narrow, M51):** optional **`--post-bootstrap-protocol-phases`** on the M50 executor (aggregated weighted refit phase, orchestrated M42 skip, watchable M44 on refit; `hidden_rollout_campaign_run` v2, per-phase `phase_receipt.json`) — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance, **not** automatic M41 wrapping of M45 refit bundles.

**M52 note:** **M52** is **merged** to `main` ([PR #63](https://github.com/m-cahill/starlab/pull/63); **authoritative PR-head CI** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983) on `11ba11e…`; **merge-boundary `main` CI** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on `c80a47b…`; tag **`v0.0.52-m52`**; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge; superseded **failure** PR-head [`24434871264`](https://github.com/m-cahill/starlab/actions/runs/24434871264) on `a938ac6…` — Ruff format — **not** merge authority; see §18 / `M52_run1.md`). **Proved (narrow, M52):** ledger **M00**–**M61** + Phase VII + charter runtime doc + `starlab.equivalence` deterministic charter/report JSON — **not** paired replay↔execution proof, **not** benchmark integrity, **not** live SC2 in CI.

**M53 note:** **M53** is **merged** to `main` ([PR #64](https://github.com/m-cahill/starlab/pull/64); **authoritative PR-head CI** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924) on `ec166ff…`; **merge-boundary `main` CI** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on `99bd43d…`; tag **`v0.0.53-m53`**; branch `m53-replay-execution-equivalence-evidence-surface` **deleted** after merge; see §18 / `M53_run1.md`). **Proved (narrow, M53):** deterministic `replay_execution_equivalence_evidence.json` / report; bounded profile **`starlab.m53.profile.identity_binding_v1`**; explicit artifact paths — **not** universal replay↔execution equivalence, **not** M54 audit semantics in M53 JSON, **not** benchmark integrity, **not** live SC2 in CI.

**M54 note:** **M54** is **merged** to `main` ([PR #65](https://github.com/m-cahill/starlab/pull/65); **authoritative PR-head CI** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561) on `70f4f2d…`; **merge-boundary `main` CI** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on `773dd19…`; tag **`v0.0.54-m54`**; branch `m54-replay-execution-equivalence-audit-acceptance-gates` **deleted** after merge; see §18 / `M54_run1.md`). **Proved (narrow, M54):** deterministic `replay_execution_equivalence_audit.json` / report over **M53** evidence; gate pack **`starlab.m54.gatepack.identity_binding_acceptance_v1`**; profile-scoped `profile_scope_status` + descriptive `merge_bar_language` — **not** universal replay↔execution equivalence, **not** benchmark integrity, **not** live SC2 in CI, **not** repository branch protection automation.

**M59 note:** **closed** on `main` ([PR #70](https://github.com/m-cahill/starlab/pull/70); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; **final PR head** `074598af81b1c4ce7f3702b4002daacf9adb6bf3`; **authoritative PR-head CI** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360); **merge-boundary `main` CI** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on merge commit `319bc3d…` — **success**; tag **`v0.0.59-m59`**; branch `m59-ladder-public-evaluation-protocol-evidence-surface-v1` **deleted** after merge; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority; see §18 / `M59_run1.md`). **Proved (narrow, M59):** `starlab.sc2` deterministic **`ladder_public_evaluation_protocol.json`** / **`ladder_public_evaluation_protocol_report.json`** + **`ladder_public_evaluation_evidence.json`** / **`ladder_public_evaluation_evidence_report.json`**; runtime `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md`; bounded profile **`starlab.m59.protocol_profile.single_candidate_public_eval_v1`**; JSON-first inputs + synthetic fixture tests — **not** ladder/public **performance** proof, **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in default CI, **not** automated ladder play or scraping.

**M43 note:** **M43** is **merged** to `main` ([PR #54](https://github.com/m-cahill/starlab/pull/54); **authoritative PR-head CI** [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558) on `ffc4284…`; **merge-boundary `main` CI** [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) on `8850e37…`; tag **`v0.0.43-m43`**; superseded PR-head runs on feature branch — [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — **not** merge authority for final head `ffc4284…`; see §18 / `M43_run1.md`). **Proved (narrow, M43):** first governed **hierarchical training run** pipeline — `starlab.hierarchy` training modules + CLI, `hierarchical_training_run.json` / report, optional local-only combined `joblib`, **M40** contract binding, **M29** interface trace schema linkage, **M30** `starlab.m30.delegate.fixed_four_v1`, **delegate_coverage** — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** **M42** comparison consumption of outputs, **not** **M44**–**M45** product.

**M41 note:** **M41** is **merged** to `main` ([PR #52](https://github.com/m-cahill/starlab/pull/52); **authoritative PR-head CI** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) on `7c092ed…`; **merge-boundary `main` CI** [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) on `5e0add12…`; tag **`v0.0.41-m41`**; superseded PR-head runs on the M41 branch — [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190), [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — **not** merge authority for final head `7c092ed…`; see §18 / `M41_run1.md`). **Proved (narrow, M41):** first governed **replay-imitation training pipeline** — `starlab.imitation` training modules, **`replay_imitation_training_run.json`** / report, optional local-only weights (not in repo), **M40** contract binding + feature schema — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** **M42** comparison harness.

**M40 note:** **M40** is **merged** to `main` ([PR #51](https://github.com/m-cahill/starlab/pull/51); **authoritative PR-head CI** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) on `be47d91…`; **merge-boundary `main` CI** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) on `44e8edc…`; tag **`v0.0.40-m40`**; superseded PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) on `6690cd7…` — Ruff format — **not** merge authority; see §18 / `M40_run1.md`). **Proved (narrow, M40):** training-program **charter** — `starlab.training`, deterministic `agent_training_program_contract.json` / report, `docs/runtime/agent_training_program_contract_v1.md`, ledger **42 → 46** milestones, stub **M42**–**M45** — **not** actual training, **not** weights, **not** benchmark integrity, **not** live SC2 in CI, **not** M42+ product.

**M36 note:** **M36** is **merged** to `main` ([PR #47](https://github.com/m-cahill/starlab/pull/47); **authoritative PR-head CI** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **merge-boundary `main` CI** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; tag **`v0.0.36-m36`**; superseded PR-head: none; see §18 / `M36_run1.md`). **M36** delivers **ledger archive** (`docs/starlab_archive.md` for verbatim **M01–M27** §7 notes), **§7** archival policy + **M28–M35** inline notes, governance-test consolidation — coverage gate **unchanged** at **75.4**. **Not** M39 flagship proof-pack **product** code, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1.

## Post-v1 (PV1) — Long Industrial Campaign & Scaling Evidence

**Boundary:** **M00–M61** is the **completed, closed v1** program arc on `main`. **PV1** is **not** a continuation of v1 numbering — there is **no** **M62**. **PV1** engineering and evidence work was **rechartered** under **`PV1-MNN`**. After **PV1** closure, the **PX1** execution-and-demonstration sequence is **rechartered** under **`PX1-MNN`** (**separate** arc — **not** “more PV1 cleanup”). **PV1** is **not** labeled as “Phase VIII” of the original v1 phase map; it is a **separate** governed phase entry in this ledger.

**Phase identity:** **PV1 — Long Industrial Campaign & Scaling Evidence**

**One-sentence charter:** Governed long-run industrial training campaigns on the **already-closed** **M49** / **M50** / **M51** (and related) campaign machinery, with explicit tranche boundaries, checkpoint receipts, watchable validation references, and operator decision gates — **without** widening global non-claims that v1 preserved (benchmark integrity, universal replay↔execution equivalence, ladder/public strength, merge-gate live SC2, multi-environment generalization).

**Private working surface:** Milestone working notes may live under `docs/company_secrets/milestones/post-v1/PV1-MNN/` and are **not** the public source of truth; this section plus §11 **PV1-M00** entry anchor the **public** roadmap.

**Tagging:** **v0.0.NN-m61**-style tags remain the **v1** closure line. **No** new **PV1** tag naming convention is introduced in **PV1-M00** (deferred unless a repo-level need arises).

### PV1 roadmap (planned / optional — not approved execution)

| Milestone | Title | Status | Notes |
| --- | --- | --- | --- |
| `PV1-M00` | Post-v1 Industrial Campaign Charter & Success Criteria | **closed** on `main` ([PR #73](https://github.com/m-cahill/starlab/pull/73)) | Governance-first charter; locks threshold **shape**, tranche/checkpoint/evidence model — **not** numeric campaign commitments; **merge does not** open later PV1 rows |
| `PV1-M01` | Campaign Observability & Checkpoint Discipline | **closed** on `main` ([PR #74](https://github.com/m-cahill/starlab/pull/74)) | Deterministic **`tranche_checkpoint_receipt`** + **`campaign_observability_index`** helpers — **inspection/reference only**; runtime **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`** — **not** Tranche A execution |
| `PV1-M02` | Tranche A Execution Evidence | **closed** on `main` ([PR #76](https://github.com/m-cahill/starlab/pull/76)) | Bounded **operator-local** Tranche A evidence — runtime **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`** — **not** full-run completion; **not** Tranche B |
| `PV1-M03` | Tranche B / Full-Run Completion Evidence | **closed** on `main` (implementation [PR #77](https://github.com/m-cahill/starlab/pull/77); closeout [PR #78](https://github.com/m-cahill/starlab/pull/78)) | Tranche B **completed within scope**; **`full_run_threshold_declaration.md`** = **`threshold-not-met`** (frozen **`full_run_duration_target`** — **not** reinterpreted); runtime **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`**; **`--skip-bootstrap-phases`** — **does not** **alone** charter later milestones |
| `PV1-M04` | Post-Campaign Analysis / Comparative Readout | **closed** on `main` ([PR #79](https://github.com/m-cahill/starlab/pull/79) implementation; [PR #81](https://github.com/m-cahill/starlab/pull/81) closeout) | Deterministic **`pv1_post_campaign_readout.json`** / report + runtime **`docs/runtime/pv1_post_campaign_readout_v1.md`** — **post-campaign comparative readout only** — **not** new execution; **not** threshold reinterpretation |

**Roadmap disclaimer:** **PV1-M00** through **PV1-M04** are **closed** on `main`; **no** later **PV1** row is **opened** unless explicitly chartered (**not** implied by prior merges).

**Governance merge note:** **PV1-M00** through **PV1-M02** merged under **separate** charters; **PV1-M03** **implementation** merged on `main` via [PR #77](https://github.com/m-cahill/starlab/pull/77); **PV1-M03** **milestone closeout** via [PR #78](https://github.com/m-cahill/starlab/pull/78); **PV1-M04** **implementation** merged via [PR #79](https://github.com/m-cahill/starlab/pull/79); **PV1-M04** **milestone closeout** via [PR #81](https://github.com/m-cahill/starlab/pull/81) (**not** implied by **PV1-M03** closeout).

### PV1 evidence surfaces (PV1-M01 — inspection helpers)

| Artifact(s) | Role |
| --- | --- |
| `tranche_checkpoint_receipt.json` / `tranche_checkpoint_receipt_report.json` | Bind a named **tranche** + **checkpoint** to discovered campaign paths; list **required** vs **missing** evidence classes; support operator pause/incomplete flags — **reference only** (`python -m starlab.training.emit_tranche_checkpoint_receipt`). |
| `campaign_observability_index.json` / `campaign_observability_index_report.json` | One-pass **inventory** over an existing `out/training_campaigns/<campaign_id>/` tree (executions, phase receipts, replay bindings, watchable validations) — **reference only** (`python -m starlab.training.emit_campaign_observability_index`). |

**Non-claims:** these artifacts **do not** fabricate execution evidence, **do not** prove a full-run threshold, and **do not** widen benchmark / equivalence / ladder / live-SC2 posture.

### PV1 evidence surfaces (PV1-M02 — Tranche A operator-local execution)

| Artifact(s) | Role |
| --- | --- |
| **`tranche_a_operator_note.md`** (canonical basename at campaign root) | Operator-authored **Tranche A posture** (completed / not completed within scope) + **continue / pause / stop** — **not** full-run threshold; **not** Tranche B. |
| M49 / M50 / M51 tree | `full_local_training_campaign_contract.json`, preflight receipts, `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json`, phase receipts as run — see **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`**. |
| PV1-M01 index + checkpoint | Same inspection helpers as above — **reference only** at tranche boundary. |

**Non-claims:** **PV1-M02** is **bounded Tranche A execution evidence only** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **not** Tranche B / full-run threshold — those are **PV1-M03** (see §11).

### PV1 evidence surfaces (PV1-M03 — Tranche B / full-run threshold)

| Artifact(s) | Role |
| --- | --- |
| **`tranche_b_operator_note.md`** (canonical basename at campaign root) | Operator-authored **Tranche B posture** (completed / not completed within scope) + **continue / pause / stop** — **not** interchangeable with the threshold declaration. |
| **`full_run_threshold_declaration.md`** | Operator-authored **`threshold-met`** or **`threshold-not-met`** vs the **frozen** PV1 full-run threshold block — **not** Tranche A/B tranche posture alone. |
| M49 / M50 / M51 tree | Same campaign root may host **multiple** `execution_id` trees; continuation may use **`--skip-bootstrap-phases`** when the sealed protocol lists earlier tranches — see **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`**. |
| PV1-M01 index + checkpoint | **`tranche_b`** / **`tranche_b_close`** checkpoint receipt + campaign observability index — **reference only**. |

**Non-claims:** **PV1-M03** is **Tranche B / bounded full-run completion evidence only** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **PV1-M04** is **closed** on `main` (readout milestone — **not** new execution) — **not** **PV1-M05** unless separately chartered.

### Canonical PV1 operator artifacts (campaign root)

These **canonical basenames** live at the **`out/training_campaigns/<campaign_id>/`** root in governed campaigns (operator-local trees **not** committed by default):

| Artifact | Role |
| --- | --- |
| **`tranche_a_operator_note.md`** | Operator **Tranche A** posture (`completed within scope` / not) + `execution_id` — **not** interchangeable with threshold posture. |
| **`tranche_b_operator_note.md`** | Operator **Tranche B** posture + `execution_id` — **not** interchangeable with **`full_run_threshold_declaration.md`**. |
| **`full_run_threshold_declaration.md`** | Operator full-run **`threshold-met`** / **`threshold-not-met`** vs the **frozen** PV1 threshold block — **threshold posture only**. |

**Related:** **PV1-M04** readout emitter (`python -m starlab.training.emit_pv1_post_campaign_readout`) — **`docs/runtime/pv1_post_campaign_readout_v1.md`**.

---

## Post-PV1 (PX1) — Full Industrial Run & Demonstration Proof

**Boundary:** **PX1** is a **new** governed phase **after** the **closed** **PV1** arc. It is **not** “Phase VIII” of **v1**; it is **not** “more PV1 cleanup”; there is **no** **M62**. Post-PV1 execution-and-demonstration work is chartered under **`PX1-MNN`**.

**Phase identity:** **PX1 — Full Industrial Run & Demonstration Proof**

**One-sentence charter:** **PX1 is a governed post-PV1 execution-and-demonstration phase focused on completing a true full industrial-grade training run on the closed STARLAB substrate and producing bounded, evidence-backed proof that a selected agent can play well enough to win in a governed demonstration, without silently upgrading benchmark, equivalence, ladder, or live-CI claims.**

**Pre-v2 bridge (explicit):** **PX1** exists to close **PX1-class gaps** (industrial run completion, bounded play quality, governed demo/video proof) **before** **v2** is considered. **v2** does **not** open automatically when PX1 ends; **PX1-M00** does **not** open **v2**.

**Public runtime charter:** **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`**

**PX1-M01 execution runtime (full industrial run):** **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**

**PX1-M01 execution evidence (operator-local campaign root — canonical basenames):**

| Artifact | Role |
| --- | --- |
| `tranche_a_operator_note.md` | Tranche A posture (**within scope** / not) — **not** the full-run threshold declaration |
| `tranche_b_operator_note.md` | Tranche B posture — **not** the full-run threshold declaration |
| `px1_full_run_operator_note.md` | Whole-campaign operator posture vs frozen rules |
| `full_run_threshold_declaration.md` | **`threshold-met`** / **`threshold-not-met`** vs **frozen PX1 block** |
| `checkpoints/tranche_a_close/`, `checkpoints/tranche_b_close/` | Preserved checkpoint receipts (bounded **PV1**/**PX1** discipline) |

**PX1-M02 play-quality runtime (demo candidate selection):** **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**

**PX1-M03 demo-readiness remediation runtime (candidate strengthening — not winning-video):** **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`**

**PX1-M04 governed demo proof pack runtime (packaging / proof governance — not remediation):** **`docs/runtime/px1_governed_demo_proof_pack_v1.md`**

**PX1 demo-candidate evidence (operator-local campaign / evaluation root — canonical basenames):**

| Artifact | Role |
| --- | --- |
| `px1_play_quality_operator_note.md` | Operator posture vs frozen protocol (candidate set, opponents, interruptions) |
| `demo_candidate_selection_declaration.md` | Exactly **`candidate-selected`** or **`no-candidate-selected`** |
| `px1_play_quality_protocol.json` | Frozen evaluation protocol (+ `px1_play_quality_protocol_report.json`) |
| `px1_play_quality_evidence.json` | Observed evaluation results (+ `px1_play_quality_evidence_report.json`) |

**Private working surface:** Milestone notes may live under `docs/company_secrets/milestones/post-v1/PX1-MNN/` (not committed by default). This section + §11 anchor the **public** roadmap.

### PX1 roadmap (PX1-M00 **closed**; **PX1-M01** **closed**; **PX1-M02** **closed**; **PX1-M03** **closed**; **PX1-M04** **closed**; **PX1-M05** **optional / not yet opened**)

**Recharter note:** **PX1-M03** was rechartered from a prior “demo proof pack / winning video” placeholder because **PX1-M02** closed honestly with **`no-candidate-selected`** — more bounded capability uplift and a fresh remediation evaluation were required before a governed demo attempt (**PX1-M04**) could be justified.

| Milestone | Title | Status | Notes |
| --- | --- | --- | --- |
| `PX1-M00` | Full Industrial Run & Demonstration Charter | **closed** on `main` ([PR #83](https://github.com/m-cahill/starlab/pull/83) implementation; [PR #84](https://github.com/m-cahill/starlab/pull/84) closeout) | Governance-first charter; defines run success, play-quality success, demo/video success, non-claims, and PX1 roadmap — **no** campaign execution; **no** demo recording |
| `PX1-M01` | Full Industrial Campaign Execution Evidence | **closed** on `main` (milestone closeout [PR #87](https://github.com/m-cahill/starlab/pull/87)) | **Frozen** threshold package in **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; **authoritative** operator-local run + honest **`threshold-met`** — **not** play-quality (**PX1-M02**) or demo readiness (**PX1-M03**/**PX1-M04**) |
| `PX1-M02` | Play-Quality Evaluation & Demo Candidate Selection | **closed** on `main` (opening [PR #88](https://github.com/m-cahill/starlab/pull/88); closeout [PR #89](https://github.com/m-cahill/starlab/pull/89)) | Bounded **`local_live_sc2`** evaluation under **protocol v2**; honest **`no-candidate-selected`** — **not** **PX1-M01** reinterpretation; **not** demo readiness closure; **not** ladder proof |
| `PX1-M03` | Candidate Strengthening & Demo Readiness Remediation | **closed** on `main` (opening [PR #90](https://github.com/m-cahill/starlab/pull/90); closeout [PR #91](https://github.com/m-cahill/starlab/pull/91)) | **Remediation** milestone after **PX1-M02** **`no-candidate-selected`**; bounded hybrid live surface + frozen **`px1_demo_readiness_*`** protocol; **closed** with **`demo-ready-candidate-selected`** — **not** the final proof-pack milestone (**PX1-M04**) |
| `PX1-M04` | Governed Demo Proof Pack & Winning Video | **closed** on `main` (opening [PR #92](https://github.com/m-cahill/starlab/pull/92); closeout [PR #93](https://github.com/m-cahill/starlab/pull/93)) | **Packaging** + proof governance after successful **PX1-M03**; runtime **`docs/runtime/px1_governed_demo_proof_pack_v1.md`** — **not** default gameplay tuning; **not** new campaign |
| `PX1-M05` | Optional Demo Hardening / Strategic Recharter Decision | **optional / not yet opened** | Polish, packaging, or explicit post-demo strategic decision **only if needed** |

**Roadmap disclaimer:** **PX1-M00**–**PX1-M04** (closed) do **not** imply **PX1-M05** is required; **PX1-M05** does **not** open automatically from **PX1-M04** closeout. **PX1** is **not** implied by closed **PV1** merges.

#### PX1 canonical demo artifacts (PX1-M04 — initial references)

| Artifact | Reference |
| --- | --- |
| **Candidate id** | `px1_m01_weighted_refit_rl_bootstrap_v1` (unchanged from PX1-M03) |
| **Primary canonical run directory** | `runs/scripted_01` (under PX1-M03 watchable-capture evaluation series root — operator-local) |
| **Replay** | `runs/scripted_01/replay/validation.SC2Replay` (per sealed run JSON `replay.replay_file`) |
| **Operator-captured video (local)** | `out/px1_m03_operator_watchable.mp4` |
| **PX1-M03 declaration** | **`demo-ready-candidate-selected`** (authoritative remediation series) |
| **Runtime contract** | **`docs/runtime/px1_governed_demo_proof_pack_v1.md`** |
| **Selection memo** | **`docs/company_secrets/milestones/post-v1/PX1-M04/PX1-M04_canonical_demo_selection.md`** |

**Ledger truths (PX1 phase — historical; program `current milestone` = quick scan / §11 / `V15-M00` + Post-PX1 (PX2) history; v1.5 detail `docs/starlab-v1.5.md`):**

- **v1** (**M00–M61**) is **complete** and **historical**.
- **PV1** (**PV1-M00**–**PV1-M04**) is **complete** and **historical**; bounded **PV1** outcome is **not** reinterpreted here.
- **PX1** is **separate** from **PV1**; **PX1-M00** established the **PX1** charter and roadmap (**governance only**).
- **PX1-M04** **closed** on `main` ([PR #93](https://github.com/m-cahill/starlab/pull/93)) — **packaging / proof governance** only — **does not** auto-open **`PX1-M05`** or **v2**. **PX1-M03** **`demo-ready-candidate-selected`**; **PX1-M02** **`no-candidate-selected`** (**preserved**); **PX1-M01** **`threshold-met`** — industrial run **only**.
- **v2** is **not** opened.
- **`PX1-M05`** is **optional / not yet opened** — **does not** open automatically from **PX1-M04** closeout.
- **Governed demo proof pack** narrative is **frozen** in runtime + private memos; physical large binaries remain operator-local.

### Explicit non-claims (PX1 phase)

PX1 **does not** silently authorize: global benchmark integrity; universal replay↔execution equivalence; ladder/public-strength claims; live SC2 in CI as default merge norm; multi-environment generalization beyond declared scope; automatic **v2** readiness; or the equation “winning bounded demo” ⇒ broad strategic superiority.

---

## Post-PX1 (PX2) — Autonomous Full-Game Skill Development

**Boundary:** **PX1 proved industrial execution, bounded remediation, and governed demo/video packaging; PX2 is the first separate post-PX1 phase aimed at autonomous full-game strength development.**

> **PX1 proved demo-proof packaging and bounded remediation; PX2 is the first phase aimed at autonomous full-game strength development.**

**Why a new phase:** **PX1** closed the industrial-run and governed demo/video **proof** arc. **PX2** is a **new** capability-development program with its own **`PX2-MNN`** namespace — **not** a continuation of **PX1** packaging milestones and **not** **v2** (which remains separately rechartered).

**Phase identity:** **PX2 — Autonomous Full-Game Skill Development**

**One-sentence charter:** **PX2 develops autonomous full-game Terran 1v1 play strength on the closed STARLAB substrate under explicit evaluation and promotion rules — without silently upgrading benchmark, equivalence, ladder, or live-CI claims.**

**Public runtime charter:** **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`**

**Private working surface:** Milestone notes may live under **`docs/company_secrets/milestones/post-v1/PX2-MNN/`** (not committed by default). This section + §11 anchor the **public** roadmap.

**PX2-M03 opening discipline:** **`PX2-M03`** opens only after a **positive** readiness/preflight decision recorded in **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`** — **not** automatically when **`PX2-M02`** closes. That readiness decision **permits** the milestone; committed implementation slices include **governed campaign wiring + fixture smoke** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** — **slice 2** — **execution skeleton** + **run manifest** + **checkpoint/eval receipts** — **slice 3** — **operator-local execution preflight** + bounded **real-weights** smoke — **slice 4** — **multi-step continuity** + **sealed linkage** + **promotion/rollback receipts** — **slice 5** — **operator-local campaign-root manifest** + **opponent-pool rotation hardening** — and **slice 6** — **preflight seal normalization** + **canonical operator-local campaign-root smoke path** — and **slice 7** — **first bounded operator-local real-run execution record** — and **slice 8** — **bounded operator-local multi-run session** under one campaign root — and **slice 9** — **bounded session + one governed promotion/rollback execution step** — and **slice 10** — **bounded current-candidate carry-forward** after transition (`px2_self_play_current_candidate.json`) — and **slice 11** — **bounded continuation run** that **consumes** the current-candidate pointer (`px2_self_play_continuation_run.json`) — and **slice 12** — **bounded post-continuation current-candidate re-anchoring** (`px2_self_play_current_candidate_reanchor.json`) — and **slice 13** — **bounded second continuation hop** + optional symmetric re-anchor (`px2_self_play_second_hop_continuation.json`) — and **slice 14** — **bounded pointer-seeded** operator-local run (`px2_self_play_pointer_seeded_run.json`) — and **slice 15** — **bounded post–pointer-seeded handoff** (`px2_self_play_pointer_seeded_handoff.json`, lineage from slice-14 pointer-seeded run) — and **slice 16** — **bounded handoff-anchored** operator-local run (`px2_self_play_handoff_anchored_run.json`, declared anchor = slice-15 handoff JSON) — **after slice 16** — **bounded substantive execution** (`px2_self_play_bounded_substantive_execution.json`, §8q). After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale. — **not** the operator-local industrial Blackwell-scale run (still **within** **`PX2-M03`**, later).

| Track | Scope |
| --- | --- |
| **`PX2-M03` slice 1** | Campaign contract/profile, policy-runtime bridge, snapshot/opponent-pool stub, fixture-only smoke validation (CI-safe) |
| **`PX2-M03` slice 2** | PX2-native bounded execution skeleton, `run_manifest.json`, sealed `px2_self_play_campaign_run.json`, checkpoint + evaluation **receipt** artifacts (fixture-only) — **not** industrial campaign completion |
| **`PX2-M03` slice 3** | `px2_self_play_execution_preflight` + sealed operator-local smoke (`real` weights file or init-only), weight file SHA-256 — **not** industrial campaign; **not** default merge-gate live operator path |
| **`PX2-M03` slice 4** | Bounded **multi-step continuity** (`run_operator_local_campaign_continuity`), checkpoint/eval linkage, `continuity_chain.json`, **promotion** + **rollback** receipt JSON — **not** industrial run; **not** **PX2-M04** |
| **`PX2-M03` slice 5** | **Campaign-root manifest** (`px2_self_play_campaign_root_manifest.json`), **`opponent_pool/`** metadata, **`runs/<run_id>/`** continuity trees, **opponent rotation traces** in continuity JSON — **not** industrial run; **not** full anti-collapse |
| **`PX2-M03` slice 6** | **`preflight_seal_basis`** / logical-path normalization for **`preflight_sha256`**; **`out/px2_self_play_campaigns/<campaign_id>/`** canonical bounded smoke (`execution_kind` slice-6) — **not** industrial run; **not** full machine portability of every field |
| **`PX2-M03` slice 7** | **`px2_self_play_operator_local_real_run.json`** — bounded **real filesystem** operator-local run + sealed identity (`execution_kind` slice-7) — **not** industrial run; **not** ladder strength |
| **`PX2-M03` slice 8** | **`px2_self_play_operator_local_session.json`** — **multiple** bounded runs under one campaign root + per-run **`runs/<run_id>/px2_self_play_operator_local_real_run.json`** (`execution_kind` slice-8) — **not** industrial run; **not** multi-day scale |
| **`PX2-M03` slice 9** | **`px2_self_play_operator_local_session_transition.json`** — session-level **promotion** or **rollback** stub bound to per-run receipt lineage — **not** **PX2-M04** exploit closure; **not** industrial run |
| **`PX2-M03` slice 10** | **`px2_self_play_current_candidate.json`** — sealed **current-candidate** pointer (checkpoint + **`weight_identity`**) after transition — **not** global best policy; **not** **PX2-M04** |
| **`PX2-M03` slice 11** | **`px2_self_play_continuation_run.json`** — validates next-run inputs against **`px2_self_play_current_candidate.json`**, runs one bounded continuity pass, records **`consumed_ok`** or **`rejected_mismatch`** — **not** industrial execution; **not** **PX2-M04** exploit closure |
| **`PX2-M03` slice 12** | **`px2_self_play_current_candidate_reanchor.json`** — after **`consumed_ok`** continuation, refreshes **`px2_self_play_current_candidate.json`** anchor to continuation run — **not** industrial execution; **not** **PX2-M04** |
| **`PX2-M03` slice 13** | **`px2_self_play_second_hop_continuation.json`** — second bounded continuation on post-slice-12 pointer + optional **`px2_self_play_current_candidate_reanchor.json`** refresh — **not** industrial execution; **not** **PX2-M04** |
| **`PX2-M03` slice 14** | **`px2_self_play_pointer_seeded_run.json`** — bounded operator-local run whose **declared seed** is the latest **`px2_self_play_current_candidate.json`** (self-seal + lineage checks) — **not** industrial execution; **not** **PX2-M04** |
| **`PX2-M03` slice 15** | **`px2_self_play_pointer_seeded_handoff.json`** — validates **`seeded_ok`** slice-14 pointer-seeded run + binds continuity/manifest SHAs as governed **next-step lineage** — **not** industrial execution; **not** **PX2-M04** |
| **`PX2-M03` slice 16** | **`px2_self_play_handoff_anchored_run.json`** — bounded operator-local pass whose **declared anchor** is slice-15 **`px2_self_play_pointer_seeded_handoff.json`** (`handed_off_ok` + lineage checks) — **not** industrial execution; **not** **PX2-M04** |
| **`PX2-M03` §8q bounded substantive** | **`px2_self_play_bounded_substantive_execution.json`** — post–slice-16, **not** a numbered slice; first **bounded substantive** operator-local execution (`EXECUTION_KIND_BOUNDED_SUBSTANTIVE`, default **15** steps) — **not** industrial execution; **not** **PX2-M04** |
| **Later `PX2-M03` execution** | Operator-local industrial self-play (Blackwell-class **intent**), long-run checkpoints/evals/promotion as implemented — **not** claimed by slices 1–16 or §8q alone |

### PX2 roadmap (**PX2-M00**–**`PX2-M03`** **closed** on the ledger; **`PX2-M04`**–**`PX2-M05`** **planned**; program **`V15-M00`**, **v1.5** — authority **`docs/starlab-v1.5.md`**)

| Milestone | Title | Status | Notes |
| --- | --- | --- | --- |
| `PX2-M00` | Autonomous Full-Game Agent Charter & Success Criteria | **closed** on `main` (governance closeout [PR #94](https://github.com/m-cahill/starlab/pull/94)) | Governance-first: phase identity, Terran-first scope, full-game definitions, scaffolding rules, promotion ladder, non-claims — **no** runtime expansion; **no** training implementation; **no** Blackwell campaign |
| `PX2-M01` | Full Terran Runtime & Action Surface | **closed** on `main` ([PR #95](https://github.com/m-cahill/starlab/pull/95)) | Public **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`**; `starlab.sc2.px2` — structured actions, legality, compiler, receipts — **not** training; **not** strength proof |
| `PX2-M02` | Neural Bootstrap from Replays | **closed** on `main` ([PR #96](https://github.com/m-cahill/starlab/pull/96)) | **`docs/runtime/px2_neural_bootstrap_from_replays_v1.md`**; `starlab.sc2.px2.bootstrap` — replay labeler, dataset, first neural policy, eval — **replay-bootstrap only**; **not** self-play; **not** strength proof |
| `PX2-M03` | Industrial Self-Play Campaign | **closed** (ledger / transition) | Preflight **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**; **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** — slices 1–16 (through handoff-anchored bounded run) + **§8q bounded substantive** — **not** a long **GPU** run as a **program** deliverable; **not** **PX2-M04**; **not** demo refresh; **v1.5** = **`V15-M00`** (see **`docs/starlab-v1.5.md`**) |
| `PX2-M04` | Promotion, Evaluation, and Exploit Closure | **planned** | Checkpoint promotion + exploit-closure readout |
| `PX2-M05` | Demo Refresh / Proof Pack | **planned** | Demo/proof **after** stronger full-game agent exists |

**PX2 evidence chain (compact):**

| Milestone | Role |
| --- | --- |
| **PX2-M00** | Phase charter & claim boundaries |
| **PX2-M01** | Runtime / action substrate (Terran core v1) |
| **PX2-M02** | Replay-bootstrap dataset + first neural policy |
| **PX2-M03** | Industrial self-play |
| **PX2-M04** | Promotion / exploit closure |
| **PX2-M05** | Demo / proof refresh |

**Roadmap disclaimer:** **`PX2-M03`** is **not** opened automatically by **`PX2-M02`** closeout — **readiness doc** + governance PR required. **`PX2-M04`**+ are **not** opened automatically by **`PX2-M03`**. **PX2-M02** was **not** opened automatically by **PX2-M01** closeout (separate governance). **PX2-M01** was **not** opened automatically by **PX2-M00** closeout (separate governance).

### Explicit non-claims (PX2 phase)

PX2 **does not** silently authorize: ladder/public strength proof; benchmark universality; multi-race coverage; **v2** opening; automatic Blackwell execution; or “charter merged” ⇒ “strong agent exists.” **PX2** (through **PX2-M03** closeout) does **not** claim a **long wall-clock GPU training session** as a **completed program** outcome — that is a **v1.5** / **`V15-M00+`** matter. **PX2-M00** does **not** implement the Terran action surface, replay training, or industrial campaigns. **`PX2-M01`** **delivered** the **Terran runtime/action substrate** — **not** replay-bootstrap training (**PX2-M02**), **not** industrial Blackwell campaigns as **proved** in **CI** (**PX2-M03** implementation), **not** autonomous strength proof.

**Ledger truths (PX2 phase, **closeout**; program **current** v1.5 = **`V15-M04`** (**not** started); **last closed** v1.5 = **`V15-M03`** / **`V15-M02`** / … — authority **`docs/starlab-v1.5.md`**; M03 runtime (closed) `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`):**

- **PX2** is **separate** from **PX1** — **PX1-M04** did **not** open **PX2**; **PX2** was **opened** by explicit governance (**PX2-M00** on [PR #94](https://github.com/m-cahill/starlab/pull/94)). **PX2** (through **`PX2-M03`**) is **closed** / **transition-complete** for the post-v1 transition; **PX2** did **not** perform a **long wall-clock GPU** training run as a **Program** deliverable.
- **`PX2-M00`** **closed** on `main` — charter & success criteria **recorded** — **not** proof of strength.
- **`PX2-M01`** **closed** on `main` ([PR #95](https://github.com/m-cahill/starlab/pull/95)) — Terran core v1 runtime/action surface — **not** training; **not** Blackwell execution; **not** strength certification.
- **`PX2-M02`** **closed** on `main` ([PR #96](https://github.com/m-cahill/starlab/pull/96)) — first **replay-bootstrap** supervised path over **M01** — **not** industrial self-play evidence; **not** strength proof.
- **`PX2-M03`** **closed** on the ledger — industrial self-play **campaign** implementation + **bounded** operator-local **surfaces** (operator-local / Blackwell-class **intent** in narrative; **readiness** **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**) — **slice 1** + **slice 2** + **slice 3** + **slice 4** + **slice 5** + **slice 6** + **slice 7** + **slice 8** + **slice 9** + **slice 10** + **slice 11** + **slice 12** + **slice 13** + **slice 14** + **slice 15** + **slice 16** + **§8q bounded substantive** — **not** a **long GPU** training **campaign** as a **default** or **proven** program outcome; **not** industrial Blackwell-scale completion; **not** merge-gate long-run execution; **not** **PX2-M04** promotion/exploit closure.
- **`PX1-M05`** remains **optional / not yet opened**; **v2** remains **not** opened.

### Post-PX2 transition & **v1.5** (**V15**) — public authority

**Status:** **PX2** (through **PX2-M03** governed closeout) is **transition-complete** on the repo ledger. **v1.5** program governance (charter, gates, milestone map, non-claims, artifact family names) lives in **`docs/starlab-v1.5.md`** — **not** duplicated here. Strategic anchor: **`docs/starlab-v1.5moonshot.md`**. **Not** **v2**. **Not** **PX2-M04** auto-opened.

**Unresolved M32-family / structural risks** are tracked in **`docs/starlab-v1.5.md`** §11 (carry-forward).

---

## 8. Milestone intent map

This section exists so each milestone has a stable “why,” not just a title.

| Milestone | Intent |
| --------- | ------ |
| M00 | Make the project legible, governed, and safe to start |
| M01 | Decide the SC2 runtime boundary and lock the environment posture |
| M02 | Prove deterministic, controlled match execution is possible |
| M03 | Seed run identity and lineage primitives |
| M04 | Bind replays to run identity |
| M05 | Establish the first canonical run artifact boundary |
| M06 | Detect environment drift and define runtime smoke expectations |
| M07 | Enforce replay intake and provenance rules |
| M08 | Stand up replay parsing substrate |
| M09 | Extract replay metadata reliably |
| M10 | Extract timelines and event streams |
| M11 | Extract build-order and economy structure |
| M12 | Extract combat, scouting, and visibility windows |
| M13 | Generate reusable replay slices |
| M14 | Package replay bundles with lineage contract v1 |
| M15 | Define canonical state schema v1 |
| M16 | Materialize one canonical state frame per gameloop from M14 bundles |
| M17 | Define observation surface contract |
| M18 | Prototype perceptual bridge |
| M19 | Reconcile modes and audit representations |
| M20 | Define benchmark contracts and scorecard semantics |
| M21 | Scripted baseline suite |
| M22 | Heuristic baseline suite |
| M23 | Evaluation runner and tournament harness (fixture-only tournament consumer; **M23** proves runner/harness mechanics — **not** benchmark integrity) |
| M24 | Attribution, diagnostics, and failure views |
| M25 | Baseline evidence pack |
| M26 | Replay corpus governance and training dataset contract |
| M27 | Replay-derived imitation baseline |
| M28 | Learned-agent evaluation harness (offline frozen baseline vs M20 contract; **not** benchmark integrity) |
| M29 | Hierarchical agent interface layer (contract-first two-level manager→worker trace; **not** learned policy) |
| M30 | First learned hierarchical agent (offline imitation; fixed four-delegate policy; **not** benchmark integrity) |
| M31 | Replay explorer / operator evidence surface |
| M32 | Audit closure I — coverage visibility, clone-to-run baseline, operating manual scaffold |
| M33 | Audit closure II — CI tiering, architecture surface, field-test readiness |
| M34 | Audit closure III — structural hygiene, deferred-issue closure, operating manual promotion prep |
| M35 | Audit closure IV — structural decoupling and module decomposition |
| M36 | Audit closure V — governance surface rationalization and documentation density control |
| M37 | Audit closure VI — coverage margin recovery and CI evidence hardening |
| M38 | Audit closure VII — public face refresh, governance rationalization, and code-health tightening |
| M39 | Public flagship proof pack |
| M40 | Agent training program charter and artifact contract (governance; no model training) |
| M41 | First governed replay-imitation training run artifact + local training path (sklearn; not benchmark integrity) |
| M42 | First governed learned-agent comparison harness — compare frozen M27 baseline and M41 training-run candidates on the M28 offline evaluation surface; ranking policy + pairwise deltas (**not** benchmark integrity; **closed** on `main`) |
| M43 | First governed hierarchical training run artifact and local hierarchical training path (sklearn manager + workers; M29/M30 binding; **not** benchmark integrity; **closed** on `main`) |
| M44 | Local live-play validation harness v1 — replay-backed validation for an **M43** hierarchical candidate (**closed** on `main`; see §11 / §18) |
| M45 | First governed rollout / self-play / RL bootstrap artifact over M43 + M44 surfaces (bounded bootstrap; not full RL product) |
| M46 | Align bounded **burnysc2** `match_execution.final_status` with fixture validation success (`ok` at step-cap exit); preserve literal SC2 `Result` as `sc2_game_result` — **not** victory, **not** ladder, **not** benchmark integrity |
| M47 | M45 **bootstrap episode distinctness** (per-episode M02 `seed`, manifest v2, collapse warnings) + **operator ergonomics** — **not** benchmark integrity |
| M48 | Align **M42** benchmark vs **M40** charter CLI paths + M41 identity check — **closed** on `main` (**not** bounded live semantics beyond contract-path clarity) |
| M49 | Full local training / bootstrap campaign charter + preflight — **closed** on `main` (contract + preflight + docs + tests; **not** long-run execution proof) |
| M50 | Industrial-scale hidden rollout & governed campaign execution v1 — executor + locks + honest visibility (**closed** on `main`; see §11 / §18) |
| M51 | Governed post-bootstrap phase orchestration v1 — optional refit + M42 skip + watchable M44 on refit (orchestration; **closed** on `main`; **not** M42 semantics extension for refit bundles) |
| M52 | V1 endgame recharter & replay↔execution equivalence charter v1 — ledger recharter M00–M61; Phase VII; runtime `replay_execution_equivalence_charter_v1.md` + `starlab.equivalence` emits charter JSON — **closed** on `main` — **not** paired equivalence proof |
| M53 | Replay↔execution equivalence evidence surface v1 — bounded evidence + `identity_binding_v1` profile (**closed** on `main`; evidence-only JSON; **not** universal equivalence) |
| M54 | Replay↔execution equivalence audit & acceptance gates v1 — **closed** on `main` (deterministic audit over M53 evidence; first gate pack; profile-scoped outcomes; **not** universal equivalence) |
| M55 | Benchmark integrity charter & split-governance controls v1 — **closed** on `main` (**charter-only** JSON + runtime contract; **M56** = evidence/gates) |
| M56 | Benchmark integrity evidence & reproducibility gates v1 — **closed** on `main` (bounded fixture-only chain; **not** global benchmark integrity proof) |
| M57 | Narrow live SC2 in CI charter & controlled runner v1 — **closed** on `main` (charter + controlled runner over **M44**; **not** merge-gate live SC2; **not** global live-SC2-in-CI proof) |
| M58 | Live SC2 in CI hardening & cost guardrails v1 — **closed** on `main` (bounded **M57** hardening + cost guardrails — **not** global live-SC2-in-CI proof) |
| M59 | Ladder/public evaluation protocol & evidence surface v1 — **closed** on `main` (bounded descriptive protocol + evidence JSON — **not** ladder/public **performance** proof) |
| M60 | Audit hardening & v2 readiness v1 — **closed** on `main` (private campaign executor split + guardrails + audit mapping — **not** new product artifact claims) |
| M61 | SC2 foundation release lock & v1 proof pack — **closed** on `main` (release-lock emitters + docs + operator-local **`ready_within_scope`** evidence — **not** global benchmark / equivalence / ladder / merge-gate live SC2 claims) |
| PX2-M00 | Freeze separate **PX2** phase identity, Terran-first scope, claim boundaries, training/eval regime shape, and promotion ladder for autonomous full-game skill development — **closed** on `main` ([PR #94](https://github.com/m-cahill/starlab/pull/94)) (**governance**; **not** runtime) |
| PX2-M01 | Full Terran runtime & action substrate v1 — **closed** on `main` ([PR #95](https://github.com/m-cahill/starlab/pull/95)) (`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`; **not** training / Blackwell / strength proof) |
| PX2-M02 | First learned replay-bootstrapped policy over the **PX2-M01** Terran surface — bounded offline metrics only (**closed** on `main` — [PR #96](https://github.com/m-cahill/starlab/pull/96)) |
| PX2-M03 | Industrial self-play **campaign** (operator-local / Blackwell-class intent; checkpoints/evals/promotion/rollback/opponent pool; slices 1–16 through handoff-anchored bounded run + **§8q bounded substantive** — **closed** on the ledger — preflight **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**) — **not** a long **GPU** run as a program deliverable; **not** M04 promotion closure; **not** campaign **evidence** by open / close text alone |
| PX2-M04 | Determine which checkpoint is actually stronger and where it still fails (promotion + exploit closure) |
| PX2-M05 | Package refreshed demonstration / proof only after stronger full-game capability exists |

---

## 9. Governance rules

1. Every milestone must:
   
   - have a plan
   - have explicit scope
   - be evidence-backed
   - be summarized
   - be audited
   - update this document

2. CI must remain truthful.

3. Required checks may not be weakened without explicit audit rationale.

4. Public claims must be bounded and evidence-backed.

5. Licensing, provenance, and contributor ownership decisions must be tracked explicitly.

6. Public/private boundary decisions must not be left implicit.

7. The project should prefer smaller reversible milestones over sprawling implementation waves.

8. This document must be updated after each milestone closeout.

9. **Canonical corpus promotion:** no replay, map, ladder-derived asset, or derived label enters a canonical STARLAB corpus until explicit provenance status and redistribution posture are recorded (see `docs/replay_data_provenance.md` and `docs/rights_register.md`).

### Intake status glossary (M07)

| Status | Meaning |
| ------ | ------- |
| `eligible_for_canonical_review` | Declared metadata and optional lineage evidence satisfy the **narrow** review bar for further governance review; **not** automatic corpus promotion. |
| `accepted_local_only` | Structurally valid; suitable for **local/private** experimentation only; **not** sufficient for canonical-review corpus posture. |
| `quarantined` | Structurally valid input, but **policy conflict** or **unsafe** posture (for example **forbidden** redistribution or **evidence conflict**). |
| `rejected` | Hard failure: unreadable replay, invalid metadata, hash mismatch, or malformed linked artifact. |

See `docs/runtime/replay_intake_policy.md`.

---

## 10. Standing invariants

These rules should hold unless explicitly revised through milestone governance.

- STARLAB remains **lab-first**, not ladder-first.
- SC2 remains the initial proving ground until explicitly expanded.
- Replay and artifact surfaces are treated as first-class evidence.
- The project prefers **benchmark integrity** over leaderboard optics.
- The project should not overclaim capabilities.
- The project should remain clean enough for serious diligence.
- Multi-environment expansion is **earned**, not assumed.
- Public docs should preserve historical truth rather than erase it.

### Untrusted boundary rule

The **SC2 client and runtime surface** (game client, replay parser libraries, protocol adapters, and third-party tooling that touches Blizzard assets) is an **untrusted boundary**. STARLAB does not treat vendor or upstream behavior as a semantic guarantee of the lab.

STARLAB-owned claims attach to **STARLAB artifacts, schemas, lineage, evaluation, and governance** — not to upstream quirks.

### Change control for contract-affecting surfaces

Changes to the following require **explicit milestone governance** (plan, scope, ledger update):

- Artifact schemas and serialization rules  
- Canonical state surface definitions  
- Benchmark scorecards and evaluation semantics  
- Rights / provenance posture  
- Public / private boundary  
- Deployment posture (Netlify / Render or successors)  
- Consumer-facing APIs or public artifact contracts  

### Proved vs not yet proved

**Private milestone path references:** Rows below cite paths under `docs/company_secrets/…` as **expected local/operator basenames** for historical closeout evidence. That entire tree is **private**, **gitignored**, and **not** present in a default clone. Public review and CI do **not** require those files to exist; operators may keep supplements in private storage or a local checkout only.

| Claim | Status |
|-------|--------|
| Canonical ledger exists | Proved (M00) |
| Milestone governance posture and tracked milestone path exist | Proved (M00) |
| Source-available license posture recorded | Proved (M00) |
| Minimal governance CI is truthful | Proved (M00) |
| SC2 runtime boundary decision + environment lock (documented; typed probe) | Proved (M01) |
| Controlled deterministic match execution | **Proved (narrow sense only):** same machine, same committed config, two successful proof-producing runs, matching normalized STARLAB `artifact_hash` — see `docs/company_secrets/milestones/M02/` (M02). **Not** proved: cross-host reproducibility, cross-install portability, or equivalence to replay bytes. |
| Run identity + lineage seed records (deterministic `run_identity.json` / `lineage_seed.json` from proof + config) | **Proved (narrow, M03):** deterministic IDs and stable JSON emission from normalized proof + config inputs — see `docs/runtime/run_identity_lineage_seed.md`, `starlab/runs/`, `docs/company_secrets/milestones/M03/`. **Does not** (by itself) claim replay binding, canonical run artifact v0, or benchmark validity. |
| Replay binding (opaque replay bytes → `replay_binding.json` linked to M03 IDs) | **Proved (narrow, M04):** deterministic `replay_content_sha256` + `replay_binding_id` from M03 `run_identity` / `lineage_seed` + opaque replay file bytes — see `docs/runtime/replay_binding.md`, `starlab/runs/replay_binding.py`, `starlab/runs/bind_replay.py`, `docs/company_secrets/milestones/M04/`. **Does not** claim replay parser correctness, replay↔proof semantic equivalence, replay event extraction, canonical run artifact v0, benchmark validity, cross-host reproducibility, or new live SC2 execution in CI (fixtures only). |
| Canonical run artifacts | **Proved (narrow, M05):** deterministic directory bundle (`manifest.json`, `hashes.json`, canonical M03/M04 JSON only; `run_artifact_id`) — see `docs/runtime/canonical_run_artifact_v0.md`, `starlab/runs/canonical_run_artifact.py`, `starlab/runs/build_canonical_run_artifact.py`, `docs/company_secrets/milestones/M05/`. **Does not** claim replay parser semantics, replay↔proof equivalence, replay event extraction, **raw replay bytes or raw proof/config in the bundle**, benchmark validity, cross-host reproducibility, or new live SC2 execution in CI. |
| Environment drift / runtime smoke matrix | **Proved (narrow, M06):** deterministic `runtime_smoke_matrix.json` + `environment_drift_report.json` from validated M01 probe JSON; optional advisory comparison with M03 `environment_fingerprint` — see `docs/runtime/environment_drift_smoke_matrix.md`, `starlab/sc2/environment_drift.py`, `starlab/sc2/evaluate_environment_drift.py`, `docs/company_secrets/milestones/M06/`. **Does not** claim cross-host portability, cross-install portability, replay parser correctness, replay semantic extraction, replay provenance finalization, benchmark integrity, or new live SC2 execution in CI. |
| Replay intake policy & provenance gate | **Proved (narrow, M07):** deterministic `replay_intake_receipt.json` + `replay_intake_report.json` from opaque replay bytes + declared intake metadata; optional M03/M04/M05 cross-check — see `docs/runtime/replay_intake_policy.md`, `starlab/replays/`, `docs/company_secrets/milestones/M07/`. **Does not** claim replay parser correctness, replay semantic extraction, build-order extraction, replay equivalence to execution proof, benchmark integrity, cross-host portability, live SC2 in CI, or legal certification of third-party rights as a matter of law. |
| Parser substrate (governed replay parse artifacts) | **Proved (narrow, M08):** deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`; deterministic normalization of parser-native output to JSON-safe trees; **`s2protocol` isolated** behind adapter — see `docs/runtime/replay_parser_substrate.md`, `starlab/replays/`, `docs/company_secrets/milestones/M08/`. **Does not** claim broad parser correctness, stable **public** normalized metadata (delivered in **M09**), event/timeline semantics (M10), build-order extraction, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Stable normalized replay metadata (public contract) | **Proved (narrow, M09):** deterministic `replay_metadata.json` + `replay_metadata_report.json` from M08 `replay_raw_parse.json` (optional parse receipt/report linkage); **no** `s2protocol` in M09 — see `docs/runtime/replay_metadata_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M09/`. **Does not** claim event/timeline semantics (M10), build-order extraction (M11), replay↔execution equivalence, benchmark integrity, broad Blizzard parser correctness beyond the mapping, live SC2 in CI, or legal certification of replay rights. |
| Governed replay timeline (public contract) | **Proved (narrow, M10):** deterministic `replay_timeline.json` + `replay_timeline_report.json` from `replay_raw_parse.json` (v1 or v2; v2 includes `raw_event_streams`); fixture-driven CI — see `docs/runtime/replay_timeline_event_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M10/`. **Does not** claim build-order/economy (that is **M11**), combat/scouting, benchmark integrity, upstream semantic certification, replay↔execution equivalence, live SC2 in CI, or legal certification of replay rights. |
| Governed build-order / economy plane | **Proved (narrow, M11):** deterministic `replay_build_order_economy.json` + `replay_build_order_economy_report.json` from M10 `replay_timeline.json` with optional supplemental `replay_raw_parse.json` v2 identity lookup only — see `docs/runtime/replay_build_order_economy_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M11/`. **Does not** claim combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Governed combat / scouting / visibility plane | **Proved (narrow, M12):** deterministic `replay_combat_scouting_visibility.json` + `replay_combat_scouting_visibility_report.json` from M10 `replay_timeline.json` + M11 `replay_build_order_economy.json` with optional supplemental `replay_raw_parse.json` v2 for identity / position / explicit visibility fields only — see `docs/runtime/replay_combat_scouting_visibility_extraction.md`, `starlab/replays/`, `docs/company_secrets/milestones/M12/`. **Does not** claim replay slice definition artifacts (M13), replay bundle packaging (M14), true fog-of-war certification, replay↔execution equivalence, benchmark integrity, live SC2 in CI, or legal certification of replay rights. |
| Governed replay slice definitions (metadata-only temporal spans) | **Proved (narrow, M13):** deterministic `replay_slices.json` + `replay_slices_report.json` from M10+M11+M12 governed JSON with lineage; **no** `replay_raw_parse.json` in M13 v1 — see `docs/runtime/replay_slice_generation.md`, `starlab/replays/`, `docs/company_secrets/milestones/M13/`. **Does not** claim raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, live SC2 in CI, legal certification of replay rights, or **M14** replay bundle / lineage packaging. |
| Replay bundle & lineage packaging (manifest + graph + inventory) | **Proved (narrow, M14):** deterministic `replay_bundle_manifest.json` + `replay_bundle_lineage.json` + `replay_bundle_contents.json` over M09–M13 primary governed JSON (+ optional `*_report.json`); **no** raw replay bytes, **no** `replay_raw_parse.json` in bundle, **no** archive requirement in v1 — see `docs/runtime/replay_bundle_lineage_contract.md`, `starlab/replays/`, `docs/company_secrets/milestones/M14/`. **`bundle_id` / `lineage_root`** are **packaging identities only** — **not** replay↔execution equivalence, benchmark integrity, live SC2 in CI, canonical state semantics, or legal certification of replay rights. |
| Canonical state schema (single frame) + validation | **Proved (narrow, M15):** deterministic `canonical_state_schema.json` + `canonical_state_schema_report.json`; validation of example state JSON against the schema (`jsonschema`); contract `docs/runtime/canonical_state_schema_v1.md`, `starlab/state/` — see `docs/company_secrets/milestones/M15/`. **Does not** prove replay-to-state **materialization** (M16), observation surface (M17), perceptual bridge (M18), stronger economy or visibility semantics than M11/M12, replay↔execution equivalence, benchmark integrity, or live SC2 in CI. |
| Structured state pipeline (one frame from M14 bundle) | **Proved (narrow, M16):** deterministic `canonical_state.json` + `canonical_state_report.json` from a **complete M14 replay bundle** + M09–M13 primary JSON at one requested `gameloop`; validates against M15 schema; contract `docs/runtime/canonical_state_pipeline_v1.md`, `starlab/state/` — see `docs/company_secrets/milestones/M16/`. **Does not** prove agent-facing **observation surface contract** (M17), perceptual bridge (M18), multi-frame sequences, replay↔execution equivalence, benchmark integrity, exact banked mineral/gas truth beyond prior bounded planes, certified fog-of-war truth, or live SC2 in CI. |
| Observation surface contract (single frame, JSON Schema + validation) | **Proved (narrow, M17):** deterministic `observation_surface_schema.json` + `observation_surface_schema_report.json`; validation of example observation JSON against the schema (`jsonschema`); contract `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/` — semantic upstream is **M16 `canonical_state.json`** (not replay bundles directly). **Does not** prove canonical-state→observation **materialization** (that is **M18**), mask **legality** / dynamic mask generation, full SC2 action coverage, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI. |
| Prototype perceptual bridge (M16 canonical state → one M17-shaped observation instance) | **Proved (narrow, M18):** deterministic `observation_surface.json` + `observation_surface_report.json` per CLI invocation from one `canonical_state.json`; optional `canonical_state_report.json` hash cross-check; validates emitted observation against M17 schema; contract `docs/runtime/perceptual_bridge_prototype_v1.md`, materialization modules under `starlab/observation/` — **no** replay parsing or M14 bundle load in those modules. **Does not** prove full action legality, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, exact banked resources beyond prior bounded planes, multi-frame tensors, live SC2 in CI, or **M19** cross-mode reconciliation (M19 is a separate proof). |
| Cross-mode reconciliation audit (canonical state vs observation instance) | **Proved (narrow, M19):** deterministic `observation_reconciliation_audit.json` + `observation_reconciliation_audit_report.json` per CLI invocation from paired `canonical_state.json` + `observation_surface.json`; optional upstream reports; contract `docs/runtime/observation_reconciliation_audit_v1.md`, audit modules under `starlab/observation/` — **no** replay parsing or M14 bundle load in M19 modules. **Does not** prove benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, live SC2 in CI, or **M20** benchmark contract semantics. |
| Benchmark contract + scorecard schemas | **Proved (narrow, M20):** deterministic `benchmark_contract_schema.json` + `benchmark_contract_schema_report.json` + `benchmark_scorecard_schema.json` + `benchmark_scorecard_schema_report.json`; fixture validation with `jsonschema`; contract `docs/runtime/benchmark_contract_scorecard_v1.md`, modules under `starlab/benchmarks/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M20 benchmark modules. **Does not** prove benchmark integrity, scripted/heuristic baselines (**M21–M22**), evaluation runner (**M23**), replay↔execution equivalence, or live SC2 in CI. |
| Scripted baseline suite (fixture-only consumer) | **Proved (narrow, M21):** deterministic `scripted_baseline_suite.json` + `scripted_baseline_suite_report.json` from one M20-validated **`fixture_only`** benchmark contract with embedded M20 scorecards for fixed **scripted** subjects; contract `docs/runtime/scripted_baseline_suite_v1.md`, `starlab/baselines/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M21 baseline modules — see §18 / `M21_run1.md`. **Does not** prove heuristic baselines (**M22** by itself), evaluation runner (**M23**), benchmark integrity, replay↔execution equivalence, or live SC2 in CI. |
| Heuristic baseline suite (fixture-only consumer) | **Proved (narrow, M22):** deterministic `heuristic_baseline_suite.json` + `heuristic_baseline_suite_report.json` from one M20-validated **`fixture_only`** benchmark contract with embedded M20 scorecards for fixed **heuristic** subjects; contract `docs/runtime/heuristic_baseline_suite_v1.md`, `starlab/baselines/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M22 baseline modules — see §18 / `M22_run1.md`. **Does not** prove evaluation runner / tournament harness (**M23** by itself), attribution/diagnostics (**M24**), benchmark integrity, replay↔execution equivalence, or live SC2 in CI. |
| Evaluation runner + tournament harness (fixture-only) | **Proved (narrow, M23):** deterministic `evaluation_tournament.json` + `evaluation_tournament_report.json` from one M20-validated **`fixture_only`** benchmark contract plus one or more **M21/M22** suite artifacts; contract `docs/runtime/evaluation_runner_tournament_harness_v1.md`, `starlab/evaluation/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M23 evaluation modules — see §18 / `M23_run1.md`. **Does not** prove evaluation diagnostics (**M24**), baseline evidence pack (**M25**), **M26** replay training dataset contract, **M27** imitation baseline, benchmark integrity, replay↔execution equivalence, or live SC2 in CI. |
| Evaluation diagnostics + failure views (M23 consumer) | **Proved (narrow, M24):** deterministic `evaluation_diagnostics.json` + `evaluation_diagnostics_report.json` from one governed **`fixture_only`** **M23** `evaluation_tournament.json`; contract `docs/runtime/evaluation_diagnostics_failure_views_v1.md`, `starlab/evaluation/` — **interpretive**; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M24 evaluation modules — **green PR-head** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) on `5caf1fb…`; **green merge-push `main`** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) on `7b4d3b4…`; see §18 / `M24_run1.md`. **Does not** prove baseline evidence pack (**M25**), **M26** replay training dataset contract, **M27** imitation baseline, benchmark integrity, replay↔execution equivalence, or live SC2 in CI. |
| Baseline evidence pack (M21/M22 + M23 + M24 chain) | **Proved (narrow, M25):** deterministic `baseline_evidence_pack.json` + `baseline_evidence_pack_report.json` from governed **M21/M22** suites + **M23** tournament + **M24** diagnostics; contract `docs/runtime/baseline_evidence_pack_v1.md`, `starlab/evaluation/` — **interpretive packaging**; **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M25 evaluation modules — **green PR-head** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on `b132bfd…`; **green merge-push `main`** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) on `f03c7bf…`; see §18 / `M25_run1.md`. **Does not** prove benchmark integrity, replay↔execution equivalence, live SC2 in CI, or **M27** imitation baseline. |
| Replay training dataset (M14 bundle consumer) | **Proved (narrow, M26):** deterministic `replay_training_dataset.json` + `replay_training_dataset_report.json` from governed **M14** bundle directories; contract `docs/runtime/replay_training_dataset_v1.md`, `starlab/imitation/` — **no** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M26 imitation modules — **green PR-head** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on `d8d3c4c…`; **green merge-push `main`** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) on `e83a849…`; see §18 / `M26_run1.md`. **Does not** prove model training, imitation quality, benchmark integrity, replay↔execution equivalence, live SC2 in CI, or **M27** imitation baseline. |
| Replay imitation baseline (M26 + M14; offline) | **Proved (narrow, M27):** deterministic `replay_imitation_baseline.json` + `replay_imitation_baseline_report.json` from governed **M26** + **M14** via **M16 → M18** materialization; majority-label-per-signature with lexicographic tie-break and global fallback; **`agreement_by_split`** = internal smoke only; contract `docs/runtime/replay_imitation_baseline_v1.md`, `starlab/imitation/` — **green PR-head** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) on `65dcd2f…`; **green merge-push `main`** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) on `49b4582…`; see §18 / `M27_run1.md`. **Does not** prove benchmark integrity, leaderboard validity, hierarchical control, replay↔execution equivalence, live SC2 in CI, or imitation quality beyond explicit smoke metrics. |
| Learned-agent evaluation (frozen M27 on M26 `test`; offline) | **Proved (narrow, M28):** deterministic `learned_agent_evaluation.json` + `learned_agent_evaluation_report.json` from one **M20** `fixture_only` benchmark contract + frozen **M27** baseline + **M26** dataset + **M14** bundles; embedded M20 scorecard; contract `docs/runtime/learned_agent_evaluation_harness_v1.md`, `starlab/evaluation/` — **green PR-head** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) on `c7ca6e6…`; **green merge-push `main`** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) on `1ef6365…`; see §18 / `M28_run1.md`. **Does not** prove benchmark integrity, leaderboard validity, M23 tournament, M24/M25 surfaces, live SC2 in CI, replay parser execution in M28 modules, or stronger imitation quality than explicit metrics. |
| Hierarchical agent interface (offline two-level trace; contract schema) | **Proved (narrow, M29):** deterministic `hierarchical_agent_interface_schema.json` + `hierarchical_agent_interface_schema_report.json`; runtime contract `docs/runtime/hierarchical_agent_interface_v1.md`, `starlab/hierarchy/` — **green PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **green merge-push `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; see §18 / `M29_run1.md`. **Does not** prove learned hierarchical policy (**M30**), benchmark integrity, live SC2, or raw action legality. |
| First learned hierarchical imitation agent (offline; M26 + M14; M29 trace schema) | **Proved (narrow, M30):** deterministic `replay_hierarchical_imitation_agent.json` + `replay_hierarchical_imitation_agent_report.json`; fixed delegate policy **`starlab.m30.delegate.fixed_four_v1`**; runtime contract `docs/runtime/replay_hierarchical_imitation_agent_v1.md`, `starlab/hierarchy/` — **green PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **green merge-push `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; see §18 / `M30_run1.md`. **Does not** prove benchmark integrity, live SC2, raw action legality, replay↔execution equivalence, or M39 flagship proof pack. |
| Replay explorer / operator evidence surface (offline; bounded panels) | **Proved (narrow, M31):** deterministic `replay_explorer_surface.json` + `replay_explorer_surface_report.json`; runtime contract `docs/runtime/replay_explorer_surface_v1.md`, `starlab/explorer/` — **green PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **green merge-push `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; see §18 / `M31_run1.md`. **Does not** prove benchmark integrity, live SC2, web UI / hosting, replay↔execution equivalence, or M39 flagship proof pack semantics. |
| Explicit parallel CI tiering + fixture field-test CI artifact readiness (audit closure II) | **Proved (narrow, M33):** workflow **`CI`** with jobs **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, final **`governance`**; artifacts **`coverage.xml`**, **`pytest-junit.xml`**, **`pytest-smoke-junit.xml`**, **`fieldtest-output`** (`out/fieldtest/` including required explorer JSON); runtime contract `docs/runtime/ci_tiering_field_test_readiness_v1.md`; **green PR-head** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **green merge-push `main`** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md`. **Does not** prove M34 structural hygiene product work, M39 flagship proof pack, benchmark integrity, live SC2 in CI, or operating manual v1. |
| Structural hygiene + deferred-issue closure (audit closure III) | **Proved (narrow, M34):** `starlab._io`, governance test split, **DIR-003**–**DIR-006**, operating-manual promotion prep docs; **green PR-head** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **green merge-push `main`** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; see §18 / `M34_run1.md`. **Does not** prove M39 flagship proof pack, benchmark integrity, live SC2 in CI, or operating manual v1. |
| Structural decoupling + module decomposition (audit closure IV) | **Proved (narrow, M35):** `M14BundleLoader`, `parser_io` / `replay_slice_generation` / observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39**; **green PR-head** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **green merge-push `main`** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) on `5b4d24b…`; superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) — **not** merge authority; see §18 / `M35_run1.md`. **Does not** prove M39 flagship proof pack, benchmark integrity, live SC2 in CI, or operating manual v1. |
| Governance surface + documentation density (audit closure V) | **Proved (narrow, M36):** `docs/starlab_archive.md` (verbatim **M01–M27** §7 notes), ledger §7 archival policy + **M28–M35** inline notes, governance-test consolidation (`tests/test_governance_milestones.py`, `tests/test_governance_runtime.py`), `docs/starlab_archive.md` on governance doc list; **green PR-head** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **green merge-push `main`** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; see §18 / `M36_run1.md` / [PR #47](https://github.com/m-cahill/starlab/pull/47). **Does not** prove M39 flagship proof-pack **product** work, benchmark integrity, live SC2 in CI, or operating manual v1. |
| Benchmark integrity | Not yet proved |
| Learning or agent capability (beyond **M31** narrow offline evidence surface + prior milestones) | Not yet proved |

**Local harness vs portability:** a **local deterministic harness proof** (same machine, same config, normalized STARLAB artifact hash) is a **narrower** claim than **cross-host reproducibility** or **cross-install portability**. The ledger uses “controlled deterministic match execution” **only** in that **narrow harness-scoped** sense for M02.

**Execution / substrate claims (split for audits):**

| Subclaim | Milestone | Notes |
| -------- | --------- | ----- |
| Runtime boundary + environment lock | M01 | Probe + docs; not full execution proof |
| Deterministic match harness + M02 proof artifact | M02 | Narrow same-machine harness claim only |
| Run identity + lineage seed primitives | M03 | **On `main`** — narrow claim; distinct from replay binding and canonical run packaging |
| Replay binding to run identity | M04 | **On `main`** — **narrow** opaque-bytes binding to M03 records; not parser/canonical-run/benchmark claims |
| Canonical run artifact v0 | M05 | **On `main`** — narrow packaging only; see `docs/runtime/canonical_run_artifact_v0.md` |
| Environment drift / smoke matrix | M06 | **On `main`** — fixture-driven probe + drift report; not portability/parser/benchmark claims |
| Replay intake / provenance gate | M07 | **On `main`** — opaque bytes + declared metadata; governed receipts/reports; not parser/build-order/benchmark/live-SC2/legal claims |
| Parser substrate (replay parse artifacts) | M08 | **On `main`** — raw sections + availability flags; deterministic artifacts; not normalized-metadata/event-semantics claims |
| Normalized replay metadata (public contract) | M09 | **On `main`** — small deterministic projection from M08 raw parse; not event semantics or build-order claims |
| Governed timeline / event extraction | M10 | **On `main`** — bounded semantic kinds + deterministic merge; not build-order or benchmark claims |
| Build-order / economy plane | M11 | **On `main`** — narrow extraction over timeline (+ optional raw-parse identity); not combat/scouting or benchmark claims |
| Combat / scouting / visibility plane | M12 | **On `main`** — narrow extraction over timeline + BOE (+ optional raw-parse supplemental); not replay slice definitions or FOW truth |
| Replay slice definitions (metadata-only) | M13 | **On `main`** — narrow temporal spans over governed M10–M12 JSON; not raw clipping or M14 bundles |
| Replay bundle / lineage packaging | M14 | **On `main`** — narrow manifest + lineage + contents over governed M09–M13 JSON; not raw bytes, raw parse in bundle, or execution equivalence |
| Canonical state schema v1 (single frame) | M15 | **On `main`** — narrow JSON Schema + report + fixture validation; not materialization pipeline, sequences, tensors, or observation API |
| Structured state pipeline (bundle → one frame) | M16 | **On `main`** — narrow M14 bundle load + deterministic derivation + schema validation + report; not observation surface contract proof, tensors, or replay↔execution equivalence |
| Observation surface contract v1 (single player-relative frame) | M17 | **On `main`** — narrow JSON Schema + report + fixture validation; upstream M16 canonical state; **not** materialization proof (M18), replay↔execution equivalence |
| Prototype perceptual bridge (canonical state → observation instance) | M18 | **On `main`** — narrow prototype materialization + report; **not** legality, benchmark integrity, M19 reconciliation, or replay↔execution equivalence |
| Cross-mode reconciliation audit (canonical vs observation) | M19 | **On `main`** — narrow deterministic audit + report; **not** benchmark integrity, M20 benchmark contract, or replay↔execution equivalence |
| Benchmark contract + scorecard schemas | M20 | **On `main`** — narrow JSON Schemas + reports + fixture validation; **not** baselines (**M21–M22**), runner (**M23**), benchmark integrity, or replay↔execution equivalence |
| Scripted baseline suite (fixture-only) | M21 | **On `main`** — narrow scripted suite + report + embedded scorecards; **not** heuristic suite (**M22**), runner (**M23**), benchmark integrity, or replay↔execution equivalence |
| Heuristic baseline suite (fixture-only) | M22 | **On `main`** — narrow heuristic suite + report + embedded scorecards (**green PR-head** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) on `96aba18…`; **green merge-push `main`** [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) on `470afa8…`; see §18 / `M22_run1.md`); **not** evaluation tournament (**M23** by itself), attribution/diagnostics (**M24**), benchmark integrity, or replay↔execution equivalence |
| Evaluation runner + tournament harness (fixture-only) | M23 | **On `main`** — narrow tournament artifacts + round-robin harness over embedded scorecards (**green PR-head** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) on `f00711a…`; **green merge-push `main`** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) on `b8857d2…`; see §18 / `M23_run1.md`); **not** evaluation diagnostics (**M24**), benchmark integrity, or replay↔execution equivalence |
| Evaluation diagnostics + failure views (fixture-only) | M24 | **On `main`** — narrow diagnostics + report over governed **M23** tournament JSON (**green PR-head** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) on `5caf1fb…`; **green merge-push `main`** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) on `7b4d3b4…`; see §18 / `M24_run1.md`); **not** baseline evidence pack (**M25** by itself), **M26** replay training dataset contract, **M27** imitation baseline, benchmark integrity, or replay↔execution equivalence |
| Baseline evidence pack (Phase IV packaging) | M25 | **On `main`** — narrow packaging over **M21/M22 + M23 + M24** (**green PR-head** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on `b132bfd…`; **green merge-push `main`** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) on `f03c7bf…`; see §18 / `M25_run1.md`); **not** benchmark integrity or replay↔execution equivalence |
| Replay training dataset (Phase V; M14 bundles) | M26 | **On `main`** — narrow dataset + report over governed **M14** bundles (**green PR-head** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on `d8d3c4c…`; **green merge-push `main`** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) on `e83a849…`; see §18 / `M26_run1.md`); **not** model training, benchmark integrity, **M27** imitation baseline, or replay↔execution equivalence |
| Replay imitation baseline (Phase V; M26 + M14) | M27 | **On `main`** — narrow `replay_imitation_baseline.json` + `replay_imitation_baseline_report.json` over governed **M26** dataset + **M14** bundles via **M16 → M18** materialization (**green PR-head** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) on `65dcd2f…`; **green merge-push `main`** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) on `49b4582…`; see §18 / `M27_run1.md`); runtime contract `docs/runtime/replay_imitation_baseline_v1.md`, modules + CLI under `starlab/imitation/`; **not** benchmark integrity, **not** hierarchical control, **not** live SC2 in CI, **not** replay parser execution in M27 imitation modules |
| Learned-agent evaluation harness (Phase V; M20 + M27 + M26 + M14) | M28 | **On `main`** — narrow offline `learned_agent_evaluation.json` + report + embedded M20 scorecard (**green PR-head** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) on `c7ca6e6…`; **green merge-push `main`** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) on `1ef6365…`; see §18 / `M28_run1.md` / [PR #34](https://github.com/m-cahill/starlab/pull/34)); runtime `docs/runtime/learned_agent_evaluation_harness_v1.md`, `starlab/evaluation/`; **not** benchmark integrity, **not** M23–M25 surfaces, **not** live SC2 in CI, **not** replay parser in M28 evaluation modules |
| Hierarchical agent interface (Phase V; contract schema) | M29 | **On `main`** — narrow `hierarchical_agent_interface_schema.json` + report (**green PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **green merge-push `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; see §18 / `M29_run1.md` / [PR #35](https://github.com/m-cahill/starlab/pull/35)); runtime `docs/runtime/hierarchical_agent_interface_v1.md`, `starlab/hierarchy/`; **not** learned hierarchical agent (**M30**), **not** benchmark integrity, **not** live SC2 in CI |
| Learned hierarchical imitation agent (Phase V; M26 + M14 + M29 trace) | M30 | **On `main`** — narrow `replay_hierarchical_imitation_agent.json` + report (**green PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **green merge-push `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; see §18 / `M30_run1.md` / [PR #36](https://github.com/m-cahill/starlab/pull/36)); runtime `docs/runtime/replay_hierarchical_imitation_agent_v1.md`, `starlab/hierarchy/`; **not** benchmark integrity, **not** live SC2 in CI, **not** M39 flagship proof pack |
| Replay explorer evidence surface (Phase V; M14 + M30 + M16→M18) | M31 | **On `main`** — narrow `replay_explorer_surface.json` + report (**green PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **green merge-push `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; see §18 / `M31_run1.md` / [PR #37](https://github.com/m-cahill/starlab/pull/37)); runtime `docs/runtime/replay_explorer_surface_v1.md`, `starlab/explorer/`; **not** benchmark integrity, **not** live SC2 in CI, **not** web UI, **not** M39 flagship proof pack product |
| Audit closure II — CI tiering + field-test artifact (Phase V) | M33 | **On `main`** — parallel **`CI`** jobs + **`fieldtest-output`** + expanded architecture / operator / diligence surfaces (**green PR-head** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **green merge-push `main`** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md` / [PR #39](https://github.com/m-cahill/starlab/pull/39)); **not** M34 structural hygiene product, **not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI |
| Audit closure III — structural hygiene + deferred issues (Phase V) | M34 | **On `main`** — `starlab._io`, governance test split, Dependabot + dev caps, manual prep docs, **DIR-003**–**DIR-006** (**green PR-head** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **green merge-push `main`** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; see §18 / `M34_run1.md` / [PR #40](https://github.com/m-cahill/starlab/pull/40)); **not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI |
| Audit closure IV — structural decoupling (Phase V) | M35 | **On `main`** — `M14BundleLoader`, `parser_io` / `replay_slice_generation` / observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39** (**green PR-head** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **green merge-push `main`** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) on `5b4d24b…`; see §18 / `M35_run1.md` / [PR #46](https://github.com/m-cahill/starlab/pull/46)); superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) — **not** merge authority; **not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI |
| Audit closure V — governance surface + ledger archive (Phase V) | M36 | **On `main`** — `docs/starlab_archive.md`, §7 archival policy + **M28–M35** inline notes, governance-test consolidation (**green PR-head** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **green merge-push `main`** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; see §18 / `M36_run1.md` / [PR #47](https://github.com/m-cahill/starlab/pull/47)); superseded PR-head: none; **not** M39 flagship proof-pack **product**, **not** benchmark integrity, **not** live SC2 in CI |

### Slice vs bundle glossary (M13–M14)

| Term | Meaning |
| ---- | ------- |
| **Slice (M13)** | A **metadata-defined temporal span** (`replay_slices.json`): addressable `[start_gameloop, end_gameloop]` anchored to M12 combat or scouting signals, with lineage to governed upstream JSON — **not** clipped replay bytes. |
| **Bundle / lineage packaging (M14)** | **M14** scope: packaging and **lineage contract v1** for replay bundles — distinct from M13 slice **definitions**. |
| **Primary governed replay artifacts (M14)** | The five required JSON data artifacts: `replay_metadata.json`, `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`, `replay_slices.json`. |
| **Report artifacts (M14)** | Optional secondary `*_report.json` companions when present — not interchangeable with primary data artifacts. |
| **Excluded raw/parser artifacts (M14)** | Raw `.SC2Replay` bytes, `replay_raw_parse.json`, parser blobs — **not** bundle members in M14 v1. |
| **`bundle_id` / `lineage_root` (M14)** | Deterministic **packaging identity** over hashes of governed JSON — **not** replay↔execution equivalence, benchmark integrity, or legal certification of replay rights. |

### Phase III schema / pipeline / observation glossary (M15–M19)

| Term | Meaning |
| ---- | ------- |
| **M15 canonical state schema** | The **governed JSON Schema** (`canonical_state_schema.json`) and **report** (`canonical_state_schema_report.json`) for a **single** replay-derived state **frame** at one `gameloop` — **schema + validation only**; **not** materialization from replay bundles (that is **M16**). |
| **M16 structured state pipeline** | **Proved on `main`:** **materialize** exactly one M15-shaped `canonical_state.json` per CLI invocation from a **complete M14 bundle** + governed upstream JSON, with `jsonschema` validation and `canonical_state_report.json` — **not** an observation **contract proof** by itself (**M17**), **not** perceptual bridge (**M18**) by itself. |
| **M17 observation surface contract** | **Proved (narrow, in-repo):** deterministic JSON Schema + report for one **player-relative** observation frame at one `gameloop`, bound to **M16 canonical state** as upstream — **contract + validation only**; materialization is **M18** (separate proof). **Proxy visibility** remains bounded (M12/M16 non-claims), not certified fog-of-war truth. |
| **M18 perceptual bridge prototype** | **Proved on `main`:** deterministic **prototype** materialization from one M16 `canonical_state.json` to one M17-shaped `observation_surface.json` + `observation_surface_report.json` (fixture-backed tests; optional report hash cross-check) — **not** replay parsing in `starlab/observation/`, **not** mask legality or benchmark claims, **not** M19 reconciliation by itself. |
| **M19 cross-mode reconciliation audit** | **Proved on `main`:** deterministic audit of one M16 `canonical_state.json` against one M18 `observation_surface.json` (same frame identity), emitting `observation_reconciliation_audit.json` + `observation_reconciliation_audit_report.json` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** M20 benchmark semantics. |

### Phase III reconciliation status glossary (M19)

| Status | Meaning |
| ------ | ------- |
| `exact` | Observation field matches M18 deterministic expectation and is a direct carry-through (or faithful omission of zero-valued aggregates). |
| `derived` | Matches expectation from a deterministic transform (list lengths, prototype action-mask heuristics). |
| `bounded_lossy` | Matches expectation but remains explicitly bounded / proxy / category-level — not full game truth. |
| `unavailable_by_design` | Signal intentionally absent or null when upstream cannot supply it under the contract. |
| `mismatch` | Observation does not match M18 deterministic expectation from the supplied canonical state — audit **failure** when unexpected. |

### Phase IV scorecard glossary (M20)

| Term | Meaning |
| ---- | ------- |
| `scored` | Metric values are populated under the benchmark contract’s scoring rules. |
| `unscored` | No scored metric values (e.g. contract-only or not yet evaluated). |
| `disqualified` | Subject or run excluded from scored comparison (policy or gating). |
| `comparable` | Results may be compared under stated assumptions (still **not** a proof of benchmark integrity). |
| `provisional` | Comparison is tentative or incomplete. |
| `non_comparable` | Results must not be treated as comparable across subjects or runs. |

### Phase IV baseline subject glossary (M20 vocabulary; ledgered for M21+)

| Subject kind | Meaning |
| ------------ | ------- |
| `scripted` | Hand-authored or fixed-policy baseline behavior (deterministic fixture scoring in **M21**). |
| `heuristic` | Rule- or search-based baseline without learned weights; deterministic fixture scoring in **M22** (not live SC2 execution in CI). |
| `imitation` | Behavior derived from replay or demonstration data (**later milestones**). |
| `hierarchical` | Multi-level control / delegation interfaces (**later milestones**). |
| `rl` | Reinforcement-learning-style agents (**later milestones**). |
| `human_replay` | Human play as a reference or subject (**later milestones**). |

### Phase IV evaluation / tournament glossary (M23)

| Term | Meaning |
| ---- | ------- |
| **Suite input** | One governed **M21** or **M22** suite JSON artifact passed to the runner (CLI order preserved). |
| **Entrant** | One subject derived from an embedded suite scorecard; `entrant_id` is `{suite_id}::{subject_id}` (deterministic). |
| **Match** | One pairwise **round-robin** fixture-only comparison; **win/loss/draw** is decided by the contract **`primary`** metric only; full metric rows are recorded for auditability. |
| **Standings** | Deterministic ordering by tournament points, then primary-metric tie-break scalar, then `entrant_id` ascending. |
| **Runner / harness non-claims** | **Not** benchmark integrity, leaderboard validity, replay↔execution equivalence, live SC2, replay parsing, attribution/diagnostics (**M24**), baseline evidence pack (**M25**), **M26** replay training dataset contract, or **M27** imitation baseline. |

### Phase IV diagnostics glossary (M24)

| Term | Meaning |
| ---- | ------- |
| **Diagnostic view** | Deterministic, offline summary derived from one **M23** tournament artifact (entrant summaries, match rows, standing explanations). |
| **Failure view** | Diagnostic **negative** or **edge** surface (e.g. zero-win entrants, lowest points, draw-on-primary, tie-break usage) — **not** runtime crashes. |
| **Standing explanation** | Why a standing row sits where it does relative to the next row (points, primary tie-break scalar, or lexicographic `entrant_id` under M23 rules). |
| **Decisive metric** | The **primary** contract metric used for pairwise outcomes in **M23** (`scoring_role: primary`); recorded again on each match diagnostic for traceability. |

### Phase IV evidence pack glossary (M25)

| Term | Meaning |
| ---- | ------- |
| **Evidence pack** | Deterministic JSON bundle (`baseline_evidence_pack.json` + report) tying one fixture-only tournament chain together — **packaging**, not new evaluation. |
| **Evidence row** | One `entrants[]` object in **`baseline_evidence_pack.json`**, ordered by **M23** standings, with **`evidence_refs`** back to suite / tournament / diagnostics identities. |
| **Source artifact identity** | Benchmark + suite + tournament + diagnostics fields and hashes used to bind the chain (**M25** adds **`tournament_sha256`** / **`diagnostics_sha256`** as packaging identity; does **not** change **M24**’s governed inputs). |
| **Pack non-claims** | Explicit **`non_claims[]`** on the pack — benchmark integrity, new semantics, live SC2, replay execution, **M26**/**M27** learning work, etc. |

### Phase V imitation baseline glossary (M27)

| Term | Meaning |
| ---- | ------- |
| **Imitation baseline** | Deterministic trained artifact (`replay_imitation_baseline.json` + report) over governed **M26** examples — **narrow** majority model, not a benchmark claim. |
| **Context signature** | Bounded, bucketed projection from governed **M18** observation + **M16** canonical state fields (`starlab.m27.feature.observation_signature_v1`). |
| **Fallback label** | Global majority label over **training** split when a signature was unseen during training (lexicographic tie-break). |
| **Internal split-agreement smoke metric** | `agreement_by_split` in `replay_imitation_baseline_report.json` — **diagnostic fit only**, not leaderboard or benchmark integrity. |

### Phase V replay explorer glossary (M31)

| Term | Meaning |
| ---- | ------- |
| **`selection_policy_id`** | Declares which deterministic rule produced panel ordering and anchors — **M31 v1:** `starlab.m31.selection.slice_anchor_v1` (sort slices by `start_gameloop` then `slice_id`; anchor = integer midpoint of the slice window). |
| **`anchor_gameloop`** | The single gameloop at which **M16** canonical state and **M18** observation are materialized for a panel, and at which the **M30** predictor emits an **M29** trace. |
| **Evidence panel** | One bounded bundle of slice metadata, upstream excerpts (M10–M12), state/observation excerpts, optional warnings, and one hierarchical trace — **not** a full replay or a UI view. |
| **`replay_explorer_surface.json`** | Primary operator evidence artifact (`surface_version` `starlab.replay_explorer_surface.v1`). |
| **`replay_explorer_surface_report.json`** | Summary report (`report_version` `starlab.replay_explorer_surface_report.v1`) with counts and excerpt policy. |

### Phase III progression (compact)

| Milestone | What it proves (Phase III) |
| --------- | -------------------------- |
| **M15** | Canonical **state schema** only (no bundle materialization). |
| **M16** | **Bundle → one canonical state frame** (replay-derived JSON planes → `canonical_state.json`). |
| **M17** | **Canonical frame → agent-facing observation contract** (schema/report; upstream is **M16**, not raw replay bundles). |
| **M18** | **Prototype perceptual bridge** — canonical state → one M17-shaped observation instance (**proved** on `main`; see §18 / PR #19). |
| **M19** | **Cross-mode reconciliation audit** — canonical state vs observation instance under explicit classification (**proved** on `main`; see §18 / PR #20). |

### Phase IV progression (compact)

| Milestone | What it proves (Phase IV) |
| --------- | ------------------------- |
| **M20** | **Benchmark contract + scorecard schemas** — deterministic JSON Schemas + reports + fixture validation (**proved** on `main`; see §18 / PR #21). |
| **M21** | **Scripted baseline suite** — load one **`fixture_only`** benchmark contract, emit deterministic `scripted_baseline_suite.json` + `scripted_baseline_suite_report.json` with embedded M20 scorecards (**proved** on `main`; see §18 / PR #22). |
| **M22** | **Heuristic baseline suite** — same contract posture as M21 with fixed **heuristic** subjects (`heuristic_baseline_suite.json` / `heuristic_baseline_suite_report.json`) (**proved** on `main`; see §18 / PR #23). |
| **M23** | **Evaluation runner + tournament harness** — load M20 contract + **M21/M22** suite artifacts; deterministic `evaluation_tournament.json` / `evaluation_tournament_report.json` (**proved** on `main`; see §18 / PR #24). |
| **M24** | **Evaluation diagnostics + failure views** — load one governed **M23** `evaluation_tournament.json`; deterministic `evaluation_diagnostics.json` / `evaluation_diagnostics_report.json` (**interpretive**; **not** new scoring semantics) (**proved** on `main`; see §18 / [PR #27](https://github.com/m-cahill/starlab/pull/27)). |
| **M25** | **Baseline evidence pack** — package governed **M21/M22 → M23 → M24** into `baseline_evidence_pack.json` / `baseline_evidence_pack_report.json` (**interpretive packaging**; **not** benchmark-integrity claims) (**proved** on `main`; see §18 / [PR #31](https://github.com/m-cahill/starlab/pull/31)). |

### Phase V progression (compact)

**Phase V bridge (compact):** dataset contract → trained imitation baseline → learned-agent evaluation → hierarchy → evidence surface → **audit closure (M32–M34)** → **audit closure IV/V (M35–M36)** → **audit closure VI (M37)** → **audit closure VII (M38)** → flagship proof (**M39**).

| Milestone | What it proves (Phase V) |
| --------- | ------------------------ |
| **M26** | **Replay corpus governance + training dataset contract** — deterministic `replay_training_dataset.json` / `replay_training_dataset_report.json` from governed **M14** bundle directories (dataset contract only; **not** model training) (**proved** on `main`; see §18 / [PR #32](https://github.com/m-cahill/starlab/pull/32)). |
| **M27** | **Replay-derived imitation baseline (narrow, trained artifact)** — deterministic `replay_imitation_baseline.json` / `replay_imitation_baseline_report.json` from governed **M26** + **M14** (majority-label-per-context-signature; explicit non-claims; **not** benchmark integrity) (**proved** on `main`; see §18 / [PR #33](https://github.com/m-cahill/starlab/pull/33)). |
| **M28** | **Learned-agent evaluation harness** — deterministic `learned_agent_evaluation.json` / `learned_agent_evaluation_report.json` (M20 contract + frozen **M27** + **M26** `test` + **M14**) (**proved** on `main`; see §18 / [PR #34](https://github.com/m-cahill/starlab/pull/34)). |
| **M29** | **Hierarchical agent interface layer** — deterministic `hierarchical_agent_interface_schema.json` / `hierarchical_agent_interface_schema_report.json` (**proved** on `main`; see §18 / [PR #35](https://github.com/m-cahill/starlab/pull/35)). |
| **M30** | **First learned hierarchical agent** — deterministic `replay_hierarchical_imitation_agent.json` / `replay_hierarchical_imitation_agent_report.json` (**proved** on `main`; see §18 / [PR #36](https://github.com/m-cahill/starlab/pull/36)). |
| **M31** | **Replay explorer / operator evidence surface** — deterministic `replay_explorer_surface.json` / `replay_explorer_surface_report.json` (**proved** on `main`; see §18 / [PR #37](https://github.com/m-cahill/starlab/pull/37)). |
| **M32** | **Audit closure I** — measurable test coverage + JUnit in CI; clone-to-run / smoke / field-test documentation; `Makefile` developer surface; draft `docs/starlab_operating_manual_v0.md`; public `docs/audit/DeferredIssuesRegistry.md` (**proved** on `main`; see §18 / [PR #38](https://github.com/m-cahill/starlab/pull/38)). |
| **M33** | **Audit closure II** — parallel **`quality` / `smoke` / `tests` / `security` / `fieldtest`** + aggregate **`governance`**; **`fieldtest-output`** CI artifact (`out/fieldtest/`); `docs/runtime/ci_tiering_field_test_readiness_v1.md` + expanded architecture / operating manual + field-test session template; coverage gate **unchanged** at **75.4** (**proved** on `main`; see §18 / [PR #39](https://github.com/m-cahill/starlab/pull/39)). |
| **M34** | **Audit closure III** — `starlab._io`; governance test split; Dependabot + dev caps; operating-manual promotion prep docs; **DIR-003**–**DIR-006** (**proved** on `main`; [PR #40](https://github.com/m-cahill/starlab/pull/40); see §18 / `M34_run1.md`). |
| **M35** | **Audit closure IV** — `M14BundleLoader`, `parser_io` / `replay_slice_generation` / observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39** (**proved** on `main`; [PR #46](https://github.com/m-cahill/starlab/pull/46); see §18 / `M35_run1.md`). **Not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI. |
| **M36** | **Audit closure V** — `docs/starlab_archive.md` (verbatim **M01–M27** §7 notes), ledger §7 archival policy + **M28–M35** inline notes, governance-test consolidation (**proved** on `main`; [PR #47](https://github.com/m-cahill/starlab/pull/47); see §18 / `M36_run1.md`). **Not** M39 flagship proof-pack **product** code. |
| **M37** | **Audit closure VI** — coverage margin recovery + CI evidence hardening (**closed** on `main`; see §11 / §18). |
| **M38** | **Audit closure VII** — public face refresh, governance rationalization, code-health tightening (**closed** on `main`; see §11 / `M38_run1.md`). |
| **M39** | **Public flagship proof pack** (**closed** on `main`; see §11 / §18). |

### Phase VI progression (compact)

| Milestone | What it proves (Phase VI) |
| --------- | ------------------------- |
| **M40** | **Agent training program charter & artifact contract** — `starlab.training`, `agent_training_program_contract.json` / report; governance / charter only (**closed** on `main`; see §11 / §18). |
| **M41** | **Replay-imitation training pipeline v1** — `starlab.imitation`, `replay_imitation_training_run.json` / report, optional local joblib weights; local-first vs CI fixture-only (**closed** on `main`; see §11 / §18). |
| **M42** | **Learned-agent comparison harness v1** — `starlab.evaluation`, `learned_agent_comparison.json` / report, `TrainedRunPredictor`, M28 metric surface reuse, ranking policy `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1`; local-first vs CI fixture-only (**closed** on `main`; see §11 / §18). |
| **M43** | **Hierarchical training pipeline v1** — `starlab.hierarchy`, `hierarchical_training_run.json` / report, optional combined joblib bundle (**closed** on `main`; see §11 / §18). |
| **M44** | **Local live-play validation harness v1** — `starlab.sc2`, M43 candidate + local `joblib`, replay binding, optional video metadata (**closed** on `main`; see §11 / §18). |
| **M45** | **Self-play / RL bootstrap v1** — `starlab.training` bootstrap emitter + M44 harness; `self_play_rl_bootstrap_run.json` / report; optional weighted re-fit (**closed** on `main`; see §11 / §18). |
| **M50** | **Industrial-scale hidden rollout + governed campaign execution v1** — campaign executor over M49 + M45, PID locks, honest visibility, extended preflight (**closed** on `main`; see §11 / §18). |

### Parser glossary (M08–M12)

| Term | Meaning |
| ---- | ------- |
| **Raw parse blocks** | Parser-owned sections lowered deterministically into `replay_raw_parse.json` (e.g. `header`, `details`, `init_data`, optional `attribute_events`). **M08** exposes structure and normalization — **not** the small public metadata API. |
| **Normalized metadata** | **M09** public contract: stable comparable fields in `replay_metadata.json` derived from M08 raw blocks — **not** event semantics. |
| **Event semantics** | Ordered interpretation of game/message/tracker streams (timeline, unit births, commands) — **M10+** scope; M08 may record **availability** only. |
| **Normalized timeline entry** | One row in `replay_timeline.json` `entries[]` after deterministic merge, semantic mapping, and privacy scrub — **M10** public contract. |
| **Event semantic** | The `semantic_kind` field — a small STARLAB enum mapped conservatively from Blizzard `_event` typenames. |
| **Strategic derivation** | Build order / economy plane — **M11** (`replay_build_order_economy.json`); combat / scouting / visibility — **M12** (`replay_combat_scouting_visibility.json`); not the M10 timeline contract by itself. |

### Phase II layering chain (compact)

M08 raw parse → M09 metadata → M10 timeline → **M11 build-order/economy** (primary: `replay_timeline.json`; optional: `replay_raw_parse.json` v2 for identity only) → **M12 combat/scouting/visibility** (primary: `replay_timeline.json` + `replay_build_order_economy.json`; optional: `replay_raw_parse.json` v2 supplemental) → **M13 replay slice definitions** (M10+M11+M12 governed JSON only; **no** `replay_raw_parse.json` in M13 v1) → **M14** bundle / lineage packaging (**not** M13).

### Phase II signal planes (compact)

- **M10** — merged event timeline (`replay_timeline.json`).  
- **M11** — macro / build-order economy (`replay_build_order_economy.json`).  
- **M12** — combat windows, scouting first-seen signals, visibility proxies (`replay_combat_scouting_visibility.json`).  
- **M13** — metadata-only replay slice definitions (`replay_slices.json`).  
- **M14** — replay bundle manifest + lineage + contents (`replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`).

### Visibility glossary (M12)

| Term | Meaning |
| ---- | ------- |
| **Explicit visibility** | Visibility state or transitions **directly** supported by governed upstream fields; M12 emits `explicit_visibility` only when unambiguous. |
| **Observation proxy** | Conservative presence interval from timeline/replay-visible signals (e.g. `unit_tag` span); **not** certified fog-of-war truth and **not** implied when observer identity is absent. |

### Metadata field glossary (M09)

| Category | Meaning |
| -------- | ------- |
| **Replay identity** | `replay_content_sha256` (opaque replay bytes); `source_raw_parse_sha256` (canonical hash of the M08 raw parse object); ties metadata to lineage without shipping raw bytes. |
| **Protocol metadata** | `protocol.base_build`, `protocol.data_build`, `protocol.data_version` — mapped from `protocol_context` / `header.m_version` only; no inference beyond M08 fields. |
| **Map / game metadata** | `map.map_name` (from `details.m_title`); `game.game_length_loops`, `game.player_count`, `game.event_streams_available` — **copied or mapped** from M08 raw sections; **no** timeline semantics from event bodies. |
| **Player metadata** | Per-player `player_index`, `player_kind`, `race_requested`, `race_actual`, `result` — from `details.m_playerList` with conservative enums; **no** display names or PII in the M09 contract. |
| **Deferred (event plane)** | Game / message / tracker **streams** and their interpretation — **M10**; not part of M09 metadata extraction. |

### Assumed vs owned guarantees

| Class | Meaning |
|-------|---------|
| **Assumed** | Upstream SC2 clients, replays, and tools behave as documented by their owners; behavior may change outside STARLAB control. |
| **Owned** | STARLAB artifact integrity, schema validity, lineage records, scorecards (once they exist), governance, CI truthfulness, and public evidence posture under this repository’s policies. |

### Deployment posture (preparatory only)

Future intent (not active in M00):

- **Netlify** — future home for `frontend/` and optionally static docs or evidence.  
- **Render** — future home for `backend/` services.  

M00 records conventions only. See `docs/deployment/deployment_posture.md` and `docs/deployment/env_matrix.md`.

### Deployment readiness is not deployment

M00 establishes hosting **conventions and governance** only. Naming Netlify and Render does **not** imply live sites, production readiness, or rights-cleared public distribution. Public hosting waits on explicit milestone authorization and provenance posture.

---

## 11. Current milestone

**Current v1.5 focus:** **`V15-M32`** — *bounded candidate checkpoint evaluation execution* — **implementation** (**`§V15-M32`** on **`docs/starlab-v1.5.md`**; merge to `main` pending) — **`python -m starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution`** — **not** benchmark pass / strength / promotion **by default**; **provisional next:** **`§V15-M33`**. **`V15-M31`** — *Candidate Checkpoint Evaluation Harness Dry-Run…* — **closed** on `main` ([PR #167](https://github.com/m-cahill/starlab/pull/167); merge `6fa7efc9372aa2e5015b0fbc87878d87dd867cc5`; authoritative PR-head [`25092872655`](https://github.com/m-cahill/starlab/actions/runs/25092872655); merge-boundary `main` [`25093208089`](https://github.com/m-cahill/starlab/actions/runs/25093208089) — **success**); **`python -m starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate`** consumes sealed **`§V15-M30`** packages — **`evaluation_harness_ready` ≠ benchmark pass**. **`V15-M28`** — *SC2-Backed T1 Candidate Training Attempt* — **closed** on `main` ([PR #164](https://github.com/m-cahill/starlab/pull/164); merge `35d59f11e64b5b8fcb2c2937572478bfa9f37863`; **authoritative PR-head CI** [`25083196925`](https://github.com/m-cahill/starlab/actions/runs/25083196925); **merge-boundary `main` CI** [`25083354466`](https://github.com/m-cahill/starlab/actions/runs/25083354466) — **success**; **`docs/starlab-v1.5.md`** **§V15-M28** — **`fixture_only`** in CI; operator-local sample **`sc2_backed_candidate_training_completed_with_candidate_checkpoint`** — **not** strength). **`V15-M27`** — *SC2 Rollout Duration and Training-Loop Integration Fix* — **closed** on `main` ([PR #163](https://github.com/m-cahill/starlab/pull/163); merge `960f925afb2d1913055fe3ae18dc0b76a4c0951f` merged **2026-04-28T21:41:00Z** UTC; **authoritative PR-head CI** [`25078974410`](https://github.com/m-cahill/starlab/actions/runs/25078974410) on head `f5915527b7bc8e3c64cb617b6a83d08b9e70a074`; **merge-boundary `main` CI** [`25079150705`](https://github.com/m-cahill/starlab/actions/runs/25079150705) — **success**). **Operator-local outcome** (see **`docs/starlab-v1.5.md`** §V15-M27): **`sc2_rollout_training_loop_integration_completed`** — real **SC2** rollout + integration-smoke training binding; **not** strength / benchmark / v2. **`V15-M26`** — **closed** on `main` ([PR #162](https://github.com/m-cahill/starlab/pull/162); merge `393adb7fb91536c16927b93216bc7045981061e5` merged **2026-04-28T10:15:38Z** UTC) — outcome **`t1_checkpoint_plumbing_completed_but_sc2_training_not_yet_meaningful`**: **synthetic CUDA** **`t1_30min_checkpoint_produced_package_ready`** (**candidate** `.pt` — **plumbing** / hash recorded — **no** promotion; **not** SC2 gameplay learning); **SC2 rollout path** bounded smoke/bootstrap — **not yet meaningful SC2 training**. **Authoritative PR-head CI** [`25046959088`](https://github.com/m-cahill/starlab/actions/runs/25046959088) (head `9d877da21bd94df1d0685215ca9f29aac808ac98`); **merge-boundary `main` CI** [`25047132158`](https://github.com/m-cahill/starlab/actions/runs/25047132158) on merge commit `393adb7f…` — **success**. Attempt A **`t1_30min_completed_without_candidate_checkpoint`**. **Honest closeout:** **not** **successful SC2 T1 training**. See **`docs/starlab-v1.5.md`** **§V15-M26**. **`V15-M25`** — **closed** on `main` ([PR #160](https://github.com/m-cahill/starlab/pull/160); PR-head [`25039149033`](https://github.com/m-cahill/starlab/actions/runs/25039149033); merge-boundary [`25039367953`](https://github.com/m-cahill/starlab/actions/runs/25039367953); merge `e4ecc95e…`): **`m21_dry_run_preflight_passed` / `ready_for_v15_m26_t1_attempt`**; **`--dry-run-preflight-only`**; **real T1** **not** entered; **no** checkpoint (**M15** **`fixture_ci`**). **`V15-M24`** — *Real Operator T1 30-Minute GPU Run Attempt & Evidence Capture* — **closed** on `main` ([PR #159](https://github.com/m-cahill/starlab/pull/159); PR-head [`25036985830`](https://github.com/m-cahill/starlab/actions/runs/25036985830); merge-boundary [`25037125881`](https://github.com/m-cahill/starlab/actions/runs/25037125881); merge `4d8e8464…`); operator-local **`operator_preflight_blocked` / `missing_private_manifest_inputs`**; **`.venv`** CUDA re-verified; **M21** **not** invoked. **Immediately preceding v1.5 milestone on `main` (before M27):** **`V15-M26`** ([PR #162](https://github.com/m-cahill/starlab/pull/162); merge `393adb7f…`). **Prior closed:** **`V15-M23`** — *CUDA PyTorch Operator Environment Remediation* — **closed** on `main` ([PR #156](https://github.com/m-cahill/starlab/pull/156); PR-head [`25032909816`](https://github.com/m-cahill/starlab/actions/runs/25032909816); merge-boundary [`25033137726`](https://github.com/m-cahill/starlab/actions/runs/25033137726); merge `7ceb750a…`; branch `v15-m23-cuda-pytorch-operator-env-remediation`). CUDA **`.venv`** (`torch 2.11.0+cu128`); **`torch.cuda.is_available()`** **true** in **`.venv`**; **RTX** **5090**; default **PATH** **Python** **CPU-only**; **M21** dry-run **not** rerun in **M23**; **no** real **T1** claim. **Prior:** **`V15-M22`** — **closed** on `main` ([PR #154](https://github.com/m-cahill/starlab/pull/154); PR-head [`25031597888`](https://github.com/m-cahill/starlab/actions/runs/25031597888); merge-boundary [`25031726394`](https://github.com/m-cahill/starlab/actions/runs/25031726394); merge `364ce5b6…`); **`operator_preflight_blocked`** / **`torch_cuda_unavailable`**; **`run_v15_m21_t1_30min_gpu_run_execution`** **not** invoked. **v1.5 GPU ladder:** T1 real 30-minute operator run → T2 2-hour scale-up → T3 12-hour campaign; evaluation, XAI, human benchmark, showcase, and v2 remain downstream of governed checkpoint evidence. **`V15-M21`** — operator-local **T1** execution/evidence tooling — **closed** on `main` ([PR #153](https://github.com/m-cahill/starlab/pull/153); PR-head [`25029512815`](https://github.com/m-cahill/starlab/actions/runs/25029512815); merge-boundary [`25029902265`](https://github.com/m-cahill/starlab/actions/runs/25029902265)); **`docs/runtime/v15_operator_t1_30min_gpu_run_execution_v1.md`**, `starlab.v15.operator_t1_30min_gpu_run_execution.v1`, `python -m starlab.v15.emit_v15_operator_t1_30min_gpu_run_execution`, `python -m starlab.v15.run_v15_m21_t1_30min_gpu_run_execution`; **dry-run preflight** posture only; **full T1** **not** merge CI; **default** **`t1_30min_run_not_started`**. **`V15-M20`** — *Real Candidate Checkpoint Production Gate* — **closed** on `main` ([PR #152](https://github.com/m-cahill/starlab/pull/152); PR-head [`25027412708`](https://github.com/m-cahill/starlab/actions/runs/25027412708); merge-boundary [`25027870414`](https://github.com/m-cahill/starlab/actions/runs/25027870414)) — `docs/runtime/v15_real_candidate_checkpoint_production_gate_v1.md`, `starlab.v15.real_candidate_checkpoint_production_gate.v1`, `python -m starlab.v15.emit_v15_real_candidate_checkpoint_production_gate`, `python -m starlab.v15.run_v15_t1_30min_candidate_checkpoint_gate` — **`fixture_no_operator_run`** default; **full T1** GPU run **not** merge CI; **not** strength evaluation; see **§V15-M20** in **`docs/starlab-v1.5.md`**. **Last closed (package assembly):** **`V15-M19`** — *Candidate checkpoint evaluation **package** assembly* — **closed** on `main` ([PR #151](https://github.com/m-cahill/starlab/pull/151); merge `e9a40a21…`; **authoritative PR-head CI** [`25025083247`](https://github.com/m-cahill/starlab/actions/runs/25025083247); **merge-boundary `main` CI** [`25025427887`](https://github.com/m-cahill/starlab/actions/runs/25025427887) — **success**). `starlab.v15.candidate_checkpoint_evaluation_package.v1` — **`docs/runtime/v15_candidate_checkpoint_evaluation_package_v1.md`** — **package assembly / SHA cross-checks only**; **not** strength evaluation; default **`blocked_missing_candidate_checkpoint_evidence`** on merge CI paths. **Last closed (readiness / refusal):** **`V15-M18`** — *Candidate Checkpoint Evaluation Readiness & Refusal Contract v1* — **closed** on `main` ([PR #150](https://github.com/m-cahill/starlab/pull/150); merge `e58e249e…`; **authoritative PR-head CI** [`25023439537`](https://github.com/m-cahill/starlab/actions/runs/25023439537); **merge-boundary `main` CI** [`25023582158`](https://github.com/m-cahill/starlab/actions/runs/25023582158) — **success**). Contract `starlab.v15.checkpoint_evaluation_readiness.v1`; runtime **`docs/runtime/v15_checkpoint_evaluation_readiness_v1.md`**; `python -m starlab.v15.emit_v15_checkpoint_evaluation_readiness`. Default fixture posture **`no_candidate_refusal`**. Strongest allowed claim: STARLAB can **deterministically classify** whether governed inputs exist to begin a **future** candidate-checkpoint **evaluation** milestone. **`candidate_ready_for_evaluation`** means structural readiness only — **not** strength evaluation. **Prior closed:** **`V15-M17`** — *Long GPU Campaign Evidence Collection* — [PR #143](https://github.com/m-cahill/starlab/pull/143) (`starlab.v15.long_gpu_campaign_evidence.v1`; **`docs/runtime/v15_long_gpu_campaign_evidence_v1.md`**) — **evidence / preflight** **surface ready**; **not** a real long campaign in implementation PR/CI; **M08** `run_v15_long_gpu_campaign` for real runs; default **`long_gpu_run_authorized` false**. **Prior closed:** **`V15-M16`** — [PR #142](https://github.com/m-cahill/starlab/pull/142) — **`docs/runtime/v15_short_gpu_environment_evidence_v1.md`**. **`V15-M15`** — [PR #141](https://github.com/m-cahill/starlab/pull/141); **preflight** only. **`V15-M14`** — [PR #140](https://github.com/m-cahill/starlab/pull/140). **`V15-M13`** — [PR #139](https://github.com/m-cahill/starlab/pull/139); default no-go. **Full V15:** **`docs/starlab-v1.5.md`**. **V15-M12** — [PR #138](https://github.com/m-cahill/starlab/pull/138). **V15-M11** — [PR #137](https://github.com/m-cahill/starlab/pull/137). **V15-M10** — [PR #136](https://github.com/m-cahill/starlab/pull/136). **Prior closed packaging / harness gate anchors:** **`§V15-M31`** (**closed** [**PR #167**](https://github.com/m-cahill/starlab/pull/167)); sealed **`§V15-M30`** assembly (**[**PR #166**](https://github.com/m-cahill/starlab/pull/166)**). **`V15-M26`** — **closed** on `main` ([PR #162](https://github.com/m-cahill/starlab/pull/162)) — bounded **non-dry-run** **T1** + **`t1_30min_checkpoint_produced_package_ready`** (**candidate** `.pt` only — **no** promotion); Attempt A **`t1_30min_completed_without_candidate_checkpoint`**. **`V15-M00`**, **`V15-M01`** — registers: **`docs/runtime/v15_training_scale_provenance_asset_registers_v1.md`**. **PX2 (closed / transition):** **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**, **`docs/runtime/px2_industrial_self_play_campaign_v1.md`**. M08: **`docs/runtime/v15_long_gpu_campaign_execution_v1.md`**. M07: **`docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`**. **`V15-M06`**: **`docs/runtime/v15_human_panel_benchmark_protocol_v1.md`**; **`V15-M05`**: **`docs/runtime/v15_strong_agent_benchmark_protocol_v1.md`**; **`V15-M04`**: **`docs/runtime/v15_xai_evidence_contract_v1.md`**; **`V15-M03`**: **`docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`**; **`V15-M02`**: **`docs/runtime/v15_long_gpu_run_environment_lock_v1.md`**.

### V15-M08 — *Long GPU Campaign Execution* — **closed** on `main` (**implementation surface**; **`implementation_ready_waiting_for_operator_run`**) 

**V15-M08** ships the **governed long-campaign surface** (preflight gates **A–G**, manifest + receipt scaffolding, **dual-guard** runner wrapping **M49–M51** `execute_full_local_training_campaign`). **Fixture / public path:** **`long_gpu_run_authorized` false**; **no** substitute for an operator-local long run. Operator execution requires **`--allow-operator-local-execution`** and **`--authorize-long-gpu-campaign`**, valid **`campaign_plan.json`**, and honest gate results (see **`docs/starlab-v1.5.md`** M08 non-claims block). **Implementation:** [PR #133](https://github.com/m-cahill/starlab/pull/133). **No** completed long GPU campaign recorded on `main` from this milestone.

### V15-M09 — *Checkpoint Evaluation and Promotion* — **closed** on `main` (implementation [PR #135](https://github.com/m-cahill/starlab/pull/135); **closeout** **`blocked_missing_m08_campaign_receipt`**)

**V15-M09** defines `starlab.v15.checkpoint_evaluation.v1` and `starlab.v15.checkpoint_promotion_decision.v1` with `python -m starlab.v15.emit_v15_checkpoint_evaluation` and `python -m starlab.v15.emit_v15_checkpoint_promotion_decision`. **Not** a completed campaign receipt by itself; default posture remains **`blocked_missing_m08_campaign_receipt`** when M08 has not completed a long run. **Authoritative PR-head CI:** [`24942859847`](https://github.com/m-cahill/starlab/actions/runs/24942859847) (head `b503ec3a…`); **merge-boundary `main` CI:** [`24942925570`](https://github.com/m-cahill/starlab/actions/runs/24942925570) on merge `eaa928d2…`.

### V15-M10 — *Replay-Native XAI Demonstration* — **closed** on `main` (implementation [PR #136](https://github.com/m-cahill/starlab/pull/136); merge `a7e9b6e9…` **2026-04-26T00:10:50Z** UTC; **authoritative PR-head CI** [`24943450910`](https://github.com/m-cahill/starlab/actions/runs/24943450910); **merge-boundary `main` CI** [`24943955088`](https://github.com/m-cahill/starlab/actions/runs/24943955088))

**V15-M10** defines `starlab.v15.replay_native_xai_demonstration.v1` with `python -m starlab.v15.emit_v15_replay_native_xai_demonstration` (default **`fixture_ci`**; optional **`operator_declared`**; optional **`operator_preflight`**). Emits `v15_replay_native_xai_demonstration.json`, JSON report, and `v15_xai_explanation_report.md`. **Not** real XAI inference, **not** faithfulness proof, **not** a promoted-checkpoint claim on the default path. **Runtime** **`docs/runtime/v15_replay_native_xai_demonstration_v1.md`**. **Authority:** **`docs/starlab-v1.5.md`** (M10 non-claims). *Future doc-density cleanup* may consolidate redundant V15 runtime pointers here without duplicating `docs/starlab-v1.5.md` narrative.

### V15-M11 — *Human Panel / Bounded Human Benchmark* — **closed** on `main` (implementation [PR #137](https://github.com/m-cahill/starlab/pull/137); merge `468d90fc…`; **authoritative PR-head CI** [`24945588527`](https://github.com/m-cahill/starlab/actions/runs/24945588527); **merge-boundary `main` CI** [`24945647654`](https://github.com/m-cahill/starlab/actions/runs/24945647654)) (governance **surface**; **not** a completed human **panel** in merge CI)

**V15-M11** defines `starlab.v15.human_panel_execution.v1` and `starlab.v15.human_benchmark_claim_decision.v1` with `python -m starlab.v15.emit_v15_human_panel_execution` and `python -m starlab.v15.emit_v15_human_benchmark_claim_decision` (default **`fixture_ci`**; optional **`operator_declared`**; optional **`operator_preflight`** for SHA-only bindings including M08/M05/M03). Binds M06 / M09 / M10 (and preflight: M08 / M05 / M03) by canonical JSON **SHA-256** only. **Not** a completed human **panel** in merge CI; **not** a “beats most humans” **public** **claim** on the default path. **Runtime** **`docs/runtime/v15_human_panel_bounded_benchmark_v1.md`**. **Authority:** **`docs/starlab-v1.5.md`** (M11 non-claims).

### V15-M12 — *Showcase Agent Release Pack* — **closed** on `main` (implementation [PR #138](https://github.com/m-cahill/starlab/pull/138); merge `1182b1bc…`; **authoritative PR-head CI** [`24946748829`](https://github.com/m-cahill/starlab/actions/runs/24946748829); **merge-boundary `main` CI** [`24946807747`](https://github.com/m-cahill/starlab/actions/runs/24946807747))

**V15-M12** defines `starlab.v15.showcase_agent_release_pack.v1` with `python -m starlab.v15.emit_v15_showcase_agent_release_pack` (default **`fixture_ci`**; optional **`operator_preflight`**; optional **`operator_declared`** with **`--release-evidence-json`**). Emits `v15_showcase_agent_release_pack.json`, JSON report, and `v15_showcase_agent_release_brief.md`. **Not** a showcase-agent **release** on the default path; **not** release **authorization**; **not** v2 (**V15-M13**). **Runtime** **`docs/runtime/v15_showcase_agent_release_pack_v1.md`**. **Authority:** **`docs/starlab-v1.5.md`** (M12 non-claims).

### V15-M13 — *v2 Go / No-Go Decision* — **closed** on `main` (implementation [PR #139](https://github.com/m-cahill/starlab/pull/139); merge `f0af5a62…` **2026-04-26T04:36:36Z** UTC; **authoritative PR-head CI** [`24948284106`](https://github.com/m-cahill/starlab/actions/runs/24948284106); **merge-boundary `main` CI** [`24948356222`](https://github.com/m-cahill/starlab/actions/runs/24948356222)) (decision surface; **not** v2 implementation)

**V15-M13** defines `starlab.v15.v2_go_no_go_decision.v1` with `python -m starlab.v15.emit_v15_v2_go_no_go_decision` (default **`fixture_ci`**; **`operator_preflight`** binds **`--m12-showcase-release-pack-json`**; optional upstream SHA cross-checks; **`operator_declared`** with **`--decision-evidence-json`** for **`starlab.v15.v2_decision_operator_evidence_declared.v1`**). Emits `v15_v2_go_no_go_decision.json`, JSON report, and `v15_v2_go_no_go_decision_brief.md`. **Not** v2 **authorization** on the default path; **not** benchmark / XAI / human-panel **execution**. **Runtime** **`docs/runtime/v15_v2_go_no_go_decision_v1.md`**. **Authority:** **`docs/starlab-v1.5.md`** (M13 non-claims).

### V15-M07 — *Training Smoke and Short GPU Shakedown* — **closed** on `main`

**PR #129:** merge `b7e4dc7c891687aea0e92ef622ab48f007bdbefe` (merged **2026-04-25T07:40:26Z** UTC). **Authoritative PR-head CI:** [`24925848388`](https://github.com/m-cahill/starlab/actions/runs/24925848388) (head `c05f3e1429674f24d8a4efd06e358490e5060ad1`); **merge-boundary `main` CI:** [`24925929052`](https://github.com/m-cahill/starlab/actions/runs/24925929052) on merge commit `b7e4dc7c…` — **success**.

V15-M07 is **receipt and bounded shakedown tooling only** — *Training smoke and short GPU shakedown* **receipt** (`starlab.v15.training_run_receipt.v1`, `python -m starlab.v15.emit_v15_training_run_receipt`). **Bounded** shakedown only; **no** long GPU **campaign** (**V15-M08**), **no** checkpoint **promotion**, **no** benchmark **execution**, and **no** claim **authorization** — see **`docs/starlab-v1.5.md`** (M07 non-claims) and **`docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`**. **Intent (met):** `v15_training_run_receipt.json` + report; default **`fixture_ci`**; optional **`operator_declared`**; optional **`operator_local_short_gpu`** with explicit guard and isolated **synthetic** trainer (not SC2/PX2 pipelines). **Operator-local shakedown** for this public closeout: **`operator_local_short_gpu_not_run`** (CUDA **unavailable** on record); **not** a claim of operator-local GPU completion. **`long_gpu_run_authorized` false**. **V15-M08** — **implementation closed** on `main` ([PR #133](https://github.com/m-cahill/starlab/pull/133)); operator-local long run **not** executed in this program record (see M08 subsection above).

### V15-M06 — *Human Panel Benchmark Protocol* — **closed** on `main`

**PR #127:** merge `994f24e605e32c0738f34eb4d09be2020d543c3c` (merged **2026-04-25T06:11:16Z** UTC). **Authoritative PR-head CI:** [`24924293130`](https://github.com/m-cahill/starlab/actions/runs/24924293130) (head `c6b2c7ddb81859b1171ace983befdf9782ef81c3`); **merge-boundary `main` CI:** [`24924371412`](https://github.com/m-cahill/starlab/actions/runs/24924371412) on merge commit `994f24e6…` — **success**.

**Intent (met):** Deterministic **human panel benchmark protocol** JSON + report (`v15_human_panel_benchmark.json` / `v15_human_panel_benchmark_report.json`); default **`fixture_ci`**; optional **`operator_declared`** with **`--protocol-json`** and optional SHA-only bindings. **Not** human-panel **recruitment** or **execution**; **not** public human-panel result **rows**; **not** a strong-agent or human-benchmark **claim**; public authority: **`docs/starlab-v1.5.md`** and **`docs/human_benchmark_register.md`**.

### V15-M05 — *Strong-Agent Benchmark Protocol* — **closed** on `main**

**PR #125:** merge `d7daee6e43613daf85e544ac5a25179cb5697c76` (merged **2026-04-25T05:18:15Z** UTC). **Authoritative PR-head CI:** [`24923242320`](https://github.com/m-cahill/starlab/actions/runs/24923242320) (head `703a874e7ff43a5aa4f92c97516e86e0d17bc89d`); **merge-boundary `main` CI:** [`24923432833`](https://github.com/m-cahill/starlab/actions/runs/24923432833) on merge commit `d7daee6e…` — **success**.

**Intent (met):** Deterministic **strong-agent scorecard / benchmark protocol** JSON + report (`starlab.v15.strong_agent_scorecard.v1` + `starlab.v15.strong_agent_benchmark_protocol.v1`); default **`fixture_ci`**; optional **`operator_declared`** with **`--protocol-json`**. **Not** benchmark or tournament **execution**; **not** live SC2; **not** checkpoint **evaluation**; **not** strong-agent **claim**; **not** XAI **review**; **not** human-panel **execution**; see **`docs/starlab-v1.5.md`** M05 non-claims. Superseded **failed** PR-head run [`24923167471`](https://github.com/m-cahill/starlab/actions/runs/24923167471) (Mypy) — **not** merge authority; fix at head `703a874e7ff43a5aa4f92c97516e86e0d17bc89d` before merge of PR #125.

### V15-M04 — *XAI Evidence Contract v1* — **closed** on `main`

**PR #123:** merge `3bf4e2ca5343b116e4e979d5dc50213596b7519b` (merged **2026-04-25T04:11:30Z** UTC). **Authoritative PR-head CI:** [`24922143448`](https://github.com/m-cahill/starlab/actions/runs/24922143448); **merge-boundary `main` CI:** [`24922278255`](https://github.com/m-cahill/starlab/actions/runs/24922278255) on merge commit `3bf4e2ca…` — **success**.

**Intent (met):** Deterministic **XAI evidence pack** JSON + report (`starlab.v15.xai_evidence_pack.v1`); default **`fixture_ci`**; optional **`operator_declared`** with **`--evidence-json`**. **Not** model inference; **not** real replay or checkpoint-blob I/O; **not** `long_gpu_run_authorized` **true**; see **`docs/starlab-v1.5.md`** M04 non-claims.

### V15-M03 — *Checkpoint Lineage and Resume Discipline* — **closed** on `main`

**PR #120:** merge `47a3fcb0a58ad6280dadc8967297774ed94ab4ad` (merged **2026-04-25T02:08:19Z** UTC). **Authoritative PR-head CI:** [`24919300604`](https://github.com/m-cahill/starlab/actions/runs/24919300604) on `68ff0556…`; **merge-boundary `main` CI:** [`24920070670`](https://github.com/m-cahill/starlab/actions/runs/24920070670) on `47a3fcb0…` — **success**.

**Intent (met):** Deterministic **checkpoint lineage manifest** JSON + report via `python -m starlab.v15.emit_v15_checkpoint_lineage_manifest --output-dir <path>`; default **`fixture_ci`**; optional **`operator_declared`** with **`--lineage-json`**. **Not** on-disk **byte** reads in default CI; **not** trainer **resume** or **rollback** **execution**; **not** `long_gpu_run_authorized` **true**; see **`docs/starlab-v1.5.md`** M03 non-claims.

### V15-M02 — Long GPU Run Environment Lock — **closed** on `main`

**PR #118:** merge `3f7e226ff0402cbb91b831e7c9397080cc8a77aa` (merged **2026-04-25**). **Authoritative PR-head CI:** [`24918006750`](https://github.com/m-cahill/starlab/actions/runs/24918006750) on `4aab910e…`; **merge-boundary `main` CI:** [`24918563270`](https://github.com/m-cahill/starlab/actions/runs/24918563270) on `3f7e226f…` — **success**.

**Intent (met):** Deterministic **environment-lock** JSON + report via `python -m starlab.v15.emit_v15_long_gpu_environment_lock --output-dir <path>`; default **`fixture_ci`**; optional **`operator_local`** with **`--probe-json`**. **Not** GPU shakedown; **not** long training; **not** claim that **fixture** CI output proves a real operator GPU + SC2 environment.

### V15-M01 — Training-Scale Provenance and Asset Registers — **closed** on `main`

**PR #117:** merge `f618a1f90d44e02879501ea067a079c760c20e6c` (merged **2026-04-24**). **Authoritative PR-head CI:** [`24914804421`](https://github.com/m-cahill/starlab/actions/runs/24914804421) on `8d4caf6…`; **merge-boundary `main` CI:** [`24916076997`](https://github.com/m-cahill/starlab/actions/runs/24916076997) on `f618a1f…` — **success**.

**Intent (met):** Public **template** registers and **`starlab.v15.training_asset_registers.v1`** emission (`python -m starlab.v15.emit_v15_training_asset_registers`); runtime **`docs/runtime/v15_training_scale_provenance_asset_registers_v1.md`** — **not** long GPU execution, **not** asset approval for claim-critical use, **not** **PX2-M04** / **PX2-M05**.

**Non-claims (preserved):** Same as **`docs/starlab-v1.5.md`** M01 block; closure **does not** register real assets or execute training.

### V15-M00 — v1.5 Training Readiness Charter and Long GPU Run Gate — **closed** on `main`

**Intent (met):** Establish **v1.5** public governance (`docs/starlab-v1.5.md`), training readiness charter JSON (`python -m starlab.v15.emit_v15_training_readiness_charter`), and runtime narrative (`docs/runtime/v15_training_readiness_charter_v1.md`) — **not** long GPU execution, **not** strength proof.

**Non-claims (preserved):** **Not** a claim that long training **ran**; **not** **PX2-M04**; **not** strength / human-benchmark / XAI completion.

### PX2-M03 — Industrial Self-Play Campaign — **closed** (ledger; implementation on `main`)

**Intent (met as bounded / governed surfaces):** First **industrial self-play** milestone line: **operator-local**, **Blackwell-class** compute **narrative** **intent**; **checkpoint** cadence, **eval** cadence, **promotion / rollback** rules, **opponent pool** / **anti-collapse** posture — per charter + readiness — **not** a **long GPU** program run as a **ledger** **deliverable**; **not** **PX2-M04** (promotion / exploit closure); **not** **PX2-M05** (demo refresh).

**Preflight:** **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`** — opening verdict **green** with **partial** opponent-pool row carried into M03 implementation.

**Slice 1 (contract + smoke, not the industrial run):** Public runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`**; Python **`starlab.sc2.px2.self_play`** — versioned campaign contract + report emitters; **policy-runtime bridge** (closed **PX2-M02** `BootstrapTerranPolicy` → **PX2-M01** TerranAction + compiler); snapshot/opponent-pool **stub** with deterministic selection; checkpoint/eval/promotion/rollback fields at contract level; **fixture-only** smoke (`tests/fixtures/px2_m02/corpus` lineage + **`tests/test_px2_m03_self_play_campaign.py`**). **Proves** campaign wiring — **not** operator-local campaign execution; **not** Blackwell completion; **not** strength proof.

**Slice 2 (execution skeleton + receipts, not the industrial run):** **`run_px2_campaign_execution_skeleton`** + **`run_manifest.json`** + sealed **`px2_self_play_campaign_run.json`** / report; **`checkpoint_receipts/`** and **`evaluation_receipts/`** subdirs with bounded **checkpoint** and **evaluation** receipt JSON (+ reports); multi-episode fixture loop + round-robin opponent **refs** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8b. **Proves** artifact tree + receipt discipline **— not** operator-local industrial completion; **not** long-run checkpoint persistence; **not** strength proof.

**Slice 3 (preflight + bounded real-weights smoke, not the industrial run):** **`run_execution_preflight`** → **`px2_self_play_execution_preflight.json`** (+ report); **`build_policy_operator_local`** (init-only or **`torch`** state_dict file + **SHA-256**); **`run_operator_local_campaign_smoke`** → sealed **`px2_self_play_operator_local_smoke.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8c. **Proves** operator-local **readiness** and **auditable weight identity** — **not** Blackwell-scale execution; **not** default merge-gate operator campaign; **not** strength proof.

**Slice 4 (multi-step continuity + sealed linkage, not the industrial run):** **`run_operator_local_campaign_continuity`** → sealed **`px2_self_play_campaign_continuity.json`** (+ report), **`continuity_chain.json`**, per-step **checkpoint** / **evaluation** / **promotion** / **rollback** receipts — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8d. **Proves** **bounded** multi-step receipt linkage — **not** industrial campaign completion; **not** **PX2-M04** promotion policy; **not** strength proof.

**Slice 5 (campaign-root manifest + opponent rotation, not the industrial run):** **`run_slice5_operator_local_campaign`** → sealed **`px2_self_play_campaign_root_manifest.json`** (+ report), **`opponent_pool/px2_opponent_pool_metadata.json`**, continuity under **`runs/<run_id>/`** with **`opponent_rotation_trace`** per episode — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8e. **Proves** **governed** operator-local **root** bookkeeping + **traceable** opponent selection — **not** industrial campaign completion; **not** full anti-collapse; **not** strength proof.

**Slice 6 (preflight seal normalization + canonical smoke path, not the industrial run):** **`preflight_seal_basis`** + **`run_canonical_operator_local_campaign_root_smoke`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8f. **Proves** logical-path preflight seals + canonical operator-local tree — **not** industrial completion.

**Slice 7 (first bounded real-run record, not the industrial run):** **`run_bounded_operator_local_real_run`** + **`px2_self_play_operator_local_real_run.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8g. **Proves** first governed **real filesystem** bounded run record — **not** industrial scale.

**Slice 8 (bounded multi-run session, not the industrial run):** **`run_bounded_operator_local_session`** + **`px2_self_play_operator_local_session.json`** + per-run **`runs/<run_id>/px2_self_play_operator_local_real_run.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8h. **Proves** **multiple** bounded runs under one campaign root — **not** long-horizon industrial self-play.

**Slice 9 (session + promotion/rollback execution step, not the industrial run):** **`run_bounded_operator_local_session_with_transition`** + **`px2_self_play_operator_local_session_transition.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8i. **Proves** one **deterministic** session-level transition bound to existing receipt lineage — **not** **PX2-M04** exploit closure; **not** industrial scale.

**Slice 10 (current-candidate carry-forward, not the industrial run):** **`run_bounded_operator_local_session_transition_with_current_candidate`** + **`px2_self_play_current_candidate.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8j; **`next_run_preflight_hints_from_current_candidate`**. **Proves** a **sealed** session-level **pointer** to checkpoint / **`weight_identity`** for the next bounded step — **not** global best policy; **not** **PX2-M04**; **not** industrial execution.

**Slice 11 (continuation run consuming current-candidate, not the industrial run):** **`run_bounded_continuation_run_consuming_current_candidate`** + **`px2_self_play_continuation_run.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8k; **`validate_current_candidate_for_continuation_run`**; CLI **`emit_px2_self_play_continuation_run`**. **Proves** the **next** bounded step **reads** **`px2_self_play_current_candidate.json`**, **rejects** input **mismatch**, and **records** **`consumed_ok`** or **`rejected_mismatch`** — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Slice 12 (post-continuation current-candidate re-anchoring, not the industrial run):** **`run_bounded_current_candidate_reanchor_after_continuation`** + **`px2_self_play_current_candidate_reanchor.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8l; CLI **`emit_px2_self_play_current_candidate_reanchor`**; refreshes **`px2_self_play_current_candidate.json`** with **`execution_kind`** slice-12 after **`consumed_ok`** continuation — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Slice 13 (second-hop continuation + optional symmetric re-anchor, not the industrial run):** **`run_bounded_second_hop_continuation_after_slice12`** + **`px2_self_play_second_hop_continuation.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8m; **`run_bounded_current_candidate_reanchor_after_second_hop`** when symmetric re-anchor is enabled; CLI **`emit_px2_self_play_second_hop_continuation`** — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Slice 14 (bounded pointer-seeded run, not the industrial run):** **`run_bounded_pointer_seeded_operator_local_run`** + **`px2_self_play_pointer_seeded_run.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8n; **`verify_loaded_current_candidate_self_seal`** + **`validate_current_candidate_for_continuation_run`**; CLI **`emit_px2_self_play_pointer_seeded_run`** — **declared seed** = latest **`px2_self_play_current_candidate.json`** — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Slice 15 (post–pointer-seeded handoff, not the industrial run):** **`run_bounded_pointer_seeded_handoff`** + **`px2_self_play_pointer_seeded_handoff.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8o; **`verify_loaded_pointer_seeded_run_self_seal`**; CLI **`emit_px2_self_play_pointer_seeded_handoff`** — **declared next-step lineage** from slice-14 **`px2_self_play_pointer_seeded_run.json`** — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Slice 16 (handoff-anchored bounded run, not the industrial run):** **`run_bounded_handoff_anchored_operator_local_run`** + **`px2_self_play_handoff_anchored_run.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8p; **`verify_loaded_pointer_seeded_handoff_self_seal`**; CLI **`emit_px2_self_play_handoff_anchored_run`** — **declared anchor** = slice-15 **`px2_self_play_pointer_seeded_handoff.json`** (`handed_off_ok` + on-disk lineage) — **not** industrial execution; **not** **PX2-M04** exploit closure.

**Bounded substantive execution (post–slice-16, not a numbered slice — not the industrial run):** **`run_bounded_substantive_operator_local_execution`** + **`px2_self_play_bounded_substantive_execution.json`** — **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8q (+ §8q evidence table); **`EXECUTION_KIND_BOUNDED_SUBSTANTIVE`**; default **15** continuity steps (bounded default, not a scientific claim); operator real-weights mode requires explicit **`--weights`** path; sealed **`weights_file_sha256_declared`** when using a real **PX2-M02** `state_dict` file; optional binding to slice-15/16 artifacts when present — **bounded substantive operator-local execution evidence** — **not** later industrial **`PX2-M03`** campaign evidence; **not** **PX2-M04** exploit closure.

**After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale.**

**In scope (milestone narrative):** Campaign **discipline** and artifact expectations; **M49–M51** as **governance reference** (exact **torch** executor wiring **not** pre-proved — **PX2-M03** implementation).

**Out of scope:** Default **CI** proof of long runs; **ladder** strength; silent **PX2-M04** opening.

**Non-claims:** **not** self-play **evidence** in-repo; **not** Blackwell run **completed** by opening; **not** strength proof; slices 1–16 and bounded substantive §8q **not** substitute for industrial **`PX2-M03`** execution phase.

### PX2-M02 — Neural Bootstrap from Replays — **closed** on `main`

**Intent (met):** Prove a **governed replay → TerranAction → neural policy → offline eval** vertical slice over the **closed PX2-M01** surface — **bounded** supervised claims only.

**PR #96 ([PX2-M02](https://github.com/m-cahill/starlab/pull/96)):** Public **`docs/runtime/px2_neural_bootstrap_from_replays_v1.md`**; Python **`starlab.sc2.px2.bootstrap`** (labeler, dataset contract, M18 flat feature adapter, policy, training/eval, dataset emitter CLI); conservative BOE-first labeling; deterministic replay-level split; CPU fixture end-to-end test (`tests/fixtures/px2_m02/`, **`tests/test_px2_m02_replay_bootstrap.py`**). **`torch`** pinned **`>=2.8,<3`** in **`pyproject.toml`** (merge includes **`pip-audit`**-clean range).

**Authoritative PR-head CI (final head before merge):** [`24645967129`](https://github.com/m-cahill/starlab/actions/runs/24645967129) on **`377d8dc9d1d5e91dbb11024334126cca14e5f0b6`** — **success**.

**Merge commit (`main`):** `3b16c73fc3dd1cd4c5fbd73dd33c6bb0b2e486db` — **merge-boundary `main` CI** [`24646072791`](https://github.com/m-cahill/starlab/actions/runs/24646072791) on merge commit `3b16c73f…` — **success**.

**Out of scope:** **PX2-M03** self-play; Blackwell campaign execution; strength or ladder proof; **`PX2-M03`** silent opening.

**Non-claims:** **not** proof the agent wins games; **not** operator campaign evidence in-repo.

**Post-closeout ledger (historical):** After **`PX2-M02`** closeout, **`current milestone`** was **`None`** until **`PX2-M03`** opened by **readiness** + governance (**`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`**). **`PX1-M05`** / **v2** **not** opened by **`PX2-M02`**. After **`PX2-M03`** transition closeout (**2026-04-23**), **`current milestone`** → **`V15-M00`** — see §23 and **`docs/starlab-v1.5.md`**.

### PX2-M01 — Full Terran Runtime & Action Surface — **closed** on `main`

**PR #95 ([PX2-M01](https://github.com/m-cahill/starlab/pull/95)):** Implementation + closeout on **`px2-m01-terran-runtime-action-surface`** — public **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`**; **`starlab.sc2.px2`**; fixture tests; ledger + governance tests — **runtime/action substrate only** — **not** training; **not** Blackwell execution; **not** strength proof.

**Authoritative PR-head CI (implementation head, pre-closeout commit):** [`24643980874`](https://github.com/m-cahill/starlab/actions/runs/24643980874) on **`c9d573460a0a82edba5a2941500902a8ccde1db8`** — **success** — **not** the closeout head CI.

**Authoritative PR-head CI (closeout head):** [`24644245868`](https://github.com/m-cahill/starlab/actions/runs/24644245868) on **`f4773d61e9981337f4799e77ec8f8ddae533f1e3`** — **success** — **not** merge-boundary `main` CI.

**Merge commit (`main`):** `dd5ce04a5ab531326ebf2b6a65951edea49e5813` — **merge-boundary `main` CI** [`24644285043`](https://github.com/m-cahill/starlab/actions/runs/24644285043) — **success** (see §23 changelog + private **`PX2-M01_run1.md`**).

**Delivered (intent):** Versioned **Terran core v1** structured action schema; placement/target vocabulary; legality/masking over a conservative **`GameStateSnapshot`**; `compile_terran_action` → **`Px2InternalCommand`**; **`burny_bridge`** semantic hints for traceability; deterministic compile receipts; fixture tests — see **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`**.

**Out of scope:** Replay imitation bootstrap (**PX2-M02**); neural architecture product work; self-play / Blackwell campaigns; strength claims; demo refresh; multi-race substrate; silent changes to closed **PX1** / **M44** semantics.

**Non-claims:** **not** training; **not** ladder proof; **not** operator campaign evidence in-repo for this milestone.

**Post-closeout ledger:** After **`PX2-M01`** closeout, **`current milestone`** = **`None`**; **`PX2-M02`** **not** opened; **`PX1-M05`** / **v2** **not** opened by **`PX2-M01`**.

### PX2-M00 — Autonomous Full-Game Agent Charter & Success Criteria — **closed** (`main`)

**PR #94 ([PX2-M00](https://github.com/m-cahill/starlab/pull/94)):** Governance PR — phase opening + closeout ledger edits on the same branch; public **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`**; **`docs/starlab.md`** + governance tests; private **`docs/company_secrets/milestones/post-v1/PX2-M00/`** memos — **not** committed by default.

**Authoritative PR-head CI (pre-closeout commit):** [`24641787057`](https://github.com/m-cahill/starlab/actions/runs/24641787057) on final opening head `b7aa3f472da19db2ed454740543d7c7dadb205eb` — **success** — **not** merge-boundary `main` CI (see changelog / private **`PX2-M00_run1.md`** for closeout commit + post-merge merge-boundary IDs).

**Delivered (intent):** Bounded public charter: Terran-first **1v1** full-game scope; definitions of full-game, “without our modifications,” and “plays well”; allowed vs disallowed scaffolding; promotion ladder **PX2-M01**–**PX2-M05**; industrial campaign **discipline** as future milestone requirement; explicit non-claims.

**Non-claims (PX2-M00 overall):** **not** Terran action-surface implementation; **not** replay-training code; **not** model architecture product work; **not** days-long Blackwell run; **not** new weights; **not** operator campaign evidence in-repo; **not** demo refresh; **not** ladder proof; **not** **v2**.

**Post-closeout ledger (historical):** After **PX2-M00** closeout, **`current milestone`** was **`None`** until **`PX2-M01`** opened separately. **`PX1-M05`** / **v2** **not** opened by **PX2-M00**.

### PX1-M04 — Governed Demo Proof Pack & Winning Video — **closed** (`main`)

**PR1 (opening / merge):** [PR #92](https://github.com/m-cahill/starlab/pull/92) — merge commit `f5e4521d35e152c97eb07458b38fb296929b5aaf` merged **2026-04-19T19:18:21Z** (UTC); **final PR head** `e57dac36d44c073198d773c8a8abd54bec5b5b56`; **authoritative PR-head CI** [`24637019658`](https://github.com/m-cahill/starlab/actions/runs/24637019658) — **success**; **merge-boundary `main` CI** [`24637049478`](https://github.com/m-cahill/starlab/actions/runs/24637049478) on merge commit `f5e4521d…` — **success**. **Superseded** PR-head run — **not** merge authority: [`24623471026`](https://github.com/m-cahill/starlab/actions/runs/24623471026) — **failure** (Ruff format — **not** merge authority). Private workflow record: **`PX1-M04_run1.md`**.

**Closeout PR:** [PR #93](https://github.com/m-cahill/starlab/pull/93) — ledger + **`PX1-M04_summary.md`** / **`PX1-M04_audit.md`** / **`PX1-M04_run2.md`**; canonical selection memo + checklist polish — records **PX1-M04** closure; **`current milestone` → None**; **PX1-M05** / **v2** **not** opened.

**Delivered:** Public runtime **`docs/runtime/px1_governed_demo_proof_pack_v1.md`** (status updated); private **`docs/company_secrets/milestones/post-v1/PX1-M04/`** — canonical run **`scripted_01`**, operator video **`out/px1_m03_operator_watchable.mp4`**, candidate **`px1_m01_weighted_refit_rl_bootstrap_v1`** — references operator-local; **not** large binary commit by default.

**Intent (met):** **Package** bounded **PX1-M03** success evidence (canonical winning run + replay + video references + traceability) — **not** new industrial campaign; **not** further remediation.

**Non-claims (PX1-M04 overall):** **not** ladder strength; **not** benchmark universality; **not** replay↔execution gameplay semantics; **not** **v2** readiness; **not** automatic **PX1-M05**.

### PX1-M03 — Candidate Strengthening & Demo Readiness Remediation — **closed** (`main`)

**PR1 (opening / freeze):** [PR #90](https://github.com/m-cahill/starlab/pull/90) — public runtime **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`**; **`starlab.sc2.emit_px1_demo_readiness_protocol`** + **`starlab.sc2.emit_px1_demo_readiness_evidence`**; hybrid **`burnysc2_policy`** `px1_m03_hybrid_v1` + fixtures — **not** operator remediation evidence.

**Closeout PR:** [PR #91](https://github.com/m-cahill/starlab/pull/91) — ledger + **`PX1-M03_summary.md`** / **`PX1-M03_audit.md`** / **`PX1-M03_run2.md`** — records successful **remediation** closure (**`demo-ready-candidate-selected`**). That closeout set **`current milestone`** to **None** until **PX1-M04** opened by a **separate** governance PR — **PX1-M04** was **opened** on `main` ([PR #92](https://github.com/m-cahill/starlab/pull/92)) and is now **closed** ([PR #93](https://github.com/m-cahill/starlab/pull/93)); **`current milestone`** is **None** again until the next chartered **`PX1-MNN`**.

**Intent (delivered):** Corrective milestone after **PX1-M02** **`no-candidate-selected`** — bounded capability uplift + fresh **`local_live_sc2`** evaluation under frozen **`px1_demo_readiness_*`** minima — **not** the final proof-pack milestone (**PX1-M04**).

**Non-claims (PX1-M03 overall):** **not** governed winning demo **pack** closure (that is **PX1-M04**); **not** ladder strength; **not** automatic **v2**; operator-local decisive evidence — **not** default merge-gate live SC2.

### PX1-M02 — Play-Quality Evaluation & Demo Candidate Selection — **closed** (`main`)

**Implementation PR (opening / protocol freeze):** [PR #88](https://github.com/m-cahill/starlab/pull/88) — merge commit `5521d8b8671e72a5f9297148ff972b13b75e408a` merged **2026-04-18T01:49:56Z** (UTC); **final PR head** `f44c66add532cc73b5dfa99ca26eb7640f961ae6`; **authoritative PR-head CI** [`24594170354`](https://github.com/m-cahill/starlab/actions/runs/24594170354) — **success**; **merge-boundary `main` CI** [`24594198357`](https://github.com/m-cahill/starlab/actions/runs/24594198357) on merge commit `5521d8b…` — **success**. **Superseded** PR-head runs: [`24594051547`](https://github.com/m-cahill/starlab/actions/runs/24594051547) — **failure** (Ruff format / coverage — **not** merge authority); [`24594125553`](https://github.com/m-cahill/starlab/actions/runs/24594125553) — **failure** (branch-aware coverage **77.98%** vs **78.0%** gate — **not** merge authority). Branch `px1-m02-play-quality-demo-candidate-selection` **retained** on `origin`. **Delivered in repo:** public runtime **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**; deterministic protocol/evidence emitters; fixtures + governance tests — **not** default CI live SC2.

**Protocol v1 → v2 (corrective):** **Protocol profile v1** was **non-discriminating** for play-quality evidence. **Protocol profile v2** is the **authoritative** bounded evaluation basis (see **`PX1-M02_protocol_v2_correction.md`**). The final evaluation series used **v2** fixtures and frozen minima; outcome **`no-candidate-selected`**.

**Milestone closeout PR:** [PR #89](https://github.com/m-cahill/starlab/pull/89) — ledger + private **`PX1-M02_summary.md`** / **`PX1-M02_audit.md`** — records **`no-candidate-selected`** — **does not** open **PX1-M03** or **v2**.

**Post-closeout ledger / CI record:** private **`PX1-M02_run2.md`** — PR-head + merge-boundary workflow analysis for closeout PR.

**Non-claims (PX1-M02 overall):** **not** demo/video proof; **not** ladder strength; operator-local bounded evaluation — **not** merge-gate live SC2 proof.

**Authoritative narrative:** **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**; **Post-PV1 (PX1)** (above §7).

### PX1-M01 — Full Industrial Campaign Execution Evidence — **closed** (`main`)

**Implementation PR (opening):** [PR #85](https://github.com/m-cahill/starlab/pull/85) — merge commit `2b97b2afe556ad61a56b6604566ef935a70669d7`; **final PR head** `135b5c9688a3d3a6b3274157d5f6130a83e66a34`; **authoritative PR-head CI** [`24589931847`](https://github.com/m-cahill/starlab/actions/runs/24589931847) — **success**; **merge-boundary `main` CI** [`24589979870`](https://github.com/m-cahill/starlab/actions/runs/24589979870) on merge commit `2b97b2a…` — **success**. **Delivered:** public runtime **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; **frozen** full-run threshold block (see doc + private **`PX1-M01_threshold_freeze.md`**); synthetic protocol fixture **`tests/fixtures/px1_m01/px1_m01_campaign_protocol.json`**; private **`PX1-M01_plan.md`**, **`PX1-M01_operator_checklist.md`**, **`PX1-M01_toolcalls.md`**, **`PX1-M01_execution_readiness.md`**; governance tests — **does not** add live SC2 to default CI; **does not** fabricate operator **`out/`** evidence.

**Post-merge ledger / CI record:** private **`PX1-M01_run1.md`** — PR-head + merge-boundary workflow analysis for [PR #85](https://github.com/m-cahill/starlab/pull/85) — **not** milestone closeout.

**Milestone closeout PR:** [PR #87](https://github.com/m-cahill/starlab/pull/87) — ledger + private **`PX1-M01_summary.md`** / **`PX1-M01_audit.md`** — **governance closeout**; records **`threshold-met`** from operator-local evidence — **does not** open **PX1-M02** or **v2**.

**Intent (delivered):** **One** authoritative **PX1** full industrial campaign under **`local_live_sc2`**, **`campaign_id`** `px1_m01_full_run_2026_04_17_a`, primary **`execution_id`** `px1_m01_exec_001`, with **M51** **`--post-bootstrap-protocol-phases`** where in scope; **minimum** evidence package + honest **`threshold-met`** — **not** **PX1-M02**/**PX1-M03**/**v2**.

**Non-claims (PX1-M01):** **not** play-quality proof; **not** demo/video; **not** ladder; **not** implying **PX1-M02** opens automatically; operator-local evidence — **not** default CI merge proof.

**Authoritative narrative:** **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; **Post-PV1 (PX1)** (above §7).

### PX1-M00 — Full Industrial Run & Demonstration Charter — **closed** (`main`)

**Implementation PR:** [PR #83](https://github.com/m-cahill/starlab/pull/83) — merged charter surfaces (public ledger, **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`**, governance tests, private plan/charter). **Authoritative PR-head CI** [`24587023204`](https://github.com/m-cahill/starlab/actions/runs/24587023204) — **success**; **merge-boundary `main` CI** [`24587086428`](https://github.com/m-cahill/starlab/actions/runs/24587086428) on merge commit `92da985…` — **success**.

**Milestone closeout PR:** [PR #84](https://github.com/m-cahill/starlab/pull/84) — ledger + private **`PX1-M00_summary.md`** / **`PX1-M00_audit.md`** — **governance closeout only**; **does not** add execution evidence; **does not** open **PX1-M01**.

**Intent (delivered):** Established **PX1** as a **separate** post-**PV1** phase with **three-way** success separation (full industrial run vs play‑quality vs demo/video), **PX1** roadmap rows, **PX1** non-claims, and public-ledger framing — **no** operator campaigns, **no** demos, **no** threshold value freeze (**schema** in charter; **PX1-M01** freezes values before execution).

**Non-claims (PX1-M00):** **governance charter + roadmap only** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **not** new Tranche A/B execution or **threshold-met** fabrication against **PV1** history; **not** automatic **v2** readiness; **did not** open **PX1-M01**–**M04**; **does not** imply **v2** begins after **PX1** automatically.

**Authoritative narrative:** **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`**; **Post-PV1 (PX1)** (below §7); private **`PX1-M00_charter.md`**.

**Post-closeout ledger (PX1-M00):** §1 quick scan + §23 + §11 — **PX1-M00** **closed**; **`current milestone`** was **None** until **PX1-M01** **opened** — **PX1-M01** is now **closed** (see **§11 `PX1-M01`**).

### PV1-M04 — Post-Campaign Analysis / Comparative Readout — **closed** (`main`)

**Implementation PR (opened milestone on `main`):** [PR #79](https://github.com/m-cahill/starlab/pull/79) — merge commit `d5280ee9cc69f8d7750546b7ed597e2de466f8a7` merged **2026-04-17** (UTC); **final PR head** `819cc2ea57b1fe3d27d09296aaebf6008577560c`; **authoritative PR-head CI** [`24548939513`](https://github.com/m-cahill/starlab/actions/runs/24548939513) — **success**; **superseded** PR-head [`24548853149`](https://github.com/m-cahill/starlab/actions/runs/24548853149) — tests job **failure** (branch-aware coverage **77.99%** vs **78.0%** gate — **not** merge authority; repaired on PR head); **merge-boundary `main` CI** [`24548992189`](https://github.com/m-cahill/starlab/actions/runs/24548992189) on merge commit `d5280ee…` — **success**. Branch `pv1-m04-post-campaign-readout` **retained** on `origin` (optional delete).

**Milestone closeout PR:** [PR #81](https://github.com/m-cahill/starlab/pull/81) — ledger + private **`PV1-M04_summary.md`** / **`PV1-M04_audit.md`** — **honest governance closeout**; **does not** add execution evidence; **does not** reinterpret **`threshold-not-met`**.

**Authoritative closeout PR-head CI** [`24549710647`](https://github.com/m-cahill/starlab/actions/runs/24549710647) on **final PR head** `99caf2156d915851df21d45a7fe1725da7094924` — **success**; **merge-boundary `main` CI** [`24549764138`](https://github.com/m-cahill/starlab/actions/runs/24549764138) on merge commit `0b2c427199ed4a42ca31119274984b8a1a456daa` — **success**.

**Product (in repo):** runtime **`docs/runtime/pv1_post_campaign_readout_v1.md`**; deterministic **`pv1_post_campaign_readout.json`** / **`pv1_post_campaign_readout_report.json`** via `python -m starlab.training.emit_pv1_post_campaign_readout` (**aggregation only** over existing campaign trees — default outputs under `--campaign-root`, optional **`--output-dir`**); **`tests/fixtures/pv1_m04/`** + **`tests/test_pv1_post_campaign_readout.py`** — **fixture-only** — **not** operator **`out/`** trees in CI.

**Non-claims (PV1-M04):** **bounded post-campaign comparative readout only** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **not** new Tranche A/B execution or **threshold-met** fabrication; **not** automatic charter of **PV1-M05**.

**Post-closeout ledger:** §1 quick scan + §23 + §11 — **PV1-M04** **closed**; **`current milestone`** → **None**; **no** **PV1-M05** opened.

### PV1-M03 — Tranche B / Full-Run Completion Evidence — **closed** (`main`)

**Merged implementation PR:** [PR #77](https://github.com/m-cahill/starlab/pull/77) — merge commit `9105a7ee6dff47acfb409f4cd08ca2693e98f9f1` merged **2026-04-17** (UTC); **final PR head** `946e332a87556767a322e8cb3039d6e4a757271c`; **authoritative PR-head CI** [`24541829597`](https://github.com/m-cahill/starlab/actions/runs/24541829597) — **success**; **merge-boundary `main` CI** [`24541875605`](https://github.com/m-cahill/starlab/actions/runs/24541875605) on merge commit `9105a7e…` — **success**. Branch `pv1-m03-tranche-b-full-run-evidence` **retained** on `origin` (optional delete).

**Milestone closeout PR:** [PR #78](https://github.com/m-cahill/starlab/pull/78) — ledger + private **`PV1-M03_run1.md`** / **`PV1-M03_summary.md`** / **`PV1-M03_audit.md`** — **honest bounded closeout**; **not** `threshold-met` fabrication.

**Post-v1 phase:** **PV1** — **not** “Phase VIII” of v1; milestone ids **`PV1-MNN`** (**not** **M62**). **v1** arc **M00–M61** remains **closed** on `main`.

**In-repo (on `main`):** Runtime **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`**; protocol fixture **`tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json`**; executor **`--skip-bootstrap-phases`** for multi-tranche continuation; governance tests — **not** default CI.

**Operator-local outcome (truthful):** Tranche B execution **`pv1_m03_exec_001`** **completed within scope** under **`local_live_sc2`** with coherent **`hidden_rollout_campaign_run.json`** and operator notes; **`full_run_threshold_declaration.md`** records **`threshold-not-met`** because the frozen **`full_run_duration_target`** is **not** satisfied by **separate** operator sessions for Tranche A vs Tranche B — **not** a claim that **`threshold-met`** was met.

**Non-claims (PV1-M03):** **Tranche B / bounded full-run completion evidence only** — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **does not** **alone** implement **PV1-M04** (separate PR).

**Next substantial follow-on (historical at PV1-M03 closeout):** **PV1** program line is **closed** on `main`; post-**PV1** work continues under **`PX1-MNN`**. **Superseded by §11 (post-PX1-M02 closeout):** **`PX1-M01`** and **`PX1-M02`** are **closed** on `main`; **`current milestone`** = **None**; **`PX1-M03`+** remain **not yet opened**; **v2** remains **not** opened.

### PV1-M02 — Tranche A Execution Evidence — **closed**

**Closed** on `main` ([PR #76](https://github.com/m-cahill/starlab/pull/76); merge commit `1c79c06f70e12215da14d1b0e0b5b71beac11ffd` merged **2026-04-16** (UTC); **final PR head** `d6e0c9c572d26b1cbc4c8c8fb791c63c7717d574`; **authoritative PR-head CI** [`24539086056`](https://github.com/m-cahill/starlab/actions/runs/24539086056) — **success**; **merge-boundary `main` CI** [`24539635014`](https://github.com/m-cahill/starlab/actions/runs/24539635014) on merge commit `1c79c06…` — **success**). Branch `pv1-m02-tranche-a-execution-evidence` **retained** on `origin` (optional delete).

**Post-v1 phase:** **PV1** — **not** “Phase VIII” of v1; milestone ids **`PV1-MNN`** (**not** **M62**). **v1** arc **M00–M61** remains **closed** on `main`.

**Intent (delivered):** Bounded **operator-local Tranche A execution evidence** on closed **M49 → M50 → M51** (`execute_full_local_training_campaign` with `--post-bootstrap-protocol-phases` where in scope); runtime **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`**; reproducible protocol fixture **`tests/fixtures/pv1_m02/pv1_m02_campaign_protocol.json`**; governance tests; canonical operator note basename **`tranche_a_operator_note.md`**; **PV1-M01** tranche checkpoint + observability index at boundary — **inspection/reference only**. Raw **`out/`** campaign trees **not** required on `main`; reference identifiers: **`pv1_m02_tranche_a_2026_04_16`** / **`pv1_m02_exec_001`**.

**Non-claims (PV1-M02):** **bounded Tranche A execution evidence only** — **not** full-run threshold satisfaction; **not** Tranche B; **not** PV1 program completion; **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as merge norm; **PV1-M03** is a **separate** milestone — **not** implied closed by **PV1-M02** merge alone.

**Next substantial follow-on (historical at PV1-M02 closeout):** **PV1** program line is **closed** on `main`; post-**PV1** work continues under **`PX1-MNN`**. **Superseded by §11 (post-PX1-M02 closeout):** **`PX1-M01`** and **`PX1-M02`** are **closed** on `main`; **`current milestone`** = **None**; **`PX1-M03`+** remain **not yet opened**; **v2** remains **not** opened.

### PV1-M01 — Campaign Observability & Checkpoint Discipline — **closed**

**Closed** on `main` ([PR #74](https://github.com/m-cahill/starlab/pull/74); merge commit `a0cb05d96c1e57b58992efd07c4bd841be539aba` merged **2026-04-16T21:37:31Z** (UTC); **final PR head** `dfe1e7761eb2155c3fc6eb5604f8b40c5337a4c5`; **authoritative PR-head CI** [`24535255531`](https://github.com/m-cahill/starlab/actions/runs/24535255531) — **success**; **merge-boundary `main` CI** [`24535324891`](https://github.com/m-cahill/starlab/actions/runs/24535324891) on merge commit `a0cb05d…` — **success**).

**Post-v1 phase:** **PV1** — **not** “Phase VIII” of v1; milestone ids **`PV1-MNN`** (**not** **M62**). **v1** arc **M00–M61** remains **closed** on `main`.

**Intent (delivered):** Pre-execution **tooling** only: deterministic **`tranche_checkpoint_receipt`** + **`campaign_observability_index`** inspection helpers over existing M49/M50/M51 campaign trees (`starlab.training` emitters); runtime **`docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`**; fixture tests — **does not** execute campaigns, **does not** constitute Tranche A evidence, **does not** fabricate missing receipts.

**Non-claims (PV1-M01):** **not** benchmark integrity; **not** replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as default merge norm; **not** full-run threshold satisfaction; **not** a substitute for operator-local execution.

**Next substantial follow-on (historical at PV1-M01 tooling closeout):** **PV1** program line is **closed** on `main`; post-**PV1** work continues under **`PX1-MNN`**. **Superseded by §11 (post-PX1-M02 closeout):** **`PX1-M01`** (full industrial run) and **`PX1-M02`** are **closed** on `main`; **`current milestone`** = **None**; **`PX1-M03`+** remain **not yet opened**; **v2** remains **not** opened.

### PV1-M00 — Post-v1 Industrial Campaign Charter & Success Criteria — **closed**

**Closed** on `main` ([PR #73](https://github.com/m-cahill/starlab/pull/73); merge commit `77118675a6f9f76e7cd466269c8d2a19ace3552f` merged **2026-04-16T20:20:27Z** (UTC); **final PR head** `2f80cfa9c1d329b520ebb99280bb12c21bfaa81d`; **authoritative PR-head CI** [`24531908110`](https://github.com/m-cahill/starlab/actions/runs/24531908110) — **success**; **merge-boundary `main` CI** [`24532016096`](https://github.com/m-cahill/starlab/actions/runs/24532016096) on merge commit `77118675…` — **success**). Branch `pv1-m00-charter-post-v1-industrial-campaign` **retained** on `origin` at closeout (optional delete).

**Intent (delivered):** **PV1** charter, full-run threshold **shape**, tranche model, checkpoint cadence, evidence classes, operator gates, explicit **non-claims** — **no** long-run campaign execution, **no** new benchmark/equivalence/ladder/live-CI product claims in this milestone.

**Artifacts:** Private charter and plan under `docs/company_secrets/milestones/post-v1/PV1-M00/` (local working surface — **not** public source of truth). Public roadmap and status: **Post-v1 (PV1)** section below §7 and quick-scan table.

**Non-claims (PV1-M00):** **not** universal benchmark integrity; **not** universal replay↔execution equivalence; **not** ladder/public strength; **not** live SC2 in CI as default merge norm; **not** multi-environment generalization.

**Post-merge:** **PV1-M02** was **not** opened by **PV1-M00**; **PV1-M01** was chartered and closed separately ([PR #74](https://github.com/m-cahill/starlab/pull/74)).

### M61 — SC2 foundation release lock & v1 proof pack — **closed**

**Closed** on `main` ([PR #72](https://github.com/m-cahill/starlab/pull/72); merge commit `35d7734d14113adf206390f153f517a93d7d41ba` merged **2026-04-16T05:33:27Z** (UTC); **authoritative PR-head CI** [`24493016581`](https://github.com/m-cahill/starlab/actions/runs/24493016581) — **success**; **merge-boundary `main` CI** [`24493963087`](https://github.com/m-cahill/starlab/actions/runs/24493963087) on merge commit `35d7734…` — **success**; tag **`v0.0.61-m61`** on merge commit **`35d7734…`**). Branch `m61-sc2-foundation-release-lock-v1` **retained** on `origin`. **Operator-local** campaign **`m61_evidence_2026_04_16_a`**, execution **`m61_exec_001`**, governed **M49→M50→M51** path with **`--post-bootstrap-protocol-phases`**, watchable **M44** validation, emitted proof pack + release-lock audit with **`release_scope_status`: `ready_within_scope`** — **not** evidenced by default CI or fixture-only tests alone.

**Phase VII** — **v1 foundation-completion** milestone after **M60**. **Product (in-repo machinery):** runtime `docs/runtime/sc2_foundation_release_lock_v1.md`; deterministic **`sc2_foundation_v1_proof_pack.json`** / **`sc2_foundation_v1_proof_pack_report.json`** (`starlab.sc2_foundation_v1_proof_pack.v1`); **`sc2_foundation_release_lock_audit.json`** / **`sc2_foundation_release_lock_audit_report.json`** (`starlab.sc2_foundation_release_lock_audit.v1`); emitters `python -m starlab.release_lock.emit_sc2_foundation_v1_proof_pack` and `python -m starlab.release_lock.emit_sc2_foundation_release_lock_audit`; operator-authored **`proof_pack_input.json`** contract (`starlab.sc2_foundation_v1_proof_pack_input.v1`); **`tests/test_m61_sc2_foundation_release_lock.py`** + `tests/fixtures/m61/` — **fixture-only** M44/campaign rows — real **`ready_within_scope`** requires the same evidence profile as the operator run (post-bootstrap, watchable M44, operator-declared full run, explicit **non-claims** — see audit checks).

**Operator recipe (not default CI):** fresh M61-designated operator-local **`python -m starlab.training.execute_full_local_training_campaign`** with **`--post-bootstrap-protocol-phases`**, governed **M49** contract + preflight, then emit proof pack + audit — raw outputs remain under **`out/`** locally; **do not** commit `docs/company_secrets/` or heavy `out/` trees.

**Explicit non-claims:** **not** universal benchmark integrity or replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public strength; **not** a substitute for bounded prior milestones; **v1 program arc ends at M61** — **no** **M62** stub unless the ledger is rechartered.

### M60 — Audit hardening & v2 readiness v1 — **closed**

**Closed** on `main` ([PR #71](https://github.com/m-cahill/starlab/pull/71); merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`; merged **2026-04-16T03:57:51Z** (UTC); **final PR head** `c7f615639bc1b26d6d2813bc55f078a048cab405`; **authoritative PR-head CI** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150); **merge-boundary `main` CI** [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939) on merge commit `9ef4e04…` — **success**; tag **`v0.0.60-m60`** on merge commit `9ef4e04…`; branch `m60-audit-hardening-v2-readiness` **deleted** after merge; see §18 / `M60_run1.md`; closeout `M60_summary.md` / `M60_audit.md` **local only** under `docs/company_secrets/` — **not** committed).

**Product (in repo):** short audit mapping `docs/audit/m60_v2_readiness_findings.md`; runtime/diligence note `docs/runtime/v2_readiness_audit_hardening_v1.md`; **private** module **`starlab.training._full_local_training_campaign_execution`** (M50 bootstrap-only + M51 protocol phase execution extracted from **`execute_full_local_training_campaign`** — **no** new public Python API); guardrails **`tests/test_m60_v2_readiness_guardrails.py`**. **Does not** reopen **M33**–**M37** / **M35** closure themes without regression evidence.

**Explicit non-claims:** **not** new equivalence/benchmark/ladder/live-SC2 claims; **not** v2 multi-environment proof; **not** substitute for **M61** release lock.

#### Residual audit debt tracker (compact)

| Audit finding (historical anchor) | First surfaced | Resolved by | Still material? | Targeted milestone |
| --- | --- | --- | --- | --- |
| Shared JSON I/O | M32 | **M34** (`starlab._io`) | No | — |
| Governance test split | M32 | **M34** | No | — |
| CI tiering / field-test artifacts | M32 | **M33** | No | — |
| Coverage / CI evidence hardening | M32 | **M37** | No | — |
| Evaluation ↔ state bundle load | M32 | **M35** (`m14_bundle_loader`) | No (regression guard in M60 tests) | — |
| Large `execute_full_local_training_campaign` module | Current-main | **M60** (private split) | No | **M60** |
| v1 release lock / proof pack | — | **M61** (operator-local `ready_within_scope`) | No | — |

### M59 — Ladder/public evaluation protocol & evidence surface v1 — **closed**

**Closed** on `main` ([PR #70](https://github.com/m-cahill/starlab/pull/70); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; merged **2026-04-16T02:45:33Z** (UTC); **final PR head** `074598af81b1c4ce7f3702b4002daacf9adb6bf3`; **authoritative PR-head CI** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360); **merge-boundary `main` CI** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on merge commit `319bc3d…` — **success**; tag **`v0.0.59-m59`** on merge commit `319bc3d…`; branch `m59-ladder-public-evaluation-protocol-evidence-surface-v1` **deleted** after merge; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority; see §18 / `M59_run1.md`; closeout `M59_summary.md` / `M59_audit.md` **local only** under `docs/company_secrets/` — **not** committed).

**Product (in repo):** runtime `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md`; `python -m starlab.sc2.emit_ladder_public_evaluation_protocol --input <protocol.json> --output-dir <dir>` → **`ladder_public_evaluation_protocol.json`** + **`ladder_public_evaluation_protocol_report.json`** (contracts **`starlab.ladder_public_evaluation_protocol.v1`**); `python -m starlab.sc2.emit_ladder_public_evaluation_evidence --protocol <protocol.json> --result-rows <rows.json> --output-dir <dir>` → **`ladder_public_evaluation_evidence.json`** + **`ladder_public_evaluation_evidence_report.json`** (contracts **`starlab.ladder_public_evaluation_evidence.v1`**); **exactly one** bounded protocol profile **`starlab.m59.protocol_profile.single_candidate_public_eval_v1`**; fixture tests + synthetic `tests/fixtures/m59/` — **not** real ladder evidence; **not** automated ladder play; **not** OCR/screenshot/scraper surfaces.

**Explicit non-claims:** **no** ladder/public **strength** or statistical-significance proof; **no** substitution for **M52**–**M56** or **M57**–**M58** tracks; **no** default merge-gate live SC2; **no** repository branch-protection automation via M59 artifacts.

### M58 — Live SC2 in CI hardening & cost guardrails v1 — **closed**

**Closed** on `main` ([PR #69](https://github.com/m-cahill/starlab/pull/69); merge commit `3a6f13910dc8056cb0d88161796dd5fe7888629d`; merged **2026-04-16T01:14:18Z** (UTC); **final PR head** `4d8fa3e6cb067b9784efc01f7668f777078b5a2d`; **authoritative PR-head CI** [`24485185914`](https://github.com/m-cahill/starlab/actions/runs/24485185914); **merge-boundary `main` CI** [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247) on merge commit `3a6f139…` — **success**; tag **`v0.0.58-m58`** on merge commit `3a6f139…`; branch `m58-live-sc2-in-ci-hardening-cost-guardrails` **retained** on `origin`; see §18 / `M58_run1.md`; closeout `M58_summary.md` / `M58_audit.md`).

**Product (in repo):** runtime `docs/runtime/live_sc2_in_ci_hardening_cost_guardrails_v1.md`; `python -m starlab.sc2.emit_live_sc2_in_ci_guardrails --output-dir <dir>` → **`live_sc2_in_ci_hardening_guardrails.json`** + **`live_sc2_in_ci_hardening_guardrails_report.json`** (contract **`starlab.live_sc2_in_ci_hardening_guardrails.v1`**); `python -m starlab.sc2.emit_live_sc2_in_ci_preflight ...` → **`live_sc2_in_ci_preflight_receipt.json`** + **`live_sc2_in_ci_preflight_receipt_report.json`** (contract **`starlab.live_sc2_in_ci_preflight_receipt.v1`**); **exactly one** guardrail profile **`starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1`**; optional **`.github/workflows/live-sc2-controlled-runner.yml`** — **`workflow_dispatch` only**, **30** minute job timeout, **7** day artifact retention, **minimal** `contents: read`, preflight-before-runner gate, explicit **`confirm_live_sc2`** input when using **`local_live_sc2`** — **not** required CI.

**Explicit non-claims:** **no** new live runner profiles beyond **`starlab.m57.runner_profile.m44_single_validation_v1`**; **no** new candidate classes beyond bounded **M43** + explicit weights; **no** substitution for **M52**–**M54** / **M55**–**M56** tracks; **no** global live-SC2-in-CI proof; **no** ladder/public evaluation by **M58** alone. Folder: `docs/company_secrets/milestones/M58/`.

### M57 — Narrow live SC2 in CI charter & controlled runner v1 — **closed**

**Closed** on `main` ([PR #68](https://github.com/m-cahill/starlab/pull/68); merge commit `29c383f85f380d2eb2a6b2a411aa7c3262f2bc0d`; merged **2026-04-15T21:32:49Z** (UTC); **final PR head** `eaff0104f140c2468bc6382984cd7e25f7323aa7`; **authoritative PR-head CI** [`24479060243`](https://github.com/m-cahill/starlab/actions/runs/24479060243); **merge-boundary `main` CI** [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on merge commit `29c383f…` — **success**; tag **`v0.0.57-m57`** on merge commit `29c383f…`; branch `m57-live-sc2-in-ci-charter-controlled-runner` **retained** on `origin`; see §18 / `M57_run1.md`; closeout `M57_summary.md` / `M57_audit.md`).

**Product (in repo):** runtime `docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md`; `python -m starlab.sc2.emit_live_sc2_in_ci_charter --output-dir <dir>` → deterministic **`live_sc2_in_ci_charter.json`** + **`live_sc2_in_ci_charter_report.json`** (contract **`starlab.live_sc2_in_ci_charter.v1`**); `python -m starlab.sc2.run_live_sc2_in_ci_controlled_runner` (wraps **`run_local_live_play_validation`**) → **`live_sc2_in_ci_controlled_runner_receipt.json`** + **`live_sc2_in_ci_controlled_runner_receipt_report.json`** (contract **`starlab.live_sc2_in_ci_controlled_runner_receipt.v1`**); **exactly one** runner profile **`starlab.m57.runner_profile.m44_single_validation_v1`**; **M43** hierarchical candidates + explicit weights only; optional **`.github/workflows/live-sc2-controlled-runner.yml`** (`workflow_dispatch` only — **not** required CI).

**Explicit non-claims:** **no** default merge-gate live SC2; **no** silent downgrade from `local_live_sc2` to `fixture_stub_ci`; **no** **M58** hardening/cost controls here; **no** ladder/public evaluation; benchmark integrity / replay↔execution equivalence remain **separate** tracks; **not** substitution for **M52**–**M54**. Folder: `docs/company_secrets/milestones/M57/`.

### M56 — Benchmark integrity evidence & reproducibility gates v1 — **closed**

**Phase VII track separation:** **Replay↔execution equivalence** (**M52**–**M54**, **closed** on `main`) and **benchmark integrity** (**M55**→**M56**) are **adjacent Phase VII tracks** with the same charter→evidence→gates *shape*, but **separate subject matter** — **M55**–**M56** do **not** collapse into or replace equivalence proofs.

**Closed** on `main` ([PR #67](https://github.com/m-cahill/starlab/pull/67); merge commit `bd7da9a6229fa067217dd04db918972a5ec73caf`; merged **2026-04-15T20:07:56Z** (UTC); **final PR head** `2c5d23b063f42bddecdc175721e8233e71938984`; **authoritative PR-head CI** [`24474743293`](https://github.com/m-cahill/starlab/actions/runs/24474743293); **merge-boundary `main` CI** [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843) on merge commit `bd7da9a…` — **success**; tag **`v0.0.56-m56`** on merge commit `bd7da9a…`; branch `m56-benchmark-integrity-evidence-reproducibility-gates` **retained** on `origin`; superseded **failure** PR-head [`24474659745`](https://github.com/m-cahill/starlab/actions/runs/24474659745) — Ruff format — **not** merge authority; see §18 / `M56_run1.md`; closeout `M56_summary.md` / `M56_audit.md`).

**Product (in repo):** runtime `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md`; `python -m starlab.benchmark_integrity.emit_benchmark_integrity_evidence` with explicit `--scripted-baseline-suite` / `--heuristic-baseline-suite` / `--evaluation-tournament` / `--evaluation-diagnostics` / `--baseline-evidence-pack`; `python -m starlab.benchmark_integrity.emit_benchmark_integrity_gates` with `--evidence` and optional `--evidence-report`; deterministic **`benchmark_integrity_evidence.json`** + **`benchmark_integrity_evidence_report.json`** (contract **`starlab.benchmark_integrity_evidence.v1`**) + **`benchmark_integrity_reproducibility_gates.json`** + **`benchmark_integrity_reproducibility_gates_report.json`** (contract **`starlab.benchmark_integrity_reproducibility_gates.v1`**); **exactly one** bounded scope **`starlab.m56.scope.fixture_only_baseline_chain_v1`** and **exactly one** gate pack **`starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`**.

**Explicit non-claims:** **M56** proves **no** global benchmark integrity; **no** substitution for **M52**–**M54** replay↔execution equivalence; **no** live SC2-in-CI / ladder / learned-subject / replay-corpus canonical promotion proofs by default. Top-level gate scope status is **`accepted_within_scope`** \| **`rejected_within_scope`** \| **`not_evaluable`** only. Folder: `docs/company_secrets/milestones/M56/`.

### M55 — Benchmark integrity charter & split-governance controls v1 — **closed**

**Closed** on `main` ([PR #66](https://github.com/m-cahill/starlab/pull/66); merge commit `625dd756f09ceb4aebe8d5f3c60ea216f9cab98e`; merged **2026-04-15T19:01:02Z** (UTC); **final PR head** `f7b1306de78b0a27b7f6095be55125630ded0aaa`; **authoritative PR-head CI** [`24472349322`](https://github.com/m-cahill/starlab/actions/runs/24472349322); **merge-boundary `main` CI** [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on merge commit `625dd75…` — **success**; tag **`v0.0.55-m55`** on merge commit `625dd75…`; branch `m55-benchmark-integrity-charter-split-governance-controls` **retained** on `origin`; superseded **failure** PR-head [`24472253485`](https://github.com/m-cahill/starlab/actions/runs/24472253485) — Ruff format — **not** merge authority; see §18 / `M55_run1.md`; closeout `M55_summary.md` / `M55_audit.md`.

**Product (in repo):** runtime `docs/runtime/benchmark_integrity_charter_v1.md`; `python -m starlab.benchmark_integrity.emit_benchmark_integrity_charter --output-dir <dir>`; deterministic **`benchmark_integrity_charter.json`** + **`benchmark_integrity_charter_report.json`**; contract id **`starlab.benchmark_integrity_charter.v1`**. **Explicit non-claims:** benchmark integrity **not yet proved**; **no** M56-style evidence/gates in M55; **no** live SC2-in-CI / ladder claims; **no** merge-bar semantics for benchmark integrity; **not** a substitute for **M52**–**M54** replay↔execution equivalence work. Folder: `docs/company_secrets/milestones/M55/`.

### M54 — Replay↔execution equivalence audit & acceptance gates v1 — **closed**

**Closed** on `main` ([PR #65](https://github.com/m-cahill/starlab/pull/65); merge commit `773dd1982f28f92512785ce0ab349b7c625f4c3d`; merged **2026-04-15T07:38:15Z** (UTC); **final PR head** `70f4f2d51049948197863e76e806cc1adbc903aa`; **authoritative PR-head CI** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561); **merge-boundary `main` CI** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on merge commit `773dd19…` — **success**; tag **`v0.0.54-m54`** on merge commit `773dd19…`; branch `m54-replay-execution-equivalence-audit-acceptance-gates` **deleted** after merge; see §18 / `M54_run1.md`; closeout `M54_summary.md` / `M54_audit.md`.

**Product (in repo):** runtime `docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md`; `python -m starlab.equivalence.emit_replay_execution_equivalence_audit` with `--evidence` (required), optional `--evidence-report`; deterministic `replay_execution_equivalence_audit.json` + `replay_execution_equivalence_audit_report.json`; gate pack **`starlab.m54.gatepack.identity_binding_acceptance_v1`** for **`starlab.m53.profile.identity_binding_v1`** — **consumes M53 evidence JSON** (canonical SHA-256 of the evidence object), **does not** rebuild evidence from raw artifacts. **Explicit non-claims:** profile-scoped outcomes only (`accepted_within_profile_scope` \| `rejected_within_profile_scope` \| `not_evaluable`); descriptive `merge_bar_language` only (`would_clear_profile_scope_gate` \| `would_block_profile_scope_gate` \| `no_profile_scope_decision`); **not** universal replay↔execution equivalence; **not** benchmark integrity; **not** live SC2 in CI; **not** ladder/public performance; **`merge_bar_language`** is **not** repository branch-protection automation. Folder: `docs/company_secrets/milestones/M54/`.

### M53 — Replay↔execution equivalence evidence surface v1 — **closed**

**Closed** on `main` ([PR #64](https://github.com/m-cahill/starlab/pull/64); merge commit `99bd43da41ac5a4d22a3eb2f438bc8ebe93b591d`; merged **2026-04-15T05:39:22Z** (UTC); **final PR head** `ec166ff4108af939755d5578a408b07e6a9d6bb1`; **authoritative PR-head CI** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924); **merge-boundary `main` CI** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on merge commit `99bd43d…` — **success**; tag **`v0.0.53-m53`** on merge commit `99bd43d…`; branch `m53-replay-execution-equivalence-evidence-surface` **deleted** after merge; see §18 / `M53_run1.md`; closeout `M53_summary.md` / `M53_audit.md`).

**Product (in repo):** runtime `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`; `python -m starlab.equivalence.emit_replay_execution_equivalence_evidence` with explicit `--run-identity` / `--lineage-seed` / `--replay-binding` paths; deterministic `replay_execution_equivalence_evidence.json` + `replay_execution_equivalence_evidence_report.json`; profile **`starlab.m53.profile.identity_binding_v1`** (M03/M04 identity chain only). **Depends on:** **M52** closed — charter `docs/runtime/replay_execution_equivalence_charter_v1.md` + contract id `starlab.replay_execution_equivalence_charter.v1`. **Explicit non-claims:** **M53** emits **evidence only** — **no** M54 audit pass/fail synthesis, **no** merge-bar equivalence verdict, **no** universal replay↔execution theorem; benchmark integrity, live SC2-in-CI proof, ladder surfaces remain **not** proved. Folder: `docs/company_secrets/milestones/M53/`.

### M52 — V1 endgame recharter & replay↔execution equivalence charter v1 — **closed**

**Closed** on `main` ([PR #63](https://github.com/m-cahill/starlab/pull/63); merge commit `c80a47bedcc5e607e45381d401411d9aa5e2f10b`; merged **2026-04-15T03:41:47Z** (UTC); **final PR head** `11ba11e0c1bcb39baaec130105a1955cfcf4d703`; **authoritative PR-head CI** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983); **merge-boundary `main` CI** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on merge commit `c80a47b…` — **success**; tag **`v0.0.52-m52`** on merge commit `c80a47b…`; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge; see §18 / `M52_run1.md`; closeout `M52_summary.md` / `M52_audit.md`).

**Product (in repo):** `docs/starlab.md` recharter to **62** milestones + Phase VII + *Remaining v1 proof-track map*; `docs/runtime/replay_execution_equivalence_charter_v1.md`; `starlab.equivalence` + `python -m starlab.equivalence.emit_replay_execution_equivalence_charter` — **charter + deterministic JSON only** — **not** paired equivalence proof (**M53** / **M54**). Folder: `docs/company_secrets/milestones/M52/`.

### M51 — Governed post-bootstrap phase orchestration v1 — **closed**

**Closed** on `main` ([PR #62](https://github.com/m-cahill/starlab/pull/62); merge commit `1e88466eb2635385b7ad56e666c45436a12f0b59`; merged **2026-04-15T00:14:35Z** (UTC); **final PR head** `f812f8098608f8c3ae45c51f12f8f40f7fbe083c`; **authoritative PR-head CI** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222); **merge-boundary `main` CI** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on merge commit `1e88466…` — **success**; tag **`v0.0.51-m51`** on merge commit `1e88466…`; branch `m51-governed-post-bootstrap-phase-orchestration` **deleted** after merge; see §18 / `M51_run1.md`; closeout `M51_summary.md` / `M51_audit.md`).

**Product (in repo):** extends `python -m starlab.training.execute_full_local_training_campaign` with `--post-bootstrap-protocol-phases` to run, in strict M49 order after bootstrap episodes: optional **aggregated weighted refit** (separate phase; consumes pseudo-label rows re-derived from completed bootstrap phase `bootstrap_dataset.json` / episode M44 JSON), **honest skip** for offline **M42** (`candidate_not_m41_comparison_compatible` — no M42 semantics extension), and one **watchable M44** on the refit joblib when refit succeeds (`run_local_live_play_validation` with `enforce_weights_sidecar_sha256=False` for refit SHA mismatch vs M43 sidecar). Per-phase `phase_receipt.json` plus `phase_receipts` on `hidden_rollout_campaign_run.json` (**`starlab.hidden_rollout_campaign_run.v2`**). Runtime: `docs/runtime/full_local_training_campaign_v1.md`, `docs/runtime/industrial_hidden_rollout_mode_v1.md`. **Not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance. Folder: `docs/company_secrets/milestones/M51/`.

### M50 — Industrial-scale hidden rollout mode & governed campaign execution v1 — **closed**

**Closed** on `main` ([PR #61](https://github.com/m-cahill/starlab/pull/61); merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b`; merged **2026-04-14T21:48:43Z** (UTC); **final PR head** `a6f0b90045a01908d4a57682bd41743826e5d543`; **authoritative PR-head CI** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763); **merge-boundary `main` CI** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) on merge commit `a0430d3…` — **success**; tag **`v0.0.50-m50`** on merge commit `a0430d3…`; branch `m50-industrial-hidden-rollout-mode` **retained** on `origin`; see §18 / `M50_run1.md`; closeout `M50_summary.md` / `M50_audit.md`).

**Product (in repo):** `python -m starlab.training.execute_full_local_training_campaign` (consumes M49 contract; orchestrates M45 `bootstrap_episodes` phases); PID lockfiles (`.starlab_campaign_output.lock`, `.campaign_execution.lock`); execution artifacts under `out/training_campaigns/<campaign_id>/campaign_runs/<execution_id>/` (`hidden_rollout_campaign_run.json`, manifest, heartbeat, resume state); `starlab.training.campaign_execution_preflight.run_campaign_execution_preflight` extends M49 preflight for maps/locks/visibility (when invoked from the executor, `campaign_execution_preflight_receipt.json` is written). Runtime: `docs/runtime/industrial_hidden_rollout_mode_v1.md`; operator guide: `docs/diligence/industrial_hidden_rollout_operator_guide.md`. **Not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance. Folder: `docs/company_secrets/milestones/M50/`.

### M49 — Full Local Training / Bootstrap Campaign Charter & Evidence Protocol — **closed**

**Closed** on `main` ([PR #60](https://github.com/m-cahill/starlab/pull/60); merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed`; merged **2026-04-14T04:43:06Z** (UTC); **final PR head** `2780de11bccd6a51cba3a1d14b24a0433e776873`; **authoritative PR-head CI** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623); **merge-boundary `main` CI** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315); tag **`v0.0.49-m49`** on merge commit `cad5f2b…`; branch `m49-full-local-training-campaign-charter` **deleted** after merge; see §18 / `M49_run1.md`; closeout `M49_summary.md` / `M49_audit.md`).

**Product (in repo):** governed **`full_local_training_campaign_contract.json`** / report + **`campaign_preflight_receipt.json`** under `out/training_campaigns/<campaign_id>/`; CLIs `python -m starlab.training.emit_full_local_training_campaign_contract` and `python -m starlab.training.emit_full_local_training_campaign_preflight`; runtime `docs/runtime/full_local_training_campaign_v1.md`. **Charter / preflight only** — **not** automatic execution, **not** automatic success, **not** proof that a long local operator campaign was executed on the merge path. **Narrow proof:** contract + preflight + docs + fixture tests. Folder: `docs/company_secrets/milestones/M49/`.

### M48 — Learned-Agent Comparison Contract-Path Alignment — **closed**

**Closed** on `main` ([PR #59](https://github.com/m-cahill/starlab/pull/59); merge commit `cdd023cb388ae99c3649978857e07af04c17df50`; merged **2026-04-14T02:21:43Z** (UTC); **final PR head** `d94bc02c78bf75605edc4d28473f48cac986e53c`; **authoritative PR-head CI** [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299); **merge-boundary `main` CI** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on merge commit `cdd023c…` — **success**; tag **`v0.0.48-m48`** on merge commit `cdd023c…`; branch `m48-learned-agent-comparison-contract-path-alignment` **deleted** after merge; see §18 / `M48_run1.md`; closeout `M48_summary.md` / `M48_audit.md`).

**Scope proved (narrow):** **M20** benchmark contract via **`--benchmark-contract`** (alias **`--contract`**); optional **`--training-program-contract`** for on-disk M40 JSON (default: in-process `build_agent_training_program_contract()`); when **`--m41`** candidates are present, **strict** **`ValueError`** if any M41 run’s `training_program_contract_sha256` / `training_program_contract_version` does not match the active M40 charter. **Not** benchmark integrity expansion, **not** new M28 metrics, **not** live SC2 in CI. Runtime: `docs/runtime/learned_agent_comparison_harness_v1.md`.

### M47 — Bootstrap Episode Distinctness & Operator Ergonomics — **closed**

**Governance recharter (2026-04-13 — user-directed):** The prior ledger **M47** stub (**M42** `--contract` path alignment) was **deferred** to **M48** (**now closed** on `main`). **M47** is rechartered to **Bootstrap Episode Distinctness & Operator Ergonomics**.

**Closed** on `main` ([PR #58](https://github.com/m-cahill/starlab/pull/58); merge commit `ebc5de0864ef6231d13efa741150d73c1ef1b98b`; merged **2026-04-14T00:47:56Z** (UTC); **final PR head** `4a8fb3e2f7aad95d2cde5b6b77577db25e42e91e`; **authoritative PR-head CI** [`24374720293`](https://github.com/m-cahill/starlab/actions/runs/24374720293); **merge-boundary `main` CI** [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on merge commit `ebc5de0…` — **success**; tag **`v0.0.47-m47`** on merge commit `ebc5de0…`; branch `m47-bootstrap-episode-distinctness-ergonomics` **retained** on `origin`; see §18 / `M47_run1.md`).

**Scope proved (narrow):** **Campaign interpretation** for multi-episode **M45** runs (**`episode_count_configured`** ≠ independent samples unless governed episode identities differ — at minimum distinct **`validation_run_sha256`**, preferably distinct **`run_id`**). **Product:** default **per-episode** M02 **`seed`** = **`bootstrap_base_seed + episode_index`** on copied match configs (`bootstrap_match_config.json`); **`starlab.m47.episode_manifest.v2`** with **`episode_seed_policy`**, **`distinct_episode_identities`**, **`episode_distinctness`** on sealed bootstrap run/report, and **`warnings`** when identities **collapse**. **Operator guidance** in `docs/runtime/self_play_rl_bootstrap_v1.md`. **Not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance. **M42** `--contract` path alignment is **M48** (**closed** on `main`).

### M46 — Bounded Live Validation Final-Status Semantics — **closed**

**Closed** on `main` ([PR #57](https://github.com/m-cahill/starlab/pull/57); merge commit `b925130d2e6bb9b2586139b17d100285e89b8e54`; merged **2026-04-13T18:12:03Z** (UTC); **final PR head** `ddb18f4cf5e74af2cf3a0f657b66911c93bb97a8`; **authoritative PR-head CI** [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005); **merge-boundary `main` CI** on merge commit [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) — **failure** (`pip-audit`); **repaired green `main` CI** [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) on `1b7b25e…` (pytest **≥9.0.3**); tag **`v0.0.46-m46`** on merge commit `b925130…`; **post-closeout `main` CI** [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) on `1b33acd…` — **success** (ledger + tag — **not** merge authority); branch `recharter/m44-bounded-live-final-status-semantics` **retained** on `origin`; see §18 / `M46_run1.md`). **Proved (narrow, M46):** **Option A** — bounded **burnysc2** runs that complete the step cap emit **`match_execution.final_status="ok"`** (governed validation success); literal SC2 **`Result`** in **`sc2_game_result`** on execution proof and M44 run JSON — **not** match victory, **not** ladder strength, **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI. Runtime docs: `docs/runtime/local_live_play_validation_harness_v1.md`, `docs/runtime/self_play_rl_bootstrap_v1.md`. **M42** `--contract` path alignment is **M48** (**closed** on `main`; see **M48** section above).

**Explicit non-claims:** **not** game outcome claims; **M42** contract-path alignment is **M48** (**closed** — see **M48** section above).

### M45 — Self-Play / RL Bootstrap v1 — **closed**

**Closed** on `main` ([PR #56](https://github.com/m-cahill/starlab/pull/56); merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`; merged **2026-04-12T20:07:19Z** (UTC); **final PR head** `0e89081cd786b527951a98eb3e63b7677f8c8c00`; **authoritative PR-head CI** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292); **merge-boundary `main` CI** [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180); tag **`v0.0.45-m45`** on merge commit `1a585b6…`; branch `m45-self-play-rl-bootstrap-v1` **retained** on `origin`; **superseded** **failure** PR-head [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — Ruff format — **not** merge authority; see §18 / `M45_run1.md`). **Proved (narrow, M45):** first **governed self-play / RL bootstrap** surface — `starlab.training` pipeline + emitter CLI, **`self_play_rl_bootstrap_run.json`** / **`self_play_rl_bootstrap_run_report.json`**, **`bootstrap_dataset.json`**, **`episodes/episode_manifest.json`**, **M44** harness rollouts, **M43** hierarchical candidate + local `joblib`, optional **`updated_policy/rl_bootstrap_candidate_bundle.joblib`**, bounded policy fields — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** broad deep RL, **not** **Phase VI integrated test campaign** completion. Runtime `docs/runtime/self_play_rl_bootstrap_v1.md`.

**Objective (historical scope):** First **governed** self-play / RL **bootstrap** surface: consume a **governed M43** hierarchical candidate + **local** `joblib` weights; drive **bounded** rollout collection through the **M44** local live-play validation harness; record rollout / reward / provenance metadata; optionally perform **one** conservative **weighted re-fit** over the existing sklearn logistic-regression family; emit deterministic **`self_play_rl_bootstrap_run.json`** / **`self_play_rl_bootstrap_run_report.json`** (+ `bootstrap_dataset.json`, per-episode M44 outputs under `out/rl_bootstrap_runs/<run_id>/episodes/`). CLI: `python -m starlab.training.emit_self_play_rl_bootstrap_run`. Plan: `docs/company_secrets/milestones/M45/M45_plan.md` (**Complete**); closeout `M45_run1.md`, `M45_summary.md`, `M45_audit.md`.

**Supported candidate source:** **M43** `hierarchical_training_run.json` + weights (same as M44).

**Rollout / bootstrap posture:** **Single-candidate** loop by default; **`bootstrap_mode`** records `single_candidate_fixture_stub` vs `single_candidate_local_live` vs reserved `mirror_self_play_local` (not implemented in v1). Episode budget is **CLI-configurable** (defaults: **1** episode for `fixture_stub_ci`, **5** for `local_live_sc2`).

**Local vs CI:** Bootstrap outputs are **local-first** (`out/rl_bootstrap_runs/`). **CI** validates a **fixture-only** `fixture_stub_ci` path (**no** live SC2, **no** committed weights).

**Explicit non-claims:** **not** benchmark integrity; **not** replay↔execution equivalence; **not** live SC2 in CI; **not** ladder / public performance; **not** a full deep-RL program; **not** the **Phase VI integrated test campaign** as an in-milestone proof — that campaign is **post-M45** (`docs/diligence/phase_vi_integrated_test_campaign.md`).

**Operator interpretation (extended local bootstrap):** An extended local **M45** campaign may be **integration-successful** (end-to-end artifacts under `out/rl_bootstrap_runs/`) but **analytically weak** if per-episode governed identities **collapse** — e.g. the same **`validation_run_sha256`** across **`episodes/e000…`** — in which case **`N` episodes must not be read as `N` independent rollout samples** for variance or refit without additional diversity controls. **M47** adds default **per-episode** M02 **`seed`** variation and **`starlab.m47.episode_manifest.v2`** distinctness fields; authoritative operator/runtime text: `docs/runtime/self_play_rl_bootstrap_v1.md`. Historical plan note: `docs/company_secrets/milestones/M45/M45_followon_operator_ergonomics_plan.md`.

### M44 — Local Live-Play Validation Harness v1 — **closed**

**Closed** on `main` ([PR #55](https://github.com/m-cahill/starlab/pull/55); merge commit `1b1067ad632643d2b14da05d510a7c2a263cc8ea`; merged **2026-04-12T18:13:50Z** (UTC); **final PR head** `dc8e74d98701c6080e525b8a79aa7aa4b7872867`; **authoritative PR-head CI** [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411); **merge-boundary `main` CI** [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884); tag **`v0.0.44-m44`** on merge commit `1b1067a…`; branch `m44-local-live-play-validation-harness-v1` **retained** on `origin`; **superseded** **failure** PR-head [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) on `c8b989a…` — Ruff format — **not** merge authority; see §18 / `M44_run1.md`). **Proved (narrow, M44):** first **governed local live-play validation harness** — **`starlab.sc2`** harness + emitter CLI, **`local_live_play_validation_run.json`** / **`local_live_play_validation_run_report.json`**, **`starlab.hierarchy.m43_sklearn_runtime`**, bounded adapter **`starlab.m44.semantic_live_action_adapter.v1`**, replay-backed validation chain (M02 proof, M03 identity / lineage, M04 replay binding), **`runtime_mode`** `fixture_stub_ci` \| `local_live_sc2`, optional video metadata — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** **M45** RL product. Runtime `docs/runtime/local_live_play_validation_harness_v1.md`.

**Objective (historical scope):** First governed **local-only** live-play validation harness: load an **M43** `hierarchical_training_run.json` + **local** `joblib` weights, run the bounded **M02** match harness (`fixture_stub_ci` + `fake` in CI; `local_live_sc2` + `burnysc2` on an operator machine), invoke **M43** manager/worker inference per step with a **bounded semantic-to-live action adapter**, emit `local_live_play_validation_run.json` / report, write **`replay/validation.SC2Replay`** (deterministic stub bytes in fixture mode; real replay when available locally), and bind via **M04** `replay_binding.json`; optional **video** path → hashed metadata only.

**Supported candidate:** **M43** hierarchical training run + weights only (v1).

**Local vs CI:** Full validation layout **local-first** (`out/live_validation_runs/`). **CI** exercises a **fixture-only** path in the **`tests`** lane (**no** GPU training, **no** live SC2, **no** committed weights).

**Explicit non-claims:** **not** benchmark integrity; **not** replay↔execution equivalence; **not** live SC2 in CI; **not** ladder / public performance; **not** mandatory video as primary proof (replay + artifacts remain primary). Plan `docs/company_secrets/milestones/M44/M44_plan.md` (**Complete**); closeout `M44_run1.md`, `M44_summary.md`, `M44_audit.md`.

### M43 — Hierarchical Training Pipeline v1 — **closed**

**Closed** on `main` ([PR #54](https://github.com/m-cahill/starlab/pull/54); merge commit `8850e378a584c9821eeab3e8c72bc499d590b308`; merged **2026-04-12T07:25:40Z** (UTC); **final PR head** `ffc428454939702fbe9c100ace9e109ee0c51605`; **authoritative PR-head CI** [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558); **merge-boundary `main` CI** [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897); tag **`v0.0.43-m43`** on merge commit `8850e37…`; superseded PR-head runs on feature branch — [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — **not** merge authority for final head `ffc4284…`; see §18 / `M43_run1.md`). **Proved (narrow, M43):** first **governed hierarchical training run** surface — **M30** four-delegate policy `starlab.m30.delegate.fixed_four_v1` over governed **M26** + **M14** with **M41**-aligned sklearn **LogisticRegression** manager and per-delegate workers, **`hierarchical_training_run.json`** / **`hierarchical_training_run_report.json`** under **`out/hierarchical_training_runs/<run_id>/`**, optional **local-only** combined `joblib` weights, **delegate_coverage**, **M40** contract binding, **M29** `interface_trace_schema_version` — **not** M42 comparison integration beyond metadata compatibility, **not** **M44** live-play, **not** benchmark integrity, **not** live SC2 in CI. Runtime `docs/runtime/hierarchical_training_pipeline_v1.md`.

**Local vs CI:** Full runs **local-first** (`out/hierarchical_training_runs/`). **CI** exercises a **fixture-only** path in the **`tests`** lane (**no** GPU training, **no** live SC2, **no** committed weights).

**Explicit non-claims:** **not** benchmark integrity; **not** replay↔execution equivalence; **not** live SC2 in CI; **not** **M42** comparison consumption of M43 outputs (deferred); **not** **M44**–**M45** product. Plan `docs/company_secrets/milestones/M43/M43_plan.md` (**Complete**); closeout `M43_run1.md`, `M43_summary.md`, `M43_audit.md`.

### M42 — Learned-Agent Comparison Harness v1 — **closed**

**Closed** on `main` ([PR #53](https://github.com/m-cahill/starlab/pull/53); merge commit `3eb091aba832cb0a66066d6fca6db091eb53c8f5`; merged **2026-04-12T06:02:16Z** (UTC); **final PR head** `191a95511a7428b0c12c79edc978070c406ad736`; **authoritative PR-head CI** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553); **merge-boundary `main` CI** [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842); tag **`v0.0.42-m42`** on merge commit `3eb091a…`; branch `m42-learned-agent-comparison-harness-v1` **deleted** after merge; superseded PR-head runs: none — sole run on final head; see §18 / `M42_run1.md`). **Proved (narrow, M42):** first governed **learned-agent comparison harness** — `starlab.evaluation` comparison modules + CLI, **`learned_agent_comparison.json`** / **`learned_agent_comparison_report.json`**, `TrainedRunPredictor` for M41 `joblib` sidecar loading, M28 metric surface reuse via `evaluate_predictor_on_test_split`, ranking policy `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1` (accuracy ↓, macro_f1 ↓, candidate_id ↑), pairwise deltas, deterministic comparison_id (SHA-256 seal); runtime `docs/runtime/learned_agent_comparison_harness_v1.md`.

**Local vs CI:** Comparison and training weights **local-first**; CI validates **fixture-only** synthesis (**no** GPU training, **no** live SC2, **no** committed weights).

**Explicit non-claims:** **not** benchmark integrity; **not** replay↔execution equivalence; **not** live SC2 in CI; **not** M43 hierarchical training; **not** statistical significance or leaderboard claims. Plan `docs/company_secrets/milestones/M42/M42_plan.md` (**Complete**); closeout `M42_run1.md`, `M42_summary.md`, `M42_audit.md`.

### M41 — Replay-Imitation Training Pipeline v1 — **closed**

**Closed** on `main` ([PR #52](https://github.com/m-cahill/starlab/pull/52); merge commit `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`; merged **2026-04-12T02:58:11Z** (UTC); **final PR head** `7c092eda7fe6554a2168968ffddbe37e929159e4`; **authoritative PR-head CI** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733); **merge-boundary `main` CI** [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820); tag **`v0.0.41-m41`** on merge commit `5e0add12…`; branch `m41-replay-imitation-training-pipeline-v1` **retained** on `origin`; superseded PR-head runs on that branch — [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190) on `4f85583…`, [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — **not** merge authority for final head `7c092ed…`; see §18 / `M41_run1.md`). **Proved (narrow, M41):** first governed **replay-imitation training pipeline** — `starlab.imitation` training modules + CLI, **`replay_imitation_training_run.json`** / **`replay_imitation_training_run_report.json`**, optional **local-only** `joblib` weights (not in repo), **M40** contract binding + feature schema; runtime `docs/runtime/replay_imitation_training_pipeline_v1.md`.

**Local vs CI:** Full training runs are **local-first**. **CI** exercises a **fixture-only** path in the **`tests`** lane (**no** GPU training, **no** live SC2).

**Explicit non-claims:** **not** benchmark-integrity upgrade; **not** ladder / live-play claims; **not** superiority over **M27** beyond bounded recorded metrics; **not** weights in-repo; **not** **M42** comparison harness as in-scope for **M41**. Plan `docs/company_secrets/milestones/M41/M41_plan.md` (**Complete**); closeout `M41_run1.md`, `M41_summary.md`, `M41_audit.md`.

### M40 — Agent Training Program Charter & Artifact Contract — **closed**

**Closed** on `main` ([PR #51](https://github.com/m-cahill/starlab/pull/51); merge commit `44e8edc5bcce8dc99576bf2be542b273095e5072`; merged **2026-04-12T00:52:29Z** (UTC); **final PR head** `be47d913737f322bbf8e9e08a672561c71d322eb`; **authoritative PR-head CI** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784); **merge-boundary `main` CI** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123); tag **`v0.0.40-m40`** on merge commit `44e8edc…`; branch `m40-agent-training-program-charter` **deleted** after merge; superseded PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) on `6690cd7f0ae79abe0db85695a0d20b4d7c48cdaf` — Ruff format — **not** merge authority; see §18 / `M40_run1.md`). **Proved (narrow, M40):** recharter Phase VI to **M40**–**M45**, **`starlab.training`**, deterministic **`agent_training_program_contract.json`** / **`agent_training_program_contract_report.json`** under `out/training_program/` (via `python -m starlab.training.emit_agent_training_program_contract`), **`docs/runtime/agent_training_program_contract_v1.md`**, ledger **42 → 46** milestones, stub **M42**–**M45** — **not** actual training, **not** weights, **not** benchmark integrity, **not** live SC2 in CI. Plan `docs/company_secrets/milestones/M40/M40_plan.md` (**Complete**); closeout `M40_run1.md`, `M40_summary.md`, `M40_audit.md`.

**Explicit non-claims (M40 — historical scope):** **not** actual model training or weights in-repo; **not** GPU training in CI; **not** live SC2 in CI; **not** benchmark integrity or replay↔execution equivalence; **not** ladder or live-play ranking claims. Training runs remain **local-first** where referenced; local GPU **RTX 5090 Blackwell** references are **non-binding** environment notes only.

### M39 — Public Flagship Proof Pack — **closed**

**Closed** on `main` ([PR #50](https://github.com/m-cahill/starlab/pull/50); merge commit `ca97027cf1827942a25c886f04b5db56b8b9fe7b`; **final PR head** `2c3fce7d3820bbfdfb655deedd3c0bb980ddc45b`; **authoritative PR-head CI** [`24292861437`](https://github.com/m-cahill/starlab/actions/runs/24292861437); **merge-boundary `main` CI** [`24293162871`](https://github.com/m-cahill/starlab/actions/runs/24293162871); tag **`v0.0.39-m39`** on merge commit `ca97027…`; superseded PR-head: none — **not** merge authority for alternate heads; see §18 / `M39_run1.md`). **Proved (narrow, M39):** `starlab.flagship` proof-pack assembly (M25/M28/M31 surfaces), `make flagship`, CI **`flagship`** + **`flagship-proof-pack`**, `docs/runtime/public_flagship_proof_pack_v1.md`, `docs/flagship_proof_pack.md` — **not** benchmark integrity, **not** live SC2 in CI, **not** replay↔execution equivalence, **not** new training-track work, **not** Phase VI product. Plan `docs/company_secrets/milestones/M39/M39_plan.md` (**Complete**); closeout `M39_run1.md`, `M39_summary.md`, `M39_audit.md`.

### M38 — Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening — **closed**

**Closed** on `main` ([PR #49](https://github.com/m-cahill/starlab/pull/49); merge commit `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96`; **authoritative PR-head CI** [`24272425346`](https://github.com/m-cahill/starlab/actions/runs/24272425346) on `3e00641…`; **merge-boundary `main` CI** [`24291882960`](https://github.com/m-cahill/starlab/actions/runs/24291882960); tag **`v0.0.38-m38`**; superseded PR-head: none — **not** merge authority; see §18 / `M38_run1.md`). **Proved (narrow, M38):** public README refresh; ledger quick-scan / current-truth table; governance test rationalization (`test_planned_program_arc_is_42_milestones` removal; **M07**/**M37** row checks); `tests/runpy_helpers.py` + regression test — **not** M39 flagship proof-pack **product**, **not** benchmark-integrity upgrade, **not** live SC2 in CI, **not** gate weakening. Plan `docs/company_secrets/milestones/M38/M38_plan.md` (**Complete**); closeout `M38_run1.md`, `M38_summary.md`, `M38_audit.md`.

### M37 — Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening — **closed**

**Closed** on `main` ([PR #48](https://github.com/m-cahill/starlab/pull/48); merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd`; **authoritative PR-head CI** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) on `a38d3a7…`; **merge-boundary `main` CI** [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848); tag **`v0.0.37-m37`**; superseded **failure** PR-head [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — **not** merge authority; see §18 / `M37_run1.md`). **Measured outcomes (CI, branch-aware TOTAL):** **~80.34%** on authoritative PR-head; **`fail_under`** raised to **78.0** (disciplined buffer vs measured baseline; **not** below prior **75.4** as a cheat). **Proved (narrow, M37):** coverage tests across core modules + CLIs; **`make check`**; CI **`$GITHUB_STEP_SUMMARY`** line for coverage TOTAL; cross-platform **`_posix_path_name_for_identity`** for Windows-style paths in `normalize_match_config_for_identity` / map path mode. **~85%** coverage remains a **stretch** across the **M37**–**M39** campaign — **not** a guaranteed claim. Plan `docs/company_secrets/milestones/M37/M37_plan.md` (**Complete**); closeout `M37_run1.md`, `M37_summary.md`, `M37_audit.md`.

**Not** benchmark-integrity upgrade by default, **not** live SC2 in CI unless a milestone explicitly changes that posture, **not** operating manual v1 unless a milestone explicitly promotes it.

### M36 — Audit Closure V — Governance Surface Rationalization and Documentation Density Control — **closed**

**Closed** on `main` ([PR #47](https://github.com/m-cahill/starlab/pull/47); merge commit `e73a53b28a4b6eeb3a2c19dd358d928c64806e89`; **authoritative PR-head CI** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **merge-boundary `main` CI** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173); tag **`v0.0.36-m36`**; superseded PR-head: none; see §18 / `M36_run1.md`). **Proved (narrow, M36):** `docs/starlab_archive.md`; **§7** archival policy + pointer + **M28–M35** inline notes; consolidated `tests/test_governance_milestones.py` / duplicate removal in `tests/test_governance_runtime.py`; `docs/starlab_archive.md` on governance doc list. Coverage gate **75.4** unchanged. **Not** M39 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI. Plan `docs/company_secrets/milestones/M36/M36_plan.md` (**Complete**); closeout `M36_run1.md`, `M36_summary.md`, `M36_audit.md`.

The **M35 full audit** artifacts (`M35_fullaudit.md`, `M35_fullaudit.json`), where present, record a **“proceed directly to flagship”** recommendation; the program **chose** **M35–M36** corrective milestones first — audit files are **historical**; this ledger records the **governance decision** without rewriting that audit.

### M35 — Audit Closure IV — Structural Decoupling and Module Decomposition — **closed**

**Closed** on `main` ([PR #46](https://github.com/m-cahill/starlab/pull/46); merge commit `5b4d24b0eca578b70f2963f1561b99bc89fef033`; **authoritative PR-head CI** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **merge-boundary `main` CI** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432); tag **`v0.0.35-m35`**; superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015) (Ruff format), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) (Mypy) — **not** merge authority; see §18 / `M35_run1.md`). **Proved (narrow, M35):** evaluation↔state decoupling via `M14BundleLoader`; `parser_io` / `replay_slice_generation` / observation reconciliation module splits; `load_json_object_strict`; ledger **M00–M39** + stubs **M36–M39**; governance tests. Plan `docs/company_secrets/milestones/M35/M35_plan.md` (**Complete**); closeout `M35_run1.md`, `M35_summary.md`, `M35_audit.md`. **Not** M39 flagship proof-pack product.

**M34** — **Audit Closure III** — **closed** on `main` ([PR #40](https://github.com/m-cahill/starlab/pull/40); merge commit `51e960d0c1c0eb20923836a8ac2400a59013bcc5`; **authoritative PR-head CI** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **merge-boundary `main` CI** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; superseded **failure** PR-head [`24261032237`](https://github.com/m-cahill/starlab/actions/runs/24261032237) — **not** merge authority). **Proved (narrow, M34):** `starlab._io` shared JSON object load helper; governance tests split across `tests/test_governance_*.py`; dev dependency upper bounds + `.github/dependabot.yml`; **`docs/diligence/operating_manual_promotion_readiness.md`** (manual remains **non-canonical**; **prep only**); **`docs/audit/broad_exception_boundaries.md`** (**DIR-005** documentation closure); **`docs/audit/DeferredIssuesRegistry.md`** **DIR-003**–**DIR-006** resolutions; coverage **75.4** unchanged. **DIR-005** resolved by **confirming/documenting** that only **approved adapter/untrusted** broad `except Exception` sites remain — **not** by code narrowing. Plan `docs/company_secrets/milestones/M34/M34_plan.md` (**Complete**); closeout `M34_run1.md`, `M34_summary.md`, `M34_audit.md`; tag **`v0.0.34-m34`** on merge commit `51e960d…`. See §18 / `M34_run1.md`.

**M33** is **closed** on `main` ([PR #39](https://github.com/m-cahill/starlab/pull/39); merge commit `975ac52fff206f9ceb1b0be66a0e7f1c7386a248`; **authoritative PR-head CI** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **merge-boundary `main` CI** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md`); plan `docs/company_secrets/milestones/M33/M33_plan.md` (**Complete**); closeout `M33_run1.md`, `M33_summary.md`, `M33_audit.md`; tag **`v0.0.33-m33`** on merge commit `975ac52…`.

**Predecessor (M33):** **Audit Closure II** — parallel **`CI`** jobs (`quality`, `smoke`, `tests`, `security`, `fieldtest`, **`governance`**), **`fieldtest-output`** artifact, **`docs/runtime/ci_tiering_field_test_readiness_v1.md`**, **`docs/diligence/field_test_session_template.md`**, expanded **`docs/architecture.md`** / **`docs/starlab_operating_manual_v0.md`** / clone-to-run / checklist / smoke surfaces; **DIR-001**, **DIR-002**, **DIR-007** resolved; coverage **75.4** unchanged.

**Predecessor (M32):** **Audit Closure I** — measured **`coverage.xml` / `pytest-junit.xml`** in CI, **`fail_under`** line gate, SHA-pinned actions, **`@pytest.mark.smoke`** + `make smoke`, **`Makefile`**, **`docs/audit/DeferredIssuesRegistry.md`**, **42 milestones (M00–M41)** at the time (per §7; M32 closeout originally recorded a shorter arc — historical); **OD-007** later tracked legacy **M41** platform charter — now **deferred beyond the active arc** (§12).

**Predecessor (M31):** **Replay explorer / operator evidence surface** — deterministic **`replay_explorer_surface.json`** / **`replay_explorer_surface_report.json`**; runtime contract `docs/runtime/replay_explorer_surface_v1.md`; product `starlab/explorer/` + CLI `python -m starlab.explorer.emit_replay_explorer_surface`. **Import rule:** listed explorer modules do not import `starlab.replays`, `starlab.sc2`, or `s2protocol`. See **Phase V replay explorer glossary (M31)** in §10.

**Explicit non-claims (M31):** not benchmark integrity, not live SC2, not web UI, not M39 flagship proof pack product.

**Predecessor (M30):** **First learned hierarchical agent** — deterministic **`replay_hierarchical_imitation_agent.json`** / **`replay_hierarchical_imitation_agent_report.json`**; runtime contract `docs/runtime/replay_hierarchical_imitation_agent_v1.md`; product `starlab/hierarchy/` (`delegate_policy.py`, `hierarchical_agent_*.py`, `emit_replay_hierarchical_imitation_agent.py`) + CLI `python -m starlab.hierarchy.emit_replay_hierarchical_imitation_agent`; delegate policy **`starlab.m30.delegate.fixed_four_v1`**; traces use **`starlab.hierarchical_agent_interface_trace.v1`**. **Explicit non-claims:** not benchmark integrity, not live SC2, not raw action legality.

**Predecessor (M29):** **Hierarchical agent interface layer** — deterministic **`hierarchical_agent_interface_schema.json`** / **`hierarchical_agent_interface_schema_report.json`** on `main` ([PR #35](https://github.com/m-cahill/starlab/pull/35); see §18 / `M29_run1.md`).

#### Post–M46 closure — explicit non-claims (standing)

**M40**–**M46** are **closed** on `main` with recorded CI (see §18). Treat the following as **not proved** by default:

- **Benchmark integrity** / leaderboard claims; **replay↔execution equivalence**; **live SC2 in CI**; **ladder / public performance**; completion of the **Phase VI integrated test campaign** (operator-local post-M45 work unless separately evidenced). **M42** comparison artifacts **do not** prove benchmark integrity, statistical significance, or live-play outcomes.

**M51**–**M61** are **closed** on `main` (**M61** closes the **planned v1** foundation-completion arc). **M52** delivered **governance + charter** only; **M53** delivered **evidence surface** JSON/report only (evidence-only posture); **M54** delivered the **profile-scoped audit / acceptance-gate** layer over M53 evidence (bounded, not universal equivalence); **M55** delivered **charter-only** benchmark-integrity JSON + runtime contract (**not** integrity proved); **M56**–**M60** are **closed** on `main`; **M61** adds **within-scope release-lock closure** (`ready_within_scope`) via **operator-local** industrial campaign evidence + proof pack + audit — **not** global benchmark integrity; **not** universal replay↔execution equivalence; **not** merge-gate live SC2; **not** ladder/public performance; **not** `ready_within_scope` from repo CI alone without that evidence profile.
- **Operating manual** promoted to canonical **v1** (**not** claimed until a promotion milestone).

**M39 (closed) does not prove:** benchmark integrity, live SC2 in CI, replay↔execution equivalence, or new training tracks — see `docs/runtime/public_flagship_proof_pack_v1.md` and `public_flagship_proof_pack.json` **non_claims**.

#### M34 deferred-issue closure (compact)

| ID | Resolution |
| -- | ----------- |
| **DIR-003** | `starlab/_io.py` — `load_json_object` + `parse_json_object_text`; tuple-return callers import shared helper; raise-on-error callers use thin wrappers over `parse_json_object_text`. |
| **DIR-004** | `tests/test_governance*.py` split (`tests/test_governance.py` removed). |
| **DIR-005** | **Documentation-only validation** — see `docs/audit/broad_exception_boundaries.md` (approved boundary catches only). |
| **DIR-006** | Dev dependency upper bounds in `pyproject.toml` + `.github/dependabot.yml` (weekly `pip` + `github-actions` on `main`). |

**Operating manual v1 blockers (still):** ledger remains authoritative; runtime contracts govern artifacts; a future promotion milestone must define v1 scope and governance without contradicting `docs/starlab.md` (see `docs/diligence/operating_manual_promotion_readiness.md`).

---

## 12. Open decisions

| ID     | Decision                         | Status   | Target Milestone | Notes                                                              |
| ------ | -------------------------------- | -------- | ---------------- | ------------------------------------------------------------------ |
| OD-001 | License posture                  | Resolved | M00              | Custom source-available terms in `LICENSE` (evaluation/verification); public/private surfaces governed by `docs/public_private_boundary.md` |
| OD-002 | Public/private boundary          | Resolved | M00              | `docs/public_private_boundary.md`                                  |
| OD-003 | Replay/data provenance policy    | Resolved | M07 | Governed intake gate (`docs/runtime/replay_intake_policy.md`, `starlab/replays/`); interim policy remains in `docs/replay_data_provenance.md` for broader context |
| OD-004 | Naming / brand diligence posture | Resolved | M00              | `docs/branding_and_naming.md`                                      |
| OD-005 | SC2 runtime surface selection    | Resolved | M01              | Canonical: SC2API/`s2client-proto` + `s2protocol`; optional `python-sc2` as adapter only; PySC2 deferred — see `docs/runtime/sc2_runtime_surface.md` |
| OD-006 | Rights register format           | Resolved | M00              | `docs/rights_register.md` (canonical); this ledger summarizes      |
| OD-007 | Second-environment posture       | Deferred | Beyond **v1** arc (post-**M61**); **v2** multi-environment expansion | Formerly tied to legacy **M41** platform charter stub; **FUT-005** items remain deferred — see §19; not a **Phase VII** merge obligation |

---

## 13. Risks and constraints

### Early known risks

- SC2 environment brittleness
- replay/data rights ambiguity
- premature abstraction toward multi-game support
- public/private surface drift
- unclear acquisition posture decisions made too late
- accidental dependency or license contamination
- narrative dilution through overexpansion

### Constraint summary

- project should remain milestone-sized
- public docs should stay honest
- acquisition-aware cleanliness should not turn into bureaucracy
- platform ambition should not outrun substrate proof

---

## 14. Strategic value ladder (target framing)

This ledger uses the following strategic value ladder as a planning aid, not a literal market-price claim.

| Tier | Program State                       | Strategic / Platform-Equivalent Value |
| ---- | ----------------------------------- | ------------------------------------- |
| 1    | Prototype / Early Lab               | $0.5M–$2M                             |
| 2    | Full Lab Substrate                  | $2M–$10M                              |
| 3    | Multi-Environment-Capable Substrate | $10M–$25M                             |
| 4    | Community Benchmark Standard        | $25M–$75M                             |
| 5    | Strategic Internal Asset            | $50M–$150M                            |
| 6    | Field-Defining Platform             | $150M–$300M+                          |

**Interpretation:** early value is most likely to appear as **career signal → strategic internal leverage → platform leverage**, not as immediate direct commercialization.

---

## 15. Public evidence posture

STARLAB should prefer evidence that is:

- milestone-tied
- reproducible
- reviewable
- low on hype
- explicit about both proofs and non-proofs

Examples of good evidence:

- tests
- benchmark reports
- replay-linked artifacts
- milestone summaries
- audit notes
- explicit non-claims
- provenance notes
- dependency disclosures

Examples of weak evidence:

- vague capability claims
- anecdotal performance
- architecture claims without milestone proof
- public statements that outrun documentation

---

## 16. Rights / provenance / diligence tracker (starter)

This section starts simple and should become more explicit as the project matures.

| Surface                            | Current posture                                                | Status                 |
| ---------------------------------- | -------------------------------------------------------------- | ---------------------- |
| Code ownership                     | Expected to be first-party and traceable                       | Initial                |
| Documentation ownership            | Expected to be first-party and traceable                       | Initial                |
| SC2 client / Battle.net runtime    | Acquire under Blizzard terms (EULA / AI & ML license as applicable); **not** redistributed via this repo; see `docs/runtime/*` | Governed (M01) |
| SC2 maps / replay packs            | Local-only; **not** committed; rights per Blizzard / pack terms; quarantine if unclear | Governed (M01) |
| Raw replay bytes (third-party / ladder) | Local-only; **not** committed; rights per Blizzard / pack terms; quarantine if unclear; **M07** records **declared** posture only | Governed (M07) |
| Replay intake receipts / reports (`replay_intake_*.json`) | STARLAB **governed** JSON; operator-declared metadata + policy outcome; **not** legal certification | Governed (M07) |
| Canonical-reviewed corpus assets | **No** corpus promotion without explicit provenance + redistribution posture; see `docs/replay_data_provenance.md`, `docs/rights_register.md`, and M07 intake statuses | Governed (M01 / M07) |
| Replay/data rights (interim policy) | `docs/replay_data_provenance.md` + M07 intake contract | Resolved (M07) |
| Third-party dependency obligations | CI: pip-audit + CycloneDX SBOM artifact (`pyproject.toml` dev) | Initial                |
| Public/private split               | `docs/public_private_boundary.md`                              | Initial                |
| Contributor policy                 | `CONTRIBUTING.md`                                              | Initial                |
| License decision                   | Custom source-available (`LICENSE`)                            | Initial                |

---

## 17. Milestone closeout requirements

Every closed milestone should update this ledger with:

1. milestone status
2. merged branch / PR / SHA (if applicable)
3. CI evidence
4. short summary of what was actually proved
5. explicit non-proofs
6. open decisions changed by the milestone
7. any new risks or deferred items
8. changelog entry

**Rule:** a milestone is not fully closed until this file reflects it.

**Closeout hygiene:** Prefer **at most one** post-merge `main` documentation-only commit per milestone closeout; if further fixes are needed afterward, land them on the **next milestone branch** rather than repeated doc-only churn on `main` (see M09 run-record footnotes on merge-boundary vs non-merge-boundary CI).

### CI authority glossary (compact)

| Term | Meaning |
| ---- | ------- |
| **Authoritative green PR-head CI** | A completed **success** `pull_request` workflow run on the **final PR head SHA** before merge — primary **merge-gate** evidence when present. |
| **Merge-boundary `main` CI** | First `push` workflow run to `main` triggered by merging a PR (merge commit or squash), before unrelated follow-up commits. |
| **Repaired green `main` CI** | A later `main` run that fixes red merge-boundary CI (e.g. M10 Mypy repair) — **not** a substitute for PR-head green when citing merge discipline. |
| **Non-merge-boundary runs** | Doc-only, ledger, or chore pushes to `main` after the merge boundary — **not** merge authority; keep tables capped (M09 lesson). |

---

## 18. Milestone closeout ledger

This section should be filled as milestones close.

| Milestone | Closeout Date | PR | Merge commit | Notes |
| --------- | ------------- | -- | ------------ | ----- |
| M00       | 2026-04-06    | [#1](https://github.com/m-cahill/starlab/pull/1) | `f9203dd555ea267bc2d72c3470b174ca35a23788` | Governance bootstrap; merged to `main`; see CI evidence below |
| M01       | 2026-04-06    | [#2](https://github.com/m-cahill/starlab/pull/2) | `4a916033f55c6b8c4a582f985233a64ca039ead3` | SC2 runtime surface decision, environment lock docs, `starlab.sc2` probe; OD-005 resolved; merged to `main`; see CI evidence below |
| M02       | 2026-04-06    | [#3](https://github.com/m-cahill/starlab/pull/3) | `53a24a4a6106168afe79e0a70d51a20bfef4ea18` | Deterministic match harness, proof artifact, fake + BurnySc2 adapters; merged to `main`; narrow local harness evidence in `docs/company_secrets/milestones/M02/`; see CI evidence below |
| M03       | 2026-04-07    | [#4](https://github.com/m-cahill/starlab/pull/4) | `6bfe6a7b32a004f62a491bf31573e12cd211118a` | Run identity + lineage seed (`starlab/runs/`), runtime contract, fixtures/tests; merged to `main`; narrow claims only — see CI evidence below |
| M04       | 2026-04-07    | [#5](https://github.com/m-cahill/starlab/pull/5) | `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` | Replay binding (`replay_binding.json`), `docs/runtime/replay_binding.md`, synthetic replay fixture, tests/CLI; merged to `main`; narrow opaque-bytes claim only — see CI evidence below |
| M05       | 2026-04-07    | [#6](https://github.com/m-cahill/starlab/pull/6) | `bad27db36c135fd772e38dcafa64d6fa59577db0` | Canonical run artifact v0 (`manifest.json` / `hashes.json` + M03/M04 JSON); merged to `main`; narrow packaging only — see CI evidence below |
| M06       | 2026-04-07    | [#7](https://github.com/m-cahill/starlab/pull/7) | `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` | Environment drift + smoke matrix (`runtime_smoke_matrix.json` / `environment_drift_report.json`); merged to `main`; narrow fixture-driven claims only — see CI evidence below |
| M07       | 2026-04-07    | [#8](https://github.com/m-cahill/starlab/pull/8) | `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` | Replay intake policy (`replay_intake_receipt.json` / `replay_intake_report.json`); merged to `main`; narrow opaque-bytes + declared-metadata claims only — see CI evidence below |
| M08       | 2026-04-07    | [#9](https://github.com/m-cahill/starlab/pull/9) | `b99233e807177d65737beaba5246efa67a3edce2` | Replay parser substrate (`replay_parse_receipt.json` / `replay_parse_report.json` / `replay_raw_parse.json`); merged to `main`; narrow substrate + deterministic artifacts only — see CI evidence below |
| M09       | 2026-04-07    | [#10](https://github.com/m-cahill/starlab/pull/10) | `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` | Replay metadata extraction (`replay_metadata.json` / `replay_metadata_report.json`); merged to `main`; narrow pure extraction over M08 artifacts — see CI evidence below |
| M10       | 2026-04-07    | [#11](https://github.com/m-cahill/starlab/pull/11) | `cb3e581f70f85653477081eb1ef4772229f05983` | Timeline & event extraction (`replay_timeline.json` / `replay_timeline_report.json`, optional `replay_raw_parse` v2 `raw_event_streams`); merge-push CI failed Mypy — repaired on `main` (`cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b`); see §18 / `M10_run1.md` |
| M11       | 2026-04-07    | [#12](https://github.com/m-cahill/starlab/pull/12) | `38c15302badd49966b17f9195ddb139f6ae9a9b4` | Build-order & economy plane (`replay_build_order_economy.json` / `replay_build_order_economy_report.json`); **green PR-head** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320); **green merge-push `main`** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347); see §18 / `M11_run1.md` |
| M12       | 2026-04-07    | [#13](https://github.com/m-cahill/starlab/pull/13) | `78528958a616177b564e603c193fb0d7f8af734e` | Combat/scouting/visibility (`replay_combat_scouting_visibility.json` / `replay_combat_scouting_visibility_report.json`); **green PR-head** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392); **green merge-push `main`** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513); see §18 / `M12_run1.md` |
| M13       | 2026-04-08    | [#14](https://github.com/m-cahill/starlab/pull/14) | `f86e36837e81b8552639c5a885a13a773b96215c` | Replay slice definitions (`replay_slices.json` / `replay_slices_report.json`); **green PR-head** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047); **green merge-push `main`** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177); see §18 / `M13_run1.md` |
| M14       | 2026-04-08    | [#15](https://github.com/m-cahill/starlab/pull/15) | `8a0439a9a2970a74f3a5087390fc080f02852246` | Replay bundle + lineage (`replay_bundle_manifest.json` / `replay_bundle_lineage.json` / `replay_bundle_contents.json`); **green PR-head** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373); **green merge-push `main`** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909); see §18 / `M14_run1.md` |
| M15       | 2026-04-08    | [#16](https://github.com/m-cahill/starlab/pull/16) | `b0f7132a54508f35d54406011cd3b37bce776927` | Canonical state schema v1 (`canonical_state_schema.json` / `canonical_state_schema_report.json`); **green PR-head** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141); **green merge-push `main`** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800); see §18 / `M15_run1.md` |
| M16       | 2026-04-08    | [#17](https://github.com/m-cahill/starlab/pull/17) | `dd9546f88ebcf9b454498eec83a14d742d17d070` | Structured state pipeline (`canonical_state.json` / `canonical_state_report.json`); **green PR-head** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775); **green merge-push `main`** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811); superseded red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority); see §18 / `M16_run1.md` |
| M17       | 2026-04-08    | [#18](https://github.com/m-cahill/starlab/pull/18) | `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` | Observation surface contract (`observation_surface_schema.json` / `observation_surface_schema_report.json`); **green PR-head** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530); **green merge-push `main`** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167); see §18 / `M17_run1.md` |
| M18       | 2026-04-09    | [#19](https://github.com/m-cahill/starlab/pull/19) | `59d2d6e2af08852d63e0c91a984000c11decfece` | Perceptual bridge prototype (`observation_surface.json` / `observation_surface_report.json`); **green PR-head** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039); **green merge-push `main`** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479); see §18 / `M18_run1.md` |
| M19       | 2026-04-09    | [#20](https://github.com/m-cahill/starlab/pull/20) | `9e855329fc50f4f00db9c857f982d18ef93e4e65` | Cross-mode reconciliation audit (`observation_reconciliation_audit.json` / `observation_reconciliation_audit_report.json`); **green PR-head** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) on `1453eee…`; **green merge-push `main`** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) on `9e85532…`; see §18 / `M19_run1.md` |
| M20       | 2026-04-09    | [#21](https://github.com/m-cahill/starlab/pull/21) | `cf1bee980756b3b59d4db2620c041a23f14eba18` | Benchmark contract + scorecard schemas (`benchmark_contract_schema.json` / `benchmark_contract_schema_report.json` / `benchmark_scorecard_schema.json` / `benchmark_scorecard_schema_report.json`); **green PR-head** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) on `5c22336…`; **green merge-push `main`** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) on `cf1bee9…`; see §18 / `M20_run1.md` |
| M21       | 2026-04-09    | [#22](https://github.com/m-cahill/starlab/pull/22) | `092d00a8aff720a1df9cbb1beec1cbf661546953` | Scripted baseline suite (`scripted_baseline_suite.json` / `scripted_baseline_suite_report.json`); **green PR-head** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) on `818002e…`; **green merge-push `main`** [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) on `092d00a…`; superseded red PR-head [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) (Ruff format — **not** merge authority); see §18 / `M21_run1.md` |
| M22       | 2026-04-09    | [#23](https://github.com/m-cahill/starlab/pull/23) | `470afa84ff80a2d76fb2693bce3a4397e6526afe` | Heuristic baseline suite (`heuristic_baseline_suite.json` / `heuristic_baseline_suite_report.json`); **green PR-head** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) on `96aba18…`; **green merge-push `main`** [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) on `470afa8…`; see §18 / `M22_run1.md` |
| M23       | 2026-04-09    | [#24](https://github.com/m-cahill/starlab/pull/24) | `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252` | Evaluation tournament (`evaluation_tournament.json` / `evaluation_tournament_report.json`); **green PR-head** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) on `f00711a…`; **green merge-push `main`** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) on `b8857d2…`; see §18 / `M23_run1.md` |
| M24       | 2026-04-09    | [#27](https://github.com/m-cahill/starlab/pull/27) | `7b4d3b4603dc40fe2ade33e1c943a0efd40ca5a4` | Evaluation diagnostics (`evaluation_diagnostics.json` / `evaluation_diagnostics_report.json`); **green PR-head** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) on `5caf1fb…`; **green merge-push `main`** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) on `7b4d3b4…`; see §18 / `M24_run1.md` |
| M25       | 2026-04-09    | [#31](https://github.com/m-cahill/starlab/pull/31) | `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b` | Baseline evidence pack (`baseline_evidence_pack.json` / `baseline_evidence_pack_report.json`); **green PR-head** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on `b132bfd…`; **green merge-push `main`** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) on `f03c7bf…`; superseded red PR-head [`24215241322`](https://github.com/m-cahill/starlab/actions/runs/24215241322), [`24215286216`](https://github.com/m-cahill/starlab/actions/runs/24215286216) — **not** merge authority; see §18 / `M25_run1.md` |
| M26       | 2026-04-09    | [#32](https://github.com/m-cahill/starlab/pull/32) | `e83a8493a577c9013d720f1debab009dcf9c464f` | Replay training dataset (`replay_training_dataset.json` / `replay_training_dataset_report.json`); **green PR-head** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on `d8d3c4c…`; **green merge-push `main`** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) on `e83a849…`; see §18 / `M26_run1.md` |
| M27       | 2026-04-09    | [#33](https://github.com/m-cahill/starlab/pull/33) | `49b45825b65e56deb5cf991c5f74889e3daf2f59` | Replay imitation baseline (`replay_imitation_baseline.json` / `replay_imitation_baseline_report.json`); **green PR-head** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) on `65dcd2f…`; **green merge-push `main`** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) on `49b4582…`; superseded red PR-head [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) (Ruff format — **not** merge authority); see §18 / `M27_run1.md` |
| M28       | 2026-04-10    | [#34](https://github.com/m-cahill/starlab/pull/34) | `1ef636524269ff77ac26ac37584d43b50e9fcbc6` | Learned-agent evaluation harness (`learned_agent_evaluation.json` / `learned_agent_evaluation_report.json`); **green PR-head** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) on `c7ca6e6…`; **green merge-push `main`** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) on `1ef6365…`; see §18 / `M28_run1.md` |
| M29       | 2026-04-10    | [#35](https://github.com/m-cahill/starlab/pull/35) | `187d9ddd8e6b5234245923200c3a396d602e7b06` | Hierarchical agent interface (`hierarchical_agent_interface_schema.json` / `hierarchical_agent_interface_schema_report.json`); **green PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **green merge-push `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; superseded red PR-head [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) (Ruff format — **not** merge authority); see §18 / `M29_run1.md` |
| M30       | 2026-04-10    | [#36](https://github.com/m-cahill/starlab/pull/36) | `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf` | First learned hierarchical imitation agent (`replay_hierarchical_imitation_agent.json` / `replay_hierarchical_imitation_agent_report.json`); **green PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **green merge-push `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; superseded red PR-head: none recorded; see §18 / `M30_run1.md` |
| M31       | 2026-04-10    | [#37](https://github.com/m-cahill/starlab/pull/37) | `41d62056e1956627b63152221932dc9c2423429c` | Replay explorer / operator evidence surface (`replay_explorer_surface.json` / `replay_explorer_surface_report.json`); **green PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **green merge-push `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; superseded red PR-head: none recorded; see §18 / `M31_run1.md` |
| M32       | 2026-04-10    | [#38](https://github.com/m-cahill/starlab/pull/38) | `cf7219911a208da584537b4c08ab5811fa3f67de` | Audit closure I — coverage + JUnit CI artifacts, SHA-pinned actions, smoke/Makefile, clone-to-run docs, public deferred registry, arc M00–M37; **green PR-head** [`24228528798`](https://github.com/m-cahill/starlab/actions/runs/24228528798) on `0c3f6ce…`; **green merge-push `main`** [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230) on `cf72199…`; superseded red PR-head: none recorded; see §18 / `M32_run1.md` |
| M33       | 2026-04-10    | [#39](https://github.com/m-cahill/starlab/pull/39) | `975ac52fff206f9ceb1b0be66a0e7f1c7386a248` | Audit closure II — parallel CI tiers + `fieldtest-output` + architecture / operator / diligence docs + DIR-001/002/007; **green PR-head** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **green merge-push `main`** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; superseded green PR-head [`24231252478`](https://github.com/m-cahill/starlab/actions/runs/24231252478) on earlier tip — **not** final merge authority; superseded red PR-head: none recorded; see §18 / `M33_run1.md` |
| M34       | 2026-04-10    | [#40](https://github.com/m-cahill/starlab/pull/40) | `51e960d0c1c0eb20923836a8ac2400a59013bcc5` | Audit closure III — `starlab._io`, governance split, Dependabot, DIR-003–006, manual prep docs; **green PR-head** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **green merge-push `main`** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`; superseded **failure** PR-head [`24261032237`](https://github.com/m-cahill/starlab/actions/runs/24261032237) on `d1e92ae…` — **not** merge authority; see §18 / `M34_run1.md` |
| M35       | 2026-04-10    | [#46](https://github.com/m-cahill/starlab/pull/46) | `5b4d24b0eca578b70f2963f1561b99bc89fef033` | Audit closure IV — structural decoupling (`M14BundleLoader`, `parser_io`, `replay_slice_generation`, observation reconciliation), `load_json_object_strict`, ledger M00–M39; **green PR-head** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **green merge-push `main`** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) on `5b4d24b…`; superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015) (Ruff format), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) (Mypy) — **not** merge authority; see §18 / `M35_run1.md` |
| M36       | 2026-04-10    | [#47](https://github.com/m-cahill/starlab/pull/47) | `e73a53b28a4b6eeb3a2c19dd358d928c64806e89` | Audit closure V — `docs/starlab_archive.md` (verbatim **M01–M27** §7 notes), ledger §7 archival policy + governance-test consolidation; **green PR-head** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **green merge-push `main`** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; superseded PR-head: none recorded; see §18 / `M36_run1.md` |
| M37       | 2026-04-11    | [#48](https://github.com/m-cahill/starlab/pull/48) | `d2474bd365290a9c77f854b13d36a5ea1d8777cd` | Audit closure VI — coverage margin recovery, `fail_under` 78.0, `make check`, CI step summary; **green PR-head** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) on `a38d3a7…`; **green merge-push `main`** [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) on `d2474bd…`; superseded **failure** PR-head [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) — **not** merge authority; see §18 / `M37_run1.md` |
| M38       | 2026-04-11    | [#49](https://github.com/m-cahill/starlab/pull/49) | `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` | Audit closure VII — README + ledger quick-scan, governance tests, `runpy_helpers`; **green PR-head** [`24272425346`](https://github.com/m-cahill/starlab/actions/runs/24272425346) on `3e00641…`; **green merge-push `main`** [`24291882960`](https://github.com/m-cahill/starlab/actions/runs/24291882960) on `bf6bf4a…`; superseded PR-head: none; see §18 / `M38_run1.md` |
| M39       | 2026-04-11    | [#50](https://github.com/m-cahill/starlab/pull/50) | `ca97027cf1827942a25c886f04b5db56b8b9fe7b` | Public flagship proof pack (`starlab.flagship`, `make flagship`, CI **`flagship`** + **`flagship-proof-pack`**); **green PR-head** [`24292861437`](https://github.com/m-cahill/starlab/actions/runs/24292861437) on `2c3fce7…`; **green merge-push `main`** [`24293162871`](https://github.com/m-cahill/starlab/actions/runs/24293162871) on `ca97027…`; superseded PR-head: none; see §18 / `M39_run1.md` |
| M40       | 2026-04-12    | [#51](https://github.com/m-cahill/starlab/pull/51) | `44e8edc5bcce8dc99576bf2be542b273095e5072` | Agent training program charter (`starlab.training`, `agent_training_program_contract.json` / report); **green PR-head** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) on `be47d91…`; **green merge-push `main`** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) on `44e8edc…`; superseded PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) — Ruff format — **not** merge authority; see §18 / `M40_run1.md` |
| M41       | 2026-04-12    | [#52](https://github.com/m-cahill/starlab/pull/52) | `5e0add12dd8f4b3a9b4dd31023319cc1999f826b` | Replay-imitation training pipeline (`replay_imitation_training_run.json` / report; optional local weights not in repo); **green PR-head** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) on `7c092ed…`; **green merge-push `main`** [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) on `5e0add12…`; superseded PR-head runs on M41 branch — [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190), [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — **not** merge authority for final head; see §18 / `M41_run1.md` |
| M42       | 2026-04-12    | [#53](https://github.com/m-cahill/starlab/pull/53) | `3eb091aba832cb0a66066d6fca6db091eb53c8f5` | Learned-agent comparison harness (`learned_agent_comparison.json` / report); **green PR-head** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) on `191a955…`; **green merge-push `main`** [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) on `3eb091a…`; superseded PR-head: none; see §18 / `M42_run1.md` |
| M43       | 2026-04-12    | [#54](https://github.com/m-cahill/starlab/pull/54) | `8850e378a584c9821eeab3e8c72bc499d590b308` | Hierarchical training pipeline (`hierarchical_training_run.json` / report); **green PR-head** [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558) on `ffc4284…`; **green merge-push `main`** [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) on `8850e37…`; superseded PR-head runs on M43 branch — [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — **not** merge authority for final head; see §18 / `M43_run1.md` |
| M44       | 2026-04-12    | [#55](https://github.com/m-cahill/starlab/pull/55) | `1b1067ad632643d2b14da05d510a7c2a263cc8ea` | Local live-play validation harness (`local_live_play_validation_run.json` / report; `starlab.sc2`); **green PR-head** [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411) on `dc8e74d…`; **green merge-push `main`** [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) on `1b1067a…`; **superseded** **failure** PR-head [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) on `c8b989a…` — Ruff format — **not** merge authority; see §18 / `M44_run1.md` |
| M45       | 2026-04-12    | [#56](https://github.com/m-cahill/starlab/pull/56) | `1a585b68ea7413852ce78c220c6512bba6a004d7` | Self-play / RL bootstrap (`self_play_rl_bootstrap_run.json` / report; `starlab.training`); **green PR-head** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) on `0e89081…`; **green merge-push `main`** [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) on `1a585b6…`; **superseded** **failure** PR-head [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — Ruff format — **not** merge authority; see §18 / `M45_run1.md` |
| M46       | 2026-04-13    | [#57](https://github.com/m-cahill/starlab/pull/57) | `b925130d2e6bb9b2586139b17d100285e89b8e54` | Bounded live `final_status` / `sc2_game_result` (`starlab.sc2`); **green PR-head** [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005) on `ddb18f4…`; **merge-push `main`** [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) on `b925130…` — **failure** (`pip-audit`); **repaired green `main`** [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) on `1b7b25e…` (pytest bump); tag **`v0.0.46-m46`**; **post-closeout `main`** [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) on `1b33acd…` — **success**; see §18 / `M46_run1.md` |
| M47       | 2026-04-14    | [#58](https://github.com/m-cahill/starlab/pull/58) | `ebc5de0864ef6231d13efa741150d73c1ef1b98b` | Bootstrap episode distinctness / operator ergonomics (`starlab.training`); **green PR-head** [`24374720293`](https://github.com/m-cahill/starlab/actions/runs/24374720293) on `4a8fb3e…`; **merge-push `main`** [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on `ebc5de0…` — **success**; tag **`v0.0.47-m47`**; branch `m47-bootstrap-episode-distinctness-ergonomics` **retained**; see §18 / `M47_run1.md` |
| M48       | 2026-04-14    | [#59](https://github.com/m-cahill/starlab/pull/59) | `cdd023cb388ae99c3649978857e07af04c17df50` | Learned-agent comparison contract-path alignment (`--benchmark-contract`, `--training-program-contract`, M41↔M40 identity check); **green PR-head** [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299) on `d94bc02…`; **merge-push `main`** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on `cdd023c…` — **success**; tag **`v0.0.48-m48`**; branch `m48-learned-agent-comparison-contract-path-alignment` **deleted**; see §18 / `M48_run1.md` |
| M49       | 2026-04-14    | [#60](https://github.com/m-cahill/starlab/pull/60) | `cad5f2b4ad2a1ef01530efa35d996f513795b0ed` | Full local training / bootstrap campaign charter + preflight (`out/training_campaigns/` contract layout; **not** long-run execution proof); **green PR-head** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623) on `2780de1…`; **merge-push `main`** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) on `cad5f2b…` — **success**; superseded **failure** PR-head [`24381216946`](https://github.com/m-cahill/starlab/actions/runs/24381216946), [`24381253831`](https://github.com/m-cahill/starlab/actions/runs/24381253831) — **not** merge authority; tag **`v0.0.49-m49`**; branch `m49-full-local-training-campaign-charter` **deleted**; see §18 / `M49_run1.md` |
| M50       | 2026-04-14    | [#61](https://github.com/m-cahill/starlab/pull/61) | `a0430d3cd79b23d04c81cca1e11a404f50c4c35b` | Industrial-scale hidden rollout + governed campaign execution (executor, locks, honest visibility, extended preflight); **green PR-head** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763) on `a6f0b90…`; **merge-push `main`** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) on `a0430d3…` — **success**; tag **`v0.0.50-m50`**; branch `m50-industrial-hidden-rollout-mode` **retained**; see §18 / `M50_run1.md` |
| M51       | 2026-04-15    | [#62](https://github.com/m-cahill/starlab/pull/62) | `1e88466eb2635385b7ad56e666c45436a12f0b59` | Governed post-bootstrap phase orchestration (`--post-bootstrap-protocol-phases`, phase receipts, `hidden_rollout_campaign_run` v2); **green PR-head** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222) on `f812f80…`; **merge-push `main`** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on `1e88466…` — **success**; tag **`v0.0.51-m51`**; branch `m51-governed-post-bootstrap-phase-orchestration` **deleted**; see §18 / `M51_run1.md` |
| M52       | 2026-04-15    | [#63](https://github.com/m-cahill/starlab/pull/63) | `c80a47bedcc5e607e45381d401411d9aa5e2f10b` | V1 endgame recharter + replay↔execution equivalence charter v1 (`docs/runtime/replay_execution_equivalence_charter_v1.md`, `starlab.equivalence`); **green PR-head** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983) on `11ba11e…`; **merge-push `main`** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on `c80a47b…` — **success**; superseded **failure** PR-head [`24434871264`](https://github.com/m-cahill/starlab/actions/runs/24434871264) on `a938ac6…` — Ruff format — **not** merge authority; tag **`v0.0.52-m52`**; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted**; see §18 / `M52_run1.md` |
| M53       | 2026-04-15    | [#64](https://github.com/m-cahill/starlab/pull/64) | `99bd43da41ac5a4d22a3eb2f438bc8ebe93b591d` | Replay↔execution equivalence evidence surface v1 (`replay_execution_equivalence_evidence.json` / report; profile `starlab.m53.profile.identity_binding_v1`; explicit artifact-path CLI); **green PR-head** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924) on `ec166ff…`; **merge-push `main`** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on `99bd43d…` — **success**; tag **`v0.0.53-m53`**; branch `m53-replay-execution-equivalence-evidence-surface` **deleted**; see §18 / `M53_run1.md` — **evidence surface only**; **not** universal equivalence; **not** M54 audit gates |
| M54       | 2026-04-15    | [#65](https://github.com/m-cahill/starlab/pull/65) | `773dd1982f28f92512785ce0ab349b7c625f4c3d` | Replay↔execution equivalence audit & acceptance gates v1 (`replay_execution_equivalence_audit.json` / report; gate pack `starlab.m54.gatepack.identity_binding_acceptance_v1`, profile-scoped outcomes only); **green PR-head** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561) on `70f4f2d…`; **merge-push `main`** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on `773dd19…` — **success**; tag **`v0.0.54-m54`**; branch `m54-replay-execution-equivalence-audit-acceptance-gates` **deleted**; see §18 / `M54_run1.md` — **bounded audit over M53 evidence**; **not** universal equivalence; **not** benchmark integrity; **not** branch protection |
| M55       | 2026-04-15    | [#66](https://github.com/m-cahill/starlab/pull/66) | `625dd756f09ceb4aebe8d5f3c60ea216f9cab98e` | Benchmark integrity charter & split-governance controls v1 (`starlab.benchmark_integrity_charter.v1`, deterministic charter/report JSON); **green PR-head** [`24472349322`](https://github.com/m-cahill/starlab/actions/runs/24472349322) on `f7b1306…`; **merge-push `main`** [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on `625dd75…` — **success**; superseded **failure** PR-head [`24472253485`](https://github.com/m-cahill/starlab/actions/runs/24472253485) — Ruff format — **not** merge authority; tag **`v0.0.55-m55`**; branch `m55-benchmark-integrity-charter-split-governance-controls` **retained**; see §18 / `M55_run1.md` — **charter-only**; **not** benchmark integrity proved; **not** M56 gates |
| M56       | 2026-04-15    | [#67](https://github.com/m-cahill/starlab/pull/67) | `bd7da9a6229fa067217dd04db918972a5ec73caf` | Benchmark integrity evidence & reproducibility gates v1 (bounded scope `starlab.m56.scope.fixture_only_baseline_chain_v1` + gate pack `starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`; deterministic evidence + gates JSON); **green PR-head** [`24474743293`](https://github.com/m-cahill/starlab/actions/runs/24474743293) on `2c5d23b…`; **merge-push `main`** [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843) on `bd7da9a…` — **success**; superseded **failure** PR-head [`24474659745`](https://github.com/m-cahill/starlab/actions/runs/24474659745) — Ruff format — **not** merge authority; tag **`v0.0.56-m56`**; branch `m56-benchmark-integrity-evidence-reproducibility-gates` **retained**; see §18 / `M56_run1.md` — **not** global benchmark integrity proof; **not** M52–M54 equivalence substitute |
| M57       | 2026-04-15    | [#68](https://github.com/m-cahill/starlab/pull/68) | `29c383f85f380d2eb2a6b2a411aa7c3262f2bc0d` | Narrow live SC2 in CI charter & controlled runner v1 (`starlab.sc2` charter + controlled-runner receipt wrapping **M44**; profile `starlab.m57.runner_profile.m44_single_validation_v1`; optional `workflow_dispatch` workflow); **green PR-head** [`24479060243`](https://github.com/m-cahill/starlab/actions/runs/24479060243) on `eaff010…`; **merge-push `main`** [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on `29c383f…` — **success**; tag **`v0.0.57-m57`**; branch `m57-live-sc2-in-ci-charter-controlled-runner` **retained**; see §18 / `M57_run1.md` — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof; **not** M52–M54 equivalence substitute |
| M58       | 2026-04-16    | [#69](https://github.com/m-cahill/starlab/pull/69) | `3a6f13910dc8056cb0d88161796dd5fe7888629d` | Live SC2 in CI hardening & cost guardrails v1 (guardrails + preflight JSON; **one** guardrail profile `starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1`; hardened optional `workflow_dispatch` workflow); **green PR-head** [`24485185914`](https://github.com/m-cahill/starlab/actions/runs/24485185914) on `4d8fa3e…`; **merge-push `main`** [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247) on `3a6f139…` — **success**; tag **`v0.0.58-m58`**; branch `m58-live-sc2-in-ci-hardening-cost-guardrails` **retained**; see §18 / `M58_run1.md` — **bounded M57 hardening**; **not** global live-SC2-in-CI proof; **not** ladder/public **performance** (**M59** is the separate bounded descriptive layer) |
| M59       | 2026-04-16    | [#70](https://github.com/m-cahill/starlab/pull/70) | `319bc3d496b78c573c57991cd0fcc461219da6a4` | Ladder/public evaluation protocol & evidence surface v1 (`starlab.sc2` protocol + evidence JSON; runtime `ladder_public_evaluation_protocol_evidence_surface_v1.md`); **green PR-head** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360) on `074598a…`; **merge-push `main`** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on `319bc3d…` — **success**; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority; tag **`v0.0.59-m59`**; branch `m59-ladder-public-evaluation-protocol-evidence-surface-v1` **deleted**; see §18 / `M59_run1.md` — **descriptive packaging only**; **not** ladder strength; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion |
| M60       | 2026-04-16    | [#71](https://github.com/m-cahill/starlab/pull/71) | `9ef4e049f1e04ee36952be53647d48c649ad6915` | Audit hardening & v2 readiness v1 (`docs/audit/m60_v2_readiness_findings.md`; `docs/runtime/v2_readiness_audit_hardening_v1.md`; private `starlab.training._full_local_training_campaign_execution`; `tests/test_m60_v2_readiness_guardrails.py`); **green PR-head** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150) on `c7f6156…`; **merge-push `main`** [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939) on `9ef4e04…` — **success**; tag **`v0.0.60-m60`**; branch `m60-audit-hardening-v2-readiness` **deleted**; see §18 / `M60_run1.md` — **structural/diligence**; **not** new governed product artifact family; **not** equivalence/benchmark/ladder/live-SC2 claims |
| M61       | 2026-04-16    | [#72](https://github.com/m-cahill/starlab/pull/72) | `35d7734d14113adf206390f153f517a93d7d41ba` | SC2 foundation release lock & v1 proof pack (`starlab.release_lock` proof pack + audit emitters; `docs/runtime/sc2_foundation_release_lock_v1.md`); operator-local campaign **`m61_evidence_2026_04_16_a`** / **`m61_exec_001`** with **`ready_within_scope`**; **green PR-head** [`24493016581`](https://github.com/m-cahill/starlab/actions/runs/24493016581); **merge-push `main`** [`24493963087`](https://github.com/m-cahill/starlab/actions/runs/24493963087) on `35d7734…` — **success**; tag **`v0.0.61-m61`**; branch `m61-sc2-foundation-release-lock-v1` **retained**; see §18 / `M61_run1.md` — **bounded within-scope release lock**; **not** global benchmark integrity; **not** universal equivalence; **not** merge-gate live SC2; **not** ladder/public performance |

**M61 merge:** [PR #72](https://github.com/m-cahill/starlab/pull/72) merged **2026-04-16** (UTC `2026-04-16T05:33:27Z`) via **merge commit** `35d7734d14113adf206390f153f517a93d7d41ba`. Remote branch `m61-sc2-foundation-release-lock-v1` was **retained** on `origin`. Final PR head before merge: `bb5a216e83f6048cfa0ad9b437d74d367ff59a5b`.

**M61 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `bb5a216…` | `24493016581` | success | https://github.com/m-cahill/starlab/actions/runs/24493016581 |

**Authoritative green PR-head CI:** [`24493016581`](https://github.com/m-cahill/starlab/actions/runs/24493016581) — **success** on final tip `bb5a216…`.

**M61 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M61 merge (`35d7734…`) | `24493963087` | success | https://github.com/m-cahill/starlab/actions/runs/24493963087 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Annotated tag push **`v0.0.61-m61`** is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority.*

**M61 milestone artifacts:** `docs/company_secrets/milestones/M61/` (`M61_plan.md`, `M61_toolcalls.md`, `M61_run1.md`, `M61_summary.md`, `M61_audit.md`, etc.) — **local only** — **not** committed.

**M60 merge:** [PR #71](https://github.com/m-cahill/starlab/pull/71) merged **2026-04-16** (UTC `2026-04-16T03:57:51Z`) via **merge commit** `9ef4e049f1e04ee36952be53647d48c649ad6915`. Remote branch `m60-audit-hardening-v2-readiness` was **deleted** after merge. Final PR head before merge: `c7f615639bc1b26d6d2813bc55f078a048cab405`.

**M60 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `c7f6156…` | `24491193150` | success | https://github.com/m-cahill/starlab/actions/runs/24491193150 |

**Authoritative green PR-head CI:** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150) — **success** on final tip `c7f6156…`.

**M60 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M60 merge (`9ef4e04…`) | `24491232939` | success | https://github.com/m-cahill/starlab/actions/runs/24491232939 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Annotated tag push **`v0.0.60-m60`** is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority.*

**M60 milestone artifacts:** `docs/company_secrets/milestones/M60/` (`M60_plan.md`, `M60_toolcalls.md`, `M60_run1.md`, `M60_summary.md`, `M60_audit.md`, etc.) — **local only** — **not** committed.

**M00 PR head (pre-merge):** `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91`

**M00 CI evidence (authoritative)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| PR #1 head | `24015581129` | success | https://github.com/m-cahill/starlab/actions/runs/24015581129 |
| `main` after merge (`f9203dd…`) | `24015599413` | success | https://github.com/m-cahill/starlab/actions/runs/24015599413 |
| `main` after M00 evidence finalization (`523993e…`) | `24015634285` | success | https://github.com/m-cahill/starlab/actions/runs/24015634285 |

**M00 milestone artifacts:** `docs/company_secrets/milestones/M00/` (`M00_summary.md`, `M00_audit.md`, `M00_run1.md`, etc.) — **local only** — **not** in a default clone (gitignored).

**M01 merge:** [PR #2](https://github.com/m-cahill/starlab/pull/2) merged **2026-04-06** (UTC `2026-04-06T20:26:27Z`) via **merge commit** `4a916033f55c6b8c4a582f985233a64ca039ead3`. Remote branch `m01-sc2-runtime-surface-env-lock` was **deleted** after merge.

**M01 CI evidence (PR-head runs witnessed before merge)**

Each row is a green `pull_request` run on branch `m01-sc2-runtime-surface-env-lock` at the listed commit (historical record).

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `378c864…` | `24048416111` | success | https://github.com/m-cahill/starlab/actions/runs/24048416111 |
| `260c4e0…` | `24048498203` | success | https://github.com/m-cahill/starlab/actions/runs/24048498203 |
| `88b06db…` | `24048576545` | success | https://github.com/m-cahill/starlab/actions/runs/24048576545 |

Further commits on the PR after `88b06db…` had additional green PR-head runs on GitHub before the final merge tip.

**M01 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M01 merge (`4a91603…`) | `24049637412` | success | https://github.com/m-cahill/starlab/actions/runs/24049637412 |
| `main` after M01 merge closeout / ledger update (`c920876…`) | `24049868109` | success | https://github.com/m-cahill/starlab/actions/runs/24049868109 |
| `main` after M01 §18 / `M01_run1` post-merge alignment (`aa46fc4…`) | `24049956985` | success | https://github.com/m-cahill/starlab/actions/runs/24049956985 |

*Later documentation-only pushes to `main` re-run CI; additional green runs after the rows above are not milestone events — the merge boundary for M01 remains PR #2 merge commit `4a91603…`.*

*Additional follow-up (ledger commit recording run 3):* `main` @ `8251cef…` — workflow run `24049998835` (success): https://github.com/m-cahill/starlab/actions/runs/24049998835

**M01 milestone artifacts:** `docs/company_secrets/milestones/M01/` (`M01_plan.md`, `M01_toolcalls.md`, `M01_run1.md`, `M01_summary.md`, `M01_audit.md`, optional redacted probe sample, etc.) — **local only** — **not** in a default clone (gitignored).

**M02 merge:** [PR #3](https://github.com/m-cahill/starlab/pull/3) merged **2026-04-06** (UTC `2026-04-06T23:35:21Z`) via **merge commit** `53a24a4a6106168afe79e0a70d51a20bfef4ea18`. Remote branch `m02-deterministic-match-execution-harness` was **deleted** after merge. Final PR head before merge: `e88ca20424410cd99f834eeec92a5ec5d8034284`.

**M02 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `e88ca20…` | `24055678613` | success | https://github.com/m-cahill/starlab/actions/runs/24055678613 |

**M02 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M02 merge (`53a24a4…`) | `24056523452` | success | https://github.com/m-cahill/starlab/actions/runs/24056523452 |

*M02 closeout documentation push:* `main` @ `d81a0952335cbc93d2144da1c428a42287561793` — workflow run `24056595358` (success): https://github.com/m-cahill/starlab/actions/runs/24056595358

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 if they record ledger-only updates.*

**M02 milestone artifacts:** `docs/company_secrets/milestones/M02/` (`M02_plan.md`, `M02_toolcalls.md`, `M02_run1.md`, `M02_summary.md`, `M02_audit.md`, `M02_local_execution_note.md`, `M02_determinism_check.md`, `M02_execution_proof_redacted.json`, `m02_local_config.json`, etc.)

**M03 merge:** [PR #4](https://github.com/m-cahill/starlab/pull/4) merged **2026-04-07** (UTC `2026-04-07T01:10:32Z`) via **merge commit** `6bfe6a7b32a004f62a491bf31573e12cd211118a`. Remote branch `m03-run-identity-lineage-seed` was **deleted** after merge. Final PR head before merge: `884055c34b78f182c704df5a10a9eced5515fa78`.

**M03 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `884055c…` | `24059095399` | success | https://github.com/m-cahill/starlab/actions/runs/24059095399 |

**M03 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M03 merge (`6bfe6a7…`) | `24059246337` | success | https://github.com/m-cahill/starlab/actions/runs/24059246337 |
| `main` after M03 closeout / ledger + M04 stubs (`43d99f6…`) | `24059294330` | success | https://github.com/m-cahill/starlab/actions/runs/24059294330 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23.*

**M03 milestone artifacts:** `docs/company_secrets/milestones/M03/` (`M03_plan.md`, `M03_toolcalls.md`, `M03_run1.md`, `M03_summary.md`, `M03_audit.md`, etc.)

**M04 merge:** [PR #5](https://github.com/m-cahill/starlab/pull/5) merged **2026-04-07** (UTC `2026-04-07T02:17:04Z`) via **merge commit** `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed`. Remote branch `m04-replay-binding-to-run-identity` was **deleted** after merge. Final PR head before merge: `6991978cb35172edda75f721149b1558d7ead226`.

**M04 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6991978…` | `24060734950` | success | https://github.com/m-cahill/starlab/actions/runs/24060734950 |

**M04 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M04 merge (`c38de5d…`) | `24060997255` | success | https://github.com/m-cahill/starlab/actions/runs/24060997255 |
| `main` after M04 closeout / ledger + M05 stubs (`c099752…`) | `24061285459` | success | https://github.com/m-cahill/starlab/actions/runs/24061285459 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23.*

**M04 milestone artifacts:** `docs/company_secrets/milestones/M04/` (`M04_plan.md`, `M04_toolcalls.md`, `M04_run1.md`, `M04_summary.md`, `M04_audit.md`, etc.)

**M05 merge:** [PR #6](https://github.com/m-cahill/starlab/pull/6) merged **2026-04-07** (UTC `2026-04-07T03:20:10Z`) via **merge commit** `bad27db36c135fd772e38dcafa64d6fa59577db0`. Remote branch `m05-canonical-run-artifact-v0` was **deleted** after merge. Final PR head before merge: `53ace08e2ec9d29c780f31593bd945e82e1dfcac`.

**M05 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `53ace08…` | `24062592376` | success | https://github.com/m-cahill/starlab/actions/runs/24062592376 |

**M05 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M05 merge (`bad27db…`) | `24062610358` | success | https://github.com/m-cahill/starlab/actions/runs/24062610358 |
| `main` after M05 closeout / ledger + M06 stubs (`6edeb8a…`) | `24062664914` | success | https://github.com/m-cahill/starlab/actions/runs/24062664914 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs (e.g. ledger cross-reference update `ebca1e9…` — run `24062700534`); distinguish them in §23 — **not** merge-boundary events.*

**M05 milestone artifacts:** `docs/company_secrets/milestones/M05/` (`M05_plan.md`, `M05_toolcalls.md`, `M05_run1.md`, `M05_summary.md`, `M05_audit.md`, etc.)

**M06 merge:** [PR #7](https://github.com/m-cahill/starlab/pull/7) merged **2026-04-07** (UTC `2026-04-07T04:26:10Z`) via **merge commit** `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a`. Remote branch `m06-environment-drift-runtime-smoke-matrix` was **deleted** after merge. Final PR head before merge: `6f9ef463f90abe914f3c98c8977d49f8da0102cb`.

**M06 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6f9ef46…` | `24064200725` | success | https://github.com/m-cahill/starlab/actions/runs/24064200725 |

**Superseded (not merge authority):** earlier PR-head run `24064181198` failed at **Ruff format** — fixed on tip `6f9ef46…`.

**M06 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M06 merge (`4953d7a…`) | `24064229874` | success | https://github.com/m-cahill/starlab/actions/runs/24064229874 |

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary events unless they record ledger closeout for M06.*

**M06 milestone artifacts:** `docs/company_secrets/milestones/M06/` (`M06_plan.md`, `M06_toolcalls.md`, `M06_run1.md`, `M06_summary.md`, `M06_audit.md`, etc.)

**M07 merge:** [PR #8](https://github.com/m-cahill/starlab/pull/8) merged **2026-04-07** (UTC `2026-04-07T05:50:09Z`) via **merge commit** `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`. Remote branch `m07-replay-intake-policy-provenance-enforcement` was **deleted** after merge. Final PR head before merge: `a5188ad88bab688ab40136dea77a8b4d3caa0495`.

**M07 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `a5188ad…` | `24065819186` | success | https://github.com/m-cahill/starlab/actions/runs/24065819186 |

**M07 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M07 merge (`1c7bb0c…`) | `24066550699` | success | https://github.com/m-cahill/starlab/actions/runs/24066550699 |
| `main` after M07 closeout docs (`2ccac7e…`) | `24066606427` | success | https://github.com/m-cahill/starlab/actions/runs/24066606427 |
| `main` after M07 doc CI cross-reference (`20a1870…`) | `24066644075` | success | https://github.com/m-cahill/starlab/actions/runs/24066644075 |

*Rows `24066606427` and `24066644075` are **ledger / documentation only** — **not** merge-boundary events. Merge-boundary post-merge `main` CI for M07 remains `24066550699` on merge commit `1c7bb0c…`.*

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M07 milestone artifacts:** `docs/company_secrets/milestones/M07/` (`M07_plan.md`, `M07_toolcalls.md`, `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, etc.)

**M08 merge:** [PR #9](https://github.com/m-cahill/starlab/pull/9) merged **2026-04-07** (UTC `2026-04-07T07:52:12Z`) via **merge commit** `b99233e807177d65737beaba5246efa67a3edce2`. Remote branch `m08-replay-parser-substrate` was **deleted** after merge. Final PR head before merge: `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`.

**M08 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `a65fabf…` | `24069974048` | success | https://github.com/m-cahill/starlab/actions/runs/24069974048 |

**Superseded (not merge authority):** [`24069652969`](https://github.com/m-cahill/starlab/actions/runs/24069652969) — **failure** at Pytest (M05 golden vs Linux replay hash — CRLF/LF); fixed before final tip.

**M08 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M08 merge (`b99233e…`) | `24070602968` | success | https://github.com/m-cahill/starlab/actions/runs/24070602968 |
| `main` after M08 closeout docs (`a089f18…`) | `24070704576` | failure | https://github.com/m-cahill/starlab/actions/runs/24070704576 |
| `main` after M08 governance test fix (`c3b6f2c…`) | `24070774045` | success | https://github.com/m-cahill/starlab/actions/runs/24070774045 |
| `main` after M08 ledger CI record sync (`1cca021…`) | `24070813310` | success | https://github.com/m-cahill/starlab/actions/runs/24070813310 |

*Rows `24070704576`, `24070774045`, and `24070813310` are **not** merge-boundary events — closeout documentation + governance test alignment + ledger CI hygiene after M08 merge. **Authoritative** merge-boundary post-merge `main` CI for M08 remains `24070602968` on merge commit `b99233e…`.*

*Further documentation-only pushes to `main` after these rows may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M08 milestone artifacts:** `docs/company_secrets/milestones/M08/` (`M08_plan.md`, `M08_toolcalls.md`, `M08_run1.md`, `M08_summary.md`, `M08_audit.md`, etc.)

**M09 merge:** [PR #10](https://github.com/m-cahill/starlab/pull/10) merged **2026-04-07** (UTC `2026-04-07T20:05:59Z`) via **merge commit** `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`. Remote branch `m09-replay-metadata-extraction` was **deleted** after merge. Final PR head before merge: `3f161dea12a9b7ffb6dbe01c73b01f351a7219da`.

**M09 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `3f161de…` | `24101861888` | success | https://github.com/m-cahill/starlab/actions/runs/24101861888 |

**Superseded PR-head runs:** none observed for the final merge tip — single green `pull_request` run at `3f161de…` is merge authority.

**M09 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M09 merge (`fc9b442…`) | `24101900950` | success | https://github.com/m-cahill/starlab/actions/runs/24101900950 |

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M09 milestone artifacts:** `docs/company_secrets/milestones/M09/` (`M09_plan.md`, `M09_toolcalls.md`, `M09_run1.md`, `M09_summary.md`, `M09_audit.md`, etc.)

**M10 merge:** [PR #11](https://github.com/m-cahill/starlab/pull/11) merged **2026-04-07** (UTC `2026-04-07T20:58:46Z`) via **merge commit** `cb3e581f70f85653477081eb1ef4772229f05983`. Remote branch `m10-timeline-event-extraction` was **deleted** after merge. Final PR head before merge: `cb066fe3f09b07f3390e85928c88f65a6e75cd6f`.

**M10 CI evidence (PR-head run — merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `cb066fe…` | `24104110934` | cancelled | https://github.com/m-cahill/starlab/actions/runs/24104110934 |

**Authoritative green PR-head CI:** **none** — the only witnessed `pull_request` run on the final merge tip was **cancelled** (merge landed while the workflow was starting).

**M10 CI evidence (post-merge `main`)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M10 merge (`cb3e581…`) | `24104111851` | failure | https://github.com/m-cahill/starlab/actions/runs/24104111851 |
| `main` after M10 Mypy repair (`cf2074e…`) | `24104197912` | success | https://github.com/m-cahill/starlab/actions/runs/24104197912 |

*Merge-push on `cb3e581…` failed **Mypy**; **authoritative green `main`** for current governance is **`24104197912`** on `cf2074e…` (repair — **not** a merge-boundary event). Further documentation-only pushes after closeout may produce additional green runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only churn per closeout hygiene.*

**M10 milestone artifacts:** `docs/company_secrets/milestones/M10/` (`M10_plan.md`, `M10_toolcalls.md`, `M10_run1.md`, `M10_summary.md`, `M10_audit.md`, etc.)

**M11 merge:** [PR #12](https://github.com/m-cahill/starlab/pull/12) merged **2026-04-07** (UTC `2026-04-07T21:49:23Z`) via **merge commit** `38c15302badd49966b17f9195ddb139f6ae9a9b4`. Remote branch `m11-build-order-economy-plane` was **deleted** after merge. Final PR head before merge: `88ce7f9615c6c462b76674e1afb0734fc3dcc5be`.

**M11 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `88ce7f9…` | `24106029320` | success | https://github.com/m-cahill/starlab/actions/runs/24106029320 |

**Authoritative green PR-head CI:** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) — **success** on final tip `88ce7f9…` (contrast M10 cancelled merge-gate run).

**M11 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M11 merge (`38c1530…`) | `24106124347` | success | https://github.com/m-cahill/starlab/actions/runs/24106124347 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M11 milestone artifacts:** `docs/company_secrets/milestones/M11/` (`M11_plan.md`, `M11_toolcalls.md`, `M11_run1.md`, `M11_summary.md`, `M11_audit.md`, etc.)

**M12 merge:** [PR #13](https://github.com/m-cahill/starlab/pull/13) merged **2026-04-07** (UTC `2026-04-07T23:23:48Z`) via **merge commit** `78528958a616177b564e603c193fb0d7f8af734e`. Remote branch `m12-combat-scouting-visibility-windows` was **deleted** after merge. Final PR head before merge: `59adce3422a840692a4961278c995c5029da43bb`.

**M12 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `59adce3…` | `24109242392` | success | https://github.com/m-cahill/starlab/actions/runs/24109242392 |

**Authoritative green PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) — **success** on final tip `59adce3…`.

**M12 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M12 merge (`7852895…`) | `24109269513` | success | https://github.com/m-cahill/starlab/actions/runs/24109269513 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M12 milestone artifacts:** `docs/company_secrets/milestones/M12/` (`M12_plan.md`, `M12_toolcalls.md`, `M12_run1.md`, `M12_summary.md`, `M12_audit.md`, etc.)

**M13 merge:** [PR #14](https://github.com/m-cahill/starlab/pull/14) merged **2026-04-08** (UTC `2026-04-08T01:20:38Z`) via **merge commit** `f86e36837e81b8552639c5a885a13a773b96215c`. Remote branch `m13-replay-slice-generator` was **deleted** after merge. Final PR head before merge: `6231b19cd7067130fd3324dcd3070172333ba766`.

**M13 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `6231b19…` | `24112526047` | success | https://github.com/m-cahill/starlab/actions/runs/24112526047 |

**Authoritative green PR-head CI:** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) — **success** on final tip `6231b19…`.

**M13 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M13 merge (`f86e368…`) | `24112556177` | success | https://github.com/m-cahill/starlab/actions/runs/24112556177 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M13 milestone artifacts:** `docs/company_secrets/milestones/M13/` (`M13_plan.md`, `M13_toolcalls.md`, `M13_run1.md`, `M13_summary.md`, `M13_audit.md`, etc.)

**M14 merge:** [PR #15](https://github.com/m-cahill/starlab/pull/15) merged **2026-04-08** (UTC `2026-04-08T05:00:41Z`) via **merge commit** `8a0439a9a2970a74f3a5087390fc080f02852246`. Remote branch `m14-replay-bundle-lineage-contract-v1` was **deleted** after merge. Final PR head before merge: `42e29f2a64fa4672dbd2df435a04836c379b5258`.

**M14 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `42e29f2…` | `24118622373` | success | https://github.com/m-cahill/starlab/actions/runs/24118622373 |

**Authoritative green PR-head CI:** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) — **success** on final tip `42e29f2…`.

**M14 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M14 merge (`8a0439a…`) | `24118654909` | success | https://github.com/m-cahill/starlab/actions/runs/24118654909 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M14 milestone artifacts:** `docs/company_secrets/milestones/M14/` (`M14_plan.md`, `M14_toolcalls.md`, `M14_run1.md`, `M14_summary.md`, `M14_audit.md`, etc.)

**M15 merge:** [PR #16](https://github.com/m-cahill/starlab/pull/16) merged **2026-04-08** (UTC `2026-04-08T06:51:06Z`) via **merge commit** `b0f7132a54508f35d54406011cd3b37bce776927`. Remote branch `m15-canonical-state-schema-v1` was **deleted** after merge. Final PR head before merge: `abc8ffcd223536568fcf134b1e21273915cf1d4d`.

**M15 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `abc8ffc…` | `24122064141` | success | https://github.com/m-cahill/starlab/actions/runs/24122064141 |

**Authoritative green PR-head CI:** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) — **success** on final tip `abc8ffc…`.

**Superseded (not merge authority):** [`24121376545`](https://github.com/m-cahill/starlab/actions/runs/24121376545) — **failure** at **Mypy** (`import-untyped` for `jsonschema`); fixed on tip `abc8ffc…` with `types-jsonschema`.

**M15 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M15 merge (`b0f7132…`) | `24122092800` | success | https://github.com/m-cahill/starlab/actions/runs/24122092800 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M15 milestone artifacts:** `docs/company_secrets/milestones/M15/` (`M15_plan.md`, `M15_toolcalls.md`, `M15_run1.md`, `M15_summary.md`, `M15_audit.md`, etc.)

**M21 merge:** [PR #22](https://github.com/m-cahill/starlab/pull/22) merged **2026-04-09** (UTC `2026-04-09T05:41:36Z`) via **merge commit** `092d00a8aff720a1df9cbb1beec1cbf661546953`. Remote branch `m21-scripted-baseline-suite` was **deleted** after merge. Final PR head before merge: `818002e56b512e504c27f12aba8a39bc73627c82`.

**M21 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `818002e…` | `24174468912` | success | https://github.com/m-cahill/starlab/actions/runs/24174468912 |

**Authoritative green PR-head CI:** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) — **success** on final tip `818002e…`.

**Superseded (not merge authority):** [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) — **failure** at **Ruff format check**; fixed on tip `818002e…`.

**M21 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M21 merge (`092d00a…`) | `24174498486` | success | https://github.com/m-cahill/starlab/actions/runs/24174498486 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M21 milestone artifacts:** `docs/company_secrets/milestones/M21/` (`M21_plan.md`, `M21_toolcalls.md`, `M21_run1.md`, `M21_summary.md`, `M21_audit.md`, etc.)

**M22 merge:** [PR #23](https://github.com/m-cahill/starlab/pull/23) merged **2026-04-09** (UTC `2026-04-09T06:50:36Z`) via **merge commit** `470afa84ff80a2d76fb2693bce3a4397e6526afe`. Remote branch `m22-heuristic-baseline-suite` was **deleted** after merge. Final PR head before merge: `96aba181f725b1303d54779d48556b7dffd7feb4`.

**M22 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `96aba18…` | `24176685407` | success | https://github.com/m-cahill/starlab/actions/runs/24176685407 |

**Authoritative green PR-head CI:** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) — **success** on final tip `96aba18…`.

**M22 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M22 merge (`470afa8…`) | `24176717132` | success | https://github.com/m-cahill/starlab/actions/runs/24176717132 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M22 milestone artifacts:** `docs/company_secrets/milestones/M22/` (`M22_plan.md`, `M22_toolcalls.md`, `M22_run1.md`, `M22_summary.md`, `M22_audit.md`, etc.)

**M23 merge:** [PR #24](https://github.com/m-cahill/starlab/pull/24) merged **2026-04-09** (UTC `2026-04-09T07:41:53Z`) via **merge commit** `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`. Remote branch `m23-evaluation-runner-tournament-harness` was **deleted** after merge. Final PR head before merge: `f00711a3a2c16573f31492398de59387fe284711`.

**M23 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `f00711a…` | `24178571859` | success | https://github.com/m-cahill/starlab/actions/runs/24178571859 |

**Authoritative green PR-head CI:** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) — **success** on final tip `f00711a…`.

**M23 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M23 merge (`b8857d2…`) | `24178615940` | success | https://github.com/m-cahill/starlab/actions/runs/24178615940 |
| `main` after M23 milestone closeout ([PR #25](https://github.com/m-cahill/starlab/pull/25)) (`317b3a0…`) | `24178745007` | success | https://github.com/m-cahill/starlab/actions/runs/24178745007 |

*Row `24178745007` is **milestone documentation / governance alignment** — **not** merge-boundary product evidence for M23. **Authoritative** M23 product merge remains PR-head [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) + merge-boundary [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) ([PR #24](https://github.com/m-cahill/starlab/pull/24)).*

*Closeout / ledger documentation pushes after these rows may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M23 milestone artifacts:** `docs/company_secrets/milestones/M23/` (`M23_plan.md`, `M23_toolcalls.md`, `M23_run1.md`, `M23_summary.md`, `M23_audit.md`, etc.)

**M24 merge:** [PR #27](https://github.com/m-cahill/starlab/pull/27) merged **2026-04-09** (UTC `2026-04-09T21:00:08Z`) via **merge commit** `7b4d3b4603dc40fe2ade33e1c943a0efd40ca5a4`. Remote branch `m24-evaluation-diagnostics-failure-views` was **deleted** after merge. Final PR head before merge: `5caf1fbdbe7f7441fc2c8144efc3b18a37682779`.

**M24 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `5caf1fb…` | `24213046380` | success | https://github.com/m-cahill/starlab/actions/runs/24213046380 |

**Authoritative green PR-head CI:** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) — **success** on final tip `5caf1fb…`.

**M24 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M24 merge (`7b4d3b4…`) | `24213094531` | success | https://github.com/m-cahill/starlab/actions/runs/24213094531 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M24 milestone artifacts:** `docs/company_secrets/milestones/M24/` (`M24_plan.md`, `M24_toolcalls.md`, `M24_run1.md`, `M24_summary.md`, `M24_audit.md`, etc.)

**M25 merge:** [PR #31](https://github.com/m-cahill/starlab/pull/31) merged **2026-04-09** (UTC `2026-04-09T21:57:32Z`) via **merge commit** `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b`. Remote branch `m25-baseline-evidence-pack` was **deleted** after merge. Final PR head before merge: `b132bfd53f0f31b81f6d2955ca659d5923cdd4b1`.

**M25 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `b132bfd…` | `24215322933` | success | https://github.com/m-cahill/starlab/actions/runs/24215322933 |

**Authoritative green PR-head CI:** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) — **success** on final tip `b132bfd…`.

**M25 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M25 merge (`f03c7bf…`) | `24215360351` | success | https://github.com/m-cahill/starlab/actions/runs/24215360351 |

**M25 CI evidence (post-merge `main` — non-merge-boundary closeout)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M25 closeout (`78ced31…`) | `24215484700` | success | https://github.com/m-cahill/starlab/actions/runs/24215484700 |

Milestone docs + ledger + governance tests + **M26** stubs only — **not** substitute merge authority for M25 **product** (**authoritative** remains PR-head [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) + merge-boundary [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351)).

**Superseded red PR-head (not merge authority):** [`24215241322`](https://github.com/m-cahill/starlab/actions/runs/24215241322), [`24215286216`](https://github.com/m-cahill/starlab/actions/runs/24215286216) — see `M25_run1.md`.

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary events unless they record a new PR merge. Prefer **at most one** post-merge doc-only churn per closeout hygiene.*

**M25 milestone artifacts:** `docs/company_secrets/milestones/M25/` (`M25_plan.md`, `M25_toolcalls.md`, `M25_run1.md`, `M25_summary.md`, `M25_audit.md`, etc.)

**M26 merge:** [PR #32](https://github.com/m-cahill/starlab/pull/32) merged **2026-04-09** (UTC `2026-04-09T22:50:52Z`) via **merge commit** `e83a8493a577c9013d720f1debab009dcf9c464f`. Remote branch `m26-replay-corpus-training-dataset-contract` was **deleted** after merge. Final PR head before merge: `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f`.

**M26 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `d8d3c4c…` | `24217118559` | success | https://github.com/m-cahill/starlab/actions/runs/24217118559 |

**Authoritative green PR-head CI:** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) — **success** on final tip `d8d3c4c…`.

**M26 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M26 merge (`e83a849…`) | `24217178208` | success | https://github.com/m-cahill/starlab/actions/runs/24217178208 |

**M26 CI evidence (post-merge `main` — non-merge-boundary closeout)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M26 closeout (`2ccf60e…`) | `24217359747` | success | https://github.com/m-cahill/starlab/actions/runs/24217359747 |

Milestone docs + ledger + governance tests + **M27** stubs only — **not** substitute merge authority for M26 **product** (**authoritative** remains PR-head [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) + merge-boundary [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208)).

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M26 milestone artifacts:** `docs/company_secrets/milestones/M26/` (`M26_plan.md`, `M26_toolcalls.md`, `M26_run1.md`, `M26_summary.md`, `M26_audit.md`, etc.)

**M27 merge:** [PR #33](https://github.com/m-cahill/starlab/pull/33) merged **2026-04-09** (UTC `2026-04-09T23:45:00Z`) via **merge commit** `49b45825b65e56deb5cf991c5f74889e3daf2f59`. Remote branch `m27-replay-derived-imitation-baseline` was **deleted** after merge. Final PR head before merge: `65dcd2fbfa1b6e8d05f6db8bebe191f4b8822ccc`.

**M27 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `65dcd2f…` | `24218875847` | success | https://github.com/m-cahill/starlab/actions/runs/24218875847 |

**Authoritative green PR-head CI:** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) — **success** on final tip `65dcd2f…`.

**Superseded red PR-head (not merge authority):** [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) — **failure** at Ruff format on earlier tip — see `M27_run1.md`.

**M27 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M27 merge (`49b4582…`) | `24218902938` | success | https://github.com/m-cahill/starlab/actions/runs/24218902938 |

**M27 CI evidence (post-merge `main` — non-merge-boundary closeout)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M27 closeout (`f41ba73…`) | `24218984682` | success | https://github.com/m-cahill/starlab/actions/runs/24218984682 |

Milestone docs + ledger + governance tests + **M28** stubs only — **not** substitute merge authority for M27 **product** (**authoritative** remains PR-head [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) + merge-boundary [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938)). *Historical note at M27 closeout; **M28** product scope is recorded in §6 / §11 after implementation.*

*Further documentation-only pushes to `main` after this row may produce additional green CI runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge.*

**M27 milestone artifacts:** `docs/company_secrets/milestones/M27/` (`M27_plan.md`, `M27_toolcalls.md`, `M27_run1.md`, `M27_summary.md`, `M27_audit.md`, etc.)

**M28 merge:** [PR #34](https://github.com/m-cahill/starlab/pull/34) merged **2026-04-10** (UTC `2026-04-10T00:35:30Z`) via **merge commit** `1ef636524269ff77ac26ac37584d43b50e9fcbc6`. Remote branch `m28-learned-agent-evaluation-harness` was **deleted** after merge. Final PR head before merge: `c7ca6e6be8fbd44e39357da82cca857eddbd8eb3`.

**M28 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `c7ca6e6…` | `24220323130` | success | https://github.com/m-cahill/starlab/actions/runs/24220323130 |

**Authoritative green PR-head CI:** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) — **success** on final tip `c7ca6e6…`.

**Superseded red PR-head (not merge authority):** none recorded for M28 — see `M28_run1.md`.

**M28 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M28 merge (`1ef6365…`) | `24220357580` | success | https://github.com/m-cahill/starlab/actions/runs/24220357580 |

**M28 milestone artifacts:** `docs/company_secrets/milestones/M28/` (`M28_plan.md`, `M28_toolcalls.md`, `M28_run1.md`, `M28_summary.md`, `M28_audit.md`, etc.)

**M29 merge:** [PR #35](https://github.com/m-cahill/starlab/pull/35) merged **2026-04-10** (UTC `2026-04-10T01:29:12Z`) via **merge commit** `187d9ddd8e6b5234245923200c3a396d602e7b06`. Remote branch `m29-hierarchical-agent-interface-layer` was **deleted** after merge. Final PR head before merge: `60554e960a9227202578a3910052acaddf29677a`.

**M29 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `60554e9…` | `24221769054` | success | https://github.com/m-cahill/starlab/actions/runs/24221769054 |

**Authoritative green PR-head CI:** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) — **success** on final tip `60554e9…`.

**Superseded red PR-head (not merge authority):** [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) — **failure** at **Ruff format** on earlier tip `bcc5e94…` — fixed on tip `60554e9…`.

**M29 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M29 merge (`187d9dd…`) | `24221791088` | success | https://github.com/m-cahill/starlab/actions/runs/24221791088 |

**M29 milestone artifacts:** `docs/company_secrets/milestones/M29/` (`M29_plan.md`, `M29_toolcalls.md`, `M29_run1.md`, `M29_summary.md`, `M29_audit.md`, etc.)

**M30 merge:** [PR #36](https://github.com/m-cahill/starlab/pull/36) merged **2026-04-10** (UTC `2026-04-10T02:55:11Z`) via **merge commit** `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf`. Remote branch `m30-first-learned-hierarchical-agent` was **deleted** after merge. Final PR head before merge: `2a2744527d74acd953507e5b847ef9ce0a7497d3`.

**M30 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `2a27445…` | `24223946664` | success | https://github.com/m-cahill/starlab/actions/runs/24223946664 |

**Authoritative green PR-head CI:** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) — **success** on final tip `2a27445…`.

**Superseded red PR-head (not merge authority):** none recorded for M30 — see `M30_run1.md`.

**M30 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M30 merge (`1c3a5f6…`) | `24223976390` | success | https://github.com/m-cahill/starlab/actions/runs/24223976390 |

**M30 milestone artifacts:** `docs/company_secrets/milestones/M30/` (`M30_plan.md`, `M30_toolcalls.md`, `M30_run1.md`, `M30_summary.md`, `M30_audit.md`, etc.)

**M31 merge:** [PR #37](https://github.com/m-cahill/starlab/pull/37) merged **2026-04-10** (UTC `2026-04-10T04:24:58Z`) via **merge commit** `41d62056e1956627b63152221932dc9c2423429c`. Remote branch `m31-replay-explorer-operator-evidence-surface` was **deleted** after merge. Final PR head before merge: `4972a56c335342fbf2f1c5fa179bb1920561317c`.

**M31 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `4972a56…` | `24225153475` | success | https://github.com/m-cahill/starlab/actions/runs/24225153475 |

**Authoritative green PR-head CI:** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) — **success** on final tip `4972a56…`.

**Superseded red PR-head (not merge authority):** none recorded for M31 — see `M31_run1.md`.

**M31 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M31 merge (`41d6205…`) | `24226308356` | success | https://github.com/m-cahill/starlab/actions/runs/24226308356 |

**M31 milestone artifacts:** `docs/company_secrets/milestones/M31/` (`M31_plan.md`, `M31_toolcalls.md`, `M31_run1.md`, `M31_summary.md`, `M31_audit.md`, etc.)

**M40 merge:** [PR #51](https://github.com/m-cahill/starlab/pull/51) merged **2026-04-12** (UTC `2026-04-12T00:52:29Z`) via **merge commit** `44e8edc5bcce8dc99576bf2be542b273095e5072`. Remote branch `m40-agent-training-program-charter` was **deleted** after merge. Final PR head before merge: `be47d913737f322bbf8e9e08a672561c71d322eb`.

**M40 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `be47d91…` | `24295050784` | success | https://github.com/m-cahill/starlab/actions/runs/24295050784 |

**Authoritative green PR-head CI:** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) — **success** on final tip `be47d91…`.

**Superseded (not merge authority):** [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) — **failure** at **Ruff format** on `6690cd7f0ae79abe0db85695a0d20b4d7c48cdaf`; fixed on tip `be47d91…`.

**M40 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M40 merge (`44e8edc…`) | `24295326123` | success | https://github.com/m-cahill/starlab/actions/runs/24295326123 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs; distinguish them in §23 — **not** merge-boundary unless the event is a PR merge. Prefer **at most one** post-merge doc-only commit per closeout hygiene.*

**M40 milestone artifacts:** `docs/company_secrets/milestones/M40/` (`M40_plan.md`, `M40_toolcalls.md`, `M40_run1.md`, `M40_summary.md`, `M40_audit.md`, etc.)

**M41 merge:** [PR #52](https://github.com/m-cahill/starlab/pull/52) merged **2026-04-12** (UTC `2026-04-12T02:58:11Z`) via **merge commit** `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`. Remote branch `m41-replay-imitation-training-pipeline-v1` was **retained** on `origin` after merge. Final PR head before merge: `7c092eda7fe6554a2168968ffddbe37e929159e4`.

**M41 CI evidence (PR-head run — authoritative merge gate)**

| Commit (short) | Workflow run | Conclusion | URL |
| -------------- | ------------ | ---------- | --- |
| `7c092ed…` | `24297208733` | success | https://github.com/m-cahill/starlab/actions/runs/24297208733 |

**Authoritative green PR-head CI:** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) — **success** on final tip `7c092ed…`.

**Superseded (not merge authority for final head):** [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190), [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — intermediate green runs on the M41 feature branch.

**M41 CI evidence (post-merge `main` — merge boundary)**

| Event | Workflow run | Conclusion | URL |
| ----- | ------------ | ---------- | --- |
| `main` after M41 merge (`5e0add12…`) | `24297269820` | success | https://github.com/m-cahill/starlab/actions/runs/24297269820 |

*Closeout / ledger documentation pushes after this row may produce additional green `main` runs — **non-merge-boundary** for M41 product merge; merge-boundary remains **`24297269820`** on `5e0add12…`.*

**M41 milestone artifacts:** `docs/company_secrets/milestones/M41/` (`M41_plan.md`, `M41_toolcalls.md`, `M41_run1.md`, `M41_summary.md`, `M41_audit.md`, etc.)

---

## 19. Deferred items / future-only tracks

These are intentionally not current default scope.

| ID      | Item                                         | Status   | Notes                                               |
| ------- | -------------------------------------------- | -------- | --------------------------------------------------- |
| FUT-001 | Multi-environment expansion                  | Deferred | Only after SC2 substrate proves itself              |
| FUT-002 | Audio / AURORA-adjacent modality integration | Deferred | Optional sibling influence, not core starting scope |
| FUT-003 | Broader commercialization posture            | Deferred | Not the near-term goal                              |
| FUT-004 | Community benchmark leadership posture       | Deferred | Must be earned by evidence, not declared early      |
| FUT-005 | Phase VI legacy stubs — **SC2 Substrate Review & Expansion Decision**; **Platform Boundary Review & Multi-Environment Charter** | Deferred beyond M00–M45 | Listed in pre–M40 ledger as **M40**/**M41** stubs; after **M39** the program rechartered Phase VI to the **M40**–**M45** training track; these substrate/platform review items are not deleted from history — they await a **future charter** after the current active arc |

---

## 20. Suggested score trend table

This is a placeholder table for future audit tracking once milestones begin closing.

| Milestone | Arch | Governance | Evidence | CI  | Diligence | Docs | Overall |
| --------- | ---- | ---------- | -------- | --- | --------- | ---- | ------- |
| M00       | 3.5  | +          | +        | +   | +         | +    | 4.0     |
| M01       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M02       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M03       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M04       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M05       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M06       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M07       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M08       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M09       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M10       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M11       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M12       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M13       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M14       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M15       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M16       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M17       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M18       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M19       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M20       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M21       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M22       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M23       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M24       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M25       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M26       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M27       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M28       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M29       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M30       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M31       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M32       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M33       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M34       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M35       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M36       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M37       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M38       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M39       | 3.5  | +          | +        | +   | +         | +    | 4.5     |
| M40       | 3.5  | +          | +        | +   | +         | +    | 4.5     |

**M33 note:** Evidence column reflects **explicit parallel CI tiers** + **`fieldtest-output`** artifact (`out/fieldtest/` with required explorer JSON) + **expanded architecture / operator / diligence** surfaces — **proved** on `main` ([PR #39](https://github.com/m-cahill/starlab/pull/39); §18 / `M33_run1.md`); **not** M34 structural hygiene product work, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity.

**M34 note:** Evidence column — **merged** to `main` ([PR #40](https://github.com/m-cahill/starlab/pull/40); §18 / `M34_run1.md`): **`starlab._io`**, split `tests/test_governance_*.py`, **Dependabot** + dev dependency caps, **`docs/diligence/operating_manual_promotion_readiness.md`** (prep only), **`docs/audit/broad_exception_boundaries.md`** (**DIR-005** = **confirming/documenting** approved boundary catches — **not** code narrowing); coverage gate **75.4** unchanged; **green PR-head** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) on `a748bd7…`; **green merge-push `main`** [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) on `51e960d…`. **Not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI.

**M35 note:** Evidence column — **merged** to `main` ([PR #46](https://github.com/m-cahill/starlab/pull/46); §18 / `M35_run1.md`): **`M14BundleLoader`**, **`parser_io`**, **`replay_slice_generation`**, observation reconciliation split, **`load_json_object_strict`**, ledger **M00–M39** + stubs, governance tests; coverage gate **75.4** unchanged; **green PR-head** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) on `91e45dd…`; **green merge-push `main`** [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) on `5b4d24b…`; superseded PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) — **not** merge authority. **Not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI.

**M36 note:** Evidence column — **merged** to `main` ([PR #47](https://github.com/m-cahill/starlab/pull/47); §18 / `M36_run1.md`): **`docs/starlab_archive.md`**, **§7** archival policy + **M28–M35** inline notes, **`tests/test_governance_milestones.py`** consolidation, duplicate opaque-replay test removal in **`tests/test_governance_runtime.py`**, **`docs/starlab_archive.md`** on governance doc list; coverage gate **75.4** unchanged; **green PR-head** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) on `63fe116…`; **green merge-push `main`** [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) on `e73a53b…`; superseded PR-head: none recorded. **Not** M39 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI. **Not** operating manual v1.

**M02 note:** Evidence column reflects **narrow** local harness proof + CI; not benchmark or cross-host certification.

**M03 note:** Evidence column reflects **fixture/proof-driven** identity + lineage seed + CI on `main`; not replay binding, canonical artifact v0, or benchmark certification.

**M04 note:** Evidence column reflects **fixture-driven replay binding** (`replay_binding.json`) + CI on `main`; **not** replay parser semantics, replay↔proof equivalence, canonical run artifact v0, or benchmark certification.

**M05 note:** Evidence column reflects **fixture-driven canonical bundle** (`manifest.json` / `hashes.json` + M03/M04 JSON) **on `main`**; **not** replay parser semantics, raw replay/proof shipping, benchmark validity, or cross-host reproducibility.

**M06 note:** Evidence column reflects **fixture-driven** smoke matrix + drift report + CI on `main`; **not** replay parser semantics, portability certification, benchmark validity, provenance closure, or live SC2 execution in CI.

**M07 note:** Evidence column reflects **fixture-driven** replay intake receipt/report + CI **on `main`**; **not** replay parser semantics, build-order extraction, benchmark validity, live SC2 execution in CI, or legal certification of third-party replay rights as a matter of law.

**M08 note:** Evidence column reflects **fixture-driven** parser substrate + deterministic parse artifacts + CI **on `main`**; **not** stable normalized metadata (M09), event semantics (M10), broad parser correctness, benchmark validity, or live SC2 execution in CI.

**M09 note:** Evidence column reflects **fixture-driven** metadata extraction + deterministic metadata artifacts + CI **on `main`**; **not** event/timeline semantics (M10), build-order extraction (M11), or benchmark validity.

**M10 note:** Evidence column reflects **fixture-driven** timeline extraction + deterministic timeline artifacts + CI **on `main`** (merge-push on merge commit failed Mypy — **authoritative green `main`** on repair `cf2074e…`, run `24104197912`); **not** build-order/economy (M11), combat/scouting, benchmark validity, or live SC2 execution in CI.

**M11 note:** Evidence column reflects **fixture-driven** build-order/economy extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) on `88ce7f9…`; **green merge-push** [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) on `38c1530…`); **not** combat/scouting (M12), exact resource reconstruction, benchmark validity, replay↔execution equivalence, or live SC2 execution in CI.

**M12 note:** Evidence column reflects **fixture-driven** combat/scouting/visibility extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) on `59adce3…`; **green merge-push** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) on `7852895…`); **not** replay slice definitions (M13), true fog-of-war certification, benchmark validity, replay↔execution equivalence, or live SC2 execution in CI.

**M13 note:** Evidence column reflects **fixture-driven** replay slice definition extraction + deterministic artifacts + CI **on `main`** (**green PR-head** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) on `6231b19…`; **green merge-push** [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) on `f86e368…`); **not** raw replay clipping, benchmark validity, replay↔execution equivalence, fog-of-war truth, or live SC2 execution in CI.

**M14 note:** Evidence column reflects **fixture-driven** replay bundle packaging + lineage + contents + CI **on `main`** (**green PR-head** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) on `42e29f2…`; **green merge-push** [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) on `8a0439a…`); **not** raw replay clipping, replay↔execution equivalence, benchmark validity, canonical state schema (M15), live SC2 execution in CI, or legal certification of replay rights.

**M15 note:** Evidence column reflects **schema + report emission**, **jsonschema** validation over fixtures, and full governance CI **on `main`** (**green PR-head** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) on `abc8ffc…`; **green merge-push** [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) on `b0f7132…`); **not** replay-to-state materialization (M16), observation contract (M17), perceptual bridge (M18), stronger economy or visibility claims than M11/M12, replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

**M16 note:** Evidence column reflects **M14 bundle → one `canonical_state.json` + report**, **jsonschema** validation against M15 schema, and full governance CI **on `main`** (**green PR-head** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) on `11fb080…`; **green merge-push** [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) on `dd9546f…`); **superseded** red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority); **not** observation tensors / action masks (M17), perceptual bridge (M18), replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI.

**M17 note:** Evidence column reflects **observation surface schema + report emission**, **jsonschema** validation over fixtures, and full governance CI **on `main`** (**green PR-head** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) on `801af8b…`; **green merge-push `main`** [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) on `f63c8e9…`); **not** canonical-state→observation materialization (that is **M18**), mask legality computation, replay↔execution equivalence, benchmark integrity, exact banked resources, certified fog-of-war truth, or live SC2 in CI.

**M18 note:** Evidence column reflects **prototype materialization** from M16 `canonical_state.json` to M17-shaped `observation_surface.json` + report, **jsonschema** validation on emitted observation, and full governance CI **on `main`** (**green PR-head** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) on `8d9f9e1…`; **green merge-push `main`** [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) on `59d2d6e…`); **not** full action legality, benchmark integrity, replay↔execution equivalence, certified fog-of-war truth, exact banked resources, live SC2 in CI, or **M19** reconciliation (M19 is a separate proof).

**M19 note:** Evidence column reflects **cross-mode reconciliation audit** over paired M16 `canonical_state.json` + M18 `observation_surface.json` (fixture-backed goldens under `tests/fixtures/m19/`) + full governance CI **on `main`** (**green PR-head** [`24168988693`](https://github.com/m-cahill/starlab/actions/runs/24168988693) on `1453eee…`; **green merge-push `main`** [`24169013104`](https://github.com/m-cahill/starlab/actions/runs/24169013104) on `9e85532…`). **Not** benchmark integrity, replay↔execution equivalence, live SC2 in CI, or **M20** benchmark contract semantics.

**M20 note:** Evidence column reflects **benchmark contract + scorecard JSON Schema emission** + fixture validation + full governance CI **on `main`** (**green PR-head** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) on `5c22336…`; **green merge-push `main`** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) on `cf1bee9…`; see §18 / `M20_run1.md`). **Not** scripted/heuristic baselines (**M21–M22**), evaluation runner (**M23**), benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

**M21 note:** Evidence column reflects **scripted baseline suite + report emission** from one **`fixture_only`** M20-validated benchmark contract + embedded M20 scorecards + full governance CI **on `main`** (**green PR-head** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) on `818002e…`; **green merge-push `main`** [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) on `092d00a…`; see §18 / `M21_run1.md`). **Superseded** red PR-head [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) (Ruff format — **not** merge authority). **Not** heuristic baselines (**M22**), evaluation runner (**M23**), benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

**M22 note:** Evidence column reflects **heuristic baseline suite + report emission** from one **`fixture_only`** M20-validated benchmark contract + embedded M20 scorecards for **heuristic** subjects + full governance CI **on `main`** (**green PR-head** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) on `96aba18…`; **green merge-push `main`** [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) on `470afa8…`; see §18 / `M22_run1.md`). **Not** evaluation runner (**M23**), tournament harness, benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

**M23 note:** Evidence column reflects **fixture-only evaluation tournament** (`evaluation_tournament.json` / `evaluation_tournament_report.json`) from M20 + **M21/M22** suite artifacts + full governance CI **on `main`** (**green PR-head** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) on `f00711a…`; **green merge-push `main`** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) on `b8857d2…`; see §18 / `M23_run1.md`). **Not** evaluation diagnostics (**M24**), baseline evidence pack (**M25**), **M26** replay training dataset contract, **M27** imitation baseline, benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

**M24 note:** Evidence column reflects **fixture-only evaluation diagnostics** (`evaluation_diagnostics.json` / `evaluation_diagnostics_report.json`) from one governed **M23** `evaluation_tournament.json` + full governance CI **on `main`** (**green PR-head** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) on `5caf1fb…`; **green merge-push `main`** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) on `7b4d3b4…`; see §18 / `M24_run1.md`). **Interpretive** over M23 — **not** new tournament semantics. **Not** baseline evidence pack (**M25**), **M26** replay training dataset contract, **M27** imitation baseline, benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

**M25 note:** Evidence column reflects **baseline evidence pack** (`baseline_evidence_pack.json` / `baseline_evidence_pack_report.json`) from governed **M21/M22 + M23 + M24** + full governance CI **on `main`** (**green PR-head** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on `b132bfd…`; **green merge-push `main`** [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) on `f03c7bf…`; see §18 / `M25_run1.md`). **Interpretive packaging** — **not** benchmark integrity, **M27** imitation baseline, replay↔execution equivalence, or live SC2 in CI.

**M26 note:** Evidence column reflects **replay training dataset** (`replay_training_dataset.json` / `replay_training_dataset_report.json`) from governed **M14** bundles + full governance CI **on `main`** (**green PR-head** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on `d8d3c4c…`; **green merge-push `main`** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) on `e83a849…`; see §18 / `M26_run1.md`). **Dataset contract only** — **not** model training, imitation quality, benchmark integrity, **M27** imitation baseline, replay↔execution equivalence, or live SC2 in CI.

**M27 note:** Evidence column reflects **replay imitation baseline** (`replay_imitation_baseline.json` / `replay_imitation_baseline_report.json`) over governed **M26** + **M14** via **M16 → M18** + full governance CI **on `main`** (**green PR-head** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) on `65dcd2f…`; **green merge-push `main`** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) on `49b4582…`; see §18 / `M27_run1.md`). **Superseded** red PR-head [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) (Ruff format — **not** merge authority). **First** narrow **offline** **replay-derived trained** baseline artifact — **`agreement_by_split`** is **internal smoke only**; **not** benchmark integrity, hierarchical agents, replay↔execution equivalence, live SC2 in CI, or strong imitation quality beyond explicit non-claims.

**M28 note:** Evidence column reflects **learned-agent evaluation** (`learned_agent_evaluation.json` / `learned_agent_evaluation_report.json`) over **M20** contract + frozen **M27** + **M26** + **M14** + full governance CI **on `main`** (**green PR-head** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) on `c7ca6e6…`; **green merge-push `main`** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) on `1ef6365…`; see §18 / `M28_run1.md`). **Not** benchmark integrity, **not** M23–M25 chain surfaces, **not** live SC2 in CI, **not** replay parser execution in M28 evaluation modules.

**M29 note:** Evidence column reflects **hierarchical agent interface** (`hierarchical_agent_interface_schema.json` / `hierarchical_agent_interface_schema_report.json`) + full governance CI **on `main`** (**green PR-head** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) on `60554e9…`; **green merge-push `main`** [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) on `187d9dd…`; see §18 / `M29_run1.md`). **Superseded** red PR-head [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) (Ruff format — **not** merge authority). **Not** learned hierarchical agent (**M30**), **not** benchmark integrity, **not** live SC2 in CI, **not** `starlab.replays` / `starlab.sc2` / `s2protocol` in listed M29 hierarchy modules.

**M30 note:** Evidence column reflects **first learned hierarchical imitation agent** (`replay_hierarchical_imitation_agent.json` / `replay_hierarchical_imitation_agent_report.json`) over governed **M26** + **M14** via **M16 → M18** + fixed delegate policy **`starlab.m30.delegate.fixed_four_v1`** + full governance CI **on `main`** (**green PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) on `2a27445…`; **green merge-push `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) on `1c3a5f6…`; see §18 / `M30_run1.md`). **Superseded** red PR-head: none recorded. **Not** benchmark integrity, **not** live SC2 in CI, **not** raw action legality, **not** replay↔execution equivalence, **not** M31 replay explorer / flagship proof pack.

**M31 note:** Evidence column reflects **replay explorer / operator evidence surface** (`replay_explorer_surface.json` / `replay_explorer_surface_report.json`) over governed **M14** + frozen **M30** agent + **M16 → M18** + full governance CI **on `main`** (**green PR-head** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) on `4972a56…`; **green merge-push `main`** [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) on `41d6205…`; see §18 / `M31_run1.md`). **Superseded** red PR-head: none recorded. **Not** benchmark integrity, **not** live SC2 in CI, **not** web UI, **not** M39 flagship proof pack product.

**M40 note:** Evidence column reflects **training-program charter** — `starlab.training`, deterministic `agent_training_program_contract.json` / report, runtime contract doc, ledger arc then **46** milestones + **M41**–**M45** stubs (superseded by **M46** extension to **47** — see §7) — **merged** to `main` (**green PR-head** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) on `be47d91…`; **green merge-push `main`** [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) on `44e8edc…`; see §18 / `M40_run1.md`). **Superseded** red PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) (Ruff format — **not** merge authority). **Not** actual training, **not** weights, **not** benchmark integrity, **not** live SC2 in CI, **not** **M41+** product.

**M33 note:** Evidence column reflects **explicit parallel `CI` job topology** + **`fieldtest-output`** + **`ci_tiering_field_test_readiness_v1.md`** + expanded architecture / operator / diligence surfaces + **DIR-001/002/007** resolutions — **green PR-head** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) on `6640c69…`; **green merge-push `main`** [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) on `975ac52…`; see §18 / `M33_run1.md`. **Superseded** green PR-head [`24231252478`](https://github.com/m-cahill/starlab/actions/runs/24231252478) on earlier tip — **not** final merge authority. **Not** M34 structural hygiene product work, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity.

---

## 21. README alignment rule

The README should stay shorter and simpler than this file.

- README = front door  
- `docs/starlab.md` = public ledger / living source of truth  
- Vision = thesis and moonshot  
- `docs/bicetb.md` = operating discipline for cleanliness and diligence  

If those documents drift, this file should record the resolution.

---

## 22. Living document rule

This file is the **public-facing source of truth** for STARLAB’s current state.

It should always answer, with minimal ambiguity:

- what STARLAB is
- what phase it is in
- which milestone is current
- which milestones are closed
- what has actually been proved
- what remains open
- what the project is intentionally not doing yet

---

## 23. Changelog

### 2026-04-23 — **PX2** transition closeout + **`V15-M00`** opened (v1.5 planning surface; **not** long GPU run)

- **Ledger:** **PX2** (**`PX2-M03`** last) **closed** / **transition-complete**; **`current milestone`** → **`V15-M00`** — **v1.5 Training Readiness Charter and Long GPU Run Gate** (private plan folder `docs/company_secrets/milestones/post-v1/V15-M00/`; public authority later **`docs/starlab-v1.5.md`**). **Non-claim:** **PX2** did **not** perform a **long wall-clock GPU training session** as a program deliverable. **M32**-family carry-forwards recorded in §7 / v1.5 doc. Private closeout memos: `PX2-M03_summary.md` / `PX2-M03_audit.md` (may be local-only).

### 2026-04-21 — **PX2-M03** first real bounded substantive operator-local pass (evidence + weight seal)

- **Delivered:** Sealed **`weights_file_sha256_declared`** in **`px2_self_play_bounded_substantive_execution.json`** (record **`px2_m03_bounded_substantive_operator_local_execution_v2`**); **§8q** table distinguishing **bounded substantive operator-local execution evidence** vs **later industrial `PX2-M03` execution evidence**; test **`test_bounded_substantive_real_weights_seals_weights_file_sha256`** (real **`state_dict`** path — **not** merge-gate operator repro). **not** industrial campaign; **not** **PX2-M04**; **PX2-M03** historically **open** on ledger at that time (superseded by **2026-04-23** closeout).

### 2026-04-21 — **PX2-M03** bounded substantive operator-local execution (post–slice-16, not a micro-slice)

- **Delivered:** **`run_bounded_substantive_operator_local_execution`** + **`px2_self_play_bounded_substantive_execution.json`** / report; **`bounded_substantive_execution_record`**; **`EXECUTION_KIND_BOUNDED_SUBSTANTIVE`** (continuity steps **2–20**, default **15**); continuity clamp extended for this kind only; CLI **`emit_px2_self_play_bounded_substantive_execution`**; real-weights mode **fail closed** without **`--weights`**; optional slice-15/16 lineage binding when artifacts OK; runtime §8q + ledger (quick scan / §11 / Start Here) — **After slice 16, PX2-M03 exits lineage-surface expansion and enters bounded substantive execution, still below industrial scale.** — **not** industrial campaign; **not** **PX2-M04**.

### 2026-04-19 — **PX2-M03** sixteenth implementation slice — bounded handoff-anchored operator-local run

- **Delivered:** **`run_bounded_handoff_anchored_operator_local_run`** + **`verify_loaded_pointer_seeded_handoff_self_seal`** + **`px2_self_play_handoff_anchored_run.json`** / report (sealed **`handoff_anchored_run_sha256`**); **`handoff_anchored_run_record`**; **`EXECUTION_KIND_SLICE16`**; CLI **`emit_px2_self_play_handoff_anchored_run`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8p — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 16** / **later industrial `PX2-M03` execution**.

### 2026-04-19 — **PX2-M03** fifteenth implementation slice — bounded post–pointer-seeded handoff

- **Delivered:** **`run_bounded_pointer_seeded_handoff`** + **`verify_loaded_pointer_seeded_run_self_seal`** + **`px2_self_play_pointer_seeded_handoff.json`** / report (sealed **`pointer_seeded_handoff_sha256`**); **`pointer_seeded_handoff_record`**; **`EXECUTION_KIND_SLICE15`**; rule **`px2_m03_slice15_handoff_after_slice14_pointer_seeded_stub_v1`**; lineage **`declared_next_bounded_step_from_slice14_pointer_seeded_run_v1`**; CLI **`emit_px2_self_play_pointer_seeded_handoff`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8o; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 15** / **later industrial `PX2-M03` execution**.

### 2026-04-19 — **PX2-M03** fourteenth implementation slice — bounded pointer-seeded operator-local run

- **Delivered:** **`run_bounded_pointer_seeded_operator_local_run`** + **`verify_loaded_current_candidate_self_seal`** + **`px2_self_play_pointer_seeded_run.json`** / report (sealed **`pointer_seeded_run_sha256`**); **`pointer_seeded_run_record`**; **`EXECUTION_KIND_SLICE14`** on continuity + manifest append; rule **`px2_m03_slice14_seed_from_current_candidate_pointer_stub_v1`**; CLI **`emit_px2_self_play_pointer_seeded_run`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8n; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 14** / **later industrial `PX2-M03` execution**.

### 2026-04-22 — **PX2-M03** thirteenth implementation slice — bounded second-hop continuation + optional symmetric re-anchor

- **Delivered:** **`run_bounded_second_hop_continuation_after_slice12`** + **`px2_self_play_second_hop_continuation.json`** / report (sealed **`second_hop_continuation_sha256`**); **`second_hop_continuation_record`**; **`run_bounded_current_candidate_reanchor_after_second_hop`** + extended **`current_candidate_reanchor`** seal ( **`EXECUTION_KIND_SLICE13`** continuation + **`EXECUTION_KIND_SLICE13_REANCHOR`** refresh); refreshed **`px2_self_play_current_candidate.json`** with **`CURRENT_CANDIDATE_RECORD_VERSION_SLICE13`** when re-anchor runs; continuation **`EXECUTION_KIND_SLICE13`** + **`CONTINUATION_RUN_RECORD_VERSION_SLICE13`**; snapshots **`px2_self_play_first_hop_continuation_snapshot.json`** / **`px2_self_play_slice12_reanchor_snapshot.json`**; CLI **`emit_px2_self_play_second_hop_continuation`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8m; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 13** / **later industrial `PX2-M03` execution**.

### 2026-04-22 — **PX2-M03** twelfth implementation slice — post-continuation current-candidate re-anchoring

- **Delivered:** **`run_bounded_current_candidate_reanchor_after_continuation`** + **`px2_self_play_current_candidate_reanchor.json`** / report (sealed **`current_candidate_reanchor_sha256`**); refreshed **`px2_self_play_current_candidate.json`** with **`CURRENT_CANDIDATE_RECORD_VERSION_SLICE12`** / **`EXECUTION_KIND_SLICE12`**; **`current_candidate_reanchor_record`**; rules **`px2_m03_slice12_reanchor_after_consumed_continuation_stub_v1`** / **`px2_m03_slice12_reanchor_from_continuation_stub_v1`**; CLI **`emit_px2_self_play_current_candidate_reanchor`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8l; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 12** / **later industrial `PX2-M03` execution**.

### 2026-04-22 — **PX2-M03** eleventh implementation slice — bounded continuation run consuming current-candidate pointer

- **Delivered:** **`run_bounded_continuation_run_consuming_current_candidate`** + **`validate_current_candidate_for_continuation_run`** + **`px2_self_play_continuation_run.json`** / report (sealed **`continuation_run_sha256`**); **`EXECUTION_KIND_SLICE11`**; **`continuation_run_record`**; rule **`px2_m03_slice11_consume_current_candidate_stub_v1`**; CLI **`emit_px2_self_play_continuation_run`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8k; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 11** / **later industrial `PX2-M03` execution**.

### 2026-04-21 — **PX2-M03** tenth implementation slice — current-candidate carry-forward after transition

- **Delivered:** **`run_bounded_operator_local_session_transition_with_current_candidate`** + **`px2_self_play_current_candidate.json`** / report (sealed **`current_candidate_sha256`**); **`EXECUTION_KIND_SLICE10`**; **`current_candidate_record`**; stub rule **`px2_m03_slice10_carry_forward_from_session_transition_stub_v1`**; **`next_run_preflight_hints_from_current_candidate`**; CLI **`emit_px2_self_play_current_candidate`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8j; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** … **slice 10** / **later industrial `PX2-M03` execution**.

### 2026-04-20 — **PX2-M03** ninth implementation slice — bounded session + promotion/rollback execution step

- **Delivered:** **`run_bounded_operator_local_session_with_transition`** + **`px2_self_play_operator_local_session_transition.json`** / report (sealed **`operator_local_session_transition_sha256`**); **`EXECUTION_KIND_SLICE9`**; **`operator_local_session_transition_record`**; deterministic stub rules **`px2_m03_slice9_last_run_final_promotion_stub_v1`** / **`px2_m03_slice9_rollback_to_first_run_first_checkpoint_stub_v1`**; CLI **`emit_px2_self_play_operator_local_session_transition`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8i; tests — **not** industrial campaign; **not** **PX2-M04** exploit closure; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **slice 5** / **slice 6** / **slice 7** / **slice 8** / **slice 9** / **later industrial `PX2-M03` execution**.

### 2026-04-20 — **PX2-M03** eighth implementation slice — bounded operator-local multi-run session

- **Delivered:** **`run_bounded_operator_local_session`** + **`px2_self_play_operator_local_session.json`** / report (sealed **`operator_local_session_sha256`**); **`EXECUTION_KIND_SLICE8`**; per-run **`runs/<run_id>/px2_self_play_operator_local_real_run.json`** (slice-8 kind); **`operator_local_session_record`**; optional session operator note **`px2_operator_local_session_operator_note.md`** (documented; not sealed); **`write_campaign_root_manifest`** on **`run_slice5_operator_local_campaign`** for session orchestration; CLI **`emit_px2_self_play_operator_local_session`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8h; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **slice 5** / **slice 6** / **slice 7** / **slice 8** / **later industrial `PX2-M03` execution**.

### 2026-04-20 — **PX2-M03** seventh implementation slice — bounded operator-local real-run execution record

- **Delivered:** **`run_bounded_operator_local_real_run`** + **`px2_self_play_operator_local_real_run.json`** / report (sealed **`operator_local_real_run_sha256`**); **`EXECUTION_KIND_SLICE7`**; **`operator_local_real_run_record`**; CLI **`emit_px2_self_play_operator_local_real_run`**; optional operator note **`px2_operator_local_real_run_operator_note.md`** (documented; not sealed); runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8g; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **slice 5** / **slice 6** / **slice 7** / **later industrial `PX2-M03` execution**.

### 2026-04-19 — **PX2-M03** sixth implementation slice — preflight seal normalization + canonical operator-local campaign-root smoke

- **Delivered:** **`path_identity`** + **`preflight_seal_basis`** (logical-path **`preflight_sha256`**); **`canonical_operator_local_run`** + CLI **`emit_px2_self_play_canonical_campaign_root_smoke`**; **`EXECUTION_KIND_SLICE6`** on bounded canonical smoke; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8f; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **slice 5** / **slice 6** / **later industrial `PX2-M03` execution**.

### 2026-04-19 — **PX2-M03** fifth implementation slice — campaign-root manifest + opponent rotation hardening

- **Delivered:** **`run_slice5_operator_local_campaign`** + sealed **`px2_self_play_campaign_root_manifest.json`** / report; **`opponent_pool/px2_opponent_pool_metadata.json`**; expanded **`build_slice5_opponent_pool`** + **`opponent_pool_identity_sha256`**; **`opponent_rotation_trace`** on continuity episodes; **`OPPONENT_SELECTION_WEIGHTED_FROZEN_STUB`**; CLI **`emit_px2_self_play_slice5_campaign_root`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8e; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **slice 5** / **later industrial `PX2-M03` execution**.

### 2026-04-20 — **PX2-M03** fourth implementation slice — multi-step continuity + sealed linkage + promotion/rollback receipts

- **Delivered:** **`run_operator_local_campaign_continuity`** + sealed **`px2_self_play_campaign_continuity.json`** / report + **`continuity_chain.json`**; **`promotion_receipts`** / **`rollback_receipts`**; slice-4 checkpoint/eval linkage fields; **`ensure_operator_local_slice4_layout`**; CLI **`emit_px2_self_play_campaign_continuity`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8d; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **slice 4** / **later industrial `PX2-M03` execution**.

### 2026-04-20 — **PX2-M03** third implementation slice — operator-local execution preflight + bounded real-weights smoke

- **Delivered:** **`run_execution_preflight`** + **`px2_self_play_execution_preflight.json`** / report; **`build_policy_operator_local`** + file **SHA-256**; **`run_operator_local_campaign_smoke`** + sealed operator-local smoke JSON; CLIs **`emit_px2_self_play_execution_preflight`**, **`emit_px2_self_play_operator_local_smoke`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8c; tests — **not** industrial campaign; **not** Blackwell default; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **slice 3** / **later industrial `PX2-M03` execution**.

### 2026-04-19 — **PX2-M03** second implementation slice — execution skeleton, artifact tree, checkpoint/eval receipts

- **Delivered:** **`run_px2_campaign_execution_skeleton`** + **`run_manifest.json`** + sealed **`px2_self_play_campaign_run.json`** / report; **`checkpoint_receipts/`** and **`evaluation_receipts/`** receipt JSON (+ reports); CLI **`emit_px2_self_play_campaign_execution_skeleton`**; runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`** §8b; tests extended — **not** operator-local industrial run; **not** Blackwell evidence; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / opening-discipline table / §11 / Start Here / §23 — distinguishes **slice 1** / **slice 2** / **later `PX2-M03` industrial execution**.

### 2026-04-19 — **PX2-M03** first implementation slice — campaign contract, policy-runtime bridge, fixture smoke

- **Delivered:** public runtime **`docs/runtime/px2_industrial_self_play_campaign_v1.md`**; package **`starlab.sc2.px2.self_play`** (campaign contract + report, opponent selection stub, **`bootstrap_policy_runtime_step`** bridge, fixture smoke + emitters); tests **`tests/test_px2_m03_self_play_campaign.py`** — **not** operator-local industrial run; **not** Blackwell evidence; **not** **`PX2-M04`**. Ledger — quick scan / Post-PX1 (PX2) / §11 / Start Here / §23 — distinguishes **slice 1** (wiring + smoke) vs **later `PX2-M03` execution** (operator-local industrial self-play).

### 2026-04-20 — **PX2-M03** opening — Industrial Self-Play Campaign — **`current milestone`** → **`PX2-M03`**

- **Opened** **`PX2-M03`** on `main`: readiness / preflight **`docs/runtime/px2_industrial_self_play_campaign_readiness_v1.md`** (overall **green** opening verdict; **partial** opponent-pool / anti-collapse — **M03** implementation obligations); ledger §1 / §7 / §11 / Start Here / §8 intent — **`PX2-M04`** / **`PX2-M05`** **planned only**; **`PX1-M05`** optional / not yet opened; **v2** not opened. **Not** campaign execution; **not** Blackwell evidence; **not** strength proof. **PX2-M03** does **not** auto-open from **PX2-M02** closeout alone.

### 2026-04-20 — **PX2-M02** closeout — Neural Bootstrap from Replays — **`current milestone`** → **`None`**

- **Closed** **`PX2-M02`** on `main` via [PR #96](https://github.com/m-cahill/starlab/pull/96) (**branch** `px2-m02-neural-bootstrap-from-replays`): product merge + dependency pin — **`torch`** **`>=2.8,<3`** for **`pip-audit`** (CVE-2025-2953 / CVE-2025-3730); ledger §1 / §7 / §11 / Start Here — **`current milestone`** = **`None`**; **`PX2-M03`** **planned only**; **`PX1-M05`** optional / not yet opened; **v2** not opened.
- **Authoritative PR-head CI (final head before merge):** [`24645967129`](https://github.com/m-cahill/starlab/actions/runs/24645967129) on **`377d8dc9d1d5e91dbb11024334126cca14e5f0b6`** — **success**.
- **Merge commit (`main`):** `3b16c73fc3dd1cd4c5fbd73dd33c6bb0b2e486db` — **merge-boundary `main` CI** [`24646072791`](https://github.com/m-cahill/starlab/actions/runs/24646072791) on merge commit `3b16c73f…` — **success** — private workflow record: **`PX2-M02_run1.md`**.

### 2026-04-19 — **PX2-M02** opening — Neural Bootstrap from Replays — **`current milestone`** → **`PX2-M02`** (historical — **closed** **2026-04-20** — see entry above)

- **Opened** **`PX2-M02`** on `main`: public **`docs/runtime/px2_neural_bootstrap_from_replays_v1.md`**; Python **`starlab.sc2.px2.bootstrap`** (conservative BOE labeler, governed dataset contract + emitter, M18 flat feature adapter, `BootstrapTerranPolicy`, training/eval, legality-aware decode + compile stats); **`tests/fixtures/px2_m02/`** corpus + **`tests/test_px2_m02_replay_bootstrap.py`** (CPU fixture end-to-end: tiny train/eval, baselines) — **first PX2 learning milestone** — **not** self-play (**PX2-M03**); **not** Blackwell execution; **not** strength proof. **`torch`** pinned in **`pyproject.toml`** (initial range superseded at closeout merge — **`>=2.8,<3`** on `main`). **`PX2-M03`** — **planned only**. **`PX1-M05`** optional / not yet opened; **v2** not opened.

### 2026-04-19 — **PX2-M01** closeout — Full Terran Runtime & Action Surface — **`current milestone`** → **`None`** (historical — later **`PX2-M02`** opened then closed — see §23 **PX2-M02** entries)

- **Closed** **`PX2-M01`** on `main` via [PR #95](https://github.com/m-cahill/starlab/pull/95) (**branch** `px2-m01-terran-runtime-action-surface`): ledger + governance tests — **`PX2-M01`** **closed** at merge; **`current milestone`** = **`None`**; **`PX2-M02`** **not** opened; **`PX1-M05`** optional / not yet opened; **v2** not opened. **Runtime/action substrate only** — **not** training; **not** Blackwell execution; **not** strength proof.
- **Implementation PR-head (authoritative merge gate before closeout commit):** `c9d573460a0a82edba5a2941500902a8ccde1db8` — **authoritative PR-head CI** [`24643980874`](https://github.com/m-cahill/starlab/actions/runs/24643980874) — **success**.
- **Closeout final PR head:** `f4773d61e9981337f4799e77ec8f8ddae533f1e3` — **authoritative closeout PR-head CI** [`24644245868`](https://github.com/m-cahill/starlab/actions/runs/24644245868) — **success**.
- **Merge commit (`main`):** `dd5ce04a5ab531326ebf2b6a65951edea49e5813` — **merge-boundary `main` CI** [`24644285043`](https://github.com/m-cahill/starlab/actions/runs/24644285043) on merge commit `dd5ce04a…` — **success** — private workflow record: **`PX2-M01_run1.md`**.

### 2026-04-19 — **PX2-M01** opening — Full Terran Runtime & Action Surface — **`current milestone`** → **`PX2-M01`**

- **Opened** **`PX2-M01`** on `main`: public runtime **`docs/runtime/px2_full_terran_runtime_action_surface_v1.md`**; Python package **`starlab.sc2.px2`** (structured Terran actions, legality/masking, internal commands, Burny bridge hints, compile receipts); fixture tests — **runtime/action substrate only**; **not** replay-bootstrap training (**PX2-M02**); **not** Blackwell execution; **not** strength proof. **`PX2-M02`** — **not** opened automatically. **`PX1-M05`** optional / not yet opened; **v2** not opened.

### 2026-04-20 — **PX2-M00** governance closeout — **PR #94** — **`current milestone`** → **`None`**

- **Closed** **`PX2-M00`** via [PR #94](https://github.com/m-cahill/starlab/pull/94) (branch **`px2-m00-autonomous-full-game-charter`**): ledger + governance tests — **`PX2-M00`** **closed** on `main` at merge; **`current milestone`** = **`None`**; **`PX2-M01`** **not** opened; **`PX1-M05`** optional / not yet opened; **v2** not opened. Public runtime **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`** unchanged in scope (charter v1). Private **`PX2-M00_summary.md`** / **`PX2-M00_audit.md`** / **`PX2-M00_run1.md`** — local only.
- **Authoritative PR-head CI (pre-closeout opening head):** [`24641787057`](https://github.com/m-cahill/starlab/actions/runs/24641787057) on **`b7aa3f472da19db2ed454740543d7c7dadb205eb`** — **success**. **Closeout PR-head CI** and **merge-boundary `main` CI** on merge commit — recorded in private **`PX2-M00_run1.md`** (and optional post-merge changelog pointer only if a follow-up ledger edit is ever justified).

### 2026-04-19 — **PX2-M00** opening — **Post-PX1 (PX2)** phase chartered on `main`

- **Opened** **`PX2-M00`** — Autonomous Full-Game Agent Charter & Success Criteria — **`current milestone`** → **`PX2-M00`**; public runtime **`docs/runtime/px2_autonomous_full_game_agent_charter_v1.md`**; **Post-PX1 (PX2)** section + phase boundary matrix + §8 intent rows + §11 + Start Here + governance tests; private **`docs/company_secrets/milestones/post-v1/PX2-M00/`** working surface — **governance only**; **not** Terran runtime; **not** training; **not** Blackwell execution.
- **Ledger posture:** **PX2** is a **new** post-**PX1** capability phase — **PX1-M04** **closed** as packaging/proof governance **does not** auto-open **PX1-M05** or **v2** (**preserved**). **`PX1-M05`** optional / not yet opened; **v2** not opened.

### 2026-04-20 — **PX1-M04** governance closeout — merged to `main` ([PR #93](https://github.com/m-cahill/starlab/pull/93)) — **closed**; **`current milestone`** → **None** (historical — later superseded **2026-04-19** by **PX2-M00** open on **PR #94** — see §23)

- **Closed** **PX1-M04** on `main` with governance closeout: ledger + private **`PX1-M04_summary.md`** / **`PX1-M04_audit.md`** / **`PX1-M04_run2.md`**; canonical selection memo + checklist polish — **packaging / proof governance** only; operator-local demo proof pack chain verified (**`scripted_01`**, **`out/px1_m03_operator_watchable.mp4`**, **`px1_m01_weighted_refit_rl_bootstrap_v1`**) — **not** new remediation; **not** **PX1-M05** or **v2** auto-open.
- **Post-closeout ledger:** §1 quick scan + §7 + §11 + §23 — **PX1-M04** **closed**; **`current milestone`** = **None**; **`PX1-M05`** **optional / not yet opened**; **v2** **not** opened.
- **Workflow record:** **`PX1-M04_run2.md`** finalized with authoritative PR-head CI [`24637621474`](https://github.com/m-cahill/starlab/actions/runs/24637621474) and merge-boundary `main` CI [`24637654026`](https://github.com/m-cahill/starlab/actions/runs/24637654026) on merge commit `36095686110f994a0c8d4fc4ad5e83cdf873cc7f`.

### 2026-04-19 — **PX1-M04** Governed Demo Proof Pack & Winning Video — merged to `main` ([PR #92](https://github.com/m-cahill/starlab/pull/92)) — PR1 **open** (not closeout)

- **Merged** [PR #92](https://github.com/m-cahill/starlab/pull/92) to `main`; merge commit `f5e4521d35e152c97eb07458b38fb296929b5aaf` merged **2026-04-19T19:18:21Z** (UTC); **final PR head** `e57dac36d44c073198d773c8a8abd54bec5b5b56`; **authoritative PR-head CI** [`24637019658`](https://github.com/m-cahill/starlab/actions/runs/24637019658) — **success**; **merge-boundary `main` CI** [`24637049478`](https://github.com/m-cahill/starlab/actions/runs/24637049478) on merge commit `f5e4521d…` — **success**. **Superseded** failed PR-head run — **not** merge authority: [`24623471026`](https://github.com/m-cahill/starlab/actions/runs/24623471026) — **failure** (Ruff format check — **not** merge authority).
- **Opened** **`PX1-M04`** as the **packaging / proof governance** milestone after **PX1-M03** successful closeout: public runtime **`docs/runtime/px1_governed_demo_proof_pack_v1.md`**; private **`docs/company_secrets/milestones/post-v1/PX1-M04/`** (plan, pack checklist, pack freeze, canonical demo selection, toolcalls) — **not** default gameplay remediation; **not** new industrial campaign; **not** operator-local pack assembly; **not** **PX1-M05** or **v2** auto-open.
- **Ledger:** §1 quick scan + §7 + §11 + §23 — **`current milestone`** → **`PX1-M04`**; **PX1-M03** remains **closed** with **`demo-ready-candidate-selected`** (**preserved**). Private workflow record: **`PX1-M04_run1.md`**.

### 2026-04-19 — **PX1-M03** governance closeout — merged to `main` ([PR #91](https://github.com/m-cahill/starlab/pull/91)) — **closed**; **`current milestone`** → **None**

- **Closed** **PX1-M03** on `main` with governance closeout: ledger + private **`PX1-M03_summary.md`** / **`PX1-M03_audit.md`** / **`PX1-M03_run2.md`** — **frozen-protocol** operator-local **`local_live_sc2`** remediation evaluation concluded with **`demo-ready-candidate-selected`** for **`px1_m01_weighted_refit_rl_bootstrap_v1`** (**6**/**10** wins, **6** replay-backed, **≥1** watchable win); optional media registration on the watchable win points to operator-local **`out/px1_m03_operator_watchable.mp4`** (same winning run **`runs/scripted_01`**, re-sealed registration metadata — **not** committed). Authoritative series root (operator-local): **`out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m03_eval_series_post_watchable_capture_2026_04_19`**. **PX1-M02** **`no-candidate-selected`** — **preserved**; **not** reinterpreted.
- **Post-closeout ledger:** §1 quick scan + §7 + §11 + §23 — **PX1-M03** **closed**; **`current milestone`** = **None**; **`PX1-M04`–`PX1-M05`** **planned / not yet opened**; **PX1-M04** **does not** open automatically; **v2** **not** opened.

### 2026-04-18 — **PX1-M03** Candidate Strengthening & Demo Readiness Remediation — merged to `main` ([PR #90](https://github.com/m-cahill/starlab/pull/90)) — PR1 **open** (not closeout)

- **Merged** [PR #90](https://github.com/m-cahill/starlab/pull/90) to `main`; merge commit `fdd2b9d9b76e2816b4e99e793d8b7a37ef4fd64b`; **final PR head** `b5e79274173b388903020d807fd0cb149394c16a`; **authoritative PR-head CI** [`24610112326`](https://github.com/m-cahill/starlab/actions/runs/24610112326) — **success**; **merge-boundary `main` CI** [`24610141976`](https://github.com/m-cahill/starlab/actions/runs/24610141976) on merge commit `fdd2b9d9…` — **success**. **Superseded** failed PR-head runs — **not** merge authority: [`24609919629`](https://github.com/m-cahill/starlab/actions/runs/24609919629); [`24610058969`](https://github.com/m-cahill/starlab/actions/runs/24610058969).
- **Opened** **`PX1-M03`** as a **corrective** milestone after **PX1-M02** closed with **`no-candidate-selected`**: recharter moves governed demo/video proof to **`PX1-M04`**; adds optional **`PX1-M05`**; public runtime **`docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`**; deterministic **`px1_demo_readiness_protocol.json`** / **`px1_demo_readiness_evidence.json`** emitters; hybrid **`burnysc2_policy`** `px1_m03_hybrid_v1`; private **`docs/company_secrets/milestones/post-v1/PX1-M03/`** plans — **not** **PX1-M04**/**v2** auto-open; **not** winning-video proof.
- **Delivered:** §1 quick scan + §7 PX1 roadmap + §11 + §23 — **`current milestone`** → **`PX1-M03`**; **PX1-M02** remains **closed** with **`no-candidate-selected`** (**not** reinterpreted).
- **Post-PR1 ledger:** **`PX1-M03`** **open** on `main` until operator remediation reruns + later closeout PR — **not** operator reruns in PR1. Private workflow record: **`PX1-M03_run1.md`**.

### 2026-04-18 — **PX1-M02** governance closeout — merged to `main` ([PR #89](https://github.com/m-cahill/starlab/pull/89)) — **closed**; **`current milestone`** → **None** (superseded by **PX1-M03** open — see entry above)

- **Closed** **PX1-M02** on `main` with governance closeout: ledger + private **`PX1-M02_summary.md`** / **`PX1-M02_audit.md`** / **`PX1-M02_run2.md`** — **bounded play-quality evaluation only**; final authoritative **protocol v2** **`local_live_sc2`** series **`no-candidate-selected`** (**0**/**10** wins); replay-backed runs; **not** demo/video (**PX1-M03**); **not** **v2**. Authoritative operator-local series root: **`out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m02_eval_series_final`**.
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PX1-M02** **closed**; **`current milestone`** = **None**; **`PX1-M03`–`PX1-M04`** **planned / not yet opened**; **v2** **not** opened.

### 2026-04-18 — **PX1-M02** PR1 merged to `main` ([PR #88](https://github.com/m-cahill/starlab/pull/88)) — protocol freeze + emitters — **open** (not closeout)

- **Merged** [PR #88](https://github.com/m-cahill/starlab/pull/88) to `main`; merge commit `5521d8b8671e72a5f9297148ff972b13b75e408a` merged **2026-04-18T01:49:56Z** (UTC); **final PR head** `f44c66add532cc73b5dfa99ca26eb7640f961ae6`; **authoritative PR-head CI** [`24594170354`](https://github.com/m-cahill/starlab/actions/runs/24594170354) — **success**; **merge-boundary `main` CI** [`24594198357`](https://github.com/m-cahill/starlab/actions/runs/24594198357) on merge commit `5521d8b…` — **success**. **Superseded** PR-head runs — **not** merge authority: [`24594051547`](https://github.com/m-cahill/starlab/actions/runs/24594051547); [`24594125553`](https://github.com/m-cahill/starlab/actions/runs/24594125553).
- **`PX1-M02`** remains **open** on `main` (protocol freeze + runtime contract + deterministic emitters + synthetic fixtures + readiness checkpoint); **not** milestone closeout; **not** the live SC2 evaluation series; **not** demo-candidate selection claim; **`PX1-M03`–`PX1-M04`** **planned / not yet opened**; **v2** **not** opened.
- **Post-merge ledger:** §11 **PX1-M02** PR pins; private **`PX1-M02_run1.md`** — **not** operator **`out/`** play-quality evidence.

### 2026-04-17 — **PX1-M02** Play-Quality Evaluation & Demo Candidate Selection — **open** (PR1 — protocol freeze + emitters; pre-merge on branch)

- **Opened** **`PX1-M02`** on branch **`px1-m02-play-quality-demo-candidate-selection`**: **`current milestone`** → **`PX1-M02`**.
- **Delivered:** public runtime **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**; **`starlab.sc2.emit_px1_play_quality_protocol`** + **`starlab.sc2.emit_px1_play_quality_evidence`**; synthetic **`tests/fixtures/px1_m02/`** + **`tests/test_px1_m02_play_quality_protocol_evidence.py`**; private **`PX1-M02_plan.md`**, **`PX1-M02_protocol_freeze.md`**, **`PX1-M02_operator_checklist.md`**, **`PX1-M02_execution_readiness.md`**, **`PX1-M02_toolcalls.md`** — **not** operator **`out/`** evidence; **not** live SC2 in default CI; **not** **PX1-M03** or **v2**.
- **Authoritative merge + CI** — **2026-04-18** entry above ([PR #88](https://github.com/m-cahill/starlab/pull/88)).

### 2026-04-17 — **PX1-M01** milestone closeout — merged to `main` ([PR #87](https://github.com/m-cahill/starlab/pull/87)) — **closed**; **`current milestone`** → **None**

- **Closed** **PX1-M01** on `main` with **governance** closeout: ledger + private **`PX1-M01_summary.md`** / **`PX1-M01_audit.md`** — **does not** open **PX1-M02** or **v2**. **Authoritative** operator-local run: **`campaign_id`** `px1_m01_full_run_2026_04_17_a`, **`execution_id`** `px1_m01_exec_001`, **`local_live_sc2`**; Tranche A **completed within scope**; Tranche B **completed within scope**; full-run **`threshold-met`** — **not** play-quality (**PX1-M02**) or demo/video (**PX1-M03**).
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PX1-M01** **closed**; **`current milestone`** = **None**. **Authoritative closeout PR-head CI** and **merge-boundary `main` CI** — see private **`PX1-M01_run2.md`**.

### 2026-04-17 — **PX1-M01** Full Industrial Campaign Execution Evidence — **open** on `main` — merged ([PR #85](https://github.com/m-cahill/starlab/pull/85)) — threshold freeze + runtime contract

- **Merged** [PR #85](https://github.com/m-cahill/starlab/pull/85) to `main`; merge commit `2b97b2afe556ad61a56b6604566ef935a70669d7`; **final PR head** `135b5c9688a3d3a6b3274157d5f6130a83e66a34`; **authoritative PR-head CI** [`24589931847`](https://github.com/m-cahill/starlab/actions/runs/24589931847) — **success**; **merge-boundary `main` CI** [`24589979870`](https://github.com/m-cahill/starlab/actions/runs/24589979870) on merge commit `2b97b2a…` — **success**.
- **Opened** **PX1-M01** on `main`: **`current milestone`** → **PX1-M01**; **frozen** PX1 full-run threshold block in **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`** and private **`PX1-M01_threshold_freeze.md`** — **before** authoritative operator execution.
- **Delivered:** **`docs/runtime/px1_full_industrial_campaign_execution_evidence_v1.md`**; **Post-PV1 (PX1)** quick scan + roadmap + execution evidence subtable; §1 quick scan + §11 **PX1-M01** section; **`tests/fixtures/px1_m01/px1_m01_campaign_protocol.json`** (synthetic CI-safe protocol mirror); private **`PX1-M01_plan.md`**, **`PX1-M01_operator_checklist.md`**, **`PX1-M01_toolcalls.md`**, **`PX1-M01_execution_readiness.md`** — **not** default CI live SC2; **not** **`threshold-met`** before real run; **not** **PX1-M02** auto-open.
- **Preserved:** closed **v1** (**M00–M61**); closed **PV1**; bounded **PV1** outcome (**unchanged**); closed **PX1-M00** — **not** reinterpreted.
- **Post-merge ledger:** §1 quick scan + §23 + §11 — **PX1-M01** **open**; **PR2** closes milestone after **real** execution evidence.

### 2026-04-17 — **PX1-M01** post-merge ledger + CI record (documentation-only)

- **Recorded** authoritative [PR #85](https://github.com/m-cahill/starlab/pull/85) SHAs + CI run IDs in §11 / §23; private **`PX1-M01_run1.md`** — **not** live SC2 execution; **not** **`threshold-met`**; **not** **PX1-M01** closeout.

### 2026-04-17 — **PX1-M00** milestone closeout — merged to `main` ([PR #84](https://github.com/m-cahill/starlab/pull/84)) — **closed**; **`current milestone`** → **None**

- **Closed** **PX1-M00** on `main` with **governance** closeout only: **no** new SC2 execution; **no** demo recording; **no** opening **PX1-M01** or **v2**. **PX1** phase + roadmap **remain** in **Post-PV1 (PX1)**; **PX1-M01**–**M04** **planned / not yet opened**.
- **Delivered:** §1 quick scan + §11 + §23 + **Post-PV1 (PX1)** roadmap row for **PX1-M00** → **closed**; private **`PX1-M00_summary.md`** / **`PX1-M00_audit.md`**; governance test updates — **not** industrial-run or demo proof.
- **Preserved:** closed **v1** (**M00–M61**); closed **PV1**; bounded **PV1** outcome (**unchanged**); **PR #83** as **PX1-M00** implementation anchor — **not** reinterpreted.
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PX1-M00** **closed**; **`current milestone`** = **None**. **Authoritative closeout PR-head CI** and **merge-boundary `main` CI** — see closeout PR checks (recorded in **`PX1-M00_run2.md`**).

### 2026-04-17 — **PX1-M00** Full Industrial Run & Demonstration Charter — **open** on `main` — merged ([PR #83](https://github.com/m-cahill/starlab/pull/83)) — new **Post-PV1 (PX1)** phase

- **Merged** [PR #83](https://github.com/m-cahill/starlab/pull/83) to `main`; merge commit `92da98595e29499405bfee0c25f85f32114d68ad`; **final PR head** `4f0e010a5a480ab249a31a164b8d10cb84c068b0`; **authoritative PR-head CI** [`24587023204`](https://github.com/m-cahill/starlab/actions/runs/24587023204) — **success**; **merge-boundary `main` CI** [`24587086428`](https://github.com/m-cahill/starlab/actions/runs/24587086428) on merge commit `92da985…` — **success**.
- **Opened** **PX1 — Full Industrial Run & Demonstration Proof** as a **separate** post-**PV1** governed phase (**not** “Phase VIII”; **not** **M62**; **not** PV1 cleanup). **`current milestone`** → **PX1-M00** (governance-first charter; **no** operator campaign execution; **no** demo recording). **Not** milestone closeout — **PX1-M00** remains **open** until separate governance closeout.
- **Delivered:** public runtime **`docs/runtime/px1_full_industrial_run_demo_charter_v1.md`**; **Post-PV1 (PX1)** section + roadmap table ( **PX1-M01**–**M04** **planned / not opened** ); §1 quick scan + §11 + Start Here item 9; private **`PX1-M00_plan.md`** / **`PX1-M00_charter.md`** under `docs/company_secrets/milestones/post-v1/PX1-M00/`; private **`PX1-M00_run1.md`** (CI/workflow analysis — **not** closeout audit).
- **Preserved:** closed **v1** (**M00–M61**) and closed **PV1** (**PV1-M00**–**PV1-M04**) history; bounded **PV1** outcome (**unchanged**): Tranche A/B **within scope**; full-run **`threshold-not-met`** (**not** reinterpreted). **v2** remains **unopened**; **PX1 completion does not** automatically open **v2**.

### 2026-04-17 — **PV1-M04** milestone closeout — merged to `main` ([PR #81](https://github.com/m-cahill/starlab/pull/81)) — **closed**; **`current milestone`** → **None**

- **Closed** **PV1-M04** on `main` with **governance** closeout only: **no** new SC2 execution; **no** reinterpretation of **`threshold-not-met`** on **`full_run_duration_target`**. The **bounded** **PV1** campaign result remains: Tranche A **completed within scope**; Tranche B **completed within scope**; full-run threshold **`threshold-not-met`** (**separate** operator sessions — **not** reinterpreted).
- **Preserved:** [PR #79](https://github.com/m-cahill/starlab/pull/79) as the **implementation** merge (readout emitter + runtime + fixtures); **this PR** is the **milestone closeout** step (ledger + private **`PV1-M04_summary.md`** / **`PV1-M04_audit.md`**). **Does not** open **PV1-M05** or any later **PV1** row.
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PV1-M04** **closed**; **`current milestone`** = **None**. **Authoritative closeout PR-head CI** [`24549710647`](https://github.com/m-cahill/starlab/actions/runs/24549710647) on **final PR head** `99caf2156d915851df21d45a7fe1725da7094924` — **success**; **merge-boundary `main` CI** [`24549764138`](https://github.com/m-cahill/starlab/actions/runs/24549764138) on merge commit `0b2c427199ed4a42ca31119274984b8a1a456daa` — **success**.

### 2026-04-16 — **PV1-M04** Post-Campaign Analysis / Comparative Readout — merged to `main` ([PR #79](https://github.com/m-cahill/starlab/pull/79)) — **open** (not closeout)

- **Delivered:** runtime **`docs/runtime/pv1_post_campaign_readout_v1.md`**; deterministic **`pv1_post_campaign_readout.json`** / **`pv1_post_campaign_readout_report.json`** via **`python -m starlab.training.emit_pv1_post_campaign_readout`** (**aggregation only**); synthetic **`tests/fixtures/pv1_m04/`** + **`tests/test_pv1_post_campaign_readout.py`** (incl. CLI coverage for **78.0%** gate) — **not** operator-local SC2 execution; **not** **`threshold-met`** fabrication; **not** reinterpretation of **`threshold-not-met`** on **`full_run_duration_target`**.
- **Authoritative PR-head CI** [`24548939513`](https://github.com/m-cahill/starlab/actions/runs/24548939513) on **final PR head** `819cc2ea57b1fe3d27d09296aaebf6008577560c` — **success**; **superseded** [`24548853149`](https://github.com/m-cahill/starlab/actions/runs/24548853149) — **failure** (coverage gate — **not** merge authority).
- **Merge-boundary `main` CI** [`24548992189`](https://github.com/m-cahill/starlab/actions/runs/24548992189) on merge commit `d5280ee9cc69f8d7750546b7ed597e2de466f8a7` — **success**.
- **Post-merge ledger:** §1 quick scan + §7 + §11 — **PV1-M04** **open**; **PV1-M03** remains **closed**; **`current milestone`** = **PV1-M04** until separate closeout — **not** **`PV1-M04_summary.md`** / **`PV1-M04_audit.md`** in this entry.

### 2026-04-17 — **PV1-M03** milestone closeout — merged to `main` ([PR #78](https://github.com/m-cahill/starlab/pull/78)) — **closed**; honest **`threshold-not-met`**

- **Closed** **PV1-M03** on `main` with **bounded** outcome: **Tranche B completed within scope** (operator-local); **full-run threshold** = **`threshold-not-met`** — frozen **`full_run_duration_target`** was **not** satisfied because Tranche A and Tranche B ran in **separate** operator sessions (**not** reinterpreted). **Does not** claim **`threshold-met`**; **does not** open **PV1-M04**.
- **Preserved:** [PR #77](https://github.com/m-cahill/starlab/pull/77) as the **implementation** merge; **this PR** is the **milestone closeout** step (ledger + private **`PV1-M03_run1.md`** / **`PV1-M03_summary.md`** / **`PV1-M03_audit.md`**). Checkpoint receipts under `checkpoints/tranche_a_close/` and `checkpoints/tranche_b_close/` per PV1-M01 discipline (operator-local trees **not** committed by default).
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PV1-M03** **closed**; **current milestone** → **None**; **PV1-M04** **not opened**. **Authoritative closeout PR-head CI** [`24546554872`](https://github.com/m-cahill/starlab/actions/runs/24546554872) on **final PR head** `da3ba525aed7fa254cebe928e898a5bdb40c9141` — **success**; **superseded** PR-head run on earlier head [`24546550354`](https://github.com/m-cahill/starlab/actions/runs/24546550354) — **cancelled** — **not** merge authority. **Merge-boundary `main` CI** [`24546618727`](https://github.com/m-cahill/starlab/actions/runs/24546618727) on merge commit `aa06289df5a3f41c1f94292c054ab4bf82ca6abb` — **success**.

### 2026-04-17 — **PV1-M03** Tranche B / full-run threshold — merged to `main` (PR #77) — **open milestone** (not closeout)

- **Merged** [PR #77](https://github.com/m-cahill/starlab/pull/77) to `main`; merge commit `9105a7ee6dff47acfb409f4cd08ca2693e98f9f1` merged **2026-04-17T00:49:32Z** (UTC); **final PR head** `946e332a87556767a322e8cb3039d6e4a757271c`; **authoritative PR-head CI** [`24541829597`](https://github.com/m-cahill/starlab/actions/runs/24541829597) — **success**; **merge-boundary `main` CI** [`24541875605`](https://github.com/m-cahill/starlab/actions/runs/24541875605) on merge commit `9105a7e…` — **success**.
- **Delivered:** runtime **`docs/runtime/pv1_tranche_b_full_run_threshold_evidence_v1.md`**, protocol fixture **`tests/fixtures/pv1_m03/pv1_m03_campaign_protocol.json`**, **`--skip-bootstrap-phases`**, governance tests — **not** operator Tranche B execution or **`threshold-met`** in the environment that authored this PR (SC2 preconditions **not** met); **not** milestone closeout; **no** **`PV1-M03_summary.md`** / **`PV1-M03_audit.md`** as closed-milestone artifacts.
- **Post-merge ledger:** §1 quick scan + §23 + §11 — **PV1-M03** **open** on `main` (**current** milestone); **PV1-M04** **not opened**.
- **Historical note:** A **pre-merge** branch draft incorrectly implied **PV1-M03** was **closed** with a **fake** PR number; corrected **before** merge — **this** PR **#77** is the **real** merge documenting **open** implementation posture.

### 2026-04-16 — **PV1-M02** Tranche A Execution Evidence — merged to `main` (PR #76) + merge-boundary CI + ledger closeout

- **Merged** [PR #76](https://github.com/m-cahill/starlab/pull/76) to `main`; merge commit `1c79c06f70e12215da14d1b0e0b5b71beac11ffd`; **final PR head** `d6e0c9c572d26b1cbc4c8c8fb791c63c7717d574`; **authoritative PR-head CI** [`24539086056`](https://github.com/m-cahill/starlab/actions/runs/24539086056) — **success**; **merge-boundary `main` CI** [`24539635014`](https://github.com/m-cahill/starlab/actions/runs/24539635014) on merge commit `1c79c06…` — **success** (superseded PR-head run on earlier head: [`24539076254`](https://github.com/m-cahill/starlab/actions/runs/24539076254) — **cancelled** — **not** merge authority).
- **Delivered:** bounded **operator-local Tranche A** evidence contract + ledger + governance tests + protocol fixture — **not** full-run threshold; **not** **PV1-M03**; private closeout **`PV1-M02_run1.md`** / **`PV1-M02_summary.md`** / **`PV1-M02_audit.md`** under `docs/company_secrets/milestones/post-v1/PV1-M02/`.
- **Post-closeout ledger (on `main` immediately after PV1-M02 merge):** §1 quick scan + §23 + §11 — **PV1-M02** **closed**; **current milestone on `main`** → **None** (no PV1-M03 merge on `main` yet); **PV1-M03** / **PV1-M04** **not opened on `main`** — **integration-branch** PV1-M03 implementation / honest-blocked operator posture is **separate** — **superseded** for **current milestone** after **PV1-M03** [PR #77](https://github.com/m-cahill/starlab/pull/77) merged (**2026-04-17**; see §23 entry above).

### 2026-04-16 — **PV1-M02** Tranche A Execution Evidence — governance + runtime (integration branch, pre-merge)

- **Branch:** `pv1-m02-tranche-a-execution-evidence` — [PR #76](https://github.com/m-cahill/starlab/pull/76) to `main`.
- **In-repo:** runtime **`docs/runtime/pv1_tranche_a_execution_evidence_v1.md`**; reproducible protocol fixture **`tests/fixtures/pv1_m02/pv1_m02_campaign_protocol.json`**; ledger §11 / quick scan / **Post-v1 (PV1)** roadmap + evidence surfaces — superseded by merge closeout entry above.
- **Operator-local:** reference campaign **`pv1_m02_tranche_a_2026_04_16`**, execution **`pv1_m02_exec_001`**, **`tranche_a_operator_note.md`**, PV1-M01 inspection JSON — raw **`out/`** trees **not** committed unless policy allows.

### 2026-04-16 — **PV1-M01** merged to `main` (PR #74) + merge-boundary CI + ledger closeout

- **Merged** [PR #74](https://github.com/m-cahill/starlab/pull/74) to `main` at **2026-04-16T21:37:31Z** (UTC); merge commit `a0cb05d96c1e57b58992efd07c4bd841be539aba`; **final PR head** `dfe1e7761eb2155c3fc6eb5604f8b40c5337a4c5`; **authoritative PR-head CI** [`24535255531`](https://github.com/m-cahill/starlab/actions/runs/24535255531) — **success**; **merge-boundary `main` CI** [`24535324891`](https://github.com/m-cahill/starlab/actions/runs/24535324891) on merge commit `a0cb05d…` — **success**.
- **Delivered:** inspection/reference emitters + runtime contract + fixtures — **not** campaign execution, **not** Tranche A evidence.
- **Post-closeout ledger:** §1 quick scan + §23 + §11 — **PV1-M01** **closed**; **current milestone** → **None**; **PV1-M02**–**M04** **not opened**; private **`PV1-M01_summary.md`** / **`PV1-M01_audit.md`** / **`PV1-M01_run1.md`** under `docs/company_secrets/milestones/post-v1/PV1-M01/`.
- **Not merge authority:** ledger-only follow-up PR CI — cite separately from merge-boundary [`24535324891`](https://github.com/m-cahill/starlab/actions/runs/24535324891) on `a0cb05d…` when recording narrative-only alignment.

### 2026-04-16 — **PV1-M01** Campaign Observability & Checkpoint Discipline — tooling (pre-merge)

- **PV1-M01** opens as a **narrow pre-execution tooling** milestone (**not** Tranche A execution evidence).
- **In-repo:** `starlab.training.emit_tranche_checkpoint_receipt`, `starlab.training.emit_campaign_observability_index`; runtime `docs/runtime/pv1_campaign_observability_checkpoint_discipline_v1.md`; fixture tests under `tests/fixtures/pv1_m01/`.
- **Public ledger:** **Post-v1 (PV1)** roadmap + **PV1 evidence surfaces** subtable; §11 **PV1-M01** stub; quick-scan **current milestone** → **PV1-M01** while this milestone is open on the integration branch.
- **Explicit non-claims:** **not** benchmark integrity; **not** replay↔execution equivalence; **not** ladder/public proof; **not** merge-gate live SC2; inspection helpers **do not** fabricate missing campaign artifacts.

### 2026-04-16 — **PV1-M00** merged to `main` (PR #73) + merge-boundary CI

- **Merged** [PR #73](https://github.com/m-cahill/starlab/pull/73) to `main` at **2026-04-16T20:20:27Z** (UTC); merge commit `77118675a6f9f76e7cd466269c8d2a19ace3552f`; **final PR head** `2f80cfa9c1d329b520ebb99280bb12c21bfaa81d`; **authoritative PR-head CI** [`24531908110`](https://github.com/m-cahill/starlab/actions/runs/24531908110) — **success**; **merge-boundary `main` CI** [`24532016096`](https://github.com/m-cahill/starlab/actions/runs/24532016096) on merge commit `77118675…` — **success**.
- **Post-merge:** **PV1-M01**–**M04** remain **roadmap placeholders** only (**not** opened by this merge).
- **Not merge authority:** doc-only follow-up commits on `main` after this boundary — cite separately from [`24532016096`](https://github.com/m-cahill/starlab/actions/runs/24532016096) on `77118675…` when used as merge evidence.

### 2026-04-16 — **PV1-M00** Post-v1 Industrial Campaign Charter & Success Criteria — governance (charter milestone)

- **Post-v1 / PV1:** Opens the **rechartered** post-v1 program line **PV1 — Long Industrial Campaign & Scaling Evidence** under milestone ids **`PV1-MNN`** (**not** **M62**; **not** “Phase VIII” of the original v1 phase map). Public ledger: **Post-v1 (PV1)** section (after §7 milestone table), §11 **PV1-M00**, quick-scan rows, Start Here item 8; **PV1-M01**–**M04** are **roadmap placeholders** only (**planned** / **optional** / **not yet opened**).
- **Private working surface (local):** `docs/company_secrets/milestones/post-v1/PV1-M00/` — `PV1-M00_charter.md`, `PV1-M00_plan.md` (not public source of truth).
- **Non-goals:** **no** long-run campaign execution in-repo; **no** new benchmark / equivalence / ladder / live-CI claims; **no** new **PV1** git tag naming convention (deferred).

### 2026-04-16 — **M61** SC2 foundation release lock & v1 proof pack — public closeout on `main` (post-merge evidence alignment)

- **Product merge authority (unchanged):** [PR #72](https://github.com/m-cahill/starlab/pull/72) merged to `main` at **2026-04-16T05:33:27Z** (UTC); merge commit `35d7734d14113adf206390f153f517a93d7d41ba`; **final PR head** `bb5a216e83f6048cfa0ad9b437d74d367ff59a5b`; **authoritative PR-head CI** [`24493016581`](https://github.com/m-cahill/starlab/actions/runs/24493016581) — **success**; **merge-boundary `main` CI** [`24493963087`](https://github.com/m-cahill/starlab/actions/runs/24493963087) on merge commit `35d7734…` — **success**; tag **`v0.0.61-m61`** on merge commit `35d7734…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI).
- **Evidence alignment (this closeout):** ledger + runtime contract updated so **M61** and the **M00–M61** **v1** arc read as **closed** with **operator-local** campaign **`m61_evidence_2026_04_16_a`** / **`m61_exec_001`**, **`--post-bootstrap-protocol-phases`**, watchable **M44**, proof pack + audit **`ready_within_scope`** — **not** new global claims; **no** **M62** stub.
- **Not merge-boundary authority:** any subsequent **doc-only** `main` CI runs or **tag-push** workflows after the merge boundary — cite separately from [`24493963087`](https://github.com/m-cahill/starlab/actions/runs/24493963087) on `35d7734…` (e.g. later ledger alignment commits if present).
- **Closeout:** `M61_run1.md`, `M61_summary.md`, `M61_audit.md` (**local only** under `docs/company_secrets/` — **not** committed); §1 / quick scan / §6–§8 / §7 **M61** **Complete** / §11 **M61** **closed** / §18 closeout table + **M61** CI block / §23; `docs/runtime/sc2_foundation_release_lock_v1.md` (**M61** **closed**); governance tests (`tests/test_m58_live_sc2_in_ci_hardening_cost_guardrails.py`) ledger §11 checks.

### 2026-04-16 — **M60** Audit hardening & v2 readiness v1 — merged to `main` (PR #71) + milestone closeout

- **Merged** [PR #71](https://github.com/m-cahill/starlab/pull/71) to `main` at **2026-04-16T03:57:51Z** (UTC); merge commit `9ef4e049f1e04ee36952be53647d48c649ad6915`; **final PR head** `c7f615639bc1b26d6d2813bc55f078a048cab405`; **authoritative PR-head CI** [`24491193150`](https://github.com/m-cahill/starlab/actions/runs/24491193150) — **success**; **merge-boundary `main` CI** [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939) on merge commit `9ef4e04…` — **success**; tag **`v0.0.60-m60`** on merge commit `9ef4e04…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m60-audit-hardening-v2-readiness` **deleted** after merge.
- **M60 proof (narrow, structural/diligence):** `docs/audit/m60_v2_readiness_findings.md`; `docs/runtime/v2_readiness_audit_hardening_v1.md`; private **`starlab.training._full_local_training_campaign_execution`**; **`tests/test_m60_v2_readiness_guardrails.py`** — **not** a new governed product artifact family; **not** replay↔execution equivalence; **not** benchmark integrity; **not** live SC2 in CI expansion; **not** ladder/public performance.
- **Closeout:** `M60_run1.md`, `M60_summary.md`, `M60_audit.md` (**local only** under `docs/company_secrets/` — **not** committed); §1 / quick scan / §6 / §7 **M60** **Complete** + tag **`v0.0.60-m60`** / §11 current milestone pointer **M61** (**closed** after operator-local **`ready_within_scope`** evidence; see **M61** public closeout) + **M60** **closed** section / §18 / §23; `docs/runtime/v2_readiness_audit_hardening_v1.md` header (**M60** **closed** on `main`); governance tests (`tests/test_m58_live_sc2_in_ci_hardening_cost_guardrails.py`) ledger pointer checks.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24491232939`](https://github.com/m-cahill/starlab/actions/runs/24491232939) on merge commit `9ef4e04…`.

### 2026-04-16 — **M59** Ladder/public evaluation protocol & evidence surface v1 — merged to `main` (PR #70) + milestone closeout

- **Merged** [PR #70](https://github.com/m-cahill/starlab/pull/70) to `main` at **2026-04-16T02:45:33Z** (UTC); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; **final PR head** `074598af81b1c4ce7f3702b4002daacf9adb6bf3`; **authoritative PR-head CI** [`24488983360`](https://github.com/m-cahill/starlab/actions/runs/24488983360) — **success**; **merge-boundary `main` CI** [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on merge commit `319bc3d…` — **success**; superseded **failure** PR-head [`24488932004`](https://github.com/m-cahill/starlab/actions/runs/24488932004) — Ruff format — **not** merge authority for final head; tag **`v0.0.59-m59`** on merge commit `319bc3d…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m59-ladder-public-evaluation-protocol-evidence-surface-v1` **deleted** after merge.
- **M59 proof (narrow, bounded):** runtime `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md`; `starlab.sc2` deterministic **`ladder_public_evaluation_protocol.json`** / **`ladder_public_evaluation_protocol_report.json`** (contracts **`starlab.ladder_public_evaluation_protocol.v1`**) + **`ladder_public_evaluation_evidence.json`** / **`ladder_public_evaluation_evidence_report.json`** (contracts **`starlab.ladder_public_evaluation_evidence.v1`**); **exactly one** bounded protocol profile **`starlab.m59.protocol_profile.single_candidate_public_eval_v1`**; fixture tests + synthetic `tests/fixtures/m59/` — **not** ladder/public **performance** proof; **not** benchmark integrity; **not** replay↔execution equivalence; **not** live-SC2-in-CI expansion; **not** automated ladder play or scraping.
- **Closeout:** `M59_run1.md`, `M59_summary.md`, `M59_audit.md` (**local only** under `docs/company_secrets/` — **not** committed); §1 / quick scan / Phase VII artifact-contract index (M52–M59) / §6 / §7 **M59** **Complete** + tag **`v0.0.59-m59`** / §11 current milestone pointer **M61** (**closed** after **M61** release-lock evidence; see **M61** public closeout) after **M60** closeout + **M59** **closed** section / §18 / §23; `docs/runtime/ladder_public_evaluation_protocol_evidence_surface_v1.md` header (**M59** **closed** on `main`); governance tests (`tests/test_m58_live_sc2_in_ci_hardening_cost_guardrails.py`, `tests/test_m57_live_sc2_in_ci_charter_controlled_runner.py`, `tests/test_m59_ladder_public_evaluation_protocol_evidence_surface.py`) ledger pointer checks.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24489229014`](https://github.com/m-cahill/starlab/actions/runs/24489229014) on merge commit `319bc3d…`.

### 2026-04-16 — **M58** Live SC2 in CI hardening & cost guardrails v1 — merged to `main` (PR #69) + milestone closeout

- **Merged** [PR #69](https://github.com/m-cahill/starlab/pull/69) to `main` at **2026-04-16T01:14:18Z** (UTC); merge commit `3a6f13910dc8056cb0d88161796dd5fe7888629d`; **final PR head** `4d8fa3e6cb067b9784efc01f7668f777078b5a2d`; **authoritative PR-head CI** [`24485185914`](https://github.com/m-cahill/starlab/actions/runs/24485185914) — **success**; **merge-boundary `main` CI** [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247) on merge commit `3a6f139…` — **success**; tag **`v0.0.58-m58`** on merge commit `3a6f139…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m58-live-sc2-in-ci-hardening-cost-guardrails` **retained** on `origin`.
- **M58 proof (narrow, bounded):** runtime `docs/runtime/live_sc2_in_ci_hardening_cost_guardrails_v1.md`; `starlab.sc2` deterministic **`live_sc2_in_ci_hardening_guardrails.json`** / **`live_sc2_in_ci_hardening_guardrails_report.json`** (contract **`starlab.live_sc2_in_ci_hardening_guardrails.v1`**); **`live_sc2_in_ci_preflight_receipt.json`** / **`live_sc2_in_ci_preflight_receipt_report.json`** (contract **`starlab.live_sc2_in_ci_preflight_receipt.v1`**); **exactly one** guardrail profile **`starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1`**; optional **`.github/workflows/live-sc2-controlled-runner.yml`** hardened (**`workflow_dispatch` only**; **30** min job timeout; **7** day artifact retention; **`contents: read`**; preflight-before-runner; explicit **`confirm_live_sc2`** for **`local_live_sc2`**; GitHub **concurrency** + **M58** advisory lockfile under the output dir) — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof; **not** ladder/public evaluation (**M59** stub).
- **Closeout:** `M58_run1.md`, `M58_summary.md`, `M58_audit.md`; `M58_plan.md` **closed**; §1 / quick scan / Phase VII bounded live-SC2 **runner + guardrail** tables / §6 / §7 **M58** **Complete** + tag **`v0.0.58-m58`** / §11 current milestone pointer **M59** (**stub/planned**) + **M58** **closed** section / §18 / §23; `docs/runtime/live_sc2_in_ci_hardening_cost_guardrails_v1.md` header (**M58** **closed** on `main`); governance tests (`tests/test_m58_live_sc2_in_ci_hardening_cost_guardrails.py`, `tests/test_m57_live_sc2_in_ci_charter_controlled_runner.py`) ledger pointer checks. **Non-public** milestone artifacts under `docs/company_secrets/` exist **locally only** — **not** committed.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24486698247`](https://github.com/m-cahill/starlab/actions/runs/24486698247) on merge commit `3a6f139…`.

### 2026-04-15 — **M57** Narrow live SC2 in CI charter & controlled runner v1 — merged to `main` (PR #68) + milestone closeout

- **Merged** [PR #68](https://github.com/m-cahill/starlab/pull/68) to `main` at **2026-04-15T21:32:49Z** (UTC); merge commit `29c383f85f380d2eb2a6b2a411aa7c3262f2bc0d`; **final PR head** `eaff0104f140c2468bc6382984cd7e25f7323aa7`; **authoritative PR-head CI** [`24479060243`](https://github.com/m-cahill/starlab/actions/runs/24479060243) — **success**; **merge-boundary `main` CI** [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on merge commit `29c383f…` — **success**; tag **`v0.0.57-m57`** on merge commit `29c383f…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m57-live-sc2-in-ci-charter-controlled-runner` **retained** on `origin`.
- **M57 proof (narrow, bounded):** runtime `docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md`; `starlab.sc2` deterministic **`live_sc2_in_ci_charter.json`** / **`live_sc2_in_ci_charter_report.json`** (contract **`starlab.live_sc2_in_ci_charter.v1`**); **`live_sc2_in_ci_controlled_runner_receipt.json`** / **`live_sc2_in_ci_controlled_runner_receipt_report.json`** (contract **`starlab.live_sc2_in_ci_controlled_runner_receipt.v1`**) wrapping **`run_local_live_play_validation`** (**M44**); **exactly one** runner profile **`starlab.m57.runner_profile.m44_single_validation_v1`**; **M43** candidates + explicit weights only; optional **`.github/workflows/live-sc2-controlled-runner.yml`** (`workflow_dispatch` only — **not** required CI) — **not** default merge-gate live SC2; **not** global live-SC2-in-CI proof; **not** benchmark-integrity / **M52**–**M54** replay↔execution equivalence substitute.
- **Closeout:** `M57_run1.md`, `M57_summary.md`, `M57_audit.md`; `M57_plan.md` **closed**; §1 / quick scan / Phase VII bounded live-SC2 runner profile table / §6 / §7 **M57** **Complete** + tag **`v0.0.57-m57`** / §11 current milestone pointer **M58** (**stub/planned**) + **M57** **closed** section / §18 / §23; `docs/runtime/live_sc2_in_ci_charter_controlled_runner_v1.md` header (**M57** **closed** on `main`); governance tests (`tests/test_m57_live_sc2_in_ci_charter_controlled_runner.py`, `tests/test_m55_benchmark_integrity_charter.py`, `tests/test_m56_benchmark_integrity_evidence_reproducibility_gates.py`) ledger pointer checks. **Non-public** milestone artifacts under `docs/company_secrets/` exist **locally only** — **not** committed.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24479514905`](https://github.com/m-cahill/starlab/actions/runs/24479514905) on merge commit `29c383f…`.

### 2026-04-15 — **M56** Benchmark integrity evidence & reproducibility gates v1 — merged to `main` (PR #67) + milestone closeout

- **Merged** [PR #67](https://github.com/m-cahill/starlab/pull/67) to `main` at **2026-04-15T20:07:56Z** (UTC); merge commit `bd7da9a6229fa067217dd04db918972a5ec73caf`; **final PR head** `2c5d23b063f42bddecdc175721e8233e71938984`; **authoritative PR-head CI** [`24474743293`](https://github.com/m-cahill/starlab/actions/runs/24474743293) — **success**; **merge-boundary `main` CI** [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843) on merge commit `bd7da9a…` — **success**; superseded **failure** PR-head [`24474659745`](https://github.com/m-cahill/starlab/actions/runs/24474659745) — Ruff format — **not** merge authority for final head; tag **`v0.0.56-m56`** on merge commit `bd7da9a…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m56-benchmark-integrity-evidence-reproducibility-gates` **retained** on `origin`.
- **M56 proof (narrow, bounded):** runtime `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md`; `starlab.benchmark_integrity` deterministic **`benchmark_integrity_evidence.json`** / **`benchmark_integrity_evidence_report.json`** (contract **`starlab.benchmark_integrity_evidence.v1`**) + **`benchmark_integrity_reproducibility_gates.json`** / **`benchmark_integrity_reproducibility_gates_report.json`** (contract **`starlab.benchmark_integrity_reproducibility_gates.v1`**); CLIs `python -m starlab.benchmark_integrity.emit_benchmark_integrity_evidence` and `python -m starlab.benchmark_integrity.emit_benchmark_integrity_gates`; **exactly one** scope **`starlab.m56.scope.fixture_only_baseline_chain_v1`**; **exactly one** gate pack **`starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`**; M55-reserved evidence classes; explicit artifact paths only — **not** global benchmark integrity proof; **not** M52–M54 replay↔execution equivalence substitute; **not** live SC2 in CI / ladder / merge-bar claims.
- **Closeout:** `M56_run1.md`, `M56_summary.md`, `M56_audit.md`; `M56_plan.md` **closed**; §1 / quick scan / §6 Phase VII + bounded benchmark-integrity tables / §7 **M56** **Complete** + tag **`v0.0.56-m56`** / §11 current milestone pointer **M57** (**stub/planned**) + **M56** **closed** section / §18 / §23; `docs/runtime/benchmark_integrity_evidence_reproducibility_gates_v1.md` header (**M56** **closed** on `main`); governance tests (`tests/test_m55_benchmark_integrity_charter.py`, `tests/test_m56_benchmark_integrity_evidence_reproducibility_gates.py`) ledger pointer checks. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime contract). **Non-public** milestone artifacts under `docs/company_secrets/` exist **locally only** — **not** committed.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24475796843`](https://github.com/m-cahill/starlab/actions/runs/24475796843) on merge commit `bd7da9a…`.

### 2026-04-15 — **M55** Benchmark integrity charter & split-governance controls v1 — merged to `main` (PR #66) + milestone closeout

- **Merged** [PR #66](https://github.com/m-cahill/starlab/pull/66) to `main` at **2026-04-15T19:01:02Z** (UTC); merge commit `625dd756f09ceb4aebe8d5f3c60ea216f9cab98e`; **final PR head** `f7b1306de78b0a27b7f6095be55125630ded0aaa`; **authoritative PR-head CI** [`24472349322`](https://github.com/m-cahill/starlab/actions/runs/24472349322) — **success**; **merge-boundary `main` CI** [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on merge commit `625dd75…` — **success**; superseded **failure** PR-head [`24472253485`](https://github.com/m-cahill/starlab/actions/runs/24472253485) — Ruff format — **not** merge authority for final head; tag **`v0.0.55-m55`** on merge commit `625dd75…` (annotated tag push is a **`push` event on the tag**, **not** the merge-push `main` boundary for CI; any tag-triggered workflow runs are **not** merge-boundary authority); branch `m55-benchmark-integrity-charter-split-governance-controls` **retained** on `origin`.
- **M55 proof (narrow, charter-only):** runtime `docs/runtime/benchmark_integrity_charter_v1.md`; `starlab.benchmark_integrity` deterministic **`benchmark_integrity_charter.json`** / **`benchmark_integrity_charter_report.json`**; CLI `python -m starlab.benchmark_integrity.emit_benchmark_integrity_charter`; contract **`starlab.benchmark_integrity_charter.v1`**; six **split_governance_controls** (one entry per family); **evidence_classes_reserved_for_m56** — **not** benchmark integrity proved; **not** M56 reproducibility gates; **not** live SC2 in CI / ladder claims; **not** merge-bar semantics; **not** a substitute for closed **M52**–**M54** replay↔execution equivalence.
- **Closeout:** `M55_run1.md`, `M55_summary.md`, `M55_audit.md`; `M55_plan.md` **closed**; §1 / quick scan / §6 **Benchmark integrity track** + **Phase VII track separation** / §7 **M55** **Complete** + tag **`v0.0.55-m55`** / §8 intent map / §11 current milestone pointer **M56** (**stub/planned**) + **M55** **closed** section / §18 / §23; `docs/runtime/benchmark_integrity_charter_v1.md` ledger alignment (`benchmark_integrity_charter_v1.md` header: **M55** **closed** on `main`); governance tests (`tests/test_m55_benchmark_integrity_charter.py`) ledger pointer checks. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime charter). **Non-public** milestone artifacts under `docs/company_secrets/` exist **locally only** — **not** committed.
- **Post-closeout `main` CI:** any run from a **subsequent single closeout commit** updating the public ledger after the merge boundary — **success** or **failure** — is **not** merge-boundary authority vs [`24472759632`](https://github.com/m-cahill/starlab/actions/runs/24472759632) on merge commit `625dd75…`.

### 2026-04-15 — **M54** Replay↔execution equivalence audit & acceptance gates v1 — merged to `main` (PR #65) + milestone closeout

- **Merged** [PR #65](https://github.com/m-cahill/starlab/pull/65) to `main` at **2026-04-15T07:38:15Z** (UTC); merge commit `773dd1982f28f92512785ce0ab349b7c625f4c3d`; **final PR head** `70f4f2d51049948197863e76e806cc1adbc903aa`; **authoritative PR-head CI** [`24441617561`](https://github.com/m-cahill/starlab/actions/runs/24441617561) — **success**; **merge-boundary `main` CI** [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on merge commit `773dd19…` — **success**; tag **`v0.0.54-m54`**; branch `m54-replay-execution-equivalence-audit-acceptance-gates` **deleted** after merge.
- **M54 proof (narrow):** runtime `docs/runtime/replay_execution_equivalence_audit_acceptance_gates_v1.md`; `starlab.equivalence` deterministic `replay_execution_equivalence_audit.json` / `replay_execution_equivalence_audit_report.json`; gate pack **`starlab.m54.gatepack.identity_binding_acceptance_v1`**; CLI `python -m starlab.equivalence.emit_replay_execution_equivalence_audit` — **consumes** M53 evidence (canonical SHA-256), optional M53 report cross-check — profile-scoped outcomes + descriptive merge-bar language only — **not** universal replay↔execution equivalence; **not** benchmark integrity; **not** live SC2 in CI; **not** ladder/public performance; **not** GitHub branch protection.
- **Closeout:** `M54_run1.md`, `M54_summary.md`, `M54_audit.md`; `M54_plan.md` **closed**; §1 / quick scan / Phase VII profile + **bounded equivalence gatepacks** table / §6–§8 / §7 / §11 / §18 / §23; §7 **M54** **Complete** + tag column **v0.0.54-m54**; current milestone pointer **M55** (**stub/planned** — benchmark-integrity charter); annotated tag **`v0.0.54-m54`** on merge commit `773dd19…`; **M55** stub folder (`M55_plan.md`, `M55_toolcalls.md`) only. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime audit / evidence / charter cross-links).
- **Post-closeout `main` CI** (ledger closeout commit `c20eca7a9f4a975fcccdbdd59766453b3eb0ebc2`): [`24442548064`](https://github.com/m-cahill/starlab/actions/runs/24442548064) — **success** — **not** merge-boundary authority vs [`24442394865`](https://github.com/m-cahill/starlab/actions/runs/24442394865) on merge commit `773dd19…`. Annotated tag **`v0.0.54-m54`** on `773dd19…` does not, by itself, trigger an additional `CI` run (workflow is **`on.push`** to **`main`**).

### 2026-04-15 — **M53** Replay↔execution equivalence evidence surface v1 — merged to `main` (PR #64) + milestone closeout

- **Merged** [PR #64](https://github.com/m-cahill/starlab/pull/64) to `main` at **2026-04-15T05:39:22Z** (UTC); merge commit `99bd43da41ac5a4d22a3eb2f438bc8ebe93b591d`; **final PR head** `ec166ff4108af939755d5578a408b07e6a9d6bb1`; **authoritative green PR-head CI** [`24438220924`](https://github.com/m-cahill/starlab/actions/runs/24438220924) (**success**); **merge-boundary `main` CI** [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on merge commit `99bd43d…` (**success**); tag **`v0.0.53-m53`**; branch `m53-replay-execution-equivalence-evidence-surface` **deleted** after merge.
- **M53 proof (narrow):** runtime `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`; `starlab.equivalence` deterministic `replay_execution_equivalence_evidence.json` / `replay_execution_equivalence_evidence_report.json`; bounded profile registry; **`starlab.m53.profile.identity_binding_v1`**; explicit artifact-path CLI; M52 mismatch / availability vocabulary; **no** top-level pass/fail verdict — **not** universal replay↔execution equivalence; **not** M54 audit gates; **not** benchmark integrity; **not** live SC2 in CI; **not** ladder/public performance.
- **Closeout:** `M53_run1.md`, `M53_summary.md`, `M53_audit.md`; `M53_plan.md` **closed**; §1 / quick scan / Phase VII profile table / §6–§8 / §7 / §11 / §18 / **STARLAB v1**; §7 **M53** **Complete** + tag column **v0.0.53-m53**; current milestone pointer **M54** (**stub/planned** — audit / acceptance-gate milestone); annotated tag **`v0.0.53-m53`** on merge commit `99bd43d…`; **M54** stub folder (`M54_plan.md`, `M54_toolcalls.md`) only. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime evidence surface alignment).
- **Post-closeout `main` CI:** [`24438868028`](https://github.com/m-cahill/starlab/actions/runs/24438868028) on closeout commit `9827e580580237879509bf2f85e7f76d46b3d577` — **success** (public ledger + runtime docs — **not** PR #64 merge authority; merge-boundary remains [`24438374334`](https://github.com/m-cahill/starlab/actions/runs/24438374334) on `99bd43d…`). **Non-merge-boundary:** tag push **`v0.0.53-m53`** does not trigger the `CI` workflow (`on.push` is **`branches: [main]`** only).

### 2026-04-15 — **M52** V1 endgame recharter & replay↔execution equivalence charter v1 — merged to `main` (PR #63) + milestone closeout

- **Merged** [PR #63](https://github.com/m-cahill/starlab/pull/63) to `main` at **2026-04-15T03:41:47Z** (UTC); merge commit `c80a47bedcc5e607e45381d401411d9aa5e2f10b`; **final PR head** `11ba11e0c1bcb39baaec130105a1955cfcf4d703`; **authoritative green PR-head CI** [`24434922983`](https://github.com/m-cahill/starlab/actions/runs/24434922983) (**success**); **merge-boundary `main` CI** [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on merge commit `c80a47b…` (**success**); **superseded** **failure** PR-head [`24434871264`](https://github.com/m-cahill/starlab/actions/runs/24434871264) on `a938ac6…` — Ruff format — **not** merge authority for final head; branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge.
- **M52 proof (narrow):** governance + charter only — **62** milestones (**M00**–**M61**), **Phase VII**, public ledger + intent map + *Remaining v1 proof-track map*; `docs/runtime/replay_execution_equivalence_charter_v1.md`; `starlab.equivalence` deterministic `replay_execution_equivalence_charter.json` / `replay_execution_equivalence_charter_report.json` — **not** paired replay↔execution equivalence proof, **not** benchmark integrity implementation, **not** live SC2 in CI, **not** ladder/public performance.
- **Closeout:** `M52_run1.md`, `M52_summary.md`, `M52_audit.md`; `M52_plan.md` **closed**; §1 / quick scan / §6–§8 / §7 / §11 / §18 / **STARLAB v1**; §7 **M52** **Complete** + tag column **v0.0.52-m52**; current milestone pointer **M53** (**stub/planned**); annotated tag **`v0.0.52-m52`** on merge commit `c80a47b…`; **M53** stub folder (`M53_plan.md`, `M53_toolcalls.md`) only. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime charter alignment).
- **Post-closeout `main` CI:** [`24435319655`](https://github.com/m-cahill/starlab/actions/runs/24435319655) on closeout commit `9af5ccbf36f334ff9d96c030fd4ff6f6e2f016cf` — **success** (ledger + milestone artifacts + tag push — **not** PR #63 merge authority; merge-boundary remains [`24435208211`](https://github.com/m-cahill/starlab/actions/runs/24435208211) on `c80a47b…`). **Non-merge-boundary:** tag push **`v0.0.52-m52`** does not trigger the `CI` workflow (`on.push` is **`branches: [main]`** only).

### 2026-04-15 — Governance recharter: **62 milestones (M00–M61)**; **Phase VII**; **M52** charter surface (**closed** with PR #63)

- **Governance:** planned program arc expands from **53 (M00–M52)** to **62 (M00–M61)**. **Phase VII — Trust, Equivalence, Benchmark Integrity, and Release Lock** introduced for **M52**–**M61**; **Phase VI** (**M40**–**M51**) remains **closed** on `main` as the training/execution track.
- **v1 boundary:** present-tense non-claims preserved for benchmark integrity, replay↔execution equivalence, live SC2-in-CI proof, ladder/public performance — reframed as **planned within the remaining v1 arc** (not silently “post-v1”). **v2** (multi-game, AURORA/audio, broader productization) begins after **M61** per quick-scan note.
- **Artifacts:** `docs/runtime/replay_execution_equivalence_charter_v1.md`; `starlab.equivalence` emits `replay_execution_equivalence_charter.json` / `replay_execution_equivalence_charter_report.json` — **charter / contract only**; **not** paired equivalence proof.
- **Ledger:** §1 / quick scan / §6–§8 / §7 / §11 / **STARLAB v1** / OD-007; *Remaining v1 proof-track map*; intent map **M52**–**M61**; milestone table rows **M52**–**M61**.

### 2026-04-15 — **M51** Governed post-bootstrap phase orchestration v1 — merged to `main` (PR #62) + milestone closeout

- **Merged** [PR #62](https://github.com/m-cahill/starlab/pull/62) to `main` at **2026-04-15T00:14:35Z** (UTC); merge commit `1e88466eb2635385b7ad56e666c45436a12f0b59`; **final PR head** `f812f8098608f8c3ae45c51f12f8f40f7fbe083c`; **authoritative green PR-head CI** [`24427191222`](https://github.com/m-cahill/starlab/actions/runs/24427191222) (**success**); **merge-boundary `main` CI** [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on merge commit `1e88466…` (**success**); branch `m51-governed-post-bootstrap-phase-orchestration` **deleted** after merge.
- **M51 proof (narrow):** optional **`--post-bootstrap-protocol-phases`** on **`execute_full_local_training_campaign`** — aggregated weighted refit phase, orchestrated **M42** skip (`candidate_not_m41_comparison_compatible`), watchable **M44** on refit joblib; **`starlab.hidden_rollout_campaign_run.v2`** + per-phase **`phase_receipt.json`** — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance, **not** M42 semantics extension for M45 refit bundles.
- **Closeout:** `M51_run1.md`, `M51_summary.md`, `M51_audit.md`; `M51_plan.md` **closed**; §1 / quick scan / §6–§8 / §11 / §18 / **STARLAB v1** boundary table; planned arc **53 (M00–M52)**; §7 **M51** **Complete** + **M52** stub row; annotated tag **`v0.0.51-m51`** on merge commit `1e88466…`; **M52** stub folder (`M52_plan.md`, `M52_toolcalls.md`) only. Closeout included steps to **ensure all documentation is updated as necessary** (public ledger + runtime operator surfaces).
- **Post-closeout `main` CI:** [`24429638756`](https://github.com/m-cahill/starlab/actions/runs/24429638756) on closeout commit `f3e6817…` — **success** (ledger + tag push — **not** PR #62 merge authority; merge-boundary remains [`24429524114`](https://github.com/m-cahill/starlab/actions/runs/24429524114) on `1e88466…`).

### 2026-04-14 — **M50** Industrial-scale hidden rollout mode & governed campaign execution v1 — merged to `main` (PR #61) + milestone closeout

- **Merged** [PR #61](https://github.com/m-cahill/starlab/pull/61) to `main` at **2026-04-14T21:48:43Z** (UTC); merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b`; **final PR head** `a6f0b90045a01908d4a57682bd41743826e5d543`; **authoritative green PR-head CI** [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763) (**success**); **merge-boundary `main` CI** [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) on merge commit `a0430d3…` (**success**); branch `m50-industrial-hidden-rollout-mode` **retained** on `origin`.
- **M50 proof (narrow):** governed **`execute_full_local_training_campaign`** over M49 + M45, PID lockfiles, honest **requested** vs **resolved** visibility, extended execution preflight, heartbeat / stop / quarantine-first resume posture — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance. **M49** remains charter/preflight only.
- **Closeout:** `M50_run1.md`, `M50_summary.md`, `M50_audit.md`; §1 / §6–§8 / §11 / §18; planned arc **52 (M00–M51)**; §7 **M50** **Complete** + **M51** stub row; annotated tag **`v0.0.50-m50`** on merge commit `a0430d3…`; **M51** stub folder (`M51_plan.md`, `M51_toolcalls.md`) only.

### 2026-04-14 — **M49** Full local training / bootstrap campaign charter & evidence protocol — merged to `main` (PR #60) + milestone closeout

- **Merged** [PR #60](https://github.com/m-cahill/starlab/pull/60) to `main` at **2026-04-14T04:43:06Z** (UTC); merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed`; **final PR head** `2780de11bccd6a51cba3a1d14b24a0433e776873`; **authoritative green PR-head CI** [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623) (**success**); **merge-boundary `main` CI** [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) on merge commit `cad5f2b…` (**success**); branch `m49-full-local-training-campaign-charter` **deleted** after merge. **Superseded** **failure** PR-head runs [`24381216946`](https://github.com/m-cahill/starlab/actions/runs/24381216946), [`24381253831`](https://github.com/m-cahill/starlab/actions/runs/24381253831) — **not** merge authority for final head.
- **M49 proof (narrow):** governed **`full_local_training_campaign_contract.json`** / report + **`campaign_preflight_receipt.json`** emitters; runtime `docs/runtime/full_local_training_campaign_v1.md`; cross-links; fixture tests — **not** execution of a long local campaign, **not** learning outcomes, **not** live SC2 in CI, **not** `out/` in repo.
- **Closeout:** `M49_run1.md`, `M49_summary.md`, `M49_audit.md`; §1 / §6–§8 / §11; planned arc **51 (M00–M50)**; §7 **M49** **Complete** + **M50** active row; Phase VI operator glossary (**shakedown**, **tranche**, **full local campaign**, **bootstrap run artifact**) + **operator campaign ladder** (local evidence steps: shakedown → tranche A → tranche B → governed full-run threshold); annotated tag **`v0.0.49-m49`** on merge commit `cad5f2b…`; **M50** plan folder (`M50_plan.md`, `M50_toolcalls.md`) + execution surface (`execute_full_local_training_campaign`, `industrial_hidden_rollout_mode_v1.md`).

### 2026-04-14 — **M48** Learned-agent comparison contract-path alignment — merged to `main` (PR #59) + milestone closeout

- **Merged** [PR #59](https://github.com/m-cahill/starlab/pull/59) to `main` at **2026-04-14T02:21:43Z** (UTC); merge commit `cdd023cb388ae99c3649978857e07af04c17df50`; **final PR head** `d94bc02c78bf75605edc4d28473f48cac986e53c`; **authoritative green PR-head CI** [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299) (**success**); **merge-boundary `main` CI** [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on merge commit `cdd023c…` (**success**); branch `m48-learned-agent-comparison-contract-path-alignment` **deleted** after merge.
- **M48 proof (narrow):** explicit **`--benchmark-contract`** (M20; alias **`--contract`**); optional **`--training-program-contract`** (M40 JSON from disk with digest verification); **strict** `ValueError` when **M41** candidates’ recorded `training_program_contract_sha256` / `training_program_contract_version` do not match the active M40 charter — **not** benchmark math expansion, **not** new M28 metrics, **not** live SC2 in CI.
- **Closeout:** `M48_run1.md`, `M48_summary.md`, `M48_audit.md`; §7 **M48** **Complete**; annotated tag **`v0.0.48-m48`** on merge commit `cdd023c…`; **M49** stub folder (`M49_plan.md`, `M49_toolcalls.md`) only.
- **Non-merge-boundary:** `main` CI [`24377643770`](https://github.com/m-cahill/starlab/actions/runs/24377643770) on closeout commit `64f4c9c…` — **failure** — Ruff **E501** — **not** PR #59 merge authority. **Repaired green `main`:** [`24377688981`](https://github.com/m-cahill/starlab/actions/runs/24377688981) on `915562a…` — **success** (format fix — **not** product merge authority; merge-boundary remains [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on `cdd023c…`).

### 2026-04-14 — **M47** Bootstrap Episode Distinctness & Operator Ergonomics — merged to `main` (PR #58) + milestone closeout

- **Recharter (explicit):** Prior ledger **M47** stub (**M42** `--contract` path alignment) remains **deferred** to **M48** (stub). **M47** delivered the rechartered scope: bootstrap **episode distinctness** + **operator ergonomics** — **not** M48 product work.
- **Merged** [PR #58](https://github.com/m-cahill/starlab/pull/58) to `main` at **2026-04-14T00:47:56Z** (UTC); merge commit `ebc5de0864ef6231d13efa741150d73c1ef1b98b`; **final PR head** `4a8fb3e2f7aad95d2cde5b6b77577db25e42e91e`; **authoritative green PR-head CI** [`24374720293`](https://github.com/m-cahill/starlab/actions/runs/24374720293) (**success**); **merge-boundary `main` CI** [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on merge commit `ebc5de0…` (**success**).
- **M47 proof (narrow):** per-episode M02 **`seed`** (`bootstrap_base_seed + episode_index`), **`starlab.m47.episode_manifest.v2`**, **`episode_distinctness`** on sealed bootstrap run/report, collapse **`warnings`**, operator/runtime interpretation in `docs/runtime/self_play_rl_bootstrap_v1.md` — **not** benchmark integrity, **not** live SC2 in CI, **not** **M42** `--contract` product (**M48** stub).
- **Closeout:** `M47_run1.md`, `M47_summary.md`, `M47_audit.md`; §7 **M47** **Complete**; annotated tag **`v0.0.47-m47`** on merge commit `ebc5de0…`; branch `m47-bootstrap-episode-distinctness-ergonomics` **retained**; **M48** remains **stub only**.
- **Non-merge-boundary:** `main` CI [`24374876505`](https://github.com/m-cahill/starlab/actions/runs/24374876505) on closeout commit `5dcba2d…` — **failure** — Ruff **format** — **not** PR #58 merge authority. **Repaired green `main`:** [`24374915005`](https://github.com/m-cahill/starlab/actions/runs/24374915005) on `9a80f7f…` — **success** (format fix — **not** product merge authority; merge-boundary remains [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on `ebc5de0…`).

### 2026-04-13 — **Governance recharter: M47 / M48** (user-directed)

- **Recharter:** **M47** stub (**M42** `--contract` path alignment) **deferred** to **M48** (stub). **M47** rechartered to **Bootstrap Episode Distinctness & Operator Ergonomics** — multi-episode **M45** interpretation (`episode_count_configured` vs distinct **`validation_run_sha256`** / **`run_id`**), default per-episode M02 **`seed`** = **`bootstrap_base_seed + episode_index`**, **`starlab.m47.episode_manifest.v2`**, collapse **`warnings`**, operator guidance in `docs/runtime/self_play_rl_bootstrap_v1.md`. **Not** benchmark integrity, **not** M42 `--contract` product (**M48**).
- **Product:** `starlab.training` bootstrap loop writes per-episode `bootstrap_match_config.json`; `episode_distinctness` on sealed bootstrap run + report; identity adds **`episode_seed_policy`**.
- **Stub:** `docs/company_secrets/milestones/M48/M48_plan.md`, `M48_toolcalls.md` — **M48** placeholder only.

### 2026-04-13 — **M46** bounded live validation final-status semantics — merged to `main` (PR #57) + CI repair + closeout

- **Governance input:** `docs/diligence/m44_bounded_live_final_status_recharter.md` — **Option A:** bounded **burnysc2** runs that record `bounded_exit` emit **`match_execution.final_status`** **`ok`**; literal SC2 `Result` as **`sc2_game_result`** — **not** match victory, **not** ladder strength, **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI.
- **Merged** [PR #57](https://github.com/m-cahill/starlab/pull/57) to `main` at **2026-04-13T18:12:03Z** (UTC); merge commit `b925130d2e6bb9b2586139b17d100285e89b8e54`; **final PR head** `ddb18f4cf5e74af2cf3a0f657b66911c93bb97a8`; **authoritative green PR-head CI** [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005) (**success**); superseded earlier green on non-final head [`24332502917`](https://github.com/m-cahill/starlab/actions/runs/24332502917) on `a100849…` — **not** merge authority for `ddb18f4…`.
- **Merge-push `main` CI** on merge commit: [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) — **failure** — `pip-audit` / **pytest** `CVE-2025-71176` (fix **≥9.0.3**). **Repaired `main`:** commit `1b7b25ea22392a709bec726ce0827913d18cdca7` — **green** [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) — **not** M46 product scope; `pyproject.toml` **`pytest>=9.0.3,<10`**, `tests/test_m34_audit_closure.py` bound check.
- **Closeout:** `M46_run1.md`, `M46_summary.md`, `M46_audit.md`; §7 **M46** **Complete**; **M47** stub row; annotated tag **`v0.0.46-m46`** on merge commit `b925130…`; branch `recharter/m44-bounded-live-final-status-semantics` **retained**.
- **Non-merge-boundary:** `main` CI [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) on closeout commit `1b33acd…` — **success** — ledger / closeout artifacts + governance tests + tag push — **not** PR #57 merge authority; merge-boundary remains [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) on `b925130…` (**failure**) + repaired [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370).
- **Out of scope:** **M42** `--contract` path mismatch — **M47** stub only.

### 2026-04-12 — M45 merged to `main` (PR #56) + milestone closeout

- Merged [PR #56](https://github.com/m-cahill/starlab/pull/56) to `main` at **2026-04-12T20:07:19Z** (UTC); merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7` (merge method: **merge commit**); branch `m45-self-play-rl-bootstrap-v1` **retained** on `origin` after merge.
- Final PR head `0e89081cd786b527951a98eb3e63b7677f8c8c00` — **authoritative green PR-head CI:** [`24314869292`](https://github.com/m-cahill/starlab/actions/runs/24314869292) (**success**); **superseded** **failure** PR-head [`24314843956`](https://github.com/m-cahill/starlab/actions/runs/24314843956) on `3b19200…` — Ruff format — **not** merge authority for final head `0e89081…`.
- **Merge-push `main` CI** on merge commit: [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M45 proof (narrow):** first governed **self-play / RL bootstrap** — `starlab.training` bootstrap modules + CLI, `self_play_rl_bootstrap_run.json` / report, `bootstrap_dataset.json`, **M44** harness reuse, **M43** candidate + local `joblib`, optional conservative weighted re-fit — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** **Phase VI integrated test campaign** completion.
- §7 milestone table → **M45** **Complete**; §11 **M00–M45** arc **closed** on `main`; closeout `M45_run1.md`, `M45_summary.md`, `M45_audit.md`, `M45_plan.md` (**Complete**), `M45_toolcalls.md`.
- Annotated tag **`v0.0.45-m45`** on merge commit `1a585b68ea7413852ce78c220c6512bba6a004d7`.
- **Non-merge-boundary:** `main` CI [`24315387918`](https://github.com/m-cahill/starlab/actions/runs/24315387918) on closeout commit `879a878…` — **success** — ledger/README/architecture/M45 artifacts/governance tests; [`24315413976`](https://github.com/m-cahill/starlab/actions/runs/24315413976) on `2075ae0…` — **success** — `M45_run1` non-merge-boundary table; **not** PR #56 product merge authority; merge-boundary remains [`24315311180`](https://github.com/m-cahill/starlab/actions/runs/24315311180) on `1a585b6…`.

### 2026-04-12 — M44 merged to `main` (PR #55) + milestone closeout

- Merged [PR #55](https://github.com/m-cahill/starlab/pull/55) to `main` at **2026-04-12T18:13:50Z** (UTC); merge commit `1b1067ad632643d2b14da05d510a7c2a263cc8ea` (merge method: **merge commit**); branch `m44-local-live-play-validation-harness-v1` **retained** on `origin` after merge.
- Final PR head `dc8e74d98701c6080e525b8a79aa7aa4b7872867` — **authoritative green PR-head CI:** [`24312599411`](https://github.com/m-cahill/starlab/actions/runs/24312599411) (**success**); **superseded** **failure** PR-head [`24312572604`](https://github.com/m-cahill/starlab/actions/runs/24312572604) on `c8b989a…` — Ruff format — **not** merge authority for final head `dc8e74d…`.
- **Merge-push `main` CI** on merge commit: [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M44 proof (narrow):** first governed **local live-play validation harness** — `starlab.sc2` harness + emitter, `local_live_play_validation_run.json` / report, `m43_sklearn_runtime`, bounded adapter **`starlab.m44.semantic_live_action_adapter.v1`**, replay-backed chain (M02/M03/M04), `runtime_mode` `fixture_stub_ci` \| `local_live_sc2`, optional video metadata — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance, **not** **M45** RL product.
- §11 **current milestone** → **M45** (**In progress** after this ledger update; **M45** was **stub** until M45 product work landed on a feature branch); **M44** **Complete**; closeout `M44_run1.md`, `M44_summary.md`, `M44_audit.md`, `M44_plan.md` (**Complete**), `M44_toolcalls.md`.
- Annotated tag **`v0.0.44-m44`** on merge commit `1b1067ad632643d2b14da05d510a7c2a263cc8ea`.
- **Non-merge-boundary:** `main` CI [`24313225285`](https://github.com/m-cahill/starlab/actions/runs/24313225285) on closeout commit `e3d14f4…` — **success** — documentation-only closeout + tag push; [`24313253583`](https://github.com/m-cahill/starlab/actions/runs/24313253583) on `5e4456c…` — **success** — documentation-only ledger/`M44_run1` refinement; [`24313282328`](https://github.com/m-cahill/starlab/actions/runs/24313282328) on `7f493f8…` — **success** — documentation-only `M44_run1` table completion; **not** PR #55 product merge authority; merge-boundary remains [`24313143884`](https://github.com/m-cahill/starlab/actions/runs/24313143884) on `1b1067a…`.

### 2026-04-12 — M43 merged to `main` (PR #54) + milestone closeout

- Merged [PR #54](https://github.com/m-cahill/starlab/pull/54) to `main` at **2026-04-12T07:25:40Z** (UTC); merge commit `8850e378a584c9821eeab3e8c72bc499d590b308` (merge method: **merge commit**); branch `m43-hierarchical-training-pipeline-v1` **retained** on `origin` after merge.
- Final PR head `ffc428454939702fbe9c100ace9e109ee0c51605` — **authoritative green PR-head CI:** [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558) (**success**); **superseded** intermediate green PR-head runs on the M43 branch — [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) — **not** merge authority for final head `ffc4284…`.
- **Merge-push `main` CI** on merge commit: [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M43 proof (narrow):** first governed **hierarchical training pipeline** — `starlab.hierarchy` training modules + CLI, `hierarchical_training_run.json` / report, optional local-only combined `joblib`, **M40** contract binding, **M29** interface trace schema linkage, **M30** `starlab.m30.delegate.fixed_four_v1`, manager/worker **LogisticRegression**, **delegate_coverage** — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** **M42** comparison consumption beyond metadata compatibility, **not** **M44** live-play or **M45** RL.
- §11 **current milestone** → **M44** (**stub**); **M43** **Complete**; closeout `M43_run1.md`, `M43_summary.md`, `M43_audit.md`, `M43_plan.md` (**Complete**), `M43_toolcalls.md`.
- Annotated tag **`v0.0.43-m43`** on merge commit `8850e378a584c9821eeab3e8c72bc499d590b308`.
- **Non-merge-boundary:** later `push` workflows on `main` after the merge boundary (closeout commits, etc.) — **not** PR #54 merge authority; merge-boundary remains [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897) on `8850e37…` — see Actions history for run IDs.

### 2026-04-12 — M42 merged to `main` (PR #53) + milestone closeout

- Merged [PR #53](https://github.com/m-cahill/starlab/pull/53) to `main` at **2026-04-12T06:02:16Z** (UTC); merge commit `3eb091aba832cb0a66066d6fca6db091eb53c8f5` (merge method: **merge commit**); branch `m42-learned-agent-comparison-harness-v1` **deleted** on `origin` after merge.
- Final PR head `191a95511a7428b0c12c79edc978070c406ad736` — **authoritative green PR-head CI:** [`24298501553`](https://github.com/m-cahill/starlab/actions/runs/24298501553) (**success**); **superseded** PR-head runs: none — sole run on final head.
- **Merge-push `main` CI** on merge commit: [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M42 proof (narrow):** first governed **learned-agent comparison harness** — `starlab.evaluation` comparison modules + CLI, `learned_agent_comparison.json` / report, `TrainedRunPredictor` for M41 `joblib` sidecar loading, M28 metric surface reuse via `evaluate_predictor_on_test_split`, ranking policy `starlab.m42.ranking.accuracy_macro_f1_candidate_id_v1` — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** **M43** hierarchical training product.
- §11 **current milestone** → **M43** (**in progress**); **M42** **Complete**; closeout `M42_run1.md`, `M42_summary.md`, `M42_audit.md`, `M42_plan.md` (**Complete**), `M42_toolcalls.md`.
- Annotated tag **`v0.0.42-m42`** on merge commit `3eb091aba832cb0a66066d6fca6db091eb53c8f5`.
- **Non-merge-boundary:** any **`main` CI** run triggered **only** by this ledger/closeout documentation push after the merge boundary — **not** PR #53 merge authority; merge-boundary remains [`24300065842`](https://github.com/m-cahill/starlab/actions/runs/24300065842) on `3eb091a…`.

### 2026-04-12 — M41 merged to `main` (PR #52) + milestone closeout

- Merged [PR #52](https://github.com/m-cahill/starlab/pull/52) to `main` at **2026-04-12T02:58:11Z** (UTC); merge commit `5e0add12dd8f4b3a9b4dd31023319cc1999f826b` (merge method: **merge commit**); branch `m41-replay-imitation-training-pipeline-v1` **retained** on `origin` after merge.
- Final PR head `7c092eda7fe6554a2168968ffddbe37e929159e4` — **authoritative green PR-head CI:** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) (**success**); **superseded** intermediate green PR-head runs on the M41 branch — [`24297190190`](https://github.com/m-cahill/starlab/actions/runs/24297190190), [`24297168010`](https://github.com/m-cahill/starlab/actions/runs/24297168010), [`24297148773`](https://github.com/m-cahill/starlab/actions/runs/24297148773), [`24297129471`](https://github.com/m-cahill/starlab/actions/runs/24297129471), [`24297108516`](https://github.com/m-cahill/starlab/actions/runs/24297108516) — **not** merge authority for final head.
- **Merge-push `main` CI** on merge commit: [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M41 proof (narrow):** first governed **replay-imitation training pipeline** — `starlab.imitation` training modules + CLI, `replay_imitation_training_run.json` / report, optional local-only weights (not in repo), **M40** contract binding + feature schema — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** **M42** comparison harness product.
- §11 **current milestone** → **M42** (**stub**); **M41** **Complete**; closeout `M41_run1.md`, `M41_summary.md`, `M41_audit.md`, `M41_plan.md` (**Complete**), `M41_toolcalls.md`.
- Annotated tag **`v0.0.41-m41`** on merge commit `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`.
- **Non-merge-boundary:** any **`main` CI** run triggered **only** by this ledger/closeout documentation push after the merge boundary — **not** PR #52 merge authority; merge-boundary remains [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) on `5e0add12…`.

### 2026-04-12 — M40 merged to `main` (PR #51) + milestone closeout

- Merged [PR #51](https://github.com/m-cahill/starlab/pull/51) to `main` at **2026-04-12T00:52:29Z** (UTC); merge commit `44e8edc5bcce8dc99576bf2be542b273095e5072` (merge method: **merge commit**); branch `m40-agent-training-program-charter` deleted after merge.
- Final PR head `be47d913737f322bbf8e9e08a672561c71d322eb` — **authoritative green PR-head CI:** [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784) (**success**); **superseded PR-head** [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) on `6690cd7f0ae79abe0db85695a0d20b4d7c48cdaf` — Ruff format — **not** merge authority.
- **Merge-push `main` CI** on merge commit: [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123) (**success**) — merge-boundary evidence (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).
- **M40 proof (narrow):** training-program **charter** — `starlab.training`, deterministic `agent_training_program_contract.json` / report, `docs/runtime/agent_training_program_contract_v1.md`, ledger **42 → 46** recharter, stub **M41**–**M45** — **not** actual training, **not** weights, **not** benchmark integrity, **not** live SC2 in CI, **not** **M41** product.
- §11 **current milestone** → **M41** (**stub**); **M40** **Complete**; closeout `M40_run1.md`, `M40_summary.md`, `M40_audit.md`, `M40_plan.md` (**Complete**), `M40_toolcalls.md`.
- Annotated tag **`v0.0.40-m40`** on merge commit `44e8edc5bcce8dc99576bf2be542b273095e5072`.

### 2026-04-11 — Planned program arc revised to **46 milestones (M00–M45)**; Phase VI recharter (governance; M40)

- **Governance:** after **M39** closeout on `main`, the active program arc expands from **42 (M00–M41)** to **46 (M00–M45)**. **Phase VI** is rechartered to **Governed Agent Training, Comparison, and Local Validation** — **M40** Agent Training Program Charter & Artifact Contract through **M45** Self-Play / RL Bootstrap v1. The former Phase VI stub milestones (**SC2 Substrate Review & Expansion Decision**; **Platform Boundary Review & Multi-Environment Charter**) are **deferred beyond the current active arc** (§19 **FUT-005**); **OD-007** is no longer tied to a milestone number inside M00–M45.
- **Dual truth:** historical changelog entries and audits that reference the **42-milestone** arc or the old Phase VI **M40**/**M41** stubs remain **historical**; this entry records the **governance decision** without rewriting closed-milestone facts.
- **Ledger / code:** `docs/starlab.md` §§1, 6, 7, 8, 11, 12, 19; `starlab.training` contract emission; `docs/runtime/agent_training_program_contract_v1.md`; stub milestone folders **M41**–**M45**.

### 2026-04-11 — M39 merged to `main` (PR #50) + milestone closeout

- Merged [PR #50](https://github.com/m-cahill/starlab/pull/50) to `main` at **2026-04-11T22:36:41Z** (UTC); merge commit `ca97027cf1827942a25c886f04b5db56b8b9fe7b` (merge method: **merge commit**); branch `m39-public-flagship-proof-pack` deleted after merge.
- Final PR head `2c3fce7d3820bbfdfb655deedd3c0bb980ddc45b` — **authoritative green PR-head CI:** [`24292861437`](https://github.com/m-cahill/starlab/actions/runs/24292861437) (**success**); **superseded PR-head:** none.
- **Merge-push `main` CI** on merge commit: [`24293162871`](https://github.com/m-cahill/starlab/actions/runs/24293162871) (**success**) — merge-boundary evidence for M39 product merge.
- **M39 proof (narrow):** `starlab.flagship`, `make flagship`, CI **`flagship`** + artifact **`flagship-proof-pack`**, deterministic public proof pack + docs — **not** benchmark integrity, **not** live SC2 in CI, **not** training-track work, **not** Phase VI product.
- §11 **current milestone** at M39 closeout → **M40** (next); **M39** **Complete**; closeout `M39_run1.md`, `M39_summary.md`, `M39_audit.md`, `M39_plan.md` (**Complete**), `M39_toolcalls.md`. *(Superseded by **M40** closeout entry above: **M41** stub is current after **M40** merges.)*
- Annotated tag **`v0.0.39-m39`** on merge commit `ca97027cf1827942a25c886f04b5db56b8b9fe7b`.
- **Non-merge-boundary `main` CI** after closeout (doc + ledger + governance test; **not** PR #50 merge authority): [`24293207074`](https://github.com/m-cahill/starlab/actions/runs/24293207074) on `744e514c3168d73ac20ee938a904d9b8b23823a1` — **success** (required jobs: **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`flagship`**, **`governance`**).

### 2026-04-11 — M38 merged to `main` (PR #49) + milestone closeout

- Merged [PR #49](https://github.com/m-cahill/starlab/pull/49) to `main` at **2026-04-11T21:21:43Z** (UTC); merge commit `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` (merge method: **merge commit**); branch `m38-public-face-governance-code-health` deleted after merge.
- Final PR head `3e00641922fc11f7f906d9d163312993a83816c1` — **authoritative green PR-head CI:** [`24272425346`](https://github.com/m-cahill/starlab/actions/runs/24272425346) (**success**); **superseded PR-head:** none.
- **Merge-push `main` CI** on merge commit: [`24291882960`](https://github.com/m-cahill/starlab/actions/runs/24291882960) (**success**) — merge-boundary evidence.
- **M38 proof (narrow):** README + ledger quick-scan; governance test dedup + milestone row checks; `tests/runpy_helpers.py` — **not** M39 flagship proof pack, **not** benchmark integrity, **not** live SC2 in CI, **not** gate weakening.
- §11 **current milestone** → **M39** (stub); **M38** **Complete**; closeout `M38_run1.md`, `M38_summary.md`, `M38_audit.md`, `M38_plan.md` (**Complete**), `M38_toolcalls.md`.
- Annotated tag **`v0.0.38-m38`** on merge commit `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` (push tag per release discipline).
- **Non-merge-boundary `main` CI** after closeout (doc-only; **not** PR #49 merge authority): [`24291941420`](https://github.com/m-cahill/starlab/actions/runs/24291941420) on `d8e318d…` — **success**; follow-up evidence commit [`24291960962`](https://github.com/m-cahill/starlab/actions/runs/24291960962) on `c419762…` — **success**.

### 2026-04-10 — Planned program arc revised to **42 milestones (M00–M41)**; **M37** recharter (governance)

- **Governance:** expand the planned program arc from **40 (M00–M39)** to **42 (M00–M41)**. **M37** — **Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening**; **M38** — **Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening**; **M39** — **Public Flagship Proof Pack**; **Phase VI** is **M40** — **SC2 Substrate Review & Expansion Decision** and **M41** — **Platform Boundary Review & Multi-Environment Charter**. **OD-007** now targets **M41** (moved from **M39**).
- **Dual truth:** prior audits and **M37** full-audit artifacts may still read under older milestone numbering; this ledger records the **governance decision** without rewriting historical audit files.
- **Campaign note:** the program runs a **three-milestone audit/flagship sequence** (**M37**–**M39**); **~85%** coverage is a **stretch target**, not a guaranteed claim (see §1 status line).
- **Ledger:** §§1, 6, 7, 8, 10, 11, 12, 20 (score trend placeholders); milestone stubs **M36–M41**; new **M40** / **M41** minimal stubs.

### 2026-04-11 — M37 merged to `main` (PR #48) + milestone closeout

- Merged [PR #48](https://github.com/m-cahill/starlab/pull/48) to `main` at **2026-04-11T01:15:16Z** (UTC); merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd` (merge method: **merge commit**).
- Final PR head `a38d3a7dcbb870f3d425e112f464f228889ae1c5` — **authoritative green PR-head CI:** [`24271250678`](https://github.com/m-cahill/starlab/actions/runs/24271250678) (**success**); **superseded failure** PR-head [`24271229377`](https://github.com/m-cahill/starlab/actions/runs/24271229377) (pytest — **not** merge authority).
- **Merge-push `main` CI** on merge commit: [`24271267848`](https://github.com/m-cahill/starlab/actions/runs/24271267848) (**success**) — merge-boundary evidence.
- **Coverage:** branch-aware TOTAL **~80.34%** on authoritative PR-head CI; **`fail_under`** **78.0** in `pyproject.toml` (disciplined buffer vs measured baseline).
- **M37 proof (narrow):** coverage margin recovery, CI evidence (`$GITHUB_STEP_SUMMARY` TOTAL line, `make check`), governance tests for **42**-milestone arc, cross-platform replay/map basename normalization in `starlab.runs.identity` — **not** M39 flagship proof pack, **not** subprocess coverage hacks, **not** lowering the gate below honest margin.
- §11 **current milestone** → **M38** (stub); **M37** **Complete**; closeout `M37_run1.md`, `M37_summary.md`, `M37_audit.md`, `M37_plan.md` (**Complete**), `M37_toolcalls.md`.
- Annotated tag **`v0.0.37-m37`** on merge commit `d2474bd365290a9c77f854b13d36a5ea1d8777cd`.
- Post–merge-closeout doc commit `b98862befbbb381af27db184c646feb0ec26530d`: **`CI`** run [`24271317002`](https://github.com/m-cahill/starlab/actions/runs/24271317002) — **success** — **not** merge-boundary authority (same distinction as M36 post-closeout runs).

### 2026-04-10 — M36 merged to `main` (PR #47) + milestone closeout

- Merged [PR #47](https://github.com/m-cahill/starlab/pull/47) to `main` at **2026-04-10T22:23:02Z** (UTC); merge commit `e73a53b28a4b6eeb3a2c19dd358d928c64806e89` (merge method: **merge commit**)
- Final PR head `63fe1168e8a4bb7961948526589aba3c0a01c9ba` — **authoritative green PR-head CI:** [`24266877684`](https://github.com/m-cahill/starlab/actions/runs/24266877684) (**success**); **superseded PR-head:** none recorded
- **Merge-push `main` CI** on merge commit: [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) (**success**) — merge-boundary evidence
- Governance / docs: `docs/starlab_archive.md`, `docs/starlab.md` §7 archival policy + pointer, **M28–M35** inline notes, consolidated `tests/test_governance_milestones.py`, `tests/test_governance_runtime.py` deduplication; **616** pytest on merge-boundary `main` CI [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) (one pre-existing `s2protocol` deprecation warning — unchanged)
- **M36 proof (narrow):** ledger readability + governance test surface rationalization — **not** M39 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M36** **Complete** on `main`; **current milestone** → **M37** (**stub only**); **M37** stubs unchanged (`M37_plan.md`, `M37_toolcalls.md`) — **no** M37 product code in this closeout
- Milestone closeout docs: `M36_run1.md`, `M36_summary.md`, `M36_audit.md`, `M36_plan.md` (**Complete**), `M36_toolcalls.md`
- Annotated tag **`v0.0.36-m36`** on merge commit `e73a53b28a4b6eeb3a2c19dd358d928c64806e89` (milestone boundary — **not** a later doc-only tip)
- Post–merge-closeout doc/governance commit `e4b306584a6cc0cb4a7f582c50f8fe3100094d8b`: M36 complete-row smoke + `test_current_milestone_is_m37` + full `M36_*` closeout files — **`617`** `pytest` locally; **non-merge-boundary `main` CI** [`24267000568`](https://github.com/m-cahill/starlab/actions/runs/24267000568) (**success**) — **does not** replace merge-boundary **`616`** tests on [`24266906173`](https://github.com/m-cahill/starlab/actions/runs/24266906173) at `e73a53b…` (authoritative M36 **implementation** merge CI remains **`24266877684`** + **`24266906173`**)

### 2026-04-10 — M35 merged to `main` (PR #46) + milestone closeout

- Merged [PR #46](https://github.com/m-cahill/starlab/pull/46) to `main` at **2026-04-10T21:30:06Z** (UTC); merge commit `5b4d24b0eca578b70f2963f1561b99bc89fef033` (merge method: **merge commit**)
- Final PR head `91e45ddfbb7a1f610ba25ac59a107c1b7e40af1a` — **authoritative green PR-head CI:** [`24265022396`](https://github.com/m-cahill/starlab/actions/runs/24265022396) (**success**); **superseded failure** PR-head [`24264929015`](https://github.com/m-cahill/starlab/actions/runs/24264929015) (Ruff format), [`24264963434`](https://github.com/m-cahill/starlab/actions/runs/24264963434) (Mypy) — **not** merge authority
- **Merge-push `main` CI** on merge commit: [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) (**success**) — merge-boundary evidence
- Product / governance: `M14BundleLoader`, `parser_io` / `replay_slice_generation` / observation reconciliation splits, `load_json_object_strict`, ledger **M00–M39**, **M36–M39** stubs, governance tests; **613** pytest on merge-boundary `main` CI [`24265056432`](https://github.com/m-cahill/starlab/actions/runs/24265056432) (one pre-existing `s2protocol` deprecation warning — unchanged)
- **M35 proof (narrow):** structural decoupling + module decomposition — **not** M39 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M35** **Complete** on `main`; **current milestone** → **M36** (**stub only**); **M36** stubs (`M36_plan.md`, `M36_toolcalls.md`) — **no** M36 product code in this closeout
- Milestone closeout docs: `M35_run1.md`, `M35_summary.md`, `M35_audit.md`, `M35_plan.md` (**Complete**), `M35_toolcalls.md`
- Annotated tag **`v0.0.35-m35`** on merge commit `5b4d24b0eca578b70f2963f1561b99bc89fef033` (milestone boundary — **not** a later doc-only tip)

### 2026-04-10 — Planned program arc revised to 40 milestones (M00–M39); M35 charter (governance)

- **Governance:** expand the planned program arc from **38 (M00–M37)** to **40 (M00–M39)**. **M35** is **Audit Closure IV — Structural Decoupling and Module Decomposition**; **M36** — **Audit Closure V — Governance Surface Rationalization and Documentation Density Control**; **M37** — **Public Flagship Proof Pack**; **Phase VI** is **M38** — **SC2 Substrate Review & Expansion Decision** and **M39** — **Platform Boundary Review & Multi-Environment Charter**. **OD-007** now targets **M39**.
- **Dual truth:** the **M35 full audit** recommended proceeding **directly** to flagship-class work; the program **intentionally** chose a **stricter audit-maximizing path** by inserting **two corrective milestones** before **M37**. The audit JSON/Markdown artifacts are **unchanged**; this ledger states the later governance decision.
- **Ledger:** §§3, 6, 7, 8, 10, 11, 12, 20 (score trend placeholders); milestone stubs **M36–M39** (`*_plan.md`, `*_toolcalls.md`).

### 2026-04-10 — M34 merged to `main` (PR #40) + milestone closeout

- Merged [PR #40](https://github.com/m-cahill/starlab/pull/40) to `main` at **2026-04-10T19:47:02Z** (UTC); merge commit `51e960d0c1c0eb20923836a8ac2400a59013bcc5` (merge method: **merge commit**); branch `m34-audit-closure-iii-structural-hygiene-manual-prep`
- Final PR head `a748bd7cc0be2b7e2acb423e098190429ae6fe2a` — **authoritative green PR-head CI:** [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) (**success**); **superseded failure** PR-head [`24261032237`](https://github.com/m-cahill/starlab/actions/runs/24261032237) on `d1e92ae2a9b4e64326ebd68a5fe364f8f75a163f` (missing M35 stub files in first commit) — **not** merge authority
- **Merge-push `main` CI** on merge commit: [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) (**success**) — merge-boundary evidence
- Product / governance: `starlab/_io.py`, split `tests/test_governance_*.py`, `tests/test_m34_audit_closure.py`, `.github/dependabot.yml`, `pyproject.toml` dev caps, `docs/diligence/operating_manual_promotion_readiness.md`, `docs/audit/broad_exception_boundaries.md`, `DeferredIssuesRegistry` **DIR-003**–**DIR-006**; **M35** plan/toolcalls **stubs only** (governance expectation; **no** M35 product code); **609** pytest on merge-boundary `main` CI [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337) (one pre-existing `s2protocol` deprecation warning — unchanged)
- **M34 proof (narrow):** structural hygiene + deferred-issue closure + operating-manual **promotion prep** — **not** M39 flagship proof-pack product, **not** benchmark integrity, **not** live SC2 in CI, **not** operating manual v1
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M34** **Complete** on `main`; **current milestone** → **M35** (**stub only**)
- Milestone closeout docs: `M34_run1.md`, `M34_summary.md`, `M34_audit.md`, `M34_plan.md` (**Complete**), `M34_toolcalls.md`
- Annotated tag **`v0.0.34-m34`** on merge commit `51e960d0c1c0eb20923836a8ac2400a59013bcc5` (milestone boundary — **not** a later doc-only tip)
- **Non-merge-boundary `main` CI (post-closeout docs):** [`24261183636`](https://github.com/m-cahill/starlab/actions/runs/24261183636) on closeout commit `6dcf8079cebd06d4a3714d6d85932a2415241c05` — **success** (ledger/closeout only); **not** substitute merge authority for M34 product (authoritative remains [`24261065226`](https://github.com/m-cahill/starlab/actions/runs/24261065226) + [`24261102337`](https://github.com/m-cahill/starlab/actions/runs/24261102337)); see `M34_run1.md`

### 2026-04-10 — M33 merged to `main` (PR #39) + milestone closeout

- Merged [PR #39](https://github.com/m-cahill/starlab/pull/39) to `main` at **2026-04-10T18:02:21Z** (UTC); merge commit `975ac52fff206f9ceb1b0be66a0e7f1c7386a248` (merge method: **merge commit**); remote branch `m33-audit-closure-ii-ci-tiering-field-test-readiness` **deleted** after merge
- Final PR head `6640c69b64dfc8a905a24535bbf86a8fba10d7e9` — **authoritative green PR-head CI:** [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) (**success**); **superseded** earlier green PR-head [`24231252478`](https://github.com/m-cahill/starlab/actions/runs/24231252478) on `b758e6d…` — **not** final merge authority
- **Merge-push `main` CI** on merge commit: [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) (**success**) — merge-boundary evidence
- Product / governance: `.github/workflows/ci.yml` (parallel **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, **`governance`**), `docs/runtime/ci_tiering_field_test_readiness_v1.md`, `docs/diligence/field_test_session_template.md`, architecture / operating manual / clone-to-run / checklist / smoke expansions, `tests/test_m33_audit_closure.py`, `DeferredIssuesRegistry` **DIR-001/002/007**; **591** pytest on merge-boundary `main` CI [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M33 proof (narrow):** explicit **CI** tiering + fixture-only **`fieldtest-output`** + expanded operator / diligence surfaces — **not** M34 structural hygiene product, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity, **not** operating manual v1
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M33** **Complete** on `main`; **current milestone** → **M34** (**stub only**); **M34** stubs (`M34_plan.md`, `M34_toolcalls.md`) — **no** M34 product code
- Milestone closeout docs: `M33_run1.md`, `M33_summary.md`, `M33_audit.md`, `M33_plan.md` (**Complete**), `M33_toolcalls.md`
- Annotated tag **`v0.0.33-m33`** on merge commit `975ac52fff206f9ceb1b0be66a0e7f1c7386a248` (milestone boundary — **not** a later doc-only tip)
- **Non-merge-boundary `main` CI (post-closeout):** [`24257044304`](https://github.com/m-cahill/starlab/actions/runs/24257044304) on closeout commit `e98f30c082343fd22bd53c80e8bbeea0a073c173` — **failure** (Ruff E501 in `tests/test_m33_audit_closure.py`); **not** M33 product merge authority
- **Repair / green `main` CI:** [`24257093617`](https://github.com/m-cahill/starlab/actions/runs/24257093617) on `c5835a37c52248e92d89050f43c33508c8f048ae` — **success** (Ruff wrap only); **not** substitute merge authority for M33 **product** (authoritative remains [`24231313561`](https://github.com/m-cahill/starlab/actions/runs/24231313561) + [`24256871132`](https://github.com/m-cahill/starlab/actions/runs/24256871132)); see `M33_run1.md`

### 2026-04-09 — M33 chartered: CI tiering, field-test CI artifact, architecture / operator docs (implementation)

- **M33** plan: `docs/company_secrets/milestones/M33/M33_plan.md` (**charter** — replaces stub).
- **CI:** `.github/workflows/ci.yml` — jobs **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, aggregate **`governance`**; workflow name **`CI`**; SHA-pinned actions; artifacts **`coverage-xml`**, **`pytest-junit-xml`**, **`pytest-smoke-junit-xml`**, **`sbom-cyclonedx-json`**, **`fieldtest-output`** (`out/fieldtest/` with `replay_explorer_surface.json` + `replay_explorer_surface_report.json`).
- **Docs:** `docs/runtime/ci_tiering_field_test_readiness_v1.md`, `docs/diligence/field_test_session_template.md`; updates to `docs/architecture.md`, `docs/starlab_operating_manual_v0.md`, `docs/getting_started_clone_to_run.md`, `docs/runtime/clone_to_run_smoke_v1.md`, `docs/diligence/field_test_checklist.md`; governance tests in `tests/test_m33_audit_closure.py`; **DeferredIssuesRegistry** — **DIR-001**, **DIR-002**, **DIR-007** → **M33 resolutions** (coverage gate **unchanged** at **75.4**).
- **Ledger:** §3 / §6 Phase V / §7 / §11 / §20 score trend; **not** §18 merge row until PR merges.
- **Non-claims:** **not** M34 structural hygiene closure, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark integrity.

### 2026-04-10 — M32 merged to `main` (PR #38) + milestone closeout

- Merged [PR #38](https://github.com/m-cahill/starlab/pull/38) to `main` at **2026-04-10T05:56:16Z** (UTC); merge commit `cf7219911a208da584537b4c08ab5811fa3f67de` (merge method: **merge commit**); remote branch `m32-audit-closure-coverage-clone-run-manual-scaffold` **deleted** after merge
- Final PR head `0c3f6ce4ab674c6fcc00daa3af0a6efabb69c6ce` — **authoritative green PR-head CI:** [`24228528798`](https://github.com/m-cahill/starlab/actions/runs/24228528798) (**success**); **superseded** red PR-head: none recorded
- **Merge-push `main` CI** on merge commit: [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230) (**success**)
- Product / governance: `.github/workflows/ci.yml` (coverage + JUnit XML, artifact uploads, SHA-pinned actions), `pyproject.toml` coverage gate (`fail_under = 75.4`), `Makefile`, `docs/architecture.md`, `docs/getting_started_clone_to_run.md`, `docs/starlab_operating_manual_v0.md`, `docs/audit/DeferredIssuesRegistry.md`, `docs/runtime/clone_to_run_smoke_v1.md`, `docs/diligence/field_test_checklist.md`, smoke markers + `tests/test_m32_audit_closure.py`; **574** pytest on merge-boundary `main` CI [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M32 proof (narrow):** truthful **line coverage** measurement + gate in CI; **`coverage.xml`** and **`pytest-junit.xml`** artifacts; **SHA-pinned** Actions; **smoke** lane + **`Makefile`**; **clone-to-run** + **field-test** docs; **draft** operating manual scaffold; **public** deferred registry; **M31**-based **fixture-only** `make fieldtest`; **not** M33 CI tiering, **not** M34 structural hygiene, **not** M39 flagship proof pack, **not** live SC2 in CI, **not** benchmark-integrity proof
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M32** **Complete** on `main`; **current milestone** → **M33** (**stub-only**); **M33** stubs (`M33_plan.md`, `M33_toolcalls.md`) — **no** M33 product code
- Milestone closeout docs: `M32_run1.md`, `M32_summary.md`, `M32_audit.md`, `M32_plan.md` (**Complete**), `M32_toolcalls.md`
- Annotated tag **`v0.0.32-m32`** on merge commit `cf7219911a208da584537b4c08ab5811fa3f67de` (milestone boundary — **not** a later doc-only tip unless repo convention changes)
- **Non-merge-boundary** `main` CI on closeout commit `6866bf718adc829526ae46cb6de0141416f72f94`: [`24228864767`](https://github.com/m-cahill/starlab/actions/runs/24228864767) (**success**) — documentation + governance + M33 stubs only; **not** product merge authority for M32 (authoritative remains [`24228528798`](https://github.com/m-cahill/starlab/actions/runs/24228528798) + [`24228788230`](https://github.com/m-cahill/starlab/actions/runs/24228788230))

### 2026-04-10 — M32 governance: future milestone arc revised (35 → 38 milestones)

- **Governance (ledger-only):** the **planned program arc** is revised from **35 milestones (M00–M34)** to **38 milestones (M00–M37)** as part of **M32** — **historical M00–M31 closed-milestone facts, merge SHAs, and CI evidence are unchanged in substance**.
- **Renumbering / renaming (future plan only):** **M32** — Audit Closure I (coverage, clone-to-run, operating manual scaffold); **M33** — Audit Closure II; **M34** — Audit Closure III; **M35** — Public Flagship Proof Pack (renamed from prior **M32** flagship slot); **M36** — SC2 Substrate Review & Expansion Decision (renamed from prior **M33**); **M37** — Platform Boundary Review & Multi-Environment Charter (renamed from prior **M34**).
- **OD-007** target milestone updated from **M34** to **M37** (second-environment / multi-environment charter posture).
- **Product (M32 scope):** operational / diligence surfaces only — **not** flagship proof-pack product code (**M35**).

### 2026-04-10 — M31 merged to `main` (PR #37) + milestone closeout

- Merged [PR #37](https://github.com/m-cahill/starlab/pull/37) to `main` at **2026-04-10T04:24:58Z** (UTC); merge commit `41d62056e1956627b63152221932dc9c2423429c` (merge method: **merge commit**); remote branch `m31-replay-explorer-operator-evidence-surface` **deleted**
- Final PR head `4972a56c335342fbf2f1c5fa179bb1920561317c` — **authoritative green PR-head CI:** [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) (**success**); **superseded** red PR-head: none recorded
- **Merge-push `main` CI** on merge commit: [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) (**success**)
- Product: `docs/runtime/replay_explorer_surface_v1.md`, `starlab/explorer/*`, `tests/fixtures/m31/`, `tests/test_replay_explorer_surface.py`; **558** pytest on merge commit / merge-boundary `main` CI [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged); **560** pytest on doc closeout run [`24226392793`](https://github.com/m-cahill/starlab/actions/runs/24226392793) (**+2** governance tests)
- **M31 proof (narrow):** deterministic offline **`replay_explorer_surface.json`** / **`replay_explorer_surface_report.json`** — bounded panels over M13 slices, M10–M12 excerpts, M16→M18 anchor frame, **M30** hierarchical traces with **M29** validation; **not** benchmark integrity, **not** live SC2, **not** web UI, **not** M39 flagship proof pack
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M31** **Complete** on `main`; **current milestone** → **M32** (**stub-only**); **M32** stubs (`M32_plan.md`, `M32_toolcalls.md`) — **no** M32 product code
- Milestone closeout docs: `M31_run1.md`, `M31_summary.md`, `M31_audit.md`, `M31_plan.md` (**Complete**), `M31_toolcalls.md`
- **Non-merge-boundary** `main` CI on closeout commit `59dcfeca869b1700587a6260aa72822b18ded87b` (short `59dcfec…`): [`24226392793`](https://github.com/m-cahill/starlab/actions/runs/24226392793) (**success**) — documentation + governance + M32 stubs only; **not** product merge authority for M31 (authoritative remains [`24225153475`](https://github.com/m-cahill/starlab/actions/runs/24225153475) + [`24226308356`](https://github.com/m-cahill/starlab/actions/runs/24226308356))

### 2026-04-10 — M30 merged to `main` (PR #36) + milestone closeout

- Merged [PR #36](https://github.com/m-cahill/starlab/pull/36) to `main` at **2026-04-10T02:55:11Z** (UTC); merge commit `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf` (merge method: **merge commit**); remote branch `m30-first-learned-hierarchical-agent` **deleted**
- Final PR head `2a2744527d74acd953507e5b847ef9ce0a7497d3` — **authoritative green PR-head CI:** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) (**success**); **superseded** red PR-head: none recorded
- **Merge-push `main` CI** on merge commit: [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390) (**success**)
- Product: `docs/runtime/replay_hierarchical_imitation_agent_v1.md`, `starlab/hierarchy/` (delegate policy, hierarchical agent fit/predictor, emit CLI), `tests/fixtures/m30/`, `tests/test_replay_hierarchical_imitation_agent.py`; **537** pytest on authoritative PR-head CI [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M30 proof (narrow):** deterministic offline **`replay_hierarchical_imitation_agent.json`** / **`replay_hierarchical_imitation_agent_report.json`** — replay-derived two-level learned imitation with **M29** trace schema (`starlab.hierarchical_agent_interface_trace.v1`), fixed delegate policy **`starlab.m30.delegate.fixed_four_v1`**; stock M26 fixture delegates may be sparse — fallback proof traces documented in `M30_summary.md`; **not** benchmark integrity, **not** live SC2, **not** raw action legality, **not** replay↔execution equivalence, **not** M31 replay explorer semantics
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M30** **Complete** on `main`; **current milestone** → **M31** (**stub-only**); **M31** stubs (`M31_plan.md`, `M31_toolcalls.md`) — **no** M31 product code
- Milestone closeout docs: `M30_run1.md`, `M30_summary.md`, `M30_audit.md`, `M30_plan.md` (**Complete**), `M30_toolcalls.md`
- **Non-merge-boundary** `main` CI on closeout commit `d4c9e63fab1072a1be2e235f74c1b6decc74498d` (short `d4c9e63…`): [`24224064068`](https://github.com/m-cahill/starlab/actions/runs/24224064068) (**success**) — documentation + governance only; **not** product merge authority for M30 (authoritative remains [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) + [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390))

### 2026-04-10 — M29 merged to `main` (PR #35) + milestone closeout

- Merged [PR #35](https://github.com/m-cahill/starlab/pull/35) to `main` at **2026-04-10T01:29:12Z** (UTC); merge commit `187d9ddd8e6b5234245923200c3a396d602e7b06` (merge method: **merge commit**); remote branch `m29-hierarchical-agent-interface-layer` **deleted**
- Final PR head `60554e960a9227202578a3910052acaddf29677a` — **authoritative green PR-head CI:** [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) (**success**); **superseded** red PR-head [`24221737387`](https://github.com/m-cahill/starlab/actions/runs/24221737387) (Ruff format on earlier tip — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088) (**success**)
- Product: `docs/runtime/hierarchical_agent_interface_v1.md`, `starlab/hierarchy/` (`hierarchical_interface_models.py`, `hierarchical_interface_schema.py`, `hierarchical_interface_io.py`, `emit_hierarchical_agent_interface.py`), `tests/fixtures/m29/`, `tests/test_hierarchical_agent_interface.py`; **519** pytest on authoritative PR-head CI [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M29 proof (narrow):** deterministic **`hierarchical_agent_interface_schema.json`** / **`hierarchical_agent_interface_schema_report.json`** — offline **two-level** manager→worker **trace** contract; worker **`semantic_coarse_label`** enum owned by M29, aligned 1:1 to **`starlab.m26.label.coarse_action_v1`** with **`label_policy_id`** on `worker_response`; **not** learned hierarchical agent (**M30**), **not** benchmark integrity, **not** live SC2, **not** raw action legality
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23: **M29** **Complete** on `main`; **current milestone** → **M30** (**stub-only**); **M30** stubs (`M30_plan.md`, `M30_toolcalls.md`)
- Milestone closeout docs: `M29_run1.md`, `M29_summary.md`, `M29_audit.md`, `M29_plan.md` (**Complete**), `M29_toolcalls.md`
- **Non-merge-boundary** `main` CI on closeout commit `d1566dd72884a98845bfb760fd1a591a311723f2` (short `d1566dd…`): [`24221851352`](https://github.com/m-cahill/starlab/actions/runs/24221851352) (**success**) — documentation + governance only; **not** substitute merge authority for M29 **product** (authoritative remains [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) + [`24221791088`](https://github.com/m-cahill/starlab/actions/runs/24221791088))

### 2026-04-10 — M28 merged to `main` (PR #34) + milestone closeout

- Merged [PR #34](https://github.com/m-cahill/starlab/pull/34) to `main` at **2026-04-10T00:35:30Z** (UTC); merge commit `1ef636524269ff77ac26ac37584d43b50e9fcbc6` (merge method: **merge commit**); remote branch `m28-learned-agent-evaluation-harness` **deleted**
- Final PR head `c7ca6e6be8fbd44e39357da82cca857eddbd8eb3` — **authoritative green PR-head CI:** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) (**success**); **superseded** red PR-head: none recorded for M28
- **Merge-push `main` CI** on merge commit: [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) (**success**)
- Product: `docs/runtime/learned_agent_evaluation_harness_v1.md`, `starlab/evaluation/` (learned-agent evaluation + emit CLI), `starlab/imitation/replay_imitation_predictor.py`, `tests/fixtures/m28/`, `tests/test_learned_agent_evaluation.py`; **502** pytest on authoritative PR-head CI [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M28 proof (narrow):** deterministic **offline** **`learned_agent_evaluation.json`** / **`learned_agent_evaluation_report.json`** over **M20** `fixture_only` contract + frozen **M27** + **M26** (held-out **`split == "test"`** only in v1) + referenced **M14** bundles; embedded **M20-compatible** scorecard; **not** benchmark integrity, **not** M23 tournament / M24 diagnostics / M25 evidence-pack semantics, **not** live SC2, **not** replay↔execution equivalence
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **M28** **Complete**; **current milestone** → **M29** (**stub-only**); **35-milestone (M00–M34)** plan unchanged; historical **M00–M27** facts unchanged in substance
- Milestone closeout: `M28_run1.md`, `M28_summary.md`, `M28_audit.md`, `M28_plan.md` (**Complete**), `M28_toolcalls.md`; **M29** stubs (`M29_plan.md`, `M29_toolcalls.md`) — **no** M29 product code

### 2026-04-09 — M27 merged to `main` (PR #33) + milestone closeout

- Merged [PR #33](https://github.com/m-cahill/starlab/pull/33) to `main` at **2026-04-09T23:45:00Z** (UTC); merge commit `49b45825b65e56deb5cf991c5f74889e3daf2f59` (merge method: **merge commit**); remote branch `m27-replay-derived-imitation-baseline` **deleted**
- Final PR head `65dcd2fbfa1b6e8d05f6db8bebe191f4b8822ccc` — **authoritative green PR-head CI:** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) (**success**); **superseded** red PR-head [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) (Ruff format — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) (**success**)
- Product: `docs/runtime/replay_imitation_baseline_v1.md`, `starlab/imitation/` (baseline fit/features/materialization + `emit_replay_imitation_baseline`), `tests/fixtures/m27/`, `tests/test_replay_imitation_baseline.py`; **482** pytest on authoritative PR-head CI [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged)
- **M27 proof (narrow):** **first** deterministic **offline** **replay-derived trained imitation baseline** artifact over governed **M26** + **M14**; **in-process M16 → M18** seam; majority-label-per-signature + lexicographic tie-break + global fallback; **`agreement_by_split`** = internal smoke only — **not** benchmark integrity, live SC2, **M28** harness semantics, hierarchy, or replay↔execution equivalence
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **M27** **Complete**; **current milestone** → **M28** (**stub-only**); **35-milestone (M00–M34)** plan unchanged; historical **M00–M26** facts unchanged in substance
- Milestone closeout: `M27_run1.md`, `M27_summary.md`, `M27_audit.md`, `M27_plan.md` (**Complete**), `M27_toolcalls.md`; **M28** stubs (`M28_plan.md`, `M28_toolcalls.md`) — **no** M28 product code
- **Non-merge-boundary** `main` CI on closeout commit `f41ba737855367136083a6c20d471fbff9b70070` (short `f41ba73…`): [`24218984682`](https://github.com/m-cahill/starlab/actions/runs/24218984682) (**success**) — documentation + governance only; **not** substitute merge authority for M27 **product** (authoritative remains [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) + [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938))

### 2026-04-09 — M26 closeout CI recorded (§18 / `M26_run1.md`)

- **Non-merge-boundary** `main` CI on closeout commit `2ccf60ea3a5aa6a4c4106bf9f6372bde06202d41` (short `2ccf60e…`): [`24217359747`](https://github.com/m-cahill/starlab/actions/runs/24217359747) (**success**) — documentation + governance alignment; **not** substitute merge authority for M26 **product** (PR-head [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) + merge-boundary [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208))

### 2026-04-09 — M26 merged to `main` (PR #32) + milestone closeout

- Merged [PR #32](https://github.com/m-cahill/starlab/pull/32) to `main` at **2026-04-09T22:50:52Z** (UTC); merge commit `e83a8493a577c9013d720f1debab009dcf9c464f` (merge method: **merge commit**); remote branch `m26-replay-corpus-training-dataset-contract` **deleted**
- Final PR head `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f` — **authoritative green PR-head CI:** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) (**success**)
- **Merge-push `main` CI** on merge commit: [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) (**success**)
- Product: `docs/runtime/replay_training_dataset_v1.md`, `starlab/imitation/` (`dataset_models.py`, `dataset_views.py`, `emit_replay_training_dataset.py`), `tests/fixtures/m26/`, `tests/test_replay_training_dataset.py`; **469** pytest on full local `main` tip after closeout (one pre-existing `s2protocol` deprecation warning in replay CLI tests — not M26)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed replay training dataset** (narrow, Phase V) **proved on `main`**; **current milestone** → **M27** (stub); §18 compact closeout + M26 merge rows; score trend M26 row
- **Governance formalized in M26:** the future program arc is **35 milestones (M00–M34)** (revised from **33 milestones (M00–M32)**); **OD-007** → **M34** — recorded in **M26** governance + product merge; **historical M00–M25** merge/CI facts remain unchanged in substance
- Milestone closeout: `M26_run1.md`, `M26_summary.md`, `M26_audit.md`, `M26_plan.md` (**Complete**), `M26_toolcalls.md`; **M27** stubs (`M27_plan.md`, `M27_toolcalls.md`) — **no** M27 product code

### 2026-04-09 — M26 governance: future milestone arc revised (33 → 35 milestones)

- **Governance (ledger-only):** the **planned program arc** is revised from **33 milestones (M00–M32)** to **35 milestones (M00–M34)** as part of **M26** planning — **historical M00–M25 closed-milestone facts, merge SHAs, and CI evidence are unchanged**.
- **Renumbering / renaming (future plan only):** **M26** is **Replay Corpus Governance & Training Dataset Contract**; **M27** — Replay-Derived Imitation Baseline; **M28** — Learned-Agent Evaluation Harness; **M29** — Hierarchical Agent Interface Layer; **M30** — First Learned Hierarchical Agent; **M31** — Replay Explorer / Operator Evidence Surface; **M32** — Public Flagship Proof Pack; **M33** — SC2 Substrate Review & Expansion Decision; **M34** — Platform Boundary Review & Multi-Environment Charter.
- **OD-007** target milestone updated from **M32** to **M34** (second-environment / multi-environment charter posture).
- **Product (M26 scope):** `docs/runtime/replay_training_dataset_v1.md`, `starlab/imitation/` (dataset emitters + CLI), `tests/fixtures/m26/` goldens, `tests/test_replay_training_dataset.py` — **replay-derived training dataset contract only**; **not** **M27** imitation-baseline training code.

### 2026-04-09 — M25 merged to `main` (PR #31) + milestone closeout

- Merged [PR #31](https://github.com/m-cahill/starlab/pull/31) to `main` at **2026-04-09T21:57:32Z** (UTC); merge commit `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b` (merge method: **merge commit**); remote branch `m25-baseline-evidence-pack` **deleted**
- Final PR head `b132bfd53f0f31b81f6d2955ca659d5923cdd4b1` — **authoritative green PR-head CI:** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) (**success**)
- **Merge-push `main` CI** on merge commit: [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351) (**success**)
- **Superseded** red PR-head runs [`24215241322`](https://github.com/m-cahill/starlab/actions/runs/24215241322), [`24215286216`](https://github.com/m-cahill/starlab/actions/runs/24215286216) — **not** merge authority (see `M25_run1.md`)
- Product: `docs/runtime/baseline_evidence_pack_v1.md`, `starlab/evaluation/evidence_pack_models.py`, `evidence_pack_views.py`, `emit_baseline_evidence_pack.py`, `tests/fixtures/m25/`, `tests/test_baseline_evidence_pack.py` (includes **M20 → M21/M22 → M23 → M24 → M25** chain test); **448** pytest on authoritative PR-head CI [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M25). **449** pytest on full `main` after this closeout commit (milestone docs + governance tests) — **not** additional product merge authority for M25
- §3 / §6 / §7 / §9 / §11 / §18 / §23: **governed baseline evidence pack** (narrow) **proved on `main`**; Phase IV chain through **M25**; **current milestone** → **M26** (stub); evidence-pack glossary; M25 merge rows in §18
- Milestone closeout: `M25_run1.md`, `M25_summary.md`, `M25_audit.md`, `M25_plan.md` (**Complete**), `M25_toolcalls.md`; **M26** stubs (`M26_plan.md`, `M26_toolcalls.md`) — **no** M26 product code
- **Non-merge-boundary** `main` CI — closeout commit `78ced31526e4370e43d4ddbf8887ac827853e55d` (short `78ced31…`): [`24215484700`](https://github.com/m-cahill/starlab/actions/runs/24215484700) (**success**) — milestone docs + ledger + governance tests only; **authoritative** M25 **product** merge evidence remains PR-head [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) + merge-boundary [`24215360351`](https://github.com/m-cahill/starlab/actions/runs/24215360351)

### 2026-04-09 — M24 merged to `main` (PR #27) + milestone closeout

- Merged [PR #27](https://github.com/m-cahill/starlab/pull/27) to `main` at **2026-04-09T21:00:08Z** (UTC); merge commit `7b4d3b4603dc40fe2ade33e1c943a0efd40ca5a4` (merge method: **merge commit**); remote branch `m24-evaluation-diagnostics-failure-views` **deleted**
- Final PR head `5caf1fbdbe7f7441fc2c8144efc3b18a37682779` — **authoritative green PR-head CI:** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) (**success**)
- **Merge-push `main` CI** on merge commit: [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) (**success**)
- Product: `docs/runtime/evaluation_diagnostics_failure_views_v1.md`, `starlab/evaluation/diagnostics_models.py`, `diagnostics_views.py`, `emit_evaluation_diagnostics.py`, `tests/fixtures/m24/`, `tests/test_evaluation_diagnostics.py` (includes **M20 → M21/M22 emitters → M23 → M24** chain test); **436** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M24)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed fixture-only evaluation diagnostics** (narrow) **proved on `main`**; Phase IV chain (M20 contract / M21–M22 emitters / **M23** runner / **M24** diagnostics); **current milestone** → **M25** (planned); compact closeout table M23–M24 rows; Phase IV diagnostics glossary
- Milestone closeout: `M24_run1.md`, `M24_summary.md`, `M24_audit.md`, `M24_plan.md` (**Complete**), `M24_toolcalls.md`; **M25** stubs (`M25_plan.md`, `M25_toolcalls.md`) — **no** M25 product code
- Merged [PR #28](https://github.com/m-cahill/starlab/pull/28) to `main` at **2026-04-09T21:05:11Z** (UTC); merge commit `5590f544cb29e7ad14fcbf5398903995b27da95c` (merge method: **merge commit**); remote branch `m24-closeout-docs` **deleted**
- Final PR head `49f175d108ec3bb9eaed7044be92471994c9b79e` — **green PR-head CI** (doc/governance closeout): [`24213306545`](https://github.com/m-cahill/starlab/actions/runs/24213306545) (**success**) — **not** product merge authority for M24
- **Merge-push `main` CI** on merge commit: [`24213308716`](https://github.com/m-cahill/starlab/actions/runs/24213308716) (**success**) — milestone docs + governance tests only; **authoritative** M24 **product** merge evidence remains PR-head [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) + merge-boundary [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) ([PR #27](https://github.com/m-cahill/starlab/pull/27))
- Merged [PR #29](https://github.com/m-cahill/starlab/pull/29) to `main` at **2026-04-09T21:06:41Z** (UTC); merge commit `2a7d979e64c5001a390014f91f914c618d7f2cb6` (merge method: **merge commit**); remote branch `m24-pr28-ci-record` **deleted** — records PR #28 CI in `M24_run1.md` / §23; **merge-push `main` CI** [`24213371024`](https://github.com/m-cahill/starlab/actions/runs/24213371024) (**success**; initial attempt **cancelled** due to Actions concurrency — **rerun** green) — **not** product merge authority for M24

### 2026-04-09 — M23 merged to `main` (PR #24) + closeout

- Merged [PR #24](https://github.com/m-cahill/starlab/pull/24) to `main` at **2026-04-09T07:41:53Z**; merge commit `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252` (merge method: **merge commit**); remote branch `m23-evaluation-runner-tournament-harness` **deleted**
- Final PR head `f00711a3a2c16573f31492398de59387fe284711` — **authoritative green PR-head CI:** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) (**success**)
- **Merge-push `main` CI** on merge commit: [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) (**success**)
- Product: `docs/runtime/evaluation_runner_tournament_harness_v1.md`, `starlab/evaluation/` (runner + round-robin harness + `python -m starlab.evaluation.emit_evaluation_tournament`), `tests/fixtures/m23/`, `tests/test_evaluation_tournament.py` (includes **M20 → M21/M22 emitters → M23** chain test); **413** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M23)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed fixture-only evaluation tournament** (narrow) **proved on `main`**; Phase IV chain (M20 contract / M21–M22 emitters / **M23** runner); **current milestone** → **M24** (stub); score trend M23 row; Phase IV evaluation/tournament glossary
- Milestone closeout: `M23_run1.md`, `M23_summary.md`, `M23_audit.md`, `M23_plan.md` (**closed**), `M23_toolcalls.md`; **M24** stubs (`M24_plan.md`, `M24_toolcalls.md`) — **no** M24 product code
- Merged [PR #25](https://github.com/m-cahill/starlab/pull/25) to `main` at **2026-04-09T07:45:11Z**; merge commit `317b3a02c8b7977e3af597069899e1fe9454cafd` (merge method: **merge commit**); remote branch `m23-closeout-docs` **deleted**
- Final PR head `1b6e7b76e97cf2fffaa549526ff80249c698be6c` — **green PR-head CI** (doc-only closeout): [`24178744293`](https://github.com/m-cahill/starlab/actions/runs/24178744293) (**success**) — **not** product merge authority for M23
- **Non-merge-boundary** `main` CI — merge commit `317b3a0…`: [`24178745007`](https://github.com/m-cahill/starlab/actions/runs/24178745007) (**success**) — milestone docs + ledger + governance tests only; **authoritative** M23 product merge evidence remains PR-head [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) + merge-boundary [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940)

### 2026-04-09 — M22 merged to `main` (PR #23) + closeout

- Merged [PR #23](https://github.com/m-cahill/starlab/pull/23) to `main` at **2026-04-09T06:50:36Z**; merge commit `470afa84ff80a2d76fb2693bce3a4397e6526afe` (merge method: **merge commit**); remote branch `m22-heuristic-baseline-suite` **deleted**
- Final PR head `96aba181f725b1303d54779d48556b7dffd7feb4` — **authoritative green PR-head CI:** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) (**success**)
- **Merge-push `main` CI** on merge commit: [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) (**success**)
- Product: `docs/runtime/heuristic_baseline_suite_v1.md`, `starlab/baselines/` (heuristic suite + scorecards + CLI), `tests/fixtures/m22/`, `tests/test_heuristic_baseline_suite.py`; **392** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M22)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed heuristic baseline suite** (narrow) **proved on `main`**; Phase IV boundary (M20 contract / M21–M22 fixture-only emitters / M23 runner); **current milestone** → **M23** (stub); closeout ledger M22 row; score trend M22 note
- Milestone closeout: `M22_run1.md`, `M22_summary.md`, `M22_audit.md`, `M22_plan.md` (**Status: Complete**), `M22_toolcalls.md`; **M23** stubs (`M23_plan.md`, `M23_toolcalls.md`) — **no** M23 product code

### 2026-04-09 — M21 merged to `main` (PR #22) + closeout

- Merged [PR #22](https://github.com/m-cahill/starlab/pull/22) to `main` at **2026-04-09T05:41:36Z**; merge commit `092d00a8aff720a1df9cbb1beec1cbf661546953` (merge method: **merge commit**); remote branch `m21-scripted-baseline-suite` **deleted**
- Final PR head `818002e56b512e504c27f12aba8a39bc73627c82` — **authoritative green PR-head CI:** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) (**success**)
- **Merge-push `main` CI** on merge commit: [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) (**success**)
- Product: `docs/runtime/scripted_baseline_suite_v1.md`, `starlab/baselines/` (suite + scorecards + CLI), `tests/fixtures/m21/`, `tests/test_scripted_baseline_suite.py`; **371** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M21)
- **Superseded** red PR-head [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) (Ruff format — **not** merge authority, **M21**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed scripted baseline suite** (narrow) **proved on `main`**; **current milestone** → **M22** (stub); closeout ledger M21 row; score trend M21 note
- Milestone closeout: `M21_run1.md`, `M21_summary.md`, `M21_audit.md`, `M21_plan.md` (**closed**), `M21_toolcalls.md`; **M22** stubs (`M22_plan.md`, `M22_toolcalls.md`) — **no** M22 product code
- **Non-merge-boundary** `main` CI — closeout commit `25719da03418c729143c9c48d8106e76a51c2de9` (short `25719da…`): [`24174583165`](https://github.com/m-cahill/starlab/actions/runs/24174583165) (**success**) — milestone docs + ledger + governance tests only; **authoritative** M21 product merge evidence remains PR-head [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) + merge-boundary [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486)

### 2026-04-09 — M20 merged to `main` (PR #21) + closeout

- Merged [PR #21](https://github.com/m-cahill/starlab/pull/21) to `main` at **2026-04-09T04:59:35Z**; merge commit `cf1bee980756b3b59d4db2620c041a23f14eba18` (merge method: **merge commit**); remote branch `m20-benchmark-contract-scorecard-semantics` **deleted**
- Final PR head `5c2233690a3dc6d352dd9b06be16430b3d73b6e8` — **authoritative green PR-head CI:** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) (**success**)
- **Merge-push `main` CI** on merge commit: [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) (**success**)
- Product: `docs/runtime/benchmark_contract_scorecard_v1.md`, `starlab/benchmarks/` (contract models + JSON Schema builders + `python -m starlab.benchmarks.emit_benchmark_contracts`), `tests/fixtures/m20/`, `tests/test_benchmark_contracts.py`; **357** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M20)
- Phase IV artifact row + Phase IV scorecard glossary (`scored` / `unscored` / `disqualified` / `comparable` / `provisional` / `non_comparable`)
- §3 / §6 / §10 / §11 / §18 / §20 / §23: **governed benchmark contract + scorecard schemas** (narrow) **proved on `main`**; **current milestone** → **M21** (stub); closeout ledger M20 row; score trend M20 note
- Milestone closeout: `M20_run1.md`, `M20_summary.md`, `M20_audit.md`, `M20_plan.md` (**closed**), `M20_toolcalls.md`; **M21** stubs (`M21_plan.md`, `M21_toolcalls.md`) — **no** M21 product code
- **Non-merge-boundary** `main` CI — closeout commit `8d6a1135bc2f71a729cf81cad4b5ee6adb022626`: [`24173318958`](https://github.com/m-cahill/starlab/actions/runs/24173318958) (**success**) — milestone docs + ledger + governance test only; **authoritative** M20 product merge evidence remains PR-head [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) + merge-boundary [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201)

### 2026-04-09 — M18 merged to `main` (PR #19) + closeout

- Merged [PR #19](https://github.com/m-cahill/starlab/pull/19) to `main` at **2026-04-09T00:32:06Z**; merge commit `59d2d6e2af08852d63e0c91a984000c11decfece` (merge method: **merge commit**); remote branch `m18-perceptual-bridge-prototype` **deleted**
- Final PR head `8d9f9e1f8343120dd32916fb23668fd0ecee3fa0` — **authoritative green PR-head CI:** [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) (**success**)
- **Merge-push `main` CI** on merge commit: [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479) (**success**)
- Product: `docs/runtime/perceptual_bridge_prototype_v1.md`, `starlab/observation/` materialization modules + CLI, `tests/fixtures/m18/`, `tests/test_observation_surface_pipeline.py`; **322** pytest on authoritative CI (one pre-existing `s2protocol` deprecation warning in replay CLI test — not M18)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed perceptual bridge prototype** (narrow) **proved on `main`**; Phase III progression (M15 schema / M16 bundle→frame / M17 observation contract / **M18 prototype bridge**); **current milestone** → **M19** (stub); closeout ledger M18 row; score trend M18 note
- Milestone closeout: `M18_run1.md`, `M18_summary.md`, `M18_audit.md`, `M18_plan.md` (**closed**), `M18_toolcalls.md`; **M19** stubs (`M19_plan.md`, `M19_toolcalls.md`) — **no** M19 product code
- **Non-merge-boundary** `main` CI — closeout commit `977b625f09ab3db893c26a31e6c3c0e730a9fea4`: [`24166079739`](https://github.com/m-cahill/starlab/actions/runs/24166079739) (**success**) — milestone docs + ledger only; **authoritative** M18 product merge evidence remains PR-head [`24165977039`](https://github.com/m-cahill/starlab/actions/runs/24165977039) + merge-boundary [`24166004479`](https://github.com/m-cahill/starlab/actions/runs/24166004479)

### 2026-04-08 — M17 merged to `main` (PR #18) + closeout

- Merged [PR #18](https://github.com/m-cahill/starlab/pull/18) to `main` at **2026-04-08T23:30:53Z**; merge commit `f63c8e93cb0a2943b9149f4384dbde68b74f9e76` (merge method: **merge commit**); remote branch `m17-observation-surface-contract` **deleted**
- Final PR head `801af8b9c1a525e19fe3804cb7ed968e80d8b0f6` — **authoritative green PR-head CI:** [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) (**success**)
- **Merge-push `main` CI** on merge commit: [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167) (**success**)
- Product: `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/` (contract-only), `tests/fixtures/m17/`, observation tests; **310** pytest on authoritative CI
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23: **governed observation surface contract** (narrow) **proved on `main`**; Phase III progression (M15 schema / M16 bundle→frame / **M17 observation contract** / M18 bridge stub); **current milestone** → **M18**; closeout ledger M17 row; score trend M17 note
- Milestone closeout: `M17_run1.md`, `M17_summary.md`, `M17_audit.md`, `M17_plan.md` (**closed**), `M17_toolcalls.md`; **M18** stubs (`M18_plan.md`, `M18_toolcalls.md`) — **no** M18 product code
- **Non-merge-boundary** `main` CI — closeout commit `87fd04617ad06522efca8d6a89e31d74c83e12cb`: [`24164136804`](https://github.com/m-cahill/starlab/actions/runs/24164136804) (**success**) — milestone docs + ledger only; **authoritative** M17 product merge evidence remains PR-head [`24164045530`](https://github.com/m-cahill/starlab/actions/runs/24164045530) + merge-boundary [`24164075167`](https://github.com/m-cahill/starlab/actions/runs/24164075167)

### 2026-04-08 — M16 merged to `main` (PR #17) + closeout

- Merged [PR #17](https://github.com/m-cahill/starlab/pull/17) to `main` at **2026-04-08T21:58:44Z**; merge commit `dd9546f88ebcf9b454498eec83a14d742d17d070` (merge method: **merge commit**); remote branch `m16-structured-state-pipeline` **deleted**
- Final PR head `11fb0803b8fa0343c08d9c3bda06929092a437d1` — **authoritative green PR-head CI:** [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) (**success**); superseded red PR-head [`24160804226`](https://github.com/m-cahill/starlab/actions/runs/24160804226) (Ruff format — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811) (**success**)
- §3 / §6 / §7 / §8 / §10 / §11 / §18 / §20 / §23 updated: **governed structured state pipeline** (narrow) **proved on `main`**; Phase III artifact row (M16); Phase III glossary (M15 schema-only vs M16 pipeline vs M17 observation); **current milestone** → **M17** (stub); closeout ledger M16 row + compact table M16 row; score trend M16 note
- Milestone closeout: `M16_run1.md`, `M16_summary.md`, `M16_audit.md`, `M16_plan.md` (**Status: Complete**), `M16_toolcalls.md`; **M17** stubs present (`M17_plan.md`, `M17_toolcalls.md`) — **no** M17 product code in this pass
- **Non-merge-boundary** `main` CI — closeout commit `a6a3ea62e8bfa036b87727e1d8e93a60176c4ef8` (short `a6a3ea6…`): [`24160991810`](https://github.com/m-cahill/starlab/actions/runs/24160991810) (**success**) — ledger + milestone artifacts + governance tests only; **authoritative** PR-head / merge-boundary CI for M16 product merge remains [`24160830775`](https://github.com/m-cahill/starlab/actions/runs/24160830775) / [`24160871811`](https://github.com/m-cahill/starlab/actions/runs/24160871811)
- **Non-merge-boundary** `main` CI — follow-up commit `7b1731f151a3ae75006f039a0b79cdec48561289` (short `7b1731f…`): [`24161024608`](https://github.com/m-cahill/starlab/actions/runs/24161024608) (**success**) — changelog row for prior closeout run; **not** merge authority

### 2026-04-08 — M15 merged to `main` (PR #16) + closeout

- Merged [PR #16](https://github.com/m-cahill/starlab/pull/16) to `main` at **2026-04-08T06:51:06Z**; merge commit `b0f7132a54508f35d54406011cd3b37bce776927` (merge method: **merge commit**); remote branch `m15-canonical-state-schema-v1` **deleted**
- Final PR head `abc8ffcd223536568fcf134b1e21273915cf1d4d` — **authoritative green PR-head CI:** [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) (**success**); superseded red PR-head [`24121376545`](https://github.com/m-cahill/starlab/actions/runs/24121376545) (Mypy — **not** merge authority)
- **Merge-push `main` CI** on merge commit: [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed canonical state schema v1** (narrow) **proved on `main`**; Phase III artifact row (M15); Phase III glossary (M15 vs M16 vs M17); **current milestone** → **M16** (stub); closeout ledger M15 row + compact table M14/M15 rows; score trend M15 note
- Milestone closeout: `M15_run1.md`, `M15_summary.md`, `M15_audit.md`, `M15_plan.md` (**Status: Complete**), `M15_toolcalls.md`; **M16** stubs seeded (`M16_plan.md`, `M16_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `1c1e89ed8137c5df9d2c0d7e0ee4e5ff886c00e0` (short `1c1e89e…`): [`24122183559`](https://github.com/m-cahill/starlab/actions/runs/24122183559) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M15 product merge remains [`24122064141`](https://github.com/m-cahill/starlab/actions/runs/24122064141) / [`24122092800`](https://github.com/m-cahill/starlab/actions/runs/24122092800)
- **Non-merge-boundary** `main` CI — follow-up commit `0764cae100848b52eb18933ce630daa7629c5ac3`: [`24122213663`](https://github.com/m-cahill/starlab/actions/runs/24122213663) (**success**) — changelog row for prior closeout run; **not** merge authority

### 2026-04-08 — M14 merged to `main` (PR #15) + closeout

- Merged [PR #15](https://github.com/m-cahill/starlab/pull/15) to `main` at **2026-04-08T05:00:41Z**; merge commit `8a0439a9a2970a74f3a5087390fc080f02852246` (merge method: **merge commit**); remote branch `m14-replay-bundle-lineage-contract-v1` **deleted**
- Final PR head `42e29f2a64fa4672dbd2df435a04836c379b5258` — **authoritative green PR-head CI:** [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) (**success**)
- **Merge-push `main` CI** on merge commit: [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay bundle packaging + lineage contract v1** (narrow) **proved on `main`**; Phase II artifact row (M14); **current milestone** → **M15** (stub); closeout ledger M14 row; score trend M14 note; Phase II complete with M14
- Milestone closeout: `M14_run1.md`, `M14_summary.md`, `M14_audit.md`, `M14_plan.md` (**Status: Complete**), `M14_toolcalls.md`; **M15** stubs seeded (`M15_plan.md`, `M15_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `680d966b5115e22cb67fee76da15c9a2c261de10` (short `680d966…`): [`24118726116`](https://github.com/m-cahill/starlab/actions/runs/24118726116) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M14 product merge remains [`24118622373`](https://github.com/m-cahill/starlab/actions/runs/24118622373) / [`24118654909`](https://github.com/m-cahill/starlab/actions/runs/24118654909)

### 2026-04-08 — M13 merged to `main` (PR #14) + closeout

- Merged [PR #14](https://github.com/m-cahill/starlab/pull/14) to `main` at **2026-04-08T01:20:38Z**; merge commit `f86e36837e81b8552639c5a885a13a773b96215c` (merge method: **merge commit**); remote branch `m13-replay-slice-generator` **deleted**
- Final PR head `6231b19cd7067130fd3324dcd3070172333ba766` — **authoritative green PR-head CI:** [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) (**success**)
- **Merge-push `main` CI** on merge commit: [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay slice definitions** (narrow) **proved on `main`**; Phase II artifact row (M13); slice/bundle glossary + Phase II boundary note; **current milestone** → **M14** (stub); closeout ledger M13 row; score trend M13 note
- Milestone closeout: `M13_run1.md`, `M13_summary.md`, `M13_audit.md`, `M13_plan.md` (**Status: Complete**), `M13_toolcalls.md`; **M14** stubs seeded (`M14_plan.md`, `M14_toolcalls.md`)

### 2026-04-07 — M12 merged to `main` (PR #13) + closeout

- Merged [PR #13](https://github.com/m-cahill/starlab/pull/13) to `main` at **2026-04-07T23:23:48Z**; merge commit `78528958a616177b564e603c193fb0d7f8af734e` (merge method: **merge commit**); remote branch `m12-combat-scouting-visibility-windows` **deleted**
- Final PR head `59adce3422a840692a4961278c995c5029da43bb` — **authoritative green PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) (**success**)
- **Merge-push `main` CI** on merge commit: [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed combat / scouting / visibility plane** (narrow) **proved on `main`**; **current milestone** → **M13** (stub); closeout ledger M12 row; score trend M12 note
- Milestone closeout: `M12_run1.md`, `M12_summary.md`, `M12_audit.md`, `M12_plan.md` (**Status: Complete**), `M12_toolcalls.md`; **M13** stubs seeded (`M13_plan.md`, `M13_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `87ab90fd9bec523409c609c9adb8d5465406f9c1`: [`24109339683`](https://github.com/m-cahill/starlab/actions/runs/24109339683) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M12 product merge remains [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) / [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513)

### 2026-04-07 — M11 merged to `main` (PR #12) + closeout

- Merged [PR #12](https://github.com/m-cahill/starlab/pull/12) to `main` at **2026-04-07T21:49:23Z**; merge commit `38c15302badd49966b17f9195ddb139f6ae9a9b4` (merge method: **merge commit**); remote branch `m11-build-order-economy-plane` **deleted**
- Final PR head `88ce7f9615c6c462b76674e1afb0734fc3dcc5be` — **authoritative green PR-head CI:** [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) (**success**)
- **Merge-push `main` CI** on merge commit: [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed build-order / economy plane** (narrow) **proved on `main`**; **current milestone** → **M12** (stub); closeout ledger M11 row; score trend M11 note; Phase II layering chain + parser glossary alignment
- Milestone closeout: `M11_run1.md`, `M11_summary.md`, `M11_audit.md`, `M11_plan.md` (**Status: Complete**), `M11_toolcalls.md`; **M12** stubs seeded (`M12_plan.md`, `M12_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `0ebc81b6044c39809aa94f5e7f04915936b00e1e`: [`24106210049`](https://github.com/m-cahill/starlab/actions/runs/24106210049) (**success**) — ledger + milestone artifacts only; **authoritative** PR-head / merge-boundary CI for M11 product merge remains [`24106029320`](https://github.com/m-cahill/starlab/actions/runs/24106029320) / [`24106124347`](https://github.com/m-cahill/starlab/actions/runs/24106124347)

### 2026-04-07 — M10 merged to `main` (PR #11) + closeout

- Merged [PR #11](https://github.com/m-cahill/starlab/pull/11) to `main` at **2026-04-07T20:58:46Z**; merge commit `cb3e581f70f85653477081eb1ef4772229f05983` (merge method: **merge commit**); remote branch `m10-timeline-event-extraction` **deleted**
- Final PR head `cb066fe3f09b07f3390e85928c88f65a6e75cd6f` — **witnessed PR-head CI:** [`24104110934`](https://github.com/m-cahill/starlab/actions/runs/24104110934) (**cancelled** — no green merge-gate run on final tip)
- **Merge-push `main` CI** on merge commit: [`24104111851`](https://github.com/m-cahill/starlab/actions/runs/24104111851) (**failure** — Mypy)
- **Mypy repair** `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b` — **authoritative green `main` CI:** [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912) (**success**) — **not** a merge-boundary event
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **governed event/timeline extraction** (narrow) **proved on `main`**; **current milestone** → **M11** (stub); closeout ledger M10 row; score trend M10 note
- Milestone closeout: `M10_run1.md`, `M10_summary.md`, `M10_audit.md`, `M10_plan.md` (**Status: Complete**), `M10_toolcalls.md`; **M11** remains stub-only (`M11_plan.md`, `M11_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `f78a435e50e27b725b34548d0037771d3bfccf49`: [`24104280039`](https://github.com/m-cahill/starlab/actions/runs/24104280039) (**success**) — **not** merge-boundary; **authoritative** green repair `main` remains `cf2074e…` / [`24104197912`](https://github.com/m-cahill/starlab/actions/runs/24104197912)

### 2026-04-07 — M10: timeline & event extraction (pre-merge implementation log)

- **Historical:** development log before **PR #11** merged **2026-04-07**; authoritative merge + CI — see changelog entry **2026-04-07 — M10 merged to `main` (PR #11) + closeout**
- **M10** delivers governed **`replay_timeline.json`** / **`replay_timeline_report.json`**, **`docs/runtime/replay_timeline_event_extraction.md`**, parser-boundary extension **`raw_event_streams`** on **`replay_raw_parse.json`** schema **`starlab.replay_raw_parse.v2`** (when the adapter lowers streams), extraction modules + CLI (`python -m starlab.replays.extract_replay_timeline`), and fixture-driven tests under `tests/fixtures/m10/`.
- **M09** accepts raw-parse schema **v1** or **v2** for metadata extraction linkage.

### 2026-04-07 — M09 merged to `main` (PR #10) + closeout

- Merged [PR #10](https://github.com/m-cahill/starlab/pull/10) to `main` at **2026-04-07T20:05:59Z**; merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` (merge method: **merge commit**); remote branch `m09-replay-metadata-extraction` **deleted**
- Final PR head `3f161dea12a9b7ffb6dbe01c73b01f351a7219da` — **authoritative PR-head CI:** [`24101861888`](https://github.com/m-cahill/starlab/actions/runs/24101861888) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) (**success**)
- §3 / §6 / §7 / §10 / §11 / §18 / §20 / §23 updated: **stable normalized replay metadata** (narrow) **proved on `main`**; Phase II artifact row (M09); metadata field glossary; **current milestone** → **M10** (stub only)
- Milestone closeout: `M09_run1.md`, `M09_summary.md`, `M09_audit.md`, `M09_plan.md` (**Status: Complete**), `M09_toolcalls.md`; **M10** stubs seeded (`M10_plan.md`, `M10_toolcalls.md`).
- **Non-merge-boundary** `main` CI — closeout commit `147b1f4810ad2e0dbb926c7a971748c4db68bdbc`: [`24102029092`](https://github.com/m-cahill/starlab/actions/runs/24102029092) (**success**) — ledger + milestone artifacts only; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `44a0bce631854e6039442ca49609228a0650adf3`: [`24102071251`](https://github.com/m-cahill/starlab/actions/runs/24102071251) (**success**) — ledger / `M09_run1` non-merge-boundary row hygiene — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `2d3bc95d97b14a01d40d41b84565f270ca6b22ab`: [`24102113672`](https://github.com/m-cahill/starlab/actions/runs/24102113672) (**success**) — §23 / `M09_run1` sync for prior non-merge-boundary row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `bdd75b95af1de4fae1ee1bf3f5dea0d0d6aabaec`: [`24102151912`](https://github.com/m-cahill/starlab/actions/runs/24102151912) (**success**) — ledger / `M09_run1` sync for `2d3bc95…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `cedcd410b829261bc479ef4eb2a3faab2a07fd0c`: [`24102190259`](https://github.com/m-cahill/starlab/actions/runs/24102190259) (**success**) — ledger / `M09_run1` sync for `bdd75b9…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `887037bb6af16cf3205423fc33ef71cd619d040d`: [`24102230285`](https://github.com/m-cahill/starlab/actions/runs/24102230285) (**success**) — ledger / `M09_run1` sync for `cedcd41…` CI row — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `b4c5cfc55b9c5203deee8adc3e113f2233d13ffe`: [`24102263459`](https://github.com/m-cahill/starlab/actions/runs/24102263459) (**success**) — final ledger / `M09_run1` sync for `887037b…` CI row (see `M09_run1` footnote on capping doc/CI rows) — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.
- **Non-merge-boundary** `main` CI — follow-up commit `f4d47ac2267b7993da6e2a94d47b5eb0c2402f08`: [`24102304889`](https://github.com/m-cahill/starlab/actions/runs/24102304889) (**success**) — `M09_run1` table cap + doc/CI loop-stop footnote (no new table row per that footnote) — **not** a merge-boundary event; **authoritative** merge-boundary post-merge `main` CI for M09 remains [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) on merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.

### 2026-04-07 — M08 merged to `main` (PR #9) + closeout

- Merged [PR #9](https://github.com/m-cahill/starlab/pull/9) to `main` at **2026-04-07T07:52:12Z**; merge commit `b99233e807177d65737beaba5246efa67a3edce2` (merge method: **merge commit**); remote branch `m08-replay-parser-substrate` **deleted**
- Final PR head `a65fabfa7fd76d94a250208fe20c2c4dfdf57105` — **authoritative PR-head CI:** [`24069974048`](https://github.com/m-cahill/starlab/actions/runs/24069974048) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**)
- §7 / §10 / §11 / §18 / §20 / §23 updated: **governed replay parser substrate** (narrow) **proved on `main`**; Phase II artifact row (M08); parser glossary (raw blocks vs normalized metadata vs event semantics); **current milestone** → **M09** (stub only)
- Milestone closeout: `M08_run1.md`, `M08_summary.md`, `M08_audit.md`, `M08_plan.md` (**Status: Complete**), `M08_toolcalls.md`; **M09** remains stub-only (`M09_plan.md`, `M09_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `a089f18dfa1306ab041b32430dcbfbf2339eb8de`: [`24070704576`](https://github.com/m-cahill/starlab/actions/runs/24070704576) (**failure** — Pytest: governance test expected §11 **M08**); fix commit `c3b6f2c25efe2252d27d2d78065035f8965edc48`: [`24070774045`](https://github.com/m-cahill/starlab/actions/runs/24070774045) (**success**); ledger CI record commit `1cca0219350237c7288ceb2d5d814bb1b5224a03`: [`24070813310`](https://github.com/m-cahill/starlab/actions/runs/24070813310) (**success**) — **authoritative** merge-boundary post-merge `main` CI remains [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) on merge commit `b99233e807177d65737beaba5246efa67a3edce2`

### 2026-04-07 — M07 merged to `main` (PR #8) + closeout

- Merged [PR #8](https://github.com/m-cahill/starlab/pull/8) to `main` at **2026-04-07T05:50:09Z**; merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a` (merge method: **merge commit**); remote branch `m07-replay-intake-policy-provenance-enforcement` **deleted**
- Final PR head `a5188ad88bab688ab40136dea77a8b4d3caa0495` — **authoritative PR-head CI:** [`24065819186`](https://github.com/m-cahill/starlab/actions/runs/24065819186) (**success**)
- **Authoritative post-merge `main` CI** on merge commit: [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) (**success**)
- §7 / §10 / §11 / §16 / §18 / §20 / §23 updated: **replay intake / provenance gate** (narrow) **proved on `main`**; **current milestone** → **M08** (stub only); **replay parser substrate** — **not** proved
- Milestone closeout: `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, `M07_plan.md` (**Status: Complete**), `M07_toolcalls.md`; **M08** remains stub-only (`M08_plan.md`, `M08_toolcalls.md`)
- **Non-merge-boundary** `main` CI — closeout commit `2ccac7ed1d9d3fc3c466916f41f1c4d6e9d6a2cc`: [`24066606427`](https://github.com/m-cahill/starlab/actions/runs/24066606427) (**success**); ledger/CI-ID hygiene commit `20a18706fe0c7338fbe4e1922e1a84ae7dc800d9`: [`24066644075`](https://github.com/m-cahill/starlab/actions/runs/24066644075) (**success**) — both **doc-only**; **authoritative** merge-boundary post-merge `main` CI remains [`24066550699`](https://github.com/m-cahill/starlab/actions/runs/24066550699) on merge commit `1c7bb0c0381c0f3c8a3eab354ca53e3e503d8d2a`

### 2026-04-06 — M07 replay intake policy & provenance enforcement (pre-merge branch; superseded by PR #8 merge)

- **Historical:** development log before **PR #8** merged **2026-04-07**; authoritative merge + CI — see §18 and changelog entry **2026-04-07 — M07 merged to `main` (PR #8) + closeout**
- **Branch:** `m07-replay-intake-policy-provenance-enforcement`; **superseded:** merged via [PR #8](https://github.com/m-cahill/starlab/pull/8)
- **Contract:** `docs/runtime/replay_intake_policy.md`; **policy version** `starlab.replay_intake_policy.v1`
- **Code:** `starlab/replays/` (`intake_models.py`, `intake_policy.py`, `intake_io.py`, `intake_cli.py`); `load_canonical_manifest` in `starlab/runs/canonical_run_artifact.py`
- **Artifacts:** `replay_intake_receipt.json`, `replay_intake_report.json` (deterministic JSON; exit codes 0/2/3/4)
- **Tests:** `tests/test_replay_intake.py`, `tests/test_replay_intake_cli.py`; fixtures `replay_m07_sample.SC2Replay`, `replay_m07_generated.SC2Replay`
- **Ledger:** Phase II artifact-contract row (M07), intake status glossary (§9), rights/provenance tracker split (§16), **OD-003** resolved (M07); **§11** current milestone → **M08**; **M08** stubs under `docs/company_secrets/milestones/M08/`
- **Explicit non-proofs:** replay parser, replay semantic extraction, benchmark integrity, live SC2 in CI, legal certification of third-party rights
- **Closeout docs:** finalized in **2026-04-07** entry after merge — `M07_run1.md`, `M07_summary.md`, `M07_audit.md`, `M07_plan.md` (**Status: Complete**)

### 2026-04-07 — M06 merged to `main` (PR #7) + closeout

- Merged [PR #7](https://github.com/m-cahill/starlab/pull/7) to `main` at **2026-04-07T04:26:10Z**; merge commit `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a` (merge method: **merge commit**); remote branch `m06-environment-drift-runtime-smoke-matrix` **deleted**
- Final PR head `6f9ef463f90abe914f3c98c8977d49f8da0102cb` — authoritative PR-head CI: [`24064200725`](https://github.com/m-cahill/starlab/actions/runs/24064200725) (**success**); superseded failed run [`24064181198`](https://github.com/m-cahill/starlab/actions/runs/24064181198) (Ruff format only — fixed before merge)
- Post-merge `main` CI on merge commit: [`24064229874`](https://github.com/m-cahill/starlab/actions/runs/24064229874) (**success**)
- §10 updated: **environment drift / smoke matrix** (narrow) **proved on `main`** — deterministic `runtime_smoke_matrix.json` + `environment_drift_report.json` from M01 probe surface + optional M03 `environment_fingerprint` hint; **cross-host portability**, **replay parser substrate**, **replay semantic extraction**, **replay provenance finalization**, **benchmark integrity**, **new live SC2 execution in CI** — **not** proved
- M07 stubs seeded: `docs/company_secrets/milestones/M07/M07_plan.md`, `M07_toolcalls.md` — **no** M07 implementation
- Milestone artifacts: `M06_run1.md`, `M06_summary.md`, `M06_audit.md`; contract `docs/runtime/environment_drift_smoke_matrix.md`; modules `starlab/sc2/runtime_smoke_matrix.py`, `environment_drift.py`, `evaluate_environment_drift.py`
- M06 post-closeout documentation push on `main` (`1f5bbc2…`): CI [`24064323510`](https://github.com/m-cahill/starlab/actions/runs/24064323510) (**success**) — **not** a merge-boundary event; ledger / M07 stubs / governance tests

### 2026-04-07 — M05 merged to `main` (PR #6) + closeout

- Merged [PR #6](https://github.com/m-cahill/starlab/pull/6) to `main` at **2026-04-07T03:20:10Z**; merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0` (merge method: **merge commit**); remote branch `m05-canonical-run-artifact-v0` **deleted**
- Final PR head `53ace08e2ec9d29c780f31593bd945e82e1dfcac` — authoritative PR-head CI: [`24062592376`](https://github.com/m-cahill/starlab/actions/runs/24062592376) (**success**)
- Post-merge `main` CI on merge commit: [`24062610358`](https://github.com/m-cahill/starlab/actions/runs/24062610358) (**success**)
- M05 closeout documentation push on `main` (`6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`): CI [`24062664914`](https://github.com/m-cahill/starlab/actions/runs/24062664914) (**success**) — **not** a merge-boundary event; ledger / milestone artifacts / M06 stubs
- M05 §18/§23 post-closeout CI evidence cross-reference (`ebca1e964c0539c78165bfab72c249a2157402cc`): CI [`24062700534`](https://github.com/m-cahill/starlab/actions/runs/24062700534) (**success**) — **not** a merge-boundary event
- §10 updated: **canonical run artifact v0** (narrow) **proved on `main`** — deterministic M03/M04 JSON bundle + `run_artifact_id`; **raw replay bytes and raw proof/config files are not included** in the bundle; **replay parser substrate**, **replay semantic equivalence**, **benchmark validity**, **cross-host reproducibility**, **new live SC2 execution in CI** — **not** proved
- M06 stubs seeded: `docs/company_secrets/milestones/M06/M06_plan.md`, `M06_toolcalls.md` — **no** M06 implementation
- Milestone artifacts: `M05_run1.md`, `M05_summary.md`, `M05_audit.md`; `docs/runtime/run_identity_lineage_seed.md` — note on `seed_from_proof` path/JSON digest portability

### 2026-04-06 — M05 canonical run artifact v0 (pre-merge branch work; superseded by PR #6 merge)

- Development on `m05-canonical-run-artifact-v0`; landed via **PR #6** — see entry above for authoritative merge + CI

### 2026-04-07 — M04 merged to `main` (PR #5) + closeout

- Merged [PR #5](https://github.com/m-cahill/starlab/pull/5) to `main` at **2026-04-07T02:17:04Z**; merge commit `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` (merge method: **merge commit**); remote branch `m04-replay-binding-to-run-identity` **deleted**
- Final PR head `6991978cb35172edda75f721149b1558d7ead226` — authoritative PR-head CI: [`24060734950`](https://github.com/m-cahill/starlab/actions/runs/24060734950) (**success**)
- Post-merge `main` CI on merge commit: [`24060997255`](https://github.com/m-cahill/starlab/actions/runs/24060997255) (**success**)
- §10 updated: **replay binding** (opaque replay bytes → `replay_binding.json` linked to M03 IDs) **proved on `main` (narrow)**; **canonical run artifact v0**, **replay parser substrate**, **benchmark validity**, **replay semantic equivalence**, **new live SC2 execution in CI** — **not** proved
- M05 stubs seeded: `docs/company_secrets/milestones/M05/M05_plan.md`, `M05_toolcalls.md` — **no** M05 implementation
- M04 closeout documentation push on `main` (`c099752…`): CI [`24061285459`](https://github.com/m-cahill/starlab/actions/runs/24061285459) (**success**) — **not** a merge-boundary event; ledger / milestone artifacts update

### 2026-04-07 — M03 merged to `main` (PR #4) + closeout

- Merged [PR #4](https://github.com/m-cahill/starlab/pull/4) to `main` at **2026-04-07T01:10:32Z**; merge commit `6bfe6a7b32a004f62a491bf31573e12cd211118a` (merge method: **merge commit**); remote branch `m03-run-identity-lineage-seed` **deleted**
- Final PR head `884055c34b78f182c704df5a10a9eced5515fa78` — authoritative PR-head CI: [`24059095399`](https://github.com/m-cahill/starlab/actions/runs/24059095399) (**success**)
- Post-merge `main` CI on merge commit: [`24059246337`](https://github.com/m-cahill/starlab/actions/runs/24059246337) (**success**)
- §10 updated: **run identity + lineage seed** (narrow) **proved on `main`** from proof/config inputs; **replay binding**, **canonical run artifact v0**, **benchmark validity** — **not** proved
- M04 stubs seeded: `docs/company_secrets/milestones/M04/M04_plan.md`, `M04_toolcalls.md` — **no** M04 implementation
- M03 closeout documentation push on `main` (`43d99f6…`): CI [`24059294330`](https://github.com/m-cahill/starlab/actions/runs/24059294330) (**success**)

### 2026-04-06 — M02 merged to `main` (PR #3) + closeout

- Merged [PR #3](https://github.com/m-cahill/starlab/pull/3) to `main` at **2026-04-06T23:35:21Z**; merge commit `53a24a4a6106168afe79e0a70d51a20bfef4ea18` (merge method: **merge commit**); remote branch `m02-deterministic-match-execution-harness` **deleted**
- Final PR head `e88ca20424410cd99f834eeec92a5ec5d8034284` — authoritative PR-head CI: [`24055678613`](https://github.com/m-cahill/starlab/actions/runs/24055678613) (**success**)
- Post-merge `main` CI on merge commit: [`24056523452`](https://github.com/m-cahill/starlab/actions/runs/24056523452) (**success**)
- Closeout doc push on `main` (`d81a095…`): CI [`24056595358`](https://github.com/m-cahill/starlab/actions/runs/24056595358) (**success**)
- Local evidence (narrow same-machine harness): two `burnysc2` runs, matching normalized `artifact_hash` — `docs/company_secrets/milestones/M02/`
- §10 updated: **controlled deterministic match execution** proved **only** in that narrow sense; replay binding, canonical run artifact v0, benchmark validity, cross-host reproducibility — **not** proved
- M03 stubs seeded: `docs/company_secrets/milestones/M03/M03_plan.md`, `M03_toolcalls.md` — **no** M03 implementation

### 2026-04-06 — M02 local evidence recovery (map path + two successful burny runs)

- **Recovery session:** placed a real `.SC2Map` file (pysc2 mini-game `MoveToBeacon`; see `M02_local_execution_note.md`) under gitignored `_local_maps/`; fixed explicit map path resolution to **absolute** paths in `starlab.sc2.maps` so python-sc2 does not mis-resolve repo-relative paths under install `Maps/`.
- **Result:** two `python -m starlab.sc2.run_match … --redact` runs with the same committed config — **exit 0**; **matching** `artifact_hash` recorded in `M02_determinism_check.md`; redacted proof JSON committed as `M02_execution_proof_redacted.json`.
- **Not merged** to `main` in this update; PR **#3** remains the merge vehicle when review completes.

### 2026-04-06 — M02 harness: PR #3 opened (pre-merge; not closed on `main`)

- Opened [PR #3](https://github.com/m-cahill/starlab/pull/3) (**M02: deterministic match execution harness**) from `m02-deterministic-match-execution-harness`; current PR head `290304a3ad3986029879c183f4e40159e7f5792c` (supersede with current branch tip after pushes; early local evidence in commit `5ec0ccb…` was **blocked** — see milestone files)
- **Authoritative PR-head CI** for that tip: workflow **CI** run [`24054732181`](https://github.com/m-cahill/starlab/actions/runs/24054732181) — **success** (earlier green runs on older tips: `24054586191` on `c03691b…`; `24054529734` on `5ec0ccb…`; `24053526611` on `061c212…`; `24053475644` on `bfab038…`; `24053430560` on `3952c40…`; `24053381609` on `08fb582…`; `24053317502` on `10a2b13…`; `24053264747` on `22b2b57…`; `24053218335` on `d80ae12…`; `24052325999` on `f457cf5…`; `24052291273` on `79b341a…`; `24052230417` on `5f5c8a5…`; `24052172714` on `59dcf15…`; `24052112581` on `1bd98f1…`; `24052043305` on `8884078…`)
- **Not merged** to `main` at this changelog entry; **local real-execution / determinism evidence** for M02 remains **pending** (CI is SC2-free by design)
- Milestone artifacts: `M02_run1.md`, `M02_summary.md`, `M02_audit.md` under `docs/company_secrets/milestones/M02/`

### 2026-04-06 — M01 merged to `main` (PR #2)

- Merged [PR #2](https://github.com/m-cahill/starlab/pull/2) to `main` at **2026-04-06T20:26:27Z**; merge commit `4a916033f55c6b8c4a582f985233a64ca039ead3` (merge method: **merge commit**); remote branch `m01-sc2-runtime-surface-env-lock` **deleted**
- Post-merge `main` CI: workflow run `24049637412` (success) on merge commit `4a91603…`: https://github.com/m-cahill/starlab/actions/runs/24049637412
- Follow-up `main` push for merge closeout documentation (`c920876…`): workflow run `24049868109` (success): https://github.com/m-cahill/starlab/actions/runs/24049868109
- Follow-up `main` push aligning §18 second post-merge row and `M01_run1.md` (`aa46fc4…`): workflow run `24049956985` (success): https://github.com/m-cahill/starlab/actions/runs/24049956985
- Follow-up `main` push recording the third post-merge row + `M01_run1` run 3 (`8251cef…`): workflow run `24049998835` (success): https://github.com/m-cahill/starlab/actions/runs/24049998835
- §18 ledger and this changelog updated with merge/post-merge evidence

### 2026-04-06 — M01 closeout (SC2 runtime surface & environment lock)

- Resolved **OD-005**: canonical control/observation boundary = Blizzard SC2 API / `s2client-proto`; canonical replay decode boundary = `s2protocol`; optional `python-sc2` only behind adapter boundaries; PySC2 deferred for substrate — see `docs/runtime/sc2_runtime_surface.md`
- Added `docs/runtime/environment_lock.md` and deterministic `starlab.sc2` path/config probe (`run_probe`, `probe_result_to_json`); **no** SC2 Python packages added in M01
- Updated `docs/rights_register.md`, `docs/replay_data_provenance.md`, 33-milestone ledger map, phase names, and canonical corpus promotion rule
- **Does not claim:** controlled match execution, replay parsing correctness, or benchmark validity (M02+)
- Witnessed PR-head CI runs before merge: `24048416111` (`378c864…`), `24048498203` (`260c4e0…`), `24048576545` (`88b06db…`) — all success

### 2026-04-06 — M00 evidence finalization (PR #1 merged)

- Merged [PR #1](https://github.com/m-cahill/starlab/pull/1); merge commit `f9203dd555ea267bc2d72c3470b174ca35a23788`; PR head `5dcb6cf6f95af23b58c6af202d58a7bcad1d0b91`
- Authoritative CI: PR-head run `24015581129` (success); post-merge `main` run `24015599413` (success); post–evidence-finalization `main` run `24015634285` (success) on `523993edb22938e13bdbf308bb511c204ddd71a6`
- Completed `M00_summary.md`, `M00_audit.md`, `M00_run1.md` under `docs/company_secrets/milestones/M00/`
- Updated §18 closeout ledger and score trend with concrete evidence

### 2026-04-05 — M00 closeout (Governance bootstrap)

- Hardened ledger: untrusted SC2 boundary, change control, proved/not-proved, assumed/owned, deployment posture (Netlify / Render preparatory), “deployment readiness is not deployment”
- Resolved OD-002, OD-004, OD-006; conditionally resolved OD-003 (interim replay policy)
- Added `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/*`, `CONTRIBUTING.md`, `SECURITY.md`
- Seeded `frontend/`, `backend/`, `ops/` placeholders; non-operative Netlify/Render examples
- Python 3.11 dev tooling + GitHub Actions CI (Ruff, format, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks)
- Milestone artifacts under `docs/company_secrets/milestones/M00/`; M01 stubs seeded
- `.gitignore` narrowed so `docs/company_secrets/milestones/` is trackable; other company_secrets subfolders remain ignored

### 2026-04-05 — Documentation and license alignment

- Aligned ledger with `LICENSE` (source-available, evaluation-only)
- Resolved OD-001; updated rights tracker
- Removed citation artifacts; named `docs/bicetb.md` in authority hierarchy and README alignment

### 2026-04-05 — Initial ledger seed

- Created canonical project ledger
- Established authority hierarchy
- Added phase map and planned milestone table
- Added open decisions and risk tracker
- Added milestone closeout rules
- Added acquisition-aware but concise posture
- Set ledger up for Cursor-based incremental milestone updates
