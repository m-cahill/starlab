# STARLAB — Match execution harness (M02)

This document defines the **M02 proof surface**: a bounded, seeded, single-client **bot vs built-in AI** run under the M01 runtime boundary, producing a STARLAB-owned **execution proof artifact** (not the canonical run artifact from M05).

## Proof surface (exact)

| Dimension | M02 choice |
|-----------|------------|
| Clients | One local SC2 process (single-player create) |
| Opponents | Built-in AI (Computer player) |
| Control | Official SC2 API / `s2client-proto` (via adapter) |
| Interfaces | **Raw + score** only for the first slice; no rendered RGB; feature layers off unless later justified |
| Stepping | Bounded loop: `game_step=1`, default **100** iterations then clean exit |
| Seed | Fixed `random_seed` on game creation (recorded in proof) |
| Map | Explicit path in config **or** deterministic discovery of an offline `.SC2Map` under the install `Maps/` tree — not a hard dependency on ladder cache names |
| Evidence | `match_execution_proof` JSON + SHA-256 over normalized payload (excluding the hash field) |

## Adapter implementation path (M02)

**Implementation:** [BurnySc2](https://github.com/BurnySc2/python-sc2) (`burnysc2` on PyPI), isolated under `starlab/sc2/adapters/`.

**Canonical contract (unchanged from M01):** Blizzard SC2API / `s2client-proto`. The Python library is a convenience; quirks are **adapter behavior**, not a redefinition of STARLAB semantics.

STARLAB-owned surfaces (`MatchConfig`, `HarnessResult`, `ExecutionProofRecord`) remain **wrapper-agnostic**.

## Single-player proof flow

Aligned with the official protocol flow:

1. **Create game** — `RequestCreateGame` with local map, player setup (participant + computer), `random_seed`
2. **Join game** — participant joins with interface options (raw + score)
3. **Observe** — repeated observations each step
4. **Action** — optional; M02 may issue zero actions (idle bot) for stability
5. **Step** — advance simulation (`game_step` ticks per iteration)
6. **Quit / end** — leave cleanly after bounded horizon (resign/leave as implemented by the adapter)

Reference: [s2client-proto protocol.md](https://github.com/Blizzard/s2client-proto/blob/master/docs/protocol.md).

## Fixed-seed rule

The configured integer seed is passed to game creation and recorded in the proof artifact. STARLAB does not claim cross-version or cross-host seed reproducibility.

## Bounded-horizon rule

Default **100** harness iterations with **`game_step=1`** so each iteration advances the simulation by one game loop tick (within adapter semantics). The values are explicit in config and proof.

## Artifact normalization rules

Stable comparison uses a **normalized** proof record:

* Include: schema version, adapter id, runtime boundary label, seed, interface flags, step policy, status sequence, selected observation summaries, action counts, final status, optional replay metadata (saved flag, redacted path token, file hash if saved).
* **Exclude from hash input:** `artifact_hash` field itself.
* **Normalize away:** absolute machine paths → logical map keys relative to install `Maps/` when possible, else basename only; timestamps if any.
* **Do not** depend on raw replay bytes or absolute paths for determinism claims.

Local evidence compares **STARLAB artifact hashes**, not upstream raw bytes.

## Environment discovery

* Prefer `STARLAB_SC2_ROOT` / `STARLAB_SC2_BIN` / `STARLAB_SC2_MAPS_DIR` from `docs/runtime/environment_lock.md`.
* The BurnySc2 runtime resolves the install via `SC2PATH`; the harness sets `SC2PATH` from `STARLAB_SC2_ROOT` when present so installs are **probe-discovered**, not hardcoded.

## Local-only evidence procedure

1. Configure a map (explicit path recommended) and seed.
2. Run `python -m starlab.sc2.run_match --config ... --output-dir ...` twice with the same config.
3. Compare normalized `artifact_hash` fields in the two `match_execution_proof.json` files.
4. If hashes differ, stop and document why before claiming deterministic harness proof.

## Explicit non-claims

M02 does **not** prove:

* Replay parsing correctness or replay binding (M04+)
* Canonical run artifact v0 (M05)
* Benchmark validity or tournament integrity
* Cross-host or cross-install reproducibility
* That ladder or Battle.net cached maps are available

## CI posture

CI runs **fake adapter** tests only — no SC2 installation required.

## Evidence status in repo (M02)

GitHub **CI** on `main` validates the harness and fake path only (no SC2 in CI). **Operator-local** burny evidence may be recorded under `docs/company_secrets/milestones/M02/` (**gitignored**; not in a default clone): **two successful** same-config runs with **matching** normalized `artifact_hash` (see `M02_determinism_check.md` and `M02_execution_proof_redacted.json` when present). The ledger (see `docs/starlab.md` §10) records **controlled deterministic match execution** as **proved only in the narrow same-machine harness sense** evidenced there — **not** a cross-host, replay-binding, or benchmark claim. Explicit map paths in config are resolved to **absolute** paths before CreateGame (repo-relative paths require running the CLI from the repository root).

## Example config (shape)

```json
{
  "schema_version": "1",
  "adapter": "burnysc2",
  "seed": 42,
  "bounded_horizon": { "max_game_steps": 100, "game_step": 1 },
  "map": { "path": "docs/company_secrets/milestones/M02/_local_maps/MoveToBeacon.SC2Map" },
  "interface": {
    "raw_interface": true,
    "score_interface": true,
    "feature_layer_interface": false,
    "rendered_interface": false
  },
  "save_replay": false
}
```

Use `"adapter": "fake"` for CI-safe runs. Prefer a real `.SC2Map` **file** path you control (the example filename matches the pysc2 mini-game often placed under gitignored `M02/_local_maps/`) or `"discover_under_maps_dir": true` when `STARLAB_SC2_MAPS_DIR` (or `STARLAB_SC2_ROOT`) resolves to a `Maps/` tree that contains playable map files.
