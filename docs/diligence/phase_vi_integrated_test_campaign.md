# Phase VI integrated test campaign (post‑M45 follow‑on)

**M45** is **closed** on `main` (see `docs/starlab.md` §11 / §18). This note remains **preparation and framing** for the **next** follow-on: it does **not** assert that a full integrated Phase VI test campaign has been executed or that additional claims beyond closed milestones are proved.

## Intent

After **M45** closes on `main`, the next natural follow‑on is a **deliberate, cross‑surface integrated test campaign** that exercises the Phase VI stack end‑to‑end in a **local, operator‑controlled** setting:

- **M40** training program contract
- **M41** flat training artifacts
- **M42** comparison artifacts
- **M43** hierarchical training artifacts
- **M44** local live‑play validation artifacts
- **M45** bootstrap artifacts

**M46 (bounded live semantics):** For **bounded** `local_live_sc2` / **burnysc2** runs that hit the configured step cap (`bounded_exit` in the execution proof), treat **`match_execution.final_status == "ok"`** as **validation-contract success** (aligned with the fixture path). The literal SC2 client **`Result`** is preserved separately as **`sc2_game_result`** — **not** a ladder or “won the game” claim. Authoritative: `docs/runtime/local_live_play_validation_harness_v1.md`.

## Boundary

CI remains **fixture‑only** for SC2 and live play. Any **live SC2** or long‑running runs belong **outside** default CI, on operator machines, with results captured as **local artifacts** under the governed layouts (`out/…` roots, not committed weights).

## Out of scope for this document

This file does **not** define benchmark integrity, statistical guarantees, or product‑level RL performance. Those remain governed by `docs/starlab.md` and the relevant runtime contracts.
