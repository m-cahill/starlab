# Public flagship proof pack (v1)

## Purpose

The **public flagship proof pack** is a **bounded evidence index**: one directory tree that regenerates from repository code and governed fixtures, assembling the strongest **already-proved** STARLAB surfaces (**M25** baseline evidence pack, **M28** learned-agent evaluation, **M31** replay explorer) under explicit **non-claims**.

It is **not** a benchmark engine, **not** a product UI, and **not** a substitute for benchmark-integrity or live-runtime proof.

## Artifact layout

Under the pack root (default `out/flagship/` from `make flagship`):

| Relative path | Role |
| --- | --- |
| `public_flagship_proof_pack.json` | Pack manifest: version, `proof_pack_sha256`, included artifacts (paths + hashes), `source_provenance`, `non_claims`, contract references |
| `public_flagship_proof_pack_report.json` | Short report: subordinate surface versions, roles |
| `hashes.json` | SHA-256 of **generated pack outputs only** (eight JSON files); keys are paths relative to the pack root |
| `baseline/baseline_evidence_pack.json` | M25 |
| `baseline/baseline_evidence_pack_report.json` | M25 report |
| `learned/learned_agent_evaluation.json` | M28 |
| `learned/learned_agent_evaluation_report.json` | M28 report |
| `explorer/replay_explorer_surface.json` | M31 |
| `explorer/replay_explorer_surface_report.json` | M31 report |

## Regeneration

```bash
python -m starlab.flagship.emit_public_flagship_proof_pack --output-dir out/flagship
# or
make flagship
```

CI runs the same emission via **`flagship`** job (`make flagship`) and uploads the **`flagship-proof-pack`** artifact.

## M25 segment (determinism)

The M25 baseline evidence pack is emitted **in-process** via `write_baseline_evidence_pack_artifacts` from the **governed Phase-IV fixture graph** (M21/M22 suite JSON, M23 tournament, M24 diagnostics) checked in under `tests/fixtures/`. This matches the golden path in `tests/test_baseline_evidence_pack.py` and avoids unstable hashes from cwd-relative `suite_path` fields that a fresh M20–M24 chain would embed when intermediate directories differ.

## Provenance vs hashes

- **`hashes.json`** hashes **outputs only** (clean public hash contract).
- **`source_provenance`** inside `public_flagship_proof_pack.json` records repo-relative fixture paths and SHA-256 of key governed inputs (including bundle manifests where applicable).

## Non-claims

See `PUBLIC_FLAGSHIP_PROOF_PACK_NON_CLAIMS_V1` in `starlab/flagship/models.py` and the `non_claims` field in the emitted pack. Typical standing exclusions: benchmark integrity, live SC2 in CI, replay↔execution equivalence, new training tracks, Phase VI (**M40**/**M41**), operating manual v1, hosted UI as milestone scope.

## Related contracts

- `docs/runtime/baseline_evidence_pack_v1.md` (M25)
- `docs/runtime/learned_agent_evaluation_harness_v1.md` (M28)
- `docs/runtime/replay_explorer_surface_v1.md` (M31)
- `docs/flagship_proof_pack.md` (narrative)
