"""Assemble heuristic baseline suite + report artifacts (M22)."""

from __future__ import annotations

from typing import Any

from starlab.baselines.heuristic_baseline_models import (
    HEURISTIC_BASELINE_FIXTURE_CASE_IDS,
    HEURISTIC_BASELINE_SUBJECT_IDS,
    HEURISTIC_BASELINE_SUBJECT_METRIC_VALUES,
    HEURISTIC_BASELINE_SUITE_ID,
    HEURISTIC_BASELINE_SUITE_NON_CLAIMS_V1,
    HEURISTIC_BASELINE_SUITE_REPORT_VERSION,
    HEURISTIC_BASELINE_SUITE_VERSION,
    HEURISTIC_BASELINE_SUITE_WARNINGS_V1,
    SUITE_VERDICT_PASS,
)
from starlab.baselines.heuristic_baseline_scorecards import (
    assert_scorecards_valid,
    build_heuristic_scorecard,
)
from starlab.benchmarks.benchmark_contract_schema import validate_benchmark_contract
from starlab.runs.json_util import sha256_hex_of_canonical_json


def _require_fixture_only_measurement_surface(contract: dict[str, Any]) -> None:
    surface = contract.get("measurement_surface")
    if surface != "fixture_only":
        msg = f"M22 requires measurement_surface 'fixture_only', got {surface!r}"
        raise ValueError(msg)


def build_heuristic_baseline_suite_and_report(
    benchmark_contract: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate the contract, build suite + report dicts, validate embedded scorecards."""

    errs = validate_benchmark_contract(benchmark_contract)
    if errs:
        msg = "benchmark contract validation failed: " + "; ".join(errs)
        raise ValueError(msg)

    _require_fixture_only_measurement_surface(benchmark_contract)

    contract_sha256 = sha256_hex_of_canonical_json(benchmark_contract)

    subjects: list[dict[str, Any]] = []
    for sid in HEURISTIC_BASELINE_SUBJECT_IDS:
        subjects.append(
            {
                "subject_id": sid,
                "subject_kind": "heuristic",
            },
        )

    fixture_cases: list[dict[str, Any]] = []
    for cid in HEURISTIC_BASELINE_FIXTURE_CASE_IDS:
        fixture_cases.append(
            {
                "case_id": cid,
                "description": "M22 deterministic fixture-only evaluation case.",
            },
        )

    scorecards: list[dict[str, Any]] = []
    for sid in HEURISTIC_BASELINE_SUBJECT_IDS:
        metric_values = HEURISTIC_BASELINE_SUBJECT_METRIC_VALUES[sid]
        scorecards.append(
            build_heuristic_scorecard(
                benchmark_contract=benchmark_contract,
                benchmark_contract_sha256=contract_sha256,
                subject_id=sid,
                metric_values=metric_values,
            ),
        )

    assert_scorecards_valid(scorecards)

    suite_warnings = sorted(HEURISTIC_BASELINE_SUITE_WARNINGS_V1)
    suite_non_claims = sorted(HEURISTIC_BASELINE_SUITE_NON_CLAIMS_V1)

    suite: dict[str, Any] = {
        "benchmark_contract_sha256": contract_sha256,
        "benchmark_id": benchmark_contract["benchmark_id"],
        "evaluation_posture": "fixture_only",
        "fixture_cases": fixture_cases,
        "measurement_surface": benchmark_contract["measurement_surface"],
        "non_claims": suite_non_claims,
        "scorecards": scorecards,
        "subjects": subjects,
        "suite_id": HEURISTIC_BASELINE_SUITE_ID,
        "suite_version": HEURISTIC_BASELINE_SUITE_VERSION,
        "warnings": suite_warnings,
    }

    report: dict[str, Any] = {
        "benchmark_contract_sha256": contract_sha256,
        "failures": [],
        "fixture_case_count": len(fixture_cases),
        "non_claims": suite_non_claims,
        "report_version": HEURISTIC_BASELINE_SUITE_REPORT_VERSION,
        "scorecard_count": len(scorecards),
        "subject_count": len(subjects),
        "suite_verdict": SUITE_VERDICT_PASS,
        "warnings": suite_warnings,
    }

    return suite, report
