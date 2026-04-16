# Ladder / public evaluation protocol & evidence surface v1 (M59)

**Status:** M59 product contract (**closed** on `main` — [PR #70](https://github.com/m-cahill/starlab/pull/70); merge commit `319bc3d496b78c573c57991cd0fcc461219da6a4`; tag **`v0.0.59-m59`**). **Not** ladder performance proof. **Not** benchmark integrity. **Not** replay↔execution equivalence.

## Purpose

Define a **bounded, deterministic, audit-friendly** way to describe and package **descriptive** public- or ladder-shaped evaluation evidence for **exactly one** governed candidate per emitted artifact family.

M59 answers:

> How does STARLAB **describe** and **package** public/ladder evaluation evidence for a governed candidate in a deterministic, reviewable way?

M59 does **not** answer:

> Is STARLAB now proven strong on ladder or public matchmaking performance?

## Bounded scope

- **One candidate subject** per protocol and per evidence artifact.
- **JSON-first ingestion** only: structured inputs and operator-provided rows. **No** OCR, screenshot parsing, scraping, or hosted service integrations.
- **Fixture-only CI**: tests use synthetic JSON; **no** live public ladder runs, submissions, or merge-gate live SC2.
- **Descriptive evidence only**: counts and explicit gaps. **No** statistical significance, rating certification, benchmark-integrity claims, or replay↔execution equivalence claims.
- **Small and reversible**: protocol and emitters; not an operations or automation milestone.

## Product artifacts

| Artifact | Contract id |
| -------- | ----------- |
| `ladder_public_evaluation_protocol.json` | `starlab.ladder_public_evaluation_protocol.v1` |
| `ladder_public_evaluation_protocol_report.json` | (report schema `starlab.ladder_public_evaluation_protocol_report.v1`) |
| `ladder_public_evaluation_evidence.json` | `starlab.ladder_public_evaluation_evidence.v1` |
| `ladder_public_evaluation_evidence_report.json` | (report schema `starlab.ladder_public_evaluation_evidence_report.v1`) |

**Bounded protocol profile (M59 v1):** `starlab.m59.protocol_profile.single_candidate_public_eval_v1`

### CLI

```bash
python -m starlab.sc2.emit_ladder_public_evaluation_protocol --input <protocol.json> --output-dir <dir>
python -m starlab.sc2.emit_ladder_public_evaluation_evidence --protocol <dir>/ladder_public_evaluation_protocol.json --result-rows <rows.json> --output-dir <dir>
```

Inputs are **file-based** and deterministic; prefer one JSON file for protocol fields and one for `evidence_session_id` + `result_rows`.

## Allowed evidence classes

| Class | Meaning |
| ----- | ------- |
| `replay_bound_result` | Row tied to replay/provenance material when hash or explicit absence is recorded. |
| `result_row_only` | Descriptive result without replay binding (weaker). |
| `operator_attested_result` | Operator-provided (weaker; labeled explicitly in warnings). |

**Not in M59:** screenshot/OCR/scraping classes.

## Evaluation surface kind

- `ladder_public`
- `public_match_set`

Rows must use `venue_surface_kind` equal to the protocol’s `evaluation_surface_kind`.

## Required fields (protocol input)

The protocol emitter validates at least:

- `protocol_profile_id` (must be the bounded profile above in M59 v1)
- `protocol_version`
- `subject_candidate.candidate_id` (non-empty)
- `evaluation_surface_kind`
- `venue_descriptor` (object)
- `accepted_evidence_classes` (non-empty subset of allowed classes)
- `aggregation_rules` (object; descriptive policy only)

Optional: `candidate_lineage` (array of shallow provenance records — **string fields only**, no cross-import of M44/M57/M58 model types).

Default `required_non_claims` and `explicit_out_of_scope` blocks are merged with any user-provided lines.

## Result rows (evidence input)

Each row includes:

- `stable_match_id` (unique)
- `observed_at`
- `venue_surface_kind` (must match protocol)
- `opponent_label`
- `map_name` (optional; absence is surfaced as a coverage gap)
- `match_result`: `win` | `loss` | `draw` | `unknown`
- `evidence_class` (must be allowed by protocol)
- `subject_candidate_id` (must match protocol subject)
- Optional: `replay_reference_hash`, `source_reference`
- Optional: `absence_flags` (sorted strings; e.g. `replay_missing`, `outcome_unavailable_in_source`)

For `replay_bound_result`, either `replay_reference_hash` is present or `absence_flags` contains `replay_missing`; otherwise a **replay linkage** gap is recorded.

## Deterministic ordering

- Protocol JSON: canonical sorted keys (`canonical_json_dumps`).
- Result rows: sorted by `(stable_match_id, observed_at, opponent_label, map_name, evidence_class, source_reference, replay_reference_hash)` after normalization.

## Aggregation rules (descriptive only)

Allowed summary fields include:

- Totals for wins / losses / draws / unknown
- Total rows observed
- Counts by evidence class
- Map coverage: rows with known vs unknown map name
- Per-map result counts when `map_name` is present

**Not allowed in M59:** significance, confidence intervals as proof, “outperforms ladder field,” benchmark-integrity language, replay↔execution equivalence language, merge-bar or release-bar claims.

Descriptive ladder/MMR-like numbers may appear only as **optional passthrough** in future extensions; M59 v1 focuses on counts above.

## Evidence posture

`evidence_posture_status` is one of:

- `bounded_complete` — no absence flags, no map/replay linkage gaps for the stated rules.
- `bounded_incomplete` — explicit gaps (e.g. unknown map, incomplete replay binding, or non-empty `absence_flags`).
- `invalid` — reserved for malformed bundles; normal validation failures raise errors instead of emitting.

## Explicit non-claims

M59 artifacts and this runtime doc preserve:

- **No** substitution for **M52–M54** (replay↔execution equivalence) or **M55–M56** (benchmark integrity).
- **No** claim that **M57–M58** live-SC2-in-CI guardrails prove ladder or public evaluation.
- **No** automated ladder submission, public ladder scraper, OCR/screenshot parsing, or hosted dashboard.
- **No** default merge-gate live SC2 expansion.
- **No** new candidate classes beyond existing governed candidate surfaces.

## Relationship to M44 / M57 / M58 provenance

Lineage entries may cite paths, contract ids, profile ids, SHAs, and run ids as **opaque strings**. M59 does **not** validate M44/M57/M58 artifacts or import their Python types.

## Relationship to M52–M56 non-substitution boundaries

M59 is a **separate** descriptive packaging layer. It does **not** satisfy equivalence audits (M53–M54), benchmark-integrity charter or gates (M55–M56), or live-SC2 charter/guardrails (M57–M58) for ladder claims.

---

**Emitter modules:** `starlab.sc2.emit_ladder_public_evaluation_protocol`, `starlab.sc2.emit_ladder_public_evaluation_evidence`  
**Models:** `starlab.sc2.ladder_public_evaluation_models`, `starlab.sc2.ladder_public_evaluation_protocol`, `starlab.sc2.ladder_public_evaluation_evidence`
