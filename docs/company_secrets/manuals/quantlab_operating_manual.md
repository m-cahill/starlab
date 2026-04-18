# QuantLab Operating Manual

**Version:** 1.10.0
**Status:** Canonical
**Authority:** This document is the primary operating reference for QuantLab.

---

## 1. Executive Identity

QuantLab is a deterministic, governed research engine that compiles declarative financial modeling intent into content-addressable artifacts. It produces strategy evaluation bundles that downstream trading systems consume.

### What QuantLab Is

- A compiler front-end that transforms `IntentConfig` into governed, reproducible `StrategyArtifactBundle` artifacts
- A deterministic research pipeline: intent → compilation → validation → simulation → evaluation → registration
- A governed artifact producer with content-addressable hashing, replay guarantees, and drift detection
- A dependency for external trading systems via `quantlab.public`

### What QuantLab Is Not

- Not a trading engine (no order routing, no position management, no live execution)
- Not a backtesting framework (walk-forward validation is a compiler primitive, not a backtest system)
- Not an AutoML wrapper (no automatic model selection or hyperparameter tuning)
- Not a data vendor platform (no data provisioning; data is adapter-driven)
- Not an ML framework (no training implementation; execution is adapter-driven)
- Not a cloud platform (no infrastructure, deployment, or orchestration)
- Not a feature store or model registry

### Target User

External trading systems (e.g. `quantlab-trader`) that need governed research artifacts. All imports must come from `quantlab.public`.

---

## 2. Core Mental Model

### Unit of Work

The unit of work is a **contract** (`IntentConfig`), not code. Every pipeline execution begins with a declarative specification of modeling intent and produces deterministic, immutable artifacts.

### System Flow

```
IntentConfig
  → normalize_intent()     → ModelingIntent         [contract]
  → build_feature_graph()  → FeatureGraph           [graph IR]
  → build_feature_pipeline() → FeaturePipeline      [pipeline IR]
  → build_training_harness() → TrainingHarness      [harness IR]
  → WalkForwardEngine.run() → WalkForwardResult     [validation]
  → ExecutionSimulator      → ExecutionRecord[]      [simulation]
  → evaluate_promotion()    → PromotionDecision      [evaluation]
  → build_strategy_report() → StrategyEvaluationReport [reporting]
  → build_strategy_bundle() → StrategyArtifactBundle [artifact]
  → StrategyRegistry        → StrategyRegistryEntry  [catalog]
  → ExperimentTracker       → ExperimentRecord       [tracking]
```

### Determinism-First Philosophy

Every transformation in the pipeline produces identical output for identical input. There is no randomness, no system time, no hidden state. All artifacts are content-addressable via SHA256 of canonical JSON (sorted keys, no whitespace variation, UTF-8).

### Governance-First Philosophy

Every artifact is:
- **Immutable** — frozen dataclasses or Pydantic models
- **Hashable** — deterministic content hash
- **Snapshot-enforced** — CI fails on drift
- **Replayable** — identical inputs produce identical hashes

No silent failures. No muted CI gates. No governance bypass.

### Canonical Compiler Spine (Authoritative)

The QuantLab system is defined by the following invariant pipeline:

IntentConfig
→ ModelingIntent
→ FeatureGraph
→ FeaturePipeline
→ TrainingHarness
→ WalkForwardResult
→ ExecutionRecord[]
→ PromotionDecision
→ StrategyEvaluationReport
→ StrategyArtifactBundle
→ StrategyRegistryEntry
→ ExperimentRecord

This pipeline is:

- deterministic
- immutable
- replayable
- audit-enforced

Any deviation from this pipeline is invalid.

---

## 3. System Architecture

### Layer Definitions

#### 3.1 Contracts (`quantlab/contracts/`)

- **Responsibility:** Define the canonical modeling contract
- **Key types:** `ModelingIntent`, `SCHEMA_VERSION`
- **Boundary:** Input must be valid; output is versioned, immutable, snapshot-enforced
- **Invariant:** Schema changes require snapshot update and version bump

#### 3.2 DSL (`quantlab/dsl/`)

- **Responsibility:** User-facing input normalization
- **Key types:** `IntentConfig`, `normalize_intent()`
- **Boundary:** Accepts unvalidated user input; produces canonical `ModelingIntent`
- **Invariant:** Same `IntentConfig` always produces same `ModelingIntent` (features sorted, deduplicated; whitespace stripped)

#### 3.3 Graph (`quantlab/graph/`)

- **Responsibility:** Feature dependency graph assembly
- **Key types:** `FeatureNode`, `FeatureGraph`, `build_feature_graph()`
- **Boundary:** Consumes `ModelingIntent`; produces deterministic structural IR
- **Invariant:** Execution-free; no side effects; sorted canonical output

#### 3.4 Pipeline (`quantlab/pipeline/`)

- **Responsibility:** Feature computation stage assembly
- **Key types:** `PipelineStage`, `FeaturePipeline`, `build_feature_pipeline()`
- **Boundary:** Consumes `FeatureGraph`; produces deterministic structural IR
- **Invariant:** Execution-free; no side effects; sorted canonical output

#### 3.5 Training (`quantlab/training/`)

- **Responsibility:** Model training harness assembly
- **Key types:** `ModelSpec`, `TrainingHarness`, `build_training_harness()`
- **Boundary:** Consumes `FeaturePipeline` and `ModelingIntent`; produces structural IR
- **Invariant:** Execution-free; no side effects; sorted canonical output

#### 3.6 Runtime (`quantlab/runtime/`)

- **Responsibility:** Execution boundary — validation, simulation, evaluation, bundling, registration, tracking
- **Boundary:** Adapter-driven execution; isolated from IR layers
- **Invariant:** All execution happens here; IR layers remain execution-free

##### 3.6.1 Walk-Forward Validation

- **Key types:** `ExecutionAdapter` (Protocol), `WalkForwardEngine`, `WalkForwardResult`
- **Behavior:** Expanding-window walk-forward with deterministic synthetic data
- **Output:** `WalkForwardResult` with `artifact_hash` (SHA256 of canonical JSON)

##### 3.6.2 Trading Simulation (`quantlab/runtime/trading/`)

- **Key types:** `SimConfig`, `DecisionTrace`, `ExecutionRecord`, `PnLSeries`, `PnLAttribution`
- **Simulator:** `ExecutionSimulator` — spread, slippage, latency, fill probability models
- **Invariant:** Pure, replayable, seed-free; no RNG, no system time

##### 3.6.3 Promotion Gates (`quantlab/runtime/trading/evaluation/`)

- **Key types:** `PromotionDecision`, `evaluate_promotion()`
- **Gates:** expectancy, drawdown, stability, trace completeness
- **Rule:** `passed = all(gates pass)`; failed strategies rank last

##### 3.6.4 Reporting (`quantlab/runtime/trading/reporting/`)

- **Key types:** `StrategyEvaluationReport`, `build_strategy_report()`
- **Output:** Human-reviewable report with metrics, attribution, trace diagnostics

##### 3.6.5 Bundling (`quantlab/runtime/trading/bundle/`)

- **Key types:** `StrategyArtifactBundle`, `build_strategy_bundle()`
- **Output:** Portable research artifact with `bundle_hash` (self-hash pattern)
- **Contract:** Bundle is the artifact that downstream systems consume

##### 3.6.6 Registry (`quantlab/runtime/trading/registry/`)

- **Key types:** `StrategyRegistry`, `StrategyRegistryEntry`
- **Operations:** `register_bundle()`, `list_strategies()`, `top_strategies()`, `compare_strategies()`
- **Ranking:** `rank_score = expectancy - |max_drawdown| * 0.5 - stability_variance * 0.25`; failed strategies get `-inf`

##### 3.6.7 Experiments (`quantlab/runtime/trading/experiments/`)

- **Key types:** `ExperimentTracker`, `ExperimentRecord`
- **Operations:** `register_experiment()`, `list_experiments()`, `best_experiment()`
- **ID derivation:** `experiment_id = deterministic_hash(intent_hash + bundle_hash + canonical_json(metadata))`

##### 3.6.8 Research Runner (`quantlab/runtime/research/`)

- **Key types:** `ResearchRunner`, `ResearchRunResult`
- **Operations:** `run_intent()`, `run_many()`, `best_strategy()`
- **Pipeline:** Orchestrates full lifecycle from `IntentConfig` to registered `StrategyArtifactBundle`

### Layer Boundaries (Strict)

| Layer | Execution | Mutation | Dependencies |
|-------|-----------|----------|--------------|
| contracts/ | None | Immutable | None |
| dsl/ | None | Immutable | contracts/ |
| graph/ | None | Immutable | contracts/ |
| pipeline/ | None | Immutable | graph/ |
| training/ | None | Immutable | pipeline/, contracts/ |
| runtime/ | Adapter-driven | Immutable outputs | All above |

IR layers (contracts, dsl, graph, pipeline, training) are **execution-free, deterministic, immutable, and snapshot-enforced**.

All execution is isolated in `runtime/` via the `ExecutionAdapter` protocol.

---

## 4. System Contracts (Invariants)

### 4.1 Determinism

- **Definition:** Same input always produces same output, across runs, environments, and releases
- **Enforcement:**
  - All IR transformations sort keys and deduplicate
  - `deterministic_hash()` uses canonical JSON (sorted keys, `separators=(",", ":")`, UTF-8) + SHA256
  - No randomness, no system time, no hidden state anywhere in the pipeline
  - CI snapshot tests fail on any output change

### 4.2 Reproducibility

- **Definition:** Artifacts can be reconstructed from inputs and produce identical hashes
- **Enforcement:**
  - Wheel builds are reproducible (CI verifies hash equality across two builds)
  - Bundle replay produces identical `root_hash` (golden bundle fixture test)
  - `verify_bundle_replay()` reconstructs and compares hashes
  - 7+ snapshot boundaries enforce drift detection

### 4.3 Auditability

- **Definition:** Every artifact is traceable to its inputs; every change is detectable
- **Enforcement:**
  - Content-addressable artifacts (`artifact_hash`, `bundle_hash`, `experiment_id`)
  - `compute_structural_diff()` produces `DriftReport` with added/removed/changed keys
  - Milestone-driven governance: every change has plan, CI run, audit, summary
  - `docs/quantlab.md` is the canonical ledger

### 4.4 CI Truthfulness

- **Definition:** CI must accurately reflect system health; no muted failures
- **Enforcement:**
  - Single required job (`test`); merge-blocking
  - No `continue-on-error` on any step
  - Gates: Ruff check, Ruff format, MyPy strict, pip-audit, pytest (coverage >= 85%), schema validation, wheel reproducibility
  - All GitHub Actions SHA-pinned (no version tags)

### 4.5 No Silent Failures

- **Definition:** Any failure must be visible, reported, and blocking
- **Enforcement:**
  - CI fails on any lint error, type error, test failure, vulnerability, or schema drift
  - Promotion gates explicitly list `gates_failed`; `passed = all(gates pass)`
  - Bundle validation raises `ValueError` on missing artifacts
  - Registry validation raises `ValueError` on incomplete bundles
  - ExperimentTracker validation raises `ValueError` on missing fields

### 4.6 Immutability

- **Definition:** All artifacts are frozen after construction; no mutation
- **Enforcement:**
  - All IR types are `frozen=True` dataclasses or Pydantic `BaseModel` (frozen)
  - `StrategyArtifactBundle`, `PromotionDecision`, `ResearchRunResult`, `ExperimentRecord`, `StrategyRegistryEntry` are all frozen dataclasses
  - No setter methods; no mutable state on any artifact

### 4.7 Consumer Contract

- **Definition:** External systems import only from `quantlab.public`; internal modules are not stable
- **Enforcement:**
  - `tests/test_public_surface.py` verifies all consumer symbols exist and are correct types
  - `docs/quantlab.md` §19 documents the contract
  - §12.1 defines frozen compiler API; §19 defines consumer artifact surface
  - Internal module changes do not require MAJOR version bump

---

## 5. Execution Model

### 5.1 Lifecycle

#### Step 1 — Define Contract

Create an `IntentConfig` specifying modeling intent:

```python
from quantlab.public import IntentConfig

config = IntentConfig(
    asset_universe="US large-cap equities",
    target="next-day return direction",
    horizon_days=1,
    features=["momentum", "volatility", "volume"],
    governance_level="exploratory",
)
```

#### Step 2 — Run Research Pipeline

Use `ResearchRunner` to execute the full lifecycle:

```python
from quantlab.public import ResearchRunner

runner = ResearchRunner()
result = runner.run_intent(config)
```

This executes the complete pipeline:
1. `normalize_intent(config)` → `ModelingIntent`
2. `build_feature_graph()` → `FeatureGraph`
3. `build_feature_pipeline()` → `FeaturePipeline`
4. `build_training_harness()` → `TrainingHarness`
5. `WalkForwardEngine.run()` → `WalkForwardResult`
6. Bridge → `DecisionTrace[]`, market prices, `SimConfig`
7. `ExecutionSimulator.simulate()` → `ExecutionRecord[]`, `PnLSeries`
8. `evaluate_promotion()` → `PromotionDecision`
9. `build_strategy_report()` → `StrategyEvaluationReport`
10. `build_strategy_bundle()` → `StrategyArtifactBundle`
11. `StrategyRegistry.register_bundle()` → `StrategyRegistryEntry`
12. `ExperimentTracker.register_experiment()` → `ExperimentRecord`

#### Step 3 — Inspect Results

```python
# Result summary
print(result.strategy_id)       # deterministic: "strat-<hash[:12]>"
print(result.bundle_hash)       # SHA256 of canonical bundle payload
print(result.experiment_id)     # deterministic hash of intent + bundle + metadata
print(result.promotion_passed)  # True if all gates passed
print(result.rank_score)        # ranking metric

# Registry: compare strategies
best = runner.best_strategy()   # top-ranked StrategyRegistryEntry
```

#### Step 4 — Batch Execution

```python
configs = [config_a, config_b, config_c]
results = runner.run_many(configs)

# Results are deterministically ordered
for r in results:
    print(r.strategy_id, r.promotion_passed, r.rank_score)
```

### 5.2 Canonical End-to-End Example

```python
from quantlab.public import IntentConfig, ResearchRunner, StrategyRegistry

registry = StrategyRegistry()
runner = ResearchRunner(strategy_registry=registry)

intent = IntentConfig(
    asset_universe="US large-cap equities",
    target="next-day return direction",
    horizon_days=1,
    features=["momentum", "volatility", "volume"],
    governance_level="exploratory",
)

result = runner.run_intent(intent, metadata={"run": "baseline"})

assert isinstance(result.strategy_id, str)
assert isinstance(result.bundle_hash, str)
assert isinstance(result.experiment_id, str)
assert isinstance(result.promotion_passed, bool)
assert isinstance(result.rank_score, float)

top = registry.top_strategies(1)
assert len(top) == 1
assert top[0].strategy_id == result.strategy_id
```

This example is:
- Deterministic (same output every time)
- Complete (covers full pipeline)
- Verifiable (assertions prove correctness)
- Representative (uses all system layers)

### 5.3 Execution Modes

#### Research Mode
- Purpose: exploratory strategy development
- Gates: advisory (results recorded but not enforced)
- Output: full StrategyArtifactBundle

#### Validation Mode
- Purpose: candidate verification for promotion
- Gates: enforced (all must pass)
- Output: promotable bundles only

#### Production Mode
- Purpose: downstream consumption by external systems
- Input: StrategyArtifactBundle
- Execution: read-only (no mutation, no retraining)

---

## 5A. Failure Model

A pipeline run is considered failed if any of the following occur:

- Walk-forward validation fails to produce a valid WalkForwardResult
- ExecutionSimulator fails to produce deterministic ExecutionRecord[]
- PromotionDecision.passed == False
- Required artifacts are missing or invalid
- Hash mismatch occurs during replay verification

Failure is:

- explicit
- blocking
- never silent

Failed strategies:

- remain valid artifacts
- are registered but ranked last
- cannot be promoted

---

## 6. Consumer Import Contract

### Rule

External repositories **MUST** import only from `quantlab.public`:

```python
from quantlab.public import ResearchRunner, StrategyArtifactBundle
from quantlab import __version__
```

### Never

```python
from quantlab.runtime.trading.bundle import StrategyArtifactBundle   # WRONG
from quantlab.runtime.research import ResearchRunner                 # WRONG
```

### Available Symbols

| Symbol | Type | Role |
|--------|------|------|
| `IntentConfig` | class | User-facing modeling input |
| `normalize_intent` | function | DSL → contract normalization |
| `ModelingIntent` | class | Canonical modeling contract |
| `SCHEMA_VERSION` | str | Contract schema version |
| `FeatureNode` | class | Graph node |
| `FeatureGraph` | class | Feature dependency graph IR |
| `build_feature_graph` | function | ModelingIntent → FeatureGraph |
| `PipelineStage` | class | Pipeline stage |
| `FeaturePipeline` | class | Feature pipeline IR |
| `build_feature_pipeline` | function | FeatureGraph → FeaturePipeline |
| `ModelSpec` | class | Model specification |
| `TrainingHarness` | class | Training harness IR |
| `build_training_harness` | function | FeaturePipeline + ModelingIntent → TrainingHarness |
| `ExecutionAdapter` | protocol | Adapter for fit/predict |
| `WalkForwardEngine` | class | Walk-forward validation engine |
| `WalkForwardResult` | class | Validation result with artifact_hash |
| `BaselineExplainer` | class | XAI baseline explainer |
| `ExplainedWalkForwardResult` | class | Explained result with artifact_hash |
| `Explanation` | class | Feature contributions |
| `deterministic_hash` | function | Canonical JSON → SHA256 |
| `StrategyArtifactBundle` | class | Portable research artifact |
| `StrategyRegistryEntry` | class | Registry entry with rank_score |
| `StrategyRegistry` | class | Multi-strategy catalog |
| `ExperimentRecord` | class | Reproducible research run record |
| `ExperimentTracker` | class | Experiment catalog |
| `ResearchRunner` | class | Full pipeline orchestrator |
| `ResearchRunResult` | class | Single research run result |

---

## 7. Artifact Model

### Artifact Types

| Artifact | Location | Hash | Frozen |
|----------|----------|------|--------|
| ModelingIntent | contracts/ | Implicit (snapshot) | Yes (Pydantic) |
| FeatureGraph | graph/ | Implicit (snapshot) | Yes (frozen) |
| FeaturePipeline | pipeline/ | Implicit (snapshot) | Yes (frozen) |
| TrainingHarness | training/ | Implicit (snapshot) | Yes (frozen) |
| WalkForwardResult | runtime/ | `artifact_hash` | Yes (frozen) |
| ExplainedWalkForwardResult | runtime/ | `artifact_hash` | Yes (frozen) |
| StrategyArtifactBundle | runtime/trading/bundle/ | `bundle_hash` | Yes (frozen) |
| StrategyRegistryEntry | runtime/trading/registry/ | Via `bundle_hash` | Yes (frozen) |
| ExperimentRecord | runtime/trading/experiments/ | `experiment_id` | Yes (frozen) |
| ResearchRunResult | runtime/research/ | Via `bundle_hash` | Yes (frozen) |

### Hash Algorithm

- `deterministic_hash(payload)`:
  1. Serialize to canonical JSON: `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`
  2. Encode UTF-8
  3. SHA256 hexdigest
- Stable across runs, environments, and patch/minor releases
- Algorithm change is a breaking change (MAJOR version bump)

### Snapshot Boundaries

7+ snapshot boundaries enforce drift detection:

1. `modeling_intent_schema.json`
2. `normalized_intent.json`
3. `feature_graph.json`
4. `feature_pipeline.json`
5. `training_harness.json`
6. `walk_forward_result.json`
7. `explained_walk_forward_result.json`
8. `golden_bundle_v1.json`

CI fails if any snapshot changes without explicit update.

### Artifact Lifecycle

Artifacts follow a strict lifecycle:

1. Constructed (build_strategy_bundle)
2. Validated (schema + completeness checks)
3. Evaluated (PromotionDecision)
4. Registered (StrategyRegistry)
5. Tracked (ExperimentTracker)
6. Consumed (external systems via quantlab.public)

Artifacts are immutable and never modified after creation.

---

## 8. Agent Guardrails

### Rules for AI Agents Operating on QuantLab

1. **No silent failures.** Every operation must produce observable output. If a step fails, it must be reported, not swallowed.

2. **No CI weakening.** Do not add `continue-on-error`, remove required checks, lower coverage thresholds, or disable linters.

3. **No contract bypass.** Do not modify snapshot files without updating the corresponding source code. Do not change hash algorithms. Do not alter frozen dataclass definitions.

4. **No hidden state.** Do not introduce randomness, system time dependencies, or environment-dependent behavior into any pipeline step.

5. **No IR contamination.** Do not add execution logic to contracts/, dsl/, graph/, pipeline/, or training/. All execution belongs in runtime/.

6. **No internal imports in external code.** External systems must use `quantlab.public` only. Do not bypass the consumer contract.

7. **No version drift.** Version in `pyproject.toml`, `quantlab/version.py`, and version tests must always agree. Golden bundle must be regenerated after version bump.

8. **No scope creep.** Each change must be minimal, PR-sized, and traceable to a milestone or explicit request.

### Verification Commands

```bash
pytest                      # All tests pass
ruff check .                # Zero lint violations
ruff format --check .       # Format compliance
mypy quantlab               # Strict type checking, zero errors
pip-audit                   # No known vulnerabilities
```

All five must pass before any merge.

---

## 8A. AI-Agent Operating Model

When operating on QuantLab, an AI agent must:

1. Begin from IntentConfig (never bypass DSL layer)
2. Execute the full compiler spine (no stage skipping)
3. Treat all artifacts as immutable
4. Validate outputs at each stage
5. Preserve determinism (no randomness or hidden state)

Agents must:

- produce deterministic, reproducible outputs
- operate in small, auditable changes
- preserve all system invariants

---

## 8B. Anti-Patterns

The following behaviors are prohibited:

- Executing logic outside runtime/
- Modifying artifacts after creation
- Introducing randomness or system time dependencies
- Bypassing PromotionDecision evaluation
- Importing internal modules from external systems
- Weakening CI enforcement (coverage, lint, security)
- Editing snapshot files without corresponding code changes

---

## 9. Versioning and Stability

### Semantic Versioning

- **MAJOR (X.0.0):** Breaking change to frozen API (§12.1) or consumer contract (§19)
- **MINOR (0.X.0):** Backward-compatible additions
- **PATCH (0.0.X):** Bug fixes, internal improvements

### Stability Tiers

| Tier | Surface | Policy |
|------|---------|--------|
| Frozen (§12.1) | Compiler symbols: `ModelingIntent`, `normalize_intent`, IR builders, `WalkForwardEngine`, `deterministic_hash` | Breaking changes require MAJOR bump |
| Consumer (§19) | `StrategyArtifactBundle`, `StrategyRegistry`, `ExperimentTracker`, `ResearchRunner`, `ResearchRunResult` | Stable across MINOR releases; may evolve across MAJOR |
| Internal | All other modules | May change without notice |

### Version Pinning for Downstream

- Promotable trading branches: pin `==X.Y.Z` (exact)
- Development branches: may use `>=X.Y,<X.(Y+1)`
- Promotion requires exact pin

---

## 10. Quick Reference

### Installation

```bash
pip install -e .           # Runtime
pip install -e ".[dev]"    # Development (Ruff, MyPy, pip-audit)
```

### Run Tests

```bash
pytest
```

### Check Quality Gates

```bash
ruff check .
ruff format --check .
mypy quantlab
pip-audit
```

### Project Structure

```
quantlab/
  contracts/          Contract layer (ModelingIntent, SCHEMA_VERSION)
  dsl/                DSL layer (IntentConfig, normalize_intent)
  graph/              Graph IR (FeatureGraph, build_feature_graph)
  pipeline/           Pipeline IR (FeaturePipeline, build_feature_pipeline)
  training/           Training IR (TrainingHarness, build_training_harness)
  runtime/            Execution boundary
    walk_forward.py     WalkForwardEngine
    explanation.py      BaselineExplainer
    hash_utils.py       deterministic_hash
    bundle.py           ArtifactBundle (compiler-level)
    drift.py            DriftReport, compute_structural_diff
    regime.py           RegimeReport
    portfolio.py        PortfolioReport
    risk.py             RiskReport
    trading/            Trading pipeline
      sim_config.py       SimConfig
      decision_trace.py   DecisionTrace
      execution_record.py ExecutionRecord
      pnl_series.py       PnLSeries
      pnl_attribution.py  PnLAttribution
      simulator/          ExecutionSimulator
      evaluation/         Promotion gates
      reporting/          StrategyEvaluationReport
      bundle/             StrategyArtifactBundle
      registry/           StrategyRegistry
      experiments/        ExperimentTracker
    research/           ResearchRunner
  public/             Consumer API surface
    __init__.py         All consumer exports
    artifacts.py        Trading artifact re-exports
    research.py         Research re-exports
docs/
  quantlab.md           Canonical project ledger
  quantlab_operating_manual.md  This document
tests/
  snapshots/            Snapshot boundary fixtures
  fixtures/             Golden bundle fixture
```

### Minimal Execution Recipe

1. Define IntentConfig
2. Run ResearchRunner.run_intent()
3. Inspect ResearchRunResult
4. Select strategy from StrategyRegistry
5. Export StrategyArtifactBundle to downstream system

### Source of Truth

- **Operating reference:** `docs/quantlab_operating_manual.md` (this document)
- **Canonical ledger:** `docs/quantlab.md` (milestone history, §12 stability contract, §19 consumer contract)
- **Consumer surface:** `quantlab/public/__init__.py`

---

*End of QuantLab Operating Manual.*
