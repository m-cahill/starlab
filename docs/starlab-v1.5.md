# STARLAB v1.5 — Authoritative Public Governance (V15)

**Program phase:** v1.5 (milestone namespace **V15**)  
**Status:** Active program line — **V15-M00** is **closed** on `main` ([PR #116](https://github.com/m-cahill/starlab/pull/116); merge `1391518eb4a4a7e90b5b1b81074d070e2957c8a3`). **Authoritative PR-head CI** [`24911939851`](https://github.com/m-cahill/starlab/actions/runs/24911939851) (head `aeabdb9274aea43e660dedf4d2090db0b6e24237`); **merge-boundary `main` CI** [`24913025515`](https://github.com/m-cahill/starlab/actions/runs/24913025515) on merge commit `1391518e…` — **success**. M00 **does not** claim a completed long GPU run, strong agent, human benchmark, or XAI demo. **V15-M01** is **closed** on `main` ([PR #117](https://github.com/m-cahill/starlab/pull/117); merge `f618a1f90d44e02879501ea067a079c760c20e6c`). **Authoritative PR-head CI** [`24914804421`](https://github.com/m-cahill/starlab/actions/runs/24914804421) (head `8d4caf6cbc5c03e8e42e4aea62de6210b0947ae8`); **merge-boundary `main` CI** [`24916076997`](https://github.com/m-cahill/starlab/actions/runs/24916076997) on merge commit `f618a1f…` — **success**. M01 **does not** execute training or approve claim-critical assets; **M01 non-claims** below remain in force after closure. **V15-M02** is **closed** on `main` ([PR #118](https://github.com/m-cahill/starlab/pull/118); merge `3f7e226ff0402cbb91b831e7c9397080cc8a77aa` merged **2026-04-25T00:53:35Z** UTC). **Authoritative PR-head CI** [`24918006750`](https://github.com/m-cahill/starlab/actions/runs/24918006750) (head `4aab910eb01f50f03e866630c34a3c91d772ad13`); **merge-boundary `main` CI** [`24918563270`](https://github.com/m-cahill/starlab/actions/runs/24918563270) on merge commit `3f7e226f…` — **success**. M02 **does not** execute GPU training, **does not** run GPU shakedown, and **does not** green-light a long run or operator-local RTX 5090 readiness from fixture-only output — **M02 non-claims** below apply after closure. **V15-M03** — *Checkpoint Lineage and Resume Discipline* — is **not** started (no implementation on `main`; **do not** begin until **explicit** plan approval).

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

---

## 5. V15 milestone table (plan)

| Milestone | Title |
| --- | --- |
| **V15-M00** | Training Readiness Charter and Long GPU Run Gate — **closed** on `main` (PR #116) |
| **V15-M01** | Training-Scale Provenance and Asset Registers — **closed** on `main` (PR #117) |
| **V15-M02** | Long GPU Run Environment Lock — **closed** on `main` (PR #118) |
| **V15-M03** | Checkpoint Lineage and Resume Discipline — **not** started (await **explicit** plan approval) |
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

### V15 asset and register map (compact)

Navigation aid — authoritative field lists and vocabulary live in `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and emitted `v15_training_asset_registers.json`.

| Surface / register | Public doc | Private / local counterpart (typical) | Strongest allowed claim (until populated & reviewed) | Next dependent milestone |
| --- | --- | --- | --- | --- |
| `starlab.v15.training_readiness_charter.v1` | `docs/runtime/v15_training_readiness_charter_v1.md` | Local charter JSON emit only | `readiness_only` (gates defined, not satisfied) | **V15-M01+** |
| Training asset register | `docs/training_asset_register.md` | Dataset manifests under `out/` / `docs/company_secrets/` (not raw commits) | `readiness_only` | **V15-M02** (environment lock) / later data gates |
| Replay corpus register | `docs/replay_corpus_register.md` | Raw replays local; rights notes private | `readiness_only` | **V15-M02** / gate **C** |
| Model weight register | `docs/model_weight_register.md` | Weight blobs local / external archive | `readiness_only` | **V15-M07**+ training shakedown |
| Checkpoint register | `docs/checkpoint_asset_register.md` | Checkpoint files local / external archive | `readiness_only` | **V15-M03** lineage |
| Human benchmark register | `docs/human_benchmark_register.md` | Human-panel records private by default | `readiness_only` | **V15-M06** protocol |
| XAI evidence register | `docs/xai_evidence_register.md` | Operator-local packs until contract freeze | `readiness_only` | **V15-M04** contract |
| Rights register | `docs/rights_register.md` | Supplemental rights under `docs/company_secrets/` | `readiness_only` | Ongoing |

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

---

## 6. Artifact family contract ids (governed names)

These are the **intended** v1.5 contract identifiers (emission implemented per milestone; M00 defines names and charter JSON).

- `starlab.v15.training_readiness_charter.v1` (**M00**)
- `starlab.v15.training_asset_registers.v1` (**M01** — register contract / vocabulary only)
- `starlab.v15.long_gpu_environment_lock.v1` (**M02** — environment-lock contract; fixture and optional operator probe)
- `starlab.v15.long_gpu_training_manifest.v1`
- `starlab.v15.checkpoint_lineage_manifest.v1`
- `starlab.v15.training_run_receipt.v1`
- `starlab.v15.strong_agent_scorecard.v1`
- `starlab.v15.xai_evidence_pack.v1`
- `starlab.v15.human_panel_benchmark.v1`
- `starlab.v15.showcase_agent_release_pack.v1`

**M00 emitter:** `python -m starlab.v15.emit_v15_training_readiness_charter --output-dir <path>` writes `v15_training_readiness_charter.json` and `v15_training_readiness_charter_report.json`.

**M01 emitter:** `python -m starlab.v15.emit_v15_training_asset_registers --output-dir <path>` writes `v15_training_asset_registers.json` and `v15_training_asset_registers_report.json`.

**M01 runtime narrative:** `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md`  
**M01 public registers:** `docs/training_asset_register.md`, `docs/replay_corpus_register.md`, `docs/model_weight_register.md`, `docs/checkpoint_asset_register.md`, `docs/human_benchmark_register.md`, `docs/xai_evidence_register.md` (plus `docs/rights_register.md` V15 subsection).

**M02 emitter:** `python -m starlab.v15.emit_v15_long_gpu_environment_lock --output-dir <path>` writes `v15_long_gpu_environment_lock.json` and `v15_long_gpu_environment_lock_report.json` (default profile **`fixture_ci`**; optional `--profile operator_local` and `--probe-json <path>`).

**M02 runtime narrative:** `docs/runtime/v15_long_gpu_run_environment_lock_v1.md`

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

## 11. CI security note (M00–M02, temporary)

The default merge CI runs **`pip-audit`** with a **single** narrow ignore: **`--ignore-vuln CVE-2026-3219`** for the **`pip` toolchain**. **M01 re-check (2026-04-24, CI-like env):** after `pip install --upgrade pip`, **`pip` 26.0.1** still reported **CVE-2026-3219** to **`pip-audit`**. **M02 re-check (2026-04-25, CI-like local env):** same — **`pip` 26.0.1** still reports the CVE; **no** audit-clean **`pip`** upgrade path observed. **Leave** the narrow ignore in place; do **not** broaden exceptions. This is **not** `continue-on-error`. **CycloneDX SBOM** generation, **SBOM upload**, **Gitleaks**, and the aggregate **governance** job still run. **Remove** the ignore when a fixed, audit-clean **`pip`** is published on PyPI.

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
