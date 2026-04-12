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

## Boundary

CI remains **fixture‑only** for SC2 and live play. Any **live SC2** or long‑running runs belong **outside** default CI, on operator machines, with results captured as **local artifacts** under the governed layouts (`out/…` roots, not committed weights).

## Out of scope for this document

This file does **not** define benchmark integrity, statistical guarantees, or product‑level RL performance. Those remain governed by `docs/starlab.md` and the relevant runtime contracts.
