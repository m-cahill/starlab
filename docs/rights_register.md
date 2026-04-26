# Rights register

Living inventory of major surfaces: ownership, terms, redistribution, and risk. Update when assets or dependencies materially change.

### V15-M01 — training-scale registers (v1.5)

**V15-M01** adds **public, template-only** asset registers (`docs/training_asset_register.md`, `docs/replay_corpus_register.md`, `docs/model_weight_register.md`, `docs/checkpoint_asset_register.md`, `docs/human_benchmark_register.md`, `docs/xai_evidence_register.md`) plus the runtime contract **`docs/runtime/v15_training_scale_provenance_asset_registers_v1.md`** and emitted JSON **`starlab.v15.training_asset_registers.v1`**. They define **required fields and vocabulary** for future rows; **M01 does not** register raw weights, bulk replays, checkpoints, or human identities in public docs. **Private** supplements (paths, participant details, uncleared corpora) stay under **local** **`docs/company_secrets/`** (gitignored) or operator **`out/`** — **not** committed and **not** in a default clone. Row-level **`rights_posture`** / **`redistribution_posture`** in those registers must stay consistent with this file.

### V15-M08 — long GPU campaign (v1.5)

**V15-M08** (implementation surface **closed** on `main`, [PR #133](https://github.com/m-cahill/starlab/pull/133); **`implementation_ready_waiting_for_operator_run`**) may bind training manifests, dataset references, and operator-local campaign trees under `out/v15_m08_campaigns/` when an operator runs the guarded path. **Default:** long-campaign corpora, weights, logs, and uncleared paths remain **private** / **local_only**; `docs/company_secrets/**` stays **gitignored**. Public governance references **`docs/runtime/v15_long_gpu_campaign_execution_v1.md`** and **`docs/starlab-v1.5.md`** (M08 non-claims block) — **not** automatic rights clearance for redistribution.

### V15-M09 — checkpoint evaluation / promotion (v1.5)

**V15-M09** is **closed** on `main` ([PR #135](https://github.com/m-cahill/starlab/pull/135)); defines `starlab.v15.checkpoint_evaluation.v1` and `starlab.v15.checkpoint_promotion_decision.v1` with **`docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`**. Emissions use **SHA-only** JSON bindings for dataset/rights/descriptor inputs; they do **not** import uncleared media into the repo. Public-rights posture is **unchanged** by M09; **no** new public register rows are implied.

### V15-M10 — replay-native XAI demonstration (v1.5)

**V15-M10** is **closed** on `main` ([PR #136](https://github.com/m-cahill/starlab/pull/136)); adds **`docs/runtime/v15_replay_native_xai_demonstration_v1.md`** and `starlab.v15.replay_native_xai_demonstration.v1` — governance JSON + deterministic Markdown; **not** a commitment to public redistribution of **raw** replays, **videos**, **saliency** tensors, or **uncleared** XAI media. Explanations and overlay references remain subject to the same public/private and Blizzard/TOS rules as other SC2 and replay materials. **V15-M11** not started; rights/public-private posture is otherwise **unchanged** except for the governed M10 surface and honest non-claims in **`docs/starlab-v1.5.md`**.

### V15-M02 — environment references (v1.5)

**V15-M02** adds the environment-lock contract **`starlab.v15.long_gpu_environment_lock.v1`** and runtime **`docs/runtime/v15_long_gpu_run_environment_lock_v1.md`** (merged **2026-04-25** per **`docs/starlab-v1.5.md`**). **SC2 client paths**, **map pool / on-disk map locations**, **GPU driver or machine-identifying details**, and other **operator-local environment facts** are **private by default** unless intentionally **sanitized** for public reference. Public surfaces should use **logical references** (map id, pool id, version strings) — not raw paths. The emitter **redacts** absolute path strings in operator `--probe-json` output; do not treat that as rights clearance for redistribution. Milestone **closure** does not relax default **private** posture for operator paths or media.

| Asset / surface | Type | Source | Owner | License / terms | Redistribution allowed? | Commercial use allowed? | Public / private | Notes / risk | Status |
|-----------------|------|--------|-------|-----------------|-------------------------|-------------------------|------------------|--------------|--------|
| Repository code | code | First-party | Michael Cahill | `LICENSE` (source-available, eval/verification) | No (per `LICENSE`) | No (per `LICENSE`) | Public repo | Evaluation-only clone/run | Initial |
| Repository docs | docs | First-party | Michael Cahill | Same as code unless noted | Same as code | Same as code | Public | — | Initial |
| SC2 client / game dependency surface | dependency | Blizzard | Blizzard | EULA; Blizzard AI & ML license applies to API/maps/replay pack materials where Blizzard requires it | N/A (don’t redistribute client) | Per EULA / applicable Blizzard terms | Public discussion only; binaries acquired locally | Untrusted boundary; see `docs/starlab.md`, `docs/runtime/sc2_runtime_surface.md` | Governed (M01) |
| SC2 Linux packages / map packs / replay packs (official) | dependency / media | Blizzard | Blizzard | Per Blizzard distribution terms (incl. AI & ML license where referenced) | No bulk redistribution via STARLAB | Research use per terms | Not committed to repo | Acquire under applicable terms; paths only in env/provenance metadata | Governed (M01) |
| Replay assets | replay | Various / TBD | Various | Varies; often restricted | Unknown unless explicit | Unknown unless explicit | Default private / quarantine | High diligence risk if unclear; quarantine until provenance clear | Open |
| Map assets | map | Various / TBD | Various | Map-specific + EULA | Often no | Often no | Default private | Not committed; local paths via `STARLAB_SC2_*` | Open |
| Python dev dependencies | dependency | PyPI | Upstream authors | Per-package (see lock/pip list in CI) | Per license | Per license | Declared in SBOM/CI | Track in CI (pip-audit) | Initial |
| Future generated artifacts | artifact | STARLAB tooling | Michael Cahill | TBD at generation | TBD | TBD | TBD | Define in milestone | Deferred |
| Future model weights | model | TBD | TBD | TBD | TBD | TBD | Private default | — | Deferred |

**OD-006 resolution:** This file is the canonical rights register format; `docs/starlab.md` may summarize but defers detail here.
