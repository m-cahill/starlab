# STARLAB v1.5 — Authoritative Public Governance (V15)

**Program phase:** v1.5 (milestone namespace **V15**)  
**Status:** Active program line — **V15-M00** establishes charter, gates, and artifact names; it does **not** claim a completed long GPU run, strong agent, human benchmark, or XAI demo.

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

---

## 5. V15 milestone table (plan)

| Milestone | Title |
| --- | --- |
| **V15-M00** | Training Readiness Charter and Long GPU Run Gate |
| **V15-M01** | Training-Scale Provenance and Asset Registers |
| **V15-M02** | Long GPU Run Environment Lock |
| **V15-M03** | Checkpoint Lineage and Resume Discipline |
| **V15-M04** | XAI Evidence Contract v1 |
| **V15-M05** | Strong-Agent Benchmark Protocol |
| **V15-M06** | Human Panel Benchmark Protocol |
| **V15-M07** | Training Smoke and Short GPU Shakedown |
| **V15-M08** | Long GPU Campaign Execution |
| **V15-M09** | Checkpoint Evaluation and Promotion |
| **V15-M10** | Replay-Native XAI Demonstration |
| **V15-M11** | Human Panel / Bounded Human Benchmark |
| **V15-M12** | Showcase Agent Release Pack |
| **V15-M13** | v2 Go / No-Go Decision |

---

## 6. Artifact family contract ids (governed names)

These are the **intended** v1.5 contract identifiers (emission implemented per milestone; M00 defines names and charter JSON).

- `starlab.v15.training_readiness_charter.v1`
- `starlab.v15.long_gpu_training_manifest.v1`
- `starlab.v15.checkpoint_lineage_manifest.v1`
- `starlab.v15.training_run_receipt.v1`
- `starlab.v15.strong_agent_scorecard.v1`
- `starlab.v15.xai_evidence_pack.v1`
- `starlab.v15.human_panel_benchmark.v1`
- `starlab.v15.showcase_agent_release_pack.v1`

**M00 emitter:** `python -m starlab.v15.emit_v15_training_readiness_charter --output-dir <path>` writes `v15_training_readiness_charter.json` and `v15_training_readiness_charter_report.json`.

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

## 11. Open risks and carry-forward items (M32-family)

Addressed or explicitly deferred in future **V15** milestones:

- Meaningful **coverage** gate vs floor-only policy.
- **CI tiering** (fast / slow / operator-local) vs default merge path truthfulness.
- **JSON I/O** deduplication at long-run scale.
- **Architecture** overview for training-scale operator paths.
- **Provenance** for replay, data, weights, and benchmarks under long-run storage.

---

## 12. Document maintenance (per `.cursorrules`)

Any milestone that changes artifact shape, contract behavior, interface boundaries, environment pins, or replay/evaluation semantics must update **this file** in the same milestone. This document must stay synchronized with code, label **stable vs provisional** surfaces, and remain suitable as the first document an auditor reads for v1.5.
