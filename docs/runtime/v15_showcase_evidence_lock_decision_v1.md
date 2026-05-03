# V15 Showcase Evidence Lock Decision v1 (`V15-M60`)

**STARLAB phase:** v1.5 (`V15`)  
**Purpose:** Consume the closed **V15-M53 → V15-M59** public evidence chain and emit a deterministic **bounded showcase-evidence lock vs continue/remediate** decision. No benchmark execution; no strength claim; no checkpoint promotion; no 72-hour charter; no v2 recharter authorization.

---

## Contract IDs

| Artifact | Contract / schema identifier |
| --- | --- |
| Decision JSON | `starlab.v15.m60.showcase_evidence_lock_decision.v1` |
| Report JSON | `starlab.v15.m60.showcase_evidence_lock_decision_report.v1` |
| Decision profile label | `starlab.v15.m60.showcase_evidence_lock_vs_continue_remediate.v1` |

Emitted basenames (default):

- `v15_m60_showcase_evidence_lock_decision.json`
- `v15_m60_showcase_evidence_lock_decision_report.json`

---

## Profiles

| Profile | Behaviour |
| --- | --- |
| `fixture_ci` | Canonical closed-chain metadata (**M53/M54/candidate SHA** anchors + structural closure posture for **M55–M59**). Emits **`showcase_lock_recommended`** with **`bounded_showcase_evidence_package_only`** when all internal gates pass. |
| `operator_preflight` | Requires **`--m59-readout-json`** pointing at a **`V15-M59`** readout JSON validating benchmark-as-evidence refusal. On success emits the **same deterministic lock recommendation** as `fixture_ci` and records **`validated_m59_readout_canonical_sha256`** in the report. Invalid **M59 → exit code 2** (no emitted artifacts guaranteed). |
| `operator_declared` | Requires **`--operator-declaration-json`** matching exactly `{"m53_m59_public_closure_acknowledged": true}`. Validates no forbidden private-boundary leakage in string values (e.g. `company_secrets`). On failure **exit code 2**. |

---

## Decision vocabulary (`decision_status`)

- `showcase_lock_recommended` — Bounded showcase-evidence / proof-pack lock is recommended (still **no** benchmark/strength/etc. authorization).
- `showcase_lock_deferred` — Reserved for deterministic deferral (**fixture_ci** selects **recommended** branch when gates pass).
- `continue_remediate_recommended` — Internal remediation routing when gates fail (test / future operator inputs).

---

## Lock class (`lock_class`)

Used with `fixture_ci` success:

- `bounded_showcase_evidence_lock`

On gate failure (**continue/remediate**):

- `no_lock_missing_required_evidence`

Reserved:

- `no_lock_due_to_overclaim_risk`

---

## Evidence chain (consumption posture)

Minimum categories reasoned inside **M60** (no milestone re-exec):

| Category | Typical source | M60 stance |
| --- | --- | --- |
| 12-hour training execution | **V15-M53** | Training artifact + candidate checkpoint SHA anchors |
| Package / readiness | **V15-M54** | Package SHA anchor; readiness routing posture |
| Evaluation package preflight | **V15-M55** | Closed + structural preflight posture |
| Readout-only | **V15-M56** | Closed + bounded-readout posture |
| Visual/watchability | **V15-M56A** or **V15-M57A** | Observation-only closure |
| Governed charter / dry-run | **V15-M57** | Charter posture only |
| Adapter smoke execution | **V15-M58** | Bounded adapter smoke |
| Benchmark overclaim refusal | **V15-M59** | Refusal upheld (extra validation in **`operator_preflight`**) |

**M55–M59:** closure + contract/evidence-class metadata in the decision artifact; **M60 does not recurse into every upstream JSON SHA unless an operator chooses to validate **M59** explicitly.

---

## Lock scope (`lock_scope`)

If **`showcase_lock_recommended`:**

```text
bounded_showcase_evidence_package_only
```

Not:

```text
benchmark_passed_release
strength_proven_release
checkpoint_promoted_release
v2_release
72_hour_authorization
```

---

## Non-claims (standing)

Emitted in **`non_claims`** on each path; **`claim_flags`** keep benchmark/strength/promotion/72h/v2/`release_lock_executed` **false** on the **`fixture_ci` lock-recommended posture.

---

## Next routing

On **`fixture_ci`** lock recommendation:

```text
next_milestone = V15-M61
next_route = route_to_v15_m61_release_lock_proof_pack_update
next_route_status = recommended_not_executed
```

**M61** is **documentation / proof-pack / release-lock update only** — not benchmark execution inside **M60** or automatically here.

Remediation route (gates failed):

```text
next_route = route_to_v15_m60_remediation_followup
```

Defer / **M62+** vocabulary exists for ledger consistency only (**not executed inside M60**).

---

## CLI

Fixture (CI-safe):

```bash
python -m starlab.v15.emit_v15_m60_showcase_evidence_lock_decision \
  --profile fixture_ci \
  --output-dir out/v15_m60
```

Operator preflight (**M59** validation):

```bash
python -m starlab.v15.emit_v15_m60_showcase_evidence_lock_decision \
  --profile operator_preflight \
  --m59-readout-json path/to/v15_m59_adapter_smoke_readout.json \
  --output-dir out/v15_m60_operator_preflight
```

Operator declared acknowledgement:

```bash
python -m starlab.v15.emit_v15_m60_showcase_evidence_lock_decision \
  --profile operator_declared \
  --operator-declaration-json path/to/ack.json \
  --output-dir out/v15_m60_operator_declared
```

Do **not** commit raw outputs under **`out/`** or files under **`docs/company_secrets/`**.

---

## Public / private boundary

- Canonical **M53/M54/candidate SHA** anchors are **public ledger facts**.
- **`operator_preflight`** and **`operator_declared`** are for **operator-local** validation workflows; refusal exits **must not** silently weaken CI truthfulness.

---

## Strongest allowed M60 posture (`fixture_ci`)

Proceed to **`V15-M61`** **release-lock / proof-pack update** for v1.5 as a **bounded showcase-evidence package**, without claiming benchmark pass/fail, strength, promotion, ladder/public performance proof, human-panel success, **72-hour authorization**, or **v2 authorization**.
