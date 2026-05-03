# V15-M61 — Release-Lock / Showcase Video Proof-Pack (v1)

**Milestone:** `V15-M61`  
**Purpose:** Bind **V15-M60**’s `showcase_lock_recommended` / `bounded_showcase_evidence_package_only` route into a **deterministic release-lock proof pack** and a governed **showcase video capture manifest**. This is **demonstration evidence only** — not benchmark execution, not strength proof, not checkpoint promotion, not 72-hour authorization, not v2 recharter.

**Authority:** `docs/starlab-v1.5.md` §V15-M61.

---

## Contract IDs

| Artifact | `contract_id` |
| --- | --- |
| Proof pack | `starlab.v15.m61.release_lock_proof_pack.v1` |
| Proof pack report | `starlab.v15.m61.release_lock_proof_pack_report.v1` |
| Showcase video capture manifest | `starlab.v15.m61.showcase_video_capture_manifest.v1` |
| Profile (optional reference) | `starlab.v15.m61.release_lock_showcase_video_proof_pack_update.v1` |

---

## Profiles (`emit_v15_m61_release_lock_proof_pack`)

| Profile | Intent |
| --- | --- |
| `fixture_ci` | CI-safe: proof-pack **shape** + `capture_status` = `fixture_schema_only_no_video`; `release_lock_executed` = false; `release_lock_status` = `fixture_schema_only_release_lock_shape`. |
| `operator_preflight` | Validates `--m60-lock-decision-json` + capture manifest; emits proof pack with `release_lock_status` = `operator_preflight_validated_not_release_locked` (`release_lock_executed` false). |
| `operator_declared` | Operator-supplied manifest + validated M60 JSON; `release_lock_status` = `v1_5_bounded_showcase_evidence_locked`; `release_lock_executed` true when capture is operator-classified. |
| `operator_release_lock` | Same as `operator_declared` plus **dual guards:** `--allow-operator-local-execution` and `--authorize-v15-release-lock`. |

M60 validation (operator paths) requires:

- `decision_status` = `showcase_lock_recommended`
- `lock_decision.lock_scope` = `bounded_showcase_evidence_package_only`
- `lock_decision.next_route` = `route_to_v15_m61_release_lock_proof_pack_update`
- `lock_decision.next_route_status` = `recommended_not_executed`

---

## CLI — proof pack

```bash
python -m starlab.v15.emit_v15_m61_release_lock_proof_pack \
  --profile fixture_ci \
  --output-dir out/v15_m61_fixture_check
```

```bash
python -m starlab.v15.emit_v15_m61_release_lock_proof_pack \
  --profile operator_declared \
  --m60-lock-decision-json path/to/v15_m60_showcase_evidence_lock_decision.json \
  --showcase-video-capture-manifest-json path/to/v15_m61_showcase_video_capture_manifest.json \
  --output-dir out/v15_m61_release_lock
```

```bash
python -m starlab.v15.emit_v15_m61_release_lock_proof_pack \
  --profile operator_release_lock \
  --allow-operator-local-execution \
  --authorize-v15-release-lock \
  --m60-lock-decision-json path/to/v15_m60_showcase_evidence_lock_decision.json \
  --showcase-video-capture-manifest-json path/to/v15_m61_showcase_video_capture_manifest.json \
  --output-dir out/v15_m61_release_lock
```

---

## CLI — capture manifest helper

Hashes local video/replay files and writes `v15_m61_showcase_video_capture_manifest.json`.

```bash
python -m starlab.v15.emit_v15_m61_showcase_video_capture_manifest \
  --video-file path/to/showcase.mp4 \
  --replay-file path/to/showcase.SC2Replay \
  --capture-method replay_playback_screen_recording \
  --playback-speed 0.5x \
  --session-source existing_m57a_replay \
  --output-dir out/v15_m61/showcase_video
```

Fixture / schema-only (no files):

```bash
python -m starlab.v15.emit_v15_m61_showcase_video_capture_manifest \
  --fixture-only \
  --output-dir out/v15_m61/showcase_video_fixture
```

**Allowed `session_source` values (operator):** `existing_m57a_replay`, `existing_m58_adapter_smoke_replay`, `new_m61_showcase_capture`, `V15-M57A/V15-M58/M52A-derived-or-new-M61-capture`.

Any new live session for sales/demo capture is classified as **`showcase_video_capture_only`**, not benchmark or training.

---

## Showcase video capture manifest (schema sketch)

- `capture_status`: `fixture_schema_only_no_video` | `operator_video_captured`
- `video_file` / `replay_file`: `storage_posture` = `operator_local_not_committed`; `relative_or_redacted_path` (no absolute paths, no `docs/company_secrets`); `sha256` (64-hex)
- `sc2_context`: map, opponent/baseline, `session_source`, `playback_speed`, `slow_watchability_mode`
- `non_claims`: benchmark/strength/promotion/ladder/human-panel/v2 tokens

**Overclaim refusal:** any manifest subtree with `benchmark_passed`, `strength_evaluated`, `checkpoint_promoted`, or `v2_authorized` (etc.) set **true** is rejected (CLI exit `2`).

---

## Release-lock proof pack (schema sketch)

- `upstream_m60`: closed decision summary bound to M60 vocabulary
- `release_lock`: `release_lock_status`, `release_lock_scope` = `bounded_showcase_evidence_package_only`, `proof_pack_updated`, `showcase_video_manifest_bound`
- `candidate`: canonical program candidate SHA; `promotion_status` = `not_promoted_candidate_only`
- `evidence_chain`: M53–M60 closure class tokens (fixture summary)
- `showcase_video`: manifest-derived hash fields + pacing metadata
- `claim_flags`: all benchmark/strength/promotion/72h/v2 flags **false** except narrowly scoped `release_lock_executed` when appropriate
- `non_claims`: explicit M61 denials + “demonstration evidence only” for video

---

## Storage policy

- **Commit:** JSON/MD proof-pack artifacts from emitters in `out/` only as **local** dev/CI outputs; do **not** commit `out/` to Git.
- **Do not commit:** raw `.mp4`, `.SC2Replay` blobs, checkpoints, or private `docs/company_secrets/**` paths in public metadata.

---

## Relationship to M60

M60 **`recommended_not_executed`** routes here. M61 **executes** the bounded release-lock / proof-pack **surface** and optional operator video binding; it does **not** re-open benchmark or strength charters.

---

## V15-M62+ routing

Next private/public planning is a **decision fork only** — e.g. **V15-M62 — 72-Hour Charter vs v2 Recharter Decision**. It is **not** “first 12-hour run,” not automatic 72-hour execution, and not automatic v2 authorization.
