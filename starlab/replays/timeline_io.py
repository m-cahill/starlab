"""Load raw parse + optional lineage, emit ``replay_timeline`` artifacts (M10)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.timeline_extraction import extract_timeline_envelope
from starlab.replays.timeline_models import (
    MERGE_ORDER_POLICY,
    TIMELINE_CONTRACT_VERSION,
    TIMELINE_PROFILE,
    TIMELINE_REPORT_SCHEMA_VERSION,
    TIMELINE_SCHEMA_VERSION,
    TimelineCheckResult,
    finalize_timeline_checks,
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


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "JSON root must be an object"
    return raw, None


def exit_code_for_timeline_run(status: str) -> int:
    if status == "completed":
        return 0
    if status == "source_contract_failed":
        return 5
    if status == "extraction_failed":
        return 4
    msg = f"unknown timeline run status: {status!r}"
    raise ValueError(msg)


def run_timeline_extraction(
    *,
    raw_parse: dict[str, Any],
    source_raw_parse_sha256: str,
    parse_receipt: dict[str, Any] | None,
    parse_report: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Return ``(run_status, timeline, report)`` — report includes finalized ``checks``."""

    checks: list[TimelineCheckResult] = []
    reason_notes: list[str] = []

    schema_ok = isinstance(raw_parse.get("schema_version"), str) and raw_parse.get(
        "schema_version",
    ) in (
        "starlab.replay_raw_parse.v1",
        "starlab.replay_raw_parse.v2",
    )
    checks.append(
        TimelineCheckResult(
            check_id="raw_parse_schema_valid",
            detail=None if schema_ok else "unsupported schema_version",
            severity="required",
            status="pass" if schema_ok else "fail",
        ),
    )

    rhash = raw_parse.get("replay_content_sha256")
    hash_ok = _is_hex_sha256(rhash)
    checks.append(
        TimelineCheckResult(
            check_id="replay_hash_present",
            detail=None if hash_ok else "replay_content_sha256 missing or not 64-hex",
            severity="required",
            status="pass" if hash_ok else "fail",
        ),
    )

    checks.append(
        TimelineCheckResult(
            check_id="source_raw_parse_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    if parse_receipt is None:
        checks.append(
            TimelineCheckResult(
                check_id="parse_receipt_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
        receipt_ok = True
    else:
        cr = parse_receipt.get("replay_content_sha256")
        rr = parse_receipt.get("raw_parse_sha256")
        receipt_ok = (
            isinstance(cr, str)
            and isinstance(rhash, str)
            and cr.lower() == rhash.lower()
            and isinstance(rr, str)
            and rr.lower() == source_raw_parse_sha256.lower()
        )
        if not receipt_ok:
            reason_notes.append("parse receipt linkage failed")
        checks.append(
            TimelineCheckResult(
                check_id="parse_receipt_hash_match",
                detail=None if receipt_ok else "receipt hash mismatch",
                severity="required",
                status="pass" if receipt_ok else "fail",
            ),
        )

    if parse_report is None:
        checks.append(
            TimelineCheckResult(
                check_id="parse_report_status_parsed",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
        report_ok = True
    else:
        pr = parse_report.get("replay_content_sha256")
        st = parse_report.get("parse_status")
        report_ok = (
            isinstance(pr, str)
            and isinstance(rhash, str)
            and pr.lower() == rhash.lower()
            and st == "parsed"
        )
        if not report_ok:
            reason_notes.append("parse report linkage failed or parse_status not parsed")
        checks.append(
            TimelineCheckResult(
                check_id="parse_report_status_parsed",
                detail=None if report_ok else "parse report mismatch",
                severity="required",
                status="pass" if report_ok else "fail",
            ),
        )

    if metadata is None:
        checks.append(
            TimelineCheckResult(
                check_id="metadata_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
        meta_ok = True
    else:
        mh = metadata.get("source_raw_parse_sha256")
        mr = metadata.get("replay_content_sha256")
        meta_ok = (
            isinstance(mh, str)
            and mh.lower() == source_raw_parse_sha256.lower()
            and isinstance(mr, str)
            and isinstance(rhash, str)
            and mr.lower() == rhash.lower()
        )
        if not meta_ok:
            reason_notes.append("metadata linkage failed")
        checks.append(
            TimelineCheckResult(
                check_id="metadata_hash_match",
                detail=None if meta_ok else "metadata sha mismatch",
                severity="required",
                status="pass" if meta_ok else "fail",
            ),
        )

    if metadata_report is None:
        checks.append(
            TimelineCheckResult(
                check_id="metadata_report_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
        meta_rep_ok = True
    else:
        ms = metadata_report.get("source_raw_parse_sha256")
        meta_rep_ok = isinstance(ms, str) and ms.lower() == source_raw_parse_sha256.lower()
        if not meta_rep_ok:
            reason_notes.append("metadata report linkage failed")
        checks.append(
            TimelineCheckResult(
                check_id="metadata_report_hash_match",
                detail=None if meta_rep_ok else "metadata report sha mismatch",
                severity="required",
                status="pass" if meta_rep_ok else "fail",
            ),
        )

    streams = raw_parse.get("raw_event_streams")
    streams_present = isinstance(streams, dict) and any(
        isinstance(streams.get(k), list)
        for k in ("game_events", "message_events", "tracker_events")
    )
    checks.append(
        TimelineCheckResult(
            check_id="raw_event_streams_present",
            detail=None if streams_present else "no raw_event_streams lists (v1 or empty)",
            severity="warning",
            status="pass" if streams_present else "warn",
        ),
    )

    contract_failed = not schema_ok or not hash_ok or not receipt_ok or not report_ok
    contract_failed = contract_failed or not meta_ok or not meta_rep_ok

    if contract_failed:
        timeline: dict[str, Any] = {
            "entries": [],
            "event_streams_available": raw_parse.get("event_streams_available"),
            "merge_order_policy": MERGE_ORDER_POLICY,
            "replay_content_sha256": rhash if isinstance(rhash, str) else None,
            "schema_version": TIMELINE_SCHEMA_VERSION,
            "source_metadata_report_sha256": None,
            "source_metadata_sha256": None,
            "source_parse_receipt_sha256": None,
            "source_parse_report_sha256": None,
            "source_raw_parse_sha256": source_raw_parse_sha256,
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
        }
        checks.append(
            TimelineCheckResult(
                check_id="timeline_emitted",
                detail="empty envelope due to contract failure",
                severity="required",
                status="fail",
            ),
        )
        ordered = finalize_timeline_checks(checks)
        report_out: dict[str, Any] = {
            "advisory_notes": sorted(set(reason_notes)),
            "check_results": [c.to_mapping() for c in ordered],
            "counts_by_semantic_kind": {},
            "counts_by_stream": {},
            "extraction_status": "failed",
            "reason_codes": ["source_contract_failed"],
            "schema_version": TIMELINE_REPORT_SCHEMA_VERSION,
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
            "unsupported_event_names": [],
            "warnings": [],
        }
        return "source_contract_failed", timeline, report_out

    timeline, report_body = extract_timeline_envelope(
        raw_parse=raw_parse,
        source_metadata_report_sha256=sha256_hex_of_canonical_json(metadata_report)
        if metadata_report is not None
        else None,
        source_metadata_sha256=sha256_hex_of_canonical_json(metadata)
        if metadata is not None
        else None,
        source_parse_receipt_sha256=sha256_hex_of_canonical_json(parse_receipt)
        if parse_receipt is not None
        else None,
        source_parse_report_sha256=sha256_hex_of_canonical_json(parse_report)
        if parse_report is not None
        else None,
        source_raw_parse_sha256=source_raw_parse_sha256,
    )

    checks.append(
        TimelineCheckResult(
            check_id="timeline_emitted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )
    ordered = finalize_timeline_checks(checks)
    report_out = {
        **report_body,
        "advisory_notes": sorted(set(reason_notes)),
        "check_results": [c.to_mapping() for c in ordered],
        "reason_codes": [],
    }
    return "completed", timeline, report_out


def write_timeline_artifacts(
    *,
    output_dir: Path,
    timeline: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tp = output_dir / "replay_timeline.json"
    rp = output_dir / "replay_timeline_report.json"
    tp.write_text(canonical_json_dumps(timeline), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return tp, rp


def extract_timeline_from_paths(
    *,
    raw_parse_path: Path,
    output_dir: Path,
    parse_receipt_path: Path | None,
    parse_report_path: Path | None,
    metadata_path: Path | None,
    metadata_report_path: Path | None,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    raw, err = load_json_object(raw_parse_path)
    if raw is None:
        timeline = {
            "entries": [],
            "schema_version": TIMELINE_SCHEMA_VERSION,
            "source_raw_parse_sha256": "",
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
        }
        report: dict[str, Any] = {
            "advisory_notes": [f"failed to load raw parse: {err}"],
            "check_results": [],
            "extraction_status": "failed",
            "reason_codes": ["raw_parse_load_failed"],
            "schema_version": TIMELINE_REPORT_SCHEMA_VERSION,
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
        }
        report["check_results"] = [
            c.to_mapping()
            for c in finalize_timeline_checks(
                [
                    TimelineCheckResult(
                        check_id="raw_parse_schema_valid",
                        detail=str(err),
                        severity="required",
                        status="fail",
                    ),
                ],
            )
        ]
        write_timeline_artifacts(output_dir=output_dir, report=report, timeline=timeline)
        return "extraction_failed", timeline, report

    source_sha = sha256_hex_of_canonical_json(raw)

    def _load_opt(p: Path | None) -> dict[str, Any] | None:
        if p is None:
            return None
        d, e = load_json_object(p)
        if e is not None:
            raise ValueError(e)
        return d

    try:
        receipt = _load_opt(parse_receipt_path)
        report_parse = _load_opt(parse_report_path)
        meta = _load_opt(metadata_path)
        meta_rep = _load_opt(metadata_report_path)
    except ValueError as exc:
        timeline = {
            "entries": [],
            "schema_version": TIMELINE_SCHEMA_VERSION,
            "source_raw_parse_sha256": source_sha,
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
        }
        rep: dict[str, Any] = {
            "advisory_notes": [str(exc)],
            "check_results": [],
            "extraction_status": "failed",
            "reason_codes": ["lineage_load_failed"],
            "schema_version": TIMELINE_REPORT_SCHEMA_VERSION,
            "timeline_contract_version": TIMELINE_CONTRACT_VERSION,
            "timeline_profile": TIMELINE_PROFILE,
        }
        rep["check_results"] = [
            c.to_mapping()
            for c in finalize_timeline_checks(
                [
                    TimelineCheckResult(
                        check_id="parse_receipt_hash_match",
                        detail=str(exc),
                        severity="required",
                        status="fail",
                    ),
                ],
            )
        ]
        write_timeline_artifacts(output_dir=output_dir, report=rep, timeline=timeline)
        return "extraction_failed", timeline, rep

    status, timeline, report_out = run_timeline_extraction(
        metadata=meta,
        metadata_report=meta_rep,
        parse_receipt=receipt,
        parse_report=report_parse,
        raw_parse=raw,
        source_raw_parse_sha256=source_sha,
    )
    write_timeline_artifacts(output_dir=output_dir, report=report_out, timeline=timeline)
    return status, timeline, report_out
