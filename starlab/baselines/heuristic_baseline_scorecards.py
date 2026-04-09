"""Build M20-conformant scorecards for the M22 heuristic baseline suite."""

from __future__ import annotations

from typing import Any

from starlab.baselines.heuristic_baseline_models import (
    HEURISTIC_BASELINE_SCORECARD_NON_CLAIMS_V1,
    HEURISTIC_BASELINE_SCORECARD_WARNINGS_V1,
)
from starlab.benchmarks.benchmark_scorecard_schema import validate_benchmark_scorecard


def build_heuristic_scorecard(
    *,
    benchmark_contract: dict[str, Any],
    benchmark_contract_sha256: str,
    subject_id: str,
    metric_values: dict[str, float | int],
) -> dict[str, Any]:
    """Return one scorecard for ``subject_id`` (deterministic fixture values)."""

    bench_id = benchmark_contract["benchmark_id"]
    bench_version = benchmark_contract["benchmark_version"]
    metric_defs: list[dict[str, Any]] = list(
        benchmark_contract["metric_definitions"],
    )
    gating: list[dict[str, Any]] = list(benchmark_contract["gating_rules"])

    metric_rows: list[dict[str, Any]] = []
    for md in metric_defs:
        mid = md["metric_id"]
        if mid not in metric_values:
            msg = f"missing fixture metric value for metric_id={mid!r} subject={subject_id!r}"
            raise ValueError(msg)
        raw = metric_values[mid]
        val: float | int
        if isinstance(raw, bool):  # pragma: no cover
            msg = "boolean metric values are not supported"
            raise TypeError(msg)
        val = raw
        metric_rows.append(
            {
                "metric_id": mid,
                "unit": md["unit"],
                "value": val,
            },
        )

    gating_outcomes: list[dict[str, Any]] = []
    for rule in gating:
        gating_outcomes.append(
            {
                "detail": None,
                "passed": True,
                "rule_id": rule["rule_id"],
            },
        )

    warnings = sorted(HEURISTIC_BASELINE_SCORECARD_WARNINGS_V1)
    non_claims = sorted(HEURISTIC_BASELINE_SCORECARD_NON_CLAIMS_V1)

    scorecard: dict[str, Any] = {
        "aggregate_scores": [],
        "benchmark_contract_sha256": benchmark_contract_sha256,
        "benchmark_id": bench_id,
        "benchmark_version": bench_version,
        "comparability_status": "provisional",
        "evaluation_posture": "fixture_only",
        "gating_outcomes": gating_outcomes,
        "metric_rows": metric_rows,
        "non_claims": non_claims,
        "schema_version": "starlab.benchmark_scorecard.v1",
        "scoring_status": "scored",
        "subject_ref": {
            "subject_id": subject_id,
            "subject_kind": "heuristic",
        },
        "warnings": warnings,
    }

    errs = validate_benchmark_scorecard(scorecard)
    if errs:
        msg = "generated scorecard failed validation: " + "; ".join(errs)
        raise ValueError(msg)
    return scorecard


def assert_scorecards_valid(scorecards: list[dict[str, Any]]) -> None:
    """Re-validate each scorecard (defensive)."""

    for sc in scorecards:
        errs = validate_benchmark_scorecard(sc)
        if errs:
            msg = "scorecard validation failed: " + "; ".join(errs)
            raise ValueError(msg)
