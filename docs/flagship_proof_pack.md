# STARLAB public flagship proof pack

## What this is

The **public flagship proof pack** (**M39**) is a **single, reproducible bundle** that answers one diligence question:

> Can an outsider see **governed evaluation evidence**, **learned-agent evaluation**, and **hierarchical / explorer evidence surfaces** in one place, with **explicit boundaries** on what STARLAB does **not** claim?

It is an **evidence index**—emphasizing regeneration, provenance, bounded claims, and non-claims—not demo theater or a “we solved RTS AI” narrative.

## Why these artifacts

| Surface | Milestone | Why it is in the pack |
| --- | --- | --- |
| Baseline evidence pack | M25 | Governed tournament/diagnostics packaging over baseline suites |
| Learned-agent evaluation | M28 | Fixture-only benchmark + imitation baseline + bundles |
| Replay explorer surface | M31 | Operator-facing bounded panels over M14 bundles + M30 agent |

**M33** CI field-test readiness proved fixture-only explorer emission; **M39** layers a **flagship** job that builds the **full** pack and uploads **`flagship-proof-pack`**.

## How to regenerate

```bash
make flagship
# writes to out/flagship/ (gitignored locally; CI uploads artifact)
```

Equivalent:

```bash
python -m starlab.flagship.emit_public_flagship_proof_pack --output-dir out/flagship
```

## What is proved (narrowly)

- STARLAB can **assemble** those three governed JSON families into one **deterministic** manifest with **output hashes** and **source provenance** metadata.
- The same command works in **CI** (`flagship` job) on authoritative PR / `main` runs.

## What is **not** proved

The pack does **not** establish: benchmark integrity, leaderboard validity in a live sense, live SC2 in CI, replay↔execution equivalence, new training results, or Phase VI expansion decisions. Agent training tracks remain **out of scope** until **M38**/**M39** are closed per program discipline.

## Public boundary

The pack is suitable for **external legibility** alongside `docs/public_private_boundary.md` and `LICENSE`; it does not expose crown-jewel operator internals.

## Canonical contract

See `docs/runtime/public_flagship_proof_pack_v1.md` and the emitted `public_flagship_proof_pack.json`.
