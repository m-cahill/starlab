"""Load benchmark contract + baseline suite artifacts; build entrant catalog (M23)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from starlab.benchmarks.benchmark_contract_schema import validate_benchmark_contract
from starlab.benchmarks.benchmark_scorecard_schema import validate_benchmark_scorecard
from starlab.evaluation.evaluation_runner_models import (
    HEURISTIC_BASELINE_SUITE_VERSION,
    SCRIPTED_BASELINE_SUITE_VERSION,
)
from starlab.runs.json_util import sha256_hex_of_canonical_json


def load_benchmark_contract_json(path: Path) -> dict[str, Any]:
    """Load and return a benchmark contract object."""

    raw = path.read_text(encoding="utf-8")
    try:
        obj: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in benchmark contract: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(obj, dict):
        msg = "benchmark contract must be a JSON object"
        raise TypeError(msg)
    return obj


def load_suite_json(path: Path) -> dict[str, Any]:
    """Load a baseline suite JSON object."""

    raw = path.read_text(encoding="utf-8")
    try:
        obj: Any = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"invalid JSON in suite artifact: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(obj, dict):
        msg = "suite artifact must be a JSON object"
        raise ValueError(msg)
    return obj


def _require_keys(obj: dict[str, Any], keys: tuple[str, ...], *, label: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        msg = f"{label}: missing required keys: {', '.join(sorted(missing))}"
        raise ValueError(msg)


def validate_suite_against_contract(
    suite: dict[str, Any],
    *,
    benchmark_contract: dict[str, Any],
    benchmark_contract_sha256: str,
    suite_path: Path,
) -> Literal["scripted", "heuristic"]:
    """Structural + semantic validation for M21/M22 governed suite artifacts."""

    label = f"suite {suite_path}"
    _require_keys(
        suite,
        (
            "benchmark_contract_sha256",
            "benchmark_id",
            "evaluation_posture",
            "measurement_surface",
            "scorecards",
            "subjects",
            "suite_id",
            "suite_version",
        ),
        label=label,
    )

    sv = suite["suite_version"]
    if sv == SCRIPTED_BASELINE_SUITE_VERSION:
        kind: Literal["scripted", "heuristic"] = "scripted"
    elif sv == HEURISTIC_BASELINE_SUITE_VERSION:
        kind = "heuristic"
    else:
        msg = f"{label}: unsupported suite_version {sv!r}"
        raise ValueError(msg)

    if suite.get("measurement_surface") != "fixture_only":
        msg = f"{label}: measurement_surface must be fixture_only"
        raise ValueError(msg)
    if suite.get("evaluation_posture") != "fixture_only":
        msg = f"{label}: evaluation_posture must be fixture_only"
        raise ValueError(msg)
    if suite.get("benchmark_id") != benchmark_contract["benchmark_id"]:
        msg = f"{label}: benchmark_id does not match loaded benchmark contract"
        raise ValueError(msg)
    if suite.get("benchmark_contract_sha256") != benchmark_contract_sha256:
        msg = f"{label}: benchmark_contract_sha256 does not match loaded benchmark contract"
        raise ValueError(msg)

    subjects = suite["subjects"]
    scorecards = suite["scorecards"]
    if not isinstance(subjects, list) or not isinstance(scorecards, list):
        msg = f"{label}: subjects and scorecards must be arrays"
        raise ValueError(msg)
    if len(subjects) != len(scorecards):
        msg = f"{label}: subjects and scorecards length mismatch"
        raise ValueError(msg)

    for i, sub in enumerate(subjects):
        if not isinstance(sub, dict):
            msg = f"{label}: subjects[{i}] must be an object"
            raise ValueError(msg)
        sk = sub.get("subject_kind")
        sid = sub.get("subject_id")
        if sk != kind:
            msg = f"{label}: expected subject_kind {kind!r} for this suite, got {sk!r}"
            raise ValueError(msg)
        if not isinstance(sid, str) or not sid:
            msg = f"{label}: invalid subject_id at subjects[{i}]"
            raise ValueError(msg)

    for i, sc in enumerate(scorecards):
        if not isinstance(sc, dict):
            msg = f"{label}: scorecards[{i}] must be an object"
            raise ValueError(msg)
        errs = validate_benchmark_scorecard(sc)
        if errs:
            msg = f"{label}: scorecard validation failed: " + "; ".join(errs)
            raise ValueError(msg)
        if sc.get("benchmark_contract_sha256") != benchmark_contract_sha256:
            msg = f"{label}: embedded scorecard benchmark_contract_sha256 mismatch"
            raise ValueError(msg)
        if sc.get("evaluation_posture") != "fixture_only":
            msg = f"{label}: embedded scorecard evaluation_posture must be fixture_only"
            raise ValueError(msg)
        ref = sc.get("subject_ref")
        if not isinstance(ref, dict):
            msg = f"{label}: scorecards[{i}] missing subject_ref"
            raise ValueError(msg)
        if ref.get("subject_kind") != kind:
            msg = f"{label}: scorecard subject_kind mismatch at index {i}"
            raise ValueError(msg)
        want_id = subjects[i]["subject_id"]
        if ref.get("subject_id") != want_id:
            msg = f"{label}: scorecard subject_id order mismatch at index {i}"
            raise ValueError(msg)

    return kind


def suite_path_for_artifact(path: Path) -> str:
    """Prefer a cwd-relative path string for stable, portable artifacts."""

    try:
        cwd = Path.cwd().resolve()
        resolved = path.resolve()
        return str(resolved.relative_to(cwd).as_posix())
    except ValueError:
        return str(path.as_posix())


def build_entrant_catalog(
    suites: list[dict[str, Any]],
    suite_meta: list[tuple[Path, str]],
) -> list[dict[str, Any]]:
    """Flatten entrants: suite path order, then subject/scorecard order within each suite."""

    entrants: list[dict[str, Any]] = []
    for suite, (path, content_sha256) in zip(suites, suite_meta, strict=True):
        suite_id = suite["suite_id"]
        suite_version = suite["suite_version"]
        scorecards = suite["scorecards"]
        for idx, sc in enumerate(scorecards):
            ref = sc["subject_ref"]
            subject_id = ref["subject_id"]
            subject_kind = ref["subject_kind"]
            entrant_id = f"{suite_id}::{subject_id}"
            entrants.append(
                {
                    "entrant_id": entrant_id,
                    "source_scorecard_ref": {
                        "scorecard_index": idx,
                        "suite_id": suite_id,
                        "suite_path": suite_path_for_artifact(path),
                        "suite_sha256": content_sha256,
                        "suite_version": suite_version,
                    },
                    "subject_id": subject_id,
                    "subject_kind": subject_kind,
                    "suite_id": suite_id,
                },
            )
    return entrants


def prepare_runner_inputs(
    *,
    benchmark_contract_path: Path,
    suite_paths: list[Path],
) -> tuple[
    dict[str, Any],
    str,
    list[dict[str, Any]],
    list[tuple[Path, str]],
    list[dict[str, Any]],
]:
    """Validate contract + suites and return (contract, sha256, suites, meta, entrants)."""

    benchmark_contract = load_benchmark_contract_json(benchmark_contract_path)
    errs = validate_benchmark_contract(benchmark_contract)
    if errs:
        msg = "benchmark contract validation failed: " + "; ".join(errs)
        raise ValueError(msg)
    if benchmark_contract.get("measurement_surface") != "fixture_only":
        msg = "M23 requires measurement_surface 'fixture_only' on the benchmark contract"
        raise ValueError(msg)

    benchmark_contract_sha256 = sha256_hex_of_canonical_json(benchmark_contract)

    suites: list[dict[str, Any]] = []
    meta: list[tuple[Path, str]] = []
    for p in suite_paths:
        suite = load_suite_json(p)
        content_sha256 = sha256_hex_of_canonical_json(suite)
        validate_suite_against_contract(
            suite,
            benchmark_contract=benchmark_contract,
            benchmark_contract_sha256=benchmark_contract_sha256,
            suite_path=p,
        )
        suites.append(suite)
        meta.append((p, content_sha256))

    entrants = build_entrant_catalog(suites, meta)
    seen: set[str] = set()
    for e in entrants:
        eid = e["entrant_id"]
        if eid in seen:
            msg = f"duplicate entrant_id after flattening: {eid!r}"
            raise ValueError(msg)
        seen.add(eid)

    return benchmark_contract, benchmark_contract_sha256, suites, meta, entrants
