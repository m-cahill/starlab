# Replay and data provenance

## Purpose

Replay files, maps, ladder-derived data, screenshots, and derived labels have **independent rights risk** from source code. This policy defines interim rules until a fuller corpus program exists (refine with replay intake milestones, e.g. M07+).

**Blizzard materials:** Official SC2 API resources reference Linux packages, map packs, and replay packs; access may require agreement to Blizzard’s **AI and Machine Learning License** and other applicable terms. STARLAB does **not** commit those assets to the repository; acquire locally under the governing terms and record posture in `docs/rights_register.md`.

## Allowed sources (interim)

- **First-party**: Replays and data you create yourself on terms you control.
- **Blizzard / StarCraft II ecosystem**: Use only under applicable game EULA, map terms, and redistribution rules. Do not assume redistribution rights for third-party maps or ladder assets.
- **Third-party replay packs**: Allowed only with explicit license terms permitting your use (research, storage, redistribution as applicable). If terms are unclear, do not import into a canonical corpus.

## Local storage

- Local copies of replays and maps are allowed for **research and evaluation** on machines you control.
- Store paths and hashes in lineage metadata when STARLAB defines artifact formats; until then, keep informal notes sufficient for audit.

## Redistribution

- **Do not** redistribute replays, maps, or ladder dumps unless license terms explicitly permit it.
- **May** redistribute **metadata only** (hashes, player IDs if permitted, build orders extracted as factual summaries) when rights allow; when in doubt, metadata-only or no publication.

## Reference by metadata / hash

Preferred pattern for uncertain rights:

- Record **hash**, **source**, **date acquired**, and **license status** in `docs/rights_register.md` or successor registry.
- Point to assets by reference, not bulk re-hosting.

## Provenance recording

For each asset class, record:

| Field | Notes |
|-------|--------|
| Source | URL, pack name, or “first-party” |
| License / terms | Citation or “unknown” |
| Redistribution | yes / no / unknown |
| Location | local path pattern or “not stored” |

## Quarantine for uncertain rights

If provenance or redistribution rights are **unclear**, the asset:

- is **not** promoted into a canonical STARLAB corpus or public benchmark set;
- may live in a **quarantine** area (local-only, clearly labeled) until resolved.

**Minimum rule:** *If provenance or redistribution rights are unclear, the asset is not promoted into a canonical corpus.*

## Third-party replay packs, maps, ladder data, screenshots, derived labels

| Asset type | Default rule |
|------------|----------------|
| Replay packs | License must permit use; otherwise quarantine |
| Maps | Map author / EULA terms; often no redistribution |
| Ladder data | Usually ToS-restricted; metadata-only unless explicitly allowed |
| Screenshots | Blizzard/content policy; avoid bulk redistribution |
| Derived labels | Provenance follows parent replay; no cleaner rights than source |

## M01 / M02+ follow-up (conditionally)

Tighten ingestion paths, hash formats, and registry fields once replay intake policy (M07) and binding pipelines exist. M01 documents environment lock and runtime boundary only — not ingestion automation.

## Canonical corpus promotion (ledger rule)

No replay, map, ladder-derived asset, or derived label is promoted into a **canonical** STARLAB corpus without explicit provenance status and redistribution posture recorded (see `docs/starlab.md` §9).
