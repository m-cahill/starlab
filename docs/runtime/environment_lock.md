# Environment lock — SC2 runtime (M01)

**Purpose:** Define how STARLAB **pins intent** for local development and future execution work without committing licensed game assets. This is a **governance and detection** contract; it is **not** proof that matches run correctly.

## Canonical local dev host posture (M01 / M02)

- **OS:** Linux is the **reference** posture for headless/automation alignment with Blizzard’s Linux SC2 packages and documented API workflows.  
- **Windows:** Supported for **local development** when developers use a **live Battle.net** StarCraft II install (see below). Paths and builds differ; the **probe** reports what is configured, not what is “best.”
- **macOS:** Not the primary lock target for M01/M02; treat as best-effort until explicitly governed.

## Python version posture

- **Python 3.11.x** only, as pinned in `pyproject.toml` (`requires-python = ">=3.11,<3.12"`).  
- CI runs on **3.11**; local dev should match CI for governance checks.

## Package / dependency posture (M01)

- **No SC2-related Python packages** are required in M01 (`pyproject.toml` remains free of `s2protocol`, `python-sc2`, PySC2, etc.).  
- **M02** is intended to introduce **optional** runtime dependencies and wiring (e.g. `s2protocol` for decode experiments, clients/adapters) under explicit milestone scope.  
- M01’s **probe** is **path/config detection only** — no Blizzard binaries shipped, no PyPI SC2 stack in CI.

## Environment variables and path conventions

The following variables are read by `starlab.sc2.env_probe` (see precedence in code and below). All are **optional**; unset variables mean “unknown / default derivation.”

| Variable | Meaning |
|----------|---------|
| `STARLAB_SC2_ROOT` | Root of the SC2 installation (e.g. Linux package root, or Windows root containing `Versions/`). |
| `STARLAB_SC2_BIN` | Explicit path to the SC2 **binary** (e.g. `SC2_x64.exe`, `SC2` on Linux). Overrides derivation from `STARLAB_SC2_ROOT`. |
| `STARLAB_SC2_MAPS_DIR` | Directory containing maps for tooling (maps not committed to repo). |
| `STARLAB_SC2_REPLAYS_DIR` | Directory for local replay storage (replays not committed). |
| `STARLAB_SC2_BASE_BUILD` | Optional string for build / base version reporting (e.g. for lineage). |
| `STARLAB_SC2_DATA_VERSION` | Optional string for data version / bundle identity when known. |

**Precedence (summary):**

- **`STARLAB_SC2_BIN`:** If set, used as the canonical binary path for detection; **else** derive from `STARLAB_SC2_ROOT` using common layout hints (platform-specific).  
- **`STARLAB_SC2_MAPS_DIR` / `STARLAB_SC2_REPLAYS_DIR`:** If set, used as-is (normalized); **else** optional derivation from `STARLAB_SC2_ROOT` (e.g. `Maps` subfolder).  
- **Build / data version:** `STARLAB_SC2_BASE_BUILD` and `STARLAB_SC2_DATA_VERSION` override empty defaults when present.

Paths are normalized for **stable output** (absolute, resolved where possible, POSIX-style strings in JSON for cross-platform consistency).

## Live Battle.net client (Windows) — local installation posture

Many developers install StarCraft II via the **Battle.net** client. That layout is **valid local posture** for development:

- Install is **not** committed to the repo.  
- Typical paths include versioned directories under the game root (e.g. `Versions\` on Windows).  
- Configure `STARLAB_SC2_ROOT` and/or `STARLAB_SC2_BIN` to point at the **local** install so the probe reports presence without embedding secrets.

**Distinction (required):**

| Concept | M01 | M02+ |
|--------|-----|------|
| **Live client present** on disk | Yes — can be **detected** via paths | Still assumed only where configured |
| **Governed execution proof** (deterministic harness, controlled match) | **Not claimed** | In scope for M02 |

## Asset acquisition (no repo commits)

- **Binaries, maps, replay packs:** Acquire under **Blizzard’s applicable terms** (including AI/ML license terms where referenced for API/maps/replay packs). Store **only on local or CI-controlled paths** configured via env vars.  
- **Do not** commit SC2 binaries, maps, or replay packs to STARLAB.  
- **Hashes and metadata** may be recorded in lineage artifacts in later milestones; M01 only records lock **intent** and probe **detection**.

## What CI does and does not validate

**CI validates:**

- Repository governance: lint, typecheck, tests, SBOM, secret scanning (see `.github/workflows/ci.yml`).  
- That the **probe** runs deterministically in fixture-based tests **without** SC2 installed.

**CI does not validate:**

- Presence of a real SC2 installation.  
- Correctness of Blizzard builds, maps, or replay content.  
- Network, Battle.net, or license acceptance flows.

## Local-only optional evidence

Developers with a local SC2 install may run:

```bash
python -m starlab.sc2.env_probe --json
```

Use **`--redact`** when pasting output into milestone artifacts (user-specific path segments).

## Environment lock is not execution proof

Locking paths, env vars, and Python version **reduces ambiguity** and supports **auditability**. It does **not** by itself prove:

- that matches start reliably in all target configurations;  
- that replay decode is correct on all replay versions;  
- that benchmarks are fair or stable.

Those are **M02+** concerns. M01 explicitly documents the boundary and provides **typed probe output** only.
