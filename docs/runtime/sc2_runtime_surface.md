# SC2 runtime surface — decision record (M01)

**Status:** Canonical for STARLAB as of M01 closeout.  
**Open decision:** OD-005 — **resolved** here; `docs/starlab.md` §12 summarizes.

## Purpose

STARLAB treats the StarCraft II client and tooling as an **untrusted boundary** (see `docs/starlab.md`). This document records an **evidence-backed** choice of which upstream surfaces define STARLAB’s **canonical contract** versus **optional adapters** versus **deferred** layers, so later milestones (notably M02) do not reopen foundational boundary decisions without explicit governance.

## Candidate set evaluated

| Candidate | Role |
|-----------|------|
| Official SC2 API / `s2client-proto` | Protocol definitions and documentation for communicating with the SC2 client (WebSocket + protobuf). |
| `s2protocol` | Blizzard reference **replay protocol** decoder (Python); low-level decode of replay blobs. |
| `python-sc2` | Community Python client for the **scripted** bot interface; builds on the official API. |
| PySC2 | DeepMind RL-oriented Linux environment; feature layers and research ergonomics, not the official protocol contract. |

**Sources (authority):** Blizzard publishes `s2client-proto` and `s2protocol`; `python-sc2` and PySC2 are third-party with their own READMEs and licenses.

## Evaluation criteria

| Criterion | Meaning |
|-----------|---------|
| **Upstream authority** | Whether the surface is owned/documented by Blizzard vs community-only. |
| **Interface coverage** | Control, observation, replay, and API breadth for lab use. |
| **Replay relevance** | Suitability as the **replay decode** contract (not full analytics). |
| **Headless / Linux posture** | Fit for automated and server-style use where applicable. |
| **Contract stability** | How stable the boundary is for versioning and audit. |
| **Python ergonomics** | Ease of use in this repo’s primary language (secondary to authority). |
| **Auditability** | Ability to explain and review what the lab depends on. |
| **Lockability** | Ability to pin versions, paths, and environment without hidden magic. |

## Candidate matrix (qualitative)

Scores: **H** high, **M** medium, **L** low, **N** not applicable / poor fit for that row’s intent.

| Candidate | Authority | Interface coverage | Replay relevance | Headless/Linux | Stability | Python ergonomics | Auditability | Lockability |
|-----------|-----------|-------------------|------------------|----------------|-----------|---------------------|--------------|-------------|
| `s2client-proto` / SC2API | H | H (control + observation + replay hooks per protocol) | M (replay via client/API; not a file decoder by itself) | H (Linux build documented in Blizzard materials) | H | L–M (proto-level) | H | H |
| `s2protocol` | H | N for live control | **H** (decode reference) | H | M | M | H | H |
| `python-sc2` | L (community) | M–H for scripted API | L (not the replay decode reference) | M | M | **H** | M | M |
| PySC2 | L (research stack) | H for RL env | M (not canonical decode layer) | H (Linux-focused) | M | H | M | M |

## Final decision

| Layer | Canonical STARLAB choice | Notes |
|-------|-------------------------|--------|
| **Control / observation** | **Blizzard official SC2 API** using **`s2client-proto`** (SC2API protocol) | Canonical lab boundary for driving the client and reading structured game state. |
| **Replay file decode** | **`s2protocol`** | Canonical **replay decode** reference surface (low-level; “first tool in the chain,” not full replay analytics). |
| **Optional Python adapter** | **`python-sc2`** | **Allowed** behind a STARLAB adapter boundary only; does **not** define the public substrate contract. |
| **RL / feature-layer environment** | **PySC2** (or equivalent) | **Deferred** as a non-canonical research environment; not the M01 substrate contract. |

### Canonical (normative for STARLAB)

- **SC2API + `s2client-proto`** as the **canonical control/observation** contract.
- **`s2protocol`** as the **canonical replay protocol decode** contract for `.SC2Replay` blobs.

### Allowed but non-canonical

- **`python-sc2`** (and similar wrappers) for developer ergonomics, **provided** they are isolated behind explicit adapter modules and do not replace the official protocol as the lab’s contract.
- Future internal facades that **wrap** protobuf or file paths without claiming to be upstream.

**BurnySc2 (optional harness):** the STARLAB M02 config may set optional **`computer_difficulty`** (default **`Easy`**) to select python-sc2 **`sc2.data.Difficulty`** values (`VeryEasy` … `Hard` in the supported allowlist) for the built-in computer opponent. This controls **local operator pressure** for bounded validation; it is **not** a performance or benchmark claim.

Optional **`opponent_mode`** (default **`computer`**) may select a **`passive_bot`** second player instead of the built-in AI for **watchability-only** operator smokes. That bot does **not** issue attacks; the adapter may apply **light non-combat** economic heartbeats. This does **not** assert ladder or benchmark strength.

Optional **`burnysc2_suppress_attack`** (default **`false`**, **`px1_m03_hybrid_v1` only**) disables marine **attack-move** in the hybrid Terran policy for **operator-local** watchability/sandbox smokes. It is **not** a performance, ladder, or benchmark claim. Setting **`burnysc2_suppress_attack`** with other policies (including **`px1_watchability_macro_scout_v1`**) is invalid — reject at config validation.

Optional **`burnysc2_policy`** value **`px1_watchability_macro_scout_v1`** selects a **scripted** Terran bot intended only for **operator-local visual validation**: macro, scouting, and **non-combat** patrol-style movement near the base — **no** attack orders by design. It does **not** use runtime M43 inference in the bot. It is **not** benchmark evidence, not ladder performance, and not a strong-agent claim.

### Deferred

- **PySC2**-style RL environments as the **default** substrate (may be revisited for specific experiments under milestone governance).
- Full replay **analysis** pipeline (metadata, timelines, economy) — later milestones.
- **M02** will add deterministic **match execution** proof; M01 does not claim it.

## Assumed vs owned guarantees

| Class | Statement |
|-------|-----------|
| **Assumed** | Blizzard clients, builds, and tools behave as described in Blizzard’s documentation and licenses; versions and OS paths may change outside STARLAB’s control. |
| **Owned** | STARLAB’s written contract (this document + `docs/starlab.md`), environment lock docs, probe output shape, tests that enforce doc alignment, and governance of what the repo claims. |

## Community wrappers and canonical contract

**Community wrappers (including `python-sc2`) do not become STARLAB’s canonical contract.**  
The canonical boundary remains the **official Blizzard protocol and reference decoders** (`s2client-proto`, `s2protocol`). Wrappers are implementation conveniences; any divergence is a bug against the official surface, not a redefinition of STARLAB semantics.

## References (external)

- Blizzard `s2client-proto`: protocol definitions and docs (e.g. protocol overview).  
- Blizzard `s2protocol`: replay protocol decode.  
- `python-sc2`: scripted API client (community).  
- PySC2: RL-oriented environment (research).

## M01 non-claims

- M01 does **not** prove controlled match execution, replay parsing correctness end-to-end, or benchmark validity.  
- Dependency **packages** for `s2protocol` / runtime wiring are intentionally **not** added in M01; see `docs/runtime/environment_lock.md` and M02.
