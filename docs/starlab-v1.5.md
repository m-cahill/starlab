# STARLAB v1.5 — Authoritative Public Governance (V15)

**Program phase:** v1.5 (milestone namespace **V15**)  
**Status:** Active program line — **V15-M00** is **closed** on `main` ([PR #116](https://github.com/m-cahill/starlab/pull/116); merge `1391518eb4a4a7e90b5b1b81074d070e2957c8a3`). **Authoritative PR-head CI** [`24911939851`](https://github.com/m-cahill/starlab/actions/runs/24911939851) (head `aeabdb9274aea43e660dedf4d2090db0b6e24237`); **merge-boundary `main` CI** [`24913025515`](https://github.com/m-cahill/starlab/actions/runs/24913025515) on merge commit `1391518e…` — **success**. M00 **does not** claim a completed long GPU run, strong agent, human benchmark, or XAI demo. **V15-M01** is **closed** on `main` ([PR #117](https://github.com/m-cahill/starlab/pull/117); merge `f618a1f90d44e02879501ea067a079c760c20e6c`). **Authoritative PR-head CI** [`24914804421`](https://github.com/m-cahill/starlab/actions/runs/24914804421) (head `8d4caf6cbc5c03e8e42e4aea62de6210b0947ae8`); **merge-boundary `main` CI** [`24916076997`](https://github.com/m-cahill/starlab/actions/runs/24916076997) on merge commit `f618a1f…` — **success**. M01 **does not** execute training or approve claim-critical assets; **M01 non-claims** below remain in force after closure. **V15-M02** is **closed** on `main` ([PR #118](https://github.com/m-cahill/starlab/pull/118); merge `3f7e226ff0402cbb91b831e7c9397080cc8a77aa` merged **2026-04-25T00:53:35Z** UTC). **Authoritative PR-head CI** [`24918006750`](https://github.com/m-cahill/starlab/actions/runs/24918006750) (head `4aab910eb01f50f03e866630c34a3c91d772ad13`); **merge-boundary `main` CI** [`24918563270`](https://github.com/m-cahill/starlab/actions/runs/24918563270) on merge commit `3f7e226f…` — **success**. M02 **does not** execute GPU training, **does not** run GPU shakedown, and **does not** green-light a long run or operator-local RTX 5090 readiness from fixture-only output — **M02 non-claims** below apply after closure. **V15-M03** is **closed** on `main` ([PR #120](https://github.com/m-cahill/starlab/pull/120); merge `47a3fcb0a58ad6280dadc8967297774ed94ab4ad` merged **2026-04-25T02:08:19Z** UTC). **Authoritative PR-head CI** [`24919300604`](https://github.com/m-cahill/starlab/actions/runs/24919300604) (head `68ff0556b43775b5cb78adebd357bfc918eabbfb`); **merge-boundary `main` CI** [`24920070670`](https://github.com/m-cahill/starlab/actions/runs/24920070670) on merge commit `47a3fcb0…` — **success**. M03 **does not** read or hash on-disk weight blobs, does **not** verify checkpoint bytes by default, does **not** execute trainer resume or rollback, does **not** promote a strong checkpoint, and does **not** authorize a long GPU run — **M03 non-claims** below apply after closure; see `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md` (M03 is **lineage / resume *discipline* metadata** only — **not** GPU training, **not** checkpoint-blob I/O, **not** `long_gpu_run_authorized` **true**). **V15-M04** — *XAI Evidence Contract v1* — is **closed** on `main` ([PR #123](https://github.com/m-cahill/starlab/pull/123); merge `3bf4e2ca5343b116e4e979d5dc50213596b7519b` merged **2026-04-25T04:11:30Z** UTC). **Authoritative PR-head CI** [`24922143448`](https://github.com/m-cahill/starlab/actions/runs/24922143448) (head `4c4c1344bf004db543298458a46e61b31815c201`); **merge-boundary `main` CI** [`24922278255`](https://github.com/m-cahill/starlab/actions/runs/24922278255) on merge commit `3bf4e2ca…` — **success**. **V15-M00–M04** remain **closed** on `main` as above. **V15-M05** — *Strong-Agent Benchmark Protocol* — is **closed** on `main` ([PR #125](https://github.com/m-cahill/starlab/pull/125); merge `d7daee6e43613daf85e544ac5a25179cb5697c76` merged **2026-04-25T05:18:15Z** UTC). **Authoritative PR-head CI** [`24923242320`](https://github.com/m-cahill/starlab/actions/runs/24923242320) (head `703a874e7ff43a5aa4f92c97516e86e0d17bc89d`); **merge-boundary `main` CI** [`24923432833`](https://github.com/m-cahill/starlab/actions/runs/24923432833) on merge commit `d7daee6e…` — **success**. M05 **defines** the strong-agent **protocol and scorecard contract** (with **fixture** CI) — **not** benchmark **execution**; **not** strong-agent **claim** authorization. **V15-M06** — *Human Panel Benchmark Protocol* — is **closed** on `main` ([PR #127](https://github.com/m-cahill/starlab/pull/127); merge `994f24e605e32c0738f34eb4d09be2020d543c3c` merged **2026-04-25T06:11:16Z** UTC). **Authoritative PR-head CI** [`24924293130`](https://github.com/m-cahill/starlab/actions/runs/24924293130) (head `c6b2c7ddb81859b1171ace983befdf9782ef81c3`); **merge-boundary `main` CI** [`24924371412`](https://github.com/m-cahill/starlab/actions/runs/24924371412) on merge commit `994f24e6…` — **success**. M06 **defines** the human-panel **protocol and fixture contract** (with **optional** **operator_declared** validation) — **not** human-panel **execution**; **not** “beats most humans” **claim** authorization. M04 **does not** execute XAI inference, **does not** prove explanation faithfulness, and **does not** authorize a long GPU run — **M04 non-claims** below apply after closure. **M05** **does not** run benchmark matches, **does not** run live SC2, **does not** evaluate a checkpoint, **does not** select or promote a strong agent, **does not** run XAI review or human-panel evaluation, and **does not** authorize a long GPU run — **M05 non-claims** below apply. **V15-M07** — *Training Smoke and Short GPU Shakedown* — is **closed** on `main` (implementation [PR #129](https://github.com/m-cahill/starlab/pull/129); merge `b7e4dc7c891687aea0e92ef622ab48f007bdbefe` merged **2026-04-25T07:40:26Z** UTC). **Authoritative PR-head CI** [`24925848388`](https://github.com/m-cahill/starlab/actions/runs/24925848388) (head `c05f3e1429674f24d8a4efd06e358490e5060ad1`); **merge-boundary `main` CI** [`24925929052`](https://github.com/m-cahill/starlab/actions/runs/24925929052) on merge commit `b7e4dc7c…` — **success**. M07 **defines** the training-run **receipt** and optional bounded shakedown **tooling** — **not** the **V15-M08** long campaign; **`long_gpu_run_authorized` remains false**; public program record: **operator-local shakedown** — **not run** on the closeout environment (**CUDA unavailable**; honest **`operator_local_short_gpu_not_run`**). **V15-M08** — *Long GPU Campaign Execution* — **closed** on `main` as **implementation / preflight / guard tooling only** (implementation [PR #133](https://github.com/m-cahill/starlab/pull/133); merge `33b277383d3383ada607039b7a7586859a5925a8` merged **2026-04-25T20:35:52Z** UTC). **Authoritative PR-head CI** [`24940027890`](https://github.com/m-cahill/starlab/actions/runs/24940027890) (head `b414013129062940a78af009fba0bd8db71c0beb`); **merge-boundary `main` CI** [`24940102671`](https://github.com/m-cahill/starlab/actions/runs/24940102671) on merge commit `33b27738…` — **success**. **Public closeout status:** **`implementation_ready_waiting_for_operator_run`** — **no** operator-local long GPU campaign **completed**; **`long_gpu_run_authorized` remains false** on fixture/default paths; a real run remains **blocked** until valid preflight inputs (including M07 GPU shakedown receipt or recorded governance override) and explicit operator authorization. Operator execution requires **dual** CLI guards and honest gate **A–G** results. **V15-M09** — *Checkpoint Evaluation and Promotion* — **closed** on `main` (implementation [PR #135](https://github.com/m-cahill/starlab/pull/135); merge `eaa928d2177ca3f18caece3c2dac82b474203d08` **2026-04-25T23:12:19Z** UTC). **Authoritative PR-head CI** [`24942859847`](https://github.com/m-cahill/starlab/actions/runs/24942859847) (head `b503ec3a98aa003299ef1efc25c30cb89453c466`); **merge-boundary `main` CI** [`24942925570`](https://github.com/m-cahill/starlab/actions/runs/24942925570) on merge commit `eaa928d2…` — **success**. Checkpoint evaluation + promotion-decision emitters; **`docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`**. **M09 public closeout:** **`blocked_missing_m08_campaign_receipt`** — **no** checkpoint **promoted**; **no** public register **rows**; default fixture / honest path keeps claim flags **false**. **V15-M10** — *Replay-Native XAI Demonstration* — **closed** on `main` (implementation [PR #136](https://github.com/m-cahill/starlab/pull/136); merge `a7e9b6e9af7c1cc084d4b73d2a64a2a05ac3cf1f` **2026-04-26T00:10:50Z** UTC). **Authoritative PR-head CI** [`24943450910`](https://github.com/m-cahill/starlab/actions/runs/24943450910) (head `142e13a8d6933f376818498d1a390cf3ba242101`); **merge-boundary `main` CI** [`24943955088`](https://github.com/m-cahill/starlab/actions/runs/24943955088) on merge commit `a7e9b6e9…` — **success**. Contract `starlab.v15.replay_native_xai_demonstration.v1`; **`docs/runtime/v15_replay_native_xai_demonstration_v1.md`**; `python -m starlab.v15.emit_v15_replay_native_xai_demonstration`. **M10 public closeout:** default **`fixture_contract_only`** / **`blocked_missing_promoted_checkpoint`**; **real XAI inference executed:** **no**; **faithfulness validated:** **no**; **checkpoint promoted for XAI:** **no** on the default path; **strong-agent / ladder / human-benchmark / v2 claim flags:** **false** in the honest public record; **claim-critical public register rows:** **no**; **raw** media, saliency tensors, replays, weights, or checkpoint blobs: **not** committed. **V15-M11** — *Human Panel / Bounded Human Benchmark* — **closed** on `main` (implementation [PR #137](https://github.com/m-cahill/starlab/pull/137); merge `468d90fc0094bbe9f8bbffc4bc69ebbb1d333a3b`). **Authoritative PR-head CI** [`24945588527`](https://github.com/m-cahill/starlab/actions/runs/24945588527) (head `91cced54a54e72f51cdfe5a0ab82beeab5aa1ea6`); **merge-boundary `main` CI** [`24945647654`](https://github.com/m-cahill/starlab/actions/runs/24945647654) on merge commit `468d90fc…` — **success**. **M11 public closeout:** default **`fixture_contract_only`** / **`blocked_missing_promoted_checkpoint`** / **`blocked_missing_human_panel_execution`**; **human panel execution performed:** **no** on default path; **human benchmark claim authorized:** **no**; **strong-agent claim authorized:** **no**; **checkpoint promoted for human panel:** **no** on default path; **participant identities committed:** **no**; **claim-critical public human benchmark register rows:** **no**; **raw replays / videos / private participant materials committed:** **no**. Contracts **`starlab.v15.human_panel_execution.v1`** / **`starlab.v15.human_benchmark_claim_decision.v1`**; **`docs/runtime/v15_human_panel_bounded_benchmark_v1.md`**; emitters `emit_v15_human_panel_execution`, `emit_v15_human_benchmark_claim_decision`; **M11 non-claims** below remain in force. **V15-M12** — *Showcase Agent Release Pack* — **not started**.

**Strategic moonshot anchor:** `docs/starlab-v1.5moonshot.md`  
**Historical ledgers:** v1 / PV1 / PX1 / PX2 narrative remains in `docs/starlab.md` (concise pointer only—no duplication of this file’s full governance here).

---

## 1. Purpose and scope

**v1.5** bridges governed substrate work (closed **v1** arc **M00–M61**, post-v1 phases **PV1**, **PX1**, **PX2**) and a potential **v2** recharter. It exists to run a **serious long local GPU training campaign** with **merge-grade or operator-approved provenance**, and to produce a **bounded, replay-native, explainable** Terran-first 1v1 agent—**without** overclaiming ladder universality, global benchmark superiority, or v2 readiness.

**In scope for the v1.5 program (not necessarily for every milestone):**

- Long GPU training with manifests, checkpoint lineage, eval cadence, and receipts.
- Strong-agent evaluation under **predeclared** benchmark ladders.
- Replay-native **XAI** evidence packs on frozen contracts.
- Optional **human-panel** or bounded “beats most humans” claims **only** under frozen protocol and recorded non-claims.

**Out of scope for governance documents:** executing training in CI by default; claiming results that operators have not produced under declared protocols.

---

## 2. Relationship to prior phases

| Phase | Role relative to v1.5 |
| --- | --- |
| **v1 (M00–M61)** | Delivered governed replay-native SC2 substrate, deterministic artifact families, bounded training/eval surfaces. Remains the technical foundation. |
| **PV1** | Long industrial campaign discipline and operator-local scaling evidence—not autonomous full-game strength as v1.5’s sole gate. |
| **PX1** | Full industrial run + demo proof packaging—separate from autonomous skill development. |
| **PX2 (M00–M03)** | **Closed / transition-complete.** Delivered bounded self-play and operator-local surfaces; **did not** ship a long wall-clock GPU training session as a program deliverable. |

---

## 3. Moonshot goals (five pillars)

Success of the **overall** v1.5 program requires evidence for all five (see moonshot doc for detail). **V15-M00** only **defines** these—it does not satisfy them.

1. **Full GPU training run completed** — manifests, lineage, logs, receipts (not a smoke or fixture-only story).
2. **Strong-agent benchmark passed** — predeclared ladder (fixture → scripted → heuristic → prior checkpoints → live → human panel as applicable).
3. **Replay-native XAI demonstration** — frozen artifact shapes; wins, losses, macro/tactical/scout/counterfactual coverage.
4. **Human-benchmark claim bounded** — “beats most humans” only under declared STARLAB benchmark rules and non-claims.
5. **v2 go/no-go decision evidence-based** — proceed, harden, extend training, or recharter based on artifacts.

---

## 4. Standing non-claims (v1.5)

Unless separately proved and scoped:

- Not a global StarCraft II solution; not ladder dominance; not multi-race generality.
- Not guaranteed benchmark universality or replay↔execution equivalence.
- Not v2 by default; not **PX2-M04** auto-opened.
- XAI artifacts are **governed explanation packs**, not proofs of causal human-like reasoning.

**M00 non-claims:** No long GPU run completed in M00; no strong-agent, human-panel, or XAI completion claimed.

**M01 non-claims (persist after M01 closure):** No long GPU run; no **M01** environment lock surface (delivered in **M02**); no checkpoint lineage **runtime**; no XAI contract freeze or XAI execution; no benchmark execution; no human-panel execution; no v2; no **PX2-M04** / **PX2-M05**; no claim-critical asset rows in public registers (templates only). Milestone closure records merge/CI evidence only — **not** asset approval for claim-critical use.

**M02 non-claims (after M02 closure on `main` until superseded by later milestones):** V15-M02 defines and emits the long GPU run **environment-lock surface** and may normalize **supplied** operator probe JSON **or** run the **fixture** profile in CI. **Fixture `fixture_ci` output does not imply operator-local readiness** (including RTX 5090–class). It does **not** execute GPU training; does **not** run GPU shakedown (**V15-M07**); does **not** grant **long_run** or program long-GPU **authorization**; does **not** alone satisfy Gate B for a program-valid long run; does **not** claim operator-local hardware readiness from CI fixture output; does **not** run SC2, `nvidia-smi`, or map introspection in CI; does **not** implement checkpoint lineage **runtime**; does **not** freeze XAI; does **not** run benchmarks, human panel, or XAI execution; does **not** approve claim-critical real assets; does **not** open v2 or **PX2-M04** / **PX2-M05**. The field `long_gpu_run_authorized` in the M02 contract remains **false** — M02 does not grant program authorization.

**M03 non-claims (after M03 closure on `main` until superseded by later milestones as applicable):** V15-M03 defines and emits the **checkpoint lineage and resume-discipline** manifest (`starlab.v15.checkpoint_lineage_manifest.v1`). It is **metadata and governance only**: it may normalize operator-declared **lineage JSON** and may bind an **M02** environment lock file by **canonical JSON SHA-256**; it does **not** read or hash on-disk **checkpoint weight blobs**; does **not** verify checkpoint bytes by default; does **not** execute **trainer** resume or rollback; does **not** set `resume_execution_verified` / `rollback_execution_verified` to true at the program-manifest root (M03 does not prove execution); does **not** run GPU training or shakedown; does **not** authorize a long GPU run (`long_gpu_run_authorized` remains **false**); does **not** promote a “strong” checkpoint; does **not** approve real assets for claim-critical public registers; does **not** open v2 or **PX2-M04** / **PX2-M05**. A lineage manifest is **not** proof that checkpoint bytes exist unless `hash_verification_status` and external scope say so. A **resume receipt** is **not** proof that training resumed unless an external path says so, and M03 does not independently verify that path.

**M04 non-claims (after M04 closure on `main` until superseded by later milestones as applicable):** V15-M04 defines and emits the **XAI evidence contract** (`starlab.v15.xai_evidence_pack.v1`) and **fixture** `v15_xai_evidence_pack.json` + report. It is **metadata and schema only**: it may validate operator-declared **evidence JSON** and redact path-like strings; it does **not** run model **inference**; does **not** generate real saliency, attribution, or concept activations; does **not** execute counterfactual **evaluation**; does **not** parse real **replays**; does **not** read checkpoint **blobs**; does **not** verify checkpoint **bytes** as an execution path; does **not** **prove** explanation **faithfulness**; does **not** run **benchmarks** or **human** evaluation; does **not** execute GPU **training** or **shakedown**; does **not** set `long_gpu_run_authorized` to **true**; does **not** approve real XAI assets for claim-critical public **registers**; does **not** open **v2** or **PX2-M04** / **PX2-M05**. A fixture pack is **not** an explanation of a trained agent. Public **`docs/xai_evidence_register.md`** gets **no** new real XAI **rows** in M04 (contract definition only).

**M05 non-claims (during and after M05; supersede only where a later milestone explicitly changes posture):** V15-M05 defines and emits the **strong-agent benchmark protocol and scorecard contract** (`starlab.v15.strong_agent_scorecard.v1` with `protocol_profile_id` `starlab.v15.strong_agent_benchmark_protocol.v1`) and **fixture** `v15_strong_agent_scorecard.json` + report. It is **metadata and protocol vocabulary only** (ladder, scorecard field definitions, gate shapes, evidence classes, reserved human-panel and XAI-review milestones): it may validate **fixture** protocol metadata and may normalize **operator-declared** protocol JSON (with absolute-path **redaction**); it does **not** run **benchmarks** or tournaments; does **not** run **live SC2**; does **not** **evaluate** a **checkpoint**; does **not** **select** or **promote** a “strong” agent; does **not** run **XAI review** or **human-panel** execution; does **not** add **real** match or scorecard **results**; does **not** execute GPU **training** or **shakedown**; does **not** set `long_gpu_run_authorized` / `strong_agent_claim_authorized` / `benchmark_execution_performed` to **true**; does **not** approve real assets for **claim-critical** public **registers**; does **not** open **v2** or **PX2-M04** / **PX2-M05**. A **strong-agent scorecard contract** is **not** evidence that a strong-agent benchmark has **passed**. A **fixture** benchmark protocol is **schema / wiring** evidence only, **not** a performance result.

**M06 non-claims (during and after M06; supersede only where a later milestone explicitly changes posture):** V15-M06 defines and emits the human-panel benchmark protocol contract (`starlab.v15.human_panel_benchmark.v1` with `protocol_profile_id` `starlab.v15.human_panel_benchmark_protocol.v1`) and **fixture** `v15_human_panel_benchmark.json` + `v15_human_panel_benchmark_report.json`. It is **protocol and governance metadata only**: it does **not** recruit or evaluate human participants; does **not** run human-panel **matches**; does **not** run live **SC2**; does **not** evaluate or **promote** a **checkpoint**; does **not** add real participant **identities** or **results**; does **not** authorize a “beats most humans” **claim**; does **not** run GPU **training** or **shakedown**; does **not** perform **XAI** **review**; does **not** set `human_benchmark_claim_authorized`, `strong_agent_claim_authorized`, `benchmark_execution_performed`, `human_panel_execution_performed`, or `long_gpu_run_authorized` to **true**; does **not** approve real assets for **claim-critical** public **registers**; does **not** open **v2** or **PX2-M04** / **PX2-M05**. A **human-panel benchmark protocol** is **not** evidence that a human benchmark has been **run** or **passed**. **Public** `docs/human_benchmark_register.md` receives **no** new real participant **rows** in M06 (one-line M06 **note** only; **no rows** in the public register table). 

**M07 non-claims (during and after M07; supersede only where a later milestone explicitly changes posture):** V15-M07 defines and emits the training smoke / short GPU shakedown receipt contract (`starlab.v15.training_run_receipt.v1` with profile `starlab.v15.training_smoke_short_gpu_shakedown.v1`) and may run a bounded **operator-local** GPU or CPU shakedown only when **explicitly** invoked with `--allow-operator-local-execution`. It does **not** execute the **V15-M08** long GPU campaign; does **not** authorize a long run; does **not** promote a checkpoint; does **not** run a strong-agent benchmark; does **not** run human-panel matches; does **not** perform XAI review; does **not** authorize human-benchmark or strong-agent claims; does **not** approve real public register rows for claim-critical use; does **not** commit model weights or checkpoint blobs; and does **not** open v2 or PX2-M04/PX2-M05. A short GPU shakedown receipt is **not** evidence that the long GPU campaign has completed or that a strong agent exists. **M07** may close as **shakedown tooling and receipt contract implemented** if no operator-local GPU is available; **M07** must **not** be described as “operator-local GPU shakedown **completed**” unless a real private receipt exists.

**M08 non-claims block:** V15-M08 defines and, when explicitly authorized, executes the long GPU campaign under `starlab.v15.long_gpu_training_manifest.v1` and related training-run receipt surfaces. M08 may record that a long GPU run was authorized, executed, and completed within a declared operator-local scope only if the preflight gates pass and a real campaign receipt exists. M08 does not by itself promote a checkpoint; does not pass or execute the strong-agent benchmark; does not run human-panel matches; does not perform XAI review; does not authorize human-benchmark or strong-agent claims; does not approve v2; does not prove ladder dominance, global SC2 solution, multi-race generality, benchmark universality, or replay↔execution equivalence; does not commit raw checkpoints, model weights, replays, logs, or private operator paths; and does not open PX2-M04/PX2-M05. A completed long GPU campaign is training evidence, not a strong-agent claim.

**M09 non-claims block:** V15-M09 defines and emits checkpoint evaluation and promotion-decision artifacts under `starlab.v15.checkpoint_evaluation.v1` and `starlab.v15.checkpoint_promotion_decision.v1`. **Default and fixture / honest public paths** remain **`blocked_missing_m08_campaign_receipt`** / not promoted; **all** program claim flags stay **false** on those paths. A hypothetical `promoted_candidate_for_downstream_evaluation` label, if ever emitted under explicit non-default evidence, is **governance routing only** — **not** “strong agent,” “release-ready,” or a benchmark pass. M09 does not execute the long GPU campaign; does not train new checkpoints; does not pass or execute the strong-agent benchmark; does not authorize strong-agent or human-benchmark claims; does not run human-panel matches; does not perform XAI review; does not release model weights; does not approve v2; does not prove ladder dominance, global SC2 solution, multi-race generality, benchmark universality, or replay↔execution equivalence; and does not commit raw checkpoints, model weights, replays, logs, or private operator paths. A checkpoint promotion decision record is **governance metadata** for routing labels, not a strong-agent or performance claim.

**M10 non-claims block (closed on `main` — PR #136; non-claims and default blocked/fixture posture remain in force):** V15-M10 defines and emits the replay-native XAI **demonstration and reporting** surface under `starlab.v15.replay_native_xai_demonstration.v1` and binds M04 `starlab.v15.xai_evidence_pack.v1` and M09 `starlab.v15.checkpoint_promotion_decision.v1` JSON by **canonical SHA-256** when operator inputs are supplied. It emits `v15_replay_native_xai_demonstration.json`, a JSON report, and a deterministic **`v15_xai_explanation_report.md`**. M10 does **not** run model **inference**; does **not** parse raw **replays**; does **not** read checkpoint **weight blobs**; does **not** **prove** explanation **faithfulness**; does **not** run human-panel or strong-agent **benchmarks**; does **not** authorize ladder, v2, or human-benchmark **claims** by default; does **not** add **claim-critical** public XAI **rows** in **`docs/xai_evidence_register.md`** on the default path; and does **not** commit **raw** media, saliency tensors, or **private** operator paths. A stronger demonstration label is allowed only with explicit non-default operator evidence; fixture and default CI remain **schema/report validation** only.

**M11 non-claims block (closed on `main` — PR #137; default fixture / honest public paths):** V15-M11 defines the human-panel **execution evidence** and **bounded human-benchmark claim-decision** surfaces under **`starlab.v15.human_panel_execution.v1`** and **`starlab.v15.human_benchmark_claim_decision.v1`**, binding M06 / M09 / M10 JSON by **canonical SHA-256** when operator inputs are supplied (preflight additionally binds M08 / M05 / M03). M11 does **not** recruit human participants; does **not** run human-panel **matches** in CI; does **not** run live **SC2** by default; does **not** **promote** a **checkpoint**; does **not** **train** a **checkpoint**; does **not** prove a **strong-agent** benchmark; does **not** authorize “beats most humans,” ladder, strong-agent, or v2 **claims** on the default path; and does **not** commit participant identities, raw replays, videos, checkpoint blobs, weights, private operator paths, or private human-panel **notes**. The claim-decision artifact is a deterministic read of the execution artifact, not a second upstream binder. **No** **claim-critical** public human-benchmark **register** **rows** on the default path.

---

## 5. V15 milestone table (plan)

| Milestone | Title |
| --- | --- |
| **V15-M00** | Training Readiness Charter and Long GPU Run Gate — **closed** on `main` (PR #116) |
| **V15-M01** | Training-Scale Provenance and Asset Registers — **closed** on `main` (PR #117) |
| **V15-M02** | Long GPU Run Environment Lock — **closed** on `main` (PR #118) |
| **V15-M03** | Checkpoint Lineage and Resume Discipline — **closed** on `main` ([PR #120](https://github.com/m-cahill/starlab/pull/120)) |
| **V15-M04** | XAI Evidence Contract v1 — **closed** on `main` ([PR #123](https://github.com/m-cahill/starlab/pull/123)) |
| **V15-M05** | Strong-Agent Benchmark Protocol — **closed** on `main` ([PR #125](https://github.com/m-cahill/starlab/pull/125)) — contract + `fixture_ci` emitter; **not** benchmark execution |
| **V15-M06** | Human Panel Benchmark Protocol — **closed** on `main` ([PR #127](https://github.com/m-cahill/starlab/pull/127)) — contract + `fixture_ci`; **not** human-panel **execution** |
| **V15-M07** | Training Smoke and Short GPU Shakedown — **closed** on `main` ([PR #129](https://github.com/m-cahill/starlab/pull/129)) — receipt `starlab.v15.training_run_receipt.v1` + `emit_v15_training_run_receipt`; runtime `docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`; **not** V15-M08; **not** `long_gpu_run_authorized` true; operator shakedown: tooling + CI; local GPU not run in this program record |
| **V15-M08** | Long GPU Campaign Execution — **closed** on `main` ([PR #133](https://github.com/m-cahill/starlab/pull/133)) — `emit_v15_long_gpu_training_manifest`, `run_v15_long_gpu_campaign`; `docs/runtime/v15_long_gpu_campaign_execution_v1.md`; **status** **`implementation_ready_waiting_for_operator_run`**; **not** completed long campaign without operator receipts; fixture **`long_gpu_run_authorized` false** |
| **V15-M09** | Checkpoint Evaluation and Promotion — **closed** on `main` ([PR #135](https://github.com/m-cahill/starlab/pull/135)); default posture **blocked** / **not promoted** when M08 campaign receipt absent; **`docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`** |
| **V15-M10** | Replay-Native XAI Demonstration — **closed** on `main` ([PR #136](https://github.com/m-cahill/starlab/pull/136)) — `emit_v15_replay_native_xai_demonstration`; `docs/runtime/v15_replay_native_xai_demonstration_v1.md`; default **fixture** / **blocked**; **not** real inference; **not** claim-critical register rows |
| **V15-M11** | Human Panel / Bounded Human Benchmark — **closed** on `main` ([PR #137](https://github.com/m-cahill/starlab/pull/137)) — execution + claim-decision **surface**; not live panel in CI |
| **V15-M12** | Showcase Agent Release Pack |
| **V15-M13** | v2 Go / No-Go Decision |

### V15 asset and register map (compact)

Navigation aid — authoritative field lists and vocabulary live in `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and emitted `v15_training_asset_registers.json`.

| Surface / register | Public doc | Private / local counterpart (typical) | Strongest allowed claim (until populated & reviewed) | Next dependent milestone |
| --- | --- | --- | --- | --- |
| `starlab.v15.training_readiness_charter.v1` | `docs/runtime/v15_training_readiness_charter_v1.md` | Local charter JSON emit only | `readiness_only` (gates defined, not satisfied) | **V15-M01+** |
| Training asset register | `docs/training_asset_register.md` | Dataset manifests under `out/` or **local** `docs/company_secrets/` (not raw commits; private tree not in default clone) | `readiness_only` | **V15-M02** (environment lock) / later data gates |
| Replay corpus register | `docs/replay_corpus_register.md` | Raw replays local; rights notes private | `readiness_only` | **V15-M02** / gate **C** |
| Model weight register | `docs/model_weight_register.md` | Weight blobs local / external archive | `readiness_only` | **V15-M07**+ training shakedown |
| Checkpoint register | `docs/checkpoint_asset_register.md` | Checkpoint files local / external archive | `readiness_only` | **V15-M03** lineage |
| Human benchmark register | `docs/human_benchmark_register.md` | Human-panel records private by default | `readiness_only` | **M06** protocol **closed**; human **execution** = **M11+** (roadmap) |
| XAI evidence register | `docs/xai_evidence_register.md` | Operator-local packs until contract freeze | `readiness_only` | **V15-M04** contract / **M10** real demo |
| Rights register | `docs/rights_register.md` | Supplemental rights under **local** `docs/company_secrets/` (private; not in default clone) | `readiness_only` | Ongoing |

### V15-M02 — Environment lock status (compact)

Fixture CI proves **wiring and schema**; **operator-local** evidence is required to claim a real **Gate B** environment. Default operator-local status is **`not_evaluated`** until a probe is recorded.

| Environment surface | Required evidence (operator) | CI fixture | Operator-local (default) | Public / private | Next |
| --- | --- | --- | --- | --- | --- |
| Repo identity | git SHA, branch, repo | `fixture` (stable placeholders) | `not_evaluated` | public-safe SHAs; no unsanitized paths | **M03+** |
| Python | version, platform, venv policy | `fixture` | `not_evaluated` | public | ongoing |
| Dependency lock / hash | fingerprint, lockfile refs | `fixture` | `not_evaluated` | public refs; private local paths | ongoing |
| CUDA | version, driver posture | not evaluated in fixture | `not_evaluated` | mostly **private_local_only** in notes | **M07**+ |
| PyTorch | torch build, CUDA build string | not evaluated in fixture | `not_evaluated` | public versions | **M07**+ |
| GPU | name, mem, driver | not evaluated in fixture | `not_evaluated` | private by default (sanitize for public) | **M07**+ |
| SC2 client | version, declared path posture | not evaluated in fixture | `not_evaluated` | **Blizzard TOS**; path **private** | **M07**+ |
| Map pool | pool id, required map list | not evaluated in fixture | `not_evaluated` | logical refs; raw paths **private** | **C** / **M07**+ |
| Disk / output root | policy, min free space | not evaluated in fixture | `not_evaluated` | **private** absolute roots | **M08**+ |
| Operator notes | optional text | N/A in fixture | optional | `private_local_only` by default | ongoing |

`long_gpu_run_authorized` in the M02 contract is **always false**; use **`operator_local_ready`** (with `--probe-json`) for “M02 check list satisfied,” not for program go-ahead.

### V15-M03 — Checkpoint lineage status (compact)

| Checkpoint surface | What M03 defines | Fixture (`fixture_ci`) | Operator-local (typical) | Public / private posture | Next dependent milestone |
| --- | --- | --- | --- | --- | --- |
| **Checkpoint identity** | `checkpoint_id`, roles, URI/ref | `fixture-root`, `fixture-child` (metadata only) | `not_evaluated` until declared | logical refs; paths **redacted** / **private** as needed | M07+ (shakedown) / M08+ |
| **Parent/child lineage** | `parent_checkpoint_id` graph | `fixture` chain | `not_evaluated` / declared in lineage JSON | public-safe if no paths leaked | M08+ |
| **Checkpoint hash reference** | `checkpoint_sha256` + `hash_verification_status` | all-zero placeholder; `fixture` status | `declared_only` / `verified_external` (pass-through) | hash refs public; **blobs** private | M09+ promotion |
| **Model config binding** | `model_config_sha256` per row + ref | placeholder | `not_evaluated` / declared | public refs; private paths | M08+ |
| **Dataset / register binding** | `dataset_manifest_sha256` + manifest refs | placeholder | `not_evaluated` / declared | public refs; private corpora | Gate **C** / M08+ |
| **Environment lock binding** | `environment_lock_sha256` + optional M02 file bind | not bound to a real M02 file | `not_evaluated` / `--environment-lock-json` | public SHA only; no unsanitized paths | M02 evidence + M08+ |
| **Interruption receipt** | `interruption_receipts[]` | fixture-shaped | operator-declared / external attestation (not verified by M03) | sanitize paths | M08+ |
| **Resume receipt** | `resume_receipts[]` | `resume_verification_status` may be `fixture` (not execution) | `declared_only` / `not_executed` default | same | M07+ proves execution |
| **Rollback receipt** | `rollback_receipts[]` | `fixture` (not execution) | `declared_only` / `not_executed` default | same | M09+ |
| **Promotion status** | `promotion_status` + vocabulary | `fixture_only` for fixture rows | candidate / … per gate | public narrative only w/ non-claims | M09+ |

`checkpoint_bytes_verified` is **true** only if **every** checkpoint row has `hash_verification_status == "verified_external"` (operator pass-through; M03 does not read blobs). `resume_execution_verified` and `rollback_execution_verified` are **false** in M03. `long_gpu_run_authorized` is **false**.

### V15-M04 — XAI evidence status (compact)

M04 separates **schema exists** (CI fixture / contract), **real inference executed**, and **faithfulness validated** — future milestones own real XAI execution and validation paths.

| XAI surface | What M04 defines | Fixture schema exists | Real inference executed | Faithfulness validated | Public / private posture | Next dependent milestone |
| --- | --- | --- | --- | --- | --- | --- |
| `xai_manifest` (logical) | Required logical name + pack identity | yes / fixture | false | false | public-safe | **M10** |
| `replay_identity` | Row fields + binding vocabulary | yes / fixture | false | false | logical refs; paths **redacted** / **private** | **M10**+ |
| `checkpoint_identity` | Row fields + hash/binding vocabulary | yes / fixture | false | false | hash refs public; **blobs** private | M03+ bind / **M10**+ |
| `decision_trace` | Trace row schema | yes / fixture | false | false | public-safe in fixture; sanitize operator paths | **M10**+ |
| `critical_decision_index` | Scene types + index rows | yes / fixture | false | false | public narrative with non-claims | **M10**+ |
| `attribution_summary` | Attribution row schema (not maps) | yes / fixture | false | false | public-safe fixture only | **M10**+ |
| `concept_activation_summary` | Concept row schema | yes / fixture | false | false | public-safe fixture only | **M10**+ |
| `counterfactual_probe_results` | Counterfactual row schema | yes / fixture | false | false | public-safe fixture only | **M10**+ |
| `alternative_action_rankings` | Ranking row schema | yes / fixture | false | false | public-safe fixture only | **M10**+ |
| `uncertainty_report` | Uncertainty row schema | yes / fixture | false | false | public-safe fixture only | **M10**+ |
| `replay_overlay_manifest` | Overlay metadata (no render in M04) | yes / fixture | false | false | **private** for raw media paths by default | **M10**+ |
| `xai_explanation_report` | Report metadata (`.md` logical name) | yes / fixture | false | false | public summaries only w/ non-claims | **M10**+ |

`long_gpu_run_authorized` in the M04 contract is **always false**.

### V15-M05 — Strong-agent benchmark status (compact)

M05 separates **protocol defined** (CI fixture + optional operator declaration), **benchmark executed** (real matches / evaluation), and **strong-agent claim authorized** (program-level certification) — the latter two remain **false** in M05.

| Benchmark surface | What M05 defines | Fixture protocol exists | Benchmark executed | Strong-agent claim authorized | Public / private posture | Next dependent milestone |
| --- | --- | --- | --- | --- | --- | --- |
| `evaluation_ladder` | E0–E8 stage ids, names, `stage_status` vocabulary | yes / fixture + vocabulary | false | false | public-safe; no unsanitized paths | **M09+** / eval execution |
| `protocol_profile` | `starlab.v15.strong_agent_benchmark_protocol.v1` | yes / metadata | n/a (not an execution) | false | public | **M09+** |
| `candidate_identity` | Candidate + baseline **subject** row shapes; fixture ids | yes / fixture | false | false | logical refs; paths **redacted** | M03+ bind / **M09+** |
| `checkpoint_binding` | SHA references only (no blob reads in M05) | fixture placeholder | false | false | hash refs public | M03+ / **M08+** |
| `map_pool` | Map pool + rights posture **shape** | yes / fixture | false | false | logical map ids; raw paths private | **M07+** / gate **C** |
| `opponent_pool` | Opponent pool **shape** | yes / fixture | false | false | public-safe ids in fixture | **M09+** |
| `scorecard_fields` | Required metric **names** / field definitions (no results) | yes / all required metrics listed | false | false | public vocabulary | **M09+** |
| `gate_thresholds` | Gate / threshold **definitions** (no pass/fail outcome) | yes / fixture | false | false | public protocol text | **M09+** |
| `evidence_requirements` | Required evidence **kinds** (M02/M03/M04 contracts) | yes / fixture | false | false | public contract refs | M02–M04 bind / **M10** |
| `failure_mode_probes` | Probe **schema** (not executed) | yes / fixture | false | false | public-safe | **M09+** |
| `xai_trace_requirements` | XAI pack trace coverage as **requirement** only | yes / defined | false | false | public | **M10+** (review) |
| `human_panel_reserved` | **Reserved** for **V15-M06+**; `reserved`, `claim_authorized` false | yes / section present | false | false | public narrative; participants private | **M06+** |
| `xai_review_reserved` | **Reserved** for **V15-M10+**; `review_performed` / `faithfulness_validated` false | yes / section present | false | false | public | **M10+** |

`long_gpu_run_authorized`, `benchmark_execution_performed`, and `strong_agent_claim_authorized` in the M05 scorecard contract are **always false** in M05 (fixture or operator-declared **protocol** path).

### V15-M06 — Human panel benchmark status (compact)

M06 separates **protocol defined** (CI fixture + optional operator **declaration**), **human panel executed** (real / operator-local **matches** in a later milestone), and **human benchmark claim authorized** (program-level certification) — the latter two remain **false** in M06.

| Human-panel surface | What M06 defines | Fixture protocol exists | Human panel executed | Human benchmark claim authorized | Public / private posture | Next dependent milestone |
| --- | --- | --- | --- | --- | --- | --- |
| `participant_tiers` | Deterministic `tier_id` vocabulary | yes / fixture | false | false | public-safe; no real roster in fixture | **M11+** |
| `participant_privacy_profile` | Strict `posture_id` enum rows | yes / fixture | false | false | public vocabulary; rosters private | **M11+** |
| `threshold_policy` | Majority / supermajority / tier / freeze **options** | yes / no pass/fail | false | false | public protocol text | **M11+** |
| `evidence_requirements` | Required evidence **kinds** (not filled results) | yes / classes | false | false | public contract refs | M02–M05 bind / **M11** |
| `claim_boundary` | Allowed + disallowed **claim** shapes (text) | yes / fixture | false | false | public | **M11+** |
| `optional_bindings` | SHA-256 of M02 / M03 / M05 / M04 **JSON** only | optional | n/a | false | public SHA; no path leaks in operator path | M02–M05 |

`benchmark_execution_performed`, `human_panel_execution_performed`, `human_benchmark_claim_authorized`, `strong_agent_claim_authorized`, and `long_gpu_run_authorized` in the M06 contract are **false** in M06 (fixture or operator-**declared** **protocol** path).

---

## 6. Artifact family contract ids (governed names)

These are the **intended** v1.5 contract identifiers (emission implemented per milestone; M00 defines names and charter JSON).

- `starlab.v15.training_readiness_charter.v1` (**M00**)
- `starlab.v15.training_asset_registers.v1` (**M01** — register contract / vocabulary only)
- `starlab.v15.long_gpu_environment_lock.v1` (**M02** — environment-lock contract; fixture and optional operator probe)
- `starlab.v15.long_gpu_training_manifest.v1` (**M08** — long campaign manifest + preflight; `starlab.v15.long_gpu_campaign_receipt.v1` for operator-local receipt stub)
- `starlab.v15.checkpoint_lineage_manifest.v1` (**M03** — checkpoint lineage + receipt vocabulary; **implemented** in M03; **not** a training or checkpoint I/O **runtime**)
- `starlab.v15.training_run_receipt.v1` (**M07** — training smoke / shakedown receipt; **not** long campaign)
- `starlab.v15.strong_agent_scorecard.v1` (**M05** — strong-agent scorecard / benchmark **protocol** contract; **not** executed benchmark; embeds **`protocol_profile_id`:** `starlab.v15.strong_agent_benchmark_protocol.v1`)
- `starlab.v15.xai_evidence_pack.v1` (**M04** — XAI pack contract; **implemented** in M04; **not** real XAI inference)
- `starlab.v15.human_panel_benchmark.v1` (**M06** — human-panel **protocol** contract; **closed**; embeds **`protocol_profile_id`:** `starlab.v15.human_panel_benchmark_protocol.v1`)
- `starlab.v15.checkpoint_evaluation.v1` (**M09** — checkpoint **evaluation** contract; **not** verified blob evaluation in fixture CI)
- `starlab.v15.checkpoint_promotion_decision.v1` (**M09** — promotion **decision** contract; **not** strong-agent claim)
- `starlab.v15.replay_native_xai_demonstration.v1` (**M10** — XAI **demonstration/reporting** surface; **binds** M04/M09 JSON by SHA; **not** inference)
- `starlab.v15.human_panel_execution.v1` (**M11** — human-panel **execution** metadata + H0–H12 **gates**; **binds** M06/M09/M10 JSON by SHA; **not** real panel execution in CI)
- `starlab.v15.human_benchmark_claim_decision.v1` (**M11** — **claim decision** over execution JSON; **not** a second upstream binder)
- `starlab.v15.showcase_agent_release_pack.v1`

**M00 emitter:** `python -m starlab.v15.emit_v15_training_readiness_charter --output-dir <path>` writes `v15_training_readiness_charter.json` and `v15_training_readiness_charter_report.json`.

**M01 emitter:** `python -m starlab.v15.emit_v15_training_asset_registers --output-dir <path>` writes `v15_training_asset_registers.json` and `v15_training_asset_registers_report.json`.

**M01 runtime narrative:** `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md`  
**M01 public registers:** `docs/training_asset_register.md`, `docs/replay_corpus_register.md`, `docs/model_weight_register.md`, `docs/checkpoint_asset_register.md`, `docs/human_benchmark_register.md`, `docs/xai_evidence_register.md` (plus `docs/rights_register.md` V15 subsection).

**M02 emitter:** `python -m starlab.v15.emit_v15_long_gpu_environment_lock --output-dir <path>` writes `v15_long_gpu_environment_lock.json` and `v15_long_gpu_environment_lock_report.json` (default profile **`fixture_ci`**; optional `--profile operator_local` and `--probe-json <path>`).

**M02 runtime narrative:** `docs/runtime/v15_long_gpu_run_environment_lock_v1.md`

**M03 emitter:** `python -m starlab.v15.emit_v15_checkpoint_lineage_manifest --output-dir <path>` writes `v15_checkpoint_lineage_manifest.json` and `v15_checkpoint_lineage_manifest_report.json` (default profile **`fixture_ci`**; optional `--profile operator_declared` with `--lineage-json <path>`; optional `--environment-lock-json <path>` to bind the canonical SHA-256 of an M02 environment lock file).

**M03 runtime narrative:** `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`

**M04 emitter:** `python -m starlab.v15.emit_v15_xai_evidence_pack --output-dir <path>` writes `v15_xai_evidence_pack.json` and `v15_xai_evidence_pack_report.json` (default profile **`fixture_ci`**; optional `--profile operator_declared` with `--evidence-json <path>`; optional `--checkpoint-lineage-json` / `--environment-lock-json` for canonical JSON SHA binding only).

**M04 runtime narrative:** `docs/runtime/v15_xai_evidence_contract_v1.md`

**M05 emitter:** `python -m starlab.v15.emit_v15_strong_agent_scorecard --output-dir <path>` writes `v15_strong_agent_scorecard.json` and `v15_strong_agent_scorecard_report.json` (default profile **`fixture_ci`**; optional `--profile operator_declared` with `--protocol-json <path>`; optional `--checkpoint-lineage-json` / `--xai-evidence-json` / `--environment-lock-json` for canonical JSON SHA binding only — **no** checkpoint blobs, **no** XAI execution).

**M05 runtime narrative:** `docs/runtime/v15_strong_agent_benchmark_protocol_v1.md`

**M06 emitter:** `python -m starlab.v15.emit_v15_human_panel_benchmark --output-dir <path>` writes `v15_human_panel_benchmark.json` and `v15_human_panel_benchmark_report.json` (default profile **`fixture_ci`**; optional `--profile operator_declared` with `--protocol-json <path>`; optional `--environment-lock-json` / `--checkpoint-lineage-json` / `--strong-agent-scorecard-json` / `--xai-evidence-json` for **canonical JSON SHA-256** binding only — no checkpoint blobs, no real participant I/O, no XAI inference).

**M06 runtime narrative:** `docs/runtime/v15_human_panel_benchmark_protocol_v1.md`

**M07 emitter:** `python -m starlab.v15.emit_v15_training_run_receipt --output-dir <path>` writes `v15_training_run_receipt.json` and `v15_training_run_receipt_report.json` (default profile **`fixture_ci`**, no PyTorch in CI; optional **`operator_declared`** with **`--receipt-json`**; optional **`operator_local_short_gpu`** with **`--allow-operator-local-execution`**, bounded **`--max-steps`**, **`--device cuda|cpu`** — isolated **synthetic** trainer only, not SC2 or PX2 pipelines; optional M02–M06 / config / dataset / rights JSON bindings by canonical SHA-256 only).

**M07 runtime narrative:** `docs/runtime/v15_training_smoke_short_gpu_shakedown_v1.md`

**M08 emitter:** `python -m starlab.v15.emit_v15_long_gpu_training_manifest --output-dir <path>` writes `v15_long_gpu_training_manifest.json`, `v15_long_gpu_training_manifest_report.json`, and (fixture) `v15_long_gpu_campaign_receipt.json` + report (default profile **`fixture_ci`**; **`operator_preflight`** binds M02/M03/M07/config/dataset/rights JSON by SHA-256; **`operator_declared`** normalizes a supplied manifest).

**M08 runner (operator-local only):** `python -m starlab.v15.run_v15_long_gpu_campaign` — requires `--allow-operator-local-execution` and `--authorize-long-gpu-campaign`; wraps `starlab.training.execute_full_local_training_campaign` after manifest/plan SHA match and gate checks.

**M08 runtime narrative:** `docs/runtime/v15_long_gpu_campaign_execution_v1.md`

**M09 emitter:** `python -m starlab.v15.emit_v15_checkpoint_evaluation --output-dir <path>` writes `v15_checkpoint_evaluation.json` and `v15_checkpoint_evaluation_report.json` (default profile **`fixture_ci`**; optional **`operator_preflight`** and bindings; optional **`operator_declared`** with **`--evaluation-json`**; optional **`operator_local_evaluation`** with dual local guards — **dry-run / validation only** in this repository default). `python -m starlab.v15.emit_v15_checkpoint_promotion_decision --evaluation-json <path> --output-dir <path>` writes `v15_checkpoint_promotion_decision.json` and `v15_checkpoint_promotion_decision_report.json`.

**M09 runtime narrative:** `docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`

**M10 emitter:** `python -m starlab.v15.emit_v15_replay_native_xai_demonstration --output-dir <path>` writes `v15_replay_native_xai_demonstration.json`, `v15_replay_native_xai_demonstration_report.json`, and `v15_xai_explanation_report.md` (default profile **`fixture_ci`**; optional **`operator_declared`** with **`--m09-promotion-decision-json`** and **`--m04-xai-evidence-pack-json`**; optional **`operator_preflight`** with additional M08/M03/M05 JSON inputs — **SHA-256 binding only**).

**M10 runtime narrative:** `docs/runtime/v15_replay_native_xai_demonstration_v1.md`

**M11 emitters:** `python -m starlab.v15.emit_v15_human_panel_execution --output-dir <path>` (default **`fixture_ci`**; optional **`operator_declared`**; optional **`operator_preflight`**) writes `v15_human_panel_execution.json` + `v15_human_panel_execution_report.json`. `python -m starlab.v15.emit_v15_human_benchmark_claim_decision --human-panel-execution-json <path> --output-dir <path>` writes `v15_human_benchmark_claim_decision.json` + `v15_human_benchmark_claim_decision_report.json` (deterministic over the **sealed** execution JSON; optional **`--strict`** requires non-placeholder M06/M09/M10 SHA fields).

**M11 runtime narrative:** `docs/runtime/v15_human_panel_bounded_benchmark_v1.md`

---

## 7. Long GPU run gate (definition)

Training at “long GPU run” scale is **not** treated as program-valid until gates **A–G** are explicitly satisfied by evidence in later milestones. Summary:

| Gate | Name | Intent |
| --- | --- | --- |
| **A** | Governance | Charter, claims, non-claims, public/private surfaces |
| **B** | Environment | GPU, CUDA/PyTorch, SC2, maps, disk, dependency pins |
| **C** | Data | Manifests, hashes, rights, reproducible labels |
| **D** | Checkpoints | Hashing, lineage, resume, rollback, promotion states |
| **E** | Evaluation | Frozen scorecard / baselines, fixture and live paths as declared |
| **F** | XAI | Frozen contract, fixture pack, traces, reports |
| **G** | Operator | Runbook, stop/resume, retention, failure handling |

Canonical machine-readable structure: `long_gpu_run_gates` in `v15_training_readiness_charter.json`.

---

## 8. Evaluation ladder (summary)

Ordered evidence stages used for v1.5 evaluation narrative (details in moonshot doc): **E0** artifact integrity → **E1** fixture smoke → **E2** scripted baselines → **E3** heuristic baselines → **E4** prior STARLAB checkpoints → **E5** local live SC2 (bounded) → **E6** exploit/failure probes → **E7** human panel → **E8** XAI review.

---

## 9. XAI demonstration surfaces (minimum)

Minimum demonstration expectations include governance-style artifacts such as: decision trace, attribution / concept summaries, counterfactual probes, alternative action rankings, replay overlay manifest, and an explanation report—bound to replay and checkpoint identity. **M00** defines intent; later milestones freeze formats and emit fixture packs.

---

## 10. Configuration and reproducibility governance

Long runs must bind identity and environment fields (git SHA, branch, milestone, Python/deps, CUDA, PyTorch, GPU, SC2 version, map pool, seeds, dataset and checkpoint hashes, config hash, operator notes). Run-class manifests (training, environment, hardware, dataset, checkpoint, evaluation, XAI, human benchmark, rights) are expected for v1.5-scale evidence. **M00** states the requirement; **V15-M01+** implements registers and automation as needed.

---

## 11. CI security note (M00–M07, temporary)

The default merge CI runs **`pip-audit`** with a **single** narrow ignore: **`--ignore-vuln CVE-2026-3219`** for the **`pip` toolchain**. **M01 re-check (2026-04-24, CI-like env):** after `pip install --upgrade pip`, **`pip` 26.0.1** still reported **CVE-2026-3219** to **`pip-audit`**. **M02 re-check (2026-04-25, CI-like local env):** same — **`pip` 26.0.1** still reports the CVE; **no** audit-clean **`pip`** upgrade path observed. **M03 re-check (2026-04-25, local env):** **`pip` 26.0.1** is still the latest on PyPI; **`pip-audit`** still flags **CVE-2026-3219** for **`pip`**. **M04 re-check (2026-04-25, local env):** **`pip index versions pip`** still shows **26.0.1** as latest; **no** newer audit-clean wheel observed — **leave** the **same** single narrow ignore. **M05 re-check (2026-04-25, local env):** **`pip index versions pip`** still shows **26.0.1** as latest; **no** audit-clean fixed **`pip`** on PyPI observed — **leave** the same single narrow ignore; do **not** broaden exceptions. **M06 re-check (2026-04-25, local env):** **`python -m pip index versions pip`** still shows **26.0.1** as **LATEST**; **no** newer audit-clean **`pip`** on PyPI observed — **leave** the same single narrow **pip-only** ignore; do **not** broaden exceptions. **M07 re-check (2026-04-25, local env):** same — **`pip` 26.0.1** still latest; **leave** the **same** narrow **`pip`**-only **CVE-2026-3219** ignore; do **not** broaden. This is **not** `continue-on-error`. **CycloneDX SBOM** generation, **SBOM upload**, **Gitleaks**, and the aggregate **governance** job still run. **Remove** the ignore when a fixed, audit-clean **`pip`** is published on PyPI.

---

## 12. Open risks and carry-forward items (M32-family)

Addressed or explicitly deferred in future **V15** milestones:

- Meaningful **coverage** gate vs floor-only policy.
- **CI tiering** (fast / slow / operator-local) vs default merge path truthfulness.
- **JSON I/O** deduplication at long-run scale.
- **Architecture** overview for training-scale operator paths.
- **Provenance** for replay, data, weights, and benchmarks under long-run storage.

---

## 13. Document maintenance (per `.cursorrules`)

Any milestone that changes artifact shape, contract behavior, interface boundaries, environment pins, or replay/evaluation semantics must update **this file** in the same milestone. This document must stay synchronized with code, label **stable vs provisional** surfaces, and remain suitable as the first document an auditor reads for v1.5.
