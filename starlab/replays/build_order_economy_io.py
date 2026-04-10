"""Load timeline + optional lineage / raw parse; emit build-order/economy artifacts (M11)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab._io import load_json_object
from starlab.replays.build_order_economy_extraction import (
    extract_build_order_economy_envelope,
    validate_timeline_contract,
)
from starlab.replays.build_order_economy_models import (
    BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
    BUILD_ORDER_ECONOMY_PROFILE,
    BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
    BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
    ORDERING_POLICY,
    BuildOrderEconomyCheckResult,
    ExtractionStatus,
    RunStatus,
    finalize_build_order_economy_checks,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def _is_hex_sha256(v: Any) -> bool:
    if not isinstance(v, str) or len(v) != 64:
        return False
    try:
        int(v, 16)
    except ValueError:
        return False
    return True


def exit_code_for_build_order_economy_run(status: str) -> int:
    if status == "completed":
        return 0
    if status == "source_contract_failed":
        return 5
    if status == "extraction_failed":
        return 4
    msg = f"unknown build-order/economy run status: {status!r}"
    raise ValueError(msg)


def _counts_from_steps(
    steps: list[dict[str, Any]],
) -> tuple[dict[str, int], dict[str, int], dict[int, dict[str, int]]]:
    by_cat: dict[str, int] = {}
    by_phase: dict[str, int] = {}
    by_player: dict[int, dict[str, int]] = {}
    for s in steps:
        c = s.get("category")
        if isinstance(c, str):
            by_cat[c] = by_cat.get(c, 0) + 1
        p = s.get("phase")
        if isinstance(p, str):
            by_phase[p] = by_phase.get(p, 0) + 1
        pi = s.get("player_index")
        if isinstance(pi, int) and not isinstance(pi, bool):
            by_player.setdefault(pi, {})
            by_player[pi]["steps"] = by_player[pi].get("steps", 0) + 1
    return by_cat, by_phase, by_player


def run_build_order_economy_extraction(
    *,
    timeline: dict[str, Any],
    source_timeline_sha256: str,
    raw_parse: dict[str, Any] | None,
    source_raw_parse_sha256: str | None,
    timeline_report: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    """Return ``(run_status, artifact, report)`` including finalized ``check_results``."""

    checks: list[BuildOrderEconomyCheckResult] = []

    ok, err = validate_timeline_contract(timeline)
    checks.append(
        BuildOrderEconomyCheckResult(
            check_id="timeline_schema_valid",
            detail=None if ok else err,
            severity="required",
            status="pass" if ok else "fail",
        ),
    )

    rhash = timeline.get("replay_content_sha256")
    hash_ok = _is_hex_sha256(rhash)
    checks.append(
        BuildOrderEconomyCheckResult(
            check_id="replay_hash_present",
            detail=None if hash_ok else "replay_content_sha256 missing or not 64-hex",
            severity="required",
            status="pass" if hash_ok else "fail",
        ),
    )

    checks.append(
        BuildOrderEconomyCheckResult(
            check_id="source_timeline_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    raw_match_ok = True
    detail_raw: str | None = None
    if raw_parse is not None:
        t_sr = timeline.get("source_raw_parse_sha256")
        if isinstance(t_sr, str) and t_sr:
            if not isinstance(source_raw_parse_sha256, str):
                raw_match_ok = False
                detail_raw = "source_raw_parse_sha256 unavailable for comparison"
            elif t_sr.lower() != source_raw_parse_sha256.lower():
                raw_match_ok = False
                detail_raw = "timeline source_raw_parse_sha256 mismatch vs supplemental raw parse"
        elif t_sr is None:
            raw_match_ok = True
            detail_raw = None
    checks.append(
        BuildOrderEconomyCheckResult(
            check_id="source_raw_parse_identity_match",
            detail=detail_raw,
            severity="warning",
            status="pass" if raw_match_ok else "warn" if raw_parse is not None else "not_evaluated",
        ),
    )

    contract_failed = not ok or not hash_ok

    source_tr_sha = (
        sha256_hex_of_canonical_json(timeline_report) if timeline_report is not None else None
    )
    source_meta_sha = sha256_hex_of_canonical_json(metadata) if metadata is not None else None
    source_meta_rep_sha = (
        sha256_hex_of_canonical_json(metadata_report) if metadata_report is not None else None
    )

    if contract_failed:
        empty: dict[str, Any] = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "schema_version": BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
            "replay_content_sha256": rhash if isinstance(rhash, str) else None,
            "source_timeline_sha256": source_timeline_sha256,
            "source_timeline_report_sha256": source_tr_sha,
            "source_metadata_sha256": source_meta_sha,
            "source_metadata_report_sha256": source_meta_rep_sha,
            "source_raw_parse_sha256": source_raw_parse_sha256,
            "ordering_policy": ORDERING_POLICY,
            "classification_profile": {},
            "players": [],
            "build_order_steps": [],
            "economy_checkpoints": [],
        }
        checks.append(
            BuildOrderEconomyCheckResult(
                check_id="build_order_economy_emitted",
                detail="empty envelope due to contract failure",
                severity="required",
                status="fail",
            ),
        )
        ordered = finalize_build_order_economy_checks(checks)
        report_out: dict[str, Any] = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "check_results": [c.to_mapping() for c in ordered],
            "counts_by_category": {},
            "counts_by_phase": {},
            "counts_by_player": {},
            "extraction_status": "failed",
            "ignored_timeline_semantic_kinds": {},
            "reason_codes": ["source_contract_failed"],
            "schema_version": BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
            "unclassified_unit_names": [],
            "unclassified_upgrade_names": [],
            "warnings": [],
        }
        return "source_contract_failed", empty, report_out

    body, report_partial = extract_build_order_economy_envelope(
        raw_parse=raw_parse,
        source_metadata_report_sha256=source_meta_rep_sha,
        source_metadata_sha256=source_meta_sha,
        source_raw_parse_sha256=source_raw_parse_sha256,
        source_timeline_report_sha256=source_tr_sha,
        source_timeline_sha256=source_timeline_sha256,
        timeline=timeline,
    )

    steps = body.get("build_order_steps")
    if not isinstance(steps, list):
        steps = []
    by_cat, by_phase, by_player = _counts_from_steps([s for s in steps if isinstance(s, dict)])

    extraction_status: ExtractionStatus = "ok"
    if report_partial.get("warnings") or not raw_match_ok:
        extraction_status = "partial"

    checks.append(
        BuildOrderEconomyCheckResult(
            check_id="build_order_economy_emitted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )
    ordered = finalize_build_order_economy_checks(checks)

    counts_by_player_out: dict[str, Any] = {
        str(k): v for k, v in sorted(by_player.items(), key=lambda kv: kv[0])
    }

    report_out = {
        **report_partial,
        "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
        "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
        "check_results": [c.to_mapping() for c in ordered],
        "counts_by_category": dict(sorted(by_cat.items())),
        "counts_by_phase": dict(sorted(by_phase.items())),
        "counts_by_player": counts_by_player_out,
        "extraction_status": extraction_status,
        "reason_codes": [] if raw_match_ok else ["supplemental_raw_parse_hash_mismatch"],
        "schema_version": BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
    }
    return "completed", body, report_out


def write_build_order_economy_artifacts(
    *,
    output_dir: Path,
    artifact: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ap = output_dir / "replay_build_order_economy.json"
    rp = output_dir / "replay_build_order_economy_report.json"
    ap.write_text(canonical_json_dumps(artifact), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ap, rp


def extract_build_order_economy_from_paths(
    *,
    timeline_path: Path,
    output_dir: Path,
    raw_parse_path: Path | None,
    timeline_report_path: Path | None,
    metadata_path: Path | None,
    metadata_report_path: Path | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    timeline, terr = load_json_object(timeline_path)
    if timeline is None:
        artifact = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "schema_version": BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
            "build_order_steps": [],
            "economy_checkpoints": [],
            "players": [],
        }
        report: dict[str, Any] = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "check_results": [
                c.to_mapping()
                for c in finalize_build_order_economy_checks(
                    [
                        BuildOrderEconomyCheckResult(
                            check_id="timeline_schema_valid",
                            detail=str(terr),
                            severity="required",
                            status="fail",
                        ),
                    ],
                )
            ],
            "extraction_status": "failed",
            "reason_codes": ["timeline_load_failed"],
            "schema_version": BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
            "warnings": [f"failed to load timeline: {terr}"],
        }
        write_build_order_economy_artifacts(artifact=artifact, output_dir=output_dir, report=report)
        return "extraction_failed", artifact, report

    source_timeline_sha256 = sha256_hex_of_canonical_json(timeline)

    def _load_opt(p: Path | None) -> dict[str, Any] | None:
        if p is None:
            return None
        d, e = load_json_object(p)
        if e is not None:
            raise ValueError(e)
        return d

    try:
        raw_parse = _load_opt(raw_parse_path)
        timeline_report = _load_opt(timeline_report_path)
        metadata = _load_opt(metadata_path)
        metadata_report = _load_opt(metadata_report_path)
    except ValueError as exc:
        artifact_err = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "schema_version": BUILD_ORDER_ECONOMY_SCHEMA_VERSION,
            "source_timeline_sha256": source_timeline_sha256,
            "build_order_steps": [],
            "economy_checkpoints": [],
            "players": [],
        }
        report_err = {
            "build_order_economy_contract_version": BUILD_ORDER_ECONOMY_CONTRACT_VERSION,
            "build_order_economy_profile": BUILD_ORDER_ECONOMY_PROFILE,
            "check_results": [
                c.to_mapping()
                for c in finalize_build_order_economy_checks(
                    [
                        BuildOrderEconomyCheckResult(
                            check_id="source_raw_parse_identity_match",
                            detail=str(exc),
                            severity="required",
                            status="fail",
                        ),
                    ],
                )
            ],
            "extraction_status": "failed",
            "reason_codes": ["lineage_load_failed"],
            "schema_version": BUILD_ORDER_ECONOMY_REPORT_SCHEMA_VERSION,
            "warnings": [str(exc)],
        }
        write_build_order_economy_artifacts(
            artifact=artifact_err,
            output_dir=output_dir,
            report=report_err,
        )
        return "extraction_failed", artifact_err, report_err

    source_raw_parse_sha256 = (
        sha256_hex_of_canonical_json(raw_parse) if raw_parse is not None else None
    )

    status, body, report_out = run_build_order_economy_extraction(
        metadata=metadata,
        metadata_report=metadata_report,
        raw_parse=raw_parse,
        source_raw_parse_sha256=source_raw_parse_sha256,
        timeline=timeline,
        timeline_report=timeline_report,
        source_timeline_sha256=source_timeline_sha256,
    )
    write_build_order_economy_artifacts(artifact=body, output_dir=output_dir, report=report_out)
    return status, body, report_out
