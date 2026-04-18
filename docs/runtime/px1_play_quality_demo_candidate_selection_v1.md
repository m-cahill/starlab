# PX1-M02 — Play-quality evaluation & demo candidate selection (runtime contract v1)

**Contract id:** `starlab.px1_play_quality_protocol.v1` / `starlab.px1_play_quality_evidence.v1`  
**Ledger:** `docs/starlab.md` — **Post-PV1 (PX1)**  
**Scope:** This document is the **public** runtime contract for **PX1-M02**. It does **not** substitute for the frozen **`px1_play_quality_protocol.json`** artifact pair; the JSON is the machine-checkable freeze.

---

## 1. Purpose

**PX1-M02** answers:

> Does STARLAB have a **bounded, evidence-backed** candidate that plays well enough under **declared** conditions to justify a later **governed** demo attempt (**PX1-M03**)?

This milestone is **narrower** than “the system is generally strong” and **narrower** than “winning video proof already exists.”

Success classes **remain separated**:

| Class | Milestone |
| --- | --- |
| Full industrial run success | **PX1-M01** (closed) |
| Play-quality / demo-candidate selection | **PX1-M02** |
| Demo / proof pack / winning video | **PX1-M03** (not opened by PX1-M02) |

---

## 2. Frozen play-quality evaluation protocol (summary)

The **authoritative** numeric and structural freeze lives in **`px1_play_quality_protocol.json`** (and its report), emitted from validated input. At a high level, the default frozen parameters are:

| Parameter | Value |
| --- | ---: |
| `minimum_candidates_evaluated` | 1 |
| `preferred_candidates_evaluated` | 2+ when coherent artifacts exist |
| `minimum_distinct_opponent_profiles` | 2 |
| `minimum_matches_per_candidate_per_opponent_profile` | 5 |
| `minimum_total_live_matches_for_selected_candidate` | 10 |
| `minimum_selected_candidate_overall_win_rate` | 0.60 |
| `minimum_selected_candidate_win_count` | 6 |
| `minimum_replay_backed_wins_for_selected_candidate` | 2 |
| `minimum_watchable_wins_for_selected_candidate` | 1 |
| `minimum_evidence_completeness` | `complete` |
| `required_runtime_mode` | `local_live_sc2` |
| `allowed_continuity_invalidations` | 0 (within a declared evaluation series for a candidate/opponent profile) |
| `selection_rule` | Choose highest bounded evidence-backed candidate that satisfies the frozen protocol; if tie, prefer stronger declared demo-opponent performance, then stable deterministic tiebreak |

**Primary evidence surface:** governed **local live-play** runs (e.g. M44-style validation), **`required_runtime_mode` = `local_live_sc2`**.  
**Secondary support:** offline metrics (e.g. M42/M28-style) may be **supporting** context only — not decisive play-quality proof.

---

## 3. Candidate pool (separate from opponent profiles)

The **candidate pool** is taken from **PX1-M01** artifacts only — **no fabrication**.

- **Primary:** post-bootstrap **weighted refit** bundle when present and coherent (`optional_weighted_refit` / `rl_bootstrap_candidate_bundle.joblib` under the authoritative execution tree).
- **Optional second:** only if repo inspection finds another surface that is **both** coherent **and** honestly comparable under this protocol — **do not** force pre-refit M43 weights in merely to improve a comparison story.

**Plain truth:** If **one** coherent candidate is all PX1-M01 yields, the protocol and operator notes **state that plainly** — it is **not** a deficiency to hide.

---

## 4. Opponent profiles (separate from candidate pool)

Two **declared bounded** opponent profiles are required for the evaluation series:

- **Profile A — scripted-style:** bounded local harness configuration (frozen repo-relative match config JSON).
- **Profile B — heuristic-style:** second bounded local harness configuration (distinct frozen match config).

These labels are **methodological** names for two frozen **M02 burnysc2** harness profiles (e.g. distinct seeds / horizons). They are **not** claims about public ladder opponents, scripted baseline suite (M21), or heuristic baseline suite (M22) as **ladder-equivalent** opponents.

---

## 5. Selection rule (separate from pool and profiles)

Encoded in the protocol JSON: choose the **highest** bounded evidence-backed candidate that **satisfies** the frozen protocol; tie-break per the frozen `selection_rule` string.

---

## 6. What counts as a **candidate**

A **candidate** is a coherent **policy artifact** (e.g. M43 hierarchical sklearn bundle path) that can be loaded for **M44**-style local live-play under the campaign’s **execution identity**, with provenance traceable to **PX1-M01** outputs.

---

## 7. What counts as a **demo-worthy candidate** (for PX1-M02)

A candidate is **demo-worthy within PX1-M02** only if **all** of the following hold:

- It is evaluated under the **frozen** protocol artifact.
- It meets the **frozen** minima (matches per profile, totals, win rate, replay-backed and watchable wins, completeness, runtime mode, continuity invalidations).
- Evidence is recorded in **`px1_play_quality_evidence.json`** (and report) with **`selection.status` = `candidate-selected`**.

---

## 8. Evidence required

Minimum authoritative **conceptual** package (operator-local heavy files stay under **`out/`** by default):

- Frozen **`px1_play_quality_protocol.json`** + **`px1_play_quality_protocol_report.json`**
- **`px1_play_quality_evidence.json`** + **`px1_play_quality_evidence_report.json`**
- Replay-backed evaluation outputs for evaluated/selected candidates
- Watchable validation for at least one selected-candidate win **if** selected
- **`px1_play_quality_operator_note.md`**
- **`demo_candidate_selection_declaration.md`** (`candidate-selected` or `no-candidate-selected`)
- References to **PX1-M01** `campaign_id` / `execution_id` and candidate origins

---

## 9. How selection is declared

- **`demo_candidate_selection_declaration.md`** must say exactly **`candidate-selected`** or **`no-candidate-selected`**.
- If selected: name **`candidate_id`**, bounded reason, and evidence basis.
- If not: honest reason.

---

## 10. Explicit non-claims

- **Not** ladder/public strength, **not** benchmark integrity, **not** universal replay↔execution equivalence.
- **Not** automatic opening of **PX1-M03** or **v2**.
- **Not** reinterpretation of **PX1-M01** as play-quality or demo proof.

---

## 11. PX1-M03 does not open automatically

**PX1-M03** (governed demo proof pack / winning video) requires a **separate** governance decision. Closing **PX1-M02** with or without a selected candidate **does not** open **PX1-M03** or **v2**.

---

## 12. Emitters (repo)

- `python -m starlab.sc2.emit_px1_play_quality_protocol --input <protocol_input.json> --output-dir <dir>`
- `python -m starlab.sc2.emit_px1_play_quality_evidence --protocol <px1_play_quality_protocol.json> --evaluation-input <eval.json> --output-dir <dir>`
