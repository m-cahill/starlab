# STARLAB v1.5 — Long GPU Training & Explainable Strong-Agent Moonshot

**Document Type:** Moonshot Anchor / v1.5 Charter Draft
**Project:** STARLAB — Strategic Testing, Analysis, Replay, and Learning Lab
**Phase:** v1.5 / V15
**Opening Milestone:** `V15-M00` — Training Readiness Charter and Long GPU Run Gate
**Status:** Proposed anchor document
**Primary Machine:** Local RTX 5090 Blackwell workstation
**Primary Domain:** StarCraft II, Terran-first, 1v1
**Primary Objective:** A bounded strong agent with replay-native XAI evidence

---

## 0. Source anchors

This v1.5 moonshot is anchored in four existing truths:

1. **STARLAB is a replay-native, governed RTS research substrate**, not merely a ladder bot project. The original STARLAB vision defines the project as a reproducible, replay-native StarCraft II research substrate for hierarchical, perception-grounded, multi-agent research. 

2. **PX2 is closed as a governed transition phase, not as a long GPU training success.** PX2-M03 closed with bounded self-play / operator-local surfaces, but explicitly did **not** complete a long GPU training campaign or prove strong-agent capability.  

3. **The current ledger places the program at `V15-M00`.** `docs/starlab.md` records `V15-M00` as the current milestone and frames it as the v1.5 Training Readiness Charter and Long GPU Run Gate. 

4. **v1.5 must carry forward unresolved structural risks.** The M32 audit family identified coverage visibility/gating, CI tiering, duplicated JSON I/O, architecture overview, and training-scale provenance as material issues that become more important before a serious long training run. 

---

## 1. One-line moonshot

**STARLAB v1.5 exists to produce a bounded, replay-native, explainable StarCraft II agent trained through a full local GPU campaign, with enough governed evidence to credibly claim it beats most humans under a declared STARLAB benchmark — without overclaiming ladder universality, benchmark universality, or v2 readiness.**

---

## 2. The v1.5 thesis

The v1 foundation proved that STARLAB can be governed, replay-native, artifact-driven, and careful about non-claims.

PV1 and PX1 proved that STARLAB can run industrial-style campaigns, package bounded demos, and preserve evidence discipline.

PX2 created the autonomous full-game skill-development line and built many bounded self-play surfaces, but closed honestly as a transition phase rather than a long GPU training outcome.

**v1.5 is the missing bridge:**

```text
governed substrate
→ long GPU training session
→ stronger full-game agent
→ replay-native XAI explanation pack
→ bounded human-facing benchmark claim
→ v2 readiness decision
```

The v1.5 goal is not just “train longer.” The goal is to make a long GPU run **auditable, inspectable, reproducible enough to trust, and explainable enough to demonstrate.**

---

## 3. Why v1.5 exists before v2

v2 should not begin merely because the v1 substrate is strong or because PX2 created self-play machinery.

v2 should begin only after STARLAB can show:

* a serious long training campaign
* checkpoint lineage
* training/data/weight provenance
* benchmark discipline
* a bounded strong-agent claim
* replay-native XAI evidence
* honest unresolved-risk tracking

v1.5 exists because **moving to v2 before proving a strong, explainable agent would weaken the STARLAB story.**

The v1.5 phase should answer:

> Can STARLAB turn its governed substrate into a real trained agent that plays substantially better than ordinary humans, while explaining its decisions through replay-native evidence?

If the answer is no, v2 should wait.

If the answer is yes, v2 begins from strength rather than aspiration.

---

## 4. Strategic objective

The v1.5 strategic objective is:

> Produce a governed STARLAB Showcase Agent that can beat most evaluated human players under a declared, bounded protocol, and demonstrate replay-native XAI explanations for wins, losses, and critical decisions.

The wording matters.

v1.5 should **not** claim:

```text
The agent beats all humans.
The agent is ladder-dominant.
The agent is globally benchmark-superior.
The agent has solved SC2.
The agent is equivalent to AlphaStar.
```

v1.5 may claim, if evidence supports it:

```text
The v1.5 Showcase Agent beats most humans in STARLAB Human Panel Benchmark v1 under declared constraints.
```

or:

```text
The v1.5 Showcase Agent exceeds the declared STARLAB human-panel majority threshold under fixed map, race, protocol, and replay-capture rules.
```

---

## 5. v1.5 success definition

v1.5 succeeds only if all five pillars are satisfied.

### Pillar 1 — Full GPU training run completed

A long local GPU training campaign must complete with:

* run manifest
* environment manifest
* dataset manifest
* checkpoint manifest
* model config
* training logs
* checkpoint cadence
* eval cadence
* stop/resume receipts
* failure/interrupt receipts if applicable
* final lineage bundle

The campaign must be materially more than a fixture run, smoke run, or bounded continuity surface.

### Pillar 2 — Strong-agent benchmark passed

The trained agent must pass a predeclared benchmark ladder, such as:

```text
T0 — fixture smoke
T1 — scripted baselines
T2 — heuristic baselines
T3 — prior STARLAB checkpoint agents
T4 — bounded local live SC2 tests
T5 — human panel benchmark
```

The benchmark must be declared before the final claim is made.

### Pillar 3 — Replay-native XAI demonstration works

The agent must produce XAI evidence packs for selected games.

At minimum:

```text
decision_trace.json
saliency_or_attention_summary.json
concept_activation_summary.json
counterfactual_decision_probe.json
alternative_action_report.json
replay_overlay_manifest.json
xai_explanation_report.md
```

The XAI demo must include:

* at least one win
* at least one loss or failure case
* at least one macro decision
* at least one tactical/combat decision
* at least one scouting or uncertainty decision
* at least one counterfactual explanation

RediAI v3’s architectural posture treats XAI as first-class through attribution, saliency, concept discovery, counterfactuals, and integrated training hooks, which is the right design direction for STARLAB’s v1.5 evidence model. 

### Pillar 4 — Human-benchmark claim is bounded and evidence-backed

If v1.5 says “beats most humans,” then the claim must mean:

```text
beats most humans in a declared STARLAB benchmark,
under declared rules,
against recorded participants or equivalent human reference set,
with replay evidence,
using the declared checkpoint,
on declared maps,
with declared race and action constraints.
```

No broader claim should be made.

### Pillar 5 — v2 go/no-go decision becomes evidence-based

v1.5 must end with a clear decision:

```text
Proceed to v2
Proceed to v1.6 hardening
Repeat/extend training
Stop and recharter
```

The decision must be grounded in artifacts, not enthusiasm.

---

## 6. Non-goals

v1.5 is **not**:

* v2
* a multi-game expansion
* a multi-race program
* a public ladder dominance claim
* a replacement for benchmark integrity work
* a replacement for replay↔execution equivalence work
* an unbounded research experiment
* a private-only training run with no auditable evidence
* a marketing demo detached from artifacts
* a pure XAI visualization project without agent strength
* a pure agent-strength project without XAI

---

## 7. Claim boundaries

### Allowed v1.5 claim shape

A strong v1.5 claim should look like:

> “The STARLAB v1.5 Showcase Agent, trained under campaign `V15-…`, using checkpoint `…`, beats the declared majority threshold in STARLAB Human Panel Benchmark v1 under fixed Terran-first 1v1 conditions, with replay-native XAI evidence packs for representative wins, losses, and critical decisions.”

### Disallowed claim shape

Avoid:

> “The agent beats most humans.”

without protocol boundaries.

Avoid:

> “STARLAB has solved StarCraft II.”

Avoid:

> “The v1.5 agent is ladder-proven.”

unless an actual ladder/public evaluation protocol is executed and separately evidenced.

Avoid:

> “The model is explainable.”

Instead say:

> “The run produced replay-native XAI evidence packs under the declared XAI Evidence Contract.”

---

## 8. Training philosophy

v1.5 should use a **hybrid hierarchical training strategy** rather than an unbounded pure-RL-first approach.

The recommended training ladder is:

```text
replay-bootstrap supervised policy
→ constrained self-play
→ curriculum opponent pool
→ promotion/rollback gates
→ checkpoint league
→ targeted refit / fine-tuning
→ final strong-agent evaluation
→ human-panel benchmark
→ XAI evidence pack
```

The reason is practical: STARLAB already has replay, state, observation, hierarchy, bootstrap, live-play, and self-play surfaces. v1.5 should compound those surfaces rather than discard them.

---

## 9. Agent architecture target

The v1.5 agent should be described as a **Showcase Agent**, not a final general agent.

Recommended structure:

```text
Replay / game-state inputs
  → representation encoder
  → strategic intent head
  → macro policy head
  → tactical policy head
  → value / outcome head
  → legality / action-mask layer
  → XAI hooks
  → action compiler
  → SC2 runtime bridge
```

### Minimum action hierarchy

The agent should distinguish at least:

* economy / worker control
* production
* army movement
* scouting
* combat engagement / disengagement
* expansion
* technology progression
* defensive response
* fallback/no-op safety

### Minimum explanation hierarchy

The XAI layer should explain at least:

* why this strategic intent was selected
* why this macro action was selected
* why this tactical action was selected
* which state features influenced the action
* which alternatives were considered
* what counterfactual state would have changed the decision

---

## 10. XAI demonstration target

The v1.5 XAI demo should be one of the flagship outcomes.

It should let a viewer ask:

```text
Why did the agent expand here?
Why did it attack here?
Why did it retreat?
Why did it scout this region?
Why did it build this tech?
Why did it lose this fight?
What would have changed the decision?
```

The answer should be supported by artifacts, not narration.

### XAI evidence pack

Each selected replay should have:

```text
xai/
  xai_manifest.json
  replay_identity.json
  checkpoint_identity.json
  decision_trace.json
  critical_decision_index.json
  attribution_summary.json
  concept_activation_summary.json
  counterfactual_probe_results.json
  alternative_action_rankings.json
  uncertainty_report.json
  replay_overlay_manifest.json
  xai_explanation_report.md
```

### XAI demo scenes

v1.5 should curate a small set of scenes:

| Scene              | Purpose                                       |
| ------------------ | --------------------------------------------- |
| Opening build      | explain macro plan                            |
| First scout        | explain uncertainty and information gathering |
| First combat       | explain tactical policy                       |
| Expansion timing   | explain risk/reward                           |
| Defensive response | explain adaptation                            |
| Winning push       | explain decisive action                       |
| Loss/failure case  | explain limitation honestly                   |

### XAI non-claims

The XAI demo does **not** prove:

* the model is fully interpretable
* saliency is causal truth
* every decision has a human-like explanation
* explanations are globally faithful without validation
* the agent reasons the way humans do

The XAI demo proves only that STARLAB can produce governed, replay-native explanation artifacts under a declared contract.

---

## 11. Human benchmark target

The preferred v1.5 human-facing claim is:

> “The Showcase Agent beats most participants in STARLAB Human Panel Benchmark v1.”

### Human Panel Benchmark v1

Minimum structure:

```text
benchmark_id: starlab.v15.human_panel_benchmark.v1
race: Terran
opponents: human participants
map_pool: fixed
agent_checkpoint: fixed
game_count: predeclared
replay_capture: required
xai_pack_sample: required for selected games
result_policy: predeclared
participant_skill_tags: recorded where available
non_claims: required
```

### Participant tiers

Even a small panel should tag participants by rough skill:

```text
casual / unranked
Bronze-Silver equivalent
Gold-Platinum equivalent
Diamond+ equivalent
unknown / self-reported only
```

If skill cannot be verified, it must be labeled as self-reported or unknown.

### Claim threshold

A reasonable claim threshold:

```text
Agent wins >50% of games against the declared human panel.
```

A stronger threshold:

```text
Agent wins ≥65% of games against the declared human panel.
```

A more conservative first v1.5 threshold:

```text
Agent wins a majority against casual-to-mid-skill human participants under declared constraints.
```

The chosen threshold must be frozen before the benchmark is run.

---

## 12. Training-run governance

A long GPU run is not valid unless it is governed.

### Required run manifests

```text
training_manifest.json
environment_manifest.json
hardware_manifest.json
dataset_manifest.json
checkpoint_manifest.json
evaluation_manifest.json
xai_manifest.json
human_benchmark_manifest.json
rights_manifest.json
```

### Required identity fields

Every major artifact should bind:

* git SHA
* branch
* milestone
* Python version
* dependency lock/hash
* CUDA version
* PyTorch version
* GPU identity
* SC2 client version
* map pool
* run seed policy
* dataset hash
* checkpoint hash
* config hash
* operator note
* non-claims

### Minimum checkpoint metadata

Each checkpoint should record:

```json
{
  "checkpoint_id": "...",
  "checkpoint_path": "...",
  "checkpoint_sha256": "...",
  "parent_checkpoint_id": "...",
  "training_run_id": "...",
  "step": 0,
  "episode": 0,
  "wall_clock_elapsed": "...",
  "dataset_manifest_sha256": "...",
  "model_config_sha256": "...",
  "eval_summary_sha256": "...",
  "promotion_status": "candidate|promoted|rejected|archived"
}
```

---

## 13. Provenance posture

v1.5 must preserve the “clean enough to buy” discipline.

The acquisition-readiness posture says a project should be ownable, legible, separable, defensible, maintainable, and low-friction to diligence; it also warns that code, data, replays, labels, weights, and benchmark assets need separate provenance and governance. 

For v1.5, this means:

```text
code ≠ data ≠ replays ≠ labels ≠ weights ≠ benchmarks ≠ videos ≠ XAI reports
```

Each surface needs its own rights status.

### Required asset registers

v1.5 should create or update:

```text
docs/training_asset_register.md
docs/model_weight_register.md
docs/replay_corpus_register.md
docs/human_benchmark_register.md
docs/xai_evidence_register.md
docs/rights_register.md
```

If private versions are required:

```text
docs/company_secrets/training_asset_register.md
docs/company_secrets/model_weight_register.md
docs/company_secrets/human_panel_register.md
```

### Rule

If provenance is unclear, the asset must not be used for the core v1.5 claim.

---

## 14. v1.5 audit posture

The v1.5 audit goal is **5/5**, but only if evidence supports it.

A 5/5 audit requires:

* no hidden long-run evidence
* no untracked weights
* no untracked datasets
* no vague human benchmark
* no overclaiming agent strength
* no missing checkpoint hashes
* no missing environment manifests
* no “it worked locally” without receipts
* no XAI cherry-picking without declared sample policy
* no post-hoc benchmark threshold changes

The standing audit principle remains:

> Audits are active governance signals, not retrospective reports.

Material audit findings should be addressed in the next appropriate milestone unless explicitly deferred with rationale.

---

## 15. Structural risks carried into v1.5

v1.5 must explicitly address or deliberately defer these carried-forward risks.

| Risk                                           | Why it matters in v1.5                                                                   | Expected treatment                                   |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Coverage gate / meaningful coverage            | Long training changes need trustworthy regression detection                              | define target and gate before training-heavy changes |
| CI tiering policy                              | Long-run artifacts cannot all be merge-gate CI, but smoke/quality paths must be truthful | document fast/slow/operator-local split              |
| JSON I/O dedup                                 | Long-run manifests multiply artifact parsing risk                                        | converge or inventory remaining duplication          |
| Architecture overview for training-scale paths | Operators need a clear mental model before long runs                                     | add v1.5 training architecture/runbook diagram       |
| Replay/data/weight provenance                  | Long run creates valuable, risky assets                                                  | manifests + registers required                       |
| XAI artifact contract                          | Explanations can become ad hoc if not frozen                                             | create formal XAI evidence contract                  |
| Human benchmark protocol                       | “Beats most humans” can overclaim easily                                                 | freeze benchmark before evaluation                   |
| Checkpoint lineage                             | Promotion/rollback requires exact identity                                               | checkpoint manifest required                         |
| Operator interruption / resume                 | Long run will likely be interrupted                                                      | resume receipts required                             |
| Storage discipline                             | Long runs produce large artifacts                                                        | retention, archival, and hash policy required        |

---

## 16. v1.5 artifact family

v1.5 should introduce a small, explicit artifact family.

Recommended contracts:

```text
starlab.v15.training_readiness_charter.v1
starlab.v15.long_gpu_training_manifest.v1
starlab.v15.checkpoint_lineage_manifest.v1
starlab.v15.training_run_receipt.v1
starlab.v15.strong_agent_scorecard.v1
starlab.v15.xai_evidence_pack.v1
starlab.v15.human_panel_benchmark.v1
starlab.v15.showcase_agent_release_pack.v1
```

Primary files:

```text
v15_training_readiness_charter.json
v15_training_readiness_charter_report.json

v15_long_gpu_training_manifest.json
v15_long_gpu_training_manifest_report.json

v15_checkpoint_lineage_manifest.json
v15_checkpoint_lineage_manifest_report.json

v15_strong_agent_scorecard.json
v15_strong_agent_scorecard_report.json

v15_xai_evidence_pack.json
v15_xai_evidence_pack_report.json

v15_human_panel_benchmark.json
v15_human_panel_benchmark_report.json

v15_showcase_agent_release_pack.json
v15_showcase_agent_release_pack_report.json
```

---

## 17. Recommended v1.5 milestone map

Keep milestones small. The goal is not to sprint into the long run; the goal is to make the long run survivable.

| Milestone | Title                                            | Purpose                                                                         | Done when                                                         |
| --------- | ------------------------------------------------ | ------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `V15-M00` | Training Readiness Charter and Long GPU Run Gate | Freeze v1.5 goals, claims, non-claims, artifact families, and go/no-go gates    | `docs/starlab.md` updated; charter artifact emitted; audit passes |
| `V15-M01` | Training-Scale Provenance and Asset Registers    | Create data/replay/weights/checkpoint provenance surfaces                       | registers exist; tests validate required fields                   |
| `V15-M02` | Long GPU Run Environment Lock                    | Capture RTX 5090 / CUDA / PyTorch / SC2 / dependency environment                | environment manifest and smoke run pass                           |
| `V15-M03` | Checkpoint Lineage and Resume Discipline         | Make checkpoint, resume, interrupt, and rollback receipts first-class           | checkpoint manifest + resume test pass                            |
| `V15-M04` | XAI Evidence Contract v1                         | Freeze decision trace, attribution, concept, and counterfactual artifact shapes | fixture XAI pack validates                                        |
| `V15-M05` | Strong-Agent Benchmark Protocol                  | Freeze baseline ladder, maps, agent constraints, and scorecard                  | scorecard schemas + fixture eval pass                             |
| `V15-M06` | Human Panel Benchmark Protocol                   | Freeze “beats most humans” protocol and non-claims                              | human benchmark contract validates                                |
| `V15-M07` | Training Smoke and Short GPU Shakedown           | Run short GPU training with full manifests and checkpoint receipts              | shakedown completes; no provenance gaps                           |
| `V15-M08` | Long GPU Campaign Execution                      | Execute the actual long run                                                     | training receipt + checkpoint lineage complete                    |
| `V15-M09` | Checkpoint Evaluation and Promotion              | Select candidate checkpoint using frozen benchmark                              | promoted candidate has scorecard                                  |
| `V15-M10` | Replay-Native XAI Demonstration                  | Produce XAI packs for selected games                                            | XAI packs validate and reports render                             |
| `V15-M11` | Human Panel / Bounded Human Benchmark            | Run human benchmark under frozen rules                                          | result report produced; claim determined                          |
| `V15-M12` | Showcase Agent Release Pack                      | Package final agent, evidence, XAI, benchmark, and non-claims                   | release pack and audit complete                                   |
| `V15-M13` | v2 Go / No-Go Decision                           | Decide whether to move to v2                                                    | decision recorded in `docs/starlab.md`                            |

This can be shortened if implementation surfaces already exist, but it should not collapse readiness, long run, evaluation, XAI, and human benchmark into one milestone.

---

## 18. Long GPU run gate

The long GPU run should not begin until `V15-M00`–`V15-M07` or equivalent readiness gates are green.

### Gate A — Governance

* `docs/starlab.md` updated
* v1.5 charter exists
* claim boundaries frozen
* non-claims explicit
* private/public surfaces defined

### Gate B — Environment

* GPU detected
* CUDA/PyTorch compatible
* SC2 runtime available
* maps available
* disk space sufficient
* dependency versions recorded

### Gate C — Data

* replay/data manifests exist
* data hash recorded
* rights posture recorded
* labels reproducible
* no unclear provenance in core training set

### Gate D — Checkpoints

* checkpoint hashing works
* parent/child lineage works
* resume from checkpoint tested
* rollback tested
* promotion/rejection states tested

### Gate E — Evaluation

* benchmark scorecard frozen
* fixture eval works
* live eval path available where needed
* prior baselines recorded

### Gate F — XAI

* XAI contract frozen
* fixture XAI pack generated
* decision trace works
* report generation works

### Gate G — Operator

* runbook exists
* stop/resume procedure tested
* artifact retention policy recorded
* failure handling recorded

---

## 19. Training run classes

v1.5 should distinguish run classes.

| Run class           | Purpose                     | Claim allowed                                |
| ------------------- | --------------------------- | -------------------------------------------- |
| Fixture smoke       | CI-safe artifact wiring     | wiring works                                 |
| GPU shakedown       | local GPU readiness         | environment and trainer work                 |
| Short training run  | pipeline sanity             | training loop is viable                      |
| Medium training run | early performance trend     | candidate quality emerging                   |
| Long GPU run        | v1.5 core training campaign | checkpoint lineage and long-run result       |
| Evaluation run      | benchmark measurement       | scorecard result                             |
| Human panel run     | bounded human claim         | “beats most humans” only if threshold passes |
| XAI run             | explanation evidence        | replay-native XAI artifacts                  |

The moonshot depends on the **long GPU run**, but the long GPU run depends on the earlier run classes.

---

## 20. Evaluation ladder

Recommended v1.5 evaluation ladder:

```text
E0 — Artifact integrity
E1 — Fixture smoke
E2 — Scripted baseline tournament
E3 — Heuristic baseline tournament
E4 — Prior STARLAB checkpoint comparison
E5 — Local live SC2 bounded eval
E6 — Exploit / failure-mode probe
E7 — Human panel benchmark
E8 — XAI explanation review
```

### Promotion rule

A checkpoint should be promoted only if:

* it passes artifact integrity
* it improves over the previous promoted checkpoint
* it does not regress catastrophically on baseline tasks
* it has no unresolved lineage/provenance gap
* it can produce XAI traces
* it passes declared safety/fallback constraints

---

## 21. Strong-agent scorecard

A v1.5 strong-agent scorecard should include:

```text
checkpoint_id
training_run_id
evaluation_protocol_id
map_pool_id
opponent_pool_id
game_count
win_rate
loss_rate
draw_or_timeout_rate
average_game_length
early_loss_rate
economy_score
production_score
combat_score
scouting_score
expansion_score
fallback_action_rate
invalid_action_rate
xai_trace_coverage
critical_decision_trace_count
non_claims
```

This should be separate from the human-panel scorecard.

---

## 22. Human-panel scorecard

A human-panel scorecard should include:

```text
participant_id_or_alias
skill_tag
skill_tag_source
map
race
agent_checkpoint_id
result
replay_path
replay_sha256
game_length
agent_win_condition
human_feedback_optional
xai_pack_selected
notes
```

If privacy requires aliases, use aliases. Do not expose personally identifying information unless explicitly authorized.

---

## 23. XAI evaluation

XAI should itself be evaluated.

Minimum XAI review questions:

| Question                                                | Expected evidence                   |
| ------------------------------------------------------- | ----------------------------------- |
| Did the decision trace cover the critical decision?     | `critical_decision_index.json`      |
| Did the explanation cite actual state facts?            | `decision_trace.json`               |
| Were alternatives ranked?                               | `alternative_action_rankings.json`  |
| Was at least one counterfactual tested?                 | `counterfactual_probe_results.json` |
| Was the replay binding preserved?                       | `replay_identity.json`              |
| Was the checkpoint identity preserved?                  | `checkpoint_identity.json`          |
| Was the explanation generated for both wins and losses? | `xai_manifest.json`                 |

---

## 24. Operator runbook requirements

v1.5 needs a real runbook before the long GPU run.

Required sections:

```text
1. Environment setup
2. GPU / CUDA verification
3. SC2 runtime verification
4. Data manifest verification
5. Training command
6. Checkpoint cadence
7. Evaluation cadence
8. XAI sample cadence
9. Stop procedure
10. Resume procedure
11. Failure quarantine
12. Artifact archival
13. Post-run validation
14. Human benchmark preparation
15. Closeout instructions
```

The runbook should be public where possible and private where necessary.

---

## 25. Storage and artifact retention

Long runs produce too much material for casual handling.

v1.5 should define:

* what is committed
* what is local-only
* what is archived
* what is hashed but not copied
* what is private
* what can be public
* what is excluded by `.gitignore`
* what belongs in `docs/company_secrets`
* what belongs in `out/`
* what belongs in a model-weight archive

### Recommended default

```text
Commit:
  schemas
  manifests
  reports
  summary markdown
  small fixture artifacts

Do not commit:
  raw weights
  large checkpoints
  raw replay corpora
  videos
  private human panel information
  large training logs

Hash and reference:
  weights
  checkpoints
  replays
  videos
  human benchmark private records
```

---

## 26. Public/private boundary

v1.5 should expose enough to be credible, but not casually leak sensitive or rights-unclear assets.

### Public-friendly

* v1.5 charter
* artifact schemas
* non-claims
* run summaries
* benchmark protocol
* XAI evidence contract
* selected sanitized reports
* release-pack summary

### Private/local-only by default

* raw model weights
* raw checkpoints
* raw human panel identities
* raw replay files if rights unclear
* videos unless cleared
* operator notes with sensitive environment paths
* `docs/company_secrets/**`

---

## 27. v1.5 release pack

The final v1.5 release pack should include:

```text
v15_showcase_agent_release_pack.json
v15_showcase_agent_release_pack_report.json
model_card.md
training_run_summary.md
benchmark_summary.md
human_panel_summary.md
xai_demo_summary.md
non_claims.md
asset_register_summary.md
audit.md
```

It should answer:

* What checkpoint is the Showcase Agent?
* What trained it?
* What data did it use?
* What did it beat?
* What did it fail at?
* What XAI evidence exists?
* What claim is allowed?
* What claim is disallowed?
* Should STARLAB proceed to v2?

---

## 28. v2 go/no-go criteria

v2 may begin only if v1.5 closes with one of these outcomes:

### Green v2 gate

Proceed to v2 if:

* long GPU run completed
* promoted checkpoint exists
* benchmark threshold passed
* XAI packs exist
* human-panel claim is either passed or honestly recorded
* provenance is clean
* audit score is high
* `docs/starlab.md` is updated

### Yellow v2 gate

Delay v2 and continue v1.5 / v1.6 if:

* long run completed but agent is not strong enough
* XAI works but benchmark fails
* benchmark works but provenance is weak
* human-panel result is inconclusive
* audit finds material issues

### Red v2 gate

Do not proceed if:

* no long run completed
* checkpoint lineage is broken
* data/weights provenance is unclear
* strong-agent claim is unsupported
* XAI evidence is ad hoc or cherry-picked
* audit score is poor
* CI/governance was weakened to make the run look successful

---

## 29. Standing non-claims for v1.5

Even if v1.5 succeeds, these remain non-claims unless separately proved:

* not global SC2 solution
* not ladder dominance
* not multi-race performance
* not multi-game generality
* not universal benchmark integrity
* not universal replay↔execution equivalence
* not guarantee of human-like reasoning
* not guarantee that XAI explanations are causal truth
* not public rights clearance for all assets
* not production deployment readiness
* not v2 by default

---

## 30. Suggested `docs/starlab.md` additions for V15-M00

At `V15-M00` closeout, add a compact version of this moonshot to `docs/starlab.md`.

Recommended ledger sections:

```markdown
## v1.5 — Long GPU Training & Explainable Strong-Agent Moonshot

### v1.5 identity
### v1.5 success criteria
### v1.5 non-claims
### v1.5 artifact family
### v1.5 long GPU run gate
### v1.5 XAI evidence contract
### v1.5 human-panel benchmark boundary
### v1.5 v2 go/no-go criteria
```

Also update the quick-scan table:

```markdown
| Current phase | v1.5 (V15) — Long GPU Training & Explainable Strong-Agent Moonshot |
| Current milestone | V15-M00 — Training Readiness Charter and Long GPU Run Gate |
| PX2 status | Closed / transition-complete; no long GPU run claimed |
| v2 status | Not opened |
```

---

## 31. First Cursor handoff prompt for `V15-M00`

Use this after the moonshot is accepted.

```markdown
We are opening STARLAB v1.5 with V15-M00.

Goal:
Create the v1.5 Training Readiness Charter and Long GPU Run Gate. This is a governance/artifact-contract milestone, not the long GPU run itself.

Required source anchors:
- docs/starlab.md
- docs/runtime/v15_long_gpu_training_moonshot_v1.md or docs/v15_moonshot.md
- PX2-M03 closeout notes if available locally
- M32/M33/M34/M35 audit closure context where relevant

Tasks:
1. Add a public v1.5 runtime/charter document:
   docs/runtime/v15_training_readiness_charter_v1.md

2. Add deterministic charter emitter(s), if consistent with existing STARLAB patterns:
   - v15_training_readiness_charter.json
   - v15_training_readiness_charter_report.json

3. Define, but do not execute, the long GPU run gate:
   - governance gate
   - environment gate
   - data/provenance gate
   - checkpoint gate
   - evaluation gate
   - XAI gate
   - operator gate

4. Define v1.5 artifact-family names:
   - training manifest
   - checkpoint lineage manifest
   - XAI evidence pack
   - strong-agent scorecard
   - human-panel benchmark
   - showcase release pack

5. Update docs/starlab.md:
   - V15-M00 opened/closed according to milestone status
   - v1.5 moonshot summarized
   - PX2 remains closed and does not claim long GPU training
   - v2 remains not opened
   - v1.5 non-claims recorded

6. Add governance tests that confirm:
   - docs/starlab.md mentions V15-M00
   - v1.5 charter exists
   - PX2 long-GPU non-claim remains present
   - v2 is not opened
   - required v1.5 artifact families are listed

7. Validate locally:
   - ruff check starlab tests
   - ruff format --check starlab tests
   - mypy starlab tests
   - python -m pytest -q

8. Do not run the long GPU campaign in V15-M00.
9. Do not commit private docs/company_secrets artifacts unless policy explicitly allows.
10. Return:
   - files changed
   - validation results
   - emitted artifact paths
   - unresolved risks
   - next recommended milestone
```

---

## 32. Final moonshot anchor

The v1.5 project should be ambitious, but not vague.

The north star is:

```text
A strong STARLAB Showcase Agent,
trained through a real long GPU campaign,
evaluated under frozen benchmark rules,
explained through replay-native XAI artifacts,
and bounded by honest non-claims.
```

The emotional goal is impressive:

> “This agent can beat most humans we evaluate.”

The engineering goal is stricter:

> “This claim is backed by manifests, checkpoints, replays, scorecards, XAI packs, human-panel records, and an audit trail strong enough to survive scrutiny.”

That is the v1.5 moonshot.
