# PX2 — Autonomous Full-Game Agent Charter (v1)

**Contract type:** Public runtime / phase charter (governance).  
**Scope:** **PX2-M00** and later **PX2-MNN** milestones — not v1 (**M00–M61**), not **PV1**, not **PX1** packaging.

---

## 1. Purpose

**PX2** exists because **PX1** closed the industrial-run, bounded remediation, and governed demo/video proof arc. The substrate and proof-pack story are **not** the same problem as building an agent that plays **full 1v1 games** with **autonomous** macro and micro under honest evaluation.

**PX2** is intentionally **separate** from **PX1**: extending **PX1** would blur packaging milestones with multi-milestone capability development and invite overclaim.

---

## 2. Phase identity

**PX2 — Autonomous Full-Game Skill Development**

---

## 3. Boundary from PX1

> **PX1 proved demo-proof packaging and bounded remediation; PX2 is the first phase aimed at autonomous full-game strength development.**

**PX1** established: industrial campaign execution evidence, play-quality and demo-readiness narratives, and governed demo proof pack **packaging** — **not** an open-ended program to maximize autonomous full-game strength.

**PX2** is the **first separate post-PX1 phase** aimed at **autonomous full-game strength development** (Terran-first; see below).

---

## 4. Target scope

| Dimension | Freeze (initial PX2 posture) |
| --- | --- |
| **Race** | **Terran only** — one full-race game surface first; not all races in parallel. |
| **Mode** | **1v1** StarCraft II, **full game** (see §5). |
| **Action surface** | **One** coherent full-race surface — not “every possible action head on day one,” but the milestone ladder must converge toward full-game coverage. |
| **Maps** | **Bounded** evaluation and training map pool — explicitly declared per milestone; **no** claim of universality in **PX2-M00**. |

---

## 5. Definition of “full-game”

**Full-game** means play that spans:

- Starting **economy** through **tech**, **production**, **combat**, and **cleanup** phases as they arise in a normal match.
- Legal progression including: worker production, supply, production structures, unit production, **scouting**, **expansions**, army movement, **attack / regroup / cleanup**, and reactive unit control.
- Run to a **terminal game outcome** or an **explicit governed failure** condition (timeout, forfeit rules, etc.) — as defined by the evaluation contract for that milestone.

**Not full-game:** a mid-game slice, a scripted combat loop, or a bounded demo scenario **alone** — those may be **building blocks**, but they do **not** satisfy “full-game strength” claims.

---

## 6. Action-surface target (intent)

Over **PX2-M01+**, the program targets coverage across (non-exhaustive): worker/economy, supply, structures and tech, unit production, scouting, expansion, attack/regroup/cleanup, and reactive unit control — implemented and governed incrementally.

---

## 7. Model-regime target (intent — not M00 claim)

The long-run PX2 direction includes a more expressive **learned** stack: memory / recurrent handling for partial observability, structured action heads, learned target selection and timing — **PX2-M00 does not claim any of this is implemented.**

---

## 8. Training regime target (intent)

Expected layers (later milestones):

1. **Replay bootstrap** — imitation / warm-start from governed replays.  
2. **Bounded self-play** — controlled opponent pool and anti-collapse posture.  
3. **Industrial self-play** — long campaigns with checkpointed progress.

**PX2-M00** charters expectations only — **no** training implementation.

---

## 9. Industrial campaign rules (future milestone discipline)

A **days-long Blackwell-class** industrial run is a **later** governed milestone — **not** part of **PX2-M00**. When executed, it must satisfy at least:

- Resumable **checkpoints**  
- Periodic automatic **eval**  
- Snapshot **retention**  
- **Promotion / rollback** rules  
- Opponent pool / **anti-collapse** posture  
- Explicit **artifact discipline** for weights, configs, evals, and operator notes  

Local **RTX 5090 Blackwell** is the **intended** operator-local campaign hardware — **not** default CI.

---

## 10. Promotion ladder (PX2-M01–PX2-M05)

| Milestone | Intent |
| --- | --- |
| **PX2-M01** | Full Terran **runtime / action-surface substrate** exists and is **governed**. |
| **PX2-M02** | First **replay-bootstrapped** learned **full-game** policy exists (bounded claims). |
| **PX2-M03** | **Industrial self-play campaign** runs on Blackwell with checkpoints and eval cadence. |
| **PX2-M04** | **Checkpoint promotion** and **exploit-closure** readout — what is actually stronger and where it fails. |
| **PX2-M05** | **Demo / proof refresh** only **after** a stronger full-game agent exists. |

---

## 11. Allowed scaffolding vs disallowed hand-authored gameplay patches

**For a promotable PX2 agent**, the **primary live-play decision loop** must **not** depend on hand-authored tactical patches for:

- Target-selection logic  
- Cleanup / search logic  
- Attack timing rules  
- Tactical special-case branches for common enemy states  

**Allowed scaffolding** (non-exhaustive): action **legality / masking**; **runtime safety** guards; **observation/state adapters**; rollout / eval / **checkpoint** infrastructure; **logging**, replay capture, artifact **packaging**; **fail-safe** boundaries clearly labeled as **safety infrastructure**, not gameplay intelligence.

---

## 12. Definition of “without our modifications”

“Without our modifications” means: **no reliance on disallowed tactical patching** (§11) in the primary policy loop. Scaffolding listed as **allowed** remains permissible if honestly disclosed.

---

## 13. Definition of “plays well” (promotable claim shape)

A **PX2** candidate **plays well** only if **all** hold:

- Finishes **full games** without operator intervention.  
- Uses economy, supply, production, scouting, expansion, and combat in a **recognizable full-game** way.  
- Achieves **replay-backed wins** under governed evaluation.  
- **Beats** at least the **current bounded PX1 demo-ready candidate** and selected **scripted/heuristic baselines** under the same governed evaluation contract — as frozen per milestone.  
- Satisfies **§11 / §12** (no disallowed tactical patching in the primary loop).

---

## 14. Explicit non-claims (PX2, especially PX2-M00)

PX2 — and **PX2-M00** in particular — **does not** claim:

- **Ladder** / public ranking proof  
- **Benchmark universality** across maps or opponents  
- **Multi-race** strength  
- **v2** platform opening (**v2** remains separately rechartered)  
- Automatic **Blackwell** execution or success  
- **Proof of strength** yet — **PX2-M00** is **charter and success-criteria freeze only**

---

## 15. Hardware posture

**Local RTX 5090 Blackwell** is the **intended** operator-local campaign hardware for later industrial milestones — **not** CI merge gates.

---

## Document control

- **Public source of truth:** `docs/starlab.md`  
- **Private working notes:** `docs/company_secrets/milestones/post-v1/PX2-MNN/` (not committed by default)
