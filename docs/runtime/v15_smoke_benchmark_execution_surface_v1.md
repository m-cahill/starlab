# V15-M36 — Smoke benchmark execution surface (v1)

**Contract:** `starlab.v15.smoke_benchmark_execution.v1`  
**Profile:** `starlab.v15.m36.smoke_benchmark_execution_surface.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m36_smoke_benchmark_execution`

**Required phrase:** **V15-M36 is not a 2-hour run, not T2/T3, not a benchmark pass, not strength evaluation, and not checkpoint promotion.**

---

## Purpose

**V15-M36** is the first governed **smoke benchmark execution bookkeeping** surface downstream of sealed **[M35](v15_candidate_checkpoint_smoke_benchmark_readiness_v1.md)** readiness. It emits honest **execution/refusal** artifacts (**SHA-sealed**) that bind **`m35_readiness`** by **`artifact_sha256`** only (**no checkpoint blob I/O**, **no** **`torch.load`**, **no** live SC2 on this milestone path).

M36 **`benchmark_execution_performed`** stays **`false`** on all emitted profiles to prevent benchmark-result overclaiming. **`smoke_execution_performed`** may be **`true`** only for **`operator_local_bounded_smoke`**, meaning **deterministic synthetic bounded smoke bookkeeping** over validated M35 JSON — **not** gameplay scoring.

---

## Modes

### Fixture CI (`--fixture-ci`)

CI-safe wiring; **no** M35 file required.

```powershell
python -m starlab.v15.emit_v15_m36_smoke_benchmark_execution `
  --fixture-ci `
  --output-dir out/v15_m36_fixture
```

- **`execution_status`:** **`fixture_schema_only_no_candidate_execution`**
- **`smoke_execution_performed`:** **`false`**
- **`benchmark_execution_performed`:** **`false`** (always in M36)

### Operator preflight (`--profile operator_preflight`)

Validates sealed **M35** **`v15_candidate_checkpoint_smoke_benchmark_readiness.json`**.

```powershell
python -m starlab.v15.emit_v15_m36_smoke_benchmark_execution `
  --profile operator_preflight `
  --m35-readiness-json <path-to-sealed-v15_candidate_checkpoint_smoke_benchmark_readiness.json> `
  --expected-candidate-sha256 eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26 `
  --output-dir out/v15_m36_operator_preflight
```

- **`--expected-candidate-sha256`** optional; when omitted, must match M35 **`candidate_checkpoint.sha256`**.
- Success path: **`execution_status`:** **`smoke_benchmark_execution_ready_but_not_run`** — **no** synthetic smoke step.

### Operator local bounded smoke (`--profile operator_local_bounded_smoke`)

**Dual guards** + sealed M35 + optional expected SHA. **Synthetic** receipt only.

```powershell
python -m starlab.v15.emit_v15_m36_smoke_benchmark_execution `
  --profile operator_local_bounded_smoke `
  --allow-operator-local-execution `
  --authorize-smoke-benchmark-execution `
  --m35-readiness-json <path-to-sealed-v15_candidate_checkpoint_smoke_benchmark_readiness.json> `
  --expected-candidate-sha256 eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26 `
  --max-smoke-steps 1 `
  --output-dir out/v15_m36_operator_bounded_smoke
```

- **`execution_status`:** **`smoke_benchmark_execution_completed`** — interprets **synthetic bounded bookkeeping completed**, **not** benchmark pass.
- **`smoke_execution_performed`:** **`true`**; **`benchmark_execution_performed`:** **`false`**.

---

## Inputs

| Input | Requirement |
| --- | --- |
| Sealed **M35** JSON | Readable path via **`--m35-readiness-json`** |
| **`contract_id`** | **`starlab.v15.candidate_checkpoint_smoke_benchmark_readiness.v1`** |
| **`profile_id`** | **`starlab.v15.m35.candidate_checkpoint_smoke_benchmark_readiness.v1`** |
| **`readiness_status`** | **`smoke_benchmark_ready_for_future_execution`** for success-path preflight/smoke |
| Candidate SHA | **`expected-candidate-sha256`** must match **`candidate_checkpoint.sha256`** when provided |
| M35 **`claim_flags` / smoke requirements** | Must remain refusal posture (**no benchmark / strength / promotion** flags) |

Paths under **`out/`** from operator workflows are **not** hardcoded; pass explicit **`--m35-readiness-json`**.

---

## Execution statuses

| Status | Meaning |
| --- | --- |
| **`fixture_schema_only_no_candidate_execution`** | Merge CI fixture — no execution |
| **`smoke_benchmark_execution_blocked_missing_m35_readiness`** | No/readable M35 |
| **`smoke_benchmark_execution_blocked_invalid_m35_readiness`** | Seal/contract/profile/claims invalid |
| **`smoke_benchmark_execution_blocked_candidate_not_ready`** | **`readiness_status`** ≠ **`smoke_benchmark_ready_for_future_execution`** |
| **`smoke_benchmark_execution_blocked_candidate_sha_mismatch`** | Expected vs M35 SHA mismatch |
| **`smoke_benchmark_execution_ready_but_not_run`** | M35 passes gates; bookkeeping only |
| **`smoke_benchmark_execution_completed`** | Bounded **synthetic** smoke receipt only |

---

## Gate pack (X0–X6)

| Gate | Name | Pass intuition |
| --- | --- | --- |
| **X0** | M35 readiness contract valid | Seal + **M35** **contract/profile** |
| **X1** | Candidate SHA consistent | Matches expected / M35 |
| **X2** | Readiness posture supports smoke route | **`readiness_status`** ready when required |
| **X3** | Smoke execution bounded | Fixture/refusal/no-run or **≤ 1** synthetic step |
| **X4** | No strength/promotion claims | **`claim_flags`** honest |
| **X5** | Public/private boundary | No private path patterns in emissions |
| **X6** | Non-claims present | **`non_claims`** retained |

---

## Artifacts

- `v15_smoke_benchmark_execution.json` (sealed)
- `v15_smoke_benchmark_execution_report.json`
- `v15_smoke_benchmark_execution_checklist.md`

---

## Relationship to **M35**

**[M35](v15_candidate_checkpoint_smoke_benchmark_readiness_v1.md)** proves **routing readiness**. **M36** consumes that artifact by **SHA** and emits **execution/refusal bookkeeping** — **still not** a benchmark **pass**.

---

## Relationship to future **2-hour** / long-run work

**M36** **does not** run the **operator 2-hour** wall-clock posture, **`run_v29`**, **`long_gpu_campaign`**, or **T2**/**T3** tiers. Downstream charters remain separate.

---

## Public / private boundary

Emissions use path **redaction** patterns consistent with earlier V15 surfaces. **Do not** embed **`docs/company_secrets`**, unchecked **`out/`** literals, or private operator notes in emitted JSON/checklists.

---

## Non-claims

**M36** **does not** claim benchmark **pass**, benchmark **scorecard results**, strength evaluation, checkpoint **promotion**, **2-hour** run completion, live SC2 tournament outcome, XAI inference, human-panel execution, showcase release, **v2**, **T2**/**T3**, or **`benchmark_execution_performed`** (remains **`false`** in M36 receipts).

See **`docs/starlab-v1.5.md`** — **M36 non-claims block**.

---

## Ledger

Governance telemetry (**PR**, **CI**, merge SHAs): **`docs/starlab-v1.5.md`** — **§V15-M36** (authoritative).
